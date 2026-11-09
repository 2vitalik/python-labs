---
title: "Yggdra Union: We'll Never Fight Alone"
slug: yggdra-union
aka: [Yggdra Union, ユグドラ・ユニオン, Dept. Heaven Episode II]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2006
platforms: [GBA, PSP, iOS, Android, Switch, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Yggdra_Union", best: true, note: "картки POW/ACE/MOV, одна атака за хід, юніони X і +, лідер + до 7 підлеглих, 5 сутичок"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ユグドラ・ユニオン", note: "JA: вибір карток перед боєм, умови поразки, предмети без валюти, ландшафтні здібності класів"}
  - {kind: steam, url: "https://store.steampowered.com/app/2107860/Yggdra_Union/", note: "PC 2023: rewind, автосейв, швидкість бою до 5×, trick-режими"}
  - {kind: other, url: "https://www.rpgfan.com/review/yggdra-union-well-never-fight-alone/", note: "огляд PSP: юніон X у чоловіка, хрест у жінки, війська 8-на-8"}
  - {kind: other, url: "https://www.siliconera.com/yggdra-union/", note: "картка з 12 MOV: один іде на 2, інший на 10; шкала навички 100 %"}
  - {kind: other, url: "https://www.honestgamers.com/7356/game-boy-advance/yggdra-union-well-never-fight-alone/review.html", note: "огляд GBA: sword > axe > lance > sword, пасив/агресив, мінус воїн за повторний бій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Yggdra+Union+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, ai-opponent, status-effects, floor-types, item-pickup, inventory-items, sequential-levels, save-game, save-autosave, undo-unlimited, difficulty-levels, tutorial-window, game-screen, end-screen, +card-per-turn, +shared-move-pool, +one-attack-per-turn, +union-formation, +clash-sim, +outnumber-attrition, +weapon-triangle, +skill-gauge-tug, +deck-exhaustion-lose, +day-night-cycle, +weapon-durability, +morale-carryover, +staged-objectives, +custom-rules]
proposes: ["+trigger:card_played", "+trigger:deck_empty", "+cond:in_formation", "+cond:time_of_day", "+effect:clash", "+ui:card-hand", "+ui:skill-gauge", "+window:card-select", "+window:clash-screen"]
author: opus
date: 2026-11-09
---

# Yggdra Union — картка ходу дає спільний пул руху й одну атаку, а атакує цілий юніон-формація

## Суть
Покрокова тактика від Sting (серія Dept. Heaven): на початку кожного ходу гравець грає **одну тактичну картку**, і її число MOV — це **спільний бюджет клітин руху** на весь загін, а POW — сила удару. За хід дозволена **лише одна атака**: атакувальник стає лідером юніону, і союзники, що стоять навколо нього за фігурою **X** (лідер-чоловік) або **+** (лідер-жінка), вступають у бій за чергою. Бій — окрема «сутичка» загонів солдатиків; програвши, юніт втрачає мораль (аналог HP), яка між полями бою сама не відновлюється.

## Поле і час
- Квадратна сітка з ландшафтом (замок, пустир, місто, ліс, водна гладь); мапи часто вузькі, «як план будівлі» — коридори в одну клітину заважають зібрати юніон.
- Хід = фаза гравця (картка → рух у межах пулу → не більше однієї атаки) і фаза ворога. Є цикл доби: деякі класи й картки залежать від часу (у «Полудень» діє картка Refreshment).
- Бій юніону — окремий екран «сутичок» (clash): пари юнітів зводяться по черзі, всередині — бій солдатиків з елементами реального часу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт (герой/клас) | piece | Morale, GEN, ATK, TEC, LUK; REP (свої) / POW.UP (ворожі); стать; тип зброї; ландшафтна здатність | ходить у межах пулу MOV; може бути лідером або членом юніону |
| Лідер юніону (切り込み隊長) | piece | стать → форма X або + | той, хто атакує; задає форму й дає зброю для ACE картки |
| Солдати юніта | object | лідер + до 7 підлеглих (?) | «HP» сутички; кожен програш повторного бою — мінус один воїн |
| Мілано, Іґдра | piece | — | герої: мораль 0 → поразка |
| Ворожі юніти | enemy | ті ж стати + POW.UP | атакують своїм юніоном |
| Тактична картка | supply | POW, ACE (тип зброї), MOV, навичка | одна на хід; зіграна вибуває до кінця поля бою |
| Предмет | pickup | ефект, міцність у «поля бою» | знайдений на клітині → трофеї; спорядити або зʼїсти (мораль) |
| Ландшафт | terrain | тип | модифікує шкоду; класи мають ландшафтну здатність; навички карток можуть змінювати ландшафт |
| Опорний пункт / мета мапи | zone | — | ціль «зайняти» на деяких полях |
| Гармати, катапульти | hazard | — | зʼявляються на пізніх мапах (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `choose(cards)`: із колоди береться фіксована для цього поля кількість карток («зазвичай менше десяти»).
- КОЛИ `turn_start(player)` → ТО `choose(card)` із взятих; `custom: «картка вибуває до кінця поля бою»`; `counter(mov_pool, MOV)`, `set_value(power, POW)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `counter(mov_pool, ≥, path_len)` → ТО `move(unit, cell)`, `counter(mov_pool, -path_len)`; пул 5 = п'ять юнітів по 1 клітині або один на 5.
- КОЛИ `input(move, knight)` → ЯКЩО `occupied(path, enemy)` → ТО `custom: «Knight проходить крізь ворожих юнітів»`; Dragon Knight — `custom: «ходить по воді»`.
- КОЛИ `input(attack, leader, enemy)` → ЯКЩО `counter(attacks_this_turn, ==, 0)` → ТО `custom: «зібрати юніон»`, `custom: «почати сутичку»`; інакше `block`.
- Юніон: КОЛИ `custom: «зібрати юніон»` → ЯКЩО `custom: «союзник у клітині X від лідера (чоловік) або + (жінка)»` і `count(union, <, 5)` → ТО `custom: «союзник вступає в юніон»`; порядок бою — за позицією у формі.
- КОЛИ `custom: «почати сутичку»` → ТО `custom: «пари юнітів бʼються по черзі; удар — контрудар, доки одна сторона не вибита»`.
- КОЛИ `custom: «юніони різного розміру»` → ЯКЩО `count(union_a, >, union_b)` → ТО `custom: «менший бʼється повторно»`, `counter(soldiers, -1)` за кожен наступний бій.
- КОЛИ `custom: «програш у парі»` → ТО `damage(loser_morale, n)`: n залежить від POW картки, відриву, статів і ландшафту.
- Зброя: ЯКЩО `custom: «sword > axe > lance > sword»` → ТО `custom: «перевага в парі»`; решта типів (bow, staff, scythe, book, lump) — свої сумісності (?).
- КОЛИ `input(order, passive)` → ТО `counter(skill_gauge, +n)`, `custom: «менша шкода»`; КОЛИ `input(order, aggressive)` → ТО `counter(skill_gauge, -n)`, `custom: «більша шкода»`.
- КОЛИ `counter(skill_gauge, ==, 100)` → ЯКЩО `same(leader, card, weapon)` і `custom: «умова навички (лідер, ландшафт, час доби)»` → ТО `custom: «навичка картки»`: статус, відновлення моралі, зміна ландшафту.
- КОЛИ `hp_zero(unit)` (мораль 0) → ТО `disappear(unit)` — гине або відступає; прогрес до рівня скидається в 0.
- ЯКЩО `custom: «день або ніч»` → ТО `custom: «Assassin/Necromancer мають інший ATK»`.
- КОЛИ `enter(unit, item_cell)` → ТО `pickup(unit, item)` у трофеї; доступний на наступному розгортанні.
- КОЛИ `input(use, item)` → ТО `heal(unit, n)` (мораль; кількість видно заздалегідь); спорядити → `set_state(unit, equipped)`, зняти не можна до зламу.
- КОЛИ `custom: «минуло N полів бою»` → ТО `disappear(item)` (міцність у стадіях).
- КОЛИ `level_end` → ТО `custom: «мораль не відновлюється сама»` — переходить на наступну мапу.
- КОЛИ `custom: «поточну ціль поля виконано»` → ТО `custom: «нова ціль / підкріплення ворога»` або `win`; цілі відкриваються по черзі.
- КОЛИ `hp_zero(milanor)` або `hp_zero(yggdra)` → ТО `lose`.
- КОЛИ `counter(cards_left, ==, 0)` → ТО `lose` — колода як ліміт ходів.
- Перемога: ціль поля (вбити лідера, зайняти опорний пункт…) · Поразка: мораль героя 0 / картки скінчились / своя умова мапи · Рахунок: нема; валюти теж нема — предмети для бартеру.

## Керування і ввід
- Курсор по сітці: картка → вибір юніта → клітина (рух списує пул) → атака по сусідньому ворогу.
- У сутичці: вибір наказу Aggressive / Neutral / Passive (музика пришвидшується / звичайна / сповільнюється).
- Кнопка прискорення: 2× або 4× (PSP), до 5× (PC); suspend — швидке збереження посеред бою.
- PC 2023: миша, клавіатура з переназначенням, геймпад.

## Вікна, меню, HUD
- `custom-window` «Card select»: перед полем вибір N карток із колоди.
- Розгортання: юніти й предмети з трофеїв (спорядити / тримати) (?).
- `game-screen`: сітка, ряд узятих карток (`+ui:card-hand`), лічильник пулу MOV, вікно юніта (мораль, стати), поточна ціль.
- `custom-window` «Clash»: дві колони солдатиків, `+ui:skill-gauge` вгорі (рухається в «+» і «−»), вибір наказу.
- `dialogue-window` — сюжет; `log-window` — журнал розмов (PC).
- `end-screen` — Game Over (картки скінчились / герой упав); `save-slots` — збереження будь-де (PC).
- `settings-window` (PC): голос JP/EN, три набори звуку, швидкість бою, клавіші.

## Фічі поза полем
- `levels-sequential`: лінійна низка полів бою з розвилками сюжету.
- `undo` без ліміту (PC: rewind), `autosave` (продовжити з обраного ходу), `save-slots`.
- `difficulty-presets`: EASY (PC) — предмети вічні; `custom-rules` — trick-режими: обмін форм X/+ між статями, без критів, Мілано як Круз.
- `tutorial` вбудований; `stats` не переносяться в нову гру після проходження.
- Предмети: бартер замість валюти, деякі змінюються з часом або від використання.

## Варіації й родичі
- Серія Dept. Heaven: Riviera (ep. I), [knights-in-the-nightmare](knights-in-the-nightmare.md) (ep. IV), Gungnir; спін-офи Yggdra Unison, Blaze Union, Gloria Union.
- Родичі в корпусі: [advance-wars](advance-wars.md) (сітка, фаза сторони), [fire-emblem](fire-emblem.md) (трикутник зброї, мораль як HP героїв), [disgaea](disgaea.md) (командна атака сусідів), [card-hunter](card-hunter.md) (картки як дії).
- **Осі варіацій**: бюджет руху — на юніта / очки дії / спільний пул із картки · атак за хід — усі юніти / одна на сторону · хто вступає в бій — лише двоє / сусіди / формація за статтю лідера · ліміт ходів — лічильник / колода карток.

## Цікавинки для курсу
- Спільний пул MOV з картки, розподілений між юнітами — 📎 (один лічильник, перевірка довжини шляху).
- Юніон-формація: союзники в клітинах X або + від лідера залежно від статі; ліміт 5 — 🥉 (шаблон навколо клітини + збирання ланцюжка «linked»).
- Сутичка-симуляція: пари, удар-контрудар, мінус воїн за повторний бій меншого загону — 🥉.
- Шкала навички «туди-сюди» від наказу Passive/Aggressive — 📎.
- Колода як ліміт ходів: картки скінчились → поразка — 🌱.
- Trick-режими як перемикачі правил (обмін форм, без критів) — 📎.

## Мапа на каталог
- Є: `hp-damage` (мораль) · `ai-opponent` · `status-effects` (навички карток) · `floor-types` (ландшафт і здатності класів) · `item-pickup` · `inventory-items` · `sequential-levels` · `save-game` · `save-autosave` · `undo-unlimited` (PC rewind) · `difficulty-levels` · `tutorial-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+card-per-turn` «Картка ходу задає параметри ходу» · game-logic/opponent · 📎 · слоти {POW, MOV, skill}.
  - `+shared-move-pool` «Спільний бюджет руху на загін» · entities/move · 📎.
  - `+one-attack-per-turn` «Одна атака на сторону за хід» · game-logic/opponent · 🌱.
  - `+union-formation` «Учасники бою за формою навколо лідера» · entities/combat · 🥉 · слот {shape: X|plus, max: 5}.
  - `+clash-sim` «Бій загонів солдатиків» · entities/combat · 🥉.
  - `+outnumber-attrition` «Повторний бій меншого загону з втратою воїна» · entities/combat · 📎.
  - `+weapon-triangle` «Трикутник зброї» · entities/combat · 🌱 — як у Fire Emblem.
  - `+skill-gauge-tug` «Шкала навички від наказу» · entities/state · 📎.
  - `+deck-exhaustion-lose` «Колода скінчилась — поразка» · game-logic/lose · 🌱.
  - `+day-night-cycle` · `+weapon-durability` · `+custom-rules` — уже пропоновані в корпусі.
  - `+morale-carryover` «HP не відновлюється між рівнями» · entities/state · 🌱.
  - `+staged-objectives` «Цілі відкриваються по черзі» · game-logic/win · 📎.

## Пропозиції до словників
- `+trigger:card_played` — гравець зіграв картку ходу (уже пропоновано в корпусі).
- `+trigger:deck_empty` — скінчились картки (уже пропоновано).
- `+cond:in_formation` — сутність стоїть у клітині шаблону відносно іншої (X, +, лінія).
- `+cond:time_of_day` — фаза доби (день/ніч/полудень) для класів і карток.
- `+effect:clash` — запустити підбій двох груп з власними правилами.
- `+ui:card-hand` — ряд доступних карток; `+ui:skill-gauge` — шкала з «+» і «−», що наповнюється від наказів.
- `+window:card-select` — вибір підмножини карток перед рівнем; `+window:clash-screen` — екран бою загонів.

## Джерела
- ⭐ [Wikipedia: Yggdra Union](https://en.wikipedia.org/wiki/Yggdra_Union) — POW/ACE/MOV, одна атака за хід, форми X і +, linked unions з 15-го поля, стати, предмети.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ユグドラ・ユニオン) — юніон до 5, повторні бої меншого загону, умови поразки, бартер, класи й ландшафт, день/ніч.
- [Steam: Yggdra Union](https://store.steampowered.com/app/2107860/Yggdra_Union/) — PC-доповнення: rewind, автосейв, швидкість до 5×, trick-режими, EASY.
- [RPGFan (PSP)](https://www.rpgfan.com/review/yggdra-union-well-never-fight-alone/) — X у чоловіка, хрест у жінки, війська 8-на-8, мораль переходить між боями.
- [Siliconera](https://www.siliconera.com/yggdra-union/) — розподіл 12 MOV, шкала навички 100 %, поразка через картки.
- [HonestGamers (GBA)](https://www.honestgamers.com/7356/game-boy-advance/yggdra-union-well-never-fight-alone/review.html) — удар/контрудар, трикутник зброї, пасив/агресив і шкала, скидання прогресу при смерті.
- YouTube: пошук «Yggdra Union gameplay».

## Непевне
- (?) Розмір загону: Wikipedia — лідер + до 7 підлеглих («до 80 солдатів у 5 сутичках»), Siliconera — «до шести бійців», HonestGamers — «сила шести воїнів».
- (?) Як працюють linked unions (з 15-го поля): ймовірно, член юніону зі своєю формою додає наступних — не перевірено.
- (?) Чи збирає юніон захисник за тими самими формами і як ворог обирає свою картку.
- (?) Сумісності зброї поза sword/axe/lance (bow, staff, scythe, book, lump) і точна формула втрати моралі.
- (?) Гармати й катапульти як окремі сутності поля — лише згадка в огляді.
