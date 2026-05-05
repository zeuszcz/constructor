import { useEffect, useMemo, useState } from 'react'
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion'
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
} from 'lucide-react'
import { track } from './lib/track.js'

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

function NavBar() {
  const [scrolled, setScrolled] = useState(false)
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const links = [
    { id: 'demo', label: 'Демо' },
    { id: 'versions', label: 'Версии и откат' },
    { id: 'how', label: 'Как работает' },
    { id: 'pricing', label: 'Тарифы' },
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
          <a
            href="#start"
            className="btn-primary"
            onClick={() => track('cta_click', { location: 'navbar', label: 'Начать' })}
          >
            Начать
            <ArrowRight className="h-4 w-4" />
          </a>
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

function MockWarm({ withMenu, mini = false }) {
  const sz = mini ? mockMiniSizes : mockFullSizes
  return (
    <div
      className="relative h-full w-full overflow-hidden"
      style={{
        background:
          'radial-gradient(ellipse 100% 70% at 50% 0%, #f5e6c8 0%, #e8d4ad 45%, #d4ba83 100%)',
      }}
    >
      {/* paper grain */}
      <div
        className="absolute inset-0 opacity-30 mix-blend-multiply"
        style={{
          backgroundImage:
            'radial-gradient(circle at 30% 20%, rgba(120,80,30,0.08), transparent 40%), radial-gradient(circle at 80% 70%, rgba(140,90,40,0.07), transparent 40%)',
        }}
      />
      <div className={'relative z-10 ' + sz.pad}>
        <div className={'inline-flex items-center gap-1.5 rounded-full border border-amber-900/20 bg-white/40 backdrop-blur ' + sz.eyebrow}>
          <Coffee className={sz.tinyIcon + ' text-amber-900/70'} />
          <span className="uppercase tracking-[0.22em] text-amber-900/80">
            Кофейня · Патрики
          </span>
        </div>

        <h3 className={'mt-3 font-serif text-amber-950 ' + sz.h1} style={{ fontWeight: 590, letterSpacing: '-0.01em' }}>
          Эспрессо у Нади
        </h3>
        <p className={'mt-1 text-amber-900/75 ' + sz.body}>
          Зерно прямого обжарова с ферм Эфиопии и Бразилии
        </p>

        {!withMenu ? (
          <div className={'mt-4 grid grid-cols-2 gap-2 ' + sz.bodyBlock}>
            <div className="rounded-lg border border-amber-900/15 bg-white/60 p-2.5">
              <Clock className={sz.tinyIcon + ' text-amber-900/70'} />
              <div className={'mt-1 text-amber-950 ' + sz.label} style={{ fontWeight: 510 }}>
                Открыто
              </div>
              <div className={'text-amber-900/70 ' + sz.tinyText}>пн–вс · 8:00–22:00</div>
            </div>
            <div className="rounded-lg border border-amber-900/15 bg-white/60 p-2.5">
              <MapPin className={sz.tinyIcon + ' text-amber-900/70'} />
              <div className={'mt-1 text-amber-950 ' + sz.label} style={{ fontWeight: 510 }}>
                Найти нас
              </div>
              <div className={'text-amber-900/70 ' + sz.tinyText}>Малая Бронная, 12</div>
            </div>
          </div>
        ) : (
          <MockMenu mini={mini} accent="warm" />
        )}

        <div className={'mt-4 inline-flex items-center gap-1.5 rounded-full bg-amber-700 px-4 py-2 text-white ' + sz.cta} style={{ fontWeight: 510 }}>
          {withMenu ? 'Заказать онлайн' : 'Забронировать столик'}
          <ArrowRight className={sz.tinyIcon} />
        </div>
      </div>
    </div>
  )
}

function MockDark({ broken = false, restored = false, mini = false }) {
  const sz = mini ? mockMiniSizes : mockFullSizes
  return (
    <div
      className="relative h-full w-full overflow-hidden"
      style={{
        background:
          'radial-gradient(ellipse 90% 60% at 50% 0%, rgba(255,193,107,0.08) 0%, transparent 60%), linear-gradient(180deg, #0c0d10 0%, #08090a 100%)',
      }}
    >
      {/* faint grid */}
      <div
        className="absolute inset-0 opacity-50"
        style={{
          backgroundImage:
            'linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />

      <div className={'relative z-10 ' + sz.pad}>
        <div className="flex items-center justify-between">
          <div className={'inline-flex items-center gap-1.5 rounded-full border border-amber-300/20 bg-amber-300/[0.06] backdrop-blur ' + sz.eyebrow}>
            <Coffee className={sz.tinyIcon + ' text-amber-300/80'} />
            <span className="uppercase tracking-[0.22em] text-amber-200/80">
              Кофейня · Патрики
            </span>
          </div>
          {broken && !mini && (
            <div className="inline-flex items-center gap-1.5 rounded-md border border-danger/40 bg-danger/10 px-2 py-1 font-mono text-[10px] text-danger">
              <AlertTriangle className="h-3 w-3 animate-pulse" />
              layout collision
            </div>
          )}
        </div>

        {/* Heading area — broken state shows logo overlapping */}
        <div className="relative mt-3">
          {broken && (
            <div
              className={'absolute -left-2 -top-2 z-10 rounded-md border border-danger/30 bg-danger/15 px-2 py-1 ' + sz.h1}
              style={{ fontWeight: 590, color: '#fca5a5' }}
            >
              ☕ Надя
            </div>
          )}
          <h3
            className={'font-serif text-amber-50 ' + sz.h1 + (broken ? ' opacity-40 line-through decoration-danger/60' : '')}
            style={{ fontWeight: 590, letterSpacing: '-0.01em' }}
          >
            Эспрессо у Нади
          </h3>
        </div>
        <p className={'mt-1 text-amber-100/60 ' + sz.body + (broken ? ' opacity-40' : '')}>
          Зерно прямого обжарова с ферм Эфиопии и Бразилии
        </p>

        <MockMenu mini={mini} accent="dark" muted={broken} />

        <div
          className={
            'mt-4 inline-flex items-center gap-1.5 rounded-full px-4 py-2 ' +
            sz.cta +
            (broken
              ? ' border border-danger/30 bg-danger/10 text-danger'
              : ' bg-amber-400 text-amber-950')
          }
          style={{ fontWeight: 510 }}
        >
          {broken ? 'Кнопка не работает' : 'Заказать онлайн'}
          {!broken && <ArrowRight className={sz.tinyIcon} />}
        </div>

        {/* Restored success toast */}
        <AnimatePresence>
          {restored && !mini && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="absolute right-4 top-4 z-20 inline-flex items-center gap-2 rounded-lg border border-success/40 bg-success/15 px-3 py-2 text-[12px] text-success backdrop-blur"
            >
              <CheckCircle2 className="h-3.5 w-3.5" />
              Откатил на v3 за 0.4 сек
            </motion.div>
          )}
        </AnimatePresence>

        {/* Mini badge for restored thumbnail */}
        {restored && mini && (
          <div className="absolute right-1 top-1 grid h-3 w-3 place-items-center rounded-full bg-success">
            <CheckCircle2 className="h-2 w-2 text-canvas" />
          </div>
        )}

        {/* Mini badge for broken thumbnail */}
        {broken && mini && (
          <div className="absolute right-1 top-1 grid h-3 w-3 place-items-center rounded-full bg-danger">
            <X className="h-2 w-2 text-canvas" strokeWidth={3} />
          </div>
        )}
      </div>
    </div>
  )
}

function MockMenu({ mini, accent = 'warm', muted = false }) {
  const sz = mini ? mockMiniSizes : mockFullSizes
  const items = [
    { name: 'Эспрессо', price: '200 ₽', tag: null },
    { name: 'Капучино', price: '320 ₽', tag: 'хит' },
    { name: 'Раф ванильный', price: '380 ₽', tag: null },
    { name: 'Латте', price: '350 ₽', tag: null },
  ]
  const isWarm = accent === 'warm'
  return (
    <div
      className={
        'mt-4 grid gap-1.5 rounded-xl border p-2.5 ' +
        (isWarm
          ? 'border-amber-900/15 bg-white/60'
          : 'border-amber-200/10 bg-white/[0.02]') +
        (muted ? ' opacity-30' : '')
      }
    >
      {items.map((it) => (
        <div
          key={it.name}
          className={
            'flex items-center justify-between border-b py-1.5 last:border-b-0 ' +
            (isWarm ? 'border-amber-900/10' : 'border-white/5')
          }
        >
          <span
            className={
              'flex items-center gap-1.5 ' +
              sz.bodyBlock +
              (isWarm ? ' text-amber-950' : ' text-amber-50')
            }
            style={{ fontWeight: 510 }}
          >
            {it.name}
            {it.tag && !mini && (
              <span
                className={
                  'rounded-full px-1.5 py-0 font-mono text-[9px] uppercase ' +
                  (isWarm
                    ? 'bg-amber-700/15 text-amber-800'
                    : 'bg-amber-300/15 text-amber-300')
                }
              >
                {it.tag}
              </span>
            )}
          </span>
          <span
            className={
              'font-mono ' +
              sz.bodyBlock +
              (isWarm ? ' text-amber-900/80' : ' text-amber-200/80')
            }
          >
            {it.price}
          </span>
        </div>
      ))}
    </div>
  )
}

const mockFullSizes = {
  pad: 'p-5 sm:p-6',
  eyebrow: 'px-2.5 py-1 text-[10px]',
  h1: 'text-[26px] sm:text-[30px]',
  body: 'text-[12.5px] sm:text-[13px]',
  bodyBlock: 'text-[12px]',
  label: 'text-[12px]',
  tinyText: 'text-[10.5px]',
  cta: 'text-[12px]',
  tinyIcon: 'h-3 w-3',
}
const mockMiniSizes = {
  pad: 'p-1.5',
  eyebrow: 'px-1 py-0.5 text-[5px]',
  h1: 'text-[8px]',
  body: 'text-[5px]',
  bodyBlock: 'text-[5px]',
  label: 'text-[5px]',
  tinyText: 'text-[4px]',
  cta: 'text-[5px]',
  tinyIcon: 'h-1 w-1',
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
  return (
    <section id="top" className="relative overflow-hidden pb-12 pt-28 md:pb-16 md:pt-32">
      <div className="grid-bg pointer-events-none absolute inset-0 opacity-60" />
      <div className="container-x relative">
        <div className="mx-auto flex max-w-3xl flex-col items-center text-center">
          <span className="eyebrow">
            <Sparkles className="h-3 w-3 text-accent-glow" />
            Российская AI-платформа · pre-launch
          </span>
          <h1 className="display-h1 mt-5">
            <span className="text-gradient">Промпт. Сайт.</span>{' '}
            <span className="accent-gradient">Откат.</span>
          </h1>
          <p className="mt-5 max-w-xl text-[17px] leading-relaxed text-ink-muted md:text-[18px]">
            Сайт с backend, доменом и SSL — за минуты по одному чату. И откат любой
            версии в один клик, если AI что-то сломает.
          </p>

          <div className="mt-7 flex flex-col items-center gap-3 sm:flex-row">
            <a
              href="#start"
              className="btn-primary text-[15px]"
              onClick={() => track('cta_click', { location: 'hero', label: 'Начать' })}
            >
              Начать бесплатно
              <ArrowRight className="h-4 w-4" />
            </a>
            <a
              href="#demo"
              className="text-[14px] text-ink-muted transition hover:text-ink"
              onClick={() => track('hero_demo_link')}
            >
              ↓ Смотри живой пример
            </a>
          </div>

          <div className="mt-5 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-ink-dim">
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Без VPN и крипты
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Российские серверы
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Оплата ₽ · ЮKassa
            </span>
          </div>
        </div>

        {/* The demo — story-driven, the heart of the page */}
        <div className="relative mx-auto mt-12 max-w-6xl">
          <HeroDemo />
        </div>
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
/* Comparison table                                                   */
/* ================================================================== */

const COMPARISON = [
  {
    name: 'Omnia.AI',
    accent: true,
    rows: [true, true, true, true, true, true],
  },
  { name: 'Lovable / v0 / Bolt', rows: [true, false, false, 'partial', false, false] },
  { name: 'Tilda / Wix', rows: [false, true, false, true, false, false] },
  { name: 'Студия / агентство', rows: [false, true, false, true, true, false] },
]

const COMPARISON_FEATURES = [
  'AI-чат генерация',
  'Российский рынок и рубли',
  'Backend под ключ',
  'Auto-deploy + SSL',
  'Кастом-логика',
  'Откат версий в 1 клик',
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

        <div className="mt-10 overflow-hidden rounded-2xl border border-line bg-elev1/60">
          <div className="grid grid-cols-[1.6fr_repeat(4,_1fr)] text-[12px] text-ink-muted">
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
    name: 'Starter',
    price: '6 990',
    sub: 'для физиков и портфолио',
    features: [
      'Сервер S (2 vCPU, 2 ГБ)',
      'Кошелёк токенов 1 500 ₽',
      'Домен .ru или .рф',
      'SSL автоматом',
      'Auto-deploy',
      '50 снапшотов истории',
    ],
    cta: 'Начать',
  },
  {
    name: 'Pro',
    price: '17 990',
    sub: 'для бизнеса и стартапов',
    highlight: true,
    badge: 'Популярный',
    features: [
      'Сервер M (4 vCPU, 8 ГБ)',
      'Кошелёк токенов 5 000 ₽',
      '2 домена + Let\'s Encrypt DV',
      'Backend + Redis + S3',
      'Staging + GitHub-синк',
      '500 снапшотов + side-by-side',
      'Email-поддержка SLA 24ч',
    ],
    cta: 'Начать с Pro',
  },
  {
    name: 'Enterprise',
    price: '34 990',
    sub: 'для агентств и команд',
    features: [
      'Сервер L (8 vCPU, 16 ГБ)',
      'Кошелёк токенов 15 000 ₽',
      'До 5 доменов, OV/EV SSL',
      'DR-реплика + офсайт-бэкапы',
      'Приоритет очереди LLM',
      'Без лимита снапшотов',
      'Менеджер + SLA 4ч',
    ],
    cta: 'Связаться',
  },
]

function PricingSection() {
  return (
    <section id="pricing" className="relative py-20 md:py-24">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Wallet className="h-3 w-3 text-accent-glow" /> Тарифы
          </span>
          <h2 className="display-h2 mt-5 text-gradient">Один счёт. Без сюрпризов.</h2>
          <p className="mt-5 text-ink-muted">
            Хостинг, AI-токены, домен и поддержка — в одной подписке. Можно менять
            модель LLM на лету. Первые 100 клиентов фиксируют цену на год.
          </p>
        </div>

        <div className="mt-12 grid gap-4 lg:grid-cols-3">
          {TIERS.map((t) => (
            <div
              key={t.name}
              className={
                'relative flex flex-col rounded-2xl border p-6 transition ' +
                (t.highlight
                  ? 'border-accent/40 bg-gradient-to-b from-accent/[0.08] to-elev1 shadow-glow'
                  : 'border-line bg-elev1/70 hover:border-white/15')
              }
            >
              {t.badge && (
                <div className="absolute -top-3 right-6 rounded-full bg-accent px-3 py-1 text-[10px] uppercase tracking-[0.18em] text-white">
                  {t.badge}
                </div>
              )}

              <div className="text-[14px] uppercase tracking-[0.2em] text-ink-muted">
                {t.name}
              </div>
              <div className="mt-1 text-[12px] text-ink-dim">{t.sub}</div>

              <div className="mt-5 flex items-baseline gap-1.5">
                <span
                  className="text-[44px] leading-none text-ink"
                  style={{ fontWeight: 590, letterSpacing: '-0.02em' }}
                >
                  {t.price}
                </span>
                <span className="text-[14px] text-ink-muted">₽ / мес</span>
              </div>

              <ul className="mt-6 space-y-2.5">
                {t.features.map((f) => (
                  <li
                    key={f}
                    className="flex items-start gap-2.5 text-[13.5px] text-ink-muted"
                  >
                    <Check className="mt-0.5 h-4 w-4 flex-none text-accent-glow" />
                    {f}
                  </li>
                ))}
              </ul>

              <div className="mt-7">
                <a
                  href="#start"
                  className={t.highlight ? 'btn-primary w-full' : 'btn-ghost w-full'}
                  onClick={() =>
                    track('cta_click', {
                      location: 'pricing',
                      tier: t.name,
                      label: t.cta,
                    })
                  }
                >
                  {t.cta} <ArrowRight className="h-4 w-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ================================================================== */
/* FAQ                                                                 */
/* ================================================================== */

const FAQ = [
  {
    q: 'А если AI сломает сайт неудачным промптом?',
    a: 'Не сломает — каждый промпт создаёт новый снапшот, старая версия живёт. Откат в один клик через ленту версий, без git и терминала. Это главное, чем мы отличаемся от Lovable, Bolt и v0.',
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
        <VersioningSection />
        <ProblemsSection />
        <HowItWorks />
        <ComparisonSection />
        <FeaturesSection />
        <PricingSection />
        <FaqSection />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  )
}
