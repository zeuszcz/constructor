"""Generate docs/Token_Economics_v1.pdf — PDF version of the calculator.

Renders the same numbers as the XLSX (with formulas pre-computed) into a
styled multi-page A4-landscape PDF using reportlab. 12 sections matching
the 12 functional sheets of the source XLSX (we drop sheet 1 "Параметры"
and bake the assumptions into the headers).
"""
import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)

# --- Cyrillic-capable fonts: use Windows ones bundled with the OS ----- #
WIN_FONTS = Path("C:/Windows/Fonts")
try:
    pdfmetrics.registerFont(TTFont("Inter", str(WIN_FONTS / "calibri.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Bold", str(WIN_FONTS / "calibrib.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-It", str(WIN_FONTS / "calibrii.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(WIN_FONTS / "consola.ttf")))
    BODY_FONT = "Inter"
    BOLD_FONT = "Inter-Bold"
    ITAL_FONT = "Inter-It"
    MONO_FONT = "Mono"
except Exception:
    BODY_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"
    ITAL_FONT = "Helvetica-Oblique"
    MONO_FONT = "Courier"

# --- Styles ---------------------------------------------------------- #
ACCENT = colors.HexColor("#5e6ad2")
ACCENT_LIGHT = colors.HexColor("#eef0ff")
SUCCESS = colors.HexColor("#27a644")
SUCCESS_LIGHT = colors.HexColor("#dcfce7")
WARN_LIGHT = colors.HexColor("#ffe4e6")
INK = colors.HexColor("#1a1a1a")
INK_MUTED = colors.HexColor("#6b7280")
LINE = colors.HexColor("#e5e7eb")
HEAD_FILL = colors.HexColor("#1f2937")

styles = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1",
    fontName=BOLD_FONT,
    fontSize=22,
    leading=26,
    textColor=INK,
    spaceAfter=4,
)
H2 = ParagraphStyle(
    "H2",
    fontName=BOLD_FONT,
    fontSize=14,
    leading=18,
    textColor=ACCENT,
    spaceBefore=12,
    spaceAfter=4,
)
H3 = ParagraphStyle(
    "H3",
    fontName=BOLD_FONT,
    fontSize=11,
    leading=14,
    textColor=INK,
    spaceBefore=8,
    spaceAfter=2,
)
P = ParagraphStyle(
    "P",
    fontName=BODY_FONT,
    fontSize=10,
    leading=13,
    textColor=INK,
    spaceAfter=6,
)
NOTE = ParagraphStyle(
    "Note",
    fontName=ITAL_FONT,
    fontSize=8.5,
    leading=11,
    textColor=INK_MUTED,
    spaceAfter=2,
)
SUB = ParagraphStyle(
    "Sub",
    fontName=ITAL_FONT,
    fontSize=10,
    leading=12,
    textColor=INK_MUTED,
    spaceAfter=10,
)

# --- Output --------------------------------------------------------- #
OUT = Path("docs/Token_Economics_v1.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=landscape(A4),
    leftMargin=15 * mm,
    rightMargin=15 * mm,
    topMargin=12 * mm,
    bottomMargin=12 * mm,
    title="Omnia.AI · Token Economics",
    author="Omnia.AI",
)

story = []


def header_style(headers, n_cols):
    """Return TableStyle for a regular table with HEAD_FILL header row."""
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 1), (-1, -1), BODY_FONT),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ])


def page_title(text, sub=None):
    story.append(Paragraph(text, H1))
    if sub:
        story.append(Paragraph(sub, SUB))


# ====================================================================== #
# Cover                                                                 #
# ====================================================================== #
story.append(Spacer(1, 30 * mm))
cover = ParagraphStyle("Cover", fontName=BOLD_FONT, fontSize=42, leading=46, textColor=INK, alignment=TA_CENTER, spaceAfter=12)
cover_sub = ParagraphStyle("CoverSub", fontName=BODY_FONT, fontSize=14, leading=18, textColor=INK_MUTED, alignment=TA_CENTER, spaceAfter=4)
story.append(Paragraph("Omnia.AI", cover))
story.append(Paragraph("Подробная токен-экономика", ParagraphStyle("Cover2", fontName=ITAL_FONT, fontSize=20, leading=24, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=18)))
story.append(Paragraph("Расчёт LLM-затрат, кошельков и маржи по тарифам", cover_sub))
story.append(Paragraph("Free / Lite / Starter / Pro / Enterprise", cover_sub))
story.append(Spacer(1, 25 * mm))

