---
title: Tetris Link
slug: tetris-link
aka: [Tetris Link Travel]
family: board-digital
also: [falling-match]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2011
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/tetris-link/game-rules.php", best: true, note: "правила: кубик форм, пропуск ходу, звʼязки ≥3, блокування, штраф за порожнини, кінець і тай-брейк"}
  - {kind: other, url: "https://rulespal.com/tetris-link/rulebook", note: "5 форм (L/J, O, S/Z, T, I), 4 кольори по 25, приклади сальдо +3−1, +4−2"}
  - {kind: other, url: "https://www.ultraboardgames.com/tetris-link/index.php", note: "склад, 2–4 гравці, видавці, альтернативна назва Tetris Link Travel"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tetris+Link+board+game", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [gravity-fall, polyomino-placement, piece-rotate-flip, multi-cell-size, connectivity-check, event-points, pass-turn, hot-seat, turn-enforcement, ai-opponent, drag-drop-piece, hover-highlight, game-screen, main-menu, match-setup, end-screen, help-window, +column-drop, +die-selects-piece, +wild-face, +link-group-scoring, +hole-under-penalty, +penalty-cap-per-turn, +longest-link-tiebreak, +no-line-clear]
proposes: ["+effect:roll_dice", "+cond:holes_below", "+cond:group_size", "+ui:dice-result", "+ui:score-rail", "+card:link-group-scoring", "+card:hole-under-penalty", "+card:die-selects-piece"]
author: opus
date: 2026-11-09
---

# Tetris Link — тетроміно з кубика вкидаються у вертикальну вежу: очки за звʼязані групи свого кольору, мінус за порожнини під фігурою

## Суть
Настільна гра за мотивами Tetris на 2–4 гравці. Кожен має 25 тетроміно свого кольору (5 форм по 5 штук); на початку ходу кидає кубик, грані якого — форми плюс «TETRIS LINK» (вибір будь-якої), і мусить вкинути випалу фігуру в спільну вертикальну вежу, як у Connect Four — фігура падає до опори. Групи з ≥3 своїх фігур, що торкаються сторонами, дають по очку за фігуру; порожні клітини під своєю щойно вкинутою фігурою — штраф до −2 за хід. Рядки не зникають: вежа лише заповнюється, і гра — про те, де звʼязатися з собою і як перекрити суперника.

## Поле і час
- Вежа — вертикальна прямокутна сітка зі стінками; фігури входять згори й осідають (`gravity: down`), висувати за верх не можна. Розмір (ширина × висота) — (?).
- Шари: клітини вежі (порожня / зайнята фігурою кольору) + маркери рахунку по боках.
- Хід = кидок кубика + одна фігура (або пропуск); без таймера. Кінець — вежа заповнена, жодна фігура не влазить.
- Інформація повна; випадковість — лише кубик.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вежа | zone | вертикальна сітка; верх відкритий | фігура вкидається згори в будь-якому положенні й падає до опори |
| Тетроміно | piece | колір (Blue, Green, Red, Yellow); форма I, O, T, L/J, S/Z; 5 кожної на гравця | обертається/перевертається перед вкиданням; після посадки не рухається |
| Кубик | object | 6 граней: 5 форм + «TETRIS LINK» | задає форму ходу; «TETRIS LINK» — будь-яка своя |
| Група | zone | фігури одного кольору, звʼязані сторонами (не діагоналлю) | ≥3 фігур → очки; кожна наступна приєднана → +1 |
| Порожнина під фігурою | zone | порожня клітина прямо під клітинами фігури | 1 → −1, ≥2 → −2 (максимум −2 за хід) |
| Маркер рахунку | mark | по одному на колір, бічні треки вежі | рух на сальдо ходу; може йти в мінус |
| Запас гравця | supply | 25 фігур | нема випалої форми → пропуск ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен кидає кубик; першим ходить той, у кого випало TETRIS LINK»`.
- КОЛИ `turn_start(player)` → ТО `custom: «кинути кубик форм»` (`+effect:roll_dice`).
- КОЛИ `after(roll_dice)` → ЯКЩО `not has(player, rolled_shape)` → ТО `skip_turn(player)`.
- КОЛИ `after(roll_dice)` → ЯКЩО `not fits(rolled_shape, tower)` (вежа майже повна) → ТО `skip_turn(player)`.
- КОЛИ `after(roll_dice)` → ЯКЩО `custom: «випало TETRIS LINK»` → ТО `choose(any_own_shape)`.
- КОЛИ `input(drop, column, orientation)` → ТО `rotate(piece, deg)`, `place(player, piece)` згори, `fall(piece)` до першої опори; вкинути треба, навіть якщо під фігурою лишиться порожнина.
- КОЛИ `locked(piece)` → ЯКЩО `connected(own_group)` і `custom: «у групі ≥ 3 фігур, звʼязаних сторонами»` (`+cond:group_size`) → ТО `score(+1 за кожну ще не зараховану фігуру групи)` — нова група з 3 = +3, приєднання до готової = +1.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «фігура зʼєднала дві групи»` → ТО `score(+1 лише за фігури, що ще не рахувались)`.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «під фігурою рівно 1 порожня клітина»` (`+cond:holes_below`) → ТО `score(-1)`; ЯКЩО `custom: «≥ 2 порожні клітини»` → ТО `score(-2)` — не більше −2 за хід.
- КОЛИ `turn_end(player)` → ТО `custom: «плюс і мінус ходу сальдуються (+3 −1 = +2; +4 −2 = +2)»`, `counter(score_marker, ±n)`.
- Перший кидок S/Z: `custom: «на рівному дні S/Z завжди лишає порожнину — стартовий рахунок мінусовий»`.
- Блокування: КОЛИ `locked(enemy_piece)` → ЯКЩО `custom: «чужі фігури оточили групу так, що до неї не дотягнутись»` → ТО `custom: «група поза грою; щоб знову рахувати, треба нову групу з 3»`.
- Поодинокі фігури й пари — 0 очок; можна в будь-який момент почати нову групу деінде й будувати від будь-якої.
- КОЛИ `no_moves(all)` (вежа заповнена) → ТО `game_over`.
- Перемога: найбільший рахунок · тай-брейк: найдовша звʼязка свого кольору (найбільше фігур у групі) · Поразка: — · Рахунок: групи мінус порожнини.

## Керування і ввід
- Настільна: кинути кубик, узяти фігуру, повернути/перевернути, вкинути в щілину вежі згори.
- (цифрова версія) `drag-drop-piece`: тягнути фігуру над вежею, клавіші/колесо — поворот і віддзеркалення; `ghost-piece` показує, де вона ляже, і скільки буде порожнин; кнопка «Кинути кубик» на старті ходу.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра · Правила.
- `match-setup`: 2–4 гравці, кольори, AI.
- `game-screen`: вежа; `dice-result` — випала форма; `pocket` — запас фігур гравця за формами (з лічильниками); `ghost-piece`; `score-rail` — бічні треки рахунку всіх кольорів (можна в мінус); `popup-text` «+3», «−1» над фігурою; `turn-indicator`.
- `toast` «нема такої форми — пропуск ходу».
- `end-screen`: рахунки, тай-брейк найдовшою звʼязкою; `help-window`: грані кубика, рахунок груп і штрафів.
- Переходи: main-menu → match-setup → game-screen ×N → end-screen.

## Фічі поза полем
- `hotseat` 2–4; варіант для 2 гравців — той самий (один колір на гравця).
- `ai-opponent-levels` (?) — жадібний AI легко оцінює кожне (колонка × поворот).
- Travel-версія (назва з UBG) — та сама гра в іншому форм-факторі (?).

## Варіації й родичі
- Tetris (`tetris.md`, falling-match) — те саме падіння тетроміно, але реальний час і зникнення рядків; тут рядки не зникають.
- FITS (`fits.md`) — тетроміно-подібні фігури вкидаються згори у власне поле, штраф за порожнини; Tricky Towers (`tricky-towers.md`) — вежі з фізикою.
- Connect Four (`line-games.md`, chess-abstract) — вкидання в колонку; тут замість лінії з 4 — звʼязні групи.
- **Осі варіацій**: хто обирає фігуру (кубик / рука / черга) · гравітація (вежа / плоска дошка) · що рахується (групи ≥3 / лінії / зниклі рядки) · штраф (порожнини під фігурою / нема) · кінець (вежа повна / ліміт фігур).

## Цікавинки для курсу
- Вкидання тетроміно в колонку з поворотом/віддзеркаленням: знайти найнижчу позицію, де фігура не перетинає зайняті клітини — 📎.
- Порожнини під фігурою: для кожної нижньої клітини фігури перевірити порожнечу під нею + стеля −2 — 🌱.
- Рахунок груп свого кольору (flood fill по фігурах, а не клітинах) з памʼяттю «уже зараховані» і злиттям груп — 🥉.
- Кубик з wild-гранню, пропуск ходу при відсутній формі або коли нема місця — 🌱.
- AI: перебір колонок × 8 орієнтацій з оцінкою «+звʼязки −порожнини −допомога супернику» — 🥉.
- Тай-брейк «найдовша звʼязка» = максимальна компонента — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `polyomino-placement` · `piece-rotate-flip` · `multi-cell-size` · `connectivity-check` ↔ групи · `event-points` · `pass-turn` ↔ пропуск без форми · `hot-seat` · `turn-enforcement` · `ai-opponent` · `drag-drop-piece` · `hover-highlight` · `game-screen`, `main-menu`, `match-setup`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+column-drop` (уже пропонована N-in-a-row) — вкидання з осіданням.
  - `+die-selects-piece` «Кубик визначає, яку фігуру грати» · game-logic/opponent · 🌱 · слоти {faces: 5 + wild}.
  - `+wild-face` «Грань-джокер: будь-яка фігура» · 🌱.
  - `+link-group-scoring` «Очки за кожну фігуру групи ≥3, раз за фігуру» · game-logic/score · 📎 · слоти {min: 3, adjacency: orthogonal}.
  - `+hole-under-penalty` «Штраф за порожні клітини під щойно поставленою фігурою» · game-logic/score · 🌱 · слоти {1: −1, 2+: −2}.
  - `+penalty-cap-per-turn` · `+longest-link-tiebreak` · `+no-line-clear` (уже пропонована Tricky Towers).

## Пропозиції до словників
- `+effect:roll_dice` — кинути кубик (уже пропоноване корпусом; `roll` у словнику — скочування).
- `+cond:holes_below(a, op, n)` — кількість порожніх клітин прямо під A.
- `+cond:group_size(a, op, n)` — розмір групи, до якої належить A (у фігурах).
- `+ui:dice-result` — результат кидка (уже пропоноване); `+ui:score-rail` — бічні треки рахунку всіх гравців.
- `+card:link-group-scoring` · `+card:hole-under-penalty` · `+card:die-selects-piece`.

## Джерела
- ⭐ [UltraBoardGames: Tetris Link rules](https://www.ultraboardgames.com/tetris-link/game-rules.php) — склад (вежа, 100 фігур, кубик), хід, пропуски, «TETRIS LINK» на кубику, звʼязки, блокування, штраф за порожнини, кінець, тай-брейк.
- [RulesPal: Tetris Link rulebook](https://rulespal.com/tetris-link/rulebook) — форми L/J, O, S/Z, T, I; кольори; сальдо ходу; «правила однакові для 2 і 3 гравців».
- [UltraBoardGames: Tetris Link](https://www.ultraboardgames.com/tetris-link/index.php) — 2011, 2–4 гравці, Asmodee / Ideal / John Adams Toys, дизайнер не вказаний, Tetris Link Travel.
- YouTube: пошук «Tetris Link board game».

## Непевне
- (?) Ширина й висота вежі — у правилах не названо.
- (?) Правила на 4 гравців (команди?) — UBG/RulesPal описують лише 2 і 3 гравців, хоча коробка «2–4».
- (?) Чи можна віддзеркалювати фігуру (L↔J, S↔Z) — виводиться з того, що це «одна форма» і фігуру можна вкинути «в будь-якому напрямку»; явно не сказано.
- (?) Як саме «блокування» визначається механічно (оточення з усіх боків?) — сказано лише «surrounding an opponent's pieces».
- (?) Цифрової версії не знайшов; вікна гіпотетичні.
