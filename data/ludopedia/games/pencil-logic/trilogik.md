---
title: Trilogik (Trilogic, Trilogy)
slug: trilogik
aka: [Trilogic, Trilogy]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Trilogik/index.htm", best: true, note: "Janko: 2 правила DE/EN, Lexikon (автор невідомий, можливо з конкурсу), 70 пазлів 4×4…14×14, складність 1–8"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Trilogik/001.a.htm", note: "аплет Janko, пазл №1 (Alberto Fabris, Amico Logico Nr. 7, 2014)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Trilogik/Bedienung.htm", note: "ввід: клік циклить символи; клавіші D/T, K/C, Q/S, A/B/C, 1/2/3; вигляд фігури / ABC / 123; F7, F6, F4"}
  - {kind: other, url: "https://puzzlegenius.org/trilogy/", note: "Puzzle Genius «Trilogy»: ті самі 2 правила, техніки AxCC, ABxB і перетини; книга на 120 пазлів, 7 рівнів"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Bedienung.htm", note: "загальна інструкція аплетів Janko: undo/redo, підказка F3, збереження, час"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=trilogic+puzzle+triangle+circle+square", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, pencil-marks, conflict-highlight, theme-select, undo-redo, level-solver, unique-puzzle-generation, difficulty-rating, level-bank, level-rating, puzzle-select, save-multi-slot, help-window, +diagonal-run-check, +anti-set-triple, +hint-reveal, +trial-mode, +solution-path-replay]
proposes: ["+card:anti-set-triple", "+feature:view-toggle"]
author: opus
date: 2026-11-19
---

# Trilogik — заповни сітку трикутниками, колами й квадратами: жодна трійка поспіль не однакова й не вся різна

## Суть
Квадратна сітка, частина клітинок уже має символ — трикутник, коло або квадрат. Гравець заповнює решту так, щоб будь-які три клітинки поспіль по горизонталі, вертикалі чи діагоналі не були ні всі однакові, ні всі різні — тобто в кожній трійці рівно два різні символи: один удвічі, другий раз. Незвичне: заборона з двох боків — і «трьох однакових» (як у Takuzu), і «трьох різних», а діагоналі рахуються нарівні з лініями.

