---
title: Mini Cactpot (Final Fantasy XIV)
slug: mini-cactpot
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: score
year: 2015
platforms: [Final Fantasy XIV (PC, консолі) — мінігра Gold Saucer]
links:
  - {kind: wiki, url: "https://ffxiv.consolegameswiki.com/wiki/Mini_Cactpot", best: true, note: "правила: 3×3 з числами 1–9, одне відкрите + 3 на вибір, 8 ліній, таблиця виплат MGP за сумою, 3 квитки на день по 10 MGP, скидання, досягнення Dream Small"}
  - {kind: wiki, url: "https://ffxiv.consolegameswiki.com/wiki/Scratch_It_Rich", note: "квест-розблокування: слова Mini Cactpot Broker про квиток, 3 квитки на день, скидання о 15:00 GMT"}
  - {kind: wiki, url: "https://ffxiv.consolegameswiki.com/wiki/Patch_2.51", note: "патч 2.51 — 23.02.2015, додано Manderville Gold Saucer"}
  - {kind: other, url: "https://github.com/super-aardvark/cactpot-calculator", note: "JS-калькулятор спільноти (26.02.2015): «maximizing your profits»"}
  - {kind: other, url: "https://github.com/crowreeve/cactacalc", note: "Windows-солвер (25.02.2015): сподіваний виграш кожного рядка/стовпця перебором усіх варіантів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=FFXIV+Mini+Cactpot+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, event-points, game-screen, end-screen, help-window, achievements-window, level-solver, +permutation-grid, +reveal-budget, +line-choice-payout, +payout-table, +daily-attempts, +ev-reveal-advisor]
proposes: ["+effect:payout", "+trigger:wallclock", "+ui:payout-table", "+feature:daily-attempts", "+card:permutation-grid", "+card:reveal-budget", "+card:line-choice-payout", "+card:payout-table", "+card:daily-attempts", "+card:ev-reveal-advisor"]
author: opus
date: 2026-11-09
---

# Mini Cactpot — щоденний «стиральний» квиток 3×3: відкрий три числа з дев'яти, обери лінію і отримай MGP за сумою

## Суть
Лотерея-стиралка в Gold Saucer (Final Fantasy XIV). Під дев'ятьма клітинами 3×3 лежать числа 1–9 у випадковій перестановці; одне відкрите одразу. Гравець стирає ще три клітини на вибір, потім обирає одну з восьми ліній (3 рядки, 3 стовпці, 2 діагоналі) — і отримує MGP за сумою трьох чисел цієї лінії за фіксованою таблицею. Програшу нема, є лише ціна квитка; вся гра — дедукція «що лишилось» і ризик-вибір за нерівною таблицею виплат.

## Поле і час
- Поле 3×3; кожне число 1–9 рівно один раз (перестановка).
- Шари: приховане число · відкрите число · лінії-вибори навколо поля (8 штук).
- Статичний пазл без таймера: 3 стирання → 1 вибір лінії → кінець квитка.
- Сесія — квиток; до 3 квитків на «земну» добу, лічильник скидається за реальним часом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Квиток | container | ціна 10 MGP | 9 клітин, одна відкрита на старті |
| Клітина | tile | число 1–9 (приховане) | відкривається стиранням; число унікальне на квитку |
| Лінія | zone | 3 рядки · 3 стовпці · 2 діагоналі | обирається одна; її сума — ключ таблиці |
| Таблиця виплат | static | сума 6–24 → MGP | фіксована, видна гравцеві |
| MGP | resource | валюта Gold Saucer | ціна квитка і виграш |
| Mini Cactpot Broker | neutral | NPC у Gold Saucer | продає квитки, відкриває гру квестом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(talk, Mini Cactpot Broker)` → ЯКЩО `custom: «квест It Could Happen to You виконано, рівень ≥ 15»` → ТО `unlock(Mini Cactpot)` (квест Scratch It Rich без кроків: розмова = виконання).
- КОЛИ `input(buy_ticket)` → ЯКЩО `counter(tickets_today, <, 3)` → ТО `currency(-10)`, `spawn(ticket)`; інакше `block`.
- КОЛИ `spawned(ticket)` → ТО `custom: «числа 1–9 розкладено випадковою перестановкою»`, `reveal(одна клітина)`.
- Інваріант квитка: `unique(grid)` — кожне з 1–9 рівно раз (кожне відкрите число виключає себе з решти клітин).
- КОЛИ `input(scratch, c)` → ЯКЩО `custom: «c закрита»` and `counter(scratches, <, 3)` → ТО `reveal(c)`, `counter(scratches, +1)`.
- КОЛИ `input(scratch, c)` → ЯКЩО `counter(scratches, ==, 3)` → ТО `block`.
- КОЛИ `counter(scratches, ==, 3)` → ТО `choose(лінія з 8: рядок 1–3, стовпець 1–3, діагональ ×2)`.
- КОЛИ `input(select_line, L)` → ТО `reveal(усі клітини)`, `custom: «s = сума трьох чисел лінії L»`, `currency(+payout[s])`.
- Таблиця виплат (сума → MGP): 6 → 10 000 · 7 → 36 · 8 → 720 · 9 → 360 · 10 → 80 · 11 → 252 · 12 → 108 · 13 → 72 · 14 → 54 · 15 → 180 · 16 → 72 · 17 → 180 · 18 → 119 · 19 → 36 · 20 → 306 · 21 → 1 080 · 22 → 144 · 23 → 1 800 · 24 → 3 600.
- КОЛИ `custom: «щоденне скидання: 15:00 GMT (10:00 EST)»` → ТО `counter(tickets_today, =0)`.
- КОЛИ `counter(mini_cactpot_mgp, >=, 5 | 10 000 | 500 000)` → ТО `custom: «досягнення Dream Small I / II / III»`.
- Перемога: нема (кожен квиток платить щонайменше 36 MGP) · Поразка: нема · Рахунок: MGP за таблицею; ціна квитка 10 MGP.

## Керування і ввід
- Розмова з NPC → купити квиток (до 3 на добу).
- Клік (миша/геймпад) по закритій клітині — стерти; рівно три стирання.
- Після трьох — вибір однієї з 8 ліній; підтвердження відкриває весь квиток і нараховує MGP.
- Порядок важливий: стирання адаптивні (наступне обирається, бачивши попередні числа).

## Вікна, меню, HUD
- `dialogue-window` — Mini Cactpot Broker: купівля квитка, пояснення правил (у квесті Scratch It Rich).
- `game-screen` — квиток: поле 3×3, відкриті числа, вибір ліній навколо поля, таблиця виплат (`payout-table`) (?).
- `end-screen` — усі 9 чисел відкриті, обрана лінія і сума, нарахований виграш MGP.
- `achievements-window` — загальне вікно досягнень гри (Dream Small I–III, Mountains out of Gil-hills).
- HUD: `remaining-counter` — скільки стирань лишилось (?); баланс MGP (?).
- Переходи: broker → game-screen → (3 стирання, лінія) → end-screen → broker (наступний квиток або «ліміт на сьогодні»).

## Фічі поза полем
- `daily-attempts` — 3 квитки на земну добу, спільне скидання за реальним часом (не за сесією).
- Розблокування квестом (рівень 15, NPC за координатами X:5, Y:6 у Gold Saucer).
- Досягнення за сумарний виграш MGP і титул «Raiser of Mountains» (умова на сторінці не описана).
- Спільнотні солвери (калькулятори сподіваного виграшу) зʼявились за 1–3 дні після патча — фактично `hint` поза грою.

## Варіації й родичі
- Jumbo Cactpot — сусідня лотерея Gold Saucer (на сторінці лише згадана).
- [Faux Hollows](faux-hollows.md) — інша FFXIV-мінігра з прихованим полем 6×6 і бюджетом відкриттів.
- [Voltorb Flip](voltorb-flip.md) — лінійні суми, ризик і вихід зі ставкою; тут сума лінії — не підказка, а ключ виплати.
- [Mastermind](mastermind.md) — дедукція прихованого стану за бюджетом спроб.
- Паперові лотерейні стиралки (scratch cards) — та сама «стерти N з M», але без дедукції.
- **Осі варіацій**: відкрито на старті 0 / 1 / k · стирань 3 / N · ліній 8 / лише рядки · виплата за сумою / за добутком / за збігом символів · ліміт квитків на день / вільно.

## Цікавинки для курсу
- Квиток як перестановка 1–9 з однією відкритою клітиною, сума лінії і таблиця виплат — 🌱 (масиви й словник).
- Порадник лінії: для кожної з 8 ліній перебрати розкладки невідомих чисел і порахувати сподіваний виграш — 📎.
- Повний expectimax «яку клітину стерти»: 3 рівні вибору × відповіді з кешем станів; мій розрахунок за таблицею: оптимальна гра ≈ 1 485 MGP за квиток, без жодного стирання ≈ 446, лінія навмання ≈ 360 — 🥈 (цінність інформації наочно).
- Розподіл сум трійок різних чисел 1–9 (84 трійки: 1, 1, 2, 3, 4, 5, 7, 7, 8, 8, 8, 7, 7, 5, 4, 3, 2, 1, 1 для сум 6…24) проти таблиці: чому 7 і 19 рідкісні, але платять 36 — 🌱.
- Ліміт спроб за реальним часом (скидання о 15:00 GMT, а не з рестартом гри) — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ стирання · `event-points` ↔ таблиця виплат як таблиця вартостей · `game-screen` / `end-screen` · `help-window` ↔ пояснення брокера · `achievements-window` · `level-solver` ↔ калькулятори спільноти.
- **Нема** → пропозиції карток:
  - `+permutation-grid` «Поле — випадкова перестановка 1…N» · levels/generation · 🌱.
  - `+reveal-budget` «Фіксована кількість відкриттів без поразки» · game-logic/constraints · 🌱 · слот {reveals: 3}.
  - `+line-choice-payout` «Обрати лінію поля — виплата за її сумою» · game-logic/score · 🌱 · слот {lines: rows|cols|diags}.
  - `+payout-table` «Таблиця виплат за ключем (сума → очки)» · game-logic/score · 🌱.
  - `+daily-attempts` «N спроб на добу зі скиданням за годинником» · game-logic/save · 📎.
  - `+ev-reveal-advisor` «Порадник ходу за сподіваним виграшем (expectimax)» · levels/solvability · 🥈.

## Пропозиції до словників
- `+effect:payout(table, key)` — нарахувати виграш за таблицею (сума лінії → MGP); `currency` лише додає число.
- `+trigger:wallclock(t)` — настав момент реального часу (щоденне скидання о 15:00 GMT).
- `+ui:payout-table` — таблиця виплат на ігровому екрані.
- `+feature:daily-attempts` — денний ліміт спроб зі скиданням.
- Вжито наявні без пропозицій: `unique` (перестановка), `choose` (вибір лінії), `unlock` (квест), `dialogue-window`.

## Джерела
- ⭐ [FF14 Wiki: Mini Cactpot](https://ffxiv.consolegameswiki.com/wiki/Mini_Cactpot) — 3×3, числа 1–9, одне відкрите, 3 вибрані клітини, 8 ліній, повна таблиця виплат, 3 квитки на добу по 10 MGP, скидання 10 AM EST, досягнення.
- [FF14 Wiki: Scratch It Rich](https://ffxiv.consolegameswiki.com/wiki/Scratch_It_Rich) — квест-розблокування, слова брокера про квиток і скидання о 15:00 GMT.
- [FF14 Wiki: Patch 2.51](https://ffxiv.consolegameswiki.com/wiki/Patch_2.51) — 23.02.2015, Gold Saucer.
- [super-aardvark/cactpot-calculator](https://github.com/super-aardvark/cactpot-calculator) · [crowreeve/cactacalc](https://github.com/crowreeve/cactacalc) — солвери спільноти лютого 2015 (опис і README через GitHub API).
- Числа ≈ 1 485 / 446 / 360 MGP і розподіл сум — мій скрипт перебору за таблицею з вікі (не джерело гри).

## Непевне
- (?) Вигляд квитка: де саме таблиця виплат, як вибирається лінія (стрілки біля рядків/стовпців/діагоналей), чи є лічильник стирань — з памʼяті, не перевірено.
- (?) Чи множать виплату бонуси MGP (кампанії на кшталт «Make It Rain», на яку посилається сторінка) — не перевірено.
- (?) Розрахунок EV припускає, що перша відкрита клітина й число — рівномірно випадкові.
- (?) Перелік виграшних комбінацій у таблиці вікі в переказі виглядав неповним для сум 18–22; кількості трійок я перерахував сам.
- (?) Поле `platforms` — загальні платформи FFXIV, не перевірено для 2015 року.
