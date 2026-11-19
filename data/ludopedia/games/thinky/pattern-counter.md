---
title: Pattern Counter
slug: pattern-counter
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
year: 2026
platforms: [web, Windows]
links:
  - {kind: itch, url: "https://pulleybun.itch.io/pattern-counter-jam", best: true, note: "грати в браузері; нашийник із числом, керування Z/Y/R/Backspace, секрет Shift+↓; GMTK Game Jam 2026, тема «COUNT DOWN»"}
  - {kind: other, url: "https://itch.io/jam/gmtk-jam-2026/rate/4815536", note: "сторінка джему: «COUNT: Pattern is counted. DOWN: You die when it reaches 0!»; Enjoyment #251, Creativity #519 (139 оцінок)"}
  - {kind: other, url: "https://html-classic.itch.zone/html/18541627/html5game/PatternCounter.js", note: "код HTML5-збірки (GameMaker): підрахунок зразка 2×2, перемога, 14 назв рівнів, прихований тестер рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pattern+Counter+GMTK+2026", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, player-death, death-animation, undo-redo, undo-unlimited, redo, restart-level, sequential-levels, level-select, highlights, status-panel, particles, sound-effects, background-music, in-game-editor, editor-palette, editor-erase, editor-playtest, level-from-txt, +push-chain, +shape-pattern-match, +pattern-count-life, +pattern-frame, +undoable-restart, +reactive-portrait]
proposes: ["+effect:count_pattern", "+ui:pattern-preview", "+ui:reactive-portrait", "+card:pattern-count-life", "+card:pattern-frame", "+card:undoable-restart"]
author: opus
date: 2026-11-19
---

# Pattern Counter — Sokoban із нашийником: число на ньому — скільки разів на полі повторюється зразок 2×2, і нуль убиває

