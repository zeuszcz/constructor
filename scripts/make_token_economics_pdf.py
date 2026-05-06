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
    ["30/30/10/30", "M7", "M9", "60 М ₽"],
    ["структура расходов %", "первая прибыль", "вернули вложенное", "на счёте к M24"],
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
    "Себестоимость 1 миллиона токенов = (цена input × 0.5 + цена output × 0.5) × 100 ₽/$. Цена клиенту = себестоимость × 2.8.",
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


rows = [["AI-модель", "Категория", "Цена input $/1M", "Цена output $/1M", "Себест ₽/1M", "Цена клиенту ₽/1M"]]
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
    "Себестоимость 1 сообщения = себестоимость 1 миллиона × 0.008 (8К токенов). Цена клиенту = себестоимость × 2.8.",
)

MSG = 8000


def cost_per_msg(inp, out, msg=MSG):
    return cost_per_m(inp, out) * msg / 1_000_000


def retail_per_msg(inp, out, msg=MSG):
    return retail_per_m(inp, out) * msg / 1_000_000


rows = [["AI-модель", "Себест ₽ за сообщение", "Цена клиенту", "Маржа ₽", "Маржа %"]]
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
    "Цена что заплатит пользователь. 50 сообщений = 400 К токенов · 200 = 1.6 М · 1 000 = 8 М.",
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


rows = [["Профиль", "Состав", "Себест/сообщ", "Цена клиенту", "50 сообщ", "200 сообщ", "1 000 сообщ"]]
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
    "• 80% обычных SMB-проектов укладываются в Lite (200 сообщ/мес на балансном миксе).",
    "• Pro оправдан только при 200+ сообщ/мес — активный SaaS-MVP, чат-боты, или 2-3 проекта одновременно.",
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
    "7. Структура расходов: 30% / 30% / 10% / 30% от выручки",
    "Все расходы привязаны к выручке как фиксированная доля. Это упрощает планирование и масштабируется автоматически.",
)

story.append(Paragraph("4 категории расходов как % от выручки", H3))

cost_structure = [
    ["Категория", "Доля от выручки", "Что входит"],
    ["Зарплаты", "30% (минимум 30 К/мес)",
     "Юрист + основатели/команда. В первые месяцы при низкой выручке держим минимум 30 К."],
    ["Токены + наша инфра", "30%",
     "Платежи Anthropic/OpenAI/Yandex за AI + наши сервера, БД, бэкапы, мониторинг, CDN, защита от атак."],
    ["Бэкофис: VPS клиентов + домены", "10%",
     "Серверум за сайт каждого клиента + его домен + HTTPS + операционные мелочи."],
    ["Маркетинг и реклама", "Фиксированный бюджет",
     "100→300 К/мес. Не % от выручки, а отдельный план: M2-M5=100К, M6-M9=150К, M10-M14=200К, M15-M20=250К, M21-M24=300К."],
    ["ОПЕРАЦИОННАЯ ПРИБЫЛЬ", "30% выручки − маркетинг",
     "Что остаётся после всех расходов. На зрелости (M15+) это становится ~25-28% от выручки."],
]
t = Table(cost_structure, colWidths=[55 * mm, 50 * mm, 110 * mm])
ts = header_style(cost_structure, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Почему такая структура работает:</b> расходы автоматически масштабируются с выручкой. "
    "Когда клиентов мало — расходы небольшие, когда много — растут пропорционально. "
    "В первые месяцы зарплата держится на минимальных 30 К (юрист + минимум основателю), "
    "пока выручка не позволит платить нормально команде.",
    NOTE,
))
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Что покрывают токены+инфра (30% от выручки)", H3))

infra_brackets = [
    ["Размер базы", "30% от выручки в мес ₽", "Что покрывает"],
    ["10 платящих", "≈ 3 000", "AI-токены + минимальная инфра"],
    ["165 платящих", "≈ 60 000", "Токены + primary БД + бэкапы"],
    ["480 платящих", "≈ 245 000", "Токены + копия БД + Redis + мониторинг"],
    ["1 100 платящих", "≈ 860 000", "Кластер + аварийное восстановление"],
    ["2 710 платящих", "≈ 3.1 М", "Multi-region бэкапы + защита от атак"],
    ["6 250 платящих", "≈ 7.8 М", "Premium ops + дежурный инженер"],
]
t = Table(infra_brackets, colWidths=[40 * mm, 40 * mm, 130 * mm])
t.setStyle(header_style(infra_brackets, 3))
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Переменные затраты на клиента (профиль B — балансный)", H3))

