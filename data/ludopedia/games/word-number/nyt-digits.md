---
title: Digits (The New York Times)
slug: nyt-digits
aka: [NYT Digits, Digits]
family: word-number
also: []
klass: puzzle
axes:
  field: 1d
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 2023
platforms: [web]
links:
  - {kind: other, url: "https://alexanderell.is/posts/digits/", best: true, note: "правила (лише додатні цілі, кожне число раз) і brute-force солвер на Python"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_New_York_Times_Games", note: "бета 10.04.2023 – закрито 08.08.2023; родич раунду чисел Countdown"}
  - {kind: other, url: "https://wordfinder.yourdictionary.com/blog/what-is-digits-a-daily-math-game", note: "зірки 25/10/0, ранги дня, Rewind, Reveal"}
  - {kind: other, url: "https://www.slashgear.com/1254567/wordle-nyt-game-beta/", note: "огляд бети: результат не дріб і не відʼємний, спроб без ліку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nyt+digits+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, daily-puzzle, completion-detection, undo-unlimited, level-solver, end-screen, game-screen, help-window, sequential-levels, +number-combine, +stars-by-distance, +daily-rank, +reveal-solution]
proposes: ["+cond:positive_integer", "+cond:distance", "+ui:operator-buttons", "+ui:stars-rating", "+ui:target-number", "+feature:reveal-penalty"]
author: opus
date: 2026-11-09
---

# Digits — склади з шести чисел і чотирьох дій якомога ближче до цілі

## Суть
Пʼять задач на день; у кожній — ціль і шість чисел. Гравець обирає число, операцію (+ − × ÷) і друге число: обидва зникають, на їхнє місце стає результат, який можна вживати далі. Мета — точно влучити в ціль (3 зірки) або хоча б підійти близько (1–2 зірки). По суті це раунд чисел з Countdown / «Des chiffres et des lettres» у вебоболонці NYT; існувала лише як бета (квітень–серпень 2023).

## Поле і час
- «Поле» — ряд із 6 плиток-чисел (1d); після кожної операції плиток стає на одну менше (до 1).
- Над рядом — ціль; під ним — 4 кнопки операцій.
- Час статичний; задачі дня — послідовно (п'ять «рівнів» складності), новий набір опівночі за східним часом США.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-число | tile | ціле додатне значення | вибирається; після операції зникає разом з парною |
| Плитка-результат | tile | значення a∘b | зʼявляється на місці операндів; далі — як звичайне число |
| Операція | static (UI) | + − × ÷ | застосовується до двох обраних плиток |
| Ціль | static | ціле число | порівнюється з кожною плиткою після операції |
| Задача дня | zone | 6 чисел + ціль, 0–3 зірки | 5 штук на день |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile)` → ТО `custom: «обрати перший операнд»`; далі `input(op)` → `input(click tile)` — другий операнд.
- КОЛИ `input(click tile b)` (a і op уже обрано) → ЯКЩО `positive_integer(a op b)` → ТО `merge(a, b → a op b)`.
- КОЛИ `input(click tile b)` → ЯКЩО `op == − and not positive_integer(a − b)` → ТО `block` (відʼємне / нуль заборонено).
- КОЛИ `input(click tile b)` → ЯКЩО `op == ÷ and not positive_integer(a ÷ b)` → ТО `block` (лише ділення націло).
- Кожне вихідне число — не більше одного разу; результат можна використати в наступній операції.
- КОЛИ `after(merge)` → ЯКЩО `same(result, target)` → ТО `custom: «задача розвʼязана на 3 зірки»`, `next_level`.
- КОЛИ `input(submit)` → ЯКЩО `distance(best tile, target) <= 10` → ТО `counter(stars, +2)`; ЯКЩО `<= 25` → `counter(stars, +1)`; інакше 0.
- КОЛИ `input(rewind)` → ТО `custom: «скасувати останню операцію: результат розпадається на операнди»` — навіть після submit.
- КОЛИ `input(reveal)` → ТО `custom: «показати оптимальний шлях»`, `custom: «задача отримує мінімальний бал»`.
- Спроб без ліку: можна перебирати, доки не здаси.
- КОЛИ `counter(puzzles_done, ==, 5)` → ТО `window(end-screen)` з рангом дня.
- Ранги за сумою зірок (макс 15): Beginner 0 · Moving Up 3 · Solid 6 · Nice 9 · Great 12 · Amazing 14 · Genius 15.
- Перемога: точний збіг · Поразки нема · Рахунок: 0–3 зірки на задачу, сума — ранг дня.

## Керування і ввід
- Тапи/кліки: число → операція → число. Кнопки Rewind (undo), Submit, Reveal.
- Опційний «chain mode» — результат операції лишається обраним для наступної (?).

## Вікна, меню, HUD
- `game-screen`: `target-number`, ряд плиток-чисел, `operator-buttons`, `stars-rating` поточної задачі, перемикач 5 задач, `undo-button` (Rewind), кнопки Submit/Reveal.
- `help-window`: правила (?).
- `end-screen`: зірки по 5 задачах і ранг дня (?) — точний вигляд не бачив.
- Переходи: задача 1 → … → 5 → `end-screen`.

## Фічі поза полем
- `daily-puzzle` (5 задач, однакові для всіх), `rank-tiers` (ранг дня скидається опівночі ET), `undo` (без ліку, Rewind), `show-solution` зі штрафом (Reveal).
- `share-result`, `streaks` — не підтверджено (?).

## Варіації й родичі
- Раунд чисел Countdown / «Des chiffres et des lettres» — той самий пазл з таймером 30 с і вибором «великих» і «малих» чисел.
- Гра «24» (чотири числа → 24), Krypto (картки).
- Nerdle (`nerdle.md`) — арифметика в Wordle-оболонці; Mathable (`mathable.md`) — рівності на полі.
- **Осі варіацій:** кількість чисел (4 / 6) · дозволені операції (± лише / + дужки / степінь) · обмеження результату (лише додатні цілі / будь-які раціональні) · оцінка (точно / близькість зірками / час) · кількість задач на день.

## Цікавинки для курсу
- Операція над двома плитками з валідацією «додатне ціле» + undo-стек — 🌱.
- Зірки за близькістю (найкраща плитка після submit) і ранг дня — 🌱.
- Brute-force солвер: рекурсія по впорядкованих парах і операціях; ~777 000 підзадач для 6 чисел — 🥉.
- Прунінг солвера: канонічний порядок для + і ×, пропуск ×1 і ÷1, мемо станів — 🥈.
- Генератор задач дня з оцінкою складності (кількість розвʼязків, мінімум операцій) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `daily-puzzle` · `completion-detection` ↔ точний збіг · `undo-unlimited` ↔ Rewind · `level-solver` ↔ Reveal / солвер · `sequential-levels` ↔ 5 задач дня · `game-screen` · `help-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+number-combine` «Обʼєднати дві плитки-числа операцією» · entities/legality · 📎 · слоти {ops: list, integer_only: bool}.
  - `+stars-by-distance` «Зірки за близькістю до цілі» · game-logic/score · 🌱 · слоти {thresholds: list}.
  - `+daily-rank` «Ранг дня за сумою зірок» · interface/results · 🌱.
  - `+reveal-solution` «Показати розвʼязок ціною балу» · game-logic/difficulty · 📎.

## Пропозиції до словників
- `+cond:positive_integer` — результат операції ціле і > 0 (Digits, Countdown).
- `+cond:distance` — відстань значення до цілі ≤ N (зірки Digits).
- `+ui:operator-buttons` — панель операцій + − × ÷.
- `+ui:stars-rating` — зірки поточної задачі (Digits, Waffle).
- `+ui:target-number` — ціль, з якою порівнюється кожен результат.
- `+feature:reveal-penalty` — показ розвʼязку з мінімальною оцінкою задачі.

## Джерела
- ⭐ [Alex Ell: Digits](https://alexanderell.is/posts/digits/) — правила (лише додатні цілі, ділення націло, кожне число раз), 5 задач на день, солвер і статистика розвʼязків.
- [Wikipedia: The New York Times Games](https://en.wikipedia.org/wiki/The_New_York_Times_Games) — бета з 10.04.2023, закрито 08.08.2023, подібність до Countdown.
- [YourDictionary: What Is Digits](https://wordfinder.yourdictionary.com/blog/what-is-digits-a-daily-math-game) — пороги зірок 25/10/0, ранги, Rewind, chain mode, Reveal.
- [SlashGear, 2023](https://www.slashgear.com/1254567/wordle-nyt-game-beta/) — бета без застосунку, спроб без ліку.
- YouTube: пошук «nyt digits gameplay».

## Непевне
- (?) Ширина 1d і точний вигляд HUD — з опису, сам екран не бачив (гру закрито).
- (?) Chain mode — як саме працює; джерело описує лише одним рядком.
- (?) Чи був share-текст і серії днів.
- (?) Поріг «0 зірок» — лише якщо здаєшся, чи також далі 25 від цілі.
