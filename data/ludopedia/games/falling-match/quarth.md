---
title: Quarth (Кварт)
slug: quarth
aka: [Block Hole, Block Game, クォース]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: survive
year: 1989
platforms: [arcade, MSX2, Famicom, Game Boy, PC-9801, X68000, PS2, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quarth", best: true, note: "корабель стріляє блоками вгору, добудувати прямокутник, очки за розмір, поразка на пунктирній лінії, 2P split/coop, версії"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/クォース", note: "деталі: до 4 пострілів підряд, розʼєднані блоки як сторона фігури, срібний/золотий блок, предмети FC (E/B/S/C) і GB, зони 0–9, versus-атаки"}
  - {kind: other, url: "https://www.hardcoregaming101.net/quarth/", note: "HG101 — стаття (під час дослідження сайт на техобслуговуванні)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quarth+arcade+konami+gameplay", note: "пошук; аркадний геймплей"}
stage: v1
coverage: 65
mechanics: [projectile-shot, shoot-forward, move-by-input, keyboard-controls, progress-acceleration, event-points, extra-life-threshold, item-pickup, temporary-modes, sequential-levels, score-records, hot-seat, simultaneous-versus, mode-select, end-screen, +shoot-to-complete-shape, +rectangle-closure-clear, +descending-pattern, +clear-all-special, +blind-attack, +shared-field-coop]
proposes: ["+effect:attach_to", "+effect:scroll_field", "+cond:rectangle_complete"]
author: opus
date: 2026-11-09
---

# Quarth — Tetris навиворіт: корабель знизу стріляє блоками, добудовуючи падаючі фігури до прямокутників

## Суть
Зверху повільно насувається поле з незавершених фігур із блоків. Гравець керує гарматою-кораблем знизу, рухає її ліворуч/праворуч і **вистрілює окремі блоки вгору**; вони прилипають до фігур. Щойно фігура стає **повним прямокутником чи квадратом** — вона зникає, і що більша, то більше очок. Якщо фігури доповзли до пунктирної лінії над кораблем — корабель розчавлено. Shooter-керування поверх Tetris-ідеї «заповни дірки».