tier_data = [
    # name, price, wallet, server, domain
    ("Lite", 990, 1000, 50, 25),
    ("Starter", 2990, 2500, 600, 50),
    ("Pro", 7990, 6000, 3000, 100),
    ("Enterprise", 19990, 18000, 8000, 250),
]
markup = 2.8
rows = [["Тариф", "Цена", "Затраты на AI (кошелёк ÷ 2.8)", "Сервер", "Домен", "Комиссия 3%", "Все затраты", "Маржа ₽", "Маржа %"]]
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
    "8. Точка безубыточности (с новой структурой 30/30/10/30)",
    "В новой модели расходы привязаны к выручке (зарплаты 30% + токены/инфра 30% + бэкофис 10% = 70%). До маркетинга на каждом рубле выручки остаётся 30 коп. чистого. Маркетинг поверх — фиксированный бюджет.",
)

# Mix распределения тарифов
mix = {"Lite": 0.50, "Starter": 0.25, "Pro": 0.18, "Enterprise": 0.07}
# Считаем средний доход и маржу по миксу (используется для оценки на одного клиента)
prices_d = {n: p for n, p, _, _, _ in tier_data}
gms = {}
for name, price, wallet, server, domain in tier_data:
    llm = wallet / markup
    com = price * 0.03
    gms[name] = price - (llm + server + domain + com)

arpu = sum(prices_d[t] * mix[t] for t in mix)
gm_per = sum(gms[t] * mix[t] for t in mix)
gm_ratio = gm_per / arpu

# В новой модели операционная прибыль = 30% × выручка - маркетинг
# Точка безубыточности: 0.30 × ARPU × N = маркетинг → N = маркетинг / (0.30 × ARPU)
# Где: 30% — операционная прибыль до маркетинга, ARPU = средний доход с клиента
op_margin_pct = 0.30  # после зарплат+токенов+бэкофиса остаётся 30%

story.append(Paragraph("Базовый расчёт (зрелый микс M15+)", H3))
rows = [
    ["Параметр", "Значение"],
    ["Средний доход с клиента в месяц", fmt_rub(arpu)],
    ["Операционная маржа после 30/30/10", f"{op_margin_pct*100:.0f}% (30% от выручки)"],
    ["Маркетинговый бюджет на M15-M20", fmt_rub(250000)],
    ["Точка безубыточности: платящих клиентов", f"{math.ceil(250000 / (op_margin_pct * arpu))}"],
    ["Точка безубыточности: выручка ₽/мес", fmt_rub(math.ceil(250000 / (op_margin_pct * arpu)) * arpu)],
]
t = Table(rows, colWidths=[80 * mm, 50 * mm])
ts = header_style(rows, 2)
ts.add("BACKGROUND", (0, -2), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -2), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Чувствительность по миксу тарифов", H3))

scenarios = [
    ("Зрелый (M15+, основной)", {"Lite": 0.50, "Starter": 0.25, "Pro": 0.18, "Enterprise": 0.07}),
    ("Lite-доминантный (M5-9)", {"Lite": 0.80, "Starter": 0.15, "Pro": 0.04, "Enterprise": 0.01}),
    ("Бизнес-микс (M10-14)", {"Lite": 0.60, "Starter": 0.25, "Pro": 0.12, "Enterprise": 0.03}),
    ("Премиум-перекос (M18+)", {"Lite": 0.30, "Starter": 0.25, "Pro": 0.30, "Enterprise": 0.15}),
    ("Только Pro/Enterprise (фокус на бизнес)", {"Lite": 0.0, "Starter": 0.0, "Pro": 0.70, "Enterprise": 0.30}),
]
rows = [["Сценарий", "Lite %", "Starter %", "Pro %", "Ent %", "Доход с клиента", "Опер. маржа", "Клиентов до плюса"]]
for name, m in scenarios:
    a = sum(prices_d[t] * m[t] for t in m)
    op_margin = a * op_margin_pct  # 30% от ARPU = операционная маржа на 1 клиента
    be = math.ceil(250000 / op_margin) if op_margin > 0 else float("inf")
    rows.append([
        name,
        f"{int(m['Lite']*100)}%",
        f"{int(m['Starter']*100)}%",
        f"{int(m['Pro']*100)}%",
        f"{int(m['Enterprise']*100)}%",
        fmt_rub(a),
        fmt_rub(op_margin),
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
    "9. Финмодель 24 месяца · структура 30/30/10/30 + маркет.реальность",
    "Платящие пересчитаны под маркетинг 2026: M2 = 10 (вместо 30), к M7+ догоняет план. Расходы привязаны к выручке: зарплаты 30%, токены+инфра 30%, бэкофис 10%, операц.доход 30% (минус маркетинг).",
)

paying = [
    0,
    10, 30, 75, 165,                         # M2-M5 (маркетинговая реальность)
    300, 480, 660, 870,                      # M6-M9 (М7+ начинает догонять)
    1100, 1380, 1670, 1980, 2330,            # M10-M14 (полностью догнал)
    2710, 3120, 3550, 4000,                  # M15-M18
    4400, 4800, 5200, 5550, 5900, 6250,      # M19-M24
]
arpus = [
    0,
    990, 990, 1100, 1200,
    1400, 1700, 2000, 2300,
    2600, 2900, 3150, 3400, 3650,
    3850, 3950, 4030, 4080,
    4080, 4100, 4120, 4140, 4150, 4160,
]
marketing_per_month = [
    0,
    100000, 100000, 100000, 100000,
    150000, 150000, 150000, 150000,
    200000, 200000, 200000, 200000, 200000,
    250000, 250000, 250000, 250000,
    250000, 250000, 300000, 300000, 300000, 300000,
]

# Новая структура расходов: % от выручки
SALARY_FLOOR = 30000  # Минимум зарплат в первые месяцы
SALARY_PCT = 0.30     # Зарплаты 30% выручки
TOKENS_INFRA_PCT = 0.30  # Токены + инфра 30%
BACKOFFICE_PCT = 0.10    # Бэкофис 10%

cum = 30000
month_data = []
for i in range(24):
    mrr = paying[i] * arpus[i]
    salaries = max(SALARY_FLOOR, SALARY_PCT * mrr)
    tokens_infra = TOKENS_INFRA_PCT * mrr
    backoffice = BACKOFFICE_PCT * mrr
    mkt = marketing_per_month[i]
    total_opex = salaries + tokens_infra + backoffice + mkt
    profit = mrr - total_opex
    cum += profit
    month_data.append((
        i + 1, paying[i], mrr, salaries, tokens_infra, backoffice, mkt, profit, cum,
    ))

rows = [["Мес", "Платящ", "Выручка", "Зарплаты", "Токен+Инф", "Бэкофис", "Маркет", "Прибыль", "На счёте"]]
for m, p, mrr, sal, ti, bo, mkt, pr, c in month_data:
    rows.append([
        f"M{m}",
        f"{p:,}".replace(",", " "),
        fmt_rub(mrr),
        fmt_rub(sal),
        fmt_rub(ti),
        fmt_rub(bo),
        fmt_rub(mkt),
        fmt_rub(pr),
        fmt_rub(c),
    ])

t = Table(
    rows,
    colWidths=[12 * mm, 17 * mm, 28 * mm, 26 * mm, 26 * mm, 24 * mm, 22 * mm, 28 * mm, 30 * mm],
)
ts = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
    ("FONTSIZE", (0, 0), (-1, 0), 8),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, -1), BODY_FONT),
    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
    ("TEXTCOLOR", (0, 1), (-1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
    ("TOPPADDING", (0, 0), (-1, 0), 4),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 1), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
])
# Цветовая разметка по знаку прибыли и счёта
for i, entry in enumerate(month_data, start=1):
    pr = entry[7]
    c = entry[8]
    if pr < 0:
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

