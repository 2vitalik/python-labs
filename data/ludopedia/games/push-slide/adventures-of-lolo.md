---
title: Adventures of Lolo (Eggerland)
slug: adventures-of-lolo
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1989
platforms: [NES, Game Boy, MSX (Eggerland), Virtual Console, Nintendo Switch Online]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Adventures_of_Lolo", best: true, note: "ціль кімнати, яйця, вороги, історія Eggerland"}
  - {kind: other, url: "https://www.video-games-museum.com/en/faqs/Nes/7241-Adventures-of-Lolo-2.pdf", note: "FAQ Lolo 2 (Shibu_Jason, 2011): усі вороги, тип підлоги, предмети, напівклітини, респавн"}
  - {kind: fandom, url: "https://strategywiki.org/wiki/Adventures_of_Lolo", note: "StrategyWiki: проходження кімнат"}
  - {kind: fandom, url: "https://strategywiki.org/wiki/Adventures_of_Lolo_2/Gameplay", note: "StrategyWiki: механіки Lolo 2"}
  - {kind: other, url: "https://www.giantbomb.com/games/3030-5026/", note: "Giant Bomb: опис ворогів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=adventures+of+lolo+gameplay", note: "пошук; геймплей NES"}
stage: v1
coverage: 70
mechanics: [move-4dir, push-object, impassable-cells, collect-all, reach-exit, item-pickup, projectile-shot, touch-death, environment-death, respawn, spawn-points, timed-despawn, cell-transform, floor-types, speed-per-type, chase-greedy, enemy-patrol, inventory-items, sequential-levels, player-death, +line-of-sight-attack, +wake-on-event, +enemy-to-object, +one-way-cell, +half-cell-move]
proposes: ["+trigger:line_of_sight", "+trigger:counter", "+trigger:input", "+cond:has", "+cond:state", "+effect:set_state", "+effect:transform", "+effect:respawn", "+effect:set_cell", "+effect:lives", "+effect:speed", "+role:terrain", "+role:hazard", "+role:projectile", "+role:gate", "+role:container", "+trigger:sleep_on_contact", "+ui:shots-counter", "+window:level-password", "+feature:give-up-restart", "+axis:grid-resolution"]
author: opus
date: 2026-11-02
---

# Adventures of Lolo — збери всі серця, сховавшись від поглядів за блоками, і забери скарб

## Суть
Lolo ходить однокімнатним пазлом, збирає всі Heart Framer-и, щоб відкрити скриню, і бере з неї коштовність — тоді всі вороги зникають і відчиняються двері. Ядро — **Sokoban під вогнем**: зелені блоки (Emerald Framer) штовхаються, але головна їхня роль — щит від ворогів, що вбивають, щойно Lolo опиниться з ними на одній лінії. Друга опора — постріли: ворог стає яйцем, яке можна штовхати, ставити як щит або пустити по воді як пліт. Рівні — переважно детерміновані головоломки в реальному часі, а не аркада.

