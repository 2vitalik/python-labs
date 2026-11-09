---
title: Overwords
slug: overwords
aka: ["Overwords: Calm Word Puzzle", "Overwords: Infinity"]
family: word-number
also: [thinky]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: partial
  random: none
  goal: state
year: 2025
platforms: [PC, Mac, Linux, iOS, Android, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3902010/Overwords/", best: true, note: "опис («Overlap words. Grow the board.»), 30 рівнів, 5 скриншотів і трейлер з кількома ходами"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.rt.overthewords&hl=en", note: "Google Play: «crossword you build yourself», без таймерів і очок, офлайн"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.rt.overwordsinfinity&hl=en", note: "Overwords: Infinity — безкінечний режим з онлайн-рекордами, 10 досягнень"}
  - {kind: itch, url: "https://targaciej.itch.io/overwordsinfinity", note: "веб-бета Infinity; коментарі: «можна грати поверх літер», «гра просить обрати, де поставити нову клітину»"}
  - {kind: official, url: "http://rainbowtrain.eu", note: "сайт автора (Maciej Targoni: Hook, Klocki, Zerko); новини про запуск"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Overwords+Maciej+Targoni+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [next-queue, completion-detection, no-moves-left, sequential-levels, restart-level, leaderboard, achievements-window, game-screen, +overlap-fuse-letters, +grow-board-cell, +given-word-queue, +letter-wear-clear]
proposes: ["+ui:growth-dots", "+ui:word-queue", "+card:overlap-fuse-letters", "+card:grow-board-cell", "+card:given-word-queue"]
author: opus
date: 2026-11-09
---

# Overwords — клади слова поверх слів: збіглі літери зварюються, двічі перекриті зникають, а поле доростає клітина за клітиною

## Суть
Мінімалістичний пазл Мацея Таргоні: на маленькому полі з кількох клітин треба по черзі розмістити всі слова зі списку рівня. Слово можна покласти поверх уже вписаних літер, якщо вони збігаються, — «як кросворд, що будуєш сам». Перекриті літери змінюють стан, а повторно перекриті звільняють клітину; між ходами поле росте на клітину в обране гравцем місце. Ядро — планування накладань у тісному просторі, щоб останні слова ще мали куди лягти.

## Поле і час
- Квадратна сітка без фіксованої рамки: старт — кілька клітин (у трейлері — 4: ряд із 3 і одна над серединою), довкола — білі точки, де поле може вирости.
- Поле росте від ходу до ходу: нова клітина зʼявляється на місці однієї з точок (за коментарем на itch — гравець обирає, де).
- Хід = розмістити одне слово зі списку. Таймерів і очок нема (Google Play: «No timers, no scores»).
- Рівень = черга слів; використані показуються рисками над списком. Overwords: Infinity — без рівнів, поле росте, доки є куди класти слова.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітина | terrain | — | приймає будь-яку літеру |
| Літера (чорна) | tile | буква, покладена один раз | може бути перекрита тією ж буквою |
| Зварена літера (синя) | tile | буква, перекрита один раз | повторне перекриття тією ж буквою звільняє клітину (з трейлера) |
| Точка росту | zone | місце біля краю поля | стає новою клітиною, коли поле росте |
| Слово зі списку | piece | 3–5 літер у прикладах | обирається стрілками ▸◂ і кладеться на поле |
| Список слів рівня | spawner | 1–4 видимих слова + риски використаних | після ходу інколи додає нові слова (у трейлері: BAT/CAB/CAT → TAB → HAT/CAR) |
| Червона клітина | hazard | (?) | видна на одному скриншоті посеред слова; значення не встановлено |
| Хрестик | static | на місці точок росту | зʼявляється, коли хід неможливий (скриншот «глухого кута») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «стартове поле з кількох клітин, точки росту довкола, черга слів рівня»`.
- КОЛИ `input(select word)` → ТО `custom: «слово виділяється стрілками ▸◂ у списку»`.
- КОЛИ `input(place word)` → ЯКЩО `custom: «кожна літера лягає на клітину поля, ланцюжком сусідніх клітин»` and `custom: «зайнята клітина під літерою містить ту саму букву»` → ТО `place(player, word)`; інакше `block`.
- КОЛИ `after(place)` → ЯКЩО `free(cell)` → ТО `mark(cell, letter)` — нова чорна літера.
- КОЛИ `after(place)` → ЯКЩО `same(letter, cell_letter, letter)` and `state(cell, plain)` → ТО `set_state(cell, fused)` — літера синіє.
- КОЛИ `after(place)` → ЯКЩО `same(letter, cell_letter, letter)` and `state(cell, fused)` → ТО `unmark(cell)` — клітина знову порожня.
- КОЛИ `after(place)` → ЯКЩО `custom: «настав момент росту»` → ТО `choose(growth dot)`, `set_cell(dot, cell)`.
- КОЛИ `after(place)` → ТО `custom: «слово йде з черги; черга може поповнитись новими словами»`.
- КОЛИ `no_moves(player)` → ТО `custom: «решта слів перекреслена, місця росту — хрестики»`, `restart`.
- КОЛИ `custom: «черга слів рівня вичерпана»` → ТО `win`, `next_level`.
- КОЛИ `level_start` → ЯКЩО `mode(infinity)` → ТО `custom: «рівнів нема; гра триває, доки знаходяться слова, що влазять; рахунок — в онлайн-рекорди»`.
- Перемога: розмістити всі слова рівня · Поразка: глухий кут, рестарт рівня · Рахунок: нема (в Infinity — high score).

## Керування і ввід
- Обрати слово зі списку (стрілки ▸◂ біля вибраного), потім показати, куди його покласти; точний жест (drag чи кліки по клітинах) не встановлено.
- Обрати точку росту, коли гра пропонує нову клітину.
- Меню — кнопка ☰ у правому верхньому куті.

## Вікна, меню, HUD
- `game-screen`: поле в центрі, `word-queue` унизу (риски використаних + видимі слова), `growth-dots` довкола поля, значок прогресу вгорі (сітка квадратиків, що заповнюються, ?), кнопка ☰.
- `end-screen`-стан глухого кута: темний фон, перекреслені слова, хрестики замість точок росту.
- `level-select` / `pause-menu` за ☰ — не перевірено.
- Переходи: `game-screen` → (усі слова розміщено) → наступний рівень · (глухий кут) → рестарт.

## Фічі поза полем
- `levels-sequential`: 30 рівнів у Overwords, «free updates ahead».
- `mode-endless`: окрема гра Overwords: Infinity — безкінечне поле, `leaderboard-online`, 10 досягнень, безкоштовна.
- `achievements`: Steam Achievements в Overwords.
- `theme-select`: кольоровий фон змінюється від рівня до рівня (зі скриншотів, ?).

## Варіації й родичі
- **Overwords** (2025): 30 рівнів, без очок. **Overwords: Infinity** (2026): нескінченний режим з рекордами, Steam, мобільні, веб-бета на itch.
- Родичі в корпусі: Upwords (`upwords.md`) — літеру кладуть поверх літери, стос до 5; Scrabble (`scrabble.md`) — перетини слів; Bonza (`bonza.md`) — кросворд, складений з фрагментів; Fill-In (`fill-in.md`) — розставити список слів у сітку.
- **Осі варіацій:** що буває з перекритою літерою (стос / зварювання / зникнення) · як росте поле (фіксоване / за вибором гравця / за правилом) · список слів (заданий рівнем / власні слова / генерований) · мета (розмістити всі / протриматись якнайдовше).

## Цікавинки для курсу
- Стан клітини «порожня → літера → зварена → порожня» як маленький автомат — 🌱.
- Перевірка розміщення слова ланцюжком сусідніх клітин зі збігом літер — 📎 (пошук шляху DFS).
- Ріст поля в обрану точку: динамічна множина клітин без рамки — 📎.
- Детектор глухого кута: чи лягає хоч одне слово з черги кудись на поле — 🥉.
- Дизайн рівня: черга слів, що гарантовано розвʼязна, — 🥇 (пошук із відкатом).

## Мапа на каталог
- Є: `next-queue` ↔ черга слів рівня · `completion-detection` ↔ усі слова розміщено · `no-moves-left` ↔ глухий кут · `sequential-levels` ↔ 30 рівнів · `restart-level` ↔ після глухого кута · `leaderboard` ↔ рекорди Infinity · `achievements-window` ↔ досягнення · `game-screen`.
- **Нема** → пропозиції карток:
  - `+overlap-fuse-letters` «Слово лягає поверх наявних літер, якщо вони збігаються» · entities/interact · 📎.
  - `+letter-wear-clear` «Повторно перекрита літера звільняє клітину» (дитина попередньої) · entities/state · 🌱.
  - `+grow-board-cell` «Поле росте на клітину в обране гравцем місце» · levels/generation · 📎 · слоти {when}.
  - `+given-word-queue` «Рівень — задана черга слів для розміщення» · levels/format · 🌱.

## Пропозиції до словників
- `+ui:growth-dots` — точки біля краю поля, куди воно може вирости.
- `+ui:word-queue` — список слів до розміщення з позначкою вибраного й рисками використаних.
- `+card:overlap-fuse-letters`, `+card:grow-board-cell`, `+card:given-word-queue` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Overwords](https://store.steampowered.com/app/3902010/Overwords/) — «Pick a word, place it on the board, and let overlapping letters fuse into new words», 30 рівнів; скриншоти й 28-секундний трейлер (BAT → CAB → CAT → TAB → HAT/CAR).
- [Google Play: Overwords: Calm Word Puzzle](https://play.google.com/store/apps/details?id=com.rt.overthewords&hl=en) — «a bit like a crossword you build yourself», без таймерів і очок.
- [Google Play: Overwords: Infinity](https://play.google.com/store/apps/details?id=com.rt.overwordsinfinity&hl=en) — безкінечний сиквел, онлайн-рекорди, 10 досягнень.
- [itch.io: Overwords Infinity](https://targaciej.itch.io/overwordsinfinity) — веб-бета; коментарі гравців про гру поверх літер і вибір місця нової клітини.
- [rainbowtrain.eu](http://rainbowtrain.eu) — сайт автора, новини про запуск.
- YouTube: пошук «Overwords Maciej Targoni gameplay».

## Непевне
- (?) Автомат «чорна → синя → порожня» виведено з кадрів трейлера (CAB зварює B і A; CAT стирає синю A; TAB стирає сині B і T); чи це загальне правило — не підтверджено текстом.
- (?) Форма розміщення: у трейлері CAB лягло «гачком» (C над A, далі B ліворуч), TAB — прямо справа наліво; чи дозволено будь-який ланцюжок сусідніх клітин, чи лише певні форми.
- (?) Коли саме поле росте (після кожного слова, після зварювання, за лічильником-значком угорі) і хто обирає місце.
- (?) Звідки беруться нові слова в черзі посеред рівня і чи видно їх наперед (`info: partial` — з рисок над списком).
- (?) Значення червоної клітини й хрестиків; чи є undo і вибір рівня в меню ☰.
- (?) Рік Infinity: Steam-реліз «17.03» з новин автора, веб-бета з 2026 — рік виведено з дат itch і Google Play.
