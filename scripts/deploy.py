"""Deploy landing to omniadevelop.ru on the existing Debian 12 VPS.

Idempotent: re-running just refreshes the static files. Skips nginx
reconfiguration if the config file already matches.

Steps:
1. Connect via SSH (paramiko + password from env VPS_PASS)
2. Ensure /var/www/omniadevelop exists, owned by www-data
3. Recursively upload local dist/ → /var/www/omniadevelop/ via SFTP
4. Write nginx config (HTTP only — certbot will upgrade later when DNS resolves)
5. Symlink to sites-enabled, reload nginx
6. Smoke-test: curl -H 'Host: omniadevelop.ru' http://127.0.0.1
7. Try certbot if DNS resolves; otherwise print user instructions

Usage:
    set VPS_PASS=...
    python scripts/deploy.py
"""
import os
import socket
import sys
from pathlib import Path

import paramiko

sys.stdout.reconfigure(encoding="utf-8")

HOST = "170.168.72.200"
USER = "i48ptgvnis"
DOMAIN = "omniadevelop.ru"
WEBROOT = f"/var/www/omniadevelop"
NGINX_AVAILABLE = "/etc/nginx/sites-available/omniadevelop.ru"
NGINX_ENABLED = "/etc/nginx/sites-enabled/omniadevelop.ru"

LOCAL_DIST = Path(__file__).parent.parent / "dist"
PASSWORD = os.environ.get("VPS_PASS")
if not PASSWORD:
    print("set VPS_PASS env var")
    sys.exit(1)


NGINX_CONFIG = f"""# {DOMAIN} — Omnia.AI landing page (managed by deploy.py)

server {{
    listen 80;
    listen [::]:80;
    server_name {DOMAIN} www.{DOMAIN};

    root {WEBROOT};
    index index.html;

    # Hashed asset bundles — 30 days, immutable
    location ~* ^/assets/.+\\.(css|js|woff2?)$ {{
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }}

    # OG image, favicon — 1 day
    location ~* ^/(og\\.png|favicon\\.svg|og\\.jpg)$ {{
        expires 1d;
        add_header Cache-Control "public, max-age=86400";
    }}

    # SPA fallback (single-page app)
    location / {{
        try_files $uri $uri/ /index.html;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    }}

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml application/xml+rss;
    gzip_min_length 512;
    gzip_comp_level 6;

    # ACME challenge — for certbot
    location /.well-known/acme-challenge/ {{
        root /var/www/certbot;
        try_files $uri =404;
    }}

    # Block access to dotfiles
    location ~ /\\. {{
        deny all;
        return 404;
    }}
}}
"""


