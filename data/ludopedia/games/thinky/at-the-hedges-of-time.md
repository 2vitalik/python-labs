---
title: At the Hedges of Time
slug: at-the-hedges-of-time
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://galactical.itch.io/at-the-hedges-of-time", best: true, note: "грати в браузері; опис: сер Монтакле, прокляття відьми, перемотування часу як здібність; 4.8★ (38 оцінок)"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=2fad7fdd93a1a9d6f689024baeb84f5b", note: "запасний запуск на puzzlescript.net (лінк автора з itch)"}
  - {kind: other, url: "https://api.github.com/gists/2fad7fdd93a1a9d6f689024baeb84f5b", note: "вихідний код PuzzleScript (gist, 2021-05-21): обʼєкти, шари, правила перемотування й годинника, мапа з 10 кімнат"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=At+the+Hedges+of+Time+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, key-and-door, reach-exit, move-limit, rewind, undo-step, checkpoint, restart-level, player-camera, sound-effects, +undo-immune-objects, +flip-screen-rooms, +statue-at-zero, +targets-open-doors, +step-stamp-history]
proposes: ["+cond:immune", "+ui:in-world-counter", "+window:message-screen", "+axis:undo", "+card:statue-at-zero", "+card:targets-open-doors", "+card:step-stamp-history"]
author: opus
date: 2026-11-19
---

# At the Hedges of Time — Sokoban у лабіринті живоплоту, де кожна кімната має годинник кроків, а перемотування часу не чіпає фіолетових ящиків

## Суть
Лицар сер Монтакле проклятий відьмою: «one step too many» перетворює його на камінь. Лабіринт — одна мапа з 10 кімнат; у кожній свій годинник кроків, а проходи до сусідніх кімнат відчиняються, коли всі жовті цілі кімнати накриті ящиками. Замість undo — здібність героя «повернути годинник» (space): лицар іде на крок назад, годинник повертає крок, звичайні ящики відкочуються. **Фіолетові часові ящики перемотування не бачать** — їх можна зсунути, перемотатись назад і мати і ящик на новому місці, і кроки в запасі. Мета — вийти крізь золоту браму.

