---
title: BurgerTime
slug: burgertime
aka: [Hamburger (JP), Burger Time]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1982
platforms: [arcade (Data East DECO Cassette), Intellivision, Atari 2600, Apple II, IBM PC, ColecoVision, NES, MSX, Game Boy (Deluxe)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BurgerTime", best: true, note: "інгредієнти падають поверхом нижче, вороги на інгредієнті — +2 поверхи кожен, перець, бонуси, 6 дошок, порти й клони"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/バーガータイム", note: "ланцюгове падіння, вага ворогів-пасажирів, скасування смерті, якщо падіння завершило дошку; прискорення ворогів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BurgerTime+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 60
mechanics: [move-4dir, ladder-climb, gravity-fall, multi-cell-size, chase-player, touch-death, player-death, respawn, projectile-shot, item-pickup, event-points, chain-reaction, all-on-targets, sequential-levels, extra-life-threshold, score-records, status-panel, game-screen, end-screen, +walk-over-to-drop, +rider-extra-fall, +crush-by-fall, +stun-cloud, +ammo-refill-pickup, +bonus-after-n-drops, +death-cancel-by-clear]
proposes: ["+trigger:walked_over(a, obj)", "+trigger:landed", "+effect:fall_floors(a, n)", "+cond:riders(obj, op, n)", "+ui:ammo-counter", "+card:walk-over-to-drop", "+card:rider-extra-fall", "+card:crush-by-fall", "+card:stun-cloud"]
author: opus
date: 2026-11-09
---

# BurgerTime — кухар проходить по велетенських інгредієнтах, вони падають поверхом нижче і давлять ворогів, доки бургери не складуться на тарілках

## Суть
Peter Pepper бігає лабіринтом поверхів і драбин. Щоб інгредієнт (булка, котлета, салат, сир, помідор) упав на поверх нижче, треба **пройти його по всій довжині**. Падаючий інгредієнт збиває той, що лежить під ним, і давить ворогів унизу; ворог, що стояв на інгредієнті, додає йому падіння. Дошка пройдена, коли всі бургери зібрано на тарілках. Захист — кілька порцій перцю, що оглушує ворогів.

## Поле і час
- Один нескролений екран збоку: горизонтальні поверхи-платформи + драбини; внизу ряд тарілок.
- Інгредієнт — широкий обʼєкт на кілька клітин поверху; лежить на поверсі, над своєю тарілкою (стовпчик бургера вертикальний).
- Real-time; вороги з часом прискорюються.
- 6 дошок зі зростанням складності (більше бургерів і ворогів, тісніші лабіринти), потім цикл повторюється.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Peter Pepper | player | життя, перець | ходить поверхами, лазить драбинами; не стрибає |
| Поверх | terrain | — | по ньому ходять усі; інгредієнти лежать на ньому |
| Драбина | terrain | — | вертикальний рух між поверхами |
| Інгредієнт | object | кілька секцій; натиснуті/ні | після проходу всіх секцій падає на поверх нижче; несе на собі ворогів |
| Тарілка | sink | — | кінцева точка стовпчика; інгредієнти на ній складаються в бургер |
| Mr. Hot Dog | enemy | — | переслідує кухаря поверхами й драбинами |
| Mr. Pickle | enemy | — | так само |
| Mr. Egg | enemy | — | так само |
| Хмара перцю | projectile | коротко живе | перед кухарем у напрямку погляду; оглушує ворогів |
| Морозиво / кава / картопля | pickup | — | зʼявляються після певної кількості скинутих інгредієнтів; очки + 1 перець |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; вгору/вниз — лише ЯКЩО `cell(here, ladder)`.
- КОЛИ `enter(player, ingredient_section)` → ТО `set_state(section, pressed)`.
- КОЛИ `counter(pressed_sections, ==, all)` → ЯКЩО `custom: «на інгредієнті нема ворогів»` → ТО `fall(ingredient)` до наступного поверху під ним.
- КОЛИ `counter(pressed_sections, ==, all)` → ЯКЩО `custom: «на інгредієнті стоять N ворогів»` → ТО `custom: «падає на 1 + 2×N поверхів, де N — вороги на ньому»`, вороги падають разом, `score(n)` більший, ніж за роздавлення.
- КОЛИ `contact(falling_ingredient, ingredient)` → ТО `fall(ingredient)` — нижній інгредієнт збито на поверх нижче (ланцюг).
- КОЛИ `contact(falling_ingredient, enemy)` → ТО `disappear_b`, `score(n)`; згодом `respawn(enemy, edge)`.
- КОЛИ `custom: «ворог-пасажир приземлився»` → ТО `respawn(enemy, here)`; ворог вилазить назад у лабіринт.
- КОЛИ `contact(falling_ingredient, plate_stack)` → ТО `custom: «інгредієнт лягає на тарілку/стос і більше не рухається»`.
- КОЛИ `input(pepper)` → ЯКЩО `has(player, pepper)` → ТО `spawn_at(pepper_cloud, front)`, `take(player, pepper)`.
- КОЛИ `contact(pepper_cloud, enemy)` → ТО `stun(enemy, n)`.
- КОЛИ `contact(player, enemy)` → ЯКЩО `state(enemy, stunned)` → ТО прохід крізь ворога; інакше `lives(-1)`.
- КОЛИ `counter(dropped, ==, n)` → ТО `spawn_at(bonus_item, fixed)`; КОЛИ `contact(player, bonus_item)` → ТО `pickup`, `score(n)`, `give(player, pepper)`.
- КОЛИ `all_on(ingredient, plate)` → ТО `win` дошки, `next_level`.
- КОЛИ `died(player)` → ЯКЩО `custom: «інгредієнти, що ще падають, завершили дошку»` → ТО `custom: «смерть скасовано»` (JA Wikipedia).
- КОЛИ `timer(every)` → ТО `speed(enemy, +n)`.
- Перемога: нема (цикл 6 дошок). Поразка: 0 життів. Рахунок: роздавлені вороги, скинуті з пасажирами, бонус-предмети, скинуті інгредієнти (?).

## Керування і ввід
- 4-позиційний джойстик: ліво/право — хід поверхом, вгору/вниз — драбина.
- Одна кнопка — перець (у напрямку погляду). Запас на старті — 5.
- Тактика: заманити ворогів на інгредієнт і дотиснути останню секцію — «їзда» дає більше очок і пришвидшує дошку.

## Вікна, меню, HUD
- `game-screen`: поверхи, драбини, тарілки + HUD: `score`, `hi-score`, `lives`, лічильник перцю (`+ui:ammo-counter`), номер дошки (`level-number`) (?).
- `end-screen` — game over.
- Переходи: монета → гра → (усі бургери) наступна дошка → (0 життів) game over.

## Фічі поза полем
- `levels-sequential`: 6 дошок по колу з наростанням складності.
- Пороги додаткових життів — різні в різних портах.
- BurgerTime Deluxe (Game Boy): 24 дошки, паролі (`level-password`), versus.

## Варіації й родичі
- Сиквели: Peter Pepper's Ice Cream Factory (1984), Diner (Intellivision: кухар штовхає кулі-їжу по пандусах на тарілку), Super BurgerTime (1990, 2 гравці одночасно, боси), BurgerTime Deluxe (1991), BurgerTime Delight (2007, сільничка оглушує всіх), BurgerTime World Tour (2011, 3D), BurgerTime Party! (2019).
- Клони: Mr. Wimpy, Bear Bovver, BurgerSpace (open source, 2007), Burger Chase, Barmy Burgers та ін.
- Родичі в корпусі: [space-panic](space-panic.md) (вбивство ворога падінням крізь поверхи), [lode-runner](lode-runner.md) (поверхи+драбини, вороги-переслідувачі), [wrecking-crew](wrecking-crew.md).
- Осі: **що скидає обʼєкт** (пройти всі секції / штовхнути / копнути); **вплив пасажирів** (нема / +N поверхів за кожного); **як убити ворога** (роздавити зверху / скинути разом / оглушити й обійти).

## Цікавинки для курсу
- «Пройди обʼєкт по всій довжині — він падає»: стан на кожній секції широкого обʼєкта — 📎.
- Пасажири додають висоту падіння (+2 поверхи за ворога) — 🥉, бо треба рахувати, хто стоїть на обʼєкті, і вести всіх разом.
- Ланцюгове збивання: падаючий інгредієнт збиває нижній, той — наступний, до тарілки — 🥉 (каскад).
- Стос на тарілці: інгредієнт стає опорою для наступного — 🌱.
- Перець як обмежені «набої» з поповненням бонусом — 🌱.
- Скасування смерті, якщо фізика, що вже йде, завершила рівень — 📎 (порядок обробки подій).

## Мапа на каталог
- Є: `move-4dir` · `ladder-climb` · `gravity-fall` (падіння інгредієнтів) · `multi-cell-size` (широкий інгредієнт) · `chase-player` · `touch-death` · `player-death` · `respawn` (вороги) · `projectile-shot` (хмара перцю) · `item-pickup` · `event-points` · `chain-reaction` (збивання інгредієнтів) · `all-on-targets` (усі на тарілках) · `sequential-levels` · `extra-life-threshold` · `score-records` · `status-panel` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+walk-over-to-drop` «Пройти обʼєкт по всіх секціях — він падає» · entities/interact · 📎.
  - `+rider-extra-fall` «Сутності на обʼєкті збільшують висоту його падіння» · entities/move · 🥉 · слот {floors per rider}.
  - `+crush-by-fall` «Падаючий обʼєкт убиває сутність під собою» · entities/combat · 🌱 (пара до `crush-by-slide`).
  - `+stun-cloud` «Оглушити ворога хмарою; оглушеного можна пройти» · entities/combat · 🌱.
  - `+ammo-refill-pickup`, `+bonus-after-n-drops`, `+death-cancel-by-clear` — див. правила.

## Пропозиції до словників
- `+trigger:walked_over(a, obj)` — A пройшов усі секції обʼєкта (BurgerTime).
- `+trigger:landed` — сутність приземлилась після падіння (BurgerTime, Space Panic, Fire 'n Ice).
- `+effect:fall_floors(a, n)` — упасти рівно на N поверхів, а не до дна.
- `+cond:riders(obj, op, n)` — скільки сутностей стоїть на обʼєкті.
- `+ui:ammo-counter` — лічильник набоїв/зарядів (перець).
- `+card:walk-over-to-drop`, `+card:rider-extra-fall`, `+card:crush-by-fall`, `+card:stun-cloud` — див. вище.

## Джерела
- ⭐ [Wikipedia: BurgerTime](https://en.wikipedia.org/wiki/BurgerTime) — правила падіння, пасажири (+2 поверхи за ворога), перець 5 шт., бонус-предмети, 6 дошок, порти, сиквели, клони.
- [Wikipedia JA: バーガータイム](https://ja.wikipedia.org/wiki/バーガータイム) — ланцюгове падіння, скасування смерті, прискорення ворогів, Deluxe: 24 дошки, паролі.
- YouTube: пошук «BurgerTime arcade gameplay».

## Непевне
- (?) Очки: за роздавленого ворога, за пасажирів (подвоєння за кожного?), за скинутий інгредієнт, за бонус-предмети — у відкритих джерелах значень нема.
- (?) Скільки секцій має інгредієнт і чи падає він, якщо пройти секції в довільному порядку чи з перервами.
- (?) Через скільки скинутих інгредієнтів зʼявляється бонус-предмет і скільки він лежить.
- (?) Скільки ворогів кожного типу на дошці; чи відрізняються вони поведінкою (у джерелах — ні).
- (?) Чи можна скинути інгредієнт, коли кухар сам стоїть на ньому разом з ворогами; що буває з кухарем.
- (?) Аркадний 2-гравцевий режим по черзі; HUD — з памʼяті.
