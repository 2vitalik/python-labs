---
title: Countdown — numbers round / Countle
slug: countdown-numbers
aka: [Countdown numbers game, Numbers round, Countle, Des chiffres et des lettres, Le compte est bon, Цифровий раунд Countdown]
family: word-number
also: []
klass: puzzle
axes:
  field: 1d
  time: realtime
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 1982
platforms: [TV, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Countdown_(game_show)", best: true, note: "раунд чисел: 24 плитки (20 малих 1–10 ×2, 4 великі 25/50/75/100), 0–4 великих, ціль 100–999 від CECIL, 30 с, очки 10/7/5; французький оригінал"}
  - {kind: play, url: "https://www.countle.org/", note: "Countle — щоденна версія (JS-сторінка)"}
  - {kind: other, url: "https://incoherency.co.uk/countdown/posts/countle-solver-is-live", note: "Countle: 6 чисел, ціль, 4 дії; солвер з точними й найближчими розвʼязками, share"}
  - {kind: other, url: "https://incoherency.co.uk/countdown/pages/", note: "правила раунду чисел, вибір 0–4 великих, солвер і ймовірності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=countdown+numbers+round", note: "пошук; раунди з ТБ"}
stage: v1
coverage: 70
mechanics: [cell-click, move-timer, time-out, event-points, simultaneous-versus, hot-seat, level-solver, daily-puzzle, share-result, undo-step, game-screen, end-screen, help-window, mode-select, +number-combine, +stars-by-distance, +large-small-draw, +closest-wins, +random-target]
proposes: ["+cond:positive_integer", "+cond:distance", "+ui:target-number", "+ui:operator-buttons", "+feature:declare-and-verify", "+card:large-small-draw"]
author: opus
date: 2026-11-09
---

# Countdown, раунд чисел — шість плиток і чотири дії: за 30 секунд підійди до трицифрової цілі ближче за суперника

## Суть
Гравець у контролі обирає, скільки «великих» чисел (0–4) узяти; решту з шести добирають «малі». Машина CECIL генерує ціль 100–999, і обидва учасники 30 секунд комбінують числа діями + − × ÷ (лише цілі додатні проміжні результати, кожна плитка — не більше разу, усі шість не обовʼязкові). Хто ближче — отримує очки за близькість. Countle (2022) — щоденна вебверсія: однакові шість чисел і ціль для всіх. Відмінності від [nyt-digits.md](nyt-digits.md): вибір складу «великі/малі», трицифрова випадкова ціль, жорсткий таймер і суперник, оцінка 10/7/5 замість зірок і п'яти задач на день.

## Поле і час
- «Поле» — ряд із 6 плиток-чисел (1d) + ціль; на ТБ плитки лежать у чотирьох рядах, великі — у верхньому.
- Пул: 24 перевернуті плитки — 20 малих (по дві 1–10) і 4 великі (25, 50, 75, 100); після раунду пул відновлюється повністю.
- Час: 30 с на ТБ (45 с у Des chiffres et des lettres); Countle — без таймера (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мала плитка | tile | 1–10, кожне ×2 у пулі | вживається ≤1 разу |
| Велика плитка | tile | 25 · 50 · 75 · 100 | кількість (0–4) обирає гравець у контролі |
| Результат операції | tile | ціле > 0 | заміщує два операнди; можна вживати далі |
| Ціль | static | 100–999, випадкова | генерує CECIL; порівнюється з відповіддю |
| Учасник | player | очки | оголошує число й показує обчислення |
| Таймер | static | 30 с | після нього нові обчислення не приймаються |
| Пул плиток | container | 24 плитки | відновлюється після раунду (на відміну від літер) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `choose(large count 0–4)`; `custom: «тягнуть 6 плиток: обрану кількість великих, решту — малі»`.
- КОЛИ `after(choose)` → ТО `spawn_at(target, board)` — випадкове 100–999, `timer(start 30s)`.
- КОЛИ `input(a op b)` → ЯКЩО `custom: «результат цілий і > 0»` → ТО `merge(a, b → a op b)`.
- КОЛИ `input(a − b | a ÷ b)` → ЯКЩО `custom: «відʼємне, нуль або дріб»` → ТО `block`.
- Кожну плитку — не більше, ніж вона є на дошці; усі шість не обовʼязкові.
- КОЛИ `tick` → ЯКЩО `timer(left, ==, 0)` → ТО `custom: «учасники оголошують число; пізня відповідь — 0»`.
- КОЛИ `input(declare)` → ЯКЩО `custom: «обчислення з помилкою»` → ТО `score(0)`.
- КОЛИ `level_end` → ЯКЩО `custom: «результат = ціль»` → ТО `score(10)`.
- КОЛИ `level_end` → ЯКЩО `custom: «відстань до цілі 1–5»` → ТО `score(7)`; ЯКЩО `custom: «6–10»` → ТО `score(5)`; далі — 0.
- Очки отримує лише найближчий; однаково близькі — обидва (`draw` за раунд).
- КОЛИ `level_end` → ЯКЩО `custom: «ніхто не влучив точно»` → ТО `custom: «асистент показує розвʼязок»` (у вебверсіях — солвер).
- Countle: КОЛИ `input(a op b)` → ТО як вище; КОЛИ `custom: «є плитка = ціль»` → ТО `win`, `custom: «результат для share»` (?).
- Перемога: більше очок за гру (ТБ) / влучити в ціль (Countle) · Поразка: менше очок · Рахунок: 10 / 7 / 5 / 0 за близькість.

## Керування і ввід
- ТБ: на папері; оголосити число, потім продиктувати обчислення.
- Цифрова версія (Countle та ін.): тап число → операція → число; результат стає новою плиткою; undo останньої дії (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): `target-number`, ряд плиток, `operator-buttons`, `timer-countdown` (ТБ-режим), undo/reset.
- `mode-select` (цифрова версія): вибір кількості великих чисел.
- `end-screen`: відповіді гравців, очки, оптимальний розвʼязок.
- `help-window`: правила (Countle).
- Переходи: вибір великих → ціль і таймер → оголошення → `end-screen`.

## Фічі поза полем
- `daily-puzzle` (Countle): однаковий набір для всіх; `share-result`.
- Солвер з точними й найближчими розвʼязками, share задачі з лінком на розвʼязки (incoherency.co.uk).
- Спецвипуски: великі числа 12, 37, 62, 87 замість звичних (2010).
- Пілот ТБ мав іншу шкалу: 5 / 3 / 1.

## Варіації й родичі
- Des chiffres et des lettres / «Le compte est bon» (Франція, раунди чисел з 1972): 45 с, 9 очок за точно і 6 — найближчому.
- [nyt-digits.md](nyt-digits.md) — та сама механіка, 5 задач на день, зірки за близькістю ≤10 / ≤25.
- Гра «24», Krypto; [nerdle.md](nerdle.md), [mathable.md](mathable.md); раунд літер Countdown — найдовше слово з 9 літер ([scrabble.md](scrabble.md), [boggle.md](boggle.md) за духом).
- **Осі варіацій:** склад набору (вибір великих / фіксований) · ціль (випадкова 100–999 / підібрана) · час (30 с / 45 с / без ліку) · оцінка (близькість 10/7/5 / зірки / лише точно) · суперник (дуель / щоденна для всіх).

## Цікавинки для курсу
- Механіка «дві плитки → результат» з валідацією «ціле > 0» і undo — 🌱.
- Оцінка 10/7/5 за відстанню, дуель «найближчий бере» — 🌱.
- Вибір 0–4 великих і випадкове тягнення з пулу 24 + ціль 100–999 — 🌱.
- Повний солвер (рекурсія по парах і операціях, мемо станів, канонічний порядок для + ×) з «найближчим», якщо точного нема — 🥉.
- Статистика: частка розвʼязних задач для кожної кількості великих (перебір усіх наборів) — 🥈.

## Мапа на каталог
- Є: `cell-click` ↔ вибір плиток · `move-timer` / `time-out` ↔ 30 с · `event-points` ↔ 10/7/5 · `simultaneous-versus` / `hot-seat` ↔ двоє розвʼязують те саме · `level-solver` ↔ розвʼязок асистента/солвер · `daily-puzzle` / `share-result` ↔ Countle · `undo-step` · `game-screen` · `end-screen` · `help-window` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+number-combine`, `+stars-by-distance` — як у nyt-digits.md (тут оцінка 10/7/5 — ще один пресет порогів).
  - `+large-small-draw` «Склад набору: скільки великих, решта малі, з пулу» · levels/generation · 🌱 · слоти {large: 0–4, pool}.
  - `+closest-wins` «Очки лише найближчому до цілі, нічия — обом» · game-logic/opponent · 🌱.
  - `+random-target` «Випадкова ціль у діапазоні» · levels/generation · 🌱 · слоти {min: 100, max: 999}.

## Пропозиції до словників
- `+cond:positive_integer` — результат операції ціле і > 0 (Countdown, Digits) — друга гра корпусу.
- `+cond:distance` — відстань значення до цілі в межах N (10/7/5 тут, зірки в Digits).
- `+ui:target-number`, `+ui:operator-buttons` — як у Digits (друга гра).
- `+feature:declare-and-verify` — відповідь оголошують, потім перевіряють обчислення (ТБ-формат).
- `+card:large-small-draw` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Countdown (game show)](https://en.wikipedia.org/wiki/Countdown_(game_show)) — повні правила раунду чисел, CECIL, оцінка, стратегії (1 великий + 5 малих — найчастіше, 2 великі — найлегше точне), спецвипуски, французький оригінал.
- [Countle](https://www.countle.org/) — щоденна версія.
- [incoherency.co.uk: Countle Solver](https://incoherency.co.uk/countdown/posts/countle-solver-is-live) — опис Countle, солвер, share.
- [incoherency.co.uk: Countdown pages](https://incoherency.co.uk/countdown/pages/) — правила й налаштування раунду.
- YouTube: пошук «countdown numbers round».

## Непевне
- (?) Інтерфейс Countle (ряди операцій, ліміт кроків, undo, таймер, вигляд share) — сторінка на JS, текст не прочитано.
- (?) Рік Countle — 2022 за рядком черги, не перевірено.
- (?) Як саме CECIL генерує ціль (рівномірно 100–999) — так у статті, без деталей алгоритму.