## Поле і час
- Квадратна сітка; банк Janko — 4×4 (1), 5×5 (1), 6×6 (5), 7×7 (1), 8×8 (17), 10×10 (17), 12×12 (14), 14×14 (14), разом 70.
- Частина клітинок задана; правила кажуть «у кожну порожню білу клітинку» — чи бувають чорні, не бачив (?).
- Перевіряються всі трійки поспіль у 4 напрямках: горизонталь, вертикаль, дві діагоналі; трійки перекриваються.
- Час статичний; хід — поставити, змінити чи стерти символ.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітинка | mark | △ / ○ / □ / порожньо | приймає один символ |
| Задана клітинка | static | символ | незмінна підказка |
| Трійка поспіль | zone | 3 клітинки в ряд, 4 напрямки | рівно два різні символи |
| Кандидати | mark | множина ⊆ {△, ○, □} | нотатка гравця (Janko F7) |
| Кольорова позначка ходу | mark | колір 0–9 | група ходів-гіпотези, приймається чи скидається разом (Janko) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not state(cell, given)` → ТО `custom: «наступний символ по колу: △ → ○ → □ → порожньо»` (Janko: Dreieck | Kreis | Quadrat …, leer).
- КОЛИ `input(key, cell)` → ТО `mark(cell, symbol)`: D або T — △, K або C — ○, Q або S — □; у вигляді ABC — A / B / C, у вигляді 123 — 1 / 2 / 3.
- КОЛИ `input(delete, cell)` → ТО `unmark(cell)` (клавіші `-`, `/`, Delete, Backspace).
- КОЛИ `input(view_toggle)` → ЯКЩО `custom: «на полі ще нічого не змінено»` → ТО `custom: «вигляд символів: фігури / ABC / 123»` (`+feature:view-toggle`).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(a, b, c, symbol)` → ТО `custom: «конфлікт: три однакові поспіль»` (рядок, стовпець, обидві діагоналі).
- КОЛИ `pattern(line(3))` → ЯКЩО `unique(triple)` → ТО `custom: «конфлікт: три різні поспіль»`.
- КОЛИ `input(check)` → ТО `custom: «усі порушення — червоним»` (Janko F6).
- КОЛИ `input(hint, cell)` → ЯКЩО `mode(hint)` → ТО `reveal(cell)` (Janko F3).
- КОЛИ `input(solve)` → ТО `custom: «вписати розвʼязок і, якщо є, шлях розвʼязання у список ходів»` (Janko F4).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «зелена рамка навколо діаграми»`.
- Наслідок: у кожній трійці рівно два різні символи; якщо двоє сусідів однакові — третій інший, якщо різні — третій повторює одного з них.
- Наслідок «mod 3»: символи як 0, 1, 2 → «усі однакові або всі різні» рівносильне a + b + c ≡ 0 (mod 3); отже правило — «сума кожної трійки не ділиться на 3» (той самий факт, що в картковій грі SET).
- Дедукції: `A A x` → x ≠ A · `A B x` → x ∈ {A, B} · `A x A` → x ≠ A · `A x C` → x ∈ {A, C}.
- Дедукції Puzzle Genius: `A x C C` → x = A · `A B x B` → x = A; на перетині двох ліній: AAx + BBx → C · AAx + ABx → B · ACx + BAx → A · AxA + ABx → B · AxC + ABx → A.
- Перемога: усі порожні клітинки заповнені, жодна трійка не порушує правила. Поразки й рахунку нема.

## Керування і ввід
- Janko, миша й тач: лівий клік / тап — наступний символ по колу, далі порожньо.
- Janko, клавіатура: стрілки — рамка вибору; Enter / Space / Insert — цикл; D/T, K/C, Q/S — прямо символ; A/B/C і 1/2/3 — у відповідних виглядах; `-`, `/`, Delete, Backspace — стерти.
- Значок режиму — вигляд символів (фігури / ABC / 123); перемикається лише до першої зміни поля.
- F7 — кандидати; Alt+0…9 — колір наступних ходів; правий клік — попап кольору; F6 — перевірка; F4 — розвʼязок; undo/redo — PgUp / PgDn.
- Папір (Puzzle Genius): малювати фігури, на складних — нотатки.

## Вікна, меню, HUD
- `game-screen` (Janko): сітка з фігурами, рамка вибору, `pencil-marks`, `conflict-highlight` (червоне за F6), зелена рамка при розвʼязку; панель значків: режим вигляду, кандидати, перевірка, підказка, розвʼязок, undo/redo, збереження, info.
- `help-window`: на сторінці пазла згортні «Regeln», «Bedienungsanleitung», «Quelle und Copyright».
- `save-slots` (Ctrl+S / Ctrl+L): серверний слот на 10 днів і 8 локальних.
- `custom-window` info (F1): час брутто й нетто.
- `puzzle-select` (сторінка жанру): 70 пазлів, сортування за датою / розміром / складністю 1–8; кольором — пазли з відтворюваним логічним шляхом.
- Переходи: сторінка жанру → пазл NNN → F6 / зелена рамка → «Weiter».

## Фічі поза полем
- `undo` / `redo`, `hint` (F3), `show-solution` зі шляхом розвʼязання (F4), `auto-check` за кнопкою (F6), кольорові групи ходів (F8 прийняти / F9 стерти).
- `theme-select`-подібний перемикач вигляду: той самий стан — фігурами, літерами чи цифрами (`+feature:view-toggle`).
- `puzzle-bank` з рейтингом за часом розвʼязування, незалежно від розміру; `save-slots`; друк.
- Puzzle Genius — книги «Trilogy», зокрема збірка на 120 пазлів у 7 рівнях складності.

## Варіації й родичі
- [Takuzu](takuzu.md) — два символи, заборона трьох однакових поспіль лише в рядках і стовпцях, плюс баланс.
- [Nondango](nondango.md) — три однакові поспіль заборонені навіть по діагоналі (картка `+diagonal-run-check` звідти).
- [Tawamurenga](tawamurenga.md), [No Three](no-three.md) — інші заборони трійок у ряду.
- [Easy as ABC](easy-as-abc.md) — теж літери-символи, але латинське правило.
- Карткова гра SET: «сет» — трійка, де ознака або вся однакова, або вся різна; Trilogik забороняє якраз «сети» з однією ознакою.
- **Осі варіацій**: кількість символів (2 — Takuzu / 3 — Trilogik) · що заборонено в трійці (лише однакові / однакові й різні) · напрямки (рядок і стовпець / + діагоналі) · баланс кількостей (є / нема).

## Цікавинки для курсу
- Ковзне вікно 3 у 4 напрямках з перевіркою «рівно два різні символи» — 🌱.
- Та сама перевірка через суму mod 3 — 🌱 за кодом, але гарний «ага»-момент і місток до SET.
- Розвʼязувач пропагацією шаблонів (AAx, ABx, AxA, AxC і перетини) до нерухомої точки — 🥉.
- Повний розвʼязувач з доведенням єдиності: пропагація + бектрекінг по трьох значеннях — 🥈.
- Генератор з єдиним розвʼязком і мінімумом заданих — 👑 (`unique-puzzle-generation`).
- Перемикач вигляду символів (фігури / ABC / 123) без зміни стану — 🌱, приклад відділення логіки від рендера.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `pencil-marks` · `conflict-highlight` · `theme-select` ↔ фігури / ABC / 123 · `undo-redo` · `level-solver` · `unique-puzzle-generation` · `difficulty-rating` · `level-bank`, `level-rating`, `puzzle-select` ↔ банк Janko · `save-multi-slot` · `help-window`.
- Перевикористано: `+diagonal-run-check` (Nondango) — слот {n: 3, dirs: 8} ↔ «не всі однакові» · `+hint-reveal` ↔ F3 · `+trial-mode` ↔ кольорові групи · `+solution-path-replay` (Tenner Grid, ця пачка) ↔ F4.
- **Нема** → пропозиції карток:
  - `+anti-set-triple` «Трійка поспіль — ні всі однакові, ні всі різні» · game-logic/constraints · 🌱 · слот {symbols: 3, dirs: 4|8}.

## Пропозиції до словників
- `+card:anti-set-triple` — заборона «сету» в кожній трійці поспіль (Trilogik, Puzzle Genius Trilogy).
- `+feature:view-toggle` — той самий стан у кількох виглядах символів (повтор з Kwirk, 4D, The Brainies).

## Джерела
- ⭐ [Janko: Trilogik](https://www.janko.at/Raetsel/Trilogik/index.htm) — 2 правила DE/EN, автор і першоджерело невідомі (можливо, конкурс), 70 пазлів з розмірами, складність 1–8.
- [Janko: пазл №1](https://www.janko.at/Raetsel/Trilogik/001.a.htm) і №2 — Alberto Fabris, Amico Logico Nr. 7, 2014.
- [Janko: керування Trilogik](https://www.janko.at/Raetsel/Trilogik/Bedienung.htm) — цикл кліком, клавіші символів, три вигляди, кандидати, F6, F4, зелена рамка.
- [Janko: загальна інструкція](https://www.janko.at/Raetsel/Bedienung.htm) — undo/redo, F3, збереження, кольори, час.
- [Puzzle Genius: Trilogy](https://puzzlegenius.org/trilogy/) — ті самі правила з діагоналями, техніки й таблиця перетинів, розібраний приклад, книга на 120 пазлів.
- YouTube: [пошук](https://www.youtube.com/results?search_query=trilogic+puzzle+triangle+circle+square).

## Непевне
- (?) Чорні клітинки: формулювання «порожня біла клітинка» на них натякає, але пазлів зсередини аплета не бачив.
- (?) Порядок циклу кліком записаний в інструкції коротко («Dreieck | Kreis | Quadrat | ABC | 123, leer») — трактую як три символи поточного вигляду, потім порожньо.
- (?) Автор жанру й рік: Janko не знає; найраніша бачена публікація — пазли Alberto Fabris в Amico Logico Nr. 7 (2014), рік у шапці лишаю порожнім.
- (?) Чи «Trilogy» Puzzle Genius — та сама гра під британською назвою чи незалежний винахід — правила збігаються, походження сторінка не називає.