# Сводка
m24 = month_data[-1]
min_cash = min(entry[8] for entry in month_data)
first_pos_pr = None
for entry in month_data:
    if entry[7] > 0:
        first_pos_pr = entry[0]
        break
first_pos_cash = None
for entry in month_data:
    if entry[8] > 0 and entry[0] > 1:
        first_pos_cash = entry[0]
        break

mkt_total = sum(marketing_per_month)
sal_total = sum(entry[3] for entry in month_data)
ti_total = sum(entry[4] for entry in month_data)
bo_total = sum(entry[5] for entry in month_data)
rows = [
    ["Метрика", "Значение"],
    ["Выручка в мес на M24", fmt_rub(m24[2])],
    ["Выручка в год на M24", fmt_rub(m24[2] * 12)],
    ["Деньги на счёте на M24", fmt_rub(m24[8])],
    ["Самый большой минус по деньгам", fmt_rub(min_cash)],
    ["Первый плюсовой месяц (прибыль > расходов)", f"M{first_pos_pr}"],
    ["Когда вернули вложенные деньги (счёт > 0)", f"M{first_pos_cash}"],
    ["Маркетинг суммарно за 24 мес", fmt_rub(mkt_total)],
    ["Зарплаты суммарно за 24 мес", fmt_rub(sal_total)],
    ["Токены + инфра суммарно за 24 мес", fmt_rub(ti_total)],
    ["Бэкофис суммарно за 24 мес", fmt_rub(bo_total)],
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

rows = [["AI-модель", "Себест/сообщ без кеша", "Себест/сообщ с кешем", "Экономия %"]]
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
    "11. Свой AI-сервер Qwen 3 235B — когда окупится",
    "Покупка железа 250к ₽ + текущие траты 120к/мес. Окупается с 500+ активных Pro клиентов.",
)

CAPEX = 250000
OPEX = 120000
THROUGHPUT = 60  # msg/h per GPU
UPTIME = 720  # h/mo
ROUTE_RATIO = 0.30
CAPACITY = THROUGHPUT * UPTIME  # 43 200 msg/mo

