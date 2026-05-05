"""Generate docs/Token_Economics_v1.xlsx — interactive token-economy calculator.

8 sheets:
  1. Inputs        — editable parameters (markup, FX, msg size)
  2. Models        — 8 LLMs with input/output $/M, our cost ₽/M, retail ₽/M
  3. Per-message   — cost per single message (input + output)
  4. Volumes       — 50 / 200 / 1000 messages on each model
  5. Tariff cover  — how many messages each wallet buys on key models
  6. Mix scenarios — 4 user profiles (MVP / balanced / premium / 152-FZ)
  7. Tariff margin — gross margin per tier with COGS broken down
  8. Sensitivity   — what if msg size = 4K / 8K / 16K / 30K

Blue cells are inputs (you change them). Black cells are formulas.
"""
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

OUT = Path("docs/Token_Economics_v1.xlsx")
OUT.parent.mkdir(parents=True, exist_ok=True)

wb = openpyxl.Workbook()
wb.remove(wb.active)

# --- styles ---
THIN = Font(name="Calibri", size=11)
BOLD = Font(name="Calibri", size=11, bold=True)
TITLE = Font(name="Calibri", size=14, bold=True)
HEAD = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
INPUT = Font(name="Calibri", size=11, color="0000FF")
NOTE = Font(name="Calibri", size=10, italic=True, color="6B7280")

HEAD_FILL = PatternFill("solid", start_color="1F2937")
ACCENT_FILL = PatternFill("solid", start_color="EEF0FF")
INPUT_FILL = PatternFill("solid", start_color="FEF3C7")
GOOD_FILL = PatternFill("solid", start_color="DCFCE7")
WARN_FILL = PatternFill("solid", start_color="FFE4E6")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")

THIN_BORDER = Border(
    left=Side(style="thin", color="E5E7EB"),
    right=Side(style="thin", color="E5E7EB"),
    top=Side(style="thin", color="E5E7EB"),
    bottom=Side(style="thin", color="E5E7EB"),
)


def write_title(ws, row, text, sub=None):
    ws.cell(row=row, column=1, value=text).font = TITLE
    if sub:
        ws.cell(row=row + 1, column=1, value=sub).font = NOTE
        ws.row_dimensions[row + 1].height = 32


def write_head(ws, row, headers):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = HEAD
        c.fill = HEAD_FILL
        c.alignment = CENTER
        c.border = THIN_BORDER
    ws.row_dimensions[row].height = 36


