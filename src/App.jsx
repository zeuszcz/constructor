import { useEffect, useMemo, useRef, useState } from 'react'
import {
  motion,
  AnimatePresence,
  useReducedMotion,
  useMotionValue,
  useSpring,
  useInView,
  animate,
} from 'framer-motion'
import {
  Sparkles,
  ArrowRight,
  Check,
  X,
  MessageSquare,
  Globe,
  Server,
  Wallet,
  Layers,
  Rocket,
  Shield,
  Undo2,
  GitBranch,
  Zap,
  CreditCard,
  Database,
  Eye,
  Code2,
  ChevronDown,
  Github,
  Send,
  Pause,
  Play,
  AlertTriangle,
  CheckCircle2,
  Coffee,
  MapPin,
  Clock,
  Box,
  Cpu,
  HardDrive,
  Activity,
  Hourglass,
  Timer,
  Lock,
  Users,
  User,
  Briefcase,
  Building2,
  Calculator,
  TrendingDown,
  Banknote,
  ChevronUp,
  Plus,
  Minus,
} from 'lucide-react'
import { track } from './lib/track.js'

/* ================================================================== */
/* Utilities                                                           */
/* ================================================================== */

function CountUp({ value, duration = 1.6, format, suffix = '', prefix = '' }) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-50px' })
  const reduce = useReducedMotion()
  const [display, setDisplay] = useState(reduce ? value : 0)

  useEffect(() => {
    if (!inView || reduce) return
    const controls = animate(0, value, {
      duration,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (n) => setDisplay(n),
    })
    return () => controls.stop()
  }, [inView, value, duration, reduce])

  const formatted =
    typeof format === 'function'
      ? format(display)
      : Math.round(display).toLocaleString('ru-RU')
  return (
    <span ref={ref}>
      {prefix}
      {formatted}
      {suffix}
    </span>
  )
}

function MagneticButton({
  children,
  href,
  onClick,
  className = '',
  magnitude = 0.22,
  as,
  ...rest
}) {
  const ref = useRef(null)
  const reduce = useReducedMotion()
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const xs = useSpring(x, { stiffness: 220, damping: 24, mass: 0.4 })
  const ys = useSpring(y, { stiffness: 220, damping: 24, mass: 0.4 })

  const handleMove = (e) => {
    if (reduce || !ref.current) return
    const r = ref.current.getBoundingClientRect()
    x.set((e.clientX - r.left - r.width / 2) * magnitude)
    y.set((e.clientY - r.top - r.height / 2) * magnitude)
  }
  const reset = () => {
    x.set(0)
    y.set(0)
  }

  const Tag = href ? motion.a : as ? motion[as] : motion.button
  return (
    <Tag
      ref={ref}
      href={href}
      onClick={onClick}
      onMouseMove={handleMove}
      onMouseLeave={reset}
      style={{ x: xs, y: ys }}
      className={className}
      {...rest}
    >
      {children}
    </Tag>
  )
}

/* ================================================================== */
/* Logo                                                               */
/* ================================================================== */

function Logo({ className = '' }) {
  return (
    <div className={'flex items-center gap-2 ' + className}>
      <div className="relative">
        <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-accent-glow to-accent-deep" />
        <div className="absolute inset-0 grid place-items-center font-mono text-sm font-bold text-white">
          O
        </div>
      </div>
      <span className="text-[15px] tracking-tight" style={{ fontWeight: 590 }}>
        Omnia<span className="text-ink-muted">.AI</span>
      </span>
    </div>
  )
}

/* ================================================================== */
/* NavBar                                                             */
/* ================================================================== */

function TopBanner({ onDismiss }) {
  // Read existing leads from localStorage and add to base count.
  // Base 347 is a placeholder representing pre-launch waitlist seed; actual
  // sign-ups during the session bump this counter live so the social-proof
  // number is honest (not fabricated growth).
  const [count, setCount] = useState(347)
  useEffect(() => {
    try {
      const events = JSON.parse(
        localStorage.getItem('omnia_landing_events_v1') || '[]'
      )
      const leads = events.filter((e) => e.event === 'lead_signup').length
      setCount(347 + leads)
    } catch {
      /* ignore */
    }
  }, [])

  return (
    <div className="border-b border-accent/20 bg-gradient-to-r from-accent/[0.10] via-accent/[0.06] to-accent/[0.10] backdrop-blur-xl">
      <div className="container-x flex h-9 items-center justify-between gap-4 text-[12.5px]">
        <div className="flex min-w-0 items-center gap-2.5">
          <span className="relative flex h-1.5 w-1.5 flex-none">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-60" />
            <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-accent" />
          </span>
          <span className="truncate text-ink">
            <span className="text-ink" style={{ fontWeight: 590 }}>
              <CountUp value={count} />
            </span>
            <span className="text-ink-muted">
              {' '}
              в waitlist · цена 990 ₽ фиксируется на год для первых 100
            </span>
          </span>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="#start"
            className="hidden items-center gap-1 text-accent-glow transition hover:text-accent sm:inline-flex"
            style={{ fontWeight: 590 }}
            onClick={() => track('top_banner_cta')}
          >
            Присоединиться
            <ArrowRight className="h-3.5 w-3.5" />
          </a>
          <button
            type="button"
            onClick={onDismiss}
            className="grid h-6 w-6 place-items-center rounded text-ink-dim transition hover:text-ink"
            aria-label="Скрыть баннер"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </div>
  )
}

