---
title: Colt Express
slug: colt-express
aka: [Кольт Експрес]
family: program-robots
also: [board-digital]
klass: avatar
axes:
  field: layers
  time: programmed
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2014
platforms: [board, PC, Mac, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Colt_Express", best: true, note: "огляд: фази Schemin'/Stealin', 5 раундів, дії руху/поверху/удару/пострілу/грабунку/маршала, бонус $1000, доповнення"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Colt_Express", note: "автор Christophe Raimbault, Ludonaute, Spiel des Jahres 2015, здібності бандитів, цифрова версія"}
  - {kind: other, url: "https://www.ultraboardgames.com/colt-express/game-rules.php", note: "склад гри, розкладка потяга, хід раунду, підрахунок, нічия"}
  - {kind: other, url: "https://www.ultraboardgames.com/colt-express/action-cards.php", note: "точні ефекти всіх карт дій, лінія вогню на даху, маршал"}
  - {kind: other, url: "https://www.ultraboardgames.com/colt-express/events.php", note: "події кінця раунду й станції"}
  - {kind: other, url: "https://rulespal.com/colt-express/rulebook", note: "типи ходів на картах раунду, 10 карт дій на гравця, номінали здобичі, варіант на 2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=colt+express+how+to+play", note: "пошук; правила за 10 хв"}
stage: v1
coverage: 60
mechanics: [command-program, line-of-sight-attack, item-pickup, thief, hot-seat, event-points, score-records, +card-programming-registers, +shared-program-stack, +face-down-program-cards, +round-card-turn-types, +play-or-draw-choice, +deck-clogging-bullets, +two-level-row-board, +roof-fast-movement, +npc-moved-by-players, +punch-knockback-drop, +end-of-round-events, +most-shots-bonus, +hidden-loot-value, +character-abilities]
proposes: ["+effect:draw_card", "+effect:discard", "+effect:play_card(face)", "+effect:steal", "+effect:drop", "+effect:shuffle_deck", "+trigger:revealed", "+trigger:round_end", "+cond:same_spot(a, b)", "+role:card", "+window:program-stack", "+ui:card-hand", "+ui:round-card", "+ui:loot-tokens", "+feature:character-powers"]
author: opus
date: 2026-11-09
---

# Colt Express — бандити по черзі кладуть карти в одну спільну стопку, а потім стопка розігрується, і плани всіх перемішуються

## Суть
2–6 бандитів грабують потяг на Дикому Заході за 5 раундів. У раунді спершу **планування** (Schemin'): гравці по черзі кладуть карти дій у спільну стопку (або добирають 3 карти), частина ходів — закрито (тунель); потім **виконання** (Stealin'): стопку перевертають і розігрують карту за картою в тому самому порядку. Ти програмуєш свого бандита, знаючи лише частину чужих намірів, а до твоєї карти «рух уперед» хтось уже штовхнув тебе в інший вагон. Перемагає найбагатший, плюс $1000 тому, хто вистріляв найбільше куль.

