---
title: Loopz
slug: loopz
aka: []
family: connect-rotate
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1990
platforms: [Atari ST, Amiga, DOS, C64, ZX Spectrum, Amstrad CPC, BBC Micro, Acorn Electron, Acorn Archimedes, NES, Game Boy, Lynx]
links:
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0014635/LoopzCollectionThe(EN).pdf", best: true, note: "мануал The Loopz Collection (1991): керування, Game A/B/C, життя, бонус-ігри, множник, ховрахи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Loopz", note: "фігури з прямих і кутів, три режими, порти, Super Loopz"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Loopz", note: "Ian Upton 1989, Super Loopz лише в Японії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Loopz+Audiogenic+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cursor-place, piece-rotate-flip, pipe-connectors, move-timer, player-death, extra-life-threshold, event-points, progress-acceleration, difficulty-levels, sequential-levels, mode-select, level-password, keyboard-controls, game-pause, main-menu, game-screen, status-panel, +loop-detection, +loop-clear, +all-clear-bonus, +bonus-stage, +remover-item, +restore-puzzle, +coverage-multiplier]
proposes: ["+window:bonus-round", "+ui:target-score", "+card:loop-clear", "+card:restore-puzzle", "+card:coverage-multiplier"]
author: opus
date: 2026-11-09
---

# Loopz — клади й крути відрізки колії на час; замкнена петля дає очки й зникає

## Суть
Гравцеві по одній видають випадкові фігури з відрізків колії: клітина з прямою, клітина з кутом 90° або сполучення кількох таких клітин. Фігуру можна рухати й обертати над полем і покласти будь-де, поки не вийшов час на фігуру; не встиг — мінус життя. Коли відрізки утворюють замкнену петлю, вона приносить очки й зникає. Більша й складніша петля дає набагато більше очок, але поле забивається незамкненими хвостами, які лише заважають.

