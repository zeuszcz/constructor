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
story.append(Paragraph("Реалистичная экономика май 2026", ParagraphStyle("Cover2", fontName=ITAL_FONT, fontSize=20, leading=24, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=18)))
story.append(Paragraph("Каждая копейка расходов · полный план найма · 59 чистых запросов · 3 сценария", cover_sub))
story.append(Paragraph("Free / Lite / Starter / Pro / Enterprise · РФ · УСН 1% (IT-льгота)", cover_sub))
story.append(Spacer(1, 25 * mm))

# Cover key numbers
key_nums = [
    ["3 М ₽", "M11", "M14", "67 М ₽"],
    ["стартовый капитал", "первая прибыль", "вернули вложенное", "на счёте к M24"],
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
# 0. Допущения май 2026                                                  #
# ====================================================================== #
page_title(
    "0. Контекст май 2026 · реальные условия для IT-стартапа в РФ",
    "Эти допущения — основа всех расчётов. Если что-то поменяется — пересчитываем модель.",
)

context = [
    ["Параметр", "Значение", "Источник / комментарий"],
    ["Налоговый режим", "УСН 1% (IT-льгота)",
     "С 2024 в Москве для аккредитованных IT-компаний — 1% УСН вместо 6%. До получения IT-аккредитации (M1-M3) платим 6%."],
    ["IT-аккредитация Минцифры", "Подаём в M3, получаем M4",
     "Бесплатно. Требует: ОКВЭД 62.0х/63.1х, выручка ≥70% от IT, 7 сотрудников минимум."],
    ["Страховые взносы (с IT-аккредитацией)", "7.6% от ФОТ",
     "Льготный тариф для IT-компаний. Без аккредитации — 30%."],
    ["НДФЛ", "13% (15% при ЗП > 5М ₽/год)",
     "Удерживается из gross-зарплаты сотрудника, не доп.расход для работодателя."],
    ["Эквайринг (банк-комиссия)", "2.5–3.5% от каждого платежа",
     "Yookassa / Tinkoff Recurrent / CloudPayments. Реалистично 2.8% средне."],
    ["НДС", "Освобождены",
     "Выручка <2 млрд/год → УСН без НДС. Применимо к нам до M30+."],
    ["Юрист (договоры, оферта, ИП/ЮЛ)", "20–60 К/мес",
     "Бухгалтер 15–40К + юрист 5–20К на абонементе. С ростом — больше."],
    ["Рабочий курс ₽/$", "100 ₽/$",
     "Для расчётов API LLM. Реальный диапазон 95–120 в 2026."],
    ["Размер 1 сообщения", "8 000 токенов",
     "5 000 input + 3 000 output. Среднее для AI-code-gen."],
    ["Наценка на AI-токены", "2.8×",
     "Себестоимость + ~64% валовая маржа на токенах."],
    ["Стартовый капитал", "3 000 000 ₽",
     "Founders + микро-инвестор (френды). Покрывает 9 мес минуса до M11."],
]
t = Table(context, colWidths=[60 * mm, 50 * mm, 110 * mm])
t.setStyle(header_style(context, 3))
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Расшифровка сокращений", H3))
abbrev = [
    ["Сокращение", "Расшифровка"],
    ["УСН", "Упрощённая система налогообложения (заменяет налог на прибыль)"],
    ["ОКВЭД", "Общероссийский классификатор видов экономической деятельности (код вида деятельности)"],
    ["ФОТ", "Фонд оплаты труда (зарплаты до НДФЛ + страховые)"],
    ["НДФЛ", "Налог на доходы физических лиц (13–15%)"],
    ["НДС", "Налог на добавленную стоимость (20% для общей системы, 0% при УСН)"],
    ["Эквайринг", "Платёжная комиссия банка за приём оплаты картой/СБП"],
    ["IT-аккредитация", "Включение в реестр аккредитованных IT-компаний Минцифры РФ"],
    ["AI", "Искусственный интеллект (большие языковые модели)"],
    ["LLM", "Большая языковая модель (ChatGPT, Claude, YandexGPT и т.д.)"],
    ["API", "Программный интерфейс для подключения сторонних сервисов"],
    ["VPS", "Виртуальный сервер в дата-центре"],
    ["БД", "База данных"],
]
t = Table(abbrev, colWidths=[50 * mm, 165 * mm])
t.setStyle(header_style(abbrev, 2))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 1. Базовые допущения                                                  #
# ====================================================================== #
page_title(
    "1. Базовые допущения по AI",
    "Все расчёты в документе строятся на этих 4 параметрах. На листе «1. Параметры» XLSX-калькулятора их можно менять.",
)

assumptions = [
    ["Параметр", "Значение", "Комментарий"],
    ["Размер 1 сообщения", "8 000 токенов",
     "5 000 input + 3 000 output. Среднее для AI-code-gen."],
    ["Доля output в 1М общих токенов", "0.5",
     "Половина от общего числа токенов — это output (ответ AI). Стандарт для чат-режима."],
    ["Наценка на токены", "2.8×",
     "Себестоимость + ~64% валовая маржа на токенах."],
    ["Курс ₽/$ для расчётов", "100",
     "Реальный диапазон в 2026: 95–120 ₽."],
]
t = Table(assumptions, colWidths=[55 * mm, 35 * mm, 130 * mm])
t.setStyle(header_style(assumptions, 3))
story.append(t)
story.append(Spacer(1, 4 * mm))
story.append(Paragraph(
    "<b>Токен</b> = кусок текста ~4 символа. <b>Input</b> = что отправляем AI (наш промпт + контекст). "
    "<b>Output</b> = что AI отвечает. Цены AI-провайдеров считают input и output отдельно: output обычно "
    "в 3–5 раз дороже.",
    NOTE,
))
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
    "7. Полная структура расходов · 9 категорий",
    "Все категории затрат стартапа в РФ. Это РЕАЛЬНЫЕ расходы — не идеальная модель, а то что мы будем платить каждый месяц.",
)