## Поле і час
- Одна кімната на екран, квадратна сітка (~11×11 клітин усередині рамки (?)); двері вгорі рамки. Усе видно, камера статична.
- Шари: підлога (звичайна, трава, пісок, вода, лава, міст, стрілка) + обʼєкти (блоки, дерева, скелі, серця, скриня, вороги, яйця).
- Real-time: вороги рухаються своїм темпом, яйце вилуплюється за таймером, яйце на воді тоне за таймером. Lolo й обʼєкти рухаються **напівклітинами** — ворог, перекритий наполовину, перекритий повністю; це легальний прийом розвʼязання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Lolo | player | життя; постріли; предмет-сила | рух 4 напрямки напівклітинами; штовхає блоки/яйця; стріляє вперед |
| Emerald Framer (блок) | object | — | штовхається, не тягнеться; блокує ворогів і всі постріли — головний щит |
| Heart Framer (серце) | pickup | дає 0 або 2 постріли | зібрати всі → скриня відкривається |
| Скриня (Treasure) | container | closed / open | відкрита — показує коштовність; по ній можна ходити |
| Коштовність (Jewel) | pickup | — | взяти → усі вороги зникають, двері відчиняються |
| Двері / сходи | static | closed / open | вихід у наступну кімнату; в останній кімнаті поверху — сходи |
| Постріл Lolo (magic shot) | projectile | — | летить прямо; ворог → яйце; яйце → ворог вилітає з екрана |
| Яйце | object | таймер вилуплення | штовхається як блок; щит; на воді — пліт, що тоне; вилуплюється в того самого ворога |
| Дерево | static | — | блокує Lolo, ворогів і постріли Lolo, але **не** постріли ворогів |
| Скеля (rock) | static | — | блокує все, включно з пострілами ворогів; молот ламає |
| Вода | terrain | — | непрохідна; яйце у воду → пліт |
| Лава | terrain | — | як вода, але яйце не заходить; міст на лаві згорає за час |
| Міст | terrain | — | прохідна підлога над водою для всіх |
| Трава | terrain | — | для Lolo підлога; частина ворогів не заходить |
| Пісок | terrain | — | сповільнює Lolo (ворогів — ні) |
| Стрілка (Arrow Block / one-way) | terrain | напрям | прохід лише за стрілкою або збоку; проти стрілки — `block` |
| Snakey | enemy | — | стоїть, нешкідливий; живий щит і «яйце-пліт» |
| Medusa | enemy | не рухається | побачила Lolo на прямій (4 напрямки) без перешкоди → миттєвий постріл, смерть |
| Don Medusa | enemy | вісь патруля | як Medusa, але ходить туди-сюди по одній лінії |
| Gol | enemy | напрям погляду | спить до останнього серця; потім пускає вогонь, коли Lolo попереду |
| Skull | enemy | — | спить до останнього серця; потім швидко женеться, смерть при дотику |
| Alma | enemy | — | бігає/котиться, женеться за Lolo, смерть при дотику |
| Leeper | enemy | — | стрибає; торкнувся Lolo → засинає назавжди і стає нерухомою перешкодою |
| Rocky | enemy | — | повільний, прискорюється на одній лінії з Lolo; не вбиває, а штовхає/запирає |
| Сила (Hammer · Bridge · Arrow) | pickup | ціна в серцях | після N сердець — одноразова дія: розбити скелю / покласти міст / повернути стрілку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(lolo, dir)` (на піску — `speed(lolo, ×k)`).
- КОЛИ `contact(lolo, framer|egg)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`. Тягнути не можна — блок у куті застряг.
- КОЛИ `contact(lolo, heart)` → ТО `pickup`, `counter(hearts_left, -1)`; ЯКЩО `custom: «серце зі зарядом»` → ТО `counter(shots, +2)`.
- КОЛИ `counter(hearts_left, ==, 0)` → ТО `set_state(chest, open)`, `set_state(gol|skull, awake)`.
- КОЛИ `contact(lolo, jewel)` → ТО `disappear_b`, `custom: «усі вороги зникають у диму»`, `set_state(door, open)` (або `spawn(staircase)`).
- КОЛИ `contact(lolo, door_open|staircase)` → ТО `next_level`.
- КОЛИ `input(fire)` → ЯКЩО `has(lolo, shots)` → ТО `spawn(shot)` вперед, `counter(shots, -1)`.
- КОЛИ `contact(shot, enemy)` → ЯКЩО `custom: «ворог не імунний»` → ТО `transform(egg)`, `timer(hatch)`.
- КОЛИ `timer(hatch)` → ТО `transform(enemy_same_kind)` на місці яйця.
- КОЛИ `contact(shot, egg)` → ТО `disappear_b`, через час `respawn(enemy, start_cell)` з маркером «квадрат» перед появою.
- КОЛИ `respawn(enemy)` → ЯКЩО `occupied(start_cell, framer)` → ТО `custom: «ворог зникає назавжди або зʼявляється деінде»` (respawn relocation, Lolo 2).
- КОЛИ `line_of_sight(medusa|don_medusa, lolo)` → ТО `lose` (миттєвий постріл); перешкода — блок, яйце, інший ворог, скеля; дерево **не** захищає. Напівперекриття блокує повністю.
- КОЛИ `line_of_sight(gol, lolo)` → ЯКЩО `state(gol, awake)` і `facing(gol, lolo)` → ТО `spawn(fireball)`; КОЛИ `contact(fireball, lolo)` → ТО `lose`.
- КОЛИ `state_on(skull, awake)` → ТО `custom: «chase-greedy, швидко»`; КОЛИ `contact(skull|alma, lolo)` → ТО `lose`.
- КОЛИ `contact(leeper, lolo)` → ТО `set_state(leeper, asleep)` назавжди, далі `block` для всіх.
- КОЛИ `in_range(rocky, lolo)` на одній лінії → ТО `speed(rocky, +n)`; `contact(rocky, lolo)` → `push` Lolo (не смерть).
- КОЛИ `enter(egg, water)` → ТО `custom: «пліт»`; Lolo може стати на нього; яйце пливе за течією (?) і через час тоне → ЯКЩО `occupied(egg, lolo)` → ТО `lose`. КОЛИ `enter(egg, lava)` → ТО `block`.
- КОЛИ `enter(lolo, arrow_cell)` → ЯКЩО `moving(lolo, against_arrow)` → ТО `block`.
- КОЛИ `input(use)` → ЯКЩО `has(lolo, power_item)` і `counter(hearts, >=, price)` → ТО молот `set_cell(rock → floor)` / міст `set_cell(water → bridge)` / стрілка `rotate(arrow, 90)`.
- КОЛИ `input(give_up)` → ТО `lives(-1)`, `restart` кімнати.
- Перемога: взяти коштовність і вийти в двері; 50 кімнат (10 поверхів по 5). · Поразка: смерть → `lives(-1)`, кімната заново; 0 життів → `game_over`. · Рахунку немає (?), є життя і паролі.

## Керування і ввід
- Хрестовина — рух; A — постріл (якщо є заряди) або застосування предмета-сили; Select — здатися (життя за рестарт кімнати; потрібно, коли зробив глухий кут); Start — старт.
- Без курсора, без undo: єдиний «відкат» — Select.

## Вікна, меню, HUD
- `splash-screen` / титул; якщо чекати — демо-навчання (Lolo 2) як `tutorial-window`.
- `main-menu`: Start / Continue (пароль) → `level-password`.
- `game-screen`: кімната + права панель — `lives`, лічильник пострілів (`+ui:shots-counter`), панель «Power» з іконками доступних сил і ціною в серцях (?).
- `end-screen`: поверх пройдено → перехід сходами; `game-over-continue` після останнього життя з паролем (?).
- `dialogue-window`: катсцени початку/кінця, бос Great Devil у Lolo 2.
- Переходи: титул → (пароль?) → кімната 1-1 → двері → наступна кімната → сходи → новий поверх.

## Фічі поза полем
- `levels-sequential` (поверхи по 5 кімнат) + `level-password` (паролі продовження; у Lolo 2 секретні PROA–PROD відкривають 4 Pro-рівні).
- `restart-level` ціною життя (Select); нема undo/підказок/збереження, крім паролів.
- `idle-animation`: Lolo засинає, якщо гравець довго стоїть (Lolo 2).
- Повтори на Virtual Console/Switch Online додають suspend-точки платформи (не механіка гри).

## Варіації й родичі
- Серія Eggerland (HAL, MSX/Famicom Disk) → Adventures of Lolo 1–3 (NES), Lolo (GB); NES Lolo 1 зібрана з пазлів Eggerland: Meikyū no Fukkatsu і Sōzō e no Tabidachi.
- Lolo 2: лава, respawn relocation, бос; Lolo 3: другий персонаж Lala (?).
- Осі варіацій: **блок як щит** (Lolo) vs **блок як вантаж** (Sokoban); **ворог → обʼєкт** (яйце — тимчасова трансформація ворога у блок/пліт); **атака ворога**: дотик / лінія погляду / вогонь вперед / «приспати» / штовхати.
- Родичі: Sokoban (штовхання), Chip's Challenge (дошка з багатьма ворогами), Kickle Cubicle (вороги → крижані кубики), DROD.

## Цікавинки для курсу
- Ворог із лінією погляду (Medusa): BFS/промінь по рядку і стовпцю до першої перешкоди, різні типи перешкод для різних снарядів — 🥉.
- Ворог → яйце → обʼєкт з таймером → знов ворог (трансформація з поверненням і новими властивостями: штовхається, плаває) — 🥈.
- «Пробудження» ворогів подією (останнє серце) — Gol/Skull спершу пасивні — 📎.
- Respawn relocation: ворог повертається на точку старту, а блок на ній його знищує або переносить — 📎.
- Напівклітинний рух (сітка для логіки, хід — пів клітини): часткове перекриття — 🥇 (зміна моделі поля).
- Пліт-яйце на воді з таймером тонення й течією — 🥉.
- Предмети-сили «після N сердець» (молот, міст, стрілка) — 📎.

## Мапа на каталог
- Є: `move-4dir`; `push-object` ↔ блоки/яйця; `impassable-cells` ↔ дерева, скелі, вода; `collect-all` ↔ усі серця; `reach-exit` ↔ двері; `item-pickup` ↔ серця, коштовність; `projectile-shot` ↔ постріл Lolo, вогонь Gol; `touch-death` ↔ Skull/Alma; `environment-death` ↔ яйце тоне; `respawn` + `spawn-points` ↔ ворог повертається на старт; `timed-despawn` ↔ міст на лаві, яйце тоне; `cell-transform` ↔ молот/міст змінюють клітину; `floor-types` ↔ пісок, трава, вода, лава, стрілки; `speed-per-type` ↔ пісок, Rocky; `chase-greedy` ↔ Skull/Alma; `enemy-patrol` ↔ Don Medusa; `inventory-items` ↔ сили; `sequential-levels`; `player-death` ↔ життя.
- **Нема** → пропозиції карток:
  - `+line-of-sight-attack` «Атака по лінії погляду» · entities/combat · 🥉 · слот {blockers: list} — Medusa, Gol.
  - `+wake-on-event` «Ворог прокидається від події» · entities/state · 📎 · слот {event} — Skull/Gol після останнього серця.
  - `+enemy-to-object` «Ворог стає обʼєктом на час» · entities/interact · 🥈 · слот {duration} — яйце.
  - `+one-way-cell` «Клітина одностороннього проходу» · entities/legality · 🌱 · слот {dir}.
  - `+half-cell-move` «Рух напівклітинами» · entities/move · 🥇.

## Пропозиції до словників
- `+trigger:line_of_sight` — Medusa/Don Medusa/Gol стріляють, коли бачать Lolo.
- `+trigger:counter` — останнє серце зібрано (`hearts_left == 0`) відкриває скриню і будить ворогів; `+trigger:input` — постріл/предмет/здатися.
- `+cond:has` — є заряди/предмет; `+cond:state` — Gol/Skull прокинувся.
- `+effect:set_state` (скриня, двері, сон Leeper), `+effect:transform` (ворог ↔ яйце), `+effect:respawn` (повернення на точку старту), `+effect:set_cell` (молот, міст), `+effect:lives` (здатися), `+effect:speed` (пісок, Rocky).
- `+role:terrain` (вода, лава, пісок, трава, стрілки), `+role:hazard` (?) для лави, `+role:projectile` (постріл, вогонь, голки), `+role:gate` (двері), `+role:container` (скриня).
- `+trigger:sleep_on_contact` — спец-випадок Leeper: дотик робить ворога перешкодою (можна виразити `contact` + `set_state`, тож — лише якщо повториться).
- `+ui:shots-counter` — кількість зарядів у HUD.
- `+window:level-password` — продовження паролем.
- `+feature:give-up-restart` — рестарт кімнати ціною життя як заміна undo.
- `+axis:grid-resolution` — логічна сітка клітин vs крок руху пів клітини.

## Джерела
- ⭐ [Wikipedia: Adventures of Lolo](https://en.wikipedia.org/wiki/Adventures_of_Lolo) — ціль кімнати, яйця (пліт, повторний постріл), сили, 50 кімнат, звʼязок з Eggerland.
- [FAQ Lolo 2 (PDF)](https://www.video-games-museum.com/en/faqs/Nes/7241-Adventures-of-Lolo-2.pdf) — повні описи ворогів (Snakey, Gol, Leeper, Alma, Medusa, Don Medusa, Skull, Rocky), тип підлоги, предмети, напівклітини, respawn relocation, керування.
- [StrategyWiki: Adventures of Lolo](https://strategywiki.org/wiki/Adventures_of_Lolo) — проходження (сторінка з пошуку, сам вміст закритий для бота).
- [StrategyWiki: Lolo 2 Gameplay](https://strategywiki.org/wiki/Adventures_of_Lolo_2/Gameplay) — причини смерті, Heart/Emerald Framer-и, яйця.
- [Giant Bomb](https://www.giantbomb.com/games/3030-5026/) — Don Medusa, Skull, Leeper (зі сніпетів пошуку).
- YouTube: пошук «adventures of lolo gameplay».

## Непевне
- (?) Розмір кімнати 11×11 — за памʼяттю, не перевірено.
- (?) Хто з ворогів імунний до пострілів (Wikipedia: «деякі»); за памʼяттю Medusa/Don Medusa/Rocky — не підтверджено.
- (?) HUD-панель «Power» і точні ціни сил у серцях; яйце пливе «за течією» — FAQ каже «по визначеному шляху», механіку течії не уточнено.
- (?) Рахунок/очки — в описах не згадано; Lolo 3 з Lala — за памʼяттю.
- Основні описи ворогів — з FAQ Lolo 2; поведінка в Lolo 1 може незначно відрізнятись.
- Пошуковий бюджет сесії вичерпався під час дослідження Lolo: StrategyWiki і Giant Bomb повертали 403 — опис ґрунтується на Wikipedia + FAQ.
