---
title: Bingo / Keno / Lotto (Бінго, Лото)
slug: bingo
aka: [Бінго, Лото, Beano, Housie, Tombola, Keno, Кено, 75-ball bingo, 90-ball bingo, Bingo Blitz]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: both
  goal: race
year: 1929
platforms: [board, web, mobile, arcade]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bingo_(American_version)", best: true, note: "картка 5×5 B-I-N-G-O, діапазони колонок, вільний центр, патерни (лінія, кути, марка, blackout), варіанти, історія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bingo_(British_version)", note: "90-куля: квиток 3×9 з 15 числами, стрічка з 6 квитків, лінія / дві лінії / full house, «bingo lingo»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Keno", note: "Keno: 1–80, тягнуть 20, гравець обирає «spots», таблиця виплат, гіпергеометричні шанси"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bingo_Blitz", note: "цифрове бінго: 24 числа на картці, кілька карток за кредити, power-ups, бонус-клітини, кімнати-міста, колекції"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=how+to+play+bingo", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [completion-detection, cell-click, round-currency, leaderboard, shop-window, world-map, game-screen, end-screen, help-window, mode-select, +called-number-queue, +pattern-win, +free-center-cell, +multi-card-play, +auto-daub, +false-claim-penalty, +pay-table, +pick-spots-ahead, +wild-number]
proposes: ["+trigger:called", "+role:tool", "+cond:on_card", "+cond:pattern_complete", "+effect:daub", "+effect:claim", "+ui:called-board", "+ui:last-called", "+ui:pattern-card", "+ui:pay-table", "+window:card-buy", "+axis:opponent=parallel", "+feature:auto-daub"]
author: opus
date: 2026-11-09
---

# Bingo / Keno / Lotto — межа корпусу: сітка-картка, випадкові числа від ведучого, перемагає той, хто першим закрив патерн

## Суть
Кожен гравець має свою картку з числами; ведучий (кульова машина, RNG) по одному оголошує випадкові числа; гравець позначає («даубить») ті, що є на картці. Хто першим закрив потрібний патерн — лінію, чотири кути, усе поле — кричить «Bingo!», картку перевіряють. Рішень майже нема: це **чистий шанс** з паралельними гравцями, корисний корпусу як нижня межа «гри на сітці» і як зразок черги подій, перевірки патерну й паралельного змагання без взаємодії. Keno — лотерейний родич: числа обираєш **наперед**, виплата за таблицею збігів.

