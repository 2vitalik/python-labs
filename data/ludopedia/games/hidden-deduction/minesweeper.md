---
title: Minesweeper (Сапер)
slug: minesweeper
family: hidden-deduction
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 1990
platforms: [Windows (Entertainment Pack → Windows 3.1…7), Windows 8+ Store (Arkadium), Linux (KDE/GNOME), web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Minesweeper_(video_game)", best: true, note: "правила, chord, перший клік, пресети, історія, NP-повнота"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Microsoft_Minesweeper", note: "версії Windows: Vista/7 теми, Windows 8+ режими Adventure і Daily"}
  - {kind: play, url: "https://minesweeper.online/", note: "грати в браузері: Standard, No guessing, PvP, рейтинги 3BV/s"}
  - {kind: official, url: "https://minesweepergame.com/statistics.php", note: "Minesweeper Authoritative: 3BV, IOE, RQP, ZiNi — формули"}
  - {kind: official, url: "https://minesweepergame.com/strategy/first-click.php", note: "безпечний перший клік по версіях, шанс відкриття"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html", note: "Tatham Mines: генератор без вгадувань, undo після вибуху, гекс/трикутні сітки"}
  - {kind: official, url: "https://minesweepergame.com/database/games.php?id=37", note: "Minesweeper Flags (MSN, 2003): 16×16, 51 міна, хто перший 26"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=minesweeper+expert+world+record", note: "пошук; рекордні проходження Expert"}
stage: v1
coverage: 80
mechanics: [cell-click, chord-click, mines-after-first-click, difficulty-levels, game-settings, field-size-picker, score-records, leaderboard, profile-stats, game-screen, end-screen, settings-window, help-window, theme-select, save-game, completion-detection, daily-puzzle, level-solver, difficulty-rating, +flood-reveal, +neighbor-count-clue, +flag-cycle, +no-guess-generation, +board-metrics-3bv, +mine-flag-race]
proposes: ["+cond:flags_match", "+effect:flood_reveal", "+ui:face-button", "+ui:mine-counter", "+window:custom-size-dialog", "+window:record-name-dialog", "+feature:no-guess", "+feature:board-metrics", "+feature:no-flags-style", "+card:flood-reveal", "+card:neighbor-count-clue", "+card:flag-cycle", "+card:no-guess-generation", "+card:board-metrics-3bv", "+card:mine-flag-race"]
author: opus
date: 2026-11-02
---

# Minesweeper — відкрий усі безпечні клітини, читаючи числа сусідніх мін

## Суть
Поле прямокутних клітин, під частиною — міни. Гравець клацає клітину: міна — програш, інакше клітина показує, скільки мін серед її 8 сусідів; нуль автоматично розкриває всю «порожню» область. Права кнопка ставить прапорець на підозрювану міну, «акорд» по числу відкриває всіх незапрапорених сусідів. Ядро — локальна дедукція з чисел (і часом вимушене вгадування); перемога — відкрити всі клітини без мін, рахунку нема, лише час.

## Поле і час
- Прямокутна сітка W×H, сусідство — 8 (Мура). Пресети Windows: Beginner 8×8 або 9×9 / 10 мін, Intermediate 16×16 / 40, Expert 30×16 / 99; Custom — до 30×24, мін від 10 до (W−1)(H−1).
- Шари клітини: прихований вміст (міна / число 0–8) + стан поверх (закрита / відкрита / прапорець / знак питання).
- Час статичний: нічого не стається без кліку. Таймер (секунди, старт першим кліком, стеля 999) — лише міра результату.
- Розстановка — один раз на старті; у Windows — **після першого кліку** або з переносом міни, щоб перший клік був безпечним.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | — | приймає відкриття / прапорець / «?» |
| Число 1–8 | mark | n = кількість мін серед 8 сусідів | відкрита клітина-підказка; акорд по ній |
| Порожня клітина (0) | mark | n = 0 | відкриття → каскад відкриття сусідів |
| Міна | hazard | — | відкриття → програш; на перемозі — автопрапорець |
| Прапорець | mark | — | блокує відкриття клітини лівим кліком; −1 у лічильнику мін |
| Знак питання «?» | mark | опція Marks | нотатка «не певен»; відкривається звичайно |
| Вибухла міна | hazard | червоне тло | показує клітину, що вбила |
| Хибний прапорець | mark | хрест на міні | на програші — прапорець там, де міни не було |
| Кнопка-смайлик | static (UI) | стани 🙂 😮 😵 😎 | клік — нова гра; обличчя відбиває стан |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `first_time` → ТО `custom: «перенести міну»`: Win 3.1–XP — у першу вільну клітину верхнього рядка зліва; Vista+ — генерувати так, щоб `c` був нулем (гарантоване відкриття); далі як звичайне відкриття.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, flag)` → ТО `block`.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `lose`, `reveal(all_mines)`, `mark(wrong_flags, x)`, `timer(stop)`.
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` зі значенням `adjacent_count(c, mine)`.
- КОЛИ `after(reveal(c))` → ЯКЩО `adjacent_count(c, mine, ==, 0)` → ТО `reveal(neighbors8(c))` рекурсивно (flood fill; зупиняється на числах, прапорці не відкриває).
- КОЛИ `input(flag, c)` → ЯКЩО `cell(c, closed)` → ТО `mark(c, flag)`, `counter(mines_left, -1)`; повторно → `mark(c, ?)` (якщо Marks увімкнено) → ще раз → `unmark(c)`, `counter(mines_left, +1)`.
- КОЛИ `input(chord, n)` → ЯКЩО `adjacent_count(n, flag, ==, value(n))` → ТО `reveal(закриті незапрапорені сусіди n)`; ЯКЩО серед них міна (хибний прапорець) → ТО `lose`; ЯКЩО прапорців менше → ТО `custom: «лише підсвітити сусідів»`.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, opened)` (Tatham, minesweeper.online, Windows 7) → ТО як `chord` — «клік по числу = акорд».
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `win`, `mark(all_mines, flag)`, `timer(stop)`; ЯКЩО час < рекорду рівня → ТО `window(record-name-dialog)`.
- КОЛИ `input(open|flag, c)` → ЯКЩО `first_time` → ТО `timer(start)`; щосекунди `counter(time, +1)` до 999.
- Лічильник мін = міни − прапорці; може піти в мінус (прапорець не перевіряється).
- Перемога: усі безпечні клітини відкриті (прапорці не потрібні — стиль NF). · Поразка: відкрита міна. · Рахунок: час; на спортивних сайтах — 3BV/s та IOE.
- Метрики дошки (Minesweeper Authoritative): **3BV** = мінімум лівих кліків для розвʼязання = кількість «островів» нулів (кожна область відкриття = 1) + числа, що не межують з жодним відкриттям; **3BV/s** = 3BV / час; **IOE** = 3BV / усі кліки (акорди дають >1); **Correctness** = ефективні / усі кліки; **Throughput** = 3BV / ефективні кліки; **ZiNi** — мінімум кліків з прапорцями й акордами (жадібний / випадковий пошук).
- **Minesweeper Flags** (MSN Messenger 6.0, 2003): 16×16, 51 міна, двоє гравців по черзі; хід = відкрити клітину; знайшов міну — вона твоя (`score(+1)`) і ходиш знову (?); не влучив — хід переходить. КОЛИ `counter(my_mines, >=, 26)` → ТО `win`. Одна «бомба» на гравця відкриває 5×5, дозволена лише тому, хто програє.

## Керування і ввід
- Ліва кнопка — відкрити; права — цикл «прапорець → ? → порожньо»; обидві разом (або середня, або клік по числу в сучасних версіях) — акорд.
- «1.5-клік» спортсменів: тримати праву після прапорця, клікнути лівою число, відпустити обидві — акорд без зайвого кліку.
- Натиснута ліва кнопка «втискає» клітину під курсором (і 3×3 під акордом) — превʼю до відпускання; смайлик стає 😮.
- Клавіатура: F2 — нова гра (Windows); Tatham — стрілки для курсора, Enter = ліва, Space = права.
- Тач (Windows 8+, мобільні): перемикач «режим прапорця», довге натискання = прапорець.

## Вікна, меню, HUD
- `game-screen`: поле; зверху `remaining-counter` (міни − прапорці, семисегментні цифри зліва), `face-button` (смайлик по центру), `timer-elapsed` (праворуч).
- Меню Windows 3.1–XP: Game — New (F2), Beginner, Intermediate, Expert, Custom… → `custom-size-dialog` (Height, Width, Mines), Marks (?), Color, Sound, Best Times… → `leaderboard`, Exit · Help — Contents, `about-window`.
- `leaderboard` «Fastest Mine Sweepers»: по одному рекорду на складність з іменем, кнопка Reset Scores.
- `record-name-dialog` — після рекорду: «You have the fastest time for … level. Please enter your name.»
- Windows Vista/7: Game — New Game, Statistics → `stats-window` (зіграно, виграно, %, найдовші серії перемог/поразок, поточна серія, 5 найкращих часів), Options → `settings-window` (складність + custom, анімації, звуки, підказки, автозбереження, Allow question marks), Change Appearance → `theme-select` (міни / квіти «Flower Garden»), Exit.
- `end-screen` Windows 7: поразка — «Exit / Restart this game / Play again» (Restart повторює ту саму дошку); перемога — час, рекорд, статистика.
- Windows 8+ (Arkadium): `main-menu` — Classic 8×8, Easy 9×9, Medium 16×16, Expert 30×16, Custom, Adventure, Daily Challenges; Awards (`achievements-window`), Leaderboards, Statistics, Tutorials; теми Modern/Retro.
- Переходи: game-screen → (міна) поразка → клік смайлика → нова дошка; game-screen → (перемога) [record-name-dialog] → leaderboard.

## Фічі поза полем
- `difficulty-presets` + `custom-difficulty` (W, H, кількість мін) — канонічний приклад.
- `leaderboard-local` найкращих часів по складності; Windows 7 — `stats` і серії, `autosave` незавершеної гри («Always continue saved games»).
- `theme-select`: міни ↔ квіти (кампанія 1999–2001 проти «мінної» образності → «Flower Field»/«Flower Garden»).
- `sound-toggle`, `colorblind-palette`-попередник: Color ↔ чорно-біле.
- No-guess режими (Tatham «Ensure solubility», minesweeper.online NG з кнопкою підказки, Evil-дошки), `no-flags`-стиль (NF), рейтинги 3BV/s і мінімальний 3BV для рекордів (5 / 30 / 100).
- `mode-daily` і Adventure (Windows 8+), PvP-мультиплеєр (Minesweeper Flags, minesweeper.online).
- Tatham: `undo` після вибуху (лічильник смертей не зменшується), Solve, гекс/трикутні сітки з обгортанням (тор).

## Варіації й родичі
- Предки: Mined-Out (ZX Spectrum, 1983 — аватар іде мінним полем), Mines (SunOS, Tom Anderson, 1987). Клони для спорту: Minesweeper Arbiter, Minesweeper X, Viennasweeper.
- Осі варіацій:
  - **перший клік**: без захисту / безпечна клітина / безпечні 3×3 / гарантоване відкриття (Vista+);
  - **генерація**: випадкова / no-guess (перевірка солвером) / «злий» Kaboom (міна там, де вгадуєш) / «щасливий» LuckSweeper;
  - **топологія**: квадрат / гекс / трикутник / тор / сфера (Globesweeper) / 3D / 4D;
  - **підказка**: кількість сусідніх мін / сума рівнів (Mamono, Dragonsweeper) / лінійні суми (Hexcells, Voltorb Flip) / правила-модифікатори (14 Minesweeper Variants);
  - **кількість мін у клітині**: 1 / кілька;
  - **гравці**: соло / дуель на кількість мін (Flags) / кооператив.
- Паперовий родич — Tentaizu (усі підказки дано, єдиний розвʼязок) → межа з `pencil-logic`.
- Теорія: перевірка узгодженості дошки NP-повна (Kaye, 2000), розвʼязання узгодженої — co-NP-повне; нескінченний сапер Тюрінг-повний.

## Цікавинки для курсу
- Каскад нулів (flood fill BFS/DFS з зупинкою на числах) — 📎: класика рекурсії/черги.
- Безпечний перший клік — 🌱 (перенос міни) → 📎 (гарантоване відкриття: генерація після кліку з виключеною зоною 3×3).
- Акорд з перевіркою прапорців і цикл «прапорець → ? → порожньо» — 📎.
- Метрики дошки 3BV / IOE — 🥉: 3BV — зв'язні компоненти нулів + «острівні» числа; ZiNi — 🥈 (пошук мінімуму кліків).
- Солвер «простих» дедукцій (одна клітина, пари клітин через різницю множин) — 🥈; повний ймовірнісний солвер — 🥇.
- Генерація без вгадувань (згенерувати → прогнати солвер → перегенерувати/підправити) — 🥇.
- Дуель Minesweeper Flags (влучив — ходиш ще, бомба 5×5 лише тому, хто відстає) — 📎 поверх готового сапера.

## Мапа на каталог
- Є: `cell-click` ↔ відкриття · `chord-click` ↔ акорд · `mines-after-first-click` ↔ безпечний перший клік · `difficulty-levels` ↔ пресети · `game-settings` + `field-size-picker` ↔ Custom · `score-records` + `leaderboard` ↔ Best Times · `profile-stats` ↔ Statistics Windows 7 · `game-screen` · `end-screen` · `settings-window` · `help-window` · `about-window` · `theme-select` ↔ квіти/міни · `sound-effects` · `save-game` ↔ автозбереження Win7 · `completion-detection` ↔ всі безпечні відкриті · `daily-puzzle` ↔ Daily Challenges · `level-solver` + `difficulty-rating` ↔ no-guess і ZiNi.
- **Нема** → пропозиції карток:
  - `+flood-reveal` «Каскадне відкриття нулів» · levels/… або entities/interact · 📎 · слот {neighborhood: 4|8}.
  - `+neighbor-count-clue` «Число = кількість сусідів виду» · game-logic/constraints · 🌱 · слот {neighborhood: 4|8|hex}.
  - `+flag-cycle` «Цикл позначок клітини (прапорець/?/порожньо)» · interface/input · 🌱.
  - `+no-guess-generation` «Генерація без вгадувань» · levels/generation · 🥇 — дитина `unique-puzzle-generation`, але вимога слабша: розвʼязність логікою з точки старту.
  - `+board-metrics-3bv` «Метрики дошки (3BV, IOE)» · interface/results · 🥉.
  - `+mine-flag-race` «Дуель на знайдені міни (влучив — ходиш ще)» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+cond:flags_match` — кількість прапорців навколо числа = його значенню (умова акорду); через `adjacent_count` пишеться, але порівняння з власним значенням клітини — окрема форма.