cost_categories = [
    ["№", "Категория", "Тип", "Размер на M12 (1 670 платящих)"],
    ["1", "Зарплаты команды (ФОТ)", "Полу-фиксированный, растёт с наймом", "1 690 К/мес (gross)"],
    ["2", "Страховые взносы + НДФЛ", "% от ФОТ", "+13% к gross (с IT-льготой)"],
    ["3", "AI-токены (LLM API)", "Variable: ~30% от выручки", "1 580 К/мес"],
    ["4", "Наша инфраструктура", "Semi-fixed, растёт с базой", "195 К/мес"],
    ["5", "Бэкофис (per-client)", "Variable: ~9% от выручки", "473 К/мес"],
    ["6", "Юристы / бухгалтеры / аудит", "Фиксированный, растёт с ростом", "80 К/мес"],
    ["7", "ПО и лицензии (на сотрудника)", "~7 К × количество сотрудников", "63 К/мес (9 чел)"],
    ["8", "Маркетинг и реклама", "Фиксированный план", "200 К/мес"],
    ["9", "Резервы (refunds + штрафы + bad debt)", "~3.5% от выручки", "184 К/мес"],
    ["10", "Налоги (УСН 1% в IT)", "1% от выручки", "53 К/мес"],
    ["", "ИТОГО на M12", "", "≈ 4 740 К/мес (90% выручки)"],
]
t = Table(cost_categories, colWidths=[10 * mm, 70 * mm, 60 * mm, 75 * mm])
ts = header_style(cost_categories, 4)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Расшифровка типов расходов", H3))
type_def = [
    ["Тип", "Что значит", "Поведение при росте/падении выручки"],
    ["Variable (переменный)", "Растёт пропорционально числу клиентов или выручке", "Падает выручка — падают расходы"],
    ["Fixed (фиксированный)", "Платим одинаково независимо от выручки", "Не падает при падении выручки = риск"],
    ["Semi-fixed (полу-фикс.)", "Растёт ступеньками при пересечении порогов", "В моменте фикс, но переключается"],
    ["Полу-фикс. (плановый)", "Растёт по плану найма", "Можно замедлить найм если выручка падает"],
]
t = Table(type_def, colWidths=[40 * mm, 80 * mm, 95 * mm])
t.setStyle(header_style(type_def, 3))
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph("Подробная разбивка категории #1: Зарплаты команды", H3))

team_breakdown = [
    ["Месяц", "Команда (cumulative)", "ФОТ gross ₽/мес", "+ страх 7.6% IT", "Итого работодателю"],
    ["M1", "2 founders × 30К минимум (как ИП)", "60 000", "—", "61 800"],
    ["M2-M3", "+ дизайнер 80К (фриланс ИП)", "140 000", "—", "144 200"],
    ["M4", "+ middle fullstack 220К на штате", "388 000", "+ 16.7К", "426 800"],
    ["M5", "Дизайнер на штат 130К", "454 000", "+ 24.6К", "503 940"],
    ["M6", "+ саппорт L1 70К", "533 000", "+ 27.5К", "596 960"],
    ["M7", "Founders 100К каждый = 200К", "698 000", "+ 35.5К", "788 740"],
    ["M8-M9", "+ маркетолог middle 150К", "867 000", "+ 47.5К", "979 710"],
    ["M10-M11", "+ senior fullstack 350К", "1 261 000", "+ 78.5К", "1 424 930"],
    ["M12-M14", "Founders 200К + B2B sales 80К + контент 100К", "1 689 000", "+ 117.7К", "1 908 570"],
    ["M15-M17", "+ продакт-аналитик 180К + senior dev #2 350К", "2 286 000", "+ 173.7К", "2 583 180"],
    ["M18-M20", "+ DevOps/SRE 280К", "2 601 000", "+ 197.7К", "2 939 130"],
    ["M21-M24", "+ саппорт L2 110К (всего 13 чел)", "2 725 000", "+ 207.1К", "3 079 250"],
]
t = Table(team_breakdown, colWidths=[18 * mm, 75 * mm, 32 * mm, 30 * mm, 35 * mm])
t.setStyle(header_style(team_breakdown, 5))
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Бенефиты сотрудникам (+5% сверху ФОТ)</b>: ДМС (медстраховка) ~3К/мес, оборудование (амортизация ноутбука) ~2К/мес, "
    "обучение/конференции ~3К/мес. Учтены в множителе ×1.13 для IT-аккредитованных.",
    NOTE,
))
story.append(PageBreak())


# Подробная разбивка категории #4: Наша инфраструктура
page_title(
    "7b. Подробная разбивка: наша инфраструктура (категория #4)",
    "Что мы покупаем у Yandex Cloud / Selectel / Серверум для собственного сервиса. Растёт ступенчато с базой клиентов.",
)