def write_row(ws, row, values, fmt=None, bold=False, fill=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = BOLD if bold else THIN
        c.border = THIN_BORDER
        if fmt:
            c.number_format = fmt
        if fill:
            c.fill = fill
        if isinstance(v, str) and v.startswith("="):
            c.font = THIN if not bold else BOLD


def col_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ====================================================================== #
# Sheet 1 — Inputs                                                       #
# ====================================================================== #
ws = wb.create_sheet("1. Параметры")
write_title(
    ws,
    1,
    "Omnia.AI · Токен-экономика — параметры (v1)",
    "Все жёлтые ячейки — input. Меняй и пересчитай. Чёрные — формулы.",
)

ws["A4"] = "Параметр"
ws["A4"].font = HEAD
ws["A4"].fill = HEAD_FILL
ws["B4"] = "Значение"
ws["B4"].font = HEAD
ws["B4"].fill = HEAD_FILL
ws["C4"] = "Комментарий"
ws["C4"].font = HEAD
ws["C4"].fill = HEAD_FILL
ws.row_dimensions[4].height = 32

inputs = [
    ("Курс ₽/$", 100, "Базовый курс на 2025"),
    ("Markup на токены", 2.8, "Себестоимость + ~64% маржа на токенах"),
    ("Output share", 0.5, "Доля output в общем объёме токенов"),
    ("Размер сообщения, токенов", 8000, "5 000 input + 3 000 output (consrv. среднее)"),
]
for i, (k, v, n) in enumerate(inputs, start=5):
    ws.cell(row=i, column=1, value=k).font = THIN
    c = ws.cell(row=i, column=2, value=v)
    c.font = INPUT
    c.fill = INPUT_FILL
    if isinstance(v, float):
        c.number_format = "0.0"
    ws.cell(row=i, column=3, value=n).font = NOTE
    ws.cell(row=i, column=3).alignment = WRAP

col_widths(ws, [40, 18, 60])

# Named cell references for use in other sheets
FX = "'1. Параметры'!$B$5"
MARKUP = "'1. Параметры'!$B$6"
OUT_SHARE = "'1. Параметры'!$B$7"
MSG_SIZE = "'1. Параметры'!$B$8"


# ====================================================================== #
# Sheet 2 — Models                                                       #
# ====================================================================== #
ws = wb.create_sheet("2. Модели LLM")
write_title(
    ws,
    1,
    "8 моделей · себестоимость и retail-цена",
    "Cost ₽/M = (input × output_share + output × output_share) × FX. Retail ₽/M = cost × markup.",
)

write_head(
    ws,
    4,
    ["Модель", "Категория", "Input $/1M", "Output $/1M", "Себест. ₽/1M", "Retail ₽/1M"],
)

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

for i, (name, cat, inp, out) in enumerate(models, start=5):
    ws.cell(row=i, column=1, value=name).font = THIN
    ws.cell(row=i, column=2, value=cat).font = THIN
    ws.cell(row=i, column=3, value=inp).font = THIN
    ws.cell(row=i, column=3).number_format = "0.00"
    ws.cell(row=i, column=4, value=out).font = THIN
    ws.cell(row=i, column=4).number_format = "0.00"
    # Cost ₽/M = (input × (1 - out_share) + output × out_share) × FX
    ws.cell(
        row=i,
        column=5,
        value=f"=(C{i}*(1-{OUT_SHARE})+D{i}*{OUT_SHARE})*{FX}",
    ).number_format = "#,##0 ₽"
    # Retail ₽/M = cost × markup
    ws.cell(row=i, column=6, value=f"=E{i}*{MARKUP}").number_format = "#,##0 ₽"

# borders
for r in range(4, 4 + len(models) + 1):
    for c in range(1, 7):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [32, 22, 14, 14, 18, 18])


# ====================================================================== #
# Sheet 3 — Per-message                                                  #
# ====================================================================== #
ws = wb.create_sheet("3. Цена сообщения")
write_title(
    ws,
    1,
    "Стоимость 1 сообщения · 8 000 токенов",
    "1 сообщение = размер_сообщения / 1 000 000 миллионов токенов. Меняй msg_size в 1.Параметры.",
)

write_head(
    ws,
    4,
    ["Модель", "Себест. ₽/msg", "Retail ₽/msg", "Маржа ₽/msg", "Маржа %"],
)

for i, (name, _, _, _) in enumerate(models, start=5):
    src = i  # row number on Models sheet
    ws.cell(row=i, column=1, value=name).font = THIN
    # Cost per msg = cost_per_M × (msg_size / 1 000 000)
    ws.cell(
        row=i,
        column=2,
        value=f"='2. Модели LLM'!E{src}*{MSG_SIZE}/1000000",
    ).number_format = "0.00 ₽"
    ws.cell(
        row=i,
        column=3,
        value=f"='2. Модели LLM'!F{src}*{MSG_SIZE}/1000000",
    ).number_format = "0.00 ₽"
    ws.cell(row=i, column=4, value=f"=C{i}-B{i}").number_format = "0.00 ₽"
    ws.cell(row=i, column=5, value=f"=(C{i}-B{i})/C{i}").number_format = "0.0%"

for r in range(4, 4 + len(models) + 1):
    for c in range(1, 6):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [32, 16, 16, 16, 14])


# ====================================================================== #
# Sheet 4 — Volumes 50/200/1000                                          #
# ====================================================================== #
ws = wb.create_sheet("4. Объёмы 50-200-1000")
write_title(
    ws,
    1,
    "Сколько стоит 50 / 200 / 1 000 сообщений",
    "Retail-цена что заплатит пользователь · меняй msg_size в 1.Параметры.",
)

write_head(
    ws,
    4,
    ["Модель", "50 сообщений", "200 сообщений", "1 000 сообщений", "Токенов всего"],
)