rows = [
    ["Параметр", "Значение"],
    ["Покупка железа (1× A100 80GB или 2× RTX 4090)", fmt_rub(CAPEX)],
    ["Текущие траты в месяц (электричество + охлаждение + износ за 5 лет)", fmt_rub(OPEX)],
    ["Производительность на 1 видеокарту", f"{THROUGHPUT} сообщений/час (8K токенов)"],
    ["Часов работы в месяц", f"{UPTIME} ч/мес"],
    ["Сколько сообщений может обработать в месяц", f"{CAPACITY:,} сообщений".replace(",", " ")],
    ["Себестоимость 1 сообщения на Qwen", fmt_dec(OPEX / CAPACITY)],
    ["Доля задач, отправляемых на Qwen", f"{int(ROUTE_RATIO*100)}%"],
]
t = Table(rows, colWidths=[100 * mm, 60 * mm])
t.setStyle(header_style(rows, 2))
story.append(t)
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("Когда окупится: зависит от количества активных Pro-клиентов (сравнение со стоимостью Sonnet через API)", H3))

sonnet_cost_msg = cost_per_msg(3.0, 15.0)
rows = [["Активных Pro", "Сообщений/мес всего", "Сообщений на Qwen", "Если бы Sonnet, ₽", "Текущие на Qwen, ₽", "Экономия в мес", "Месяцев до окупаемости"]]
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
    "<b>До 200 клиентов:</b> Qwen НЕ окупается — текущие траты 120к/мес больше экономии на API.",
    "<b>200–500 клиентов:</b> 4–12 мес до окупаемости. Только если есть стратегические причины (закон 152-ФЗ, защита от блокировки).",
    "<b>500+ клиентов:</b> 1–3 мес до окупаемости — однозначно стоит ставить.",
    "<b>По плану на M15:</b> ~1 000 платящих → окупится на 4-м месяце после запуска Qwen.",
    "<b>Зачем вообще:</b> закон 152-ФЗ из коробки + защита от блокировки западных AI + площадка для дообучения под Tilda/ЮKassa/1С.",
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
    "200 сообщений в реальном миксе моделей стоят пользователю <b>≈ 1 000 ₽</b> = ровно Lite-кошелёк.",
    "На каждом платящем клиенте мы зарабатываем в среднем <b>1 385 ₽/мес</b>.",
    "Структура расходов привязана к выручке: <b>30% зарплаты + 30% токены/инфра + 10% бэкофис</b>. Это автоматически масштабируется без переплат на старте.",
    "Маркетинг отдельно фиксированно: 100 → 300 К/мес. С учётом маркет.реальности 2026 платящие медленнее в M2-M5 (10 → 165 вместо 30 → 250), к M7+ догоняют план.",
    "Прибыль покрывает все расходы уже на <b>месяце 7</b> при 480 платящих. Возврат вложений — на <b>месяце 9</b> (870 платящих).",
    "За 24 месяца модель выходит на <b>26 М ₽/мес выручки</b> (~312 М в год) и <b>+60 М ₽ на счёте</b>.",
    "Самый большой минус — всего <b>~380 К ₽</b> на месяце 6. Это <b>в 6 раз меньше</b> чем при найме команды на оклад без % от выручки.",
    "Запускаться можно <b>без инвесторов и почти без денег</b>: 30 К ₽ хватит на месяц 1, далее нужно ~380 К запас на 5 месяцев минуса.",
]
for i, p in enumerate(main_pts, start=1):
    story.append(Paragraph(f"<b>{i}.</b> {p}", P))

story.append(Spacer(1, 8 * mm))
story.append(Paragraph(
    "Источник: Token_Economics_v1.xlsx (16 листов с живыми формулами). "
    "Всё, что в PDF — это снапшот калькулятора. Меняй параметры в XLSX чтобы пересчитать.",
    NOTE,
))
story.append(PageBreak())


# ====================================================================== #
# 13. Маркетинг 2026 — контекст + чистые vs грязные запросы              #
# ====================================================================== #
page_title(
    "13. Маркетинг 2026 · только чистые таргетированные запросы",
    "После ухода Google Ads (2022) и AI-хайпа 2024-2025 цены в Яндекс.Директ выросли. Принцип: брать ТОЛЬКО запросы с явным намерением купить — отраслевые / AI / боль-ориентированные / сравнение.",
)

