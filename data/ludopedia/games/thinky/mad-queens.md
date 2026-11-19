---
title: Mad Queens
slug: mad-queens
aka: []
family: thinky
also: [push-slide, chess-abstract]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2020
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=8ba10d6a0a5a0edd640e0b9431858259", best: true, note: "грати в браузері: 11 рівнів на дошці 8×8"}
  - {kind: other, url: "https://api.github.com/gists/8ba10d6a0a5a0edd640e0b9431858259", note: "вихідний код (gist, JSON, 2020-03-18): штовхання, загрози 6 фігур, загибель, перемога у верхньому ряду"}
  - {kind: other, url: "https://www.puzzlescript.net/Gallery/gifs/8ba10d6a0a5a0edd640e0b9431858259.gif", note: "GIF з галереї: рівень з кіньми, червоні крапки — клітини під боєм"}
  - {kind: official, url: "https://sfiera.net/", note: "сайт автора (Chris Pickel)"}
  - {kind: other, url: "https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js", note: "дані галереї PuzzleScript: назва, автор, лінк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mad+Queens+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, piece-move-patterns, threat-range, death-animation, player-death, reach-exit, undo-unlimited, restart-level, sequential-levels, save-progress, level-from-txt, sound-effects, +attacked-square-death, +royal-try]
proposes: ["+card:attacked-square-death", "+card:royal-try", "+window:title-screen"]
author: opus
date: 2026-11-19
---

# Mad Queens — Аліса штовхає шахові фігури на дошці 8×8: усе, що стоїть на клітині під боєм, гине; дійди до верхнього ряду живою

## Суть
PuzzleScript-гра Chris Pickel (sfiera), 2020, 11 рівнів. Аліса ходить шахівницею серед червоних фігур, які **ніколи не ходять** — вони лише «бʼють» клітини за шаховими патернами (король, ферзь, тура, слон, кінь, пішак), і ці клітини позначено червоними крапками. Хто стоїть на клітині під боєм — Аліса чи фігура, — гине.

Аліса штовхає фігуру на одну клітину: штовхнута фігура може загинути сама або зі свого нового місця вбити інших. Мета — дійти до верхнього ряду, не ставши під бій.

## Поле і час
- Дошка 8×8 у всіх рівнях; шахове забарвлення малюють пізні правила. Аліса стартує внизу, на d1.
- Шари колізій: фон → тверді (Аліса, фігури) → службові маркери променів → «під боєм» (червона крапка) → «гине» (червоний квадрат).
- Покроково: хід = крок Аліси; прапорець `require_player_movement` скасовує хід, якщо Аліса не зрушила, `noaction` вимикає дію.
- Після руху пізні правила наново рахують клітини під боєм; загибель — у повторному проході `again` (0.1 с): спершу червоний спалах, потім зникнення.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аліса | player | — | крок у 4 напрямки; штовхає фігуру на 1; гине на клітині під боєм; перемагає у верхньому ряду |
| Пішак | piece | — | бʼє дві клітини по діагоналі **вгору** |
| Кінь | piece | — | бʼє 8 клітин ходом коня |
| Король | piece | — | бʼє 8 сусідніх клітин |
| Тура | piece | — | бʼє рядок і стовпець до краю дошки |
| Слон | piece | — | бʼє обидві діагоналі до краю дошки |
| Ферзь | piece | — | тура + слон |
| Загроза (`Threatened`) | mark | — | червона крапка на кожній клітині під боєм; перераховується щоходу |
| Загибель (`Dying`) | mark | — | червоний квадрат на один прохід перед зникненням |
| Клітина дошки | terrain | біла / чорна | лише вигляд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(alice, dir)`.
- КОЛИ `contact(alice, piece)` → ЯКЩО `free(cell_behind_piece)` → ТО `push`, `move(alice, dir)`; інакше `block` і хід скасовано: дві фігури поспіль не штовхаються, край дошки — упор.
- КОЛИ `after(move)` → ТО `mark(attacked_cells, threatened)` — для кожної фігури за її патерном: пішак — дві діагоналі вгору, кінь — 8 стрибків, король — 8 сусідів, тура, слон і ферзь — промені до краю дошки.
- КОЛИ `after(move)` → ЯКЩО `occupied(cell, threatened)` and `occupied(cell, alice|piece)` → ТО `set_state(x, dying)`, `sound(destroy)`.
- КОЛИ `state_on(x, dying)` → ТО `disappear` у наступному проході; загроза від загиблої фігури зникає разом з нею.
- Фігури бʼють і одна одну (сторони нема): штовхнута фігура гине, якщо стала під бій, і вбиває тих, хто опинився під її боєм; дві фігури, що бʼють одна одну, гинуть разом.
- КОЛИ `died(alice)` → ТО `custom: «гравця більше нема — лишаються undo / restart»`.
- КОЛИ `reach(alice, top_row)` → ЯКЩО `not state(alice, dying)` → ТО `win`, `next_level`.
- КОЛИ `level_start` → ТО `mark(attacked_cells, threatened)` — загрози видно ще до першого кроку.
- Перемога: Аліса у верхньому ряду й жива · Поразка: Аліса під боєм гине, далі лише undo / restart · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; дії нема; повтор при утриманні — 0.25 с.
- Z — undo, R — рестарт (стандарт PuzzleScript; у коді є звуки undo і restart).

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (`title-screen`): «Mad Queens», «Chris Pickel»; темно-червоний текст на сірому тлі.
- `game-screen` — дошка 8×8; HUD у самому полі: `threat-range` — червоні крапки на атакованих клітинах, червоний спалах загибелі.
- Повідомлень між рівнями нема; переходи: титул → рівень 0 → … → рівень 10.

## Фічі поза полем
- `levels-sequential` (11 рівнів: порожня дошка → пішаки → коні → тури → слони → ферзь → король), `undo` ∞, `restart-level`, `continue` (стандарт PuzzleScript).
- `sound-effects`: окремі звуки кроку Аліси, руху фігури, загибелі Аліси й фігури, старту, кінця рівня, кінця гри, undo, рестарту.

## Варіації й родичі
- «Аліса в Задзеркаллі» Керрола: Аліса — білий пішак, що на восьмій горизонталі стає королевою; мета «дійти до верхнього ряду» і назва, схоже, звідти.
- [SokoChess](../push-slide/sokochess.md) — Sokoban із шахами: там свої фігури штовхають, а чорні бʼють, коли можуть; тут фігури не ходять зовсім — бʼє саме поле під боєм.
- [N-queens і Knight's tour](../pencil-logic/n-queens-knights-tour.md) — клітини під боєм як обмеження; [Dynamo chess](../chess-abstract/dynamo-chess.md) — шахи, де фігури виштовхують; [Шахи](../chess-abstract/chess.md) — самі патерни; [Dobutsu shogi](../chess-abstract/dobutsu-shogi.md) — перемога «дійти до дальнього ряду не під ударом».
- Осі варіацій: **хто бʼє** — ворог своїм ходом (шахи, SokoChess) / зона бою вбиває будь-кого без ходу (тут); **чим грає гравець** — фігурою / аватаром, що штовхає чужі фігури (тут); **промені** — спиняються на першій фігурі (шахи) / наскрізь до краю (тут, за кодом); **мета** — мат / дійти до ряду живим (тут).

## Цікавинки для курсу
- Клітини під боєм для 6 типів фігур: промені, стрибки коня, діагоналі пішака — 📎 (`piece-move-patterns` як множина клітин).
- Смерть на атакованій клітині для всіх, з фазою «гине» в наступному проході — 🌱.
- Штовхнута фігура як зброя: вбиває зі свого нового місця, взаємне знищення — 📎.
- Підсвітка атакованих клітин червоними крапками — 🌱.
- Перемога «дійти до ряду, не будучи під боєм» — 🌱.
- Розвʼязувач BFS: стан = Аліса + множина фігур на 8×8 — 🥉 (малий простір, зручно перевіряти рівні).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки; `push-object` ↔ Аліса штовхає фігуру; `piece-move-patterns` ↔ загрози 6 фігур; `threat-range` ↔ червоні крапки; `death-animation` ↔ червоний спалах перед зникненням; `player-death` ↔ Аліса під боєм; `reach-exit` ↔ верхній ряд; `undo-unlimited` · `restart-level` · `sequential-levels` · `save-progress` · `level-from-txt` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+attacked-square-death` «Хто стоїть на клітині під боєм — гине» · entities/death · 📎 · слоти {who: all | player | pieces, delay: 1 прохід}.
  - `+royal-try` (Dobutsu shogi) — тут {row: верхній, safe: true}, і перемагає аватар, а не фігура.

## Пропозиції до словників
- `+card:attacked-square-death`, `+card:royal-try` — див. вище.
- `+window:title-screen` — повтор (стандартний титул PuzzleScript).

## Джерела
- ⭐ [PuzzleScript: Mad Queens](https://www.puzzlescript.net/play.html?p=8ba10d6a0a5a0edd640e0b9431858259) — гра в браузері, 11 рівнів.
- [Вихідний код (gist через GitHub API)](https://api.github.com/gists/8ba10d6a0a5a0edd640e0b9431858259) — обʼєкти й шари, правило штовхання, пізні правила загроз для 6 фігур, загибель і перемога `late up [||||||| Alice no Dying] -> win`; 8 ревізій 2020-03-18.
- [GIF з галереї](https://www.puzzlescript.net/Gallery/gifs/8ba10d6a0a5a0edd640e0b9431858259.gif) — рівень з кіньми: червоні крапки на атакованих клітинах, червоні квадрати загибелі.
- [Дані галереї PuzzleScript](https://raw.githubusercontent.com/increpare/PuzzleScript/master/src/games_dat.js) — запис «Mad Queens · Chris Pickel · sfiera.net».
- [Документація PuzzleScript: прелюдія](https://www.puzzlescript.net/Documentation/prelude.html) — що роблять `require_player_movement`, `noaction`, `run_rules_on_level_start`.
- [sfiera.net](https://sfiera.net/) — сайт автора (про гру там нічого).
- YouTube: пошук «Mad Queens puzzlescript».

## Непевне
- (?) Промені тури, слона й ферзя в коді не мають умови зупинки на фігурі, тобто бʼють наскрізь до краю дошки; грою не перевірено.
- (?) Звʼязок із «Задзеркаллям» — тлумачення назви й імені героїні.
- (?) Що гра показує після рівня 10, не перевірено.
- (?) Клавіші Z / R — стандарт PuzzleScript, у коді не задані.