for i, (name, _, _, _) in enumerate(models, start=5):
    ws.cell(row=i, column=1, value=name).font = THIN
    # Use cost/msg from sheet 3
    ws.cell(row=i, column=2, value=f"='3. Цена сообщения'!C{i}*50").number_format = (
        "#,##0 ₽"
    )
    ws.cell(row=i, column=3, value=f"='3. Цена сообщения'!C{i}*200").number_format = (
        "#,##0 ₽"
    )
    ws.cell(row=i, column=4, value=f"='3. Цена сообщения'!C{i}*1000").number_format = (
        "#,##0 ₽"
    )
    ws.cell(row=i, column=5, value=f"=1000*{MSG_SIZE}/1000000").number_format = "0.00 М"

# Add reference row showing token volumes
ws.cell(row=14, column=1, value="Токенов суммарно (для 1 000 msg)").font = NOTE
ws.cell(row=14, column=2, value=f"=50*{MSG_SIZE}").number_format = "#,##0"
ws.cell(row=14, column=3, value=f"=200*{MSG_SIZE}").number_format = "#,##0"
ws.cell(row=14, column=4, value=f"=1000*{MSG_SIZE}").number_format = "#,##0"
ws.cell(row=14, column=5, value="токенов").font = NOTE

for r in range(4, 14):
    for c in range(1, 6):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [32, 16, 16, 18, 16])


# ====================================================================== #
# Sheet 5 — Tariff coverage                                              #
# ====================================================================== #
ws = wb.create_sheet("5. Кошелёк → сообщения")
write_title(
    ws,
    1,
    "Сколько сообщений покрывает кошелёк каждого тарифа",
    "Если пользователь использует только одну модель.",
)

write_head(
    ws,
    4,
    [
        "Тариф",
        "Кошелёк ₽",
        "DeepSeek",
        "Qwen",
        "Gemini Flash",
        "Haiku 4.5",
        "GigaChat",
        "GPT-4.1",
        "Sonnet 4.6",
        "YandexGPT",
    ],
)

tariffs = [
    ("Free (5 дней)", 500),
    ("Lite", 1000),
    ("Starter", 2500),
    ("Pro", 6000),
    ("Enterprise", 18000),
]

for i, (name, wallet) in enumerate(tariffs, start=5):
    ws.cell(row=i, column=1, value=name).font = THIN
    c = ws.cell(row=i, column=2, value=wallet)
    c.font = INPUT
    c.fill = INPUT_FILL
    c.number_format = "#,##0 ₽"
    # For each model: wallet / retail_per_msg (rounded down)
    for col, model_row in enumerate(range(5, 13), start=3):
        cell = ws.cell(
            row=i,
            column=col,
            value=f"=ROUNDDOWN(B{i}/'3. Цена сообщения'!C{model_row},0)",
        )
        cell.number_format = "#,##0"

for r in range(4, 4 + len(tariffs) + 1):
    for c in range(1, 11):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [22, 14, 12, 12, 14, 14, 12, 12, 14, 14])


# ====================================================================== #
# Sheet 6 — Mix scenarios                                                #
# ====================================================================== #
ws = wb.create_sheet("6. Mix-сценарии")
write_title(
    ws,
    1,
    "4 типичных профиля пользователя",
    "Меняй веса в столбце B — пересчёт автоматический.",
)

# Four profiles, each with shares for 8 models
ws["A4"] = "Модель"
ws["A4"].font = HEAD
ws["A4"].fill = HEAD_FILL
profile_names = [
    "A. MVP-эконом",
    "B. Балансный",
    "C. Премиум",
    "D. 152-ФЗ",
]
for col, name in enumerate(profile_names, start=2):
    c = ws.cell(row=4, column=col, value=name)
    c.font = HEAD
    c.fill = HEAD_FILL
    c.alignment = CENTER

