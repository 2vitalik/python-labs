---
title: Sugar, Sugar
slug: sugar-sugar
aka: [Sugar Sugar, "sugar, sugar 2", "sugar, sugar 3"]
family: dig-gravity
also: [thinky]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 2011
platforms: [web (Flash → HTML5), iOS, Android]
links:
  - {kind: official, url: "https://www.bartbonte.com/sugarsugar/", best: true, note: "сторінка автора: мета «Draw and get enough sugar in the cups!», лінки на HTML5-версію і мобільні"}
  - {kind: play, url: "https://poki.com/en/g/sugar-sugar-html5", note: "грати в браузері (HTML5-конверсія Flash-оригіналу)"}
  - {kind: other, url: "https://apps.apple.com/app/sugar-sugar/id568141784", note: "iOS-версія 2012: тисячі частинок, кольорові фільтри, перемикачі гравітації, телепорти, режим вільного малювання"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bart_Bonte", note: "автор; Sugar, Sugar (2011) у списку ігор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sugar+sugar+bart+bonte+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, particles, collect-quota, goal-counter, remaining-counter, teleport, sequential-levels, restart-level, level-select, game-screen, main-menu, end-screen, +freehand-draw-barrier, +permanent-ink, +particle-sand-flow, +color-filter, +gravity-flip, +cup-countdown, +sandbox-draw-mode]
proposes: ["+effect:draw_barrier", "+effect:flow", "+trigger:pass_through", "+ui:cup-counter", "+feature:sandbox-draw", "+card:freehand-draw-barrier", "+card:particle-sand-flow", "+card:color-filter", "+card:gravity-flip", "+card:cup-countdown"]
author: opus
date: 2026-11-09
---

# Sugar, Sugar — намалюй лінії, по яких падаючий цукор сам скотиться в чашки

## Суть
Зверху з носика безперервно сиплеться цукор — тисячі частинок з гравітацією. Гравець мишею або пальцем малює лінії, які стають твердими: по них цукор скочується, ними його розділяють і загороджують. Мета рівня — набрати в кожну чашку потрібну кількість цукру, у пізніших рівнях — ще й потрібного кольору (кольорові фільтри) і з перемиканням гравітації. Ядро для корпусу: **гравець не керує частинками, а лише будує рельєф**, по якому тече «пісок»; намальоване не стерти. Описую рельєфний (намальований) шар і частинки; клітинного поля нема — це піксельна маска.

## Поле і час
- Один екран бічного виду; шари: тло, намальовані лінії й готові перешкоди (тверді пікселі), частинки цукру, чашки, фільтри, джерела.
- Частинки симулюються щокадру: падають, скочуються по похилих лініях, накопичуються купками (поведінка falling sand).
- Real-time: цукор сиплеться весь час, гравець малює на ходу.
- Рівень — фіксована композиція; оригінал (браузер) має послідовні рівні й фінальний вільний (?), мобільна версія — 125 нових рівнів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Носик-джерело | spawner | позиція, колір цукру (?) | безперервно спавнить частинки |
| Частинка цукру | object | колір | падає; на перешкоді скочується вбік; накопичується; виліт за екран — втрачена (?) |
| Намальована лінія | static | товщина пензля | тверда, назавжди; цукор її не проходить |
| Перешкода рівня | static | — | готові стінки/полиці |
| Чашка | zone | число-квота, колір (опц.) | рахує цукор, що впав усередину; число спадає до 0 |
| Кольоровий фільтр | terrain | колір | частинка, що пролетіла крізь нього, перефарбовується |
| Перемикач гравітації | switch | — | обертає напрям падіння (вгору/вниз) (?) щодо деталей |
| Телепорт | gate | пара | частинка входить в одну точку, виходить з іншої (мобільна версія) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `spawn_at(sugar, spout)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(sugar)`; інакше ЯКЩО `free(below_diag)` → ТО `move(sugar, diag)`; інакше `block` — частинка лягає на купу.
- КОЛИ `input(draw, path)` → ТО `custom: «пікселі вздовж штриха стають твердою стіною»`; стерти не можна.
- КОЛИ `contact(sugar, filter)` → ТО `custom: «частинка набуває кольору фільтра»`.
- КОЛИ `enter(sugar, cup)` → ЯКЩО `custom: «колір чашки не заданий або збігається з кольором частинки»` → ТО `counter(cup_quota, −1)`.
- КОЛИ `enter(sugar, cup)` → ЯКЩО `not same(sugar, cup, color)` → ТО `custom: «частинка не зараховується»` (?) щодо штрафу.
- КОЛИ `counter(cup_quota, =, 0)` → ТО `custom: «чашка заповнена»`.
- КОЛИ `input(gravity_switch)` → ТО `custom: «гравітація частинок змінює напрям»` — цукор у повітрі летить назад.
- КОЛИ `contact(sugar, teleport)` → ТО `teleport(sugar, pair)`.
- КОЛИ `edge(sugar)` → ТО `disappear(sugar)` (?).
- КОЛИ `custom: «усі чашки заповнені»` → ТО `win`, `next_level`.
- КОЛИ `input(reset)` → ТО `restart` — єдиний спосіб прибрати намальоване.
- Перемога: всі чашки до нуля · Поразка: нема, лише рестарт · Рахунок: нема.