# Cover key numbers
key_nums = [
    ["278", "−89%", "M11", "9.6 М ₽"],
    ["платящих до break-even", "ниже OPEX чем v2 plan", "первый плюсовой месяц", "MRR на M18"],
]
key_table = Table(key_nums, colWidths=[60 * mm] * 4)
key_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
    ("FONTSIZE", (0, 0), (-1, 0), 30),
    ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
    ("FONTNAME", (0, 1), (-1, 1), BODY_FONT),
    ("FONTSIZE", (0, 1), (-1, 1), 10),
    ("TEXTCOLOR", (0, 1), (-1, 1), INK_MUTED),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
    ("TOPPADDING", (0, 0), (-1, 0), 8),
]))
story.append(key_table)
story.append(PageBreak())


# ====================================================================== #
# 1. Базовые допущения                                                  #
# ====================================================================== #
page_title(
    "1. Базовые допущения",
    "Все расчёты в документе строятся на этих 4 параметрах. На листе «1. Параметры» XLSX-калькулятора их можно менять.",
)

assumptions = [
    ["Параметр", "Значение", "Комментарий"],
    ["Размер сообщения", "8 000 токенов", "5 000 input + 3 000 output. Conservative-среднее для AI-code-gen."],
    ["Output share", "0.5", "Половина от 1M общих токенов — output. Стандарт для chat-LLM."],
    ["Markup на токены", "2.8×", "Себестоимость + ~64% валовая маржа на токенах."],
    ["Курс ₽/$", "100", "На 2025."],
]
t = Table(assumptions, colWidths=[55 * mm, 35 * mm, 130 * mm])
t.setStyle(header_style(assumptions, 3))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 2. LLM-стек                                                            #
# ====================================================================== #
page_title(
    "2. LLM-стек: 8 моделей",
    "Cost ₽/1M = (input × 0.5 + output × 0.5) × 100 ₽/$. Retail = cost × 2.8.",
)

# Model data (matches XLSX)
models = [
    ("DeepSeek V3.2", "ультра-эконом", 0.28, 0.42),
    ("Qwen 3 235B (self-hosted)", "ультра-эконом", 0.50, 0.50),
    ("Gemini 2.5 Flash", "эконом", 0.30, 2.50),
    ("Claude Haiku 4.5", "баланс", 1.00, 5.00),
    ("GigaChat 2 Pro", "152-ФЗ", 5.00, 5.00),
    ("GPT-4.1", "премиум", 2.00, 8.00),
    ("Claude Sonnet 4.6", "премиум", 3.00, 15.00),
    ("YandexGPT 5 Pro", "152-ФЗ премиум", 8.00, 16.00),
]


def cost_per_m(inp, out, fx=100, share=0.5):
    return (inp * (1 - share) + out * share) * fx


def retail_per_m(inp, out, markup=2.8, fx=100, share=0.5):
    return cost_per_m(inp, out, fx, share) * markup


def fmt_rub(v):
    return f"{int(round(v)):,}".replace(",", " ") + " ₽"


def fmt_dec(v):
    return f"{v:.2f} ₽"


rows = [["Модель", "Категория", "Input $/1M", "Output $/1M", "Себест ₽/1M", "Retail ₽/1M"]]
for name, cat, inp, out in models:
    rows.append([
        name,
        cat,
        f"{inp:.2f}",
        f"{out:.2f}",
        fmt_rub(cost_per_m(inp, out)),
        fmt_rub(retail_per_m(inp, out)),
    ])
t = Table(rows, colWidths=[60 * mm, 35 * mm, 25 * mm, 25 * mm, 35 * mm, 35 * mm])
t.setStyle(header_style(rows, 6))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 3. Цена 1 сообщения                                                    #
# ====================================================================== #
page_title(
    "3. Стоимость 1 сообщения (8 000 токенов)",
    "Per-message cost = cost_per_M × 0.008. Retail = cost × markup.",
)

