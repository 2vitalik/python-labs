---
title: SameGame / Clickomania + Flood (Tatham)
slug: samegame-flood
family: falling-match
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 1985
platforms: [FM-8/FM-7, Mac, Windows, Linux (KSame, Swell Foop), web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/samegame.html", best: true, note: "Tatham: точні правила Same Game, керування, (n−2)² vs (n−1)², параметри, ensure solubility"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flood.html", note: "Tatham: правила Flood, заливка з кута, ліміт ходів = розвʼязок солвера + extra moves"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/samegame.html", note: "грати Same Game у браузері"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flood.html", note: "грати Flood у браузері"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SameGame", note: "Chain Shot! 1985, розміри полів, (n−k)², бонус за чисте поле, варіанти, NP-повнота"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flood_fill", note: "алгоритм заливки: стек/черга/scanline, 4- vs 8-звʼязність"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=samegame+clickomania+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [cell-click, hover-highlight, keyboard-controls, gravity-fall, no-moves-left, event-points, score-records, reachability-check, level-solver, difficulty-levels, field-size-picker, game-settings, satisfy-constraints, +connected-group-pop, +column-collapse-left, +group-score-quadratic, +all-clear-bonus, +solvable-generation, +flood-fill-region, +move-limit, +solver-par, +undo-redo]
proposes: ["+trigger:input", "+trigger:no_moves", "+cond:connected", "+cond:group_size", "+cond:same", "+effect:fall", "+effect:collapse_left", "+effect:flood", "+effect:paint", "+ui:selection-highlight", "+ui:move-counter", "+feature:solver-par", "+feature:custom-difficulty", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# SameGame + Flood — дві гри про звʼязну одноколірну область: прибрати групу кліком або залити її з кута

## Суть
**SameGame** (Chain Shot!, 1985; Clickomania, Same Gnome, KSame): поле випадкових кольорових клітин; клік по звʼязній групі з 2+ однакових прибирає її, верхні клітини падають, порожні стовпці зсуваються вліво. Очки — квадратичні від розміру групи `(n−2)²`, тож вигідно спершу «виростити» великі групи; гра кінчається, коли лишились лише одиночні клітини. **Flood** (Tatham; Flood-It): поле кольорів, хід — обрати колір, і область верхнього лівого кута, звʼязна по однаковому кольору, перефарбовується й зливається з сусідами того кольору; треба залити все поле одним кольором за ліміт ходів. Пара показує два способи працювати з однією структурою даних — **flood fill по звʼязній одноколірній області**: в одній грі область знищують, в іншій — нарощують.

## Поле і час
- SameGame: прямокутник (Chain Shot! 20×10, 4 кольори; Amiga 15×10, 3 кольори; Windows до 25×15; Tatham — довільні Width/Height і кількість кольорів).
- Flood: квадрат/прямокутник (Width × Height задаються), 3–10 кольорів; «джерело» — верхня ліва клітина.
- Статика: нема часу, нема випадковості після генерації (`random: setup`); хід = клік. Деякі версії SameGame мають таймер або «continuous»-правило — нові стовпці/рядки додаються (?).
- Звʼязність — 4-сусідство (ортогональне) в обох іграх; варіанти SameGame — з діагоналями.
- SameGame після ходу: **дві гравітації** — вниз у стовпці, потім порожні стовпці зникають, решта зсувається вліво (Tatham: «порожні стовпці заповнюються справа»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор / виділення (SameGame) | player | клітина, виділена група | клік 1 — виділити групу (показати розмір і очки), клік 2 — прибрати |
| Клітина-блок (SameGame) | tile | колір | у групі 2+ → прибирається; без опори падає; стовпець порожній → зсув уліво |
| Група (SameGame) | zone | колір, n клітин | максимальна 4-звʼязна одноколірна множина; n ≥ 2 → клікабельна |
| Клітина (Flood) | tile | колір | належить залитій області, якщо 4-звʼязана з кутом через той самий колір |
| Залита область (Flood) | zone | колір, розмір | після ходу перефарбовується в обраний колір і поглинає сусідні клітини цього кольору |
| Кут-джерело (Flood) | static | (0,0) | звідки росте область |
| Солвер (Flood) | — (logic) | довжина розвʼязку | задає ліміт ходів = свій розвʼязок + extra moves |

## Правила (КОЛИ → ЯКЩО → ТО)
SameGame:
- КОЛИ `input(click cell)` → ЯКЩО `group_size(cell) ≥ 2` → ТО `custom: «select — підсвітити групу, показати n і очки»`; клік поза групою — нове виділення; правий клік — зняти.
- КОЛИ `input(click selected)` → ТО `clear(group)`, `score((n−2)²)` (Tatham за замовчуванням; варіант `(n−1)²`; деякі версії — 1 за клітину).
- КОЛИ `after(clear)` → ТО `fall(cells)` у кожному стовпці (наївна, без ланцюгів — нові групи не лопаються самі).
- КОЛИ `after(fall)` → ЯКЩО `count(column_cells, ==, 0)` → ТО `custom: «collapse_left — порожній стовпець прибирається, праві зсуваються вліво»`.
- КОЛИ `custom: «settled»` → ЯКЩО `count(cells, ==, 0)` → ТО `win`, у частині версій великий `score(all_clear_bonus)`.
- КОЛИ `no_moves(player)` (лише одиночні клітини) → ТО `lose` (Tatham) / `game_over` з рахунком; у деяких версіях — штраф за залишок або бонус, якщо лишилось ≤ N.
- Генерація (Tatham): `ensure solubility` — поле гарантовано розвʼязне; вимкнено — лише ≥ 2 клітини кожного кольору.

Flood:
- КОЛИ `input(click cell)` → ЯКЩО `not same(cell.color, region.color)` → ТО `custom: «flood — paint(region, cell.color)»`, `counter(moves, +1)`; інакше хід не зараховано.
- КОЛИ `after(paint)` → ТО `custom: «region = усі клітини, 4-звʼязні з (0,0) через один колір»` (BFS/DFS заливка).
- КОЛИ `count(region, ==, all_cells)` → ЯКЩО `counter(moves, ≤, limit)` → ТО `win`; інакше — поле залито, але ліміт перевищено (поразка, можна продовжити (?)).
- Ліміт: `limit = len(solver_solution) + extra_moves`; при extra = 0 треба зрівнятися з солвером.
- Рахунок: SameGame — очки за групи (+ бонус за чисте поле); Flood — кількість ходів проти ліміту.

## Керування і ввід
- SameGame (Tatham): лівий клік — виділити групу / вдруге — прибрати; правий клік — зняти виділення; стрілки + Space/Enter — те саме з клавіатури. Classic Clickomania — один клік одразу прибирає (?).
- Flood (Tatham): клік по будь-якій клітині — залити кут її кольором; стрілки — чорний курсор-рамка, Enter — залити кольором під курсором.
- Спільні дії Tatham: `n` — нова гра, `u`/`r` — undo/redo, `restart`, Solve (Flood — показує хід солвера (?)).

## Вікна, меню, HUD
- Tatham (обидві): `game-screen` з полем + рядок стану: SameGame — «Score: N» і розмір/очки виділеної групи, «Game over»/«Cleared!»; Flood — `move-counter` «Moves: X / limit» (?), повідомлення про перемогу.
- Меню Game: New game · Restart · Undo · Redo · Solve (Flood) · Specific/Random seed (`seed-input`) · Load/Save · Print; меню Type — пресети розмірів і Custom… (`settings-window`: Width, Height, кольори, scoring system / extra moves, ensure solubility).
- `help-window` — сторінка документації.
- Клони SameGame (Same Gnome / Swell Foop, KSame, Windows-версії): `leaderboard` рекордів, вибір розміру/теми (кульки, камінці).
- Переходи: game-screen → (нема ходів / чисте поле / залито) статус-рядок → New game.

## Фічі поза полем
- `custom-difficulty` — розмір, кількість кольорів, extra moves; `difficulty-presets` у меню Type.
- `undo` / `redo` необмежено (Tatham), `restart-level`, `seed-display` / `seed-input` — повторити ту саму генерацію, `save-slots`-подібне Save/Load файлом.
- `auto-solve` (Flood: солвер є, бо він задає ліміт).
- Генерація з гарантією розвʼязності (SameGame) — `custom: «solvable-generation»`.
- Клони — `leaderboard-local`, `theme-select`.

## Варіації й родичі
- SameGame: Chain Shot! (Kuniaki Moribe, 1985, FM-8/FM-7) → Mac SameGame (Takahiro Sumiya) → KSame, Same GNOME, Swell Foop → Clickomania! (1998, мета — просто очистити поле) → Jawbreaker (Pocket PC, 2003), Same Pets/Hearths (1 очко за клітину).
- Варіанти SameGame: діагональна звʼязність, спецблоки, життя, «shift/continuous» — нові стовпці/рядки додаються в міру зчищення.
- Flood: Flood-It (мобільна/веб гра (?)), Tatham Flood, «Colour Flood»; Filler (дуель: двоє заливають з протилежних кутів).
- Родичі: Puyo (звʼязна група лопається сама, 4+), Triple Town (звʼязна група зливається), Collapse (SameGame + рядки знизу), Toon Blast/Pet Rescue (SameGame з цілями рівнів у стилі Candy Crush) (?).
- **Осі варіацій**: дія над групою (прибрати / перефарбувати / злити) · мін. розмір (1 / 2 / 3) · звʼязність (4 / 8) · гравітація (вниз / вниз + вліво / нема) · очки (за клітину / (n−1)² / (n−2)²) · кінець (нема груп / ліміт ходів / таймер) · генерація (випадкова / з гарантією розвʼязку).
- Складність: Clickomania NP-повна вже для 2 стовпців × 5 кольорів і 5 стовпців × 3 кольорів, важка навіть для 2 кольорів (2015); Flood-It оптимум — NP-важкий (?).

## Цікавинки для курсу
- Пошук звʼязної одноколірної групи (BFS/DFS, 4-сусідство) — 🌱; підсвітка групи під курсором з очками — 🌱.
- Подвійна гравітація: падіння в стовпці + стискання порожніх стовпців уліво — 📎.
- Детектор «нема груп ≥ 2» + квадратичний рахунок — 🌱.
- Flood: заливка з кута, що поглинає сусідів, + лічильник ходів проти ліміту — 📎.
- Солвер Flood (жадібний за розміром області / BFS на малих полях) як джерело ліміту ходів — 🥇 (оптимум NP-важкий, треба евристика).
- SameGame: генерація з гарантією розвʼязності (ensure solubility) — 🥇.
- Undo/redo на стані поля + seed — 📎.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` (група під курсором) · `keyboard-controls` (курсор) · `gravity-fall` · `no-moves-left` (лише одиночні) · `event-points` · `score-records` · `reachability-check` (flood fill — та сама BFS) · `level-solver` (солвер Flood) · `difficulty-levels` · `field-size-picker` · `game-settings` · `satisfy-constraints` (Flood: поле одного кольору).
- **Нема** → пропозиції карток:
  - `+connected-group-pop` · entities/legality · 📎 · слоти {min: 2, adjacency: 4, trigger: click} (спільна з Puyo/Puzznic; тут — за кліком, не сама).
  - `+column-collapse-left` «Порожні стовпці стискаються вбік» · entities/move · 🌱.
  - `+group-score-quadratic` «Очки (n−k)² за групу» · game-logic/score · 🌱 · слот {k: 1|2}.
  - `+all-clear-bonus` · game-logic/score · 🌱 (спільна з Puyo).
  - `+solvable-generation` «Генерація з гарантією розвʼязку» · levels/generation · 🥇 (родич `unique-puzzle-generation`, але без унікальності).
  - `+flood-fill-region` «Заливка області з джерела» · entities/interact · 📎.
  - `+move-limit` «Ліміт ходів» · game-logic/lose · 🌱 (спільна з Candy Crush).
  - `+solver-par` «Ліміт = розвʼязок солвера + запас» · levels/generation · 🥇.
  - `+undo-redo` · interface/input · 📎 (спільна з 2048).

## Пропозиції до словників
- `+trigger:input` — ⏳ підтверджую; `+trigger:no_moves` — ⏳ підтверджую (лише одиночні клітини).
- `+cond:connected` — 🔥 підтверджую (клітина в області джерела); `+cond:group_size(cell, op, n)` — розмір звʼязної групи клітини (SameGame n ≥ 2, Puyo 4+); `+cond:same` — 🔥.
- `+effect:fall` — 🔥; `+effect:collapse_left` — стиснути порожні стовпці вбік (друга гравітація).
- `+effect:flood` — перефарбувати область джерела й поглинути сусідів кольору (композиція `paint` + перерахунок `connected`); `+effect:paint` — ⏳ підтверджую.
- `+ui:selection-highlight` — ⏳ підтверджую (виділена група з n та очками); `+ui:move-counter` — 🔥 (ходи / ліміт).
- `+feature:solver-par` — ліміт ходів, обчислений солвером; `+feature:custom-difficulty` — ⏳ підтверджую.
- `+axis:gravity` — значення `down-then-left` (SameGame) і `none` (Flood).

## Джерела
- ⭐ [Tatham: Same Game](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/samegame.html) — правила (групи > 1, падіння, порожні стовпці заповнюються справа), керування, очки (n−2)² / (n−1)², параметри, ensure solubility.
- [Tatham: Flood](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/flood.html) — правила, клік = колір, клік у колір кута не рахується, кольори 3–10, extra moves до розвʼязку солвера.
- [Грати Same Game](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/samegame.html) · [Грати Flood](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/flood.html) — браузерні версії Tatham.
- [Wikipedia: SameGame](https://en.wikipedia.org/wiki/SameGame) — Chain Shot! 1985, розміри полів, формула (n−k)², бонуси, варіанти, NP-повнота (Biedl 2001, Adler 2015).
- [Wikipedia: Flood fill](https://en.wikipedia.org/wiki/Flood_fill) — стек/черга/scanline, 4- vs 8-звʼязність.
- YouTube: пошук «samegame clickomania gameplay».

## Непевне
- (?) Походження Flood-It (мобільна гра кінця 2000-х) і NP-важкість оптимального Flood-It — з памʼяті; окремої статті на Wikipedia не знайшлось, WebSearch вичерпано.
- (?) Чи Tatham дозволяє продовжити після перевищення ліміту Flood і як саме показує «Moves: X / limit».
- (?) Classic Clickomania з одним кліком без виділення; «continuous»-варіанти, Collapse, Toon Blast — з памʼяті.
- (?) Пункт Solve у Flood — у Tatham солвер є (задає ліміт), але чи виведено його в меню, не перевірено.
