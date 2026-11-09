---
title: "Ishar: Legend of the Fortress"
slug: ishar
aka: [Ishar, Ishar 1]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1992
platforms: [Amiga, Atari ST, Atari Falcon, MS-DOS, Macintosh]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ishar:_Legend_of_the_Fortress", best: true, note: "суть: до 5 персонажів, симпатії й антипатії, голосування за прийом і вигнання, ланцюг убивств, сейв за 1000 золота"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Ishar:_Legend_of_the_Fortress", note: "FR: голосування при наймі в таверні й у полі, помста друзів жертви, платні сейви лише в Ishar 1"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2020/02/game-358-ishar-legend-of-fortress-1992.html", note: "CRPG Addict: клітинний рух від першої особи як Dungeon Master, бій у реальному часі, стати, навички, ціни, голосування на практиці"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2020/03/ishar-legend-of-fortress-won-with.html", note: "CRPG Addict, фінал: заклинання, алхімія 15 рецептів, тренери, економіка, 5 рунічних табличок, Krogh"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ishar+Legend+of+the+Fortress+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, impassable-cells, hp-damage, inventory-items, item-pickup, hunger-clock, status-effects, unit-xp-skills, round-currency, shop-catalog, teleport, button-toggle, player-death, save-game, map-window, gui-render, +first-person-grid, +party-formation, +party-vote, +member-murder-chain, +paid-save, +alchemy-recipes, +stat-trainer, +sleep-regen]
proposes: ["+trigger:vote(party, proposal)", "+cond:affinity(a, b, op, n)", "+cond:vote_passed", "+effect:recruit(a)", "+effect:dismiss(a)", "+effect:assassinate(a, b)", "+effect:brew(recipe)", "+role:party-member", "+window:tavern-window", "+window:vote-result", "+feature:paid-save", "+card:party-vote", "+card:member-murder-chain"]
author: opus
date: 2026-11-09
---

# Ishar: Legend of the Fortress — блобер у стилі Dungeon Master, де загін сам голосує, кого взяти, а сейв коштує 1000 золота

## Суть
Загін до п'яти персонажів ходить клітинами переважно **відкритого світу** (острів Кендорія) від першої особи й б'ється в реальному часі, як у [Dungeon Master](dungeon-master.md). Своє в ньому — **соціальний шар загону**: кожен персонаж має симпатії й антипатії до інших, прийом і вигнання вирішує **голосування** членів, а неугодного можна наказати вбити — після чого друзі жертви можуть помститися, і ланцюг убивств здатен лишити одного живого. Сейв не безплатний: **1000 золота** з казни загону, тож збереження — економічне рішення.