## Поле і час
- Вертикальне поле фіксованої ширини (?); фігури «прокручуються» вниз по одному ряду за тік прокрутки.
- Real-time: темп прокрутки росте з рівнем; порожні постріли (FC) коротко прискорюють прокрутку.
- Під час анімації зникнення прямокутника прокрутка стоїть, а стріляти можна.
- Структура: зони 0–9, у кожній рівні; на екрані «Y/X» (рівень/зона); після 9/9 — петля на 0/0 (FC).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Корабель-гармата | player | позиція x, швидкість | рух ліворуч/праворуч; постріл блоком угору; до 4 пострілів у повітрі |
| Блок-снаряд | projectile | 1 клітина | летить угору, прилипає до першого блоку/фігури над собою |
| Фігура (група блоків) | object | форма | спускається з прокруткою; повний прямокутник → зникає |
| Розʼєднані блоки | object | — | кілька окремих груп можуть утворити одну сторону прямокутника; дірки всередині допускаються й рахуються як заповнені |
| Срібний блок | tile | раз на 75 блоків | його прямокутник стирає все на екрані + очки |
| Золотий блок (аркада) | tile | після «9/X» | зникнення завершує зону |
| Кольорові блоки FC: E · B · S · C | pickup | тип | E — стерти все; B — бонус за розмір; S — пауза прокрутки (можна виїхати вперед); C — гармата змінюється на час, очки ×2 |
| Предмети GB | pickup | 4 + випадковий | швидші снаряди · стоп прокрутки · стерти все · повільніше падіння; 5-й — випадково один із них, «пов'язка на очі» або всі разом |
| Пунктирна лінія | static | над кораблем | межа поразки |
| Другий корабель (coop) | ally | — | на ширшому спільному полі; кораблі не проходять один крізь одного |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(target_cell)` → ТО `move(ship, dir)`.
- КОЛИ `input(fire)` → ЯКЩО `count(shots_in_air, <, 4)` → ТО `spawn_at(block_shot, above_ship)`.
- КОЛИ `tick` → ТО `move(block_shot, up)`.
- КОЛИ `contact(block_shot, block)` → ТО `custom: «attach — снаряд стає частиною фігури над собою»`.
- КОЛИ `after(attach)` → ЯКЩО `custom: «група утворює повний прямокутник (дірки всередині дозволені)»` → ТО `clear(group)`, `score(size_incl_holes)`.
- КОЛИ `after(clear)` → ЯКЩО `count(groups_cleared_at_once, ≥, 2)` → ТО `multiplier(×n)`.
- КОЛИ `timer(scroll_rate)` → ЯКЩО `custom: «нема анімації зникнення»` → ТО `custom: «scroll — уся маса фігур на ряд вниз»`.
- КОЛИ `reach(any_block, dotted_line)` → ТО `lose` («quarthed» — корабель сплющено); аркада може мати життя: `lives(−1)`.
- КОЛИ `counter(blocks, %, 75)` → ТО `spawn_at(silver_block, pattern)`; КОЛИ `destroyed(silver_block)` → ТО `clear(all)`, `score(+bonus)`.
- КОЛИ `destroyed(gold_block)` → ТО `next_level` (кінець зони, аркада).
- КОЛИ `destroyed(item_block)` → ТО ефект: E `clear(all)` · B `score(+size_bonus)` · S `set_state(scroll, paused, t)` · C `set_state(ship, powered, t)`, `multiplier(×2)` (FC).
- КОЛИ `input(fire)` → ЯКЩО `custom: «постріл пішов у порожнечу»` → ТО `speed(scroll, +)` коротко (FC).
- КОЛИ `counter(score, %, 10000)` → ТО `lives(+1)` (FC).
- КОЛИ `counter(level_distance, ≥, n)` → ТО `counter(level, +1)`, `speed(scroll, +)`.
- Versus (аркада): КОЛИ `custom: «зчищено 3+ блоки за раз»` → ТО `hide(opponent_field, from_top)`; свої сховані ділянки відкриваються зчищенням.
- Versus (FC): КОЛИ `after(clear)` → ТО `custom: «корабель суперника підіймається, твій опускається»`.
- GB stage-set: КОЛИ `level_end` → ЯКЩО `counter(cleared, <, quota)` → ТО `restart`.
- Поразка: блок на пунктирі. Рахунок: розмір прямокутника (з дірками), множник за одночасні.

## Керування і ввід
- Аркада: важіль ←/→ і кнопка пострілу; до 4 снарядів у повітрі одночасно.
- Навмисно стріляти «зайве», щоб злити фігури в більшу — більше очок.
- Coop: два кораблі на одному полі, можуть заходити в центр, але не штовхають і не проходять один одного.

## Вікна, меню, HUD
- `attract-demo` → `main-menu`/вибір кількості гравців: 1P · 2P versus · 2P coop (аркада); GB — random mode / stage set, вибір з 6 гармат (кожна зі своєю музикою).
- `game-screen`: поле з фігурами, пунктирна лінія, корабель, `score`, `hi-score`, «Y/X» (`level-number`), `lives` (FC, аркада за DIP).
- 2P: два поля поруч (P1 ліворуч, P2 праворуч) або одне широке (coop).
- `end-screen` Game Over → `leaderboard` (аркада).
- Переходи: demo → старт → game-screen → (пунктир) game over / (золотий блок) наступна зона.

## Фічі поза полем
- `mode-versus`, `mode-coop` (спільне поле), GB: `mode-endless` (random) і stage set з квотами (`levels-sequential`).
- `custom: «вибір типу гармати»` (FC — 2, GB — 6).
- `operator-settings`: життя замість однієї спроби (аркада).
- Нема hold, undo, pause у меню (?).

## Варіації й родичі
- Quarth (аркада, 1989) → MSX2 (SCC-звук, coop на вузькому полі), Famicom (кольорові предмети, 1UP), Game Boy (Block Hole у США, предмети, link-versus) → «Block Game» у Konami GB Collection Vol.2 → Arcade Archives (2021).
- Родичі: Tetris (дірки заповнюються згори вниз), Space Invaders (стрілець знизу проти маси, що спускається), Puzznic, Plotting (Taito, стріляєш блоком у поле), Shooting-puzzle ігри Taito.
- **Осі варіацій**: звідки приходить блок (падає / вистрілюється) · критерій зникнення (повний ряд / колір / повний прямокутник) · дірки всередині (заборонені / зараховуються) · атака у versus (сміття / сховати поле / зсув гармати).

## Цікавинки для курсу
- Перевірка «група клітин — повний прямокутник» (bbox = кількість клітин, з поправкою на дірки) — 🌱.
- Звʼязні групи блоків (flood fill) і злиття груп при прилипанні снаряда — 📎.
- Стрілець знизу + прокрутка поля вниз, пауза прокрутки під час анімації — 📎.
- Розʼєднані групи, що разом утворюють прямокутник — 🥉 (нетривіальне визначення «фігури»).
- Предмети-модифікатори (стоп прокрутки, стерти все, ×2) — 🌱.
- Versus-атака «сховати верх поля суперника» — 📎.

## Мапа на каталог
- Є: `projectile-shot` · `shoot-forward` · `move-by-input` · `keyboard-controls` · `progress-acceleration` · `event-points` · `extra-life-threshold` (1UP за 10000) · `item-pickup` · `temporary-modes` (S, C) · `sequential-levels` · `score-records` · `hot-seat` (2P одночасно; найближча) · `simultaneous-versus` · `mode-select` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+shoot-to-complete-shape` «Стріляєш блоками, щоб добудувати фігуру» · entities/interact · 📎.
  - `+rectangle-closure-clear` «Група, що стала прямокутником, зникає» · entities/interact · 🌱.
  - `+descending-pattern` «Маса фігур спускається прокруткою» · entities/move · 🌱.
  - `+clear-all-special` «Спецблок/предмет стирає все поле» · entities/interact · 🌱.
  - `+blind-attack` «Атака ховає частину поля суперника» · game-logic/opponent · 📎.
  - `+shared-field-coop` «Двоє гравців на одному ширшому полі» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+effect:attach_to` — снаряд прилипає до цілі й стає її частиною (Quarth; близьке до ⏳ `attach`, але одностороннє й без розʼєднання — можливо, досить `attach`).
- `+effect:scroll_field` — усе поле зсувається на ряд (прокрутка маси вниз; Quarth, Panel de Pon — підйом).
- `+cond:rectangle_complete` — множина клітин утворює повний прямокутник.

## Джерела
- ⭐ [Wikipedia: Quarth](https://en.wikipedia.org/wiki/Quarth) — суть, корабель, очки за розмір, поразка, бонуси, 2P, платформи й назви.
- [ja.wikipedia: クォース](https://ja.wikipedia.org/wiki/クォース) — 4 постріли, розʼєднані блоки й дірки, срібний (кожні 75) і золотий блоки, предмети FC/GB, зони «Y/X», versus-атаки, відмінності версій.
- [Hardcore Gaming 101: Quarth](https://www.hardcoregaming101.net/quarth/) — стаття з черги; під час дослідження сайт був на техобслуговуванні, зміст не перевірено.
- YouTube: пошук «quarth arcade konami gameplay».

## Непевне
- (?) Ширина поля і висота; чи шаблони фігур фіксовані на рівень, чи випадкові (`random: runtime` — припущення).
- (?) Чи прилиплий снаряд, що не торкається жодної фігури (порожній постріл) зникає за верхом.
- (?) Формула множника за одночасні прямокутники.
- (?) Деталі «Y/X»: скільки рівнів у зоні.
- (?) Пункти меню й наявність паузи на кожній платформі.
