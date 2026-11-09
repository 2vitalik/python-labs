---
title: Mendel Palace (Quinty)
slug: mendel-palace
aka: [Quinty, クインティ, Kuinti]
family: push-slide
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: state
year: 1989
platforms: [Famicom / NES, Nintendo Switch (Nintendo Classics)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mendel_Palace", best: true, note: "кімната 5×7 плиток, перевернути плитку під собою чи поруч — ляльку відкидає, у стіну — знищено; «stalemate»; темні кімнати; кооп 2P"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/クインティ", note: "2–7 шарів плиток, 10 етапів × 10 раундів, усі вороги за етапами, 15 типів плиток з очками, прихований таймер, 2P по черзі й одночасно, Extra Quinty"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mendel+Palace+NES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, impassable-cells, destroy-all-enemies, touch-death, player-death, chase-greedy, random-walk, temporary-modes, item-pickup, extra-life-threshold, event-points, timeout-punisher, level-select, level-unlock, spawn-points, +knockback, +tile-flip-knockback, +layered-tile-stack, +stalemate-win, +flip-area-tile, +bonus-roulette, +launch-tile, +bonus-stage, +dark-zone, +mimic-copy, +split-on-death, +lock-cell, +paint-cell, +mode-coop]
proposes: ["+effect:flip", "+effect:knockback", "+cond:layers_left", "+trigger:knocked_into_wall", "+feature:hidden-hurry-timer", "+card:tile-flip-knockback", "+card:layered-tile-stack", "+card:flip-area-tile", "+card:launch-tile"]
author: opus
date: 2026-11-09
---

# Mendel Palace (Quinty) — перевертай плитки підлоги 5×7: лялька відлітає в стіну, а під плиткою — нова плитка

## Суть
Одна кімната — сітка 5×7 плиток підлоги в рамці стін. Гравець не бʼє ворогів: він **перевертає плитку** під собою чи перед собою, і лялька-ворог, що стоїть на ній, відлітає; удар об стіну чи непрохідний блок її знищує. Кожна плитка — **стос шарів**: перевертання знімає верхній і відкриває наступний візерунок (зірка, сонце, хрест, рулетка, метал, замок…), тож поле змінюється з кожною дією. Раунд пройдено, коли знищено всіх ляльок або коли не лишилось жодної плитки, яку можна перевернути. Перша гра Game Freak (режисер — Satoshi Tajiri).

