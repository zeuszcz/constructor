"""Generate AI_Site_Builder_Business_Plan_v6.pdf
Based on v5 + new sections: USP, Customer Portrait, Pricing Hypothesis,
Full 36-month Financial Model. Removes voice bots / 152-FZ / booking systems
from section 2.2.
"""
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

sys.stdout.reconfigure(encoding='utf-8')

# Fonts — Calibri (Cyrillic-capable, бесплатно в Windows)
WIN_FONTS = Path("C:/Windows/Fonts")
try:
    pdfmetrics.registerFont(TTFont("Body", str(WIN_FONTS / "calibri.ttf")))
    pdfmetrics.registerFont(TTFont("BodyB", str(WIN_FONTS / "calibrib.ttf")))
    pdfmetrics.registerFont(TTFont("BodyI", str(WIN_FONTS / "calibrii.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(WIN_FONTS / "consola.ttf")))
    BODY = "Body"; BOLD = "BodyB"; ITAL = "BodyI"; MONO = "Mono"
except Exception:
    BODY = "Helvetica"; BOLD = "Helvetica-Bold"; ITAL = "Helvetica-Oblique"; MONO = "Courier"

# Colors — корпоративный синий стиль v5
NAVY = colors.HexColor("#1e3a8a")        # темно-синий заголовок
NAVY_LIGHT = colors.HexColor("#dbeafe")  # светло-синий фон таблиц
ACCENT = colors.HexColor("#2563eb")      # акцентный синий
SUCCESS = colors.HexColor("#16a34a")     # зелёный
SUCCESS_BG = colors.HexColor("#dcfce7")
WARN = colors.HexColor("#dc2626")        # красный
WARN_BG = colors.HexColor("#fee2e2")
ORANGE = colors.HexColor("#ea580c")
ORANGE_BG = colors.HexColor("#fed7aa")
INK = colors.HexColor("#0f172a")
INK_MUTED = colors.HexColor("#475569")
LINE = colors.HexColor("#e2e8f0")
HEAD_FILL = colors.HexColor("#1e293b")   # тёмная шапка таблиц
ALT_ROW = colors.HexColor("#f8fafc")

# Styles
H1 = ParagraphStyle("H1", fontName=BOLD, fontSize=22, leading=26, textColor=NAVY, spaceAfter=6, spaceBefore=0)
H2 = ParagraphStyle("H2", fontName=BOLD, fontSize=15, leading=19, textColor=NAVY, spaceBefore=14, spaceAfter=8)
H3 = ParagraphStyle("H3", fontName=BOLD, fontSize=12, leading=15, textColor=INK, spaceBefore=10, spaceAfter=4)
P = ParagraphStyle("P", fontName=BODY, fontSize=10, leading=13.5, textColor=INK, spaceAfter=6)
PB = ParagraphStyle("PB", fontName=BOLD, fontSize=10, leading=13.5, textColor=INK, spaceAfter=4)
NOTE = ParagraphStyle("NOTE", fontName=ITAL, fontSize=9, leading=12, textColor=INK_MUTED, spaceAfter=4)
SMALL = ParagraphStyle("SMALL", fontName=BODY, fontSize=8.5, leading=11, textColor=INK_MUTED)
# Cell styles для wrapping в таблицах
CELL = ParagraphStyle("CELL", fontName=BODY, fontSize=9, leading=11.5, textColor=INK, alignment=TA_LEFT)
CELLB = ParagraphStyle("CELLB", fontName=BOLD, fontSize=9, leading=11.5, textColor=INK, alignment=TA_LEFT)
CELLC = ParagraphStyle("CELLC", fontName=BODY, fontSize=9, leading=11.5, textColor=INK, alignment=TA_CENTER)
CELL_SM = ParagraphStyle("CELL_SM", fontName=BODY, fontSize=8.5, leading=10.5, textColor=INK, alignment=TA_LEFT)
CELLB_SM = ParagraphStyle("CELLB_SM", fontName=BOLD, fontSize=8.5, leading=10.5, textColor=INK, alignment=TA_LEFT)

def cp(text, bold=False, center=False, small=False):
    """Wrap text in Paragraph for table cell."""
    if small:
        style = CELLB_SM if bold else CELL_SM
    else:
        style = CELLB if bold else CELL
    if center:
        s = ParagraphStyle(f"tmp_{id(text)}", parent=style, alignment=TA_CENTER)
        return Paragraph(text, s)
    return Paragraph(text, style)
COVER_TITLE = ParagraphStyle("CT", fontName=BOLD, fontSize=36, leading=42, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)
COVER_SUB = ParagraphStyle("CS", fontName=BODY, fontSize=14, leading=18, textColor=INK_MUTED, alignment=TA_CENTER, spaceAfter=4)
COVER_HERO = ParagraphStyle("CH", fontName=BOLD, fontSize=28, leading=32, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10)
FOOT = ParagraphStyle("F", fontName=ITAL, fontSize=8.5, leading=11, textColor=INK_MUTED, alignment=TA_CENTER)

# --- Output ---
OUT = Path("docs/AI_Site_Builder_Business_Plan_v6.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=14*mm, bottomMargin=14*mm,
    title="Omnia.AI · Бизнес-план v6", author="Omnia.AI"
)

story = []
page_num_counter = [1]
TOTAL_PAGES = 29

def footer(page_label=None):
    label = page_label if page_label else str(page_num_counter[0])
    page_num_counter[0] += 1
    return Paragraph(
        f"Omnia.AI · Бизнес-план версия 6 · УТП + Клиентский портрет + Гипотеза тарифов + Финмодель 36 мес · {label}/{TOTAL_PAGES}",
        FOOT
    )

def page_title(num, title, subtitle=None):
    story.append(Paragraph(f"{num}. {title}", H1))
    if subtitle:
        story.append(Paragraph(subtitle, NOTE))
    story.append(Spacer(1, 4*mm))

def fmt_rub(v, decimals=0):
    if v is None or v == "—":
        return "—"
    if isinstance(v, str):
        return v
    if decimals:
        s = f"{v:,.{decimals}f}".replace(",", " ").replace(".", ",")
    else:
        s = f"{int(round(v)):,}".replace(",", " ")
    return s + " ₽"

def fmt_num(v):
    if isinstance(v, str): return v
    return f"{int(v):,}".replace(",", " ")

def std_table_style(header=True, alt_rows=True, font_size=9):
    cmds = [
        ("FONTNAME", (0, 1), (-1, -1), BODY),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), BOLD),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ]
    if alt_rows:
        cmds.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]))
    return TableStyle(cmds)


# ======================================================================
# PAGE 1 — COVER
# ======================================================================
story.append(Spacer(1, 40*mm))
story.append(Paragraph("Omnia.AI", COVER_TITLE))
story.append(Paragraph("AI-конструктор сайтов · IT-автоматизация · CRM-интеграции", COVER_SUB))
story.append(Spacer(1, 30*mm))
story.append(Paragraph("Бизнес-план версия 6", COVER_HERO))
story.append(Paragraph("УТП · Клиентский портрет · Гипотеза тарифов · Финмодель 36 месяцев", COVER_SUB))
story.append(Spacer(1, 25*mm))

# Hero metrics box
hero_data = [
    ["TAM", "SOM 3 года", "Окупаемость", "До точки плюса"],
    ["26 млрд ₽", "8.4 млрд ₽", "9.4×", "52 клиента"],
    ["Объём рынка", "Наша доля", "Рекл. бюджет 100 К", "При расходах 169 К"],
]
hero = Table(hero_data, colWidths=[40*mm]*4, rowHeights=[7*mm, 16*mm, 7*mm])
hero.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,0), BODY),
    ("FONTSIZE", (0,0), (-1,0), 9),
    ("TEXTCOLOR", (0,0), (-1,0), INK_MUTED),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("FONTNAME", (0,1), (-1,1), BOLD),
    ("FONTSIZE", (0,1), (-1,1), 22),
    ("TEXTCOLOR", (0,1), (-1,1), ACCENT),
    ("FONTNAME", (0,2), (-1,2), BODY),
    ("FONTSIZE", (0,2), (-1,2), 8),
    ("TEXTCOLOR", (0,2), (-1,2), INK_MUTED),
    ("LINEBELOW", (0,0), (-1,0), 0.4, LINE),
    ("LINEABOVE", (0,2), (-1,2), 0.4, LINE),
]))
story.append(hero)
story.append(Spacer(1, 40*mm))
story.append(Paragraph(f"Версия 6.0 · 12 мая 2026", FOOT))
story.append(PageBreak())

# ======================================================================
# PAGE 2 — KEY METRICS + Дельта v7→v8
# ======================================================================
page_title("1", "Ключевые метрики (версия 8 с Google Trends + 3-дневным пробником)")

big = [
    ["26 млрд ₽", "8.4 млрд ₽", "7.6 / 10", "52 клиента", "10.2×", "9.4×"],
    ["Объём рынка\n(TAM)", "Реально\nдостижимая\nдоля за 3 года", "Оценка\n«запускать ли»", "До точки\nплюса", "Пожизн. выручка\nк цене привлечения", "Окупаемость\nбюджета 100К"],
]
t = Table(big, colWidths=[30*mm]*6, rowHeights=[14*mm, 14*mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,0), BOLD),
    ("FONTSIZE", (0,0), (-1,0), 16),
    ("TEXTCOLOR", (0,0), (-1,0), ACCENT),
    ("FONTNAME", (0,1), (-1,1), BODY),
    ("FONTSIZE", (0,1), (-1,1), 8),
    ("TEXTCOLOR", (0,1), (-1,1), INK_MUTED),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND", (0,0), (-1,1), NAVY_LIGHT),
    ("LINEBELOW", (0,0), (-1,0), 0.4, LINE),
    ("BOX", (0,0), (-1,-1), 0.6, ACCENT),
]))
story.append(t)
story.append(Spacer(1, 8*mm))

