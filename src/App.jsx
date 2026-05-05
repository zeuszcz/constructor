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
  PlayCircle,
} from 'lucide-react'
import { track } from './lib/track.js'

/* ------------------------------------------------------------------ */
/* Logo                                                               */
/* ------------------------------------------------------------------ */

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

/* ------------------------------------------------------------------ */
/* NavBar                                                             */
/* ------------------------------------------------------------------ */

function NavBar() {
  const [scrolled, setScrolled] = useState(false)
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const links = [
    { id: 'how', label: 'Как работает' },
    { id: 'features', label: 'Возможности' },
    { id: 'pricing', label: 'Тарифы' },
    { id: 'faq', label: 'Вопросы' },
  ]

  return (
    <header
      className={
        'fixed inset-x-0 top-0 z-50 transition ' +
        (scrolled
          ? 'border-b border-line bg-canvas/80 backdrop-blur-xl'
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
          <a
            href="#start"
            className="hidden btn-ghost sm:inline-flex"
            onClick={() => track('nav_login')}
          >
            Войти
          </a>
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

/* ------------------------------------------------------------------ */
/* Hero — animated demo                                               */
/* ------------------------------------------------------------------ */

const DEMO_MESSAGES = [
  { role: 'user', text: 'Сделай лендинг для кофейни «Эспрессо у Нади» — Москва, Патрики' },
  {
    role: 'ai',
    text: 'Ок! Подбираю шрифты, тёплую палитру, добавляю меню, карту и форму брони. Деплою на espressonadya.ru…',
  },
  { role: 'user', text: 'Замени фон на тёмный' },
]

function HeroDemo() {
  const reduce = useReducedMotion()
  const [step, setStep] = useState(0)

  useEffect(() => {
    if (reduce) return
    const t = setInterval(() => setStep((s) => (s + 1) % 5), 2200)
    return () => clearInterval(t)
  }, [reduce])

  const messagesShown = Math.min(step + 1, DEMO_MESSAGES.length)
  const versionsBuilt = Math.min(step, 4)

  return (
    <div className="relative">
      {/* glow orbs */}
      <div className="pointer-events-none absolute -left-16 -top-16 h-72 w-72 glow-orb opacity-90" />
      <div className="pointer-events-none absolute -right-10 bottom-0 h-72 w-72 glow-orb opacity-60" />

      <div className="relative grid gap-3 rounded-3xl border border-line bg-elev1/60 p-3 shadow-cardLift backdrop-blur-xl md:p-4 lg:grid-cols-[360px_1fr]">
        {/* Chat side */}
        <div className="flex flex-col gap-2 rounded-2xl border border-line bg-canvas/90 p-3">
          <div className="flex items-center justify-between border-b border-line pb-2">
            <div className="flex items-center gap-2 text-xs text-ink-muted">
              <MessageSquare className="h-3.5 w-3.5" />
              Чат проекта
            </div>
            <span className="rounded-full border border-line bg-white/[0.03] px-2 py-0.5 font-mono text-[10px] text-ink-muted">
              Sonnet 4.6
            </span>
          </div>

          <div className="flex min-h-[200px] flex-col gap-2 overflow-hidden">
            <AnimatePresence initial={false}>
              {DEMO_MESSAGES.slice(0, messagesShown).map((m, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.35 }}
                  className={
                    'max-w-[88%] rounded-2xl px-3 py-2 text-[13px] leading-snug ' +
                    (m.role === 'user'
                      ? 'self-end bg-accent/20 text-ink'
                      : 'self-start border border-line bg-white/[0.02] text-ink-muted')
                  }
                >
                  {m.text}
                </motion.div>
              ))}
              {messagesShown < DEMO_MESSAGES.length && (
                <motion.div
                  key="typing"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="self-start rounded-2xl border border-line bg-white/[0.02] px-3 py-2 text-[13px] text-ink-dim"
                >
                  <span className="inline-flex gap-1">
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-ink-dim" />
                    <span
                      className="h-1.5 w-1.5 animate-pulse rounded-full bg-ink-dim"
                      style={{ animationDelay: '0.2s' }}
                    />
                    <span
                      className="h-1.5 w-1.5 animate-pulse rounded-full bg-ink-dim"
                      style={{ animationDelay: '0.4s' }}
                    />
                  </span>
                </motion.div>
              )}
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

        {/* Preview side */}
        <div className="overflow-hidden rounded-2xl border border-line bg-canvas">
          <div className="flex items-center gap-2 border-b border-line bg-elev1/80 px-3 py-2">
            <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
            <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
            <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
            <span className="ml-2 truncate font-mono text-[11px] text-ink-dim">
              https://espressonadya.ru
            </span>
            <span className="ml-auto rounded-md border border-line bg-white/[0.03] px-1.5 py-0.5 font-mono text-[10px] text-success">
              ● live
            </span>
          </div>

          <div className="relative h-[260px] sm:h-[300px]">
            <AnimatePresence mode="wait">
              <motion.div
                key={step}
                initial={{ opacity: 0, scale: 0.985 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.45 }}
                className="absolute inset-0"
              >
                <PreviewMock variant={step % 3} />
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Version timeline */}
          <div className="border-t border-line bg-elev1/80 px-3 py-2.5">
            <div className="mb-1.5 flex items-center justify-between text-[11px] text-ink-dim">
              <span className="inline-flex items-center gap-1.5">
                <GitBranch className="h-3 w-3" />
                Лента версий
              </span>
              <span>после каждого промпта</span>
            </div>
            <div className="flex items-center gap-1.5">
              {Array.from({ length: 5 }).map((_, i) => {
                const built = i <= versionsBuilt
                const active = i === versionsBuilt
                return (
                  <div
                    key={i}
                    className={
                      'flex-1 overflow-hidden rounded-md border transition ' +
                      (active
                        ? 'border-accent shadow-glow'
                        : built
                          ? 'border-line'
                          : 'border-line/40')
                    }
                  >
                    <div
                      className={
                        'h-9 w-full ' +
                        (built
                          ? 'bg-gradient-to-br from-accent/20 via-white/5 to-white/0'
                          : 'bg-white/[0.02]')
                      }
                    />
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function PreviewMock({ variant }) {
  if (variant === 0) {
    return (
      <div className="h-full w-full bg-gradient-to-b from-[#1a120a] via-[#0f0a07] to-[#08090a] p-4">
        <div className="mx-auto max-w-[420px]">
          <div className="text-[10px] uppercase tracking-[0.2em] text-amber-300/70">
            Кофейня · Патрики
          </div>
          <div
            className="mt-1 text-[22px] leading-tight text-ink"
            style={{ fontWeight: 590 }}
          >
            Эспрессо у Нади
          </div>
          <div className="mt-1 text-[11px] text-ink-muted">
            Зерно прямого обжарова. Открыто с 8:00.
          </div>
          <div className="mt-3 grid grid-cols-3 gap-1.5">
            {['Эспрессо', 'Капучино', 'Раф'].map((t) => (
              <div
                key={t}
                className="rounded-md border border-amber-500/20 bg-amber-500/5 p-2 text-[10px] text-amber-100/80"
              >
                {t}
              </div>
            ))}
          </div>
          <div className="mt-2 inline-flex rounded-full bg-amber-400 px-3 py-1 text-[10px] text-[#1a120a]">
            Забронировать столик
          </div>
        </div>
      </div>
    )
  }
  if (variant === 1) {
    return (
      <div className="h-full w-full bg-gradient-to-br from-emerald-500/10 via-canvas to-canvas p-4">
        <div className="mx-auto max-w-[420px]">
          <div className="text-[10px] uppercase tracking-[0.2em] text-emerald-300/70">
            Готовая бизнес-страница
          </div>
          <div
            className="mt-1 text-[22px] leading-tight text-ink"
            style={{ fontWeight: 590 }}
          >
            Меню, бронь, доставка
          </div>
          <div className="mt-3 grid grid-cols-2 gap-1.5">
            <div className="rounded-md border border-line bg-white/[0.03] p-2">
              <div className="h-1.5 w-12 rounded-full bg-white/15" />
              <div className="mt-1 h-1.5 w-20 rounded-full bg-white/10" />
            </div>
            <div className="rounded-md border border-line bg-white/[0.03] p-2">
              <div className="h-1.5 w-10 rounded-full bg-white/15" />
              <div className="mt-1 h-1.5 w-16 rounded-full bg-white/10" />
            </div>
            <div className="col-span-2 rounded-md border border-emerald-400/20 bg-emerald-500/5 p-2">
              <div className="text-[10px] text-emerald-200/80">
                ✓ Forms, БД, авторизация — готовы
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
  return (
    <div className="h-full w-full bg-gradient-to-b from-[#0a0b14] via-canvas to-canvas p-4">
      <div className="mx-auto max-w-[420px]">
        <div className="text-[10px] uppercase tracking-[0.2em] text-accent-glow">
          Тёмная тема · откат на v3
        </div>
        <div
          className="mt-1 text-[22px] leading-tight text-ink"
          style={{ fontWeight: 590 }}
        >
          Эспрессо у Нади
        </div>
        <div className="mt-3 grid grid-cols-3 gap-1.5">
          {['Эспрессо', 'Капучино', 'Раф'].map((t) => (
            <div
              key={t}
              className="rounded-md border border-line bg-white/[0.03] p-2 text-[10px] text-ink-muted"
            >
              {t}
            </div>
          ))}
        </div>
        <div className="mt-2 inline-flex rounded-full bg-accent px-3 py-1 text-[10px] text-white">
          Забронировать столик
        </div>
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* Hero                                                               */
/* ------------------------------------------------------------------ */

function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pb-16 pt-32 md:pb-24 md:pt-36">
      <div className="grid-bg pointer-events-none absolute inset-0 opacity-60" />
      <div className="container-x relative">
        <div className="mx-auto flex max-w-3xl flex-col items-center text-center">
          <span className="eyebrow">
            <Sparkles className="h-3 w-3 text-accent-glow" />
            Российская vibe-coding платформа · pre-launch
          </span>
          <h1 className="display-h1 mt-6">
            <span className="text-gradient">Промпт. Сайт.</span>{' '}
            <span className="accent-gradient">Готово.</span>
          </h1>
          <p className="mt-6 max-w-xl text-[17px] leading-relaxed text-ink-muted md:text-[18px]">
            Сайт с backend, доменом и деплоем — за минуты. По одному чату. Откат
            любой версии в один клик. Всё в рублях, без VPN и крипты.
          </p>

          <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row">
            <a
              href="#start"
              className="btn-primary text-[15px]"
              onClick={() => track('cta_click', { location: 'hero', label: 'Начать' })}
            >
              Начать
              <ArrowRight className="h-4 w-4" />
            </a>
            <a
              href="#demo"
              className="btn-ghost text-[15px]"
              onClick={() => track('hero_demo')}
            >
              <PlayCircle className="h-4 w-4" />
              Посмотреть, как работает
            </a>
          </div>

          <div className="mt-6 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs text-ink-dim">
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Без VPN и криптокошельков
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> Российские серверы
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Check className="h-3 w-3 text-success" /> ЮKassa и Tinkoff
            </span>
          </div>
        </div>

        <div id="demo" className="relative mx-auto mt-14 max-w-5xl">
          <HeroDemo />
        </div>

        <div className="mx-auto mt-10 grid max-w-4xl grid-cols-2 gap-x-6 gap-y-4 text-center md:grid-cols-4">
          {[
            { k: 'минуты', v: 'до live-сайта' },
            { k: '1 счёт', v: 'вместо пяти сервисов' },
            { k: '1 клик', v: 'откат любой версии' },
            { k: '₽', v: 'оплата и поддержка' },
          ].map((s) => (
            <div key={s.v} className="flex flex-col items-center gap-1">
              <div className="text-2xl text-ink" style={{ fontWeight: 590 }}>
                {s.k}
              </div>
              <div className="text-xs text-ink-dim">{s.v}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

/* ------------------------------------------------------------------ */
/* Problems                                                            */
/* ------------------------------------------------------------------ */

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
    pain: 'Lovable, Bolt и v0 не работают для РФ',
    solution: 'Рублёвая оплата, российские серверы, поддержка на русском.',
  },
]

function ProblemsSection() {
  return (
    <section className="relative py-20 md:py-28">
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
              initial={{ opacity: 0, y: 16 }}
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

/* ------------------------------------------------------------------ */
/* How it works                                                        */
/* ------------------------------------------------------------------ */

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
    <section id="how" className="relative py-20 md:py-28">
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
              initial={{ opacity: 0, y: 16 }}
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

/* ------------------------------------------------------------------ */
/* Versioning — flagship feature                                       */
/* ------------------------------------------------------------------ */

function VersioningSection() {
  const versions = [
    { id: 'v1', label: 'Стартовый шаблон', delta: '+ 312 строк', warm: true },
    { id: 'v2', label: 'Добавили меню', delta: '+ 78 строк' },
    { id: 'v3', label: 'Тёмная тема', delta: '~ 41 строка', highlight: true },
    { id: 'v4', label: 'Подвинули CTA', delta: '~ 12 строк' },
    { id: 'v5', label: 'Сломал AI промптом', delta: '− 88 строк', danger: true },
  ]
  return (
    <section className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="mx-auto grid items-center gap-12 lg:grid-cols-2">
          <div>
            <span className="eyebrow">
              <Undo2 className="h-3 w-3 text-accent-glow" /> Главная фича
            </span>
            <h2 className="display-h2 mt-5 text-gradient">
              AI-кодинг без страха —
              <br className="hidden md:block" /> с кнопкой «вернуть как было»
            </h2>
            <p className="mt-5 max-w-xl text-ink-muted">
              После каждого промпта мы делаем снапшот: код + превью-скриншот.
              Сломал AI сайт неудачным промптом — открываешь ленту версий, выбираешь
              нужную, нажимаешь один раз. Без git, без терминала, без &laquo;ой, я не
              сохранил&raquo;.
            </p>

            <ul className="mt-7 space-y-3">
              {[
                'Снапшот после каждого изменения — автоматически',
                'Превью каждой версии: видишь, как было, до отката',
                'Откат в один клик, без потери текущей работы',
                'История промптов — что именно изменили в тот раз',
              ].map((t) => (
                <li key={t} className="flex items-start gap-3 text-[15px] text-ink">
                  <span className="mt-1 grid h-5 w-5 flex-none place-items-center rounded-full bg-accent/20 text-accent-glow">
                    <Check className="h-3 w-3" />
                  </span>
                  {t}
                </li>
              ))}
            </ul>

            <div className="mt-8">
              <a
                href="#start"
                className="btn-primary text-[15px]"
                onClick={() =>
                  track('cta_click', { location: 'versioning', label: 'Начать' })
                }
              >
                Попробовать <ArrowRight className="h-4 w-4" />
              </a>
            </div>
          </div>

          <motion.div
            initial={{ opacity: 0, x: 24 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.55 }}
            className="card-elev"
          >
            <div className="mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2 text-[12px] text-ink-muted">
                <GitBranch className="h-3.5 w-3.5" />
                Лента версий проекта
              </div>
              <span className="rounded-md border border-line bg-white/[0.03] px-2 py-0.5 font-mono text-[10px] text-ink-muted">
                espressonadya.ru
              </span>
            </div>

            <div className="divide-line overflow-hidden rounded-xl border border-line bg-canvas/60">
              {versions.map((v) => (
                <div
                  key={v.id}
                  className={
                    'flex items-center gap-3 px-3 py-3 transition ' +
                    (v.highlight ? 'bg-accent/[0.08]' : '')
                  }
                >
                  <div
                    className={
                      'h-12 w-16 flex-none rounded-md border ' +
                      (v.warm
                        ? 'border-amber-500/20 bg-gradient-to-br from-amber-500/20 to-amber-500/0'
                        : v.danger
                          ? 'border-danger/30 bg-gradient-to-br from-danger/20 to-danger/0'
                          : v.highlight
                            ? 'border-accent/40 bg-gradient-to-br from-accent/30 to-accent/0'
                            : 'border-line bg-white/[0.03]')
                    }
                  />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[11px] text-ink-dim">
                        {v.id}
                      </span>
                      <span
                        className={
                          'truncate text-[14px] ' +
                          (v.danger ? 'text-danger' : 'text-ink')
                        }
                        style={{ fontWeight: 510 }}
                      >
                        {v.label}
                      </span>
                    </div>
                    <div className="mt-0.5 font-mono text-[11px] text-ink-dim">
                      {v.delta}
                    </div>
                  </div>
                  <button
                    type="button"
                    className={
                      'rounded-full px-3 py-1 text-[11px] transition ' +
                      (v.highlight
                        ? 'bg-accent text-white'
                        : 'border border-line bg-white/[0.02] text-ink-muted hover:text-ink')
                    }
                    tabIndex={-1}
                  >
                    {v.highlight ? 'Активна' : 'Вернуться сюда'}
                  </button>
                </div>
              ))}
            </div>

            <div className="mt-4 flex items-start gap-3 rounded-xl border border-accent/30 bg-accent/[0.08] p-3 text-[13px] text-ink">
              <Shield className="mt-0.5 h-4 w-4 flex-none text-accent-glow" />
              <span>
                Никто из конкурентов не делает версионирование с превью «в один клик».
                У Lovable и Bolt — git вручную, у Tilda — нет AI вообще.
              </span>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

/* ------------------------------------------------------------------ */
/* Comparison                                                         */
/* ------------------------------------------------------------------ */

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
    <section className="relative py-20 md:py-28">
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

/* ------------------------------------------------------------------ */
/* Features grid                                                       */
/* ------------------------------------------------------------------ */

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
    desc: 'Регистрация .ru/.рф автоматом, Let\'s Encrypt без настроек.',
  },
  {
    icon: Server,
    title: 'Российские серверы',
    desc: 'Стратегический партнёр SafeCloud / CORTEL. 152-ФЗ — из коробки.',
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
    <section id="features" className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Sparkles className="h-3 w-3 text-accent-glow" /> Возможности
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Всё под одной крышей
          </h2>
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

/* ------------------------------------------------------------------ */
/* Pricing                                                             */
/* ------------------------------------------------------------------ */

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
    <section id="pricing" className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">
            <Wallet className="h-3 w-3 text-accent-glow" /> Тарифы
          </span>
          <h2 className="display-h2 mt-5 text-gradient">
            Один счёт. Никаких сюрпризов.
          </h2>
          <p className="mt-5 text-ink-muted">
            Хостинг, AI-токены, домен и поддержка — в одной подписке. Можно
            докупать токены отдельно, можно менять модель LLM на лету.
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

        <p className="mt-6 text-center text-[12px] text-ink-dim">
          На pre-launch фиксируем цену для первых 100 клиентов.
        </p>
      </div>
    </section>
  )
}

/* ------------------------------------------------------------------ */
/* FAQ                                                                 */
/* ------------------------------------------------------------------ */

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
    <section id="faq" className="relative py-20 md:py-28">
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

/* ------------------------------------------------------------------ */
/* Final CTA + email capture                                           */
/* ------------------------------------------------------------------ */

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
    <section id="start" className="relative py-20 md:py-28">
      <div className="container-x">
        <div className="relative mx-auto max-w-4xl overflow-hidden rounded-3xl border border-line bg-gradient-to-br from-accent/[0.12] via-elev1 to-canvas px-6 py-14 md:px-12 md:py-20">
          <div className="pointer-events-none absolute -left-24 -top-24 h-72 w-72 glow-orb opacity-90" />
          <div className="pointer-events-none absolute -right-16 -bottom-16 h-72 w-72 glow-orb opacity-60" />

          <div className="relative mx-auto max-w-2xl text-center">
            <span className="eyebrow">
              <Rocket className="h-3 w-3 text-accent-glow" /> Pre-launch waitlist
            </span>
            <h2 className="display-h2 mt-5">
              <span className="text-gradient">Готовы попробовать </span>
              <span className="accent-gradient">первыми?</span>
            </h2>
            <p className="mt-5 text-ink-muted">
              Оставь email — получишь приглашение в закрытую бету и зафиксируешь
              стартовую цену для первых 100 клиентов.
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
                  Начать <ArrowRight className="h-4 w-4" />
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

/* ------------------------------------------------------------------ */
/* Footer                                                              */
/* ------------------------------------------------------------------ */

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
          <a href="#how" className="hover:text-ink">
            Как работает
          </a>
          <a href="#features" className="hover:text-ink">
            Возможности
          </a>
          <a href="#pricing" className="hover:text-ink">
            Тарифы
          </a>
          <a href="#faq" className="hover:text-ink">
            Вопросы
          </a>
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

/* ------------------------------------------------------------------ */
/* App root                                                           */
/* ------------------------------------------------------------------ */

export default function App() {
  useEffect(() => {
    track('page_view')
  }, [])

  return (
    <div className="relative">
      <NavBar />
      <main>
        <Hero />
        <ProblemsSection />
        <HowItWorks />
        <VersioningSection />
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