## Поле і час
- Квадратна сітка клітин; кожна клітина або порожня, або містить відрізок колії з двома виходами (пряма чи кут). Розмір поля — (?).
- Real-time: на кожну фігуру є таймер; з рівнем час на фігуру скорочується, а петлі коштують дорожче.
- Шари: поле з покладеними відрізками + фігура, що «висить» під курсором до кладення.
- Видно все поле; гравітації нема, нічого не падає — Tetris-подібний тиск часу на статичному полі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітина | static | — | сюди можна покласти фігуру |
| Фігура (поточна) | tile | 1+ клітин; кожна — пряма або кут | рухається й обертається курсором; кладеться цілою |
| Пряма | tile | 1 або 3 клітини | 2 виходи на протилежних сторонах |
| Кут | tile | 1 клітина, поворот 90° | 2 виходи на сусідніх сторонах |
| Відрізок на полі | tile | 2 виходи | нерухомий; стає частиною петлі або лишається «хвостом» |
| Петля | zone | кількість клітин | замкнена ланка відрізків; рахується й зникає |
| Ховрах (gopher) | object | — | спецфігура Game A/B: покладена на незамкнену петлю стирає її |
| Готова петля (Game C) | static | N вийнятих відрізків | пазл-екран: дірки треба заповнити так, щоб відновити петлю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(piece, dir)` над полем.
- КОЛИ `input(rotate)` → ТО `rotate(piece, 90)`.
- КОЛИ `input(drop)` → ЯКЩО `free(cells_under_piece)` і `custom: «жоден відрізок не виводить колію за край поля»` → ТО `place(player, piece)`, `custom: «наступна випадкова фігура, таймер з початку»`; інакше `block` (?).
- КОЛИ `counter(piece_time, ==, 0)` → ЯКЩО `custom: «фігуру не покладено»` → ТО `lives(-1)`.
- КОЛИ `pattern(loop_closed)` → ТО `score(+n)` (росте з розміром і складністю петлі та з рівнем), `clear(loop)`, `counter(loops, +1)`.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля покриває все поле»` → ТО `score(+10000)` на рівні 0 … `score(+100000)` на рівні 9, `custom: «життя добираються до 3, якщо їх менше»`.
- КОЛИ `after(place)` → ТО `custom: «множник бонусу росте з кількістю покритих клітин, ×1…×10»`.
- Game A: КОЛИ `after(clear)` → ЯКЩО `count(track, ==, 0)` → ТО `score(+100…10000)` (за рівнем і множником), `multiplier(1)`.
- КОЛИ `counter(loops, ==, 25)` (кожні 25 петель, Game A/B) → ТО `lives(+1)` (не більше 10).
- Game B: КОЛИ `counter(loops, ==, 10)` (кожні 10 петель) → ТО `counter(level, +1)`: менше часу на фігуру, більше очок.
- КОЛИ `input(drop)` → ЯКЩО `custom: «фігура — ховрах»` і `occupied(cell, track)` → ТО `disappear(incomplete_loop)`; невикористаний ховрах без штрафу.
- Game B: КОЛИ `after(clear)` → ЯКЩО `count(track, ==, 0)` → ТО `window(bonus-round)` — бонус-гра 1.
- Бонус-гра 1: КОЛИ `pattern(loop_closed)` → ТО `score(+n)`, `multiplier(k)`, `custom: «петля НЕ зникає»`.
- Бонус-гра 1: КОЛИ `counter(piece_time, ==, 0)` → ТО `custom: «бонус-гра закінчується, очки додаються, гра йде далі»`.
- Game B: КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «очки за цю петлю > цільового числа над таймером»` → ТО `window(bonus-round)` — бонус-гра 2: випадковий пазл із Game C.
- Бонус-гра 2: КОЛИ `custom: «пазл розвʼязано»` → ТО `counter(level, -1)`, `score(+n)`.
- Game C: КОЛИ `level_start` → ТО `custom: «на полі готова петля, з якої вийнято кілька відрізків; вони приходять як фігури»`.
- Game C: КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля = оригінал»` → ТО `next_level`.
- Game C: КОЛИ `custom: «петлю не відновлено»` → ТО `lives(-1)` (що саме вважається провалом — ?).
- Game C: КОЛИ `counter(screens, ==, 5)` (кожні 5 екранів) → ТО `message(password)`.
- Game C: КОЛИ `counter(screens, ==, 10)` (кожні 10 екранів) → ТО `lives(+1)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: нема (Game A/B — рахунок до кінця життів; Game C — пройти 50 екранів). · Поразка: скінчились життя (3 на старті). · Рахунок: петлі (надлінійно від розміру), петля на все поле, бонус чистого поля × множник, бонус-ігри.

## Керування і ввід
- Джойстик: рух фігури над полем; вогонь + вправо — повернути, вогонь + вліво — покласти.
- ZX Spectrum: курсорні клавіші + Space (повернути) + Enter (покласти) або Q-A-O-P + будь-яка клавіша нижнього ряду Z…M (повернути) + верхнього ряду 1…5 (покласти); H — пауза, R у паузі — нова гра.
- Amstrad: курсорні + «.» (повернути) + Enter (покласти) або чотири літерні клавіші + Caps Lock / Tab; P — пауза, Esc у паузі — перервати гру. C64 — лише джойстик; клавіша Commodore — пауза, Run/Stop — перервати.
- Двоє: Game A — одночасно, окремі рахунки й навіть різні рівні складності; Game B — по черзі кладуть фігури, рахунок спільний.

## Вікна, меню, HUD
- `main-menu` (`match-setup`): список опцій — гра A/B/C, рівень, гравці, керування; вгору-вниз — пункт, вліво-вправо — значення; Space — старт.
- `level-password` (Game C): ввести пароль, щоб почати з потрібного екрана.
- `game-screen`: поле, фігура під курсором; HUD — `score`, `timer-countdown` фігури, `lives` (над ромбом ліворуч унизу), `multiplier` (над ромбом праворуч унизу; не в 2P Game A), `level-number`, ціль для бонус-гри 2 над таймером (Game B).
- `custom-window` бонус-гра 1 і бонус-гра 2 (Game B).
- `pause-menu`: пауза з виходом / новою грою.
- `end-screen` game over; таблиця рекордів — (?).
- Переходи: main-menu → (Game C) level-password → game-screen → (чисте поле / велика петля) бонус-гра → game-screen → (0 життів) game over → main-menu.

## Фічі поза полем
- `mode-select`: Game A (обраний рівень 0–9, рівень сталий), Game B (рівень росте кожні 10 петель, дві бонус-гри), Game C (50 пазл-екранів).
- `difficulty-presets`: рівні 0–9 у Game A; вищий — менше часу, більше очок.
- `levels-sequential` + `level-password` (Game C, пароль кожні 5 екранів).
- `local-multiplayer`: 2P одночасно (A) і `mode-coop` по черзі зі спільним рахунком (B).
- Життя: старт 3; +1 за кожні 25 петель (A/B) або 10 екранів (C), максимум 10.
- `pause`.

## Варіації й родичі
- Super Loopz (SNES, Imagineer, 1994 — лише Японія; Amiga CD32 від Audiogenic); порт для Atari Lynx вийшов лише 2004 року (Songbird Productions); прототипи аркадного автомата Capcom і призового автомата Barcrest не вийшли.
- **Осі варіацій**:
  - звідки фігура: випадкова черга з поворотом (Loopz) / черга без повороту (`pipe-mania`) / обертання вже покладених плиток (`infinity-loop`) / малювання шляху (`flow-free`);
  - що є метою: замкнена петля зникає (Loopz) / довжина шляху від джерела (`pipe-mania`) / рівно одна петля як обмеження без часу (`pencil-logic/slitherlink` — інша гра, не Loopz);
  - що робить петля: зникає (A/B) / лишається (бонус-гра 1);
  - тиск: таймер на фігуру (Loopz) / потік, що наздоганяє (`pipe-mania`).
- Родичі: `pipe-mania` (труби з черги), `rocket-mania` (згорілий шлях зникає), `tantrix` і `trax` (петля як ціль на плитках), `atomino` (замкнена структура зникає, черга з переповненням), Tetris (таймер + очищення).

## Цікавинки для курсу
- Виявлення замкненої петлі після кожного кладення: обхід портами від щойно покладеної клітини, петля = повернулись у старт без відкритих кінців — 📎.
- Фігури з кількох клітин з поворотом і перевіркою «колія не виходить за край» — 📎.
- Ховрах: стерти незамкнену ланку (компоненту звʼязності по портах) — 📎.
- Множник ×1–×10 за покриттям + бонус чистого поля + надлінійні очки за великі петлі — 🌱.
- Game C: пазл «вийняти N відрізків з готової петлі» з перевіркою відновлення й паролями — 🥉.
- Бонус-гра, де петлі не зникають, як окремий режим з тими самими правилами — 🌱.
- 2P: одночасно на окремих рахунках vs по черзі зі спільним рахунком — 🥉.

## Мапа на каталог
- Є: `cursor-place` ↔ кладення фігури · `piece-rotate-flip` ↔ поворот перед кладенням · `pipe-connectors` ↔ пряма/кут з двома виходами · `move-timer` ↔ час на фігуру · `player-death` + `extra-life-threshold` ↔ життя, +1 за 25 петель · `event-points` ↔ петля/повне поле/бонус · `progress-acceleration` + `difficulty-levels` ↔ рівні 0–9 · `sequential-levels` + `level-password` ↔ Game C · `mode-select` ↔ A/B/C · `keyboard-controls`, `game-pause`, `main-menu`, `game-screen`, `status-panel`.
- **Нема** → пропозиції карток:
  - `+loop-detection` (є в корпусі) — виявлення циклу в графі портів.
  - `+loop-clear` «Замкнена петля зникає з очками за розмір» · entities/interact · 📎 · слот {keep_in_bonus: bool}.
  - `+all-clear-bonus` (є в корпусі) — бонус за чисте поле.
  - `+bonus-stage` (є в корпусі) — дві бонус-гри Game B.
  - `+remover-item` (є в корпусі) — ховрах стирає незамкнену ланку.
  - `+restore-puzzle` «Відновити вийняті частини готової конструкції» · levels/generation · 🥉 — Game C, бонус-гра 2.
  - `+coverage-multiplier` «Множник росте з покриттям поля, скидається при очищенні» · game-logic/score · 🌱.

## Пропозиції до словників
- `+window:bonus-round` (повтор Pipe Mania) — бонус-гра з іншими правилами між звичайною грою.
- `+ui:target-score` — поріг очок за одну петлю, що відкриває бонус-гру 2.
- `+card:loop-clear`, `+card:restore-puzzle`, `+card:coverage-multiplier` — див. «Мапа на каталог».

## Джерела
- ⭐ [Мануал The Loopz Collection (1991, PDF)](https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0014635/LoopzCollectionThe(EN).pdf) — повні правила Loopz: керування для C64/Spectrum/Amstrad, Game A/B/C, рівні 0–9, життя, бонуси й множник, бонус-ігри 1 і 2, ховрахи, поради (прямі 1 і 3 клітини).
- [Wikipedia EN: Loopz](https://en.wikipedia.org/wiki/Loopz) — форма фігур, «лінії не за край», три режими, порти, Super Loopz, прототипи.
- [Wikipedia DE: Loopz](https://de.wikipedia.org/wiki/Loopz) — автор Ian Upton (1989), Super Loopz лише в Японії, оцінки преси.
- YouTube: пошук «Loopz Audiogenic gameplay».

## Непевне
- (?) Розмір поля в клітинах, набір форм багатоклітинних фігур і чи показують наступну фігуру — у джерелах нема.
- (?) Чи можна класти фігуру так, що її виходи не збігаються з сусідніми відрізками (з тексту «клади будь-де» — так), і що саме блокує кладення: зайняті клітини та вихід колії за край (Wikipedia, без джерела).
- (?) Що відбувається з фігурою, коли вийшов час: зникає, а життя — мінус (мануал), чи кладеться автоматично — не сказано.
- (?) Як саме виглядає 2P Game A: одне поле на двох чи два поля — мануал каже лише «одночасно, окремі рахунки».
- (?) Game C: що вважається провалом (неправильний відрізок чи вихід часу) — мануал: «if you fail you lose a life».
- (?) Таблиця рекордів і формула очок за петлю — не описані.
- Плутанина черги: автоматика звʼязала Loopz з `pencil-logic/slitherlink` — це різні ігри (Slitherlink — паперовий пазл без часу).