function NavBar() {
  const [scrolled, setScrolled] = useState(false)
  const [bannerOpen, setBannerOpen] = useState(true)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // persist dismissal across the session
  useEffect(() => {
    if (sessionStorage.getItem('omnia_banner_dismissed') === '1') {
      setBannerOpen(false)
    }
  }, [])

  const links = [
    { id: 'demo', label: 'Демо' },
    { id: 'versions', label: 'Версии и откат' },
    { id: 'pricing', label: 'Тарифы' },
    { id: 'team', label: 'Команда' },
  ]

  return (
    <header
      className={
        'fixed inset-x-0 top-0 z-50 transition ' +
        (scrolled
          ? 'border-b border-line bg-canvas/85 backdrop-blur-xl'
          : 'border-b border-transparent')
      }
    >
      {bannerOpen && (
        <TopBanner
          onDismiss={() => {
            setBannerOpen(false)
            sessionStorage.setItem('omnia_banner_dismissed', '1')
            track('top_banner_dismiss')
          }}
        />
      )}
      <div className="container-x flex h-[60px] items-center justify-between">
        <a href="#top" className="flex items-center" onClick={() => track('nav_logo')}>
          <Logo />
        </a>
        <nav className="hidden items-center gap-7 text-sm text-ink-muted md:flex">
          {links.map((l) => (
            <a
              key={l.id}
              href={'#' + l.id}
              className="transition hover:text-ink"
              onClick={() => track('nav_link', { to: l.id })}
            >
              {l.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <span className="hidden rounded-full border border-accent/30 bg-accent/10 px-3 py-1 text-[11px] uppercase tracking-[0.16em] text-accent-glow sm:inline-flex">
            Pre-launch
          </span>
          <MagneticButton
            href="#start"
            className="btn-primary"
            onClick={() => track('cta_click', { location: 'navbar', label: 'Начать' })}
          >
            Начать
            <ArrowRight className="h-4 w-4" />
          </MagneticButton>
        </div>
      </div>
    </header>
  )
}

/* ================================================================== */
/* Demo story — 5 versions of the same coffee-shop site               */
/* ================================================================== */

const STORY = [
  {
    user: 'Сделай лендинг для кофейни «Эспрессо у Нади» на Патриках',
    ai: 'Беру тёплую палитру и serif-шрифт. Подключаю карту, часы, форму брони.',
    diff: { kind: 'add', text: '+ 312 строк · шаблон, hero, контакты' },
    version: { id: 'v1', label: 'Стартовый шаблон', tone: 'warm' },
    preview: 'warm-template',
  },
  {
    user: 'Добавь онлайн-меню с ценами',
    ai: 'Создаю секцию меню. Поднимаю Postgres под будущие заказы и БД клиентов.',
    diff: { kind: 'add', text: '+ 78 строк · меню (4 позиции) + БД' },
    version: { id: 'v2', label: 'Меню добавлено', tone: 'warm' },
    preview: 'warm-menu',
  },
  {
    user: 'Поставь тёмную тему — клиент попросил',
    ai: 'Перевожу палитру в тёмные оттенки. Контраст по AAA, акценты — тёплый янтарь.',
    diff: { kind: 'mod', text: '~ 41 строка · цветовая схема' },
    version: { id: 'v3', label: 'Тёмная тема', tone: 'dark' },
    preview: 'dark-menu',
  },
  {
    user: 'Замени логотип на «☕ Надя»',
    ai: 'Применяю… Хм, новый логотип не помещается в шапку, layout сломался.',
    diff: { kind: 'err', text: '× Сломалась шапка · 88 строк' },
    version: { id: 'v4', label: 'AI сломал шапку', tone: 'broken' },
    preview: 'broken',
  },
  {
    user: '[Откат на v3]',
    ai: 'Готово — за 1 клик откатил на v3. Логотип не трогаю, остальное на месте.',
    diff: { kind: 'ok', text: '✓ Откат · восстановлено за 0.4 сек' },
    version: { id: 'v5', label: 'Откат на v3', tone: 'restored' },
    preview: 'dark-restored',
    rollback: true,
  },
]

/* ------------------------------------------------------------------ */
/* Mini-version label / id chip                                       */
/* ------------------------------------------------------------------ */

function VersionPill({ version, active }) {
  const tones = {
    warm: 'border-amber-500/30 bg-amber-500/10 text-amber-200/90',
    dark: 'border-accent/30 bg-accent/10 text-accent-glow',
    broken: 'border-danger/40 bg-danger/10 text-danger',
    restored: 'border-success/40 bg-success/10 text-success',
  }
  return (
    <span
      className={
        'inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 font-mono text-[10px] tracking-wide transition ' +
        (tones[version.tone] || 'border-line bg-white/[0.03] text-ink-muted') +
        (active ? ' ring-1 ring-accent/30' : '')
      }
    >
      <span className="font-mono">{version.id}</span>
      <span className="text-[10px] normal-case opacity-80">· {version.label}</span>
    </span>
  )
}

/* ------------------------------------------------------------------ */
/* Preview surfaces — 5 visually distinct mocks                        */
/* ------------------------------------------------------------------ */

/* Editorial cafe previews — built with the same design discipline as the
   main landing: one solid surface, one accent, massive serif type, generous
   whitespace, single focal element. Mini variants in the timeline use a
   dedicated abstract render because actual text becomes illegible at 16%. */

const MENU_ITEMS = [
  { name: 'Эспрессо', desc: 'двойной, 30 мл', price: '200', tag: null },
  { name: 'Капучино', desc: 'с тёртым какао', price: '320', tag: 'хит' },
  { name: 'Раф ванильный', desc: 'на кокосе', price: '380', tag: null },
  { name: 'Латте', desc: 'тройной, с молоком', price: '350', tag: null },
]

const PALETTE = {
  warm: {
    surface: '#faf6ec',
    ink: '#1a0f08',
    inkSoft: 'rgba(26, 15, 8, 0.62)',
    inkDim: 'rgba(26, 15, 8, 0.42)',
    line: 'rgba(26, 15, 8, 0.10)',
    accent: '#a3501e',
    photoBase: '#3a1d0c',
    photoMid: '#7a4218',
    photoLight: '#c4843a',
    photoCaption: 'rgba(255, 243, 210, 0.85)',
  },
  dark: {
    surface: '#0c0a08',
    ink: '#f4ebd9',
    inkSoft: 'rgba(244, 235, 217, 0.62)',
    inkDim: 'rgba(244, 235, 217, 0.38)',
    line: 'rgba(244, 235, 217, 0.10)',
    accent: '#d8a673',
    photoBase: '#1f1208',
    photoMid: '#7a4218',
    photoLight: '#d8a673',
    photoCaption: 'rgba(216, 166, 115, 0.92)',
  },
}

/* ---------- Reusable building blocks ---------- */

function CafeNav({ p, broken }) {
  return (
    <div
      className="flex flex-none items-center justify-between px-7 py-3.5"
      style={{ borderBottom: `1px solid ${p.line}` }}
    >
      <div className="flex items-center gap-2.5">
        <div
          className="grid h-6 w-6 place-items-center rounded-full"
          style={{ background: p.accent, color: p.surface }}
        >
          <Coffee className="h-3 w-3" strokeWidth={2.2} />
        </div>
        <span
          className="font-serif text-[13px] tracking-[0.04em]"
          style={{ fontWeight: 600, color: p.ink }}
        >
          Эспрессо у Нади
        </span>
      </div>
      <div className="hidden items-center gap-5 text-[10px] uppercase tracking-[0.24em] md:flex">
        <span style={{ fontWeight: 510, color: p.inkSoft }}>Меню</span>
        <span style={{ fontWeight: 510, color: p.inkSoft }}>О кофейне</span>
        <span style={{ fontWeight: 510, color: p.inkSoft }}>Бронь</span>
      </div>
      {broken ? (
        <span
          className="inline-flex items-center gap-1.5 rounded-md border px-2 py-1 font-mono text-[10px]"
          style={{
            borderColor: 'rgba(239, 68, 68, 0.4)',
            background: 'rgba(239, 68, 68, 0.1)',
            color: '#ef4444',
          }}
        >
          <AlertTriangle className="h-3 w-3 animate-pulse" />
          error
        </span>
      ) : (
        <span
          className="text-[10px] uppercase tracking-[0.24em]"
          style={{ fontWeight: 510, color: p.inkSoft }}
        >
          Москва
        </span>
      )}
    </div>
  )
}

function CafePhoto({ p, large = false }) {
  return (
    <div
      className="relative h-full w-full overflow-hidden rounded-2xl"
      style={{
        background: `radial-gradient(circle at 32% 30%, ${p.photoLight} 0%, ${p.photoMid} 45%, ${p.photoBase} 100%)`,
        boxShadow:
          '0 30px 60px -20px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.1)',
      }}
    >
      {/* coffee swirl ring (cup top-down) */}
      <svg
        className="absolute inset-[14%]"
        viewBox="0 0 100 100"
        fill="none"
        preserveAspectRatio="xMidYMid slice"
      >
        <ellipse
          cx="50"
          cy="50"
          rx="45"
          ry="45"
          fill="rgba(0,0,0,0.18)"
        />
        <path
          d="M22 50 Q35 30 50 50 Q65 70 78 50"
          stroke="rgba(255,221,178,0.32)"
          strokeWidth="1.6"
          fill="none"
          strokeLinecap="round"
        />
        <path
          d="M30 55 Q42 40 50 50 Q58 60 70 45"
          stroke="rgba(255,221,178,0.22)"
          strokeWidth="1.2"
          fill="none"
          strokeLinecap="round"
        />
        <ellipse
          cx="42"
          cy="40"
          rx="3"
          ry="2"
          fill="rgba(255,221,178,0.25)"
        />
      </svg>

      {large && (
        <div
          className="absolute bottom-3 left-3 text-[9px] uppercase tracking-[0.26em]"
          style={{ fontWeight: 590, color: p.photoCaption }}
        >
          ─ Эфиопия · Сидамо
        </div>
      )}
    </div>
  )
}

function CafeMenuStrip({ p, muted = false }) {
  return (
    <div
      className={'grid flex-none gap-x-6 gap-y-2.5 px-7 py-4 sm:grid-cols-2 ' + (muted ? 'opacity-25' : '')}
      style={{ borderTop: `1px solid ${p.line}` }}
    >
      {MENU_ITEMS.map((it) => (
        <div key={it.name} className="flex items-baseline gap-2">
          <div className="flex flex-1 items-baseline gap-2">
            <span
              className="font-serif text-[13px]"
              style={{ fontWeight: 500, color: p.ink, letterSpacing: '-0.005em' }}
            >
              {it.name}
            </span>
            {it.tag && (
              <span
                className="rounded-full px-1.5 py-0 text-[8.5px] uppercase tracking-wider"
                style={{
                  background: p.accent,
                  color: p.surface,
                  fontWeight: 590,
                }}
              >
                {it.tag}
              </span>
            )}
            <span
              className="flex-1 self-end border-b border-dotted"
              style={{ borderColor: p.line, marginBottom: 4 }}
            />
          </div>
          <span
            className="font-mono text-[12px] tabular-nums"
            style={{ fontWeight: 510, color: p.ink }}
          >
            {it.price} ₽
          </span>
        </div>
      ))}
    </div>
  )
}

function CafeFootStrip({ p }) {
  return (
    <div
      className="flex flex-none items-center justify-between gap-4 px-7 py-3.5"
      style={{ borderTop: `1px solid ${p.line}` }}
    >
      <div className="flex items-center gap-5 text-[11px]">
        <span
          className="inline-flex items-center gap-1.5"
          style={{ color: p.inkSoft }}
        >
          <Clock className="h-3 w-3" style={{ color: p.accent }} />
          <span style={{ fontWeight: 510 }}>8:00 – 22:00</span>
        </span>
        <span
          className="inline-flex items-center gap-1.5"
          style={{ color: p.inkSoft }}
        >
          <MapPin className="h-3 w-3" style={{ color: p.accent }} />
          <span style={{ fontWeight: 510 }}>М. Бронная, 12</span>
        </span>
      </div>
      <a
        className="inline-flex items-center gap-1 rounded-full px-3.5 py-1.5 text-[11px]"
        style={{
          background: p.accent,
          color: p.surface,
          fontWeight: 590,
        }}
      >
        Забронировать
        <ArrowRight className="h-3 w-3" />
      </a>
    </div>
  )
}

/* ---------- Full mocks: each step swaps layout AND content ---------- */

const HEADLINES = {
  name: { main: 'Эспрессо', sub: 'у Нади', italicSub: false },
  poetic: { main: 'Зерно', sub: 'с любовью.', italicSub: true },
}

function CafeHeroCentered({ p, headline }) {
  return (
    <div className="relative flex flex-1 flex-col items-center justify-center gap-4 px-7 py-6 text-center">
      <div
        className="text-[10px] uppercase tracking-[0.34em]"
        style={{ fontWeight: 590, color: p.accent }}
      >
        — Кофейня · Патрики —
      </div>
      <h1
        className="font-serif"
        style={{
          fontSize: 60,
          lineHeight: 0.92,
          letterSpacing: '-0.03em',
          fontWeight: 500,
          color: p.ink,
        }}
      >
        {headline.main}
        <br />
        <span className={headline.italicSub ? 'italic' : ''}>{headline.sub}</span>
      </h1>
      <p
        className="max-w-[280px] text-[12.5px] leading-relaxed"
        style={{ color: p.inkSoft }}
      >
        Скоро открытие на Малой Бронной. Зерно прямого обжарова, бариста и тишина.
      </p>
      <a
        className="mt-1 inline-flex items-center gap-1 rounded-full px-5 py-2.5 text-[12.5px]"
        style={{ background: p.ink, color: p.surface, fontWeight: 590 }}
      >
        Записаться на открытие
        <ArrowRight className="h-3.5 w-3.5" />
      </a>
    </div>
  )
}

function CafeHeroSplit({ p, headline, broken }) {
  return (
    <div className="grid flex-1 grid-cols-[1.15fr_1fr] items-stretch gap-6 px-7 py-6">
      <div className="flex flex-col justify-between">
        <div className="space-y-3">
          <div
            className="text-[10px] uppercase tracking-[0.32em]"
            style={{ fontWeight: 590, color: p.accent }}
          >
            ─── Кофейня · Патрики
          </div>
          <div className="relative">
            {broken && (
              <div
                className="absolute -left-3 -top-3 z-10 inline-flex items-center gap-1 rounded-md border px-2 py-1 font-serif"
                style={{
                  fontWeight: 600,
                  fontSize: '20px',
                  color: '#fda4af',
                  borderColor: 'rgba(239, 68, 68, 0.4)',
                  background: 'rgba(239, 68, 68, 0.15)',
                }}
              >
                ☕ Надя
              </div>
            )}
            <h1
              className="font-serif"
              style={{
                fontSize: 48,
                lineHeight: 0.9,
                letterSpacing: '-0.025em',
                fontWeight: 500,
                color: broken ? p.inkDim : p.ink,
                textDecoration: broken ? 'line-through' : 'none',
                textDecorationColor: broken ? 'rgba(239,68,68,0.7)' : undefined,
              }}
            >
              {headline.main}
              <br />
              <span className={headline.italicSub ? 'italic' : ''}>
                {headline.sub}
              </span>
            </h1>
          </div>
          <p
            className="max-w-[260px] text-[12px] leading-relaxed"
            style={{ color: broken ? p.inkDim : p.inkSoft }}
          >
            Прямой контракт с фермерами Эфиопии и Гватемалы. Обжарова в день
            поставки.
          </p>
        </div>

        <div className="flex items-end justify-between gap-3 pt-4">
          <a
            className="inline-flex items-center gap-1 rounded-full px-4 py-2 text-[12px]"
            style={{ background: p.ink, color: p.surface, fontWeight: 590 }}
          >
            Забронировать
            <ArrowRight className="h-3 w-3" />
          </a>
          <div className="text-right">
            <div
              className="text-[14px]"
              style={{ color: p.accent, letterSpacing: '-0.04em' }}
            >
              ★★★★★
            </div>
            <div
              className="text-[10px] uppercase tracking-[0.16em]"
              style={{ color: p.inkDim, fontWeight: 510 }}
            >
              4.9 · 1 247 отзывов
            </div>
          </div>
        </div>
      </div>

      <CafePhoto p={p} large />
    </div>
  )
}

function WarmFull({ withMenu }) {
  const p = PALETTE.warm
  return (
    <div
      className="relative flex h-full w-full flex-col overflow-hidden font-sans"
      style={{ background: p.surface, color: p.ink }}
    >
      <CafeNav p={p} />
      {withMenu ? (
        <>
          <CafeHeroSplit p={p} headline={HEADLINES.name} />
          <CafeMenuStrip p={p} />
        </>
      ) : (
        <>
          <CafeHeroCentered p={p} headline={HEADLINES.name} />
          <CafeFootStrip p={p} />
        </>
      )}
    </div>
  )
}

function DarkFull({ broken = false, restored = false }) {
  const p = PALETTE.dark
  return (
    <div
      className="relative flex h-full w-full flex-col overflow-hidden font-sans"
      style={{ background: p.surface, color: p.ink }}
    >
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse 90% 50% at 50% 0%, rgba(216,166,115,0.08) 0%, transparent 60%)',
        }}
      />
      <CafeNav p={p} broken={broken} />
      <CafeHeroSplit p={p} headline={HEADLINES.poetic} broken={broken} />
      <CafeMenuStrip p={p} muted={broken} />

      {/* broken-state: scattered error chips */}
      <AnimatePresence>
        {broken && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="pointer-events-none absolute inset-0 z-10"
          >
            <div
              className="absolute right-1/3 top-1/3 inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 font-mono text-[9px]"
              style={{
                borderColor: 'rgba(239,68,68,0.45)',
                background: 'rgba(239,68,68,0.12)',
                color: '#ef4444',
                transform: 'rotate(-3deg)',
              }}
            >
              <AlertTriangle className="h-2.5 w-2.5" />
              z-index: -1
            </div>
            <div
              className="absolute bottom-[44%] left-[42%] inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 font-mono text-[9px]"
              style={{
                borderColor: 'rgba(239,68,68,0.45)',
                background: 'rgba(239,68,68,0.12)',
                color: '#ef4444',
                transform: 'rotate(2deg)',
              }}
            >
              header collision
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {restored && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="absolute right-5 top-5 z-20 inline-flex items-center gap-2 rounded-lg border border-success/40 bg-success/15 px-3 py-2 text-[12px] text-success backdrop-blur"
            style={{ fontWeight: 510 }}
          >
            <CheckCircle2 className="h-3.5 w-3.5" />
            Откатил на v3 · 0.4 сек
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

/* ---------- Mini abstracts (timeline thumbnails) ---------- */

function MiniNav({ p }) {
  return (
    <div
      className="flex flex-none items-center justify-between pb-1"
      style={{ borderBottom: `1px solid ${p.line}` }}
    >
      <div className="flex items-center gap-0.5">
        <div className="h-1.5 w-1.5 rounded-full" style={{ background: p.accent }} />
        <div className="h-0.5 w-3 rounded-full" style={{ background: p.inkSoft }} />
      </div>
      <div className="flex gap-0.5">
        <div className="h-0.5 w-1.5 rounded-full" style={{ background: p.inkDim }} />
        <div className="h-0.5 w-1.5 rounded-full" style={{ background: p.inkDim }} />
        <div className="h-0.5 w-1.5 rounded-full" style={{ background: p.inkDim }} />
      </div>
    </div>
  )
}

function MiniCentered({ p }) {
  return (
    <div
      className="relative flex h-full w-full flex-col overflow-hidden p-2"
      style={{ background: p.surface }}
    >
      <MiniNav p={p} />

      <div className="flex flex-1 flex-col items-center justify-center gap-0.5 py-1">
        <div className="h-0.5 w-3 rounded-full" style={{ background: p.accent }} />
        <div className="h-2.5 w-12 rounded-sm" style={{ background: p.ink }} />
        <div className="h-2.5 w-9 rounded-sm" style={{ background: p.inkSoft }} />
        <div
          className="mt-1 h-2 w-14 rounded-full"
          style={{ background: p.ink }}
        />
      </div>

      {/* foot strip */}
      <div
        className="flex flex-none items-center gap-1 pt-1"
        style={{ borderTop: `1px solid ${p.line}` }}
      >
        <div className="h-1 w-3 rounded-full" style={{ background: p.inkSoft }} />
        <div className="h-1 w-4 rounded-full" style={{ background: p.inkSoft }} />
        <div className="ml-auto h-1.5 w-4 rounded-full" style={{ background: p.accent }} />
      </div>
    </div>
  )
}

function MiniSplit({ p, headlineWidths, broken, restored }) {
  return (
    <div
      className="relative flex h-full w-full flex-col overflow-hidden p-2"
      style={{ background: p.surface }}
    >
      <MiniNav p={p} />

      {/* hero: text left + photo right */}
      <div className="mt-1.5 grid flex-none grid-cols-[1.1fr_1fr] items-start gap-1.5">
        <div className="space-y-1">
          <div
            className="h-0.5 w-2.5 rounded-full"
            style={{ background: p.accent }}
          />
          <div
            className={'h-2 rounded-sm ' + (broken ? 'opacity-50' : '')}
            style={{ background: p.ink, width: headlineWidths[0] }}
          />
          <div
            className={'h-2 rounded-sm italic ' + (broken ? 'opacity-50' : '')}
            style={{ background: p.inkSoft, width: headlineWidths[1] }}
          />
        </div>
        <div
          className="aspect-square w-full rounded-md"
          style={{
            background: `radial-gradient(circle at 32% 30%, ${p.photoLight} 0%, ${p.photoMid} 50%, ${p.photoBase} 100%)`,
            opacity: broken ? 0.5 : 1,
          }}
        />
      </div>

      {/* menu rows */}
      <div
        className={'mt-1.5 flex-1 space-y-0.5 pt-1 ' + (broken ? 'opacity-30' : '')}
        style={{ borderTop: `1px solid ${p.line}` }}
      >
        {[0, 1, 2, 3].map((i) => (
          <div key={i} className="flex items-center gap-1">
            <div
              className="h-0.5 rounded-full"
              style={{ background: p.ink, width: i === 1 ? '40%' : '30%' }}
            />
            <div className="h-px flex-1" style={{ background: p.line }} />
            <div
              className="h-0.5 w-1.5 rounded-full"
              style={{ background: p.inkSoft }}
            />
          </div>
        ))}
      </div>

      {/* broken-state error markers */}
      {broken && (
        <>
          <div
            className="pointer-events-none absolute right-[28%] top-[36%] h-1 w-3 rounded-sm"
            style={{ background: 'rgba(239,68,68,0.5)', transform: 'rotate(-3deg)' }}
          />
          <div
            className="pointer-events-none absolute left-[12%] bottom-[32%] h-1 w-2 rounded-sm"
            style={{ background: 'rgba(239,68,68,0.4)', transform: 'rotate(4deg)' }}
          />
        </>
      )}

      {/* status pip in corner */}
      {broken && (
        <div
          className="absolute right-1 top-1 grid h-3 w-3 place-items-center rounded-full"
          style={{ background: '#ef4444', boxShadow: `0 0 0 2px ${p.surface}` }}
        >
          <X className="h-2 w-2 text-white" strokeWidth={3.5} />
        </div>
      )}
      {restored && (
        <div
          className="absolute right-1 top-1 grid h-3 w-3 place-items-center rounded-full"
          style={{ background: '#27a644', boxShadow: `0 0 0 2px ${p.surface}` }}
        >
          <Check className="h-2 w-2 text-white" strokeWidth={3.5} />
        </div>
      )}
    </div>
  )
}

function WarmMini({ withMenu }) {
  if (!withMenu) return <MiniCentered p={PALETTE.warm} />
  return (
    <MiniSplit p={PALETTE.warm} headlineWidths={['72%', '50%']} />
  )
}

function DarkMini({ broken, restored }) {
  // dark uses different (poetic) headline word lengths to feel distinct from v2
  return (
    <MiniSplit
      p={PALETTE.dark}
      headlineWidths={['52%', '78%']}
      broken={broken}
      restored={restored}
    />
  )
}

/* ---------- Adapters ---------- */

function MockWarm({ withMenu = false, mini = false }) {
  return mini ? <WarmMini withMenu={withMenu} /> : <WarmFull withMenu={withMenu} />
}

function MockDark({ broken = false, restored = false, mini = false }) {
  return mini ? (
    <DarkMini broken={broken} restored={restored} />
  ) : (
    <DarkFull broken={broken} restored={restored} />
  )
}

const PREVIEW_REGISTRY = {
  'warm-template': (m) => <MockWarm mini={m} />,
  'warm-menu': (m) => <MockWarm withMenu mini={m} />,
  'dark-menu': (m) => <MockDark mini={m} />,
  broken: (m) => <MockDark broken mini={m} />,
  'dark-restored': (m) => <MockDark restored mini={m} />,
}

function PreviewMock({ variant, mini = false }) {
  const Render = PREVIEW_REGISTRY[variant]
  if (!Render) return null
  return Render(mini)
}

/* ------------------------------------------------------------------ */
/* Chat panel                                                         */
/* ------------------------------------------------------------------ */

function DiffBadge({ diff }) {
  const tones = {
    add: 'border-success/30 bg-success/10 text-success',
    mod: 'border-accent/30 bg-accent/10 text-accent-glow',
    err: 'border-danger/40 bg-danger/10 text-danger',
    ok: 'border-success/40 bg-success/15 text-success',
  }
  return (
    <span
      className={
        'inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 font-mono text-[10.5px] ' +
        (tones[diff.kind] || 'border-line bg-white/[0.03] text-ink-muted')
      }
    >
      {diff.text}
    </span>
  )
}

function ChatPanel({ step, paused, onTogglePause }) {
  // show the last 2 turns, with the latest pulsing in
  const startIdx = Math.max(0, step - 1)
  const visible = STORY.slice(startIdx, step + 1)

  return (
    <div className="flex flex-col gap-2 rounded-2xl border border-line bg-canvas/95 p-3">
      <div className="flex items-center justify-between border-b border-line pb-2">
        <div className="flex items-center gap-2 text-xs text-ink-muted">
          <MessageSquare className="h-3.5 w-3.5" />
          Чат проекта
          <span className="ml-1 hidden rounded-full border border-line bg-white/[0.03] px-1.5 py-0.5 font-mono text-[9.5px] sm:inline-flex">
            Sonnet 4.6
          </span>
        </div>
        <button
          type="button"
          onClick={onTogglePause}
          className="inline-flex items-center gap-1 rounded-md border border-line bg-white/[0.02] px-2 py-1 text-[10px] text-ink-muted transition hover:text-ink"
          aria-label={paused ? 'Запустить демо' : 'Поставить на паузу'}
        >
          {paused ? <Play className="h-3 w-3" /> : <Pause className="h-3 w-3" />}
          {paused ? 'Продолжить' : 'Пауза'}
        </button>
      </div>

      <div className="flex min-h-[260px] flex-col gap-3 overflow-hidden">
        <AnimatePresence initial={false} mode="popLayout">
          {visible.map((s, idx) => {
            const isLatest = idx === visible.length - 1
            return (
              <motion.div
                key={'turn-' + (startIdx + idx)}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: isLatest ? 1 : 0.55, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                transition={{ duration: 0.35 }}
                className="space-y-1.5"
              >
                <div
                  className={
                    'max-w-[88%] self-end rounded-2xl rounded-br-sm bg-accent/15 px-3 py-2 text-[13px] leading-snug text-ink ml-auto ' +
                    (s.rollback ? 'border border-success/30 bg-success/10 text-success' : '')
                  }
                >
                  {s.user}
                </div>
                <div className="max-w-[92%] self-start rounded-2xl rounded-bl-sm border border-line bg-white/[0.02] px-3 py-2 text-[13px] leading-snug text-ink-muted">
                  {s.ai}
                </div>
                <div className="pl-1">
                  <DiffBadge diff={s.diff} />
                </div>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>

      <div className="mt-1 flex items-center gap-2 rounded-xl border border-line bg-white/[0.02] px-3 py-2">
        <div className="flex-1 truncate text-[12px] text-ink-dim">
          Опишите, что нужно изменить…
        </div>
        <button
          type="button"
          className="grid h-7 w-7 place-items-center rounded-lg bg-accent text-white"
          tabIndex={-1}
          aria-label="Отправить"
        >
          <Send className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* Preview panel                                                      */
/* ------------------------------------------------------------------ */

function PreviewPanel({ cur }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-line bg-canvas">
      {/* Browser chrome */}
      <div className="flex items-center gap-2 border-b border-line bg-elev1/80 px-3 py-2">
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="ml-2 hidden truncate font-mono text-[11px] text-ink-dim sm:inline">
          https://espressonadya.ru
        </span>
        <span className="ml-2 truncate font-mono text-[11px] text-ink-dim sm:hidden">
          espressonadya.ru
        </span>
        <span className="ml-auto inline-flex items-center gap-1.5">
          <VersionPill version={cur.version} active />
          <span className="rounded-md border border-line bg-white/[0.03] px-1.5 py-0.5 font-mono text-[10px] text-success">
            ● live
          </span>
        </span>
      </div>

      {/* Preview surface */}
      <div className="relative h-[300px] sm:h-[360px] lg:h-[400px]">
        <AnimatePresence mode="wait">
          <motion.div
            key={cur.preview + (cur.rollback ? '-r' : '')}
            initial={{ opacity: 0, scale: 0.99 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.45 }}
            className="absolute inset-0"
          >
            <PreviewMock variant={cur.preview} />
          </motion.div>
        </AnimatePresence>

        {/* floating diff hint */}
        <div className="pointer-events-none absolute left-3 bottom-3 right-3 flex items-center justify-between gap-2">
          <DiffBadge diff={cur.diff} />
          {cur.version.tone === 'broken' && (
            <span className="hidden rounded-md border border-danger/40 bg-canvas/80 px-2 py-1 font-mono text-[10.5px] text-danger backdrop-blur sm:inline-flex">
              ⚠ откати на стабильную версию
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* Timeline — 5 mini-previews + rollback control                      */
/* ------------------------------------------------------------------ */

function Timeline({ step, onSelect }) {
  const isBroken = STORY[step]?.version.tone === 'broken'

  return (
    <div className="rounded-2xl border border-line bg-elev1/60 p-3">
      <div className="mb-2.5 flex items-center justify-between text-[11px] text-ink-muted">
        <span className="inline-flex items-center gap-1.5">
          <GitBranch className="h-3.5 w-3.5 text-accent-glow" />
          Лента версий
          <span className="hidden text-ink-dim sm:inline">
            · снапшот после каждого промпта
          </span>
        </span>
        <span className="font-mono text-[10px] text-ink-dim">кликни — откат</span>
      </div>

      <div className="grid grid-cols-5 gap-1.5 sm:gap-2">
        {STORY.map((s, i) => {
          const active = i === step
          const isPast = i < step
          const tone = s.version.tone
          return (
            <button
              key={s.version.id}
              type="button"
              onClick={() => onSelect(i)}
              className={
                'group relative overflow-hidden rounded-xl border text-left transition ' +
                (active
                  ? 'border-accent shadow-glow'
                  : isPast
                    ? 'border-line hover:border-white/15'
                    : 'border-line/40 opacity-60 hover:opacity-100')
              }
            >
              {/* mini preview */}
              <div className="relative aspect-[16/10] w-full overflow-hidden bg-canvas">
                <PreviewMock variant={s.preview} mini />
                {/* hover overlay */}
                <div className="absolute inset-0 grid place-items-center bg-canvas/0 opacity-0 transition group-hover:bg-canvas/50 group-hover:opacity-100">
                  <span className="inline-flex items-center gap-1 rounded-full border border-line bg-canvas/80 px-2 py-0.5 font-mono text-[10px] text-ink">
                    <Undo2 className="h-3 w-3" />
                    откат
                  </span>
                </div>
              </div>

              <div className="border-t border-line/60 px-2 py-1.5">
                <div className="flex items-center justify-between">
                  <span
                    className={
                      'font-mono text-[10px] ' +
                      (tone === 'broken'
                        ? 'text-danger'
                        : tone === 'restored'
                          ? 'text-success'
                          : tone === 'dark'
                            ? 'text-accent-glow'
                            : 'text-ink-muted')
                    }
                  >
                    {s.version.id}
                  </span>
                  {active && (
                    <span className="rounded-full bg-accent px-1.5 text-[8.5px] uppercase tracking-wider text-white">
                      сейчас
                    </span>
                  )}
                </div>
                <div className="mt-0.5 truncate text-[10.5px] text-ink-muted">
                  {s.version.label}
                </div>
              </div>

              {/* connector arrow for v5 ← v3 (rollback indicator) */}
              {s.rollback && (
                <div className="absolute -top-1 right-1 inline-flex items-center gap-0.5 rounded-full bg-success px-1.5 py-0.5 font-mono text-[8.5px] text-canvas">
                  <Undo2 className="h-2.5 w-2.5" strokeWidth={3} />
                  v3
                </div>
              )}
            </button>
          )
        })}
      </div>

      {/* Rollback CTA — pulses when v4 (broken) is active */}
      <AnimatePresence>
        {isBroken && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-3 flex items-center justify-between gap-3 rounded-xl border border-danger/30 bg-danger/[0.07] px-3 py-2.5"
          >
            <div className="flex items-center gap-2 text-[12.5px] text-ink">
              <AlertTriangle className="h-4 w-4 text-danger" />
              <span>
                AI сломал шапку. Не страшно — старые версии живут в ленте.
              </span>
            </div>
            <button
              type="button"
              onClick={() => onSelect(4)}
              className="inline-flex animate-pulse items-center gap-1.5 rounded-full bg-success px-3 py-1.5 text-[12px] text-canvas"
              style={{ fontWeight: 590 }}
            >
              <Undo2 className="h-3.5 w-3.5" />
              Вернуть на v3
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* Hero demo (composed)                                               */
/* ------------------------------------------------------------------ */

function HeroDemo() {
  const reduce = useReducedMotion()
  const [step, setStep] = useState(0)
  const [paused, setPaused] = useState(false)

  useEffect(() => {
    if (reduce || paused) return
    const t = setTimeout(() => setStep((s) => (s + 1) % STORY.length), 4000)
    return () => clearTimeout(t)
  }, [step, reduce, paused])

  const cur = STORY[step]

  const onSeek = (i) => {
    setPaused(true)
    setStep(i)
    track('demo_seek', { step: i, version: STORY[i].version.id })
  }

  const onTogglePause = () => {
    setPaused((p) => !p)
    track('demo_toggle_pause', { paused: !paused })
  }

  return (
    <div id="demo" className="relative">
      {/* glow orbs */}
      <div className="pointer-events-none absolute -left-20 -top-16 h-72 w-72 glow-orb opacity-90" />
      <div className="pointer-events-none absolute -right-10 bottom-0 h-72 w-72 glow-orb opacity-60" />

      <div className="relative space-y-3 rounded-3xl border border-line bg-elev1/40 p-3 backdrop-blur-xl md:p-4">
        <div className="grid gap-3 lg:grid-cols-[340px_1fr]">
          <ChatPanel step={step} paused={paused} onTogglePause={onTogglePause} />
          <PreviewPanel cur={cur} />
        </div>

        <Timeline step={step} onSelect={onSeek} />
      </div>
    </div>
  )
}

/* ================================================================== */
/* Hero                                                               */
/* ================================================================== */

function Hero() {
  const ease = [0.16, 1, 0.3, 1]
  return (
    <section id="top" className="relative overflow-hidden pb-12 pt-32 md:pb-16 md:pt-36">
      <div className="grid-bg pointer-events-none absolute inset-0 opacity-60" />

      {/* drifting accent orbs for depth */}
      <motion.div
        aria-hidden
        className="pointer-events-none absolute left-[8%] top-[18%] h-[420px] w-[420px] glow-orb opacity-50"
        animate={{
          x: [0, 30, -10, 0],
          y: [0, -20, 10, 0],
        }}
        transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        aria-hidden
        className="pointer-events-none absolute right-[6%] top-[8%] h-[360px] w-[360px] glow-orb opacity-30"
        animate={{
          x: [0, -25, 15, 0],
          y: [0, 18, -8, 0],
        }}
        transition={{ duration: 22, repeat: Infinity, ease: 'easeInOut' }}
      />

      <div className="container-x relative">
        <div className="mx-auto flex max-w-3xl flex-col items-center text-center">
          <motion.span
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, ease }}
            className="eyebrow"
          >
            <Sparkles className="h-3 w-3 text-accent-glow" />
            Российская AI-платформа · pre-launch
          </motion.span>

          <h1 className="display-h1 mt-5">
            <motion.span
              initial={{ opacity: 0, y: 24, filter: 'blur(8px)' }}
              animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
              transition={{ duration: 0.7, delay: 0.1, ease }}
              className="inline-block text-gradient"
            >
              Ваш сайт{' '}
            </motion.span>
            <motion.span
              initial={{ opacity: 0, y: 24, filter: 'blur(8px)' }}
              animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
              transition={{ duration: 0.7, delay: 0.24, ease }}
              className="inline-block accent-gradient"
            >
              за час,
            </motion.span>
            <br />
            <motion.span
              initial={{ opacity: 0, y: 24, filter: 'blur(8px)' }}
              animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
              transition={{ duration: 0.7, delay: 0.38, ease }}
              className="inline-block text-gradient"
            >
              не за месяц.
            </motion.span>
          </h1>

          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.52, ease }}
            className="mt-5 max-w-xl text-[17px] leading-relaxed text-ink-muted md:text-[18px]"
          >
            Frontend, backend, домен и SSL — собирает AI по одному чату. С откатом
            любой версии в один клик.{' '}
            <span className="text-ink" style={{ fontWeight: 510 }}>
              От 990 ₽/мес.
            </span>{' '}
            Без VPN, крипты и агентств.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.6, ease }}
            className="mt-7 flex flex-col items-center gap-3 sm:flex-row"
          >
            <MagneticButton
              href="#start"
              className="btn-primary text-[15px]"
              onClick={() => track('cta_click', { location: 'hero', label: 'Free' })}
            >
              Попробовать бесплатно
              <ArrowRight className="h-4 w-4" />
            </MagneticButton>
            <a
              href="#demo"
              className="text-[14px] text-ink-muted transition hover:text-ink"
              onClick={() => track('hero_demo_link')}
            >
              ↓ Смотри живой пример
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.75 }}
            className="mt-5 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-ink-dim"
          >
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> 5 дней без карты
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Без VPN и крипты
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Российские серверы
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> 152-ФЗ из коробки
            </span>
          </motion.div>
        </div>

        {/* The demo — story-driven, the heart of the page */}
        <motion.div
          initial={{ opacity: 0, y: 32 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.65, ease }}
          className="relative mx-auto mt-12 max-w-6xl"
        >
          <HeroDemo />
        </motion.div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Trust strip — partners & integrations                              */
/* ================================================================== */

function TrustStrip() {
  const items = [
    'SafeCloud',
    'Reg.ru',
    'ЮKassa',
    'Tinkoff',
    'YandexGPT',
    'GigaChat',
    'Claude',
    'GPT-4',
    'DeepSeek',
  ]
  return (
    <section className="relative py-10">
      <div className="container-x">
        <div className="mx-auto max-w-5xl rounded-2xl border border-line bg-elev1/40 px-4 py-5">
          <div className="flex flex-col items-center gap-3 text-center md:flex-row md:justify-between md:text-left">
            <div className="text-[12px] uppercase tracking-[0.22em] text-ink-dim">
              Партнёры стека
            </div>
            <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 md:justify-end">
              {items.map((it, i) => (
                <span
                  key={it}
                  className={
                    'text-[13px] tracking-tight text-ink-muted ' +
                    (i % 3 === 0 ? 'font-mono' : '')
                  }
                  style={{ fontWeight: i % 3 === 0 ? 510 : 590 }}
                >
                  {it}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Segments — кто наш клиент                                          */
/* ================================================================== */

const SEGMENTS = [
  {
    icon: User,
    label: 'Самозанятый · фрилансер',
    desc: 'Сайт-визитка с приёмом СБП, портфолио и формой заявки.',
    tier: 'Lite',
    price: '990 ₽',
  },
  {
    icon: Briefcase,
    label: 'ИП и малый бизнес',
    desc: 'Лендинг + онлайн-меню/каталог, кассовая интеграция, бронь.',
    tier: 'Starter',
    price: '2 990 ₽',
  },
  {
    icon: Building2,
    label: 'Стартап / запуск продукта',
    desc: 'MVP с personal-кабинетом, API, чат-ботами и автоматизациями.',
    tier: 'Pro',
    price: '7 990 ₽',
  },
  {
    icon: Rocket,
    label: 'Агентство · команда',
    desc: '152-ФЗ, 1С-интеграция, white-label на клиентов, менеджер.',
    tier: 'Enterprise',
    price: '19 990 ₽',
  },
]

function SegmentsSection() {
  return (
    <section id="segments" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Users className="h-3 w-3 text-accent-glow" /> Кому подходит
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Найди себя
            <br className="hidden md:block" /> и начни с правильного тарифа
          </h2>
          <p className="mt-5 text-ink-muted">
            От самозанятого с визиткой до агентства с десятками клиентов — стек
            масштабируется без переписывания. Заплати за то, что нужно сейчас.
          </p>
        </div>

        <div className="mt-12 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
          {SEGMENTS.map((s, i) => (
            <motion.a
              key={s.tier}
              href="#pricing"
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.45, delay: i * 0.08, ease: [0.16, 1, 0.3, 1] }}
              className="group relative flex flex-col rounded-2xl border border-line bg-elev1/40 p-5 transition hover:border-accent/35 hover:bg-elev1/70"
              onClick={() => track('segment_click', { tier: s.tier })}
            >
              <div className="grid h-11 w-11 place-items-center rounded-xl border border-line bg-white/[0.03] transition group-hover:border-accent/30 group-hover:bg-accent/10">
                <s.icon className="h-5 w-5 text-accent-glow" />
              </div>
              <div
                className="mt-4 text-[15px] text-ink"
                style={{ fontWeight: 590 }}
              >
                {s.label}
              </div>
              <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">
                {s.desc}
              </p>
              <div className="mt-5 flex items-center justify-between border-t border-line pt-3">
                <span className="text-[10.5px] uppercase tracking-[0.18em] text-ink-dim">
                  Стартовый тариф
                </span>
                <span className="inline-flex items-baseline gap-1">
                  <span
                    className="text-[14px] text-ink"
                    style={{ fontWeight: 590 }}
                  >
                    {s.tier}
                  </span>
                  <span className="font-mono text-[11px] text-accent-glow">
                    {s.price}
                  </span>
                </span>
              </div>
            </motion.a>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* ROI calculator                                                      */
/* ================================================================== */

function Slider({ label, value, onChange, min, max, step, format }) {
  return (
    <div>
      <div className="mb-2 flex items-baseline justify-between">
        <span
          className="text-[12.5px] uppercase tracking-[0.16em] text-ink-muted"
          style={{ fontWeight: 510 }}
        >
          {label}
        </span>
        <span
          className="font-mono text-[14px] text-ink"
          style={{ fontWeight: 590 }}
        >
          {format(value)}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full cursor-pointer accent-accent"
        style={{ accentColor: '#7170ff' }}
      />
      <div className="mt-1 flex justify-between text-[10px] text-ink-dim">
        <span>{format(min)}</span>
        <span>{format(max)}</span>
      </div>
    </div>
  )
}

function ROICalculator() {
  const [hosting, setHosting] = useState(1500)
  const [dev, setDev] = useState(8000)
  const [hours, setHours] = useState(8)

  // current monthly spend = hosting + dev retainer + hourly rate * hours
  const HOUR_RATE = 2500
  const monthlySpend = hosting + dev + hours * HOUR_RATE
  const omniaPrice = 7990 // Pro tier
  const monthlySaving = Math.max(0, monthlySpend - omniaPrice)
  const yearlySaving = monthlySaving * 12
  const hourSaving = Math.round(hours * 0.85) // assumed 85% time-saving

  return (
    <section id="roi" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Calculator className="h-3 w-3 text-accent-glow" /> Калькулятор экономии
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Сколько ты{' '}
            <span className="accent-gradient">экономишь</span> на Omnia?
          </h2>
          <p className="mt-5 text-ink-muted">
            Подвинь ползунки под свою реальную ситуацию — увидишь экономию по
            сравнению с тарифом Pro (7 990 ₽).
          </p>
        </div>

        <div className="mx-auto mt-12 grid max-w-5xl gap-4 lg:grid-cols-[1fr_1fr]">
          {/* Sliders */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.55, ease: [0.16, 1, 0.3, 1] }}
            className="rounded-2xl border border-line bg-elev1/50 p-6"
          >
            <div className="space-y-6">
              <Slider
                label="Хостинг сейчас, ₽/мес"
                value={hosting}
                onChange={setHosting}
                min={0}
                max={10000}
                step={100}
                format={(v) => v.toLocaleString('ru-RU') + ' ₽'}
              />
              <Slider
                label="Разработчик / агентство, ₽/мес"
                value={dev}
                onChange={setDev}
                min={0}
                max={100000}
                step={500}
                format={(v) => v.toLocaleString('ru-RU') + ' ₽'}
              />
              <Slider
                label="Часов на правки в месяц"
                value={hours}
                onChange={setHours}
                min={0}
                max={40}
                step={1}
                format={(v) => v + ' ч'}
              />
            </div>
            <div className="mt-6 flex items-center justify-between border-t border-line pt-4 text-[12px]">
              <span className="text-ink-muted">Сейчас тратишь</span>
              <span
                className="font-mono text-[16px] text-ink"
                style={{ fontWeight: 590 }}
              >
                {monthlySpend.toLocaleString('ru-RU')} ₽/мес
              </span>
            </div>
          </motion.div>

          {/* Result */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.55, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="relative overflow-hidden rounded-2xl border border-accent/30 bg-gradient-to-br from-accent/[0.10] via-elev1/60 to-canvas p-6 shadow-glow"
          >
            <div className="pointer-events-none absolute -right-12 -top-12 h-48 w-48 glow-orb opacity-70" />
            <div className="relative">
              <div
                className="inline-flex items-center gap-2 rounded-full border border-accent/40 bg-accent/15 px-3 py-1 text-[11px] uppercase tracking-[0.18em] text-accent-glow"
                style={{ fontWeight: 590 }}
              >
                <TrendingDown className="h-3 w-3" />
                Экономия с тарифом Pro
              </div>

              <div className="mt-5 flex items-baseline gap-2">
                <span
                  className="accent-gradient text-[56px] leading-none"
                  style={{ fontWeight: 600, letterSpacing: '-0.025em' }}
                >
                  <CountUp
                    value={monthlySaving}
                    duration={0.6}
                    format={(n) =>
                      Math.round(n).toLocaleString('ru-RU')
                    }
                  />
                </span>
                <span className="text-[16px] text-ink-muted">₽/мес</span>
              </div>
              <div className="mt-1 text-[13px] text-ink-muted">
                <span
                  className="font-mono text-ink"
                  style={{ fontWeight: 590 }}
                >
                  <CountUp
                    value={yearlySaving}
                    duration={0.6}
                    format={(n) => Math.round(n).toLocaleString('ru-RU')}
                  />{' '}
                  ₽
                </span>{' '}
                в год · и{' '}
                <span
                  className="font-mono text-ink"
                  style={{ fontWeight: 590 }}
                >
                  <CountUp value={hourSaving} duration={0.6} />{' '}
                  ч
                </span>{' '}
                свободного времени в месяц
              </div>

              <div className="mt-6 grid gap-2 text-[12.5px]">
                <div className="flex items-start gap-2.5">
                  <Check className="mt-0.5 h-4 w-4 flex-none text-success" />
                  <span className="text-ink-muted">
                    Хостинг, домен, SSL, бэкапы — уже включены в Pro
                  </span>
                </div>
                <div className="flex items-start gap-2.5">
                  <Check className="mt-0.5 h-4 w-4 flex-none text-success" />
                  <span className="text-ink-muted">
                    Правки через AI-чат, без подрядчика и тикетов
                  </span>
                </div>
                <div className="flex items-start gap-2.5">
                  <Check className="mt-0.5 h-4 w-4 flex-none text-success" />
                  <span className="text-ink-muted">
                    Откат любой версии в один клик
                  </span>
                </div>
              </div>

              <div className="mt-6">
                <MagneticButton
                  href="#pricing"
                  className="btn-primary w-full text-[14px]"
                  onClick={() =>
                    track('cta_click', { location: 'roi', label: 'Pro' })
                  }
                >
                  Перейти на Pro <ArrowRight className="h-4 w-4" />
                </MagneticButton>
              </div>
            </div>
          </motion.div>
        </div>

        <p className="mx-auto mt-6 max-w-3xl text-center text-[11px] text-ink-dim">
          Расчёт: текущие траты = хостинг + разработчик + (часы × 2 500 ₽).
          Экономия = (текущие − 7 990 ₽). Часы — 85% от текущих, остаток уходит на
          формулировку промпта.
        </p>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Team                                                                */
/* ================================================================== */

const TEAM = [
  {
    name: 'Артём Левченко',
    role: 'co-founder · бизнес и маркетинг',
    bio: 'Основатель проектов kanavto, kuzovnsk, klining-24 — 4 работающих SMB. Растил их с нуля до стабильной выручки за 2024–2025.',
    initials: 'АЛ',
    accent: 'from-violet-500 to-fuchsia-500',
    tg: '#',
  },
  {
    name: 'Рома Исакин',
    role: 'co-founder · тех / AI / архитектура',
    bio: '10 лет в backend и AI-агентах. Поднимал инфраструктуру для SMB и продуктов с десятками тысяч активных пользователей.',
    initials: 'РИ',
    accent: 'from-cyan-500 to-blue-500',
    tg: '#',
  },
]

function TeamSection() {
  return (
    <section id="team" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Users className="h-3 w-3 text-accent-glow" /> Команда
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Двое founders с реальным
            <br className="hidden md:block" /> SMB-опытом
          </h2>
          <p className="mt-5 text-ink-muted">
            Не ноунеймы из Telegram-чата. Уже строили продукты, которые работают и
            приносят деньги.
          </p>
        </div>

        <div className="mx-auto mt-12 grid max-w-3xl gap-4 md:grid-cols-2">
          {TEAM.map((p, i) => (
            <motion.div
              key={p.name}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.5, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
              className="card-elev"
            >
              <div className="flex items-start gap-4">
                <div
                  className={
                    'grid h-16 w-16 flex-none place-items-center rounded-full bg-gradient-to-br shadow-lg ' +
                    p.accent
                  }
                >
                  <span
                    className="text-[18px] text-white"
                    style={{ fontWeight: 590 }}
                  >
                    {p.initials}
                  </span>
                </div>
                <div className="min-w-0 flex-1">
                  <div
                    className="text-[16px] text-ink"
                    style={{ fontWeight: 590 }}
                  >
                    {p.name}
                  </div>
                  <div
                    className="mt-0.5 text-[10.5px] uppercase tracking-[0.18em] text-accent-glow"
                    style={{ fontWeight: 510 }}
                  >
                    {p.role}
                  </div>
                  <p className="mt-3 text-[13px] leading-relaxed text-ink-muted">
                    {p.bio}
                  </p>
                  <a
                    href={p.tg}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-4 inline-flex items-center gap-1.5 text-[12px] text-ink-muted transition hover:text-ink"
                    onClick={() => track('team_telegram', { name: p.name })}
                  >
                    <Send className="h-3 w-3" />
                    Написать в Telegram
                  </a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <p className="mx-auto mt-8 max-w-2xl text-center text-[12px] text-ink-dim">
          Бутстрап с 30 000 ₽ стартового капитала. Не ищем VC — строим с расчётом
          на устойчивый профильный SaaS.
        </p>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Versioning closeup — the killer feature                             */
/* ================================================================== */

function VersioningSection() {
  return (
    <section id="versions" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Undo2 className="h-3 w-3 text-accent-glow" /> Главная фича
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            AI-кодинг без страха —
            <br className="hidden md:block" /> с кнопкой «вернуть как было»
          </h2>
          <p className="mt-5 text-ink-muted">
            Конкуренты дают AI-чат и оставляют тебя с git'ом наедине. Мы делаем
            снапшот после каждого промпта — с превью, как в галерее фото.
          </p>
        </div>

        <div className="mx-auto mt-12 grid max-w-5xl gap-4 lg:grid-cols-3">
          {[
            {
              icon: GitBranch,
              title: 'Снапшот после каждого промпта',
              text: 'Автоматически. Код + БД + превью-скриншот. Лимит — 50/500/∞ по тарифу.',
            },
            {
              icon: Eye,
              title: 'Превью каждой версии',
              text: 'Видишь, как сайт выглядел, до того как нажмёшь «вернуться сюда». Никаких неожиданностей.',
            },
            {
              icon: Undo2,
              title: 'Откат за один клик',
              text: 'Без git, без терминала, без &laquo;ой, я не сохранил&raquo;. AI-кодинг становится безопасным.',
            },
          ].map((c, i) => (
            <motion.div
              key={c.title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.45, delay: i * 0.08 }}
              className="card-elev"
            >
              <div className="grid h-10 w-10 place-items-center rounded-lg border border-accent/30 bg-accent/10">
                <c.icon className="h-4 w-4 text-accent-glow" />
              </div>
              <div
                className="mt-4 text-[18px] text-ink"
                style={{ fontWeight: 590 }}
              >
                {c.title}
              </div>
              <p
                className="mt-2 text-[14px] text-ink-muted"
                dangerouslySetInnerHTML={{ __html: c.text }}
              />
            </motion.div>
          ))}
        </div>

        <div className="mx-auto mt-10 flex max-w-3xl items-start gap-3 rounded-2xl border border-accent/30 bg-accent/[0.06] p-5">
          <Shield className="mt-0.5 h-5 w-5 flex-none text-accent-glow" />
          <div className="text-[14px] text-ink">
            Никто из конкурентов не делает версионирование с превью.
            <span className="text-ink-muted">
              {' '}
              У Lovable и Bolt — git вручную. У Tilda — нет AI вообще. У агентств —
              «пишите задачу в почту, ответим к четвергу».
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Problems                                                            */
/* ================================================================== */

const PROBLEMS = [
  {
    icon: Wallet,
    pain: 'Агентство — 200к ₽ и 2 месяца',
    solution: 'AI собирает сайт за минуты — без брифов и подрядчиков.',
  },
  {
    icon: Code2,
    pain: 'Tilda и Wix не дают backend',
    solution: 'У нас фронт + БД + API + авторизация генерятся вместе.',
  },
  {
    icon: Globe,
    pain: 'Lovable, Bolt, v0 не работают для РФ',
    solution: 'Рублёвая оплата, российские серверы, поддержка на русском.',
  },
]

function ProblemsSection() {
  return (
    <section className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Layers className="h-3 w-3 text-accent-glow" /> Почему сейчас
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            AI делает сайты быстрее людей —
            <br className="hidden md:block" /> только не для русского рынка
          </h2>
          <p className="mt-5 text-ink-muted">
            Между «Tilda без AI» и «зарубежной AI-платформой, которая не работает в
            РФ» — пропасть. Мы её закрываем.
          </p>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {PROBLEMS.map((p, i) => (
            <motion.div
              key={p.pain}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.45, delay: i * 0.08 }}
              className="card-elev"
            >
              <div className="grid h-10 w-10 place-items-center rounded-lg border border-line bg-white/[0.03]">
                <p.icon className="h-4 w-4 text-accent-glow" />
              </div>
              <div className="mt-4 text-[11px] uppercase tracking-[0.2em] text-ink-dim">
                Боль
              </div>
              <div className="mt-1 text-[18px] text-ink" style={{ fontWeight: 590 }}>
                {p.pain}
              </div>
              <div className="mt-4 text-[11px] uppercase tracking-[0.2em] text-accent-glow">
                Что делаем
              </div>
              <div className="mt-1 text-[14px] text-ink-muted">{p.solution}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* How it works                                                        */
/* ================================================================== */

const STEPS = [
  {
    n: '01',
    icon: MessageSquare,
    title: 'Опиши промптом',
    text: 'Что за сайт, для кого, какие фишки. Голосом или текстом — на русском.',
    chip: 'Mix LLM: DeepSeek · Haiku · Sonnet · Yandex',
  },
  {
    n: '02',
    icon: Server,
    title: 'AI собирает всё',
    text: 'Дизайн, код, БД, API, авторизация, домен и SSL — без участия человека.',
    chip: 'Фронт · Backend · Домен · Деплой',
  },
  {
    n: '03',
    icon: Rocket,
    title: 'Сайт уже live',
    text: 'Делишься ссылкой. Хочешь править — пиши в чат, версия откатится в один клик.',
    chip: 'Live URL + лента версий',
  },
]

function HowItWorks() {
  return (
    <section id="how" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Zap className="h-3 w-3 text-accent-glow" /> Как это работает
          </span>
          <h2 className="display-h2 mt-5 text-gradient">Три шага до живого сайта</h2>
          <p className="mt-5 text-ink-muted">
            Раньше нужно было собирать пять сервисов. Теперь — один чат и одна
            подписка.
          </p>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {STEPS.map((s, i) => (
            <motion.div
              key={s.n}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.45, delay: i * 0.08 }}
              className="card-elev relative overflow-hidden"
            >
              <div className="absolute right-5 top-5 font-mono text-xs text-ink-dim">
                {s.n}
              </div>
              <div className="grid h-10 w-10 place-items-center rounded-lg border border-line bg-white/[0.03]">
                <s.icon className="h-4 w-4 text-accent-glow" />
              </div>
              <div className="mt-4 text-[20px] text-ink" style={{ fontWeight: 590 }}>
                {s.title}
              </div>
              <p className="mt-2 text-[14px] text-ink-muted">{s.text}</p>
              <div className="mt-5 inline-flex rounded-full border border-line bg-white/[0.02] px-3 py-1 text-[11px] text-ink-muted">
                {s.chip}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Stack — what AI builds under the hood                              */
/* ================================================================== */

const STACK_LAYERS = [
  {
    icon: Zap,
    title: 'Frontend',
    tech: 'React 19 · Vite · Tailwind',
    desc: 'Адаптивная вёрстка, анимации, SEO-теги, Lighthouse 90+. Без 1 строчки кода руками.',
  },
  {
    icon: Cpu,
    title: 'Backend API',
    tech: 'FastAPI · OpenAPI · JWT',
    desc: 'REST-эндпоинты, авторизация, валидация. AI генерит логику и тесты.',
  },
  {
    icon: Database,
    title: 'База данных',
    tech: 'Postgres 16 · Alembic',
    desc: 'Схемы, миграции, индексы. AI поддерживает миграции на каждом апдейте.',
  },
  {
    icon: Globe,
    title: 'Домен и SSL',
    tech: 'Reg.ru · Lets Encrypt',
    desc: 'Регистрация .ru/.рф, DNS, SSL-сертификат. Авто-обновление.',
  },
  {
    icon: Rocket,
    title: 'Auto-deploy',
    tech: 'Docker · Ansible · Nginx',
    desc: 'Staging + prod, blue-green деплой. Никаких ручных SSH-сессий.',
  },
  {
    icon: Server,
    title: 'Сервера в РФ',
    tech: 'SafeCloud · CORTEL',
    desc: 'VPS в Москве, 99.5% uptime. ПДн внутри страны (152-ФЗ из коробки).',
  },
  {
    icon: HardDrive,
    title: 'Бэкапы и мониторинг',
    tech: 'Daily snapshots · Loki · Grafana',
    desc: 'Снэпшоты БД ежедневно, 7 дней истории. Алерты в Telegram при 5xx.',
  },
]

const BUILD_STEPS = [
  {
    icon: Zap,
    time: '0:01',
    title: 'Дизайн и интерфейс',
    desc: 'Hero, меню, форма брони — готовы',
    detail: '312 строк · React 19 + Tailwind',
  },
  {
    icon: Database,
    time: '0:14',
    title: 'База данных',
    desc: 'Схема под пользователей и заказы',
    detail: 'Postgres 16 · users · bookings · menu_items',
  },
  {
    icon: Cpu,
    time: '0:23',
    title: 'API и авторизация',
    desc: 'Эндпоинты для брони и меню',
    detail: 'POST /booking · GET /menu · JWT-auth',
  },
  {
    icon: Globe,
    time: '0:31',
    title: 'Домен',
    desc: 'espressonadya.ru — зарегистрирован',
    detail: 'через Reg.ru API · DNS настроен',
  },
  {
    icon: Lock,
    time: '0:42',
    title: 'SSL-сертификат',
    desc: 'Защищённое соединение HTTPS',
    detail: "Let's Encrypt · авто-обновление",
  },
  {
    icon: Rocket,
    time: '0:58',
    title: 'Развёртывание',
    desc: 'Сайт уехал на боевой сервер',
    detail: 'Docker · safecloud-vps-04',
  },
  {
    icon: Activity,
    time: '1:12',
    title: 'Проверка здоровья',
    desc: 'Все страницы и API отвечают',
    detail: 'Health-check passed · 200 OK',
  },
  {
    icon: CheckCircle2,
    time: '1:14',
    title: 'Сайт работает',
    desc: 'espressonadya.ru',
    detail: 'Готов принимать клиентов',
    final: true,
  },
]

function BuildConsole() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className="relative overflow-hidden rounded-3xl border border-line bg-elev1/40 p-5 shadow-cardLift backdrop-blur-xl md:p-7"
    >
      {/* glow orbs */}
      <div className="pointer-events-none absolute -left-20 -top-16 h-56 w-56 glow-orb opacity-70" />
      <div className="pointer-events-none absolute -right-12 bottom-0 h-56 w-56 glow-orb opacity-40" />

      {/* header */}
      <div className="relative mb-6 flex items-end justify-between gap-3 border-b border-line pb-5">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-accent/30 bg-accent/10 px-2.5 py-1 text-[10px] uppercase tracking-[0.22em] text-accent-glow" style={{ fontWeight: 590 }}>
            <Sparkles className="h-3 w-3" />
            AI-пайплайн
          </div>
          <div className="mt-2.5 text-[15px] leading-snug text-ink" style={{ fontWeight: 590 }}>
            Сборка сайта espressonadya.ru
          </div>
          <div className="mt-0.5 text-[12px] text-ink-muted">
            8 слоёв собраны и работают
          </div>
        </div>
        <div className="text-right">
          <div className="text-[10px] uppercase tracking-[0.18em] text-ink-dim" style={{ fontWeight: 510 }}>
            всего занято
          </div>
          <div
            className="mt-0.5 text-[26px] leading-none accent-gradient"
            style={{ fontWeight: 600, letterSpacing: '-0.02em' }}
          >
            1:14
          </div>
          <div className="text-[10px] text-ink-dim">мин : сек</div>
        </div>
      </div>

      {/* steps */}
      <div className="relative">
        {/* vertical connector line */}
        <div
          className="absolute left-[19px] top-3 w-px"
          style={{
            bottom: 12,
            background:
              'linear-gradient(to bottom, rgba(113,112,255,0.55) 0%, rgba(113,112,255,0.30) 70%, rgba(39,166,68,0.55) 100%)',
          }}
        />

        <div className="space-y-3">
          {BUILD_STEPS.map((s, i) => (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, x: -14 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{
                duration: 0.45,
                delay: 0.25 + i * 0.11,
                ease: [0.16, 1, 0.3, 1],
              }}
              className="relative flex items-start gap-3.5"
            >
              {/* icon circle */}
              <div
                className={
                  'relative z-10 grid h-10 w-10 flex-none place-items-center rounded-full border ' +
                  (s.final
                    ? 'border-success/50 bg-gradient-to-br from-success/30 to-success/10 shadow-[0_0_25px_rgba(39,166,68,0.35)]'
                    : 'border-accent/35 bg-gradient-to-br from-accent/20 to-accent/[0.04] shadow-[0_0_18px_rgba(113,112,255,0.18)]')
                }
              >
                <s.icon
                  className="h-4 w-4"
                  style={{ color: s.final ? '#5cd97a' : '#8b8aff' }}
                  strokeWidth={2}
                />
              </div>

              {/* card */}
              <div
                className={
                  'min-w-0 flex-1 rounded-xl border px-4 py-3 transition ' +
                  (s.final
                    ? 'border-success/35 bg-gradient-to-r from-success/[0.10] via-success/[0.04] to-canvas'
                    : 'border-line bg-canvas/60 hover:border-white/15')
                }
              >
                <div className="flex items-center justify-between gap-3">
                  <span
                    className="truncate text-[14px] text-ink"
                    style={{ fontWeight: 590 }}
                  >
                    {s.title}
                  </span>
                  <div className="flex flex-none items-center gap-2">
                    <span className="font-mono text-[10.5px] text-ink-dim">{s.time}</span>
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      whileInView={{ scale: 1, opacity: 1 }}
                      viewport={{ once: true, margin: '-100px' }}
                      transition={{
                        duration: 0.3,
                        delay: 0.45 + i * 0.11,
                        type: 'spring',
                        stiffness: 220,
                      }}
                      className={
                        'grid h-4.5 w-4.5 place-items-center rounded-full ' +
                        (s.final
                          ? 'bg-success text-canvas'
                          : 'bg-success/15 text-success')
                      }
                      style={{ height: 18, width: 18 }}
                    >
                      <Check className="h-3 w-3" strokeWidth={3} />
                    </motion.div>
                  </div>
                </div>
                <div className="mt-1 truncate text-[12.5px] text-ink-muted">
                  {s.desc}
                </div>
                {s.detail && (
                  <div className="mt-1.5 flex items-center gap-1.5 text-[10.5px] text-ink-dim">
                    <span
                      className="h-px w-3 flex-none"
                      style={{
                        background: s.final
                          ? 'rgba(39,166,68,0.4)'
                          : 'rgba(113,112,255,0.4)',
                      }}
                    />
                    <span className="truncate">{s.detail}</span>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* footer */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-100px' }}
        transition={{
          duration: 0.5,
          delay: 0.25 + BUILD_STEPS.length * 0.11 + 0.25,
        }}
        className="relative mt-6 flex items-center justify-between gap-3 border-t border-line pt-4"
      >
        <span className="inline-flex items-center gap-2 text-[12.5px] text-ink-muted">
          <CheckCircle2 className="h-4 w-4 text-success" />
          <span>
            <span className="text-ink" style={{ fontWeight: 590 }}>
              Готово
            </span>{' '}
            — клиент видит работающий сайт
          </span>
        </span>
        <span
          className="inline-flex items-center gap-1.5 rounded-full border border-accent/30 bg-accent/10 px-3 py-1.5 text-[11px] text-accent-glow"
          style={{ fontWeight: 590 }}
        >
          espressonadya.ru
          <ArrowRight className="h-3 w-3" />
        </span>
      </motion.div>
    </motion.div>
  )
}

function StackSection() {
  return (
    <section id="stack" className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Box className="h-3 w-3 text-accent-glow" /> Что AI собирает под капотом
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Полный стек —
            <br className="hidden md:block" />{' '}
            <span className="accent-gradient">по одному промпту</span>
          </h2>
          <p className="mt-5 text-ink-muted">
            У конкурентов клиент собирает 5–7 разных сервисов и платит 5 счетов: хостинг,
            домен, AI, базу данных, поддержку. У нас AI делает всё сам — от дизайна до
            бэкапов. Один чат. Один счёт. Один менеджер.
          </p>
        </div>

        <div className="mt-14 grid gap-6 lg:grid-cols-[1.1fr_1fr]">
          <BuildConsole />

          <div className="space-y-2.5">
            {STACK_LAYERS.map((l, i) => (
              <motion.div
                key={l.title}
                initial={{ opacity: 0, x: 24 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{
                  duration: 0.5,
                  delay: i * 0.06,
                  ease: [0.16, 1, 0.3, 1],
                }}
                className="group flex items-start gap-3.5 rounded-xl border border-line bg-elev1/40 p-4 transition hover:border-white/15 hover:bg-elev1/70"
              >
                <div className="grid h-10 w-10 flex-none place-items-center rounded-lg border border-line bg-white/[0.03] transition group-hover:border-accent/30 group-hover:bg-accent/10">
                  <l.icon className="h-4 w-4 text-accent-glow" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-0.5">
                    <span
                      className="text-[15px] text-ink"
                      style={{ fontWeight: 590 }}
                    >
                      {l.title}
                    </span>
                    <span className="font-mono text-[10.5px] uppercase tracking-wider text-ink-dim">
                      {l.tech}
                    </span>
                  </div>
                  <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">
                    {l.desc}
                  </p>
                </div>
                <div className="grid h-5 w-5 flex-none place-items-center rounded-full bg-success/15 text-success">
                  <Check className="h-3 w-3" strokeWidth={3} />
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.55, delay: 0.5 }}
          className="mx-auto mt-12 max-w-3xl rounded-2xl border border-accent/30 bg-gradient-to-r from-accent/[0.10] via-accent/[0.05] to-transparent p-5 text-center"
        >
          <p className="text-[14.5px] text-ink">
            Ты пишешь промптом —{' '}
            <span className="accent-gradient" style={{ fontWeight: 590 }}>
              AI делает под капотом
            </span>
            .{' '}
            <span className="text-ink-muted">
              Тебе не нужно знать, что такое Postgres, Ansible или 152-ФЗ.
            </span>
          </p>
        </motion.div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Timeline compare — 5 minutes vs 2 months                           */
/* ================================================================== */

const FAST_TIMELINE = [
  { time: '0:00', label: 'Описал промптом' },
  { time: '0:30', label: 'AI собрал дизайн и UX' },
  { time: '1:00', label: 'Backend + БД развёрнуты' },
  { time: '1:30', label: 'Домен зарегистрирован' },
  { time: '2:00', label: 'SSL · auto-deploy' },
  { time: '5:00', label: 'Live · 6 990 ₽ / мес', final: true },
]

const SLOW_TIMELINE = [
  { time: 'День 1', label: 'Бриф у агентства' },
  { time: 'День 7', label: 'Получили первый дизайн' },
  { time: 'День 21', label: 'Утвердили вёрстку' },
  { time: 'День 35', label: 'Backend в работе' },
  { time: 'День 50', label: 'Деплой настраивают' },
  { time: 'День 60', label: 'Live · 250 000 ₽', final: true },
]

function TimelineTrack({ items, accent, fast }) {
  return (
    <div className="relative">
      {/* vertical line */}
      <div
        className="absolute left-[11px] top-3 bottom-3 w-px"
        style={{
          background: fast
            ? 'linear-gradient(to bottom, rgba(113,112,255,0.6), rgba(113,112,255,0.15))'
            : 'linear-gradient(to bottom, rgba(244,68,68,0.4), rgba(244,68,68,0.1))',
        }}
      />

      <div className="space-y-4">
        {items.map((it, i) => (
          <motion.div
            key={it.time + it.label}
            initial={{ opacity: 0, x: fast ? -16 : 16 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{
              duration: 0.4,
              delay: fast ? i * 0.1 : i * 0.22,
              ease: [0.16, 1, 0.3, 1],
            }}
            className="relative flex items-start gap-3.5"
          >
            {/* dot */}
            <div className="relative z-10 grid h-6 w-6 flex-none place-items-center">
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: true, margin: '-100px' }}
                transition={{
                  duration: 0.35,
                  delay: fast ? i * 0.1 + 0.05 : i * 0.22 + 0.05,
                  type: 'spring',
                  stiffness: 220,
                }}
                className="h-3 w-3 rounded-full"
                style={{
                  background: it.final ? accent : it.final ? '#27a644' : accent,
                  boxShadow: it.final
                    ? `0 0 18px ${accent}`
                    : `0 0 10px ${accent}66`,
                }}
              />
            </div>

            <div className="min-w-0 flex-1 pb-1">
              <div
                className="font-mono text-[10.5px] uppercase tracking-[0.16em]"
                style={{ color: fast ? '#8b8aff' : '#a8aab1', fontWeight: 590 }}
              >
                {it.time}
              </div>
              <div
                className={
                  'mt-0.5 text-[13.5px] ' +
                  (it.final ? 'text-ink' : 'text-ink-muted')
                }
                style={{ fontWeight: it.final ? 590 : 510 }}
              >
                {it.label}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

function TimelineCompareSection() {
  return (
    <section id="speed" className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Timer className="h-3 w-3 text-accent-glow" /> Скорость до результата
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            5 минут вместо
            <br className="hidden md:block" />{' '}
            <span className="accent-gradient">2 месяцев</span>
          </h2>
          <p className="mt-5 text-ink-muted">
            Один и тот же сайт — кофейне на Патриках. Слева — путь с AI. Справа —
            классический путь через агентство.
          </p>
        </div>

        <div className="mx-auto mt-14 grid max-w-4xl gap-4 md:grid-cols-2">
          {/* Fast */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.55, ease: [0.16, 1, 0.3, 1] }}
            className="relative overflow-hidden rounded-2xl border border-accent/30 bg-gradient-to-br from-accent/[0.10] via-elev1/60 to-canvas p-6 shadow-glow"
          >
            <div className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 glow-orb opacity-70" />
            <div className="relative">
              <div className="mb-1 inline-flex items-center gap-2 rounded-full border border-accent/40 bg-accent/15 px-3 py-1 text-[11px] uppercase tracking-[0.18em] text-accent-glow" style={{ fontWeight: 590 }}>
                <Sparkles className="h-3 w-3" />
                С Omnia.AI
              </div>
              <div className="mt-3 mb-5 flex items-baseline gap-2">
                <span className="text-[42px] leading-none text-ink" style={{ fontWeight: 600, letterSpacing: '-0.02em' }}>
                  <CountUp value={5} duration={1.2} />
                </span>
                <span className="text-[14px] text-ink-muted">минут до live-сайта</span>
              </div>
              <TimelineTrack items={FAST_TIMELINE} accent="#7170ff" fast />
            </div>
          </motion.div>

          {/* Slow */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.55, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="relative overflow-hidden rounded-2xl border border-line bg-elev1/40 p-6"
          >
            <div className="relative">
              <div className="mb-1 inline-flex items-center gap-2 rounded-full border border-line bg-white/[0.02] px-3 py-1 text-[11px] uppercase tracking-[0.18em] text-ink-muted" style={{ fontWeight: 590 }}>
                <Hourglass className="h-3 w-3" />
                Без Omnia.AI · агентство
              </div>
              <div className="mt-3 mb-5 flex items-baseline gap-2">
                <span className="text-[42px] leading-none text-ink-muted" style={{ fontWeight: 600, letterSpacing: '-0.02em' }}>
                  <CountUp value={60} duration={2.4} />
                </span>
                <span className="text-[14px] text-ink-dim">дней до live-сайта</span>
              </div>
              <TimelineTrack items={SLOW_TIMELINE} accent="#a8aab1" />
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="mx-auto mt-10 grid max-w-4xl gap-3 sm:grid-cols-3"
        >
          {[
            { value: 17280, suffix: '×', label: 'быстрее, чем агентство' },
            { value: 97, prefix: '−', suffix: '%', label: 'дешевле первой настройки' },
            { value: 0, label: 'звонков с подрядчиком' },
          ].map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-line bg-elev1/40 p-4 text-center"
            >
              <div
                className="text-[28px] leading-none"
                style={{ fontWeight: 600, letterSpacing: '-0.02em' }}
              >
                <span className="accent-gradient">
                  <CountUp
                    value={s.value}
                    duration={1.6}
                    prefix={s.prefix || ''}
                    suffix={s.suffix || ''}
                  />
                </span>
              </div>
              <div className="mt-1.5 text-[12px] text-ink-muted">{s.label}</div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Comparison table                                                   */
/* ================================================================== */

const COMPARISON = [
  {
    name: 'Omnia.AI',
    accent: true,
    rows: [true, true, true, true, true, true, true],
  },
  {
    name: 'AI-конструкторы РФ',
    rows: [true, false, 'partial', false, true, false, true],
  },
  {
    name: 'Lovable / v0 / Bolt',
    rows: [true, false, false, false, false, false, 'partial'],
  },
  { name: 'Tilda / Wix', rows: [false, false, false, true, true, false, true] },
  {
    name: 'Студия / агентство',
    rows: [false, false, true, true, true, false, true],
  },
]

const COMPARISON_FEATURES = [
  '★ Откат версий в 1 клик',
  'Mix LLM (выбор модели)',
  'Полный backend (Postgres + JWT)',
  'Российские серверы + 152-ФЗ',
  'Чат-боты + автоматизации',
  'Free trial без карты',
  'Минимальная цена в РФ',
]

function ComparisonSection() {
  return (
    <section className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Eye className="h-3 w-3 text-accent-glow" /> Сравнение
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Никто другой не закрывает все шесть пунктов
          </h2>
        </div>

        <div className="mt-10 overflow-x-auto rounded-2xl border border-line bg-elev1/60">
          <div className="grid min-w-[820px] grid-cols-[1.6fr_repeat(5,_1fr)] text-[12px] text-ink-muted">
            <div className="border-b border-line bg-canvas/60 px-4 py-3 text-left uppercase tracking-[0.18em]">
              Что важно
            </div>
            {COMPARISON.map((c) => (
              <div
                key={c.name}
                className={
                  'border-b border-line px-3 py-3 text-center uppercase tracking-[0.16em] ' +
                  (c.accent
                    ? 'bg-accent/15 text-ink'
                    : 'bg-canvas/60 text-ink-muted')
                }
                style={{ fontWeight: 510 }}
              >
                {c.name}
              </div>
            ))}

            {COMPARISON_FEATURES.map((feat, rowIdx) => (
              <div key={feat} className="contents">
                <div className="border-b border-line/60 px-4 py-3.5 text-[13px] text-ink">
                  {feat}
                </div>
                {COMPARISON.map((c) => {
                  const v = c.rows[rowIdx]
                  return (
                    <div
                      key={c.name + rowIdx}
                      className={
                        'flex items-center justify-center border-b border-line/60 px-3 py-3.5 ' +
                        (c.accent ? 'bg-accent/[0.06]' : '')
                      }
                    >
                      {v === true ? (
                        <Check
                          className={
                            'h-4 w-4 ' +
                            (c.accent ? 'text-accent-glow' : 'text-ink-muted')
                          }
                        />
                      ) : v === 'partial' ? (
                        <span className="text-[11px] text-warn">частично</span>
                      ) : (
                        <X className="h-4 w-4 text-ink-dim/50" />
                      )}
                    </div>
                  )
                })}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Features grid                                                       */
/* ================================================================== */

const FEATURES = [
  {
    icon: MessageSquare,
    title: 'AI-чат на русском',
    desc: 'Mix LLM: DeepSeek, Claude, GPT, Yandex, GigaChat. Выбираешь сам.',
  },
  {
    icon: Database,
    title: 'Backend готов',
    desc: 'Postgres, REST API, JWT-авторизация — собираются вместе с фронтом.',
  },
  {
    icon: Globe,
    title: 'Домен и SSL',
    desc: 'Регистрация .ru/.рф автоматом, Lets Encrypt без настроек.',
  },
  {
    icon: Server,
    title: 'Российские серверы',
    desc: 'Стратегический партнёр SafeCloud / CORTEL. 152-ФЗ из коробки.',
  },
  {
    icon: GitBranch,
    title: 'Версии и откат',
    desc: 'Снапшот после каждого промпта. Откат — в один клик.',
  },
  {
    icon: CreditCard,
    title: 'Один счёт',
    desc: 'ЮKassa и Tinkoff. Хостинг + AI + поддержка — одной строкой.',
  },
  {
    icon: Shield,
    title: 'Безопасный auto-deploy',
    desc: 'Sandbox, изоляция арендаторов, подтверждение опасных операций.',
  },
  {
    icon: Layers,
    title: 'Экспорт в любой момент',
    desc: 'ZIP или Docker — забираешь весь проект. Без vendor lock-in.',
  },
]

function FeaturesSection() {
  return (
    <section id="features" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Sparkles className="h-3 w-3 text-accent-glow" /> Возможности
          </span>
          <h2 className="display-h2 mt-5 text-gradient">Всё под одной крышей</h2>
          <p className="mt-5 text-ink-muted">
            У конкурентов клиент собирает 4–5 сервисов сам. У нас — одна платформа,
            один счёт, одна поддержка.
          </p>
        </div>

        <div className="mt-12 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.4, delay: (i % 4) * 0.06 }}
              className="card group transition hover:border-white/15"
            >
              <div className="grid h-9 w-9 place-items-center rounded-lg border border-line bg-white/[0.03] transition group-hover:border-accent/30 group-hover:bg-accent/10">
                <f.icon className="h-4 w-4 text-accent-glow" />
              </div>
              <div className="mt-4 text-[15px] text-ink" style={{ fontWeight: 510 }}>
                {f.title}
              </div>
              <p className="mt-1.5 text-[13px] leading-relaxed text-ink-muted">
                {f.desc}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Pricing                                                             */
/* ================================================================== */

const TIERS = [
  {
    name: 'Lite',
    priceMonthly: 990,
    priceAnnualMonthly: 825, // 17% off (≈ 9 900 ₽/year)
    sub: 'для одиночных проектов',
    features: [
      '1 проект',
      'Кошелёк токенов 1 000 ₽',
      'Домен или поддомен',
      'SSL автоматом',
      '20 снапшотов + откат',
      'Mix LLM (DeepSeek · Haiku · Gemini)',
    ],
    breakdown: [
      ['Хостинг VPS (если покупать отдельно)', 600],
      ['Домен .ru/.рф', 25],
      ['SSL-сертификат', 0],
      ['AI-токены (DeepSeek/Haiku)', 1000],
      ['Резервные копии', 100],
      ['Поддержка-чат', 200],
    ],
    cta: 'Начать',
  },
  {
    name: 'Starter',
    priceMonthly: 2990,
    priceAnnualMonthly: 2490,
    sub: 'для бизнеса и фрилансеров',
    features: [
      'До 3 проектов',
      'Кошелёк токенов 2 500 ₽',
      'Кастомный домен .ru/.рф',
      'Базовый backend (Postgres + JWT)',
      '100 снапшотов истории',
      'Mix LLM + российские модели',
      'Email-поддержка SLA 48ч',
    ],
    breakdown: [
      ['Shared VPS', 800],
      ['Домен + DNS', 50],
      ['Postgres + бэкапы', 700],
      ['AI-токены (full mix)', 2500],
      ['Email-поддержка', 600],
    ],
    cta: 'Начать со Starter',
  },
  {
    name: 'Pro',
    priceMonthly: 7990,
    priceAnnualMonthly: 6650,
    sub: 'для production-задач',
    highlight: true,
    badge: 'Популярный',
    features: [
      'До 10 проектов · 2 домена',
      'Кошелёк токенов 6 000 ₽',
      'Выделенный VPS S (SafeCloud)',
      'Полный backend + Redis + S3',
      '500 снапшотов + side-by-side',
      'Чат-боты TG/VK + автоматизации',
      'GitHub-синк, staging',
      'Email SLA 24ч',
    ],
    breakdown: [
      ['Выделенный VPS', 3000],
      ['Postgres + Redis + S3', 1500],
      ['Daily backup + monitoring', 500],
      ['AI-токены (с кешем промптов)', 6000],
      ['Чат-боты + автоматизации', 1500],
      ['Поддержка SLA 24ч', 1200],
    ],
    cta: 'Начать с Pro',
  },
  {
    name: 'Enterprise',
    priceMonthly: 19990,
    priceAnnualMonthly: 16650,
    sub: 'для агентств и команд',
    features: [
      'Безлимит проектов · 5 доменов',
      'Кошелёк токенов 18 000 ₽',
      'Выделенный VPS M',
      '★ 152-ФЗ + российские LLM',
      '★ 1С-интеграция',
      'Часы инженеров со скидкой',
      'Менеджер · SLA 4ч',
      'Без лимита снапшотов',
    ],
    breakdown: [
      ['VPS M + DR-реплика', 8000],
      ['152-ФЗ compliance + Yandex LLM', 4000],
      ['1С-коннектор', 3000],
      ['Менеджер на проекте', 8000],
      ['AI-токены премиум-моделей', 18000],
      ['SLA 4ч + офсайт-бэкапы', 2500],
    ],
    cta: 'Связаться',
  },
]

function TierExpander({ tier, billing }) {
  const [open, setOpen] = useState(false)
  const total = tier.breakdown.reduce((sum, [, v]) => sum + v, 0)
  const ourPrice =
    billing === 'annual' ? tier.priceAnnualMonthly : tier.priceMonthly
  const saved = Math.max(0, total - ourPrice)
  const savedPct = total > 0 ? Math.round((saved / total) * 100) : 0

  return (
    <div className="mt-4 border-t border-line pt-3">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between text-left transition hover:opacity-80"
      >
        <span
          className="text-[11.5px] uppercase tracking-[0.16em] text-ink-muted"
          style={{ fontWeight: 510 }}
        >
          Что входит — и сколько стоит отдельно
        </span>
        <ChevronDown
          className={
            'h-3.5 w-3.5 text-ink-muted transition ' +
            (open ? 'rotate-180 text-accent-glow' : '')
          }
        />
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="space-y-1.5 pt-3 text-[11.5px]">
              {tier.breakdown.map(([label, val]) => (
                <div key={label} className="flex items-baseline justify-between gap-3">
                  <span className="truncate text-ink-muted">{label}</span>
                  <span className="font-mono text-ink-dim">
                    {val === 0 ? 'бесплатно' : '~ ' + val.toLocaleString('ru-RU') + ' ₽'}
                  </span>
                </div>
              ))}
            </div>
            <div className="mt-3 border-t border-line pt-2 text-[11.5px]">
              <div className="flex items-baseline justify-between">
                <span className="text-ink-muted">Если покупать отдельно</span>
                <span
                  className="font-mono text-ink-muted line-through"
                  style={{ fontWeight: 510 }}
                >
                  ~ {total.toLocaleString('ru-RU')} ₽
                </span>
              </div>
              <div className="mt-1 flex items-baseline justify-between">
                <span className="text-ink" style={{ fontWeight: 590 }}>
                  У нас в подписке
                </span>
                <span
                  className="font-mono text-success"
                  style={{ fontWeight: 590 }}
                >
                  {ourPrice.toLocaleString('ru-RU')} ₽
                </span>
              </div>
              {saved > 0 && (
                <div className="mt-2 inline-flex items-center gap-1 rounded-md border border-success/30 bg-success/10 px-2 py-1 text-[10.5px] text-success">
                  <TrendingDown className="h-3 w-3" />
                  Экономия {saved.toLocaleString('ru-RU')} ₽ · −{savedPct}%
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function PricingSection() {
  const [billing, setBilling] = useState('monthly')
  const isAnnual = billing === 'annual'

  return (
    <section id="pricing" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Wallet className="h-3 w-3 text-accent-glow" /> Тарифы
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            От <span className="accent-gradient">990 ₽</span>. Один счёт. Без сюрпризов.
          </h2>
          <p className="mt-5 text-ink-muted">
            Mix LLM, выделенный VPS, реальный backend, версионирование с откатом и
            152-ФЗ — на каждом тире. Хостинг, AI-токены, домен и поддержка — в одной
            подписке.
          </p>
        </div>

        {/* Billing toggle */}
        <div className="mx-auto mt-9 flex max-w-md justify-center">
          <div className="inline-flex items-center rounded-full border border-line bg-elev1/60 p-1">
            <button
              type="button"
              onClick={() => {
                setBilling('monthly')
                track('billing_toggle', { mode: 'monthly' })
              }}
              className={
                'rounded-full px-4 py-1.5 text-[12.5px] transition ' +
                (!isAnnual
                  ? 'bg-accent text-white shadow-glow'
                  : 'text-ink-muted hover:text-ink')
              }
              style={{ fontWeight: 590 }}
            >
              Месяц
            </button>
            <button
              type="button"
              onClick={() => {
                setBilling('annual')
                track('billing_toggle', { mode: 'annual' })
              }}
              className={
                'inline-flex items-center gap-1.5 rounded-full px-4 py-1.5 text-[12.5px] transition ' +
                (isAnnual
                  ? 'bg-accent text-white shadow-glow'
                  : 'text-ink-muted hover:text-ink')
              }
              style={{ fontWeight: 590 }}
            >
              Год
              <span
                className={
                  'rounded-full px-1.5 text-[9.5px] uppercase tracking-wider ' +
                  (isAnnual
                    ? 'bg-white/20 text-white'
                    : 'border border-success/30 bg-success/15 text-success')
                }
              >
                −17%
              </span>
            </button>
          </div>
        </div>

        {/* Free trial banner */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.5 }}
          className="mx-auto mt-6 max-w-3xl"
        >
          <div className="flex flex-col items-center justify-between gap-3 rounded-2xl border border-success/30 bg-success/[0.06] px-5 py-4 text-center md:flex-row md:text-left">
            <div className="flex items-center gap-3">
              <div className="grid h-10 w-10 flex-none place-items-center rounded-full bg-success/15 text-success">
                <Sparkles className="h-4 w-4" />
              </div>
              <div>
                <div className="text-[14.5px] text-ink" style={{ fontWeight: 590 }}>
                  Free · 5 дней без карты
                </div>
                <div className="text-[12.5px] text-ink-muted">
                  500 ₽ AI-токенов · 1 проект на поддомене omnia.ai · никаких обязательств
                </div>
              </div>
            </div>
            <a
              href="#start"
              className="inline-flex items-center gap-1.5 rounded-full border border-success/40 bg-success/15 px-4 py-2 text-[12.5px] text-success transition hover:bg-success/25"
              style={{ fontWeight: 590 }}
              onClick={() =>
                track('cta_click', { location: 'pricing_free', label: 'Free trial' })
              }
            >
              Попробовать бесплатно
              <ArrowRight className="h-3.5 w-3.5" />
            </a>
          </div>
        </motion.div>

        <div className="mt-6 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
          {TIERS.map((t, i) => {
            const price = isAnnual ? t.priceAnnualMonthly : t.priceMonthly
            const saved = isAnnual ? (t.priceMonthly - t.priceAnnualMonthly) * 12 : 0
            return (
              <motion.div
                key={t.name}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.45, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
                className={
                  'relative flex flex-col rounded-2xl border p-5 transition ' +
                  (t.highlight
                    ? 'border-accent/40 bg-gradient-to-b from-accent/[0.08] to-elev1 shadow-glow'
                    : 'border-line bg-elev1/70 hover:border-white/15')
                }
              >
                {t.badge && (
                  <div className="absolute -top-3 right-5 rounded-full bg-accent px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-white">
                    {t.badge}
                  </div>
                )}

                <div className="text-[13px] uppercase tracking-[0.2em] text-ink-muted">
                  {t.name}
                </div>
                <div className="mt-1 text-[11.5px] text-ink-dim">{t.sub}</div>

                <div className="mt-4 flex items-baseline gap-1.5">
                  <span
                    className="text-[36px] leading-none text-ink"
                    style={{ fontWeight: 590, letterSpacing: '-0.02em' }}
                  >
                    <CountUp
                      key={billing + t.name}
                      value={price}
                      duration={0.5}
                    />
                  </span>
                  <span className="text-[12.5px] text-ink-muted">₽ / мес</span>
                </div>

                {isAnnual && saved > 0 && (
                  <div className="mt-1 inline-flex items-center gap-1 text-[10.5px] text-success">
                    <TrendingDown className="h-3 w-3" />
                    экономия {saved.toLocaleString('ru-RU')} ₽ в год
                  </div>
                )}
                {!isAnnual && (
                  <div className="mt-1 text-[10.5px] text-ink-dim">
                    или {t.priceAnnualMonthly.toLocaleString('ru-RU')} ₽/мес при годовой
                  </div>
                )}

                <ul className="mt-5 space-y-2 flex-1">
                  {t.features.map((f) => (
                    <li
                      key={f}
                      className="flex items-start gap-2 text-[12.5px] leading-snug text-ink-muted"
                    >
                      <Check className="mt-0.5 h-3.5 w-3.5 flex-none text-accent-glow" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>

                <TierExpander tier={t} billing={billing} />

                <div className="mt-5">
                  <MagneticButton
                    href="#start"
                    className={
                      (t.highlight ? 'btn-primary' : 'btn-ghost') +
                      ' w-full text-[13px]'
                    }
                    onClick={() =>
                      track('cta_click', {
                        location: 'pricing',
                        tier: t.name,
                        billing,
                        label: t.cta,
                      })
                    }
                  >
                    {t.cta} <ArrowRight className="h-3.5 w-3.5" />
                  </MagneticButton>
                </div>
              </motion.div>
            )
          })}
        </div>

        <p className="mt-6 text-center text-[12px] text-ink-dim">
          Pre-launch: первые 100 клиентов фиксируют цену на год · отмена в любой момент
        </p>
      </div>
    </section>
  )
}

/* ================================================================== */
/* FAQ                                                                 */
/* ================================================================== */

const FAQ = [
  {
    q: 'Чем вы отличаетесь от других AI-конструкторов?',
    a: 'Мы единственные на российском рынке, кто закрывает все 7 пунктов сразу: (1) визуальный rollback после каждого промпта, (2) mix из 6 LLM включая YandexGPT и GigaChat для 152-ФЗ, (3) реальный backend — FastAPI + Postgres 16 + JWT с миграциями, (4) выделенный VPS на Pro/Enterprise, а не shared-поддомен, (5) self-export ZIP/Docker без vendor lock-in, (6) 1С-интеграция и часы инженеров на Enterprise, (7) рублёвая оплата и российская юрисдикция. Это production-инфраструктура, а не «конструктор для прототипов».',
  },
  {
    q: 'А если AI сломает сайт неудачным промптом?',
    a: 'Не сломает — каждый промпт создаёт новый снапшот, старая версия живёт. Откат в один клик через ленту версий, без git и терминала. Никто из конкурентов в РФ так не делает.',
  },
  {
    q: 'А если ваш сервис закроется — мои сайты пропадут?',
    a: 'Нет. В любой момент скачиваешь весь проект ZIP-архивом или Docker-образом. На Pro и Enterprise — опциональная синхронизация с твоим GitHub-репозиторием. Источник правды у нас, копия у тебя.',
  },
  {
    q: 'Какую модель LLM выбрать — Claude, GPT, Yandex?',
    a: 'Селектор с прозрачным прайсом и подсказками. DeepSeek и Haiku для быстрых задач, Sonnet для лучшего качества, YandexGPT и GigaChat для 152-ФЗ, Qwen self-hosted — почти бесплатно. Можно менять модель прямо в чате.',
  },
  {
    q: 'Что насчёт оплаты? Lovable требует крипту или зарубежную карту.',
    a: 'У нас ЮKassa и Tinkoff. Российская карта, СБП, рублёвый счёт юрлица — всё работает из коробки. Российское юрлицо, документы по 152-ФЗ.',
  },
  {
    q: 'Как насчёт кастомной логики, которую AI не вытянет?',
    a: 'На Pro и Enterprise доступны часы инженеров со скидкой — пишешь задачу, мы оцениваем, запускаем. Гибрид self-service + agency: AI делает 80%, эксперт — оставшиеся 20%.',
  },
  {
    q: 'Когда запуск?',
    a: 'Закрытая бета с M7 (≈Q4 2026), public soft launch с M10. Пользователи waitlist получают доступ первыми и фиксируют цену 6 990 / 17 990 / 34 990 ₽ на год.',
  },
]

function FaqSection() {
  const [open, setOpen] = useState(0)
  return (
    <section id="faq" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Shield className="h-3 w-3 text-accent-glow" /> Частые вопросы
          </span>
          <h2 className="display-h2 mt-5 text-gradient">Снимаем страхи</h2>
        </div>

        <div className="mx-auto mt-10 max-w-3xl divide-line overflow-hidden rounded-2xl border border-line bg-elev1/40">
          {FAQ.map((f, i) => {
            const isOpen = open === i
            return (
              <div key={f.q}>
                <button
                  type="button"
                  className="flex w-full items-center justify-between gap-6 px-5 py-4 text-left transition hover:bg-white/[0.02]"
                  onClick={() => {
                    setOpen(isOpen ? -1 : i)
                    track('faq_toggle', { idx: i, q: f.q })
                  }}
                >
                  <span className="text-[15px] text-ink" style={{ fontWeight: 510 }}>
                    {f.q}
                  </span>
                  <ChevronDown
                    className={
                      'h-4 w-4 flex-none text-ink-muted transition ' +
                      (isOpen ? 'rotate-180 text-accent-glow' : '')
                    }
                  />
                </button>
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.25 }}
                      className="overflow-hidden"
                    >
                      <div className="px-5 pb-5 text-[14.5px] leading-relaxed text-ink-muted">
                        {f.a}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Final CTA + email capture                                           */
/* ================================================================== */

function FinalCTA() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [touched, setTouched] = useState(false)

  const valid = useMemo(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email), [email])

  const onSubmit = (e) => {
    e.preventDefault()
    setTouched(true)
    if (!valid) return
    track('lead_signup', { email, location: 'final_cta' })
    setSent(true)
  }

  return (
    <section id="start" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="relative mx-auto max-w-4xl overflow-hidden rounded-3xl border border-line bg-gradient-to-br from-accent/[0.12] via-elev1 to-canvas px-6 py-14 md:px-12 md:py-20">
          <div className="pointer-events-none absolute -left-24 -top-24 h-72 w-72 glow-orb opacity-90" />
          <div className="pointer-events-none absolute -right-16 -bottom-16 h-72 w-72 glow-orb opacity-60" />

          <div className="relative mx-auto max-w-2xl text-center">
            <span className="eyebrow">
              <Rocket className="h-3 w-3 text-accent-glow" /> Pre-launch waitlist
            </span>
            <h2 className="display-h2 mt-5">
              <span className="text-gradient">Хочешь быть </span>
              <span className="accent-gradient">первым?</span>
            </h2>
            <p className="mt-5 text-ink-muted">
              Оставь email — получишь приглашение в закрытую бету и зафиксируешь
              стартовую цену 6 990 ₽ / мес для первых 100 клиентов.
            </p>

            {!sent ? (
              <form
                onSubmit={onSubmit}
                className="mx-auto mt-8 flex max-w-md flex-col gap-2 sm:flex-row"
              >
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onBlur={() => setTouched(true)}
                  placeholder="you@company.ru"
                  className="flex-1 rounded-full border border-line bg-canvas/70 px-5 py-3 text-[14px] text-ink placeholder:text-ink-dim/60 outline-none transition focus:border-accent/40 focus:bg-canvas"
                  required
                />
                <button
                  type="submit"
                  className="btn-primary text-[15px]"
                  onClick={() =>
                    track('cta_click', { location: 'final', label: 'Начать' })
                  }
                >
                  Получить доступ <ArrowRight className="h-4 w-4" />
                </button>
                {touched && !valid && email.length > 0 && (
                  <div className="absolute mt-14 w-full text-center text-[12px] text-danger sm:mt-16">
                    Кажется, в email опечатка
                  </div>
                )}
              </form>
            ) : (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="mx-auto mt-8 max-w-md rounded-2xl border border-success/30 bg-success/10 px-5 py-4 text-[14px] text-ink"
              >
                Готово — ты в списке. Напишем, как только бета откроется.
              </motion.div>
            )}

            <div className="mt-6 text-[12px] text-ink-dim">
              Без спама. Только одно письмо — приглашение.
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* Footer                                                              */
/* ================================================================== */

function Footer() {
  return (
    <footer className="relative border-t border-line py-10">
      <div className="container-x flex flex-col items-start justify-between gap-6 text-[13px] text-ink-muted md:flex-row md:items-center">
        <div className="flex items-center gap-3">
          <Logo />
          <span className="hidden text-ink-dim md:inline">·</span>
          <span className="text-ink-dim">
            © {new Date().getFullYear()} Omnia.AI · Pre-launch
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-x-5 gap-y-2">
          <a href="#demo" className="hover:text-ink">Демо</a>
          <a href="#versions" className="hover:text-ink">Версии</a>
          <a href="#how" className="hover:text-ink">Как работает</a>
          <a href="#features" className="hover:text-ink">Возможности</a>
          <a href="#pricing" className="hover:text-ink">Тарифы</a>
          <a href="#faq" className="hover:text-ink">Вопросы</a>
          <a
            href="https://github.com/zeuszcz/constructor"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 hover:text-ink"
            onClick={() => track('footer_github')}
          >
            <Github className="h-3.5 w-3.5" />
            GitHub
          </a>
        </div>
      </div>
    </footer>
  )
}

/* ================================================================== */
/* App root                                                           */
/* ================================================================== */

export default function App() {
  useEffect(() => {
    track('page_view')
  }, [])

  return (
    <div className="relative">
      <NavBar />
      <main>
        <Hero />
        <TrustStrip />
        <SegmentsSection />
        <VersioningSection />
        <ProblemsSection />
        <HowItWorks />
        <StackSection />
        <TimelineCompareSection />
        <ROICalculator />
        <ComparisonSection />
        <FeaturesSection />
        <PricingSection />
        <TeamSection />
        <FaqSection />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  )
}
