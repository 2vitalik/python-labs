---
title: A Man Walks Into A Scrollbar
slug: a-man-walks-into-a-scrollbar
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2026
platforms: [web]
links:
  - {kind: itch, url: "https://dee-3.itch.io/a-man-walks-into-a-scrollbar", best: true, note: "грати в браузері (HTML5, клавіатура й тач); 21 рівень; сесія «a few minutes» за itch"}
  - {kind: other, url: "https://itch.io/jam/pixojam/rate/4450777", note: "сторінка гри на PixoJam 2026 (зроблено за ~9 днів)"}
  - {kind: other, url: "https://auroriax.github.io/PuzzleScript/", note: "PuzzleScript Plus — рушій гри (flickscreen, вибір рівня з замками)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A+Man+Walks+Into+A+Scrollbar+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, sequential-levels, level-select, level-unlock, undo-unlimited, restart-level, sound-effects, +push-chain, +axis-locked-block, +world-scroll, +screen-anchored, +counter-scroll, +offscreen-content]
proposes: ["+card:world-scroll", "+card:screen-anchored", "+card:counter-scroll", "+card:offscreen-content"]
author: opus
date: 2026-11-19
---

# A Man Walks Into A Scrollbar — Sokoban, де ящик-бігунок на доріжці прокручує весь рівень під нерухомим екраном

## Суть
Sokoban у кадрі 11×9 (Dee, PuzzleScript Plus, PixoJam 2026): треба накрити ящиками всі цілі. Ядро — **бігунок прокрутки**: червоно-помаранчевий ящик, що їздить лише своєю доріжкою; кожен його крок зсуває на клітину весь рівень — стіни, ящики й цілі, зокрема ті, що лежать поза екраном. Колір кодує ставлення до прокрутки: помаранчеве їде разом із бігунком, червоне (як і сам гравець) привʼязане до екрана й стоїть, синє їде навпаки — «як справжня прокрутка». Розвʼязки будуються на зсуві одного шару відносно іншого: ціль підʼїжджає під нерухомий червоний ящик, стіна відʼїжджає й відкриває прохід.

## Поле і час
- Карта 33×27 = 3×3 екрани (`flickscreen 11x9`), гравцеві видно лише середній екран 11×9; перший рівень — сам екран 11×9 без прокрутки.
- Довкола видимого кадру — невидима рамка `Edge`: гравець за неї не виходить; поза кадром лежать стіни, ящики й цілі, які прокрутка приводить у кадр (інформація прихована, доки не прокрутиш).
- Кожен вид обʼєкта — окремий шар колізій; блокування задають лише правила (стіни зупиняють рухоме, ящики штовхаються ланцюгом).
- Покроково: хід = крок гравця з усіма поштовхами; прокрутка відбувається в тому самому ході. Анімацій чи таймерів нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | червоний (не прокручується) | рух 4 напрямки в межах кадру; штовхає будь-які ящики |
| Ящик (помаранчевий) | object | прокручується з бігунком | штовхається ланцюгом; накриває будь-яку ціль |
| Стіна (помаранчева) | static | прокручується з бігунком | непрохідна для гравця й ящиків |
| Ціль (помаранчева) | zone | прокручується з бігунком | має бути накрита ящиком будь-якого кольору |
| Бігунок прокрутки | object | лише на доріжці | штовхається тільки вздовж доріжки; крок бігунка = крок прокрутки світу; на ціль не зараховується |
| Доріжка (scrollbar) | terrain | пряма лінія клітин | по ній їздить бігунок; сама не прокручується |
| Червона стіна | static | привʼязана до екрана | при прокрутці стоїть; непрохідна |
| Червоний ящик | object | привʼязаний до екрана | при прокрутці стоїть; штовхається як звичайний; на старті може ховатися всередині помаранчевої стіни |
| Червона ціль | zone | привʼязана до екрана | при прокрутці стоїть; приймає ящик будь-якого кольору |
| Синя стіна | static | прокручується навпаки | при кроці бігунка на d зсувається на −d |
| Синій ящик | object | прокручується навпаки | зсувається на −d; штовхається як звичайний |
| Синя ціль | zone | прокручується навпаки | зсувається на −d; приймає ящик будь-якого кольору |
| Рамка кадру (Edge) | static | невидима | зупиняє лише гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, edge)` → ТО `block` — гравець завжди лишається в кадрі 11×9.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_after_chain)` (ряд ящиків будь-яких кольорів до першої клітини без стіни) → ТО `push` усього ланцюга; інакше `block`.
- КОЛИ `contact(player|crate, scroll_thumb)` → ЯКЩО `cell(next_cell, track)` and `free(next_cell)` → ТО `push`; інакше `block` (з доріжки бігунок не сходить).
- КОЛИ `after(push(scroll_thumb, d))` → ТО `shift(orange_walls+crates+targets, d)` по всій карті, `shift(blue_walls+crates+targets, −d)`; гравець, червоні обʼєкти, доріжка й рамка — на місці.
- КОЛИ `contact(player, crate)` → ЯКЩО `cell(cell_behind, edge)` → ТО `push` — ящик іде за кадр; повернути його може лише прокрутка (з коду).
- КОЛИ `all_on(target, crate)` (кожна ціль будь-якого кольору накрита ящиком будь-якого кольору, крім бігунка) → ТО `win`, `next_level`.
- КОЛИ `input(Z)` → ТО `undo(1)`.
- КОЛИ `input(R)` → ТО `restart`.
- Перемога: усі цілі накриті. · Поразки нема (глухий кут — undo/рестарт). · Рахунку нема.

