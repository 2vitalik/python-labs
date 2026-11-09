---
title: Orakyubu
slug: orakyubu
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Mac, Linux, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1654900/Orakyubu/", best: true, note: "безкоштовно; опис: Sokoban на гранях кубів, ~25 пазлів, 6 мов"}
  - {kind: itch, url: "https://peterlavigne.itch.io/orakyubu", note: "грати в браузері (HTML5); лінки на код і сайт автора"}
  - {kind: other, url: "https://github.com/Peter-Lavigne/Orakyubu", note: "відкритий код Unity/C# (GPL-2.0): правила переходу через ребро, рух кубів, undo, рівні в StartingModel.json"}
  - {kind: official, url: "https://peterlavigne.com", note: "сайт автора (Peter Lavigne)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Orakyubu+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [push-object, move-4dir, move-by-input, keyboard-controls, impassable-cells, all-on-targets, carrier-platform, party-switch, undo-unlimited, restart-level, world-map, level-unlock, save-progress, in-game-editor, selection-highlight, hover-highlight, movement-animation, main-menu, pause-menu, settings-window, confirm-dialog, volume-control, language-picker, +cube-net-wrap, +surface-transfer, +camera-relative-input, +camera-orbit, +in-world-tutorial, +click-select-actor]
proposes: ["+effect:cross_edge", "+axis:field=cube-surface", "+feature:camera-orbit", "+feature:invert-camera-axes", "+card:surface-transfer", "+card:camera-relative-input", "+card:in-world-tutorial"]
author: opus
date: 2026-11-09
---

# Orakyubu — Sokoban на поверхні кубів: кола й ящики переходять через ребра на інші грані й на сусідні куби

## Суть
Кожен пазл — один-три куби в 3D-просторі, на кожній грані куба — плоске поле 7×7 зі стінами, ящиками й цілями. Гравець виділяє коло-аватар і штовхає ящики, як у Sokoban, але край грані — не стіна: коло й ящик перекочуються через ребро на сусідню грань або переходять на грань іншого куба. Коли кубів кілька, їх самих можна виділити й зсунути в просторі, змінюючи, які грані стикаються. Близько 25 пазлів; гра безкоштовна, код відкритий.

## Поле і час
- Простір — воксельна сітка кубів: у звичайних рівнях `x, z ∈ [−3, 3]`, `y ∈ [0, 5]` (7×7×6 позицій); у фінальному рівні `x, z ∈ [−2, 2]`, висота не обмежена (з `Model.PositionInbounds`).
- Кожен куб має 6 граней (`Front, Right, Back, Left, Top, Bottom`), кожна грань — поле 7×7 клітин (`units2d: 7`). Шари грані: стіни, цілі, ящики, кола.
- Гравітації нема: коло ходить і по нижній грані куба.
- Покроково: хід = крок кола (з можливим поштовхом ящика) або зсув куба на 1. Перевірка перемоги — після кроку кола.
- Камера вільно обертається навколо сцени й зумиться; напрям стрілок тлумачиться відносно грані, на яку дивиться камера.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Коло (Player2D) | player | грань, позиція 7×7 | рух 4 напрямки по поверхні; штовхає один ящик; на краю грані переходить за правилами A/B/C |
| Ящик (Box2D) | object | грань, позиція | зсувається на 1 від поштовху, з тим самим переходом через ребро; не штовхається в стіну, ящик чи коло |
| Ціль (Goal2D) | zone | грань, позиція | перемога, коли на всіх цілях усіх граней стоять ящики |
| Стіна (Wall2D) | static | грань, позиція | непрохідна для кола й ящика |
| Куб (Box3D) | object | позиція в 3D, 6 граней | виділений куб зсувається на 1 у просторі, якщо там нема іншого куба й позиція в межах; везе все, що на його гранях |
| Грань (Plane2D) | terrain | 7×7 | поверхня, по якій ходять; сусідство граней визначає переходи |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, circle)` → ТО `set_state(circle, selected)`, `clear_state(cube, selected)`.
- КОЛИ `input(click, cube)` → ЯКЩО `count(cube, >, 1)` and `custom: «у клацнутій клітині нема кола»` → ТО `set_state(cube, selected)`, `clear_state(circle, selected)`.
- КОЛИ `input(dir)` → ЯКЩО `state(circle, selected)` → ТО `custom: «напрям перекласти з екранного на напрям грані кола»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «наступна клітина на тій самій грані»` and `free(next_cell)` → ТО `move(circle, dir)`.
- КОЛИ `edge(circle)` → ЯКЩО `occupied(cell_3d_diagonal, cube)` → ТО `custom: «випадок A — внутрішній кут: перейти на грань сусіднього куба, що дивиться назад»`.
- КОЛИ `edge(circle)` → ЯКЩО `occupied(cell_3d_ahead, cube)` → ТО `custom: «випадок B — рівне продовження: та сама грань сусіднього куба»`.
- КОЛИ `edge(circle)` → ЯКЩО `custom: «сусідніх кубів нема»` → ТО `custom: «випадок C — перегин через ребро на суміжну грань того самого куба»`; позиція загортається по модулю 7. Пріоритет A → B → C.
- КОЛИ `input(dir)` → ЯКЩО `occupied(target, wall)` or `occupied(target, circle)` → ТО `block`.
- КОЛИ `contact(circle, box)` → ЯКЩО `free(cell_behind_box)` (з тим самим переходом A/B/C, напрям перекладено на грань ящика) → ТО `push`, `move(circle, dir)`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `state(cube, selected)` and `free(cell_3d_target)` and `custom: «позиція в межах простору»` → ТО `move(cube, dir)` (вгору — від камери, вниз — до камери, вліво/вправо — відносно камери); вміст граней їде разом; інакше `block`.
- КОЛИ `custom: «після кроку кола»` → ЯКЩО `all_on(box, goal)` → ТО `win`, `custom: «рівень позначено пройденим, прогрес у Progress.json»`, `unlock(next_levels)`.
- КОЛИ `counter(completed, =, all_but_final)` → ТО `unlock(final_level)`.
- КОЛИ `level_end` → ЯКЩО `custom: «це фінальний рівень»` → ТО `window(credits-window)`.
- КОЛИ `input(Z)` → ТО `undo(1)` (стек ходів кола й куба); КОЛИ `input(R)` → ТО `restart` (відкат усього стека).
- Перемога: усі цілі під ящиками · Поразки нема · Рахунку нема.

## Керування і ввід
- ЛКМ по колу — виділити коло; ЛКМ по кубу (коли кубів більше одного) — виділити куб.
- WASD / стрілки — рух виділеного кола або зсув виділеного куба; напрям — відносно поточного ракурсу камери.
- Утримання ПКМ або Shift + рух миші — обертати камеру; колесо — зум; курсор біля краю екрана повільно обертає сцену.
- Z — undo, R — рестарт; ті самі кнопки у верхньому лівому куті; Esc — пауза.
- Редактор (Extras → Level Editor): 3 — видалення, 5 — новий куб, 6 — коло, 7 — ящик, 8 — ціль, 9 — стіна; клік по грані — поставити; підняти / опустити / відсунути / видалити куб.

## Вікна, меню, HUD
- `main-menu`: New Game / Continue (якщо є збереження) · Settings · Extras (Level Editor, Credits, Discord) · Exit (у браузерній версії прихований).
- `map-window`: вибір рівня — рівні стоять у просторі колонками, лінії прогресу між ними зʼявляються після проходження попереднього; фінальний рівень — коли пройдено всі.
- `game-screen`: куби рівня в 3D; HUD — кнопки reset/undo вгорі зліва, кнопка меню; виділене коло/куб підсвічене, куб під курсором — hover-матеріал.
- `tutorial-window` (у світі): у перших рівнях на гранях лежать текстові плашки — «клацни коло», «WASD», «ПКМ/Shift — камера», «колесо — зум», «R/Z», «клацни куб».
- `pause-menu` (Esc): Resume · Level Select · Settings · Main Menu.
- `settings-window`: Full Screen, Music, Sound Effects, Look Sensitivity, Invert Left/Right, Invert Up/Down, мова, Reset All Progress; кнопки Save / Cancel / Restore Defaults.
- `confirm-dialog`: «Are you sure you want to reset saved data?».
- `editor-window`: та сама сцена в режимі редагування.
- `credits-window`: після фінального рівня — «Thank you for playing!».

## Фічі поза полем
- `undo` ∞ (стек ходів), `restart-level`, `level-unlock` графом рівнів, `world-map`-вибір рівня, `autosave` прогресу (`Progress.json`).
- `level-editor` (режим editor, рівень «Custom Level»).
- `volume-sliders` (музика, звуки), чутливість камери, інверсія осей камери, повноекранний режим.
- `localization`: EN, FR, ES, zh-CN, JA, PT-BR.
- Рівні: 25 у `StartingModel.json` (24 + Final Level); 1–2 куби, фінальний — 3 куби й 2 кола.

## Варіації й родичі
- Kula World (гравітація по гранях куба), Advent of Code 2022 день 22 (`cube-net-wrap`), Monument Valley (ракурс і поверхні), Sokoban (база), Patrick's Parabox (поле в полі як інша «нестандартна топологія» Sokoban).
- Осі варіацій:
  - **поверхня**: площина (Sokoban) / грані одного куба (розгортка) / кілька кубів, що стикаються (тут) / довільний многогранник;
  - **перехід через ребро**: перегин на суміжну грань / рівне продовження на сусідній куб / внутрішній кут на стіну сусіда — з пріоритетом;
  - **що рухає гравець**: лише аватар / аватар і самі куби (тут) / усю сцену;
  - **інтерпретація стрілок**: відносно грані / відносно камери (тут).

## Цікавинки для курсу
- Розгортка куба: перехід через ребро зі зміною грані й перерахунком координат і напрямку — 🥈 (таблиці сусідства граней, `mod 7`).
- Три випадки переходу (внутрішній кут, рівне продовження, зовнішнє ребро) з пріоритетом — 🥇 (3D-сусідство кубів + 2D-позиції).
- Куб як платформа, що везе свої грані — 📎 (вміст привʼязаний до куба, не до світу).
- Стрілки відносно ракурсу камери — 🥉.
- Undo як стек обʼєктів-ходів з `Apply/Undo` (патерн Command) — 📎.
- Граф розблокування рівнів з лініями прогресу — 📎.

## Мапа на каталог
- Є: `push-object` ↔ ящики; `move-4dir` · `move-by-input` · `keyboard-controls` ↔ WASD; `impassable-cells` ↔ стіни; `all-on-targets` ↔ перемога; `carrier-platform` ↔ куб везе грані; `party-switch` ↔ два кола у фіналі, вибір кліком; `undo-unlimited` · `restart-level` ↔ Z/R; `world-map` · `level-unlock` ↔ вибір рівня з лініями; `save-progress`; `in-game-editor`; `selection-highlight` · `hover-highlight`; `movement-animation`; меню й налаштування — `main-menu`, `pause-menu`, `settings-window`, `confirm-dialog`, `volume-control`, `language-picker`.
- **Нема** → пропозиції карток:
  - `+cube-net-wrap` (уже в корпусі) — перегин через ребро одного куба.
  - `+surface-transfer` «Перехід між поверхнями сусідніх кубів» · entities/move · 🥇 · слоти {cases: inner-corner|flat|outer-edge, priority}.
  - `+camera-relative-input` «Стрілки відносно ракурсу камери» · interface/input · 🥉.
  - `+camera-orbit` «Обертання камери навколо сцени» · interface/render · 🥉.
  - `+in-world-tutorial` «Підказки, намальовані на самому полі» · interface/menus · 🌱.
  - `+click-select-actor` «Вибір активного обʼєкта кліком (коло або куб)» · interface/input · 📎.

## Пропозиції до словників
- `+effect:cross_edge` — обʼєкт переходить через ребро на іншу грань / куб зі зміною напрямку (тут — `custom` у правилах A/B/C).
- `+axis:field=cube-surface` — поле на поверхні кубів (зараз `3d`).
- `+feature:camera-orbit` — вільне обертання камери; `+feature:invert-camera-axes` — інверсія осей камери в налаштуваннях.
- `+card:surface-transfer`, `+card:camera-relative-input`, `+card:in-world-tutorial` — див. вище.
- ⏳-слова, вжиті тут: `input`, `edge`, `free`, `occupied`, `count`, `state`, `move`, `set_state`, `clear_state`, `all_on`, `unlock`, `undo`, `restart`, `window`.

## Джерела
- ⭐ [Steam: Orakyubu](https://store.steampowered.com/app/1654900/Orakyubu/) — опис, «around 25 puzzles», реліз 15.08.2021, Peter Lavigne, 6 мов, безкоштовно.
- [itch: Orakyubu](https://peterlavigne.itch.io/orakyubu) — браузерна версія, лінки на код і сайт; коментар про незручність стрілок при деяких ракурсах.
- [GitHub: Peter-Lavigne/Orakyubu](https://github.com/Peter-Lavigne/Orakyubu) — `MovePlayer2D.cs` (випадки A/B/C, поштовх ящика, перевірка перемоги), `MoveBox3D.cs` і `Model.cs` (зсув куба, межі простору, undo/reset, збереження), `Controller.cs` (виділення, порядок рівнів), `KeyboardInput.cs` / `MouseInput.cs` (клавіші, камера), `english.json` (тексти меню й туторіалів), `StartingModel.json` (25 рівнів).

## Непевне
- (?) Як саме працює зсув куба, коли камера дивиться згори чи знизу (`facingFace = Top/Bottom`) — чи можна тоді рухати куб по вертикалі; з коду випливає, що можна, але не перевірено в грі.
- (?) Чи кнопка Level Editor видима в релізній версії, чи лише в збірці розробника (метод `OnClickLevelEditor` є).
- (?) Що відбувається з предметами на гранях, які стикаються з іншим кубом впритул, — код цього не перевіряє.