## Поле і час
- Поле: 5 рядків × 7 стовпців плиток, обнесене стіною; кожна клітина має **2–7 шарів** залежно від раунду (JA-вікі) — що під верхнім, гравець не знає (`info: partial`).
- Шари клітини: стос плиток (верхня діє) + істоти (гравці, ляльки, боси) поверх.
- Real-time: ляльки рухаються безперервно; прихований таймер раунду — коли спливає, вороги прискорюються, музика пришвидшується, гравець сповільнюється (життя не знімається).
- Темні кімнати (плитка Moon або раунд): поле не видно, плитки й ворогів треба передбачати.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (синій / зелений хлопчик у 2P) | player | життя, зірки | рух 4 напрямки; перевертає плитку під собою або сусідню |
| Плитка-стос | tile | шари 2–7, верхній візерунок | перевертання знімає верхній шар і відкидає того, хто стояв |
| Стіна-рамка | static | — | лялька, що влетіла, знищена |
| Лялька Walkman | enemy | — | лише ходить |
| Зелена лялька | enemy | — | тікає, якщо до неї не підійти (?) |
| Помаранчева / рожева | enemy | — | переслідує / наполегливо переслідує |
| Синя → Kid ×2 | enemy | — | якщо не вибито з першого разу — ділиться на двох Kid |
| Kid | enemy | малий | від удару відлітає далеко |
| Jumpers (Pyramid) | enemy | 4 кольори | стрибають (?) |
| Artist | enemy | — | замальовує плитки (Illustration — заблоковані); синій породжує Illustman |
| Illustman | enemy | — | переслідує гравця |
| Ballerina (рожева) | enemy | — | ламає металеві плитки |
| Swimmer | enemy | — | «плаває» (Club) |
| Mimi | enemy | — | дзеркалить рухи гравця |
| Перевертач (EN-вікі) | enemy | — | сам перевертає випадкові плитки, як гравець |
| Бос (Secom, Tri, Plum, Quinty…) | boss | раунд 10 етапу | кидає плитки; Secom у Club атакує двома клонами |
| Star | pickup | 100 очок | 100 зірок → +1 життя і прискорення; остання зірка раунду блимає (бонус) |
| Roulette | tile | цикл іконок | ефект — іконка в мить проходу: STARS, 1UP, 10000, 1000, 10 |
| Time | tile | — | +5 с, 2000 очок |
| Sun | tile | — | перевертає всі інші плитки (часто чистить ворогів), 5000; знімає темряву й Illustration |
| Cross | tile | — | перевертає 4 сусідні, 1000 |
| Clock | tile | напрям обертається | перевертає в один напрям, що крутиться, 1500 |
| Moon | tile | — | темрява; видимі звичайні плитки → зірки, 3000 |
| Attack (Spinner у EN) | tile | — | запускає гравця до стіни в напрямку погляду; удари й предмети на льоту ×2 очки; 100 за відскок |
| Special Bonus | tile | — | як Attack, але виліт за екран — бонус-етап із зірками |
| Enemy | spawner | — | коли ворогів мало — випускає одного |
| Metal | static | — | як стіна (ляльок об неї знищено); ламається деякими ворогами й атаками → Rubble |
| Rubble | terrain | — | залишки металу, прохідні |
| Lock | tile | — | далі не перевертається |
| Illustration | tile | — | замальована Artist-ом, заблокована; розблоковує Sun; у 1P при смерті гравця стираються всі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(player, dir)`, `face(player, dir)`.
- КОЛИ `input(flip)` → ЯКЩО `not state(target_tile, lock|illustration|metal)` → ТО `custom: «зняти верхній шар плитки під собою чи перед собою»` (`+effect:flip`), `reveal(next_layer)`.
- КОЛИ `custom: «плитку перевернуто під лялькою»` → ТО `custom: «лялька відлітає від гравця»` (`+effect:knockback`); дальність залежить від ляльки (Kid — далеко) (?).
- КОЛИ `blocked(doll)` під час відльоту → ЯКЩО `cell(next, wall|metal)` → ТО `disappear_a`, `score(10)`.
- КОЛИ `custom: «синю ляльку відкинуло, але не знищено»` → ТО `split(doll)` → два Kid.
- КОЛИ `contact(doll, player)` → ТО `lives(-1)` (вороги атакують тілом; боси ще кидають плитки).
- КОЛИ `all_gone(doll)` → ТО `win`, `next_level`.
- КОЛИ `custom: «жодної плитки, яку можна перевернути»` (усі Lock, Metal, Illustration) → ТО `win` («stalemate»).
- КОЛИ `enter(player, star)` → ТО `pickup`, `score(100)`, `counter(stars, +1)`; КОЛИ `counter(stars, >=, 100)` → ТО `lives(+1)`, `speed(player, +1)`.
- КОЛИ `enter(player, roulette)` → ТО `custom: «ефект поточної іконки: STARS / 1UP / 10000 / 1000 / 10»`.
- КОЛИ `enter(player, time_tile)` → ТО `timer(+5)`, `score(2000)`.
- КОЛИ `custom: «відкрито Sun»` → ТО `custom: «перевернути всі інші плитки»`, `clear_state(room, dark)`, `clear_state(illustrations, locked)`, `score(5000)`.
- КОЛИ `custom: «відкрито Cross»` → ТО `custom: «перевернути 4 сусідні плитки»`, `score(1000)`; Clock — у напрямку, що обертається, `score(1500)`.
- КОЛИ `custom: «відкрито Moon»` → ТО `set_state(room, dark)`, `transform(visible_normal_tiles, star)`, `score(3000)`.
- КОЛИ `enter(player, attack_tile)` → ТО `slide(player, facing)`, `set_state(player, launched)`; ЯКЩО `contact(player, doll)` на льоту → ТО `disappear_b`, `multiplier(2)`; `score(100)` за відскок.
- КОЛИ `enter(player, special_bonus)` → ТО `custom: «виліт за екран»`, `window(custom: бонус-етап із зірками)`.
- КОЛИ `custom: «відкрито Enemy-плитку»` → ЯКЩО `count(doll, <, n)` → ТО `spawn(doll)`.
- КОЛИ `contact(pink_ballerina, metal)` або атака → ТО `set_cell(metal, rubble)`.
- КОЛИ `custom: «Artist зупинився на плитці»` → ТО `transform(tile, illustration)`; КОЛИ `died(player)` → ЯКЩО `mode(1p)` → ТО `custom: «стерти всі Illustration»`.
- КОЛИ `input(dir)` (гравець) → ТО `custom: «Mimi повторює рух дзеркально»`.
- КОЛИ `timer(hidden)` спливає → ТО `speed(dolls, +1)`, `speed(player, -1)`, `sound(fast_music)`.
- 2P одночасно: КОЛИ `custom: «перевернуто плитку під іншим гравцем»` → ТО `custom: «його відкидає»`, `set_state(other, launched)` (тимчасова невразливість, ×2 очки).
- Перемога: усі ляльки знищені або stalemate; гра — 10 етапів (8 на вибір + Castle + Sky Castle). · Поразка: життя скінчились (у 2P другий грає далі). · Рахунок: очки за ляльок, плитки, бонуси; 100 зірок = життя.

## Керування і ввід
- D-pad — рух і поворот; кнопка — перевернути плитку перед собою / під собою (?) — точна розкладка A/B не перевірена.
- 2P: другий геймпад; ті самі кнопки.
- Extra Quinty: утримати Select + Start при ввімкненні консолі.

## Вікна, меню, HUD
- `splash-screen` (титул; червоне «EXTRA» в Extra Quinty) → `mode-select` (1P / 2P) (?).
- `level-select`: палаци-етапи з ляльками, що в них живуть (EN-вікі); спершу доступні 8 з 10.
- `game-screen`: кімната 5×7; HUD — зірки й життя кожного гравця окремо, очки (?).
- `custom-window`: бонус-етап із зірками (Special Bonus); раунд-бос.
- `dialogue-window` / катсцена: після боса дівчину переносять в інше місце.
- `end-screen` / game over (?); фінал після Sky Castle.
- Переходи: level-select → 10 раундів етапу → бос → катсцена → level-select; 8 етапів → Castle → Sky Castle.

## Фічі поза полем
- `level-select` + `level-unlock`: довільний порядок 8 етапів, далі два фінальні.
- `mode-coop` (2P): різні етапи — по черзі, той самий — одночасно; смерть не зупиняє гру.
- Прихований режим Extra Quinty: раунди 1–100 підряд, швидкість росте з очками.
- `+feature:hidden-hurry-timer` — таймер, якого не видно, з покаранням швидкістю.
- Паролі / збереження / редактор — джерела не згадують (?).

## Варіації й родичі
- Осі варіацій:
  - **як прибрати ворога**: розчавити ковзним блоком (Pengo) / кинути кулю ([chew-man-fu](chew-man-fu.md)) / вибити з-під ніг підлогу, щоб він улетів у стіну (Mendel Palace) / закопати в яму (Lode Runner);
  - **підлога**: статична / одношарова, що змінюється (Q*bert) / стос шарів із прихованими візерунками;
  - **область дії плитки**: одна (звичайна) / хрест (Cross) / напрям, що обертається (Clock) / усе поле (Sun);
  - **мета раунду**: знищити всіх / зробити поле нерухомим (stalemate).
- Родичі: [pengo](pengo.md) (той самий тип кімнати-арени), Q*bert і Xonix (підлога як стан), Pac-Man (переслідувачі різного характеру); наступні ігри Game Freak — серія Pokémon.

## Цікавинки для курсу
- Плитка-стос: верхній шар діє, перевертання знімає його й відкриває наступний — 🌱 (список у клітині).
- Відкидання ляльки з перевернутої плитки до стіни зі знищенням — 📎 (напрям від гравця + дальність за типом).
- Плитки з областю дії: Cross (4 сусіди), Clock (обертовий напрям), Sun (усе поле) — 📎 за сімʼю.
- Stalemate-перемога: «усі плитки заблоковані» як друга умова — 🌱.
- Artist, що блокує плитки, і Sun, що їх звільняє — 📎.
- Mimi, що дзеркалить ввід гравця — 🌱; Blue, що ділиться на двох Kid — 📎.
- Прихований таймер: прискорення ворогів і сповільнення гравця замість смерті — 🌱.
- Рулетка-плитка: ефект за фазою циклу в момент проходу — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `impassable-cells` ↔ стіна, Metal; `destroy-all-enemies` ↔ мета раунду; `touch-death` + `player-death`; `chase-greedy` ↔ помаранчеві/рожеві/Illustman; `random-walk` ↔ Walkman (?); `temporary-modes` ↔ Attack-запуск з невразливістю; `item-pickup` ↔ зірки; `extra-life-threshold` ↔ 100 зірок; `event-points` ↔ таблиця очок плиток; `timeout-punisher` ↔ прихований таймер; `level-select` + `level-unlock` ↔ палаци; `spawn-points` ↔ Enemy-плитка.
- **Нема** → пропозиції карток:
  - `+tile-flip-knockback` «Перевернути плитку під ворогом — його відкидає» · entities/combat · 📎 · слот {range: by_kind}.
  - `+layered-tile-stack` «Клітина — стос шарів, перевертання відкриває наступний» · entities/state · 🌱 · слот {layers: 2..7}.
  - `+stalemate-win` (вже ×4) — перемога, коли поле заблоковане.
  - `+flip-area-tile` «Плитка перевертає область» · entities/interact · 📎 · слот {shape: cross|rotating|all}.
  - `+bonus-roulette` (вже пропонована) — рулетка-плитка.
  - `+launch-tile` «Плитка запускає гравця до стіни» · entities/move · 📎.
  - `+bonus-stage` · `+dark-zone` · `+mimic-copy` · `+split-on-death` · `+lock-cell` · `+paint-cell` · `+knockback` · `+mode-coop` — вже пропоновані іншими іграми.

## Пропозиції до словників
- `+effect:flip` — зняти верхній шар плитки / перевернути (×4 у пропозиціях).
- `+effect:knockback` — відкинути сутність від джерела до упору.
- `+cond:layers_left` — скільки шарів лишилось у стосі клітини.
- `+trigger:knocked_into_wall` — відкинута сутність врізалась у стіну (смерть ляльки).
- `+feature:hidden-hurry-timer` — прихований таймер раунду зі штрафом швидкістю.
- `+card:tile-flip-knockback`, `+card:layered-tile-stack`, `+card:flip-area-tile`, `+card:launch-tile` — див. вище.

## Джерела
- ⭐ [Wikipedia: Mendel Palace](https://en.wikipedia.org/wiki/Mendel_Palace) — кімната «5 by 7 grid of floor tiles», перевертання під собою чи поруч, знищення об стіну чи блок, Spinner, stalemate, ляльки-перевертачі, темні кімнати, 10 рівнів + бос на світ, кооп і лічильники кожного гравця, Game Freak, Namco/Hudson.
- [Wikipedia JA: クインティ](https://ja.wikipedia.org/wiki/クインティ) — 2–7 шарів, 10 етапів × 10 раундів, вибір 8 з 10, усі вороги за етапами, 15 типів плиток з очками, прихований таймер, правила 2P, Extra Quinty.
- YouTube: пошук «Mendel Palace NES gameplay».

## Непевне
- (?) Дальність відльоту ляльки: до стіни завжди чи на кілька клітин за типом (JA: Kid «відлітає далеко») — і чи відкидає всіх ляльок на плитці.
- (?) Яку плитку перевертає кнопка: під собою чи попереду — EN-вікі каже «standing on or adjacent to», розкладка не перевірена.
- (?) Поведінка зеленої ляльки («тікає, якщо не підійти» — дослівно з JA), стрибунів Pyramid, Swimmer.
- (?) Чи всі плитки-спецефекти діють при відкритті, чи при проході гравця (Roulette, Time, Attack — при проході; Sun, Cross — схоже, при відкритті).
- (?) Наявність паролів, екрана game over і continue.
- (?) Кількість життів на старті.
