---
title: Waterworks
slug: waterworks
aka: [Waterworks Classic, Водогін]
family: connect-rotate
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: race
year: 1972
platforms: [cards]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Waterworks_(card_game)", best: true, note: "склад, хід із 4 дій, протічки, ремонт, мінімальна довжина за кількістю гравців, видання"}
  - {kind: other, url: "https://www.ultraboardgames.com/waterworks/game-rules.php", note: "правила Winning Moves: 110 карт, 8 ключів, T-труби й заглушки, мідь не тече, мінімуми 12/10/8"}
  - {kind: other, url: "https://www.geekyhobbies.com/waterworks-card-game-review-and-rules/", note: "огляд і правила старого видання: свинець/мідь, T-труби, мінімуми 15/12/10/8"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Waterworks+card+game+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 65
mechanics: [pipe-connectors, tile-rotate, connectivity-check, cursor-place, hot-seat, turn-enforcement, pocket, game-screen, end-screen, match-setup, help-window, +hand-of-tiles, +leak-sabotage, +repair-card, +min-length-goal, +immune-tile-type, +branch-cap, +discard-to-pass]
proposes: ["+effect:draw_card", "+effect:discard", "+effect:repair", "+cond:ports_match", "+cond:keeps_open_end", "+card:leak-sabotage", "+card:min-length-goal", "+card:branch-cap"]
author: opus
date: 2026-11-09
---

# Waterworks — гонка трубопроводів з карт від вентиля до крана: свої труби кладеш собі, протічні — суперникові, ключем лагодиш

## Суть
Кожен гравець викладає на столі свій трубопровід із карт-труб від карти-вентиля до карти-крана; виграє той, хто першим збудує неперервну лінію без протічок мінімальної довжини й поставить кран. Замість будувати собі можна зіграти **протічну трубу** на кінець чужого трубопроводу — доки протічку не залатано (ключем або цілою трубою тієї самої форми), власник не може будувати далі. Мідні труби не протікають, а залатана труба вдруге не тече. Гра Parker Brothers 1972 — «take that»-родич Saboteur, але кожен будує свою лінію.

## Поле і час
- Поле — стіл; карти лягають сіткою «картка до картки» (прямокутні клітини, усі карти **вертикально**, лише поворот на 180°), трубопроводи окремі в кожного, будуються справа наліво від вентиля.
- Межа поля — край столу; не можна будувати поверх чужого трубопроводу.
- Покроково, по колу; за хід — одна дія.
- Інформація прихована (рука з 5 карт), випадковість — добір з колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вентиль | source | 1 на гравця | початок трубопроводу, кладеться вертикально праворуч від гравця |
| Кран (носик) | sink | 1 на гравця | ставиться в кінець готової лінії вертикально, «ллє вниз і від вентиля»; ставлення = перемога |
| Ціла труба (свинець / залізо) | conduit | форма: пряма, коліно, T тощо | кладеться у свій трубопровід; може стати жертвою протічки |
| Мідна труба | conduit | форма | як ціла, але не може бути замінена протічною |
| Протічна труба | hazard | форма | грається на чужий кінець; блокує розширення, доки не залатана |
| T-труба | conduit | 3 виходи | розгалуження; до перемоги одну гілку треба закрити заглушкою |
| Карта заглушок | static | 4 заглушки на карті | закриває гілку; не рахується в довжину; може бути протічною |
| Гайковий ключ | pickup | 2 на гравця | кладеться на свою протічку — ремонт; після використання зникає з гри |
| Колода й скид | supply | 110 карт (Winning Moves) | добір; скид — лицем догори |
| Рука | supply | 5 карт закрито | поповнюється після дії |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «кожному вентиль, кран і 2 ключі»`, `custom: «роздати по 5 карт»`, `place(valve, table)`.
- КОЛИ `input(place, pipe, cell)` → ЯКЩО `turn_of(p)` and `free(cell)` and `custom: «карта вертикальна (0° або 180°)»` and `custom: «вхід труби збігається з вільним кінцем свого трубопроводу»` (+cond:ports_match) and `not state(own_pipeline, leaky)` → ТО `place(p, pipe)`.
- КОЛИ `input(place, pipe, cell)` → ЯКЩО `custom: «хід повністю закриває трубопровід — нема куди продовжити»` (+cond:keeps_open_end) or `custom: «за краєм столу або поверх чужого трубопроводу»` → ТО `block`.
- КОЛИ `input(place, good_pipe, opponent_pipeline)` → ТО `block` — цілі труби лише собі.
- КОЛИ `input(play, leaky, opponent_end)` → ЯКЩО `not state(target_pipeline, leaky)` and (`custom: «поверх останньої труби тієї самої форми, не мідної»` or `custom: «поруч з останньою трубою, продовжуючи лінію»`) → ТО `place(p, leaky)`, `set_state(target_pipeline, leaky)`.
- КОЛИ `input(play, leaky, pipe)` → ЯКЩО `state(pipe, repaired)` or `same(pipe, copper, material)` → ТО `block`.
- Ремонт: КОЛИ `input(place, good_pipe, own_leak)` → ЯКЩО `same(good_pipe, own_leak, shape)` → ТО `custom: «накрити протічку»` (+effect:repair), `set_state(pipe, repaired)`, `clear_state(own_pipeline, leaky)`.
- Ремонт: КОЛИ `input(use, wrench, own_leak)` → ЯКЩО `has(p, wrench)` → ТО `use(p, wrench)`, `set_state(pipe, repaired)`, `clear_state(own_pipeline, leaky)`, `end_turn` — цього ходу карту не кладуть (лише скид / без добору — залежно від видання).
- Виняток: КОЛИ `input(place, good_cap, leaky_T)` → ТО `place(p, cap)` — заглушити одну гілку протічної T можна й до ремонту.
- КОЛИ `input(discard, card)` → ТО `custom: «скинути карту лицем догори»` (+effect:discard) — пас-замінник.
- КОЛИ `turn_end(p)` → ТО `custom: «добрати до 5 карт»` (+effect:draw_card); у старому виданні — після дії, у Winning Moves — на початку ходу, хід закінчується з 5 картами в руці.
- КОЛИ `input(place, spout, end)` → ЯКЩО `counter(pipe_length, >=, min_by_players)` and `not state(own_pipeline, leaky)` and `custom: «усі гілки T заглушено»` and `custom: «кран вертикально, ллє вниз»` → ТО `win`.
- Довжина рахує лише неперервну лінію вентиль → кран; заглушки й гілки за T не рахуються.
- Мінімальна довжина: Wikipedia — 2 гравці 15, 3 — 12, 4 — 10, 5 — 8, 6 — 6; Winning Moves — 2 → 12, 3 → 10, 4 → 8.
- Перемога: першим поставити кран · Поразка: — · Рахунку нема.

## Керування і ввід
- Обрати карту з руки, за потреби повернути на 180°, прикласти до свого кінця або до кінця суперника (протічка), або покласти ключ на свою протічку, або скинути.
- Одна дія за хід; ключ — уся дія.

## Вікна, меню, HUD
- (цифрова версія) `match-setup`: кількість гравців, видання правил (мінімуми довжин).
- `game-screen`: смуги трубопроводів усіх гравців; `pocket` — своя рука з 5 карт; лічильник ключів; `progress-bar` — довжина лінії / мінімум; `conflict-highlight` — протічна труба; `legal-move-highlight` — куди лягає обрана карта; `turn-indicator`.
- `end-screen`: переможець, довжини трубопроводів.
- `help-window`: що можна класти на свій і чужий кінець.

## Фічі поза полем
- `rules-page`: два видання з різними мінімумами й порядком добору — `custom-rules`-перемикач у цифровій версії.
- Підставка-ванна для колоди, металеві ключі (старі видання) — фізичні аксесуари.

## Варіації й родичі
- Waterworks (Parker Brothers 1972, перевидання 1976) → Waterworks Classic (Winning Moves): мідь/залізо замість міді/свинцю, 8 ключів, мінімуми 12/10/8.
- Родичі в корпусі: [saboteur](saboteur.md) (спільний тунель + саботаж і ремонт), [pipe-mania](pipe-mania.md) (вода тече на час), [plumber-pipe-rotation](plumber-pipe-rotation.md), [linie-1](linie-1.md) (гонка мереж).
- Осі варіацій:
  - **мережа**: власна на кожного (Waterworks) / спільна (Saboteur);
  - **атака**: протічка на кінець / зламаний інструмент гравцеві (Saboteur) / обвал;
  - **ремонт**: ключ-одноразовий ресурс / ціла труба тієї ж форми;
  - **імунітет**: мідь не тече; залатане не тече вдруге.

## Цікавинки для курсу
- Прикладання карти з портами при орієнтації лише 0°/180° (не 90°) — 🌱.
- «Не закривай останній вихід»: перевірка, що в трубопроводі лишився вільний кінець — 📎.
- Протічка як стан цілого трубопроводу з обмеженням «не більше однієї» і заборонами (мідь, залатане) — 📎.
- Довжина лише головної лінії вентиль → кран з гілками T і заглушками — обхід графа без гілок-тупиків — 🥉.
- AI «будувати чи атакувати»: евристика за довжиною ліній суперників і ключами в них — 🥉.

## Мапа на каталог
- Є: `pipe-connectors` ↔ карти-труби з виходами; `tile-rotate` ↔ поворот на 180°; `connectivity-check` ↔ неперервна лінія вентиль → кран; `cursor-place` ↔ карта з руки на стіл; `hot-seat` + `turn-enforcement`; `pocket` ↔ рука; `game-screen` · `end-screen` · `match-setup` · `help-window`.
- **Нема** → пропозиції карток:
  - `+leak-sabotage` «Зіграти зіпсовану плитку на чужий кінець, що блокує будівництво» · game-logic/opponent · 📎.
  - `+repair-card` (Saboteur) — ремонт ключем або цілою трубою тієї ж форми.
  - `+min-length-goal` «Перемога — лінія не коротша за N (N за кількістю гравців)» · game-logic/win · 🌱.
  - `+immune-tile-type` «Тип плитки, що не піддається атаці (мідь)» · entities/state · 🌱.
  - `+branch-cap` «Розгалуження треба заглушити до перемоги; заглушки не рахуються» · game-logic/constraints · 📎.
  - `+hand-of-tiles` · `+discard-to-pass` (Saboteur).

## Пропозиції до словників
- `+effect:draw_card` — добрати карту з колоди.
- `+effect:discard` — скинути карту з руки.
- `+effect:repair` — накрити/зняти протічку, позначити трубу «залатана».
- `+cond:ports_match` — виходи нової труби збігаються з вільним кінцем.
- `+cond:keeps_open_end` — після ходу в трубопроводу лишається хоч один вільний кінець.
- `+card:leak-sabotage` · `+card:min-length-goal` · `+card:branch-cap`.

## Джерела
- ⭐ [Wikipedia: Waterworks (card game)](https://en.wikipedia.org/wiki/Waterworks_(card_game)) — склад (110 карт, ключі), 4 дії ходу, протічки й ремонт, таблиця мінімальних довжин 2–6 гравців, перевидання.
- [UltraBoardGames: Waterworks rules](https://www.ultraboardgames.com/waterworks/game-rules.php) — правила Winning Moves: добір на початку ходу, 8 ключів, мідь не тече, T-труби, заглушки, орієнтація крана, мінімуми 12/10/8.
- [Geeky Hobbies: Waterworks review and rules](https://www.geekyhobbies.com/waterworks-card-game-review-and-rules/) — старе видання (свинець), протічка лише на останню карту або поруч, гілки за T не рахуються, ключ — уся дія.

## Непевне
- (?) Склад колоди за формами труб і кількість протічних карт — не бачив.
- (?) Мінімальні довжини розходяться між виданнями (15/12/10/8/6 проти 12/10/8); кількість гравців 2–5 чи 2–6 — Wikipedia суперечить сама собі.
- (?) Порядок «дія → добір» (старе видання) чи «добір → дія» (Winning Moves) — описано обидва.
- (?) Чи може трубопровід перетинати сам себе — правила не кажуть.
