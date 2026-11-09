---
title: King's Valley
slug: kings-valley
aka: [王家の谷, Ouke no Tani, "秘蔵版・王家の谷"]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1985
platforms: [MSX, ZX Spectrum (Retro Works 2009, неофіційний), MS-DOS]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/王家の谷_(ゲーム)", best: true, note: "JA: керування, предмети, 5 кольорів мумій з таблицею поведінки, двері-перемикач, ростуча стіна, обертові двері, версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/King%27s_Valley", note: "EN: огляд, 15 кімнат, FD-версія на 60 рівнів з редактором"}
  - {kind: other, url: "https://everygamegoing.com/larticle/kings-valley/86244", note: "рецензія порту: стрибок на 2 блоки, кирка копає на 2 блоки, меч знешкоджує мумію, односторонні двері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=King%27s+Valley+MSX+gameplay", note: "пошук; геймплей MSX"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, collect-all, reach-exit, touch-death, environment-death, player-death, chase-player, speed-per-type, respawn, spawn-points, dig-terrain, destructible-blocks, cell-transform, impassable-cells, one-way-cell, button-toggle, projectile-shot, temporary-modes, inventory-items, inventory-limit, restart-level, sequential-levels, map-window, level-password, in-game-editor, game-pause, unsolvable-states, player-camera, +stairs-diagonal, +jump-fixed-height, +single-use-tool, +item-blocks-jump, +growing-wall, +enemy-behavior-table, +enemy-reset-on-bumps, +exit-choice-back-forward]
proposes: ["+effect:dig", "+effect:jump(height)", "+cond:hands_empty", "+cond:on_stairs", "+trigger:bump_count(a, n)", "+role:stairs", "+feature:suicide-restart", "+card:enemy-behavior-table"]
author: opus
date: 2026-11-09
---

# King's Valley — Lode Runner у піраміді: збери коштовності, копаючи одноразовою киркою й метаючи меч у мумій, і не замуруй собі шлях

## Суть
Археолог Бік (Bick) обходить кімнати піраміди, збирає всі коштовності й виходить крізь двері до наступної піраміди. На відміну від Lode Runner, тут є **стрибок**, діагональні **сходи** і **предмети в руках**: кирка (одноразова, копає яму) і меч (кидається, знешкоджує мумію, лежить, доки його знову не піднімуть). Предмет у руках забороняє стрибати, тож кожна дія — вибір між рухливістю і можливістю. Помилка копання легко робить рівень нерозвʼязним — тоді лише самогубство й рестарт.