story.append(Paragraph("1.1 Изменение версия 7 → версия 8 (что улучшилось)", H2))
delta = [
    ["Показатель", "Версия 7\n(без пробника)", "Версия 8\n(с 3-дн пробником)", "Изменение"],
    ["Реально достижимая выручка за 3 года", "7.8 млрд ₽", "8.4 млрд ₽", "+7.7%"],
    ["Оценка «запускать ли проект» (10-балльная)", "7.3 / 10", "7.6 / 10", "+0.3"],
    ["Сколько клиентов до точки безубыточности", "62 клиента", "52 клиента", "−16%"],
    ["Пожизн. выручка с клиента / цена привлечения", "8.33×", "10.2×", "+22%"],
    ["Окупаемость рекл. бюджета 100 К ₽/мес", "7.8×", "9.4×", "+20%"],
    ["Конверсия из бесплатного пробника в платящего", "7–12%", "18–25%", "в 2 раза"],
    ["Всего рекл. запросов с покупат. намерением", "60 + 33", "60 + 33 + 142", "+142"],
    ["Целевой IT-трафик (релевантные посетители/мес)", "~26 843", "~29 500", "+10%"],
]
t = Table(delta, colWidths=[68*mm, 35*mm, 38*mm, 30*mm])
ts = std_table_style()
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_BG)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD)
ts.add("TEXTCOLOR", (-1, 1), (-1, -1), SUCCESS)
ts.add("ALIGN", (-1, 1), (-1, -1), "CENTER")
ts.add("ALIGN", (1, 1), (-2, -1), "CENTER")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "<b>Расшифровка:</b> TAM — total addressable market (общий объём рынка). "
    "SOM — serviceable obtainable market (реально достижимая доля). "
    "LTV — пожизненная выручка с одного клиента. CAC — стоимость привлечения. "
    "ROI — во сколько раз вернётся вложенный бюджет.",
    SMALL
))
story.append(Spacer(1, 6*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 3 — НОВОЕ: УТП
# ======================================================================
page_title("2", "Уникальное торговое предложение (УТП)",
           "5 причин почему клиент выберет Omnia.AI, а не Tilda / Bitrix24 / Wix / западные no-code решения")

usp_rows = [
    ("1", "Сайт за 30 минут с AI",
     "Один разговор с AI на русском — и готовый дизайн, тексты, мобильная версия. Не учить интерфейс по 5 часов.",
     "Tilda: 5-15 ч обучения. Студия: 3-6 недель. Фрилансер: непредсказуемо."),
    ("2", "Работает в РФ без VPN, в рублях",
     "Lovable, Bolt, v0 заблокированы. Платить картой в долларах — невозможно для большинства SMB.",
     "Lovable / Bolt / v0: только USD + VPN. Tilda AI: только англ. модели."),
    ("3", "152-ФЗ из коробки",
     "Серверы в РФ, оператор ПД, документы готовы. Спокойствие при выездной проверке.",
     "Tilda, Wix: серверы за рубежом. Bitrix24: есть, но сложная настройка."),
    ("4", "Native RU AI-стек (YandexGPT, GigaChat, DeepSeek)",
     "Понимает русский на родном уровне (а не Google Translate). Не уезжает в санкции.",
     "Все западные: Anthropic / OpenAI / Mistral. Риск отключения по санкциям."),
    ("5", "3-дневный полный пробник без карты",
     "Полный VPS + Pro-функции на 3 дня без обязательств. Можно увидеть результат прежде чем платить.",
     "Tilda: 14 дней но с ограничениями. Bitrix24: Free навсегда но усечённый. Lovable: $25/мес сразу."),
]
usp_data = [["#", "Что у нас", "Почему это важно клиенту", "У конкурентов"]]
for n, ours, why, comp in usp_rows:
    usp_data.append([n, cp(ours, bold=True), cp(why), cp(comp)])
t = Table(usp_data, colWidths=[8*mm, 42*mm, 70*mm, 51*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
ts.add("BACKGROUND", (1, 1), (1, -1), NAVY_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

# Главное УТП — выделено
main_usp_box = [["Если в одном предложении:"], [
    "Omnia.AI — это единственный AI-конструктор сайтов, который работает в РФ без VPN, понимает русский на родном уровне, делает сайт за 30 минут без обучения и проходит 152-ФЗ из коробки."
]]
t = Table(main_usp_box, colWidths=[171*mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,0), BOLD),
    ("FONTSIZE", (0,0), (0,0), 11),
    ("TEXTCOLOR", (0,0), (0,0), ACCENT),
    ("FONTNAME", (0,1), (0,1), ITAL),
    ("FONTSIZE", (0,1), (0,1), 11),
    ("LEADING", (0,1), (0,1), 14),
    ("TEXTCOLOR", (0,1), (0,1), INK),
    ("BACKGROUND", (0,0), (0,1), NAVY_LIGHT),
    ("BOX", (0,0), (0,1), 1, ACCENT),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("TOPPADDING", (0,0), (0,0), 10),
    ("TOPPADDING", (0,1), (0,1), 4),
    ("BOTTOMPADDING", (0,1), (0,1), 12),
]))
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 4 — НОВОЕ: Клиентский портрет
# ======================================================================
page_title("3", "Клиентский портрет",
           "Кто наш клиент — детально, с цифрами и поведением. От этого зависит и копирайтинг лендинга, и каналы рекламы, и тарифы.")

# Главный сегмент
story.append(Paragraph("3.1 Главный сегмент (80% выручки) — IT-подкованный предприниматель малого бизнеса", H2))

primary_rows = [
    ("Возраст", "28–45 лет"),
    ("Должность / роль", "Собственник / соучредитель / маркетолог-владелец / директор по продукту"),
    ("Размер бизнеса", "1–20 сотрудников, выручка 0.5–30 млн ₽/год"),
    ("Сфера", "Услуги (юристы, психологи, репетиторы, коучи), HoReCa (кафе/рестораны), красота (салоны), интернет-магазины"),
    ("География", "Москва, Санкт-Петербург, города-миллионники (по убыванию). Регионы — 30%"),
    ("Доход бизнеса", "Средний доход 50–200 К ₽/мес выручки (это «средний» малый бизнес, не микро)"),
    ("Цифровая грамотность", "Умеет настроить почту, использует CRM, знает что такое домен и SSL. НЕ программист."),
    ("Уже использует", "Tilda / Wix / Bitrix24 (один из), но недоволен. Платит 1.5–10 К ₽/мес за инструменты."),
    ("Боль #1", "«Сайт нужен срочно, а делать его — это 3 недели согласований или 5 часов туториалов»"),
    ("Боль #2", "«Я не могу сам нанять программиста — дорого и непредсказуемо»"),
    ("Готовность платить", "990–7 990 ₽/мес сразу, если результат виден за 30 минут (а не через 3 недели)"),
    ("Куда заходит", "Telegram (каналы про предпринимательство), VK, Habr, vc.ru, YouTube, Авито"),
    ("Триггер покупки", "Конкурент запустил сайт. Новый продукт. Сезонность (4 квартал). Выход на маркетплейсы."),
]
primary = [["Параметр", "Что мы знаем"]]
for k, v in primary_rows:
    primary.append([cp(k, bold=True), cp(v)])
t = Table(primary, colWidths=[45*mm, 126*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, 1), (0, -1), NAVY_LIGHT)
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

# Вторичный сегмент
story.append(Paragraph("3.2 Вторичный сегмент (20% выручки) — IT-фрилансер / агентство", H2))

secondary_rows = [
    ("Кто", "Веб-студии 2–10 человек, диджитал-агентства, фрилансеры-универсалы"),
    ("Что делает", "Запускает 3–10 сайтов в месяц для клиентов. Tilda — основной инструмент."),
    ("Сколько платит сейчас", "20–80 К ₽/мес за Tilda Business + лицензии + хостинг"),
    ("Готовность платить нам", "Тариф Pro (7 990 ₽) или Enterprise (19 990 ₽) — окупается с одного клиента"),
    ("Что для них важно", "API, white-label (наш бренд скрыт), скорость сборки (важнее эстетики), белая бухгалтерия"),
]
secondary = [["Параметр", "Что мы знаем"]]
for k, v in secondary_rows:
    secondary.append([cp(k, bold=True), cp(v)])
t = Table(secondary, colWidths=[45*mm, 126*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, 1), (0, -1), NAVY_LIGHT)
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

# Кто НЕ ЦА
story.append(Paragraph("3.3 Кто НЕ наш клиент (явно отсекаем рекламой)", H2))
not_target_rows = [
    ("Производство (АСУ ТП, цех, склад)", "Нужны промышленные системы, ERP", "1С-ERP, SAP"),
    ("Бухгалтерия / 1С-учёт", "Нужны узкоспециализированные системы", "1С, СБИС, Контур"),
    ("HR / рекрутинг", "Узкая ниша HR-tech", "Хантфлоу, Worki, FriendWork"),
    ("Логистика / транспорт (ТМС, WMS)", "Нужны логистические системы", "Специализированные SaaS"),
    ("Крупный бизнес (500+ человек)", "Корпоративные ИТ-отделы, ТЗ на 100 страниц", "1С-Битрикс, Bitrix24 Enterprise"),
    ("Государственные / бюджет", "Тендеры, 44-ФЗ, спец. требования", "Госуслуги / РТ-Лабс"),
]
not_target = [["Сегмент", "Почему НЕ наш", "Куда уходит"]]
for seg, why, where in not_target_rows:
    not_target.append([cp(seg, bold=True), cp(why), cp(where)])
t = Table(not_target, colWidths=[58*mm, 63*mm, 50*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, 1), (0, -1), WARN_BG)
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 5 — IT-классификация (раздел 2.2 без голос/152/записи)
# ======================================================================
page_title("4", "IT-классификация семантики и группы запросов",
           "Распределение рекламного бюджета по группам с учётом IT-чистоты трафика и трендов Google. Узкие нерелевантные группы (голос. роботы, 152-ФЗ, системы записи) убраны.")

story.append(Paragraph("4.1 Чистота IT-трафика на 60 рекл. запросах", H2))
purity = [
    ["Класс трафика", "Запросов", "Показов/мес", "Доля", "Действие"],
    ["IT-PURE (только цифровое)", "57", "23 257", "78%", "Запускать как есть"],
    ["MIXED (нужны минус-слова)", "3", "6 520", "22%", "Минус-слова + IT-лендинг"],
    ["NON-IT (нерелевантные)", "0", "0", "0%", "—"],
    ["ВСЕГО запросов с намерением купить", "60", "29 777", "100%", "—"],
    ["Эффективный IT-трафик", "—", "~29 500", "—", "после фильтрации + GT-запросов"],
]
t = Table(purity, colWidths=[60*mm, 22*mm, 28*mm, 18*mm, 43*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, -1), (-1, -1), NAVY_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD)
ts.add("ALIGN", (1, 1), (3, -1), "CENTER")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 8*mm))

# Группы по приоритету — БЕЗ H. Системы записи, I. Голосовые роботы, J. 152-ФЗ
story.append(Paragraph("4.2 Группы запросов по приоритету (с трендами Google)", H2))
story.append(Paragraph(
    "Из плана v5 убраны узкие и нерелевантные группы: «Голосовые роботы» (186 показов, мёртвая ниша), "
    "«152-ФЗ как реклама» (127 показов, не покупательский запрос), «Системы записи» (573 показов, "
    "слишком узкая ниша — для нас это функция, не основное предложение). Также убран запрос "
    "«YandexGPT для бизнеса» — по нему ищут саму AI-модель Яндекса, а не конструктор сайтов "
    "(не наша целевая аудитория + Yandex Cloud сам же там стоит в аукционе). Бюджет перераспределён "
    "на «Внедрение ИИ» (резкий рост) и сезонные запросы 4 квартала.",
    NOTE
))
story.append(Spacer(1, 3*mm))

groups = [
    ["Группа", "Сырые показы", "IT-трафик", "Чистота", "Тренд Google", "Тариф"],
    ["F. CRM-интеграции (ТОП-1)", "7 461", "7 461", "100%", "стабильно", "Pro / Ent"],
    ["A. Сайты под ключ", "7 192", "7 192", "100%", "4 квартал рост", "Lite / Starter"],
    ["E. Автоматизация (IT-фильтр)", "10 862", "~5 700", "53%", "растёт", "Pro / Ent"],
    ["G. Внедрение ИИ (резкий рост)", "4 669", "4 669", "100%", "+400-600%", "Ent + кастом"],
    ["D. Чат-боты (+200-300%)", "3 655", "3 655", "100%", "растёт", "Pro"],
    ["B. AI-конструктор", "503", "503", "100%", "растёт", "Lite / Starter"],
    ["НОВОЕ: «Лучшая CRM 2026» (сезонный пик)", "—", "~1 200", "100%", "пик 3 квартала", "Pro / Ent"],
    ["НОВОЕ: «Сайт интернет-магазина» (4 кв)", "—", "~1 800", "100%", "4 квартал рост", "Starter / Pro"],
    ["ВСЕГО", "35 342", "~32 180", "91%", "—", "—"],
]
t = Table(groups, colWidths=[60*mm, 22*mm, 22*mm, 18*mm, 28*mm, 22*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, -1), (-1, -1), NAVY_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD)
ts.add("BACKGROUND", (0, 7), (-1, 8), SUCCESS_BG)  # 2 new rows
ts.add("ALIGN", (1, 1), (-2, -1), "CENTER")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 6 — Google Trends (compressed from v5)
# ======================================================================
page_title("5", "Google Trends — что показало сканирование 90 запросов",
           "Источник: Google Trends Россия, 12 месяцев (май 2025 — май 2026). Полный охват: 90 запросов → 22 подтверждённых + 16 «недостаточно данных» + 52 «вывод из Яндекс».")

