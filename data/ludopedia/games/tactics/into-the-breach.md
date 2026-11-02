---
title: Into the Breach
slug: into-the-breach
family: tactics
also: [roguelike, chess-abstract]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2018
platforms: [PC, Mac, Linux, Switch, Stadia, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Into_the_Breach", note: "огляд: 8×8, три мехи, телеграфовані атаки, енергомережа, острови, повернення в часі"}
  - {kind: other, url: "https://www.ludo.guide/guide/into-the-breach/game-mechanics", best: true, note: "фази ходу по порядку, усі плитки, статуси, природні загрози — найповніший перелік правил"}
  - {kind: other, url: "https://www.ludo.guide/guide/into-the-breach/islands", note: "острови, їхні плитки, регіони, фінал"}
  - {kind: other, url: "https://www.gamepressure.com/into-the-breach/combat/z1aa78", note: "плитки, випадкові події, огляд Vek"}
  - {kind: other, url: "https://www.ludo.guide/guide/into-the-breach/veks", note: "усі Vek, Alpha-версії, псіони, боси — атаки й числа"}
  - {kind: steam, url: "https://store.steampowered.com/app/590380/Into_the_Breach/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=into+the+breach+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 70
mechanics: [telegraphed-intents, push-object, hp-damage, impassable-cells, floor-types, environment-death, spawn-points, spawn-animation, melee-vs-ranged, projectile-shot, blast-wave, temporary-modes, destroy-all-enemies, legal-move-highlight, difficulty-levels, shop-between-levels, in-round-upgrades, +collision-damage, +resolution-order, +spawn-block, +protect-structures, +turn-limit-survive, +reset-turn, +pilot-xp-skills, +run-meta-carry]
proposes: ["+trigger:telegraph_resolve", "+effect:bump", "+effect:set_status", "+cond:status", "+role:structure", "+ui:attack-order", "+ui:grid-power-bar", "+window:squad-select", "+window:island-map", "+window:pilot-levelup", "+window:timeline-lost", "+feature:reset-turn", "+axis:session"]
author: opus
date: 2026-11-02
---

# Into the Breach — шахова задача на 8×8: вороги кажуть, куди вдарять, а ти переставляєш світ

## Суть
Три мехи захищають міські будівлі від комах-Vek на полі 8×8. На початку ходу гравця всі атаки ворогів **уже оголошені** (стрілки й підсвітки на клітинах) — гравець бачить майбутнє і має так зсунути ворогів, щоб удари пішли в порожнечу, в інших ворогів чи у воду. Головний інструмент — не шкода, а **штовхання**: зброя мехів зсуває цілі, зіткнення ранить обох. Програш — коли згасне енергомережа (будівлі), а не коли загинуть мехи; після програшу один пілот іде в нову часову лінію (роглайк-забіг).

## Поле і час
- Поле 8×8 квадратних клітин, ізометричний рендер; кожна клітина — тип місцевості (земля, гора, вода, ліс, пісок, лід, кислота, лава, прірва, будівля) + можливий юніт + можливий статус клітини (вогонь, дим, кислотна калюжа).
- Бій — 4–5 ходів (лічильник «Turns remaining»); мета — пережити їх, зберігши мережу. Час покроковий, без таймера.
- Хід = фаза ворога + фаза гравця. Фаза ворога розкладена на детермінований **порядок розвʼязання**: вогонь → дим Storm Generator → природні загрози (повінь, лава, блискавки, повітряний удар, конвеєри) → регенерація від псіонів → дії союзних ботів → дії ворогів (у порядку номерів) → рух потяга / запуск супутника → поява нових Vek → **усі** Vek рухаються й оголошують нові атаки → хід гравця (ludo.guide).
- Інформація часткова: наміри ворогів, наступні точки появи й ефекти середовища видно; нові Vek, що зʼявляться пізніше, — ні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мех Prime (ближній) | piece | HP 3–4, рух 3–4, масивний | удар по сусідній клітині, часто зі штовханням (Titan Fist: 2 шкоди + push) |
| Мех Brute (лінійний) | piece | HP 3, рух 3 | снаряд по прямій до першої перешкоди (Taurus Cannon: 1 шкода + push) |
| Мех Ranged (артилерія) | piece | HP 2–3, рух 3 | дугою через перешкоди; шкода в центр, штовхання сусідів назовні (Artemis) |
| Мех Science (підтримка) | piece | HP 2–3, рух 4, часто летить | без шкоди: тягне, щит, дим, телепорт |
| Уламок меха | static | — | мех з HP 0: непрохідна перешкода до кінця бою; пілот гине (?) |
| Vek ближнього бою (Hornet, Scorpion, Beetle) | enemy | HP 2–5, рух 2–5 | підходить і оголошує удар у сусідню клітину / ривок по лінії |
| Vek-стрілець (Firefly, Centipede) | enemy | — | снаряд по прямій до першої цілі; Centipede лишає кислоту |
| Vek-артилерія (Scarab, Crab) | enemy | дальність 5 | дугою через перешкоди; Crab — по 2 клітинах |
| Leaper / Scorpion | enemy | — | павутина: ціль не рухається (`webbed`), удар наступного ходу |
| Blobber / Spider | enemy | — | кладе яйце / слиз, що вибухає чи вилуплюється наступного ходу |
| Burrower | enemy | не штовхається | бʼє 3 клітини в ряд; після шкоди ховається |
| Psion (Soldier/Shell/Blood/Blast) | enemy | аура | усім Vek: +1 HP / −1 шкоди / регенерація / вибух при смерті |
| Psion Tyrant | boss | — | у кінці кожного ходу 1 шкоди всім юнітам гравця (лише Volcanic Hive) |
| Alpha-версії | enemy | більше HP і шкоди | той самий патерн атаки, сильніший |
| Боси (Spider Leader, Large Goo…) | boss | масивні | не тонуть; спецправила (яйця, поділ) |
| Будівля мережі | static | 1–2 «поверхи», може мати щит | будь-яка шкода/зіткнення → −1 енергомережі; 2-поверхова витримує 2 |
| Обʼєктивна споруда (поїзд, дамба, електростанція…) | static | — | ціль місії: захистити / зруйнувати |
| Капсула часу (time pod) | pickup | падає з позначкою | підняти мехом до кінця бою; знищується шкодою; дає пілота або ядро |
| Нора появи (cracked ground) | spawner | — | наступного ходу звідси вилізе Vek; заблокувати тілом |
| Гора | static | 2 удари | блокує рух і снаряди; удар → пошкоджена гора → уламки |
| Земля | terrain | — | звичайна клітина |
| Вода | terrain | — | Vek без польоту/масивності тоне; мех не стріляє й не лікується; гасить вогонь |
| Лава | terrain | — | як вода + підпалює вцілілого |
| Кислота (A.C.I.D.) | terrain/hazard | — | калюжа: перший, хто зупинився, отримує `acid` (подвійна шкода від зброї) |
| Ліс | terrain | — | від шкоди спалахує: `fire` на клітині |
| Пісок | terrain | — | від шкоди → дим |
| Лід | terrain | 2 удари | удар → тріснутий лід → вода; вогонь топить |
| Прірва | hazard | — | наземний юніт падає й гине; летючий — ні (якщо не заморожений) |
| Дим | hazard | статус клітини | юніт у димі не атакує і не лікується; скасовує вже оголошену атаку |
| Вогонь | hazard | статус | 1 шкоди на початку ходу; знімається водою/лікуванням/заморозкою |
| Конвеєр | terrain | напрям | перед діями ворогів зсуває юніт на 1 |
| Телепорт (пара) | terrain | — | хто став — миттєво з'являється на парній клітині |
| Міна (Old Earth Mine) | hazard | — | хто ввійшов — гине |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО кожен Vek уже має оголошену атаку: напрямок **привʼязаний до Vek** (зсув Vek зсуває й удар), а ціль-клітина — туди, куди дивиться зброя (custom: «атака = вектор від позиції Vek, не від цілі»).
- КОЛИ `input(move, mech, cell)` → ЯКЩО `legal(path ≤ move)` → ТО `move(mech, cell)`; після руху мех може використати одну зброю або «Repair» (+1 HP, знімає вогонь/кислоту/павутину).
- КОЛИ `input(fire, weapon, cell)` → ТО `damage(n)` по цілі, `push(target, dir)` за патерном зброї.
- КОЛИ `after(push(a, dir))` → ЯКЩО `free(cell_behind)` → ТО `move(a, dir)`; інакше `custom: «bump»`: `damage(1)` юніту **і** тому, у що вдарився (юніт, гора, будівля → −1 мережі); юніт лишається на місці.
- КОЛИ `enter(vek, water|chasm)` → ЯКЩО `not state(vek, flying|massive)` → ТО `disappear_a` (тоне/падає); лава — те саме + `set_state(fire)`.
- КОЛИ `enter(unit, acid_pool)` → ТО `set_state(unit, acid)`, `set_cell(ground)`; `acid` → шкода від зброї ×2 (не від bump і вогню).
- КОЛИ `after(damage, forest)` → ТО `set_cell(fire)`; `after(damage, sand)` → `set_cell(smoke)`; `after(damage, ice)` → `set_cell(damaged_ice)`, другий раз → `set_cell(water)`; `after(damage, mountain)` ×2 → `set_cell(rubble)`.
- КОЛИ `turn_start(enemy)` → ЯКЩО `state(unit, fire)` → ТО `damage(1)` (першим у порядку, до дій ворогів).
- КОЛИ `custom: «phase enemy_actions»` → ТО кожен Vek у порядку номерів виконує атаку в **поточний** вектор; ЯКЩО `state(vek, smoke|frozen|dead)` → ТО `custom: «атака скасована»`.
- КОЛИ `contact(attack, building)` → ЯКЩО `rng(grid_defense%)` → ТО `custom: «будівля встояла»`; інакше `damage(building)`, `counter(grid_power, -1)`.
- КОЛИ `contact(attack, vek)` → ТО `damage(n)` йому (friendly fire — головний прийом).
- КОЛИ `custom: «phase vek_emerge»` → ЯКЩО `occupied(crack, unit)` → ТО `damage(1)` тому, хто стоїть, і `custom: «Vek не зʼявляється»` (блок тілом).
- КОЛИ `contact(mech, time_pod)` → ТО `pickup`; КОЛИ `after(damage, time_pod)` → ТО `disappear_a`.
- КОЛИ `state_on(unit, frozen)` → ТО не рухається й не атакує; КОЛИ `after(damage|push|bump|fire, frozen_unit)` → ТО `clear_state(frozen)` (шкода поглинається (?)); Repair у замороженому стані можна.
- КОЛИ `after(damage|bump, unit)` → ЯКЩО `state(unit, shielded)` → ТО `clear_state(shield)` без HP-втрат; щит також блокує заморозку.
- КОЛИ `hp_zero(mech)` → ТО `transform(wreck)`; КОЛИ `hp_zero(vek)` → ТО `disappear_a`, пілотам `counter(xp, +1)`.
- КОЛИ `counter(turns_left, ==, 0)` → ТО `win` (бій), нагорода за виконані додаткові цілі (★ репутація / +1 мережа / ядро).
- КОЛИ `counter(grid_power, ==, 0)` → ТО `lose` (кінець часової лінії) → вибір пілота для нової лінії.
- Перемога забігу: зруйнувати вулик на вулканічному острові (фінальний бій у дві фази) · Поразка: мережа = 0 · Рахунок: кількість врятованих цивільних (людей у будівлях) за забіг.

## Керування і ввід
- Мишею: клік по меху → підсвітка досяжних клітин (`legal-move-highlight`) → клік по клітині; вибір зброї (кнопки знизу або 1/2) → клік по цілі з **превʼю наслідку** (шкода, стрілки штовхання, хто зіткнеться).
- Мехи ходять у будь-якому порядку; рух можна скасовувати («Undo Move») скільки завгодно, доки **жоден** мех не атакував.
- **Reset Turn** — раз за бій повертає весь хід гравця на початок.
- Наведення на будь-яку клітину/ворога показує тип клітини, HP, статуси, атаку; утримання кнопки «Attack Order» нумерує порядок дій ворогів.
- Підтримка геймпада й тачу (Switch/мобільні).

## Вікна, меню, HUD
- `main-menu`: Continue · New Game → `squad-select` (ангар: готові загони, випадковий, свій набір) → вибір пілотів · Options → `settings-window` · Profile/Statistics · Achievements · Quit.
- `custom-window` «Island select» — карта світу з 4 корпоративними островами + вулкан; далі «region map» острова: регіони з місіями, превʼю нагород (★, мережа, ядро) і цілей.
- `custom-window` «Deploy» — розстановка трьох мехів у жовту зону перед боєм.
- `game-screen`: поле 8×8; зверху `grid-power-bar` (сегменти до 7) і відсоток Grid Defense; `turn-counter` «Turns remaining»; `objective-text` з чекбоксами бонус-цілей; зліва портрети мехів з `hp-bar` і пілотом; знизу `ability-buttons` (зброя, Repair); `telegraph-marker` — стрілки й червоні клітини атак, жовті — події середовища; `threat-range`; `tooltip` клітини; кнопки `undo-button` (Undo Move), Reset Turn, `end-turn-button`; кнопка «Attack Order».
- `upgrade-window` — підвищення рівня пілота: вибір із двох навичок (?), і екран мехів, куди вставляти ядра й зброю.
- `shop-window` — після острова: витратити репутацію на зброю, ядра, +1 мережі.
- `end-screen` — підсумок місії (виконані цілі, нагорода); «timeline lost» — вибір пілота, якого відправити в минуле; фінальна перемога зі статистикою.
- `confirm-dialog` (Reset Turn, End Turn з невикористаними мехами), `pause-menu` (Continue, Options, Abandon Timeline).

## Фічі поза полем
- **Забіг**: обрати загін → 4 корпоративні острови (Archive, R.S.T., Pinnacle, Detritus) у будь-якому порядку (після 2 захоплених відкривається Volcanic Hive, або 3/4 для сильнішого загону) → кожен острів має 8 регіонів: встигаєш 4 місії, далі оборона HQ (бос), решту 3 захоплюють Vek → магазин.
- `meta-progression`: пілот, що пережив, переноситься в новий забіг; монетки за досягнення відкривають нові загони й пілотів.
- Ядра реакторів: вмикають апгрейди зброї (+шкода, +ефект) і характеристик меха (HP, рух).
- Пілоти: досвід за вбивства → рівні (2 рівні?) → навички; кожен пілот має унікальну здібність (політ, щит на старті, рух після атаки, імунітет до диму тощо).
- `difficulty-presets`: Easy · Normal · Hard · Unfair (Advanced Edition).
- `autosave` після кожного ходу (вийти посеред бою можна), `achievements`, `stats` (профіль), `colorblind-palette`/доступність (?), Advanced Edition: нові загони, вороги, нові цілі місій.

## Варіації й родичі
- Advanced Edition (безкоштовне оновлення, 19.07.2022): +5 загонів, майже 40 нових зброй, 4 пілоти й утричі більше навичок пілотів, нові вороги й боси, нові цілі місій, складність Unfair.
- Наступники ідеї «видно намір»: Slay the Spire (наміри ворога — числом), Tactical Breach Wizards, Hoplite (ворог бʼє за правилом, яке видно), Mech Armada, Islanders-подібні.
- **Осі варіацій**: телеграф — немає / тип атаки / точна клітина й порядок (ITB) · ціль гравця — вбити всіх / захистити структури / вижити N ходів · шкода — HP / штовхання / середовище · відкат — нема / рух до атаки / весь хід раз за бій.

## Цікавинки для курсу
- Телеграфовані атаки, привʼязані до вектора ворога: штовхнеш Vek — його удар полетить в іншу клітину — 🥈 (стан «намірів» + перерахунок після кожної дії гравця).
- Фаза ворога як впорядкований конвеєр (вогонь → середовище → дії за номерами → поява) — 🥉; з повним превʼю наслідків ходу гравця (симуляція на копії стану) — 🥇.
- Штовхання із зіткненням (bump = 1 шкоди обом, будівля → мережа) — 📎 поверх `push-object`.
- Плитки, що змінюються від шкоди (ліс → вогонь, пісок → дим, лід → тріщина → вода, гора 2 HP) — 🥉 як таблиця взаємодій.
- Блокування появи тілом (поставив меха на нору — Vek не вилазить, 1 шкоди) — 🌱.
- Reset Turn раз за бій + Undo Move до атаки — 📎 (знімок стану).
- Глобальний ресурс «енергомережа» замість HP героїв — 🌱, але змінює весь стиль гри.

## Мапа на каталог
- Є: `telegraphed-intents` ↔ оголошені атаки · `push-object` ↔ штовхання зброєю · `hp-damage` · `impassable-cells` (гори, будівлі) · `floor-types` (вода, лава, лід, кислота, ліс, пісок) · `environment-death` (утоплення, прірва) · `spawn-points` + `spawn-animation` (нори, що тріснули) · `melee-vs-ranged` (ближній/лінійний/артилерія) · `projectile-shot` · `blast-wave` (артилерія зі штовханням сусідів) · `temporary-modes` (вогонь, лід, щит, дим, кислота) · `destroy-all-enemies` (деякі бонус-цілі) · `legal-move-highlight` · `hover-highlight` · `difficulty-levels` · `shop-between-levels` · `in-round-upgrades` (ядра) · `save-autosave` · `game-screen` · `main-menu` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+collision-damage` «Шкода від зіткнення при штовханні» · entities/combat · 📎 · слот {dmg: 1} — дитина `push-object`.
  - `+resolution-order` «Впорядкована фаза ворога» · game-logic/opponent · 🥉 · слот {phases: list} — вогонь → середовище → дії → поява.
  - `+spawn-block` «Блок точки появи тілом» · entities/spawn · 🌱.
  - `+protect-structures` «Захистити споруди (спільний ресурс)» · game-logic/lose · 📎 · слот {pool: grid_power}.
  - `+turn-limit-survive` «Протриматись N ходів» · game-logic/win · 🌱 · слот {turns}.
  - `+reset-turn` «Відкат ходу раз за бій» · game-logic/difficulty · 📎 · слот {uses: 1}.
  - `+pilot-xp-skills` «Досвід і навички загону» · entities/state · 🥉.
  - `+run-meta-carry` «Перенесення юніта між забігами» · levels/progression · 📎.

## Пропозиції до словників
- `+trigger:telegraph_resolve` — момент, коли оголошена атака виконується (фаза ворога); відмінне від `turn_start`, бо атаки розвʼязуються по черзі.
- `+effect:bump` — зіткнення при штовханні в зайняте: шкода обом, без руху.
- `+effect:set_status` / `+cond:status` — статуси юнітів і клітин (fire, acid, frozen, smoke, webbed, shielded); близько до `set_state`, але стосуються й клітин.
- `+role:structure` — споруда-ціль захисту (будівля мережі, поїзд, дамба): не рухається, має HP, ворожі атаки по ній — головна загроза.
- `+ui:attack-order` — кнопка-оверлей з номерами черговості дій ворогів; `+ui:grid-power-bar` — шкала спільного ресурсу «HP бази».
- `+window:squad-select` — вибір загону (3 фігури разом); `+window:island-map` — карта островів/регіонів із превʼю нагород; `+window:pilot-levelup` — вибір навички; `+window:timeline-lost` — вибір, кого перенести в новий забіг.
- `+feature:reset-turn` — одноразовий відкат ходу.
- `+axis:session` — тут `run` (забіг з кількох боїв, кінець = смерть мережі).

## Джерела
- ⭐ [ludo.guide: Game mechanics](https://www.ludo.guide/guide/into-the-breach/game-mechanics) — порядок фаз ходу, плитки, статуси, середовище.
- [Wikipedia](https://en.wikipedia.org/wiki/Into_the_Breach) — огляд механік, дати платформ (PC 2018 … iOS/Android через Netflix 2022), Advanced Edition.
- [ludo.guide: Islands](https://www.ludo.guide/guide/into-the-breach/islands) — 4 острови + Volcanic Hive, 8 регіонів, оборона HQ.
- [ludo.guide: Veks](https://www.ludo.guide/guide/into-the-breach/veks) — атаки всіх Vek, Alpha, псіони, боси.
- [gamepressure: Combat](https://www.gamepressure.com/into-the-breach/combat/z1aa78) — плитки, випадкові події (міни, лава, Ice Storm, валуни), блок нори = 1 шкоди.
- [Steam](https://store.steampowered.com/app/590380/Into_the_Breach/) — опис, склад Advanced Edition.
- YouTube: пошук «into the breach gameplay».

## Непевне
- (?) Що стається з пілотом і мехом при HP 0: пілот гине, мех після бою ремонтується з ШІ-пілотом — з памʼяті.
- (?) Grid Defense 15 % на старті — лише з форумів (GOG); ліміт мережі 7 і «надлишок → +Grid Defense» — з памʼяті.
- (?) Характеристики мехів (HP, рух) і назви/шкода зброї (Titan Fist, Taurus Cannon, Artemis) — з памʼяті; заморожений юніт не отримує шкоди від удару — з памʼяті.
- (?) Пілот: кількість рівнів і вибір «з двох навичок» — з памʼяті.
- (?) Рахунок забігу = врятовані цивільні — з памʼяті.