## Поле і час
- Квадратна сітка, вид від першої особи; загін займає клітину як одна фігура. Повороти — за мануалом на 45° (?), що на відкритій місцевості дезорієнтує.
- Світ: 4 села на природі, 2 міста-«інтер'єри», 2 підземелля, хатини; телепорти між районами.
- Реальний час: голод (запаси їжі), відновлення лише в таверні/сном, бій із кулдауном між ударами.
- Більшість ворогів відроджується (вхід-вихід у місто — фарм золота).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 5 місць у формації, спільне золото й їжа | рухається клітинами як одне ціле |
| Арамір (герой) | player | сила, статура, спритність, інтелект, мудрість, живучість; фізична й ментальна енергія | стартує сам із 2000 золота й мечем; створення персонажа нема |
| Персонаж-найманець | ally | раса/клас, навички (злом замків, орієнтування, перша допомога, зброя 1/2 руки, метання, стрільба, мови), симпатії до інших | голосує, може піти, закохатися, бути вбитим чи вбити |
| Монстр | enemy | — | нападає в реальному часі; з'являється, лише коли дивиться на загін; відроджується |
| Таверна | static | ціни | найм, їжа, ночівля (лікування) |
| Тренер | neutral | ціна | +2 / +1 / 0 до стату (понад 10 майже не росте) |
| Крамниця | static | ціни | зброя, броня, заклинання, реагенти |
| Реагент / порожня колба | pickup | — | алхімія за рецептом (15 зілль) |
| Телепорт | terrain | — | переносить між районами |
| Важелі | switch | 6 | двері-головоломка з послідовністю |
| Отруйний газ | hazard | — | потрібне зілля Apnea |
| Проклята хатина | hazard | — | виснажлива хвороба, якщо не випити зілля заздалегідь |
| Рунічна табличка | pickup | 5 штук | без усіх п'яти Крога не вразити |
| Krogh | boss | — | фінальний ворог; заклинання Anti-Krogh |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step|turn)` → ЯКЩО `free(cell)` → ТО `move(party, dir)` / `face(party, dir)`.
- КОЛИ `input(recruit, npc)` → ТО `custom: «голосують усі члени загону за симпатіями»`; ЯКЩО `custom: «голосування пройшло»` → ТО `custom: «найманець приєднується»`; інакше `message(«відмова»)`.
- КОЛИ `input(dismiss, member)` → ТО те саме голосування; ЯКЩО пройшло → `custom: «персонаж іде з загону»`.
- КОЛИ `input(assassinate, a, b)` → ТО `custom: «a вбиває b»`, `disappear(b)`; КОЛИ `died(b)` → ЯКЩО `custom: «у b є друзі в загоні»` → ТО `custom: «друг мститься вбивці»` (ланцюг).
- КОЛИ `input(save)` → ЯКЩО `counter(gold, >=, 1000)` → ТО `currency(−1000)`, `custom: «записати гру»`; інакше `block`.
- КОЛИ `in_range(monster, party, 1)` → ТО `custom: «обмін ударами в реальному часі з кулдауном»`, `damage(member, n)`.
- КОЛИ `input(attack, member)` → ЯКЩО `custom: «кулдаун минув»` → ТО `damage(monster, n)`.
- КОЛИ `input(cast, spell)` → ЯКЩО `custom: «вистачає ментальної енергії»` → ТО `custom: «ефект заклинання»` (Lightning — шкода всім видимим ворогам; Healing; Mental Shield; Invisible Party; Resurrection…).
- КОЛИ `hp_zero(member)` → ТО `custom: «персонаж гине»`; КОЛИ `all_gone(member)` → ТО `lose`.
- КОЛИ `timer(every)` → ТО `counter(food, −1)` (?); ЯКЩО `counter(food, <=, 0)` → `custom: «виснаження»` (?).
- КОЛИ `input(sleep_at_tavern)` → ЯКЩО `counter(gold, >=, price)` → ТО `currency(−price)`, `heal(party, all)`.
- КОЛИ `input(train, stat)` → ТО `currency(−price)`, `custom: «стат +2 / +1 / 0»`.
- КОЛИ `input(brew, recipe)` → ЯКЩО `has(party, flask)` і `has(party, reagents)` → ТО `give(party, potion)`.
- КОЛИ `enter(party, teleporter)` → ТО `teleport(party, …)`.
- КОЛИ `enter(party, gas)` → ЯКЩО `not state(party, apnea)` → ТО `damage(party, n)` (?).
- КОЛИ `custom: «важелі в правильній послідовності»` → ТО `set_cell(door, open)`.
- КОЛИ `died(krogh)` → ТО `win` (потрібні 5 рунічних табличок і Anti-Krogh).

## Керування і ввід
- Мишею клікають кнопки руху, атаки кожного персонажа, меню дій; кожен клік має клавіатурний відповідник (F-клавіші для атак).
- Меню дій загону: найняти / вигнати / убити члена, сейв, мапа Кендорії, алхімія, сон.

## Вікна, меню, HUD
- `game-screen`: 3D-вид від першої особи + `party-portraits` з ментальною й фізичною енергією, кнопки атаки й заклинань, інвентар.
- `custom-window` голосування — хто «за», хто «проти» прийому чи вигнання.
- `tavern-window` — найм, їжа, ночівля; `shop-window` — зброя, броня, заклинання, реагенти.
- `map-window` — мапа острова (без позначки поточного місця).
- `save-slots` за плату; `end-screen`.

## Фічі поза полем
- `save-game` за 1000 золота (лише в Ishar 1; в Ishar 2 — безплатно).
- Прогресія: рівні до 10 (росте переважно HP), тренери статів, купівля заклинань.
- Нема створення персонажа, автомапи й undo.

## Варіації й родичі
- Серія: Crystals of Arborea (1990, не від першої особи) → **Ishar 1** (1992) → Ishar 2: Messengers of Doom (1993: архіпелаг, день/ніч і закриті вночі крамниці, автомапа, кнопка «вбити», безплатні сейви) → Ishar 3: The Seven Gates of Infinity (1994: «відкриті» мапи насправді лабіринти; обов'язкові найманці, що можуть заблокувати гру голосуванням).
- Родичі: [Dungeon Master](dungeon-master.md), [Eye of the Beholder](eye-of-the-beholder.md), [Bloodwych](bloodwych.md) (діалоги з найманцями), [Legend of Grimrock](legend-of-grimrock.md).
- Осі варіацій: **загін** (сталий / наймати й виганяти / голосування членів) · **сейв** (вільний / за гроші / лише в точках) · **простір** (підземелля / відкритий світ на сітці).

## Цікавинки для курсу
- Голосування загону за матрицею симпатій (поріг, вето) — 📎.
- Ланцюг помсти: граф дружби, каскад смертей після вбивства — 📎.
- Сейв як витрата ресурсу — 🌱.
- Тренер з бюджетом і спадною віддачею (+2/+1/0) — 🌱.
- Алхімія за рецептами з невідомими назвами (частковий словник-перекладач) — 📎.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`, `impassable-cells`; `hp-damage`; `inventory-items`, `item-pickup`; `hunger-clock` ↔ їжа; `status-effects` ↔ хвороба, закоханість; `unit-xp-skills` ↔ рівні й навички; `round-currency` + `shop-catalog`; `teleport`; `button-toggle` ↔ важелі; `player-death`; `save-game`; `map-window`; `gui-render`.
- **Нема** → пропозиції карток:
  - `+first-person-grid`, `+party-formation`, `+sleep-regen` (Dungeon Master).
  - `+party-vote` «Члени загону голосують за прийом / вигнання» · entities/state · 📎 · слот {threshold}.
  - `+member-murder-chain` «Вбивство члена загону і помста друзів» · entities/state · 📎.
  - `+paid-save` «Збереження коштує ресурс» · game-logic/save · 🌱.
  - `+alchemy-recipes` «Зілля з реагентів за рецептом» · entities/state · 📎.
  - `+stat-trainer` «Купити +стат зі спадною віддачею» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:vote(party, proposal)` — запуск голосування (найм, вигнання).
- `+cond:affinity(a, b, op, n)` — симпатія персонажа до іншого; `+cond:vote_passed`.
- `+effect:recruit(a)`, `+effect:dismiss(a)`, `+effect:assassinate(a, b)` — зміни складу загону; `+effect:brew(recipe)` — алхімія.
- `+role:party-member` — член загону з власною волею (уже пропонувався з Dungeon Master).
- `+window:tavern-window`, `+window:vote-result`.
- `+feature:paid-save` — платне збереження.
- `+card:party-vote`, `+card:member-murder-chain`.

## Джерела
- ⭐ [Wikipedia: Ishar: Legend of the Fortress](https://en.wikipedia.org/wiki/Ishar:_Legend_of_the_Fortress) — загін до 5, симпатії, голосування, убивства й ланцюг, сейв за 1000 золота, платформи, дати.
- [Wikipedia FR](https://fr.wikipedia.org/wiki/Ishar:_Legend_of_the_Fortress) — голосування при наймі в таверні й у полі, помста друзів, відмінності Ishar 2/3.
- [CRPG Addict: Game 358](https://crpgaddict.blogspot.com/2020/02/game-358-ishar-legend-of-fortress-1992.html) — «tile-based, first-person gameplay similar to Dungeon Master», стати й навички, ціни, бій у реальному часі.
- [CRPG Addict: Won!](https://crpgaddict.blogspot.com/2020/03/ishar-legend-of-fortress-won-with.html) — заклинання, алхімія, тренери, економіка, фінал.
- YouTube: пошук «Ishar Legend of the Fortress gameplay».

## Непевне
- (?) Поворот на 45° — з коментаря читача CRPG Addict з посиланням на мануал; сам мануал не відкривав.
- (?) Розкладка формації (2+3 чи інша) і чи впливає вона на те, хто б'є впритул.
- (?) Темп голоду, чи шкодить газ без зілля, чи можна відмовитись від голосування — деталі не перевірено.
- (?) Як саме рахуються голоси (більшість, одностайність, вага симпатій).