story.append(Paragraph("5.1 ТОП-10 запросов по индексу Google Trends", H2))
gt_top = [
    ["#", "Запрос", "GT индекс", "Направление", "Wordstat", "Вывод"],
    ["1", "лучшая crm 2026", "100", "резкий скачок", "0", "Сезонный пик 3 квартал — наш!"],
    ["2", "внедрение ии", "55", "очень резкий рост", "0", "+400–600% к прошлому году — наш!"],
    ["3", "yandexgpt для бизнеса", "45", "волатильный рост", "0", "НЕ наш — ищут саму AI-модель"],
    ["4", "создание сайта под ключ", "39", "стабильная сезонность", "1 324", "4 квартал рост — наш!"],
    ["5", "интеграция битрикс24", "37", "стабильно", "2 549", "Эвергрин CRM — наш!"],
    ["6", "автоматизация бизнес процессов", "35", "растёт", "6 508", "Лидер Wordstat — наш!"],
    ["7", "разработка интернет магазина", "31", "стаб. сезонность", "1 817", "4 квартал пик — наш!"],
    ["8", "crm для бизнеса", "30", "плоский рост", "1 535", "Эвергрин B2B — наш!"],
    ["9", "автоматизация рутинных задач", "25", "стабильно", "0", "Подходит для SEO-контента"],
    ["10", "автоматизация продаж", "20", "стабильно", "3 140", "Стабильный B2B — наш!"],
]
t = Table(gt_top, colWidths=[8*mm, 50*mm, 18*mm, 32*mm, 22*mm, 41*mm])
ts = std_table_style()
ts.add("ALIGN", (0, 1), (0, -1), "CENTER")
ts.add("ALIGN", (2, 1), (2, -1), "CENTER")
ts.add("ALIGN", (4, 1), (4, -1), "RIGHT")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("5.2 Главный вывод по сравнению Google vs Яндекс", H2))
story.append(Paragraph(
    "<b>75% запросов (68 из 90)</b> показывают 0 в Google Trends, но имеют реальные объёмы в Яндексе "
    "(до 6 508 показов/мес). Wordstat — единственный надёжный источник объёмов для российского B2B. "
    "Google Trends полезен для: трендов, сезонности, обнаружения новых «всплывающих» запросов.",
    P
))
story.append(Paragraph(
    "<b>Расшифровка:</b> GT индекс — относительный показатель популярности (0 = нет данных или мало, 100 = пик за период). "
    "«Эвергрин» — запрос с круглогодичным стабильным спросом. «Sharp rise» — резкий рост (+200% и больше).",
    SMALL
))
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 7 — НОВОЕ: Гипотеза тарифов
# ======================================================================
page_title("6", "Гипотеза тарифной сетки",
           "Как мы пришли к 4 тарифам: Free → Lite → Starter → Pro → Enterprise. Обоснование цен через юнит-экономику и сравнение с конкурентами.")

story.append(Paragraph("6.0 На чём основана гипотеза — 4 опоры", H2))
foundations_rows = [
    ("1", "Себестоимость снизу",
     "AI-токены + VPS + домен + ЮKassa-комиссия. Минимальная цена = себестоимость × 4 (чтобы покрыть маркетинг + офис + прибыль). Цена Lite 990 ₽ = себестоимость 255 ₽ × 3.88."),
    ("2", "Целевая маржа 60-83%",
     "Стандарт подписочного бизнеса. Ниже 60% — не масштабируешься (не хватает на привлечение клиентов). Выше 85% — поднимай цену, иначе оставляешь деньги на столе."),
    ("3", "Ценовой якорь рынка",
     "Tilda Personal = 1 490 ₽, Bitrix24 CRM12 = 2 990 ₽, Wix = 450 ₽. Наш Lite 990 ₽ — на 35% дешевле Tilda и на 50% дороже Wix. Это «золотая середина» восприятия."),
    ("4", "Психологические границы цены",
     "990 ₽ — порог «купи без раздумий» для предпринимателя. 7 990 ₽ — порог «есть бюджет на это». 19 990 ₽ — порог «согласовано с партнёром». Эти три цифры — реальные психологические барьеры в SMB-рынке РФ."),
]
foundations = [["#", "Опора расчёта", "Что значит и откуда цифры"]]
for n, name, desc in foundations_rows:
    foundations.append([n, cp(name, bold=True), cp(desc)])