## Керування і ввід
- Стрілки (у грі — підпис «arrow keys to move»), також WASD (стандарт PuzzleScript); Z — undo; R — рестарт; Esc — меню.
- Тач-ввід на мобільних (itch: Keyboard, Touchscreen).
- Окремої кнопки прокрутки нема: прокрутка — це поштовх бігунка.

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript Plus із назвою, автором і підписом керування.
- `level-select` — список секцій Intro 1–3 · Scrolling 1–3 · Red 1–4 · Redder 1–3 · Blue 1–4 · Doom 1–3 · Goodnight; непройдені закриті (`level_select_lock`).
- `custom-window` — титульні картки розділів («Intro», «Scrolling», «Red», «Redder», «Blue», «Doom», «Goodnight») і фінальне «Thank you for playing!!».
- `game-screen` — кадр 11×9 без HUD; колір обʼєкта — його правило прокрутки.
- Переходи: титул → вибір рівня → рівень → (усі цілі накриті) наступний рівень / картка розділу.

## Фічі поза полем
- `levels-sequential` + `level-select` з `level-unlock`: 21 рівень у 7 розділах, кожен розділ додає колір чи комбінацію.
- `undo` без ліміту, `restart-level`, автозбереження прогресу (стандарт PuzzleScript Plus).
- Звуки на поштовх і кінець рівня; нема налаштувань, підказок, редактора.