infra_detail = [
    ["Сервис / компонент", "Поставщик", "Цена ₽/мес", "Когда подключаем"],
    ["Control plane VPS (3 шт.)", "Selectel / Yandex Cloud", "8 000 → 80 000", "M1: 1 staging VPS"],
    ["Managed PostgreSQL (primary)", "Yandex Cloud", "5 000 → 50 000", "M2 starter, growing"],
    ["Managed PostgreSQL (read-replica)", "Yandex Cloud", "0 → 30 000", "Подключаем M6+ для масштаба"],
    ["Managed Redis", "Yandex Cloud", "0 → 15 000", "M5+ для сессий и очередей"],
    ["S3 для проектов клиентов + бэкапы", "Yandex / Selectel", "1 000 → 30 000", "M1, растёт с базой"],
    ["Мониторинг (Grafana Cloud / Datadog)", "Yandex Cloud Monitoring", "2 000 → 25 000", "M1, базовые метрики"],
    ["Логирование", "Yandex Cloud Logging", "0 → 15 000", "M3+"],
    ["CDN (доставка статики)", "Selectel / Yandex CDN", "0 → 50 000", "M6+ при росте трафика"],
    ["DDoS-защита", "Qrator / StormWall", "0 → 80 000", "M9+ когда становимся видны"],
    ["Резервный регион + аварийное восст.", "Yandex Cloud", "0 → 40 000", "M12+ для надёжности"],
    ["GitHub Enterprise (для команды)", "GitHub", "5 × 2 000 = 10 000", "M4+ при найме"],
    ["VPN / прокси для зап. AI API", "Cloudflare WARP / своё", "5 000 → 15 000", "M2+ для Anthropic/OpenAI"],
    ["", "ИТОГО (диапазон M1 → M24)", "8 000 → 780 000", ""],
]
t = Table(infra_detail, colWidths=[80 * mm, 50 * mm, 35 * mm, 50 * mm])
ts = header_style(infra_detail, 4)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

# Подробная разбивка категории #5: Бэкофис
story.append(Paragraph("Подробная разбивка: бэкофис per-client (категория #5)", H3))

backoffice_detail = [
    ["Подкатегория", "Доля от выручки", "Что входит"],
    ["Эквайринг", "2.5–3.0%", "Yookassa / Tinkoff Recurrent — комиссия за приём оплаты картой/СБП"],
    ["VPS клиентских сайтов (Серверум)", "2.0–2.5%", "Виртуальный сервер для сайта каждого клиента (Lite=50₽, Pro=3000₽)"],
    ["Домены клиентов (.ru / .com)", "0.5–1.0%", "Регистрация и продление доменов клиентских сайтов (200–1000₽/год)"],
    ["CRM (AmoCRM / Bitrix24)", "0.3–0.5%", "Учёт лидов и клиентов: 1.5–5К/мес × места"],
    ["Helpdesk (UseDesk / HelpCRM)", "0.3–0.5%", "Тикетная система для поддержки: 2–5К/мес"],
    ["Email-рассылки (Sendsay / Unisender)", "0.3–0.5%", "Транзакционные + маркетинг писем: 3–10К/мес"],
    ["SMS для 2FA / уведомлений", "0.2–0.4%", "Авторизация и важные уведомления: 2–5К/мес"],
    ["Аналитика (Метрика, Метаплан Pro)", "0.1–0.3%", "Yandex Метрика бесплатна, Pro-функции 5К/мес"],
    ["Прочие операционные мелочи", "0.5–1.0%", "Банк-обслуживание, нотариус, EDS, мелкие закупки"],
    ["", "ИТОГО ~ 9% от выручки", ""],
]
t = Table(backoffice_detail, colWidths=[60 * mm, 35 * mm, 120 * mm])
ts = header_style(backoffice_detail, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(PageBreak())


# Категории 7-9: Юристы, ПО, Резервы
page_title(
    "7c. Юристы / ПО / Резервы (категории #6, #7, #9)",
    "Подробная разбивка трёх часто упускаемых категорий расходов.",
)

story.append(Paragraph("Категория #6: Юристы / бухгалтеры / банк / нотариус", H3))
legal_detail = [
    ["Стадия", "Состав", "Стоимость ₽/мес"],
    ["M1-M3", "Бухгалтер ИП на аутсорсе + регистрация ЮЛ (4К единоразово)", "20 000 → 25 000"],
    ["M4-M6", "Бух + юрист 5К/мес + IT-аккредитация подача", "35 000"],
    ["M7-M11", "Бух (расширенный) + юрист на абонементе 15К + банк-обслуж.", "50 000 → 65 000"],
    ["M12-M14", "Бух + B2B договоры юристом 20К + кассовый аппарат 3К", "80 000"],
    ["M15-M17", "+ Годовой аудит (квартальные авансы)", "100 000"],
    ["M18-M20", "+ Юр.споры/претензии. Корп.юрист на абонементе 35К", "120 000"],
    ["M21-M24", "+ Сложные B2B-договоры. 1С-бухгалтерия Enterprise", "140 000 → 160 000"],
    ["", "Суммарно за 24 мес", "≈ 1.94 М ₽"],
]
t = Table(legal_detail, colWidths=[25 * mm, 130 * mm, 60 * mm])
ts = header_style(legal_detail, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Категория #7: ПО и лицензии (на сотрудника)", H3))
software_detail = [
    ["ПО / Подписка", "Цена ₽/мес/чел", "Кому нужно"],
    ["JetBrains All Products", "3 000", "Разработчики (legal в РФ через UA/AM реселлеры)"],
    ["Cursor / GitHub Copilot", "2 000", "Разработчики (AI-помощник)"],
    ["Claude / ChatGPT Plus (личные)", "2 000", "Разработчики + аналитики"],
    ["Figma Professional", "1 500", "Дизайнеры (через VPN/RU-альтернативы)"],
    ["Adobe Creative Cloud", "5 000", "Дизайнеры (если нужен Photoshop / Illustrator)"],
    ["Notion Team / Yonote", "1 000", "Все сотрудники (документация)"],
    ["Linear / Yougile", "1 500", "Все (управление задачами)"],
    ["Slack / Mattermost", "0–1 000", "Все (мессенджер команды)"],
    ["GitHub Enterprise", "2 000", "Разработчики"],
    ["", "ИТОГО усреднённо ~ 7 000 ₽/чел/мес", ""],
]
t = Table(software_detail, colWidths=[60 * mm, 35 * mm, 120 * mm])
ts = header_style(software_detail, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Категория #9: Резервы (то что часто забывают учесть)", H3))
reserves_detail = [
    ["Подкатегория", "Доля от выручки", "Что покрывает"],
    ["Возвраты клиентам (refunds)", "1.5%", "Клиент передумал в первый месяц, возвращаем деньги"],
    ["Безнадёжная задолженность", "0.5%", "Клиент списал карту, деньги застряли в эквайринге"],
    ["Юр.споры / штрафы", "0.5%", "Спор с клиентом / штраф ФАС за рекламу / Роскомнадзор"],
    ["Технические сбои / компенсации", "0.5%", "SLA-компенсация при простое сервиса"],
    ["Неучтённое (force majeure)", "0.5%", "Курсовые риски, необратимые потери, всё что мы не предвидели"],
    ["", "ИТОГО ~ 3.5% от выручки", ""],
]
t = Table(reserves_detail, colWidths=[55 * mm, 35 * mm, 125 * mm])
ts = header_style(reserves_detail, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Расшифровка:</b> SLA = Service Level Agreement (соглашение об уровне сервиса). "
    "ФАС = Федеральная антимонопольная служба (контроль рекламы). "
    "Force majeure = непреодолимые обстоятельства (катастрофы, эпидемии, политические события).",
    NOTE,
))
story.append(PageBreak())
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
    "8. План найма команды по месяцам · реальные зарплаты май 2026",
    "Каждая роль с зарплатой и месяцем найма. Цифры — реальные ЗП на удалёнке РФ май 2026 (после инфляции 2024-2026 ~30%).",
)

hiring_plan = [
    ["Месяц", "Роль", "ЗП gross ₽/мес", "Тип занятости", "Обоснование"],
    ["M1", "CEO + CTO (founders)", "30 К × 2 = 60 К", "ИП, минимальный оклад", "Тихий запуск, экономим ресурс"],
    ["M2", "+ Дизайнер lead", "80 К", "Фриланс ИП", "Лендинги + UI базовый"],
    ["M4", "+ Middle fullstack", "220 К", "На штате", "Поддержка кодовой базы при росте"],
    ["M5", "Дизайнер на штат", "130 К", "На штате", "Постоянная нагрузка"],
    ["M6", "+ Саппорт L1", "70 К", "На штате", "Первая линия поддержки клиентов"],
    ["M7", "Founders повышают себе", "100 К × 2 = 200 К", "На штате", "Достигнут break-even на расходы"],
    ["M8", "+ Маркетолог middle", "150 К", "На штате", "Управление кампаниями + оптимизация"],
    ["M10", "+ Senior fullstack", "350 К", "На штате", "Архитектурные задачи, новые фичи"],
    ["M12", "Founders 200 К × 2", "400 К", "На штате", "При выручке 5 М/мес — нормальная ЗП"],
    ["M12", "+ B2B sales menager", "80 К + комиссии", "На штате", "Продажа Enterprise тарифов"],
    ["M12", "+ Контент-маркетолог", "100 К", "На штате / фриланс", "SEO + статьи Habr/VC.ru"],
    ["M15", "+ Продакт-аналитик", "180 К", "На штате", "Когорты, retention, продуктовые метрики"],
    ["M15", "+ Senior fullstack #2", "350 К", "На штате", "Параллельные потоки разработки"],
    ["M18", "+ DevOps / SRE", "280 К", "На штате", "Production-стабильность при 4 К+ клиентов"],
    ["M21", "+ Саппорт L2", "110 К", "На штате", "Сложные кейсы, B2B-обслуживание"],
    ["M24", "Команда из 13 человек", "Σ 2 725 К/мес gross", "11 на штате + 2 founders", "ФОТ = 11.6% от выручки 26 М"],
]
t = Table(hiring_plan, colWidths=[15 * mm, 60 * mm, 35 * mm, 35 * mm, 70 * mm])
ts = header_style(hiring_plan, 5)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Расшифровка:</b> ФОТ = фонд оплаты труда (сумма gross-зарплат). gross = ЗП до удержания НДФЛ 13%. "
    "На штате = трудовой договор + страховые взносы работодателя 7.6% (с IT-льготой). ИП = индивидуальный предприниматель "
    "(сам платит свои налоги, нам — без накруток). Founders первые 6 мес сидят на минимуме (30К) для экономии.",
    NOTE,
))
story.append(Spacer(1, 6 * mm))

