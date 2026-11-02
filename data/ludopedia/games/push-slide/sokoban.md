---
title: Sokoban (Сокобан)
slug: sokoban
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 1982
platforms: [PC-8801, PC, web, mobile, GB (Boxxle), NES]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sokoban", best: true, note: "правила, історія, складність (NP-hard / PSPACE-complete), солвери"}
  - {kind: official, url: "https://jsokoapplet.sourceforge.io/sokoban/level-format.html", note: "формат рівня XSB/RLE і нотація розвʼязку LURD"}
  - {kind: official, url: "https://jsokoapplet.sourceforge.io/sokoban/deadlocks.html", note: "типи deadlock: dead square, freeze, corral, bipartite"}
  - {kind: official, url: "https://jsokoapplet.sourceforge.io/", note: "JSoko — плеєр з розвʼязувачем, оптимізатором, редактором, базою колекцій"}
  - {kind: play, url: "https://travisarts.github.io/Sokoban/?level=364", note: "HTML5-версія в браузері"}
  - {kind: other, url: "https://au-voleur.itch.io/microban-1", note: "Microban I (David W. Skinner, 155 рівнів) — набір для новачків"}
  - {kind: other, url: "https://sokoenginepy.readthedocs.io/en/stable/tutorial.html", note: "Python-двіжок: варіанти Hexoban/Trioban/Octoban, .sok"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sokoban+gameplay", note: "пошук; геймплей"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=sokoban", note: "пошук; сучасні Sokoban-ігри"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, cell-click, push-object, impassable-cells, all-on-targets, goal-counter, deadlock-detection, unsolvable-states, reachability-check, level-solver, level-from-txt, import-open-formats, level-metadata, level-bank, level-select, in-game-editor, level-exchange, movement-animation, theme-select, replay, +undo-redo, +move-push-counters, +box-path-click, +reverse-mode]
