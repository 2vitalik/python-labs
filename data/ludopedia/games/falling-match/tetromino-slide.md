---
title: Tetromino Slide / Tetromino-Rutsch
slug: tetromino-slide
aka: [Tetromino-Rutsch]
family: falling-match
also: [push-slide, thinky]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://games.increpare.com/tetromino_slide/", best: true, note: "грати в браузері (EN/DE)"}
  - {kind: other, url: "https://github.com/increpare/tetromino-slide", note: "вихідний код (game.js, ~1300 рядків)"}
  - {kind: official, url: "https://www.increpare.com/game/tetromino-slide-tetromino-rutsch.html", note: "сторінка гри, дата 2019-08-30"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=increpare+tetromino+slide+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [swipe-all-shift, gravity-fall, multi-cell-size, piece-rotate-flip, next-queue, keyboard-controls, cell-click, score-records, save-progress, end-screen, restart-level, language-picker, sound-effects, +line-clear, +bag-randomizer, +ghost-piece, +rigid-body-stacking, +tilt-instead-of-fall, +clear-n-lines-win]
proposes: ["+card:tilt-instead-of-fall", "+card:clear-n-lines-win"]
author: opus
date: 2026-11-09
---

# Tetromino Slide — Tetris без падіння: фігури лежать, доки ти не нахилиш усе поле

## Суть
Маленька гра increpare (Stephen Lavelle), двомовна (EN/DE). Тетроміно не падають самі: гравець кидає наступну фігуру зверху, і **все поле нахиляється** — кожна фігура як тверде ціле ковзає вниз, вліво чи вправо до упору, як плитки в 2048. Повні ряди зникають. Перемога — очистити 4 ряди за один хід («тетріс»); поразка — нема місця для нової фігури. Гібрид Tetris і tilt-головоломки.

## Поле і час
- Поле 10×22, з них 4 верхні ряди приховані (зона появи); видимо 10×18.
- Кожна клітина памʼятає, з якими сусідами вона з однієї фігури (біти зʼєднань): фігура рухається як ціле. Очищення ряду рве ці звʼязки — уламки стають меншими фігурами.
- Покроково: хід = нахил; нахил анімується крок за кроком (≈30 мс), доки ніщо не рухається. Таймера нема — фігури не падають без вводу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура-тетроміно | tile | тип (7), поворот, звʼязки | при нахилі ковзає як тверде ціле на 1 за крок, доки будь-яка її клітина не впреться в край або нерухому клітину |
| Уламок фігури | tile | 1–3 клітини | частина фігури після очищення ряду; далі ковзає як окреме ціле |
| Наступна фігура | tile | тип, поворот, зсув | стоїть над полем; гравець крутить і зсуває її; контур показує, де ляже |
| Майбутня фігура | tile | тип, поворот | показана у віконці превʼю |
| Зона появи | zone | 4 приховані ряди | має бути порожня, щоб кинути фігуру |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(up)` → ТО `rotate(next_piece, 90)`; якщо не влазить — `custom: «зсунути до центру, доки не влізе»`.
- КОЛИ `input(left|right)` → ЯКЩО `fits(next_piece, offset±1)` → ТО `custom: «зсув наступної фігури на 1»`; і в будь-якому разі `shift(all, dir)`.
- КОЛИ `input(down)` → ЯКЩО `custom: «зона появи порожня й місце під фігуру вільне»` → ТО `place(player, next_piece)` у верхніх рядах, `shift(all, down)`; інакше `lose`.
- КОЛИ `after(shift)` → ЯКЩО `free(cells_ahead)` для всіх клітин фігури (або там клітина, що теж рухається) → ТО `move(piece, dir)`; повтор, доки хоч щось рухається; інакше фігура стоїть.
- КОЛИ `pattern(row_full)` (після нахилу) → ТО `clear(row)`, звʼязки з сусідніми рядами розірвано, ряди вище зсуваються вниз на 1 (простий зсув, без нового нахилу).
- КОЛИ `counter(lines_this_move, >=, 4)` → ТО `win` — екран перемоги.
- КОЛИ `settled` → ЯКЩО `custom: «зона появи зайнята або нову фігуру нема куди поставити»` → ТО `lose`.
- КОЛИ `after(clear)` → ТО `set_value(score, lines_this_move)`, `custom: «якщо більше за рекорд — рекорд = найбільше рядів за хід, у localStorage»`.
- Нова наступна фігура — з мішка 7 типів (bag), поворот — випадковий.

## Керування і ввід
- ↑ / W — повернути наступну фігуру; ← → / A D — зсунути її й нахилити поле вбік; ↓ / S / пробіл — кинути фігуру й нахилити вниз; R / N — нова гра; E — мова EN/DE; M — звук.
- Тач/миша: смуги-кнопки по краях поля (верх — поворот, низ — кинути, бічні — нахил), кнопки «рестарт», «мова», «звук» (pep.js — pointer events).

## Вікна, меню, HUD
- `game-screen`: поле, контур-тінь наступної фігури на місці приземлення, віконце майбутньої фігури, рекорд (3 цифри), кнопки по периметру.
- `end-screen`: картинка «переміг» / «програв» поверх поля; далі — рестарт.
- Меню нема; мова й звук перемикаються на ігровому екрані.

## Фічі поза полем
- `restart-level` (R/N), `leaderboard-local` (один рекорд — найбільша кількість рядів за хід, localStorage), `localization` (EN/DE), `sound-toggle`.
- Звуки — генератор sfxr у браузері.

## Варіації й родичі
- `games/falling-match/tetris.md` — та сама очистка рядів, але фігура падає за таймером і керується до приземлення; тут контролю «в польоті» нема — лише вибір позиції/повороту і напрямок нахилу.
- `games/falling-match/2048.md` і `games/push-slide/ice-sliding-puzzles.md` — нахил усього поля; тут обʼєкти — багатоклітинні тверді тіла.
- `games/thinky/increpare-sokoban-variants.md` — інші мініатюри автора.
- **Осі варіацій:** гравітація — постійна / лише за вводом (нахил); напрямки нахилу — 1 / 3 / 4; рух фігури — тверде ціле / поклітинно (sticky vs naive); ціль — очки / N рядів за хід / виживання.

## Цікавинки для курсу
- Нахил поля з твердими багатоклітинними тілами: ітерація «хто не може рухатись — зупинити й поширити на звʼязаних» до нерухомої точки — 🥉.
- Біти зʼєднань клітин (вгору/вниз/вліво/вправо) як представлення фігур, що рвуться при очищенні — 📎.
- Мішок 7 фігур + випадковий поворот — 🌱.
- Тінь-контур, де ляже фігура, через повторну перевірку `fits` вниз — 🌱.
- Перемога «4 ряди за один хід» замість очок — 🌱.

## Мапа на каталог
- Є: `swipe-all-shift` ↔ нахил поля; `gravity-fall` ↔ нахил вниз; `multi-cell-size` ↔ тетроміно; `piece-rotate-flip` ↔ поворот перед кидком; `next-queue` ↔ превʼю майбутньої; `keyboard-controls` + `cell-click` ↔ клавіші й тап-кнопки; `score-records` + `save-progress` ↔ рекорд у localStorage; `end-screen`; `restart-level`; `language-picker` ↔ EN/DE; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+line-clear`, `+bag-randomizer`, `+ghost-piece` — уже запропоновані в `tetris.md`.
  - `+rigid-body-stacking` «Фігури лежать як тверді тіла» · entities/move · 📎 (уже пропонувалась).
  - `+tilt-instead-of-fall` «Гравітація лише за ввід-нахилом усього поля» · entities/move · 🥉 · слот {dirs: down|left|right}.
  - `+clear-n-lines-win` «Перемога — N рядів за хід» · game-logic/win · 🌱 · слот {n: 4}.

## Пропозиції до словників
- `+card:tilt-instead-of-fall`, `+card:clear-n-lines-win` — механік нема в каталозі.

## Джерела
- ⭐ [Грати](https://games.increpare.com/tetromino_slide/) — EN/DE.
- [Вихідний код](https://github.com/increpare/tetromino-slide) — `game.js`: поле 10×22 (4 приховані ряди), `doMove` з поширенням блокування по звʼязках, `prüfZeilen` (≥4 ряди → перемога), мішок 7, рекорд `my_max_combo` у localStorage, клавіші.
- [Сторінка на increpare.com](https://www.increpare.com/game/tetromino-slide-tetromino-rutsch.html) — дата 2019-08-30, лінки play/source.

## Непевне
- (?) Черга описувала гру як «тетроміно-ковзання — варіація Sokoban» і клала в thinky; за кодом це Tetris-гібрид — файл у `falling-match`.
- (?) Чи можна нахилити поле вгору — у коді ↑ лише крутить фігуру; нахилу вгору нема.
- (?) Рядки вище очищеного зсуваються наївно (поклітинно на 1), а не новим нахилом твердих тіл — так у коді; як це виглядає у грі, не перевірено.
- (?) У `game.js` є залишки іншої гри (поле 4×4, flood fill) — у Tetromino Slide, схоже, не використовуються.
