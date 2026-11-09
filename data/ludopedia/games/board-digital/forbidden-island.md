---
title: Forbidden Island
slug: forbidden-island
aka: [Заборонений острів]
family: board-digital
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: coop
  info: hidden
  random: both
  goal: state
year: 2010
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Forbidden_Island_(game)", best: true, note: "суть за хвилину: кооп, 4 скарби, затоплення й потоплення плиток, умови перемоги й поразки, серія Forbidden"}
  - {kind: other, url: "https://www.ultraboardgames.com/forbidden-island/game-rules.php", note: "повні правила: склад колод, 3 дії, Waters Rise!, повінь і потоплення, плавання, 6 ролей, спецкарти, ліміт руки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Forbidden+Island+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-8dir, teleport, impassable-cells, environment-death, collect-all, reach-exit, difficulty-levels, character-select, game-screen, end-screen, help-window, +shared-field-coop, +action-points, +variable-player-powers, +deck-draw, +hand-limit, +doom-track, +escalating-draw-count, +intensify-reshuffle, +flood-then-sink, +shrinking-board, +repair-adjacent, +set-collection-cure, +treasure-site-pair, +swim-on-sink, +event-cards-any-time, +all-must-exit]
proposes: ["+effect:draw_cards", "+effect:reshuffle", "+effect:sink", "+effect:discard", "+trigger:deck_empty", "+role:card", "+ui:doom-track", "+ui:card-hand", "+card:flood-then-sink", "+card:shrinking-board", "+card:swim-on-sink"]
author: opus
date: 2026-11-09
---

# Forbidden Island — кооп на острові з 24 плиток: повінь перевертає плитку, вдруге — топить її назавжди

## Суть
Перша гра серії Matt Leacock (Gamewright, 2010) для 2–4 гравців: команда шукає 4 скарби й має разом відлетіти гелікоптером з Fools' Landing, поки острів не пішов під воду. За хід — до 3 дій (рух, укріпити плитку, передати карту, взяти скарб), потім 2 карти скарбів і стільки карт повені, скільки показує рівень води. Карта повені вперше перевертає плитку на «затоплений» бік, а вдруге — топить її: плитка й карта виходять з гри, і поле зменшується. Спільне ядро з Forbidden Desert (`forbidden-desert.md`) і Pandemic (`pandemic.md`) — ролі, дії, події з колоди наприкінці ходу, шкала ескалації.

## Поле і час
- 24 двобічні плитки (суха / затоплена) у випадковому порядку: квадрат 4×4 і по 2 плитки біля двох середніх з кожного боку — «ромб» з діркою-морем довкола; між плитками щілини.
- Затонулі плитки зникають — на їх місці море; сітка дірявіє й розпадається на частини (на відміну від FD, де плитки лише зсуваються).
- Шари: плитка (суха / затоплена / нема) + фішки мандрівників; скарби — поза полем, у команди.
- Хід гравця: до 3 дій → 2 карти скарбів → карти повені за рівнем води. Першим ходить той, хто останнім бував на острові, далі ліворуч.
- Інформація: колоди скарбів і повені закриті, руки відкриті для обговорення; випадковість — розкладка острова, ролі й колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мандрівник | piece | роль, рука ≤5 карт | 3 дії на хід; стартує на плитці своєї ролі |
| Explorer | piece | — | ходить, укріплює й пливе також по діагоналі |
| Pilot | piece | — | раз за хід летить на будь-яку плитку за 1 дію; при потопленні — летить будь-куди |
| Navigator | piece | — | за 1 дію пересуває іншого гравця до 2 сусідніх плиток |
| Diver | piece | — | за 1 дію проходить крізь сусідні затоплені й зниклі плитки; при потопленні пливе до найближчої |
| Engineer | piece | — | укріплює 2 плитки за 1 дію |
| Messenger | piece | — | передає карти скарбів будь-кому, не стоячи поруч |
| Плитка острова | tile | 24; суха / затоплена | затоплена: ходити можна; повторна повінь — тоне й зникає |
| Fools' Landing | static | 1 плитка | вертолітний майданчик: ціль виходу; затонула — поразка |
| Плитка скарбу | static | 2 на скарб: храми, печери, палаци, сади | тут береться скарб; обидві затонули до взяття — поразка |
| Скарб | pickup | 4: Earth Stone, Statue of the Wind, Crystal of Fire, Ocean's Chalice | береться за 4 однакові карти на одній з 2 його плиток |
| Карта скарбу | resource | 5 на кожен скарб (20) | у руці; передається на тій самій плитці за 1 дію |
| Waters Rise! | hazard | 3 карти в колоді скарбів | рівень води +1, скид повені — на верх колоди повені |
| Helicopter Lift | pickup | 3 карти | будь-коли без дії: переліт; потрібна для фінального вильоту |
| Sandbags | pickup | 2 карти | будь-коли без дії: укріпити будь-яку плитку |
| Карта повені | mark | 24, по одній на плитку | вперше — затопити плитку, вдруге — потопити, карта виходить з гри |
| Шкала води | supply | позначка рівня, поділки до черепа | скільки карт повені тягнути; череп — поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «6 карт повені → 6 плиток затоплено»`; `custom: «по 2 карти скарбів кожному; Waters Rise! замінити й замішати назад»`.
- КОЛИ `input(move(pawn, dir))` → ЯКЩО `custom: «dir ортогональний (Explorer — і діагональ)»` і `not cell(target, sea)` → ТО `move(pawn, dir)`, `counter(actions, -1)`; затоплену плитку можна, зниклу — `block`.
- КОЛИ `input(fly(target))` → ЯКЩО `state(pawn, pilot)` і `custom: «ще не літав цього ходу»` і `not cell(target, sea)` → ТО `teleport(pawn, target)` за 1 дію.
- КОЛИ `input(dive(path))` → ЯКЩО `state(pawn, diver)` і `custom: «шлях — через сусідні затоплені/зниклі плитки»` → ТО `move(pawn, path_end)` за 1 дію.
- КОЛИ `input(navigate(other, path))` → ЯКЩО `state(pawn, navigator)` і `custom: «≤2 сусідні плитки»` → ТО `move(other, path)` за 1 дію.
- КОЛИ `input(shore_up(tile))` → ЯКЩО `in_range(pawn, tile, 1)` (своя або ортогональна; Explorer — і діагональна) і `state(tile, flooded)` → ТО `clear_state(tile, flooded)`; Engineer — 2 плитки за 1 дію.
- КОЛИ `input(give(card, other))` → ЯКЩО `occupied(here, other)` (Messenger — будь-де) і `custom: «карта скарбу, не спецкарта»` → ТО `give(other, card)` за 1 дію на карту.
- КОЛИ `input(capture)` → ЯКЩО `cell(here, treasure_site[T])` і `has(pawn, treasure_card[T] ×4)` → ТО `take(pawn, 4 cards)`, `pickup(team, treasure_T)` за 1 дію; затоплена плитка — теж можна.
- КОЛИ `turn_end(player)` → ТО `custom: «тягнути 2 карти скарбів по одній»` (`+effect:draw_cards`).
- КОЛИ `custom: «витягнуто Waters Rise!»` → ТО `counter(water_level, +1)`, `custom: «скид повені перетасувати й покласти на верх колоди повені»` (`+effect:reshuffle`), карта — у скид без заміни; дві поспіль — тасувати раз, рівень +2; порожній скид — лише +1.
- КОЛИ `counter(hand, >, 5)` → ТО `custom: «одразу скинути до 5»` (`+effect:discard`); спецкарту можна зіграти замість скидання.
- КОЛИ `custom: «після карт скарбів»` → ТО `custom: «тягнути карти повені = рівень води, по одній»`.
- КОЛИ `custom: «карта повені плитки X»` → ЯКЩО `not state(X, flooded)` → ТО `set_state(X, flooded)`; ЯКЩО `state(X, flooded)` → ТО `disappear(X)`, `set_cell(X, sea)`, `custom: «карта повені X виходить з гри»` (`+effect:sink`).
- КОЛИ `destroyed(tile)` → ЯКЩО `occupied(tile, pawn)` і `custom: «є ортогональна сусідня плитка (Explorer — і діагональна)»` → ТО `move(pawn, adjacent)`; Diver — до найближчої, Pilot — будь-куди; інакше `lose`.
- КОЛИ `custom: «колода повені порожня»` (`+trigger:deck_empty`) → ТО `custom: «перетасувати скид повені в нову колоду й тягнути далі»`; так само для колоди скарбів.
- КОЛИ `input(play(helicopter_lift))` → ТО `teleport(pawns_on_tile, any_tile)` (?), без дії, будь-чий хід; `disappear(card)`.
- КОЛИ `input(play(sandbags, tile))` → ЯКЩО `state(tile, flooded)` → ТО `clear_state(tile, flooded)` будь-де, без дії; не рятує плитку, чия карта повені вже відкрита.
- КОЛИ `destroyed(treasure_site)` → ЯКЩО `custom: «обидві плитки скарбу T зникли»` і `not has(team, treasure_T)` → ТО `lose`.
- КОЛИ `destroyed(fools_landing)` → ТО `lose`.
- КОЛИ `counter(water_level, ==, skull)` → ТО `lose`.
- КОЛИ `all_on(pawn, fools_landing)` → ЯКЩО `has(team, treasure ×4)` і `custom: «один гравець скидає Helicopter Lift»` → ТО `win` — навіть якщо майданчик затоплений.
- Перемога: 4 скарби + усі на Fools' Landing + Helicopter Lift · Поразка: зникли обидві плитки невзятого скарбу / затонув Fools' Landing / нема куди пливти / вода на черепі · Рахунок: нема.

## Керування і ввід
- Настільна: активний гравець витрачає до 3 дій у будь-якому порядку; спецкарти (Helicopter Lift, Sandbags) — будь-коли, навіть у чужий хід, без дії; команда радиться, рішення — за активним.
- (цифрова версія) Тап по плитці — підсвітка легальних дій (рух / укріпити / взяти скарб); тап по карті руки — ціль; кнопка «Кінець ходу» запускає тягнення карт скарбів і повені з анімацією перевороту/потоплення.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра · Правила · Налаштування.
- `match-setup`: 2–4 гравці, складність від Novice (?) — стартова поділка шкали води.
- `character-select`: 6 ролей (випадково або на вибір) з описом вмінь.
- `game-screen`: острів з плиток (суха / синьо-біла затоплена / море), фішки; `+ui:doom-track` шкала води з черепом (скільки карт повені тягнути); `+ui:card-hand` руки гравців (ліміт 5); `action-points` (лишилось дій 0–3); `progress-bar` зібраних скарбів 0/4; стоси колод і скидів скарбів і повені; `turn-indicator`.
- `popup-text` «Затоплено» / «Затонуло» / «Waters Rise!»; `confirm-dialog` скидання до 5 карт.
- `end-screen`: перемога (відліт) або причина поразки.
- `help-window`: правила й памʼятка ролей.
- Переходи: main-menu → match-setup → character-select → game-screen → end-screen.

## Фічі поза полем
- `difficulty-presets`: Novice … Legendary (?) — стартова позначка на шкалі води.
- `mode-coop` — усі проти гри; за одним столом.
- Випадкова розкладка 24 плиток і ролей — кожна партія інша.

## Варіації й родичі
- **Спільне ядро з Forbidden Desert** (`forbidden-desert.md`): кооп, 6 ролей-модифікаторів базових дій, дії на хід, колода подій тягнеться наприкінці ходу, шкала ескалації з черепом, команда має зібрати 4 предмети й разом вийти з поля, підсумкова поразка з кількох незалежних причин.
- **Відмінності FI → FD**:
  - дій 3 → 4; поле — «ромб» з 24 плиток → 5×5 з діркою-бурею;
  - загроза: повінь перевертає / топить плитку (поле зменшується) → вітер зсуває плитки в дірку й насипає пісок (поле стале, рухається дірка);
  - ресурс виживання: нема → вода у флягах (спрага);
  - скарби: 4 однакові карти на одній з 2 плиток скарбу → частини машини на перетині рядка й стовпця двох підказок;
  - ліміт руки 5 → без ліміту; передача карти коштує дію → обмін на одній плитці безкоштовний;
  - Waters Rise! (скид на верх колоди повені) → Storm Picks Up (більше карт за хід).
- Pandemic (`pandemic.md`) — та сама «Intensify»-механіка: скид перетасовується на верх колоди, тож затоплені плитки повертаються першими.
- Forbidden Sky (2018), Forbidden Jungle (2023) — наступні ігри серії; у корпусі нема.
- **Осі варіацій**: доля плитки (затопити → потопити / засипати / зсунути) · відновлення (укріпити сусідню / розкопати / нема) · ескалація (рівень → більше карт / скид на верх колоди / обидва) · ціль (набори карт на місцях / предмети за підказками) · фінальний вихід (усі на майданчику + спецкарта).

## Цікавинки для курсу
- Двоетапне знищення плитки (сухо → затоплено → нема) з укріпленням назад — 🌱.
- Плавання при потопленні: пошук сусідньої плитки з правилами ролей (діагональ, найближча BFS, будь-куди) — 📎.
- «Intensify»: перетасований скид кладеться на верх колоди повені — ті самі плитки б'є знову — 📎.
- Поразка через недосяжність: обидві плитки невзятого скарбу зникли або острів розпався так, що до майданчика не дійти (перевірка звʼязності) — 📎.
- 6 ролей як модифікатори руху/укріплення/передачі — 🥉 за систему ролей.
- AI-порадник: які 3 дії мінімізують ризик втратити ключову плитку за ймовірностями колоди повені — 🥇.

## Мапа на каталог
- Є: `move-4dir` / `move-8dir` (Explorer) · `teleport` (Pilot, Helicopter Lift) · `impassable-cells` (зниклі плитки) · `environment-death` (нема куди пливти) · `collect-all` (4 скарби) · `reach-exit` (Fools' Landing) · `difficulty-levels` · `character-select` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+flood-then-sink` «Перша подія псує клітину, друга знищує» · entities/interact · 🌱 · слот {stages: 2, repair: adjacent}.
  - `+shrinking-board` «Поле втрачає клітини назавжди, може розпастись» · entities/legality · 📎.
  - `+swim-on-sink` «Фігура на знищеній клітині мусить перейти на сусідню, інакше смерть» · entities/death · 🌱.
  - `+repair-adjacent` «Дія відновлює свою або сусідню клітину» · entities/interact · 🌱.
  - `+treasure-site-pair` «Ціль береться на одному з двох місць; обидва зникли — поразка» · game-logic/lose · 🌱.
  - `+all-must-exit` «Вийти мають усі» · game-logic/win · 🌱 (вже пропонована Kwirk).
  - `+shared-field-coop` · `+action-points` · `+variable-player-powers` · `+deck-draw` · `+hand-limit` · `+doom-track` · `+escalating-draw-count` · `+intensify-reshuffle` · `+set-collection-cure` · `+event-cards-any-time` — уже в корпусі.

## Пропозиції до словників
- `+effect:draw_cards` — взяти N карт з колоди (2 скарбів, рівень води — повені).
- `+effect:reshuffle` — перетасувати скид і покласти на верх колоди (Waters Rise!).
- `+effect:sink` — клітина зникає з поля разом з тим, що на ній, і назавжди виходить з гри (відрізняється від `disappear` збереженням дірки).
- `+effect:discard` — скинути карту з руки (ліміт 5).
- `+trigger:deck_empty` — колода скінчилась → перетасувати скид.
- `+role:card` — карта як сутність (скарб, Waters Rise!, повінь).
- `+ui:doom-track` — шкала води з черепом.
- `+ui:card-hand` — руки гравців на екрані.
- `+card:flood-then-sink` · `+card:shrinking-board` · `+card:swim-on-sink` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Forbidden Island](https://en.wikipedia.org/wiki/Forbidden_Island_(game)) — автор, 2–4 гравці, розкладка 4×4 + по 2 з боків, 6 стартових повеней, дії, 2 карти скарбів, ліміт 5, повінь/потоплення, 4 умови поразки, нагороди, наступні ігри серії.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/forbidden-island/game-rules.php) — склад колод (20 + 3 + 3 + 2), підготовка, 4 дії, Waters Rise! з винятками, повінь, плавання, 6 ролей, спецкарти будь-коли, ліміт руки, перемога й поразка.
- YouTube: пошук «Forbidden Island how to play».

## Непевне
- (?) Точний ефект Helicopter Lift поза фіналом (переліт однієї чи кількох фішок з однієї плитки на будь-яку) — з памʼяті; UBG каже лише «будь-коли, без дії».
- (?) Поділки шкали води (скільки карт на кожному рівні) і стартові позначки складностей — не бачив; назви Normal / Elite / Legendary — з памʼяті за аналогією з FD (UBG називає лише Novice).
- (?) Стартові плитки ролей (кожна роль має свою плитку-старт, напр. Pilot — Fools' Landing) — з памʼяті; UBG каже «pawn on its tile».
- (?) Офіційна цифрова версія (iOS?) — не перевіряв; вікна вище «(цифрова версія)».
