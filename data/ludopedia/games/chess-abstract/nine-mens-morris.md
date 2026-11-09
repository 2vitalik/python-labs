---
title: Nine men's morris (Млин)
slug: nine-mens-morris
aka: [Mill, Mills, Merels, Merrills, Morris, Mühle, Cowboy checkers, Ninepenny marl, Млин, Мельниця]
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 8
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nine_men%27s_morris", best: true, note: "24 точки, 9 фішок, фази ставлення / руху / літання, млин знімає фішку, захист фішок у млині, перемога (2 фішки або нема ходів), розвʼязок Gasser — нічия, варіанти 3/6/12, Morabaraba, Lasker"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Nine%20Men's%20Morris", note: "Ludii: правила з літанням і захистом млинів, схожі ігри Five / Six / Twelve men's morris"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nine+men%27s+morris+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 75
mechanics: [hot-seat, turn-enforcement, ai-opponent, ai-random, ai-greedy, ai-minimax, cell-click, drag-drop-piece, hover-highlight, selection-highlight, legal-move-highlight, last-move-highlight, no-moves-left, remaining-counter, level-solver, rule-variants, game-screen, main-menu, end-screen, help-window, settings-window, replay, state-as-data, unit-tests, +place-stone, +phase-transition, +mill-removal, +mill-protection, +fly-when-few, +reform-mill, +min-pieces-lose, +hand-supply]
proposes: ["+trigger:mill_formed", "+cond:in_mill", "+cond:phase", "+effect:remove_enemy", "+effect:fly", "+ui:phase-indicator", "+ui:hand-pieces", "+ui:mill-highlight", "+ui:removal-mode", "+card:mill-removal", "+card:mill-protection", "+card:fly-when-few", "+card:reform-mill", "+card:min-pieces-lose"]
author: opus
date: 2026-11-09
---

# Млин (Nine men's morris) — розстав, потім переставляй дев'ять фішок так, щоб складати млини й знімати чужі

## Суть
Двоє по черзі **ставлять** по 9 фішок на 24 точки дошки з трьох вкладених квадратів, а коли всі поставлено — **пересувають** їх по лініях на сусідню точку. Три свої в ряд по лінії — **млин**: ти знімаєш одну фішку суперника (не з його млина, якщо є інші). Лишившись із трьома, гравець може **літати** — ставити фішку на будь-яку вільну точку. Програє той, у кого лишилось дві фішки або нема ходу. Головна ідея для курсу — одна гра з трьома фазами, у кожній свій генератор ходів.

