---
title: Hashiwokakero (Hashi, Bridges, Мости)
slug: hashiwokakero
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1990
platforms: [paper, PC, web, mobile]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/bridges.html", best: true, note: "Tatham Bridges: правила, керування мишею/клавіатурою, параметри max мостів і allow loops; поруч — грати"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hashiwokakero", note: "правила, історія Nikoli 1989–1990, техніки, NP-повнота"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/hashiwokakero/", note: "чотири правила від Nikoli"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/bridges.html", note: "грати в браузері (Tatham)"}
  - {kind: play, url: "https://www.puzzle-bridges.com/", note: "грати онлайн з таймером і daily"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hashiwokakero+bridges+puzzle+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, hover-highlight, reachability-check, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, +undo-redo, +edge-marking, +global-connectivity, +bridge-connect, +mark-done, +possible-moves-hint, +seed-share]
proposes: ["+trigger:input", "+trigger:constraint_broken", "+trigger:all_constraints_met", "+effect:mark", "+effect:unmark", "+cond:connected", "+cond:crosses", "+role:mark", "+ui:conflict-highlight", "+ui:possible-moves-overlay", "+feature:auto-check"]
author: opus
date: 2026-11-02
---

# Hashiwokakero — зʼєднай острови мостами: число острова = кількість мостів, усе в одну мережу

## Суть
На сітці розкидані острови з числами 1–8. Гравець проводить між ними горизонтальні й вертикальні мости: між парою островів — не більше двох, мости не перетинаються й не проходять крізь острови, кількість мостів біля острова дорівнює його числу, а всі острови в кінці утворюють одну звʼязну мережу. Це задача на граф: острови — вершини, мости — ребра з кратністю 0–2, плюс планарність і зʼєднаність. Nikoli, 1989–1990; Hashi у The Times, Bridges у Tatham.

## Поле і час
- Прямокутна сітка; клітини або порожні, або острів із числом. Мости живуть «між» островами вздовж рядка/стовпця і займають усі проміжні клітини.
- Справжня структура — **граф можливих зʼєднань**: кожен острів має до 4 сусідів (найближчий острів у кожному напрямку); два потенційні мости, що хрестяться, взаємовиключні.
- Час статичний; хід = додати/прибрати міст або маркер «тут моста нема».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Острів | static | число 1–8 (Tatham: до 16 при max 4 мости) | вимагає рівно N мостів; може бути позначений «завершеним» |
| Міст | mark | кратність 1 або 2 (Tatham: до 1/3/4) | пряма горизонталь/вертикаль між двома островами; не перетинає мости й острови |
| Маркер «не міст» | mark | — | гравець фіксує, що між парою моста не буде (Tatham, правий drag) |
| Мережа (компонента) | zone | — | звʼязна група островів і мостів; у розвʼязку — одна |
| Курсор | — | — | клавіатурний вибір острова (Tatham) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, island_a, dir)` → ЯКЩО `custom: «у напрямку є острів b»` і `not crosses(a–b, existing_bridge)` і `bridges(a,b) < max` → ТО `mark(edge a–b, +1 bridge)`.
- КОЛИ `input(drag, island_a, dir)` → ЯКЩО `bridges(a,b) == max` → ТО `unmark(edge a–b)` (усі мости пари зникають — цикл 0→1→2→0).
- КОЛИ `input(right_drag, a, dir)` → ТО `mark(edge a–b, no_bridge)` toggle.
- КОЛИ `input(click, island)` → ТО `set_state(island, done)` — острів і його мости підсвічені й захищені від випадкових змін; повторний клік знімає.
- КОЛИ `constraint_broken(bridges(island) > n)` → ТО острів червоний.
- КОЛИ `constraint_broken(bridges(island) < n)` → ЯКЩО `custom: «недостачу вже не покрити»` (решта напрямків перекрита мостами чи маркерами) або `state(island, done)` → ТО острів червоний.
- КОЛИ `constraint_broken(connected)` → ЯКЩО `custom: «група замкнена й не може зʼєднатися з рештою»` → ТО вся група червона.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `mode(no_loops)` → ТО петля підсвічується; розвʼязок із петлею не приймається.
- КОЛИ `all_constraints_met` (усі числа виконано, одна компонента, без перетинів) → ТО `win`, `flash(completion)`.
- Перемога: усі острови мають рівно N мостів, мережа звʼязна. Поразки нема. Рахунок нема (онлайн — час).
- Дедукції (для солвера/підказок): острів, у якого сума максимумів по напрямках = числу, — усі мости обовʼязкові (кут з 4, край з 6, центр з 8); «майже повні» (3 у куті ⇒ ≥1 міст у кожен бік); заборона «короткого замикання» — дві 1 не зʼєднуються між собою, дві 2 не зʼєднуються подвійним мостом, якщо є інші острови; міст, що ізолює групу, заборонений.

## Керування і ввід
- Tatham (миша): натиснути на острові й потягнути в бік сусіда — +1 міст (не треба дотягувати до кінця); повтор — другий; на максимумі — прибрати всі; правий drag — маркер «не міст»; лівий клік по острову — «завершено».
- Tatham (клавіатура): стрілки — курсор (до найближчого острова в напрямку); Ctrl+стрілка або Enter, стрілка — міст; Shift+стрілка — маркер; Space або Enter двічі — «завершено»; цифра — стрибок до найближчого острова з цим числом (a–f = 10–15, 0 = 16); G — показати сірим усі ще можливі зʼєднання.
- puzzle-bridges.com: клік/drag між островами (?); тач на мобільних.
- Папір: малюєш лінії, завершені острови обводиш.

## Вікна, меню, HUD
- `game-screen`: поле з островами й мостами; `conflict-highlight` (червоні острови/групи/петлі); підсвітка «завершених» островів; `possible-moves-overlay` (G / налаштування).
- Tatham: меню Game/Type з `params-dialog` (Custom) і `game-id-dialog`; Preferences — «показувати можливі мости» постійно.
- Онлайн (puzzle-bridges.com): `timer-elapsed`, Done, Start Over, розміри × складність, daily/weekly/monthly, Hall of Fame (?).
- Переходи: Type → пресет/Custom → новий пазл; розвʼязано → спалах (Tatham) / end-screen з часом (онлайн).

## Фічі поза полем
- `difficulty-presets` + `custom-difficulty` (Tatham: Width, Height, Difficulty, Allow loops, Max. bridges per direction 1–4, %age of island squares, Expansion factor) — генератор налаштовується гравцем.
- `undo`/`redo` ∞, `auto-solve`, `seed-input`/`share-code` — з оболонки Tatham.
- `auto-check` — лише очевидні помилки (див. правила), не порівняння з відповіддю.
- Онлайн: `daily-puzzle`, `leaderboard-online` (?).

## Варіації й родичі
- Tatham Bridges: **max мостів на пару** 1/2/3/4 (Nikoli — 2) і **allow loops** (вимкнено → розвʼязок має бути деревом, петлі підсвічуються).
- Назви: Bridges, Chopsticks (хибний переклад), Hashi (The Times), Ai-Ki-Ai (Франція, Бенілюкс, Данія).
- Родичі за ідеєю «граф на сітці + зʼєднаність»: Net (Tatham), Nurikabe (звʼязність стін), Flow Free (зʼєднати пари без перетинів), Tracks.
- **Осі варіацій**: кратність ребра (1 / 2 / k) · дозволені петлі (так / ні — дерево) · напрямки (ортогональні / + діагоналі (?)) · вимога зʼєднаності (вся мережа / пари) · поле (сітка / гекс (?)).

## Цікавинки для курсу
- Побудова графа потенційних мостів (найближчий острів у 4 напрямках) і перевірка перетинів горизонталь × вертикаль — 📎.
- Зʼєднаність через BFS/union-find + детектор петель для режиму «без петель» — 🥉.
- Підсвітка «неминучої недостачі» й ізольованих груп (а не просто «не дорівнює») — 🥈.
- Drag із напрямком замість точного попадання + цикл 0→1→2→0 — 📎 (ввід на ребрах графа).
- Позначка «завершено» з блокуванням змін — 🌱.
- Солвер дедукціями (обовʼязкові мости, заборона короткого замикання) + бектрекінг; генератор із параметрами щільності й expansion — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `hover-highlight` · `reachability-check` (звʼязність мережі) · `unique-puzzle-generation` · `difficulty-levels` · `difficulty-rating` · `level-solver` · `field-size-picker` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+undo-redo` (уже є в корпусі).
  - `+edge-marking` (є в slitherlink) — лінія / хрестик між вузлами.
  - `+global-connectivity` (пропоновано в tatham-collection; у nurikabe — `+cond:connected`) — уся мережа в одній компоненті.
  - `+bridge-connect` «Мости між вузлами: кратність ≤ k, без перетинів» · entities/legality · 🥉 · слот {max: 1|2|3|4, loops: bool}.
  - `+mark-done` «Позначити елемент завершеним (захист від змін)» · interface/input · 🌱.
  - `+possible-moves-hint` «Показати ще можливі ходи/зʼєднання» · interface/hud · 📎 (родич `legal-move-highlight`).
  - `+seed-share` (пропоновано).

