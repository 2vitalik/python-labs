---
title: Metal Gear Acid
slug: metal-gear-acid
aka: [Metal Gear Ac!d, メタルギア アシッド, MGA, Active Command Intelligence Duel]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2004
platforms: [PSP, mobile (Java ME, 2008)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Metal_Gear_Acid", best: true, note: "картки як дія і рух, рука 6, 3 клітини руху з карти, вартість карти відсуває наступний хід, Link Battle"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/メタルギアアシッド", note: "JA: колода 30–40, типи карт, 2 дії Снейка / 3 Теріко, +2 карти на хід, +10 вартості за перетасування, статуси, вартові із зором"}
  - {kind: other, url: "https://www.supercheats.com/psp/walkthroughs/metalgearacid-walkthrough04.txt", note: "FAQ: USE/EQUIP/MOVE, слоти екіпіровки 2/4/9, набої того ж калібру, REA 50 %, COST → черга, оцінки S/A/B/C"}
  - {kind: other, url: "https://superjumpmagazine.com/the-legacy-of-metal-gear-acid-shinta-nojiris-card-based-battler", note: "есей: карта — рух, дія чи скид; камери, тривоги, стук для приманки, картки за очки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Metal_Gear_Acid_2", note: "сиквел 2005: 565 карт, порядок за накопиченою вартістю, вогонь прикриття, підбір на ходу, Solid Eye"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Metal+Gear+Acid+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, ai-opponent, enemy-patrol, status-effects, key-and-door, item-pickup, shop-between-levels, sequential-levels, game-screen, end-screen, +deck-draw, +deck-builder, +card-as-move, +time-track-turns, +action-points, +equip-loadout, +ammo-limit, +reaction-attack, +vision-cone, +alert-phases, +noise-lure, +hold-up-from-behind, +fire-spread, +deck-reshuffle-penalty, +victory-rank, +auto-deck, +local-wireless-versus]
proposes: ["+trigger:card_played", "+trigger:deck_empty", "+trigger:spotted", "+effect:draw_card", "+effect:reshuffle", "+effect:delay_turn", "+effect:alert", "+ui:card-hand", "+ui:turn-order-bar", "+window:deck-builder", "+card:card-as-move"]
author: opus
date: 2026-11-09
---

# Metal Gear Acid — стелс-тактика на картах: кожна карта — або дія, або крок, а її вартість відсуває твій наступний хід

## Суть
Покрокова тактика Konami (реж. Shinta Nojiri) для PSP: Снейк і напарниця Теріко пробираються сітковою мапою бази, а всі дії йдуть з **руки карт** зі зібраної колоди. Кожну карту можна зіграти як ефект (USE), надіти (EQUIP) або **спалити на рух** (MOVE, зазвичай 3 клітини). Вартість (COST) зіграних карт накопичується і визначає, коли персонаж походить знову: дешеві ходи — частіші ходи. Вартові патрулюють із секторами зору; помічений Снейк спричиняє тривогу й підкріплення, тож стелс — головна тактика.