## Керування і ввід
- Ліва кнопка миші + drag (або палець) — малювати лінію довільної форми.
- Кнопка/клавіша перемикання гравітації (у рівнях, де вона є); сторонні гайди — пробіл (?).
- Кнопка reset — перезапустити рівень.

## Вікна, меню, HUD
- `main-menu`: старт, вибір рівня в мобільній версії (`level-select`) (?).
- `game-screen`: поле, джерела, чашки з числами (`cup-counter`), кнопки reset і гравітації.
- `end-screen` рівня: перехід на наступний.
- Мобільна версія: налаштування звуку (з історії версій), sandbox.

## Фічі поза полем
- `levels-sequential`; мобільна — 125 рівнів, додані оновленнями.
- `mode-sandbox` — вільне малювання без мети (мобільна версія).
- `sound-toggle` (мобільна, з історії версій).

## Варіації й родичі
- Серія: sugar, sugar 2, sugar, sugar 3 і Christmas Special (?) — нові елементи на тій самій основі.
- Родичі: [sandspiel.md](sandspiel.md), [the-powder-toy.md](the-powder-toy.md) — частинки без мети; [wheres-my-water.md](wheres-my-water.md) — направити рідину до мети, але копанням; Crayon Physics (малюнок стає фізичним тілом); Line Rider.
- **Осі варіацій**: вплив гравця «копати рельєф / малювати рельєф / ставити блоки»; матеріал «пісок / рідина»; квота «кількість / кількість + колір»; помилки «стерти можна / не можна (тут)».

## Цікавинки для курсу
- Частинки «пісок» на піксельній масці з накопиченням купок — 📎.
- Малювання твердої лінії drag-ом з товщиною (растеризація штриха без розривів) — 🌱/📎.
- Чашка з квотою і кольоровою умовою + фільтри, що перефарбовують — 🌱.
- Перемикач гравітації для всіх частинок — 🌱.
- «Незатерта» розмітка як ресурс помилки: рівень вчить планувати до першого штриха — 🌱 (правило), дизайн рівнів — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `particles` · `collect-quota` ↔ чашка · `goal-counter` / `remaining-counter` ↔ число на чашці · `teleport` · `sequential-levels` · `restart-level` · `level-select` (?) · `game-screen` / `main-menu` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+freehand-draw-barrier` «Намальований штрих стає стіною» · interface/input · 📎 · слот {brush}.
  - `+permanent-ink` «Розмітку не стерти, лише рестарт» · game-logic/rules · 🌱.
  - `+particle-sand-flow` «Частинки падають і сиплються купками» · entities/move · 📎.
  - `+color-filter` «Прохід крізь фільтр перефарбовує» · entities/interact · 🌱.
  - `+gravity-flip` «Перемикання напрямку гравітації» · entities/move · 🌱.
  - `+cup-countdown` «Ціль-контейнер з квотою, що спадає» · game-logic/goals · 🌱.
  - Також: `+sandbox-draw-mode`.

## Пропозиції до словників
- `+effect:draw_barrier` — гравець малює довільну тверду лінію (не `place` поштучно, не `set_cell` однієї клітини).
- `+effect:flow` — повтор: сипке/рідке розтікається купкою.
- `+trigger:pass_through` — частинка пройшла крізь проникну сутність (фільтр).
- `+ui:cup-counter` — число-квота на контейнері, що спадає.
- `+feature:sandbox-draw` — режим малювання без мети.

## Джерела
- ⭐ [bartbonte.com/sugarsugar](https://www.bartbonte.com/sugarsugar/) — мета гри й лінки на всі версії.
- [Poki: sugar sugar HTML5](https://poki.com/en/g/sugar-sugar-html5) — малювати лінії, заповнити кожну чашку, керування мишею/пальцем.
- [App Store](https://apps.apple.com/app/sugar-sugar/id568141784) — тисячі частинок, кольорові фільтри, перемикачі гравітації, телепорти, sandbox, 125 рівнів, v1.0 — 23.10.2012.
- [Wikipedia: Bart Bonte](https://en.wikipedia.org/wiki/Bart_Bonte) — автор, рік 2011 (у дизамбігу WP — 2012).

## Непевне
- (?) Кількість рівнів браузерного оригіналу й наявність вільного фінального рівня — з памʼяті.
- (?) Чи частинка не того кольору в чашці лише не зараховується, чи «псує» квоту — сторонні гайди розходяться.
- (?) Чи частинки, що вилетіли за екран, зникають; чи носиків кілька й різних кольорів.
- (?) Клавіша перемикання гравітації (пробіл) — з неперевіреного стороннього гайду.
- (?) Склад серії (2, 3, Christmas) — з памʼяті й назв у результатах пошуку.