- `+effect:flood_reveal` — рекурсивне відкриття від клітини до межі чисел; `reveal(cells)` не передає рекурсію.
- `+ui:face-button` — кнопка-смайлик: індикатор стану + рестарт в одному віджеті.
- `+ui:mine-counter` — лічильник «лишилось мін» = всього − позначки, може бути відʼємним (уточнення `remaining-counter`).
- `+window:custom-size-dialog` — діалог W/H/кількість мін; `+window:record-name-dialog` — ввести імʼя після рекорду.
- `+feature:no-guess` — гарантія розвʼязності логікою; `+feature:board-metrics` — 3BV/IOE/3BV/s; `+feature:no-flags-style` — гра без позначок, перемога лише відкриттям.

## Джерела
- ⭐ [Wikipedia: Minesweeper (video game)](https://en.wikipedia.org/wiki/Minesweeper_(video_game)) — правила, chord, перший клік і відкриття у Vista, пресети, клони, варіанти, складність.
- [Wikipedia: Microsoft Minesweeper](https://en.wikipedia.org/wiki/Microsoft_Minesweeper) — «?», Flower Garden, Windows 8/10 режими, Adventure, Daily Challenges.
- [Minesweeper Authoritative: How to play](https://minesweepergame.com/strategy/how-to-play-minesweeper.php) — керування, «?», Custom до 30×24 і (x−1)(y−1) мін.
- [Minesweeper Authoritative: Statistics](https://minesweepergame.com/statistics.php) — 3BV, 3BV/s, IOE, RQP, ZiNi, Correctness, Throughput.
- [Minesweeper Authoritative: First click](https://minesweepergame.com/strategy/first-click.php) — перенос міни у верхній рядок, гарантоване відкриття з Vista, шанси відкриття по позиціях.
- [minesweeper.online](https://minesweeper.online/) — гра, No guessing з підказкою, NF, мінімальні 3BV для рейтингу, PvP.
- [Simon Tatham's Mines](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mines.html) — Ensure solubility, undo після вибуху, гекс/трикутні сітки, обгортання.
- [Minesweeper Flags у базі ігор](https://minesweepergame.com/database/games.php?id=37) — 16×16, 51 міна, 26 для перемоги, бомба 5×5.
- YouTube: пошук «minesweeper expert world record».

## Непевне
- (?) Minesweeper Flags: «знайшов міну — ходиш знову» — з памʼяті й натяку джерела; база ігор прямо цього не каже.
- (?) Гарантоване відкриття: Wikipedia і minesweepergame кажуть Vista (і, відповідно, Windows 7); чи то нуль саме в клітині кліку чи «клітина без сусідніх мін» з її 3×3 — не перевірено.
- (?) Пункти меню Windows 3.1–XP і Windows 7 (Statistics, Options, Restart this game) — з памʼяті, не з джерела; межі Custom у Windows 7 (9–24 × 9–30, до 668 мін) не перевірені.
- (?) Стеля таймера 999 і старт таймера першим кліком — з памʼяті.
- (?) Клік по числу як акорд у Windows 7 — не перевірено (у Tatham і minesweeper.online — так).
