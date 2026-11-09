---
title: Watch Your Step (Aaron Steed)
slug: watch-your-step-steed
aka: [Обережно з кроками]
family: push-slide
also: [falling-match]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=0e692c47ab0b18099c2485d644590b4e", best: true, note: "грати в браузері (PuzzleScript), одна кімната 7×7"}
  - {kind: other, url: "https://api.github.com/gists/0e692c47ab0b18099c2485d644590b4e", note: "повний код: насіння, стадії росту, злиття ящиків 1→5, умова перемоги; гіст від 31.12.2017"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Watch+Your+Step+Aaron+Steed+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, tile-merge, visited-trail, impassable-cells, undo-unlimited, restart-level, level-from-txt, +growth-stages, +trail-spawn, +push-merge, +self-crowding]
proposes: ["+trigger:step_off", "+cond:uncovered", "+feature:prototype-single-level", "+card:trail-spawn", "+card:push-merge"]
author: opus
date: 2026-11-09
---

# Watch Your Step — кожен крок саджає насіння, що виростає в ящик «1»; штовхай рівні ящики один в один, доки не збереш «5»

## Суть
Мініатюрна PuzzleScript-гра Аарона Стіда (одна кімната, 2017): гравець ходить порожньою кімнатою, і **кожна клітина, з якої він зійшов, отримує насіння**. Насіння за кілька ходів проростає в ящик номер 1. Ящики штовхаються по одному; штовхнутий у ящик з тим самим номером — зливається в ящик на 1 більший, як у Threes/2048. Мета — зібрати ящик «5», не замурувавши себе ящиками, що ростуть з власного сліду.