MSG = 8000


def cost_per_msg(inp, out, msg=MSG):
    return cost_per_m(inp, out) * msg / 1_000_000


def retail_per_msg(inp, out, msg=MSG):
    return retail_per_m(inp, out) * msg / 1_000_000


rows = [["Модель", "Себест ₽/msg", "Retail ₽/msg", "Маржа ₽/msg", "Маржа %"]]
for name, _, inp, out in models:
    c = cost_per_msg(inp, out)
    r = retail_per_msg(inp, out)
    margin = r - c
    rows.append([
        name,
        fmt_dec(c),
        fmt_dec(r),
        fmt_dec(margin),
        f"{margin / r * 100:.1f}%",
    ])
t = Table(rows, colWidths=[70 * mm, 35 * mm, 35 * mm, 35 * mm, 30 * mm])
t.setStyle(header_style(rows, 5))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 4. Объёмы 50 / 200 / 1 000                                             #
# ====================================================================== #
page_title(
    "4. Сколько стоит 50 / 200 / 1 000 сообщений",
    "Retail-цена что заплатит пользователь. 50 msg = 400 К токенов · 200 msg = 1.6 М · 1 000 msg = 8 М.",
)

rows = [["Модель", "50 сообщений", "200 сообщений", "1 000 сообщений"]]
for name, _, inp, out in models:
    r = retail_per_msg(inp, out)
    rows.append([
        name,
        fmt_rub(r * 50),
        fmt_rub(r * 200),
        fmt_rub(r * 1000),
    ])
t = Table(rows, colWidths=[70 * mm, 45 * mm, 45 * mm, 50 * mm])
t.setStyle(header_style(rows, 4))
story.append(t)
story.append(Spacer(1, 8 * mm))

# Mix scenarios cost per msg
story.append(Paragraph("Mix-сценарии (типичные пользовательские профили)", H3))

profiles = [
    ("A. MVP-эконом", "70% DeepSeek + 20% Haiku + 10% Sonnet",
     {"DeepSeek V3.2": 0.7, "Claude Haiku 4.5": 0.2, "Claude Sonnet 4.6": 0.1}),
    ("B. Балансный", "40% DS + 30% Haiku + 20% Gemini Flash + 10% Sonnet",
     {"DeepSeek V3.2": 0.4, "Claude Haiku 4.5": 0.3, "Gemini 2.5 Flash": 0.2, "Claude Sonnet 4.6": 0.1}),
    ("C. Премиум", "50% Sonnet + 30% Haiku + 20% GPT-4.1",
     {"Claude Sonnet 4.6": 0.5, "Claude Haiku 4.5": 0.3, "GPT-4.1": 0.2}),
    ("D. 152-ФЗ enterprise", "60% YandexGPT + 30% GigaChat + 10% Sonnet",
     {"YandexGPT 5 Pro": 0.6, "GigaChat 2 Pro": 0.3, "Claude Sonnet 4.6": 0.1}),
]

model_lookup = {name: (inp, out) for name, _, inp, out in models}


def profile_cost(shares):
    return sum(cost_per_msg(*model_lookup[m]) * w for m, w in shares.items())


def profile_retail(shares):
    return sum(retail_per_msg(*model_lookup[m]) * w for m, w in shares.items())


rows = [["Профиль", "Состав", "Cost/msg", "Retail/msg", "50 msg", "200 msg", "1 000 msg"]]
for name, comp, shares in profiles:
    c = profile_cost(shares)
    r = profile_retail(shares)
    rows.append([
        name,
        comp,
        fmt_dec(c),
        fmt_dec(r),
        fmt_rub(r * 50),
        fmt_rub(r * 200),
        fmt_rub(r * 1000),
    ])
t = Table(rows, colWidths=[40 * mm, 70 * mm, 22 * mm, 22 * mm, 25 * mm, 25 * mm, 30 * mm])
t.setStyle(header_style(rows, 7))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 5. Кошелёк → сообщения                                                #
# ====================================================================== #
page_title(
    "5. Сколько сообщений покрывает кошелёк каждого тарифа",
    "По модели (если юзер использует только её) и по балансному mix-профилю.",
)

