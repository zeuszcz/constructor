# Omnia.AI — landing

Pre-launch лендинг для Omnia.AI. Цель — валидировать спрос: трафик с маркетинга
лендинг → клик «Начать» / лид с email.

## Стек

- Vite 6 + React 19
- Tailwind CSS 3.4 (Linear-inspired dark тема)
- framer-motion (анимация hero-демо и секций)
- lucide-react (иконки)
- Inter Variable c OpenType-фичами `cv01`, `ss03`

Дизайн-система — порт `linear-app` из
[nexu-io/open-design](https://github.com/nexu-io/open-design): dark-native
canvas (`#08090a`), achromatic palette с одним indigo-violet акцентом
(`#7170ff`), 8 px base spacing, weights 400 / 510 / 590.

## Запуск

```bash
npm install
npm run dev      # локально на http://localhost:5173
npm run build    # → dist/
npm run preview  # локальный просмотр прод-сборки
```

## Трекинг кликов

Каждый клик по «Начать» и важные UX-события идут через `src/lib/track.js`:

- `localStorage` (`omnia_landing_events_v1`) — последние 200 событий, для отладки
- `window.dataLayer` — формат GTM (`omnia_<event>`)
- `navigator.sendBeacon(VITE_TRACK_ENDPOINT, ...)` — если задан endpoint в env

Что отправляем:

| Событие         | Когда                                              |
| --------------- | -------------------------------------------------- |
| `page_view`     | загрузка                                           |
| `cta_click`     | любой клик «Начать» (с `location` и `tier`)        |
| `nav_link`      | клик по nav-ссылкам                                |
| `hero_demo`     | клик «Посмотреть, как работает»                    |
| `faq_toggle`    | разворот вопроса                                   |
| `lead_signup`   | сабмит email-формы                                 |
| `footer_github` | клик на GitHub в футере                            |

`VITE_TRACK_ENDPOINT` задаётся либо в `.env.local` локально, либо в
`vars.TRACK_ENDPOINT` репозитория для GH Actions.

## Деплой

Workflow `.github/workflows/deploy.yml` собирает `dist/` и публикует на GitHub
Pages при пуше в `main`. В Settings → Pages надо включить источник
**GitHub Actions** один раз.

После включения сайт будет доступен по
`https://zeuszcz.github.io/constructor/`.

## Контент

Контент лендинга собран из бизнес-плана `AI_Site_Builder_Business_Plan_v1.xlsx`
(листы 0–4, 5, 11, 17, 18). Главные сообщения:

- **Tagline:** «Промпт. Сайт. Готово.»
- **One-liner:** сайт с backend, доменом и деплоем за минуты, по одному чату,
  с откатом версий в один клик и оплатой в рублях
- **★ Главная фича:** визуальная лента версий — снапшот после каждого промпта,
  откат без git и терминала

## Roadmap

- [ ] Подключить реальный endpoint трекинга (Cloudflare Worker / FastAPI /
      Yandex Metrica events)
- [ ] OG-картинка
- [ ] Кастомный домен (omnia.ai) с CNAME
- [ ] A/B тест таглайнов («Промпт. Сайт. Готово.» vs «Сайт пишется промптами,
      не кодом.») через флаги