## Варіації й родичі
- Родичі в корпусі: [increpare: Scalesoban і Explodoban](increpare-sokoban-variants.md) (`+counter-move-all` — поштовх зсуває все інше), [Magiciban](magiciban.md) (зсув підлоги), [Arranger](arranger.md) і [MazezaM](../push-slide/mazezam.md) (зсув цілого ряду), [Toroban](toroban.md) (тор), [The Observer's Paradox](the-observers-paradox.md) (поза полем зору поводиться інакше).
- Осі варіацій:
  - **що рухає світ**: ніщо (Sokoban) / ряд, у якому стоїш (Arranger) / окремий бігунок на доріжці (тут);
  - **ставлення шару до прокрутки**: з бігунком / привʼязаний до екрана / навпаки (тут — усі три, кольором);
  - **скільки бігунків**: один / два на різних осях (рівень Blue 4);
  - **що поза екраном**: нічого / прихований вміст, який приїздить (тут).

## Цікавинки для курсу
- Прокрутка як зсув усіх обʼєктів шару на клітину без перевірки колізій — 📎 (цикл по шару).
- Три класи обʼєктів за кольором: з прокруткою, привʼязані до екрана, проти прокрутки — 🥉 (той самий зсув із множником +1 / 0 / −1).
- Бігунок, що ходить лише доріжкою, + ланцюгове штовхання ящиків — 📎.
- Карта більша за кадр: видно 11×9, решта прихована, доки не приїде — 🥉 (вʼюпорт + світові координати).
- Перемога «кожна ціль накрита ящиком будь-якого кольору» — 🌱.
- Розвʼязувач BFS: стан = позиція гравця + зсув світу + ящики кожного кольору — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ крок; `push-object` ↔ ящики; `impassable-cells` ↔ стіни; `all-on-targets` ↔ перемога; `sequential-levels` · `level-select` · `level-unlock` ↔ 7 розділів із замками; `undo-unlimited` · `restart-level` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+world-scroll` «Бігунок прокручує весь рівень» · entities/move · 🥉 · слоти {axis, track_len} — родич `swipe-all-shift`, але зсуває світ, а не плитки.
  - `+screen-anchored` «Обʼєкт привʼязаний до екрана, прокрутка його не зсуває» · entities/move · 🌱.
  - `+counter-scroll` «Обʼєкт прокручується в протилежний бік» · entities/move · 🌱 · слот {factor: −1}.
  - `+offscreen-content` «Рівень більший за кадр, приховане приїздить прокруткою» · interface/render · 📎 — родич `player-camera`, але камера стоїть.
  - `+push-chain` (вже в корпусі) · `+axis-locked-block` (вже в корпусі, Escape) — бігунок їздить лише своєю доріжкою.

## Пропозиції до словників
- `+card:world-scroll`, `+card:screen-anchored`, `+card:counter-scroll`, `+card:offscreen-content` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `after`, `all_on`, `free`, `cell`, `move`, `shift`, `undo`, `restart`, `next_level`.

## Джерела
- ⭐ [itch: A Man Walks Into A Scrollbar](https://dee-3.itch.io/a-man-walks-into-a-scrollbar) — гра в браузері; опис «made in about 9 days in PuzzleScript Plus», PixoJam 2026, коментарі гравців (коментар автора: бігунок червоний, бо «scrollbar, що прокручує сам себе», — надто дико); вихідний код узято з HTML вбудованої гри (`sourceCode`): OBJECTS, LEGEND, COLLISIONLAYERS, RULES, WINCONDITIONS, 21 рівень.
- [PixoJam 2026: сторінка гри](https://itch.io/jam/pixojam/rate/4450777) — участь у джемі.
- [PuzzleScript Plus](https://auroriax.github.io/PuzzleScript/) — рушій: `flickscreen`, `level_select`, `level_select_lock`, `text_controls`.
- YouTube: [пошук](https://www.youtube.com/results?search_query=A+Man+Walks+Into+A+Scrollbar+puzzlescript).

## Непевне
- (?) Прокрутка не перевіряє, куди їдуть стіни й ящики: з коду помаранчева стіна може насунутись на клітину з гравцем чи червоним обʼєктом (різні шари колізій); схоже, рівні збудовано так, щоб цього не траплялось, — у грі не перевірено.
- (?) Виштовхнути ящик за рамку кадру можна з коду (рамка зупиняє лише гравця); чи це використано в рівнях — не перевірено.
- (?) Точна дата релізу: рік 2026 — за PixoJam 2026 і найранішим коментарем (квітень 2026); дату публікації сторінка не показує.
- (?) Підтримка WASD і поведінка Esc — стандарт рушія, у грі не перевірено.