## Поле і час
- Блокова сітка: цегляні блоки, сходи-діагоналі, порожнеча; клітинна гравітація.
- Непарні стадії — один екран, парні — два екрани з горизонтальним скролом.
- Real-time; мумії ходять з різною швидкістю (на сходах швидкі типи — приблизно вдвічі швидше за Біка).
- Колір підлоги міняється кожні 4 стадії (коричневий, синій, червоний, зелений) — оформлення.
- Усе видно; частина коштовностей лежить у замурованих гробницях, до яких треба прокопатись.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бік | player | несе ≤ 1 предмет | біг, сходи, стрибок (з порожніми руками) на ~2 блоки вгору або дугою; падіння |
| Цегляний блок | terrain | — | опора; копається киркою |
| Сходи | terrain | діагональні | підйом/спуск діагоналлю |
| Коштовність (秘宝珠) | pickup | — | треба зібрати всі |
| Кирка | pickup | одноразова | яма 2 блоки вглиб × 1 завширшки; біля стіни прибирає ще й шматок стіни |
| Божий меч (神の剣) | pickup | багаторазовий | кидок по горизонталі; зупиняється на перешкоді, лежить; тимчасово прибирає мумію |
| Мумія біла | enemy | стеження низьке, повільна | роззирається; сходи — як Бік; не стрибає |
| Мумія жовта | enemy | стеження низьке | роззирається; швидкість як у Біка; стрибає |
| Мумія рожева | enemy | стеження низьке, повільна | роззирається; на сходах швидка; не стрибає |
| Мумія синя | enemy | стеження високе | не роззирається; швидкість як у Біка; стрибає |
| Мумія червона | enemy | стеження високе, швидка | не роззирається; на сходах швидка; не стрибає |
| Ростуча стіна | hazard | — | після певної точки росте зі стелі; вбиває Біка, мумій ні; прибирається лише копанням |
| Обертові двері | gate | одностороння, біла/синя сторона | прохід лише в один бік, після проходу сторони міняються; мумії не проходять; зникають, коли все зібрано |
| Вихідні двері ×2 | gate | зʼявляються після збору | одні — на попередню стадію, другі — на наступну |
| Перемикач дверей | switch | біля дверей | стрибок під ним відчиняє двері |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(bick, dir)`.
- КОЛИ `input(diagonal)` → ЯКЩО `cell(here, stairs)` → ТО `move(bick, diagonal)` (на MSX треба натиснути діагональ; у порті — вгору/вниз).
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)`.
- КОЛИ `input(fire)` → ЯКЩО `not has(bick, item)` і `supported(bick)` → ТО `custom: «стрибок прямо вгору або дугою вбік, ~2 блоки»`.
- КОЛИ `contact(bick, item)` → ЯКЩО `not has(bick, item)` → ТО `pickup` — лише один предмет.
- КОЛИ `input(fire)` → ЯКЩО `has(bick, pickaxe)` і `supported(bick)` і `not cell(here, stairs)` → ТО `set_cell(below, empty)` на 2 блоки вглиб; ЯКЩО `cell(side, wall)` → ТО `custom: «вибирає ще й шматок стіни»`; `take(bick, pickaxe)`.
- КОЛИ `input(fire)` → ЯКЩО `has(bick, sword)` і `supported(bick)` → ТО `throw(sword, facing)`.
- КОЛИ `blocked(sword)` → ТО `custom: «меч падає й лежить на місці»` — його можна підняти знову.
- КОЛИ `contact(sword, mummy)` → ТО `disappear_b`, `respawn(mummy, same_spot)` із затримкою.
- КОЛИ `contact(bick, mummy)` → ТО `lose`, `lives(-1)`, `restart`.
- КОЛИ `custom: «мумія вдарилась у стіну N разів»` → ТО `disappear_a`, `respawn(mummy, start)`.
- Мумія: `chase-player` з різною «уважністю» — тип з низьким стеженням зупиняється й роззирається; за типом різні швидкість ходьби, швидкість на сходах і вміння стрибати.
- КОЛИ `enter(bick, trigger_spot)` → ТО `spawn_at(growing_wall, ceiling)` — стіна росте вниз.
- КОЛИ `contact(growing_wall, bick)` → ТО `lose`; КОЛИ `contact(growing_wall, mummy)` → ТО нічого.
- КОЛИ `enter(a, revolving_door)` → ЯКЩО `facing(a, pass_side)` і `custom: «a — Бік»` → ТО `move(a, dir)`, `custom: «сторони дверей міняються»`; інакше `block`.
- КОЛИ `contact(bick, jewel)` → ТО `pickup`, `counter(jewels_left, -1)`.
- КОЛИ `counter(jewels_left, ==, 0)` → ТО `spawn(exit_doors)`, `custom: «обертові двері зникають»`.
- КОЛИ `input(fire)` → ЯКЩО `custom: «Бік стрибає під перемикачем»` → ТО `custom: «двері відчиняються»`.
- КОЛИ `enter(bick, door_forward)` → ТО `win`, `window(map-window)`, `next_level`; КОЛИ `enter(bick, door_back)` → ТО `custom: «попередня стадія»`.
- КОЛИ `input(f2)` → ТО `lives(-1)`, `restart` — вихід з нерозвʼязного стану (засипаний шлях, бракує кирок).
- Перемога: усі коштовності + двері вперед. Поразка: мумія, ростуча стіна → життя −1; 0 життів — кінець (продовжень у картриджі нема).

## Керування і ввід
- Курсор: вліво/вправо — рух; діагоналі — сходи (порт: вгору/вниз).
- Кнопка Shot: старт гри; з предметом — застосувати (копати / кинути); з порожніми руками — стрибок (з напрямком — дугою).
- У повітрі й на сходах кинути чи копати не можна.
- F1 — пауза; F2 — самогубство (рестарт стадії за життя).
- FD-версія: пароль кожні 15 стадій.

## Вікна, меню, HUD
- `splash-screen` / заставка Konami → титульний екран (старт кнопкою Shot).
- `game-screen` — поле (1 або 2 екрани зі скролом) + `status-panel`: очки, життя, номер стадії (?).
- `map-window` — мапа пірамід після проходження стадії, показує наступну піраміду.
- `level-password` — лише FD-версія (кожні 15 стадій).
- `editor-window` — лише FD-версія (редактор стадій).
- `pause-menu` — F1, без пунктів (?).
- `end-screen` / game over → `leaderboard` (рекорд) (?).
- Переходи: титул → game-screen → (двері вперед) map-window → наступна стадія; (смерть) та сама стадія.

## Фічі поза полем
- `levels-sequential`: картридж — 15 стадій; FD-версія — 60 стадій.
- `level-editor` — лише FD-версія (запланована в 1985, вийшла 1988 у Konami Game Collection Vol. 1).
- `level-password` (FD) — кожні 15 стадій.
- `pause`, `restart-level` (F2 ціною життя).
- Рекорд очок зберігається в сесії (?).

## Варіації й родичі
- Предок ідеї: [lode-runner](lode-runner.md) — збір, вороги, копання; тут копання витратне, а не нескінченне.
- Наступник: [kings-valley-2](kings-valley-2.md) (1988) — 6 інструментів з різною формою ями, бумеранг, нові вороги, зникомі драбини/підлога, редактор у картриджі.
- Родичі: [solomons-key](solomons-key.md), [toki-tori](toki-tori.md) (обмежені інструменти), [lode-runner-the-legend-returns](lode-runner-the-legend-returns.md) (один пристрій у руці), Spelunker.
- Осі: **скільки разів копати** (∞ / кирка на поле / запас на рівень); **що дає предмет у руці** (нічого / забирає стрибок / забирає швидкість); **як вороги відрізняються** (один тип / таблиця параметрів за кольором).