## Поле і час
- Одна кімната 7×7 вільних клітин у рамці стін; гравець стартує в центрі.
- Покроково: хід рахується, лише якщо гравець справді зрушив (`require_player_movement`); удар у стіну — не хід, насіння не росте.
- Шари: фон → насіння (стадії 0–4) → ціль (у коді є, не використовується) → обʼєкти (гравець, ящики, стіни).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух 4 напрямки; штовхає один ящик; клітина під ним отримує насіння |
| Насіння | terrain | стадія 0–4 | щохід +1 стадія, якщо на ньому нічого не стоїть; стадія 4 → ящик 1 |
| Ящик 1…5 | object | номер | штовхається на 1; у ящик з тим самим номером — зливається в номер +1 |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; інакше хід скасовано повністю (`block`).
- КОЛИ `turn_start(player)` → ЯКЩО `not cell(under_player, seed)` → ТО `set_cell(under_player, seed_0)` — клітина, з якої гравець іде, засіяна.
- КОЛИ `turn_end(player)` → ЯКЩО `not occupied(seed_cell, object)` → ТО `set_cell(seed_cell, next_stage)`; насіння під гравцем чи ящиком не росте.
- КОЛИ `custom: «насіння досягло стадії 4»` → ЯКЩО `free(seed_cell)` → ТО `spawn(crate_1)`, насіння зникає.
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`, `move(player, dir)`.
- КОЛИ `contact(moving_crate, crate)` → ЯКЩО `same(moving_crate, crate, number)` і `custom: «номер < 5»` → ТО `merge(moving_crate, crate → crate_n+1)`, `move(player, dir)` (рушійний ящик зникає, нерухомий зростає на 1).
- КОЛИ `contact(moving_crate, crate)` → ЯКЩО `not same(moving_crate, crate, number)` → ТО `block` (ряд ящиків не штовхається).
- КОЛИ `counter(crate_5, >=, 1)` → ТО `win`, `message(«well done…»)`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: на полі є ящик «5». · Поразка: нема; замурувався — undo або рестарт. · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; кнопки дії немає (у коді не використовується).
- Z — undo, R — рестарт (стандарт PuzzleScript).

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript (назва, автор).
- `custom-window` — три текстові екрани правил перед кімнатою: «кожен крок лишає насіння, що виростає в ящик 1» · «штовхни два ящики з однаковим номером, щоб отримати більший» · «зроби ящик 5».
- `game-screen` — кімната; номер ящика й стадія росту насіння намальовані крапками на спрайті (HUD нема).
- `end-screen` — повідомлення «well done, I couldn't be bothered to find out myself, do let me know».

## Фічі поза полем
- `undo` (∞), `restart-level` — штатні PuzzleScript.
- `tutorial` — правила подано трьома екранами-повідомленнями.
- Один рівень; автор сам не перевіряв, чи «5» досяжна, — `prototype-single-level`.

## Варіації й родичі
- Осі варіацій:
  - **звідки беруться плитки**: випадкова поява після ходу (`2048`, `threes`) / ставиш сам (`triple-town`) / **виростають з твого сліду** (Watch Your Step);
  - **як зливаються**: свайп рухає все поле (`2048`) / **поштовх одного ящика в рівний** (Watch Your Step) / три сусідні (`triple-town`);
  - **слід**: нема / стіна-слід (Snake, Tron) / **слід з відкладеною дією** — росте через кілька ходів (Watch Your Step), кактус-тіло (`room-to-grow`).
- Родичі: `sokoban` (поштовх одного ящика), `room-to-grow` (ріст замість кроку), `2048`, `threes`, `triple-town`.

## Цікавинки для курсу
- Слід, що через N ходів стає перешкодою: стадії росту на клітинах + пауза, коли клітина зайнята — 📎.
- Поштовх із злиттям рівних номерів (Threes без свайпа) — 📎.
- «Хід не відбувся — світ не тікає» (`require_player_movement`) — 🌱.
- Самоущільнення: кожен крок додає ящик, злиття прибирає — баланс ресурсу на 49 клітинах; перевірити розвʼязуваність «5» перебором — 🥇 (автор сам не знав).
- Порядок правил росту (від старшої стадії до молодшої, щоб насіння росло на 1 за хід) — 🌱, гарний урок про порядок оновлення клітин.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ поштовх одного ящика; `tile-merge` ↔ рівні ящики зливаються; `visited-trail` ↔ насіння на пройдених клітинах; `impassable-cells` ↔ стіни; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-карта.
- **Нема** → пропозиції карток:
  - `+growth-stages` (вже пропонована Stardew, Photosynthesis) · слот {stages: 5}.
  - `+trail-spawn` «Слід гравця за N ходів стає обʼєктом» · entities/spawn · 📎 · слот {delay}.
  - `+push-merge` «Штовхнутий у рівний — зливається в +1» · entities/legality · 📎 — дитина `tile-merge` + `push-object`.
  - `+self-crowding` «Кожна дія додає перешкоду, мета — встигнути до замурування» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+trigger:step_off` — гравець зійшов з клітини (тут — засіяти її); `leave(a, cell_type)` є, але потребує типу клітини.
- `+cond:uncovered` — на клітині нема жодного обʼєкта (умова росту).
- `+feature:prototype-single-level` — гра з одного рівня-експерименту.
- `+card:trail-spawn`, `+card:push-merge` — див. «Мапа на каталог».

## Джерела
- ⭐ [PuzzleScript: Watch Your Step](https://www.puzzlescript.net/play.html?p=0e692c47ab0b18099c2485d644590b4e) — гра в браузері.
- [GitHub Gist (API)](https://api.github.com/gists/0e692c47ab0b18099c2485d644590b4e) — сирці: `require_player_movement`, стадії Floor0–Floor4 → Crate0, злиття `[ > Crate0 | Crate0 ] -> [ | Crate1 ]` до Crate4, перемога `Any Crate4`, кімната 7×7, тексти повідомлень.
- YouTube: пошук «Watch Your Step Aaron Steed puzzlescript».

## Непевне
- (?) Скільки ходів від насіння до ящика: за порядком правил у коді — 4 ходи вільної клітини (одна стадія пізня, дві стадії за той самий хід); у грі не перевірено.
- (?) Чи досяжна «5» на 7×7 — сам автор не перевіряв.
- (?) Чи гра публікувалась ще деінде (сайт автора, itch, галерея PuzzleScript) — не перевірено; рік 2017 — за датою гіста.