## Поле і час
- Сіткова арена (3D-мапа з квадратними клітинами; висоти й укриття — (?)); камера вільна, є вигляд згори для перевірки зору вартових.
- Час: черга за COST — після ходу вартість персонажа зростає на суму зіграних карт, усім вона спадає з однаковою швидкістю; ходить той, у кого COST досяг 0. Біля кожного персонажа — номер у черзі.
- Хід персонажа: кілька дій (Снейк — 2, Теріко — 3, карта Action + — до 4); кожна карта — одна дія. Якщо поруч нема ворогів, COST падає до 0 автоматично.
- Інформація часткова: порядок колоди невідомий, сектори зору видно лише в окремому огляді.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Снейк | player | HP, COST, дії 2, слоти екіпіровки 2→4→9 | грає карти: USE / EQUIP / MOVE |
| Теріко | ally | HP, COST, дії 3 | керується гравцем, своя черга |
| Вартовий | enemy | HP, напрям погляду, маршрут патруля | бачить сектором; помітивши — тривога, кличе інших |
| Патрульний бот | enemy | великий радіус виявлення | як вартовий |
| Камера | enemy | — | спостерігає; постріл звичайною зброєю здіймає тривогу |
| Бос | boss | HP, власна колода й екіпіровка | мета частини місій |
| Солдат ACUA | enemy | — | ворог пізніх етапів |
| Карта WEAPON (USE / EQUIP) | object | COST, калібр, набої, REA | USE — одноразово; EQUIP — стріляє, коли заряджена картою того ж калібру; авто-контратака |
| Карта ACTION | object | COST | приймання (удар з розвороту), Equipment LV.2/3, Action + |
| Карта ITEM | object | COST | раціон, аптечка, бронежилет |
| Карта SUPPORT | object | COST, REA | ухил, підсилення, зняття статусу, зниження COST |
| Карта CHARACTER | object | COST | персонажі серії Metal Gear та ігор Кодзіми |
| Двері безпеки / кольорові двері | gate | рівень ключа / колір | відкриваються карткою-ключем LV.1/2 або терміналом |
| Термінал | switch | — | відкриває двері |
| Пак карт, зброя на полі | pickup | — | підбирається на мапі |
| Вибухова бочка, міна | hazard | — | вибух / шкода (?) |
| Ціль (bullseye) | zone | — | точка, куди треба дійти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «перетасувати колоду, взяти 6 карт»`.
- КОЛИ `turn_start(snake)` → ЯКЩО `not first_time` → ТО `custom: «добрати 2 карти»`.
- КОЛИ `input(card, use)` → ТО `custom: «ефект карти»`, `counter(cost[snake], +card_cost)`, `counter(actions, -1)`.
- КОЛИ `input(card, move)` → ТО `custom: «рух до 3 клітин (деякі карти — 6 і більше)»`, `counter(cost[snake], +card_cost - 1)` (за FAQ), `counter(actions, -1)`.
- КОЛИ `input(card, equip)` → ЯКЩО `custom: «є вільний слот (2; 4 після Equipment LV.2; 9 після LV.3)»` → ТО `set_state(snake, equipped)`.
- КОЛИ `input(fire, equipped_weapon, target)` → ЯКЩО `custom: «зіграно WPN-карту того ж калібру»` і `in_range(snake, target, range)` → ТО `damage(target, n)` × кількість набоїв карти.
- КОЛИ `input(attach, card, equipped_weapon)` → ТО `custom: «модифікатор зброї (Aim, Sniper Wolf, Hold Up)»`.
- КОЛИ `input(hold_up, target)` → ЯКЩО `custom: «Снейк позаду цілі»` → ТО `stun(target, n)` (?), `custom: «рівень екіпіровки −1»`.
- КОЛИ `counter(actions, ==, 0)` → ТО `end_turn`.
- КОЛИ `tick` → ТО `counter(cost[all], -1)`; КОЛИ `counter(cost[x], ==, 0)` → ТО `custom: «хід персонажа x»` — менша вартість ходить раніше.
- КОЛИ `custom: «колода скінчилась»` → ТО `counter(cost[snake], +10)`, `custom: «скид перетасовано в нову колоду»`.
- КОЛИ `custom: «поруч нема ворогів»` → ТО `set_value(cost[snake], 0)`.
- КОЛИ `custom: «атака по персонажу»` → ЯКЩО `has(target, reaction_card)` і `prob(REA)` (бронежилет, Front Evade — 50 %) → ТО `block`, `custom: «безкоштовна контратака»`; екіпірована зброя після реакції `disappear`.
- КОЛИ `line_of_sight(guard, snake)` → ЯКЩО `custom: «Снейк у секторі за напрямком погляду»` → ТО `custom: «тривога: знак оклику, виклик інших вартових»`, `spawn(guard)` (?).
- КОЛИ `input(knock)` → ТО `custom: «вартовий іде на звук»`.
- КОЛИ `custom: «постріл у камеру звичайною зброєю»` → ТО `custom: «тривога сусідніх вартових»`.
- КОЛИ `input(phase_down)` → ТО `custom: «фаза тривоги −1 рівень»`.
- КОЛИ `input(m9, target)` → ТО `set_state(target, sleep)` — не діє певну кількість COST.
- КОЛИ `custom: «рука стала порожньою після падіння»` → ТО `set_state(unit, stun)`.
- КОЛИ `custom: «минула 1 одиниця COST»` → ЯКЩО `state(unit, bleeding)` → ТО `damage(unit, 5)`; після 50 сумарно — `clear_state(unit, bleeding)`.
- КОЛИ `custom: «минула 1 одиниця COST»` → ЯКЩО `state(unit, burning)` → ТО `damage(unit, 10)`, `custom: «вогонь перекидається на сусідніх персонажів»`.
- КОЛИ `contact(snake, door)` → ЯКЩО `has(snake, card_key)` → ТО `custom: «двері відчиняються»`; інакше `block`.
- КОЛИ `enter(snake, card_pack)` → ЯКЩО `custom: «рух закінчився на клітині предмета»` → ТО `pickup(snake, card_pack)` (в Acid 2 — підбір на ходу).
- КОЛИ `reach(snake, bullseye)` або `hp_zero(boss)` → ТО `win`.
- КОЛИ `hp_zero(all_players)` → ТО `lose`.
- КОЛИ `level_end` → ТО `custom: «оцінка S/A/B/C за виявленнями, сумарним COST і вбивствами»`, `give(snake, cards)` — S 3 карти, A 2, B 1; `currency(+pts)`.
- Link Battle: КОЛИ `counter(diskettes, ==, quota)` → ТО `win`; дискети можна вкрасти в суперника.
- Перемога: ціль місії (дійти до точки, знищити боса) · Поразка: HP усіх підконтрольних 0 · Рахунок: оцінка місії + очки на картки.

## Керування і ввід
- Курсор на карті руки → USE / EQUIP / MOVE; при MOVE — вибір клітини в межах руху карти; при USE — ціль у межах дальності.
- Командне меню відкривається, коли дії скінчились (REST 0/2), або раніше кількома натисканнями X.
- Вільна камера й огляд згори з курсором на вартовому — подивитися його сектор зору.

## Вікна, меню, HUD
- `game-screen`: 3D-мапа з сіткою; HUD — `+ui:card-hand` (рука до 6+), `hp-bar`, COST персонажа, `+ui:turn-order-bar` (колонка з номерами черги), `action-points` (REST x/2), `equipment-slots`.
- `+window:deck-builder` (Intermission): колода 30–40 карт, режим AUTO для новачків; `shop-window` — карти за очки (pts).
- `dialogue-window` — брифінги й сюжет; `custom-window` — опис карти.
- `end-screen` — оцінка місії й нагорода картками; поразка — game over (?).
- Link Battle: `lobby-window` для бездротового зʼєднання двох PSP (?).

## Фічі поза полем
- `levels-sequential`: місії сюжету; повернення на старі етапи по предмети для наступних.
- Колекціонування й конструювання колоди (~200 карт у грі; у сиквелі 565): `+deck-builder`, `+auto-deck`; максимальний розмір колоди росте з прогресом.
- Нагорода за оцінку — паки карт; магазин за очки місій.
- `mode-versus`: Link Battle по Wi-Fi ad hoc — зібрати дискети раніше суперника.
- Сиквел Acid 2: продаж зайвих карт, Arena, туторіал, Solid Eye 3D.

## Варіації й родичі
- **Metal Gear Acid 2** (2005): 565 карт; черга — за накопиченою вартістю (хто має менше, той ходить); вогонь прикриття від союзника позаду ворога; проходження крізь двері без зупинки й підбір предметів на ходу; режими Arena, Sneaking, Elimination; стереокартонка Solid Eye.
- Metal Gear Acid Mobile (Glu, 2008) — версія для телефонів.
- Родичі в корпусі: [card-hunter](card-hunter.md) і [gloomhaven](gloomhaven.md) (карти як дії), [invisible-inc](invisible-inc.md) (стелс-тактика з тривогою), [final-fantasy-tactics](final-fantasy-tactics.md) (черга за вартістю дії), [yggdra-union](yggdra-union.md) (карта задає рух).
- **Осі варіацій**: звідки рух — стат юніта / карта як рух / очки дії · черга — сторони по черзі / шкала часу за вартістю дій · виявлення — нема / сектор зору / радіус бота · покарання за порожню колоду — поразка (Yggdra) / +вартість і перетасування (MGA).

## Цікавинки для курсу
- Карта з трьома режимами (ефект / екіпірування / рух на 3) — 📎.
- Черга за накопиченою вартістю: зіграні карти відсувають наступний хід — 🥉 (пріоритетна черга за COST).
- Сектор зору вартового за напрямком погляду + тривога з підкріпленням — 🥉.
- Колода, рука 6, добір 2 за хід, перетасування зі штрафом +10 — 📎.
- Зброя-слот + набої картою того ж калібру + реакція REA з руйнуванням зброї — 🥉.
- Статуси, що тікають «за одиницю вартості» (кровотеча 5, горіння 10 з поширенням) — 📎.
- Оцінка місії за виявленнями, сумарним COST і вбивствами — 🌱.
- Автозбирач колоди (AUTO) під стиль гри — 🥈.

## Мапа на каталог
- Є: `hp-damage`; `ai-opponent`; `enemy-patrol` ↔ маршрути вартових; `status-effects` ↔ сон, оглушення, кровотеча, горіння; `key-and-door` ↔ картки-ключі й кольорові двері; `item-pickup` ↔ паки карт і зброя на мапі; `shop-between-levels` ↔ карти за очки; `sequential-levels`; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+deck-draw`, `+deck-builder`, `+time-track-turns`, `+action-points`, `+equip-loadout`, `+ammo-limit`, `+reaction-attack`, `+vision-cone`, `+noise-lure`, `+fire-spread` — уже в корпусі.
  - `+card-as-move` «Будь-яку карту можна спалити на рух» · entities/move · 📎 · слот {move: 3|6}.
  - `+alert-phases` «Фази тривоги з підкріпленням і зниженням» · game-logic/waves · 🥉.
  - `+hold-up-from-behind` «Дія лише зі спини цілі» · entities/combat · 🌱.
  - `+deck-reshuffle-penalty` «Колода скінчилась → штраф і перетасування» · game-logic/economy · 🌱.
  - `+victory-rank` «Оцінка місії за умовами» · game-logic/score · 🌱 (як у Rondo of Swords).
  - `+auto-deck` «Автозбір колоди» · game-logic/economy · 🥈.
  - `+local-wireless-versus` «Гонка двох гравців по локальному звʼязку» · game-logic/opponent · 🥈.

