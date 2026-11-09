---
title: Nekograms
slug: nekograms
aka: [Nekograms+]
family: push-slide
also: []
klass: figure
axes:
  field: layers
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [iOS, Android, Switch, PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2478120/", best: true, note: "правило «коти лише вліво-вправо, подушки лише вгору-вниз», зірки за ходи, Endless, 160 рівнів у 4 світах"}
  - {kind: other, url: "https://press.hungrysky.com/nekograms", note: "прес-кіт: дати всіх платформ, історія від геймджему 2015, команда, нагороди"}
  - {kind: other, url: "https://explosionnetwork.com/nekograms-review", note: "огляд iOS: довгі й короткі коти, подушки мають бути досить довгі, лічильник ходів угорі"}
  - {kind: other, url: "https://www.cubed3.com/games/reviews/nintendo-switch/nekograms", note: "огляд Switch: кіт прокидається, коли подушку прибрали; перешкоди; Endless — випадкові пазли"}
  - {kind: other, url: "https://purenintendo.com/review-nekograms-nintendo-switch/", note: "огляд Switch: перешкоди (мʼячі, чашки), рекомендовані ходи, три світи по 40, тач"}
  - {kind: other, url: "https://apps.apple.com/us/app/nekograms/id1671723832", note: "Nekograms+ (Apple Arcade): щоденні пазли, Game Center, сезонні теми"}
  - {kind: official, url: "https://nekograms.com", note: "сайт: лінки на всі магазини"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nekograms+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, impassable-cells, drag-drop-piece, swipe-gestures, move-counter, level-select, puzzle-select, level-unlock, sequential-levels, daily-puzzle, achievements-window, leaderboard, end-screen, help-window, +axis-locked-move, +stars-rating, +layered-pieces, +cover-to-satisfy, +endless-random-puzzles, +skip-level-par]
proposes: ["+cond:on_top(a, b)", "+trigger:all_satisfied(kind)", "+axis:control=axis-per-type", "+feature:skip-after-par", "+feature:endless-random", "+card:layered-pieces", "+card:cover-to-satisfy"]
author: opus
date: 2026-11-09
---

# Nekograms — коти їздять лише вліво-вправо, подушки лише вгору-вниз; уклади кожного кота повністю на подушки

## Суть
Затишна головоломка з ковзними блоками від австралійської Hungry Sky. На сітці лежать коти (короткі й довгі, горизонтальні) і подушки (короткі й довгі, вертикальні). **Котів можна рухати лише по рядку, подушки — лише по стовпцю**; кіт засинає, коли всі його клітини лежать на подушках, а рівень пройдено, коли сплять усі коти. Рахуються ходи: уклався в оптимум — три зірки. Назва грає словами «neko» + «nonogram»: розвʼязок складається з рядів котів і стовпців подушок.

## Поле і час
- Невелика квадратна сітка (на скріншотах 4×4 … 7×6, у пізніх світах вужча й довша); обрамлення — декор світу (кавʼярня, пляж, сакуровий парк, аркада).
- Два шари рухомих фігур: подушки внизу, коти зверху — кіт може стояти на подушці, подушка — виїхати з-під кота (?) (див. «Непевне»).
- Перешкоди займають клітину: вазон, чашка, мʼяч, бенто, кіт, що полює на лазерну точку.
- Час не тече, хід = одне переміщення фігури; лічильник «Moves: X of N».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кіт | piece | довжина 1…4 (?) по горизонталі, порода, аксесуар | рухається лише вліво-вправо; спить, якщо всі його клітини на подушках |
| Подушка | piece | довжина 1…4 (?) по вертикалі | рухається лише вгору-вниз; кіт на ній засинає |
| Перешкода | static | вигляд за світом | займає клітину, блокує рух |
| Ковдра / рушник у клітині | terrain | — | є на скріншотах 2-го і 3-го світу; роль (?) |
| Кіт, що спить | piece | стан «спить» | закриті очі; прокидається, якщо подушку прибрали |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cat)` → ЯКЩО `moving(cat, left)` або `moving(cat, right)` і `free(target_cells)` → ТО `move(cat, dir)`, `counter(moves, +1)`.
- КОЛИ `input(drag, cushion)` → ЯКЩО `moving(cushion, up)` або `moving(cushion, down)` і `free(target_cells)` → ТО `move(cushion, dir)`, `counter(moves, +1)`.
- Рух по другій осі для фігури неможливий: КОЛИ `input(drag, cat)` → ЯКЩО `moving(cat, up)` або `moving(cat, down)` → ТО `block` (для подушки — навпаки).
- Перешкоди й фігури того самого шару блокують: ЯКЩО `occupied(target_cell, obstacle)` або `occupied(target_cell, cat)` (для кота) → ТО `block`.
- КОЛИ `custom: «кожна клітина кота лежить на клітині подушки»` → ТО `set_state(cat, asleep)`.
- КОЛИ `state_off(cat, on_cushions)` (подушку прибрали з-під кота) → ТО `clear_state(cat, asleep)`, `sound(wake)`.
- КОЛИ `custom: «спить кожен кіт рівня»` → ТО `win`, `window(end-screen)`.
- КОЛИ `win` → ЯКЩО `counter(moves, <=, par)` → ТО `custom: «3 зірки, PURRFECT!»`; інакше `custom: «менше зірок»`.
- КОЛИ `counter(moves, >, par)` → ТО `custom: «зʼявляється кнопка пропуску рівня»` (з оновлення 1.2.x).
- КОЛИ `input(undo)` → ТО `undo(1)`.
- Перемога: усі коти сплять. · Поразка: нема, лише менше зірок. · Рахунок: 1–3 зірки за кількістю ходів відносно `par-moves`.

## Керування і ввід
- Тач / миша: вибрати кота чи подушку й потягнути — підказкою зʼявляються стрілки дозволеної осі (◀ ▶ для кота, ▲ ▼ для подушки).
- Геймпад (Switch, Steam): курсор-лапка, Y — undo, кнопка Menu; A — далі.
- Чи хід — це зсув на одну клітину чи на будь-яку відстань одним перетягуванням, точно не перевірено (оптимуми 5–8 ходів на дошках 4×4 натякають на «будь-яку відстань») (?).

## Вікна, меню, HUD
- `main-menu` / вибір світу: Neko Cafe, пляж, сакуровий парк, Nyan Nyan Plaza; вхід в Endless.
- `puzzle-select` — сітка 40 рівнів світу (1-1…1-40) з 0–3 зірками, відсоток завершення світу, «Back», «Next» до наступного світу, кнопка «How to Play» (`help-window`).
- `game-screen` — назва рівня («4-1 Claw Machine Skills»), поле, внизу `move-counter` з `par-moves` («Moves: 0 of 5»), `undo-button`, кнопка Menu.
- `end-screen` — зірки, «PURRFECT!», «Moves: 8», галочка «Complete in 8 moves», «Next».
- `mode-select` / Endless: дошка, етап «Spirit Realm 6/20», ціль «Complete in 16 moves», мітка складності «Hard».
- `daily-window` — Nekograms+ (Apple Arcade): розминка → щоденний пазл → щоденний виклик, «кіт дня».
- `achievements-window` і `leaderboard` — Game Center (Apple Arcade).

## Фічі поза полем
- `levels-sequential` + `level-unlock` (у 2026 систему блокування прибрали — будь-який рівень будь-коли), `stars-rating`, `par-target`.
- `mode-endless` — відкривається після проходження (тепер — після будь-якого рівня), випадкові пазли етапами «станів котячої свідомості».
- `mode-daily` / `daily-puzzle` — лише Nekograms+ (Apple Arcade), сезонні теми й аксесуари.
- `+skip-after-par`, `undo`, `touch-controls`, `gamepad-support`, `localization` (15 мов), `cloud-save` (Steam).
- Косметика: 15+ порід котів, аксесуари-капелюхи (нові — в оновленнях).

## Варіації й родичі
- Версії: iOS/Android (16.12.2021) → Nekograms+ на Apple Arcade (2023, щоденні пазли) → Switch (3.10.2024) → Steam (10.03.2025) → оновлення Nyan Nyan Plaza (+40 рівнів, 4-й світ).
- Осі варіацій:
  - **обмеження осі**: кожна фігура на своїй осі (`rush-hour`, `unblock-me`) / **вісь задана типом** — усі коти горизонтально, усі подушки вертикально (тут);
  - **мета**: вивести одну фігуру (`rush-hour`) / **накрити кожну фігуру одного типу фігурами іншого** (тут) / поставити на цілі (`sokoban`);
  - **шари**: усі фігури в одному шарі / **два шари, що проходять один під одним** (тут).
- Родичі: `rush-hour`, `unblock-me`, `klotski`, `sliding-tile-permutation`.

## Цікавинки для курсу
- Фігури різної довжини з віссю, заданою типом, і перевірка вільності всіх клітин на шляху — 📎.
- Два шари: подушка проїжджає під котом, кіт — над подушкою; стан «спить» перераховується після кожного ходу — 📎.
- Оцінка ходів проти оптимуму: зірки + пропуск після перевищення — 🌱.
- Розвʼязувач BFS для пошуку оптимуму (як у Rush Hour) — 🥈.
- Генерація випадкових розвʼязних дошок для Endless з оцінкою складності — 🥇.

## Мапа на каталог
- Є: `multi-cell-size` ↔ довгі коти й подушки; `impassable-cells` ↔ перешкоди; `drag-drop-piece` + `swipe-gestures` ↔ перетягування; `move-counter` ↔ «Moves: X of N»; `level-select` + `puzzle-select` + `level-unlock` + `sequential-levels` ↔ світи по 40; `daily-puzzle` ↔ Nekograms+; `achievements-window` + `leaderboard` ↔ Game Center; `end-screen` ↔ «PURRFECT!»; `help-window` ↔ «How to Play».
- **Нема** → пропозиції карток:
  - `+axis-locked-move` (вже Rush Hour, Unblock Me) · слот {by: type}.
  - `+stars-rating` (вже Rush Hour, Klotski) · слот {by: moves}.
  - `+layered-pieces` «Два шари рухомих фігур, що проходять один під одним» · entities/legality · 📎.
  - `+cover-to-satisfy` «Фігура задоволена, коли повністю лежить на фігурах іншого типу» · game-logic/win · 🌱.
  - `+endless-random-puzzles` «Нескінченна серія згенерованих пазлів з міткою складності» · levels/generation · 🥇.
  - `+skip-level-par` «Пропуск рівня після перевищення оптимуму ходів» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:on_top(a, b)` — усі клітини A лежать на клітинах B (кіт на подушках); `fits` — про вміщення фігури у вільні клітини, а не про накриття.
