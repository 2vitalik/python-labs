---
title: Dungeon Twister
slug: dungeon-twister
aka: [DT, "Dungeon Twister: Prison"]
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: setup
  goal: score
year: 2004
platforms: [board, PS3]
links:
  - {kind: other, url: "https://rulespal.com/dungeon-twister/rulebook", best: true, note: "RulesPal: повні правила — 8 кімнат 4×2, картки дій, обертання шестернями, 8 героїв, 6 предметів, бій картками, ями й ґрати, 5 VP"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Twister", note: "Christophe Boelinger, Asmodée 2004, доповнення, PS3-версія 2012"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dungeon+Twister+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [hp-damage, impassable-cells, item-pickup, inventory-limit, line-of-sight-attack, reach-exit, event-points, hot-seat, pocket, placement-screen, pass-device, +modular-board, +rotate-structure, +room-reveal, +hand-of-cards-cycle, +simultaneous-hidden-orders, +double-blind-choice, +variable-player-powers, +hidden-setup-tokens, +carry-object, +trap-squares, +wall-pass, +stack-limit, +throw-pit-jump, +escape-to-opponent-edge]
proposes: ["+effect:play_card", "+effect:return_hand", "+effect:rotate_linked", "+cond:on_gear", "+cond:direct_access", "+role:card", "+ui:action-points-left", "+ui:card-hand", "+window:setup-tokens", "+feature:turn-timer-optional"]
author: opus
date: 2026-11-09
---

# Dungeon Twister — лабіринт, що крутиться: кімнати обертаються на чверть, щоб провести героїв через край суперника

## Суть
Двоє гравців ведуть по вісім героїв крізь підземелля з восьми кімнат-плиток, викладених 4×2 сорочкою вгору. Хід — зіграти одну з чотирьох **карток дій** (2, 3, 4 AP…) і витратити AP на відкриття кімнат, рух, бій, уміння і — головне — **обертання кімнати** на 90°, коли герой стоїть на її шестерні: стіни й проходи змінюють положення, і шлях, що був відрізаний, відкривається (або закривається перед ворогом). Очки — за вбитих ворогів і за героїв, що вийшли через стартову лінію суперника; перший до 5 VP закінчує партію. Випадковості немає, крім розкладу: бій вирішують таємно зіграні картки бою.

## Поле і час
- 8 квадратних кімнат-плиток, викладених прямокутником 4 кімнати в довжину і 2 в ширину; у кожного гравця — своя стартова лінія з короткого боку.
- Кімната — сітка клітин зі стінами, ямами, ґратами і **шестернею обертання** (кольорова стрілка + номер). Кімнати парні: дві з однаковим номером мають протилежні стрілки.
- Хід — гравця: одна картка дій → N AP, витрачених у будь-якому порядку; невикористані згорають. Кожна дія завершується до початку наступної.
- Приховане: кімнати до відкриття, жетони героїв і предметів у кімнатах (кладуться сорочкою), стартовий загін (відкривається одночасно), картки бою в руці.
- Опційно — таймер ходу 2 хвилини.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | номер пари, напрямок стрілки, місткість жетонів | відкривається; обертається на ¼ разом з усім, що на ній |
| Шестерня обертання | switch | номер, стрілка | герой на ній за 1 AP повертає свою кімнату або парну з тим самим номером |
| Стартова лінія | zone | власник | свої герої стартують; ворог, що дійшов, — тікає і дає VP |
| Стіна | static | — | блокує рух і лінію зору (крім Wall-Walker) |
| Яма-пастка | hazard | — | непрохідна; Thief стоїть, Rope дозволяє, Wizard левітує, картка Jump перестрибує |
| Ґрати (portcullis) | gate | відкриті / закриті / зламані | закриті блокують рух і зір; Thief відкриває/закриває, Warrior ламає |
| Cleric | piece | Speed 4, Strength 2 | 1 AP: лікує сусіднього пораненого |
| Goblin | piece | Speed 4, Strength 1 | втеча дає 2 VP |
| Mekanork | piece | Speed 3, Strength 2 | обертає кімнату в будь-який бік, ігнорує стрілку |
| Thief | piece | Speed 5, Strength 2 | стоїть на ямах; 1 AP — відкрити/закрити ґрати |
| Troll | piece | Speed 2, Strength 4 | 1 AP: регенерує, якщо поранений |
| Wall-Walker | piece | Speed 4, Strength 1 | 1 AP: пройти крізь стіну |
| Warrior | piece | Speed 3, Strength 3 | 1 AP: зламати закриті ґрати |
| Wizard | piece | Speed 4, Strength 1 | левітує над ямами й ворогами; єдиний користувач жезла |
| Armor | pickup | +1 бою в захисті | несеться героєм |
| Sword | pickup | +1 бою в атаці | несеться героєм |
| Fireball Wand | pickup | лише Wizard | 1 AP: прибирає першого героя на лінії зору |
| Rope | pickup | — | перетинати ями й стояти на них |
| Speed Potion | pickup | одноразове | 1 AP: випити → +4 AP |
| Treasure | pickup | +1 VP | при втечі з ним |
| Картки дій ×4 | supply | 2 / 3 / 4 AP … | одна за хід; коли скінчились — усі 4 повертаються |
| Картки бою ×9 | supply | бонус від +0 (бачені +0, +4, +5, +6) | таємна ставка в бою; зіграна — скинута, крім +0 |
| Картки Jump ×3 | supply | — | 1 AP: перестрибнути яму |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(p)` → ТО `custom: «зіграти одну картку дій горілиць; AP = її число»`; ЯКЩО `custom: «перший цикл карток»` → ТО `custom: «число ≤ найбільшого зіграного + 1; перший хід — лише 2»`, після зіграної «4» обмеження знято.
- КОЛИ `turn_end(p)` → ТО `custom: «невикористані AP згорають»`; КОЛИ `counter(action_cards, ==, 0)` → ТО `custom: «усі 4 картки дій повертаються в руку»`.
- КОЛИ `input(reveal, c, room)` → ЯКЩО `custom: «у c прямий доступ до закритої кімнати (зі стартової лінії — дві сусідні)»` → ТО `reveal(room)`, `custom: «відкривач розкладає жетони, а свої предмети за нього ставить суперник»`, −1 AP.
- КОЛИ `input(move, c, path)` → ЯКЩО `custom: «довжина ≤ Speed, лише ортогонально»` and `free(path)` → ТО `move(c, path)`, −1 AP; крізь своїх незранених — можна пройти, не зупинитись; ворог, яма, закриті ґрати, стіна — `block`.
- КОЛИ `input(rotate, c, room)` → ЯКЩО `custom: «c стоїть на шестерні з номером кімнати»` → ТО `rotate(room, 90)` за стрілкою, −1 AP; `custom: «жетони не зсуваються з клітин — обертаються разом із кімнатою»`; 1 AP — одна кімната.
- КОЛИ `input(rotate, mekanork, room)` → ЯКЩО `custom: «на шестерні»` → ТО `rotate(room, ±90)` у будь-який бік.
- КОЛИ `input(attack, c, e)` → ЯКЩО `adjacent(c, e)` → ТО `custom: «обидва таємно кладуть картку бою; Strength + картка (+1 Sword в атаці, +1 Armor у захисті)»`; більше → `set_state(loser, wounded)`; рівність — нічого, атакувальник може витратити ще AP.
- Груповий бій: КОЛИ `input(attack, …)` → ТО `custom: «усі незранені сусіди обох сторін додають Strength; кожна сторона кладе одну картку»`.
- КОЛИ `custom: «поранений програв бій»` → ТО `disappear(c)`, `score(+1)` переможцю.
- КОЛИ `state_on(c, wounded)` → ТО `custom: «не діє, бій 0, але захищається»`; КОЛИ `input(heal, cleric, w)` → ЯКЩО `adjacent(cleric, w)` → ТО `clear_state(w, wounded)`, −1 AP; Troll — сам себе.
- КОЛИ `input(wall_walk, ww)` → ТО `custom: «пройти крізь стіну»`, −1 AP.
- КОЛИ `input(open|close, thief, gate)` → ТО `set_state(gate, open|closed)`, −1 AP; КОЛИ `input(break, warrior, gate)` → ТО `set_cell(gate, broken)`, −1 AP.
- КОЛИ `custom: «рух через яму»` → ЯКЩО `not (custom: «Thief» or has(c, rope) or custom: «Wizard»)` → ТО `block`; картка Jump — `custom: «перестрибнути яму»`, −1 AP.
- КОЛИ `input(fireball, wizard)` → ЯКЩО `has(wizard, wand)` and `line_of_sight(wizard, target)` → ТО `disappear(first_in_line)`, −1 AP.
- Лінія зору: `custom: «не проходить крізь стіни, героїв (живих чи поранених), закриті ґрати; проходить крізь предмети, шестерні, ями»`.
- КОЛИ `input(drink, c, potion)` → ТО `use(c, potion)`, `counter(ap, +4)`.
- КОЛИ `contact(c, item)` → ЯКЩО `custom: «руки вільні»` → ТО `pickup`; `custom: «герой несе один предмет або одного пораненого союзника»`.
- Золоте правило: КОЛИ `custom: «кінець будь-якої дії»` → ЯКЩО `custom: «у клітині > 2 жетонів або 2 незранені герої»` → ТО `custom: «дія нелегальна»`.
- КОЛИ `reach(c, opponent_start_line)` → ТО `disappear(c)`, `score(+1)` (Goblin +2); ЯКЩО `has(c, treasure)` → ТО `score(+1)`.
- КОЛИ `counter(vp, ≥, 5)` → ТО `custom: «активний гравець доходить свій хід»`; більше VP → `win`.

## Керування і ввід
- Настільна: гравець кладе картку дій, оголошує дії по одній і пересуває жетони; бій — одночасне відкриття карток.
- Розстановка: за ширмою 14 жетонів (8 героїв + 6 предметів); 4 героя сорочкою на стартову лінію; решту гравці по черзі кладуть сорочкою в кімнати до їхньої місткості, не дивлячись.
- Обертання — поворот плитки руками на ¼ за стрілкою.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): поле 4×2 кімнат; `pocket` — рука карток дій/бою/Jump (`+ui:card-hand`); `+ui:action-points-left`; лічильник VP обох; `legal-move-highlight` для руху й шестерень; `turn-indicator`.
- `+window:setup-tokens` / `placement-screen` (цифрова версія): вибір 4 стартових героїв і розкладання жетонів по кімнатах.
- `pass-device` (hotseat): ширма між таємними виборами.
- `custom-window` (цифрова версія): одночасний вибір картки бою з відкриттям.
- `end-screen` — VP і переможець; `help-window` — опис героїв і предметів.

## Фічі поза полем
- Доповнення-набори героїв і кімнат: Paladins & Dragons, Forces of Darkness, Mercenaries, Fire and Water, 3/4-Players; Prison — окрема гра (?).
- `+feature:turn-timer-optional` — 2 хвилини на хід.
- Відеогра для PS3 (PSN, 2012), сприйнята погано.

## Варіації й родичі
- Родичі: [Labyrinth](../board-digital/labyrinth.md) (зсув рядів лабіринту замість обертання кімнат), [HeroQuest / Space Hulk](heroquest-space-hulk.md) (кімнати, загін, двері), [Summoner Wars](summoner-wars.md) (таємні картки бою, карткова економіка), [Descent](descent-journeys-in-the-dark.md).
- Осі варіацій:
  - **змінна топологія**: зсув ряду ([labyrinth](../board-digital/labyrinth.md)) / обертання кімнати на шестерні (тут) / нема;
  - **очки дій**: фіксовані / з картки, що повертається циклом (тут) / кубик;
  - **бій**: кубики / таємна ставка картою + стат (тут) / детермінований.

## Цікавинки для курсу
- Обертання підматриці-кімнати на 90° разом зі стінами і жетонами, перерахунок досяжності — 🥉 (поворот координат + BFS).
- Пара кімнат зі спільним номером і протилежними стрілками, дистанційне обертання з шестерні — 📎.
- Картки дій циклом 4 з обмеженням першого циклу — 🌱.
- Таємний бій: Strength + картка, рівність нічия, зіграна картка зникає (крім +0) — 📎 (менеджмент руки суперника).
- Здібності героїв як винятки з правил руху (крізь стіну, над ямою, ґрати) — 📎 за набір.
- Приховане розкладання жетонів, яке розкриває кімната — 🥉 (стан «невідомо» в клітині).

## Мапа на каталог
- Є: `hp-damage` ↔ поранений/знятий · `impassable-cells` · `item-pickup` · `inventory-limit` ↔ один предмет · `line-of-sight-attack` ↔ жезл · `reach-exit` ↔ стартова лінія суперника · `event-points` ↔ VP · `hot-seat` · `pocket` ↔ рука карток · `placement-screen` · `pass-device`.
- **Нема** → пропозиції карток:
  - `+modular-board`, `+rotate-structure`, `+room-reveal`, `+simultaneous-hidden-orders`, `+double-blind-choice`, `+variable-player-powers`, `+carry-object`, `+trap-squares`, `+stack-limit` — уже в корпусі.
  - `+hand-of-cards-cycle` «Картки дій циклом: повертаються, коли скінчились» · game-logic/opponent · 🌱.
  - `+hidden-setup-tokens` «Жетони сорочкою в зонах до відкриття» · entities/state · 📎.
  - `+wall-pass` «Персонаж проходить крізь стіну» · entities/legality · 🌱.
  - `+throw-pit-jump` «Одноразовий стрибок через яму» · entities/legality · 🌱 · слот {uses: 3}.
  - `+escape-to-opponent-edge` «Вихід через край суперника = очки» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:play_card` — зіграти картку з руки (дії → AP, бій → ставка); `+effect:return_hand` — повернути скинуті картки в руку.
- `+effect:rotate_linked` — повернути одну з пари кімнат, вибраних номером шестерні.
- `+cond:on_gear` — герой стоїть на шестерні кімнати; `+cond:direct_access` — герой має прямий доступ до закритої кімнати.
- `+role:card` (з summoner-wars) — картка в руці як сутність.
- `+ui:action-points-left` — залишок AP ходу; `+ui:card-hand` (з summoner-wars).
- `+window:setup-tokens` — розкладання прихованих жетонів; `+feature:turn-timer-optional` — опційний таймер ходу.

## Джерела
- ⭐ [RulesPal: Dungeon Twister rulebook](https://rulespal.com/dungeon-twister/rulebook) — розклад 4×2, 14 жетонів, 16 карток (9 бою, 3 Jump, 4 дій), обмеження першого циклу, обертання з шестерні й парна кімната, 8 героїв зі Speed/Strength, 6 предметів, лінія зору, золоті правила, 5 VP.
- [Wikipedia: Dungeon Twister](https://en.wikipedia.org/wiki/Dungeon_Twister) — автор, Asmodée 2004/2005, список доповнень, PS3-версія 2012.
- YouTube: пошук «Dungeon Twister how to play».

## Непевне
- (?) Розмір кімнати в клітинах (5×5 — з памʼяті); RulesPal каже лише «8 квадратних кімнат».
- (?) Значення четвертої картки дій (5 AP?) і повний розклад карток бою (+0…+6?) — сторінка згадує «2», «3», «4» дії та бій +0, +4, +5, +6.
- (?) Чи дає VP герой, знятий жезлом Fireball.
- (?) Чи можна обертати кімнату, де стоять ворожі герої (заборони в тексті нема).
- Черга: «кімнати обертаються парами в протилежні боки» — точніше: за 1 AP обертається одна кімната, а парні кімнати мають протилежні стрілки.
- (?) Prison — окрема гра чи доповнення: Wikipedia подає як видання серії.