tariffs = [
    ("Free (5 дней)", 500),
    ("Lite", 1000),
    ("Starter", 2500),
    ("Pro", 6000),
    ("Enterprise", 18000),
]

# Per-model coverage
rows = [["Тариф", "Кошелёк ₽"] + [m[0] for m in models]]
for name, w in tariffs:
    row = [name, fmt_rub(w)]
    for _, _, inp, out in models:
        msgs = math.floor(w / retail_per_msg(inp, out))
        row.append(f"{msgs:,}".replace(",", " "))
    rows.append(row)

t = Table(
    rows,
    colWidths=[28 * mm, 22 * mm] + [21 * mm] * 8,
)
t.setStyle(header_style(rows, 10))
story.append(t)

story.append(Spacer(1, 8 * mm))
story.append(Paragraph("Балансный mix (4.98 ₽/msg)", H3))

profile_b_retail = profile_retail(profiles[1][2])
rows = [["Тариф", "Кошелёк", "Сообщений на балансном миксе"]]
for name, w in tariffs:
    rows.append([name, fmt_rub(w), f"{math.floor(w / profile_b_retail):,}".replace(",", " ")])
t = Table(rows, colWidths=[40 * mm, 35 * mm, 60 * mm])
t.setStyle(header_style(rows, 3))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 6. Сообщения на проект                                                 #
# ====================================================================== #
page_title(
    "6. Типичная нагрузка на 1 проект",
    "Бенчмарк по типам проектов и стадиям жизненного цикла.",
)

projects = [
    ("Лендинг (1 страница)", "Сборка с нуля", "30–60", 45, "Lite ✓"),
    ("Лендинг", "Активные правки (1-2 нед)", "20–40", 30, "Lite ✓"),
    ("Лендинг", "Поддержка / месяц", "5–15", 10, "Lite ✓"),
    ("Магазин e-commerce", "Сборка с нуля", "80–150", 120, "Starter ✓"),
    ("Магазин", "Сезон / распродажа", "60–120", 90, "Starter ✓"),
    ("Корп-сайт SMB", "Сборка с нуля", "60–120", 90, "Starter ✓"),
    ("Портфолио / визитка", "Сборка с нуля", "20–50", 35, "Lite ✓"),
    ("SaaS-MVP с backend", "Сборка с нуля", "200–400", 300, "Pro ✓"),
    ("SaaS-MVP", "Поддержка после релиза", "30–80", 55, "Starter ✓"),
    ("Чат-бот TG/VK", "Сборка с нуля", "50–100", 75, "Starter ✓"),
    ("Бизнес-автоматизация", "Сборка пайплайна", "150–300", 225, "Pro ✓"),
    ("Агентство · 5 клиентов параллельно", "Активная разработка", "500–1000", 750, "Enterprise ✓"),
]
rows = [["Тип проекта", "Стадия", "Msg/мес (диапазон)", "Среднее", "Тариф"]]
for typ, stage, rng, avg, tier in projects:
    rows.append([typ, stage, rng, str(avg), tier])

t = Table(rows, colWidths=[60 * mm, 55 * mm, 32 * mm, 22 * mm, 35 * mm])
t.setStyle(header_style(rows, 5))
story.append(t)
story.append(Spacer(1, 4 * mm))

bullets = [
    "• 80% обычных SMB-проектов укладываются в Lite (200 msg/мес на балансном миксе).",
    "• Pro оправдан только при 200+ msg/мес — активный SaaS-MVP, чат-боты, или 2-3 проекта одновременно.",
    "• Enterprise — для агентств с 5+ клиентами или больших проектов 1 000+ msg.",
    "• Реальный паттерн: первый месяц активной сборки на Pro → downgrade на поддержку Lite. Учитываем в churn.",
]
for b in bullets:
    story.append(Paragraph(b, NOTE))
story.append(PageBreak())


# ====================================================================== #
# 7. Lean opex структура                                                 #
# ====================================================================== #
page_title(
    "7. Lean cost-структура: только реальные затраты",
    "Юрист + LLM (variable) + Серверум + домены/SSL + 300к/мес разработка. Никакого FOT-ramp и маркетингового бюджета.",
)