## Поле і час
- Американське бінго (75 куль): картка 5×5, колонки B 1–15 · I 16–30 · N 31–45 · G 46–60 · O 61–75; центр — вільна клітина, вважається закритою; можливих карток ≈ 5.52×10²⁶.
- Британське (90 куль): квиток 3×9 — у рядку 5 чисел і 4 порожні, колонки за десятками (1–9, 10–19 … 80–90); стрічка з 6 квитків покриває всі 90 чисел.
- Keno: поле-бланк 1–80; тягнуть 20 чисел (деякі варіанти — менше).
- Час: тік = одне оголошене число; темп задає ведучий (у цифрових — таймер); гравець має встигнути позначити.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Картка / квиток | zone | 5×5 або 3×9, числа | своя в кожного гравця; гравець може мати кілька |
| Клітина з числом | tile | число, стан open/daubed | позначається, якщо число оголошено |
| Вільна клітина (центр) | tile | — | закрита від початку |
| Ведучий / кульова машина | spawner | мішок 75 / 90 / 80 чисел | тягне без повторень одне число за тік |
| Оголошене число | object | число | додається в історію; від цього моменту його можна позначити |
| Патерн раунду | zone | набір клітин | лінія, 4 кути, марка 2×2, roving L, blackout, «hard-way» лінія без центру |
| Маркер / даубер | `+role:tool` (?) | — | позначає клітину (фішка, фломастер) |
| Keno-квиток | zone | обрані «spots» 1–20, ставка | фіксований до тиражу |
| Таблиця виплат (Keno) | static | spots × збіги → виплата | визначає виграш |
| Бонус-клітина (Bingo Blitz) | pickup | приз | дає приз, коли позначена |
| Power-up (Bingo Blitz) | pickup | — | допомагає швидше закрити патерн |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен гравець отримує/купує N карток»`; КОЛИ `custom: «центр 5×5»` → ТО `mark(center, daubed)`.
- КОЛИ `timer(every)` → ТО `custom: «ведучий тягне випадкове число без повторень»` (`+trigger:called`).
- КОЛИ `input(daub, cell)` → ЯКЩО `custom: «число клітини вже оголошено»` → ТО `mark(cell, daubed)`; інакше `block`.
- КОЛИ `pattern(line)` → ЯКЩО `mode(line)` → ТО `custom: «гравець може заявити Bingo»` — рядок, стовпець або діагональ.
- Інші патерни раунду: `pattern(four_corners)` · `custom: «марка 2×2 у куті»` · `custom: «roving L»` · `pattern(all)` — blackout/coverall (найбільший джекпот) · `custom: «hard-way: лінія без вільної клітини»`.
- КОЛИ `input(claim)` → ЯКЩО `custom: «патерн закрито оголошеними числами»` → ТО `win`, `window(end-screen)`; раунд закінчено для всіх.
- КОЛИ `input(claim)` → ЯКЩО `custom: «патерну нема» («jumping the gun»)` → ТО `custom: «заявку відхилено, гра триває»`.
- 90-ball: КОЛИ `custom: «закрито рядок / два рядки / усі 15 чисел»` → ТО `custom: «приз Line / Two lines / Full house»`; гра йде далі до Full house.
- 90-ball: ЯКЩО `custom: «останнє оголошене число не входить у патерн»` → ТО `custom: «заявку можуть анулювати»`.
- Wild numbers: КОЛИ `custom: «перше число раунду»` → ТО `custom: «усі числа з тією ж останньою цифрою вважаються оголошеними»`.
- Keno: КОЛИ `input(pick, spots)` → ТО `custom: «квиток зафіксовано, ставка»`; КОЛИ `custom: «витягнуто 20 чисел»` → ТО `currency(+pay_table[spots][hits])`.
- Цифрове: КОЛИ `custom: «оголошено число»` → ЯКЩО `mode(auto_daub)` → ТО `mark(cell, daubed)` на всіх картках (?).
- Перемога: першим закрити патерн (кілька одночасних — приз ділять (?)) · Поразка: інший гравець перший · Рахунок: призи / кредити.

## Керування і ввід
- Паперове: даубер по клітині, вигук «Bingo!» / «Line!» / «House!»; ведучий оголошує вголос (часто з «bingo lingo» — римованими прізвиськами чисел).
- Цифрове: тап по клітині з оголошеним числом, кнопка «BINGO» для заявки, кнопки power-up (Bingo Blitz); вибір кількості карток перед раундом.
- Keno: позначити 1–20 чисел на бланку, вибрати ставку, «Play».

## Вікна, меню, HUD
- `game-screen` (цифрова версія): 1–4 картки, `+ui:last-called` (велика куля з останнім числом), `+ui:called-board` (таблиця всіх оголошених 1–75), `+ui:pattern-card` (який патерн у цьому раунді), лічильник лишилось куль (`remaining-counter`), кнопка BINGO, `coins` (кредити).
- `+window:card-buy` — скільки карток купити на раунд за кредити.
- `world-map` / кімнати-міста (Bingo Blitz): проходиш міста, збираючи елементи колекцій; сезонні кімнати.
- `end-screen` — переможці раунду й призи · `leaderboard` · `shop-window` (кредити, power-ups).
- Keno: бланк 1–80 + `+ui:pay-table` поруч + `end-screen` з кількістю збігів.

## Фічі поза полем
- `+feature:auto-daub` (цифрові клієнти) (?) · `mode-select` (75/90/80 куль, патерни) · колекції й кімнати (Bingo Blitz) · кілька карток одночасно.
- Варіанти правил: U-Pick-Em (гравець сам обирає числа з трьох карток), double-action (два числа в клітині), wild numbers, music bingo.

## Варіації й родичі
- Історія: лото в Італії бл. 1530 → Tombola (Неаполь, XVIII ст.) → французьке Le Lotto (1778, макет 3×9) → «Beano» на карнавалах; Edwin S. Lowe популяризував у Нью-Йорку з 1929; Hugh J. Ward стандартизував правила (книга 1933).
- Keno — китайського походження (лотерея з 1847 у Макао), у США з часів трансконтинентальної залізниці.
- У корпусі: [word-search](word-search.md) / [boggle](boggle.md) (пошук на сітці, але рішення гравця), [nonogram](../pencil-logic/nonogram.md) (лінії й поле як обмеження), [mathable](mathable.md), [wordle](wordle.md) (черга відгуків), [number-match](number-match.md).
- **Осі варіацій**: картка — 5×5 / 3×9 / бланк 1–80 · хто обирає числа — генератор / гравець (U-Pick-Em, Keno) · ціль — патерн / кількість збігів · перевірка — гравець заявляє / авто · кількість карток — 1 / N.

## Цікавинки для курсу
- Генератор картки 5×5 з діапазонами колонок і без повторів + вільний центр — 🌱.
- Генератор квитків 90-ball: 5 чисел у рядку, колонки за десятками, стрічка з 6 квитків без повторів на 1–90 — 🥉 (комбінаторна побудова).
- Перевірка набору патернів (лінії, кути, марка, roving L, blackout) як масок — 🌱.
- Ведучий-RNG без повторень + історія оголошених + «bubble» (найраніший можливий виграш) — 📎.
- Кілька карток, auto-daub і перевірка «останнє число в патерні» — 📎.
- Keno: таблиця виплат і гіпергеометричні ймовірності / house edge — 🥉.

## Мапа на каталог
- Є: `completion-detection` ↔ патерн закрито · `cell-click` ↔ даубер · `round-currency` ↔ кредити · `leaderboard` · `shop-window` · `world-map` ↔ кімнати-міста · `game-screen` · `end-screen` · `help-window` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+called-number-queue` «Ведучий тягне числа без повторень, історія видима» · game-logic/random · 🌱.
  - `+pattern-win` «Перемога за маскою клітин з набору патернів» · game-logic/win · 🌱.
  - `+free-center-cell` «Клітина, закрита від початку» · entities/state · 🌱.
  - `+multi-card-play` «Кілька полів одного гравця, один потік подій» · game-logic/opponent · 📎.
  - `+auto-daub` «Автопозначення збігів» · interface/input · 🌱.
  - `+false-claim-penalty` «Хибна заявка на перемогу» · game-logic/win · 🌱.
  - `+pay-table` «Виплата за таблицею (вибрано × збіги)» · game-logic/economy · 📎.
  - `+pick-spots-ahead` «Гравець обирає числа до тиражу» · game-logic/random · 🌱.
  - `+wild-number` «Одне число відкриває групу інших» · game-logic/random · 🌱.