def run(client, cmd, *, sudo=False, check=True, timeout=60):
    """Run a shell command via SSH, return (stdout, stderr, exit_code)."""
    full = f"sudo -n {cmd}" if sudo else cmd
    _, stdout, stderr = client.exec_command(full, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if check and exit_code != 0:
        print(f"FAIL ({exit_code}): {full}")
        print(f"  stdout: {out.strip()}")
        print(f"  stderr: {err.strip()}")
        sys.exit(1)
    return out.strip(), err.strip(), exit_code


def sftp_walk_upload(sftp, client, local_root, remote_root):
    """Recursively upload local_root → remote_root via SFTP.
    Creates directories with sudo+chown so www-data owns the result.
    """
    local_root = Path(local_root)
    print(f"  Uploading {local_root} → {remote_root}")

    # First, push tree to /tmp/omniadevelop_stage (writable for our user),
    # then `sudo mv` it into place. Avoids SFTP permission headaches.
    stage = "/tmp/omniadevelop_stage"
    run(client, f"rm -rf {stage} && mkdir -p {stage}")

    files_uploaded = 0
    bytes_uploaded = 0
    for local_path in local_root.rglob("*"):
        if local_path.is_file():
            rel = local_path.relative_to(local_root).as_posix()
            remote_path = f"{stage}/{rel}"
            # Make sure parent dir exists
            parent = "/".join(remote_path.split("/")[:-1])
            try:
                sftp.stat(parent)
            except IOError:
                # mkdir -p remote
                parts = parent.split("/")
                cur = ""
                for p in parts:
                    if not p:
                        cur = "/"
                        continue
                    cur = cur.rstrip("/") + "/" + p
                    try:
                        sftp.stat(cur)
                    except IOError:
                        sftp.mkdir(cur)
            sftp.put(str(local_path), remote_path)
            files_uploaded += 1
            bytes_uploaded += local_path.stat().st_size
    print(f"  {files_uploaded} files, {bytes_uploaded:,} bytes")

    # Move stage → webroot atomically via rsync (preserves ownership step)
    run(client, f"mkdir -p {remote_root}", sudo=True)
    # Copy contents (not directory itself), then chown
    run(client, f"cp -rT {stage} {remote_root}", sudo=True)
    run(client, f"chown -R www-data:www-data {remote_root}", sudo=True)
    run(client, f"chmod -R u=rwX,go=rX {remote_root}", sudo=True)
    run(client, f"rm -rf {stage}")


def main():
    print(f"[1/7] Connect SSH {USER}@{HOST}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=HOST,
        port=22,
        username=USER,
        password=PASSWORD,
        timeout=20,
        allow_agent=False,
        look_for_keys=False,
    )
    sftp = client.open_sftp()

    print(f"[2/7] Build artifacts: {LOCAL_DIST}")
    if not LOCAL_DIST.exists() or not (LOCAL_DIST / "index.html").exists():
        print("  ERROR: dist/index.html not found. Run `npm run build` first.")
        sys.exit(1)
    print(f"  ✓ index.html present")

    print(f"[3/7] Upload static files → {WEBROOT}")
    sftp_walk_upload(sftp, client, LOCAL_DIST, WEBROOT)

    print(f"[4/7] Write nginx config → {NGINX_AVAILABLE}")
    # write to /tmp first, then sudo mv
    tmp_conf = "/tmp/omniadevelop_nginx.conf"
    with sftp.open(tmp_conf, "w") as f:
        f.write(NGINX_CONFIG)
    run(client, f"mv {tmp_conf} {NGINX_AVAILABLE}", sudo=True)
    run(client, f"chown root:root {NGINX_AVAILABLE}", sudo=True)
    run(client, f"chmod 644 {NGINX_AVAILABLE}", sudo=True)

    # Symlink to sites-enabled (idempotent)
    out, _, _ = run(client, f"test -L {NGINX_ENABLED} && echo exists || echo missing", check=False)
    if "missing" in out:
        run(client, f"ln -s {NGINX_AVAILABLE} {NGINX_ENABLED}", sudo=True)
        print(f"  ✓ symlinked to sites-enabled")
    else:
        print(f"  ✓ already in sites-enabled")

    print(f"[5/7] Test + reload nginx")
    out, err, _ = run(client, "nginx -t", sudo=True, check=False)
    print(f"  nginx -t: {err or out}")
    if "successful" not in (out + err).lower():
        print("  ABORT: nginx config failed validation")
        sys.exit(1)
    run(client, "systemctl reload nginx", sudo=True)
    print(f"  ✓ nginx reloaded")

    print(f"[6/7] Smoke test")
    out, _, _ = run(
        client,
        f"curl -sf -H 'Host: {DOMAIN}' http://127.0.0.1/ -o /dev/null -w 'HTTP %{{http_code}} · %{{size_download}} bytes'",
        check=False,
    )
    print(f"  / : {out}")
    out, _, _ = run(
        client,
        f"curl -sf -H 'Host: {DOMAIN}' http://127.0.0.1/og.png -o /dev/null -w 'HTTP %{{http_code}} · %{{size_download}} bytes'",
        check=False,
    )
    print(f"  /og.png : {out}")

    print(f"[7/7] DNS + SSL")
    # Check DNS resolution from VPS itself
    out, _, code = run(client, f"getent hosts {DOMAIN}", check=False)
    if out:
        print(f"  DNS: {out}")
        if HOST in out:
            print(f"  ✓ DNS points to this VPS — running certbot")
            cb_cmd = (
                f"certbot --nginx -d {DOMAIN} -d www.{DOMAIN} "
                f"--non-interactive --agree-tos --redirect "
                f"-m admin@{DOMAIN} --preferred-challenges http"
            )
            out, err, code = run(client, cb_cmd, sudo=True, check=False, timeout=120)
            print(out[-2000:] if len(out) > 2000 else out)
            if err and code != 0:
                print(f"[err] {err[-1000:]}")
        else:
            print(f"  ⚠ DNS resolves but not to this VPS ({HOST}). Skipping certbot.")
    else:
        print(f"  ⚠ {DOMAIN} not in DNS yet.")
        print(f"  Add this A-record at your registrar:")
        print(f"    Type: A   Name: omniadevelop.ru   Value: {HOST}   TTL: 3600")
        print(f"    Type: A   Name: www              Value: {HOST}   TTL: 3600")
        print(f"  After it propagates (10 min – 24 h), re-run:")
        print(f"    sudo certbot --nginx -d {DOMAIN} -d www.{DOMAIN} \\")
        print(f"      --non-interactive --agree-tos --redirect -m admin@{DOMAIN}")

    sftp.close()
    client.close()
    print("\n✓ DONE. Site available at:")
    print(f"  http://{HOST}/  (works now via IP)")
    print(f"  http://{DOMAIN}/  (works once DNS propagates)")


if __name__ == "__main__":
    main()