## Поле і час
- Потяг — ряд з локомотива й одного вагона на гравця (`field: layers`): кожен вагон має **2 рівні** — салон і дах; позиція = (вагон, рівень). Останній вагон — службовий (caboose).
- Рухи різні за рівнями: у салоні — на сусідній вагон, на даху — на 1–3 вагони; постріл у салоні — лише в сусідній вагон, на даху — на будь-яку відстань по лінії вогню.
- Раунд: карта раунду задає кількість і тип ходів → фаза 1 (планування, по колу) → фаза 2 (виконання стопки зверху вниз) → подія раунду. 5 раундів: 4 карти раунду + карта станції наприкінці.
- `time: programmed`: дії виконуються пізніше, ніж задумані, у порядку викладання; посередині — дії суперників.
- Приховане (`info: hidden`): рука, карти «тунелю» сорочкою догори, номінали гаманців (лежать закрито).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бандит | player | (вагон, рівень), здобич, 6 куль, особиста колода 10 карт | виконує свої карти зі спільної стопки |
| Маршал | enemy | лише салон | рухається картами Marshal; бандит у його вагоні тікає на дах і отримує нейтральну кулю |
| Салон вагона | zone | здобич на підлозі | рух на сусідній вагон; грабунок лише тут для салону |
| Дах вагона | zone | — | рух на 1–3 вагони; лінія вогню через дахи |
| Локомотив | zone | сейф, маршал на старті | рахується як вагон; удар з нього — лише назад |
| Службовий вагон (caboose) | zone | — | крайній; удар з нього — лише вперед |
| Гаманець (purse) | pickup | $250–500, номінал закритий | 18 шт.; по $250 — на старті кожному |
| Коштовність (jewel) | pickup | $500 | 6 шт. |
| Сейф (strongbox) | pickup | $1000 | 2 шт.: один у локомотиві, другий за подією «Take It All!» |
| Карта дії | — (`+role:card`) | Move ×2, Change Floor ×2, Fire ×2, Punch ×1, Rob ×2, Marshal ×1 | 10 на гравця |
| Куля (Bullet card) | — (карта) | колір стрільця, номер 1–6 | «мертва» карта в колоді того, в кого влучили |
| Нейтральна куля | — (карта) | 13 шт. | дає маршал і події |
| Карта раунду | — (карта) | послідовність ходів, подія | 7 для 2–4 гравців, 7 для 5–6; ще 3 карти станції |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок раунду»` → ТО кожен `custom: «draw_card(6) з власної колоди»` (Doc — 7); перший гравець відкриває карту раунду.
- КОЛИ `turn_start(bandit)` → ЯКЩО `custom: «хід стандартний»` → ТО `input(play)`: `custom: «play_card(face-up) у спільну стопку»` **або** `custom: «draw_card(3)»`.
- КОЛИ `turn_start(bandit)` → ЯКЩО `custom: «хід-тунель»` → ТО карта кладеться сорочкою догори.
- КОЛИ `turn_start(bandit)` → ЯКЩО `custom: «хід-прискорення»` → ТО `extra_move` — 2 ходи поспіль, на кожному грати або добирати.
- КОЛИ `custom: «хід-розворот»` → ТО `custom: «черга йде проти годинникової, від першого гравця»`.
- КОЛИ `custom: «кінець фази 1»` → ТО `custom: «перевернути стопку без зміни порядку і розігрувати зверху»`; кожна розіграна карта повертається власникові.
- КОЛИ `exec(move)` → ЯКЩО `state(bandit, inside)` → ТО `move(bandit, adjacent_car)`; ЯКЩО `state(bandit, roof)` → ТО `custom: «на 1–3 вагони, напрям і відстань на вибір»`; стояти на місці не можна.
- КОЛИ `exec(change_floor)` → ТО `custom: «салон ↔ дах того ж вагона»`.
- КОЛИ `exec(rob)` → ЯКЩО `count(loot_here, >, 0)` → ТО `pickup(bandit, loot)` на вибір; дах і салон — окремі місця; нема здобичі → нічого.
- КОЛИ `exec(punch)` → ЯКЩО `custom: «same_spot(bandit, target)»` → ТО `custom: «ціль кидає 1 здобич на вибір нападника (гаманець — не дивлячись)»`, `move(target, adjacent_car)` на тому ж рівні.
- КОЛИ `exec(fire)` → ЯКЩО `state(bandit, inside)` і `occupied(adjacent_car_inside, bandit)` → ТО `give(target, bullet_card)` — куля лягає на колоду цілі.
- КОЛИ `exec(fire)` → ЯКЩО `state(bandit, roof)` і `line_of_sight(bandit, target)` → ТО `give(target, bullet_card)`; перший бандит на лінії закриває інших; кілька на одному даху — стрілець обирає.
- КОЛИ `exec(fire)` → ЯКЩО `custom: «ціль на тому ж місці»` або `not has(bandit, bullet_card)` або нема цілі → ТО `block` (куля лишається).
- КОЛИ `exec(marshal)` → ТО `move(marshal, adjacent_car)` у салоні, напрям на вибір гравця; на дах маршал не виходить.
- КОЛИ `contact(bandit, marshal)` (хтось увійшов у вагон маршала або маршал увійшов до когось) → ТО `custom: «бандит тікає на дах»`, `give(bandit, neutral_bullet)`; ЯКЩО `count(neutral_bullets, <, escaping)` → ТО ніхто кулі не отримує.
- КОЛИ `custom: «кінець раунду»` → ТО подія карти раунду: Angry Marshal (кулі тим, хто на даху вагона маршала, маршал крок до хвоста) · Swivel Arm (усі з дахів — на дах caboose) · Braking (усі на дахах — на вагон до локомотива) · Take It All! (другий сейф — у вагон маршала) · Passengers' Rebellion (кожному в салоні — нейтральна куля).
- КОЛИ `custom: «кінець 5-го раунду (станція)»` → ТО подія станції: Pickpocketing (самотній на місці бере гаманець звідти) · Marshal's Revenge (бандит на даху над маршалом втрачає найдешевший гаманець) · Hostage-Taking (кожному в локомотиві чи на його даху — $250).
- КОЛИ `custom: «кінець раунду»` → ТО `custom: «shuffle_deck: усі карти дій + отримані кулі → нова колода»`, перший гравець — наступний ліворуч.
- КОЛИ `game_over` → ТО `score(sum(loot))`; ЯКЩО `custom: «вистріляв найбільше (найменше своїх куль лишилось)»` → ТО `score(+1000)` (нічия — кожному).
- Перемога: найбільше грошей; нічия → менше отриманих куль. Поразки нема.

### Здібності бандитів (база)
- Doc — бере 7 карт замість 6. Ghost — першу карту раунду може класти закрито. Cheyenne — ударом забирає гаманець, який випустила ціль. Django — постріл відкидає ціль на 1 вагон у напрямку пострілу. Belle і Tuco — у джерелах розходяться (див. «Непевне»): «не може бути ціллю, поки є інша» і «стріляє крізь дах свого вагона».

## Керування і ввід
- Фаза 1: на своєму ході — обрати карту з руки і покласти у стопку (закрито / відкрито за картою раунду) або добрати 3.
- Фаза 2: коли відкривається твоя карта — обрати параметри: куди рухатись (1–3 на даху), кого бити / в кого стріляти, яку здобич брати чи вибити, куди вести маршала.
- Цифрова версія: hotseat і онлайн, AI-бандити (?).

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `match-setup` (кількість гравців, AI) → `character-select` (6 бандитів).
- `game-screen`: потяг збоку з двома рівнями, фігурки бандитів і маршала, жетони здобичі (`+ui:loot-tokens`), `+ui:round-card` (схема ходів раунду + подія), `+ui:card-hand` (рука), лічильник куль-циліндра, `turn-indicator`.
- `+window:program-stack` — спільна стопка: відкриті / закриті карти в порядку викладання; у фазі 2 — `instruction-highlight` поточної карти.
- `end-screen` — суми здобичі, бонус Gunslinger, переможець.
- (цифрова версія) `help-window` / `tutorial-window` — правила й навчальна партія (?).
- Переходи: налаштування → раунд (карта раунду → планування → виконання → подія) ×5 → підрахунок.

## Фічі поза полем
- `+feature:character-powers` — у кожного бандита одна асиметрична здібність.
- Варіант на 2–3 гравці: кожен веде двох бандитів зі спільною колодою 11 карт, бере 7.
- Доповнення: Horses & Stagecoach (2015: дилижанс, коні, заручники), Marshal & Prisoners (2016: гравець-маршал, Mei, в'язниця), Bandits (2018), Couriers & Armoured Train (2022: другий потяг, команда на команду), міні: The Time Traveling Car, Cursed Loot та ін.
- Цифрова версія — PC, Mac, Steam, iOS, Android.

## Варіації й родичі
- Родичі в корпусі: `roborally` (таємні регістри, одночасне виконання за пріоритетом), `mechs-vs-minions` (програма в слотах, кооператив), `asteroyds` (програма маневрів під таймером).
- Осі варіацій: **де лежить програма** (особисті регістри — RoboRally / одна спільна стопка — Colt Express); **видимість** (усе закрито до розкриття / відкрито, крім тунелів); **порядок** (за пріоритетом карти / за порядком викладання); **засмічення колоди** (кулі як мертві карти — тут; пошкодження в слоті — MvM).

## Цікавинки для курсу
- Спільна FIFO-стопка команд кількох гравців з виконанням після планування — 🥉 (черга подій, відкладене виконання).
- Карти раунду як скрипт ходів: стандартний / тунель / прискорення / розворот — 📎.
- Двоповерхове 1D-поле з різними правилами руху й пострілу на рівнях — 📎.
- Лінія вогню по дахах, де перший бандит закриває інших — 🌱.
- Кулі як мертві карти в колоді цілі (deck clogging) — 📎.
- NPC-маршал, якого рухають гравці, і примусова втеча на дах — 🌱.
- Удар з вибиванням здобичі й відкиданням у сусідній вагон — 🌱.

## Мапа на каталог
- Є: `command-program` (стопка дій, приблизно) · `line-of-sight-attack` (постріл по дахах) · `item-pickup` (грабунок) · `thief` (удар вибиває здобич) · `hot-seat` · `event-points` (бонус Gunslinger) · `score-records`.
- **Нема** → пропозиції карток:
  - `+card-programming-registers` (з RoboRally) — програма з карт.
  - `+shared-program-stack` «Спільна стопка команд усіх гравців» · game-logic/program · 🥉.
  - `+face-down-program-cards` «Частина команд кладеться закрито» · game-logic/opponent · 🌱.
  - `+round-card-turn-types` «Карта раунду задає типи ходів (закрито, подвійний, розворот)» · game-logic · 📎.
  - `+play-or-draw-choice` «На ході: зіграти карту або добрати 3» · game-logic · 🌱.
  - `+deck-clogging-bullets` «Влучання додає мертву карту в колоду цілі» · entities/state · 📎.
  - `+two-level-row-board` «Ряд вагонів із двома рівнями» · entities/move · 📎.
  - `+roof-fast-movement` «На даху — рух на 1–3, у салоні — на 1» · entities/move · 🌱.
  - `+npc-moved-by-players` «Нейтральний NPC, якого рухають карти гравців» · entities/move · 🌱.
  - `+punch-knockback-drop` «Удар вибиває здобич і відкидає» · entities/combat · 🌱.
  - `+end-of-round-events` «Подія наприкінці раунду з карти» · game-logic · 🌱.
  - `+most-shots-bonus` «Бонус тому, хто вистріляв найбільше» · score · 🌱.
  - `+hidden-loot-value` «Номінал здобичі закритий до кінця» · score · 🌱.
  - `+character-abilities` «Асиметрична здібність персонажа» · entities/state · 📎.

## Пропозиції до словників
- `+effect:draw_card` — добрати N карт з особистої колоди.
- `+effect:discard` — карта йде з руки / стопки.
- `+effect:play_card(face)` — покласти карту у спільну стопку відкрито або закрито.
- `+effect:steal` — забрати здобич з місця / в іншого (Rob, Cheyenne).
- `+effect:drop` — випустити предмет на підлогу клітини.
- `+effect:shuffle_deck` — перемішати колоду разом із доданими картами.
- `+trigger:revealed` — карта розкрилась у фазі виконання.
- `+trigger:round_end` — кінець раунду (події).
- `+cond:same_spot(a, b)` — обидва в одній клітині-рівні (удар).
- `+role:card` — карта як сутність гри.
- `+window:program-stack` — спільна стопка програм з порядком і закритими картами.
- `+ui:card-hand` · `+ui:round-card` · `+ui:loot-tokens`.
- `+feature:character-powers` — асиметричні персонажі.

## Джерела
- ⭐ [Wikipedia: Colt Express](https://en.wikipedia.org/wiki/Colt_Express) — фази раунду, дії, $1000, доповнення.
- [Wikipedia FR: Colt Express](https://fr.wikipedia.org/wiki/Colt_Express) — автор, нагороди, здібності, цифрові платформи.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/colt-express/game-rules.php) · [карти дій](https://www.ultraboardgames.com/colt-express/action-cards.php) · [бандити](https://www.ultraboardgames.com/colt-express/bandits.php) · [події](https://www.ultraboardgames.com/colt-express/events.php) — детальні ефекти й розкладка.
- [RulesPal: rulebook](https://rulespal.com/colt-express/rulebook) — типи ходів раунду, склад колоди, номінали здобичі, варіант на 2.
- YouTube: пошук «colt express how to play».

## Непевне
- (?) Belle і Tuco: Wikipedia FR — Belle «уникає пострілів, якщо поруч інший бандит», Tuco «стріляє вгору/вниз»; UltraBoardGames — навпаки. За памʼяттю правильний варіант FR.
- (?) Що стається з незіграними картами руки наприкінці фази 1 (повертаються в колоду) — у джерелах сформульовано по-різному.
- (?) Розкладка здобичі по вагонах (що надруковано на підлозі кожного вагона) — не звірено.
- (?) Рік і видавець цифрової версії, наявність AI і онлайну — з памʼяті; Steam-пошук «Colt Express» зараз порожній.
- (?) Порядок стрілянини, коли кілька бандитів на одному даху «поруч», і чи блокує маршал лінію вогню — не звірено.
