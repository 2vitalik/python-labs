---
title: Larn
slug: larn
aka: [ULarn, NLarn, JS Larn, Larn 12.x]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1986
platforms: [Unix, DOS, Amiga, Atari ST, Windows, Linux, macOS, web (JS Larn)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Larn_(video_game)", best: true, note: "мета (ліки доньці), ліміт у мобулах, місто, 10 + 3 вулканічні рівні, податок наступній грі, складність росте після перемоги"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Larn", note: "RogueBasin: постійні рівні, банк з відсотками й філією, закляття 3-літерними кодами, ідентифікація завжди успішна"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Time", note: "вікі: мобул = 100 ходів, ліміт 300 мобулів"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Home", note: "вікі: умова перемоги й чотири варіанти повідомлення доктора"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/College_of_Larn", note: "вікі: 8 курсів по 250 золота, кожен коштує 5–20 мобулів"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Bank_of_Larn", note: "вікі: 0,4 % за мобул, стеля 500000, філія на рівні 5, купує самоцвіти"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Difficulty", note: "вікі: складність 0–9 і формули для HP/шкоди/досвіду монстрів"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Larn_Revenue_Service", note: "вікі: податок 5 % від рахунку після перемоги"}
  - {kind: fandom, url: "https://wiki.larn.org/wiki/Level_generation", note: "вікі: canned-рівні 4/17, нові монстри при поверненні"}
  - {kind: play, url: "https://larn.org", note: "JS Larn — грати в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Larn+roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-8dir, dungeon-generation, stairs-levels, hp-damage, inventory, inventory-items, item-pickup, item-identification, status-effects, unit-xp-skills, melee-vs-ranged, destructible-blocks, round-currency, shop-catalog, shop-buyback, time-out, permadeath, player-death, score-records, difficulty-levels, fog-of-war, message-log, status-panel, keyboard-controls, console-render, teleport, +run-deadline, +town-level, +bank-interest, +time-for-stats, +canned-levels, +level-repopulate, +win-tax-carryover, +difficulty-ladder, +spell-mnemonic, +auto-pickup]
proposes: ["+trigger:deadline", "+effect:interest(rate)", "+effect:train(stat, time)", "+effect:repopulate(n)", "+cond:time_elapsed(op, n)", "+cond:debt", "+role:shop-entrance", "+window:college-window", "+window:bank-window", "+window:tax-office", "+feature:difficulty-ladder", "+feature:cross-game-debt", "+axis:session=run", "+card:run-deadline", "+card:bank-interest", "+card:time-for-stats"]
author: opus
date: 2026-11-09
---

# Larn — роглайк на одну сесію з жорстким дедлайном: принеси ліки доньці за 300 мобулів, а все інше — торг часом

## Суть
Від [rogue](rogue.md) Larn відрізняє **дедлайн**: доньці лишилось 300 мобулів (30000 ходів), за цей час треба знайти зілля cure dianthroritis на дні й **повернутися додому** — тобто здолати шлях і вниз, і назад. Час — валюта: курси в коледжі дають стати, але коштують мобули; банк нараховує відсотки за мобул; відпочинок лікує, але їсть дедлайн. Рівні постійні, місто — постійний рівень з будівлями; гру розраховано на одну сесію. Після перемоги наступна гра складніша й починається з податку.

## Поле і час
- Квадратна сітка, 8 напрямків (?); один екран на рівень (?).
- Структура: місто (home level) → підземелля 1–10 (вхід з міста) і вулкан V1–V3 (окремий вулканічний ствол з міста).
- **Постійні рівні**: стан рівня зберігається; при кожному поверненні на відвіданий рівень зʼявляються `1 + depth / 2` нових монстрів у випадкових вільних клітинах.
- Генерація: лабіринти, ряди кімнат з дверима, круглі зали, відкриті простори з колонами або без; на більшості рівнів шанс 4/17 взяти заготовлений (canned) план; рівень 1 — ніколи, рівні 10 і V3 — завжди.
- На кожному рівні одні сходи вгору й одні вниз (крім крайніх); верх підземелля — вхід, верх вулкана — ствол.
- Час: хід = 1 тік, дробових ходів нема; мобул = 100 ходів. Деякі дії (курс коледжу) коштують цілі мобули.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | стати (STR, INT, WIS, CON, DEX, CHA), HP, спел-слоти, золото, рівень | рух, бій входом у клітину, закляття |
| Монстр | enemy | HP, шкода, AC, досвід, золото | переслідує; розумні — обходять пастки (?), тупих можна завести на пастку |
| Лепрекон | enemy | — | краде золото з собою (банк — захист) |
| Демон-принц | boss | — | викликається з Holy Altar (поріг залежить від складності) |
| Home (дім) | static | — | вхід = перевірка перемоги й показ залишку часу |
| DND store | static | — | крамниця спорядження |
| Trading post | static | — | продаж знахідок |
| College of Larn | static | 8 курсів | курс: −250 золота, −5…20 мобулів, +стати, повне лікування |
| Bank of Larn (+ філія на рівні 5) | static | баланс | вклад під 0,4 % складних за мобул до 500000; купує самоцвіти за повну ціну |
| Larn Revenue Service | static | борг | приймає податок; поки є борг — магазин і банк закриті |
| Вхід у підземелля / вулканічний ствол | static | — | спуск з міста |
| Сходи вгору / вниз | static | — | перехід між постійними рівнями |
| Статуя | static | — | руйнується (на низькій складності дає книгу); при складності ≥3 — незламна |
| Стіна | static | міцність | руйнується снарядом / заклинанням з шкодою ≥ поріг (+1 за рівень складності) |
| Holy Altar | static | — | шкода по ньому може викликати демон-принца |
| Пастки (яма, стріли) | hazard | — | шкода; можна завести туди тупого монстра |
| Зілля cure dianthroritis | pickup | — | ціль гри; після підбору банк закритий (JS Larn 12.5+) |
| Eye of Larn | pickup | самоцвіт | продається банку |
| Самоцвіти | pickup | цінність | scroll of gem perfection підвищує цінність усіх (експоненційно при повторі) |
| Зілля, сувої, книги, зброя, броня | pickup | — | тип завжди відомий (ідентифікація успішна) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `counter(turns, +1)`; КОЛИ `counter(turns, =, 100)` → ТО `counter(mobul, +1)`.
- КОЛИ `enter(hero, home)` → ЯКЩО `has(hero, cure potion)` and `custom: «мобулів < 300»` → ТО `win`.
- КОЛИ `enter(hero, home)` → ЯКЩО `not has(hero, cure potion)` and `custom: «мобулів < 300»` → ТО `message(діагноз + залишок часу)`.
- КОЛИ `enter(hero, home)` → ЯКЩО `custom: «мобулів ≥ 300»` → ТО `message(донька померла)`, `lose`.
- КОЛИ `input(take course)` → ЯКЩО `custom: «курс ще не взятий, є пререквізит»` and `custom: «золото ≥ 250»` → ТО `currency(−250)`, `custom: «час +5…20 мобулів»`, `custom: «+стат»`, `heal(hero, full)`, `custom: «знято сліпоту й сплутаність»`.
- КОЛИ `timer(every mobul)` → ТО `custom: «баланс × 1,004»`; ЯКЩО `custom: «баланс ≥ 500000»` → ТО `block`.
- КОЛИ `input(sell gem, bank)` → ТО `currency(+value)`, `disappear_b`.
- КОЛИ `input(read gem perfection)` → ТО `custom: «цінність усіх самоцвітів у рюкзаку зростає»`.
- КОЛИ `input(deposit)` → ТО `custom: «золото поза рюкзаком — лепрекон не вкраде»`.
- КОЛИ `input(stairs)` → ЯКЩО `custom: «рівень уже відвідано»` → ТО `custom: «відновити рівень»`, `spawn_at(1 + depth/2 monsters, random free cells)`.
- КОЛИ `custom: «генерація рівня»` → ЯКЩО `prob(4/17)` and `not level(=, 1)` → ТО `custom: «заготовлений план»`; ЯКЩО `level(=, 10)` or `custom: «V3»` → ТО `custom: «завжди заготовлений»`.
- КОЛИ `input(cast, mnemonic)` → ЯКЩО `custom: «є вільний спел-слот»` → ТО `custom: «закляття за 3-літерним кодом (MLE — magic missile)»`.
- КОЛИ `custom: «снаряд влучає в стіну»` → ЯКЩО `custom: «шкода ≥ поріг стіни»` → ТО `set_cell(target, floor)`.
- КОЛИ `custom: «руйнування статуї»` → ЯКЩО `custom: «складність < 3»` → ТО `set_cell(target, floor)`, `custom: «може випасти книга»`; інакше `block`.
- КОЛИ `input(self-teleport)` → ЯКЩО `prob(2/151)` → ТО `lose`; інакше `teleport(hero, random)`, `custom: «на цільовому рівні більше монстрів»`.
- КОЛИ `enter(hero, item cell)` → ЯКЩО `custom: «автопідбір увімкнено»` → ТО `pickup`.
- КОЛИ `contact(leprechaun, hero)` → ТО `custom: «краде золото з рюкзака»` (?).
- КОЛИ `win` → ТО `custom: «борг 5 % рахунку в LRS на наступну гру»`, `custom: «наступна гра — вища складність»`.
- КОЛИ `game_start` → ЯКЩО `custom: «є неоплачений податок»` → ТО `custom: «DND store і банк недоступні»`.
- КОЛИ `game_start` → ТО `custom: «складність d ∈ 0…9: HP монстрів ×(6+d)/6, шкода ×(6+d)/5, досвід ×7/(7+d), золото ×10/(10+d), регенерація героя повільніша»`.
- КОЛИ `hp_zero(hero)` → ТО `lose`.
- Перемога: принести зілля додому до 300 мобулів. Поразка: смерть або прострочений дедлайн. Рахунок: таблиця рекордів (основа податку) (?).

## Керування і ввід
- Клавіатура, roguelike-розкладка `hjklyubn` (?); команда заклинання + три літери мнемоніки.
- Автопідбір (вмикається/вимикається): лишений на клітині предмет підбирається знову, якщо стоїш.
- Вибір складності перед стартом.

## Вікна, меню, HUD
- `game-screen`: мапа рівня, нижні рядки стану (стати, HP, спел-слоти, золото, рівень, глибина, `timer-countdown` у мобулах (?)), рядок повідомлень.
- Вікна будівель (`custom-window`): DND store, Trading post, `college-window` (список курсів з ціною й часом), `bank-window` (вклад, зняття, продаж самоцвітів), `tax-office` (LRS).
- Дім: повідомлення доктора з залишком часу (`message`).
- `difficulty-select` перед грою; `end-screen` (перемога / смерть / прострочено); `leaderboard`.

## Фічі поза полем
- Сесія на один присід: мета й дедлайн задають довжину гри.
- **Сходи складності**: після перемоги наступна гра складніша (Wikipedia); у вікі — вибір 0–9 (JS Larn — до 128).
- **Борг між іграми**: податок 5 % від рахунку переходить у наступну гру; часткові виплати накопичуються (у JS Larn 12.4.5+ платити не обовʼязково).
- Сучасна гілка (26.40): вода розмиває стіни й тече, лава остигає, анімації, повний колір; ULarn — справжні класи, більше рівнів і зброї; NLarn — переосмислення.

## Варіації й родичі
- Корені — Hack/[rogue](rogue.md); постійне місто — раніше за [angband](angband.md) (там місто теж є) і ADOM ([adom](adom.md)).
- Таймер забігу: дедлайн Larn ↔ корупція [adom](adom.md) ↔ голод [nethack](nethack.md).
- Нащадки: ULarn, NLarn, JS Larn, Larn II.
- Осі варіацій: **годинник** (нема / глобальний дедлайн / дедлайн + час як ресурс) · **маршрут** (лише вниз / вниз і назад додому) · **складність** (пресет / сходи після перемог / борг між іграми).

## Цікавинки для курсу
- Глобальний дедлайн у ходах з кількома варіантами фінального повідомлення — 🌱.
- Час як валюта: курс = −золото −мобули +стати; банк = +відсотки за мобул — 📎 (баланс компромісів).
- Повернення на постійний рівень з доспавном `1 + depth/2` монстрів — 🌱.
- Canned-рівні з імовірністю 4/17 і обовʼязкові для фіналу — 📎 (змішування ручних і процедурних карт).
- Формули складності для HP/шкоди/досвіду монстрів — 🌱 (параметризація однієї змінної).
- Податок як борг, що переходить у наступну гру й блокує крамниці — 🌱.
- Руйнування стін за порогом шкоди снаряда — 📎.

## Мапа на каталог
- Є: `move-8dir` · `stairs-levels` · `dungeon-generation` · `hp-damage` · `inventory` · `item-identification` (завжди успішна) · `status-effects` (сліпота, сплутаність) · `destructible-blocks` (стіни, статуї) · `round-currency` + `shop-catalog` + `shop-buyback` · `time-out` (дедлайн) · `permadeath` · `difficulty-levels` · `teleport` · `score-records`.
- **Нема** → пропозиції карток:
  - `+run-deadline` «Глобальний дедлайн забігу в ходах; перевірка на вході в ціль» · game-logic/lose · 🌱 · слоти {limit, unit}.
  - `+bank-interest` «Вклад з відсотками за одиницю часу й стелею» · game-logic/economy · 🌱 · слоти {rate, cap}.
  - `+time-for-stats` «Курс/тренування: платиш часом за постійний бонус» · game-logic/economy · 🌱.
  - `+canned-levels` «Заготовлені плани серед процедурних з імовірністю» · levels/generation · 📎.
  - `+level-repopulate` «Доспавн монстрів при поверненні на рівень» · entities/spawn · 🌱.
  - `+win-tax-carryover` «Борг з перемоги переходить у наступну гру» · game-logic/save · 🌱.
  - `+difficulty-ladder` «Кожна перемога піднімає складність наступної гри» · game-logic/settings · 🌱.
  - `+spell-mnemonic` «Ввід закляття текстовим кодом» · interface/input · 🌱. Перевикористано: `+town-level`, `+auto-pickup`.

## Пропозиції до словників
- `+trigger:deadline` — вичерпано глобальний ліміт часу забігу.
- `+effect:interest(rate)` — нарахування відсотків на рахунок; `+effect:train(stat, time)` — +стат за час; `+effect:repopulate(n)` — доспавн N монстрів на рівні.
- `+cond:time_elapsed(op, n)` — скільки часу минуло від старту (ширше за `timer`, бо глобальний годинник забігу); `+cond:debt` — є неоплачений борг.
- `+role:shop-entrance` — клітина-вхід у вікно будівлі.
- `+window:college-window`, `+window:bank-window`, `+window:tax-office`.
- `+feature:difficulty-ladder`, `+feature:cross-game-debt`.
- `+axis:session=run`.
- `+card:run-deadline`, `+card:bank-interest`, `+card:time-for-stats`.

## Джерела
- ⭐ [Wikipedia: Larn](https://en.wikipedia.org/wiki/Larn_(video_game)) — мета, мобули, місто з 6 будівлями й двома входами, 10 + 3 рівні, податок, складність після перемоги, варіанти.
- [RogueBasin: Larn](https://www.roguebasin.com/index.php/Larn) — постійні рівні, типи генерації, банк з відсотками й філією, 3-літерні закляття, ідентифікація.
- [Larn wiki: Time](https://wiki.larn.org/wiki/Time) — мобул = 100 ходів, 300 мобулів.
- [Larn wiki: Home](https://wiki.larn.org/wiki/Home) — чотири результати входу додому.
- [Larn wiki: College](https://wiki.larn.org/wiki/College_of_Larn) — 8 курсів, 250 золота, 90 мобулів разом, повне лікування.
- [Larn wiki: Bank](https://wiki.larn.org/wiki/Bank_of_Larn) — 0,4 %/мобул, 500000, філія на 5, самоцвіти.
- [Larn wiki: Difficulty](https://wiki.larn.org/wiki/Difficulty) — 0–9, формули, статуї й стіни.
- [Larn wiki: LRS](https://wiki.larn.org/wiki/Larn_Revenue_Service) — 5 % від рахунку, блок крамниці й банку.
- [Larn wiki: Level generation](https://wiki.larn.org/wiki/Level_generation) — canned 4/17, доспавн монстрів.
- [Larn wiki: Tips for beginners](https://wiki.larn.org/wiki/Tips_for_beginners) — самотелепорт 2/151, автопідбір, gem perfection.

## Непевне
- (?) Де саме лежить зілля (вікі: «чутки — глибоко в печерах»; з памʼяті — дно вулкана V3).
- (?) Як саме росте складність після перемоги (Wikipedia: «складніше щоразу»; вікі: вибір перед грою) — можливо, різні версії.
- (?) Розкладка клавіш, HUD-рядки, чи показано час на екрані — не перевірено.
- (?) Розмір рівня (екран?), 8 напрямків руху, лепрекон краде з рюкзака — з памʼяті.
- (?) Формула рахунку — не бачив.
