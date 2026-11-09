---
title: Summoner Wars
slug: summoner-wars
aka: [Summoner Wars Second Edition, Summoner Wars Master Set, Summoner Wars Mobile]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: state
year: 2009
platforms: [board, iOS, Android, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/summoner-wars/game-rules.php", best: true, note: "UltraBoardGames: правила 1-го видання — фази, призов біля своїх стін, магія-колода з убитих і скинутих, рух/атака по 3 юніти, кубики 3+, Vine Walls, перемога"}
  - {kind: other, url: "https://media.plaidhatgames.com/filer_public/7d/07/7d075572-2254-4248-bdb5-464ef4b97180/ph3600-rulebook-v1_2.pdf", note: "офіційний PDF правил 2-го видання v1.2: трек магії, ворота-споруди, кубики з символами, Cost of Inaction, Force, boost, ряд = 6 клітин, сторона = 4 ряди, побудова колоди"}
  - {kind: official, url: "https://www.plaidhatgames.com/games/summoner-wars/", note: "Plaid Hat Games: 2-ге видання, дизайнер Colby Dauch, 2 гравці, 45–60 хв, 24 фракції, онлайн-версія"}
  - {kind: play, url: "https://breakers-vs-goblins.plaidhatgames.com/", note: "Summoner Wars Online — браузерна версія 2-го видання"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Summoner_Wars", note: "Summoner Wars Mobile (Playdek, iOS 2012, Android 2014), 2-ге видання 2021"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Summoner+Wars+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, pocket, hot-seat, online-multiplayer, character-select, legal-move-highlight, +deck-draw, +draw-to-hand-size, +summon-adjacent, +wall-spawn-point, +magic-pile-from-kills, +discard-for-mana, +unit-action-limit, +orthogonal-only, +combat-dice-symbols, +leader-death-lose, +friendly-fire, +deck-out-no-reshuffle, +first-player-handicap, +faction-decks, +deck-building, +structure-building, +back-rows-zone, +cost-of-inaction, +force-slide, +boost-tokens, +active-event, +card-keywords]
proposes: ["+trigger:phase_end", "+trigger:deck_empty", "+cond:adjacent_to", "+cond:clear_line", "+cond:on_own_side", "+effect:draw_card", "+effect:discard", "+effect:roll_dice", "+effect:force", "+effect:boost", "+role:card", "+role:summoner", "+ui:magic-track", "+ui:card-hand", "+ui:phase-indicator", "+window:deck-builder", "+feature:deck-construction"]
author: opus
date: 2026-11-09
---

# Summoner Wars — карткова тактика на сітці 6×8: призивай лише біля своїх стін, а платиш колодою з убитих і скинутих карт

## Суть
Настільна карткова гра на двох (Plaid Hat Games, дизайнер Colby Dauch): кожна колода — фракція, що виставляє карти-юніти на сітку. Мета — знищити **призивача** суперника. Головні ідеї: юніта можна призвати **лише на клітину поруч зі своєю стіною** (стіни — точки спавну, їх ставлять і руйнують), а «мана» — це окрема **колода магії**, яку поповнюють і скинуті з руки карти, і знищені тобою карти. Тож кожна карта в руці — вибір: зіграти чи спалити на магію.

## Поле і час
- Сітка 6 стовпців × 8 рядів (ряд = 6 клітин, твоя сторона = 4 ближні ряди — PDF 2-го вид.); клітини розміром з карту.
- Суміжність — лише по ребру; діагоналей нема ні в русі, ні в атаці, ні в лічбі відстаней.
- Хід — фази в строгому порядку; гравці чергуються. Перший гравець має фору-обмеження.
- Прихована інформація: рука, порядок колоди добору; свою колоду магії можна переглядати, але не перекладати.
- Випадковість: тасування колоди (setup) і кубики атаки (runtime).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Призивач | piece | атака, життя, здібність | на полі з початку; його знищення = поразка |
| Чемпіон | piece | атака, життя, ціна, здібність | унікальний сильний юніт (3 на колоду у 2-му вид.) |
| Звичайний юніт (common) | piece | атака, життя, ціна, меч/лук | основна маса армії |
| Стіна (1-ше вид.) | static | життя | точка призову; ставиться подією на своїй стороні; її можна атакувати |
| Ворота (2-ге вид.) | static | 10 (стартові) / 5 життя | споруда-точка призову; будується поруч із призивачем або в 3 задніх рядах |
| Лоза-стіна (Swamp Orcs) | terrain | 2 життя | будь-де, навіть під юнітом; вихід з неї — кидок кубика |
| Карта події | object | ефект, фаза (2-ге вид.) | грається з руки, розвʼязується, у скид |
| Активна подія (2-ге вид.) | object | ACTIVE | лежить в активній зоні до початку твого наступного ходу |
| Колода добору | supply | — | добір до 5 карт; порожня — більше не добираєш |
| Колода магії / трек магії | resource | кількість карт / позиція | валюта призову |
| Скид | supply | — | витрачена магія, зіграні події |
| Рана / жетон шкоди | mark | 1 або 3 | шкода на карті; рани ≥ життя → знищено |
| Жетон boost (2-ге вид.) | mark | — | паливо здібностей окремих карт |
| Кубик | object | 6 граней | 1-ше вид.: 3+ = влучання; 2-ге: символи меч / лук / спецсимвол |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «стартова розстановка з картки-довідки фракції; рука порожня»`; перший гравець пропускає Draw, Summon, Events і рухає лише 2 юніти.
- КОЛИ `phase_start(draw)` → ТО `custom: «добрати до 5 карт у руці»`; ЯКЩО `custom: «колода добору порожня»` → ТО `custom: «добору нема, граєш тим, що лишилось»`.
- КОЛИ `input(summon, unit_card)` → ЯКЩО `counter(magic_pile, ≥, cost)` і `custom: «порожня клітина по ребру поруч зі своєю стіною»` → ТО `place(player, unit)`, `custom: «cost карт з верху колоди магії → у скид»`.
- КОЛИ `input(event, card)` → ТО `custom: «ефект події»`, `custom: «карта у скид»`; кількість подій за хід не обмежена.
- КОЛИ `input(event, wall)` → ЯКЩО `free(cell)` і `custom: «клітина на своїй стороні»` → ТО `place(player, wall)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «≤ 3 різні юніти за фазу, кожен раз»` і `path_exists(unit, cell)` ≤ 2 клітин по ортогоналі крізь порожні → ТО `move(unit)`; закінчити — лише на порожній; рух на 0 для здібності теж займає слот.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `custom: «≤ 3 різні юніти за фазу»` і (`custom: «меч: ціль по ребру поруч»` або `custom: «лук: ціль ≤ 3 клітин по прямій, проміжні порожні»`) → ТО `custom: «кинути кубиків = атаці»`.
- КОЛИ `custom: «на кубику 3 або більше»` → ТО `damage(target, 1)` (1-ше вид.); 2-ге вид. — `damage(target, 1)` за кожен символ, що збігається з мечем/луком атакувальника.
- КОЛИ `counter(wounds, ≥, life)` → ТО `disappear(target)`, `custom: «карта сорочкою вгору на верх колоди магії атакувальника»` (1-ше вид.); 2-ге вид. — у скид власника, `currency(+1)` атакувальнику за ворожу карту.
- КОЛИ `custom: «атака по своїй карті»` → ТО `custom: «дозволено (крім себе) — свій юніт теж дасть магію»`.
- КОЛИ `phase_start(build_magic)` → ТО `custom: «будь-скільки карт з руки сорочкою вгору → у колоду магії»` (2-ге вид.: `currency(+1)` за кожну скинуту).
- КОЛИ `custom: «ворожа стіна знищена»` → ТО `custom: «суперник втрачає точку призову; без своїх стін призов неможливий»`.
- КОЛИ `custom: «юніт виходить з лози-стіни»` → ЯКЩО `prob(1/2)` (кидок ≤ 3) → ТО `damage(unit, 1)`, `block`; інакше рух звичайний.
- КОЛИ `custom: «здібність Swift»` → ТО `custom: «+1 клітина руху»`; здібності обовʼязкові, крім тих, що замінюють атаку або мають «may».
- КОЛИ `custom: «лишився лише один призивач на полі»` → ТО `win` його власнику.
- Друге видання (2021):
  - КОЛИ `turn_start(player)` → ТО фази `Summon → Move → Build → Attack → Magic`, після них — добір до 5.
  - КОЛИ `input(build, structure)` → ЯКЩО `counter(magic, ≥, cost)` і `custom: «поруч із призивачем або в 3 задніх рядах»` → ТО `place(player, gate)`.
  - КОЛИ `custom: «кінець фази атаки»` → ЯКЩО `custom: «цього ходу ти не атакував жодної ворожої карти»` → ТО `damage(own_summoner, 1)` (Cost of Inaction).
  - КОЛИ `custom: «Force N»` → ТО `slide(target, dir)` на N порожніх клітин по прямій; це не рух.
  - КОЛИ `custom: «кілька ефектів одночасно»` → ТО `choose(order)` — обирає активний гравець.
- Перемога: знищити призивача суперника · Поразка: втратити свого · Рахунок: —.

## Керування і ввід
- Настільна: карти-юніти кладуться на клітини поля, жетони ран на карти, кубики кидаються; кожна фаза — окремий набір дій.
- (цифрова версія) вибір карти з руки → підсвітка допустимих клітин біля стін; вибір юніта → `legal-move-highlight` (до 2 клітин, без діагоналей); вибір цілі в зоні меч/лук; кнопка «наступна фаза»; кидок кубиків анімацією.
- Обмеження «до 3 юнітів» на рух і атаку — головний «бюджет» ходу.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): поле 6×8, `pocket` (рука до 5), лічильник колоди магії / `+ui:magic-track`, лічильники добору і скиду, `+ui:phase-indicator`, жетони ран на картах, лоток кубиків, `turn-indicator`.
- `character-select` (цифрова версія): вибір фракції.
- `custom-window` побудова колоди (`+window:deck-builder`, 2-ге вид.): 1 призивач, ворота, 2 стартові юніти, 2 епічні події, 6 стандартних подій, 3 чемпіони, 16 звичайних; ліміти копій.
- `lobby-window` / `match-setup` (онлайн-версія); `end-screen` — переможець; `help-window` — правила й глосарій ключових слів.

## Фічі поза полем
- Фракції-колоди (24 продукти у 2-му вид.), готові до гри; `+feature:deck-construction` — змішування карт з однаковим символом колоди.
- Цифрові: Summoner Wars Mobile (Playdek, iOS 2012, Android 2014 — зараз недоступні), Summoner Wars Online (браузер, 2-ге вид.): `online-multiplayer`.
- `rules-page` — глосарій термінів (adjacent, within X spaces, behind, force, boost…).

## Варіації й родичі
- **Перше видання (2009)** і **друге (2021)** — різна економіка: колода магії з убитих і скинутих карт ↔ трек магії (+1 за ворожу карту, +1 за скинуту); стіни-події ↔ ворота-споруди з будуванням; кубики «3+» ↔ символи; додано Cost of Inaction, Force, boost, активні події.
- Родичі в корпусі: [Duelyst](duelyst.md) (призов поруч із будь-яким своїм юнітом, мана росте щоходу), [Faeria](faeria.md) (гравці будують саме поле землями), [Heroscape](heroscape.md) (фігури + кубики), [Card Hunter](card-hunter.md) (карти як дії на сітці), [Mage Knight](mage-knight.md) (карта як дія або ресурс).
- **Осі варіацій**: де можна призивати — біля своєї стіни/воріт (SW) / біля будь-якого свого юніта ([Duelyst](duelyst.md)) / на збудованій землі ([Faeria](faeria.md)) · мана — колода з убитих і скинутих (SW1) / трек (SW2) / максимум, що росте щоходу ([Duelyst](duelyst.md)) · бюджет ходу — до 3 юнітів рухаються і до 3 атакують / усі юніти / очки дій.

## Цікавинки для курсу
- Стіни як точки спавну: призов лише в порожню сусідню клітину своєї стіни; знищив стіни — суперник без підкріплення — 🌱.
- Колода магії з убитих і скинутих карт: одна стопка як валюта і «рахунок» вбивств — 📎.
- Ліміт «до 3 юнітів на рух і на атаку» за хід — 🌱.
- Дальня атака по прямій ≤ 3 клітин з перевіркою порожніх проміжних — 🌱.
- Кубики «3+» на кожен пункт атаки з ранами як жетонами — 🌱; символьні кубики 2-го вид. — 📎.
- Cost of Inaction: пасивність шкодить власному призивачу — 🌱.
- Побудова колоди з лімітами копій і обовʼязковим складом — 📎.

## Мапа на каталог
- Є: `hp-damage` (рани/життя) · `melee-vs-ranged` (меч/лук) · `line-of-sight-attack` (лук по прямій) · `pocket` (рука) · `hot-seat` · `online-multiplayer` · `character-select` (фракція) · `legal-move-highlight` (цифрова).
- **Нема** → пропозиції карток:
  - `+wall-spawn-point` «Призов лише біля своєї стіни/воріт» · entities/spawn · 🌱.
  - `+magic-pile-from-kills` «Мана — стопка з убитих і скинутих карт» · game-logic/economy · 📎.
  - `+discard-for-mana` «Скинути карту з руки → +1 магії» · game-logic/economy · 🌱.
  - `+unit-action-limit` «До N різних юнітів на рух і на атаку за хід» · game-logic/turns · 🌱.
  - `+draw-to-hand-size` «Добір до розміру руки» · game-logic/cards · 🌱.
  - `+deck-out-no-reshuffle` «Порожня колода не перетасовується» · game-logic/cards · 🌱.
  - `+first-player-handicap` «Обмеження першого ходу» · game-logic/turns · 🌱.
  - `+cost-of-inaction` «Шкода собі за хід без атаки» · game-logic/turns · 🌱.
  - `+force-slide` «Зсув на N по прямій, що не є рухом» · entities/move · 📎.
  - `+structure-building` / `+back-rows-zone` «Споруди лише в задніх рядах або біля лідера» · entities/legality · 📎.
  - `+active-event` «Подія діє до початку наступного ходу» · game-logic/cards · 🌱.
  - `+deck-draw` / `+summon-adjacent` / `+combat-dice-symbols` / `+leader-death-lose` / `+friendly-fire` / `+faction-decks` / `+deck-building` / `+boost-tokens` / `+card-keywords` / `+orthogonal-only` — уже в корпусі або дрібні.

## Пропозиції до словників
- `+trigger:phase_end` — фаза ходу завершилась (Cost of Inaction).
- `+trigger:deck_empty` — колода добору вичерпана.
- `+cond:adjacent_to` — клітина по ребру поруч із сутністю виду (призов біля стіни).
- `+cond:clear_line` — між A і B по прямій лише порожні клітини (лук).
- `+cond:on_own_side` — клітина на своїй половині поля / в задніх рядах.
- `+effect:draw_card` · `+effect:discard` · `+effect:roll_dice` · `+effect:force` (зсув по прямій без руху) · `+effect:boost`.
- `+role:card` — карта в руці/колоді як сутність поза полем; `+role:summoner` — лідер, чия смерть = поразка.
- `+ui:magic-track` · `+ui:card-hand` · `+ui:phase-indicator`.
- `+window:deck-builder` — побудова колоди з правилами складу.
- `+feature:deck-construction` — власні колоди з обмеженнями.

## Джерела
- ⭐ [UltraBoardGames: Summoner Wars rules](https://www.ultraboardgames.com/summoner-wars/game-rules.php) — повні правила 1-го видання: розстановка, фора першого гравця, 6 фаз, призов біля стіни, магія з убитих і скинутих, рух 3×2, атака 3 юнітами, кубики 3+, рани 1/3, стіни, лоза-стіни, перемога, порожня колода.
- [Plaid Hat: Rulebook 2nd Edition v1.2 (PDF)](https://media.plaidhatgames.com/filer_public/7d/07/7d075572-2254-4248-bdb5-464ef4b97180/ph3600-rulebook-v1_2.pdf) — фази 2-го вид., трек магії, ворота 10/5, будування в 3 задніх рядах, символьні кубики, Cost of Inaction, Force, boost, активні події, глосарій, ряд = 6, сторона = 4 ряди, побудова колоди.
- [Plaid Hat Games](https://www.plaidhatgames.com/games/summoner-wars/) — дизайнер, 2 гравці, 45–60 хв, фракції, онлайн-версія.
- [Wikipedia: Summoner Wars](https://en.wikipedia.org/wiki/Summoner_Wars) — мобільна версія Playdek, 2-ге видання 2021.

## Непевне
- (?) Розмір поля 1-го видання — узяв 6×8 з правил 2-го; UltraBoardGames розміру не дає.
- (?) Інтерфейс мобільної й онлайн-версій (кнопки фаз, підсвітки, AI-суперник) — не бачив, описано як «цифрова версія».
- (?) У 2-му виданні «на кубику — символи»: скільки граней якого символу — не вказано в тексті PDF.