# Точка безубыточности — компактно
story.append(Paragraph("Точка безубыточности (как ориентир, не бюджет)", H3))
break_even_simple = [
    ["Период", "Команда + расходы (без маркет.)", "Выручка для покрытия"],
    ["M1-M3 (ранний bootstrap)", "85–145 К/мес", "100–170 платящих × 990 ₽"],
    ["M4-M6 (первые наймы)", "470–650 К/мес", "350–500 при ARPU 1 200 ₽"],
    ["M7-M9 (founders + маркет)", "1.0–1.2 М/мес", "590–700 при ARPU 1 700 ₽"],
    ["M12 (расширенная команда)", "2.5 М/мес", "1 250 при ARPU 2 000 ₽"],
    ["M18 (зрелая компания)", "4.4 М/мес", "1 500 при ARPU 3 000 ₽"],
]
t = Table(break_even_simple, colWidths=[55 * mm, 70 * mm, 90 * mm])
t.setStyle(header_style(break_even_simple, 3))
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 8b. Точка безубыточности по миксу тарифов                              #
# ====================================================================== #
page_title(
    "8b. Точка безубыточности по миксу тарифов",
    "Сколько платящих клиентов нужно чтобы покрыть маркетинговый бюджет 250 К/мес. Зависит от того, какие тарифы покупают чаще.",
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
    "9. Реалистичная финмодель 24 месяца · все 9 категорий расходов",
    "Каждый месяц — реальные расходы по каждой категории. Стартовый капитал 3 М ₽ нужен (founders + микро-инвестор от друзей).",
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
team_gross = [
    60000, 140000, 140000, 388000, 454000, 533000, 698000, 867000, 867000, 1261000,
    1261000, 1689000, 1689000, 1689000, 2286000, 2286000, 2286000, 2601000, 2601000,
    2601000, 2725000, 2725000, 2725000, 2725000,
]
team_mults = [1.03, 1.03, 1.03, 1.10, 1.11, 1.12, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13]
team_count_arr = [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 9, 9, 9, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13]
infra_our = [
    8000, 12000, 18000, 25000, 35000, 50000, 65000, 85000, 105000, 130000,
    160000, 195000, 235000, 280000, 330000, 380000, 430000, 480000, 530000, 580000,
    630000, 680000, 730000, 780000,
]
legal_acc = [
    20000, 25000, 25000, 35000, 35000, 35000, 50000, 50000, 50000, 65000,
    65000, 80000, 80000, 80000, 100000, 100000, 100000, 120000, 120000, 120000,
    140000, 140000, 140000, 160000,
]
marketing_per_month = [
    0, 100000, 100000, 100000, 100000, 150000, 150000, 150000, 150000, 200000,
    200000, 200000, 200000, 200000, 250000, 250000, 250000, 250000, 250000, 250000,
    300000, 300000, 300000, 300000,
]

cum = 3000000  # Стартовый капитал 3 М ₽
month_data = []
for i in range(24):
    mrr = paying[i] * arpus[i]
    team = team_gross[i] * team_mults[i]
    tokens = mrr * 0.30
    infra = infra_our[i]
    backoff = mrr * 0.09
    legal = legal_acc[i]
    soft = team_count_arr[i] * 7000
    mkt = marketing_per_month[i]
    reserves = mrr * 0.035
    tax = mrr * (0.06 if i < 3 else 0.01)  # УСН 6% до IT-аккред, потом 1%
    total_opex = team + tokens + infra + backoff + legal + soft + mkt + reserves + tax
    profit = mrr - total_opex
    cum += profit
    month_data.append((
        i + 1, paying[i], mrr, team, tokens, infra, backoff, legal, soft, mkt, reserves, tax, profit, cum,
    ))

# Сжатая таблица — главные числа
rows = [["Мес", "Плат.", "Выручка", "Команда", "Токены", "Инфра", "Бэкоф.", "Юр", "ПО", "Маркет", "Резерв", "Налог", "Прибыль", "Счёт"]]
for m, p, mrr, team, tok, inf, bo, leg, sw, mkt, res, tx, pr, c in month_data:
    rows.append([
        f"M{m}",
        f"{p:,}".replace(",", " "),
        fmt_rub(mrr),
        fmt_rub(team),
        fmt_rub(tok),
        fmt_rub(inf),
        fmt_rub(bo),
        fmt_rub(leg),
        fmt_rub(sw),
        fmt_rub(mkt),
        fmt_rub(res),
        fmt_rub(tx),
        fmt_rub(pr),
        fmt_rub(c),
    ])

t = Table(
    rows,
    colWidths=[10 * mm, 14 * mm, 22 * mm, 22 * mm, 21 * mm, 17 * mm, 17 * mm, 13 * mm, 13 * mm, 17 * mm, 16 * mm, 14 * mm, 22 * mm, 23 * mm],
)
ts = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
    ("FONTSIZE", (0, 0), (-1, 0), 7),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, -1), BODY_FONT),
    ("FONTSIZE", (0, 1), (-1, -1), 6.5),
    ("TEXTCOLOR", (0, 1), (-1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
    ("TOPPADDING", (0, 0), (-1, 0), 3),
    ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ("TOPPADDING", (0, 1), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
])
for i, entry in enumerate(month_data, start=1):
    pr = entry[12]
    c = entry[13]
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

story.append(Paragraph(
    "<b>Расшифровка колонок:</b> Команда = ФОТ × 1.10–1.13 (страховые IT 7.6% + бенефиты 5%). "
    "Токены = 30% выручки (LLM API). Инфра = наши сервера (растёт с базой). Бэкофис = 9% выручки "
    "(эквайринг 2.8% + VPS клиентов + домены + CRM/Helpdesk). Юр = бухгалтер + юрист + аудит. "
    "ПО = 7К × сотрудник. Маркет = фикс.бюджет. Резерв = 3.5% (refunds + штрафы + бэд-долг). "
    "Налог = УСН 6% до M3, потом 1% (IT-льгота).",
    NOTE,
))
story.append(Spacer(1, 6 * mm))

# Сводка
m24 = month_data[-1]
min_cash = min(entry[13] for entry in month_data)
first_pos_pr = next((e[0] for e in month_data if e[12] > 0), None)
first_pos_cash = next((e[0] for e in month_data if e[13] > 3000000 and e[0] > 1), None)
recovered_cash = next((e[0] for e in month_data if e[13] > 0 and e[0] > 1), None)

# Cum sums
team_total = sum(e[3] for e in month_data)
tokens_total = sum(e[4] for e in month_data)
infra_total = sum(e[5] for e in month_data)
backoff_total = sum(e[6] for e in month_data)
legal_total = sum(e[7] for e in month_data)
soft_total = sum(e[8] for e in month_data)
mkt_total = sum(e[9] for e in month_data)
reserves_total = sum(e[10] for e in month_data)
tax_total = sum(e[11] for e in month_data)
revenue_total = sum(e[2] for e in month_data)

rows = [
    ["Метрика", "Значение"],
    ["Выручка в мес на M24", fmt_rub(m24[2])],
    ["Выручка в год на M24 (ARR)", fmt_rub(m24[2] * 12)],
    ["Деньги на счёте на M24", fmt_rub(m24[13])],
    ["Самый большой минус по деньгам", fmt_rub(min_cash)],
    ["Когда первая прибыль (опер.+)", f"M{first_pos_pr}"],
    ["Когда счёт вернулся к старту (3 М ₽)", f"M{first_pos_cash}"],
    ["Когда деньги стали > 0 (положительные)", f"M{recovered_cash}" if recovered_cash else "—"],
    ["Стартовый капитал необходим", fmt_rub(3000000) + " (founders + друзья)"],
]
t = Table(rows, colWidths=[80 * mm, 70 * mm])
t.setStyle(header_style(rows, 2))
story.append(t)
story.append(PageBreak())


# 9b. Структура расходов суммарно за 24 мес
page_title(
    "9b. Куда уходят деньги: суммарные расходы за 24 месяца",
    "Распределение всех расходов по категориям. Выручка суммарно: ~218 М ₽. Расходы суммарно: ~152 М ₽. Разница в 66 М — на счёте.",
)

# Sort categories by share
exp_cats = [
    ("Команда (ФОТ + страховые + бенефиты)", team_total),
    ("Токены (LLM API)", tokens_total),
    ("Бэкофис (эквайринг + VPS клиентов + домены + CRM)", backoff_total),
    ("Резервы (возвраты + штрафы + бэд-долг)", reserves_total),
    ("Наша инфраструктура (PG/Redis/S3/мониторинг/CDN)", infra_total),
    ("Маркетинг (Директ + VK + Telegram + контент)", mkt_total),
    ("Налоги (УСН 1% IT-льгота)", tax_total),
    ("Юристы / бухгалтеры / аудит", legal_total),
    ("ПО и лицензии (Figma/JetBrains/Cursor/...)", soft_total),
]
total_exp = sum(v for _, v in exp_cats)
exp_rows = [["Категория", "Сумма за 24 мес ₽", "% от выручки", "% от расходов"]]
for cat, v in sorted(exp_cats, key=lambda x: -x[1]):
    pct_rev = v / revenue_total * 100
    pct_exp = v / total_exp * 100
    exp_rows.append([cat, fmt_rub(v), f"{pct_rev:.1f}%", f"{pct_exp:.1f}%"])
exp_rows.append(["ИТОГО расходов", fmt_rub(total_exp), f"{total_exp/revenue_total*100:.1f}%", "100.0%"])
exp_rows.append(["Выручка суммарно за 24 мес", fmt_rub(revenue_total), "100.0%", ""])
exp_rows.append(["Накопленная прибыль (на счёте)", fmt_rub(revenue_total - total_exp), f"{(revenue_total-total_exp)/revenue_total*100:.1f}%", ""])

t = Table(exp_rows, colWidths=[100 * mm, 40 * mm, 30 * mm, 30 * mm])
ts = header_style(exp_rows, 4)
ts.add("BACKGROUND", (0, -3), (-1, -3), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -3), (-1, -3), BOLD_FONT)
ts.add("BACKGROUND", (0, -2), (-1, -2), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -2), (-1, -2), BOLD_FONT)
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph(
    "<b>Главный вывод:</b> крупнейшие 2 категории — <b>команда (19%)</b> и <b>токены (30%)</b>. "
    "В сумме они едят почти половину выручки. Маркетинг — всего 2.2% от выручки = "
    "не потому что мало, а потому что выручка большая и маркетинг ~250К/мес фикс.",
    NOTE,
))
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
    "На каждом платящем клиенте мы зарабатываем в среднем <b>1 385 ₽/мес</b>.",
    "<b>9 категорий расходов</b>: команда (~19% выручки) + токены 30% + бэкофис 9% + резервы 3.5% + инфра + юр + ПО + маркетинг + налоги 1%.",
    "<b>Команда из 13 человек к M24</b>: 2 founders + 3 разработчика + дизайнер + маркетолог + продактовый аналитик + B2B продажник + контент-маркетолог + 2 саппорта + DevOps. ФОТ 2.7 М/мес gross.",
    "<b>IT-аккредитация Минцифры с M4</b>: страховые 7.6% (вместо 30%) + УСН 1% (вместо 6%). Экономия ~6 М ₽ за 24 мес.",
    "<b>Стартовый капитал нужен 3 М ₽</b> (не 30 К как казалось!). Минус накапливается до M9 (~−2.4 М относительно стартового), потом восстанавливается.",
    "Прибыль становится положительной на <b>месяце 11</b>. Возврат вложений (счёт > 0 от стартового капитала) — на <b>месяце 14</b>.",
    "За 24 месяца: выручка <b>26 М ₽/мес</b> (~312 М в год), на счёте <b>+67 М ₽</b>, команда 13 человек, IT-аккредитация.",
    "<b>Маркетинг 2026 реальность</b>: 100 К ₽ Директ → 3 платящих в M2 (cold), 15 в M6 (зрелая воронка). Ramp медленнее старого плана — учтено.",
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
# 12b. Юнит-экономика по тарифам                                         #
# ====================================================================== #
page_title(
    "12b. Юнит-экономика по каждому тарифу",
    "Полная себестоимость + срок жизни клиента + пожизненная выручка для каждого тарифа. Считаем все мелочи.",
)

