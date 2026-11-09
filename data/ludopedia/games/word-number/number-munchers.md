---
title: Number Munchers / Word Munchers
slug: number-munchers
aka: [Math Munchers, Math Munchers Deluxe, Word Munchers, Word Munchers Deluxe, Munchers]
family: word-number
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1986
platforms: [Apple II, MS-DOS, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Number_Munchers", best: true, note: "режими Multiples / Factors / Primes / Equality / Inequality / Challenge, 5 видів Troggles і їхня поведінка, безпечні клітини, 4 життя, кількість Troggles за рівнями, катсцени кожні 3 рівні"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Word_Munchers", note: "Word Munchers 1985: голосні звуки, 1–5 класи, Deluxe 1996"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Munchers", note: "серія: частини мови в Word Munchers, Fraction / Super Munchers, Math Munchers Deluxe 1995, стрілки → миша"}
  - {kind: other, url: "https://chalkdustmagazine.com/blog/review-number-munchers/", note: "огляд: сітка 5×6, стрілки + пробіл, «1 is not prime», 11 рівнів складності за класами"}
  - {kind: other, url: "https://Allthetropes.org/wiki/Number_Munchers", note: "Troggles їдять одне одного, додаткові життя за очки, Hall of Fame з повідомленням, катсцени серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Number+Munchers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, touch-death, player-death, wrong-mark-lose, collect-all, chase-greedy, random-walk, turn-when-blocked, progress-acceleration, extra-life-threshold, event-points, score-records, leaderboard, sequential-levels, difficulty-levels, difficulty-select, mode-select, game-screen, end-screen, splash-screen, objective-text, +rule-predicate-cells, +flee-player, +content-eater-enemy, +content-rewriter-enemy, +safe-zone-cell, +enemy-eats-enemy, +intermission-cutscene, +hall-of-fame-message, +random-rule-mode]
proposes: ["+cond:matches_rule", "+effect:flee", "+feature:teacher-dashboard", "+feature:seasonal-skin", "+card:rule-predicate-cells", "+card:content-rewriter-enemy", "+card:safe-zone-cell"]
author: opus
date: 2026-11-09
---

# Number Munchers — зелений Muncher їсть на сітці лише числа, що підходять під правило («кратні 5», «прості»), і тікає від Troggles

## Суть
Освітня аркада MECC (дизайнер R. Philip Bouchard): Muncher ходить по сітці 5×6, у кожній клітині — число чи вираз, а згори — правило рівня. Треба зʼїсти **всі й лише** клітини, що задовольняють правило; хибна клітина чи дотик Troggle коштують життя. П'ять видів Troggles мають різну поведінку — один іде прямо, другий тікає, третій переслідує, а двоє змінюють саме поле: зʼїдають відповіді або дописують нові. Word Munchers (1985) — та сама гра зі словами й правилами про звуки та частини мови.

## Поле і час
- Сітка 5 × 6 клітин (огляд Chalkdust), у кожній — число, вираз («3 × 2») або слово; рядок правила над сіткою.
- Шари: клітина (вміст / порожньо після зʼїдання / безпечна) + сутності (Muncher, Troggles).
- Real-time: Muncher ходить по клітині за натиск, Troggles — своїм таймером; з рівня ~18 Troggles пришвидшуються. Гру можна грати й повільно — Troggles лише кілька.
- Кількість Troggles: рівні 1–3 — один, з 4-го — два, з 8-го — три.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Muncher | player | 4 життя (1 у грі + 3 у запасі) | рух 4 напрямки по клітинах; пробіл — зʼїсти вміст клітини |
| Клітина-відповідь | tile | число / вираз / слово | правильна, якщо задовольняє правило рівня; зʼїдена — порожня |
| Безпечна клітина | zone | позначка: 4 маленькі білі прямокутники в кутку | Troggles не входять; Troggle на ній гине; зникає випадково |
| Reggie | enemy | — | іде по прямій; безпечна клітина змінює його напрям |
| Bashful | enemy | — | ходить довільно, тікає, коли Muncher наближається |
| Helper | enemy | — | «мураха»: зʼїдає всі відповіді на шляху, не лишаючи нічого |
| Worker | enemy | — | дорогою додає нові відповіді або змінює наявні |
| Smartie | enemy | — | найнебезпечніший: завжди йде за Muncher |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(arrow)` → ТО `move(muncher, dir)`; на краю сітки — `block`.
- КОЛИ `input(space)` → ЯКЩО `custom: «вміст клітини задовольняє правило рівня»` → ТО `disappear(content)`, `score(+n)`.
- КОЛИ `input(space)` → ЯКЩО `custom: «вміст не задовольняє правило»` → ТО `lives(-1)`, `message(«1 is not prime»)` — пояснення, чому хибно.
- КОЛИ `contact(troggle, muncher)` → ТО `lives(-1)`.
- КОЛИ `all_gone(correct answers)` → ТО `next_level`; правила й числа складнішають.
- КОЛИ `level_start` → ЯКЩО `level(>=, 4)` → ТО `spawn(troggle)` — другий Troggle.
- КОЛИ `level_start` → ЯКЩО `level(>=, 8)` → ТО `spawn(troggle)` — третій.
- КОЛИ `level_start` → ЯКЩО `level(>, 18)` → ТО `speed(troggles, +n)`.
- КОЛИ `timer(troggle_step)` → ТО `move(reggie, dir)` — по прямій.
- КОЛИ `blocked(reggie)` (безпечна клітина попереду) → ТО `face(reggie, new_dir)`.
- КОЛИ `timer(troggle_step)` → ЯКЩО `in_range(bashful, muncher, n)` → ТО `custom: «крок від Muncher»`; інакше `move(bashful, rng_dir)`.
- КОЛИ `timer(troggle_step)` → ТО `custom: «Smartie робить крок у бік Muncher»`.
- КОЛИ `enter(helper, answer cell)` → ТО `disappear(content)` — і правильні і хибні, без очок гравцю.
- КОЛИ `leave(worker, cell)` → ТО `set_value(cell, new answer)` або `spawn_at(answer, cell)`.
- КОЛИ `contact(troggle, troggle)` → ТО `custom: «один Troggle зʼїдає іншого»` (навіть однакового виду), `disappear_b`.
- КОЛИ `enter(troggle, safe cell)` → ТО `block`.
- КОЛИ `spawned(safe cell)` → ЯКЩО `occupied(cell, troggle)` → ТО `disappear(troggle)` (пізніше може зʼявитися заміна).
- КОЛИ `rng(p)` → ТО `custom: «безпечна клітина зникає»` — довго на ній не постоїш.
- КОЛИ `counter(score, >=, 1000)` → ТО `lives(+1)`; ще одне — на 10 000 (All The Tropes).
- КОЛИ `level_end` → ЯКЩО `custom: «пройдено третій шостий… рівень»` → ТО `window(dialogue-window)` — катсцена «Great Moments in Muncher History» (6 сцен, після 21-го рівня повторюються).
- КОЛИ `level_start` → ЯКЩО `mode(challenge)` → ТО `custom: «випадковий тип правила»`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`; ЯКЩО `custom: «очок досить для Hall of Fame»` → ТО `window(leaderboard)` — імʼя і повідомлення.
- Перемога: нема фіналу — рівні йдуть далі · Поразка: життя вичерпано · Рахунок: очки за правильні клітини; Hall of Fame.

## Керування і ввід
- Стрілки — крок Muncher на сусідню клітину; пробіл — зʼїсти вміст клітини (Chalkdust).
- Ранні версії — лише клавіатура; пізніші (Math Munchers Deluxe) — миша.
- Вибір типу гри й складності — меню перед партією (батьки / вчитель налаштовують складність).

## Вікна, меню, HUD
- `splash-screen` — титул.
- `mode-select`: Multiples · Factors · Primes · Equality · Inequality · Challenge (мікс правил).
- `difficulty-select`: 11 рівнів від «third grade easy» до «eighth grade and above» (за оглядом Chalkdust (?)).
- `game-screen`: `objective-text` — правило рівня згори («Multiples of 5», «Equals 6», «Less than 12»), сітка 5×6, `score`, `lives` (запасні Munchers), `level-number` (?).
- Модал помилки: текст-пояснення («1 is not prime») — `message`.
- `dialogue-window` — катсцена кожні 3 рівні.
- `end-screen` (кінець гри) → `leaderboard` Hall of Fame з повідомленням переможця.
- Переходи: splash → mode-select → difficulty-select → game-screen → (усі правильні зʼїдено) наступний рівень / кожні 3 рівні катсцена → (життя 0) end-screen → Hall of Fame.

## Фічі поза полем
- `mode-*` за типом правила + `custom-rules`-подібний Challenge (випадковий мікс); `difficulty-presets` за класами.
- `levels-sequential` нескінченно з наростанням: більші числа, складніші правила, більше й швидші Troggles.
- `leaderboard-local` Hall of Fame з власним повідомленням.
- School Version: вчитель обʼєднує копії класу в мережу й стежить за ними — `teacher-dashboard`.
- Пасхалка: з 1 до 25 грудня Muncher у шапці Санти — `seasonal-skin` (за системним годинником).

## Варіації й родичі
- **Word Munchers** (1985, Apple II; DOS / Mac 1991; Deluxe 1996): правила — голосні звуки, частини мови (дієслова, прикметники); вчитель обирає звуки й складність, зокрема слова-винятки; 1–5 класи.
- **Number Munchers** (1986 Apple II; DOS / Mac 1990) → **Math Munchers Deluxe** (1995, 3D-оновлення, миша).
- **Fraction Munchers** — дроби, олімпійські катсцени; **Super Munchers** — Muncher перетворюється на «супер»-форму й перемагає Troggles; Knowledge (Trivia) Munchers Deluxe; спін-оф Troggle Trouble Math.
- **Осі варіацій:** вміст клітини (число / вираз / слово / дріб / факт) · правило (властивість одного числа / рівність / нерівність / мікс) · поведінка ворога (прямо / тікає / переслідує / змінює поле) · ворог проти ворога (зʼїдає / ігнорує).
- Родичі: [../maze-arcade/pac-man.md](../maze-arcade/pac-man.md) (рух по сітці, вороги з різною поведінкою), [bingo.md](bingo.md) (позначити клітини за правилом), [nyt-connections.md](nyt-connections.md) (групування за ознакою).

## Цікавинки для курсу
- Правило рівня як предикат (`is_multiple(5)`, `is_prime`, `expr == 6`, `expr != 6`) + генерація сітки з потрібною часткою правильних клітин — 🌱 (чиста функція над числом).
- П'ять поведінок Troggles: прямо з розворотом, утеча від гравця, переслідування, «їдець» вмісту, «переписувач» вмісту — 🥉 за сімʼю, кожна 📎.
- Ворог, що змінює поле (Helper стирає, Worker дописує) — після кожного кроку перераховувати «скільки правильних лишилось» — 📎.
- Безпечні клітини: зʼявляються й зникають випадково, Troggle на них гине — 📎.
- Troggles їдять одне одного при зустрічі — 🌱 (прибирання дублікатів у клітині).
- Наростання складності за рівнем (кількість Troggles, швидкість, діапазон чисел) — 🌱.
- Модал «чому хибно» з поясненням правила — 🌱, але найцінніше для освітньої гри.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки · `touch-death` + `player-death` ↔ Troggle · `wrong-mark-lose` ↔ хибна клітина · `collect-all` ↔ усі правильні · `chase-greedy` ↔ Smartie · `random-walk` ↔ Bashful · `turn-when-blocked` ↔ Reggie · `progress-acceleration` ↔ швидші й численніші Troggles · `extra-life-threshold` ↔ 1000 / 10 000 · `event-points` + `score-records` + `leaderboard` ↔ Hall of Fame · `sequential-levels` + `difficulty-levels` · `difficulty-select` + `mode-select` · `game-screen`, `end-screen`, `splash-screen`, `objective-text`.
- **Нема** → пропозиції карток:
  - `+rule-predicate-cells` «Зібрати лише клітини, що задовольняють правило» · game-logic/win · 🌱 · слот {rule}.
  - `+flee-player` «Ворог тікає від гравця» · entities/move · 📎.
  - `+content-eater-enemy` «Ворог стирає вміст клітин» · entities/interact · 📎.
  - `+content-rewriter-enemy` «Ворог дописує / змінює вміст клітин» · entities/interact · 📎.
  - `+safe-zone-cell` «Клітина-сховок: вороги не входять, зʼявляється й зникає» · entities/legality · 📎.
  - `+enemy-eats-enemy` «Вороги знищують одне одного при зустрічі» · entities/interact · 🌱.
  - `+intermission-cutscene` «Катсцена кожні N рівнів» · interface/menus · 🌱.
  - `+hall-of-fame-message` «Рекорд з повідомленням гравця» · interface/results · 🌱.
  - `+random-rule-mode` «Режим, що змішує типи правил» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:matches_rule` — вміст клітини задовольняє правило рівня (Munchers, Bingo-подібні).
- `+effect:flee` — сутність робить крок від цілі (Bashful).
- `+feature:teacher-dashboard` — вчитель обʼєднує копії класу й бачить прогрес учнів.
- `+feature:seasonal-skin` — вигляд за датою годинника (шапка Санти в грудні).
- `+card:rule-predicate-cells`, `+card:content-rewriter-enemy`, `+card:safe-zone-cell` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Number Munchers](https://en.wikipedia.org/wiki/Number_Munchers) — режими, Troggles (Reggie, Bashful, Helper, Worker, Smartie), безпечні клітини, 4 життя, кількість Troggles за рівнями, прискорення після ~18, катсцени, пасхалка, School Version.
- [Wikipedia: Word Munchers](https://en.wikipedia.org/wiki/Word_Munchers) — 1985, голосні звуки, порти й Deluxe.
- [Wikipedia: Munchers](https://en.wikipedia.org/wiki/Munchers) — серія, частини мови, «зʼїсти всі й лише», стрілки → миша, Math Munchers Deluxe 1995.
- [Chalkdust: review Number Munchers](https://chalkdustmagazine.com/blog/review-number-munchers/) — сітка 5×6, стрілки + пробіл, «1 is not prime», 11 рівнів складності.
- [All The Tropes: Number Munchers](https://Allthetropes.org/wiki/Number_Munchers) — Troggles їдять одне одного, життя на 1000 і 10 000, Hall of Fame з повідомленням.
- YouTube: пошук «Number Munchers gameplay».

## Непевне
- (?) Очки за правильну клітину й чи є бонус за рівень — не знайдено.
- (?) Звідки зʼявляються Troggles (з-за краю сітки з попередженням?) і як повертається Muncher після втрати життя — з памʼяті, не перевірено.
- (?) «Кулі, які стріляють Troggles» (All The Tropes) — імовірно, з пізніших Deluxe-версій; в оригіналі 1986 не підтверджено.
- (?) 11 рівнів складності за класами — з огляду Chalkdust; яка саме версія гри — не сказано.
- (?) Сітка Word Munchers — та сама 5×6? Джерела мовчать.
- Черга: рік Word Munchers 1985 раніший за Number Munchers 1986 — так і є за Wikipedia; Number Munchers вважається першою грою серії лише в статті Munchers.
