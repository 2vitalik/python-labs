---
title: Pokémon Duel (Pokémon Comaster)
slug: pokemon-duel
aka: [Pokémon Comaster, ポケモンコマスター, Покемон Дуель]
family: chess-abstract
also: [tactics]
klass: figure
axes:
  field: graph
  time: turn
  opponent: online
  info: full
  random: runtime
  goal: race
year: 2016
platforms: [Android, iOS]
links:
  - {kind: other, url: "https://www.pokemon.com/us/strategy/prime-yourself-for-pokemon-duels", best: true, note: "офіційний розбір правил: 26 точок + 2 цілі, маршрути, входи в кутах, ПЦ на 2, оточення, таблиця кольорів, стани, пластини"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Duel", note: "огляд: кольори атак, ПЦ, оточення, пластини, три умови перемоги, 5 хв, гача, рейтинг, закриття 2019"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ポケモンコマスター", note: "поле-сугороку, хід: вивести з лави або походити на MP, рулетка, друга перемога через блок входу"}
  - {kind: other, url: "https://www.serebii.net/duel/mechanics.shtml", note: "Serebii: портали, 300 ходів, кольори, стани, рівні, злиття, еволюція, Mega, Z-атаки"}
  - {kind: other, url: "https://www.serebii.net/duel/plates.shtml", note: "Serebii: пластини, рідкість, вартість ≤ 8 на колоду, раз на дуель"}
  - {kind: official, url: "https://www.pokemon.com/us/pokemon-video-games/pokemon-duel", note: "сторінка гри: Data Disk, пластини на початку ходу, Training Center, League Match"}
  - {kind: other, url: "https://player.one/pokemon-duel-beginners-guide-how-play-best-pokemon-tips-wins-evolution-fusion-580892", note: "гайд: меню, Deck Check, еволюція в бою, злиття, бустери"}
  - {kind: other, url: "https://www.appspy.com/features/pokemon-duel-guide-part-one-the-basics/", note: "гайд: оточення на точці з двома сусідами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pokemon+Duel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [reach-exit, no-moves-left, status-effects, respawn, online-multiplayer, rating-system, ai-opponent, move-timer, turn-enforcement, cell-click, selection-highlight, reachable-highlight, pocket, shop-window, shop-catalog, map-window, codex-window, tutorial-window, game-screen, main-menu, end-screen, save-progress, +graph-board, +spin-wheel-battle, +color-priority-battle, +surround-ko, +bench-and-board, +entry-point-spawn, +ko-queue-revive, +plate-deck, +deck-cost-limit, +evolve-on-win, +timed-transform, +z-move-gauge, +gacha-boosters, +fusion-levelling, +auto-move, +deck-check, +turn-limit]
proposes: ["+trigger:battle", "+effect:spin", "+effect:send_to", "+cond:surrounded", "+cond:color_beats", "+ui:data-disk", "+ui:pc-slots", "+ui:z-gauge", "+ui:plate-bar", "+window:deck-edit", "+window:deck-check", "+window:battle-overlay", "+window:booster-open", "+feature:gacha", "+feature:fusion", "+feature:auto-play", "+card:spin-wheel-battle", "+card:color-priority-battle", "+card:surround-ko", "+card:ko-queue-revive", "+card:deck-cost-limit"]
author: opus
date: 2026-11-09
---

# Pokémon Duel — фігурки покемонів біжать графом до чужої бази; сусіди бʼються рулетками атак, а оточеного з усіх боків знімають без бою

## Суть
Мобільна цифрова настілка (HEROZ / The Pokémon Company) за мотивами Pokémon Trading Figure Game (2007): у кожного 6 фігурок і до 6 «пластин»-карт. Хід — вивести фігуру з лави через свій вхід або пройти однією фігурою до MP кроків маршрутами поля; мета — поставити фігуру на ціль суперника. Сусідні ворожі фігури можуть битися: крутяться обидва Data Disk, і результат вирішує колір сектора (білий / золотий — шкода, фіолетовий — ефект, синій — захист, червоний — промах). Переможений іде в Покемон-центр, а фігура, всі сусідні точки якої зайняли вороги, нокаутується без бою — гра схожа на го й шахи з кубиком усередині.

## Поле і час
- Поле — граф: **26 точок + 2 цілі**, точки зʼєднані маршрутами; ходити можна лише маршрутами (`field: graph`). У частини точок лише 2 сусіди — там оточити легко.
- У кожної сторони 2 точки входу в кутах поля; зайнятий (будь-ким) вхід блокує виведення з лави. Ціль — точка на протилежному боці.
- Поза полем у кожного: лава (6 фігур на старті), Покемон-центр (ПЦ, ≤ 2 фігури), зона «вилучених до кінця дуелі» (прокляття), рука пластин.
- Покроково, один хід = одна фігура; хто перший — випадково. Онлайн — 5 хвилин на гравця (Wikipedia), ліміт 300 ходів на матч (Serebii).
- Випадковість лише в бою (рулетки) і в черговості.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура-покемон | piece | MP 1–3, тип, рідкість C/UC/R/EX/UX, здібність, Data Disk | ходить до MP точок маршрутами; бʼється із сусідом; може еволюціонувати |
| Data Disk (диск атак) | — | сектори різного розміру й кольору | крутиться в бою; сектор = атака; рівні й злиття збільшують сектори |
| Точка поля | terrain | 1 фігура | вузол графа; сусіди — за маршрутами |
| Точка входу | zone | 2 на сторону, у кутах | сюди ставлять з лави (коштує 1 MP); зайнята — вхід закрито |
| Ціль (база) | zone | 1 на сторону | ворожа фігура на ній — перемога її власника |
| Лава | supply | старт: 6 фігур | звідси виводять фігури |
| Покемон-центр | zone | ≤ 2 фігури, черга | нокаутовані; не ходять; третя виштовхує найстаршу на лаву |
| Вилучені | zone | — | прокляті (Curse) після нокауту — до кінця дуелі |
| Пластина | supply | вартість, рідкість EX/R/UC/C; ≤ 6 у колоді, сума вартостей ≤ 8 | одноразова карта на початку ходу: обмін місцями, +шкода, лікування, повернення з ПЦ…; багато закінчують хід |
| Мега-камінь, Z-атака | supply | Mega — 7 ходів, 1 раз за гру; Z — шкала | тимчасове перетворення / сильна атака за повну шкалу |

Сектори диска й таблиця кольорів (офіційна):
| Колір | Що це | Перемагає | Програє |
|---|---|---|---|
| Білий | шкода числом | білий / золотий з меншою шкодою; червоний | фіолетовий, синій |
| Золотий | пріоритетна шкода | фіолетовий; білий / золотий з меншою шкодою; червоний | синій |
| Фіолетовий | ефект, зірки ★ | білий; фіолетовий з меншими ★; червоний | золотий, синій |
| Синій | захист (Protect, Dodge) | усі інші | — (синій × синій — нічия) |
| Червоний | промах (Miss) | — | усі (червоний × червоний — нічия) |

Стани (від фіолетових атак і пластин):
| Стан | Ефект |
|---|---|
| Poison / Noxious | шкода атак −20 / −40 |
| Burn | шкода −10, найменша атака стає промахом |
| Paralysis | найменша атака стає промахом |
| Confusion | спрацьовує наступна атака за годинниковою від тієї, де зупинився диск |
| Sleep / Frozen | не бʼється (джерела розходяться, чи може ходити — див. «Непевне»); Frozen знімається після будь-якого бою |
| Wait N | не ходить і не діє N ходів (після ПЦ, Z-атак) |
| MP −1 | MP фігури −1 |
| Curse | після нокауту — вилучена до кінця дуелі |

## Правила (КОЛИ → ЯКЩО → ТО)
Старт і хід:
- КОЛИ `game_start` → ТО `custom: «6 фігур на лаві кожного; першого гравця обрано випадково»`; КОЛИ `custom: «перша фігура, що ходить у дуелі»` → ТО `custom: «її MP −1 на цей хід»`.
- КОЛИ `input(enter(fig))` → ЯКЩО `turn_of(side)` and `custom: «fig на лаві»` and `free(own_entry)` → ТО `place(side, fig)` на вхід, `custom: «вихід коштує 1 MP; решта MP — далі маршрутом»`; інакше `block`.
- КОЛИ `input(move(fig, to))` → ЯКЩО `turn_of(side)` and `path_exists(fig, to)` and `custom: «довжина шляху ≤ MP, лише по маршрутах, через вільні точки»` → ТО `move(fig, to)`.
- КОЛИ `input(move(fig))` → ЯКЩО `state(fig, wait)` або `custom: «fig у ПЦ»` → ТО `block`.
- Один хід — одна фігура: вивести / походити / почати бій / використати пластину на початку ходу.

Бій:
- КОЛИ `input(battle(a, b))` (кандидат `+trigger:battle`) → ЯКЩО `turn_of(side)` and `in_range(a, b, 1)` (сусіди за маршрутом) and not `state(a, sleep|frozen)` → ТО `custom: «обидва диски крутяться»` (кандидат `+effect:spin`).
- КОЛИ `custom: «диски зупинились»` → ЯКЩО `custom: «колір A бʼє колір B за таблицею»` (кандидат `+cond:color_beats`) → ТО виграє A; ЯКЩО кольори білий/золотий з обох боків → більша шкода; фіолетовий × фіолетовий → більше ★.
- КОЛИ `custom: «переміг білий або золотий»` → ТО `custom: «переможений нокаутований — у ПЦ»` (кандидат `+effect:send_to(pc)`).
- КОЛИ `custom: «переміг фіолетовий»` → ТО `set_state(loser, status)` або `move(loser, to)` (ефект атаки: стан, зсув на іншу точку).
- КОЛИ `custom: «переміг синій»` → ТО `custom: «зазвичай нічого — бій скасовано»`.
- КОЛИ `custom: «рівна шкода / рівні ★ / синій × синій / червоний × червоний»` → ТО `custom: «нічия, обидві лишаються»`.
- КОЛИ `custom: «бій завершено»` → ТО `end_turn`.
- КОЛИ `custom: «фігура перемогла в бою»` → ЯКЩО `custom: «у колоді є її еволюція»` → ТО `transform(fig, evolved)`, `custom: «+10 шкоди на атаках, +1 ★ на фіолетових»`.

Оточення:
- КОЛИ `after(move)` → ЯКЩО `custom: «усі точки, куди фігура могла б піти, зайняті ворожими»` (кандидат `+cond:surrounded`) → ТО `custom: «нокаут без бою — у ПЦ»` (`+effect:send_to(pc)`).
- Оточення рахується лише тим, що створив щойно зроблений хід; оточена фігура нокаутується до того, як встигне почати бій.

ПЦ, прокляття, стани:
- КОЛИ `custom: «фігура йде в ПЦ»` → ЯКЩО `count(pc, ==, 2)` → ТО `respawn(oldest, bench)`, `set_state(oldest, wait, 1)` (може ходити через хід).
- КОЛИ `died(fig)` → ЯКЩО `state(fig, curse)` → ТО `custom: «вилучено до кінця дуелі»`.
- КОЛИ `custom: «фігура потрапила в ПЦ»` → ТО `clear_state(fig, all)`.
- КОЛИ `input(touch(own_adjacent))` → ЯКЩО `state(fig, status)` → ТО `clear_state(fig, status)`, `end_turn` (свій сусід знімає майже всі стани).
- КОЛИ `state_on(fig, wait)` → ТО `stun(fig, n)`.

Пластини, Mega, Z:
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «пластина в руці ще не використана»` → ТО `use(side, plate)`; ЯКЩО `custom: «пластина з поміткою “хід закінчується”»` → `end_turn`.
- КОЛИ `custom: «зберегти колоду»` → ЯКЩО `custom: «фігур ≠ 6, пластин > 6 або сума вартостей пластин > 8»` → ТО `block`.
- КОЛИ `use(side, mega_plate)` → ЯКЩО `first_time` → ТО `transform(fig, mega)`, `set_state(fig, mega, 7)`; другий раз за гру — `block`.
- КОЛИ `counter(z_gauge, >=, max)` → ТО `custom: «Z-атака будь-якій своїй фігурі на полі; тип атаки — за типом покемона»`.

Кінець:
- КОЛИ `reach(fig, enemy_goal)` → ТО `win`.
- КОЛИ `no_moves(side)` → ТО `lose` («wait win» супернику; напр. входи заблоковані й на полі нема фігур).
- КОЛИ `custom: «час гравця вичерпано»` → ТО `lose`.
- КОЛИ `counter(turns, >=, 300)` → ТО `game_over` (результат — (?)).
- Перемога: фігура на ворожій цілі · суперник без ходу · його час вийшов · Рахунок: рейтинг Elo (загальний і місячний).

## Керування і ввід
- Тап по фігурі → підсвітка досяжних точок і доступних дій (бій, вихід з лави) → тап по точці / по ворогу.
- Бій: тап зупиняє диск (на результат не впливає — випадковий сектор); Double Chance та подібні пластини дають перекрутити.
- Пластини — тап по карті в руці на початку ходу, потім ціль.
- Auto: AI може ходити й обирати за гравця (і в бою, і на полі).
- Онлайн — шаховий годинник на 5 хвилин; хід суперника видно наживо.

## Вікна, меню, HUD
- `main-menu` (головний екран): Дуель → `mode-select` (League Match, Training Center, Quest, Friend Duel, події Carnival / Gym) · Decks → `deck-edit` (кандидат) · Fusion → `upgrade-window` · Shop → `shop-window` (геми, бустери, Player Pass) · Messages (нагороди) · щоденні місії.
- `map-window` — Quest на острові Carmonte (локації-вузли).
- `deck-check` (кандидат) — перед боєм: колода суперника проти твоєї.
- `game-screen`: граф поля з цілями й входами, обидві лави, `pc-slots` (кандидат), `plate-bar` — рука пластин (кандидат), `player-clock`, `turn-counter`, `z-gauge` (кандидат), `reachable-highlight`, кнопка Auto.
- `battle-overlay` (кандидат): два `data-disk` (кандидат), підсумок кольорів і шкоди, ефект.
- `end-screen`: перемога / поразка, рейтинг, нагорода-бустер.
- `booster-open` (кандидат): бустер відкривається через 6 годин або за перемоги.
- `codex-window` — Library: перегляд фігур (лишився після закриття сервісу).
- `tutorial-window` — Training Center як навчання.
- Переходи: main-menu → mode-select → deck-check → game-screen ⇄ battle-overlay → end-screen → booster-open.

## Фічі поза полем
- `online-multiplayer` + рейтинг Elo (загальний і місячний); постійне підключення обовʼязкове.
- Кампанія (Quest, Pokémon Figure World Championships на Carmonte) проти AI; Training Center зі сценарними колодами.
- Колекція: гача-бустери за геми (кандидат `+feature:gacha`), з 2019 — Player Pass; рідкість C → UX.
- Прокачка: рівні фігур (5, через Carmonite — до 10) дають очки на зміну розміру секторів; злиття (кандидат `+feature:fusion`) за монети; Chain Level — +1 до сили атаки за кожне злиття однакових.
- `ai-opponent-levels` — квест-суперники; `auto-play` (кандидат) — AI грає за тебе.
- Події, щоденні місії, магазин; 3 слоти колод на старті.
- Сервіс закрито 31.10.2019.

## Варіації й родичі
- Pokémon Trading Figure Game (2007) — фізичний оригінал з фігурками й дисками.
- Корпус: [onitama.md](onitama.md) і [jungle.md](jungle.md) — перемога дійти до бази суперника; [go.md](go.md) і [hive.md](hive.md) — оточення знімає / перемагає; [ataxx.md](ataxx.md) — граф-сусідство як ресурс.
- **Осі варіацій**:
  - **бій**: детермінований (шахи) · рулетки з ієрархією кольорів (Pokémon Duel) · кубики з HP (тактики);
  - **оточення**: нема · всі сусіди ворожі → нокаут (Pokémon Duel, го для групи) · оточення короля → перемога (Hive);
  - **повернення**: взяте назавжди (шахи) · черга ПЦ на 2 місця · дроп у руку (сьоґі);
  - **поле**: квадратна сітка · граф з точками різного степеня (тут: точки з 2 сусідами — пастки);
  - **мета**: мат · дійти до цілі · залишити без ходу.

## Цікавинки для курсу
- Поле-граф з маршрутами, рух ≤ MP через вільні вершини (BFS з обмеженням глибини) + підсвітка досяжних — 📎.
- Бій двома рулетками: зважений випадковий сектор + таблиця «колір × колір» з тай-брейками — 📎 (таблиця як дані).
- Оточення «усі сусіди ворожі» лише за щойно зробленим ходом, до бою — 🥉 (порядок перевірок).
- ПЦ-черга на 2 місця з виштовхуванням найстаршої + Wait — 🌱.
- Стани, що модифікують диск (промах найменшої атаки, −20, зсув за годинниковою) — 🥉.
- Колода з лімітом вартості пластин і одноразовими картами — 📎.
- AI з очікуванням бою (ймовірність перемоги за розмірами секторів) + пошук ходу — 🥇.

## Мапа на каталог
- Є: `reach-exit` ↔ фігура на ворожій цілі; `no-moves-left` ↔ «wait win»; `status-effects` ↔ отрута, сон, параліч…; `respawn` ↔ з ПЦ на лаву; `online-multiplayer`, `rating-system` ↔ League Match з Elo; `ai-opponent` ↔ квести й Auto; `move-timer` ↔ 5 хв; `reachable-highlight`, `selection-highlight`, `cell-click`; `pocket` ↔ лава/рука пластин; `shop-window`, `shop-catalog`, `map-window` (Carmonte), `codex-window` (Library), `tutorial-window`; `save-progress` ↔ колекція.
- **Нема** → пропозиції карток:
  - `+graph-board` «Поле-граф: вершини й маршрути замість клітин» · entities/move · 📎.
  - `+spin-wheel-battle` «Бій рулетками: сектор = атака, розмір = ймовірність» · entities/combat · 📎 · слоти {segments}.
  - `+color-priority-battle` «Таблиця кольорів атак з тай-брейком числом / зірками» · entities/combat · 🌱.
  - `+surround-ko` «Фігура з усіма сусідами-ворогами нокаутована без бою» · entities/combat · 🥉 — родич `+surround-win`.
  - `+bench-and-board`, `+entry-point-spawn` «Лава й вихід на поле лише через свої входи» · entities/spawn · 🌱.
  - `+ko-queue-revive` «Зона нокаутованих на N місць, найстарша повертається» · entities/death · 🌱.
  - `+plate-deck`, `+deck-cost-limit` «Одноразові карти з вартістю, ліміт суми» · game-logic/economy · 📎.
  - `+evolve-on-win`, `+timed-transform` (Mega 7 ходів), `+z-move-gauge`, `+gacha-boosters`, `+fusion-levelling`, `+auto-move`, `+deck-check`, `+turn-limit` — одним рядком у «Фічах».

## Пропозиції до словників
- `+trigger:battle(a, b)` — гравець почав бій двох сусідніх фігур.
- `+effect:spin(disk)` — випадковий сектор зваженого колеса; `+effect:send_to(a, zone)` — перемістити поза поле (ПЦ, вилучені).
- `+cond:surrounded(a)` — усі сусіди A зайняті ворожими (підтверджую з hnefatafl); `+cond:color_beats(a, b)` — колір атаки A бʼє колір B.
- `+ui:data-disk` — диск атак з секторами; `+ui:pc-slots` — два слоти ПЦ; `+ui:z-gauge` — шкала Z; `+ui:plate-bar` — рука пластин.
- `+window:deck-edit` · `+window:deck-check` · `+window:battle-overlay` · `+window:booster-open`.
- `+feature:gacha` — випадкові бустери; `+feature:fusion` — злиття фігур для досвіду; `+feature:auto-play` — AI грає за гравця.
- `+card:spin-wheel-battle` · `+card:color-priority-battle` · `+card:surround-ko` · `+card:ko-queue-revive` · `+card:deck-cost-limit` — див. «Мапа на каталог».

## Джерела
- ⭐ [Pokémon.com: Prime Yourself for Pokémon Duels](https://www.pokemon.com/us/strategy/prime-yourself-for-pokemon-duels) — 26 точок + 2 цілі, маршрути, входи в кутах (1 MP), MP −1 першої фігури, ПЦ на 2, оточення після руху, повна таблиця кольорів і нічиїх, стани, лікування сусідом, колода 6 + до 6 пластин.
- [Wikipedia: Pokémon Duel](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Duel) — кольори, ПЦ, оточення, три умови перемоги (ціль, час 5 хв, нема ходу), гача з 6-годинним відкриттям, Elo, дати, закриття.
- [Wikipedia JA: ポケモンコマスター](https://ja.wikipedia.org/wiki/ポケモンコマスター) — хід «вивести або походити на MP», рулетка, блок входу як шлях до перемоги, рідкості.
- [Serebii: механіки](https://www.serebii.net/duel/mechanics.shtml) — 2 портали, 300 ходів, стани, рівні й злиття, еволюція, Mega 7 ходів, Z-атаки; [Serebii: пластини](https://www.serebii.net/duel/plates.shtml) — список, вартість ≤ 8, раз на дуель.
- [Pokémon.com: сторінка гри](https://www.pokemon.com/us/pokemon-video-games/pokemon-duel) — режими, пластини на початку ходу.
- [Player.One: гайд](https://player.one/pokemon-duel-beginners-guide-how-play-best-pokemon-tips-wins-evolution-fusion-580892) — меню, Deck Check, еволюція в бою; [AppSpy: основи](https://www.appspy.com/features/pokemon-duel-guide-part-one-the-basics/) — оточення двома.
- YouTube: пошук «Pokemon Duel gameplay».

## Непевне
- (?) Sleep і Frozen: pokemon.com (через переказ) — сплячий може ходити, але не битися; Serebii й Player.One — сплячий не ходить і не бʼється, а заморожений ходить. Таблиця лишає це відкритим.
- (?) Синій проти золотого: офіційне «синій бʼє все»; Player.One пише «золотий бʼє синій» — узято офіційне.
- (?) Чи зараховується оточення **власної** фігури, що сама зайшла в оточення, і чи свої фігури блокують точку для оточення — джерела кажуть лише про ворожі.
- (?) Сума розмірів секторів диска (з памʼяті 96) і точна топологія 26 точок (які мають 2/3/4 сусіди) — не з відкритого джерела.
- (?) Результат матчу при ліміті 300 ходів; чи «блок входу + усі ворожі фігури з поля» (JA-вікі) — окрема перемога чи окремий випадок «нема ходу».
- (?) Ліміт 6 пластин (pokemon.com) поруч із лімітом вартості ≤ 8 (Serebii) — можливо, з різних версій гри.
- (?) Лікування «дотиком сусіда»: джерело каже «touching an adjacent Pokémon» — що це саме своя фігура і як саме «торкаються» (окрема дія чи підхід), тлумачу сам.
- (?) Чи можна в один хід і походити, і почати бій — з памʼяті так (бій після руху, тоді хід закінчується); джерела кажуть лише «на своєму ході, якщо сусіди».
