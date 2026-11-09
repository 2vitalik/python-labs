---
title: Inkulinati
slug: inkulinati
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2024
platforms: [PC, Mac, Xbox, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/957960/Inkulinati/", note: "опис: звірі, Hand Actions, горщики з бобами, апокаліпсиси, Journey/Academy/hotseat"}
  - {kind: other, url: "https://news.xbox.com/en-us/2023/01/31/seven-tips-to-become-the-best-inkulinati-master/amp", best: true, note: "7 порад від розробників: Living Ink, стартові 5 звірів, Tiny Inkulinati, смерть за краєм, Hand Actions, діапазони"}
  - {kind: other, url: "https://www.thegamer.com/inkulinati-best-beasts-units/", note: "звірі з уміннями: Bishop Cat, Exploders, Donkey Bard, Devil, Skeleton"}
  - {kind: other, url: "https://blogs.plitch.com/en/blog/8-important-inkulinati-tips-and-tricks", note: "нудьга (boredom), брама суперника, апокаліпсис-вогонь від країв, втеча й пера"}
  - {kind: other, url: "https://www.thegamer.com/inkulinati-hildegard-boss-fight-strategy-guide/", note: "калюжі чорнила, Hand Action «Take a Nap», бос"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Inkulinati+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [push-object, environment-death, hp-damage, melee-vs-ranged, explode-area, chain-detonation, status-effects, temporary-modes, round-currency, item-pickup, ai-opponent, hot-seat, world-map, map-window, codex-window, tutorial-window, difficulty-levels, permadeath, reachable-highlight, threat-range, hover-highlight, game-screen, +ring-out, +summon-for-ink, +escalating-summon-cost, +shrinking-arena, +avatar-protect, +hand-actions, +nap-state, +boredom-fatigue, +explode-on-death, +delayed-doom-status]
proposes: ["+trigger:chapter_end", "+effect:ring_out", "+effect:summon_for_cost", "+effect:knockback", "+cond:cost", "+role:avatar-commander", "+ui:ink-counter", "+window:journey-map", "+feature:roster-fatigue"]
author: opus
date: 2026-11-09
---

# Inkulinati — тактика на сторінці середньовічного рукопису: малюєш звірів живим чорнилом і виштовхуєш ворогів за край аркуша

## Суть
Гравець — Inkulinatus, маг-ілюстратор, що б'ється на полях рукопису проти інших майстрів. На полі є його маленьке втілення **Tiny Inkulinatus**: його треба вберегти, а ворожого — вбити. Армію **малюють за Living Ink** — чорнило збирають на полі, і кожен новий звір дорожчає. Головний прийом — **штовхнути** звіра чи навіть Tiny за край сторінки: це миттєва смерть, навіть для літунів. Поверх — «руки майстра» (Hand Actions): вдарити кулаком, перенести юніта, намалювати барʼєр, підірвати свого.

## Поле і час
- Поле — сторінка рукопису, поділена на клітини; за краєм — «ніщо» (смерть). Брама суперника — особлива зона: заштовхнутий у неї отримує додаткову шкоду (з вогнищем — ще більше).
- Обʼєкти поля: горщики з бобами (вибухають, ранять до 4 звірів), хмари благословення, вогнища, калюжі чорнила; кожне поле має свої небезпеки.
- Час: покроково, раунди-«розділи» (chapters); за свій хід гравець перемикається між своїми юнітами, кожен робить свою дію.
- Апокаліпсис: після певної кількості раундів почавши від країв щораунду вогонь просувається на клітину всередину і вбиває, кого торкнувся (поле стискається); також пошесті тощо.
- Інформація повна: наведення показує діапазони руху й дії кожного звіра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Tiny Inkulinatus (свій) | player | HP, таланти | аватар майстра на полі; його смерть — програш; можна виштовхнути |
| Tiny Inkulinatus (ворожий) | boss | HP | головна ціль бою |
| Звір (Beast) | ally | клас, HP, вартість чорнила, вміння | рух, атака, штовх або сон; на старті — 5 обраних, далі малюються |
| Bishop Cat | ally | — | лікує 5 і дає 2 Halo; Anointed робить ворогів Heretics (×2 шкоди від Anointed); Power Word — дальня атака, сильніша по Heretics |
| Jaw Exploder | ally | 5 чорнила | б'є обидві сусідні клітини; при смерті вибух 5 по сусідах і +1 Living Ink; підрив вручну |
| Cook Exploder | ally | — | Stew Catapult — дальній вибух 5; Bean Time лікує 5 + Bloated; Double Bloated — ширший вибух; ще раз — вибух одразу |
| Donkey Bard | ally | — | Blow the Bagpipes будить союзника на додатковий хід + Motivation; Farting the Pipe — вороги в радіусі 3 засинають + «головний біль» (без руху наступного ходу) |
| Devil (з міхом) | ally | імунітет до Fire Sparks | Pyroflatulence: 3 клітини Fire Sparks (3 шкоди тому, хто закінчив там хід); Puff of Bellows вбиває звіра на Fire Sparks; присипляє сусіда |
| Skeleton (флейта) | ally | 7 HP, дальність 6 | Danse Macabre: 5 шкоди в кінці розділу, якщо ціль не атакувала, не була штовхнута й не отримала Halo; Stinking Breath — Infection на клітину |
| Равлик (heavy snail) | ally | — | поїдає юнітів |
| Rabbit (кролик) | ally | дешевий | масовий дешевий звір (бос Hildegard) |
| Літун | ally | — | теж гине за краєм |
| Living Ink | resource | лічильник | валюта малювання звірів |
| Калюжа чорнила | pickup | — | звір, що закінчив тут хід, дає чорнило |
| Горщик з бобами | hazard | — | вибухає, шкода до 4 звірів поруч |
| Вогнище | hazard | — | посилює шкоду заштовхнутому в браму |
| Хмара благословення | object | — | ефект благословення (?) |
| Брама суперника | zone | — | заштовхнутий у неї звір отримує додаткову шкоду |
| Fire Sparks / Infection | hazard | тривалість | клітинні стани від умінь |
| Апокаліптичний вогонь | hazard | фронт від країв | щораунду на клітину ближче до центру; вбиває при дотику |
| Край сторінки | hazard | — | будь-що виштовхнуте за край — знищене |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `place(player, beast)` ×5 — обрані звірі вже на полі без витрати чорнила.
- КОЛИ `input(draw_beast, cell)` → ЯКЩО `custom: «Living Ink ≥ вартості»` → ТО `spawn(beast, cell)`, `currency(−cost)`; `custom: «вартість наступних звірів зростає»`.
- КОЛИ `turn_end(beast)` → ЯКЩО `occupied(cell, ink_puddle)` → ТО `currency(+n)`.
- КОЛИ `input(unit_action, beast)` → ТО одна дія звіра: `move` · атака · `push` · сон; після дії — `end_turn` для цього звіра.
- КОЛИ `input(push, target)` → ЯКЩО `adjacent(beast, target)` → ТО `push(target)`; ЯКЩО `occupied(dest, unit)` → ТО `custom: «ковзає до першої вільної клітини»` (?).
- КОЛИ `edge(a)` → ТО `disappear(a)` — миттєва смерть, хоч скільки HP, навіть літуна; ЯКЩО `a` = Tiny → ТО `lose`/`win`.
- КОЛИ `custom: «звіра заштовхнуто в браму суперника»` → ТО `damage(n)`; ЯКЩО `custom: «поруч вогнище»` → ТО більше.
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(beast, target, r)` → ТО `damage(n)`.
- КОЛИ `contact(explosion, pot_of_beans)` або `input(attack, pot_of_beans)` → ТО `explode(area, —)`: `damage(n)` до 4 звірам.
- КОЛИ `died(jaw_exploder)` → ТО `explode(adjacent, 5)`, `currency(+1)`.
- КОЛИ `input(bean_time, beast)` → ТО `heal(beast, 5)`, `set_state(beast, bloated)`; ЯКЩО `state(beast, double_bloated)` → ТО `custom: «вибухає одразу»`.
- КОЛИ `input(farting_the_pipe)` → ТО вороги в `in_range(bard, enemy, 3)`: `set_state(enemy, nap)` + `set_state(enemy, headache, 1)` (без руху наступного ходу).
- КОЛИ `state_on(beast, nap)` → ТО `custom: «хід звіра закінчено»`; КОЛИ `input(blow_the_bagpipes, ally)` → ТО `clear_state(ally, nap)`, `extra_move`, `set_state(ally, motivation)`.
- КОЛИ `turn_end(unit)` → ЯКЩО `cell(cell, fire_sparks) and not state(unit, devil)` → ТО `damage(3)`; КОЛИ `input(puff_of_bellows, unit)` → ЯКЩО `cell(cell, fire_sparks)` → ТО `disappear(unit)`.
- КОЛИ `custom: «кінець розділу»` → ЯКЩО `state(target, danse_macabre) and custom: «не атакував, не штовхнутий, без Halo»` → ТО `damage(5)`.
- КОЛИ `input(anoint, ...)` → ТО `set_state(enemy, heretic)`; КОЛИ `contact(anointed_attack, heretic)` → ТО `damage(n × 2)`.
- КОЛИ `input(hand_action, kind)` → ТО `damage(n)` (кулак) · `teleport(unit, cell)` (перенести) · `set_cell(cell, barrier)` (намалювати барʼєр) · `explode(own_unit)` (підірвати свого) · `set_state(enemy, nap)` (Take a Nap, мала дальність).
- КОЛИ `counter(round, >=, n)` → ТО `custom: «апокаліпсис»`; КОЛИ `custom: «кожен наступний раунд»` → ТО `custom: «вогонь просувається на 1 клітину від країв»`; КОЛИ `contact(fire, unit)` → ТО `disappear(unit)`.
- КОЛИ `hp_zero(enemy_tiny)` або `edge(enemy_tiny)` → ТО `win`; КОЛИ `hp_zero(player)` або `edge(player)` → ТО `lose`.
- КОЛИ `custom: «звір брав участь у бою»` → ТО `counter(boredom, +1)` → `custom: «вартість чорнила зростає наступного бою»`; відпочинок звіра знижує нудьгу.
- КОЛИ `input(flee)` → ТО `custom: «втеча: без нагороди, мінус пера»`; пера потрібні, щоб воскресити звірів після поразки.
- Перемога: убити або виштовхнути ворожого Tiny Inkulinatus (у боях зі звірами — перебити їх) · Поразка: загибель свого Tiny · Рахунок: — (кампанія — престиж).

## Керування і ввід
- Миша/геймпад: вибір звіра → підсвітка руху й дії при наведенні → клітина/ціль; перемикання між звірами в межах ходу.
- Окрема панель Hand Actions майстра (великою рукою над рукописом: тицьнути пальцем, вдарити, перенести).
- Малювання нового звіра — вибір з колекції й клітини (?).
- Hotseat: двоє людей за одним пристроєм.

## Вікна, меню, HUD
- `main-menu`: Journey · Academy (навчання) · Hotseat · налаштування.
- `map-window` — мапа Journey: території для завоювання, майстри (Death, Dante Alighieri), дикі звірі.
- `character-select` — створення свого Inkulinatus і вибір 5 стартових звірів.
- `codex-window` — бестіарій звірів, що поповнюється в Journey.
- `game-screen`: сторінка-поле; `hp-bar` звірів; лічильник Living Ink; `reachable-highlight` і `threat-range` при наведенні; панель Hand Actions (`ability-buttons`); `end-turn-button`; текст-хроніка бою, що генерується процедурно (`message-log`).
- `upgrade-window` — перки/таланти майстра між боями.
- `end-screen` — результат бою; вибір втечі.
- `difficulty-select` — кілька рівнів складності.

## Фічі поза полем
- Journey: кампанія з процедурною мапою територій, приручення диких звірів, перки, престиж → нові звірі й механіки.
- Нудьга (boredom): звір, якого часто беруть у бій, дорожчає в чорнилі; змушує ротацію армії.
- Пера (quills) — валюта воскресіння звірів після поразки; втеча з бою їх коштує.
- Academy — покрокове навчання; кілька рівнів складності; hotseat.

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) і [fights-in-tight-spaces](fights-in-tight-spaces.md) (штовхання за край = смерть), [hoplite](hoplite.md) (виштовхування в лаву), [duelyst](duelyst.md) (генерал-аватар на полі, юніти за ресурс), [archon](archon.md) (дуель майстрів).
- **Осі варіацій**: смерть — HP / ring out / брама суперника · армія — фіксований загін / малювання за ресурс з наростаючою ціною · поле — стале / стискається вогнем від країв · аватар — поза полем / на полі й уразливий (Tiny).

## Цікавинки для курсу
- Ring out: будь-що за краєм гине, навіть літун; поштовх у браму — бонус шкоди — 🌱.
- Малювання юнітів за ресурс, що дорожчає з кожним новим — 📎 (крива вартості).
- Поле, що стискається вогнем від країв після N раундів — 📎.
- Звір-бомба: вибух при смерті з поверненням ресурсу; «Bloated → Double Bloated → вибух» як лічильник станів — 🥉.
- Відкладена шкода Danse Macabre, яку знімає дія, поштовх або Halo — 🥉 (умова через історію ходу).
- Hand Actions майстра поверх ходу юнітів — 📎.
- Нудьга як штраф за повтор ростеру між боями — 🌱.

## Мапа на каталог
- Є: `push-object` ↔ штовх · `environment-death` ↔ край сторінки, апокаліптичний вогонь · `hp-damage` · `melee-vs-ranged` · `explode-area` / `chain-detonation` ↔ горщики, Exploders · `status-effects` / `temporary-modes` ↔ nap, Bloated, Heretic, Halo, Danse Macabre · `round-currency` ↔ Living Ink · `item-pickup` ↔ калюжі чорнила · `ai-opponent` · `hot-seat` · `world-map` / `map-window` ↔ Journey · `codex-window` ↔ бестіарій · `tutorial-window` ↔ Academy · `difficulty-levels` · `permadeath` ↔ загибель звірів (воскресіння за пера) · `reachable-highlight` / `threat-range` / `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+ring-out` «Виштовхнутий за край гине» · entities/death · 🌱.
  - `+summon-for-ink` «Виклик юніта за ресурс на полі» · game-logic/economy · 📎.
  - `+escalating-summon-cost` «Кожен виклик дорожчає» · game-logic/economy · 🌱.
  - `+shrinking-arena` «Поле стискається від країв після N раундів» · world/levels · 📎 · {start_round}.
  - `+avatar-protect` «Командир-аватар на полі: смерть = поразка» · game-logic/lose · 🌱.
  - `+hand-actions` «Окремі дії гравця поверх юнітів» · game-logic/turns · 📎.
  - `+nap-state` «Сон: юніт пропускає хід, будиться вмінням» · entities/state · 🌱.
  - `+boredom-fatigue` «Штраф за повторне використання юніта між боями» · game-logic/economy · 🌱.
  - `+explode-on-death` «Вибух при смерті» · entities/combat · 🌱.
  - `+delayed-doom-status` «Відкладена шкода, що знімається дією» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:chapter_end` — кінець розділу/раунду (Danse Macabre).
- `+effect:ring_out` — знищити сутність, виштовхнуту за край поля (зараз `edge` + `disappear`).
- `+effect:summon_for_cost` — виклик юніта за ресурс (відмінно від `spawn` без ціни і `place` з запасу).
- `+effect:knockback` — відкинути на N клітин.
- `+cond:cost` — вистачає ресурсу на дію (Living Ink).
- `+role:avatar-commander` — аватар гравця серед юнітів, смерть якого = поразка.
- `+ui:ink-counter` — лічильник ресурсу виклику з поточною ціною.
- `+window:journey-map` — кампанійна мапа територій із майстрами.
- `+feature:roster-fatigue` — нудьга/втома юнітів між боями.

## Джерела
- ⭐ [Xbox Wire: Seven tips to become the best Inkulinati master](https://news.xbox.com/en-us/2023/01/31/seven-tips-to-become-the-best-inkulinati-master/amp) — Living Ink і зростання ціни, 5 стартових звірів, Tiny Inkulinati, смерть за краєм, Hand Actions, горщики, вогнища й брама, діапазони при наведенні, Journey.
- [Steam](https://store.steampowered.com/app/957960/Inkulinati/) — Yaza Games / Daedalic, EA 31.01.2023, реліз 22.02.2024, Hand Actions, апокаліпсиси, режими.
- [TheGamer: best beasts](https://www.thegamer.com/inkulinati-best-beasts-units/) — уміння й числа Bishop Cat, Exploders, Donkey Bard, Devil, Skeleton; boredom.
- [Plitch: 8 tips](https://blogs.plitch.com/en/blog/8-important-inkulinati-tips-and-tricks) — boredom, брама, вогонь апокаліпсису від країв, втеча і пера.
- [TheGamer: Hildegard](https://www.thegamer.com/inkulinati-hildegard-boss-fight-strategy-guide/) — калюжі чорнила, Take a Nap, Inky Business.
- YouTube: пошук «Inkulinati gameplay».

## Непевне
- (?) «Бічна сторінка» з платформами/гравітацією (як у черзі) — у джерелах не підтверджено; поле описане як сітка з краями.
- (?) «Ініціатива-чорнило» з черги — не підтверджено; бачив лише «кожен звір — одна дія за хід гравця».
- (?) Поштовх «ковзає до першої вільної клітини» — з одного фан-гайду в пошуку, сторінку не відкривав.
- (?) Сон відновлює чорнило — лише з фрагмента пошуку.
- (?) Розмір поля, кількість раундів до апокаліпсису, шкода брами й вогнища — не бачив.
- (?) Давність джерел: частина з дострокового доступу 2023, у релізі могло змінитись.
- (?) Хмари благословення — ефект не описаний.
