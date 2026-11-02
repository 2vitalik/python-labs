---
title: Pushmo / Pullblox (引ク押ス) + Crashmo
slug: pushmo
family: grid-platformer
also: [push-slide, thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2011
platforms: [3DS eShop (Pushmo 2011, Crashmo 2012, Stretchmo 2015), Wii U eShop (Pushmo World 2014)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pushmo", best: true, note: "тягнення до 3 кроків, rewind/reset, люки, 250+ рівнів, Pushmo Studio і QR, огляд сиквелів"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/引ク押ス", note: "JP: точні правила — тягнення збоку, обмеження стоячи на блоці, висота стрибка, перемикачі кольору, редактор 16×16→32×32, 90 слотів, Pushmo World-блоки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crashmo", note: "гравітація, вільний рух блоків, обертання камери, QR"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pushmo+3ds+gameplay", note: "пошук; геймплей Pushmo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crashmo+gameplay", note: "пошук; геймплей Crashmo"}
stage: v1
coverage: 70
mechanics: [push-object, multi-cell-size, gravity-fall, teleport-pair, reach-exit, sequential-levels, level-select, level-unlock, in-game-editor, editor-palette, editor-erase, editor-playtest, level-exchange, save-multi-slot, game-screen, help-window, +pull-object, +rewind, +depth-pull-wall, +color-switch-extend, +reset-switch, +skip-level, +qr-level-share, +rigid-shape-fall, +camera-orbit, +linked-pieces]
proposes: ["+effect:pull", "+effect:fall", "+effect:reset_level", "+cond:depth", "+cond:standing_on", "+role:switch", "+role:gate", "+feature:rewind", "+feature:skip-level", "+feature:share-code", "+feature:level-editor", "+window:editor-window", "+window:qr-scan", "+axis:undo", "+axis:field-depth", "+card:depth-pull-wall"]
author: opus
date: 2026-11-02
---

# Pushmo — висуваєш кольорові шматки стіни на 1–3 кроки до себе і лізеш ними на вершину

## Суть
Pushmo — вертикальна піксель-картина з кольорових шматків (поліоміно), вмурована в стіну. Мелло (Mallo) хапає шматок і **висуває його до себе на 1, 2 чи 3 кроки** або вштовхує назад; висунуті шматки стають сходинками, і Мелло стрибками лізе до дитини на вершині. Ядро — 2.5D-пазл «який шматок на яку глибину і в якому порядку», бо стоячи на шматку не можна тягнути його самого, а глибина опори обмежує те, що можна тягнути вище. Crashmo додає гравітацію: шматок без опори падає, і рух можливий у всі 4 горизонтальні напрямки.

## Поле і час
- Поле — стіна W×H (до 32×32 у редакторі) з **4 шарами глибини** 0…3 перед нею + земля перед стіною; кожна клітина (x, y) належить рівно одному шматку, шматок має одну глибину для всіх своїх клітин.
- Бічна камера спереди; у Crashmo камеру можна обертати навколо структури (будь-який кут).
- Real-time (ходьба, стрибки), але детерміновано: ворогів і таймера нема — чистий пазл.
- Pushmo: гравітація діє лише на Мелло, шматки висять у стіні. Crashmo: гравітація і для шматків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мелло | player | — | ходить, стрибає на 1 клітину вгору або через проміжок у 1 клітину; хапає шматок перед собою |
| Шматок (pushmo block) | object | колір, форма-поліоміно, глибина 0–3 | висувається/вштовхується на 1 за дію як ціле; Pushmo — не падає |
| Перемикач кольору (Pull-Out Switch) | switch | колір | наступив → усі шматки цього кольору одразу висуваються на 3 |
| Люк (manhole) | gate | колір пари | вхід → вихід з люка того ж кольору; заблокований — не працює |
| Дитина / ціль | static | — | досягти = рівень пройдено (Crashmo — пташка/прапор) |
| Reset-перемикач | switch | поза структурою | повертає всі шматки на глибину 0 |
| Press-to-Reset (Pushmo World) | switch | — | вштовхує все назад (?) |
| Звʼязані блоки (Pushmo World) | object | пара | рухаються разом |
| Парні протилежні (Pushmo World) | object | пара | один висувається — інший вштовхується |
| Блок-повернення (Pushmo World) | object | затримка | сам вштовхується назад за час |
| Хмара (Crashmo) | object | — | не падає без опори (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(grab+back)` → ЯКЩО `facing(mallo, piece)` і `depth(piece) < 3` і `free(cell_behind_mallo)` і `not standing_on(mallo, piece)` → ТО `pull(piece)`, `move(mallo, back)`.
- КОЛИ `input(grab+forward)` → ЯКЩО `depth(piece) > 0` і `not standing_on(mallo, piece)` → ТО `custom: push_in(piece)`.
- КОЛИ `input(grab)` збоку висунутого шматка (глибина ≥1) → ТО шматок можна тягнути/штовхати збоку (JP wiki).
- КОЛИ `input(pull)` стоячи на шматку A лицем до шматка B вище → ТО `custom: «B можна висунути щонайбільше до глибини A − 1»` (бо Мелло потрібно відступити по A) (JP wiki).
- КОЛИ `input(jump)` → ЯКЩО ціль на 1 клітину вище або проміжок ≤1 → ТО `move(mallo, target)`; униз — з будь-якої висоти (?).
- КОЛИ `tick` → ЯКЩО `not supported(mallo)` → ТО `fall(mallo)`.
- КОЛИ `enter(mallo, switch[c])` → ТО `custom: «усі шматки кольору c → глибина 3»` (Мелло, що стоїть перед ними, зсувається (?)).
- КОЛИ `enter(mallo, manhole[c])` → ЯКЩО `free(exit_manhole[c])` → ТО `teleport(mallo, pair)`.
- КОЛИ `contact(mallo, reset_switch)` → ТО `custom: reset_all(depth=0)`.
- КОЛИ `input(rewind)` (утримання L) → ТО `custom: «відмотати дії Мелло на обмежений час назад»`.
- КОЛИ `contact(mallo, child)` → ТО `win`, `next_level`.
- Crashmo: КОЛИ `after(move)` → ЯКЩО `not supported(piece)` → ТО `fall(piece)` як тверде тіло; шматок тягнеться/штовхається в 4 горизонтальні напрямки; штовхнув нижній — верхні падають.
- Перемога: дійти до цілі. Поразка: нема (лише глухий кут → rewind/reset/skip). Рахунок: нема.

## Керування і ввід
- Хрестовина/стік — ходьба; B — стрибок (?); утримання A — схопити шматок, далі назад/вперед — висунути/вштовхнути.
- L — rewind (утримання); reset — фізичний перемикач на рівні, не меню.
- Камера: зсув/огляд стіни; у Crashmo — обертання камери навколо.
- Редактор: стилус по пікселях (3DS-тач), палітра кольорів, гумка (?).

## Вікна, меню, HUD
- `main-menu` (Pushmo Park): Play → `level-select` (банк рівнів сторінками з позначками), Pushmo Studio → `editor-window`, QR → `custom-window` «зчитати QR камерою».
- `game-screen`: стіна, Мелло, мінімальний HUD (номер рівня, піктограма rewind (?)).
- `editor-window` (ヒクオス工房): полотно 16×16 → 32×32, палітра кольорів, розміщення перемикачів/люків/цілі (?), тест-проходження, збереження до 90 слотів, експорт QR як JPEG.
- `tutorial-window` — навчальні перші рівні з поясненнями.
- `pause-menu`: продовжити · пропустити рівень · вийти.
- Переходи: main-menu → level-select → game-screen → (дитина) end-screen → level-select; main-menu → editor-window → game-screen (тест) → editor-window.

## Фічі поза полем
- `rewind` (обмежений час, L) і фізичний reset-перемикач замість рестарту.
- `skip-level` — складні рівні можна пропустити й повернутись.
- `level-editor` + `level-sharing` через **QR-код** (камера 3DS зчитує; можна друкувати, фотографувати з екрана, постити) — `share-code`.
- `puzzle-bank` 250+ рівнів; Pushmo World — онлайн-майданчики через Miiverse (закрито).
- Нема рахунку, часу, зірок — лише пройдено/ні.

## Варіації й родичі
- Pushmo (2011) → Crashmo (2012: гравітація, 4 напрямки, обертання камери) → Pushmo World (2014: нові типи звʼязаних блоків) → Stretchmo (2015, F2P).
- Родичі: Sokoban (`+pull-object`), Catherine (тягнути/штовхати блоки вежі, лізти), Lara Croft GO (колони), BoxBoy (блоки як сходи).
- Осі: **глибина** (0–3 у Pushmo / вільна в Crashmo); **гравітація шматків** (нема / є); **напрямок руху шматка** (лише до/від стіни / 4 горизонтальні); **спосіб скидання** (rewind / reset-перемикач / skip); **обмін рівнями** (QR / онлайн-хаб).

## Цікавинки для курсу
- Поле 2D + глибина 0–3 як третя координата, рендер «вигляд спереди» з підписом глибини — 🥈.
- Тягнення шматка-поліоміно як цілого з перевірками «не стоїш на ньому» і «є куди відступити» — 🥉.
- Перемикач, що висуває всі шматки кольору — один ефект на групу за ознакою — 📎.
- Rewind з обмеженим вікном часу — 🥈.
- Обмін рівнями через QR (серіалізувати рівень у рядок/картинку і назад) — 🥉 (з бібліотекою QR).
- Crashmo-гравітація для поліоміно з каскадним падінням — 🥇 (порядок падіння, опора будь-якою клітиною).

## Мапа на каталог
- Є: `push-object` (вштовхнути) · `multi-cell-size` (шматок-поліоміно) · `gravity-fall` (Мелло; шматки в Crashmo) · `teleport-pair` (люки) · `reach-exit` · `sequential-levels` · `level-select` · `level-unlock` (?) · `in-game-editor` + `editor-palette` + `editor-erase` + `editor-playtest` · `level-exchange` (QR) · `save-multi-slot` (90 слотів редактора) · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+pull-object` «Тягнення обʼєкта» · entities/legality · 🥉 (є з Sokoban-варіантів).
  - `+depth-pull-wall` «Шматки стіни на глибину 0–N» · entities/state · 🥈 · слот {max_depth: 3}.
  - `+color-switch-extend` «Перемикач діє на всі обʼєкти кольору» · entities/interact · 📎.
  - `+reset-switch` «Клітина-скидання рівня» · entities/interact · 🌱.
  - `+rewind` «Безперервний відкат часу» · game-logic/save · 🥈.
  - `+skip-level` «Пропустити рівень» · levels/progression · 🌱.
  - `+qr-level-share` «Рівень як QR/рядок» · levels/editor · 🥉 · слот {format: qr|text}.
  - `+rigid-shape-fall` «Тверда фігура падає цілою» · entities/move · 🥈 — Crashmo.
  - `+camera-orbit` «Обертання камери навколо поля» · interface/render · 🥈.
  - `+linked-pieces` «Звʼязані/дзеркальні блоки» · entities/interact · 🥉 — Pushmo World.

## Пропозиції до словників
- `+effect:pull` (є ⏳) — тут з кроком назад гравця; `+effect:fall` — падіння фігури; `+effect:reset_level` — повернути всі обʼєкти в стартовий стан (перемикач, не меню).
- `+cond:depth(a, op, n)` — глибина шматка; `+cond:standing_on(a, b)` — A стоїть на B.
- `+role:switch` (кольоровий, reset), `+role:gate` (люк).
- `+feature:rewind`, `+feature:skip-level`, `+feature:share-code` (QR), `+feature:level-editor`.
- `+window:editor-window`, `+window:qr-scan` — зчитування рівня з камери/картинки.
- `+axis:undo` = `rewind`; `+axis:field-depth` — 2D-поле з обмеженою глибиною (між `square` і `3d`).
- `+card:depth-pull-wall` — див. вище.

## Джерела
- ⭐ [Wikipedia: Pushmo](https://en.wikipedia.org/wiki/Pushmo) — тягнення до 3 кроків, лише спереду/збоку з платформи, reset і rewind, skip, люки, 250+ рівнів, Pushmo Studio, QR.
- [ja.wikipedia: 引ク押ス](https://ja.wikipedia.org/wiki/引ク押ス) — правило «стоячи на блоці — на 1 менше», висота стрибка, перемикачі кольору, люки, L-rewind, редактор 16×16→32×32 і 90 слотів, нові блоки Pushmo World.
- [Wikipedia: Crashmo](https://en.wikipedia.org/wiki/Crashmo) — гравітація, вільний рух, обертання камери, QR.
- YouTube: пошуки «pushmo 3ds gameplay», «crashmo gameplay».

## Непевне
- (?) Кнопки 3DS (A — хапати, B — стрибок) і як подається глибина в HUD.
- (?) Що стається з Мелло перед стіною, коли перемикач висуває шматок на нього.
- (?) Деталі Crashmo: хмари-блоки, двері, кількість рівнів (Wikipedia: 140 нових), ціль «пташка» vs «прапор» — стаття згадує прапори.
- (?) Драбини: у куратора в брифі не було, у Pushmo не підтверджено — не включено.
- (?) Наявність `level-unlock`: Wikipedia про skip каже, що рівні можна пропускати — значить, відкриваються послідовно.
