---
title: Tacticsweeper
slug: tacticsweeper
aka: [Tacticsweeper+]
family: hidden-deduction
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: state
year: 2024
platforms: [web (HTML5), Windows]
links:
  - {kind: itch, url: "https://moocowsgomoo.itch.io/tacticsweeper", best: true, note: "грати в браузері; правила зондів, «+»-клітин і споруд, перелік мін і спорядження; коментарі з тактикою"}
  - {kind: other, url: "https://moocowsgomoo.itch.io/tacticsweeper/devlog/743743/v11-endless-mode-new-mines", note: "v1.1: Endless після перемоги, Dual Mine / Battery / Mirror Mine, фінальний бос"}
  - {kind: other, url: "https://moocowsgomoo.itch.io/tacticsweeper/devlog/736603/v101", note: "v1.01: Terrain Map відкриває 4 міни, програш при втраті останнього зонда"}
  - {kind: other, url: "https://moocowsgomoo.itch.io/tacticsweeper/devlog/751388/v112-dark-mine-rework", note: "v1.12: усі Dark Mine рівня — в одному рядку чи стовпці"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tacticsweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, neighbor-count-clue, flood-reveal, inventory-items, shop-between-levels, run-relics, sequential-levels, completion-detection, threat-range, keep-playing-after-win, save-progress, settings-window, game-screen, end-screen, codex-window, +probe-ammo-lives, +structure-plus-clue, +disable-by-reveal, +ranged-hidden-turret, +mirror-mine-fake-number, +line-confined-mines, +flag-icon-by-kind]
proposes: ["+trigger:probe_landed", "+effect:disable", "+effect:lose_probe", "+cond:structure_active", "+ui:infocenter-panel", "+ui:tool-buttons", "+feature:mode-endless-after-win", "+card:probe-ammo-lives", "+card:structure-plus-clue", "+card:disable-by-reveal", "+card:ranged-hidden-turret", "+card:mirror-mine-fake-number", "+card:line-confined-mines", "+card:flag-icon-by-kind"]
author: opus
date: 2026-11-09
---

# Tacticsweeper — сапер-роглайк: стріляєш зондами, які можна втратити, а приховані споруди бʼють по зондах здалеку

## Суть
Кожне відкриття клітини — постріл зондом, а зонди скінченні: міна чи атака споруди «на льоту» забирає зонд, без зондів — кінець забігу. Крім звичайних мін є **споруди** (турелі, proximity-міни, кріо-будівлі), позначені «+» на сусідніх клітинах; відкрити споруду — вимкнути її разом з усіма її ефектами. Рівень пройдено, коли відкрито все безпечне й вимкнено всі споруди; між рівнями — новий предмет або апгрейд.

