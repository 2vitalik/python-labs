---
title: Super Sokobot
slug: super-sokobot
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [web (HTML5, PuzzleScript)]
links:
  - {kind: itch, url: "https://erikwmj.itch.io/super-sokobot", best: true, note: "грати в браузері; «Push batteries onto charging ports to apply their effects and power up»; стрілки, Z, R; розширення Sokobot"}
  - {kind: play, url: "https://html-classic.itch.zone/html/15893619/index.html", note: "експорт PuzzleScript з повним сирцем (sourceCode): батарейки, порти, двері, вартові, лава, 55 мап"}
  - {kind: other, url: "https://erikblog.neocities.org/posts/Super-Sokobot-Solutions", note: "розвʼязки автора GIF-ками для кімнат 1–45; 46–52 навмисно без розвʼязків"}
  - {kind: itch, url: "https://erikwmj.itch.io/sokobot", note: "попередник Sokobot (2019, JavaScript): 10 пазлів 8×8, «higher power makes it harder to control»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Super+Sokobot+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, push-object, pull-object, key-and-door, button-toggle, destructible-blocks, line-of-sight-attack, status-effects, environment-death, player-death, reach-exit, undo-unlimited, restart-level, sequential-levels, level-from-txt, tutorial-window, status-panel, mode-indicator, sound-effects, +push-chain, +strength-gate, +door-crush, +power-steps, +port-powerups, +spin-steps, +cloak-invisible, +shield-by-box]
proposes: ["+effect:repeat_move", "+cond:power", "+ui:power-slots", "+card:power-steps", "+card:port-powerups", "+card:spin-steps", "+card:cloak-invisible", "+card:shield-by-box", "+axis:control"]
author: opus
date: 2026-11-19
---

# Super Sokobot — робот-сокобан тікає з лабораторії: батарейки на зарядних портах задають, на скільки клітин він ходить і що вміє

## Суть
Сокобот має дійти до сходів у кожній кімнаті лабораторії, штовхаючи ящики й батарейки. Головна механіка — **зарядні порти**: батарейка на порті вмикає свій ефект. Сума зарядів — це «потужність», і робот за одне натискання проходить стільки клітин, скільки її є (1–4): сильний — неповороткий; без жодного заряду він вимикається.

Спеціальні батарейки відчиняють і зачиняють двері, вмикають магніт, невидимість для вартових-ботів, холод проти лави, отруту і «оберт» траєкторії. Сюжетні репліки науковця ведуть до втечі назовні; 52 кімнати, PuzzleScript, автор Erik (ErikWMJ).

## Поле і час
- Кожна кімната — мапа PuzzleScript ~12×12 (у другій половині — до 28×18); верхній і нижній ряд мапи — HUD.
- Хід = натискання; за потужності N робот робить 1 крок від вводу і ще N − 1 автоматичних (`again`, ~0,15 с між ними). Кожен крок — повноцінний (поштовх, лава), але довжина серії фіксується на першому кроці.
- Вартові стріляють, двері грюкають, холод і заряд перераховуються лише в кінці всієї серії, а не посеред неї.
- Шари: підлога → лава, порти, сходи → уламки → робот, ящики, батарейки, стіни, двері, HUD.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сокобот | player | потужність 0–4, холод 0–3, стани невидимий / магніт / оберт | рух 4 боки серією з N кроків; штовхає все рухоме |
| Зарядний порт | switch | — | батарейка на ньому вмикає свій ефект; від порту до HUD тягнеться кабель |
| Мала батарейка (світло-зелена) | object | +1 заряду | штовхається; на порті додає потужність |
| Велика батарейка (темно-зелена) | object | +2 заряду | як мала, але подвійна |
| Ключ-батарейки рожева / синя | object | колір | на порті відчиняють двері свого кольору |
| Батарейка «навпаки» (коричнева) | object | — | на порті зачиняє коричневі двері, знята — відчиняє |
| Магнітна (червона) | object | — | на порті: ящик позаду робота їде за ним |
| Плащ (сіра) | object | — | на порті: робот невидимий для вартових |
| Крижана (біла) | object | +1 холоду | на порті: холод — захист від лави; три — робот замерзає |
| Отруйна (темно-червона) | object | −1 | гасить один заряд однієї батарейки |
| Обертова (фіолетова) | object | — | на порті: кожен автокрок серії повертає на 90° за годинниковою |
| Ящик | object | — | штовхається, ряд — увесь |
| Важкий ящик (темно-зелений) | object | потрібна потужність ≥ 2 | інакше хід скасовано |
| Вартовий-бот | enemy | 4 напрямки | стріляє по рядку й стовпцю; штовхається, гине в лаві |
| Науковець | neutral | — | сюжетні репліки на тригерах; штовхається |
| Двері рожеві / сині / коричневі | gate | відчинені / зачинені | зачиняючись, нищать ящик у проході й чавлять робота |
| Стіна, кабелі | static | — | непрохідні; закривають лінію вогню |
| Лава | hazard | анімована | робот гине без холоду; ящик тоне |
| Сходи | static | — | вихід з кімнати |
| Тріснута стіна | static | — | розвалюється, коли в неї входить робот (фінальні кімнати) |
| Уламки | terrain | — | лишаються від знищеного ящика, прохідні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(sokobot, dir)`.
- КОЛИ `contact(sokobot, box)` → ЯКЩО `free(cell_behind_row)` → ТО `push` — ящики, батарейки, вартові, науковець; ряд їде весь; інакше `block`.
- КОЛИ `contact(sokobot, heavy_crate)` → ЯКЩО `counter(power, <, 2)` → ТО `block` — хід скасовано повністю.
- КОЛИ `enter(battery, port)` → ТО `counter(power, +1|+2)` (мала / велика); КОЛИ `leave(battery, port)` → ТО `counter(power, −1|−2)`.
- КОЛИ `enter(poison_battery, port)` → ТО `counter(power, −1)` — отрута гасить один заряд однієї батарейки з портів.
- КОЛИ `input(dir)` → ЯКЩО `counter(power, >=, 2)` → ТО `move(sokobot, dir)` і ще `custom: «power − 1 автоматичних кроків у тому ж напрямку»`.
- КОЛИ `turn_end` → ЯКЩО `counter(power, ==, 0)` → ТО `set_state(sokobot, powered_off)`, `lose`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(port, magnet_battery)` and `occupied(cell_behind_sokobot, box)` → ТО `pull` — на кожному кроці серії.
- КОЛИ `enter(key_battery, port)` → ТО `set_state(doors_of_colour, open)`; КОЛИ `leave(key_battery, port)` → ТО `set_state(doors_of_colour, closed)`, ящик у проході → `transform(box, rubble)`, робот у проході → `lose`.
- КОЛИ `enter(reverse_battery, port)` → ТО `set_state(brown_doors, closed)` (з тим самим розчавлюванням); КОЛИ `leave(reverse_battery, port)` → ТО `set_state(brown_doors, open)`.
- КОЛИ `enter(cloak_battery, port)` → ТО `set_state(sokobot, invisible)`; КОЛИ `leave(cloak_battery, port)` → ТО `clear_state(sokobot, invisible)`.
- КОЛИ `line_of_sight(guard, sokobot)` → ЯКЩО `not state(sokobot, invisible)` → ТО `lose` — постріл; стіни, кабелі й зачинені двері лінію закривають.
- КОЛИ `line_of_sight(guard, sokobot)` → ЯКЩО `custom: «між ними ящик або батарейка»` → ТО `transform(box, rubble)`, `set_state(guard, reloading, 1)` — цього ходу робот живий.
- КОЛИ `enter(ice_battery, port)` → ТО `set_state(sokobot, cold)` — рівень = кількість крижаних батарейок на портах; КОЛИ `counter(cold, ==, 3)` → ТО `lose` (замерз).
- КОЛИ `enter(sokobot, lava)` → ЯКЩО `not state(sokobot, cold)` → ТО `lose`; холод 1 рятує лише посеред серії кроків (пролетіти, не стати), холод 2 — завжди.
- КОЛИ `enter(box, lava)` → ТО `disappear(box)` — уперше науковець обурюється: «Those batteries are exceedingly expensive!».
- КОЛИ `input(dir)` → ЯКЩО `occupied(port, spin_battery)` and `counter(power, >=, 2)` → ТО кожен автокрок `face(sokobot, cw)`, `move(sokobot, dir)` — серія вгору → праворуч → вниз → ліворуч.
- КОЛИ `contact(sokobot, cracked_wall)` → ТО `transform(cracked_wall, broken_wall)`, `move(sokobot, dir)`.
- КОЛИ `enter(sokobot, story_trigger)` → ТО `message(…)` — репліки науковця; деякі тригери рушають і його самого.
- КОЛИ `enter(sokobot, stairs)` → ЯКЩО `custom: «серія кроків завершилась і робот цілий»` → ТО `win`, `next_level`.
- КОЛИ `input(z)` → ТО `undo`; КОЛИ `input(r)` → ТО `restart`.
- Перемога: робот на сходах після завершеної серії, не вимкнений, не зламаний, не замерзлий. · Поразка: нуль заряду, лава, постріл, двері, три холоди — робот лишається на полі мертвим, далі undo. · Рахунку нема.

## Керування і ввід
- Стрілки — напрям серії кроків; довжину серії гравець не вибирає, її задає потужність.
- Z — undo без ліміту, R — рестарт кімнати.
- Програмування ходів нема, але серія кроків з магнітом чи обертом — це по суті «макрос», налаштований батарейками.

## Вікна, меню, HUD
- `splash-screen` — титул PuzzleScript «Super Sokobot by Erik».
- `tutorial-window` — текстові екрани: «Sokobot is a highly advanced puzzle-solving robot…», «Guide Sokobot to the stairs… Press Z to undo a move or R to restart a room», сюжет про корпорацію й утечу; фінал «SO THIS IS THE SKY… IT'S BEAUTIFUL… BEEP BOOP.» і «~Fin».
- `game-screen`: кімната; верхній ряд — напис POWER і 4 комірки заряду (`energy-bar`); нижній — смуга стану (норма / рух зі стрілкою напрямку й лічильником кроків, що лишились / вимкнений / зламаний / замерзлий; значки магніту й оберту) і `level-number` «n/52».
- Сюжетні `message`-вікна посеред кімнати — репліки науковця.
- Переходи: титул → текст → кімната → сходи → наступна; кімнати 48–52 — назовні (трава, дерева, чайки), далі фінальна сцена.

## Фічі поза полем
- `undo` без ліміту, `restart-level`, `levels-sequential` (52 кімнати), `continue` — стандарт PuzzleScript.
- Розвʼязки автора — окрема сторінка з GIF (кімнати 1–45; останні навмисно без підказок).
- Попередник Sokobot (2019) — JavaScript-прототип з курсу: 10 пазлів 8×8; автор планував лаву й «термостійку батарейку» — обидві зʼявились тут.

## Варіації й родичі
- [sokoban](sokoban.md) — основа; [chips-challenge](../maze-arcade/chips-challenge.md) — кольорові двері, вогонь/лава й «дозволи» на клітини; [adventures-of-lolo](adventures-of-lolo.md) — ворог, що бʼє по лінії, і ящик як щит.
- [sokobot](../program-robots/sokobot.md) — інша гра з подібною назвою (2022, роботи за програмою), не родич.
- Осі варіацій:
  - **звідки здібності**: предмети в інвентарі (Chip's Challenge) / предмети, поставлені на порти на полі (тут) — здібність можна вимкнути, зіштовхнувши батарейку;
  - **довжина ходу**: 1 клітина / до упору (ice) / рівно N = заряд (тут);
  - **траєкторія серії**: пряма / з поворотом на 90° щокроку (оберт).

## Цікавинки для курсу
- Потужність як сума батарейок на портах і хід на N клітин з поштовхом на кожному кроці — 📎.
- Порт як «слот здібності»: тип батарейки → ефект (двері, магніт, плащ, холод, отрута, оберт) — 🥉 за систему, кожен ефект 🌱–📎.
- Двері за ключ-батарейкою з розчавлюванням того, хто в проході, і «зворотні» двері — 📎.
- Вартовий: постріл по лінії лише в кінці серії, ящик на лінії гине замість робота, вартового можна відштовхнути в лаву — 🥉.
- Холод зі стеком: 1 — пролетіти лаву посеред серії, 2 — стояти, 3 — замерз — 📎.
- Обертова серія (вгору → праворуч → вниз → ліворуч) — 🌱.
- Розвʼязувач: стан = позиції всіх рухомих + що стоїть на портах; потужність і ефекти — похідні від стану — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ ящики й батарейки; `pull-object` ↔ магніт; `key-and-door` + `button-toggle` ↔ ключ-батарейка на порті → двері кольору; `destructible-blocks` ↔ ящики в уламки від пострілу й дверей; `line-of-sight-attack` ↔ вартові; `status-effects` ↔ холод зі стеком; `environment-death` + `player-death` ↔ лава, нуль заряду; `reach-exit` ↔ сходи; `undo-unlimited` + `restart-level` ↔ Z і R; `sequential-levels` + `level-from-txt` ↔ 52 кімнати в сирці; `tutorial-window` ↔ текстові екрани; `status-panel` + `mode-indicator` ↔ POWER і смуга стану; `sound-effects` ↔ сходи, лава, постріл, вимкнення.
- **Нема** → пропозиції карток:
  - `+push-chain` (є в корпусі) — ряд ящиків штовхається весь.
  - `+strength-gate` (є в корпусі) — важкий ящик лише за потужності ≥ 2.
  - `+door-crush` (є в корпусі) — двері, зачиняючись, нищать ящик і чавлять робота.
  - `+power-steps` «Довжина ходу = сума зарядів» · entities/move · 📎 · слот {max: 4}.
  - `+port-powerups` «Предмет на порті вмикає ефект аватара» · entities/state · 🥉 · слот {effects: power, key, magnet, cloak, cold, poison, spin}.
  - `+spin-steps` «Серія кроків повертає на 90° щокроку» · entities/move · 🌱.
  - `+cloak-invisible` «Невидимість для ворогів, поки джерело активне» · entities/state · 🌱.
  - `+shield-by-box` «Обʼєкт на лінії вогню гине замість гравця» · entities/combat · 🌱.

## Пропозиції до словників
- `+effect:repeat_move` — автоматичний повтор кроку N разів (серія за потужністю); `move` описує один крок.
- `+cond:power` — сумарний заряд від предметів на портах; зараз це `counter(power, …)`, але заряд похідний від поля, а не лічильник.
- `+ui:power-slots` — ряд комірок заряду, що світяться за кількістю (POWER ▮▮▯▯).
- `+card:power-steps`, `+card:port-powerups`, `+card:spin-steps`, `+card:cloak-invisible`, `+card:shield-by-box` — див. «Мапу на каталог».
- `+axis:control` — `direct`, але довжину ходу задає стан поля (заряд), а не гравець.

## Джерела
- ⭐ [itch.io: Super Sokobot](https://erikwmj.itch.io/super-sokobot) — гра в браузері, опис, керування, подяки тестувальникам, коментарі (найраніший — 21.12.2025).
- [HTML-експорт із сирцем](https://html-classic.itch.zone/html/15893619/index.html) — `sourceCode` PuzzleScript: обʼєкти (`Charge`, `Battery1/2`, `BatteryKey*`, `BatteryMagnet`, `BatteryCloak`, `BatteryIce`, `BatteryPoison`, `BatterySpin`, `Crate2`, `Guard`, `Lava`, двері), правила токенів заряду, серії `again`, вартових, холоду, дверей; 55 мап і всі повідомлення.
- [Розвʼязки автора](https://erikblog.neocities.org/posts/Super-Sokobot-Solutions) — GIF для кімнат 1–45; лічильник кімнати в правому нижньому куті HUD.
- [itch.io: Sokobot](https://erikwmj.itch.io/sokobot) — попередник (2019, JS): 10 пазлів 8×8, плани на лаву й термостійку батарейку, коментар про PuzzleScript-переробку.
- YouTube: пошук «Super Sokobot puzzlescript».

## Непевне
- (?) Рік: на сторінці дата публікації не показана; найраніший коментар — 21.12.2025, тому 2025.
- (?) Вартові бʼють у 4 боки — з того, що правило записане для напрямків `UP RIGHT` і `DOWN LEFT`; у грі не перевірено.
- (?) Потужність понад 4 (більше батарейок, ніж комірок) — у звичайних кімнатах не трапляється; що буде — не перевіряв.
- (?) Що саме написано в нижній смузі стану (слова чи значки) — бачу лише назви спрайтів (`HUDNormal`, `HUDMoving`, `HUDDead`, `HUDBroke`, `HUDFrozen`).
