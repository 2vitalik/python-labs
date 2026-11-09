---
title: Prickle (Sunbird Studio)
slug: prickle
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC, macOS, Linux, web, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2759760/", best: true, note: "опис: їжачата прилипають до DadHog і одне до одного, прикл-поліоміно, вузькі проходи в живоплоті, 4 сезони"}
  - {kind: itch, url: "https://sunbirdstudio.itch.io/prickle", note: "повна версія в браузері й на ПК; 48 рівнів, 4 сезони, доступність"}
  - {kind: itch, url: "https://sunbirdstudio.itch.io/prickle-jam", note: "джем-версія Ludum Dare 54: керування стрілки/WASD, поворот Q/E або Z/X, R — рестарт"}
  - {kind: other, url: "https://ldjam.com/events/ludum-dare/54/prickle", note: "сторінка джему LD54 (тема «Limited Space»)"}
  - {kind: other, url: "https://sunbirdstudio.itch.io/prickle-jam/devlog/845342/steam-release-postmortem", note: "постмортем: злипання при дотику, рух і поворот, що додала повна версія"}
  - {kind: other, url: "https://www.pocketgamer.com/prickle/out-now/", note: "мобільний реліз 2025: 48 рівнів, забагато їжачат — застрягнеш"}
  - {kind: other, url: "https://therefinedgeek.com.au/index.php/2024/12/20/prickle-schnuffin-hoglets/", note: "рецензія: undo, рестарт, липкі перешкоди, що не є їжачатами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=prickle+sunbird+studio+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, stick-together, impassable-cells, collect-all, reach-exit, undo-redo, restart-level, sequential-levels, idle-animation, +pivot-rotate, +growing-polyomino-avatar]
proposes: ["+effect:move_group", "+card:growing-polyomino-avatar", "+card:pivot-rotate"]
author: opus
date: 2026-11-09
---

# Prickle — збери їжачат, що намертво прилипають до тата, і протягни цю фігуру-поліоміно крізь живопліт додому

## Суть
Сокобан-подібний пазл Sunbird Studio: тато-їжак DadHog збирає розкиданих їжачат, і кожне, торкнувшись, прилипає до нього чи до інших — разом вони утворюють «прикл», фігуру на зразок тетраміно. Прикл рухається й повертається як одне тверде тіло, і що більший він, то важче протиснути його крізь вузькі проходи в живоплоті. Головне питання кожного рівня — **порядок збирання**: забагато їжачат зарано — і фігура застрягне.

## Поле і час
- Квадратна сітка з живоплоту й проходів; рівні — одноекранні, вид згори.
- Покроково: хід = зсув прикла на 1 клітину або поворот; без вводу світ стоїть (засинання DadHog — лише анімація (?)).
- 48 рівнів у 4 сезонах, кожен сезон додає свої механіки (Steam: «over 40 levels across 4 seasons»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| DadHog | player | — | рух 4 напрямки, поворот; веде весь прикл |
| Їжачок (hoglet) | object | вільний / у приклі | лежить на полі; торкнувся прикла — прилипає назавжди |
| Прикл | object | форма-поліоміно з DadHog і зібраних | рухається й повертається цілим; блокується, якщо будь-яка клітина впирається |
| Живопліт | static | — | непрохідний; між кущами вузькі проходи |
| Дім (вихід) | static | — | ціль: прикл із усіма їжачатами |
| Липка перешкода | object | — | теж прилипає до прикла, хоч і не їжачок (?) |
| Сезонні елементи | — | — | у кожному сезоні свої (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(усі клітини, куди зсунеться прикл)` → ТО `move(prickle, dir)`; інакше `block`.
- КОЛИ `adjacent(prickle, hoglet)` → ТО `attach(hoglet, prickle)` — `custom: «назавжди, відчепити не можна»`.
- КОЛИ `input(turn_left|turn_right)` → ЯКЩО `custom: «клітини поверненої фігури вільні»` → ТО `rotate(prickle, ±90)` (центр повороту — DadHog (?)); інакше `block`.
- КОЛИ `contact(prickle, hedge)` → ТО `block`.
- КОЛИ `adjacent(prickle, sticky_obstacle)` → ТО `attach(sticky_obstacle, prickle)` (?).
- КОЛИ `reach(prickle, home)` → ЯКЩО `count(free_hoglet, ==, 0)` → ТО `win`, `next_level`.
- КОЛИ `idle(n)` → ТО `animate(dadhog_dozes)`.
- КОЛИ `input(undo)` → ТО `undo(1)` (повна версія) · КОЛИ `input(r)` → ТО `restart`.
- Перемога: усі їжачата в приклі, прикл удома. · Поразка: формально нема; застряглий прикл → undo або рестарт. · Рахунок: нема.

## Керування і ввід
- Джем-версія: стрілки / WASD — рух, Q/E або Z/X — поворот, R — рестарт.
- Повна версія: клавіатура, миша й тач; додано undo і систему підказок.

## Вікна, меню, HUD
- `main-menu` — меню повної версії (джем-версія його не мала).
- `level-select` / `world-map` — рівні за сезонами (?).
- `game-screen` — рівень, DadHog, їжачата, живопліт, дім.
- `dialogue-window` — катсцени між сезонами (тупіт їжачат на початку нового набору рівнів).
- `hints-window` — підказки (повна версія; вигляд не зʼясовано).
- `settings-window` — доступність: дальтонізм, висока контрастність, темний режим; 15 мов.

## Фічі поза полем
- `levels-sequential` у 4 сезонах; `undo`, `restart-level`, `hint`.
- `colorblind-palette`, `high-contrast`, `theme-select` (темний режим), `localization` (15 мов).
- Порти: Steam (Windows/macOS/Linux, Steam Deck), itch (HTML5), iOS, Android (2025).

## Варіації й родичі
- Prickle — джем-версія Ludum Dare 54 (2023, тема «Limited Space», 12 рівнів) → повна версія Steam 22.11.2024 → мобільна 2025.
- Осі варіацій:
  - **як росте аватар**: не росте (`sokoban`) / довшає хвостом (`thinky/snakebird`) / прилипання в довільну поліоміно-форму (Prickle) / зʼєднання за валентністю (`thinky/sokobond`);
  - **поворот**: нема / навколо півота (Prickle, Sokobond);
  - **що прилипає**: лише ціль (їжачата) / також перешкоди.
- Родичі: `thinky/sokobond`, `thinky/snakebird`, `sokoban`, `board-digital/blokus` (поліоміно в тісному просторі).

## Цікавинки для курсу
- Аватар-поліоміно: множина клітин зі зсувом і перевіркою колізії кожної клітини — 📎.
- Прилипання при дотику: обхід сусідів після ходу і злиття груп — 🥉.
- Поворот поліоміно на 90° навколо півота з перевіркою вільних клітин — 🥉.
- Перевірка «усі зібрані + фігура на виході» як умова перемоги — 🌱.
- Розвʼязувач BFS по стану (позиція, орієнтація, множина зібраних) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки/WASD; `stick-together` ↔ їжачата прилипають і рухаються разом; `impassable-cells` ↔ живопліт; `collect-all` ↔ зібрати всіх; `reach-exit` ↔ дім; `undo-redo` + `restart-level` ↔ undo і R; `sequential-levels` ↔ 48 рівнів; `idle-animation` ↔ DadHog засинає.
- **Нема** → пропозиції карток:
  - `+pivot-rotate` (вже пропонована Sokobond) — поворот усієї групи навколо півота.
  - `+growing-polyomino-avatar` «Аватар-поліоміно, що росте від зібраного» · entities/state · 🥉.

## Пропозиції до словників
- `+effect:move_group` — зсув злиплої групи як одного тіла (прикл; уже просила Elephant in a Bottle).
- `+card:growing-polyomino-avatar` · `+card:pivot-rotate` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Prickle](https://store.steampowered.com/app/2759760/) — офіційний опис: прилипання до DadHog і одне до одного, «Tetris-like shape», вузькі проходи в живоплоті, 4 сезони; реліз 22.11.2024.
- [itch.io: Prickle](https://sunbirdstudio.itch.io/prickle) — 48 рівнів, 4 сезони, доступність, мови, платформи.
- [itch.io: Prickle — Jam Version](https://sunbirdstudio.itch.io/prickle-jam) — керування (стрілки/WASD, Q/E або Z/X, R), автори.
- [Ludum Dare 54: Prickle](https://ldjam.com/events/ludum-dare/54/prickle) — опис джем-версії (через API LD).
- [Steam Release Postmortem](https://sunbirdstudio.itch.io/prickle-jam/devlog/845342/steam-release-postmortem) — «when two hedgehogs touched, they stuck together», що додала повна версія (undo, підказки, катсцени, темний режим).
- [Pocket Gamer](https://www.pocketgamer.com/prickle/out-now/) — мобільний реліз, «pivoting around obstacles», ризик застрягнути.
- [The Refined Geek](https://therefinedgeek.com.au/index.php/2024/12/20/prickle-schnuffin-hoglets/) — undo, рестарт, липкі перешкоди.
- YouTube: пошук «prickle sunbird studio gameplay».

## Непевне
- (?) Центр повороту прикла і чи перевіряється дуга повороту, а не лише кінцеві клітини.
- (?) Сезонні механіки й липкі перешкоди — джерела згадують, але не описують.
- (?) Рецензія Refined Geek пише, що їжак «штовхає» їжачат до виходу, — розходиться з офіційним «прилипають»; узято офіційне.
- (?) Засинання DadHog від бездіяльності й «тупіт їжачат» на початку нового набору рівнів — з пошукового витягу рецензії PC Gamer (сама сторінка не відкрилась).
- (?) «Prickle: Hedgehog Logic Puzzle» на Xbox/PlayStation — порт цієї гри чи інша гра, не перевірено.