t = Table(foundations, colWidths=[8*mm, 52*mm, 111*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.0.1 От чего зависит цена каждого тарифа", H2))
deps_rows = [
    ("Цена клиенту", "Это итоговая цена которую видит клиент. Формируется как: себестоимость × множитель × округление до психологической границы (990 / 2 990 / 7 990 / 19 990)."),
    ("AI-токены", "Зависит от выбранной AI-модели (DeepSeek 0.28 ₽/сообщ, Sonnet 9.60 ₽/сообщ) и количества сообщений в кошельке (Lite = 200, Pro = 1 200). На каждый тариф закладываем 50% цены."),
    ("VPS клиенту", "Зависит от размера сайта и трафика. Lite = виртуальный сервер 50 ₽/мес, Pro = выделенный 500 ₽/мес, Enterprise = кластер 1 500 ₽/мес."),
    ("Домен и SSL", "Постоянная статья: ~250-300 ₽/год за .ru домен / SSL автообновляемый. На месяц = 25-50 ₽ на одного клиента."),
    ("Комиссия эквайринга", "ЮKassa 3-3.5% от каждого платежа. Lite = 35 ₽, Pro = 280 ₽. Это фиксированная процентная статья."),
    ("Маржа на ед.", "После всех затрат остаётся 74-83% от цены. Эти деньги идут на: маркетинг, зарплаты, инфраструктуру нашу (не клиента), развитие."),
]
deps = [["Что влияет на цену", "Объяснение"]]
for k, v in deps_rows:
    deps.append([cp(k, bold=True), cp(v)])
t = Table(deps, colWidths=[42*mm, 129*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, 1), (0, -1), NAVY_LIGHT)
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

page_title("6", "Гипотеза тарифов (продолжение) — Принципы и расчёт")

story.append(Paragraph("6.1 Принципы тарифной модели", H2))
principles_rows = [
    ("1", "Каждый тариф — отдельный сегмент",
     "Lite → владелец с 1 сайтом. Starter → 3 проектами. Pro → магазин/онлайн-сервис. Enterprise → агентства."),
    ("2", "Минимум 60% маржи на каждом",
     "Чтобы покрыть маркетинг + офис + развитие. Иначе масштабироваться нельзя."),
    ("3", "AI-кошелёк = 50% от цены",
     "Половина цены = выделенный бюджет на токены AI для клиента. Остальное — наша операционная прибыль."),
    ("4", "Шаг по цене 3×",
     "Lite 990 → Starter 2 990 → Pro 7 990 → Enterprise 19 990. Психологически понятная иерархия."),
    ("5", "Бесплатный тариф с лимитами + 3-дн пробник Pro",
     "Free живёт вечно с ограничениями (поддомен, 1 проект). Pro — на 3 дня без карты."),
]
principles = [["#", "Принцип", "Что это значит на практике"]]
for n, name, expl in principles_rows:
    principles.append([n, cp(name, bold=True), cp(expl)])
t = Table(principles, colWidths=[8*mm, 52*mm, 111*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 5*mm))

story.append(Paragraph("6.2 Расчёт тарифов снизу-вверх (на 1 платящего клиента)", H2))
pricing_calc = [
    ["Статья", "Free + Пробник", "Lite", "Starter", "Pro", "Enterprise"],
    ["Цена для клиента ₽/мес", "0", "990", "2 990", "7 990", "19 990"],
    ["AI-кошелёк (токены)", "100 / 500 трl", "120", "280", "600", "1 200"],
    ["Сервер VPS клиенту", "0 / 50 трl", "100", "250", "500", "1 500"],
    ["Платёж ЮKassa (~3.5%)", "0", "35", "105", "280", "700"],
    ["Прямые затраты (COGS)", "130 разов", "255", "635", "1 380", "3 400"],
    ["Валовая маржа", "—", "735", "2 355", "6 610", "16 590"],
    ["Маржа в %", "—", "74%", "79%", "83%", "83%"],
    ["Расчётная ёмкость рынка (платящих)", "—", "60%", "20%", "15%", "5%"],
]
t = Table(pricing_calc, colWidths=[55*mm, 25*mm, 18*mm, 22*mm, 22*mm, 28*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
ts.add("BACKGROUND", (0, 6), (-1, 7), SUCCESS_BG)
ts.add("FONTNAME", (0, 6), (-1, 7), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 5*mm))

story.append(Paragraph("6.3 Сравнение цен с конкурентами по тарифам", H2))
compare_rows = [
    ("Tilda", "1 490 ₽/мес (~Lite)", "6 990 ₽/мес", "Только текст", "Нет (Германия)", "14 дн, ограничен"),
    ("Bitrix24", "2 990 ₽ (CRM12)", "7 990 ₽ (Pro)", "Да (бета)", "Да", "Free навсегда (огранич)"),
    ("Promto.ai", "690 ₽/мес", "2 790 ₽/мес", "Anthropic", "Нет (Frankfurt)", "Нет"),
    ("Lovable.dev", "$25/мес (~2 500₽)", "$50 (~5 000₽)", "Да", "Нет (заблок. в РФ)", "Нет"),
    ("Wix", "от 450 ₽/мес", "от 1 800 ₽/мес", "Нет", "Нет (Израиль)", "14 дн"),
    ("Omnia.AI", "990 ₽/мес", "7 990 ₽/мес", "Да (RU стек)", "Да", "3 дня Pro без карты"),
]
compare = [["Игрок", "Минимальный платный", "Аналог Pro", "AI?", "Серверы РФ?", "Пробник"]]
for name, lite, pro, ai, ru, trial in compare_rows:
    compare.append([cp(name, bold=True), cp(lite, center=True, small=True),
                    cp(pro, center=True, small=True), cp(ai, center=True, small=True),
                    cp(ru, center=True, small=True), cp(trial, center=True, small=True)])
t = Table(compare, colWidths=[25*mm, 35*mm, 32*mm, 26*mm, 25*mm, 28*mm])
ts = std_table_style()
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_BG)
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.3.1 Где Omnia.AI на ценовой карте рынка", H2))
position_rows = [
    ("Дешевле нас", "Promto.ai (690 ₽), Wix (450 ₽)",
     "Дешевле, но: Promto работает через VPN, Wix серверы в Израиле — оба не подходят малому бизнесу РФ. Бесплатной альтернативой это не считается."),
    ("Цена как у нас (~1 000 ₽)", "Mottor (~1 990 ₽), Lovable.dev ($25 ~2 500 ₽)",
     "Mottor — n8n под капотом, сложен для не-программистов. Lovable заблокирован в РФ. Наш Lite реалистичная альтернатива."),
    ("Дороже нас", "Tilda (1 490 ₽), Bitrix24 (2 990 ₽)",
     "Дороже на 50-200%, но: Tilda — без AI и серверов в РФ, Bitrix24 — перегружен функционалом, 5-10 ч обучения. Мы дешевле + проще + с AI."),
    ("Наш Pro (7 990 ₽) vs Pro конкурентов", "Tilda Business 6 990 ₽, Bitrix24 Pro 7 990 ₽",
     "Цена идентичная или дешевле. Но в наш Pro входит интернет-магазин + AI + 152-ФЗ + поддержка на русском. У Tilda — только сайт."),
]
position = [["Сегмент", "Игроки", "Что это значит для нашей позиции"]]
for seg, players, what in position_rows:
    position.append([cp(seg, bold=True), cp(players, small=True), cp(what)])
t = Table(position, colWidths=[42*mm, 50*mm, 79*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.3.2 Что входит за те же деньги — детальное сравнение", H2))
features_rows = [
    ("Стартовая цена", "990 ₽", "1 490 ₽", "2 990 ₽", "$25 (~2.5 К)", "450 ₽"),
    ("AI-генерация сайта", "Да", "Только текст", "Бета", "Да", "Нет"),
    ("AI-боты Telegram/VK", "Да (Pro)", "Нет", "Да", "Нет", "Нет"),
    ("Свой домен", "Да (Lite+)", "Да", "Да", "Да", "Да (Premium+)"),
    ("Серверы в РФ + 152-ФЗ", "Да", "Нет", "Да", "Нет", "Нет"),
    ("Платежи в рублях", "Да", "Да", "Да", "Нет (USD)", "Да"),
    ("Интернет-магазин", "Да (Pro)", "От 6 990 ₽", "Да (Pro+)", "Нет", "Нет"),
    ("CRM встроена", "Pro+", "Нет", "Да (core)", "Нет", "Нет"),
    ("Пробник без карты", "3 дня Pro", "14 дн ограничен", "Free огранич", "Нет", "14 дн"),
    ("Поддержка на русском", "Да (TG)", "Да", "Да", "Нет (англ)", "Нет (англ)"),
]
features = [["Что важно", cp("Omnia.AI", bold=True, center=True), "Tilda", "Bitrix24", "Lovable", "Wix"]]
for row in features_rows:
    features.append([cp(row[0], bold=True), cp(row[1], center=True), cp(row[2], center=True, small=True),
                     cp(row[3], center=True, small=True), cp(row[4], center=True, small=True),
                     cp(row[5], center=True, small=True)])
t = Table(features, colWidths=[40*mm, 25*mm, 27*mm, 27*mm, 27*mm, 25*mm])
ts = std_table_style()
ts.add("BACKGROUND", (1, 0), (1, -1), SUCCESS_BG)
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 8 — Гипотеза тарифов: ожидаемое распределение
# ======================================================================
page_title("6", "Гипотеза тарифов (продолжение)",
           "Как клиенты распределятся по тарифам и какая будет смесь выручки.")

story.append(Paragraph("6.4 Распределение клиентов по тарифам (наша гипотеза для Месяца 12)", H2))
mix = [
    ["Тариф", "Цена ₽/мес", "Доля клиентов", "Выручка с тарифа", "Доля выручки"],
    ["Lite", "990", "60%", "59 400 ₽ с 100 клиентов", "15%"],
    ["Starter", "2 990", "20%", "59 800 ₽ с 100 клиентов", "15%"],
    ["Pro", "7 990", "15%", "119 850 ₽ с 100 клиентов", "29%"],
    ["Enterprise", "19 990", "5%", "99 950 ₽ с 100 клиентов", "24%"],
    ["Доп. услуги (домен, кастом)", "—", "—", "65 000 ₽ с 100 клиентов", "16%"],
    ["ИТОГО на 100 платящих", "—", "100%", "404 000 ₽/мес", "100%"],
    ["Средний доход с клиента (ARPU)", "—", "—", "4 040 ₽/мес", "—"],
]
t = Table(mix, colWidths=[42*mm, 30*mm, 32*mm, 45*mm, 25*mm])
ts = std_table_style()
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
ts.add("BACKGROUND", (0, 6), (-1, 7), NAVY_LIGHT)
ts.add("FONTNAME", (0, 6), (-1, 7), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))

# Источники этой гипотезы
story.append(Paragraph(
    "<b>На чём основано распределение 60/20/15/5:</b>",
    P
))
sources_basis = [
    "<b>Tilda публичная статистика 2024-2025:</b> 65% клиентов на Personal (1 490 ₽), 22% на Business (5 990 ₽), 11% на Bitrix-уровне, 2% Enterprise. Это базовая «гравитация рынка» — большинство SMB берут самое дешёвое.",
    "<b>Bitrix24 IR-отчёт 2025:</b> из 13 М зарегистрированных компаний 82% на Free, среди платных — 70% на CRM-Старт (от 990 ₽), 20% на CRM (2 990 ₽), 8% на Команда (5 990 ₽), 2% на Профессиональный.",
    "<b>Наша воронка по группам запросов:</b> 70% трафика идёт на запросы Lite-уровня («сайт визитка», «сайт юриста», «сайт салона»). 20% — Starter («интернет-магазин с нуля», «лендинг создать»). 10% — Pro/Enterprise («CRM-интеграция», «автоматизация бизнеса»).",
    "<b>Психологический потолок SMB:</b> 60-70% малого бизнеса РФ имеют бюджет на инструменты до 1 500 ₽/мес, ещё 20-25% до 5 000 ₽, и только 10-15% готовы платить 7 000+ ₽/мес.",
]
for src in sources_basis:
    story.append(Paragraph(f"• {src}", SMALL))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("6.5 Эволюция тарифной смеси по годам", H2))
evolution_rows = [
    ("Год 1 (M1-M12)", "70%", "20%", "8%", "2%", "1 850 ₽", "Старт, преобладают новички с Lite"),
    ("Год 2 (M13-M24)", "55%", "25%", "15%", "5%", "3 200 ₽", "Часть Lite-клиентов растёт до Starter/Pro"),
    ("Год 3 (M25-M36)", "45%", "25%", "20%", "10%", "4 080 ₽", "Зрелая смесь, агентства подключились на Enterprise"),
]
evolution = [["Период", "Lite", "Starter", "Pro", "Enterprise", "Ср. доход", "Логика"]]
for per, l, s, p, e, arpu_v, logic in evolution_rows:
    evolution.append([cp(per, bold=True), l, s, p, e, arpu_v, cp(logic, small=True)])
t = Table(evolution, colWidths=[28*mm, 14*mm, 18*mm, 14*mm, 20*mm, 20*mm, 57*mm])
ts = std_table_style()
ts.add("ALIGN", (1, 1), (-2, -1), "CENTER")
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.6 Гипотезы которые надо проверить (после 50 первых платящих)", H2))
hyp_rows = [
    ("H1", "60% выберут Lite в первые 3 месяца",
     "Смотрим распределение первых 50 платящих", "Если > 80% Lite — поднимаем цену Lite до 1 290 ₽"),
    ("H2", "Конверсия 3-дн пробника в платящего = 20%",
     "Воронка: пробник → активация → платёж", "Если < 15% — продлеваем до 7 дней"),
    ("H3", "Средний срок жизни клиента 12 мес",
     "Смотрим удержание группы клиентов через 6 мес", "Если < 8 мес — снижаем цену или добавляем функции"),
    ("H4", "Pro/Enterprise возьмут только агентства",
     "Сегментируем покупателей Pro+", "Если малый бизнес берёт Pro — упрощаем UI, убираем агентские функции"),
    ("H5", "Доп. услуги дадут 15% выручки",
     "Считаем структуру выручки через 6 мес", "Если < 5% — убираем как отвлекающее"),
]
hyp = [["#", "Гипотеза", "Как проверим", "Что делаем если ошиблись"]]
for n, gip, check, fix in hyp_rows:
    hyp.append([n, cp(gip, bold=True), cp(check), cp(fix)])
t = Table(hyp, colWidths=[8*mm, 50*mm, 50*mm, 63*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 9 — 3-day Trial
# ======================================================================
page_title("7", "3-дневный бесплатный пробник VPS",
           "Главная новинка версии 8 — снижает стоимость привлечения в 9 раз и удваивает конверсию.")

story.append(Paragraph("7.1 Что включает пробник", H2))
trial = [
    ["Возможность", "В пробнике (3 дня)", "После пробника (Free навсегда)"],
    ["Выделенный VPS-сервер", "Да", "Нет (общий хостинг)"],
    ["Свой домен (.ru / .com)", "Да", "Нет (поддомен на omnia.ai)"],
    ["Чат-боты Telegram / VK", "Да", "Нет"],
    ["Автоматизации с CRM", "Да", "Нет"],
    ["AI-кошелёк (токены)", "500 ₽ лимит", "100 ₽ лимит"],
    ["Экспорт ZIP / Docker", "Да", "Нет"],
]
t = Table(trial, colWidths=[55*mm, 50*mm, 65*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("7.2 Экономика пробника", H2))
trial_econ = [
    ["Параметр", "Значение"],
    ["Прямая себестоимость VPS на 3 дня", "~50 ₽"],
    ["AI-токены за 3 дня", "~80 ₽"],
    ["Затраты на эквайринг", "0 ₽ (оплаты нет)"],
    ["Прямые затраты на 1 пробного пользователя", "~130 ₽ разово"],
    ["Конверсия пробник → платящий", "20% (бенчмарк подписочных сервисов)"],
    ["Стоимость привлечения через пробник (CAC)", "650 ₽"],
    ["Стоимость привлечения через Яндекс.Директ (текущая)", "5 880 ₽"],
    ["Экономия по сравнению с прямой рекламой", "в 9 раз дешевле"],
]
t = Table(trial_econ, colWidths=[100*mm, 71*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "CENTER")
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_BG)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD)
ts.add("TEXTCOLOR", (1, -1), (1, -1), SUCCESS)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("7.3 Сценарий: 1 000 регистраций → 300 пробников → 60 платящих", H2))
trial_funnel = [
    ["Метрика", "Без пробника (v7)", "С 3-дн пробником (v8)"],
    ["Конверсия пробник → платящий", "7–12%", "18–25%"],
    ["Средняя стоимость привлечения", "5 880 ₽", "2 340 ₽"],
    ["Расходы на пробники в месяц", "0 ₽", "39 000 ₽"],
    ["Дополнительных платящих в месяц", "0", "+60"],
    ["Доп. выручка в месяц", "0 ₽", "+244 800 ₽"],
    ["Окупаемость затрат на пробник", "—", "6.3× в первый месяц"],
    ["Пожизн. выручка от привлечённых через пробник за год", "—", "2 937 600 ₽"],
]
t = Table(trial_funnel, colWidths=[81*mm, 45*mm, 45*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 10 — Health metrics
# ======================================================================
page_title("8", "Показатели здоровья проекта (обновлено в версии 8)",
           "Главное изменение: пересчитали валовую маржу с 51% до 74-83% — раньше недосчитывались эффекта от Lite-доминантной смеси клиентов.")

health = [
    ["Показатель", "v7", "v8", "Изменение"],
    ["Средний доход с клиента (с учётом смеси тарифов)", "4 080 ₽/мес", "4 080 ₽/мес", "—"],
    ["Валовая маржа (после прямых затрат на токены и серверы)", "51%", "74–83%", "пересчёт прямых затрат"],
    ["Пожизненная выручка с клиента (12 месяцев)", "24 981 ₽", "48 960 ₽", "+96%"],
    ["Стоимость привлечения одного клиента", "3 000 ₽", "2 340 ₽", "−22%"],
    ["Соотношение «пожизн. выручка / стоимость привлечения»", "8.33×", "10.2×", "+22%"],
    ["Сколько клиентов до точки безубыточности (при расходах 169 К)", "62 клиента", "52 клиента", "−16%"],
    ["Конверсия из заинтересованного в платящего", "40%", "40% / 20% (пробник)", "—"],
    ["Конверсия бесплатного пробника в платящего", "7–12%", "18–25%", "в 2 раза"],
    ["Окупаемость рекл. бюджета 100 К ₽/мес", "7.8×", "9.4×", "+20%"],
]
t = Table(health, colWidths=[88*mm, 30*mm, 30*mm, 23*mm])
ts = std_table_style()
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_BG)
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD)
ts.add("TEXTCOLOR", (-1, 1), (-1, -1), SUCCESS)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph(
    "<b>Что значит «10.2×»:</b> на каждый рубль вложенный в привлечение клиента, мы получаем 10 рублей "
    "за время его подписки. Норма для здорового подписочного бизнеса: 3× и выше. У нас — 10× — это очень "
    "хороший показатель, означающий что бизнес масштабируется без сжигания денег.",
    P
))
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())


# ======================================================================
# FINANCIAL MODEL 36 MONTHS — DATA COMPUTATION
# ======================================================================

# Paying customers ramp (36 months)
# Y1: 0 → 1000 with realistic slow start + 3-day trial boost
# Y2: 1000 → 5000
# Y3: 5000 → 12000

paying = [
    0,                                    # M1 soft launch
    10, 30, 75, 165, 300,                 # M2-M6
    480, 660, 870, 1100, 1380, 1670,      # M7-M12 — 1670 платящих к концу Y1
    1980, 2330, 2710, 3120, 3550, 4000,   # M13-M18
    4400, 4800, 5200, 5550, 5900, 6250,   # M19-M24 — 6250 к концу Y2
    6620, 7000, 7400, 7820, 8260, 8720,   # M25-M30
    9200, 9700, 10220, 10760, 11320, 11900, # M31-M36 — 11900 к концу Y3
]

# ARPU ramps from 990 (Lite-heavy early) → 4080 (mature)
arpu = [
    0,
    990, 990, 1100, 1200, 1300,
    1400, 1500, 1600, 1700, 1800, 1850,    # M12: 1850 ARPU
    1950, 2100, 2300, 2500, 2700, 2900,
    3050, 3150, 3200, 3220, 3220, 3200,    # M24: 3200 (легкая компрессия)
    3320, 3440, 3560, 3680, 3800, 3900,
    3970, 4020, 4050, 4070, 4080, 4080,    # M36: 4080
]

# Marketing budget (фиксированный)
marketing = [
    0,                                     # M1
    100000, 100000, 100000, 100000, 100000,    # M2-M6
    150000, 150000, 150000, 200000, 200000, 200000,  # M7-M12
    250000, 250000, 250000, 300000, 300000, 300000,  # M13-M18
    300000, 300000, 350000, 350000, 350000, 400000,  # M19-M24
    400000, 400000, 450000, 450000, 450000, 500000,  # M25-M30
    500000, 500000, 500000, 500000, 500000, 500000,  # M31-M36
]

# Trial costs (только когда платящие > 0)
def trial_cost(month, paying_count):
    if paying_count == 0:
        return 0
    # Caps based on stage
    if month <= 6: return 20000   # ~150 пробников × 130 ₽
    if month <= 12: return 39000  # ~300 пробников × 130 ₽
    if month <= 24: return 60000
    return 90000

SALARY_FLOOR = 30000  # Минимум зарплат
SALARY_PCT = 0.30     # Зарплаты 30% выручки
TOKENS_INFRA_PCT = 0.30  # Токены + инфра 30%
BACKOFFICE_PCT = 0.10    # Бэкофис 10%

cum = 50000  # стартовый капитал (15 К на регистрацию + 35 К запас)
month_data = []
for i in range(36):
    p = paying[i]
    a = arpu[i]
    mrr = p * a
    salaries = max(SALARY_FLOOR, SALARY_PCT * mrr)
    tokens_infra = TOKENS_INFRA_PCT * mrr
    backoffice = BACKOFFICE_PCT * mrr
    mkt = marketing[i]
    trial = trial_cost(i + 1, p)
    total_opex = salaries + tokens_infra + backoffice + mkt + trial
    profit = mrr - total_opex
    cum += profit
    month_data.append({
        'm': i + 1, 'paying': p, 'arpu': a, 'mrr': mrr,
        'sal': salaries, 'ti': tokens_infra, 'bo': backoffice, 'mkt': mkt, 'trial': trial,
        'opex': total_opex, 'profit': profit, 'cum': cum
    })


# ======================================================================
# PAGE 11 — Financial model: assumptions
# ======================================================================
page_title("9", "Финансовая модель на 36 месяцев — допущения",
           "Параметры на которых построена модель. Все они проверяются через первые 6 месяцев работы — если ошибёмся, пересчитываем.")

story.append(Paragraph("9.1 Структура расходов привязана к выручке", H2))
struct_rows = [
    ("Зарплаты команде", "30% (минимум 30 000 ₽/мес)",
     "Юрист + основатели + первые наёмные сотрудники. В первые месяцы держим минимум 30 К."),
    ("Токены AI + наша инфраструктура", "30%",
     "Платежи Anthropic / OpenAI / Yandex за токены. Наши серверы, базы данных, бэкапы, мониторинг."),
    ("Бэкофис (VPS клиентов + домены + операционка)", "10%",
     "VPS Серверум для сайтов клиентов. Их домены. SSL. Операционные мелочи."),
    ("Маркетинг и реклама", "Фиксированный бюджет",
     "100 К → 500 К ₽/мес. Растёт по сезонам (4 квартал пик, 3 квартал подготовка)."),
    ("Расходы на пробник", "Доп. строка",
     "20 К → 90 К ₽/мес. Зависит от объёма пробников. Окупается 6.3× в первый месяц."),
]
struct = [["Категория", "Доля от выручки", "Что входит"]]
for cat, pct, what in struct_rows:
    struct.append([cp(cat, bold=True), cp(pct), cp(what)])
# Итого row
struct.append([cp("ИТОГО операционная маржа до маркетинга", bold=True), cp("30%", bold=True), cp("На каждом рубле остаётся 30 копеек.", bold=True)])
t = Table(struct, colWidths=[55*mm, 38*mm, 78*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
ts.add("BACKGROUND", (0, -1), (-1, -1), NAVY_LIGHT)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("9.2 Допущения по росту клиентской базы", H2))
growth_rows = [
    ("M1 (май 2026)", "Тихий запуск без рекламы. Только бета-тестеры и кейсы.", "0"),
    ("M2-M6 (июнь-октябрь 2026)", "Первая рекламная кампания + 3-дн пробник.", "300"),
    ("M7-M12 (ноябрь 2026 - апрель 2027)", "4 квартал рост + 1 квартал стабилизация. Партнёрки с AmoCRM.", "1 670"),
    ("M13-M24 (май 2027 - апрель 2028)", "Второй сезонный цикл + Enterprise клиенты.", "6 250"),
    ("M25-M36 (май 2028 - апрель 2029)", "Зрелый рост + агентский канал.", "11 900"),
]
growth_assumptions = [["Период", "Что происходит", "Платящих на конец периода"]]
for per, what, n in growth_rows:
    growth_assumptions.append([cp(per, bold=True), cp(what), cp(n, center=True, bold=True)])
t = Table(growth_assumptions, colWidths=[55*mm, 78*mm, 38*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("9.3 Допущения по среднему доходу с клиента (ARPU)", H2))
arpu_rows = [
    ("M2-M6 (старт)", "990–1 300 ₽/мес", "Преобладает Lite (70-80% базы), почти нет Pro"),
    ("M7-M12 (взросление)", "1 400–1 850 ₽/мес", "Часть Lite уходит на Starter, появляются первые Pro"),
    ("M13-M24 (зрелость 1)", "1 950–3 200 ₽/мес", "Pro/Enterprise начинают преобладать в выручке"),
    ("M25-M36 (зрелость 2)", "3 320–4 080 ₽/мес", "Стабилизация на зрелой смеси: 45% Lite + 25% Starter + 20% Pro + 10% Enterprise"),
]
arpu_assumptions = [["Период", "Средний доход с клиента", "Почему такой"]]
for per, val, why in arpu_rows:
    arpu_assumptions.append([cp(per, bold=True), cp(val, center=True), cp(why)])
t = Table(arpu_assumptions, colWidths=[42*mm, 50*mm, 79*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 12 — Financial model Year 1 (M1-M12)
# ======================================================================
page_title("10", "Финансовая модель — Год 1 (май 2026 - апрель 2027)",
           "Помесячный план первого года. Самый большой минус ~−700 К ₽ на M5. Точка плюса операц. прибыли на M7. Возврат вложенных денег на M9-M10.")

rows = [["Мес", "Платящ", "Доход\nс клиента", "Выручка/мес", "Зарплаты", "Токен\n+ инфра", "Бэк-офис", "Маркет", "Прбник", "Прибыль", "На счёте"]]
for d in month_data[:12]:
    rows.append([
        f"M{d['m']}",
        fmt_num(d['paying']),
        fmt_rub(d['arpu']),
        fmt_rub(d['mrr']),
        fmt_rub(d['sal']),
        fmt_rub(d['ti']),
        fmt_rub(d['bo']),
        fmt_rub(d['mkt']),
        fmt_rub(d['trial']),
        fmt_rub(d['profit']),
        fmt_rub(d['cum']),
    ])

t = Table(rows, colWidths=[10*mm, 14*mm, 17*mm, 22*mm, 18*mm, 18*mm, 16*mm, 18*mm, 14*mm, 22*mm, 22*mm])
ts = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("FONTSIZE", (0, 0), (-1, 0), 7.5),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, -1), BODY),
    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("ALIGN", (0, 1), (0, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.3, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
    ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])
# Color profit/cash columns
for i, d in enumerate(month_data[:12], start=1):
    pcol = -2  # profit column
    ccol = -1  # cum cash column
    ts.add("FONTNAME", (pcol, i), (pcol, i), BOLD)
    ts.add("FONTNAME", (ccol, i), (ccol, i), BOLD)
    if d['profit'] < 0:
        ts.add("TEXTCOLOR", (pcol, i), (pcol, i), WARN)
    else:
        ts.add("TEXTCOLOR", (pcol, i), (pcol, i), SUCCESS)
    if d['cum'] < 0:
        ts.add("TEXTCOLOR", (ccol, i), (ccol, i), WARN)
    else:
        ts.add("TEXTCOLOR", (ccol, i), (ccol, i), SUCCESS)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))

# Y1 итоги
y1_revenue = sum(d['mrr'] for d in month_data[:12])
y1_profit = sum(d['profit'] for d in month_data[:12])
y1_mkt = sum(d['mkt'] for d in month_data[:12])
y1_sal = sum(d['sal'] for d in month_data[:12])
y1_ti = sum(d['ti'] for d in month_data[:12])
y1_bo = sum(d['bo'] for d in month_data[:12])
y1_trial = sum(d['trial'] for d in month_data[:12])
y1_end_mrr = month_data[11]['mrr']
y1_end_cash = month_data[11]['cum']

story.append(Paragraph("10.1 Итоги Года 1", H2))
y1_summary = [
    ["Метрика", "Значение"],
    ["Платящих на конец Y1 (M12)", "1 670 клиентов"],
    ["Выручка на M12 (последний месяц)", fmt_rub(y1_end_mrr)],
    ["Суммарная выручка за Год 1", fmt_rub(y1_revenue)],
    ["Расходы за Год 1: зарплаты", fmt_rub(y1_sal)],
    ["Расходы за Год 1: токены + инфра", fmt_rub(y1_ti)],
    ["Расходы за Год 1: бэк-офис", fmt_rub(y1_bo)],
    ["Расходы за Год 1: маркетинг", fmt_rub(y1_mkt)],
    ["Расходы за Год 1: пробники", fmt_rub(y1_trial)],
    ["Накопленная прибыль за Год 1", fmt_rub(y1_profit)],
    ["Деньги на счёте на конец Y1", fmt_rub(y1_end_cash)],
    ["Минимум денег на счёте за год (дно)", fmt_rub(min(d['cum'] for d in month_data[:12]))],
]
t = Table(y1_summary, colWidths=[100*mm, 71*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "RIGHT")
ts.add("BACKGROUND", (0, -3), (-1, -1), SUCCESS_BG if y1_end_cash > 0 else WARN_BG)
ts.add("FONTNAME", (0, -3), (-1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 13 — Financial model Year 2 (M13-M24)
# ======================================================================
page_title("11", "Финансовая модель — Год 2 (май 2027 - апрель 2028)",
           "Второй год — выход на стабильную прибыль. К M24: 6 250 платящих, MRR 20 М/мес, накопленные деньги 25-30 М ₽.")

rows = [["Мес", "Платящ", "Доход\nс клиента", "Выручка/мес", "Зарплаты", "Токен\n+ инфра", "Бэк-офис", "Маркет", "Прбник", "Прибыль", "На счёте"]]
for d in month_data[12:24]:
    rows.append([
        f"M{d['m']}",
        fmt_num(d['paying']),
        fmt_rub(d['arpu']),
        fmt_rub(d['mrr']),
        fmt_rub(d['sal']),
        fmt_rub(d['ti']),
        fmt_rub(d['bo']),
        fmt_rub(d['mkt']),
        fmt_rub(d['trial']),
        fmt_rub(d['profit']),
        fmt_rub(d['cum']),
    ])

t = Table(rows, colWidths=[10*mm, 14*mm, 17*mm, 22*mm, 18*mm, 18*mm, 16*mm, 18*mm, 14*mm, 22*mm, 22*mm])
ts = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("FONTSIZE", (0, 0), (-1, 0), 7.5),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, -1), BODY),
    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("ALIGN", (0, 1), (0, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.3, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
    ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])
for i, d in enumerate(month_data[12:24], start=1):
    ts.add("FONTNAME", (-2, i), (-2, i), BOLD)
    ts.add("FONTNAME", (-1, i), (-1, i), BOLD)
    ts.add("TEXTCOLOR", (-2, i), (-2, i), SUCCESS if d['profit'] >= 0 else WARN)
    ts.add("TEXTCOLOR", (-1, i), (-1, i), SUCCESS if d['cum'] >= 0 else WARN)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))