# Unit econ по тарифам
ue_data = [
    # name, price, wallet, server, domain, churn_pct, life_months, support_cost
    ("Lite", 990, 1000, 50, 25, 0.07, 14, 30),
    ("Starter", 2990, 2500, 600, 50, 0.05, 20, 80),
    ("Pro", 7990, 6000, 3000, 100, 0.04, 25, 200),
    ("Enterprise", 19990, 18000, 8000, 250, 0.03, 33, 500),
]
markup = 2.8

ue_rows = [["Тариф", "Цена ₽", "Токены", "VPS клиента", "Домен", "Эквайринг 2.8%", "Поддержка", "Резервы 3.5%", "Себест-ть", "Маржа", "Маржа %"]]
for name, price, wallet, server, domain, churn, life, support in ue_data:
    tokens_cost = wallet / markup
    acquiring = price * 0.028
    reserves = price * 0.035
    cogs = tokens_cost + server + domain + acquiring + support + reserves
    margin = price - cogs
    margin_pct = margin / price * 100
    ue_rows.append([
        name,
        fmt_rub(price),
        fmt_rub(tokens_cost),
        fmt_rub(server),
        fmt_rub(domain),
        fmt_rub(acquiring),
        fmt_rub(support),
        fmt_rub(reserves),
        fmt_rub(cogs),
        fmt_rub(margin),
        f"{margin_pct:.1f}%",
    ])