## Цікавинки для курсу
- Таблиця поведінки ворогів «колір → стеження, роззирання, швидкість, сходи, стрибок»: один клас мумії, 5 конфігурацій — 🥉.
- Предмет у руці блокує стрибок; кнопка дії контекстна — 📎.
- Кирка як ресурс поля: яма 2×1 + шматок стіни; нерозвʼязні стани від помилки — 🥉 (детектор нерозвʼязності — 🥇).
- Меч-снаряд, що лежить там, де впав, і повертається у гру — 📎.
- Ростуча стіна: тригер-точка спавнить смертельну стіну, яку лише прокопати — 📎.
- Обертові двері: одностороння клітина, що міняє бік після проходу і не пускає ворогів — 📎.
- Два виходи «назад / вперед» з відчиненням стрибком під перемикач — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `collect-all` · `reach-exit` · `touch-death` · `environment-death` (стіна) · `player-death` · `chase-player` · `speed-per-type` · `respawn` · `spawn-points` · `dig-terrain` · `destructible-blocks` · `cell-transform` · `impassable-cells` · `one-way-cell` (обертові двері) · `button-toggle` (перемикач дверей) · `projectile-shot` (меч) · `temporary-modes` (мумія прибрана на час) · `inventory-items` · `inventory-limit` (1) · `restart-level` · `sequential-levels` · `map-window` · `level-password` · `in-game-editor` (FD) · `game-pause` · `unsolvable-states` · `player-camera` (скрол парних стадій).
- **Нема** → пропозиції карток:
  - `+stairs-diagonal` «Діагональні сходи» · entities/move · 📎.
  - `+jump-fixed-height` «Стрибок на N клітин угору/дугою» · entities/move · 📎.
  - `+single-use-tool` «Одноразовий інструмент у руці» · entities/state · 📎.
  - `+item-blocks-jump` «Предмет у руках забирає здатність» · entities/state · 🌱.
  - `+growing-wall` «Стіна росте зі стелі після тригера» · entities/spawn · 📎.
  - `+enemy-behavior-table` «Вороги одного класу з таблицею параметрів» · entities/move · 🥉 · слоти {tracking, speed, stairs, jumps}.
  - `+enemy-reset-on-bumps` «Ворог після N ударів у стіну повертається на старт» · entities/move · 🌱.
  - `+exit-choice-back-forward` «Двоє дверей: назад і вперед» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:dig(cell, shape)` — прибрати блоки формою (2×1 униз + стіна поруч).
- `+effect:jump(height)` — стрибок на N клітин (прямо / дугою).
- `+cond:hands_empty(a)` — у руках нічого (умова стрибка); короткий запис `not has(a, item)`.
- `+cond:on_stairs(a)` — стоїть на сходах (заборона дій); поки — `cell(here, stairs)`.
- `+trigger:bump_count(a, n)` — сутність N разів уперлась у перешкоду.
- `+role:stairs` — діагональні сходи (або `terrain` з прапорцем).
- `+feature:suicide-restart` — клавіша «здатися» ціною життя, коли рівень зіпсовано (F2; Ctrl-A у Lode Runner).
- `+card:enemy-behavior-table` — див. вище.

## Джерела
- ⭐ [Wikipedia JA: 王家の谷 (ゲーム)](https://ja.wikipedia.org/wiki/王家の谷_(ゲーム)) — керування (F1/F2, діагоналі), кирка 2×1 + стіна, меч, заборона стрибка з предметом, 5 мумій з таблицею, перезапуск мумій після ударів у стіну, ростуча стіна, обертові двері, двоє дверей і перемикач, 15/60 стадій, паролі й редактор FD.
- [Wikipedia EN: King's Valley](https://en.wikipedia.org/wiki/King%27s_Valley) — огляд, двері відчиняються після збору, Konami Game Collection Vol. 1, порт Retro Works.
- [Everygamegoing: King's Valley](https://everygamegoing.com/larticle/kings-valley/86244) — рецензія порту: стрибок на 2 блоки чи через мумію, одна дія за раз, кирка одноразова, односторонні двері, рестарт рівня.
- YouTube: пошук «King's Valley MSX gameplay».

## Непевне
- (?) Таблиця очок і стартова кількість життів — у джерелах нема.
- (?) Скільки ударів у стіну перезапускає мумію і скільки триває «смерть» мумії від меча.
- (?) Як саме відчиняються двері (стрибок під перемикачем — з JA-статті; EN-рецензія каже «switch to open the doorway»).
- (?) Чи мумія падає в яму й гине / застрягає (рецензія: «can be tricked into falling down holes») — механіка ями для мумій не описана.
- (?) Чи редактор FD-версії зберігає стадії на диск — лише «є редактор».