# share matrix:                  A     B     C     D
shares = [
    ("DeepSeek V3.2",            0.70, 0.40, 0.00, 0.00),
    ("Qwen 3 235B",              0.00, 0.00, 0.00, 0.00),
    ("Gemini 2.5 Flash",         0.00, 0.20, 0.00, 0.00),
    ("Claude Haiku 4.5",         0.20, 0.30, 0.30, 0.00),
    ("GigaChat 2 Pro",           0.00, 0.00, 0.00, 0.30),
    ("GPT-4.1",                  0.00, 0.00, 0.20, 0.00),
    ("Claude Sonnet 4.6",        0.10, 0.10, 0.50, 0.10),
    ("YandexGPT 5 Pro",          0.00, 0.00, 0.00, 0.60),
]
for i, row in enumerate(shares, start=5):
    ws.cell(row=i, column=1, value=row[0]).font = THIN
    for col, val in enumerate(row[1:], start=2):
        c = ws.cell(row=i, column=col, value=val)
        c.font = INPUT if val > 0 else THIN
        if val > 0:
            c.fill = INPUT_FILL
        c.number_format = "0%"

# Sum row (sanity check)
ws.cell(row=13, column=1, value="Сумма (должна = 100%)").font = BOLD
for col in range(2, 6):
    cl = get_column_letter(col)
    c = ws.cell(row=13, column=col, value=f"=SUM({cl}5:{cl}12)")
    c.font = BOLD
    c.number_format = "0%"

# Cost-per-msg row (weighted average using sheet 3)
ws.cell(row=15, column=1, value="Себест. ₽/msg").font = BOLD
ws.cell(row=15, column=1).fill = HEAD_FILL
ws.cell(row=15, column=1).font = HEAD
for col in range(2, 6):
    cl = get_column_letter(col)
    formula = f"=SUMPRODUCT({cl}5:{cl}12,'3. Цена сообщения'!B5:B12)"
    c = ws.cell(row=15, column=col, value=formula)
    c.number_format = "0.00 ₽"
    c.font = BOLD

ws.cell(row=16, column=1, value="Retail ₽/msg").font = BOLD
ws.cell(row=16, column=1).fill = HEAD_FILL
ws.cell(row=16, column=1).font = HEAD
for col in range(2, 6):
    cl = get_column_letter(col)
    formula = f"=SUMPRODUCT({cl}5:{cl}12,'3. Цена сообщения'!C5:C12)"
    c = ws.cell(row=16, column=col, value=formula)
    c.number_format = "0.00 ₽"
    c.font = BOLD
    c.fill = ACCENT_FILL

# Volumes per profile
ws.cell(row=18, column=1, value="50 сообщений (₽)").font = THIN
ws.cell(row=19, column=1, value="200 сообщений (₽)").font = THIN
ws.cell(row=20, column=1, value="1 000 сообщений (₽)").font = THIN
for col in range(2, 6):
    cl = get_column_letter(col)
    for i, mul in enumerate([50, 200, 1000]):
        c = ws.cell(
            row=18 + i,
            column=col,
            value=f"={cl}16*{mul}",
        )
        c.number_format = "#,##0 ₽"

# Wallet coverage per profile
ws.cell(row=22, column=1, value="Сообщений на 1 000 ₽ кошелёк (Lite)").font = THIN
ws.cell(row=23, column=1, value="Сообщений на 2 500 ₽ (Starter)").font = THIN
ws.cell(row=24, column=1, value="Сообщений на 6 000 ₽ (Pro)").font = THIN
ws.cell(row=25, column=1, value="Сообщений на 18 000 ₽ (Enterprise)").font = THIN
for col in range(2, 6):
    cl = get_column_letter(col)
    for i, w in enumerate([1000, 2500, 6000, 18000]):
        c = ws.cell(
            row=22 + i,
            column=col,
            value=f"=ROUNDDOWN({w}/{cl}16,0)",
        )
        c.number_format = "#,##0"

for r in range(4, 26):
    for c in range(1, 6):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [42, 18, 18, 18, 18])


# ====================================================================== #
# Sheet 7 — Tariff margin                                                #
# ====================================================================== #
ws = wb.create_sheet("7. Маржа по тарифам")
write_title(
    ws,
    1,
    "Маржа платформы при условии что user сжигает весь кошелёк",
    "Профиль B (балансный) — типичный SMB. Меняй цены/кошельки в синих ячейках.",
)