story.append(Paragraph("Что НЕ берём в семантическое ядро (грязные запросы)", H3))
dirty = [
    ["Запрос", "Показов/мес", "Почему НЕ берём"],
    ["тильда", "200 000", "Лояльность к Tilda. Конверсия в нас ~0%."],
    ["создать сайт", "80 000", "Слишком общий. 70% — школьники + охотники за халявой + любопытные без бюджета."],
    ["сделать сайт", "70 000", "То же + ещё больше «сделай сам без денег»."],
    ["сайт бесплатно", "40 000", "Прямо в названии «бесплатно» — НЕ наша аудитория."],
    ["конструктор сайтов", "25 000", "Общий, дорогой аукцион (165 ₽), Tilda+Bitrix-лояльность."],
    ["сайт визитка", "12 000", "Общий. «Визитка» без отрасли = бабушка хочет визитку."],
    ["bitrix сайт сделать", "4 500", "Лояльность к Bitrix. Конверсия в смену стека ~1%."],
    ["сайт магазина бесплатно", "1 500", "Снова «бесплатно»."],
]
t = Table(dirty, colWidths=[55 * mm, 30 * mm, 130 * mm])
ts = header_style(dirty, 3)
ts.add("BACKGROUND", (0, 1), (-1, -1), WARN_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Что мы потеряли:</b> 433 000 показов/мес «потенциального» трафика. "
    "<b>Что выиграли:</b> бюджет идёт в кампании где нажимаемость × конверсия посадочной × переход в платящего в 2-3 раза выше. "
    "На 100К это +50-100% платящих клиентов.",
    NOTE,
))
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Маркеры чистого vs грязного запроса", H3))
markers = [
    ["Чистые ✓", "Грязные ✗"],
    ["Отрасль («сайт юриста», «сайт для кафе»)", "Слово «бесплатно» в запросе"],
    ["Боль-ориентированные («сайт без программиста»)", "Общий без отрасли («создать сайт»)"],
    ["AI-специфичные («нейросеть сайт»)", "Бренд конкурента целиком («тильда»)"],
    ["Сравнение вариантов («tilda аналог», «wix или tilda»)", "Любые запросы с >50 000 показов/мес — слишком широко"],
    ["Намерение купить («сайт под ключ», «лендинг создать»)", "Фразы лояльности конкурентов («битрикс сайт»)"],
]
t = Table(markers, colWidths=[100 * mm, 110 * mm])
ts = header_style(markers, 2)
ts.add("BACKGROUND", (0, 0), (0, 0), SUCCESS_LIGHT)
ts.add("BACKGROUND", (1, 0), (1, 0), WARN_LIGHT)
ts.add("TEXTCOLOR", (0, 0), (0, 0), INK)
ts.add("TEXTCOLOR", (1, 0), (1, 0), INK)
t.setStyle(ts)
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 14. Семантическое ядро · 63 чистых запроса                              #
# ====================================================================== #
page_title(
    "14. Семантическое ядро · 63 чистых запроса · Wordstat 2026",
    "Только запросы с намерением купить. Простая средняя цена клика 93 ₽ · взвешенная по показам 107 ₽ · суммарно 141 050 показов/мес.",
)

# Aggregates
agg = [
    ["Категория", "Ключей", "Показов/мес", "Средняя цена клика ₽"],
    ["A. Намерение купить", "5", "47 500", "98"],
    ["B. AI ★ ПРИОРИТЕТ", "9", "16 650", "85"],
    ["C. Сравнение вариантов", "4", "4 000", "72"],
    ["D. Кафе / Общепит", "6", "11 900", "78"],
    ["E. Интернет-магазин", "5", "20 600", "121"],
    ["F. Юрист", "5", "5 300", "102"],
    ["G. Красота", "5", "7 800", "78"],
    ["H. Медицина", "5", "7 300", "124"],
    ["I. Авто", "4", "3 100", "85"],
    ["J. Недвижимость", "4", "4 100", "135"],
    ["K. Образование", "5", "7 500", "87"],
    ["L. Боль-ориентированные ★", "6", "5 300", "72"],
    ["ИТОГО", "63", "141 050", "93"],
]
t = Table(agg, colWidths=[60 * mm, 25 * mm, 35 * mm, 35 * mm])
ts = header_style(agg, 4)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
# Highlight priority categories
ts.add("BACKGROUND", (0, 2), (-1, 2), SUCCESS_LIGHT)  # B. AI
ts.add("BACKGROUND", (0, 12), (-1, 12), SUCCESS_LIGHT)  # L. Pain
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

# Top-priority keywords detail (B + L)
story.append(Paragraph("★ Топ-приоритет: B. AI-специфичные (9 ключей)", H3))
ai_kw = [
    ["Запрос", "Показов/мес", "Цена клика ₽"],
    ["нейросеть сайт", "4 500", "85"],
    ["ai сайт", "2 800", "90"],
    ["нейросеть создать сайт", "2 200", "80"],
    ["сайт через chatgpt", "1 500", "75"],
    ["искусственный интеллект сайт", "1 400", "80"],
    ["сделать сайт нейросетью", "1 300", "80"],
    ["ai конструктор сайтов", "1 200", "95"],
    ["сайт с помощью ai", "950", "85"],
    ["генератор сайтов ai", "800", "95"],
]
t = Table(ai_kw, colWidths=[80 * mm, 35 * mm, 25 * mm])
t.setStyle(header_style(ai_kw, 3))
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("★ Топ-приоритет: L. Боль-ориентированные (6 ключей · цена клика 72 ₽)", H3))
pain_kw = [
    ["Запрос", "Показов/мес", "Цена клика ₽"],
    ["простой сайт сделать", "1 500", "70"],
    ["сайт за день", "1 200", "95"],
    ["сайт быстро недорого", "800", "85"],
    ["сайт визитка дёшево", "800", "55"],
    ["сайт без знаний программирования", "600", "65"],
    ["сделать сайт самому без программиста", "400", "60"],
]
t = Table(pain_kw, colWidths=[80 * mm, 35 * mm, 25 * mm])
t.setStyle(header_style(pain_kw, 3))
story.append(t)
story.append(PageBreak())