## Пропозиції до словників
- `+trigger:card_played` — зіграно карту (уже пропоновано в корпусі).
- `+trigger:deck_empty` — колода скінчилась (уже пропоновано).
- `+trigger:spotted` — вартовий помітив гравця (уже пропоновано).
- `+effect:draw_card` · `+effect:reshuffle` — добір і перетасування (уже пропоновано).
- `+effect:delay_turn` — відсунути наступний хід сутності на N (тут — COST карти; уже пропоновано).
- `+effect:alert` — підняти/знизити фазу тривоги (уже пропоновано).
- `+ui:card-hand` · `+ui:turn-order-bar` — рука карт і колонка черги (уже пропоновано).
- `+window:deck-builder` — збирання колоди між місіями (уже пропоновано).
- `+card:card-as-move` — механіка, якої в каталозі нема.

## Джерела
- ⭐ [Wikipedia: Metal Gear Acid](https://en.wikipedia.org/wiki/Metal_Gear_Acid) — карти як дія й рух, рука 6, рух 3 (6+), вартість → наступний хід, приклад «COST 10 ходить раніше за 15», зброя з картами того ж калібру, Link Battle.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/メタルギアアシッド) — колода 30–40, типи WEAPON/ACTION/ITEM/CHARACTER/SUPPORT, 2/3 дії, +2 карти на хід, +10 COST за перетасування, сон/оглушення/кровотеча/горіння, вартові й тривога, поразка.
- [SuperCheats FAQ](https://www.supercheats.com/psp/walkthroughs/metalgearacid-walkthrough04.txt) — USE/EQUIP/MOVE, слоти 2/4/9, REA 50 %, COST спадає для всіх однаково, COST → 0 без ворогів, оцінки S/A/B/C.
- [SuperJump: есей](https://superjumpmagazine.com/the-legacy-of-metal-gear-acid-shinta-nojiris-card-based-battler) — «спалити на рух, зіграти дію або скинути», камери, тривоги, стук-приманка, картки за очки.
- [Wikipedia: Metal Gear Acid 2](https://en.wikipedia.org/wiki/Metal_Gear_Acid_2) — відмінності сиквела.
- YouTube: пошук «Metal Gear Acid gameplay».

## Непевне
- (?) «MOVE коштує COST карти мінус 1» — лише з FAQ; Wikipedia каже просто «вартість переходить до гравця».
- (?) Фази тривоги (Alert / Evasion / Caution?) і що саме дає тривога — підкріплення, переслідування; FAQ лише згадує Phase Down.
- (?) Чи мапа має висоти/укриття і як рахується лінія зору через перешкоди.
- (?) Чи Теріко керується гравцем повністю з першої місії; ліміт руки; що дає hold-up (оглушення чи полон).
- (?) Вибухові бочки й міни — механіка шкоди не описана.
