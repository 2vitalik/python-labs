---
title: Prince of Persia
slug: prince-of-persia
aka: [PoP, PoP1, Prince of Persia 1, Принц Персії]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 1989
platforms: [Apple II, MS-DOS, Amiga, Atari ST, Macintosh, NES, SNES, Game Boy, Genesis, Master System, PC Engine, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Prince_of_Persia_(1989_video_game)", best: true, note: "60 хвилин, трикутники здоровʼя, зілля, пастки, ворота з тригерами, шкода від падіння, фехтування, рівні"}
  - {kind: other, url: "https://github.com/NagyD/SDLPoP", note: "відкритий порт DOS-версії: повне керування, клавіші гри, чити, quicksave, replay"}
  - {kind: other, url: "https://raw.githubusercontent.com/NagyD/SDLPoP/master/src/types.h", note: "переліки тайлів (31 тип), кімната 10×3, до 24 кімнат на рівень"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Prince+of+Persia+1989+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, hp-damage, time-out, touch-death, environment-death, player-death, button-toggle, item-pickup, reach-exit, sequential-levels, save-single-slot, restart-level, game-pause, cheat-codes, movement-animation, death-animation, sound-effects, game-screen, +loose-floor, +fall-damage-by-height, +timed-gate, +ledge-grab, +sword-duel, +potion-effects, +session-timer, +boss-fight, +push-enemy-into-trap]
proposes: ["+trigger:landed", "+effect:hang", "+effect:flip_view", "+effect:parry", "+role:trap", "+card:loose-floor", "+card:fall-damage-by-height", "+card:timed-gate", "+card:session-timer", "+card:sword-duel"]
author: opus
date: 2026-11-09
---

# Prince of Persia — за 60 хвилин пройти 12 рівнів підземелля пастками, воротами й фехтуванням; рух анімаційними кроками по клітинах 10×3

## Суть
Принц тікає з підземелля до вежі, де Джафар тримає принцесу, і має на це **60 хвилин на всю гру**. Рух — ротоскопічна анімація, але логіка клітинна: кімната — 10×3 тайли, крок, стрибок і падіння вимірюються клітинами й поверхами. Небезпеки — шипи, «гільйотини», ями, **плити, що обвалюються**, і **ворота, які плита-тригер відкриває лише на час**. Вартових бʼють мечем у дуелі «удар/блок» або зіштовхують у пастки. Падіння на 2 поверхи забирає здоровʼя, на 3+ — смерть.

## Поле і час
- Рівень — граф кімнат (до 24), кожна 10 стовпців × 3 ряди тайлів; кімнати зʼєднані 4 сусідами (ліво/право/верх/низ); екран показує одну кімнату (`player-camera` фліп-екраном).
- Тайл має тип (31 тип у DOS-версії) і модифікатор (стан плити, вид зілля, відкритість воріт).
- Real-time, ~кадр; час гри — один глобальний таймер 60 хв (SNES — 120), смерть перезапускає рівень, але **не таймер**.
- Інформація часткова: видно лише поточну кімнату; плити, що обвалюються, видно за легким тремтінням (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Принц (Kid) | player | HP-трикутники (старт 3), меч | біг, обережний крок, стрибок, присід, вис на краю й підтягування, фехтування |
| Вартовий | enemy | HP-трикутники | фехтує; гине від меча, падіння чи пастки |
| Скелет (рівень 3) | enemy | безсмертний для меча | перемагається скиданням у яму |
| Тінь / двійник (дзеркало) | enemy | спільне життя з Принцом | виходить із дзеркала; шкодить, краде зілля; на 12 рівні з нею треба злитися |
| Джафар | boss | HP | фінальний фехтувальник; перемога зупиняє таймер |
| Підлога | terrain | — | опора |
| Плита, що обвалюється (loose) | terrain | ціла / падає | від кроку тремтить і падає вниз, стаючи уламками; влучивши в Принца, −1 HP |
| Уламки (debris) | terrain | — | розбита підлога, по якій ходять |
| Шипи | hazard | сховані / висунуті | висуваються, коли поряд біжать; смерть при бігу/падінні на них |
| Гільйотина (chomper) | hazard | цикл | щелепи періодично змикаються; потрапив — смерть |
| Ворота | gate | відкриті / закриваються / закриті | піднімаються від плити-відкривача на час, потім опускаються |
| Плита-відкривач (raise button) | switch | — | наступив — ворота вгору |
| Плита-закривач (drop button) | switch | — | наступив — ворота вниз |
| Застрягла плита (stuck) | switch | — | утоплена назавжди (?) |
| Двері виходу | gate | закриті / відкриті | відкриваються плитою; вхід = наступний рівень |
| Зілля мале червоне | pickup | +1 HP | лікує один трикутник |
| Зілля мале синє | pickup | −1 HP | отрута |
| Зілля велике червоне | pickup | +1 max HP | додає трикутник |
| Зілля велике зелене | pickup | стан | ширяння (повільне падіння); на рівні 9 — перевертає екран |
| Меч | pickup | — | рівень 1; без нього не фехтувати |
| Дзеркало | static | — | з нього виходить тінь; крізь нього можна стрибнути (?) |
| Колона, гобелен, факел, решітки, балкон | static | — | декор/стіни; колона закриває Принца спереду |
| Миша (рівень 8) | neutral | — | відкриває ворота, у яких Принц застряг |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(kid, dir)` анімаційними кроками; `input(shift+dir)` → обережний крок до краю.
- КОЛИ `input(up+dir)` → ТО `custom: «стрибок уперед на кілька клітин»`; з розбігу — довший.
- КОЛИ `custom: «під Принцом нема опори»` → ТО `fall(kid)`; КОЛИ `input(shift)` у падінні → ЯКЩО `custom: «поряд край»` → ТО `custom: «вчепитися й висіти»`; `input(up)` на висінні → підтягнутись.
- КОЛИ `custom: «приземлився після падіння на 2 поверхи»` → ТО `damage(1)`; на 3+ поверхи → `lose` (смерть); на 1 — без шкоди.
- КОЛИ `enter(kid, loose_floor)` → ТО `set_state(loose, shaking)`, `fall(loose)`; КОЛИ `contact(loose, floor)` → ТО `set_cell(cell, debris)`; КОЛИ `contact(loose, kid)` → ТО `damage(1)`.
- КОЛИ `enter(kid, raise_button)` → ТО `set_state(gate, open, duration)`; КОЛИ `timer(every)` → ЯКЩО `state(gate, open)` → ТО `custom: «ворота поволі опускаються»`.
- КОЛИ `enter(kid, drop_button)` → ТО `set_state(gate, closed)`.
- КОЛИ `contact(kid, gate)` → ЯКЩО `state(gate, closed)` → ТО `block`.
- КОЛИ `in_range(kid, spikes, 1)` → ТО `set_state(spikes, out)`; КОЛИ `enter(kid, spikes)` → ЯКЩО `state(spikes, out)` і `custom: «біг або стрибок/падіння»` → ТО `lose`.
- КОЛИ `timer(every)` → ТО `custom: «гільйотина змикається»`; КОЛИ `contact(kid, chomper)` → ЯКЩО `state(chomper, closed)` → ТО `lose`.
- КОЛИ `enter(kid, pit)` → ТО `fall(kid)` — ями й прірви: смерть, якщо глибоко.
- КОЛИ `contact(kid, potion)` → ТО `pickup`, ефект за видом: `heal(kid, 1)` / `damage(1)` / `custom: «max HP +1»` / `set_state(kid, float, duration)`.
- КОЛИ `custom: «зілля перевертання (рівень 9)»` → ТО `custom: «перевернути екран догори дриґом»`; друге зілля повертає.
- КОЛИ `line_of_sight(guard, kid)` → ТО `custom: «вартовий стає в стійку і йде на зближення»`.
- КОЛИ `input(shift)` у стійці → ТО `custom: «удар»`; КОЛИ удар → ЯКЩО `not custom: «суперник блокує»` → ТО `damage(1)` супернику.
- КОЛИ `input(up)` у стійці → ТО `custom: «блок»`; блок і одразу удар — контратака.
- КОЛИ `custom: «вартового відтіснили на пастку/край»` → ТО `fall(guard)` або `lose` для вартового.
- КОЛИ `hp_zero(kid)` → ТО `lose`, `restart` рівня; таймер гри йде далі.
- КОЛИ `enter(kid, exit_button)` → ТО `set_state(exit_door, open)`; КОЛИ `enter(kid, exit_door)` → ЯКЩО `state(exit_door, open)` → ТО `next_level`.
- КОЛИ `custom: «Принц і тінь зливаються (рівень 12)»` → ТО `merge(kid, shadow → kid)`, далі шлях до Джафара.
- КОЛИ `hp_zero(jaffar)` → ТО `timer(stop)`, `win` після зустрічі з принцесою.
- КОЛИ `counter(time, ==, 0)` → ТО `lose` гри (виняток у DOS/Mac: якщо вже у фінальній зоні 12 рівня).
- Перемога: перемогти Джафара й дійти до принцеси до кінця 60 хв. Поразка: вичерпано час. Рахунку нема — результат = залишок часу.

## Керування і ввід
- ←/→ — поворот і біг; Shift+←/→ — обережний крок; ↑ — стрибок на місці / вгору, Home або ↑+← — стрибок уліво; ↑ на бігу — стрибок з розбігу; ↓ — присід/злізти.
- Shift — схопитися за край у падінні, взяти/випити зілля.
- Фехтування: ←/→ — наступ/відступ, Shift — удар, ↑ — блок, ↓ — сховати меч (Shift — витягти знову).
- Службові: Esc — пауза; Space — показати залишок часу; Ctrl+A — рестарт рівня; Ctrl+G — зберегти (рівні 3+); Ctrl+L — завантажити (на заставці); Ctrl+R — на заставку; Ctrl+S — звук.

## Вікна, меню, HUD
- `splash-screen` / інтро з сюжетною сценою (Джафар і принцеса) — `dialogue-window` без тексту (?).
- `game-screen`: одна кімната + рядок унизу: `hp-bar` трикутниками Принца й суперника, повідомлення («LEVEL 2», «55 MINUTES LEFT»).
- `pause-menu` — пауза (у DOS — лише напис «Game Paused»).
- Сцени між рівнями — принцеса й пісочний годинник (`custom-window`).
- `end-screen` — фінал із принцесою або поразка за часом.
- SDLPoP (неоригінал): `settings-window` («Enhanced mode»), `replay-window`.
- Переходи: заставка → рівень 1 → (двері) наступний рівень … → Джафар → фінал; (смерть) → рестарт рівня; (час) → поразка.

## Фічі поза полем
- `levels-sequential`: 12 рівнів (+ окремий фінальний бій у деяких версіях; SNES — більше).
- `save-slots`: один сейв з рівня 2–3, лише на початок рівня (Ctrl+G).
- `restart-level`, `pause`, показ залишку часу на вимогу.
- Чити в оригіналі DOS («megahit»-режим) (?) — у SDLPoP документовані: наступний рівень, воскресити, вбити вартового, +HP.
- Неоригінальні (SDLPoP): quicksave/quickload, replay, моди рівнів; зовнішній редактор Apoplexy.

## Варіації й родичі
- Prince of Persia 2: The Shadow and the Flame (1993), Prince of Persia Classic (2007, ремейк), SNES-версія з новими рівнями і 120 хв.
- Кінематографічні платформери: Another World, Flashback, Oddworld — та сама «анімаційна клітина».
- Karateka (1984, той самий автор) — ротоскопія і фехтування.
- Осі: **шкода від падіння** (без шкоди / за поверхами / смерть); **таймер** (на рівень / на всю гру, смерть не скидає); **пастка-плита** (відкриває на час / закриває / застрягла).

## Цікавинки для курсу
- Рух як автомат анімаційних станів (біг, зупинка, обережний крок, вис) поверх сітки 10×3 — 🥈.
- Плита, що обвалюється: тремтіння → падіння як сутність → уламки, шкода тому, на кого впала — 📎.
- Ворота з таймером закриття і парою плит «відкрити/закрити» — 📎.
- Шкода від висоти падіння: лічильник поверхів у стані падіння — 🌱.
- Глобальний таймер гри, що не скидається смертю, — 🌱.
- Фехтування «удар/блок/контратака» з HP-трикутниками — 🥉.
- Зілля з кількома ефектами, включно з перевертанням екрана — 📎.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `hp-damage` · `time-out` · `touch-death` (шипи, гільйотина) · `environment-death` (падіння) · `player-death` · `button-toggle` (плити й ворота) · `item-pickup` (зілля, меч) · `reach-exit` · `sequential-levels` · `save-single-slot` · `restart-level` · `game-pause` · `cheat-codes` · `movement-animation` · `death-animation` · `sound-effects` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+loose-floor` «Плита обвалюється від кроку, падає й шкодить» · entities/interact · 📎.
  - `+fall-damage-by-height` «Шкода/смерть за кількістю поверхів падіння» · entities/death · 🌱.
  - `+timed-gate` «Ворота відкриті на N тіків після плити» · entities/interact · 📎 · слот {duration}.
  - `+ledge-grab` «Вчепитися за край і підтягнутись» · entities/move · 📎.
  - `+sword-duel` «Дуель удар/блок з HP» · entities/combat · 🥉.
  - `+potion-effects` «Зілля різних ефектів (лікування, отрута, max HP, ширяння)» · entities/state · 🌱.
  - `+session-timer` «Один таймер на всю гру, смерть не скидає» · game-logic/lose · 🌱.
  - `+push-enemy-into-trap` «Відтіснити ворога в пастку» · entities/combat · 📎.
  - `+boss-fight` — як у Kickle Cubicle.

## Пропозиції до словників
- `+trigger:landed(a, floors)` — приземлення з висоти N (спільне з Space Panic, Fire 'n Ice).
- `+effect:hang(a, ledge)` — вчепитися за край і висіти.
- `+effect:flip_view` — перевернути відображення поля (рівень 9).
- `+effect:parry` — заблокувати удар (дуелі).
- `+role:trap` — пастка зі станом/циклом (шипи, гільйотина), відмінна від статичної `hazard`.
- `+card:loose-floor`, `+card:fall-damage-by-height`, `+card:timed-gate`, `+card:session-timer`, `+card:sword-duel` — див. вище.

## Джерела
- ⭐ [Wikipedia: Prince of Persia (1989)](https://en.wikipedia.org/wiki/Prince_of_Persia_(1989_video_game)) — 60/120 хв, смерть не скидає таймер, трикутники, падіння 2/3+ поверхи, зілля, пастки, ворота й тригери, фехтування, скелет, тінь, миша, 12 рівнів, порти.
- [GitHub: SDLPoP](https://github.com/NagyD/SDLPoP) — керування Принцом і фехтуванням, службові клавіші, сейв з рівнів 3+, чити, quicksave, replay, моди.
- [SDLPoP types.h](https://raw.githubusercontent.com/NagyD/SDLPoP/master/src/types.h) — 31 тип тайла (loose, opener/closer, stuck, chomper, mirror, debris, level door…), кімната 10×3, ≤24 кімнати.
- YouTube: пошук «Prince of Persia 1989 gameplay».

## Непевне
- (?) Точна поведінка шипів (коли висуваються) і гільйотини (період) — з памʼяті.
- (?) «Застрягла» плита — утоплена назавжди чи блокує ворота відкритими; «locking triggers» з Вікіпедії, ймовірно, саме вона.
- (?) Дальність стрибків у клітинах (з місця / з розбігу) і чи плитка тремтить перед обвалом.
- (?) Чити оригінальної DOS-версії (запуск з параметром «megahit»), сцени з пісочним годинником між рівнями.
- (?) Чи можна стрибнути крізь дзеркало (рівень 4) — так виходить тінь, але деталі не перевірено.