proposes: ["+trigger:input", "+trigger:all_on", "+cond:free", "+cond:occupied", "+effect:move", "+effect:counter", "+effect:pull", "+trigger:deadlock", "+cond:dead_square", "+ui:move-counter", "+ui:push-counter", "+ui:reachable-highlight", "+window:solutions-window", "+feature:undo", "+feature:export-import", "+feature:reverse-mode", "+feature:snapshots", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Sokoban — штовхай ящики на цілі, не загнавши жодного в кут

## Суть
Комірник ходить складом по клітинах і штовхає ящики (лише штовхає, не тягне, лише по одному) на позначені цілі; ящиків рівно стільки, скільки цілей. Ворогів, часу і випадковості нема — уся складність у тому, що необережний поштовх створює **deadlock**: ящик більше ніколи не дійде до цілі, і рівень стає нерозвʼязним. Гра — еталон «чистого» пазла на сітці: правил чотири, а розвʼязання рівнів має сотні поштовхів; задача розвʼязності — NP-hard і PSPACE-complete.

## Поле і час
- Квадратна сітка довільного розміру (типово до ~20×20), обнесена стінами; клітини поза стінами — «зовні», не частина гри.
- Один шар обʼєктів (комірник або ящик) над шаром підлоги (звичайна / ціль). Камера статична, видно все поле (`info: full`).
- Хід = один крок комірника; світ не змінюється без вводу (`time: turn`). Нема таймера, лише лічильники ходів і поштовхів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Комірник (`@`) | player | позиція | рух 4 напрямки; штовхає ящик перед собою |
| Комірник на цілі (`+`) | player | — | той самий комірник, стоїть на клітині-цілі |
| Ящик (`$`) | object | — | зсувається на 1 у напрямку поштовху, якщо за ним вільна підлога |
| Ящик на цілі (`*`) | object | стан on_goal | той самий ящик, зараховується до перемоги; можна зіштовхнути далі |
| Ціль (`.`) | terrain | — | клітина підлоги-мітка; ні на що не впливає, крім умови перемоги |
| Підлога (` ` / `-` / `_`) | terrain | — | прохідна для комірника й ящиків |
| Стіна (`#`) | static | — | непрохідна для всіх |
| Dead square | terrain (неявна) | обчислюється | клітина, з якої ящик ніколи не дійде до цілі (кут без цілі, вздовж стіни без цілі) — у грі не намальована, плеєри можуть підсвічувати |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `counter(moves, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` → ТО `block` (хід не зараховується).
- КОЛИ `contact(player, box)` → ЯКЩО `free(cell_behind_box)` → ТО `push`, `move(player, dir)`, `counter(moves, +1)`, `counter(pushes, +1)`.
- КОЛИ `contact(player, box)` → ЯКЩО `occupied(cell_behind_box, box)` або `cell(cell_behind_box, wall)` → ТО `block` (ланцюга ящиків нема: два ящики підряд не штовхаються).
- Тягнути ящик неможливо: відійти від ящика — звичайний `move`, ящик лишається на місці.
- КОЛИ `enter(box, goal)` → ТО `set_state(box, on_goal)` (`$` → `*`); `leave` → стан знімається.
- КОЛИ `all_on(box, goal)` → ТО `win` (цілей = ящиків, тож це те саме, що «усі цілі зайняті»).
- КОЛИ `custom: «ящик на dead square або заморожений не на цілі»` → ТО нічого в класичній грі (поразки нема); у плеєрах — `custom: «попередження про deadlock»`. Види deadlock: **dead square** (статична клітина), **freeze** (ящик не може зрушити ні по горизонталі, ні по вертикалі, бо сусідні ящики/стіни теж заморожені), **corral** (область, недосяжна комірнику, з якої не виштовхати ящик), **bipartite** (кожен ящик окремо досягає цілі, а всі разом — ні).
- Перемога: усі ящики на цілях. · Поразка: формально нема — гравець робить undo або рестарт. · Рахунок: кількість ходів (moves) і поштовхів (pushes); «оптимальний» розвʼязок рахують або за ходами (вторинно — поштовхи), або за поштовхами (вторинно — ходи).

## Керування і ввід
- Стрілки — крок/поштовх. Undo (зазвичай Z/Backspace) — без обмежень; redo; restart рівня.
- Миша (цифрові плеєри): клік по досяжній клітині — комірник іде туди найкоротшим шляхом без поштовхів; клік по ящику, потім по клітині — плеєр сам будує серію поштовхів (box path), якщо вона існує (?).
- Розвʼязок записується **LURD**-нотацією: `u d l r` — кроки, великі `U D L R` — кроки з поштовхом (`DDrdrruLruLLDllU`); з неї працюють replay, експорт і перевірка рекордів.

## Вікна, меню, HUD
- `game-screen`: поле; HUD — `level-number` / назва рівня й колекції, `move-counter`, `push-counter`, `par-moves` (найкращий відомий розвʼязок), `undo-button`, `restart-button`.
- `level-select` / `puzzle-select`: список колекції (Original 50, Microban 155…) з позначкою «розвʼязано» і найкращими moves/pushes.
- `end-screen`: «рівень розвʼязано» з ходами/поштовхами, порівняння з рекордом, перехід далі.
- `editor-window` (JSoko, YASC): палітра `#`, `@`, `$`, `.`, перевірка «ящиків = цілей», плейтест.
- `hints-window` / solver (цифрова версія): запуск розвʼязувача, оптимізатора розвʼязку, перегляд знайденого як replay.
- `solutions-window` (?): збережені розвʼязки рівня з moves/pushes — `custom-window`.
- `settings-window`: скін (тема спрайтів), швидкість анімації, звук; `main-menu`: Грати → `level-select`; Колекції/Імпорт; Редактор; Налаштування.
- Переходи: main-menu → level-select → game-screen → (усі на цілях) end-screen → наступний рівень.

## Фічі поза полем
- `undo` ∞ + `redo` + `restart-level`: фактично замінюють «поразку»; деякі плеєри мають snapshots — іменовані точки стану (?).
- `export-import`: рівні у **XSB** (символи `# @ + $ * . ` пробіл/`-`/`_`) і **RLE** (`3#|#.3#|#*$-#|#--@#|5#`: цифра — повтор, `|` — новий рядок, хвостові порожні не пишуться); колекції — багато рівнів в одному txt із назвою/автором (`level-metadata`).
- `level-solver` (Rolling Stone, Festival/FESS, JSoko), оптимізатор розвʼязків, `deadlock-detection` з підсвіткою dead squares.
- `level-bank`/`puzzle-bank` з колекціями авторів (Microban I — 155 рівнів, 2000; Microban II–IV), `stats` найкращих moves/pushes, `replay` з LURD.
- `level-editor`, `level-sharing` (копіювати рівень у буфер як XSB).
- Reverse mode (Sokoban YASC, sokoban-elements): гравець стартує з розвʼязаного стану й **тягне** ящики назад до старту; знайдений шлях розвертається в прямий розвʼязок.

## Варіації й родичі
- Оригінал Thinking Rabbit (Hiroyuki Imabayashi, PC-8801, 1982): 20 рівнів; з 11-го деякі стіни можна ламати; продовження — Sokoban Extra (1983), Sokoban 2 (1984, +50).
- Клони й порти: Boxxle (GB), Shove It!, Boxyboy, XSokoban (90 рівнів — тестовий набір солверів), KSokoban/Skladnik.
- Осі варіацій:
  - **сила**: лише штовхати (класика) / штовхати й тягнути (Pukoban) / лише тягнути (reverse mode);
  - **ланцюг**: 1 ящик / ланцюг ящиків (Helltaker, багато thinky-ігор);
  - **поле**: квадрат / гекс (Hexoban, 6 напрямків) / трикутники (Trioban) / октагони+квадрати (Octoban);
  - **кількість штовхачів**: один / кілька по черзі (Multiban) / двоє кооперативно;
  - **тип обʼєкта**: однакові ящики / кольорові на свої цілі / ящики з орієнтацією (Pipe Push Paradise) / злипання (Sokobond) / гравітація (→ `thinky`);
  - **ціль**: усі на цілях / дійти до виходу / замкнути контур (Ultimate Sokoban: «електричне коло»).
- Родичі: Adventures of Lolo (блоки + вороги), Chip's Challenge (блоки у воду), Kwirk, Pushmo, Baba Is You (штовхання слів-правил).

## Цікавинки для курсу
- Базове штовхання з перевіркою «за ящиком вільно» і заборона ланцюга — 🌱 (одна функція руху).
- Undo/redo на стеку станів або ходів (LURD — мінімальний журнал: великий літера = поштовх, тож undo знає, чи тягнути ящик назад) — 📎.
- Парсер XSB + RLE з валідацією (ящиків = цілей, один комірник, рівень замкнений стінами — flood fill від комірника) — 🥉.
- Клік по клітині → BFS-шлях комірника без поштовхів — 🥉; клік «ящик → ціль» з BFS у просторі (ящик, бік комірника) — 🥈.
- Статичні dead squares (BFS «тягнення» від цілей: що не досяжне — мертве) + freeze deadlock — 🥈.
- Повний розвʼязувач (BFS/A* по станах, хеш станів, нормалізація позиції комірника до області досяжності, евристика — мінімальне паросполучення ящиків і цілей) — 🥇; оптимальний за поштовхами на Microban — 👑-рівень на великих рівнях.
- Reverse mode як окремий набір правил двіжка (pull замість push) — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `cell-click` ↔ клік-перехід; `push-object` ↔ поштовх; `impassable-cells` ↔ стіни; `all-on-targets` + `goal-counter` ↔ перемога й лічильник «ящиків на цілях»; `deadlock-detection` + `unsolvable-states` ↔ deadlock; `reachability-check` ↔ досяжна область комірника; `level-solver` ↔ солвери; `level-from-txt` + `import-open-formats` + `level-metadata` ↔ XSB/RLE з назвою й автором; `level-bank` + `level-select` ↔ колекції; `in-game-editor` + `level-exchange` ↔ редактор і обмін; `replay` ↔ програвання LURD; `movement-animation` ↔ анімація кроку; `theme-select` ↔ скіни.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo/redo ходів у грі» · game-logic/flow · 📎 · слот {depth: 1|N|∞} — у каталозі лише `editor-undo` для редактора.
  - `+move-push-counters` «Лічильники ходів і поштовхів» · game-logic/score · 🌱 — дві метрики оптимальності.
  - `+box-path-click` «Ящик до клітини одним кліком» · interface/input · 🥈 — пошук серії поштовхів.
  - `+reverse-mode` «Зворотний режим: тягнення від розвʼязку» · entities/legality · 📎.
  - `+pull-object` «Тягнення» · entities/legality · 📎 · слот {mode: push|pull|both} — Pukoban, reverse mode.

## Пропозиції до словників
- `+trigger:input` — ввід напрямку (основний тригер усіх покрокових ігор); `+trigger:all_on` — усі ящики на цілях.
- `+cond:free` — клітина за ящиком вільна; `+cond:occupied` — у клітині інший ящик (заборона ланцюга).
- `+effect:move` — крок комірника; `+effect:counter` — лічильники moves/pushes; `+effect:pull` — reverse mode/Pukoban.
- `+trigger:deadlock` — стан став нерозвʼязним (відмінно від `no_moves`: ходи є, розвʼязку нема); `+cond:dead_square` — клітина статично мертва для ящика.
- `+ui:move-counter`, `+ui:push-counter` — дві окремі метрики; `+ui:reachable-highlight` — підсвітка області, досяжної комірнику без поштовхів.
- `+window:solutions-window` — список збережених розвʼязків рівня з метриками.
- `+feature:undo`, `+feature:export-import` (XSB/RLE/LURD), `+feature:reverse-mode`, `+feature:snapshots` — іменовані точки стану для повернення.
- `+axis:undo` — тут `unlimited`, і це змінює природу гри: поразки нема, є лише «глухий кут».

## Джерела
- ⭐ [Wikipedia: Sokoban](https://en.wikipedia.org/wiki/Sokoban) — правила, оригінал і версії, deadlock, складність, солвери Rolling Stone і Festival.
- [JSoko: Level format](https://jsokoapplet.sourceforge.io/sokoban/level-format.html) — символи XSB, RLE з `|`, нотація розвʼязку `udlr`/`UDLR`.
- [JSoko: Deadlocks](https://jsokoapplet.sourceforge.io/sokoban/deadlocks.html) — dead square, freeze, corral, bipartite з картинками.
- [JSoko](https://jsokoapplet.sourceforge.io/) — плеєр із солвером, оптимізатором, редактором і базою колекцій.
- [Microban I на itch.io](https://au-voleur.itch.io/microban-1) — 155 рівнів Skinner-а для новачків.
- [sokoenginepy](https://sokoenginepy.readthedocs.io/en/stable/tutorial.html) — Python-двіжок з варіантами Hexoban/Trioban/Octoban.
- [HTML5 Sokoban](https://travisarts.github.io/Sokoban/?level=364) — грати в браузері.
- YouTube: пошук «sokoban gameplay».

## Непевне
- (?) Box-path-клік і snapshots — є в Sokoban YASC/JSoko за памʼяттю, сторінки функцій не перевірені.
- (?) Точний перелік фіч оригіналу 1982 (меню, вибір рівня, наявність undo) — не знайдено першоджерела; описано типовий сучасний плеєр.
- (?) Офіційний сайт Thinking Rabbit/sokoban.jp не відкрився в пошуку — замість нього довідка JSoko.
