---
title: Theseus and the Minotaur (Тесей і Мінотавр)
slug: theseus-and-the-minotaur
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 1990
platforms: [paper (книга Mad Mazes), web, PC, mobile]
links:
  - {kind: official, url: "https://logicmazes.com/theseus.html", best: true, note: "сторінка Robert Abbott: правила і лабіринти Тесея (на момент перевірки — помилка сертифіката)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Logic_maze", note: "жанр «лабіринт з правилами»; Theseus — один з відомих лабіринтів Abbott"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Robert_Abbott_(game_designer)", note: "автор; Mad Mazes (1990): «найважчий лабіринт у книзі»"}
  - {kind: other, url: "https://www.mobygames.com/game/41636/mummy-maze-deluxe/", note: "Mummy Maze Deluxe (PopCap) — комерційний нащадок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=theseus+and+the+minotaur+logic+maze", note: "пошук; розвʼязки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mummy+maze+gameplay", note: "пошук; Mummy Maze — геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, chase-greedy, chase-double-move, impassable-cells, reach-exit, touch-death, sequential-levels, level-select, level-solver, difficulty-rating, fixture-level-tests, level-from-txt, +wall-edges, +wait-turn, +undo-redo]
proposes: ["+trigger:input", "+trigger:turn_end(side)", "+cond:free_edge(a, dir)", "+cond:closer(a, b, axis)", "+effect:pass_turn", "+effect:extra_move", "+ui:move-counter", "+ui:par-moves", "+feature:undo", "+feature:puzzle-bank", "+axis:undo", "+card:greedy-axis-chase"]
author: opus
date: 2026-11-02
---

# Theseus and the Minotaur — один ворог, одне правило: Мінотавр робить два жадібних кроки на твій один

## Суть
Логічний лабіринт Robert Abbott з книги *Mad Mazes* (1990). Тесей має дійти до виходу, а Мінотавр після кожного його ходу робить **два** кроки до нього за жорстким правилом: спершу намагається скоротити відстань по горизонталі, і лише якщо не може — по вертикалі. Мінотавр удвічі швидший, тож втекти неможливо; виграєш, лише **заганяючи його за стіни**, де жадібне правило змушує його стояти. Абботт назвав його «найважчим лабіринтом книги — можливо, ніхто його не розвʼяже». Повністю детермінований: увесь пазл — у правилі ворога. У корпусі — як «мінімальний роглайк»: один монстр з одним AI-правилом уже генерує глибину.

## Поле і час
- Прямокутна сітка (типово 6×6–10×10), стіни — **на ребрах між клітинами**, а не клітини-стіни; вихід — розрив на краю поля біля однієї з клітин.
- Покроково: хід Тесея (1 крок або пропуск) → два кроки Мінотавра → перевірка. Усе видно, випадковості нема.
- Стан гри = (позиція Тесея, позиція Мінотавра) — для 8×8 лише ~4 тисячі станів, тому повний перебір тривіальний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тесей | player | — | крок на 1 у 4 напрямках через ребро без стіни, або пропуск ходу |
| Мінотавр | enemy | 2 кроки на хід | кожен крок: горизонтально до Тесея, якщо можна; інакше вертикально; інакше стоїть |
| Стіна на ребрі | static | сторона клітини | блокує рух обох через це ребро |
| Вихід | static | клітина на краю | Тесей на ній — перемога |
| (Mummy Maze) Біла мумія | enemy | 2 кроки | горизонталь першою (= Мінотавр) |
| (Mummy Maze) Червона мумія | enemy | 2 кроки | вертикаль першою |
| (Mummy Maze) Скорпіон | enemy | 1 крок | те саме жадібне правило, повільніший |
| (Mummy Maze) Пастка | hazard | — | смерть для гравця, вороги ігнорують (?) |
| (Mummy Maze) Ключ і ґрати | switch / gate | — | ключ перемикає ґрати (відкрито ↔ закрито) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free_edge(theseus, dir)` → ТО `move(theseus, dir)`; інакше `block` (хід не витрачається).
- КОЛИ `input(wait)` → ТО `pass_turn` (Тесей стоїть, Мінотавр ходить).
- КОЛИ `contact(theseus, exit)` → ТО `win` (одразу, до ходу Мінотавра).
- КОЛИ `turn_end(theseus)` → ТО двічі: ЯКЩО `closer(minotaur, theseus, x)` and `free_edge(minotaur, dir_x)` → ТО `move(minotaur, dir_x)`; ІНАКШЕ ЯКЩО `closer(minotaur, theseus, y)` and `free_edge(minotaur, dir_y)` → ТО `move(minotaur, dir_y)`; інакше — стоїть (`custom: «крок втрачено»`).
- КОЛИ `contact(minotaur, theseus)` (після будь-якого кроку, або Тесей увійшов у клітину Мінотавра) → ТО `lose`.
- Мінотавр **ніколи не відходить** від Тесея, щоб обійти стіну: якщо обидва «наближаючі» кроки заблоковані — він застрягає. На цьому побудовано кожен розвʼязок.
- Перемога: Тесей на виході. Поразка: Мінотавр на клітині Тесея. Рахунок: кількість ходів; цифрові версії показують мінімум.
- Mummy Maze додає: КОЛИ `contact(mummy_a, mummy_b)` → ТО `disappear_b` (одна знищує іншу — спосіб позбутися ворога); КОЛИ `contact(any, key)` → ТО `set_state(gates, toggle)`.

## Керування і ввід
- Стрілки (або тап/клік по сусідній клітині) — крок; окрема клавіша/кнопка — пропуск ходу.
- Цифрові версії: Undo (на хід назад), Reset (рівень з початку), перехід між лабіринтами.
- На папері: олівець — гравець сам «програє» Мінотавра (і помиляється — частина складності).

## Вікна, меню, HUD
- `game-screen`: сітка з тонкими стінами, Тесей, Мінотавр, вихід; `move-counter`; кнопки `undo-button`, `restart-button`, «чекати».
- `level-select` / `puzzle-select`: список лабіринтів з позначкою «пройдено» (цифрові версії).
- `end-screen`: «Тебе зʼїли» (рестарт / undo) або «Вибрався» з кількістю ходів (і мінімумом у деяких версіях (?)).
- `help-window`: правила руху Мінотавра одним абзацом — без них гра не грається.
- Mummy Maze (PopCap): `main-menu`, режими «пригода» (піраміди) і «класичний», `end-screen` з анімацією мумії.

## Фічі поза полем
- `undo` (необмежений у більшості цифрових версій) — ключовий, бо гра — чиста дедукція.
- `puzzle-bank` / `levels-sequential`: набір лабіринтів зростаючої складності (Abbott + доповнення інших авторів (?)).
- `hint` / `show-solution` — у деяких версіях (?).
- Генерація: оскільки простір станів малий, нові лабіринти генерують перебором і відбирають за довжиною найкоротшого розвʼязку — `difficulty-rating`.

## Варіації й родичі
- Mummy Maze / Mummy Maze Deluxe (PopCap, 2001) — кілька ворогів з різними пріоритетами осей, скорпіони, пастки, ключі й ґрати.
- Інші логічні лабіринти Abbott: «Traffic Maze in Floyd's Knob» (1962), лабіринти з кубиками, з правилами повороту.
- Родичі: Hoplite і broughlike (детерміновані вороги), DROD (монстри з точними правилами руху), Pac-Man (кожен привид має одне цільове правило), Chip's Challenge (Teeth — жадібна погоня через такт).
- Осі варіацій: **швидкість ворога** (1 / 2 / 3 кроки на хід); **пріоритет осі** (горизонталь / вертикаль / більша відстань першою); **поведінка на блоці** (стоїть / пробує іншу вісь / обходить BFS); **кількість ворогів і їхні взаємодії** (знищують одне одного?); **чи може гравець чекати**.

## Цікавинки для курсу
- Жадібна погоня з пріоритетом осі + 2 кроки на хід — картки `chase-greedy` і `chase-double-move` в одній грі — 🥉.
- Розвʼязувач: BFS по станам (Тесей, Мінотавр) з undo — 🥇, але з маленьким простором станів — ідеальне перше «золото».
- Генератор лабіринтів: випадкові стіни → BFS → залишити ті, де найкоротший розвʼязок довгий — 👑 за якісний генератор з оцінкою складності.
- Тонкі стіни на ребрах замість клітин-стін — 📎 (інша модель поля: стіна як властивість ребра).
- Тести на рівнях-фікстурах: послідовність ходів → очікувана позиція Мінотавра — 🥉 (детермінізм робить тести тривіальними й цінними).
- «Один ворог, одне правило» як генератор пазлів — урок дизайну для есе — 📎.

## Мапа на каталог
- Є: `move-4dir` · `chase-greedy` · `chase-double-move` (картка прямо названа на честь Theseus) · `impassable-cells` (стіни) · `reach-exit` · `touch-death` · `sequential-levels` · `level-select` · `level-solver` · `difficulty-rating` · `fixture-level-tests` · `level-from-txt`.
- **Нема** → пропозиції карток:
  - `+wall-edges` «Стіни на ребрах між клітинами» · entities/legality · 📎 (уже пропонувалась).
  - `+wait-turn` «Пропуск ходу» · entities/move · 🌱 (уже пропонувалась).
  - `+undo-redo` (уже пропонувалась).
  - `+greedy-axis-chase` «Жадібна погоня з пріоритетом осі» · entities/move · 📎 · слот {axis_first: x|y} — дитина `chase-greedy`.

## Пропозиції до словників
- `+cond:closer(a, b, axis)` — крок уздовж осі зменшує відстань A до B (ядро AI Мінотавра).
- `+cond:free_edge(a, dir)` — на ребрі в напрямку нема стіни (поле зі стінами-ребрами).
- `+trigger:turn_end(side)` — кінець ходу гравця запускає хід ворога.
- `+effect:pass_turn` — свідомо пропустити хід; `+effect:extra_move` — ворогу другий крок.
- `+ui:move-counter` · `+ui:par-moves` — ходи і мінімум.
- `+feature:undo` · `+feature:puzzle-bank` · `+axis:undo` — тут `unlimited`.
- `+card:greedy-axis-chase` — див. вище.
- `+trigger:input` — як в інших файлах.

## Джерела
- ⭐ [Robert Abbott: Theseus and the Minotaur](https://logicmazes.com/theseus.html) — сторінка автора з лабіринтами (на 2026-11-02 сайт віддає помилку сертифіката; URL з черги куратора й зовнішніх лінків Wikipedia).
- [Wikipedia: Logic maze](https://en.wikipedia.org/wiki/Logic_maze) — жанр, Abbott як винахідник, Theseus серед відомих лабіринтів.
- [Wikipedia: Robert Abbott](https://en.wikipedia.org/wiki/Robert_Abbott_(game_designer)) — *Mad Mazes* (1990), цитата про «найважчий лабіринт», інші версії на папері й електронні.
- [MobyGames: Mummy Maze Deluxe](https://www.mobygames.com/game/41636/mummy-maze-deluxe/) — комерційний нащадок (сторінка не відкрилась, 403).
- YouTube: [пошук «theseus and the minotaur logic maze»](https://www.youtube.com/results?search_query=theseus+and+the+minotaur+logic+maze) · [пошук «mummy maze gameplay»](https://www.youtube.com/results?search_query=mummy+maze+gameplay).

## Непевне
- (?) Точне правило Мінотавра (горизонталь першою, стоїть, якщо обидві осі заблоковані) — з памʼяті й каталожної картки `chase-double-move`; сторінку Abbott не вдалося відкрити (сертифікат), веб-пошук вичерпано.
- (?) Хто автор поширених цифрових версій (Toby Nelson?) і скільки в них лабіринтів — не перевірено.
- (?) Mummy Maze: пастки смертельні лише для гравця; ключ перемикає ґрати; мумії знищують одна одну — з памʼяті.
- (?) Чи можна Тесею свідомо ступити на клітину Мінотавра (у більшості версій — поразка).
- (?) Розміри сіток (6×6–10×10) — орієнтовно.
