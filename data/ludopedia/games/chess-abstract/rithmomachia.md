---
title: Rithmomachia (Ритмомахія)
slug: rithmomachia
aka: [Rithmomachy, Rhythmomachia, Arithmomachia, Ludus Philosophorum, "Philosophers' Game", Гра філософів, Rithmomachie]
family: chess-abstract
also: [word-number]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1030
platforms: [board, PC (Ludii)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rithmomachia", best: true, note: "ходи 4 видів, 4 способи взяття, піраміди 91/190, звичайні й «власні» перемоги, історія"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Rithmomachia", note: "Ludii: повні числа обох сторін, 7+1 способів взяття, піраміди, перемога = взяти піраміду + прогресія в чужій половині"}
  - {kind: other, url: "http://jducoeur.org/game-hist/game-recon-rhyth1.html", note: "реконструкція версії Fulke (XVI ст.): «польоти», +−×÷, Oblivion, полонені переходять на твій перший ряд, тріумфи"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Rithmomachie", note: "DE: як утворені числа (n², n(n+1)…), ходи 1–4 за класом, правила Asilo, історія Льєж ~1070"}
  - {kind: other, url: "https://www.sadbhava.ru/asilo/index.html", note: "сучасні правила «ASILO» (RU), з Wikipedia; не відкривав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rithmomachia+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, piece-drop, legal-move-highlight, selection-highlight, hot-seat, turn-enforcement, ai-opponent, cell-click, drag-drop-piece, rule-variants, match-setup, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +capture-in-place, +arithmetic-capture, +custodial-capture, +enclosure-capture, +compound-piece, +capture-count-win, +material-points-win, +progression-win, +agreed-victory-type, +numbered-piece-values]
proposes: ["+cond:value_relation", "+cond:pair_sum", "+cond:progression", "+trigger:capture_available", "+ui:piece-value-label", "+ui:capture-options", "+window:victory-setup", "+card:arithmetic-capture", "+card:progression-win", "+card:agreed-victory-type", "+card:numbered-piece-values"]
author: opus
date: 2026-11-09
---

# Rithmomachia — середньовічна «битва чисел»: фігури з числами бʼють рівністю, добутком на відстань, сумою, облогою; перемога — арифметична, геометрична чи гармонічна прогресія в таборі суперника

## Суть
Гра XI ст. з монастирських шкіл (перша згадка ~1030, монах Asilo), створена вчити теорію чисел за Боецієм. Дві сторони — «парні» й «непарні» — по 24 фігури трьох форм (круги, трикутники, квадрати) плюс складена піраміда; на кожній фігурі число. Фігура бʼє не стаючи на ворога, а коли між числами виконується відношення: рівність, «мале × відстань = велике», сума двох своїх, облога. Найвищі перемоги — вишикувати в половині суперника три-чотири свої фігури, числа яких утворюють прогресії. Правила ніколи не були стандартизовані: є версії Asilo, Boissière (1556), Fulke, Barozzi (1572), Ludii.

## Поле і час
- Дошка 8×16 клітин (8 — коротка сторона), поділена навпіл: кожна сторона стартує на своїй половині.
- Один шар, у клітині ≤1 фігура; піраміда займає одну клітину, хоч складається з 5–6 фігур.
- Покроково, хід = рух однієї фігури; взяття перевіряються після руху й можуть бути кілька за хід (Fulke).
- Числа сторін (за Ludii): **парні (білі)** — круги 2, 4, 6, 8, 4, 16, 36, 64; трикутники 6, 20, 42, 72, 9, 25, 49, 81; квадрати 15, 45, 153, 25, 81, 169, 289; піраміда 91 = 36+25 (квадрати) + 16+9 (трикутники) + 4+1 (круги). **Непарні (чорні)** — круги 3, 5, 7, 9, 9, 25, 49, 81; трикутники 12, 30, 56, 90, 16, 36, 64, 100; квадрати 28, 66, 120, 49, 121, 225, 361; піраміда 190 = 64+49+36+25+16.
- Як утворені (DE-Wikipedia): з основи n (2, 4, 6, 8 або 3, 5, 7, 9) — n², n(n+1), (n+1)², (n+1)(2n+1), (2n+1)²; напр. n=2 → 4, 6, 9, 15, 25.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Круг (round) | piece | число; ×8 на сторону | на 1 клітину по діагоналі (EN-Wikipedia); варіант — на 1 ортогонально (Ludii) |
| Трикутник | piece | число; ×8 | рівно на 2 клітини ортогонально (EN); варіант — 2 по діагоналі (Ludii); у Fulke без взяття — «політ» ходом коня |
| Квадрат | piece | число; ×7 | рівно на 3 клітини ортогонально; у Fulke без взяття — подовжений «кінь» |
| Піраміда (King у Fulke) | piece | 91 (парні) / 190 (непарні); 5–6 складників | ходить як будь-який складник, що в ній ще лишився; бʼє як складник або сумою |
| Сторона (парні / непарні) | player | 24 фігури; рахунок взятих: кількість і сума | ходить по черзі; полонені можуть грати за неї |
| Половина дошки | zone | 8×8 | у половині суперника будуються прогресії «власних» перемог |
| Полонений | piece | число ворожої фігури | за EN-Wikipedia «змінює сторону»; у Fulke — перевертається у твій колір і стає на твій перший ряд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `custom: «to за патерном виду: круг 1 діагональ, трикутник рівно 2 ортогонально, квадрат рівно 3 ортогонально»` і `free(path)` → ТО `move(piece, to)`; перестрибувати не можна.
- КОЛИ `input(move, pyramid, to)` → ЯКЩО `custom: «патерн будь-якого складника, що ще лишився в піраміді»` → ТО `move(pyramid, to)`; втрачено всі круги → зникає й круговий хід.
- Взяття без руху: фігура не стає на ворога, а лишається на місці й знімає його (`+card:capture-in-place`).
- Зустріч (Meeting): КОЛИ `after(move)` → ЯКЩО `same(own_piece, enemy, value)` і `custom: «own_piece міг би ходом стати на клітину enemy»` (`+trigger:capture_available`) → ТО `disappear(enemy)`.
- Напад (Assault): КОЛИ `after(move)` → ЯКЩО `custom: «value(малої своєї) × кількість порожніх клітин між ними = value(більшої ворожої), на одній лінії»` (`+cond:value_relation`) → ТО `disappear(enemy)`; приклад DE: 2 через 8 клітин бʼє 16.
- Засідка (Ambuscade): КОЛИ `after(move)` → ЯКЩО `custom: «ворог між двома своїми, обидві дістають його, і сума їхніх чисел = value(enemy)»` (`+cond:pair_sum`) → ТО `disappear(enemy)`.
- Облога (Siege): КОЛИ `after(move)` → ЯКЩО `adjacent_count(enemy, blocker, ==, 4)` → ТО `disappear(enemy)` — оточено з усіх 4 боків; у Ludii/Fulke — коли ворог не має жодного ходу (Oblivion/Encirclement); для простих чисел у DE — єдиний спосіб.
- Ludii/Fulke розширюють комбінації: КОЛИ `after(move)` → ЯКЩО `custom: «дві свої дістають ворога і різниця / добуток / частка їхніх чисел = value(enemy)»` → ТО `disappear(enemy)`; Ludii ще «value(своєї) ÷ відстань = value(ворога)»; у комбінаціях гравець обирає, яка з двох фігур «бере» (`choose`).
- Fulke (за домовленістю): КОЛИ `after(move)` → ЯКЩО `custom: «дві свої й ворог утворюють арифметичну, геометричну чи гармонічну пропорцію»` → ТО `disappear(enemy)`.
- Піраміду беруть: по одному складнику; облогою цілком; або числом, що дорівнює сумі всіх складників чи основи (Ludii). DE (Asilo): влучили в основу правильним ходом — падають і всі шари над нею.
- КОЛИ `destroyed(enemy)` → ТО `counter(captured_count, +1)`, `counter(captured_value, +value)`; ЯКЩО `mode(fulke)` → ТО `set_side(enemy, captor)`, `place(captor, enemy)` на будь-яку клітину свого першого ряду.
- Перед партією: КОЛИ `game_start` → ТО `choose(тип перемоги і пороги)` — обидва гравці домовляються (`+window:victory-setup`).
- De corpore: КОЛИ `counter(captured_count, >=, N)` → ТО `win`.
- De bonis: КОЛИ `counter(captured_value, >=, V)` → ТО `win` (Fulke радить 100–200).
- De lite: КОЛИ `counter(captured_value, >=, V)` → ЯКЩО `custom: «сумарна кількість цифр на взятих ≤ D»` → ТО `win` (приклад Fulke: 109 очок на 8 «знаках»).
- De honore: КОЛИ `counter(captured_value, >=, V)` → ЯКЩО `counter(captured_count, <=, N)` → ТО `win`; De honore liteque — усі три умови разом.
- Victoria magna: КОЛИ `after(move)` → ЯКЩО `custom: «3 свої фігури на прямій (або «шевроном», Ludii) у половині суперника, на рівних інтервалах»` і `custom: «їхні числа — арифметична прогресія»` (`+cond:progression`) → ТО `win`; у Fulke — будь-яка з трьох пропорцій.
- Victoria major: КОЛИ `after(move)` → ЯКЩО `custom: «4 фігури в лінію чи квадратом у половині суперника, серед них дві різні пропорції»` → ТО `win`.
- Victoria excellentissima: КОЛИ `after(move)` → ЯКЩО `custom: «4 фігури, у трьох групах — усі три пропорції: арифметична, геометрична, гармонічна»` → ТО `win`.
- Ludii й Fulke: «власні» перемоги доступні лише ПІСЛЯ взяття ворожої піраміди / Короля: ЯКЩО `not custom: «піраміду суперника взято»` → ТО прогресія не перемагає.
- Fulke: фігури тріумфу не можуть бути взяті й втрачають «політ»; DE: хто ставить першу фігуру ряду, мусить оголосити — її бити не можна (`set_state(piece, protected)`).
- Прогресії: арифметична — b − a = c − b (2, 5, 8); геометрична — b / a = c / b (4, 16, 64); гармонічна — 1/a, 1/b, 1/c арифметична, тобто (b − a) : (c − b) = a : c (DE-приклад 3, 4, 6).
- Перемога: умова, обрана наперед (звичайна) або прогресія в таборі суперника («власна») · Поразка: суперник виконав її першим · Рахунок: кількість і сума чисел узятих.

## Керування і ввід
- Настільна: пересунути фігуру; оголосити взяття (числова перевірка — усно, за таблицею).
- (цифрова версія, Ludii) Клік по фігурі → `legal-move-highlight` на фіксованій відстані; після руху — список доступних взять (`capture-options`: «зустріч 16 = 16», «засідка 9 + 7 = 16», «напад 2 × 8 = 16») з вибором; для піраміди — вибір складника, яким вона бʼє.
- Наведення на фігуру — `tooltip` з числом і «родиною» (n, n², n(n+1)…).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати · Набір правил → `match-setup` · Таблиця чисел → `help-window`.
- `match-setup` / `victory-setup`: набір правил (Wikipedia / Ludii / Fulke / Asilo), хід кругів (діагональ / ортогональ), тип перемоги й пороги (N фігур, V очок, D цифр), «спершу взяти піраміду» так/ні.
- `game-screen`: дошка 8×16 з лінією поділу; фігури з числами (`piece-value-label`); `turn-indicator`; `captured-pieces` з сумою й кількістю; `selection-highlight`, `legal-move-highlight`; підсвітка можливих прогресій у половині суперника.
- `end-screen`: тип перемоги («Victoria magna: 2–5–8 арифметична»), рахунок узятих.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — головна фіча: версій правил кілька, і вони суттєво різні (хід, способи взяття, доля полонених, передумова перемоги).
- `rules-page` з таблицею чисел обох сторін; `ai-opponent-levels` (Ludii).
- Навчальна мета (історично) — вправи з пропорціями: режим «знайди всі взяття» як тренажер.

## Варіації й родичі
- **Asilo / Льєж (~1070, DE)**: ходи за класом числа — основи на 1, «Vielfache» на 2, «Überteilige» на 3, «Mehrfachteilige» на 4 клітини; прямо або під прямим кутом; піраміда: удар по основі знімає всі шари вище.
- **Fulke (XVI ст.)**: «польоти» трикутника й квадрата ходом коня/подовженого коня (лише без взяття); полонені — на твій перший ряд; тріумфи лише після взяття Короля.
- **Ludii**: 7+1 способів взяття (×відстань, ÷відстань, +, −, ×, ÷ двох, оточення); перемога = піраміда + прогресія.
- Варіант піраміди лише з квадратів (Wikipedia) — змінює її хід.
- Родичі: [chess](chess.md) (історично Ритмомахію друкували додатком до шахових книжок), [chaturanga-shatranj](chaturanga-shatranj.md), [hnefatafl](hnefatafl.md) (взяття затиском), [go](go.md) (облога).
- **Осі варіацій**: умова взяття (позиція — шахи / числове відношення — Ритмомахія) · чи рухається той, хто бере (так / ні) · доля полонених (зникають / переходять до тебе) · мета (кількість / сума / цифри / прогресія) · обовʼязкова передумова (взяти піраміду / ні).

## Цікавинки для курсу
- Перевірка взять як таблиця предикатів над парами/трійками фігур (=, ×відстань, +, −, ×, ÷) — 📎; додати режим «гравець обирає взяття зі списку» — 🥉.
- Ходи «рівно на N» без перестрибування + «політ» конем лише без взяття — 🌱.
- Піраміда як складена фігура: хід за наявними складниками, взяття по шарах — 🥉.
- Пошук прогресій: усі трійки/четвірки на прямій із рівним кроком у чужій половині, перевірка трьох типів пропорцій — 🥉.
- Конструктор правил (4 версії × тип перемоги × пороги) — 🥈.
- AI: перебір ускладнений тим, що взяття «дистанційні» і їх багато за хід — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 1 діагональ / рівно 2 / рівно 3 · `piece-capture` · `piece-drop` ↔ Fulke: полонений стає твоїм і ставиться на перший ряд · `legal-move-highlight`, `selection-highlight` · `hot-seat`, `turn-enforcement`, `ai-opponent` · `cell-click`, `drag-drop-piece` · `rule-variants` ↔ версії правил · `match-setup` · вікна `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+capture-in-place` (взяття без руху, як igui у великих сьоґі) · `+custodial-capture` (засідка — затиск з числовою умовою) · `+enclosure-capture` (облога) · `+compound-piece` (піраміда) · `+capture-count-win` (de corpore) · `+material-points-win` (de bonis).
- **Нема** → пропозиції карток:
  - `+arithmetic-capture` «Взяття за числовим відношенням між фігурами» · entities/combat · 🥉 · слоти {ops: [eq, mul_distance, sum, diff, prod, quot]}.
  - `+progression-win` «Перемога: свої числа на прямій утворюють прогресію» · game-logic/win · 🥉 · слоти {kinds: [arith, geom, harm], n: 3|4, zone: enemy_half}.
  - `+agreed-victory-type` «Гравці обирають умову перемоги й пороги перед партією» · game-logic/win · 🌱 · слоти {types: [corpore, bonis, lite, honore]}.
  - `+numbered-piece-values` «Фігура несе число, що бере участь у правилах» · entities/state · 🌱 (відмінне від `+numbered-pieces` пазлів).

## Пропозиції до словників
- `+cond:value_relation(a, b, op, k)` — числове відношення між значеннями двох фігур з параметром (відстань): ×, ÷, =.
- `+cond:pair_sum` — підтверджую (number-match): сума значень двох своїх = значення цілі; тут ще й «обидві дістають ціль».
- `+cond:progression(pieces, kind)` — значення фігур утворюють арифметичну / геометричну / гармонічну прогресію.
- `+trigger:capture_available` — після ходу на полі зʼявилась легальна «дистанційна» можливість взяти (взяття не ходом на клітину).
- `+ui:piece-value-label` — число на фігурі як головний елемент рендера; `+ui:capture-options` — список доступних взять з формулами.
- `+window:victory-setup` — вибір типу перемоги й порогів перед партією.
- `+card:arithmetic-capture`, `+card:progression-win`, `+card:agreed-victory-type`, `+card:numbered-piece-values` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rithmomachia](https://en.wikipedia.org/wiki/Rithmomachia) — дошка 8×16, ходи кругів/трикутників/квадратів/пірамід, Meeting/Assault/Ambuscade/Siege, «взяття без руху», полонені змінюють сторону, піраміди 91 і 190, de corpore … excellentissima, історія (Asilo ~1030, Hermannus Contractus, Barozzi 1572, Arno Borst).
- [Ludii: Rithmomachia](https://ludii.games/details.php?keyword=Rithmomachia) — повні числа обох сторін, ходи (інші, ніж у Wikipedia), 7+1 способів взяття, піраміда, перемога = взяти піраміду + прогресія на рівних інтервалах (лінія чи шеврон); джерела Murray 1951, Stigter 2007.
- [jducoeur: Fulke's Rhythmomachia](http://jducoeur.org/game-hist/game-recon-rhyth1.html) — «польоти», +−×÷, пропорція за домовленістю, Oblivion, полонені на перший ряд, звичайні перемоги з прикладами (100–200 очок; 109 на 8 знаках), тріумфи після взяття Короля.
- [Wikipedia DE: Rithmomachie](https://de.wikipedia.org/wiki/Rithmomachie) — формули чисел від основи n, ходи 1–4 за класом, правила Asilo (2 через 8 клітин бʼє 16; облога для простих чисел), Льєжська версія ~1070, Odo von Tournai, оголошення першої фігури ряду.
- [Game Cabinet: правила Boissière 1556](http://www.gamecabinet.com/rules/Rithmomachia.html) — посилання з Wikipedia; не відкрилось.
- YouTube: пошук «rithmomachia how to play».

## Непевне
- (?) Ходи розходяться: Wikipedia — круг по діагоналі, трикутник рівно 2 ортогонально; Ludii — круг ортогонально, трикутник 2 по діагоналі; DE (Asilo) — 1/2/3/4 за класом, а не формою. Записано за Wikipedia.
- (?) Розстановка фігур на половинах (які клітини) — на схемах джерел, яких не бачив.
- (?) Доля полонених: Wikipedia — «змінює сторону», Fulke — на твій перший ряд, DE — «знімаються, згодом повертаються»; одного правила нема.
- (?) Чи обовʼязкове взяття піраміди перед «власною» перемогою — лише в Ludii та Fulke.
- (?) У Ludii «Victoria major» / «excellentissima» не описані; склад пропорцій у major (які саме дві) — у Wikipedia неповно.
- (?) Хто ходить першим — у джерелах не знайшов.
- (?) Рік у шапці 1030 — дата першого письмового свідчення («близько 1030»), а не точна дата винайдення.