## Пропозиції до словників
- `+trigger:input`, `+trigger:constraint_broken`, `+trigger:all_constraints_met` — ядро пазла.
- `+effect:mark` / `+effect:unmark` — на ребрі графа (міст, маркер), не лише на клітині.
- `+cond:connected(set)` — усі елементи множини в одній компоненті (Hashi, Nurikabe, Net); `+cond:crosses(edge, edge)` — відрізки перетинаються.
- `+role:mark` — міст, маркер.
- `+ui:conflict-highlight`; `+ui:possible-moves-overlay` — сірі лінії можливих зʼєднань (Tatham G).
- `+feature:auto-check`.

## Джерела
- ⭐ [Tatham: Bridges](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/bridges.html) — правила, повне керування, підсвітки помилок, усі Custom-параметри; [грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/bridges.html).
- [Wikipedia: Hashiwokakero](https://en.wikipedia.org/wiki/Hashiwokakero) — правила, Puzzle Communication Nikoli #28 (12.1989) і #31 (09.1990), техніки, NP-повнота (Andersson 2009), ILP.
- [Nikoli: Hashiwokakero](https://www.nikoli.co.jp/en/puzzles/hashiwokakero/) — чотири правила видавця.
- [puzzle-bridges.com](https://www.puzzle-bridges.com/) — онлайн-версія з розмірами й daily.
- YouTube: [пошук «hashiwokakero bridges puzzle solve»](https://www.youtube.com/results?search_query=hashiwokakero+bridges+puzzle+solve).

## Непевне
- (?) Керування й фічі puzzle-bridges.com (drag, Hall of Fame) — сторінку не відкривав, бачив лише лінк на сусідньому сайті.
- (?) Варіанти з діагональними мостами чи на гексах — не перевіряв.
- (?) Рік 1990 — повна форма (#31); рання — 1989 (#28).