## Суть
Лис (у коді `obj_fox`) із нашийником штовхає ящики на цілі, як у Sokoban, але нашийник показує лічильник: скільки разів вміст рамки-зразка 2×2 (стіни, ящики, порожнеча) повторюється деінде на полі. Лічильник перераховується після кожного ходу; дійшов до 0 — смерть (GAME OVER, лишаються undo й рестарт). Сам зразок — звичайні клітини поля в рамці, тож ящик, заштовхнутий у рамку чи виштовхнутий з неї, змінює, що саме рахується. Гра з GMTK Game Jam 2026 (тема «COUNT DOWN»); натхнення — [Baba Is You](baba-is-you.md) і [Maxwell's puzzling demon](../push-slide/maxwells-puzzling-demon.md).

## Поле і час
- Квадратна сітка клітин 32 px; рівень — кімната GameMaker, яку гра зводить до карти: стіни, ящики, лис, цілі й одна рамка-зразок 2×2. Межі рівня й камера — за маркерами кутів кімнати.
- У клітини три незалежні шари: обʼєкт (стіна / лис / ящик), позначка «зразок», позначка «ціль».
- Хід = крок лиса (можливо з поштовхом ряду ящиків), після нього — перерахунок лічильника й перевірка перемоги. Часу нема (`time: turn`); утримана клавіша — автоповтор.
- Тестові рівні в коді — текстові карти на 13 символів: `.` порожньо · `#` стіна · `P` лис · `*` ящик · `O` ціль · `!` зразок, а `%` `$` `~` `&` `>` `@` `B` — комбінації обʼєкта з позначками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лис | player | нашийник із лічильником | рух 4 напрямки, штовхає ряд ящиків будь-якої довжини |
| Ящик | object | — | зсувається, якщо ряд перед ним доходить до порожньої клітини, а не до стіни |
| Стіна | static | — | нерухома, непрохідна; у зразку — окреме значення |
| Ціль | zone | — | перемога, коли на всіх цілях стоять ящики |
| Рамка-зразок | zone | 2×2; вміст: стіна / ящик / порожньо | задає візерунок, який рахується; змінюється разом із полем |
| Збіг зразка | mark | — | вікно 2×2 поза рамкою з тим самим вмістом; підсвічується |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(fox, dir)`.
- КОЛИ `contact(fox, box)` → ЯКЩО `custom: «ряд ящиків від лиса доходить до порожньої клітини, а не до стіни»` → ТО `push(box)` усього ряду, `move(fox, dir)`; інакше `block`.
- КОЛИ `turn_end(fox)` → ТО `set_value(collar, matches)`, `custom: «matches — кількість вікон 2×2 поза рамкою, чий вміст клітина-в-клітину збігається з рамкою; стіна, ящик і порожньо різні, лис рахується як порожньо»`.
- КОЛИ `turn_end(fox)` → ТО `mark(match_windows, highlight)` — збіги підсвічено на полі.
- КОЛИ `enter(box, pattern_frame)` або `leave(box, pattern_frame)` → ТО `custom: «зразок стає іншим — з цього ходу рахується новий візерунок»`.
- КОЛИ `counter(collar, <=, 0)` → ТО `lose`, `animate(shock)`, `custom: «ходи блоковано; лишаються Z і R»`.
- КОЛИ `counter(collar, ==, 1)` → ТО `set_state(portrait, worried)`.
- КОЛИ `all_on(box, target)` → ЯКЩО `counter(collar, >, 0)` → ТО `win`, `set_state(portrait, happy)`, `custom: «рівень у списку пройдених»`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(redo)` → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(reset)` → ТО `restart`, `custom: «рестарт іде в історію — Z його скасовує»`.
- КОЛИ `counter(collar, <=, 0)` → ЯКЩО `level(==, 14)` → ТО `custom: «фінальний рівень End: нуль зараховує рівень, ввід вимикається, музика згасає»`.
- Перемога: усі цілі під ящиками при лічильнику > 0. · Поразка: лічильник 0 після ходу (крім фіналу). · Рахунку нема.

## Керування і ввід
- Стрілки або WASD — крок (утримання — автоповтор); Z — undo (утримання — прискорений повтор); Y — redo; R — рестарт (скасовний); Backspace або Esc — вихід до вибору рівнів.
- Меню: стрілки — навігація, Enter — вибір; Shift+↓ у меню — «заблокована сторінка» (секрет з опису).
- Прихований тестер рівнів (`obj_tester` у коді): 1 — стіна, 2 — лис (один), 3 — ящик, 4 — зразок (перемикач), 5 — ціль (перемикач), 6/7 — ширина/висота колесом; ЛКМ ставить, ПКМ прибирає; Enter — грати, Backspace — назад у редагування; P — наступний тестовий рівень; копіювання тексту рівня у вебі — «Not supported in web, sorry!».

## Вікна, меню, HUD
- `splash-screen`: «Pattern Counter», «Press Any Key to Start»; кредити (PulleyBun & BOMI, музика Abstraction, «Heavily inspired by <Baba Is You> and <Maxwell's puzzling demon>», «For GMTK Game Jam 2026»).
- `level-select` зі сторінками (вгору/вниз): «Use Arrow keys to navigate», «Press Enter to select»; 14 рівнів — 1. Old Friend · 2. Pattern Counter · 3. Three · 4. Three Again · 5. Little Heart · 6. COUNT DOWN · 7. Degree of Freedom · 8. Break · 9. Fill · 10. Blocked · 11. Not Enough · 12. Fill Again · 13. Consume · 14. End.
- `game-screen`: поле + `status-panel`: портрет лиса (4 стани: спокій / тривога при 1 / смерть при 0 / радість), лічильник на нашийнику (показ 0…6), превʼю зразка 2×2, підсвітка збігів; тексти-підказки в рівнях: «Arrow keys: Move», «Z: Undo, R: Reset», «Backspace: Exit», «Count: Number of the Pattern», «Don't reach 0».
- `end-screen`: смерть — «GAME OVER / Z: Undo / R: Reset» і «шок» лиса; перемога — конфеті; фінал — «Wait, it's not possible...», «...What now...?», «Thank you for playing!!», «100% Complete!!».
- `editor-window` (прихований тестер): палітра 1–7, рядок «Pattern count: N», «You cleared the stage!» / «Game Over!».
- Переходи: титул → вибір рівня → рівень → (перемога) далі → … → «14. End» → подяка.

## Фічі поза полем
- `undo` без ліміту + `redo` + `restart-level`; рестарт теж запис історії («you can undo this too!»).
- `level-select` зі сторінками й позначками пройдених; секретна сторінка (Shift+↓).
- CRT-шейдер, шрифт dalmoori, музика Abstraction, звуки sfxr.
- Прихований тестер-редактор із текстовим форматом рівня (за кодом збірки).

## Варіації й родичі
- Відома лише джем-версія (сторінка `pattern-counter-jam`, HTML5 + Windows).
- Родичі: [Maxwell's puzzling demon](../push-slide/maxwells-puzzling-demon.md) — пряме натхнення: стан поля як загроза героєві; [Baba Is You](baba-is-you.md) — правило задане обʼєктами на полі; [Sokoban](../push-slide/sokoban.md) — ядро «ящики на цілі».
- **Осі варіацій**: що рахує лічильник смерті — ходи (`move-limit`) / копії зразка на полі (Pattern Counter) · зразок — сталий / сам частина поля, що змінюється поштовхами · поштовх — один ящик / ряд будь-якої довжини · нуль лічильника — поразка / фінал гри (рівень «End»).

## Цікавинки для курсу
- Підрахунок входжень шаблону 2×2 ковзним вікном після кожного ходу — 📎 (два цикли + порівняння 4 клітин).
- Зразок як частина поля: рамку можна «переписати» ящиком — 🥉 (правило гри як дані на полі).
- Лічильник-життя: поразка на 0 і блокування ходів — 🌱.
- Ланцюгове штовхання ряду ящиків будь-якої довжини — 📎.
- Undo/redo, де рестарт — теж крок історії — 📎.
- Розвʼязувач BFS «лис + ящики» з відсіканням станів із лічильником 0 — 🥈.
- Редактор рівня з палітрою на клавішах і текстовим форматом «обʼєкт × позначки» — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ стрілки/WASD; `push-object` ↔ ящики; `impassable-cells` ↔ стіни; `all-on-targets` ↔ ящики на цілях; `player-death` + `death-animation` ↔ нуль лічильника, «шок» лиса; `undo-redo` · `undo-unlimited` · `redo` · `restart-level`; `sequential-levels` · `level-select`; `highlights` ↔ підсвітка збігів; `status-panel` ↔ портрет і нашийник; `particles` ↔ конфеті й розліт збігів; `sound-effects` · `background-music`; `in-game-editor` · `editor-palette` · `editor-erase` · `editor-playtest` · `level-from-txt` ↔ прихований тестер і текстові рівні.
- **Нема** → пропозиції карток:
  - `+pattern-count-life` «Лічильник = кількість копій зразка на полі, 0 — смерть» · game-logic/lose · 🥉 · слот {size: 2×2}.
  - `+pattern-frame` «Зразок задано вмістом рамки на полі; його міняють тими самими поштовхами» · game-logic/constraints · 🥉.
  - `+undoable-restart` «Рестарт як крок історії» · game-logic/history · 🌱.
  - `+reactive-portrait` «Портрет героя реагує на стан гри» · interface/hud · 🌱.
  - `+shape-pattern-match` (уже в корпусі, Tiny Towns) — тут без поворотів, рахуються всі входження; `+push-chain` (уже в корпусі) — ряд ящиків.

## Пропозиції до словників
- `+effect:count_pattern` — перерахувати кількість входжень шаблону на полі й записати в лічильник.
- `+ui:pattern-preview` — зразок 2×2 поруч із лічильником.
- `+ui:reactive-portrait` — портрет героя, що міняє вираз від стану (1 — тривога, 0 — смерть).
- `+card:pattern-count-life`, `+card:pattern-frame`, `+card:undoable-restart` — див. вище.

## Джерела
- ⭐ [itch.io: Pattern Counter](https://pulleybun.itch.io/pattern-counter-jam) — опис (нашийник із числом, «Manage the count»), керування, GameMaker, теги Sokoban; коментарі: рівень 12 і «Not Enough» найважчі.
- [Сторінка GMTK Game Jam 2026](https://itch.io/jam/gmtk-jam-2026/rate/4815536) — відповідь автора на тему («COUNT: Pattern is counted. DOWN: You die when it reaches 0!»), оцінки, відгуки («refreshing countdown», портрет реагує на лічильник).
- [Код HTML5-збірки](https://html-classic.itch.zone/html/18541627/html5game/PatternCounter.js) — функції контролера: рух і поштовх ряду, підрахунок збігів 2×2 (лис = порожньо, рамка не рахується), перемога «усі цілі під ящиками і лічильник > 0», undo/redo/рестарт, назви 14 рівнів, тексти, тестер із палітрою 1–7.
- YouTube: пошук «Pattern Counter GMTK 2026».

## Непевне
- (?) Опис у черзі («нашийник відлічує кроки до смерті; відтворений візерунок блоків рятує») неточний: за кодом лічильник не спадає з кроками, а щоходу перераховується як кількість копій зразка.
- (?) Сюжет фіналу «14. End»: за кодом нуль там зараховує рівень і вимикає ввід, тексти «Wait, it's not possible...», «...What now...?» — без контексту.
- (?) Зміст рівнів (окрім назв) не бачив; що на «заблокованій сторінці» (Shift+↓) і чи доступний гравцеві тестер — не перевірено.
- (?) У коді redo висить і на X, і Shift+B зараховує рівень пройденим — схоже на службові клавіші; в описі їх нема.
- (?) Чи зберігаються пройдені рівні між сесіями.
