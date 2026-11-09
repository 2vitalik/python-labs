---
title: Daedalian Opus
slug: daedalian-opus
aka: [ダイダリアンオーパス]
family: board-digital
also: [grid-platformer, pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1990
platforms: [Game Boy]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Daedalian_Opus", best: true, note: "36 пентоміно-пазлів, острови й мости, нова фігура за рівень, таймер, паролі-слова, ZEAL"}
  - {kind: other, url: "https://princewatercress.blogspot.com/2024/03/princewatercress-plays-daedalian-opus_0361009196.html", note: "лонгплей: мапа-хаб, керування (B — поворот, Select/Start — віддзеркалення), паролі всіх рівнів"}
  - {kind: other, url: "https://tasvideos.org/1230G", note: "TASVideos: найшвидші розвʼязки (з пошуку, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Daedalian+Opus+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [polyomino-placement, piece-rotate-flip, satisfy-constraints, completion-detection, cursor-place, sequential-levels, level-password, level-select, world-map, restart-level, game-screen, end-screen, +unlock-new-piece, +hub-walk-to-level, +unstoppable-level-timer]
proposes: ["+card:unlock-new-piece", "+card:hub-walk-to-level", "+card:unstoppable-level-timer", "+feature:password-word"]
author: opus
date: 2026-11-09
---

# Daedalian Opus — 36 пентоміно-пазлів на Game Boy: кожен розвʼязаний острів дає нову фігуру й міст до наступного

## Суть
Класичне «заповни фігуру пентоміно» як кампанія: у кожному рівні треба без дірок і накладань скласти задану форму (спершу прямокутники, далі — ракета, пістолет, збільшені пентоміно) з доступних фігур. Старт — з 3 фігур, після рівнів набір росте до всіх 12, а наприкінці додається 13-та — квадрат 2×2. Між пазлами — мапа-хаб: чоловічок іде до дверей наступного рівня, а розвʼязок будує міст до наступного острова. Таймер рівня не можна зупинити, доки пазл не розвʼязано.

## Поле і час
- Пазл: квадратна сітка з контуром-ціллю; фігури лежать поза контуром і переносяться курсором.
- Хаб: горизонтальна мапа островів, вигляд збоку; рух лише ліво/право і «вгору» у двері.
- Час: таймер рівня біжить від старту до розвʼязку (без поразки за час (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | — | клітина | рухається хрестовиною; бере й кладе фігуру |
| Пентоміно (12 видів) | piece | форма, орієнтація | поворот 90°, віддзеркалення по горизонталі й вертикалі |
| Квадрат 2×2 (тетроміно) | piece | — | 13-та фігура, лише в фінальному рівні |
| Контур-ціль | zone | форма | усі клітини мають бути вкриті рівно один раз |
| Чоловічок | player | — | ходить мапою між дверима рівнів |
| Двері рівня | gate | номер | вхід у пазл |
| Міст | static | — | зʼявляється після розвʼязку, веде на наступний острів |
| НЛО | neutral | — | показує пароль рівня на мапі |
| Фея на мосту | neutral | — | дає нову фігуру |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(a, piece)` → ТО `custom: «фігура «прилипає» до курсора»`.
- КОЛИ `input(b)` → ТО `rotate(piece, 90)`.
- КОЛИ `input(select|start)` → ТО `custom: «віддзеркалити фігуру по вертикалі / горизонталі»`.
- КОЛИ `input(a, cell)` → ЯКЩО `fits(piece, cells)` → ТО `place(cursor, piece)`; інакше `block`.
- КОЛИ `input(a+b)` → ТО `custom: «усі фігури повертаються на стартові місця»`.
- КОЛИ `level_start` → ТО `timer(start)` — зупинити не можна до кінця рівня.
- КОЛИ `all_constraints_met` → ТО `message(Good)`, `timer(stop)`, `spawn(bridge)`, `give(player, new_piece)`.
- КОЛИ `custom: «рівень пройдено»` → ТО `custom: «показати пароль — англійське слово з 4 літер»`.
- КОЛИ `input(up)` → ЯКЩО `occupied(here, door)` → ТО `window(game-screen)` — вхід у пазл.
- КОЛИ `input(password)` → ТО `custom: «старт з рівня за паролем»`; ЯКЩО `custom: «пароль = ZEAL»` → ТО `window(level-select)`.
- Перемога: 36 рівнів, фінал — квадрат 8×8 з 12 пентоміно + 2×2. Поразки нема. Рахунку нема — лише час.

## Керування і ввід
- Хрестовина — курсор (у пазлі) або хід чоловічка (на мапі); A — взяти/покласти; B — поворот; Select — віддзеркалення вертикально; Start — горизонтально; A+B — скинути всі фігури.
- Підказок нема.

## Вікна, меню, HUD
- `splash-screen` / титул: A показує керування (`help-window`).
- `level-password` — ввід 4-літерного слова.
- `world-map` → `map-window`: острови, двері, НЛО з паролем, міст.
- `game-screen`: контур-ціль, запас фігур поруч, курсор, таймер (`timer-elapsed`).
- `end-screen`: «Good», перегляд складеної фігури (A), далі (Start); фінал з паролем ZEAL.
- `level-select` — після ZEAL, будь-який з 36 рівнів.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: кожен рівень відкриває наступний і дає фігуру.
- Паролі-слова (+`password-word`): легко вгадати, бо це звичайні англійські слова.
- `restart-level` = A+B (скидання розкладки); можна повернутись у попередній рівень по мапі.

## Варіації й родичі
- База — пентоміно-пазли Голомба: див. [pentomino](pentomino.md) (дуель на 8×8); [ubongo](ubongo.md) (на швидкість); [blokus](blokus.md).
- Родичі-«кампанії» з набором фігур, що росте: Katamino (?).
- Осі: **набір фігур** (фіксований / росте з рівнями / з дублями); **ціль** (прямокутник / силует / 8×8 з дірою); **таймер** (нема / біжить / ліміт).

## Цікавинки для курсу
- Перевірка накладання й виходу за контур для поліоміно — 📎.
- 8 орієнтацій фігури (поворот + 2 віддзеркалення) — 🌱.
- Набір фігур, що росте від рівня до рівня — 🌱.
- Солвер пентоміно (DLX / backtracking) для перевірки рівня — 🥇.
- Мапа-хаб, де «вхід у двері» = вибір рівня — 📎.

## Мапа на каталог
- Є: `polyomino-placement` · `piece-rotate-flip` · `cursor-place` · `satisfy-constraints`, `completion-detection` · `sequential-levels` · `level-password` · `level-select` · `world-map` · `restart-level` · `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+unlock-new-piece` «Новий елемент у наборі за пройдений рівень» · levels/progression · 🌱.
  - `+hub-walk-to-level` «Хаб, де аватар іде до дверей рівня» · levels/progression · 📎.
  - `+unstoppable-level-timer` «Таймер рівня, що не ставиться на паузу» · game-logic/score · 🌱.

## Пропозиції до словників
- `+feature:password-word` — пароль рівня як словникове слово (Daedalian Opus) замість коду.
- `+card:unlock-new-piece`, `+card:hub-walk-to-level`, `+card:unstoppable-level-timer` — див. вище.

## Джерела
- ⭐ [Wikipedia: Daedalian Opus](https://en.wikipedia.org/wiki/Daedalian_Opus) — 36 рівнів, острови й мости, 3–4 фігури на старті до 12, 13-та 2×2 і 8×8 у фіналі, таймер без зупинки, паролі-слова, ZEAL.
- [PrinceWatercress: лонгплей](https://princewatercress.blogspot.com/2024/03/princewatercress-plays-daedalian-opus_0361009196.html) — мапа (ліво/право, вгору у двері), НЛО з паролем, фея з фігурою, усі кнопки, «Good», паролі.
- [TASVideos](https://tasvideos.org/1230G) — найшвидші розвʼязки (не відкривав).

## Непевне
- Сімʼя: ядро — пентоміно-упаковка (80 % часу), тому файл у `board-digital` поруч із [pentomino](pentomino.md); черга `grid-platformer` мала його через хаб.
- (?) Чи таймер обмежує (поразка за час) чи лише рахує; Wikipedia: «не можна зупинити».
- (?) Wikipedia: 36 рівнів, але 42 острови (за Jeux Video) — розбіжність.
- (?) Фінальний рівень і збільшені пентоміно в Wikipedia позначені «citation needed».
