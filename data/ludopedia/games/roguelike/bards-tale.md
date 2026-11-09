---
title: "The Bard's Tale / Might and Magic — сіткові dungeon crawl 80-х"
slug: bards-tale
aka: ["The Bard's Tale", "Tales of the Unknown: Volume I", "Might and Magic Book One", "Might and Magic: The Secret of the Inner Sanctum", "M&M1", "BT1"]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1985
platforms: [Apple II, C64, Amiga, DOS, Macintosh, NES, PC-88]
links:
  - {kind: other, url: "https://crpgaddict.blogspot.com/2021/08/revisiting-bards-tale-1985.html", best: true, note: "CRPG Addict, Revisiting The Bard's Tale: місто 32×32, 5 підземель, спінери, антимагія, темрява, Review Board, Roscoe's, сейв лише в Гільдії, стеки монстрів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Bard%27s_Tale_(1985_video_game)", note: "загін 6, класи, пісні барда як довгі заклинання, 85 заклинань з 4-літерними кодами, Skara Brae 30×30, підземелля"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2010/03/bards-tale-not-quite-as-fun-as-i.html", note: "підземелля 22×22, спінер «повертає в випадковий бік», ніч — сильніші монстри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Bard%27s_Tale_II:_The_Destiny_Knight", note: "BT2: дистанції до 90 футів, команда advance, глушина, банк і казино, Snares of Death, 7 пісень"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum", note: "M&M1: 6 класів, 5 рас, 7 статів, рух вперед/назад/поворот 90°, втеча/здача/хабар, порядок за Speed"}
  - {kind: other, url: "https://crpgaddict.blogspot.com/2010/07/game-19-might-magic-i.html", note: "M&M1: області 16×16, Varn — 20 секторів A1–E4, сейв у таверні, їжа, старіння, пошук скарбу після бою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bard%27s+tale+1985+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, teleport, teleport-one-way, stairs-levels, fog-of-war, hp-damage, status-effects, inventory-items, item-pickup, unit-xp-skills, round-currency, shop-catalog, shop-window, character-select, player-death, save-game, keyboard-controls, melee-vs-ranged, +first-person-grid, +hand-drawn-map, +party-formation, +town-hub, +random-encounter, +spinner-tile, +anti-magic-tile, +bard-song-buff, +spell-code-entry, +monster-stacks, +recruit-monster, +sector-world-map, +food-per-rest, +character-aging, +search-after-battle, +encounter-options]
proposes: ["+trigger:rest(party)", "+effect:age(a, ±n)", "+effect:sing(song)", "+cond:sector(x)", "+window:spell-entry", "+window:review-board", "+ui:compass", "+ui:light-indicator", "+feature:character-import", "+card:spinner-tile", "+card:bard-song-buff", "+card:sector-world-map"]
author: opus
date: 2026-11-09
---

# The Bard's Tale / Might and Magic — сіткові dungeon crawl 80-х: спінери, антимагія, пісні барда й світ із секторів 16×16

## Суть
Два головні нащадки [wizardry](wizardry.md) 1985–86 років: загін до 6 героїв ходить покроково сіткою від першої особи, крок = клітина, поворот = 90°. **The Bard's Tale** (Interplay, 1985) переносить лабіринт у місто Skara Brae і додає барда, чиї **пісні — тривалі бафи** загону під музику, а також «підступні» клітини: спінер, антимагія, темрява, телепорт. **Might and Magic Book One** (New World Computing, 1986) розгортає те саме ядро на величезний відкритий світ з **областей 16×16**, складених у сітку секторів A1–E4, з їжею, відпочинком і старінням. Файл описує відмінності від `wizardry` і [dungeon-master](dungeon-master.md) (той — real-time; ці — суто покрокові).

## Поле і час
- **BT**: місто Skara Brae — сітка тайлів-будинків і вулиць (30×30 за Wikipedia, 32×32 за CRPG Addict); 5 підземель (винні погреби + каналізація, катакомби, замок Харкіна, вежа Кілеарана, вежа Мангара на 5 рівнів); рівень підземелля — сітка 22×22.
- **M&M1**: кожна область (місто, підземелля, ділянка глушини) — 16×16, не всі клітини вжито; суходіл Varn поділено на 20 секторів A1…E4; разом ≈50 мап.
- Стіни — на ребрах клітин; на поверхні вони зображують хребти, ряди дерев, скелі (M&M).
- Вид від першої особи (кілька клітин углиб) + текст; автомапи в оригіналах нема — мапу малює гравець.
- Час: ходу нема, поки гравець думає (M&M); бій — раунди з наказами кожному героєві; у BT уночі виходять сильніші монстри (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 6, клітина, орієнтація | рухається як одна фігура |
| Бард (BT) | ally | інструмент, пісні | співає пісню-баф на весь загін; інструменти — магічні (Fire Horn — атака) |
| Класи BT | ally | warrior · paladin · hunter · monk · rogue · bard · magician · conjurer → sorcerer · wizard → archmage | маги міняють клас назавжди; 4 книги заклинань |
| Класи M&M | ally | knight · paladin · archer · cleric · sorcerer · robber; 5 рас, світогляд, стать, вік | paladin/archer з рівнем отримують магію жерця/чаклуна |
| Призваний / приручений монстр (BT) | ally | спецатаки монстра | будь-який монстр може стати союзником (заклинання, фігурка, дружня зустріч) |
| Група монстрів | enemy | стек до 99 (?), до 4 стеків | бʼються стеком; масові заклинання бʼють усі стеки |
| Статуя-вартовий (BT) | enemy | — | стоїть на вулиці; оживає голем, блокує прохід |
| Будинок (BT) | container | — | вхід — шанс випадкової зустрічі |
| Спінер (BT) | terrain | — | розвертає загін у випадковий бік — збиває мапу |
| Антимагічна клітина (BT) | terrain | — | знімає захисні заклинання |
| Темна зона | terrain | — | не видно стін; світло — заклинання/предмет |
| Телепорт · Sinister Street (BT) | terrain | ціль | переносить; вулиця щоразу повертає назад |
| Пастка-провал (M&M) | hazard | — | скидає загін у підземелля |
| Магічний рот / статуя-підказка | static | текст | загадка або натяк; відповідь словом відкриває прохід (катакомби — імʼя Божевільного бога) |
| Двері / таємні двері / невидима стіна / односторонні двері | gate | — | таємні шукають (M&M — ударом у стіну); двері в'язниці M&M зачиняються за спиною |
| Перемикач стін (BT, Mangar 4) | switch | — | міняє всі двері ↔ стіни рівня |
| Сходи / левітація | static | — | вгору/вниз; на верхній рівень вежі — лише з Levitate |
| Гільдія авантюристів (BT) / таверна (M&M) | static | — | єдине місце збереження |
| Review Board (BT) | static | неозначене на мапі | лише тут — новий рівень, зміна класу, нові рівні заклинань |
| Храм | static | 10 золота за HP (BT) | лікування, зняття кам'яніння/висихання, воскресіння |
| Roscoe's Energy Emporium (BT) | static | ціна | відновити очки заклинань за гроші |
| Лепрекон (M&M) | neutral | 1 самоцвіт | переносить загін в інше місто |
| Самоцвіт (M&M) | resource | — | падає з ворогів; потрібен для високих заклинань |
| Їжа (M&M) | resource | старт 10 порцій | 1 порція на відпочинок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward|back)` → ЯКЩО `free(cell)` → ТО `move(party, facing | −facing)`; інакше `block`.
- КОЛИ `input(left|right)` → ТО `face(party, ±90°)`.
- КОЛИ `enter(party, spinner)` → ТО `face(party, random)` (без повідомлення).
- КОЛИ `enter(party, antimagic)` → ТО `clear_state(party, protective spells)`, `clear_state(party, light)` (?).
- КОЛИ `enter(party, teleporter)` → ТО `teleport(party, fixed cell)`; КОЛИ `enter(party, sinister_street_end)` → ТО `teleport(party, «початок вулиці»)`.
- КОЛИ `enter(party, pit_trap)` (M&M) → ТО `custom: «загін падає в підземелля»`.
- КОЛИ `enter(party, mouth)` → ТО `message(riddle)`; ЯКЩО `custom: «введено правильне слово»` → ТО `custom: «відкрити прохід»`.
- КОЛИ `contact(party, wall)` (M&M) → ЯКЩО `custom: «таємні двері»` → ТО `move(party, facing)`.
- КОЛИ `enter(party, house)` (BT) або `rng(p)` на крок → ТО `custom: «зустріч»`, `window(battle-screen)`.
- КОЛИ `custom: «зустріч»` (M&M) → ТО `choose(attack | run | bribe | surrender)`; ЯКЩО `custom: «втеча не вдалась»` → бій.
- КОЛИ `turn_start(round)` → ТО `custom: «наказ кожному героєві: атака, заклинання, пісня, предмет, захист, втеча»`; виконання — `custom: «за Speed; щораунду випадковий бонус швидкості одній стороні»` (M&M).
- КОЛИ `input(sing song)` (BT) → ТО `set_state(party, song effect, duration)` + `sound(music)` (`+effect:sing`).
- КОЛИ `input(cast code)` → ЯКЩО `custom: «код із мануалу правильний (4 літери в BT)»` і `custom: «вистачає очок заклинань (і самоцвітів у M&M)»` → ТО `custom: «ефект заклинання»`.
- КОЛИ `input(cast MIBL|DRBR)` (BT) → ТО `damage(all stacks | stack, n)`.
- КОЛИ `input(cast APAR)` (BT) → ТО `teleport(party, coords)`.
- КОЛИ `input(cast MACO)` (BT) → ТО `set_state(party, compass)`.
- КОЛИ `wave_cleared` → ТО `custom: «XP і золото порівну між живими»` (BT); у M&M — `custom: «скарб лише після пошуку клітини»`.
- КОЛИ `input(rest)` (M&M) → ЯКЩО `has(party, food)` → ТО `take(party, food)`, `heal(party, full)`, `custom: «відновлення очок заклинань»`, `custom: «вік +»`.
- КОЛИ `custom: «вік > 80»` (M&M) → ЯКЩО `prob(p)` → ТО `custom: «герой помирає уві сні»`.
- КОЛИ `contact(party, review_board)` (BT) → ЯКЩО `custom: «XP досить»` → ТО `custom: «новий рівень (+1 випадковий атрибут)»`; маг → `choose(новий клас)`.
- КОЛИ `contact(party, roscoe)` → ЯКЩО `counter(gold, >=, price)` → ТО `currency(−price)`, `custom: «очки заклинань → максимум»`.
- КОЛИ `custom: «загін загинув»` (BT) → ТО `custom: «повернення в Гільдію; мертві стираються, якщо не принести»`.
- КОЛИ `custom: «загін вийшов і повернувся»` → ТО `custom: «фіксовані зустрічі відроджуються»`.
- КОЛИ `custom: «усі герої сплять/паралізовані»` (M&M) → ТО `lose`.
- КОЛИ `died(Mangar)` (BT) → ТО `win`; M&M — `custom: «розгадати Inner Sanctum»` → `win`.
- Перемога: BT — убити Мангара; M&M — квест Inner Sanctum. Поразка: загибель загону (повернення до сейву). Рахунку нема.

## Керування і ввід
- Клавіатура: вперед/назад, поворот 90° ліворуч/праворуч; BT — кожна команда на окремій клавіші **без підменю** (на відміну від Wizardry); E — підйом з Levitate.
- Заклинання — вводом коду з мануалу (BT: 4 літери, напр. MIBL; M&M: за рівнем і номером); у DOS/Amiga/Mac BT з мишкою — список назв.
- Бій — меню наказів на кожного героя; BT2 додає дистанції й команду «advance».

## Вікна, меню, HUD
- `game-screen`: вікно виду від першої особи, `party-roster` (імʼя, AC, HP, SP, клас), текстовий `message-log`; BT — індикатори світла, щита й компаса (MACO).
- `battle-screen`: портрет монстра, стеки груп, меню наказів; дії «повільно прокручуються» текстом.
- `town-hub`: Гільдія (створення/склад загону, сейв), Garth's (`shop-window`), таверни, храми, Review Board, Roscoe's (BT); таверна, магазини, храм, тренування, в'язниця (M&M).
- `character-create`: раса, клас, (M&M — світогляд, стать).
- `spell-entry`: рядок для коду заклинання.
- Переходи: `town-hub` ⇄ вулиці / глушина → підземелля → (зустріч) `battle-screen` → назад; сейв — лише в Гільдії/таверні.

## Фічі поза полем
- `save-game` лише в Гільдії (BT: зберігаються персонажі, не світ) або в таверні (M&M); перезавантаження з гри нема (BT).
- `character-import`: BT імпортує героїв з Wizardry та Ultima III (на частині платформ).
- Мапу малює гравець; ремастери BT додають автомапу.
- BT2: банк, казино, real-time пастки Snares of Death (з пастки не вийти, доки не розвʼязано; провал — смерть).

## Варіації й родичі
- [wizardry](wizardry.md) — спільний предок; [dungeon-master](dungeon-master.md) — той самий кроковий вид, але real-time; [legend-of-grimrock](legend-of-grimrock.md), [etrian-odyssey](etrian-odyssey.md) (ручна мапа як механіка), [dungeon-encounters](dungeon-encounters.md) (координатна сітка).
- Відмінності від `wizardry`: місто й світ — теж сітка (не меню); бард і пісні як окремий шар бафів; клітини-«брехуни» (спінер, антимагія, перемикач стін); у M&M — відкритий світ із секторів, їжа, старіння, хабар/здача.
- Осі варіацій: світ (меню-місто + лабіринт / місто-сітка / світ із секторів) · мапа (ручна / автомапа) · баф (заклинання / пісня з тривалістю) · ресурс відпочинку (немає / їжа) · смерть (стерти / лежить до рятувальників / повернення до сейву).

## Цікавинки для курсу
- Спінер: клітина, що мовчки повертає загін — 🌱 (і чудовий тест «малюй мапу»).
- Антимагічна клітина знімає бафи; перемикач «усі двері ↔ стіни» — 🌱 кожне.
- Пісня барда: баф загону на N ходів з музикою — 🌱.
- Світ із секторів 16×16 і координати A1…E4 — 📎 (адресація мап, перехід між сусідніми).
- Стеки монстрів «кількість × тип» і масові удари по стеках — 📎.
- Старіння: вік росте від часу/магії, після 80 — шанс смерті уві сні — 🌱.
- Ручна мапа: редактор-міліметрівка поруч із грою (стіни на ребрах) — 🥉.

## Мапа на каталог
- Є: `move-4dir` (вперед/назад) · `orientation-state` · `impassable-cells` · `key-and-door` · `teleport` · `teleport-one-way` (односторонні портали) · `stairs-levels` · `fog-of-war` (темрява) · `hp-damage` · `status-effects` · `inventory-items` · `item-pickup` · `unit-xp-skills` · `round-currency` · `shop-catalog` · `shop-window` · `character-select` · `player-death` · `save-game` · `keyboard-controls` · `melee-vs-ranged` (BT2 дистанції).
- **Нема** → пропозиції карток:
  - `+first-person-grid`, `+hand-drawn-map`, `+party-formation`, `+town-hub`, `+random-encounter` — як у `wizardry`.
  - `+spinner-tile` «Клітина повертає в випадковий бік» · entities/move · 🌱.
  - `+anti-magic-tile` «Клітина знімає активні бафи» · entities/state · 🌱.
  - `+bard-song-buff` «Пісня: баф загону на час» · entities/state · 🌱 · слоти {effect, duration}.
  - `+spell-code-entry` «Заклинання вводом коду» · interface/input · 🌱.
  - `+monster-stacks` «Вороги стеками N × тип» · entities/combat · 📎.
  - `+recruit-monster` «Монстр стає союзником» · entities/state · 📎.
  - `+sector-world-map` «Світ — сітка областей 16×16» · levels/progression · 📎.
  - `+food-per-rest` · `+character-aging` · `+search-after-battle` · `+encounter-options` (бій / втеча / хабар / здача) — по 🌱.

## Пропозиції до словників
- `+trigger:rest(party)` — загін відпочиває (їжа, відновлення, вік).
- `+effect:age(a, ±n)` — вік героя як стат.
- `+effect:sing(song)` — запустити пісню (баф + музика); можна звести до `set_state` + `sound`.
- `+cond:sector(x)` — загін у секторі/області (M&M).
- `+window:spell-entry` — рядок вводу коду заклинання; `+window:review-board` — екран підвищення рівня/зміни класу.
- `+ui:compass` — компас від заклинання; `+ui:light-indicator` — індикатор світла.
- `+feature:character-import` — імпорт героїв з інших ігор.
- `+card:spinner-tile` · `+card:bard-song-buff` · `+card:sector-world-map`.

## Джерела
- ⭐ [CRPG Addict: Revisiting The Bard's Tale](https://crpgaddict.blogspot.com/2021/08/revisiting-bards-tale-1985.html) — місто, підземелля, спецклітини, сейв, храми, Roscoe's, Review Board, стеки, союзники.
- [Wikipedia: The Bard's Tale (1985)](https://en.wikipedia.org/wiki/The_Bard%27s_Tale_(1985_video_game)) — загін, класи, пісні, 85 заклинань з кодами, Skara Brae, підземелля.
- [CRPG Addict: The Bard's Tale 2010](https://crpgaddict.blogspot.com/2010/03/bards-tale-not-quite-as-fun-as-i.html) — 22×22, спінер, ніч.
- [Wikipedia: The Bard's Tale II](https://en.wikipedia.org/wiki/The_Bard%27s_Tale_II:_The_Destiny_Knight) — дистанції, глушина, Snares of Death.
- [Wikipedia: Might and Magic Book One](https://en.wikipedia.org/wiki/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum) — класи, рух, бій.
- [CRPG Addict: Might and Magic I](https://crpgaddict.blogspot.com/2010/07/game-19-might-magic-i.html) — 16×16, сектори A1–E4, таверна, їжа, старіння, самоцвіти.
- YouTube: [пошук](https://www.youtube.com/results?search_query=bard%27s+tale+1985+gameplay).

## Непевне
- (?) Розмір Skara Brae: 30×30 (Wikipedia) проти 32×32 (CRPG Addict).
- (?) Перелік пісень BT1 і їхні ефекти (за памʼяттю — 6 пісень, бард «сідає голосом» і відновлюється випивкою в таверні) — у відкритих джерелах не підтверджено; Wikipedia позначає ефекти як «citation needed».
- (?) Ніч у BT: пост 2010 каже «вночі сильніші монстри», коментатор — що циклу нема (порівнює з консольним портом).
- (?) Ліміти стеків (4 групи по 99 — приклад з берсерками, не правило).
- (?) Чи антимагія гасить і світло.
- (?) День/ніч і автомапа в M&M1 — не описано; формат коду заклинань M&M (рівень-номер) — з памʼяті.
- (?) Студії й автори (Interplay / EA для BT, New World Computing / Jon Van Caneghem для M&M) — з памʼяті, у джерелах агент не звіряв.
- (?) Черга: «відкрита сітка-світ 16×16 секторами» — так у M&M; у BT світ — одне місто + підземелля.
