---
title: Tiled Words
slug: tiled-words
aka: []
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [web]
links:
  - {kind: official, url: "https://tiledwords.com/how-to-play", best: true, note: "як грати: drag, tap-поворот, Shuffle, до 3 reveal на пазл, практичний пазл"}
  - {kind: play, url: "https://tiledwords.com/puzzles/practice", note: "практичний пазл «Fruits»: 4 підказки Across/Down з довжинами"}
  - {kind: official, url: "https://tiledwords.com/", note: "щоденний пазл, Past Puzzles, Player Puzzles, Feedback; приєднується до Blue Ox Family Games"}
  - {kind: other, url: "https://paulmakeswebsites.com/writing/six-months-of-tiled-words/", note: "автор: профіль зі streak і найшвидшим/найповільнішим, акаунти й синхронізація, гравцеві набори підказок"}
  - {kind: other, url: "https://paulmakeswebsites.com/writing/a-month-of-tiled-words/", note: "автор: запуск 19 жовтня, створення пазла 20 хв – 2 год, плани (злиття плиток, конструктор)"}
  - {kind: other, url: "https://hn.svelte.dev/item/45750789", note: "Show HN від автора: «tile-placing board game mechanics + crosswords», натхнення Patchwork"}
  - {kind: other, url: "https://notes.hamatti.org/Gaming/Video-games/Word-Games", note: "огляд гравця: шматки-тетроміно, 3 reveal, «правильне слово не тими шматками», статистика дня"}
  - {kind: other, url: "https://thinkygames.com/news/solve-jigsaw-puzzles-made-of-crosswords-in-the-fresh-daily-puzzle-game-tiled-words/", note: "новина Thinky Games (403 у фетчі)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tiled+Words+daily+puzzle", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [drag-drop-piece, tile-rotate, polyomino-placement, completion-detection, daily-puzzle, level-bank, streak-stats, share-result, stats-window, profile-stats, save-progress, confirm-dialog, help-window, game-screen, end-screen, +crossword-fragments, +clue-list, +across-down-entry, +hint-reveal-word, +shuffle-board, +right-word-wrong-pieces, +user-puzzles]
proposes: ["+cond:matches_solution", "+cond:answer_spelled", "+feature:hint-reveal-word", "+feature:shuffle-tiles", "+ui:clue-list", "+card:crossword-fragments", "+card:right-word-wrong-pieces"]
author: opus
date: 2026-11-09
---

# Tiled Words — кросворд порізано на плитки: обертай і складай шматки, доки слова не зійдуться з підказками

## Суть
Щоденний вебпазл: готовий тематичний кросворд розрізано на невеликі плитки з літерами (по 2–4 клітини), які лежать розкиданими. Гравець перетягує плитки й обертає їх тапом, щоб у рядках і стовпцях прочитались відповіді на підказки Across/Down (у кожної — довжина слова). Автор описує гру як «механіку викладання плиток з настільних ігор на кшталт Patchwork + кросворд». На відміну від Bonza, підказка є до кожного слова, а плитки обертаються.

## Поле і час
- Квадратна сітка-стіл, на якій лежать плитки; розмір не вказано (автор планував зробити її «менш тісною»), кнопка Shuffle — коли бракує місця.
- Розвʼязок — кросворд з перетинами; практичний пазл «Fruits»: 4 слова (6, 6, 5, 5 літер), а літер на плитках — 19, тобто 3 перетини (?).
- Плитка — поліоміно з літерою в кожній клітині; поворот змінює розташування літер.
- Час статичний: таймер іде лише для статистики (час розвʼязання на екрані підсумку).
- Новий пазл щодня опівночі за тихоокеанським часом; архів минулих пазлів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-фрагмент | tile | 2–4 клітини з літерами, форма, орієнтація | тягнеться цілком; тап — поворот |
| Клітина-літера | mark | символ | частина плитки; належить 1–2 словам розвʼязку |
| Підказка | static | напрямок Across/Down, текст, довжина | у списку; поруч іконка reveal |
| Розвʼязок | static | розміщення слів кросворду (приховане) | з ним порівнюється складене |
| Reveal | resource | до 3 на пазл | відкриває слово підказки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «плитки розкидано по полю; показано список підказок Across/Down з довжинами»`.
- КОЛИ `input(drag tile)` → ЯКЩО `free(target_cells)` (?) → ТО `move(tile, to)`.
- КОЛИ `input(tap tile)` → ТО `rotate(tile, 90)` — літери на плитці змінюють розташування.
- КОЛИ `input(shuffle)` → ТО `custom: «плитки перерозкладаються, звільняючи місце»`.
- КОЛИ `after(move | rotate)` → ЯКЩО `custom: «суміжні плитки утворюють відповідь підказки в її напрямку так, як у розвʼязку»` → ТО `custom: «слово зʼєднано»` (?).
- КОЛИ `after(move | rotate)` → ЯКЩО `custom: «відповідь прочитано, але складено не тими плитками»` → ТО `message(«right word, wrong pieces»)`, `reveal(word)` — щоб гравець не забув слово.
- КОЛИ `input(reveal icon)` → ЯКЩО `counter(reveals, <, 3)` → ТО `window(confirm-dialog)`; Reveal → `reveal(word)`, `counter(reveals, +1)`; Cancel → нічого.
- Відкрите слово ще треба викласти з плиток на полі.
- КОЛИ `input(reveal icon)` → ЯКЩО `counter(reveals, ==, 3)` → ТО `block`.
- КОЛИ `all_constraints_met` (усі слова кросворду складено) → ТО `win`, `timer(stop)`, `window(end-screen)` з часом і кількістю reveal, `counter(streak, +1)`.
- Перемога: кросворд зібрано · Поразки нема · Рахунку нема; метрики — час і використані reveal; серія днів поспіль.

## Керування і ввід
- Миша або тач: drag плитки — перемістити; тап/клік — повернути.
- Іконка біля підказки — reveal (з підтвердженням).
- Посилання «Shuffle tiles» — перерозкласти плитки, коли тісно.
- Клавіатури нема: літери вже на плитках, змінюється лише розташування й орієнтація.

## Вікна, меню, HUD
- `help-window` (How to Play): анімовані Drag / Tap to spin / Shuffle / Reveal; кнопки «Play a practice puzzle» і «Skip to the daily puzzle».
- `game-screen`: назва пазла й рівень («Daily Puzzle — Silver»), автор і редактор пазла, поле з плитками, `clue-list` Across/Down з довжинами й іконками reveal, «Shuffle tiles».
- `confirm-dialog`: «Would you like to reveal the word?» · Reveal / Cancel · «You can reveal up to 3 words per puzzle».
- `end-screen` / `stats-window`: час розвʼязання, кількість reveal, Share, форма відгуку.
- `profile-window`: поточна й найдовша серія, кількість розвʼязаних, найшвидший і найповільніший пазл; акаунт для синхронізації.
- `puzzle-select`: Past Puzzles (архів за датами) і Player Puzzles.
- `toast` / банер: «Important Updates» про зміну збереження прогресу.
- Переходи: How to Play → практичний або щоденний пазл → `end-screen` → профіль / архів.

## Фічі поза полем
- `daily-puzzle` (ручна робота авторів, тематичний) + архів (`puzzle-bank`).
- `streaks` + `stats` + `share-result`.
- `hint-reveal-word`: до 3 відкриттів слова на пазл.
- `cloud-save`: акаунти й синхронізація між пристроями; раніше прогрес і серія жили на пристрої.
- `user-levels-browser`: Player Puzzles — набори підказок від гравців, з яких автори зробили пазли (прийом заявок закрито).
- Практичний пазл для новачків; рівні складності щоденних (?).

## Варіації й родичі
- `bonza.md` — найближчий родич: кросворд на фрагментах, але одна тема без підказок до слів і без повороту.
- `cross-figure.md`, `cryptic-crossword.md`, `arrowword.md` — класичні кросворди з підказками, де вписуєш літери, а не складаєш шматки.
- `waffle.md` — переставлення літер до правильних слів; Patchwork (board-digital) — поворот і викладання поліоміно.
- **Осі варіацій:** підказки (одна тема / до кожного слова) · поворот (нема / є) · розмір шматка (1 клітина = анаграма / 2–4 / великі) · злипання правильних шматків (нема / є) · допомога (reveal слова / ліміт 3 / за валюту).

## Цікавинки для курсу
- Drag поліоміно-плитки з привʼязкою до сітки й поворот на 90° (поворот координат клітин навколо опори) — 📎.
- Перевірка «слово складено як у розвʼязку» за відносним зсувом і орієнтацією плиток — 🥉.
- Розрізнення «правильне слово, не ті шматки» від повної відповідності — 📎.
- Різання кросворду на поліоміно 2–4 клітини так, щоб розвʼязок був однозначний — 🥈.
- Щоденний пазл, серія днів і статистика (час, reveal) з поділитися — 📎.
- Shuffle: перерозкласти N поліоміно на вільному полі без перекриттів — 🥉.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ перетягування плиток · `tile-rotate` ↔ тап-поворот · `polyomino-placement` ↔ плитки-поліоміно на сітці · `completion-detection` ↔ кросворд зібрано · `daily-puzzle` · `level-bank` ↔ Past Puzzles · `streak-stats` / `share-result` / `stats-window` / `profile-stats` ↔ серія, Share, час, профіль · `save-progress` ↔ прогрес і акаунти · `confirm-dialog` ↔ підтвердження reveal · `help-window` / `game-screen` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+crossword-fragments` — див. `bonza.md`; тут слот {rotate: true, piece_size: 2–4}.
  - `+clue-list`, `+across-down-entry` — див. `cross-figure.md`.
  - `+hint-reveal-word` — див. `bonza.md`; тут ліміт 3 на пазл і відкрите слово ще треба скласти.
  - `+shuffle-board` — перерозкласти елементи поля (див. сімʼю).
  - `+right-word-wrong-pieces` «Правильне слово, складене не тими шматками, — підказка-відкриття» · game-logic/constraints · 📎.
  - `+user-puzzles` «Пазли з наборів підказок від гравців» · levels/bank · 📎.

## Пропозиції до словників
- `+cond:matches_solution` — відносне положення й орієнтація плиток збігаються з розвʼязком (Bonza, Tiled Words).
- `+cond:answer_spelled` — у лінії прочитано відповідь підказки, байдуже якими плитками.
- `+feature:hint-reveal-word` — відкрити слово підказки, з лімітом на пазл.
- `+feature:shuffle-tiles` — перерозкласти плитки на полі, коли бракує місця.
- `+ui:clue-list` — список підказок Across/Down з довжинами й іконками дії.
- `+card:crossword-fragments`, `+card:right-word-wrong-pieces` — див. «Мапа на каталог».

## Джерела
- ⭐ [Tiled Words: How to Play](https://tiledwords.com/how-to-play) — мета, drag, tap-поворот, Shuffle, reveal ≤ 3 з діалогом, приклад-пазл «Animals», вхід у практичний і щоденний пазл.
- [Tiled Words: практичний пазл](https://tiledwords.com/puzzles/practice) і [щоденний пазл](https://tiledwords.com/puzzles/daily) — підказки з довжинами, «Daily Puzzle — Silver», автор і редактор пазла, кнопки.
- [Paul Makes Websites: Six Months of Tiled Words](https://paulmakeswebsites.com/writing/six-months-of-tiled-words/) — профіль і статистика, акаунти, гравцеві набори підказок.
- [Paul Makes Websites: A Month of Tiled Words](https://paulmakeswebsites.com/writing/a-month-of-tiled-words/) — запуск, форма відгуку після пазла, плани.
- [Show HN (дзеркало)](https://hn.svelte.dev/item/45750789) — опис автора, Patchwork як натхнення.
- [Hamatti: Word Games](https://notes.hamatti.org/Gaming/Video-games/Word-Games) — тетроміно-шматки, 3 reveal, «правильне слово не тими шматками», статистика дня.
- [Forking Mad: 100 days of Tiled Words](https://forkingmad.bearblog.dev/100-tiledwords/) — плитки по 2–3 літери, серія без логіну на пристрої, Share.
- YouTube: пошук «Tiled Words daily puzzle».

## Непевне
- (?) Розмір шматків: один огляд — «2–3 літери», інший — «тетроміно»; записано 2–4.
- (?) Що відбувається, коли слово складено правильно: злипання плиток, позначка підказки, підсвітка — не перевірено; «злиття плиток при правильному слові в неправильному напрямку» автор лише планував.
- (?) Чи може плитка лягти поверх іншої / за межі поля; крок повороту 90° — з «tap to spin», точний кут не названо.
- (?) «Silver» у назві щоденного пазла — схоже на рівень складності (Bronze/Silver/Gold?), але шкалу не бачив.
- (?) Формат Share-тексту; чи видно таймер під час гри.
- (?) Перехід до Blue Ox Family Games: що зміниться — не сказано.