# Vertical keywords detail
page_title(
    "14b. Семантическое ядро · отраслевые запросы (45 ключей)",
    "Каждая ниша — отдельный лендинг с примерами под профиль клиента.",
)

verticals = [
    ("D. Кафе / Общепит", [
        ("доставка еды сайт", "4 500", "95"),
        ("сайт ресторана", "3 000", "85"),
        ("сайт для кафе", "2 500", "75"),
        ("сайт кофейни", "800", "70"),
        ("сайт для бара", "600", "70"),
        ("сайт пиццерии", "500", "75"),
    ]),
    ("E. Интернет-магазин", [
        ("создать интернет магазин", "12 000", "165"),
        ("интернет магазин с нуля", "3 500", "130"),
        ("интернет магазин под ключ", "2 500", "145"),
        ("магазин одежды сайт", "2 000", "95"),
        ("сайт цветочного магазина", "600", "70"),
    ]),
    ("F. Юрист / Адвокат", [
        ("сайт юриста", "2 000", "105"),
        ("сайт адвоката", "1 500", "105"),
        ("сайт юридической компании", "800", "125"),
        ("сайт нотариуса", "600", "90"),
        ("сайт визитка юристу", "400", "85"),
    ]),
    ("G. Красота / Салон", [
        ("сайт салона красоты", "2 500", "85"),
        ("сайт мастера маникюра", "1 800", "75"),
        ("сайт косметолога", "1 500", "95"),
        ("сайт парикмахерской", "1 200", "65"),
        ("сайт барбершопа", "800", "70"),
    ]),
    ("H. Медицина", [
        ("сайт клиники", "2 000", "145"),
        ("сайт врача", "1 800", "95"),
        ("сайт стоматологии", "1 500", "130"),
        ("сайт медцентра", "1 200", "145"),
        ("сайт ветклиники", "800", "105"),
    ]),
    ("I. Авто / Сервис", [
        ("сайт автосервиса", "1 200", "85"),
        ("сайт автосалона", "800", "115"),
        ("сайт шиномонтажа", "600", "65"),
        ("сайт детейлинга", "500", "75"),
    ]),
    ("J. Недвижимость", [
        ("сайт агентства недвижимости", "1 500", "125"),
        ("сайт риэлтора", "1 200", "95"),
        ("сайт жк", "800", "175"),
        ("сайт застройщика", "600", "145"),
    ]),
    ("K. Образование / Услуги", [
        ("сайт психолога", "2 500", "95"),
        ("сайт репетитора", "2 000", "75"),
        ("сайт онлайн школы", "1 500", "105"),
        ("сайт коуча", "800", "85"),
        ("сайт фитнес тренера", "700", "75"),
    ]),
]

# Layout: 2 columns of vertical category mini-tables
for cat_name, items in verticals:
    rows = [[cat_name, "Показов", "Цена клика ₽"]] + [[q, imp, cpc] for q, imp, cpc in items]
    t = Table(rows, colWidths=[100 * mm, 25 * mm, 30 * mm])
    t.setStyle(header_style(rows, 3))
    story.append(KeepTogether([t, Spacer(1, 3 * mm)]))
story.append(PageBreak())


# ====================================================================== #
# 15. Воронка показ → платящий + 4 сценария                              #
# ====================================================================== #
page_title(
    "15. Воронка 100К ₽ → платящие клиенты · 2026",
    "Чистые ключи дают сопоставимую цену клика, но последующие шаги воронки в 2-3 раза лучше: нажимаемость +60%, конверсия посадочной +100%, переход в платящего +30%. Эффективная воронка ×3-4.",
)

story.append(Paragraph("Воронка: показ → клик → визит → пробник → платящий", H3))
funnel_steps = [
    ["Шаг", "Метрика", "Значение 2026"],
    ["1", "Wordstat показов/мес (адресуемые)", "141 050"],
    ["2", "Показы рекламы (зависит от ставки + бюджета)", "—"],
    ["3", "× нажимаемость рекламы (на чистых ключах)", "5–8%"],
    ["4", "= Кликов = Визитов на сайт", "—"],
    ["5", "× конверсия посадочной (визит → пробник)", "4–8%"],
    ["6", "= Регистраций на пробник (5 дней Free Lite)", "—"],
    ["7", "× переход из пробника в платящего", "6–10%"],
    ["8", "= Платящий клиент", "—"],
]
t = Table(funnel_steps, colWidths=[15 * mm, 130 * mm, 50 * mm])
ts = header_style(funnel_steps, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("4 сценария на бюджет 100 000 ₽/мес", H3))

scenarios = [
    # (name, цена клика, конверсия посадочной, пробник→платящий)
    ("А. Холодный старт (M2, чистые ключи без оптимизации)", 85, 0.04, 0.06),
    ("Б. Базовая оптимизация (M3)", 75, 0.05, 0.07),
    ("В. Отраслевые лендинги (M4)", 65, 0.06, 0.08),
    ("Г. Зрелая воронка (M6+, окупаемость 2.4)", 55, 0.08, 0.10),
]