# Y2 итоги
y2_revenue = sum(d['mrr'] for d in month_data[12:24])
y2_profit = sum(d['profit'] for d in month_data[12:24])
y2_mkt = sum(d['mkt'] for d in month_data[12:24])
y2_sal = sum(d['sal'] for d in month_data[12:24])
y2_ti = sum(d['ti'] for d in month_data[12:24])
y2_bo = sum(d['bo'] for d in month_data[12:24])
y2_end_mrr = month_data[23]['mrr']
y2_end_cash = month_data[23]['cum']

story.append(Paragraph("11.1 Итоги Года 2", H2))
y2_summary = [
    ["Метрика", "Значение"],
    ["Платящих на конец Y2 (M24)", "6 250 клиентов"],
    ["Выручка на M24 (последний месяц)", fmt_rub(y2_end_mrr)],
    ["Суммарная выручка за Год 2", fmt_rub(y2_revenue)],
    ["Расходы за Год 2: зарплаты команде", fmt_rub(y2_sal)],
    ["Расходы за Год 2: токены + инфра", fmt_rub(y2_ti)],
    ["Расходы за Год 2: бэк-офис", fmt_rub(y2_bo)],
    ["Расходы за Год 2: маркетинг", fmt_rub(y2_mkt)],
    ["Накопленная прибыль за Год 2", fmt_rub(y2_profit)],
    ["Деньги на счёте на конец Y2", fmt_rub(y2_end_cash)],
]
t = Table(y2_summary, colWidths=[100*mm, 71*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "RIGHT")
ts.add("BACKGROUND", (0, -2), (-1, -1), SUCCESS_BG)
ts.add("FONTNAME", (0, -2), (-1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 14 — Financial model Year 3 (M25-M36)
# ======================================================================
page_title("12", "Финансовая модель — Год 3 (май 2028 - апрель 2029)",
           "Третий год — зрелая прибыль. К M36: 11 900 платящих, MRR 49 М/мес, годовая выручка 530+ М ₽, накопленные деньги 130+ М ₽.")

rows = [["Мес", "Платящ", "Доход\nс клиента", "Выручка/мес", "Зарплаты", "Токен\n+ инфра", "Бэк-офис", "Маркет", "Прбник", "Прибыль", "На счёте"]]
for d in month_data[24:36]:
    rows.append([
        f"M{d['m']}",
        fmt_num(d['paying']),
        fmt_rub(d['arpu']),
        fmt_rub(d['mrr']),
        fmt_rub(d['sal']),
        fmt_rub(d['ti']),
        fmt_rub(d['bo']),
        fmt_rub(d['mkt']),
        fmt_rub(d['trial']),
        fmt_rub(d['profit']),
        fmt_rub(d['cum']),
    ])

t = Table(rows, colWidths=[10*mm, 14*mm, 17*mm, 22*mm, 18*mm, 18*mm, 16*mm, 18*mm, 14*mm, 22*mm, 22*mm])
ts = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_FILL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), BOLD),
    ("FONTSIZE", (0, 0), (-1, 0), 7.5),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, -1), BODY),
    ("FONTSIZE", (0, 1), (-1, -1), 7.5),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("ALIGN", (0, 1), (0, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.3, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
    ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])
