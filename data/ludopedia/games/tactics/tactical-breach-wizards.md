---
title: Tactical Breach Wizards
slug: tactical-breach-wizards
aka: [TBW]
family: tactics
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: none
  goal: state
year: 2024
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tactical_Breach_Wizards", best: true, note: "загін до 5 чарівників, передбачення провидця, перемотка до кінця ходу, обовʼязкові й додаткові цілі (вікно, 2 ходи), редактор рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1043810/Tactical_Breach_Wizards/", note: "вікна-дефенестрація, безкоштовні перемотки, некромедик, перки вмінь, складність Easy/Medium/Hard + змінні"}
  - {kind: official, url: "https://www.pentadact.com/2024-08-22-tactical-breach-wizards-is-out/", note: "блог Tom Francis (розробник): анонс релізу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tactical+Breach+Wizards+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [push-object, environment-death, hp-damage, impassable-cells, melee-vs-ranged, line-of-sight-attack, status-effects, telegraphed-intents, threat-range, legal-move-highlight, hover-highlight, undo-redo, undo-unlimited, destroy-all-enemies, unit-xp-skills, level-select, sequential-levels, difficulty-levels, game-settings, in-game-editor, editor-window, game-screen, main-menu, end-screen, +reset-turn, +collision-damage, +window-defenestration, +foresight-preview, +bonus-objectives, +kill-to-revive, +door-breach-opening, +ability-perks, +cosmetic-unlock-by-objectives, +custom-difficulty-variables]
proposes: ["+effect:bump", "+effect:knockback", "+effect:revive", "+trigger:breach", "+role:window-cell", "+ui:foresight-ghost", "+ui:objective-checklist", "+window:breach-banter", "+window:perk-select", "+window:outfit-select", "+feature:turn-rewind", "+feature:difficulty-variables", "+axis:undo"]
author: opus
date: 2026-11-09
---

# Tactical Breach Wizards — спецназ чарівників: вибиваєш двері, бачиш майбутнє, викидаєш ворогів у вікна, а невдалу спробу перемотуєш

## Суть
Покрокова тактика загоном до п'яти чарівників у кевларі в тісних кімнатах будівель. Бій починається з вибивання дверей (breach); далі кожен чарівник має унікальні вміння — блискавка, що відкидає, перетворення на скаженого пса, «некромедик», який мусить спершу вбити пацієнта, щоб воскресити його з повним HP. Ядро — **відкидання**: вибити ворога у вікно (дефенестрація) або в інших. Провидець загону показує, як зіграє вибір, а перемотка в межах ходу безкоштовна — гра ближча до пазла, ніж до лотереї.

## Поле і час
- Квадратна сітка кімнат на поверхах будівель; клітини: підлога, стіни, двері, **вікна** (вихід назовні = вибуття ворога), укриття (?).
- Хід гравця: кожен чарівник діє в будь-якому порядку; дій на хід більше, ніж в Into the Breach (Steam); потім хід ворогів.
- Перемотка: будь-яку дію можна скасувати й спробувати інакше, доки хід не завершено (Wikipedia); перемотки безкоштовні (Steam).
- Інформація часткова: провидець бачить наслідок вибору / дії ворогів (?) наперед; що саме зроблять вороги без провидця — частково.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник загону (до 5) | piece | HP, набір умінь (?) mana/заряди | рух + уміння; вміння відкриваються з досвідом, перки — з прокачкою вміння |
| Провидець (Zan) | piece | передбачення | показує, як зіграє вибір; привʼязка імені до ролі — (?) |
| Відьма бурі (Jen) | piece | блискавка | удар блискавкою **відкидає** ворога (Wikipedia) |
| Некромедик | piece | — | лікує через смерть: вбити союзника, потім воскресити з повним HP |
| Перевертень-пес | piece | — | перетворення на скаженого пса (Steam), ближні атаки (?) |
| Ворог-силовик / маг | enemy | HP, атака | діє у ворожий хід; цілиться в чарівників |
| Traffic Warlock та інші «-локи» | enemy | — | ворожі маги-силовики; область атаки (?) |
| Вікно | hazard | — | ворог, відкинутий у вікно, вибуває одразу (дефенестрація; додаткова ціль) |
| Двері | gate | — | breach-точка: бій починається з виламування |
| Стіна | static | — | блокує рух і відкидання; зіткнення завдає шкоди (?) |
| Укриття / щити | static | — | (?) зменшують шкоду з одного боку |
| Ціль рівня (заручник, предмет) | object | — | обовʼязкова ціль місії (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «banter перед дверима»` → `input(breach, door)` → `set_cell(door, open)`, починається покроковий бій.
- КОЛИ `input(select, wizard)` → ТО `custom: «підсвітити досяжні клітини й цілі вмінь»`.
- КОЛИ `input(move, wizard, cell)` → ЯКЩО `legal(path)` → ТО `move(wizard, cell)`.
- КОЛИ `input(cast, ability, target)` → ЯКЩО `has(wizard, mana, cost)` (?) → ТО ефект уміння: `damage(n)` і/або `custom: «knockback»` за напрямком удару.
- КОЛИ `after(custom: «knockback»)` → ЯКЩО `free(cell_behind)` → ТО `move(target, dir)`; ЯКЩО `occupied(cell_behind, unit)` → ТО `custom: «bump»` — шкода (?) обом.
- КОЛИ `enter(enemy, window)` → ТО `disappear_a` (вибуває) і `counter(defenestrations, +1)`.
- КОЛИ `input(cast, kill_ally)` → ТО `hp(ally, 0)`; КОЛИ `input(cast, revive, ally)` → ЯКЩО `state(ally, dead)` → ТО `custom: «revive з повним HP»` (некромедик).
- КОЛИ `input(cast, transform)` → ТО `transform(dog)`: інший набір дій (?).
- КОЛИ `input(foresight)` → ТО `custom: «показати, як розіграється вибір / дія ворога»` (провидець).
- КОЛИ `input(rewind)` → ЯКЩО `turn_of(player)` → ТО `custom: «скасувати дію, стан як до неї»` без ціни.
- КОЛИ `input(end_turn)` → ТО `custom: «ворожий хід»`; перемотка цього ходу вже неможлива.
- КОЛИ `turn_start(enemy)` → ТО кожен ворог атакує / рухається (?) — порядок і ціль видно через передбачення.
- КОЛИ `hp_zero(wizard)` → ТО `set_state(wizard, down)` (?); некромедик може повернути.
- КОЛИ `all_constraints_met` → ТО `win` (обовʼязкові цілі рівня).
- КОЛИ `level_end` → ЯКЩО `custom: «виконано додаткову ціль»` (ворог у вікно, усі вороги за 2 ходи) → ТО `counter(confidence, +1)` → `unlock(outfit)`.
- КОЛИ `level_end` → ЯКЩО `first_time` → ТО `counter(xp, +n)` → нові вміння; повтор місії досвіду не дає.
- Перемога: обовʼязкові цілі місії · Поразка: загін вибув / провал цілі (?) · Рахунок: виконані додаткові цілі → Confidence.

## Керування і ввід
- Миша: клік по чарівнику → клік по клітині руху → кнопка вміння → клік по цілі з превʼю наслідку (шкода, траєкторія відкидання) (?).
- Rewind — скасувати останню дію в межах ходу; завершити хід — кнопкою.
- Вбудовані пауза, сповільнення й керування камерою (?) (блог розробника, для трейлерів).

## Вікна, меню, HUD
- `main-menu`: Продовжити · Місії (`level-select`) · Редактор рівнів (`editor-window`) · Налаштування (`settings-window`: складність + окремі змінні) · Вихід.
- `dialogue-window` — бантер загону перед breach і між місіями.
- `game-screen`: поле; портрети чарівників з `hp-bar` і ресурсом умінь (?); `ability-buttons`; `threat-range` / превʼю відкидання (`path-preview`); `objective-text` з обовʼязковими й додатковими цілями; `undo-button` (rewind); `end-turn-button`.
- `upgrade-window` — нові вміння з досвідом і перки вмінь.
- `skin-select` — спеціальні вбрання за Confidence (лише косметика).
- `puzzle-select` — «anxiety dreams» (?): челенджі, що відкривають особливі вміння; пост-гейм челенджі.
- `end-screen` — підсумок місії й виконаних цілей.

## Фічі поза полем
- Кампанія з послідовних місій; повтор місії без досвіду (`level-select`).
- `difficulty-presets`: Easy · Medium · Hard + `custom-difficulty` (окремі змінні складності).
- `level-editor` (Wikipedia); `undo` без ліміту в межах ходу.
- Anxiety dreams — необовʼязкові челенджі з унікальними вміннями; пост-гейм челенджі.
- Спецвидання: коментар розробника можна кидати у ворогів як зброю (Wikipedia).

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (бачиш наслідки, штовхання в небезпеку), [xcom](xcom.md) (загін, ворожий хід), [frozen-synapse](frozen-synapse.md) (тісні кімнати й прорив дверей).
- Поза корпусом: Fights in Tight Spaces (ring out), Door Kickers (прорив дверей), Gunpoint і Heat Signature (той самий автор).
- **Осі варіацій**: невдача — кубик (XCOM) / детерміновано + rewind (TBW) · передбачення — оголошені наміри (ITB) / провидець показує майбутнє · вибуття — HP / вікно / край.

## Цікавинки для курсу
- Відкидання + вікно як миттєве вибуття (дефенестрація) — 🌱 поверх `push-object` + `environment-death`.
- Безкоштовна перемотка до кінця ходу (стек знімків стану) — 📎.
- «Провидець»: симуляція наступного ходу ворогів на копії стану й показ привидами — 🥇.
- Лікування через смерть (некромедик): kill → revive з повним HP — 🌱, але цікава зміна правила.
- Додаткові цілі рівня (ворог у вікно, усе за 2 ходи) → косметичні нагороди — 📎.
- Складність як набір окремих перемикачів — 📎.

## Мапа на каталог
- Є: `push-object` ↔ відкидання · `environment-death` ↔ вікно · `hp-damage` · `impassable-cells` · `melee-vs-ranged` · `line-of-sight-attack` · `status-effects` · `telegraphed-intents` ↔ передбачення · `threat-range` · `legal-move-highlight` · `hover-highlight` · `undo-redo` / `undo-unlimited` ↔ rewind у ході · `destroy-all-enemies` (додаткова ціль) · `unit-xp-skills` · `level-select` · `sequential-levels` · `difficulty-levels` · `game-settings` · `in-game-editor` / `editor-window`.
- **Нема** → пропозиції карток:
  - `+reset-turn` «Відкат дій у межах ходу» · game-logic/history · 📎.
  - `+collision-damage` «Шкода від зіткнення при відкиданні» · entities/combat · 📎.
  - `+window-defenestration` «Клітина-вікно: відкинутий вибуває» · entities/death · 🌱.
  - `+foresight-preview` «Симуляція ходу ворога наперед» · game-logic/opponent · 🥇.
  - `+bonus-objectives` «Додаткові цілі рівня» · game-logic/win · 📎.
  - `+kill-to-revive` «Воскресіння повним HP через смерть» · entities/death · 🌱.
  - `+door-breach-opening` «Бій починається з прориву дверей» · levels/progression · 🌱.
  - `+ability-perks` «Перки вміння з його прокачкою» · entities/state · 🥉.
  - `+cosmetic-unlock-by-objectives` «Косметика за додаткові цілі» · levels/progression · 🌱.
  - `+custom-difficulty-variables` «Складність окремими перемикачами» · game-logic/difficulty · 📎.

## Пропозиції до словників
- `+effect:bump` — зіткнення при відкиданні в зайняте (як у Into the Breach, Fights in Tight Spaces).
- `+effect:knockback` — відкинути ціль на N клітин від джерела удару (відмінне від `push`, де рушить той, хто штовхає).
- `+effect:revive` — повернути вибулу сутність з HP.
- `+trigger:breach` — старт бою з прориву дверей (рівень починається дією гравця).
- `+role:window-cell` — клітина-вікно: вихід назовні для відкинутих (смертельний край усередині кімнати).
- `+ui:foresight-ghost` — привиди майбутніх позицій/дій; `+ui:objective-checklist` — обовʼязкові й додаткові цілі з галочками.
- `+window:breach-banter` — сцена перед дверима; `+window:perk-select` — вибір перка вміння; `+window:outfit-select` — вбрання за очки.
- `+feature:turn-rewind` — безкоштовна перемотка дій до кінця ходу; `+feature:difficulty-variables` — складність окремими параметрами.
- `+axis:undo` — `turn` (відкат лише в межах поточного ходу).

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Tactical_Breach_Wizards) — загін до 5, провидець-передбачення, undo до кінця ходу, цілі (вікно, 2 ходи), Confidence → вбрання, anxiety dreams, редактор, дата 22.08.2024.
- [Steam](https://store.steampowered.com/app/1043810/Tactical_Breach_Wizards/) — вікна, безкоштовні rewind, некромедик, пес, перки вмінь, Easy/Medium/Hard + змінні.
- [pentadact.com](https://www.pentadact.com/2024-08-22-tactical-breach-wizards-is-out/) — блог розробника (Tom Francis), реліз.
- YouTube: пошук «Tactical Breach Wizards gameplay».

## Непевне
- (?) Ресурс умінь (mana / заряди / кулдауни) і кількість дій на хід — у джерелах не знайшов.
- (?) Чи показують вороги наміри без провидця, і як саме працює передбачення (власне вміння Zan чи постійне превʼю) — Wikipedia лише «seer briefly previews».
- (?) Шкода від зіткнення при відкиданні, укриття і щити ворогів, порядок дій ворогів — з памʼяті.
- (?) Імена й ролі решти загону (окрім Zan і Jen) — не перевірено; «anxiety dreams» як окреме вікно — припущення.
- (?) Пауза/сповільнення/камера — з допису про трейлер; чи це для гравця — не перевірено.