## Поле і час
- Одна мапа PuzzleScript 21×57 (з невидимою рамкою): угорі кімната, далі чотири ряди по дві кімнати, унизу ще одна — 10 кімнат з внутрішнім полем 8×8, між ними 11 проходів. На всій мапі 6 звичайних ящиків, 10 часових, 12 цілей.
- Камера (`zoomscreen 12x11`) показує лише поточну кімнату; при переході в іншу кімнату кадр перескакує.
- Покроково: тік = крок або перемотування. Вбудований undo вимкнено (`noundo`).
- Годинник кожної кімнати — дві цифри в її стіні-живоплоті, старт від 10 до 21 кроків.
- Історія ходів зберігається в самому полі: під лицаря кладеться позначка з номером кроку (q1…q150), зсунутий ящик дістає ту саму позначку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сер Монтакле | player | напрям погляду | крок 4 напрямки; штовхає ящик; space — крок назад у часі |
| Статуя (стан лицаря) | player | годинник кімнати = 00 | рух скасовується; можна лише перемотати або рестарт |
| Ящик | object | позначка кроку | штовхається на 1; перемотування повертає його разом з лицарем |
| Часовий ящик (фіолетовий) | object | без позначок | штовхається на 1; перемотування його не повертає |
| Ціль (жовта) | static | — | має бути накрита ящиком будь-якого виду |
| Живопліт | static | — | непрохідний для лицаря й ящиків |
| Межа кімнати | static | — | стіна між кімнатами; у ній годинник і цифри |
| Прохід | gate | відчинено / зачинено | зачинений, поки в поточній кімнаті є ціль без ящика |
| Годинник кімнати | static | 2 цифри | −1 за крок, +1 за перемотування |
| Золота брама | static | — | крок униз у браму — перемога |
| Позначка історії | mark | номер кроку 1…150 | невидима; за нею лицар іде назад |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(knight, statue)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(knight, dir)`, `counter(room_clock, -1)`, `mark(cell_under_knight, step_n)`.
- КОЛИ `contact(knight, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`, `mark(crate_cell, step_n)`; за ящиком стіна чи ще один ящик → `block`.
- КОЛИ `contact(knight, time_crate)` → ЯКЩО `free(cell_behind)` → ТО `push` (позначки нема); інакше `block`.
- КОЛИ `input(action)` → ЯКЩО `custom: «нема жодної позначки історії»` → ТО `block`.
- КОЛИ `input(action)` → ТО `teleport(knight, previous_mark)`, `counter(room_clock, +1)`, `face(knight, dir)` — лицар дивиться так, як ішов тим кроком.
- КОЛИ `input(action)` → ЯКЩО `custom: «верхня позначка ящика = верхня позначка під лицарем»` → ТО `move(crate, back)` — ящик стає на клітину, з якої лицар перемотується.
- КОЛИ `input(action)` → ТО `custom: «часовий ящик лишається там, куди його зсунули»`.
- КОЛИ `counter(room_clock, ==, 0)` → ТО `set_state(knight, statue)`.
- КОЛИ `input(action)` → ЯКЩО `state(knight, statue)` → ТО `clear_state(knight, statue)` — годинник знову 01.
- КОЛИ `turn_end(knight)` → ЯКЩО `custom: «у поточній кімнаті є ціль без ящика»` → ТО `set_state(room_exits, closed)`; інакше `set_state(room_exits, open)`.
- КОЛИ `enter(knight, exit)` → ТО `custom: «двері не зачиняються, поки лицар стоїть у проході»`.
- КОЛИ `enter(knight, room_entry)` → ЯКЩО `first_time` → ТО `checkpoint`, `camera(room)`.
- КОЛИ `input(restart)` → ТО `restart` до останнього checkpoint.
- КОЛИ `input(down)` → ЯКЩО `cell(cell_ahead, golden_gate)` → ТО `win`, `message(«Thank you for playing!»)`.
- Перемога: вхід у золоту браму · Поразки нема: статуя — стан, з якого виводить перемотування · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок; space / X (action PuzzleScript) — перемотати на крок назад («press space to turn back the clock»).
- R — рестарт до checkpoint, тобто до входу в поточну кімнату; Z не працює (`noundo`).
- Esc — меню PuzzleScript (?).

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript: назва, автор galactical, start / continue (?).
- `custom-window` — екрани-повідомлення: вісім рядків історії перед грою (чотири двовірші, останній — «Press R to restart, and space to turn back the clock»), наприкінці «Thank you for playing!».
- `game-screen` — одна кімната 12×11 клітин; HUD намальований у полі: значок годинника й дві цифри в живоплоті кімнати; спрайт лицаря повернутий за останнім кроком; зачинені проходи видно як двері.
- Переходи: титул → повідомлення → `game-screen` → (брама) → фінальне повідомлення.

## Фічі поза полем
- `rewind` замість `undo`: покроково, до 149 кроків історії (?).
- `restart-level` → до checkpoint на вході в кімнату; `continue` з титулу (стандарт PuzzleScript (?)).
- Один великий рівень замість списку рівнів: `level-select`, підказок і рахунку нема.

## Варіації й родичі
- [Tres Undos](tres-undos.md) — автор називає At the Hedges of Time і Braid джерелами ідей; там імунітет до undo розкладено за рівнями.
- Braid — зелені обʼєкти поза перемотуванням; [Catrap](../grid-platformer/catrap.md) і [Toki Tori](../grid-platformer/toki-tori.md) — перемотування як частина гри.
- [Sokoban](../push-slide/sokoban.md) — база штовхання; [Helltaker](../push-slide/helltaker.md), [XOR](../dig-gravity/xor.md) — ліміт кроків; [Achronal Dungeon](../roguelike/achronal-dungeon.md) — обʼєкти, які undo не бере.
- Осі варіацій:
  - **що переживає перемотування**: нічого (звичайний undo) / окремі обʼєкти (тут фіолетові ящики, у Braid зелені) / рівні імунітету (Tres Undos);
  - **ліміт кроків**: на рівень / на кімнату з поверненням за перемотування (тут) / нема;
  - **що при нулі**: програш (Helltaker) / статуя, з якої виводить лише час назад (тут);
  - **двері**: ключ / кнопка / усі цілі кімнати накриті (тут).

## Цікавинки для курсу
- Історія як позначки з номером кроку на клітинах (не стек станів): ящик бере номер кроку, що його зсунув, і повертається, коли номери збігаються — 🥉 (інша модель undo, ніж копія стану).
- Обʼєкти поза перемотуванням: стан ділиться на «історію» й «поза історією», і після перемотування два ящики можуть опинитись в одній клітині — 🥈 (узгодженість стану).
- Годинник кімнати: −1 за крок, +1 за перемотування, 00 → статуя — 📎.
- Проходи кімнати, відчинені, поки всі її цілі накриті (перерахунок щоходу) — 🌱.
- Мапа з кімнат, камера по кімнатах і checkpoint на першому вході — 📎.
- Розвʼязувач кімнати: BFS, де стан — позиції й історія кроків, бо перемотування з імунними ящиками не є простим ходом назад — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ крок; `push-object` ↔ обидва види ящиків; `impassable-cells` ↔ живопліт; `key-and-door` (сімʼя способів відкриття) ↔ цілі відчиняють проходи; `all-on-targets` не беру — тут це умова дверей, а не перемоги; `reach-exit` ↔ золота брама; `move-limit` ↔ годинник кімнати; `rewind` + `undo-step` ↔ space; `checkpoint` + `restart-level` ↔ R до входу в кімнату; `player-camera` ↔ кадр кімнати; `sound-effects` ↔ крок, перемотування, двері, статуя.
- **Нема** → пропозиції карток:
  - `+undo-immune-objects` (повтор корпусу: Tres Undos, Achronal Dungeon) — фіолетові ящики.
  - `+statue-at-zero` «0 кроків → аватар-статуя, вихід лише перемотуванням» · entities/state · 🌱 — дитина `move-limit`.
  - `+targets-open-doors` «Проходи відчинені, поки всі цілі кімнати накриті» · entities/interact · 🌱 · слот {scope: room|level}.
  - `+step-stamp-history` «Історія як номери кроків на клітинах» · game-logic/history · 🥉.
  - `+flip-screen-rooms` (повтор корпусу) — камера перескакує кімнатами.

## Пропозиції до словників
- `+cond:immune` — обʼєкт поза перемотуванням (повтор Tres Undos).
- `+ui:in-world-counter` — лічильник, намальований у самому полі (годинник у живоплоті кожної кімнати).
- `+window:message-screen` — екран-повідомлення PuzzleScript між подіями (повтор Heroes of Sokoban).
- `+axis:undo` — значення `rewind` з вибірковим імунітетом обʼєктів.
- `+card:statue-at-zero`, `+card:targets-open-doors`, `+card:step-stamp-history` — див. вище.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `enter`, `counter`, `first_time`, `free`, `state`, `cell`, `move`, `face`, `mark`, `set_state`, `clear_state`, `checkpoint`, `camera`, `restart`, `message`; ролі `gate`, `mark`.

## Джерела
- ⭐ [itch: At the Hedges of Time](https://galactical.itch.io/at-the-hedges-of-time) — гра в браузері, опис (лабіринт живоплоту, прокляття, «rewind time», «interconnected puzzles»), лінк на код.
- [Gist через GitHub API](https://api.github.com/gists/2fad7fdd93a1a9d6f689024baeb84f5b) — код: `noundo`, `zoomscreen 12x11`, шари колізій, позначки q1…q150, правила годинника, статуї, дверей і checkpoint, мапа, тексти повідомлень.
- [puzzlescript.net](https://www.puzzlescript.net/play.html?p=2fad7fdd93a1a9d6f689024baeb84f5b) — запасний запуск.
- YouTube: пошук «At the Hedges of Time gameplay».

## Непевне
- (?) Рік 2021 — за датою gist (2021-05-21); дати публікації на itch не видно.
- (?) Чи задумано перемотування назад крізь прохід у попередню кімнату: позначки лишаються на всій мапі, тож код це дозволяє; у грі не перевірено.
- (?) Звичайний і часовий ящики лежать у різних шарах колізій і можуть опинитись в одній клітині (спрайт `FadeCrate`); чи трапляється це в рівнях — не перевірено.
- (?) Межа історії 150 позначок (149 кроків) — з коду; що стається після — не перевірено.
- (?) Чи можна заштовхнути ящик у прохід: прохід не входить у стіни, але в грі не перевірено.
- (?) Esc і continue — стандарт PuzzleScript, у самій грі не перевірено.