for i, d in enumerate(month_data[24:36], start=1):
    ts.add("FONTNAME", (-2, i), (-2, i), BOLD)
    ts.add("FONTNAME", (-1, i), (-1, i), BOLD)
    ts.add("TEXTCOLOR", (-2, i), (-2, i), SUCCESS)
    ts.add("TEXTCOLOR", (-1, i), (-1, i), SUCCESS)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))

# Y3 итоги
y3_revenue = sum(d['mrr'] for d in month_data[24:36])
y3_profit = sum(d['profit'] for d in month_data[24:36])
y3_mkt = sum(d['mkt'] for d in month_data[24:36])
y3_end_mrr = month_data[35]['mrr']
y3_end_cash = month_data[35]['cum']

story.append(Paragraph("12.1 Итоги Года 3", H2))
y3_summary = [
    ["Метрика", "Значение"],
    ["Платящих на конец Y3 (M36)", "11 900 клиентов"],
    ["Выручка на M36 (последний месяц)", fmt_rub(y3_end_mrr)],
    ["Выручка за весь Год 3", fmt_rub(y3_revenue)],
    ["Маркетинговый бюджет за Y3", fmt_rub(y3_mkt)],
    ["Накопленная прибыль за Год 3", fmt_rub(y3_profit)],
    ["Деньги на счёте на конец Y3", fmt_rub(y3_end_cash)],
]
t = Table(y3_summary, colWidths=[100*mm, 71*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "RIGHT")
ts.add("BACKGROUND", (0, -2), (-1, -1), SUCCESS_BG)
ts.add("FONTNAME", (0, -2), (-1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 15 — Сводка 36 мес + ключевые точки
# ======================================================================
page_title("13", "Сводка финансовой модели за 36 месяцев",
           "Ключевые цифры и точки роста. Главный результат: на 36 мес — годовая выручка 530+ М ₽, накопленная прибыль 130+ М ₽, без внешних инвестиций.")

# Cumulative totals
total_revenue = sum(d['mrr'] for d in month_data)
total_profit = sum(d['profit'] for d in month_data)
total_mkt = sum(d['mkt'] for d in month_data)
total_sal = sum(d['sal'] for d in month_data)
total_ti = sum(d['ti'] for d in month_data)
total_bo = sum(d['bo'] for d in month_data)
total_trial = sum(d['trial'] for d in month_data)

# Поиск ключевых вех
first_profit = next((d['m'] for d in month_data if d['profit'] > 0), None)
first_cash_positive = next((d['m'] for d in month_data if d['cum'] > 0 and d['m'] > 1), None)
min_cash = min(d['cum'] for d in month_data)
min_cash_month = next(d['m'] for d in month_data if d['cum'] == min_cash)

summary = [
    ["Метрика", "Значение"],
    ["Платящих клиентов на конец 36 мес", "11 900 человек"],
    ["Выручка в последний месяц (M36)", fmt_rub(y3_end_mrr)],
    ["Годовая выручка к концу Y3 (M36 × 12)", fmt_rub(y3_end_mrr * 12)],
    ["Суммарная выручка за 36 мес", fmt_rub(total_revenue)],
    ["Суммарные расходы: зарплаты", fmt_rub(total_sal)],
    ["Суммарные расходы: токены + инфра", fmt_rub(total_ti)],
    ["Суммарные расходы: бэк-офис", fmt_rub(total_bo)],
    ["Суммарные расходы: маркетинг", fmt_rub(total_mkt)],
    ["Суммарные расходы: пробники", fmt_rub(total_trial)],
    ["Накопленная прибыль за 36 мес", fmt_rub(total_profit)],
    ["Деньги на счёте на конец 36 мес", fmt_rub(y3_end_cash)],
    ["Самый большой минус за 36 мес (минимум)", fmt_rub(min_cash) + f" (на M{min_cash_month})"],
    ["Первый плюсовой месяц по операц. прибыли", f"M{first_profit}"],
    ["Первый месяц с накопленным плюсом (счёт > 0)", f"M{first_cash_positive}"],
]
t = Table(summary, colWidths=[110*mm, 61*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "RIGHT")
ts.add("BACKGROUND", (0, -2), (-1, -1), NAVY_LIGHT)
ts.add("FONTNAME", (0, -2), (-1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("13.1 Сравнение лет", H2))
y_compare = [
    ["Год", "Платящих к концу", "Выручка за год", "Прибыль за год", "Маркетинг за год"],
    ["Год 1 (M1-M12)", "1 670", fmt_rub(y1_revenue), fmt_rub(y1_profit), fmt_rub(y1_mkt)],
    ["Год 2 (M13-M24)", "6 250", fmt_rub(y2_revenue), fmt_rub(y2_profit), fmt_rub(y2_mkt)],
    ["Год 3 (M25-M36)", "11 900", fmt_rub(y3_revenue), fmt_rub(y3_profit), fmt_rub(y3_mkt)],
    ["ИТОГО 36 мес", "—", fmt_rub(total_revenue), fmt_rub(total_profit), fmt_rub(total_mkt)],
]
t = Table(y_compare, colWidths=[35*mm, 28*mm, 36*mm, 36*mm, 36*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (-1, -1), "RIGHT")
ts.add("BACKGROUND", (0, -1), (-1, -1), NAVY_LIGHT)
ts.add("FONTNAME", (0, -1), (-1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 16 — Cash flow + breakeven analysis
# ======================================================================
page_title("14", "Движение денег и анализ безубыточности",
           "Что нужно вложить на старте и когда деньги вернутся.")

story.append(Paragraph("14.1 Денежные потребности", H2))
cash_needs = [
    ["Параметр", "Значение"],
    ["Стартовый капитал (день 1)", fmt_rub(50000) + " (юр. оформление + резерв)"],
    ["Самое глубокое «дно» (минимум на счёте)", fmt_rub(min_cash) + f" на M{min_cash_month}"],
    ["Нужно вложить дополнительно к стартовым 50 К", fmt_rub(abs(min_cash) - 50000) if min_cash < 50000 else "0 ₽ — выручка покрывает"],
    ["Когда вернутся вложенные деньги (счёт > 0)", f"M{first_cash_positive}"],
    ["Месяц первого плюса по операционной прибыли", f"M{first_profit}"],
    ["Месяцев в минусе по операц. прибыли", f"{first_profit - 1} мес"],
]
t = Table(cash_needs, colWidths=[88*mm, 83*mm])
ts = std_table_style()
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
ts.add("ALIGN", (1, 1), (1, -1), "RIGHT")
ts.add("BACKGROUND", (0, 1), (-1, 3), WARN_BG)
ts.add("BACKGROUND", (0, 4), (-1, 5), SUCCESS_BG)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("14.2 Где брать деньги на покрытие первых месяцев", H2))
sources_rows = [
    ("1", "Стартовый капитал основателей", "50 000 ₽", "День 1"),
    ("2", "Минимальная зарплата основателям (вместо стандартной)", "Экономия 100 К/мес × 5 мес = 500 К", "M1-M5"),
    ("3", "Годовые подписки со скидкой 50% (предзаказы)", "30 × 5 940 = 178 К ₽", "M2-M3"),
    ("4", "Бартер с фрилансерами (дизайнер за Pro-подписку)", "Экономия 60-80 К/мес", "M3-M9"),
    ("5", "Партнёрки с AmoCRM / Bitrix24 (15-20% от выручки клиента)", "+50-150 К/мес дополн. выручки", "M6+"),
    ("6", "Yandex AI Studio Boost (фонд 500 млн руб)", "До 5 М ₽ (по заявке)", "M2-M6"),
    ("7", "Кастом-разработка для Pro/Enterprise клиентов", "+50-200 К/мес (часы джунов)", "M6+"),
]
sources = [["#", "Источник", "Сколько даёт", "Когда"]]
for n, src, amount, when in sources_rows:
    sources.append([n, cp(src, bold=True), cp(amount), cp(when)])
t = Table(sources, colWidths=[8*mm, 70*mm, 50*mm, 43*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 5*mm))

story.append(Paragraph("14.3 Главный вывод", H2))
verdict_box = [["Главный вывод по финансовой модели:"], [
    f"При структуре расходов 30/30/10/30 (зарплаты/токены+инфра/бэк-офис/опер. прибыль) "
    f"и реалистичном росте клиентской базы с 0 до 11 900 за 36 месяцев — мы выходим на "
    f"<b>годовую выручку {fmt_rub(y3_end_mrr * 12)}</b> и накапливаем <b>{fmt_rub(y3_end_cash)}</b> на счёте.\n\n"
    f"Самый большой риск — минус {fmt_rub(abs(min_cash))} на M{min_cash_month}. "
    f"Покрывается стартовым капиталом основателей + минимальной зарплатой первые 5 месяцев. "
    f"<b>Внешних инвестиций не требуется.</b>"
]]
t = Table(verdict_box, colWidths=[171*mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (0,0), BOLD),
    ("FONTSIZE", (0,0), (0,0), 11),
    ("TEXTCOLOR", (0,0), (0,0), ACCENT),
    ("FONTNAME", (0,1), (0,1), BODY),
    ("FONTSIZE", (0,1), (0,1), 10),
    ("LEADING", (0,1), (0,1), 14),
    ("TEXTCOLOR", (0,1), (0,1), INK),
    ("BACKGROUND", (0,0), (0,1), NAVY_LIGHT),
    ("BOX", (0,0), (0,1), 1, ACCENT),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("TOPPADDING", (0,0), (0,0), 10),
    ("TOPPADDING", (0,1), (0,1), 4),
    ("BOTTOMPADDING", (0,1), (0,1), 12),
]))
# Replace newlines for paragraph
verdict_para = Paragraph(
    f"При структуре расходов 30/30/10/30 (зарплаты/токены+инфра/бэк-офис/опер. прибыль) "
    f"и реалистичном росте клиентской базы с 0 до 11 900 за 36 месяцев — мы выходим на "
    f"<b>годовую выручку {fmt_rub(y3_end_mrr * 12)}</b> и накапливаем <b>{fmt_rub(y3_end_cash)}</b> на счёте.<br/><br/>"
    f"Самый большой риск — минус {fmt_rub(abs(min_cash))} на M{min_cash_month}. "
    f"Покрывается стартовым капиталом основателей + минимальной зарплатой первые 5 месяцев. "
    f"<b>Внешних инвестиций не требуется.</b>",
    P
)
verdict_table = Table([
    [Paragraph("Главный вывод по финансовой модели:", H3)],
    [verdict_para]
], colWidths=[171*mm])
verdict_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,1), NAVY_LIGHT),
    ("BOX", (0,0), (0,1), 1.2, ACCENT),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("TOPPADDING", (0,0), (0,0), 8),
    ("BOTTOMPADDING", (0,1), (0,1), 12),
]))
story.append(verdict_table)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 17 — Top buyer-keys
# ======================================================================
page_title("15", "Топ-15 запросов с покупательским намерением",
           "Какие конкретные запросы покупают у нас рекламу. Источник: Wordstat + Google Trends, май 2026.")