t = Table(ue_rows, colWidths=[24 * mm, 18 * mm, 18 * mm, 20 * mm, 16 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm, 18 * mm, 16 * mm])
ts = header_style(ue_rows, 11)
ts.add("BACKGROUND", (-2, 1), (-2, -1), SUCCESS_LIGHT)
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_LIGHT)
ts.add("FONTNAME", (-2, 1), (-2, -1), BOLD_FONT)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Расшифровка:</b> Себест = себестоимость 1 клиента в месяц. Маржа = что остаётся нам с одного платежа клиента. "
    "Поддержка = средняя стоимость обслуживания тарифа (саппорт-время × ставка). "
    "Резервы = доля на возвраты и риски (3.5% от цены).",
    NOTE,
))
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Пожизненная выручка (LTV) и стоимость привлечения (CAC) по тарифам", H3))
ltv_cac_rows = [["Тариф", "Маржа ₽/мес", "Месячный отвал %", "Срок жизни (мес)", "Пожизн.выручка ₽", "Бюджет CAC ₽"]]
for name, price, wallet, server, domain, churn, life, support in ue_data:
    tokens_cost = wallet / markup
    acquiring = price * 0.028
    reserves = price * 0.035
    cogs = tokens_cost + server + domain + acquiring + support + reserves
    margin = price - cogs
    ltv = margin * life
    cac_budget = ltv / 3
    ltv_cac_rows.append([
        name,
        fmt_rub(margin),
        f"{churn*100:.1f}%",
        f"{life} мес",
        fmt_rub(ltv),
        fmt_rub(cac_budget),
    ])

