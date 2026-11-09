---
title: "GearHead (GearHead: Arena)"
slug: gearhead
aka: [GearHead Arena, GearHead 1, GH1]
family: roguelike
also: [tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2002
platforms: [Linux, Windows, DOS, FreeBSD]
links:
  - {kind: other, url: "https://www.roguebasin.com/index.php/GearHead", best: true, note: "RogueBasin: дві шкали (пішки / меха), «черепашачий» рух у мехі, сюжет з випадкових підсюжетів, навички за XP, дизайн мехів"}
  - {kind: official, url: "http://www.gearheadrpg.com/", note: "сайт Joseph Hewitt: GearHead 1/2/Caramel, лінки на GitHub, itch, Steam"}
  - {kind: other, url: "https://github.com/jwvhewitt/gearhead-1", note: "код і doc/: Introduction (рух, бойові навички), readme (меню мехи, режими руху, перезарядка), TheRules (конструкція, XP), man_mecha (Field HQ), talking (реакція NPC), xranplot (генератор сюжету)"}
  - {kind: steam, url: "https://store.steampowered.com/app/1565090/GearHead_Caramel/", note: "наступник GearHead Caramel"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=GearHead+roguelike+mecha+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, keyboard-controls, hp-damage, inventory, inventory-items, unit-xp-skills, height-levels, projectile-shot, shoot-burst, shoot-cooldown, melee-vs-ranged, fog-of-war, message-log, status-panel, shop-catalog, round-currency, save-multi-slot, dungeon-generation, in-game-editor, main-menu, +turtle-movement, +dual-scale, +mecha-board-eject, +move-modes, +terrain-move-cost, +speed-attack-penalty, +clock-action-time, +body-part-targeting, +limb-disable, +mecha-design, +procedural-plot, +npc-reaction, +faction-reputation, +recruit-ally, +talent-prereq, +salvage-parts, +xp-for-dodge, +data-driven-content]
proposes: ["+axis:control=turtle", "+axis:scale", "+cond:move_mode(a, m)", "+effect:board(a, vehicle)", "+effect:eject(a)", "+effect:disable_part(a, part)", "+window:vehicle-design", "+ui:reaction-meter", "+feature:procedural-plot"]
author: opus
date: 2026-11-09
---

# GearHead — перший роглайк про гігантських роботів: пішки ходиш як у Angband, у мехі — як черепаха

## Суть
Відкритий роглайк-RPG Joseph Hewitt (Free Pascal, перший реліз 10.05.2002): пілот блукає містом Hogye, шахтами й пустками, торгує, розмовляє з NPC, а згодом отримує меху й бʼється на арені та в місіях. Ядро — **дві шкали одного світу**: особиста (людина з HP, 8 статами й 30 навичками) і механічна (меха з модулів, кожен з власною бронею й функцією). Рух у них різний: пішки — звичні 8 напрямків, у мехі — напрям, швидкість і повороти («turtle movement»), а тип шасі (ноги, колеса, ховер, політ) по-різному сприймає рельєф. Сюжет кампанії збирається з **випадкових епізодів-підсюжетів** під передісторію персонажа.

## Поле і час
- Квадратна сітка з висотою: пагорби L1–L3, вода L1–L3 (глибина під водою), ліси, болото, руїни, дорога; у сутності є **напрям, швидкість і висота** (індикатор: «+» — куди дивишся, число — висота, синє — глибина).
- Дві шкали карт: особиста (вулиці, будівлі, шахти) і механічна (бойові карти); між ними — сідаєш у меху або виходиш.
- Час — **годинник у «кліках»**: кожна дія має тривалість, після команди годинник іде, доки дія не завершиться; хто перший звільнився, той і діє (як у MechForce / Titans of Steel). З 2006 є опція тактичного покрокового режиму.
- 42 типи місцевості (`terrain list.txt`); випадкові мапи (`randmaps`: пагорби, глибока вода), рівні шахт.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пілот (PC) | player | 8 статів (Reflexes, Body, Speed, Perception, Craft…), 30 навичок до рангу 15, таланти, HP, кінцівки | 8-напрямний або «черепашачий» рух; бій особистою зброєю; розмови; ремонт |
| Меха | object | розмір 1–10, модулі (тіло, руки, ноги, голова, хвіст, крила), рухові системи, кабіна, MV/TR | керується меню: швидкість, поворот, реверс, режим руху; кожен модуль має броню й ушкодження |
| Модуль мехи | object | розмір, броня ≤ розміру мехи | знищений — втрачається функція (ноги → рух, рука → зброя в руці) |
| Зброя (особиста / мехова) | object | дальність, шкода, магазин, перезарядка ~30 кліків, BV (черга) | після пострілу недоступна до перезарядки; ракети — частка залпу |
| Супутник (lancemate) | ally | навички, власна меха | бʼється поруч; тактику задаєш розмовою |
| NPC | neutral | реакція (подобається / байдуже / ворожий), терпіння | дає місії, чутки, знижки; може стати ворогом |
| Ворог (бандит, монстр, ворожа меха) | enemy | фракція | бій за тими ж правилами дії й годинника |
| Фракція | zone | союзники й вороги | стосунки змінюють реакцію NPC і доступні місії |
| Місцевість | terrain | тип, висота | ліс/руїни/болото сповільнюють колеса; вода — лише ховер або глибина |
| Крамниця (KiRin MegaMart, Mecha Sporch…) | neutral | — | особисті товари в рюкзак, мехові — у «wargear» |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух пішки й у мехі:
- КОЛИ `input(dir)` (пішки) → ЯКЩО `free(cell)` → ТО `move(pc, dir)`; набігання на ворога — атака.
- КОЛИ `input([ або ])` → ТО `rotate(pc, 45)` ліворуч/праворуч; `input(=)` → `move(pc, facing)` кроком; `input(+)` → бігом.
- КОЛИ `input(cruise|full)` (меха) → ТО `custom: «меха рухається вперед за напрямом із цією швидкістю»`; `full` → ТО `custom: «штраф до влучання»`.
- КОЛИ `input(turn_left|turn_right|reverse)` → ЯКЩО `legal(move)` → ТО `face(mecha, ±45)` / задній хід.
- КОЛИ `enter(mecha, terrain)` → ЯКЩО `custom: «режим ходьби»` → ТО `custom: «краще долає пересічену, швидко повертає»`; колеса → `speed(+n)` на дорозі, `speed(−n)` на важкій; ховер → проходить низькі перешкоди й воду.
- КОЛИ `input(movemode, m)` → ЯКЩО `custom: «меха має такі рухові системи»` → ТО `custom: «перемкнути режим (walk/roll/skim/fly/jump)»`.
- КОЛИ `counter(legs_working, <=, half)` → ТО `custom: «меха втрачає рух»`.

Бій:
- КОЛИ `input(fire, weapon, target)` → ЯКЩО `custom: «зброя перезаряджена»` → ТО `damage(n)` за кидком навички; `custom: «зброя чекає ~30 кліків»`.
- КОЛИ `input(called_shot)` → ТО `custom: «обрати модуль цілі; влучити важче»`.
- КОЛИ `custom: «BV ракет = 1/4»` → ТО `custom: «вилітає чверть боєкомплекту»`.
- КОЛИ `custom: «влучання в меху»` → ТО `damage(module, n)`; ЯКЩО `hp_zero(module)` → ТО `custom: «функцію модуля втрачено»`; ЯКЩО знищено кабіну/тіло → ТО `custom: «меха виведена з ладу»`.
- КОЛИ `input(wait_for_recharge)` → ТО `custom: «годинник іде до першої готової зброї»`.

Досвід і розвиток:
- КОЛИ `custom: «ухилився від атаки»` → ТО `counter(xp, +1)`; влучив → +1; знищив головну ціль → +5; інший обʼєкт → +1.
- КОЛИ `input(train, skill)` → ЯКЩО `counter(xp, >=, cost)` → ТО `custom: «+1 ранг (макс 15)»`; забагато навичок понад Knowledge → `custom: «дорожче»`.
- КОЛИ `custom: «виконані передумови таланту»` → ТО `choose(talent)` (Born to Fly: +3 до пілотування в польоті, Tech Vulture: знімати модулі з переможених…).

Меха, гараж і NPC:
- КОЛИ `input(board, mecha)` → ТО `custom: «пілот у кабіні, гра на шкалі мех»`; `input(eject)` → назад пішки.
- КОЛИ `input(install, part)` у Field HQ → ЯКЩО `custom: «правила конструкції (одне тіло, одна кабіна, руки лише в руках…)»` → ТО `custom: «стати мехи перераховуються»`; інакше `message(помилка)`.
- КОЛИ `input(chat, npc)` → ТО `counter(reaction, +n)`, `counter(patience, −1)`; ЯКЩО `counter(reaction, >, n)` → ТО `custom: «знижки, місії, чутки»`.
- Сюжет: КОЛИ `custom: «кінець епізоду»` → ТО `custom: «завантажити випадковий підсюжет XRAN за ворогом/фракцією/таємницею»`, `counter(difficulty, +n)`; ЯКЩО `counter(difficulty, >, 75)` → ТО `custom: «фінальний епізод»`.
- Поразка: `hp_zero(pc)` → смерть персонажа (або порятунок з постійною травмою, з пізніших версій). Перемога: завершити кампанію; на арені — бої за гроші й славу.

## Керування і ввід
- Пішки — roguelike-клавіші: цифри/стрілки (8 напрямків) або «черепаха»: `[`/`]` — поворот, `=` — крок, `+` — біг.
- У мехі — меню (як у MechFight / Titans of Steel): Cruise/Full Speed (або Walk/Run), Turn Left/Right, Reverse, режими руху, Stop/Wait, Weapons Menu, Info Menu, Options, Search; в опціях можна перемкнутись на roguelike-керування мехою.
- `C` — персонаж (рюкзак, травми, тренування, Field HQ), `H` — Field HQ, `i`/`e` — інвентар/спорядження, розмова з NPC — меню реплік.

## Вікна, меню, HUD
- `main-menu`: Start / Load RPG Campaign · New / Load Arena Unit · Create Character · Edit Map · View Design Files · View Color Selector · Quit.
- `character-select` / створення: 8 статів, 30 навичок, передісторія (сирота, біженець з Місяця, амнезія, родина загинула, колишній член Aegis).
- `game-screen`: мапа (блакитна рамка) + інфовікно (імʼя, індикатор напряму/висоти/руху `G`/`S`, HP або схема пошкоджень модулів мехи) + вікно меню + **годинник** + `message-log`.
- `inventory-window` «Backpack» (спорядження / інвентар, `/` перемикає); `stats-window` View Injuries (кінцівки); `custom-window` Training.
- `vehicle-design` — Field HQ: список wargear, передача предметів між мехами, ремонт, Examine Parts → Remove/Install Part з живими статами (швидкість, маневреність).
- `dialogue-window` з двома смугами: реакція (зелена/жовта/червона) і терпіння (`Zz`).
- `shop-window` (KiRin MegaMart), `editor-window` (Edit Map), `custom-window` (дизайн-файли мех, вибір кольорів).

## Фічі поза полем
- `save-multi-slot` — кілька персонажів у теці SaveGame; готові персонажі автора для старту.
- `procedural-plot` — кампанія з випадкових епізодів під передісторію; випадкові квести зі скриптів.
- Режим Arena Unit — окрема кампанія команди пілотів і мех.
- Увесь контент (предмети, мехи, сюжети, монстри) — у текстових файлах: легко модувати (`mod-support`).
- ASCII- і SDL-версії; опція тактичного (покрокового) режиму.

## Варіації й родичі
- GearHead 2 (2008 (?)) і GearHead Caramel (Steam/itch, Python) — той самий світ і генератор сюжетів; у Caramel рух і дії розділені, є стаміна на бонусні дії.
- Родичі: [cogmind](cogmind.md) (робот із модулів, що відпадають), [caves-of-qud](caves-of-qud.md) (кінцівки й фракції), MechWarrior / BattleTech (локаційні ушкодження, напрям мехи), Titans of Steel (годинник дій).
- Осі варіацій: **рух** (8 напрямків / поворот + крок / рух із моментом); **шкала** (одна / дві шкали з пересадкою); **пошкодження** (єдине HP / HP за модулями з утратою функцій); **час** (хід = хід / годинник тривалостей / тактичні ходи).

## Цікавинки для курсу
- «Черепашачий» рух: стан = позиція + напрям, команди «поворот / крок / біг» — 📎.
- Дві шкали одного світу з пересадкою в меху — 🥈 (два набори правил руху й бою, спільний стан пілота).
- Модульне HP: удар у модуль, утрата функції (ноги на половині → нема руху) — 🥉.
- Режими шасі × місцевість: таблиця «режим × тип клітини → вартість/заборона» — 📎.
- Годинник тривалостей: черга дій за часом завершення, перезарядка зброї в кліках — 🥈.
- Генератор сюжету з епізодів зі змінними (ворог, фракція, таємниця, складність до 75) — 🥇.
- Конструктор мехи з правилами валідності (одне тіло, кабіна, руки лише в руках) — 🥈.

## Мапа на каталог
- Є: `move-8dir` · `keyboard-controls` · `hp-damage` · `inventory` + `inventory-items` · `unit-xp-skills` · `height-levels` (пагорби, глибина) · `projectile-shot` · `shoot-burst` (BV) · `shoot-cooldown` (перезарядка) · `melee-vs-ranged` · `fog-of-war` · `message-log` · `status-panel` · `shop-catalog` · `round-currency` · `save-multi-slot` · `dungeon-generation` (шахти, випадкові мапи) · `in-game-editor` (Edit Map) · `main-menu`.
- **Нема** → пропозиції карток:
  - `+turtle-movement` «Поворот + крок вперед» · entities/move · 📎 · слот {turn_step: 45|90}.
  - `+dual-scale` + `+mecha-board-eject` «Дві шкали світу; сісти в техніку / катапультуватись» · entities/state · 🥈.
  - `+move-modes` + `+terrain-move-cost` «Режим руху × місцевість» · entities/legality · 📎 · слоти {modes, cost_table}.
  - `+speed-attack-penalty` «Повна швидкість — штраф до влучання» · entities/combat · 🌱.
  - `+clock-action-time` «Годинник: кожна дія має тривалість» · game-logic/opponent · 🥈.
  - `+body-part-targeting` + `+limb-disable` «Прицільний постріл у модуль; утрата функції» · entities/combat · 🥉.
  - `+mecha-design` «Конструктор із правилами валідності» · entities/state · 🥈.
  - `+procedural-plot` «Сюжет із випадкових епізодів» · levels/generation · 🥇.
  - `+npc-reaction` + `+faction-reputation` «Реакція NPC і фракцій» · game-logic/economy · 📎.
  - `+talent-prereq` · `+salvage-parts` · `+xp-for-dodge` · `+recruit-ally` · `+data-driven-content` — дрібніші.

## Пропозиції до словників
- `+axis:control=turtle` — нове значення осі `control`: поворот і крок окремими командами.
- `+axis:scale` — `single` / `dual` (особиста + техніка, як тут).
- `+cond:move_mode(a, m)` — сутність у режимі руху (walk/roll/skim/fly).
- `+effect:board(a, vehicle)` / `+effect:eject(a)` — сісти в техніку / вийти.
- `+effect:disable_part(a, part)` — модуль знищено, його функція недоступна.
- `+window:vehicle-design` — гараж/конструктор техніки зі статами.
- `+ui:reaction-meter` — смуги «ставлення» й «терпіння» NPC у розмові.
- `+feature:procedural-plot` — генератор сюжету з епізодів.

## Джерела
- ⭐ [RogueBasin: GearHead](https://www.roguebasin.com/index.php/GearHead) — дві шкали, «черепаха», випадкові підсюжети, навички, дизайн мехів, текстові дані.
- [gearheadrpg.com](http://www.gearheadrpg.com/) — сімʼя ігор, лінки на код і магазини.
- [GitHub: gearhead-1](https://github.com/jwvhewitt/gearhead-1) — `readme.md` (екран, годинник, меню мехи, режими руху, перезарядка 30 кліків, called shot, BV), `doc/Introduction.txt` (8 напрямків і turtle-клавіші, бойові навички), `doc/TheRules.txt` (конструкція, ноги, XP), `doc/man_mecha.txt` (Field HQ), `doc/talking.txt`, `doc/xranplot.txt`, `doc/terrain list.txt`, `history.txt` (реліз 0.500 — 10.05.2002), `pcaction.pp` (меню руху).
- [Steam: GearHead Caramel](https://store.steampowered.com/app/1565090/GearHead_Caramel/) — сучасний наступник.
- YouTube: [пошук «GearHead roguelike mecha gameplay»](https://www.youtube.com/results?search_query=GearHead+roguelike+mecha+gameplay).

## Непевне
- (?) Чи меха в режимі Cruise сама рухається далі, доки не «Stop» (момент), чи робить один крок — у меню є Stop і індикатор `G`/`S`, але код руху не читав.
- (?) Кут повороту (45°) — за 8 напрямками сітки; явно ніде не сказано.
- (?) Рік GearHead 2 і деталі Caramel — лише зі сторінки gearheadrpg.com і памʼяті.
- (?) Порятунок замість смерті з постійною травмою — з `history.txt` («Rescued PCs more likely to suffer permanent injuries»), умови порятунку не перевірені.
