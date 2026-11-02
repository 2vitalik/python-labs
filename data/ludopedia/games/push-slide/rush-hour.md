---
title: Rush Hour (ThinkFun)
slug: rush-hour
family: push-slide
also: [board-digital]
klass: figure
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 1996
platforms: [board, iOS, Android, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)", note: "правила, комплект, картки, видання, складність"}
  - {kind: play, url: "https://www.michaelfogleman.com/rush/", best: true, note: "Fogleman: усі 2,5 млн пазлів 6×6, нотація рядком, move vs step, онлайн-гра з кнопкою Random"}
  - {kind: official, url: "https://www.thinkfun.com/products/rush-hour/", note: "сторінка виробника (редірект на Ravensburger)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rush+hour+thinkfun+how+to+play", note: "пошук; правила і розвʼязки"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=rush+hour", note: "пошук; цифрові версії"}
stage: v1
coverage: 80
mechanics: [multi-cell-size, impassable-cells, reach-exit, drag-drop-piece, swipe-gestures, cell-click, level-bank, level-rating, difficulty-levels, level-select, level-solver, level-from-txt, import-open-formats, unique-puzzle-generation, difficulty-rating, sequential-levels, +stars-rating, +axis-locked-move, +move-vs-step, +undo-redo, +state-string]
proposes: ["+trigger:input", "+trigger:reach", "+cond:free", "+effect:move", "+effect:counter", "+role:piece", "+ui:move-counter", "+ui:par-moves", "+window:puzzle-select", "+feature:par-target", "+feature:stars-rating", "+feature:puzzle-bank", "+card:axis-locked-move"]
author: opus
date: 2026-11-02
---

# Rush Hour — розсунь машини на парковці 6×6, щоб червона виїхала

## Суть
Ковзна головоломка: на полі 6×6 стоять автомобілі завдовжки 2 і вантажівки завдовжки 3, кожен **рухається лише вздовж своєї осі** (вперед-назад), не повертає і не перестрибує інших. Треба розчистити шлях червоній машині до виходу в бортику. Стартову розстановку задає картка з колоди (40 карток у базовому наборі, 4 рівні складності). Задача на довільних полях PSPACE-complete; найважчий пазл 6×6 — 51 хід.

## Поле і час
- Сітка 6×6 з одним виходом у правому бортику — на рядку червоної машини (третій зверху).
- Один шар: машини займають 2 або 3 клітини; порожні клітини — «o», у цифрових варіантах бувають стіни-клітини «x» (1×1, нерухомі).
- Час відсутній (`static`): світ змінюється лише ходом гравця; лічильник ходів у цифрових версіях.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Червона машина (A) | piece | довжина 2, горизонтальна | рухається вздовж рядка; дійшла до виходу — перемога |
| Легкове авто (B…) | piece | довжина 2, орієнтація H/V | рухається вздовж своєї осі на будь-яку кількість вільних клітин |
| Вантажівка | piece | довжина 3, орієнтація H/V | те саме, довжина 3 |
| Стіна (x) | static | 1×1 | лише у варіантах (Fogleman, деякі аплікації): непрохідна |
| Вихід | static | на рядку червоної | пропускає лише червону машину |
| Бортик | static | — | межа поля |
| Картка-завдання | mark | номер, рівень складності | задає розстановку; на звороті — розвʼязок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, vehicle, n)` → ЯКЩО `custom: «напрям уздовж осі машини»` і `free(усі n клітин на шляху)` → ТО `move(vehicle, n)`; інакше `block`.
- Машина не повертає, не перестрибує, не штовхає інших (на відміну від Sokoban): рухати можна лише ту, яку взяв.
- КОЛИ `reach(red_car, exit)` → ТО `win`.
- Інші машини через вихід не виїжджають (вихід — лише для червоної).
- Рахунок у цифрових версіях: **move** = зсув однієї машини на N клітин за раз, **step** = зсув на 1 клітину; найважчий пазл 6×6 — 51 move (93 steps).
- Перемога: червона на виході. · Поразки нема (глухих кутів теж: будь-який хід зворотний). · Оцінка: кількість ходів проти мінімальної (par, зірки).

## Керування і ввід
- Настолка: рукою зсунути машину в пазі.
- Цифрові версії: drag машини пальцем/мишею вздовж осі (машина «прилипає» до сітки), або свайп по машині; undo, рестарт, підказка наступного ходу.
- Ввід — `select-then-move` у неявній формі: сам drag обирає і машину, і довжину ходу.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Грати → `puzzle-select` за рівнем складності (Beginner / Intermediate / Advanced / Expert) → сітка пазлів з позначками «розвʼязано» і зірками.
- `game-screen`: поле 6×6; HUD — номер пазла, `move-counter`, `par-moves` (мінімум), `undo-button`, `restart-button`, `hint-button`.
- `end-screen`: «розвʼязано за N ходів (мінімум M)», зірки, Далі.
- `settings-window`: звук, тема/скін машин (?).
- Fogleman: одне поле з кнопками Random / Reset, без меню.
- Переходи: main-menu → puzzle-select → game-screen → end-screen → наступний пазл.

## Фічі поза полем
- `puzzle-bank` з `difficulty-presets` (картки 4 рівнів; Deluxe +60 і Grand Master; Ultimate Collector's +155 пазлів і білий лімузин; доповнення по 40 пазлів).
- `par-target` / `stars-rating` за мінімальною кількістю ходів (цифрові версії).
- `undo`, `restart-level`, `hint`/`show-solution` (як зворот картки).
- Генерація: Fogleman перебрав усі «цікаві» стартові позиції 6×6 — 2 577 412 пазлів у 9,7 млрд станів, з до 2 стін; кластер = множина взаємодосяжних станів, канонічний стан — найменший у кластері.
- `share-code`: позиція — рядок із 36 символів (`o` — порожньо, `x` — стіна, `A` — червона, `B…Z` — інші).

## Варіації й родичі
- ThinkFun: Rush Hour Jr., Safari Rush Hour, Railroad Rush Hour, Rush Hour Brain Fitness, Rush Hour Shift (на двох).
- Цифрові: iOS (2010), Blocked (2009, мобільна), Unblock Me та численні клони (?).
- Осі варіацій: **рух**: лише вздовж осі (Rush Hour) / у будь-якому напрямку (Klotski, 15-puzzle); **розмір фігур**: 1×2/1×3 (Rush Hour) / 2×2 та інші (Klotski); **крок**: на будь-яку кількість клітин (move) / рахунок по клітинах (step); **ціль**: вивести одну фігуру (Rush Hour, Klotski) / упорядкувати всі (15-puzzle); **перешкоди**: без стін / зі стінами (Fogleman); **гравці**: соло / дуель (Shift).
- Родичі: Klotski, 15-puzzle, Unblock Me, Atomix (теж фігури-ковзанки, але до упору).

## Цікавинки для курсу
- Фігури розміром понад клітину з рухом лише вздовж осі (машина = координата + довжина + орієнтація) — 📎.
- Drag із привʼязкою до сітки й обмеженням ходу до першої перешкоди — 🥉.
- BFS-розвʼязувач з мінімальною кількістю moves і підказкою «наступний хід» — 🥈 (простір станів малий, тому BFS вистачає).
- Генератор пазлів за складністю: випадкова розстановка → BFS → відбір за довжиною розвʼязку; повний перебір кластерів як у Fogleman — 🥇.
- Нотація позиції рядком (36 символів) як формат рівня, обміну і тестів — 🌱.
- Метрики move vs step як дві різні міри складності — 🌱.

## Мапа на каталог
- Є: `multi-cell-size` ↔ машини 1×2/1×3 вздовж осі (картка прямо згадує Rush Hour); `impassable-cells` ↔ бортик, стіни; `reach-exit` ↔ червона на виході; `drag-drop-piece` + `swipe-gestures` + `cell-click` ↔ ввід у цифрових версіях; `level-bank` + `level-rating` + `difficulty-levels` + `level-select` ↔ колода карток 4 рівнів; `level-solver` ↔ BFS/підказка; `level-from-txt` + `import-open-formats` ↔ рядок-позиція; `unique-puzzle-generation` + `difficulty-rating` ↔ генерація і рейтинг за довжиною розвʼязку; `sequential-levels`; `stars-rating`.
- **Нема** → пропозиції карток:
  - `+axis-locked-move` «Рух лише вздовж власної осі» · entities/move · 📎 · слот {n: 1|any} — дитина `multi-cell-size`.
  - `+move-vs-step` «Дві метрики ходу: зсув і крок» · game-logic/score · 🌱.
  - `+undo-redo` «Undo/redo ходів у грі» · game-logic/flow · 📎.
  - `+state-string` «Стан поля одним рядком» · levels/format · 🌱 — 36 символів Fogleman.

## Пропозиції до словників
- `+trigger:input` — drag машини; `+trigger:reach` — червона дійшла до виходу.
- `+cond:free` — усі клітини шляху вільні.
- `+effect:move` — зсув на N; `+effect:counter` — лічильник moves.
- `+role:piece` — машини як фігури з власним правилом ходу.
- `+ui:move-counter`, `+ui:par-moves` — ходи й мінімум.
- `+window:puzzle-select` — сітка пазлів за рівнями складності.
- `+feature:par-target`, `+feature:stars-rating`, `+feature:puzzle-bank` — оцінка відносно мінімуму, колода карток.
- `+card:axis-locked-move` — див. вище.

## Джерела
- ⭐ [Michael Fogleman: Solving Rush Hour](https://www.michaelfogleman.com/rush/) — повний перебір пазлів 6×6, найважчі (51 хід без стін), нотація рядком, move vs step, онлайн-гра з Random.
- [Wikipedia: Rush Hour (puzzle)](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)) — винахідник Nob Yoshigahara, комплект (12 авто + 4 вантажівки), 40 карток, видання, PSPACE-complete, 93 steps / 51 moves.
- [ThinkFun: Rush Hour](https://www.thinkfun.com/products/rush-hour/) — сторінка виробника (переадресовує на Ravensburger; вміст не прочитано).
- YouTube: пошук «rush hour thinkfun how to play».

## Непевне
- (?) Назви рівнів складності Beginner/Intermediate/Advanced/Expert і кольори карток — за памʼяттю (Wikipedia каже лише «4 рівні»).
- (?) Конкретні фічі цифрових версій (зірки, підказка, скіни) — типові для клонів, конкретну аплікацію ThinkFun не перевірено.
- (?) Рік винаходу — «1970-ті» (Yoshigahara), у шапці 1996 — рік виходу ThinkFun у США.
- Пошуковий бюджет сесії вичерпався; сторінка Ravensburger повернула 403.
