---
title: IQ Puzzler Pro
slug: iq-puzzler-pro
aka: [IQ Puzzler, IQ Puzzler Pro XXL, SG 455]
family: board-digital
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2013
platforms: [board, mobile]
links:
  - {kind: official, url: "https://www.smartgames.eu/uk/one-player-games/iq-puzzler-pro", best: true, note: "SmartGames: 12 фігур, 120 задач у 3 режимах (2D, 3D-піраміда, діагональна 2D), задані фігури не рухати, один розвʼязок"}
  - {kind: official, url: "https://www.smartgamesusa.com/one-player-games/iq-puzzler-pro", note: "SmartGames USA: та сама картка, +48 задач для завантаження"}
  - {kind: other, url: "http://gamesbysmart.com/en/iq-puzzler-pro", note: "склад коробки: дошка з кришкою, 12 фігур, буклет 120 задач з розвʼязками"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=IQ+Puzzler+Pro+pyramid+solution", note: "пошук; розвʼязки 2D і піраміди"}
stage: v1
coverage: 70
mechanics: [drag-drop-piece, hover-highlight, completion-detection, satisfy-constraints, level-bank, puzzle-select, level-unlock, difficulty-levels, level-solver, unique-puzzle-generation, restart-level, sequential-levels, +polyomino-placement, +piece-rotate-flip, +exact-cover-outline, +prefilled-pieces, +polycube-pyramid, +ball-piece-lattice, +multi-board-modes]
proposes: ["+cond:covers_exactly", "+effect:mirror", "+ui:piece-tray", "+ui:challenge-card", "+axis:field=pyramid", "+card:prefilled-pieces", "+card:polycube-pyramid"]
author: opus
date: 2026-11-09
---

# IQ Puzzler Pro — заповнити дошку всіма 12 фігурами, коли частину вже покладено за тебе (2D, діагональ, 3D-піраміда)

## Суть
Соло-головоломка SmartGames: 12 кольорових фігур і дошка з кількома сітками. Задача з буклета показує, які фігури вже стоять і де — їх не можна рухати; решту фігур треба вкласти в порожні клітини так, щоб дошка (або піраміда) заповнилась повністю. Кожна задача має **рівно один** розвʼязок; складність задається кількістю заданих фігур — чим менше підказок, тим важче.

## Поле і час
- **Три поля в одній коробці**: верх дошки — 2D-прямокутник і окрема основа для 3D-піраміди; низ — інша, «діагональна» 2D-сітка.
- **Піраміда**: 5 шарів, кожен вищий шар — менший квадрат, кульки лягають у лунки між кульками шару нижче.
- Фігури складені з кульок, зʼєднаних у плоскі форми (поліоміно з кульок) (?); тому та сама фігура лягає і на квадратну сітку, і в шар піраміди, і «стоячи» в діагональній площині піраміди.
- Часу нема: `static`, хід = поставити/зняти фігуру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура | piece | колір, форма з N кульок (12 різних) | ставиться з поворотами й дзеркалами в порожні клітини, без перекриттів |
| Задана фігура | static | колір, позиція з картки задачі | ставиться першою, не рухається |
| Лунка 2D-прямокутника | terrain | — | приймає одну кульку |
| Лунка діагональної сітки | terrain | — | інший контур і орієнтація сітки (?) |
| Лунка піраміди | terrain | шар 1–5 | кулька шару k тримається на 4 кульках шару k−1 |
| Набір фігур поза дошкою | supply | 12 мінус задані | звідси беруться фігури |
| Картка задачі | mark | режим, номер, рівень, задані фігури | визначає стартову позицію; розвʼязок — у кінці буклета |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «поставити задані фігури як на картці задачі»`; вони `set_state(fixed)`.
- КОЛИ `input(place(piece, cells, rotation, flip))` → ЯКЩО `fits(piece, cells)` and `free(cells)` → ТО `place(piece)`; інакше `block`.
- КОЛИ `input(lift(piece))` → ЯКЩО `not state(piece, fixed)` → ТО `custom: «фігура повертається в набір»`.
- Піраміда: КОЛИ `input(place(piece, cells))` → ЯКЩО `supported(cells)` → ТО `place(piece)`; кулька не висить у повітрі (?).
- КОЛИ `all_constraints_met` (усі лунки поля зайняті, усі 12 фігур на полі) → ТО `win`, `next_level`.
- Обмеження: кожна фігура використана рівно раз · жодна лунка не порожня · задані фігури не зрушено.
- Розвʼязок єдиний: `custom: «задача з буклета гарантує один розвʼязок»`.
- Перемога: заповнити поле · Поразки нема · Рахунку нема (лише прогрес по буклету).

## Керування і ввід
- Фізично: взяти фігуру, повернути/перевернути, вкласти; прозора кришка тримає фігури в дорозі.
- Цифрова версія (застосунок SmartGames (?)): drag фігури з лотка, тап — поворот, подвійний тап — дзеркало; фігура «прилипає» до лунок; drag назад у лоток — зняти.
- Режим обирається вибором поля: 2D / діагональ / піраміда (обертання камери для 3D).

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `mode-select` (2D · діагональ · піраміда) → `puzzle-select` (сітка задач з рівнями й позначками «розвʼязано»).
- `game-screen`: поле, `piece-tray` з фігурами, що лишились, `challenge-card` (номер і рівень задачі), `restart-button`, `hint-button` (?).
- `end-screen`: «розвʼязано», далі → наступна задача.
- `help-window`: правила з картинками · `solutions-window` (буклет має розвʼязки).
- Переходи: main-menu → mode-select → puzzle-select → game-screen → end-screen → puzzle-select.

## Фічі поза полем
- `puzzle-bank`: 120 задач у буклеті + 48 для завантаження; XXL-версія — 188.
- `levels-sequential` за складністю, `show-solution` (розвʼязки в кінці буклета), `stars-rating`/`level-unlock` у застосунку (?).
- Рівнів складності кілька, підписані на картках (?).

## Варіації й родичі
- Родичі в корпусі: [ubongo.md](ubongo.md) (та сама задача exact cover, але гонка на час і кубик визначає фігури; там IQ Puzzler — лише згадка), [pentomino.md](pentomino.md) (класичне пакування 12 пентаміно), [blokus.md](blokus.md), [patchwork.md](patchwork.md).
- Сімейство SmartGames IQ: IQ Puzzler Pro XXL (більше задач), IQ Fit (3D-фігури з виступами на плоскій дошці), IQ Stars, IQ Twist (кілочки-обмеження) (?).
- Katamino: прямокутник з повзунком ширини, фігур задано підмножину.
- **Осі варіацій**: поле (прямокутник / діагональ / піраміда / свій контур) · підказки (задані фігури / задана підмножина фігур / нічого) · гарантія (один розвʼязок / будь-який) · фігури (поліоміно / поліміно з кульок / полікуби).

## Цікавинки для курсу
- Перевірка розміщення фігури з поворотами й дзеркалами (до 8 орієнтацій, дедуплікація симетричних) — 📎.
- Розвʼязувач exact cover (Dancing Links / backtracking) для 2D з заданими фігурами — 🥈.
- Генератор задач: зняти з повного розвʼязку стільки фігур, щоб розвʼязок лишився єдиним (перевірка через розвʼязувач) — 🥇.
- Піраміда: координати лунок у 5 шарах, фігура як плоска множина кульок у площинах піраміди (горизонтальних і діагональних) — 🥇.
- Оцінка складності задачі за кількістю заданих фігур і вузлів перебору — 🥈.

## Мапа на каталог
- Є: `drag-drop-piece` · `hover-highlight` · `completion-detection` · `satisfy-constraints` · `level-bank` · `puzzle-select` · `level-unlock` · `difficulty-levels` · `level-solver` · `unique-puzzle-generation` · `restart-level` · `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+prefilled-pieces` «Частину фігур задано наперед і заблоковано» · entities/legality · 🌱 · слоти {скільки фігур задано}.
  - `+polycube-pyramid` «Піраміда з шарів, фігури лежать у горизонтальних і діагональних площинах» · field/topology · 🥇.
  - `+ball-piece-lattice` «Фігура з кульок: одна форма для квадратної сітки й FCC-піраміди» · entities/shape · 🥈.
  - `+multi-board-modes` «Кілька полів у грі, один набір фігур» · game-flow · 🌱.
  - `+polyomino-placement` · `+piece-rotate-flip` · `+exact-cover-outline` — як у Ubongo.

## Пропозиції до словників
- `+cond:covers_exactly` — фігури разом покривають поле без залишку (Ubongo вже пропонував).
- `+effect:mirror` — віддзеркалити фігуру (ширше за `rotate`).
- `+ui:piece-tray` — лоток фігур · `+ui:challenge-card` — номер, рівень і стартова позиція задачі.
- `+axis:field=pyramid` — шаровий FCC-лаштунок (між `layers` і `3d`).
- `+card:prefilled-pieces` · `+card:polycube-pyramid`.

## Джерела
- ⭐ [SmartGames: IQ Puzzler Pro](https://www.smartgames.eu/uk/one-player-games/iq-puzzler-pro) — 12 фігур, 120 задач, три режими, правило «задані фігури не рухати, один розвʼязок», +48 задач.
- [SmartGames USA: IQ Puzzler Pro](https://www.smartgamesusa.com/one-player-games/iq-puzzler-pro) — та сама картка: верх — 2D і 3D-сітки, низ — інша 2D-сітка.
- [Games by Smart: IQ Puzzler Pro](http://gamesbysmart.com/en/iq-puzzler-pro) — склад коробки, SG 455.
- Результати пошуку (магазини) — «діагональна 2D-сітка» на звороті, «піраміда з 5 шарів», XXL з 188 задачами.

## Непевне
- (?) Розміри: прямокутник 11×5 і піраміда 5 шарів (25+16+9+4+1 = 55 лунок) — 55 кульок на 12 фігур виведено з 5 шарів, не з джерела; розмір прямокутника не підтверджено.
- (?) Що фігури саме з кульок — з памʼяті; SmartGames пише лише «12 кольорових фігур».
- (?) Геометрія «діагональної» сітки на звороті і правило «опори» в піраміді — не перевірено.
- (?) Рік (~2013) і назви рівнів складності буклета — не знайдено.
- (?) Цифровий застосунок SmartGames і його меню — з памʼяті.