## Поле і час
- Квадратна сітка, 8-сусідство; рівні йдуть послідовно, у кожній зоні додаються нові небезпеки; фінальний бос — на рівні 25 (v1.1: «пройшов 25 — бачив усе»).
- Покроково: хід = постріл зондом або застосування інструмента; споруди реагують під час падіння зонда.
- Шари: приховане поле → числа (міни) і «+» (споруди) → прапорці гравця → підсвітка небезпек інструментами.
- Endless після перемоги в забігу; гравці доходять до рівнів ~46–48.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Зонд | resource | запас N (?) | витрачається, якщо впав на міну або збитий спорудою |
| Закрита клітина | static | вміст | постріл зондом відкриває |
| Число | mark | n = міни серед 8 сусідів | класична підказка |
| «+»-клітина | mark | — | поруч (8 сусідів) активна споруда; гасне з вимкненням споруди |
| Міна | hazard | — | постріл у неї = втрата зонда |
| Proximity Mine | hazard | радіус (?) | «бікає» й атакує зонд поблизу (?) |
| Laser Turret | hazard | лінія (?) | дальня атака по лінії (?) |
| Ultimine | hazard | позначки небезпеки | найнебезпечніша; позначки зникають, щойно почнеш Disarm |
| Mirror Mine | hazard | пара | спотворює числа — «не сходиться» = ознака дзеркальної |
| Dark Mine | hazard | — | діє на все поле; з v1.12 усі в одному рядку/стовпці |
| Cryo Mine + Cryo Building | hazard + switch | — | вимикає лише відкриття будівлі, не самої міни |
| Dual Mine · Battery | hazard | — (?) | нові з v1.1, пізні рівні |
| Фальшива споруда (trap mine) | hazard | — | «+» лише ортогонально, без діагоналей |
| Фінальний бос | boss | — (?) | окрема панель-підказка (v1.1) |
| Інструменти: Scanner, Terrain Map, Stealth Kit, Analyzer, Disarm, Recycling, Armor Kit, Salvage, Hazard View | pickup | заряди (?) | кнопки праворуч; Terrain Map відкриває 4 випадкові міни; Armor Kit — зонд переживає приземлення на міну |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, c)` → ЯКЩО `not occupied(c, mine)` → ТО `reveal(c)` з числом `adjacent_count(c, mine, =, n)` і «+», якщо `custom: «серед 8 сусідів є активна споруда»`.
- КОЛИ `after(reveal(c))` → ЯКЩО `custom: «0 мін довкола»` → ТО `reveal(neighbors8)` (?).
- КОЛИ `input(fire, c)` → ЯКЩО `occupied(c, mine)` and `not has(player, armor_kit)` → ТО `counter(probes, -1)`.
- КОЛИ `input(fire, c)` → ЯКЩО `occupied(c, mine)` and `has(player, armor_kit)` → ТО `custom: «зонд переживає приземлення»`, `take(player, armor_kit)`.
- КОЛИ `input(fire, c)` → ЯКЩО `custom: «зонд у зоні атаки активної споруди»` → ТО `counter(probes, -1)` — збитий «на льоту».
- КОЛИ `input(fire, structure)` → ТО `custom: «вимкнути споруду: її атаки й «+»-клітини зникають»`.
- КОЛИ `input(fire, cryo_building)` → ТО `custom: «вимкнути»`; КОЛИ `input(fire, cryo_mine)` → ТО `custom: «не вимикає»`.
- КОЛИ `input(use, terrain_map)` → ТО `reveal(4 random mines)` (v1.01).
- КОЛИ `input(use, disarm, ultimine)` → ТО `custom: «знешкодити»`, `hide(hazard_markers)`; інший шлях — приземлитись (з Armor Kit) і застосувати Recycling.
- КОЛИ `counter(probes, <=, 0)` → ТО `lose` (з v1.01 — навіть якщо це був останній безпечний тайл).
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «усі безпечні відкрито й усі споруди вимкнено»` → ТО `next_level`, `choose(upgrade|item)`.
- КОЛИ `died(final_boss)` → ТО `win`, `custom: «запропонувати Endless»`.
- КОЛИ `input(flag, c)` → ТО `mark(c, flag_icon)` — лише нагадування, на правила не впливає.
- Перший постріл має невразливість (за порадою гравця) (?).
- Перемога: пройти фінальний бос (рівень 25 (?)). · Поразка: скінчились зонди. · Рахунок: досягнутий рівень (Endless).

## Керування і ввід
- Лише миша: ЛКМ — постріл зондом; ПКМ — прапорець; коліщатко — змінити іконку прапорця (вид міни/споруди); клік по міні в інфоцентрі — обрати її іконкою (v1.11).
- Кнопки праворуч — вибрати/активувати інструмент. ESC закриває налаштування.
- Перепризначення немає; на мобільному працює, але кнопки дрібні.

## Вікна, меню, HUD
- `game-screen`: поле; праворуч — кнопки інструментів; угорі праворуч — інфоцентр (опис мін і споруд рівня → `codex-window`-подібна панель); лічильник зондів (?).
- `shop-window` / `upgrade-window` між рівнями: вибір нового предмета чи апгрейда («entering level X»).
- `settings-window` (ESC закриває), fullscreen у завантажуваній версії.
- `main-menu` з Continue (?) — продовження стартує поточний рівень з початку.
- `end-screen`: поразка / перемога з переходом в Endless.

## Фічі поза полем
- Забіг-роглайк: `levels-sequential`, нові небезпеки за зонами, предмет після кожного рівня, `run-relics`-подібні апгрейди.
- `mode-endless` — після перемоги (v1.1).
- `autosave` / `continue` — сейв зберігає вибір магазину (v1.01).
- Hazard View, «advanced radar» — інструменти підсвітки небезпек (radar: міни глушать ортогональних сусідів (?)).