write_head(
    ws,
    4,
    [
        "Тариф",
        "Цена ₽/мес",
        "Кошелёк ₽",
        "LLM-COGS ₽",
        "Сервер COGS ₽",
        "Платёжная комиссия (3%)",
        "Прочее (+10%)",
        "Маржа ₽/мес",
        "Маржа %",
    ],
)

# Server costs from business plan
tariff_full = [
    ("Free", 0, 500, 0),
    ("Lite", 990, 1000, 0),
    ("Starter", 2990, 2500, 600),
    ("Pro", 7990, 6000, 3000),
    ("Enterprise", 19990, 18000, 8000),
]

for i, (name, price, wallet, server) in enumerate(tariff_full, start=5):
    ws.cell(row=i, column=1, value=name).font = THIN
    # Price
    c = ws.cell(row=i, column=2, value=price)
    c.font = INPUT
    c.fill = INPUT_FILL
    c.number_format = "#,##0 ₽"
    # Wallet
    c = ws.cell(row=i, column=3, value=wallet)
    c.font = INPUT
    c.fill = INPUT_FILL
    c.number_format = "#,##0 ₽"
    # LLM-COGS = wallet × (cost / retail) of profile B
    # = wallet × (B15 / B16) on Mix sheet (col B = profile B... wait that's profile A)
    # Actually columns: 2=A (col B in Excel), 3=B (col C), 4=C (col D), 5=D (col E)
    # Profile B is col C in Excel
    formula_llm_cogs = (
        f"=C{i}*'6. Mix-сценарии'!C15/'6. Mix-сценарии'!C16"
    )
    ws.cell(row=i, column=4, value=formula_llm_cogs).number_format = "#,##0 ₽"
    # Server COGS
    c = ws.cell(row=i, column=5, value=server)
    c.number_format = "#,##0 ₽"
    # Payment commission (3% of price)
    ws.cell(row=i, column=6, value=f"=B{i}*0.03").number_format = "#,##0 ₽"
    # Other COGS (10% of price)
    ws.cell(row=i, column=7, value=f"=B{i}*0.10").number_format = "#,##0 ₽"
    # Margin = Price - LLM-COGS - Server COGS - Commission - Other
    ws.cell(
        row=i,
        column=8,
        value=f"=B{i}-D{i}-E{i}-F{i}-G{i}",
    ).number_format = "#,##0 ₽"
    ws.cell(row=i, column=8).fill = (
        WARN_FILL if price < 1000 else GOOD_FILL
    )
    # Margin %
    ws.cell(
        row=i,
        column=9,
        value=f"=IF(B{i}=0,0,H{i}/B{i})",
    ).number_format = "0.0%"

for r in range(4, 4 + len(tariff_full) + 1):
    for c in range(1, 10):
        ws.cell(row=r, column=c).border = THIN_BORDER

# notes
ws.cell(
    row=12,
    column=1,
    value="Free отрицателен = это lead-magnet. Окупается через 12% conversion в Lite.",
).font = NOTE
ws.cell(
    row=13,
    column=1,
    value="LLM-COGS считается через Mix-профиль B. Если user полностью на DeepSeek — маржа выше; если на Sonnet — может уйти в минус.",
).font = NOTE

col_widths(ws, [22, 14, 14, 16, 16, 16, 14, 16, 12])


# ====================================================================== #
# Sheet 8 — Sensitivity                                                  #
# ====================================================================== #
ws = wb.create_sheet("8. Размер сообщения")
write_title(
    ws,
    1,
    "Чувствительность к размеру сообщения",
    "Если средний msg = 4K (мелкие правки) / 8K (стандарт) / 16K (большие фичи) / 30K (полная страница)",
)

write_head(
    ws,
    4,
    ["Модель", "4 000 ток.", "8 000 ток.", "16 000 ток.", "30 000 ток."],
)

# Show how many messages 6 000 ₽ wallet (Pro) covers per model and msg size
ws["A4"].value = "Модель (на 6 000 ₽ кошелёк = Pro)"

