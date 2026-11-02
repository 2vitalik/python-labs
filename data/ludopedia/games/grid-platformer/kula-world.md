---
title: Kula World (Roll Away, KulaQuest)
slug: kula-world
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: hotseat
  info: partial
  random: none
  goal: collect
year: 1998
platforms: ["PlayStation (1998 EU; 1998 NA як Roll Away; 1999 JP як KulaQuest)", "PS3/PSP (PS one Classics) (?)"]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kula_World", best: true, note: "ключі → вихід, «змінна гравітація», типи платформ, фрукти → бонус, штрафи очок, режими 2P"}
  - {kind: other, url: "https://psxdatacenter.com/games/P/K/SCES-01000.html", note: "PSX Data Center — керування з мануалу, 220 рівнів, Time Trial, Copycat, memory card"}
  - {kind: wiki, url: "https://sv.wikipedia.org/wiki/Kula_World", note: "шведська стаття: крок за кроком, бонус-рівень на час"}
  - {kind: other, url: "https://www.mobygames.com/game/9070/-/adblurbs/", note: "MobyGames (бачив у пошуку, WebFetch — 403)"}
  - {kind: other, url: "https://www.gamepressure.com/games/kula-world/z24c6e", note: "Gamepressure (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kula+World+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, impassable-cells, key-and-door, collect-quota, item-pickup, event-points, time-out, environment-death, touch-death, inertia-slide, teleport-pair, sequential-levels, save-progress, score-records, player-camera, movement-animation, +edge-roll-gravity, +relative-turn-controls, +jump-n-cells, +quota-gate, +toggle-spikes, +bounce-pad, +carrier-platform, +paint-cell, +fruit-bonus-unlock, +score-as-lives, +time-trial, +copycat-mode, +hourglass-flip]
proposes: ["+effect:reorient_gravity", "+effect:roll", "+effect:slide", "+effect:paint", "+trigger:edge", "+cond:supported", "+role:terrain", "+role:hazard", "+ui:key-slots", "+ui:fruit-slots", "+axis:gravity", "+axis:field", "+feature:time-trial", "+card:edge-roll-gravity"]
author: opus
date: 2026-11-02
---

# Kula World — котиш пляжний мʼяч кубиками в космосі; за ребром блока гравітація повертається на 90°

## Суть
Гравець котить мʼяч крок за кроком по поверхнях кубиків, що висять у порожнечі, збирає ключі (усі → відчиняється вихід), монети, самоцвіти й фрукт. Головне: якщо котитися за край блока, мʼяч **перекочується на бічну грань**, і «низ» тепер — та грань; світ на екрані перевертається. Стрибок перелітає проміжок, промах — падіння в космос. Межовий випадок сімʼї: поле 3D, але рух строго клітинний (крок = грань кубика).

## Поле і час
- Поле — воксельна сітка кубиків; мʼяч стоїть на **грані** кубика, тож стан = (клітина, грань-«підлога», напрям погляду). Будь-яка грань будь-якого кубика може бути підлогою.
- Камера завжди позаду мʼяча й обертається разом із «низом»; R1/R2 — подивитися вгору/вниз. Частину рівня не видно з поточної орієнтації → `info: partial` (вісь обзору, не туман).
- Real-time: рух дискретний (крок = 1 грань з анімацією), але таймер рівня й рухомі небезпеки йдуть безперервно.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мʼяч (kula) | player | орієнтація: грань + напрям | крок уперед, поворот 90°, стрибок; за ребро — на бічну грань |
| Кубик (звичайний) | terrain | — | опора на будь-якій грані |
| Ключ | pickup | 1+ на рівень | усі зібрано → вихід відчинено |
| Вихід | gate | closed/open | відкривається після всіх ключів; увійти → рівень пройдено |
| Монета | pickup | очки | — |
| Самоцвіт (jewel) | pickup | очки | — |
| Фрукт | pickup | 1 на рівень, 5 видів | 5 зібраних → бонус-рівень |
| Пісковий годинник | pickup | — | повʼязаний з таймером рівня (?: перевертає залишок) |
| Таблетка стрибка (jumping pill) | pickup | тривалість (?) | посилює стрибок (?) |
| «Хиткий» бонус | pickup | кілька секунд | екран хитається — заважає орієнтуватись |
| Шипи | hazard | висувні (?) | проколюють мʼяч → рестарт |
| Лід | terrain | — | мʼяч ковзає далі й може злетіти з краю |
| Лазер | hazard | — | спалює мʼяч |
| Рухома платформа | terrain | маршрут | везе мʼяч |
| Транспортер | terrain | пара | переносить мʼяч в інше місце |
| Пружна платформа | terrain | — | підкидає мʼяч |
| Кнопка прискорення (boost) | terrain | — | (?) |
| Котячий камінь / ворог, що «ловить» | enemy | — | знищує або «захоплює» мʼяч (?) |
| Гаряча поверхня | hazard | — | «розплавляє» мʼяч (?) |
| Кубик бонус-рівня | terrain | неактивний/активний | активується, коли по ньому прокотились |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward)` → ЯКЩО `occupied(cell_ahead_on_floor, cube)` → ТО `move(ball, forward)`.
- КОЛИ `input(forward)` → ЯКЩО `not occupied(cell_ahead, cube)` → ТО `custom: «перекотитись через ребро: floor := передня грань поточного кубика»` (`+effect:reorient_gravity`), камера обертається на 90°.
- КОЛИ `input(forward)` → ЯКЩО `occupied(cell_ahead_up, cube)` (стіна попереду) → ТО `custom: «вкотитись на стіну: floor := грань стіни»` (?) або `block`.
- КОЛИ `input(left|right)` → ТО `face(ball, ±90°)` (відносне керування, клітина та сама).
- КОЛИ `input(jump)` → ТО стрибок на місці; `input(jump+forward)` → ТО `move(ball, forward ×2)` у повітрі (через 1 проміжок).
- КОЛИ `custom: «приземлення без опори»` → ТО `fall(ball)` у порожнечу → `lose`, `score(-n)`.
- КОЛИ `contact(ball, key)` → ТО `pickup`; КОЛИ `custom: «all_collected(key)»` → ТО `set_state(exit, open)`.
- КОЛИ `contact(ball, exit)` → ЯКЩО `state(exit, open)` → ТО `win`, `score(+n)`, `next_level`.
- КОЛИ `contact(ball, coin|jewel)` → ТО `pickup`, `score(+n)`; КОЛИ `contact(ball, fruit)` → ТО `counter(fruit, +1)`; `counter(fruit, ==, 5)` → ТО `custom: «наступний — бонус-рівень»`.
- КОЛИ `contact(ball, hourglass)` → ТО `custom: «перевернути таймер: лишилось := минуло»` (?).
- КОЛИ `enter(ball, ice)` → ТО `slide(ball, forward)`; з краю → `fall` → `lose`.
- КОЛИ `contact(ball, spikes|laser|hot|enemy)` → ТО `lose`, `score(-n)` (проколото / спалено / розплавлено / захоплено).
- КОЛИ `enter(ball, transporter)` → ТО `teleport(ball, pair)`; `enter(ball, bounce)` → ТО `custom: «підкинути»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose`, `score(-n)`.
- КОЛИ `counter(score, <, 0)` → ТО `game_over`.
- Бонус-рівень: КОЛИ `enter(ball, cube)` → ТО `paint(cube, active)`; КОЛИ `all_on(cube, active)` до кінця часу → ТО `win`.
- Перемога: усі ключі → вихід. Поразка рівня: падіння, шипи, лазер, жар, ворог, час → рестарт рівня зі штрафом. Рахунок = «життя»: нижче нуля — кінець гри.

## Керування і ввід
- Хрестовина/лівий стік: ↑ — крок уперед, ←/→ — поворот на 90° (відносно погляду мʼяча), ↓ — розворот (?).
- X — стрибок; утримувати X + ↑ — стрибок на дві клітини вперед.
- R1/R2 — дивитися вгору/вниз; Start — пауза/меню.
- 2P: гравці по черзі (Time Trial) або Copycat: кожен повторює всю послідовність ходів і додає ще два.

## Вікна, меню, HUD
- `splash-screen` — лого.
- `main-menu`: Arcade · Time Trial · 2 Players (Time Trial / Copycat) (`mode-select`) · Load/Save · Options (?).
- `game-screen` — 3D-вигляд позаду мʼяча; HUD: `score`, пісковий годинник (`timer-countdown`), слоти ключів (`+ui:key-slots`), слоти фруктів (`+ui:fruit-slots`) (?: точний склад).
- `pause-menu` — продовжити / перезапустити / вийти (?).
- `custom-window` — заставка «BONUS» перед бонус-рівнем.
- `end-screen` — рахунок рівня; Game Over, коли очки < 0.
- `save-slots` — memory card: рекорди й прогрес (1 блок).

## Фічі поза полем
- `levels-sequential`: ≈200 рівнів (PSX Data Center — 220) у фіксованому порядку тематичних світів; бонус-рівні за 5 фруктів.
- `mode-time-attack` (Time Trial: кожен рівень за хвилину), `mode-versus` по черзі, Copycat — гра на памʼять.
- `save-progress` + `score-records` на memory card.

## Варіації й родичі
- Rolling-ball родичі: Marble Madness, Super Monkey Ball (вільна фізика, не клітини), Edge (куб по клітинах), Captain Toad (обертання камери), Bloxorz/Rolling Block (орієнтація фігури).
- Гравітація-як-орієнтація: VVVVVV (фліп), Mighty Flip Champs, Super Mario Galaxy, Manifold Garden, Q*bert-«edge-walker».
- **Осі варіацій:** гравітація (завжди вниз / перемикач / за поверхнею — тут) · поле (2D-сітка / поверхня кубиків-вокселів) · керування (абсолютне / відносне до погляду) · таймер (знижується / перевертається).

## Цікавинки для курсу
- Мʼяч на грані кубика, перекочування через ребро = зміна «низу» — 🥇 (стан = клітина + нормаль + напрям; повороти векторів, BFS по гранях).
- Відносне керування (поворот на 90° відносно погляду) — 🌱, але без нього 3D-сітка не читається.
- Ключі → вихід як ворота за квотою — 🌱 (повтор `key-and-door`/`collect-quota`).
- Рахунок як «життя» зі штрафами за смерть — 📎 (одне число замість лічильника життів).
- Copycat — гра на памʼять: повтори і додай 2 ходи — 📎 (запис/звірка послідовності вводу).
- Бонус-рівень «прокотись по всіх кубиках» — 🥉 (покриття вершин графа граней за час).
- Консольна версія: рендер «вигляду з мʼяча» в 2D-проєкції однієї грані — 🥈.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` (падіння в космос) · `impassable-cells` · `key-and-door` + `collect-quota` (ключі) · `item-pickup` · `event-points` · `time-out` · `environment-death` · `touch-death` · `inertia-slide` (лід) · `teleport-pair` (транспортери) · `sequential-levels` · `save-progress` · `score-records` · `player-camera` · `movement-animation`.
- **Нема** → пропозиції карток:
  - `+edge-roll-gravity` «Перекочування через ребро змінює низ» · entities/move · 🥇 · слоти {surface: cube-faces}; родичі `+directional-gravity`, `+cube-net-wrap`.
  - `+relative-turn-controls` (повтор Snake) — поворот відносно погляду.
  - `+jump-n-cells` «Стрибок на N клітин уперед» · entities/move · 🌱 · слот {n: 2}.
  - `+quota-gate` (повтор) — вихід після всіх ключів.
  - `+toggle-spikes` (повтор) — висувні шипи (?).
  - `+bounce-pad` «Пружна клітина підкидає» · entities/move · 🌱.
  - `+carrier-platform` (повтор Boxboy) — рухомі платформи.
  - `+paint-cell` (повтор Q*bert) — бонус-рівень «активуй усі кубики».
  - `+fruit-bonus-unlock` «Колекція по 1 на рівень відкриває бонус» · levels/progression · 📎 · слот {need: 5}.
  - `+score-as-lives` «Очки як життя: штраф за смерть, <0 — кінець» · game-logic/lose · 📎.
  - `+time-trial` (повтор) — рівень за хвилину.
  - `+copycat-mode` «Повтори послідовність суперника й додай ходи» · game-logic/opponent · 📎 · слот {add: 2}.
  - `+hourglass-flip` «Перевернути таймер» · game-logic/score · 🌱 (?).