t = Table(ltv_cac_rows, colWidths=[35 * mm, 30 * mm, 30 * mm, 30 * mm, 35 * mm, 30 * mm])
ts = header_style(ltv_cac_rows, 6)
ts.add("BACKGROUND", (-2, 1), (-2, -1), SUCCESS_LIGHT)
ts.add("BACKGROUND", (-1, 1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (-2, 1), (-2, -1), BOLD_FONT)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Расшифровка:</b> LTV = Lifetime Value = Пожизненная выручка с клиента (маржа × средний срок жизни). "
    "CAC = Customer Acquisition Cost = Стоимость привлечения нового клиента. Правило: CAC ≤ LTV / 3 "
    "(чтобы за каждый рубль вложенный в рекламу получать минимум 3 рубля прибыли).",
    NOTE,
))
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Главный вывод:</b> Pro и Enterprise дают <b>в 8-13 раз больше пожизненной выручки</b> чем Lite. "
    "Бюджет привлечения для Enterprise = 154 К ₽/клиент — это можно потратить на B2B-продажника + LinkedIn-рекламу. "
    "Для Lite — всего 5.7 К ₽/клиент, поэтому выживаем только за счёт массового дешёвого трафика (Telegram + контент).",
    NOTE,
))
story.append(PageBreak())


# ====================================================================== #
# 12c. Три сценария: песимист / реалист / оптимист                       #
# ====================================================================== #
page_title(
    "12c. Три сценария развития: песимистичный / реалистичный / оптимистичный",
    "Все цифры в реалистичном сценарии. Песимист = что если маркетинг работает в 2 раза хуже. Оптимист = если виралим на VC.ru/Habr.",
)

scenarios_compare = [
    ["Метрика", "Песимистичный", "Реалистичный (база)", "Оптимистичный"],
    ["Платящих к M6", "150", "300", "500"],
    ["Платящих к M12", "950", "1 670", "2 500"],
    ["Платящих к M24", "4 500", "6 250", "9 000"],
    ["ARPU (M24, ₽)", "3 500", "4 160", "5 000"],
    ["Выручка/мес M24, ₽", "15.7 М", "26 М", "45 М"],
    ["Выручка/год M24, ₽", "189 М", "312 М", "540 М"],
    ["Первая прибыль", "M14", "M11", "M8"],
    ["Возврат вложений", "M19", "M14", "M10"],
    ["Самый большой минус", "−4.2 М ₽", "−2.4 М ₽", "−1.1 М ₽"],
    ["Стартовый капитал", "5 М ₽", "3 М ₽", "1.5 М ₽"],
    ["Деньги на счёте M24", "+22 М ₽", "+67 М ₽", "+140 М ₽"],
    ["Когда нанимать senior dev", "M14", "M10", "M7"],
    ["Команда к M24", "10 чел", "13 чел", "18 чел"],
]
t = Table(scenarios_compare, colWidths=[60 * mm, 50 * mm, 55 * mm, 50 * mm])
ts = header_style(scenarios_compare, 4)
# Color columns
for i in range(1, len(scenarios_compare)):
    ts.add("BACKGROUND", (1, i), (1, i), WARN_LIGHT)
    ts.add("BACKGROUND", (2, i), (2, i), ACCENT_LIGHT)
    ts.add("BACKGROUND", (3, i), (3, i), SUCCESS_LIGHT)
