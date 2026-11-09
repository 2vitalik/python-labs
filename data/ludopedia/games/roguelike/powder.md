---
title: POWDER
slug: powder
aka: [iPOWDER]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2003
platforms: [GBA, Nintendo DS, Windows, Linux, macOS, PSP, GP2X, Windows CE, PS3 Linux, Wii, iPhone, Pandora]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/POWDER", best: true, note: "RogueBasin: суть за хвилину — клас із богів на кожному рівні, усі боги стежать, «спершу предмет, потім дієслово», 25 поверхів"}
  - {kind: official, url: "http://www.zincland.com/powder", note: "сайт Jeff Lait: About (як виграти, походження під GBA), Download усіх платформ, новини"}
  - {kind: other, url: "http://www.zincland.com/powder/release/powder118_src.tar.gz", note: "вихідний код 118: piety.cpp (механіка побожності), source.txt (боги, кари, дари), encyclopedia.txt, README з клавішами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=POWDER+roguelike+Jeff+Lait+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, item-pickup, item-identification, hunger-clock, status-effects, permadeath, player-death, unit-xp-skills, fog-of-war, minimap-radar, message-log, codex-window, help-window, main-menu, tutorial-window, leaderboard, score-records, save-single-slot, keyboard-controls, cell-click, projectile-shot, +god-piety, +god-per-level-class, +multi-god-watch, +divine-punish-boon, +trickster-god-whim, +xp-wipe-on-sin, +skill-spell-slots, +noun-verb-ui, +possess-unit, +polymorph-self, +swap-with-ally, +honest-savescum, +throw-item, +return-to-surface]
proposes: ["+trigger:level_up(a)", "+effect:boon(god)", "+effect:punish(god)", "+effect:possess(a, b)", "+effect:wipe_xp(a)", "+axis:command-order", "+feature:savescum-counter"]
author: opus
date: 2026-11-09
---

# POWDER — роглайк для Game Boy Advance, де клас складається з богів, обраних на кожному рівні

## Суть
Hack-подібний роглайк Jeff Lait (2003), спроєктований під GBA: 16×16 тайли, керування кнопками, партія ~3 години. Мета — спуститися до демона Baezl'bub, забрати його чорне серце й винести на поверхню. На старті нема ні класу, ні раси, ні навичок: **клас збирається з богів**, яких ти обираєш при кожному підвищенні рівня, а бог дає HP/MP і одну навичку чи закляття. Водночас **усі боги стежать одночасно**: кожна дія (убив мечем, закляттям, кинутим ножем, полікував, ідентифікував) додає або знімає побожність у кожного з семи, і розгніваний «чужий» бог може вдарити, а задоволений — обдарувати.

## Поле і час
- Поверх — квадратна сітка 32×32 (`MAP_WIDTH/HEIGHT` у коді); 25 поверхів (RogueBasin) зі сходами-драбинами; вниз і назад нагору, бо серце треба винести.
- Покроково: дія гравця → хід монстрів. Туман і запамʼятована мапа; міні-мапа окремою командою.
- Шари клітини: підлога, вода/басейни, ями (у них можна залізти й вилізти `<`/`>`), двері; предмети й істоти поверх.
- Глобальні лічильники, що тікають щоходу: голод, «примха» трікстер-бога (таймер 100–200 ходів), таймер кари вогнем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар | player | HP, MP, AC, фізичний рівень (+1 слот навичок), магічний рівень (+1 слот заклять), XP (рівень кожні 1000), бог | ходить, атакує рухом, кидає, кастує, молиться, міняється місцями, стрибає |
| Бог «no one god» (agnostic) | zone | +5/+5 HP/MP за рівень | жодних кар і дарів; «невіра» гасить гнів інших |
| Klaskov (fighter) | zone | +15/+0 | любить убивства й броню; не любить заклять |
| Belweir (wizard) | zone | +0/+15 | любить закляття, ідентифікацію, мантію; не любить ближнього бою |
| Quizar (rogue) | zone | +10/+5 | любить кидки, ідентифікацію, пастки й секрети, удар по безпорадному; не любить шуму |
| Tlosh (necromancer) | zone | +5/+10 | любить смерть здалеку й магію смерті; **заборонено** лікувальні закляття |
| H'ruth (barbarian) | zone | +20/+0 | любить ближній бій і оточення ворогами; **заборонено** будь-які закляття |
| Pax (cleric) | zone | +10/+10 | любить лікувати й нищити нежить; **заборонено** магію смерті й шкоду дружнім |
| Xom-подібний ><0\|V\| (cultist) | zone | випадкові кості HP/MP | бажає того, чого хоче бог «примхи» зараз |
| Монстр | enemy | вид, атаки, тип (нежить…) | бʼється; деякі дружні або нейтральні |
| Улюбленець / одержима істота | ally | — | команда `C`; заклинання Possess дає повне керування |
| Предмети (зброя, броня, жезли, сувої, книги, зілля, їжа, кільця) | pickup | часто невідомі | екіпірування, «zap», читання, «dip», кидок |
| Чорне серце Baezl'bub | pickup | — | мета: винести на поверхню |
| Драбина, яма, басейн | static | — | `<`/`>` — нагору/вниз, залізти/пірнути |

## Правила (КОЛИ → ЯКЩО → ТО)
Хід і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(avatar, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `damage(n)` (атака рухом); safewalk (Ctrl) — без атаки.
- КОЛИ `input(shift+dir)` → ТО `swap(avatar, creature)`; `input(alt+dir)` → `custom: «стрибок»`.
- КОЛИ `input(fire)` → ТО `throw(quivered, dir)`; кинуте з колчана піднімається безкоштовно.

Побожність (усі боги одночасно):
- КОЛИ `died(enemy)` не від закляття → ТО `counter(piety_fighter, +2v)`; від ближнього удару → ще `counter(piety_barb, +v)`; закляттям → `counter(piety_wizard, +v)`; кидком → `counter(piety_rogue, +v)`; ЯКЩО `state(enemy, undead)` → ТО `counter(piety_cleric, +v)`; `counter(piety_necro, +v)` за будь-яке вбивство (v — від рівня жертви).
- КОЛИ `input(cast, spell)` → ТО `counter(piety_wizard, +v)`; ЯКЩО `custom: «магія смерті»` → ТО `counter(piety_necro, +v/2)`, у Pax — заборонене; ЯКЩО лікування → ТО Pax +, Tlosh — заборонене; H'ruth — заборонене будь-яке.
- КОЛИ `input(identify)` → ТО `counter(piety_rogue, +5)`, `counter(piety_wizard, +3)`; знайдено секрет або поставлено пастку → Quizar +5.
- КОЛИ `custom: «оточений ≥2 ворогами»` → ТО `counter(piety_barb, +2×n)`, Belweir −1.
- КОЛИ `input(attack, friendly)` → ТО `counter(piety_cleric, −5)`; удар по безпорадному → Quizar +1, Tlosh +2, Pax −2.
- КОЛИ `custom: «одягнений у вбрання класу»` → ТО +1 відповідному богу (час від часу).
- КОЛИ `custom: «з'їв труп ситим»` → ТО Pax −2; шум → Quizar −.
- КОЛИ мінус побожності від власного обраного бога → ТО `custom: «удвічі»`; КОЛИ побожність > 200 → ТО `custom: «приріст часто пропадає»` (стеля 10 000).
- КОЛИ `custom: «догодив богу примхи»` → ТО той самий приріст іде й ><0|V|.

Гріх:
- КОЛИ `custom: «заборонена богом дія»` → ЯКЩО `custom: «це твій бог»` → ТО `custom: «стерти весь досвід»` + кара; ЯКЩО чужий бог і його «очки гніву» > побожності твого бога → ТО кара від чужого; інакше `message(«твій бог заступився»)` і `counter(piety_own, −n)`; agnostic — `custom: «невіра гасить гнів»`.

Боги діють щоходу:
- КОЛИ `tick` → ЯКЩО `custom: «очки бога > 100»` → ТО ЯКЩО `counter(piety_god, >, 0)` → ТО `custom: «дар»`; інакше `custom: «кара»`; обраний бог розглядається завжди, інші — з шансом 1/50.
- Кари (таблиця): вогняний удар, виклик монстрів, прокляття вдягненого / будь-якого, розчарування зброї / броні, отрута, параліч, сон, висмоктування мани, поліморф; ><0|V| — ще поліморф зброї.
- Дари (таблиця): форма ліча (Tlosh), удар по всіх сусідах (H'ruth), зняття прокляття та інші.
- КОЛИ `timer(100…200)` → ТО `custom: «бог примхи змінюється на випадкового»` + `message`.

Рівень:
- КОЛИ `counter(xp, >=, 1000·n)` → ТО `choose(god)`: у списку agnostic і всі боги з `counter(piety_god, >=, 10)`; показ статті енциклопедії + `confirm-dialog` «Follow X?».
- КОЛИ `after(choose)` → ТО `custom: «+кості HP/MP бога»`, `custom: «одна навичка АБО закляття зі списку бога»`; повідомлення про вільні слоти.

Мета:
- КОЛИ `died(baezlbub)` → ТО `spawn(black_heart)`; КОЛИ `reach(avatar, surface)` → ЯКЩО `has(avatar, black_heart)` → ТО `win`.
- КОЛИ `hp_zero(avatar)` → ТО `lose` + `window(leaderboard)`; сейв стирається.
- КОЛИ `hp_zero(possessed)` → ТО `custom: «повернення у власне тіло з шоком»` (краще відпустити `q` заздалегідь).

## Керування і ввід
- **Спершу предмет, потім дієслово**: в інвентарі обираєш предмет → контекстне меню (wear, take off, drop, eat/quaff, read, dip, zap, throw, quiver, name, examine); на ПК — ще й швидкі клавіші.
- Рух: стрілки / цифри / vi-клавіші; `<`/`>` — драбини, ями, басейни; `r` — біг, `s` — пошук, `R` — відпочинок, `x` — огляд (повна інформація про монстра), `_` — молитва, `z` — закляття, `J` — стрибок, `S` — обмін місцями, `C` — команда істоті, `q` — відпустити одержиму, `B` — дихання (у формі істоти), `F` — забути навичку/закляття, `&` — бажання, `m` — міні-мапа, `v` — історія повідомлень.
- GBA/DS: кнопки + контекстні меню; DS — стилус; ПК — клавіатура й миша; є підтримка геймпада.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: New Game · Tutorial · Load (є сейв) / Save Scum · View Scores · Options · Quit.
- Створення: стать, імʼя; у «advanced mode» — `choose`-меню «Initial God?».
- `game-screen`: поле 16×16-тайлів + рядок статусу `S12H010/01M010/00X932L02`: AC, HP/фізрівень, MP/магрівень, XP, поверх; `message-log` (2 рядки, `v` — уся історія → `log-window`).
- `inventory-window` з контекстним меню дій; позначка «улюблене» (жовта рамка, сортується першим).
- `upgrade-window` вибору бога на рівні (бог (побожність)) + стаття `codex-window` + `confirm-dialog`.
- `map-window` (міні-мапа), `help-window` (`?`, список команд `V`), `settings-window` (Options: safewalk, тайлсет…), `codex-window` — вбудована енциклопедія монстрів, предметів, заклять, богів.
- `end-screen` смерті/перемоги → `leaderboard` (high scores; сейв-скамери не потрапляють).
- Переходи: main-menu → (створення) → game-screen → рівень → вибір бога → game-screen; смерть → end-screen → main-menu.

## Фічі поза полем
- `permadeath` за замовчуванням, але **чесний сейв-скам**: після завантаження меню пропонує Save Scum, гра рахує, скільки разів персонаж «відкотився», і такий забіг не йде в таблицю рекордів.
- `tutorial`, `codex` (енциклопедія), кілька тайлсетів (класичний, NetHack, від гравців), `colorblind`-тайлсет спільноти (?).
- Режим «advanced»: вибір початкового бога.
- Порти на десяток платформ з одного коду; сейви не переносяться між версіями (рекорди — так).

## Варіації й родичі
- Родичі: [nethack](nethack.md) і [hack](hack.md) (сеттинг, ідентифікація, бажання, поліморф), DCSS (Xom — прямий прообраз ><0|V|), [mystery-dungeon](mystery-dungeon.md) (роглайк під кнопки консолі). Наступні 7DRL того ж автора — [jacobs-matrix](jacobs-matrix.md) та інші.
- Осі варіацій: **звідки клас** (обирається на старті / складається з виборів на рівнях / виникає з дій); **скільки богів слухає** (лише свій / усі одночасно з «гнівом» і «заступництвом»); **порядок команди** (дієслово → предмет, як у NetHack / предмет → дієслово, як тут); **сейв-скам** (заборонено / дозволено й позначено).

## Цікавинки для курсу
- Побожність як вектор: кожна дія змінює лічильники всіх богів одночасно за таблицею «дія × бог» — 🥉 (таблиця правил + лічильники).
- Клас із виборів на рівнях: список доступних богів = ті, хто тебе вже любить (≥10) — 📎.
- Заступництво: гнів чужого бога гасить побожність твого, якщо її більше — 🥈 (порівняння двох лічильників, перенесення очок).
- Трікстер-бог, що раз на 100–200 ходів «підписується» на випадкового іншого — 🌱.
- Інтерфейс «предмет → дієслово» з контекстним меню під кнопки GBA — 📎.
- Чесний сейв-скам: лічильник відкатів і виключення з рекордів — 🌱.
- Possess: керуєш іншою істотою, власне тіло лишається беззахисним — 🥈.

## Мапа на каталог
- Є: `dungeon-generation` · `stairs-levels` · `hp-damage` · `inventory` + `inventory-items` · `item-identification` · `hunger-clock` · `status-effects` · `permadeath` · `unit-xp-skills` (слоти навичок/заклять) · `fog-of-war` · `minimap-radar` · `message-log` · `codex-window` · `help-window` · `main-menu` · `tutorial-window` · `leaderboard` + `score-records` · `save-single-slot` · `keyboard-controls` · `cell-click` (стилус) · `projectile-shot` (кидки, жезли).
- **Нема** → пропозиції карток:
  - `+god-piety` + `+multi-god-watch` «Побожність до кількох богів одночасно за таблицею дій» · game-logic/score · 🥉 · слоти {gods, action_table}.
  - `+god-per-level-class` «Клас складається з вибору бога на кожному рівні» · entities/state · 📎.
  - `+divine-punish-boon` «Кари й дари з таблиць за порогом очок» · game-logic/economy · 📎.
  - `+trickster-god-whim` «Бог, що бажає того самого, що випадковий інший» · game-logic/opponent · 🌱.
  - `+xp-wipe-on-sin` «Заборонена дія стирає досвід» · game-logic/lose · 🌱.
  - `+noun-verb-ui` «Спершу предмет, потім дія» · interface/input · 📎.
  - `+possess-unit` «Вселитися в істоту» · entities/state · 🥈.
  - `+honest-savescum` «Сейв-скам дозволено, але пораховано» · game-logic/save · 🌱.
  - `+return-to-surface` «Мета — винести предмет нагору» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:level_up(a)` — сутність отримала рівень досвіду (не плутати з `level_start` — рівнем гри).
- `+effect:boon(god)` / `+effect:punish(god)` — бог обирає дар / кару з таблиці.
- `+effect:possess(a, b)` — керування переходить від A до B; тіло A лишається на полі.
- `+effect:wipe_xp(a)` — обнулити досвід.
- `+axis:command-order` — `verb-noun` (NetHack: `q` → яке зілля?) / `noun-verb` (POWDER: зілля → «випити»).
- `+feature:savescum-counter` — дозволений відкат сейву з лічильником і виключенням із рекордів.

## Джерела
- ⭐ [RogueBasin: POWDER](https://www.roguebasin.com/index.php/POWDER) — клас із богів, усі боги стежать, noun/verb, 25 поверхів, ~3 години, платформи.
- [Офіційний сайт](http://www.zincland.com/powder) — About (як виграти, «Roguelike для GBA і DS»), Download 118 для всіх платформ, новини до 2026.
- [Вихідний код 118](http://www.zincland.com/powder/release/powder118_src.tar.gz) — `piety.cpp` (приріст, гріх, заступництво, вибір бога на рівні), `source.txt` (боги, кари, дари), `encyclopedia.txt` (опис богів), `README.TXT` (клавіші й рядок статусу), `main.cpp` (меню Save Scum).
- YouTube: [пошук «POWDER roguelike Jeff Lait gameplay»](https://www.youtube.com/results?search_query=POWDER+roguelike+Jeff+Lait+gameplay).

## Непевне
- (?) Рік: Jeff Lait перше торкнувся `main.cpp` 22.01.2003; перший публічний реліз міг бути пізніше.
- (?) 8 напрямків руху: клавіші діагоналей є в коді, але на GBA-хрестовині діагоналі частково заборонені; не перевіряв, як саме.
- (?) Повний список дарів і кар кожного бога — у `source.txt` більше записів, ніж тут перелічено.
- (?) Розмір поверху 32×32 — константа графічного рушія; що це саме розмір рівня, не перевірено в генераторі.
- (?) Тайлсет для дальтоніків — зі згадки в новинах (сторонній проєкт).
