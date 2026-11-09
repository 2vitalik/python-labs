---
title: Tactics Ogre
slug: tactics-ogre
aka: ["Tactics Ogre: Let Us Cling Together", "Tactics Ogre Reborn", LUCT, TO]
family: tactics
also: []
klass: figure
axes:
  field: iso
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1995
platforms: [SNES, Saturn, PS1, PSP, PC, PS4, PS5, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tactics_Ogre", best: true, note: "ізометрична сітка з висотою, WT-черга за вагою й спритністю, Law/Neutral/Chaos, Chaos Frame, таро, Persuade"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tactics_Ogre:_Let_Us_Cling_Together_(2010_video_game)", note: "ремейк 2010 і Reborn 2022: Chariot — перемотка на 50 ходів, World, MP від нуля, крафт"}
  - {kind: other, url: "https://finalweapon.net/2022/08/25/tactics-orge-reborn-details/", note: "Reborn: RT-черга, 8 стихій, умова перемоги — убити конкретного юніта"}
  - {kind: other, url: "https://push.cx/game-influences-tactics-ogre", note: "висота дає лучникам дальність і шкоду; 4 слоти спорядження"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Tactics+Ogre+Reborn"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tactics+Ogre+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [height-levels, hp-damage, melee-vs-ranged, floor-types, impassable-cells, legal-move-highlight, threat-range, status-effects, permadeath, unit-xp-skills, inventory-items, shop-between-levels, world-map, rewind, save-game, hot-seat, codex-window, +facing-hit-bonus, +initiative-queue, +weight-speed, +elemental-affinity, +recruit-talk, +world-alignment, +death-countdown, +card-drop-buff, +leader-death-lose, +branching-story]
proposes: ["+trigger:attacked", "+trigger:round_start", "+cond:height_diff", "+cond:element", "+effect:wait_add", "+effect:recruit", "+effect:rewind_turns", "+ui:turn-order-list", "+ui:height-indicator", "+ui:hit-chance", "+window:warren-report", "+window:chariot-timeline", "+window:formation-screen", "+window:class-change", "+feature:route-revisit", "+axis:turn-structure:wait-time"]
author: opus
date: 2026-11-09
---

# Tactics Ogre — ізометрична тактика, де вага спорядження сповільнює чергу, а вибір на розвилці сюжету змінює армію

## Суть
Покрокова тактична RPG на ізометричному полі з висотою: загін до 10 бійців проти ворога, ходи кожного юніта окремо в черзі, яку визначає **WT (Wait Turn)** — що важче спорядження і нижча спритність, то рідше ходиш. Висота дає лучникам дальність і шкоду, рельєф і погода змінюють рух. Головний герой може **переконати** ворожого юніта перейти на свій бік, а загибель героя — кінець гри. Сюжет розгалужується на гілки Law / Neutral / Chaos за рішеннями героя, і прихований Chaos Frame рахує, як фракції ставляться до нього. Ремейк Let Us Cling Together (2010) додав **Chariot** — перемотку бою на 50 ходів назад.

## Поле і час
- Невелика мапа в діагональній (ізометричній) проєкції; клітини — квадратна сітка з різною висотою. Ремейк дає перемкнутись на вид згори з пласким рельєфом.
- Черга без поперемінних фаз («Non-Alternate Turn System»): кожен юніт, і свій, і ворожий, ходить, коли його WT дозволяє; дія змінює, скільки WT він набере. У Reborn система зветься RT (Recovery Time), момент ходу — AT.
- Хід юніта: рух на кілька клітин, потім атака / заклинання / предмет / особливий прийом (або лише одне), вибір напрямку наприкінці (?).
- Погода й місцевість змінюють рух і дії; на світовій мапі кожен перехід = день і нова погода.
- Інформація відкрита; випадковість — шанси влучання, дроп карт таро, зміна дій ворога при перемотці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Денам (лідер) | piece | клас, стихія, світогляд, вміння Persuade | загибель = кінець гри; може переконати ворога |
| Юніт загону | piece | клас, рівень, HP/MP, STR/AGI/INT…, вага спорядження, стихія, світогляд | рух → дія; WT залежить від ваги й спритності |
| Ворожий юніт | enemy | те саме | ШІ; може бути переконаний; лідер ворога — часто ціль місії |
| Нежить (скелет, привид) | enemy | — | повертається, доки не вигнано (?) |
| Клас (Knight, Archer, Wizard, Cleric, Berserker…) | static | зброя, броня, заклинання, ріст характеристик | розвивається боями; ремейк — клас окремо від юніта |
| Карта таро | pickup | ефект | падає з поверженого ворога; тимчасовий бонус юніту, що підібрав |
| Мішечок з предметами | pickup | — | лишається на клітині; після перемоги можна зібрати |
| Висота (уступ, пагорб, стіна) | terrain | рівень | підйом дорожчий; лучник згори бʼє далі й сильніше |
| Вода, болото, сніг… | terrain | ціна руху | місцевість і погода змінюють рух і дії |
| Перешкода (дерево, будинок) | static | — | непрохідна; може закривати постріл (?) |
| Погода (дощ, сніг, вітер) | zone | — | модифікатор мапи на бій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «тік черги»` → ТО `custom: «кожен юніт набирає WT/RT; хід дістає той, чий лічильник готовий»`; швидкість набору = f(спритність, вага спорядження).
- КОЛИ `turn_end(unit)` → ТО `custom: «наступне очікування = база + вартість дій (рух і атака — більше, пропуск — менше)»`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «шлях у межах руху класу з урахуванням висоти»` and `free(cell)` → ТО `move(unit, cell)`; кожен рівень підйому понад перший — +1 до ціни (?).
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, range(a))` and `prob(шанс)` → ТО `damage(n)`; шкода й шанс залежать від висоти, стихії, напрямку удару.
- КОЛИ `input(shoot, archer, b)` → ЯКЩО `custom: «лучник вище за ціль»` → ТО `custom: «більша дальність і шкода»`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `facing(b, away from a)` → ТО `custom: «вищий шанс влучання (спина > бік > фронт)»` (?).
- КОЛИ `input(attack, a, b)` → ЯКЩО `same(a.element, b.weakness, element)` → ТО `custom: «бонус стихії»`; збіг стихії юніта й зброї/магії підсилює.
- КОЛИ `input(cast, unit, spell)` → ЯКЩО `has(unit, MP ≥ cost)` → ТО `custom: «ефект заклинання»`; у ремейку MP починається з 0 і накопичується протягом бою.
- КОЛИ `input(persuade, leader, enemy)` → ЯКЩО `prob(p)` → ТО `set_side(enemy, player)`.
- КОЛИ `hp_zero(unit)` → ЯКЩО `same(unit, leader, role)` → ТО `lose` (повернення до сейву).
- КОЛИ `hp_zero(unit)` → ТО `set_state(unit, down, 3 turns)`; ЯКЩО `custom: «не воскрешено вчасно»` → ТО `disappear_a` назавжди (?).
- КОЛИ `died(enemy)` → ЯКЩО `prob(p)` → ТО `spawn_at(tarot_card, cell)`; КОЛИ `contact(unit, tarot_card)` → ТО `pickup`, `set_state(unit, buff, short)`.
- КОЛИ `died(target_unit)` → ЯКЩО `custom: «умова місії — убити цього юніта»` → ТО `win`, навіть якщо інші вороги живі.
- КОЛИ `custom: «перемога в бою»` → ТО `give(units, xp)`, `custom: «рівень класу; очки вмінь (ремейк)»`.
- КОЛИ `input(chariot, n)` → ЯКЩО `custom: «n ≤ 50 ходів назад»` → ТО `custom: «повернути бій до стану n ходів тому»`; ворог після перемотки може діяти інакше (випадковий елемент).
- КОЛИ `custom: «рішення на сюжетній розвилці»` → ТО `custom: «гілка Law / Neutral / Chaos; змінюються союзники й місії»`.
- КОЛИ `custom: «дії героя щодо фракцій»` → ТО `counter(chaos_frame, ±n)` (прихований; визначає кінцівку).
- КОЛИ `game_start` → ТО `custom: «анкета з питань-таро задає світогляд і стартові характеристики героя»`.
- КОЛИ `input(class_change, unit, class)` → ЯКЩО `custom: «вимоги класу виконано»` → ТО `transform(unit, class)`.
- Перемога: умова місії (часто вбити лідера ворога або всіх) · Поразка: загибель Денама / усіх · Рахунок: —; кінцівок до 8.

## Керування і ввід
- Курсор по клітинах: вибір юніта, коли настала його черга → підсвітка досяжних → клітина → меню дії (Attack, Magic, Item, Special, Persuade, Wait) → підсвітка цілей з прогнозом шансу й шкоди → вибір напрямку стояння (?).
- Обертання/перемикання камери; у ремейку — вид згори.
- Chariot — окреме меню зі шкалою ходів для перемотки.
- Training mode: гравець керує обома сторонами; на SNES — двоє гравців у тренуванні.

## Вікна, меню, HUD
- `main-menu`: New Game (анкета-таро → імʼя, день народження), Continue → `save-slots`, Options → `settings-window`.
- `map-window` — світова мапа з містами й маршрутами; переходи = дні, погода.
- `formation-screen` — вибір до 10 юнітів з армії (до 30) і розстановка перед боєм.
- `game-screen`: ізометричне поле; `turn-order-list` (черга WT/RT); `height-indicator` клітини; портрет і `stat-panel` активного (HP, MP, WT, стихія); `legal-move-highlight`, `threat-range`; `hit-chance` при виборі цілі; `message-log`.
- `class-change`, `inventory-window` (спорядження з вагою), `shop-window` у містах; ремейк — крафт-синтез.
- `warren-report` — енциклопедія лору, персонажів, світу; відкриває World після першого проходження (`codex-window`).
- `chariot-timeline` — шкала до 50 ходів для перемотки.
- `dialogue-window` — сюжетні сцени і розвилки; `end-screen` бою з досвідом і рівнями.

## Фічі поза полем
- `branching-story` — три гілки (Law / Neutral / Chaos) у перших розділах, сходяться у фіналі; до 8 кінцівок; прихований Chaos Frame.
- `route-revisit` (World у ремейку) — повернутись до розвилки й зіграти іншу гілку без нового старту.
- `rewind` (Chariot, 50 ходів) — за ціну випадкової зміни ворожих дій; `save-slots`.
- `xp-level` і класи; рекрутинг Persuade; Training mode; `codex` (Warren Report).
- Reborn: оновлене ШІ, вид згори, кросплатформа (?).

## Варіації й родичі
- Ремейки: Let Us Cling Together (PSP, 2010/2011), Reborn (2022); попередник — Ogre Battle (реалтайм-армії на мапі, Chaos Frame); духовний наступник — [Final Fantasy Tactics](final-fantasy-tactics.md) (той самий автор, CT-черга, висота, фасінг).
- Родичі в корпусі: [Disgaea](disgaea.md), [Fire Emblem](fire-emblem.md) (поперемінні фази, пермасмерть), [Battle Brothers](battle-brothers.md) (спільна черга за ініціативою).
- Осі варіацій:
  - **черга**: фази сторін (Fire Emblem) / спільна черга за WT, що залежить від ваги і дій (TO) / CT-шкала (FFT);
  - **висота**: нема / ціна руху + дальність і шкода стрільця (TO) / стрибок обмежує рух (FFT);
  - **смерть**: одразу назавжди / лічильник 3 ходи на воскресіння (?) / лише лідер = поразка;
  - **перемотка**: нема / Chariot на 50 ходів з рандомізацією ворога.

## Цікавинки для курсу
- WT-черга: пріоритетна черга за «часом до ходу», де вага спорядження й вартість дії зсувають наступний хід — 📎 (heapq).
- Висота як третя координата: ціна підйому + бонус стрільця згори — 🥉.
- Chariot: журнал ходів із перемоткою на 50 назад і рандомізацією дій ворога після відкату — 🥈 (снепшоти стану + seed).
- Persuade: переманити ворога з шансом — 🌱.
- Дроп карт таро з тимчасовим бонусом тому, хто підбере, — 🌱.
- Стихії з колом сильних/слабких і бонусом за збіг — 📎.
- Розгалужений сюжет з прихованим лічильником ставлення фракцій — 🥉.

## Мапа на каталог
- Є: `height-levels` ↔ висота клітин · `hp-damage` · `melee-vs-ranged` · `floor-types`, `impassable-cells` · `legal-move-highlight`, `threat-range` · `status-effects` · `permadeath` · `unit-xp-skills` ↔ рівні класів · `inventory-items`, `shop-between-levels` · `world-map` · `rewind` ↔ Chariot · `save-game` · `hot-seat` ↔ Training на двох · `codex-window` ↔ Warren Report.
- **Нема** → пропозиції карток:
  - `+facing-hit-bonus`, `+initiative-queue`, `+death-countdown`, `+leader-death-lose`, `+recruit-talk`, `+world-alignment` — як у корпусі.
  - `+weight-speed` «Вага сповільнює чергу» · entities/state · 🌱 · слот {weight_formula}.
  - `+elemental-affinity` «Стихії з колом переваг» · entities/combat · 📎 · слот {elements: 8}.
  - `+card-drop-buff` «Дроп тимчасового бонусу» · entities/interact · 🌱.
  - `+branching-story` «Гілки сюжету з розвилками» · levels/progression · 🥉.

## Пропозиції до словників
- `+trigger:attacked` — атака як подія (поворот цілі до атакувальника); `+trigger:round_start` — тік спільної черги.
- `+cond:height_diff` — різниця висот атакувальника і цілі; `+cond:element` — стихія юніта/атаки.
- `+effect:wait_add` — додати очікування до наступного ходу юніта; `+effect:recruit` — ворог переходить у загін (ширше за `set_side`: лишається між боями); `+effect:rewind_turns` — відкотити бій на N ходів.
- `+ui:turn-order-list` · `+ui:height-indicator` · `+ui:hit-chance`.
- `+window:warren-report` · `+window:chariot-timeline` · `+window:formation-screen` · `+window:class-change`.
- `+feature:route-revisit` — повернутися до сюжетної розвилки без нової гри.
- `+axis:turn-structure:wait-time` — нове значення: черга за накопиченим очікуванням (WT/RT), відмінна від `time-track` (?).

## Джерела
- ⭐ [Wikipedia: Tactics Ogre](https://en.wikipedia.org/wiki/Tactics_Ogre) — сітка з рельєфом у діагональній проєкції, 10/30 юнітів, WT-черга за вагою й спритністю, гілки й Chaos Frame, таро, Persuade, стихії, погода, Training mode, платформи.
- [Wikipedia: Let Us Cling Together (2010)](https://en.wikipedia.org/wiki/Tactics_Ogre:_Let_Us_Cling_Together_(2010_video_game)) — Chariot на 50 ходів (план був 100), World і Warren Report, MP від 0, класи окремо від юнітів, крафт.
- [Final Weapon: деталі Reborn](https://finalweapon.net/2022/08/25/tactics-orge-reborn-details/) — RT/AT, 8 стихій, анкета таро, умова «убити юніта».
- [push.cx: Game Influences — Tactics Ogre](https://push.cx/game-influences-tactics-ogre) — висота для лучників, 4 слоти спорядження.
- Steam: пошук «Tactics Ogre Reborn»; YouTube: пошук «Tactics Ogre gameplay».

## Непевне
- (?) Фасінг і бонус удару в спину/бік — за памʼяттю; Wikipedia про фасінг мовчить.
- (?) Лічильник смерті 3 ходи й остаточна смерть після нього (ремейк) / одразу (оригінал); нежить, що повертається без вигнання — за памʼяттю.
- (?) Ціна підйому «+1 за кожен рівень понад перший» — з уривка пошуку без певного джерела.
- (?) Вибір напрямку стояння наприкінці ходу — з уривка пошуку.
- (?) Push.cx пише «8 бійців на полі», Wikipedia — до 10; у тексті — Wikipedia.
- (?) Reborn: карти-бафи на полі, ліміт рівня за розділом, нове ШІ — не перевірено.