ts.add("FONTNAME", (2, 1), (2, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("Что меняется между сценариями", H3))
scenario_factors = [
    ["Фактор", "Песимист", "Реалист", "Оптимист"],
    ["Конверсия посадочной (визит → пробник)", "2.5%", "4.0%", "6.0%"],
    ["Переход из пробника в платящего", "5%", "7%", "10%"],
    ["Цена клика средняя", "95 ₽", "75 ₽", "55 ₽"],
    ["Месячный отвал клиентов (Lite)", "10%", "7%", "5%"],
    ["Сила бренд-узнаваемости с M6", "слабая", "средняя", "сильная"],
    ["Реакция СМИ на запуск", "тишина", "пара статей", "VC.ru топ + Habr хит"],
    ["Доля Pro/Enterprise клиентов", "20%", "25%", "35%"],
]
t = Table(scenario_factors, colWidths=[80 * mm, 35 * mm, 35 * mm, 35 * mm])
t.setStyle(header_style(scenario_factors, 4))
story.append(t)
story.append(Spacer(1, 4 * mm))

story.append(Paragraph(
    "<b>Что использовать в плане:</b> для расчёта стартового капитала и зарплат — берём <b>песимистичный</b> "
    "(нужно 5 М ₽ запас, а не 3 М). Для коммуникации инвесторам / партнёрам — <b>реалистичный</b>. "
    "Для мотивации команды — <b>оптимистичный</b>. Никогда не строить план найма по оптимистичному.",
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
    ["SMB-аудитория ✓", "Крупный бизнес (автосалоны, ЖК, застройщики)"],
    ["Малый/средний бюджет (Lite-Pro 990-7990)", "Большой бюджет (>50К/мес — у нас не клиент)"],
]
t = Table(markers, colWidths=[100 * mm, 110 * mm])
ts = header_style(markers, 2)
ts.add("BACKGROUND", (0, 0), (0, 0), SUCCESS_LIGHT)
ts.add("BACKGROUND", (1, 0), (1, 0), WARN_LIGHT)
ts.add("TEXTCOLOR", (0, 0), (0, 0), INK)
ts.add("TEXTCOLOR", (1, 0), (1, 0), INK)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("5-проходная фильтрация (чтобы не вкладывать в маркетинг впустую)", H3))
filter_passes = [
    ["Проход", "Что отсеиваем", "Сколько ключей убрали"],
    ["Проход 1: явный мусор", "Слова «бесплатно/торрент/скачать», бренды конкурентов целиком", "8 ключей (тильда, создать сайт, сделать сайт, сайт бесплатно, и т.д.)"],
    ["Проход 2: проверка на namерение купить", "Запросы без сигнала покупки (просто исследование)", "0 (все оставшиеся имеют intent)"],
    ["Проход 3: соответствие нашей нише (SMB/малый бизнес)", "Крупные корпоративные сегменты", "2 (сайт автосалона, сайт жк)"],
    ["Проход 4: соответствие цене подписки", "Сегменты где минимум сайт за 500К+ от студии", "2 (сайт застройщика, сайт медцентра)"],
    ["Проход 5: окончательная проверка стоимости клика", "CPC > 200 ₽ при низком чеке", "0 (всё проходит)"],
    ["ИТОГО осталось", "59 чистейших ключей из 71 исходных", "12 убрано (17%)"],
]
t = Table(filter_passes, colWidths=[55 * mm, 90 * mm, 65 * mm])
ts = header_style(filter_passes, 3)
ts.add("BACKGROUND", (0, -1), (-1, -1), ACCENT_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD_FONT)
t.setStyle(ts)
story.append(t)
story.append(PageBreak())


# ====================================================================== #
# 14. Семантическое ядро · 63 чистых запроса                              #
# ====================================================================== #
page_title(
    "14. Семантическое ядро · 59 ЧИСТЕЙШИХ запросов после 5-кратной фильтрации",
    "После повторной проверки убрали 4 borderline-ключа: «сайт жк», «сайт медцентра», «сайт автосалона», «сайт застройщика» — крупная аудитория не наша SMB или дорогой аукцион.",
)

# Aggregates after re-filter
agg = [
    ["Категория", "Ключей", "Показов/мес", "Средняя цена клика ₽"],
    ["A. Намерение купить", "5", "47 500", "98"],
    ["B. AI ★ ПРИОРИТЕТ", "9", "16 650", "85"],
    ["C. Сравнение вариантов", "4", "4 000", "72"],
    ["D. Кафе / Общепит", "6", "11 900", "78"],
    ["E. Интернет-магазин", "5", "20 600", "121"],
    ["F. Юрист", "5", "5 300", "102"],
    ["G. Красота", "5", "7 800", "78"],
    ["H. Медицина (без медцентра)", "4", "6 100", "119"],
    ["I. Авто (без автосалона)", "3", "2 300", "75"],
    ["J. Недвижимость (без ЖК и застройщика)", "2", "2 700", "110"],
    ["K. Образование", "5", "7 500", "87"],
    ["L. Боль-ориентированные ★", "6", "5 300", "72"],
    ["ИТОГО", "59", "137 050", "91"],
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
    ("H. Медицина (после re-filter)", [
        ("сайт клиники", "2 000", "145"),
        ("сайт врача", "1 800", "95"),
        ("сайт стоматологии", "1 500", "130"),
        ("сайт ветклиники", "800", "105"),
    ]),
    ("I. Авто / Сервис (без автосалона)", [
        ("сайт автосервиса", "1 200", "85"),
        ("сайт шиномонтажа", "600", "65"),
        ("сайт детейлинга", "500", "75"),
    ]),
    ("J. Недвижимость (без ЖК и застройщика)", [
        ("сайт агентства недвижимости", "1 500", "125"),
        ("сайт риэлтора", "1 200", "95"),
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
