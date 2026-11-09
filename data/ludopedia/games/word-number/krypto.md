---
title: Krypto
slug: krypto
aka: [Крипто, International Krypto]
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
year: 1963
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Krypto_(game)", best: true, note: "колода 56 карт, 5 + цільова, + − × ÷ лише цілі, кожну карту рівно раз, міжнародні правила: «Krypto!», 30 с пояснення, 3 хв, 10 роздач, подвоєння серії, штраф"}
  - {kind: other, url: "https://www.dcode.fr/krypto-solver", note: "солвер: «усі числа обовʼязкові», дозвіл/заборона/обовʼязковість кожної операції, без дробових ділень"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=krypto+card+game", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [cell-click, move-timer, time-out, event-points, combo-multiplier, simultaneous-versus, hot-seat, level-solver, undo-step, rule-variants, game-screen, end-screen, help-window, +number-combine, +random-target, +use-all-exactly-once, +weighted-deck, +call-and-explain, +false-call-penalty]
proposes: ["+cond:positive_integer", "+cond:all_used", "+ui:target-number", "+ui:operator-buttons", "+feature:declare-and-verify", "+card:use-all-exactly-once", "+card:weighted-deck"]
author: opus
date: 2026-11-09
---

# Krypto — пʼять карт 1–25 і шоста-ціль: використай кожну рівно раз і чотири дії, щоб отримати ціль першим

## Суть
Карткова арифметична гра (Daniel Yovich, 1963; Parker Brothers, MPH Games): роздають пʼять карт і шосту — цільову. Хто першим знайде вираз, де кожна з пʼяти карт ужита **рівно один раз** і результат дорівнює цілі, — кричить «Krypto!» і пояснює. Відмінності від [countdown-numbers](countdown-numbers.md) і [nyt-digits](nyt-digits.md): обовʼязково всі пʼять (а не «скільки треба»), ціль — теж карта з тієї самої колоди (1–25), колода зважена на малі числа, нема балів за близькість — лише точний розвʼязок, і серії подвоюють очки.

## Поле і час
- «Поле» — ряд із 5 карт + цільова (1d); у міжнародній версії пʼять лицем догори в центрі, шоста — ціль.
- Колода 56 карт: по 3 — числа 1–6, по 4 — 7–10, по 2 — 11–17, по 1 — 18–25.
- Час: 3 хвилини на роздачу, інакше нова; після «Krypto!» — 30 с на пояснення (міжнародні правила).
- Гра: 10 роздач.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робоча карта | tile | 1–25 | ужити рівно раз |
| Цільова карта | static | 1–25 | результат виразу має дорівнювати їй |
| Колода | container | 56 карт, зважена | тягнуть 6 на роздачу |
| Проміжний результат | tile | ціле ≥ 0 (?) | заміщує два операнди |
| Гравець | player | очки, серія | кличе «Krypto!» і пояснює |
| Таймер | static | 3 хв / 30 с | на роздачу / на пояснення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «роздати 5 робочих карт і 1 цільову з перетасованої колоди»`, `timer(start 3min)`.
- КОЛИ `input(a op b)` → ЯКЩО `positive_integer(a op b)` (?) → ТО `merge(a, b → a op b)`.
- КОЛИ `input(a ÷ b | a − b)` → ЯКЩО `custom: «дріб або відʼємне»` → ТО `block`.
- КОЛИ `custom: «лишилось одне число»` → ЯКЩО `all_used(cards)` and `custom: «число = ціль»` → ТО `custom: «розвʼязок»`.
- КОЛИ `input(call Krypto)` → ТО `timer(start 30s)`, `custom: «гравець пояснює вираз»`.
- КОЛИ `custom: «пояснення правильне»` → ТО `score(+1 або ×2 серії)`.
- КОЛИ `custom: «правильне і попередня роздача теж за цим гравцем»` → ТО `multiplier(×2)`; КОЛИ `custom: «серію перервано»` → ТО `reset_combo`.
- КОЛИ `custom: «пояснення хибне»` → ТО `score(−1)`, `custom: «гравець не може брати переграш цієї роздачі»`.
- КОЛИ `timer(left, ==, 0)` → ТО `custom: «нова роздача»`.
- КОЛИ `counter(hands, ==, 10)` → ТО `game_over`; нічия — додаткові роздачі.
- Варіант на двох: 11 закритих роздач, ціль — остання карта; фальшивий виклик — мінус роздача.
- Варіант: ціль 0 або 100 замість карти.
- Перемога: більше очок за 10 роздач · Поразка: менше · Рахунок: +1 за Krypto, подвоєння за серію, −1 за хибний виклик.

## Керування і ввід
- Настільна: усно / на папері.
- Цифрова версія: тап карта → операція → карта; результат — нова плитка; undo; кнопка «Krypto» з'являється, коли використано всі пʼять (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): `target-number`, 5 карт, `operator-buttons`, `timer-countdown`, рахунок і серія, undo.
- `end-screen`: розвʼязок (з солвера, якщо ніхто не знайшов), очки.
- `help-window`: правила, колода.
- `settings-window` (цифрова версія): діапазон чисел (варіант для новачків), дозволені операції (як у dCode).

## Фічі поза полем
- Солвер з налаштуваннями (dCode): «усі числа обовʼязкові», кожна операція — дозволена / обовʼязкова / заборонена, заборона дробових ділень, експорт розвʼязків CSV/TXT.
- Генератор задач (випадкові 5 + ціль).
- Варіант «будь-які 6 чисел»: менший діапазон — для початківців, більший — складніше.

## Варіації й родичі
- [countdown-numbers](countdown-numbers.md) — 6 плиток, ціль 100–999, не всі обовʼязкові, бали за близькість.
- [nyt-digits](nyt-digits.md) — 6 чисел, 5 задач на день, зірки.
- Гра «24» — чотири числа → завжди 24, кожне рівно раз; [nerdle](nerdle.md), [mathable](mathable.md).
- **Осі варіацій:** «усі рівно раз» / «не більше разу» · ціль (карта з колоди / фіксована 24 / 100–999) · дроби (заборонено / дозволено) · оцінка (лише точно / близькість) · серії (×2 / нема).

## Цікавинки для курсу
- Генератор роздачі зі зваженої колоди (56 карт) — 🌱.
- Солвер «усі пʼять рівно раз» (рекурсія по парах, дедуплікація станів) — 📎.
- Статистика: частка розвʼязних роздач і середня кількість розвʼязків (перебір усіх 6-наборів) — 🥈.
- Оцінка з подвоєнням серії і штрафом за хибний виклик — 🌱.
- Вираз-рядок → перевірка «усі карти рівно раз» через парсер — 📎.

## Мапа на каталог
- Є: `cell-click` · `move-timer` / `time-out` (3 хв) · `event-points` · `combo-multiplier` (подвоєння серії) · `simultaneous-versus` / `hot-seat` · `level-solver` · `undo-step` · `rule-variants` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+number-combine`, `+random-target` — з Countdown/Digits (підтвердження).
  - `+use-all-exactly-once` «Розвʼязок має вжити кожен елемент рівно раз» · game-logic/win · 🌱.
  - `+weighted-deck` «Колода з частотами: більше малих чисел» · levels/generation · 🌱 · слоти {freq}.
  - `+call-and-explain` «Виклик + час на пояснення» · game-logic/opponent · 🌱; `+false-call-penalty` · 🌱.

## Пропозиції до словників
- `+cond:positive_integer` — підтвердження з Countdown/Digits (третя гра).
- `+cond:all_used` — усі елементи набору вжито (Krypto, «24»).
- `+ui:target-number`, `+ui:operator-buttons` — третя гра.
- `+feature:declare-and-verify` — підтвердження з Countdown.
- `+card:use-all-exactly-once`, `+card:weighted-deck`.

## Джерела
- ⭐ [Wikipedia: Krypto (game)](https://en.wikipedia.org/wiki/Krypto_(game)) — автор і рік, колода 56 карт з частотами, роздача, операції, міжнародні правила (Krypto!, 30 с, 3 хв, 10 роздач, подвоєння, −1), варіант на двох, цілі 0/100.
- [dCode: Krypto Solver](https://www.dcode.fr/krypto-solver) — опис правил, налаштування солвера, приклад 2 3 4 5 6 → 12.
- YouTube: пошук «krypto card game».

## Непевне
- (?) Чи дозволені проміжні нулі — Wikipedia забороняє лише дроби, відʼємні й корені.
- (?) Цифрові версії Krypto (UI, кнопка виклику) — не досліджено, описано як «цифрова версія».
- (?) Оригінальні (не міжнародні) правила рахунку Parker Brothers — у статті лише загально.