## Поле і час
- Дошка: три вкладені квадрати, зʼєднані лініями посередині сторін; 24 точки (кути й середини сторін), фішки стоять на точках (`field: graph`, у кожної точки 2–4 сусіди).
- Ліній-млинів: 16 (по 2 на кожну сторону трьох квадратів = 12 + 4 поперечні) (?); діагоналей нема (є у Twelve men's morris).
- Покроково, двоє; хід = поставити / пересунути / перелетіти + можливе знімання після млина.
- Фази визначаються станом гравця, а не годинником: ставлення, доки є фішки в руці; рух; літання з трьома фішками.
- Повна інформація, без випадковості; гра розвʼязана — при ідеальній грі нічия (Gasser).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка (man) | piece | сторона; у руці / на дошці | фаза 1 — ставиться з руки; фаза 2 — крок по лінії на сусідню вільну точку; фаза 3 — на будь-яку вільну |
| Рука | supply | 9 фішок на старті | джерело фішок фази ставлення |
| Точка | static | 24, 2–4 сусіди по лініях | місце фішки; стрибків нема |
| Лінія-млин | zone | 3 точки на одній прямій лінії | три свої — млин |
| Млин | zone | 3 свої фішки на лінії | право зняти 1 ворожу; фішки млину захищені від знімання |
| Знята фішка | — | поза грою | не повертається |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `has(side, man)` (у руці є фішки) → ТО `custom: «фаза ставлення»`.
- Фаза 1: КОЛИ `input(place, man, point)` → ЯКЩО `free(point)` → ТО `place(man, point)`, `take(side, man)`.
- КОЛИ `custom: «в обох порожня рука»` → ТО `custom: «почати фазу руху»` — далі лише рух (у словнику це `phase_start(move)` як тригер наступних правил).
- Фаза 2: КОЛИ `input(move, man, to)` → ЯКЩО `free(to)` і `custom: «to — сусідня точка по лінії»` → ТО `move(man, to)`; стрибати не можна.
- Фаза 3: КОЛИ `input(move, man, to)` → ЯКЩО `count(own_men, =, 3)` і `free(to)` → ТО `custom: «перелетіти на будь-яку вільну точку»` (`+effect:fly`) — у деяких правилах літання вимкнене.
- КОЛИ `pattern(line(3))` (`+trigger:mill_formed`: новий хід склав млин зі своїх) → ТО `choose(enemy_man)` і `disappear(enemy_man)` (`+effect:remove_enemy`), потім `end_turn`.
- ЯКЩО `custom: «обрана фішка стоїть у ворожому млині»` (`+cond:in_mill`) і `custom: «у суперника є фішки поза млинами»` → ТО `block` — спершу знімаються фішки поза млинами.
- КОЛИ `custom: «фішку вивели з млину й наступним ходом повернули»` → ТО млин складено знову — знову `disappear(enemy_man)` («pounding», розмикання млину).
- КОЛИ `pattern(line(3))` → ЯКЩО `custom: «хід склав два млини одночасно»` → ТО `custom: «зняти 1 (або 2 — за домовленістю)»` (?).
- КОЛИ `count(enemy_men, <, 3)` (на дошці + в руці лишилось 2) → ТО `win`.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` (усі фішки заблоковані у фазі руху) → ТО `lose`.
- КОЛИ `custom: «жодна сторона не може виграти»` → ТО `draw` за згодою (формального лічильника у статті нема).
- Перемога: суперник з 2 фішками або без ходу · Поразка: те саме для тебе · Рахунок: партія 1 / ½ / 0.

## Керування і ввід
- Настільна: фішки з руки на точки, потім пересування рукою; зняту фішку прибирають з дошки.
- (цифрова версія) Фаза 1 — клік по вільній точці. Фаза 2 — клік по своїй фішці → підсвічуються сусідні вільні точки → клік по точці (або drag). Фаза 3 — підсвічуються **всі** вільні точки.
- Після млину гра переходить у режим знімання: курсор/підсвітка лише по знімних ворожих фішках, клік знімає.
- Індикатор фази постійно видно, бо той самий клік означає різне.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · Двоє · Онлайн · Правила.
- `variant-select` / `match-setup`: Nine / Three / Six / Twelve men's morris, Morabaraba, Lasker; літання увімк/вимк; рівень AI; хто перший.
- `game-screen`: дошка з 24 точками; `turn-indicator`; `phase-indicator` (ставлення / рух / літання для кожної сторони); `hand-pieces` (скільки фішок у руці); `remaining-counter` (на дошці); `mill-highlight` (щойно складений млин); `removal-mode` (підсвічені знімні фішки); `legal-move-highlight`; `last-move-highlight`; `undo-button` проти AI.
- `end-screen`: перемога (2 фішки / заблокований) або нічия; Реванш.
- `help-window`: три фази, захист млину, літання.
- `replay-window`: партія по ходах.
- Переходи: main-menu → match-setup → game-screen → end-screen → game-screen.

## Фічі поза полем
- `rule-variants` / `custom-rules`: кількість фішок (3/6/9/10/12), діагоналі, літання, рух у фазі ставлення (Lasker), правило подвійного млину.
- `ai-opponent-levels` (до ідеального за базою ендшпілів), `undo`, `replay`, `hint`, `online-multiplayer`.
- `stats` — перемоги / нічиї.

## Варіації й родичі
- **Three men's morris** — по 3 фішки (родич хрестиків-нуликів з рухом, див. `line-games.md`).
- **Six men's morris** — по 6, без зовнішнього квадрата, без літання.
- **Twelve men's morris / Morabaraba** (Південна Африка) — по 12, додані діагоналі.
- **Lasker morris** (ten men's morris) — по 10, у фазі ставлення вже можна ходити.
- Ludii: Five men's morris серед схожих ігор.
- Родичі: Pente (`pente.md`, лінія як джерело взяття), Fanorona (`fanorona.md`, граф-дошка з точками), хрестики-нулики з рухом.
- **Осі варіацій**: фішок (3/6/9/10/12) · дошка (без / з діагоналями, 2 / 3 квадрати) · фази (строго послідовні / рух під час ставлення) · літання (з 3 фішками / ніколи) · захист млину (так / ні) · подвійний млин (1 / 2 знімання).

## Цікавинки для курсу
- Граф дошки з 24 точками і списком 16 ліній замість сітки — 🌱.
- Три фази з окремими генераторами ходів, фаза — на гравця, а не на партію — 📎.
- Перевірка «новий млин» лише через щойно поставлену/переміщену фішку — 🌱.
- Знімання з захистом млинів і винятком «якщо всі в млинах» — 🌱.
- AI minimax з фазами й літанням — 🥇; повний розвʼязок ретроградним аналізом бази ендшпілів — 👑.

## Мапа на каталог
- Є: `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-random`, `ai-greedy`, `ai-minimax` · `cell-click`, `drag-drop-piece`, `hover-highlight`, `selection-highlight`, `legal-move-highlight`, `last-move-highlight` · `no-moves-left` ↔ заблокований програє · `remaining-counter` ↔ фішки на дошці й у руці · `level-solver` ↔ розвʼязок · `rule-variants` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `replay`, `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+place-stone` (див. `line-games.md`) — фаза 1.
  - `+phase-transition` (уже в корпусі) — ставлення → рух → літання.
  - `+hand-supply` «Фішки в руці до виставлення» · entities/legality · 🌱.
  - `+mill-removal` «Лінія з 3 дає право зняти чужу» · entities/combat · 🌱.
  - `+mill-protection` «Фігури в лінії захищені, доки є інші» · entities/legality · 🌱.
  - `+fly-when-few` «Мало фігур — ходиш куди завгодно» · entities/move · 🌱 · слоти {threshold: 3}.
  - `+reform-mill` «Розімкни й замкни млин знову» · entities/combat · 🌱.
  - `+min-pieces-lose` «Програш, коли фігур менше N» · game-logic/lose · 🌱 · слоти {n: 3}.

## Пропозиції до словників
- `+trigger:mill_formed` — хід склав нову лінію з N своїх (на відміну від `pattern(line)`, що спрацьовує на будь-яку наявну).
- `+cond:in_mill` — фішка входить до складеного млину.
- `+cond:phase` — поточна фаза гравця (ставлення / рух / літання).
- `+effect:remove_enemy` — гравець обирає й знімає ворожу фішку (не ходом на неї).
- `+effect:fly` — перемістити на будь-яку вільну клітину/точку.
- `+ui:phase-indicator` — фаза кожної сторони · `+ui:hand-pieces` — фішки в руці · `+ui:mill-highlight` — щойно складений млин · `+ui:removal-mode` — режим вибору фішки для знімання.
- `+card:mill-removal` · `+card:mill-protection` · `+card:fly-when-few` · `+card:reform-mill` · `+card:min-pieces-lose` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Nine men's morris](https://en.wikipedia.org/wiki/Nine_men%27s_morris) — 24 точки, 9 фішок, ставлення / рух / необовʼязкове літання (спірне: «rustic mode»), млин і знімання, захист фішок млину, «pounding», перемога (2 фішки або без ходу), розвʼязок (Ralph Gasser, «Solving Nine Men's Morris», 1996 — нічия), синоніми, історія (Овідій ≈ 8 р. н. е.; Kurna ≈ 1400 до н. е. — спірно), варіанти 3/6/12, Morabaraba, Lasker.
- [Ludii: Nine Men's Morris](https://ludii.games/details.php?keyword=Nine%20Men's%20Morris) — опис правил з літанням з 3 фішок, захистом млинів, перемогою при 2 фішках; схожі Five / Six / Twelve men's morris.
- YouTube: пошук «Nine men's morris rules».

## Непевне
- (?) Рік 8 — умовний: можлива згадка в «Ars Amatoria» Овідія; дошки на даху храму в Курні (≈ 1400 до н. е.) датування оскаржене.
- (?) Скільки фішок знімає подвійний млин (одним ходом склано два) — у відкритих джерелах не бачив; у багатьох правилах — одну.
- (?) Кількість ліній-млинів (16) — порахована з геометрії, не з джерела.
- (?) Кількість позицій у розвʼязку Gasser — стаття не наводить.
- (?) Чи фішку, що літає, можна поставити в точку, щоб одночасно заблокувати і скласти млин, — тривіально так, але окремо не розібрано.
- (?) Формальні правила нічиєї (повторення, ліміт ходів) у турнірних правилах — не перевірено.