## Пропозиції до словників
- `+trigger:called` — ведучий оголосив число/подію з черги.
- `+role:tool` — інструмент гравця без власної поведінки (даубер) (?).
- `+cond:on_card` — оголошене число є на картці · `+cond:pattern_complete` — закрита маска клітин раунду.
- `+effect:daub` — позначити збіг (окремо від пазлового `mark`) · `+effect:claim` — заявити перемогу на перевірку.
- `+ui:called-board` · `+ui:last-called` · `+ui:pattern-card` · `+ui:pay-table`.
- `+window:card-buy`.
- `+axis:opponent=parallel` — гравці змагаються паралельно на своїх полях без взаємодії (лінт не приймає, тому в шапці `online`).
- `+feature:auto-daub`.

## Джерела
- ⭐ [Wikipedia: Bingo (American version)](https://en.wikipedia.org/wiki/Bingo_(American_version)) — картка 5×5, діапазони, вільний центр, патерни, «jumping the gun», варіанти, історія, електронне бінго.
- [Wikipedia: Bingo (British version)](https://en.wikipedia.org/wiki/Bingo_(British_version)) — квиток 3×9, стрічка 6 квитків, призи, «bingo lingo», правило останнього числа.
- [Wikipedia: Keno](https://en.wikipedia.org/wiki/Keno) — 1–80, 20 витягнутих, spots, таблиці виплат, house edge, історія.
- [Wikipedia: Bingo Blitz](https://en.wikipedia.org/wiki/Bingo_Blitz) — цифрова версія: 24 числа, кредити за картки, power-ups, бонус-клітини, кімнати й колекції; Playtika 2012 (Buffalo Studios, 2010).
- YouTube: пошук «how to play bingo».

## Непевне
- (?) Auto-daub у цифрових клієнтах — загальновідомо, але в джерелах не бачив.
- (?) Поділ призу між кількома одночасними переможцями — не перевірено.
- (?) Роль маркера `+role:tool` — сумнівна потреба; можна обійтись без сутності.
- Lotto (домашнє лото з бочонками 1–90) — правила за аналогією з британським 90-ball, окремо не перевіряв.
