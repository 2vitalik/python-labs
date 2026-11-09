---
title: Slider
slug: slider
aka: [Slider (boomo), Slider jam]
family: push-slide
also: [thinky]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2024
platforms: [Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://randomerz.itch.io/slider", best: true, note: "сторінка гри: світ — пазл «8», 9 регіонів зі своїми поворотами (обертання, 3D-сітки, час, бій), безкоштовно"}
  - {kind: steam, url: "https://store.steampowered.com/app/1916890/Slider/", note: "Steam: «unique twist on the 8-puzzle», якорі, вагонетки, буї, світло; 1.0 — 24.07.2024"}
  - {kind: other, url: "https://github.com/randomerz/Slider", note: "відкритий код (Unity/C#): SGrid, UIArtifact, сітки 9 регіонів"}
  - {kind: other, url: "https://randomerz.itch.io/slider-jam", note: "оригінал GMTK Game Jam 2021"}
  - {kind: other, url: "https://steamcommunity.com/app/1916890/reviews/?browsefilter=toprated&l=english", note: "відгуки: квести за плитки, ковзання до упору, обертання по 4, два шари, минуле, бій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Slider+boomo+8+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [carrier-platform, completion-detection, inertia-slide, multi-cell-size, gravity-fall, teleport, beam-tracing, mirror-reflect, item-pickup, inventory-items, cell-click, drag-drop-piece, selection-highlight, legal-move-highlight, keyboard-controls, controls-remap, main-menu, pause-menu, settings-window, map-window, save-multi-slot, achievements-window, language-picker, +sliding-tile-board, +world-is-sliding-puzzle, +collect-tiles-by-quest, +anchor-lock-tile, +rotate-block-2x2, +layered-tile-grid, +mirrored-twin-grids, +slide-ends-turn, +move-queue, +lit-from-source]
proposes: ["+window:artifact-grid", "+feature:auto-move", "+axis:control", "+card:world-is-sliding-puzzle", "+card:collect-tiles-by-quest", "+card:anchor-lock-tile", "+card:rotate-block-2x2", "+card:layered-tile-grid", "+card:mirrored-twin-grids", "+card:move-queue"]
author: opus
date: 2026-11-09
---

# Slider — пригода, де весь світ — пазл «8»: ходиш по шматках мапи і переставляєш їх Артефактом

## Суть
Гравець ходить світом згори, а сам світ складено з квадратних шматків-«слайдерів» у сітці 3×3 з дірками; Артефакт показує цю сітку кнопками, і зсув кнопки фізично пересуває шматок мапи разом з усім, що на ньому стоїть. Нові слайдери видають мешканці за квести, які вимагають певного сусідства шматків (корабель біля скарбу, газель біля оазису). Кожен із 9 регіонів змінює правило зсуву: ковзання до упору, обертання блоками 2×2, подвійні плитки, два шари, минуле і теперішнє, покроковий бій. Мета регіону — скласти цільовий порядок шматків. `klass: hybrid` — аватар (ходьба, квести) + курсор (Артефакт).

## Поле і час
- Два рівні поля: **сітка Артефакта** (зазвичай 3×3; Military — 16 плиток; Mountain — 2×4 як два шари; MagiTech — 6×3 як дві сітки 3×3) і **світ** — кожна клітина сітки є шматком мапи, по якому вільно ходить персонаж.
- Порожні клітини сітки — «дірки» (неактивні слайдери позначені `#`); стан сітки записується рядком (`"563_2#8_174"`), цілі регіонів і квестів — шаблони над цим рядком.
- Час реальний: ходьба й анімація зсуву (≈0,5 с у фіналах); ходи Артефакта стають у чергу до 3, хід, що перетинається з активним, чекає. Military — покроковий: кожен зсув закінчує хід гравця.
- Регіони (сцени в коді): Village, Caves, Ocean, Jungle, Desert, Factory, Military, Mountain, MagiTech.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | позиція у світі | ходить шматками мапи; їде разом зі шматком, на якому стоїть |
| Слайдер (шматок мапи) | tile | islandId, x, y, active | зсувається в порожню клітину; несе все, що на ньому |
| Дірка (порожня клітина) | zone | — | куди можна зсунути слайдер |
| Слайдер-предмет | pickup | «Slider N» | підбирається у світі → плитка зʼявляється в сітці |
| Кнопка Артефакта | mark | complete / ні | дзеркало слайдера в UI; підсвічує, чи стоїть на цільовому місці |
| Мешканець (NPC) | neutral | квест-умова | дає слайдер або предмет, коли виконано умову сусідства |
| Якір | pickup | кинуто / в руці | кинутий на слайдер — фіксує його; у Mountain / MagiTech — спецефекти |
| Подвійний слайдер (Jungle) | tile | 2 клітини | рухається парою; горизонтальні ходи несиметричні |
| Міраж-слайдер (Desert) | tile | копія плитки N | відображення справжнього шматка |
| Джерело світла (Caves) | static | — | освітлює шматки; ціль — усі плитки освітлені |
| Портал часу (MagiTech) | terrain | минуле / теперішнє | переносить гравця між двома сітками |
| Вагонетка (Mountain, Jungle) | object | порожня / кристал / лава | везе вантаж рейками через шматки |
| Загін (Military) | ally | тип | ходить після кожного зсуву; бʼється з прибульцями |
| Прибулець (Military) | enemy | хвилі | атакує загони; поразка → «симуляція» з початку |
| Предмети (чоботи, вибухівка, скриня, самоцвіт, рейка…) | pickup | — | квестові ключі; відкривають шляхи й нові слайдери |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, tile)` → ЯКЩО `state(tile, active)` і `not state(tile, anchored)` → ТО `custom: «підсвітити дірки в 4 напрямках до першої активної плитки»`.
- КОЛИ `input(target, hole)` → ЯКЩО `free(hole)` і `custom: «дірка на одній лінії без плиток між ними»` і `custom: «черга < 3»` → ТО `move(tile, to_hole)`.
- КОЛИ `after(move)` → ЯКЩО `occupied(tile, player)` → ТО `carry(tile, player)` (гравець їде зі шматком).
- КОЛИ `picked(player, slider_item)` → ТО `spawn_at(tile, hole)` (новий слайдер у сітці Артефакта).
- КОЛИ `pattern(grid_string ∋ "41")` → ТО `reveal(treasure)` (Ocean: корабель біля скарбу); аналогічно інші квести-сусідства.
- КОЛИ `pattern(grid_string == target)` → ЯКЩО `custom: «фінальний пазл регіону запущено»` → ТО `win` (регіон завершено), `unlock(next_area)`.
- КОЛИ `input(drop_anchor)` → ТО `set_state(tile, anchored)`; КОЛИ `input(select, tile)` → ЯКЩО `state(tile, anchored)` → ТО `block`.
- Desert: КОЛИ `input(select, tile)`+`input(dir)` → ТО `slide(tile, dir)` — до найдальшої дірки в лінії, плитки лінії зсуваються разом.
- Ocean: КОЛИ `input(rotate_arrow, block2x2)` → ТО `rotate(block2x2, ±90)`; плитки з якорем лишаються на місці.
- Jungle: КОЛИ `input(select, double_tile)` → ЯКЩО `free(both_target_cells)` → ТО `move(double_tile, dir)` парою.
- Mountain: КОЛИ `input(drop_anchor)` → ЯКЩО `custom: «плитка у верхньому шарі, клітина під нею в нижньому шарі порожня»` → ТО `fall(tile)` (переходить у нижній шар).
- MagiTech: КОЛИ `after(move)` → ЯКЩО `not state(world, desync)` → ТО `custom: «двійник у минулому повторює хід (x+3 mod 6)»`.
- MagiTech: КОЛИ `input(drop_anchor)` → ТО `set_state(world, desync)`; підняття якоря → `clear_state(world, desync)`, `custom: «минуле вирівнюється з теперішнім»`.
- Caves: КОЛИ `counter(lit_tiles, ==, all)` → ЯКЩО `custom: «фінальний пазл запущено»` → ТО `win` (регіон).
- Military: КОЛИ `after(move)` → ТО `end_turn`, `custom: «загони й прибульці ходять, бій»`; КОЛИ `custom: «загони програли»` → ТО `restart` (симуляція), `counter(military_attempts, +1)`.
- Поразка: у звичайних регіонах нема; у Military — перезапуск симуляції. · Перемога: зібрати всі слайдери й скласти ціль кожного регіону. · Рахунку нема (досягнення за швидкість і «мінімум якорів»).

## Керування і ввід
- Ходьба персонажем (клавіатура/геймпад) + взаємодія з NPC і предметами.
- Артефакт: клік по плитці → клік по підсвіченій дірці, або перетягування (відпустив не над плиткою — скасовано); `+feature:auto-move` — якщо дірка одна, плитка їде одразу.
- Налаштування «keyboard only» — керування Артефактом без миші; курсор стрибає за переміщеною кнопкою; перепризначення клавіш (тека `Rebinding`).
- Якір — кинути/підняти дією персонажа.

## Вікна, меню, HUD
- `splash-screen` / вступна катсцена (`IntroCutscene`).
- `main-menu`: Грати → `save-slots` (кілька профілів), налаштування, титри.
- `game-screen`: світ згори; HUD — підказки дій, повідомлення про предмет.
- `custom-window` **Артефакт** (`+window:artifact-grid`): сітка кнопок-слайдерів з підсвіткою ходів і завершених позицій; вкладки (тека `Tabs`) — зокрема `map-window` регіонів з позначками завершення; `inventory-window`-вкладка зібраних предметів (?).
- `dialogue-window` — розмови з мешканцями.
- `pause-menu`, `settings-window` (доступність, кольори для дальтоніків, мова, керування), `credits-window`, `achievements-window`.
- Переходи: регіон → (Артефакт відкрито поверх гри) → регіон; сцена регіону → сусідній регіон через вихід мапи.

## Фічі поза полем
- `world-map`-подібна прогресія: 9 регіонів відкриваються квестами; у кожному — збір слайдерів і фінальний пазл.
- `save-slots` (кілька), `autosave` після подій (`SaveSystem`).
- `achievements`: швидкість, «мінімум якорів» в Ocean, усі рецепти «книги форм», вбити птаха в Desert тощо.
- `colorblind-palette`, `remap-controls`, `gamepad-support`, `localization` (EN, KO, zh-CN).
- Безкоштовно (itch — «name your own price»); 10+ годин контенту.

## Варіації й родичі
- [sliding-tile-permutation](sliding-tile-permutation.md) — класичні пʼятнашки й родичі; тут ті самі ходи, але плитки — шматки світу з персонажем.
- Jam-версія (GMTK 2021, 16-те місце) → розробка клубом VGDev Georgia Tech → Steam 2022 (ранні версії) → 1.0 у 2024.
- Родичі: Loco Motion (maze-arcade) — зсув шматків колії під поїздом; [klotski](klotski.md) — блоки різних розмірів (як подвійні слайдери Jungle).
- Осі варіацій (усі в одній грі):
  - **хід плитки**: у дірку по лінії (Village) / до упору лінією (Desert) / обертання 2×2 (Ocean) / пара-плитка (Jungle) / падіння між шарами (Mountain) / дзеркальна сітка в минулому (MagiTech);
  - **що несе плитка**: картинку (пʼятнашки) / шматок світу з гравцем і NPC (Slider);
  - **ціль**: порядок плиток / сусідство окремих пар (квести) / стан, обчислений на сітці (світло в Caves);
  - **час**: без ходів / зсув = хід, після якого ходять загони (Military).

## Цікавинки для курсу
- Дворівневе поле: сітка 3×3 шматків + світ, де позиція гравця перераховується при зсуві його шматка — 🥈.
- Стан сітки як рядок і цілі як шаблони з `.`/`*` (`".4._895_.3."`), квести «пара сусідів» — 📎 (regex над станом).
- Регіональні правила зсуву за одним інтерфейсом `GetMoveOptions` (лінія / до упору / пара / обертання) — 🥉 за пакет, кожне 🌱–📎.
- Дві звʼязані сітки (минуле/теперішнє) з «розсинхроном» якорем і відновленням — 🥇.
- Черга ходів з очікуванням перетину анімацій — 📎.
- Покроковий бій, де «хід» — це зсув шматка мапи під загонами — 🥈.

## Мапа на каталог
- Є: `carrier-platform` ↔ гравець їде зі шматком; `completion-detection` ↔ цільовий рядок; `inertia-slide` ↔ Desert; `multi-cell-size` ↔ подвійні слайдери Jungle; `gravity-fall` ↔ падіння між шарами Mountain; `teleport` ↔ портали MagiTech; `beam-tracing` + `mirror-reflect` ↔ лазер через регіон (з відгуку); `item-pickup` + `inventory-items`; `cell-click` + `drag-drop-piece` + `selection-highlight` + `legal-move-highlight` ↔ Артефакт; `keyboard-controls` + `controls-remap`; `main-menu`, `pause-menu`, `settings-window`, `map-window`, `save-multi-slot`, `achievements-window`, `language-picker`.
- **Нема** → пропозиції карток:
  - `+sliding-tile-board` (уже в корпусі) — зсув плитки в дірку.
  - `+world-is-sliding-puzzle` «Світ із шматків-плиток: ходиш по них і переставляєш» · world/levels · 🥈.
  - `+collect-tiles-by-quest` «Нові плитки сітки — нагорода за квести» · levels/progression · 📎.
  - `+anchor-lock-tile` «Якір фіксує плитку від зсуву» · entities/state · 🌱.
  - `+rotate-block-2x2` «Обертання блоку 2×2 плиток» · entities/move · 📎.
  - `+layered-tile-grid` «Сітка з шарів, плитка падає в нижній» · entities/move · 🥉.
  - `+mirrored-twin-grids` «Дві сітки дзеркалять ходи, якір розсинхронізує» · entities/state · 🥇.
  - `+slide-ends-turn` «Зсув плитки = хід, потім ходять юніти» · game-logic/opponent · 🥉.
  - `+move-queue` «Черга до N ходів під час анімації» · interface/input · 📎.
  - `+lit-from-source` (уже в корпусі) — Caves: освітлені плитки.

## Пропозиції до словників
- `+window:artifact-grid` — вікно-пульт поверх гри, що показує й переставляє сітку шматків світу.
- `+feature:auto-move` — один дозволений хід виконується без вибору цілі.
- `+axis:control` — тут одночасно `direct` (персонаж) і `click-cell`/`drag-piece` (Артефакт).
- `+card:world-is-sliding-puzzle`, `+card:collect-tiles-by-quest`, `+card:anchor-lock-tile`, `+card:rotate-block-2x2`, `+card:layered-tile-grid`, `+card:mirrored-twin-grids`, `+card:move-queue`.

## Джерела
- ⭐ [itch: Slider](https://randomerz.itch.io/slider) — суть «slide pieces of the world», 9 регіонів із поворотами (rotating environments, tactical combat, 3D grids, time travel), keyboard only, безкоштовно.
- [Steam: Slider](https://store.steampowered.com/app/1916890/Slider/) — «unique twist on the 8-puzzle», якорі/вагонетки/буї/світло, 1.0 24.07.2024, boomo, мови, 96 % з 654 відгуків.
- [GitHub: randomerz/Slider](https://github.com/randomerz/Slider) — README (GMTK 2021, VGDev Georgia Tech, Unity), `SGrid.cs` (рядок стану, `#`, цілі), `UIArtifact.cs` (вибір, drag, черга 3, якір), `DesertArtifact`, `OceanArtifact`, `JungleArtifact`, сітки Mountain 2×4, MagiTech 6×3, Military, Caves (освітлення).
- [itch: Slider jam](https://randomerz.itch.io/slider-jam) — оригінальна jam-версія.
- [Steam-відгуки](https://steamcommunity.com/app/1916890/reviews/?browsefilter=toprated&l=english) — квести за слайдери, ковзання до упору, обертання по 4, два шари, привид із минулого, бій, вагонетка, лазер, кілька слотів збережень.
- YouTube: пошук «Slider boomo 8 puzzle gameplay».

## Непевне
- (?) Чи можна зсунути шматок, на якому стоїть гравець, у всіх регіонах — код «чіпляє» гравця до плитки, але обмежень у `SGrid.CanMove` не бачив.
- (?) Village — базові правила 3×3 «у дірку»; окремого файла правил не читав, висновок з базового `UIArtifact`.
- (?) Розмір сітки Military (16 слайдерів → 4×4?) і правила бою (типи загонів) — лише в непрочитаних класах.
- (?) Factory: минуле/теперішнє для гравця й конвеєри — є в коді частково; правила зсуву плиток Factory не перевірено.
- (?) Лазер і «книга форм» — з відгуків; регіон, де вони, не перевірено.
- (?) `random: runtime` — лише перемішування сітки в Desert (`DesertArtifactRandomizer`) і кубики казино; решта гри детермінована.
