---
title: "Lexilotl: Crossword Puzzle Run"
slug: lexilotl
aka: [Lexilotl]
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: runtime
  goal: score
year: 2026
platforms: [PC, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4735750/Lexilotl_Crossword_Puzzle_Run/", best: true, note: "опис, How to play, фічі, 5 скриншотів і трейлер (HUD, клавіатура, «puzzle run over»)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lexilotl+crossword+puzzle+run+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [keyboard-controls, completion-detection, wrong-mark-lose, sequential-levels, score-records, game-screen, end-screen, main-menu, +hangman-letter-guess, +keyboard-state, +puzzle-run, +miss-refill-per-puzzle, +themed-crossword-gen]
proposes: ["+cond:in_answer", "+ui:on-screen-keyboard", "+ui:clue-display", "+ui:run-counter", "+card:hangman-letter-guess", "+card:puzzle-run", "+card:themed-crossword-gen"]
author: opus
date: 2026-11-09
---

# Lexilotl — «шибениця» на міні-кросворді: вгадана літера відкривається в усіх словах, три промахи — кінець забігу

## Суть
Гравцю показують порожній міні-кросворд і слово-тему («family», «rhyme»), до якої повʼязані всі слова сітки. Він вгадує по одній літері: влучна відкриває всі свої клітини в усіх словах одразу, промах забирає одну з трьох спроб-аксолотлів. Розвʼязав сітку, маючи хоч одну спробу, — спроби відновлюються і йде наступний кросворд; третій промах закінчує забіг. Ядро — шибениця, де перетини слів роблять кожну літеру ціннішою.

## Поле і час
- Квадратна сітка міні-кросворду з кількох слів, що перетинаються (зі скриншотів: 3–5 слів по 4–10 літер); навколо — декоративні силуети інших сіток.
- Пазли генеруються на льоту: між ними екран «making puzzle… get ready…».
- Хід = одна вгадана літера; таймера нема («you're not racing the clock»).
- Забіг = серія пазлів до третього промаху в межах одного пазла.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина слова | tile | прихована літера, стан hidden/revealed | відкривається, коли вгадано її літеру |
| Слово сітки | zone | 4–10 клітин, повʼязане з темою | розвʼязане, коли відкрито всі клітини; на мить показує своє слово підписом |
| Підказка-тема | static | одне слово (family, rhyme, manipulation…) | задає звʼязок між словами пазла |
| Клавіша літери | mark | стан: не пробувана / влучна (зелена) / промах (червона) | після спроби фарбується й показує історію |
| Аксолотль-спроба | pickup | 3 на пазл | зникає за кожен промах; відновлюються після розвʼязаного пазла |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «згенерувати міні-кросворд зі слів, повʼязаних із темою»`, `set_value(tries, 3)`, `message(topic)`.
- КОЛИ `input(letter)` → ЯКЩО `custom: «літера є хоч в одному слові сітки»` → ТО `reveal(all cells with letter)`, `paint(key, green)`, `score(custom: «за відкриті клітини»)`.
- КОЛИ `input(letter)` → ЯКЩО `custom: «літери нема в жодному слові»` → ТО `counter(tries, -1)`, `paint(key, red)`.
- КОЛИ `input(letter)` → ЯКЩО `custom: «літеру вже пробували»` → ТО `block`.
- КОЛИ `custom: «усі клітини слова відкрито»` → ТО `message(word)` — слово на мить підписується.
- КОЛИ `all_constraints_met` → ЯКЩО `counter(tries, >=, 1)` → ТО `counter(run, +1)`, `next_level`, `set_value(tries, 3)`.
- КОЛИ `counter(tries, ==, 0)` → ТО `game_over`, `window(end-screen)` — «puzzle run over», кнопка «ok».
- КОЛИ `game_over` → ЯКЩО `custom: «рахунок більший за рекорд»` → ТО `custom: «новий high і max»`.
- Перемога: нема — гра проти власного рекорду · Поразка: 3 промахи на одному пазлі · Рахунок: росте з довжиною забігу (формулу не знайдено).

## Керування і ввід
- Фізична клавіатура: натиснути літеру (є режим «лише клавіатура»).
- Миша або дотик: клік по клавіші екранної QWERTY-клавіатури (режими «лише миша» і «лише дотик»).
- Геймпад: часткова підтримка (DualShock / DualSense).
- Вгадування цілого слова — згадано в описі («letter and word guessing»), механізм не перевірено.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: логотип і кнопка «start».
- `loading-screen`: «making puzzle… get ready…» між пазлами.
- `game-screen`: сітка в центрі, `on-screen-keyboard` унизу з кольорами клавіш, `clue-display` (тема), `hi-score` («high»), `score`, `lives` (три аксолотлі «tries»), `run-counter` («run» — пазлів у забігу, «max» — найдовший забіг).
- `end-screen`: «puzzle run over» + «ok».
- Переходи: `main-menu` → `loading-screen` → `game-screen` → (розвʼязано) `loading-screen` → … → (3 промахи) `end-screen` → `main-menu` (?).

## Фічі поза полем
- `leaderboard-local`: high score і найдовший забіг (max run).
- `mode-endless`: забіг без кінця, доки є спроби.
- `mouse-and-keyboard`, `touch-controls`, `gamepad-support`: три окремі режими вводу.
- `music-toggle` / `sound-toggle`: «relaxing audio» (налаштування не перевірено).

## Варіації й родичі
- Родичі в корпусі: Wordle (`wordle.md`) — вгадування з кольорами клавіш; Fill-In (`fill-in.md`) і Wordscapes (`wordscapes.md`) — кросвордна сітка без класичних підказок; Codeword (`codeword.md`) — одна відкрита літера заповнює всі її клітини.
- Предок механіки — шибениця (Hangman): літера відкриває всі входження, ліміт промахів.
- **Осі варіацій:** що вгадуєш (літеру / слово) · скільки слів ділять літеру (одне / сітка з перетинами) · ліміт промахів (на пазл / на забіг) · підказка (тема / визначення / нема) · сесія (один пазл / забіг).

## Цікавинки для курсу
- Шибениця на сітці: множина прихованих літер, відкриття всіх входжень одним кроком — 🌱.
- Стан клавіатури з кольорами (як у Wordle) — 🌱.
- Забіг: відновлення спроб після кожного пазла, рахунок і рекорд довжини — 🌱.
- Генерація міні-кросворду зі слів на тему: укладання слів із перетинами — 🥇.
- Добір слів «на тему» (рими, синоніми, асоціації) зі словникової бази — 🥈.

## Мапа на каталог
- Є: `keyboard-controls` ↔ вгадування з клавіатури (і з екранної) · `completion-detection` ↔ сітку розвʼязано · `wrong-mark-lose` ↔ промахи забирають спроби · `sequential-levels` ↔ пазл за пазлом · `score-records` ↔ high / max · `game-screen` / `end-screen` / `main-menu`.
- **Нема** → пропозиції карток:
  - `+hangman-letter-guess` «Вгадування літер з лімітом промахів» · game-logic/lose · 🌱 · слоти {misses}.
  - `+keyboard-state` «Клавіатура з кольорами спроб» (є у Wordle) · interface/hud · 🌱.
  - `+puzzle-run` «Забіг: серія пазлів до першої поразки» · levels/progression · 🌱.
  - `+miss-refill-per-puzzle` «Спроби відновлюються після кожного пазла» (дитина попередньої) · levels/progression · 🌱.
  - `+themed-crossword-gen` «Генерація кросворду зі слів на тему» · levels/generation · 🥇.

## Пропозиції до словників
- `+cond:in_answer` — вгадана літера є в прихованій відповіді (шибениця, Lexilotl).
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами клавіш (Wordle, Lexilotl).
- `+ui:clue-display` — поточна підказка чи тема пазла.
- `+ui:run-counter` — довжина поточного забігу й рекорд.
- `+card:hangman-letter-guess`, `+card:puzzle-run`, `+card:themed-crossword-gen` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Lexilotl: Crossword Puzzle Run](https://store.steampowered.com/app/4735750/Lexilotl_Crossword_Puzzle_Run/) — How to play (одна літера — усі збіги, три промахи, спроби відновлюються), фічі, режими вводу, вихід 25.09.2026; скриншоти й трейлер — HUD, кольори клавіш, «puzzle run over».
- YouTube: пошук «Lexilotl crossword puzzle run gameplay».

## Непевне
- (?) Формула рахунку: за кожну відкриту клітину, за слово чи за пазл (на скриншотах score 8 і 22 на ранніх пазлах).
- (?) Чи можна вгадувати ціле слово («letter and word guessing» у короткому описі, але How to play каже лише про літери).
- (?) Розміри сіток і кількість слів у пазлі — лише зі скриншотів, офіційно не названі.
- (?) Чи складність росте з довжиною забігу («the longer your run… the more interesting words») і як саме.
- (?) Головне меню, налаштування й таблиці рекордів, окрім HUD-лічильників high/max, не видно в джерелах.