rows = [["Сценарий", "Цена клика ₽", "Кликов", "Цена визита", "Конв. поса-дочной %", "Пробни-ков", "Прб→Плт %", "Платящих", "Стоимость привлеч. ₽"]]
budget = 100000
for name, cpc, cv, tp in scenarios:
    clicks = budget / cpc
    trials = clicks * cv
    paid = trials * tp
    cac = budget / paid
    rows.append([
        name,
        f"{cpc} ₽",
        f"{int(round(clicks)):,}".replace(",", " "),
        f"{cpc} ₽",
        f"{cv*100:.0f}%",
        f"{int(round(trials)):,}".replace(",", " "),
        f"{tp*100:.0f}%",
        f"{paid:.1f}",
        f"{int(round(cac)):,}".replace(",", " ") + " ₽",
    ])

t = Table(rows, colWidths=[55 * mm, 18 * mm, 22 * mm, 22 * mm, 14 * mm, 18 * mm, 14 * mm, 22 * mm, 28 * mm])
ts = header_style(rows, 9)
# Color rows
ts.add("BACKGROUND", (-2, 1), (-2, 1), WARN_LIGHT)  # CAC row 1 — bad
ts.add("BACKGROUND", (-2, 4), (-2, 4), SUCCESS_LIGHT)  # CAC row 4 — good
ts.add("FONTNAME", (-2, 1), (-2, -1), BOLD_FONT)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Главное:</b> на 100К ₽ ТОЛЬКО Директ в первый месяц = <b>3 платящих</b> "
    "(не 30 как в финплане). К M6 при отшлифованной воронке — <b>15 платящих</b> в месяц. "
    "За 6 мес накопленно ~40 новых, база на конец M6 ≈ 34 (с 15% отвалом).",
    NOTE,
))
story.append(PageBreak())


# ====================================================================== #
# 16. График 6 мес + multi-channel + расхождение с финпланом              #
# ====================================================================== #
page_title(
    "16. Реальный график M2-M6 + расхождение с финансовым планом",
    "Пути закрытия разрыва: несколько каналов, бесплатный шум перед запуском, активные продажи бизнесу, замедленный разгон в финмодели.",
)

story.append(Paragraph("Реалистичный график 6 месяцев на 100К ₽/мес чистого Директа", H3))

ramp_pdf = [
    (1, "M1 Тихий запуск (без рекламы)", None, None, None, 0, None),
    (2, "M2 Холодный старт (чистые ключи)", 85, 0.04, 0.06, None, None),
    (3, "M3 Первая оптимизация", 75, 0.05, 0.07, None, None),
    (4, "M4 Отраслевые лендинги", 65, 0.06, 0.08, None, None),
    (5, "M5 Повторный показ + узнаваемость", 60, 0.07, 0.09, None, None),
    (6, "M6 Зрелая воронка", 55, 0.08, 0.10, None, None),
]
rows = [["Месяц", "Что происходит", "Цена клика", "Конв. посад. %", "Прб→Плт %", "Платящих/мес", "Стоимость привлеч. ₽"]]
total = 0
for m, label, cpc, cv, tp, paid_override, _ in ramp_pdf:
    if cpc is None:
        rows.append([f"M{m}", label, "—", "—", "—", "0", "—"])
    else:
        clicks = 100000 / cpc
        paid = clicks * cv * tp
        total += paid
        cac = 100000 / paid
        rows.append([
            f"M{m}",
            label,
            f"{cpc} ₽",
            f"{cv*100:.0f}%",
            f"{tp*100:.0f}%",
            f"{paid:.1f}",
            f"{int(round(cac)):,}".replace(",", " ") + " ₽",
        ])
rows.append(["", "ИТОГО за 6 мес (новых платящих)", "", "", "", f"~{int(round(total))}", f"~{int(round(100000*5/total)):,}".replace(",", " ") + " ₽"])