for i, (name, _, _, _) in enumerate(models, start=5):
    # retail per token = retail_per_M / 1M
    src_row = i
    ws.cell(row=i, column=1, value=name).font = THIN
    for col, ts in enumerate([4000, 8000, 16000, 30000], start=2):
        # msg cost = retail_per_M × ts / 1M
        # msg count = wallet / msg_cost = 6000 / (retail × ts / 1M) = 6000 × 1M / (retail × ts)
        formula = f"=ROUNDDOWN(6000*1000000/('2. Модели LLM'!F{src_row}*{ts}),0)"
        c = ws.cell(row=i, column=col, value=formula)
        c.number_format = "#,##0"

for r in range(4, 4 + len(models) + 1):
    for c in range(1, 6):
        ws.cell(row=r, column=c).border = THIN_BORDER

ws.cell(
    row=14,
    column=1,
    value="Размер сообщения зависит от сложности задачи.",
).font = NOTE
ws.cell(
    row=15,
    column=1,
    value="• 4K — «измени цвет», «передвинь блок» (мелкие правки)",
).font = NOTE
ws.cell(
    row=16,
    column=1,
    value="• 8K — стандарт: добавить секцию, изменить логику формы",
).font = NOTE
ws.cell(
    row=17,
    column=1,
    value="• 16K — фича целиком: новая страница с интеграцией",
).font = NOTE
ws.cell(
    row=18,
    column=1,
    value="• 30K — полная переделка: миграция БД + рефактор",
).font = NOTE

col_widths(ws, [38, 14, 14, 16, 16])


# ====================================================================== #
# Sheet 9 — Top-up                                                       #
# ====================================================================== #
ws = wb.create_sheet("9. Топ-up пакеты")
write_title(
    ws,
    1,
    "Дополнительные пакеты токенов поверх подписки",
    "Скидка на крупные пакеты — стимул retention и upsell.",
)

write_head(
    ws,
    4,
    [
        "Пакет (номинал)",
        "Цена клиенту",
        "Скидка",
        "DeepSeek msg",
        "Haiku msg",
        "Sonnet msg",
        "YandexGPT msg",
    ],
)

packs = [
    ("500 ₽", 500, 0),
    ("2 000 ₽", 1800, 0.10),
    ("5 000 ₽", 4250, 0.15),
    ("10 000 ₽", 8000, 0.20),
    ("25 000 ₽", 18750, 0.25),
]
# DS = row 5, Haiku = row 8, Sonnet = row 11, Yandex = row 12 on sheet 3
for i, (label, price, disc) in enumerate(packs, start=5):
    ws.cell(row=i, column=1, value=label).font = THIN
    c = ws.cell(row=i, column=2, value=price)
    c.font = INPUT
    c.fill = INPUT_FILL
    c.number_format = "#,##0 ₽"
    c = ws.cell(row=i, column=3, value=disc)
    c.number_format = "0%"
    # face value of tokens given to user = price / (1 - disc) effectively
    # but simpler: msg_count = (price / (1-disc)) / cost_per_msg... wait
    # Actually pack pays for `nominal` worth of tokens (= label) but customer pays `price`.
    # So tokens delivered = nominal_value at retail price → number of msgs = nominal / retail_per_msg
    nominal = [500, 2000, 5000, 10000, 25000][i - 5]
    ws.cell(
        row=i,
        column=4,
        value=f"=ROUNDDOWN({nominal}/'3. Цена сообщения'!C5,0)",
    ).number_format = "#,##0"
    ws.cell(
        row=i,
        column=5,
        value=f"=ROUNDDOWN({nominal}/'3. Цена сообщения'!C8,0)",
    ).number_format = "#,##0"
    ws.cell(
        row=i,
        column=6,
        value=f"=ROUNDDOWN({nominal}/'3. Цена сообщения'!C11,0)",
    ).number_format = "#,##0"
    ws.cell(
        row=i,
        column=7,
        value=f"=ROUNDDOWN({nominal}/'3. Цена сообщения'!C12,0)",
    ).number_format = "#,##0"

for r in range(4, 4 + len(packs) + 1):
    for c in range(1, 8):
        ws.cell(row=r, column=c).border = THIN_BORDER

col_widths(ws, [16, 16, 12, 14, 14, 14, 16])


wb.save(OUT)
print(f"OK saved: {OUT}")
print(f"Sheets ({len(wb.sheetnames)}): {wb.sheetnames}")
print(f"Size: {OUT.stat().st_size:,} bytes")