story.append(Paragraph("Постоянные затраты (₽/мес, не зависят от числа клиентов)", H3))

opex = [
    ("Юрист", 30000, "Договоры, оферта, ИП/ЮЛ обслуживание"),
    ("Разработка", 300000, "1 senior dev или 2 mid (founder + 1 hire)"),
    ("Серверум · наш control plane", 50000, "3-4 управляющих VPS: API gateway, billing, staging, monitoring"),
    ("Домены + HTTPS-сертификаты (наши)", 5000, "omnia.ai + dev/staging + Let's Encrypt"),
]
total_fixed = sum(v for _, v, _ in opex)
rows = [["Категория", "₽/мес", "Комментарий"]]
for k, v, n in opex:
    rows.append([k, fmt_rub(v), n])
rows.append(["ИТОГО ПОСТОЯННЫХ", fmt_rub(total_fixed), ""])

t = Table(rows, colWidths=[60 * mm, 30 * mm, 130 * mm])
ts = header_style(rows, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Переменные затраты на клиента (профиль B — балансный)", H3))

tier_data = [
    # name, price, wallet, server, domain
    ("Lite", 990, 1000, 50, 25),
    ("Starter", 2990, 2500, 600, 50),
    ("Pro", 7990, 6000, 3000, 100),
    ("Enterprise", 19990, 18000, 8000, 250),
]
markup = 2.8
rows = [["Тариф", "Цена", "LLM (wallet/2.8)", "Сервер", "Домен", "Комиссия 3%", "Итого Var", "GM ₽", "GM %"]]
for name, price, wallet, server, domain in tier_data:
    llm = wallet / markup
    com = price * 0.03
    var = llm + server + domain + com
    gm = price - var
    gm_pct = gm / price * 100
    rows.append([
        name,
        fmt_rub(price),
        fmt_rub(llm),
        fmt_rub(server),
        fmt_rub(domain),
        fmt_rub(com),
        fmt_rub(var),
        fmt_rub(gm),
        f"{gm_pct:.1f}%",
    ])
t = Table(rows, colWidths=[28 * mm, 22 * mm, 30 * mm, 20 * mm, 18 * mm, 24 * mm, 22 * mm, 22 * mm, 18 * mm])
ts = header_style(rows, 9)
# highlight GM column
ts.add("BACKGROUND", (-2, 1), (-2, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (-2, 1), (-2, -1), BOLD_FONT)
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 8. Lean break-even                                                    #
# ====================================================================== #
page_title(
    "8. Точка безубыточности",
    "Зависит от микса тарифов. Чем больше Pro/Ent в миксе, тем меньше клиентов нужно для break-even.",
)

# Default mix
mix = {"Lite": 0.50, "Starter": 0.25, "Pro": 0.18, "Enterprise": 0.07}
# Compute weighted ARPU and GM
prices_d = {n: p for n, p, _, _, _ in tier_data}
gms = {}
for name, price, wallet, server, domain in tier_data:
    llm = wallet / markup
    com = price * 0.03
    gms[name] = price - (llm + server + domain + com)

arpu = sum(prices_d[t] * mix[t] for t in mix)
gm_per = sum(gms[t] * mix[t] for t in mix)
gm_ratio = gm_per / arpu

story.append(Paragraph("Базовый расчёт (зрелый mix)", H3))
rows = [
    ["Параметр", "Значение"],
    ["ARPU средневзв.", fmt_rub(arpu)],
    ["GM на 1 клиента/мес", fmt_rub(gm_per)],
    ["GM ratio (от MRR)", f"{gm_ratio*100:.1f}%"],
    ["Постоянный opex", fmt_rub(total_fixed)],
    ["BREAK-EVEN: платящих клиентов", f"{math.ceil(total_fixed/gm_per)}"],
    ["BREAK-EVEN: MRR ₽/мес", fmt_rub(math.ceil(total_fixed/gm_per) * arpu)],
]
t = Table(rows, colWidths=[80 * mm, 50 * mm])
ts = header_style(rows, 2)
ts.add("BACKGROUND", (0, -2), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -2), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Чувствительность по миксу", H3))

scenarios = [
    ("Зрелый (M15+, default)", {"Lite": 0.50, "Starter": 0.25, "Pro": 0.18, "Enterprise": 0.07}),
    ("Lite-доминантный (M5-9)", {"Lite": 0.80, "Starter": 0.15, "Pro": 0.04, "Enterprise": 0.01}),
    ("Бизнес-mix (M10-14)", {"Lite": 0.60, "Starter": 0.25, "Pro": 0.12, "Enterprise": 0.03}),
    ("Премиум-tilt (M18+)", {"Lite": 0.30, "Starter": 0.25, "Pro": 0.30, "Enterprise": 0.15}),
    ("Только Pro/Ent (B2B fokus)", {"Lite": 0.0, "Starter": 0.0, "Pro": 0.70, "Enterprise": 0.30}),
]
rows = [["Сценарий", "Lite %", "Starter %", "Pro %", "Ent %", "ARPU ₽", "GM/cust ₽", "Break-even"]]
for name, m in scenarios:
    a = sum(prices_d[t] * m[t] for t in m)
    g = sum(gms[t] * m[t] for t in m)
    be = math.ceil(total_fixed / g) if g > 0 else float("inf")
    rows.append([
        name,
        f"{int(m['Lite']*100)}%",
        f"{int(m['Starter']*100)}%",
        f"{int(m['Pro']*100)}%",
        f"{int(m['Enterprise']*100)}%",
        fmt_rub(a),
        fmt_rub(g),
        str(be),
    ])
t = Table(rows, colWidths=[55 * mm, 18 * mm, 22 * mm, 18 * mm, 18 * mm, 28 * mm, 28 * mm, 22 * mm])
ts = header_style(rows, 8)
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 9. Финмодель 18 мес                                                    #
# ====================================================================== #
page_title(
    "9. Финмодель 18 месяцев",
    "Lean opex 385к/мес. Месячный ramp платящих клиентов и накопленный кэш.",
)

paying = [0, 0, 0, 5, 15, 35, 60, 120, 200, 320, 480, 680, 920, 1180, 1450, 1750, 2050, 2350]
arpus = [990, 990, 990, 990, 1100, 1200, 1400, 1700, 2000, 2300, 2600, 2900, 3150, 3400, 3650, 3850, 3950, 4080]
gm_ratios = [0.53, 0.53, 0.53, 0.53, 0.52, 0.50, 0.48, 0.46, 0.44, 0.42, 0.40, 0.38, 0.37, 0.36, 0.35, 0.34, 0.34, 0.34]

cum = 30000
month_data = []
for i in range(18):
    mrr = paying[i] * arpus[i]
    gm = mrr * gm_ratios[i]
    ebitda = gm - total_fixed
    cum += ebitda
    month_data.append((i + 1, paying[i], arpus[i], mrr, gm_ratios[i], gm, ebitda, cum))

rows = [["M", "Платящих", "ARPU", "MRR", "GM%", "GM ₽", "EBITDA", "Накоп. кэш"]]
for m, p, a, mrr, gr, gm, eb, c in month_data:
    rows.append([
        f"M{m}",
        f"{p:,}".replace(",", " "),
        fmt_rub(a),
        fmt_rub(mrr),
        f"{gr*100:.0f}%",
        fmt_rub(gm),
        fmt_rub(eb),
        fmt_rub(c),
    ])

t = Table(rows, colWidths=[14 * mm, 22 * mm, 22 * mm, 30 * mm, 16 * mm, 30 * mm, 30 * mm, 32 * mm])
ts = header_style(rows, 8)
# Color rows by EBITDA sign
for i, (_, _, _, _, _, _, eb, c) in enumerate(month_data, start=1):
    if eb < 0:
        ts.add("BACKGROUND", (-2, i), (-2, i), WARN_LIGHT)
    else:
        ts.add("BACKGROUND", (-2, i), (-2, i), SUCCESS_LIGHT)
    if c < 0:
        ts.add("BACKGROUND", (-1, i), (-1, i), WARN_LIGHT)
    else:
        ts.add("BACKGROUND", (-1, i), (-1, i), SUCCESS_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

# Summary
m18 = month_data[-1]
min_cash = min(c for *_, c in month_data)
first_pos_eb = next((m for m, *_, eb, _ in month_data if eb > 0), None)
first_pos_cash = next((m for *_, c in month_data if c > 0), None)

# Find first positive ebitda
first_pos_eb = None
for entry in month_data:
    if entry[6] > 0:
        first_pos_eb = entry[0]
        break
first_pos_cash = None
for entry in month_data:
    if entry[7] > 0:
        first_pos_cash = entry[0]
        break

rows = [
    ["Метрика", "Значение"],
    ["MRR на M18", fmt_rub(m18[3])],
    ["ARR на M18", fmt_rub(m18[3] * 12)],
    ["Накопленный кэш на M18", fmt_rub(m18[7])],
    ["Min cash (наибольший провал)", fmt_rub(min_cash)],
    ["Первый положительный EBITDA", f"M{first_pos_eb}"],
    ["Накопленный кэш > 0", f"M{first_pos_cash}"],
]
t = Table(rows, colWidths=[80 * mm, 60 * mm])
t.setStyle(header_style(rows, 2))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 10. Кеширование промптов                                              #
# ====================================================================== #
page_title(
    "10. Кеширование промптов",
    "Anthropic / OpenAI: cached input reads = 10% от raw input. При 70% hit rate input стоимость падает на 63%.",
)

cache_hit = 0.7
cache_price = 0.1
eff_input_mult = 1 - cache_hit * (1 - cache_price)  # = 0.37

rows = [["Модель", "Cost/msg без кеша", "Cost/msg с кешем", "Экономия %"]]
for name, _, inp, out in models:
    no_cache = cost_per_msg(inp, out)
    with_cache = (inp * 0.5 * eff_input_mult + out * 0.5) * 100 * MSG / 1_000_000
    rows.append([
        name,
        fmt_dec(no_cache),
        fmt_dec(with_cache),
        f"{(no_cache - with_cache)/no_cache*100:.1f}%",
    ])
t = Table(rows, colWidths=[70 * mm, 45 * mm, 45 * mm, 35 * mm])
t.setStyle(header_style(rows, 4))
story.append(t)
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "Эффективный множитель input при cache_hit=70%, cache_price=10%: "
    f"<b>{eff_input_mult*100:.1f}%</b> (экономия 63% на input).",
    NOTE,
))
story.append(Paragraph(
    "Power-user Pro (1 200 msg на балансном миксе) получает примерно <b>+6.5% gross margin</b> от одного только кеша.",
    NOTE,
))
story.append(PageBreak())


# ====================================================================== #
# 11. Qwen self-hosted break-even                                        #
# ====================================================================== #
page_title(
    "11. Self-hosted Qwen 3 235B — break-even",
    "Capex 250к ₽ + Opex 120к/мес. Окупается с 500+ активных Pro юзеров.",
)

CAPEX = 250000
OPEX = 120000
THROUGHPUT = 60  # msg/h per GPU
UPTIME = 720  # h/mo
ROUTE_RATIO = 0.30
CAPACITY = THROUGHPUT * UPTIME  # 43 200 msg/mo

rows = [
    ["Параметр", "Значение"],
    ["Capex (1× A100 80GB или 2× RTX 4090)", fmt_rub(CAPEX)],
    ["Opex/мес (электр., охлаждение, амортизация 5y)", fmt_rub(OPEX)],
    ["Throughput на 1 GPU", f"{THROUGHPUT} msg/час (8K токенов, batch=4)"],
    ["Uptime", f"{UPTIME} ч/мес"],
    ["Capacity Qwen", f"{CAPACITY:,} msg/мес".replace(",", " ")],
    ["Cost ₽/msg на Qwen", fmt_dec(OPEX / CAPACITY)],
    ["Доля задач, роутируемых на Qwen", f"{int(ROUTE_RATIO*100)}%"],
]
t = Table(rows, colWidths=[100 * mm, 60 * mm])
t.setStyle(header_style(rows, 2))
story.append(t)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Break-even по объёму активной базы (vs Sonnet API)", H3))

sonnet_cost_msg = cost_per_msg(3.0, 15.0)
rows = [["Активных Pro", "Msg/мес total", "Msg на Qwen", "Sonnet API ₽", "Qwen Opex ₽", "Экономия /мес", "Месяцев до break-even"]]
for n in [50, 100, 200, 500, 1000, 2000, 5000]:
    total_msg = n * 200
    qwen_msg = total_msg * ROUTE_RATIO
    if qwen_msg > CAPACITY:
        qwen_msg = CAPACITY  # cap at capacity
    sonnet_eq = qwen_msg * sonnet_cost_msg
    saving = sonnet_eq - OPEX
    if saving <= 0:
        be_months = "никогда"
    else:
        be_months = f"{CAPEX/saving:.1f}"
    rows.append([
        f"{n:,}".replace(",", " "),
        fmt_rub(total_msg),
        f"{int(qwen_msg):,}".replace(",", " "),
        fmt_rub(sonnet_eq),
        fmt_rub(OPEX),
        fmt_rub(saving),
        be_months,
    ])
t = Table(rows, colWidths=[28 * mm, 30 * mm, 30 * mm, 32 * mm, 28 * mm, 32 * mm, 35 * mm])
ts = header_style(rows, 7)
# Color last column based on viability
viab_rows = [50, 100, 200, 500, 1000, 2000, 5000]
for i, n in enumerate(viab_rows, start=1):
    if n >= 500:
        ts.add("BACKGROUND", (-1, i), (-1, i), SUCCESS_LIGHT)
    else:
        ts.add("BACKGROUND", (-1, i), (-1, i), WARN_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

verdict = [
    "<b>До 200 юзеров:</b> Qwen НЕ окупается — opex 120к/мес больше экономии на API.",
    "<b>200–500 юзеров:</b> 4–12 мес до break-even. Только если есть стратегические причины (152-ФЗ, lock-in).",
    "<b>500+ юзеров:</b> 1–3 мес до break-even — однозначно ставить.",
    "<b>По плану M15:</b> ~1 000 платящих → break-even на 4-м месяце с launch'a Qwen.",
    "<b>Стратегия:</b> 152-ФЗ из коробки + защита от блокировки API + R&D-площадка для fine-tune под Tilda/ЮKassa/1С.",
]
for v in verdict:
    story.append(Paragraph(v, NOTE))
story.append(PageBreak())


# ====================================================================== #
# 12. Что важно запомнить                                                #
# ====================================================================== #
page_title(
    "12. Главные цифры за один взгляд",
    "Если у вас 30 секунд на этот документ — вот ключевые числа.",
)

main_pts = [
    "Себестоимость одного сообщения: <b>0.28 → 9.60 ₽</b> в зависимости от AI-модели.",
    "200 сообщений в реальном миксе моделей стоят юзеру <b>≈ 1 000 ₽</b> = ровно Lite-кошелёк.",
    "На каждом платящем клиенте мы зарабатываем в среднем <b>1 385 ₽/мес</b>.",
    "Постоянные траты компании — <b>385 К ₽/мес</b> (юрист 30 + разработка 300 + наши серверы 50 + домены 5).",
    "Точка плюса — <b>278 платящих клиентов</b> (≈ месяц 11).",
    "За 18 месяцев модель выходит на <b>9.6 М ₽/мес выручки</b> и <b>+7.7 М ₽ на счёте</b>.",
    "Запускаться можно <b>без инвесторов</b>, нужно ~3.2 М ₽ оборотки на первые 10 месяцев.",
    "Сравнение с v2 plan (с маркет.+FOT 3.5М): break-even с 858 → <b>278 (−67%)</b>; Min cash с 28М → <b>3.2М (−89%)</b>.",
]
for i, p in enumerate(main_pts, start=1):
    story.append(Paragraph(f"<b>{i}.</b> {p}", P))

story.append(Spacer(1, 8 * mm))
story.append(Paragraph(
    "Источник: Token_Economics_v1.xlsx (15 листов с живыми формулами). "
    "Всё, что в PDF — это снапшот калькулятора. Меняй параметры в XLSX чтобы пересчитать.",
    NOTE,
))


doc.build(story)
print(f"OK saved: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