t = Table(rows, colWidths=[15 * mm, 80 * mm, 18 * mm, 16 * mm, 18 * mm, 28 * mm, 32 * mm])
ts = header_style(rows, 7)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
ts.add("FONTNAME", (-2, 1), (-2, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Несколько каналов одновременно (закрывает разрыв до 8-12 платящих в M2)", H3))
mc = [
    ["Канал", "Бюджет", "Платящих/мес", "Стоимость привлечения ₽"],
    ["Яндекс.Директ (только чистые)", "60 000 ₽", "4-6", "10 000–15 000"],
    ["VK Реклама (по интересам)", "25 000 ₽", "2-3", "8 300–12 500"],
    ["Telegram-каналы (партнёрки)", "15 000 ₽", "2-3", "5 000–7 500"],
    ["ИТОГО", "100 000 ₽", "8-12", "8 300–12 500"],
]
t = Table(mc, colWidths=[80 * mm, 30 * mm, 35 * mm, 45 * mm])
ts = header_style(mc, 4)
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Реалистичный план финмодели (замедленный разгон)", H3))
plan_diff = [
    ["Месяц", "Финплан (исходно)", "Реалистично (несколько каналов)", "Дельта"],
    ["M1", "0", "0", "0"],
    ["M2", "30", "8–12", "−20"],
    ["M3", "80", "25–35", "−50"],
    ["M4", "150", "65–85", "−75"],
    ["M5", "250", "150–180", "−80"],
    ["M6", "380", "280–320", "−80"],
    ["M7+", "540+", "догоняет план", "0"],
]
t = Table(plan_diff, colWidths=[20 * mm, 50 * mm, 80 * mm, 30 * mm])
ts = header_style(plan_diff, 4)
# Color delta column
for i in range(2, 7):
    ts.add("BACKGROUND", (-1, i), (-1, i), WARN_LIGHT)
ts.add("BACKGROUND", (-1, 7), (-1, 7), SUCCESS_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Накопленные потери первых 6 мес:</b> ~1.5 М ₽ выручки против плана. "
    "На счёте к M24 это уменьшит подушку с +67М до <b>~+58-62М</b> — всё равно сильный результат.",
    NOTE,
))
story.append(PageBreak())


# ====================================================================== #
# 17. LTV/CAC + что точно делать сейчас                                  #
# ====================================================================== #
page_title(
    "17. Окупаемость привлечения + план действий",
    "Правило подписочного бизнеса: стоимость привлечения ≤ пожизненная выручка / 3. Наша пожизненная выручка = 1 200 ₽ средний доход × 14 мес жизни клиента = 16 800 ₽ → бюджет на привлечение максимум 5 600 ₽.",
)

ltv_cac = [
    ["Сценарий", "Стоимость привлечения ₽", "Окупаемость", "Окупается?"],
    ["Песимистичный M2", "35 400", "0.47", "✗ нет"],
    ["Реалистичный M3", "21 400", "0.78", "✗ нет"],
    ["Оптимистичный M4", "13 500", "1.24", "⚠ за 14 мес"],
    ["Зрелая M5", "9 500", "1.77", "⚠ почти"],
    ["Идеал M6+", "6 900", "2.43", "≈ ОК"],
    ["Несколько каналов зрелый", "5 000–8 000", "2.1–3.4", "✓ проходит"],
]
t = Table(ltv_cac, colWidths=[60 * mm, 35 * mm, 30 * mm, 35 * mm])
ts = header_style(ltv_cac, 4)
for i in range(1, 3):
    ts.add("BACKGROUND", (-1, i), (-1, i), WARN_LIGHT)
for i in range(3, 5):
    ts.add("BACKGROUND", (-1, i), (-1, i), ACCENT_LIGHT)
for i in range(5, 7):
    ts.add("BACKGROUND", (-1, i), (-1, i), SUCCESS_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph(
    "<b>Главный вывод:</b> до М5 инвестируем в обучение воронки (стоимость привлечения > пожизненной выручки) — норма для подписочного стартапа. "
    "С М6+ воронка должна окупаться. К М12 средний доход с клиента должен вырасти до 3 000+ ₽ через апсейл на Pro/Enterprise — "
    "это поднимет пожизненную выручку до ~42 000 ₽ и сделает привлечение по 14К нормальным.",
    NOTE,
))
story.append(Spacer(1, 8 * mm))

story.append(Paragraph("План действий на M1-M3", H3))
plan_pts = [
    "<b>M1 тихий запуск (без платной рекламы):</b> founders посты в Telegram, статья на VC.ru/Habr, 3-5 готовых демо-кейсов, холодные сообщения 50 малому бизнесу/день.",
    "<b>M2 первая платная (только чистые):</b> Директ AI-ключи 25К + отраслевые 20К + боль-запросы 10К + сравнение 5К. VK Реклама 20К. Telegram 15К. Контент 5К. Стоп-слова: «бесплатно/скачать/торрент/студия/заказать/фриланс». Цель 8-12 платящих.",
    "<b>M3 оптимизация:</b> отсев ключей с нулевой конверсией, сравнение 2 вариантов заголовков лендинга, повторный показ +10К, реферальная программа. Цель 25-35 платящих.",
    "<b>M4-M6:</b> отраслевые лендинги под каждую нишу с реальными кейсами клиентов. Это поднимает конверсию посадочной до 6-8% и переход в платящего до 8-10%.",
]
for p in plan_pts:
    story.append(Paragraph(p, P))
story.append(Spacer(1, 6 * mm))

story.append(Paragraph(
    "<b>Перед запуском обязательно:</b> проверить 63 ключа в wordstat.yandex.ru (1 час) "
    "и Прогнозе бюджета Директа (1 час) — получить реальную цену клика и оценку показов под наш регион.",
    NOTE,
))


doc.build(story)
print(f"OK saved: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