- `+trigger:all_satisfied(kind)` — кожна сутність виду в стані «задоволена» (усі коти сплять); `all_on` — про цілі-клітини.
- `+axis:control=axis-per-type` — вісь руху задана типом фігури, а не окремою фігурою.
- `+feature:skip-after-par` — пропуск рівня зʼявляється після перевищення цільової кількості ходів.
- `+feature:endless-random` — нескінченний режим з випадковими пазлами (`mode-endless` без уточнення генерації).
- `+card:layered-pieces`, `+card:cover-to-satisfy` — див. вище.

## Джерела
- ⭐ [Steam: Nekograms](https://store.steampowered.com/app/2478120/) — «Cats only move left and right, and cushions only move up and down», «Cats only sleep on cushions», зірки за найменше ходів, Endless, 160 рівнів у 4 світах, оновлення Nyan Nyan Plaza.
- [Прес-кіт Hungry Sky](https://press.hungrysky.com/nekograms) — дати релізів (iOS/Android 16.12.2021, Apple Arcade 2023, Switch 3.10.2024, Steam 10.03.2025), історія з геймджему 2015, нагороди.
- [Explosion Network](https://explosionnetwork.com/nekograms-review) — «long cats, short cats… pillows long enough to accommodate», лічильник ходів, без покарання за довгий розвʼязок.
- [Cubed3](https://www.cubed3.com/games/reviews/nintendo-switch/nekograms) — кіт прокидається, коли подушку прибрали; перешкоди; Endless — випадкові пазли; баг «кіт на клітині перешкоди».
- [Pure Nintendo](https://purenintendo.com/review-nekograms-nintendo-switch/) — мʼячі й чашки як перешкоди, рекомендована кількість ходів, три світи по 40, тач.
- [App Store: Nekograms+](https://apps.apple.com/us/app/nekograms/id1671723832) і [App Store: Nekograms](https://apps.apple.com/us/app/nekograms/id1595765860) — щоденні пазли, Game Center, «skip option when players pass the move target».
- Скріншоти Steam (переглянуто): «Moves: 0 of 5», Undo/Menu, стрілки осі на вибраній фігурі, екран «PURRFECT!», Endless «Spirit Realm 6/20», сітка рівнів Neko Cafe зі зірками й «How to Play».

## Непевне
- (?) Хід = зсув на 1 клітину чи ковзання/перетягування на будь-яку відстань.
- (?) Чи може подушка рухатись, коли на ній кіт (Cubed3: кіт прокидається, коли подушку прибирають; Explosion Network: коти на подушках заважають рухати фігури).
- (?) Чи блокують перешкоди лише котів, лише подушки чи обидва шари; роль ковдр/рушників у клітинах.
- (?) Звʼязок із нонограмами — лише в назві й рекламі («based on nonograms»); числових підказок на полі не бачив.
- (?) Максимальна довжина кота й подушки та розміри дошок — оцінка зі скріншотів.