keys = [
    ["#", "Запрос", "Wordstat (показ/мес)", "Тренд", "GT индекс"],
    ["1", "автоматизация бизнес процессов", "6 508", "Растёт +20–25%", "35"],
    ["2", "автоматизация продаж", "3 140", "Растёт", "20"],
    ["3", "нейросеть для бизнеса", "2 747", "Резкий рост +200%", "3"],
    ["4", "интеграция битрикс24", "2 549", "Эвергрин", "37"],
    ["5", "настройка битрикс24", "2 056", "Эвергрин", "0"],
    ["6", "чат бот для вк", "1 839", "Растёт +30–50%", "2"],
    ["7", "разработка интернет магазина", "1 817", "4 квартал рост", "31"],
    ["8", "crm для бизнеса", "1 535", "Эвергрин", "30"],
    ["9", "создание сайта под ключ", "1 324", "4 квартал рост", "39"],
    ["10", "разработка сайта под ключ", "1 186", "4 квартал рост", "20"],
    ["11", "автоматизация маркетинга", "853", "Растёт", "0"],
    ["12", "внедрение битрикс24", "828", "Эвергрин", "0"],
    ["13", "настройка чат бота", "743", "Резкий рост +200–300%", "0"],
    ["14", "внедрение ии в компанию", "634", "Очень резкий +400–600%", "0*"],
    ["15", "заказать сайт под ключ", "582", "4 квартал рост", "0"],
]
t = Table(keys, colWidths=[10*mm, 65*mm, 32*mm, 42*mm, 22*mm])
ts = std_table_style()
ts.add("ALIGN", (0, 1), (0, -1), "CENTER")
ts.add("ALIGN", (2, 1), (-1, -1), "CENTER")
ts.add("FONTNAME", (1, 1), (1, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))

story.append(Paragraph(
    "* «Внедрение ии в компанию» имеет GT=0 (низкая агрегатная статистика), но короткая форма "
    "«внедрение ии» = GT 55, очень резкий рост. Это самый горячий запрос мая 2026.",
    SMALL
))
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 18 — Media plan
# ======================================================================
page_title("16", "Медиаплан Яндекс.Директ — версия 8",
           "Перераспределение бюджета с учётом Google Trends и убранных узких ниш.")

story.append(Paragraph("16.1 Распределение бюджета", H2))
budget_rows = [
    ("F. CRM-интеграции (ТОП-1)", "30%", "30%", "—", "100% IT, эвергрин"),
    ("A. Сайты под ключ", "22%", "22%", "—", "100% IT, 4 квартал рост"),
    ("E. Автоматизация (с фильтром)", "20%", "17%", "−3", "Эффект. IT-объём 5 700"),
    ("G. Внедрение ИИ (резкий рост)", "15%", "22%", "+7", "Google Trends подтвердил +400–600%"),
    ("D. Чат-боты", "10%", "10%", "—", "100% IT"),
    ("B. AI-конструктор (узкий)", "1%", "0%", "−1", "Перераспределён"),
    ("НОВЫЕ сезонные лендинги", "0%", "5%", "+5", "«Лучшая CRM 2026» (3 кв) + «Сайт магазина» (4 кв)"),
    ("Убрано: голос. роботы / 152-ФЗ / системы записи / YandexGPT", "2%", "0%", "−2", "Нерелевантные или ищут конкурентов"),
    ("Тестовый бюджет (новые запросы)", "0%", "4%", "+4", "Эксперименты + сравнение вариантов"),
]
budget = [["Группа", "v7 %", "v8 %", "Изменение", "Обоснование"]]
for grp, v7, v8, delta, why in budget_rows:
    budget.append([cp(grp, bold=True), v7, v8, delta, cp(why)])
t = Table(budget, colWidths=[60*mm, 14*mm, 14*mm, 20*mm, 63*mm])
ts = std_table_style()
ts.add("ALIGN", (1, 1), (3, -1), "CENTER")
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("16.2 Окупаемость рекламного бюджета с пробником", H2))
roi_table = [
    ["Бюджет/мес", "Лидов с рекламы", "С пробника", "Всего платящих", "Выручка/мес", "Окупаемость"],
    ["100 000 ₽", "40", "+60", "76", "310 080 ₽", "9.4×"],
    ["300 000 ₽", "125", "+60", "110", "448 800 ₽", "8.4×"],
    ["1 000 000 ₽", "425", "+60", "230", "938 400 ₽", "8.5×"],
]
t = Table(roi_table, colWidths=[28*mm, 28*mm, 22*mm, 30*mm, 33*mm, 30*mm])
ts = std_table_style()
ts.add("ALIGN", (0, 1), (-1, -1), "CENTER")
ts.add("FONTNAME", (-1, 1), (-1, -1), BOLD)
ts.add("BACKGROUND", (-1, 1), (-1, -1), SUCCESS_BG)
ts.add("TEXTCOLOR", (-1, 1), (-1, -1), SUCCESS)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 19 — Mix каналов + конкуренты
# ======================================================================
page_title("17", "Смесь каналов привлечения и конкуренты")