## Варіації й родичі
- Сапер-роглайк з предметами: [demoncrawl](demoncrawl.md); монстри замість мін: [mamono-sweeper](mamono-sweeper.md), [cavern-sweeper](cavern-sweeper.md), [dragonsweeper](dragonsweeper.md).
- Спотворені підказки (Mirror Mine) — як у [14-minesweeper-variants](14-minesweeper-variants.md).
- **Осі варіацій**: «життя» = HP / зонди-патрони; небезпека = статична міна / споруда з дальньою атакою; знешкодження = прапорець / відкриття споруди / інструмент.

## Цікавинки для курсу
- Зонди як патрони-життя (відкриття коштує ресурс лише при помилці) — 🌱.
- Дві мови підказок: числа для мін + «+» для споруд — 📎.
- Споруда з дальньою атакою, що збиває зонд на шляху; вимкнення відкриттям — 🥉.
- Mirror Mine: генерація навмисно неконсистентних чисел і їхня дедукція — 🥈.
- Обмеження розстановки (усі Dark Mine в одному рядку/стовпці) як підказка — 📎.
- Магазин/вибір предмета між рівнями з ресейвом без перекидання вибору — 📎.

## Мапа на каталог
- Є: `cell-click` · `neighbor-count-clue` · `flood-reveal` (?) · `inventory-items` ↔ інструменти · `shop-between-levels` + `run-relics` ↔ предмет після рівня · `sequential-levels` · `completion-detection` · `threat-range` ↔ Hazard View · `keep-playing-after-win` ↔ Endless · `save-progress` · `codex-window` ↔ інфоцентр.
- **Нема** → пропозиції карток:
  - `+probe-ammo-lives` «Відкриття — постріл зі скінченного запасу» · entities/state · 🌱.
  - `+structure-plus-clue` «Друга підказка: поруч споруда» · game-logic/constraints · 📎.
  - `+disable-by-reveal` «Відкрив споруду — вимкнув її ефекти» · entities/interact · 🌱.
  - `+ranged-hidden-turret` «Прихована турель бʼє по відкриттях у радіусі» · entities/combat · 🥉.
  - `+mirror-mine-fake-number` «Міна, що спотворює числа» · game-logic/constraints · 🥈.
  - `+line-confined-mines` «Міни виду лише в одному рядку/стовпці» · levels/generation · 📎.
  - `+flag-icon-by-kind` «Прапорець з іконкою виду» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:probe_landed(c)` — зонд приземлився (момент, коли споруди атакують).
- `+effect:disable(structure)` — вимкнути сутність разом з її ефектами (не `disappear`: лишається на полі).
- `+effect:lose_probe` — витрата одиниці «життя-патрона».
- `+cond:structure_active(s)` — споруда ще працює.
- `+ui:infocenter-panel` — панель опису сутностей рівня з кліком-вибором.
- `+ui:tool-buttons` — стовпчик кнопок інструментів.
- `+feature:mode-endless-after-win` — Endless як продовження виграного забігу.

## Джерела
- ⭐ [itch.io: Tacticsweeper](https://moocowsgomoo.itch.io/tacticsweeper) — правила зондів, «+», споруд; список мін і спорядження; коментарі гравців.
- [v1.1](https://moocowsgomoo.itch.io/tacticsweeper/devlog/743743/v11-endless-mode-new-mines) — Endless, нові міни, бос.
- [v1.01](https://moocowsgomoo.itch.io/tacticsweeper/devlog/736603/v101) — Terrain Map, програш на останньому зонді.
- [v1.12](https://moocowsgomoo.itch.io/tacticsweeper/devlog/751388/v112-dark-mine-rework) — Dark Mine в одному рядку/стовпці.

## Непевне
- (?) Механіка Proximity Mine, Laser Turret, Dual Mine, Battery, Dark Mine (вплив на все поле — як саме) — у відкритих джерелах не описано.
- (?) Battery — і міна (v1.1), і предмет (перелік спорядження): можливо, дві різні речі.
- (?) Стартова кількість зондів; чи поповнюються між рівнями (Salvage? Recycling?).
- (?) Ефекти Scanner, Stealth Kit, Analyzer, Salvage, Hazard View — лише натяки з коментарів.
- (?) Рік: девлог v1.01 — 23.05.2024; дата першого релізу не вказана.
- (?) Каскад нулів не підтверджено.
