---
title: Tiny Towns (Крихітні містечка)
slug: tiny-towns
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: partial
  random: setup
  goal: score
year: 2019
platforms: [board, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/tiny-towns/game-rules.php", best: true, note: "повні правила: майстер-будівничий, будівництво за шаблоном, монументи, кінець, тай-брейки, печера"}
  - {kind: other, url: "https://www.ultraboardgames.com/tiny-towns/buildings.php", note: "уточнення до кожної будівлі"}
  - {kind: other, url: "https://www.ultraboardgames.com/tiny-towns/monuments.php", note: "уточнення до 12 монументів"}
  - {kind: other, url: "https://www.ultraboardgames.com/tiny-towns/solo.php", note: "соло: колода з 15 карт ресурсів, рівні рахунку"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=tinytowns", note: "грати в браузері (BGA), 1–6 гравців"}
  - {kind: other, url: "https://en.doc.boardgamearena.com/Gamehelptinytowns", note: "довідка BGA: як будувати в інтерфейсі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tiny+Towns+board+game+how+to+play", note: "пошук; пояснення правил"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Tiny+Towns", note: "пошук BGG"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, legal-move-highlight, event-points, no-moves-left, completion-detection, game-settings, +named-resource-all-place, +shape-pattern-match, +build-from-pattern, +building-scoring-rules, +piece-rotate-flip, +secret-objective, +leftover-penalty, +rotating-caller]
proposes: ["+trigger:pattern", "+cond:shape_match", "+effect:place", "+effect:consume", "+role:building", "+ui:card-row", "+ui:pattern-highlight", "+window:card-zoom", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Tiny Towns — 4×4 містечко: ресурс називає хтось інший, будівля зводиться, коли кубики склали її шаблон

## Суть
Кожен гравець будує своє містечко 4×4. Щораунду майстер-будівничий (роль по колу) **називає** тип ресурсу, і **всі одночасно** мусять покласти кубик цього типу в порожню клітину свого міста. Коли кубики утворили шаблон будівлі з карти (повороти й дзеркала дозволені), їх можна зняти й поставити будівлю на одну з цих клітин. Будівлі по-різному дають очки (сусідство, рядки, кількість); порожні клітини — штраф. Ядро — пакування під чужий вибір: тобі дають ресурси, які ти не просив.

## Поле і час
- Особисте поле 4×4 = 16 клітин; клітина: порожня / кубик ресурсу / будівля. Сусідство — лише ортогональне.
- Спільна «вітрина»: 7 карт будівель на партію (Котедж завжди + по одній випадковій з 6 кольорових груп), кожна — шаблон з кубиків і правило очок. Плюс 1 особистий монумент (таємний).
- Раунд: майстер називає ресурс → усі кладуть кубик → кожен за бажанням будує (одночасно, оголошуючи) → роль майстра йде ліворуч.
- Ресурси після викладання не рухаються; будівлі не рухаються. Місто «завершене», коли гравець не може або не хоче більше класти/будувати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик ресурсу | resource | тип: wood, wheat, brick, glass, stone | кладеться в порожню клітину; знімається лише при будівництві |
| Карта будівлі | supply | шаблон кубиків, група-колір, правило очок | відкрита для всіх; будувати можна скільки завгодно разів |
| Будівля | building | тип з карти | займає 1 клітину; очки/ефект за своєю картою |
| Котедж (синій) | building | шаблон з 3 кубиків | 3 ПО, лише якщо «нагодований» фермою-групи |
| Ферми (червоні: Farm, Granary, Greenhouse, Orchard) | building | — | годують котеджі (Farm — 4 будь-де; Granary — 8 сусідніх; Greenhouse — одну звʼязну групу; Orchard — до 6) |
| Сірі (Fountain, Millstone, Shed, Well) | building | — | Well: +1 за сусідній котедж; Shed: ставиться в будь-яку порожню клітину; Fountain: 2 ПО поруч з іншим фонтаном |
| Оранжеві (Abbey, Chapel, Cloister, Temple) | building | — | Chapel: +1 за кожен нагодований котедж; Cloister: за кути; Temple: 4 ПО (?) біля ≥2 котеджів |
| Зелені (Almshouse, Feast Hall, Inn, Tavern) | building | — | рахуються групою за кількістю: Tavern 1/4/9/14/20 (?), Almshouse до 26 з чергуванням знаків (?) |
| Жовті (Bakery, Market, Tailor, Theater) | building | — | Theater: +1 за кожен інший тип будівлі в його ряду й стовпці |
| Чорні (Bank, Factory, Trading Post, Warehouse) | building | — | змінюють правила ресурсів: Factory підміняє названий ресурс, Warehouse зберігає до 3 кубиків, Trading Post — вічний ресурс-джокер |
| Монумент | building | 1 на гравця, таємна карта (з 2 обрати 1) | будує лише власник, один раз; сильний ефект або очки |
| Молоток майстра | object | — | хто тримає — називає ресурс; переходить ліворуч |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО майстер `input(name(resource))`.
- КОЛИ `custom: «ресурс названо»` → ТО кожен гравець `input(place(resource, cell))` → ЯКЩО `free(cell)` → ТО `place`; одночасно, обовʼязково.
- КОЛИ `input(build(card, cells, target))` → ЯКЩО `shape_match(cells, card.pattern, rot+mirror)` and `custom: «target ∈ cells»` → ТО `consume(cells)` (кубики в запас), `place(building, target)`; інакше `block`.
- Кубики шаблону не мусять бути сусідами з іншими; повний шаблон можна не будувати й чекати.
- Кожен кубик іде лише в одну будівлю. Shed — виняток: будівля ставиться в будь-яку порожню клітину.
- КОЛИ `custom: «збудовано монумент»` → ЯКЩО `custom: «це мій монумент і ще не будувався»` → ТО `place(monument)`, `trigger(monument.effect)` одразу.
- КОЛИ `no_moves(player)` (нема порожніх клітин і нема що будувати) або гравець так вирішив → ТО `set_state(player, town_complete)`; він більше не називає ресурси.
- КОЛИ лишився один незавершений гравець → ТО він сам називає ресурси до завершення.
- КОЛИ `custom: «усі міста завершені»` → ТО зняти всі кубики; `score(-1)` за кожну клітину без будівлі; `score(+правила будівель)`; `game_over`.
- Котедж: `score(+3)` лише якщо `state(cottage, fed)`; ферми розподіляють «їжу» за своїми правилами.
- Перемога — найбільше ПО (можуть бути відʼємні). Тай-брейк: менше разів був майстром → менше порожніх клітин → більше котеджів → спільна перемога.
- Варіант «печера»: до 2 названих іншими ресурсів можна відкласти вбік (без очок) замість поля.
- Соло: колода з 15 карт ресурсів, відкрито 3, обираєш одну; невикористана карта — під низ колоди; рахунок → звання (38+ — Master Architect).

## Керування і ввід
- Майстер: вибір ресурсу з 5 кнопок. Усі: клік по порожній клітині для кубика.
- Будівництво (BGA): клік по карті будівлі → клік по клітині з кубиком шаблону, де стане будівля; інтерфейс сам знаходить відповідний шаблон серед кубиків.
- Хід усіх одночасний: інтерфейс чекає, доки кожен поклав кубик (індикатор «хто ще думає»).

## Вікна, меню, HUD
(цифрова версія — BGA)
- `lobby-window` / `match-setup` (кандидат): 1–6 гравців, варіанти (печера, ратуша, соло), таймер.
- Стартовий модал: вибір 1 з 2 карт монументів (`choose`).
- `game-screen`: своє поле 4×4 крупно; `card-row` — ряд 7 карт будівель із шаблонами; свій монумент; `opponent-boards` — поля інших гравців зменшено; `turn-indicator` + молоток біля майстра; панель ресурсу, щойно названого; `pattern-highlight` — клітини, що складають доступний шаблон; `score` поточний (?).
- `card-zoom` (кандидат): збільшена карта будівлі з шаблоном і правилом очок.
- `end-screen`: таблиця очок по типах будівель, штраф за порожні клітини, тай-брейки.
- `help-window`: правила + довідка по кожній будівлі й монументу.
- Переходи: lobby → вибір монумента → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer` (BGA, 1–6), соло з колодою ресурсів і рівнями звань (`rank-tiers` за рахунком).
- `custom-rules`: печера, ратуша (Town Hall), рекомендовані набори будівель для перших партій.
- `turn-timer`, асинхронна гра (BGA).
- Розширення (паперові): Fortune (монети), Villagers (мешканці), Architects (?) — нові карти й ефекти.

## Варіації й родичі
- Набір будівель змінюється кожної партії: одна з 4 карт у кожній з 6 груп → велика реплеюваність.
- Родичі: Patchwork і Blokus (пакування форм), Bingo-подібні «назви число — всі пишуть» (Take It Easy, Cartographers), Sagrada (обмеження сусідства), Kingdomino (своє поле 5×5), Isle of Cats.
- **Осі варіацій**: хто обирає ресурс (майстер по колу / сам / колода) · шаблон (точна форма / форма з поворотами / лише склад) · будівля після збирання (на місці шаблону / будь-де) · рахунок (сусідство / ряди / кількість однакових / набір різних).

## Цікавинки для курсу
- Пошук шаблону з поворотами й дзеркалами серед клітин 4×4 — 🥉 (8 орієнтацій × зсуви; маленьке поле — простий перебір).
- «Ресурс називає інший гравець, кладуть усі одночасно» — 📎 логіка, 🥉 якщо мережева/одночасна синхронізація ходів.
- Таблиця правил очок будівель як дані (сусідство, ряд/стовпець, група, кути) — 🥈 (інтерпретатор правил на сітці).
- Годування котеджів фермами з різними радіусами (усе поле / 8 сусідів / звʼязна група) — 🥈 (flood fill + розподіл обмеженого ресурсу).
- AI-підказка «куди покласти ресурс, щоб не зламати шаблони» — 🥇.
- Соло-колода з трьома відкритими картами — 🌱.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `event-points` · `no-moves-left` (місто завершене) · `completion-detection` (усі міста завершені) · `game-settings`.
- **Нема** → пропозиції карток:
  - `+named-resource-all-place` «Один називає — всі кладуть» · game-logic/opponent · 📎 · слот {caller: rotating|deck}.
  - `+rotating-caller` «Роль, що переходить по колу» · game-logic/opponent · 🌱 (майстер; родич `+first-player-token` з Azul).
  - `+shape-pattern-match` «Пошук шаблону з поворотами/дзеркалами» · game-logic/constraints · 🥉 · слот {mirror: bool}.
  - `+build-from-pattern` «Зібрав шаблон → обмін на будівлю» · entities/interact · 📎.
  - `+building-scoring-rules` «Правила очок будівель як дані» · game-logic/score · 🥈 · слот {rules: list}.
  - `+piece-rotate-flip` — орієнтації шаблону (як у Blokus).
  - `+secret-objective` «Таємна особиста ціль/монумент» · game-logic/win · 🌱.
  - `+leftover-penalty` — −1 за клітину без будівлі.

## Пропозиції до словників
- `+trigger:pattern` вже ⏳ — тут `pattern(building_shape)` на полі гравця.
- `+cond:shape_match(cells, shape, transforms)` — набір клітин збігається з шаблоном з урахуванням поворотів/дзеркал.
- `+effect:place` — як у Blokus; `+effect:consume(cells)` — зняти ресурси з поля назад у запас (оплата будівлі).
- `+role:building` — нерухома сутність, що дає очки/ефект за правилом сусідства (Tiny Towns, Kingdomino-замки, build-sim).
- `+ui:card-row` — ряд відкритих карт (будівлі, цілі) поруч з полем; `+ui:pattern-highlight` — підсвітка клітин, що складають готовий шаблон.
- `+window:card-zoom` — збільшений перегляд карти з правилом.
- `+axis:turn-structure` = `simultaneous`.

## Джерела
- ⭐ [UltraBoardGames: Tiny Towns rules](https://www.ultraboardgames.com/tiny-towns/game-rules.php) — повний цикл, будівництво, монументи, кінець, тай-брейки, печера.
- [UltraBoardGames: Buildings](https://www.ultraboardgames.com/tiny-towns/buildings.php) і [Monuments](https://www.ultraboardgames.com/tiny-towns/monuments.php) — уточнення до кожної карти.
- [UltraBoardGames: Solo](https://www.ultraboardgames.com/tiny-towns/solo.php) — соло-колода і рівні рахунку.
- [BGA: Tiny Towns](https://en.boardgamearena.com/gamepanel?game=tinytowns) і [довідка BGA](https://en.doc.boardgamearena.com/Gamehelptinytowns) — Peter McPherson, AEG, 1–6 гравців, як будувати в інтерфейсі.
- YouTube: пошук «Tiny Towns board game how to play».

## Непевне
- (?) Точні шаблони будівель (напр. Котедж — L з wheat/brick/glass, Well — wood+stone) і більшість числових значень очок (Tavern 1/4/9/14/20, Almshouse −1/5/−3/15/−5/26, Temple 4) — з памʼяті; джерела дають лише уточнення.
- (?) Кольори груп будівель (синій/червоний/сірий/оранжевий/зелений/жовтий/чорний) — з памʼяті, UBG групує за іконками.
- (?) Радіус Orchard (джерело: «годує до 6» — де саме, не сказано).
- (?) Чи має BGA AI-суперників для Tiny Towns і чи показує поточний рахунок наживо — не перевірено.
- (?) Назва третього розширення (Architects) і Town Hall-варіант — не перевірено; Wikipedia-статті нема (404).