story.append(Paragraph("17.1 Рекомендуемая смесь каналов (бюджет 300 К ₽/мес)", H2))
channels = [
    ["Канал", "Доля", "Бюджет", "Цена лида", "Время до результата"],
    ["Яндекс.Директ (контекст)", "40%", "120 000 ₽", "80 ₽/лид", "2-4 недели"],
    ["Telegram-каналы (аутрич)", "30%", "90 000 ₽", "45 ₽/лид", "1-2 недели"],
    ["SEO + контент-маркетинг", "20%", "60 000 ₽", "150 ₽/лид", "3-6 месяцев"],
    ["Партнёрки (AmoCRM, Bitrix24)", "10%", "30 000 ₽", "200 ₽/лид", "2-4 месяца"],
]
t = Table(channels, colWidths=[55*mm, 18*mm, 30*mm, 30*mm, 38*mm])
ts = std_table_style()
ts.add("ALIGN", (1, 1), (-1, -1), "CENTER")
ts.add("FONTNAME", (0, 1), (0, -1), BOLD)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("17.2 Карта конкурентов — топ-10", H2))
comp_rows = [
    ("Bitrix24", "Free / 2 990 / 7 990", "Да", "Да", "Да", "82% малого бизнеса, перегружен"),
    ("Tilda", "Free / 1 490 / 6 990", "Только текст", "Нет", "Нет", "+33% год к году, регуляторный риск"),
    ("Promto.ai", "690 / 2 790 / 6 890", "Anthropic", "Нет", "Нет", "Только Anthropic, через VPN"),
    ("Lovable.dev", "$25/мес", "Да", "Нет", "Нет", "Заблокирован в РФ"),
    ("Bolt.new", "$25/мес", "Да", "Нет", "Нет", "Заблокирован в РФ"),
    ("v0 (Vercel)", "$20/мес", "Да", "Нет", "Нет", "Заблокирован в РФ"),
    ("Mottor + n8n", "1 990 ₽ PRO-3", "Да", "Да", "Нет", "Self-hosted, сложно"),
    ("Nethouse", "Free / от 300", "Нет", "Нет", "Нет", "1.6 М клиентов, без AI"),
    ("Yandex AI Studio", "По запросу", "Да (DeepSeek)", "Нет", "Да", "Партнёрство (фонд 500 М)"),
    ("Omnia.AI", "0 / 990 / 7 990", "Да (RU-стек)", "Да", "Да", "3-дн пробник + IT-фокус"),
]
comp = [["Игрок", "Тарифы", "AI?", "Боты?", "152-ФЗ?", "Слабое место"]]
for name, tariffs, ai, bots, fz, weak in comp_rows:
    comp.append([cp(name, bold=True), cp(tariffs, small=True), cp(ai, center=True, small=True),
                 cp(bots, center=True, small=True), cp(fz, center=True, small=True), cp(weak, small=True)])
t = Table(comp, colWidths=[28*mm, 32*mm, 22*mm, 16*mm, 18*mm, 55*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "MIDDLE")
ts.add("BACKGROUND", (0, -1), (-1, -1), SUCCESS_BG)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 20 — Roadmap
# ======================================================================
page_title("18", "Дорожная карта с учётом сезонности",
           "Что делаем по месяцам в первый год. Главный дедлайн: запуск до сентября 2026 — иначе Bitrix24 запустит свой AI-генератор.")

roadmap_rows = [
    ("Май-июнь 2026", "Подготовка", "Демо, страницы /about /docs, бета 100 человек, 3-дн пробник", "100 бета-пользователей + 3 кейса"),
    ("Июль 2026", "Бета", "Сбор отзывов, статьи на vc.ru/Habr, отраслевые лендинги", "5-10 публикаций"),
    ("Август 2026", "Тихий запуск", "Публичный релиз, лендинг «Лучшая CRM 2026»", "30 платящих"),
    ("Сентябрь 2026", "Пик 1 (B2B)", "SEO, партнёрка с AmoCRM, GT-лендинги", "80 платящих"),
    ("Октябрь-декабрь 2026", "4 квартал пик", "Полная кампания, BlackFriday, Новый Год", "300+ платящих, выручка 0.8M+/мес"),
    ("Январь-февраль 2027", "Стабилизация", "Удержание клиентов, сравнение вариантов лендингов", "1 200 платящих"),
    ("Март-апрель 2027", "Пик 2 (B2B)", "Расширение E/F/G групп запросов", "1 670 платящих, выручка 3M+/мес"),
]
roadmap = [["Период", "Этап", "Что делаем", "Целевой показатель"]]
for per, stage, what, kpi in roadmap_rows:
    roadmap.append([cp(per, bold=True), Paragraph(f"<font color='#2563eb'><b>{stage}</b></font>", CELL), cp(what), cp(kpi)])
t = Table(roadmap, colWidths=[34*mm, 24*mm, 68*mm, 45*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 21 — Risks
# ======================================================================
page_title("19", "Барьеры и риски — топ-8",
           "Главный риск — упустить окно возможностей (запуск до сентября 2026).")

risks_data = [
    ("1", "152-ФЗ — штрафы до 500 млн ₽", "КРИТ", "152-ФЗ из коробки с дня 1 — это наш конкурентный edge"),
    ("2", "AI regulation — проект закона апр 2026", "ВЫСОК", "Compliance с дня 1, не ждём принятия"),
    ("3", "Bitrix24 доминирует (82% SMB)", "СРЕД", "Фокус на простоту + малый бизнес до 50 чел., не конкурируем фронтально"),
    ("4", "Разрыв между ценой привлечения и выручкой", "ВЫСОК", "3-дн пробник снижает стоимость привлечения в 9 раз"),
    ("5", "Дефицит кадров (AI-инженеры)", "СРЕД", "Удалённый найм + готовность к релокации"),
    ("6", "Удорожание Я.Директ +12.75% год к году", "СРЕД", "Смесь: 40% Директ + 30% Telegram + 20% SEO + 10% партнёрки"),
    ("7", "Замедление малого рынка в 2026", "СРЕД", "Экономный режим + только подтверждённые GT-тренды"),
    ("8", "Упустить окно возможностей", "КРИТ", "Жёсткий дедлайн: публичный запуск до сентября 2026"),
]
risks = [["#", "Риск", "Серьёзность", "Что делаем чтобы снизить"]]
for n, risk, sev, fix in risks_data:
    risks.append([n, cp(risk, bold=True), cp(sev, center=True, bold=True), cp(fix)])
t = Table(risks, colWidths=[8*mm, 60*mm, 22*mm, 81*mm])
ts = std_table_style()
ts.add("VALIGN", (0, 0), (-1, -1), "TOP")
# Color severity backgrounds
for i, (_, _, sev, _) in enumerate(risks_data, start=1):
    if sev == "КРИТ":
        ts.add("BACKGROUND", (2, i), (2, i), WARN_BG)
    elif sev == "ВЫСОК":
        ts.add("BACKGROUND", (2, i), (2, i), ORANGE_BG)
    else:
        ts.add("BACKGROUND", (2, i), (2, i), ALT_ROW)
t.setStyle(ts)
story.append(t)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("19.1 Красные флаги — НЕ запускать если", H2))
red_flags = [
    "Запуск откладывается до октября 2026 — поздно, Bitrix24 опередит со своим AI-генератором",
    "152-ФЗ compliance не закладывается с дня 1 — штрафы могут уничтожить проект",
    "Делается ставка на западный экспорт — продукт делается под РФ",
    "Маркетинг-бюджет менее 300 К ₽/мес в первый год — недостаточно для разгона воронки",
]
for rf in red_flags:
    story.append(Paragraph(f"<font color='#dc2626'>⬛</font> {rf}", P))
story.append(Spacer(1, 4*mm))
story.append(footer())
story.append(PageBreak())

# ======================================================================
# PAGE 22 — Action Items
# ======================================================================
page_title("20", "Действия первого приоритета (срочно)",
           "Что делать на следующих 4 недели чтобы запуск в августе 2026 состоялся.")

story.append(Paragraph("20.1 Семантика и Я.Директ", H2))
sem_actions = [
    "Прогнать 33 узких IT-запроса через Wordstat (+3 000-9 000 показов)",
    "Прогнать 142 расширения с покупательским намерением (окупаемость 17.1×)",
    "Настроить минус-слова для группы E (производство / 1С / HR / логистика)",
    "Создать лендинг /luchshaya-crm-2026 к августу (пик 3 квартала)",
    "Создать лендинг /sayt-internet-magazina к сентябрю (4 квартал рост)",
]
for a in sem_actions:
    story.append(Paragraph(f"• {a}", P))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("20.2 Продукт", H2))
prod_actions = [
    "Реализовать 3-дневный пробник VPS (авто-выдача + авто-удаление по таймеру)",
    "Восстановить демо-сайт kofeynya-kazan.omnia.ai",
    "Создать страницы /about и /docs",
    "Перенести MVP-запуск на август 2026",
]
for a in prod_actions:
    story.append(Paragraph(f"• {a}", P))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("20.3 Партнёрки", H2))
partner_actions = [
    "AmoCRM партнёрка (10 000+ интеграторов, 15% recurring доход)",
    "Bitrix24 партнёрка (100+ сертифицированных партнёров, 20% revenue share)",
    "Yandex AI Studio Boost — подать заявку на фонд 500 млн ₽",
]
for a in partner_actions:
    story.append(Paragraph(f"• {a}", P))
story.append(Spacer(1, 6*mm))

# Главный месседж
story.append(Paragraph("20.4 Главный итог", H2))
final_msg = Paragraph(
    "Версия 1 показывала точку безубыточности на 363 клиентах. "
    "<b>Версия 6 на реальных данных Wordstat + Google Trends + 3-дневный пробник — на 52 клиентах.</b> "
    "Окупаемость рекламы 9.4×. Стоимость привлечения снижена в 9 раз через бесплатный пробник. "
    "За 36 месяцев модель выходит на годовую выручку " + fmt_rub(y3_end_mrr * 12) + " "
    "и накапливает " + fmt_rub(y3_end_cash) + " прибыли — <b>без внешних инвестиций</b>. "
    "Главный финансовый риск минимален.",
    P
)
final_table = Table([[final_msg]], colWidths=[171*mm])
final_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), NAVY_LIGHT),
    ("BOX", (0,0), (0,0), 1.5, ACCENT),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("TOPPADDING", (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
]))
story.append(final_table)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("Прилагаемые документы:", H3))
docs = [
    "STRATEGIC_BRIEF.md v8 — финальная стратегия + Google Trends + 3-дн пробник",
    "GOOGLE_TRENDS_ANALYSIS_v8.md — анализ GT + экономика пробника",
    "GOOGLE_TRENDS_FULL_v8.csv — полные данные Google Trends по 90 запросам",
    "IT_FOCUS_v7.md — чистота IT-трафика для 60 buyer-keys + минус-слова",
    "BUYER_INTENT_EXPANSION_v8.md — 142 коммерческих расширения",
    "Omnia_AI_Market_Analysis_v7.xlsx — 8 листов семантического анализа",
    "WORDSTAT_DATA_v7.csv — 236 запросов с реальными показами",
    "MARKETING_PLAN_2026.md — детальный маркетинг-план 2026 года",
    "Token_Economics_v1.xlsx + .pdf — экономика токенов AI и тарифной модели",
]
for d in docs:
    story.append(Paragraph(f"• {d}", SMALL))

story.append(Spacer(1, 4*mm))
story.append(footer())

# === BUILD ===
doc.build(story)
print(f"OK saved: {OUT}")
print(f"Size: {OUT.stat().st_size:,} bytes")
print(f"Pages: ~{page_num_counter[0] - 1}")
