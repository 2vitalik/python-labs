---
title: Surakarta (Roundabouts)
slug: surakarta
family: board-digital
also: [chess-abstract]
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1970
platforms: [board, Android, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Surakarta_(game)", best: true, note: "правила ходу й взяття по контурах, варіанти (Китай, Корея, Bas-basan sepur 7×7), матчі, історія"}
  - {kind: other, url: "https://project.dke.maastrichtuniversity.nl/games/games_surakarta.htm", note: "Маастрихт: короткі правила, Computer Olympiad з 2007, програма SIA"}
  - {kind: bgg, url: "https://www.boardgamegeek.com/boardgame/13715", note: "BGG"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=ts.zac.surakarta", note: "Android-застосунок (лінк з Wikipedia)"}
  - {kind: other, url: "https://sites.google.com/view/cavegames-surakarta/home", note: "дошка для друку A3"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Surakarta+board+game+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, move-8dir, legal-move-highlight, cell-click, drag-drop-piece, hover-highlight, turn-enforcement, hot-seat, ai-opponent, ai-minimax, destroy-all-enemies, no-moves-left, game-screen, end-screen, help-window, replay, state-as-data, +loop-circuit-capture, +circuit-graph, +optional-capture, +agreed-end-majority, +match-scoring, +rule-variants]
proposes: ["+cond:path_exists", "+cond:via_loop", "+effect:travel(path)", "+role:conduit", "+ui:capture-path", "+ui:circuit-colors", "+ui:last-move-highlight", "+window:variant-select", "+feature:custom-rules", "+axis:win-condition", "+card:loop-circuit-capture", "+card:circuit-graph"]
author: opus
date: 2026-11-02
---

# Surakarta — яванська абстрактна гра: ходиш на крок, а бʼєш лише після обʼїзду петлі в кутку

## Суть
Дві сторони по 12 фігур на точках сітки 6×6. Звичайний хід — на одну сусідню точку в будь-якому з 8 напрямків. **Взяття** — інше: фігура мчить уздовж одного з двох кольорових контурів, обовʼязково проходить щонайменше одну кутову петлю й зупиняється на ворожій фігурі, знімаючи її. Шлях може бути довгим і проходити ту саму порожню точку двічі, але крізь фігури — ні. Механіка взяття «через петлю» вважається унікальною серед відомих настільних ігор.

## Поле і час
- Сітка 6×6 = 36 точок; фігури стоять на перетинах ліній.
- Два контури взяття (inner / outer), кожен — замкнений цикл з 4 прямих ліній сітки, зʼєднаних 4 дугами-петлями (¾ кола) за межами дошки: малі петлі зʼєднують другі від краю лінії, великі — треті (?). Разом 8 кутових петель.
- Точка, через яку проходять обидві лінії одного контуру, проходиться двічі (на перетині); центральні точки належать обом контурам → найсильніші.
- Граф ходів: звичайний — 8-сусідство сітки; взяття — шлях по графу контуру, де петлі — додаткові ребра. Хід = одна дія, черга по черзі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура | piece | сторона (камінці / мушлі), 12 на гравця | крок на 1 у 8 напрямках на порожню точку або взяття по контуру |
| Точка | zone | належить 0/1/2 контурам | порожня / зайнята |
| Внутрішній контур | conduit | 4 лінії + 4 малі петлі; колір 1 | шлях взяття |
| Зовнішній контур | conduit | 4 лінії + 4 великі петлі; колір 2 | шлях взяття |
| Кутова петля | conduit | дуга ¾ кола, вхід/вихід по дотичній лінії | взяття можливе лише після проходу ≥1 петлі |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: кожен займає два найближчі до себе ряди (12 точок) (?).
- КОЛИ `input(step(piece, cell))` → ЯКЩО `turn_of(side)` and `custom: «cell — один із 8 сусідів»` and `free(cell)` → ТО `move(piece, cell)`.
- КОЛИ `input(capture(piece, target))` → ЯКЩО `custom: «існує шлях уздовж одного контуру від piece до target»` and `via_loop(path, ≥1)` and `custom: «усі проміжні точки порожні»` and `occupied(target, enemy)` → ТО `disappear_b`, `move(piece, target)`.
- Проміжні точки можна проходити кілька разів; власні фігури блокують шлях так само, як ворожі; власна стартова точка під час руху вважається порожньою (?).
- Шлях без петлі не бʼє: фігура, що стоїть на одній лінії з ворогом, не може його взяти напряму.
- Взяття необовʼязкове.
- Перемога: `all_gone(enemy_pieces)` → `win`.
- Якщо прогресу нема — за домовленістю `game_over`, перемагає той, у кого більше фігур (`custom: «agreed end, majority»`).
- Матч: фіксована кількість партій (очки = фігури, що лишились) або до заданої суми.
- Варіанти (Китай/Корея): без діагональних кроків; можна ковзати по зовнішньому контуру й без взяття.

## Керування і ввід
- Цифрова версія: клік по своїй фігурі → підсвітка 8 сусідніх кроків і ворожих фігур, досяжних по контурах; клік по цілі. Drag-n-drop теж.
- Для взяття з кількома можливими шляхами (два контури, два напрямки обходу) — показ шляху анімацією по петлях.
- Hot-seat або проти AI (Android-застосунки; Computer Olympiad — програми).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Гра з AI · Hot-seat · Правила · Налаштування.
- `variant-select` (кандидат): класика / без діагоналей / Bas-basan sepur 7×7.
- `game-screen`: дошка з двома кольоровими контурами (`circuit-colors`); `turn-indicator`; `captured-pieces` (лічильники 12 → 0); `capture-path` — анімація траєкторії взяття; `last-move-highlight`.
- `end-screen`: переможець, кількість фігур, що лишились (очки матчу).
- `help-window`: схема контурів з прикладом взяття.
- Переходи: main-menu → game-screen → end-screen → main-menu / реванш.

## Фічі поза полем
- `ai-opponent-levels` (мінімакс; Computer Olympiad з 2007, програма SIA — кількаразовий чемпіон).
- Матч із сумою очок (`custom-rules`: кількість партій або ціль).
- `replay` / історія ходів; `custom-rules` для варіантів.

## Варіації й родичі
- Bas-basan sepur (Джокьякарта): сітка 7×7, 14 фігур, ті самі контури. Китайський/корейський варіанти: без діагоналей, ковзання по зовнішньому контуру без взяття.
- Родичі за ідеєю «бʼє не так, як ходить»: шашки (стрибок), Fanorona (наближення/відхід), Ataxx. Родичі «траєкторія з відбиттям»: лазери Khet, біла куля в більярді.
- **Осі варіацій** взяття: по лінії сусідньо (шахи) / стрибком (шашки) / на відстані по рейці з обовʼязковою петлею (Surakarta) · блокують свої фігури чи ні · чи можна ковзати по контуру без взяття.

## Цікавинки для курсу
- Граф контурів: представлення двох циклів із петлями як списку точок з повторами — 🥉 (нетривіальна модель поля, не просто сітка).
- Перевірка взяття: прохід по циклу в обидва боки від фігури з лічильником петель до першої зайнятої точки — 🥉.
- Анімація траєкторії по дугах-петлях — 🥉 (рендер кривих).
- Кроки на 8 сусідів + 8-напрямкова підсвітка — 🌱.
- AI-мінімакс з оцінкою «фігури на перетинах контурів» — 🥇.
- Рендер дошки консоллю: контури як кольорові лінії + петлі за межами — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` · `move-8dir` · `piece-capture` · `legal-move-highlight` · `cell-click` · `drag-drop-piece` · `hover-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `ai-minimax` · `destroy-all-enemies` · `no-moves-left` · `game-screen` · `end-screen` · `help-window` · `replay` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+loop-circuit-capture` «Взяття лише через петлю контуру» · entities/combat · 🥉 · слоти {circuits: 2, min_loops: 1, own_blocks: bool}.
  - `+circuit-graph` «Контури-рейки поверх сітки» · entities/legality · 🥉 — додатковий граф руху, відмінний від сусідства.
  - `+optional-capture` «Взяття необовʼязкове» (протилежність `+forced-capture` у шашках) · entities/legality · 🌱.
  - `+agreed-end-majority` «Кінець за згодою, перемагає більшість» · game-logic/win · 🌱.
  - `+match-scoring` «Матч із суми партій або до цілі» · game-logic/score · 🌱.
  - `+rule-variants` (як шашки/лінійні ігри) — варіанти без діагоналей / 7×7.

## Пропозиції до словників
- `+cond:via_loop(path, n)` — шлях пройшов щонайменше n петель (Surakarta).
- `+cond:path_exists` (як Hex/Quoridor) — тут шлях по контуру до першої зайнятої точки.
- `+effect:travel(path)` — переміщення вздовж заданого багатоклітинного шляху з анімацією (родич `move`, але шлях — частина правила).
- `+role:conduit` — рейка/лінія, по якій рухаються (тут контури).
- `+ui:capture-path` (як шашки) · `+ui:circuit-colors` — кольорові контури на дошці · `+ui:last-move-highlight`.
- `+window:variant-select` · `+feature:custom-rules` · `+axis:win-condition` (`eliminate-all` / `majority-by-agreement`).
- `+card:loop-circuit-capture` · `+card:circuit-graph`.

## Джерела
- ⭐ [Wikipedia: Surakarta (game)](https://en.wikipedia.org/wiki/Surakarta_(game)) — хід, взяття по контурах, «можливо унікальна» механіка, варіанти, матчі, назви (Roundabouts у Сід Саксона), Computer Olympiad.
- [Maastricht DKE: Surakarta](https://project.dke.maastrichtuniversity.nl/games/games_surakarta.htm) — правила коротко, Computer Olympiad з 2007, SIA.
- [BGG 13715](https://www.boardgamegeek.com/boardgame/13715) · [Android-застосунок](https://play.google.com/store/apps/details?id=ts.zac.surakarta) · [дошка для друку](https://sites.google.com/view/cavegames-surakarta/home).
- YouTube: пошук «Surakarta board game rules».

## Непевне
- (?) Яка саме пара ліній утворює який контур (малі петлі — 2-га/5-та лінії, великі — 3-тя/4-та) і назви inner/outer — з памʼяті; Wikipedia дає лише схему.
- (?) Стартова розстановка «два ближні ряди» — з діаграми/памʼяті, текстом не описано.
- (?) Чи вважається власна стартова точка порожньою при обході (типова комп'ютерна реалізація) — джерела мовчать; про блокування своїми фігурами джерела формулюють по-різному.
- (?) Рік 1970 — перша публікація у Франції; сама гра традиційна, дата невідома.
- (?) BGA-версії нема (gamepanel повертає помилку); iOS-застосунки є в пошуку App Store, але не перевірені.