## Пропозиції до словників
- `+effect:reorient_gravity(a, face)` — новий «низ» для сутності після перекочування через ребро.
- `+effect:roll` (🔥) — тут не «скочується з округлого», а основний рух мʼяча; `+effect:slide` — лід.
- `+effect:paint` ↔ є `paint(cell, color)` — бонус-рівень.
- `+trigger:edge(a)` — вихід за ребро поточної грані (не за межу поля: поле нескінченно «загортається» по кубиках).
- `+cond:supported(a)` (🔥) — після стрибка є куди приземлитись.
- `+role:terrain` (кубики, лід, пружина, транспортер), `+role:hazard` (шипи, лазер).
- `+ui:key-slots`, `+ui:fruit-slots` — порожні/заповнені слоти предметів.
- `+axis:gravity` = `per-surface` (як Troddlers: «низ» визначає поверхня); `+axis:field` = `3d` (воксельна сітка — значення вже ⏳, тут уживання).
- `+feature:time-trial` — режим «рівень за хвилину».
- `+card:edge-roll-gravity` — див. вище.

## Джерела
- ⭐ [Wikipedia: Kula World](https://en.wikipedia.org/wiki/Kula_World) — ключі й вихід, «змінна гравітація», рухомі/пружні платформи, транспортери, таблетки стрибка, фрукти → бонус, штрафи (spiked, captured, melted, laser, falls/slides off, time), рахунок < 0, режими 2P.
- [PSX Data Center](https://psxdatacenter.com/games/P/K/SCES-01000.html) — керування з мануалу (X + ↑ = стрибок на 2), R1/R2, 220 рівнів, Time Trial за хвилину, Copycat, memory card.
- [Шведська Wikipedia](https://sv.wikipedia.org/wiki/Kula_World) — крок за кроком, бонус на час.
- [MobyGames](https://www.mobygames.com/game/9070/-/adblurbs/) · [Gamepressure](https://www.gamepressure.com/games/kula-world/z24c6e) — бачив у пошуку, не відкрив.
- YouTube: пошук «Kula World gameplay».

## Непевне
- (?) Точна механіка ребра: джерела кажуть лише «alternating physics / змінна гравітація»; опис «за ребро → на бічну грань» — з памʼяті й відгуків (широко відомий, але не процитований).
- (?) Чи можна вкотитися на стіну, що стоїть попереду (увігнутий кут), чи це блок.
- (?) Пісковий годинник перевертає таймер — з памʼяті; пошук згадує лише «годинник = таймер».
- (?) Невидимі / прозорі / крихкі блоки (згадані в завданні) — підтвердження не знайшов, у таблицю не вносив.
- (?) Що саме «захоплює» і «розплавляє» мʼяч (вороги, гарячі плити), що робить boost-кнопка і таблетка стрибка, склад HUD і меню.
- WebSearch вичерпано під час роботи; GameFAQs/мануал (regvault) недоступні.
