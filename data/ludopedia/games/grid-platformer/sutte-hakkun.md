---
title: Sutte Hakkun
slug: sutte-hakkun
aka: [すってはっくん, Suttehakkun, Сутте Хаккун]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1997
platforms: [Satellaview (SFC), Nintendo Power (SFC), Super Famicom, Wii Virtual Console, Wii U Virtual Console, Nintendo Switch Online]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/すってはっくん", best: true, note: "повні правила: що всмоктує Хаккун, кольори червоний/синій/жовтий → вертикаль/горизонталь/діагональ, пляшки, SW, Маккуни, Роккун, Букун, Цукун, скло, односторонні підлоги, очки, підказки, острови, версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sutte_Hakkun", note: "EN: три дії, осколки веселки, шипи й ями, без таймера й життів, кількість рівнів у версіях, дати"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sutte+Hakkun+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, collect-all, item-pickup, environment-death, one-way-cell, carrier-platform, button-toggle, enemy-patrol, turn-when-blocked, push-object, cell-transform, stick-together, checkpoint, restart-level, level-select, world-map, map-window, pause-menu, event-points, level-unlock, score-records, game-screen, +inhale-and-place, +color-injection-motion, +recolor-all-switch, +fusion-weight, +break-glass-by-drop, +points-decay-per-move, +hint-penalty, +secret-race-unlock, +fake-object]
proposes: ["+feature:hint-penalty", "+card:inhale-and-place", "+card:color-injection-motion", "+card:recolor-all-switch", "+card:fusion-weight", "+card:points-decay-per-move"]
author: opus
date: 2026-11-09
---

# Sutte Hakkun — всмоктати колір із пляшки, впорснути в блок, і блок стає ліфтом: червоний вгору-вниз, синій убік, жовтий навскоси

## Суть
Бічний пазл-платформер Indieszero і Nintendo R&D2 у дусі Lode Runner: прозорий птах Хаккун має зібрати всі осколки веселки в рівні. Він бігає, стрибає і **дзьобом усмоктує та випльовує**: прозорі блоки (і ставить їх будь-де, навіть у повітрі чи в стіні), фарбу з пляшок і деяких істот. Фарба, впорснута в блок, робить із нього ліфт із напрямом за кольором — так будується шлях до осколків. Ворогів, таймера, життів і game over нема: помилка — лише рестарт від початку або від швидкого збереження.

## Поле і час
- Рівень — бічна квадратна сітка блоків; помітна частина рівнів, схоже, вміщується в один екран (?).
- Час іде безперервно: ліфти й Маккуни рухаються самі, гравітація діє на Хаккуна й обʼєкти; ліміту часу нема (крім бонус-рівнів Satellaview).
- Шари: стіни й тло · односторонні підлоги, скло, SW-плити · прозорі блоки (можуть стояти навіть усередині стін) · пляшки · істоти й осколки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Хаккун | player | колір у дзьобі / блок у дзьобі / злитий з Роккуном | ходить, стрибає, усмоктує й випльовує; падає без опори |
| Прозорий блок | object | колір: нема / червоний / синій / жовтий | на ньому стоять; крізь нього проходять збоку й знизу; усмоктується й ставиться будь-де; з кольором — ліфт, доки колір не висмокчуть |
| Пляшка (ツボ) | static | колір R/B/Y | дає свій колір нескінченно; не рухається |
| SW-плита | switch | — | коли на неї впав Хаккун чи інша істота — усі пляшки рівня міняють колір разом |
| Осколок веселки | pickup | кількість на рівні | зібрати всі = рівень пройдено |
| Червоний Маккун | neutral | — | стоїть, мʼякий; Хаккун сплющує його й стрибає вище (батут) |
| Синій Маккун | neutral | — | ходить туди-сюди, розвертається біля стіни чи ями |
| Жовтий Маккун | neutral | — | раз у раз присідає на місці — натискає SW з періодом |
| Маккун (будь-який) | neutral | — | прозорий, шипи йому не шкодять; приймає впорснутий колір (?) |
| Роккун (живий камінь) | object | — | усмоктується: Хаккун зливається з ним — нижчий стрибок, повільніший; єдиний, хто бʼє скло |
| Скло | terrain | ціле / розбите | не реагує на звичайного Хаккуна; ламається від падіння з висоти злитого з Роккуном або від Роккуна, скинутого згори |
| Одностороння підлога | terrain | стрілка вгору/вниз | не пускає проти стрілки |
| Букун (фальшивий блок) | object | — | не всмоктується й не фарбується; лише штовхається й тримає |
| Цукун (фальшива пляшка) | neutral | — | реагує на дотик чи спробу всмоктати; заважає (?) |
| Фіолетовий Маккун | neutral | секретний | зʼявляється, якщо довго штовхати стіну; перегнати його до цілі праворуч — відкрити «відповідь» |
| Яма · шипи | hazard | — | падіння/дотик = промах, рестарт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(hakkun, dir)`, `counter(points, -1)` (?); КОЛИ `input(jump)` → ТО `custom: «стрибок»`.
- КОЛИ `after(move)` → ЯКЩО `not supported(a)` → ТО `fall(a)`; блок тримає Хаккуна згори, але пропускає збоку й знизу.
- КОЛИ `input(suck)` → ЯКЩО `occupied(front, block)` і `not has(hakkun, block)` → ТО `pickup(hakkun, block)`.
- КОЛИ `input(spit)` → ЯКЩО `has(hakkun, block)` → ТО `place(hakkun, block)` — у будь-яку клітину, навіть у повітря чи в стіну.
- КОЛИ `input(suck)` → ЯКЩО `occupied(front, bottle)` → ТО `give(hakkun, color)` — пляшка не вичерпується.
- КОЛИ `input(spit)` → ЯКЩО `has(hakkun, color)` і `occupied(front, block)` → ТО `set_state(block, color)`, `take(hakkun, color)`.
- КОЛИ `tick` → ЯКЩО `state(block, red)` → ТО `move(block, up|down)`; ЯКЩО `state(block, blue)` → ТО `move(block, left|right)`; ЯКЩО `state(block, yellow)` → ТО `move(block, diagonal)`; що буває на упорі — `bounce` (?).
- КОЛИ `input(suck)` → ЯКЩО `state(block, color)` → ТО `clear_state(block, color)`, `give(hakkun, color)` — ліфт зупиняється.
- КОЛИ `enter(a, block)` (стоїть на ліфті) → ТО `custom: «їде разом з блоком»`.
- КОЛИ `enter(hakkun|makkun|rokkun, switch)` (падіння згори) → ТО `custom: «усі пляшки рівня змінюють колір одночасно»`.
- КОЛИ `enter(hakkun, red_makkun)` → ТО `custom: «Маккун сплющується, наступний стрибок вищий»`.
- КОЛИ `tick` → ТО `move(blue_makkun, dir)`; КОЛИ `blocked(blue_makkun)` або `custom: «попереду яма»` → ТО `bounce(blue_makkun)`.
- КОЛИ `timer(every)` → ТО `custom: «жовтий Маккун присідає»` — якщо стоїть на SW, перемикає кольори пляшок.
- КОЛИ `input(suck)` → ЯКЩО `occupied(front, rokkun)` → ТО `attach(hakkun, rokkun)`, `speed(hakkun, -1)`, `custom: «стрибок нижчий»`.
- КОЛИ `enter(hakkun, glass)` → ЯКЩО `state(hakkun, merged)` і `custom: «падав з висоти»` → ТО `disappear(glass)`; так само для Роккуна, скинутого згори.
- КОЛИ `input(suck|spit)` → ЯКЩО `occupied(front, bukun)` → ТО `block`; КОЛИ `contact(hakkun, bukun)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `enter(hakkun, one_way)` → ЯКЩО `not moving(hakkun, arrow_dir)` → ТО `block`.
- КОЛИ `contact(hakkun, shard)` → ТО `pickup`; КОЛИ `all_gone(shard)` → ТО `win`, `score(+points_left)`.
- КОЛИ `enter(hakkun, hole|spike)` → ТО `restart` — від старту рівня або від останнього швидкого збереження.
- КОЛИ `input(quick_save)` → ТО `checkpoint`, `counter(points, -n)` (?).
- КОЛИ `input(hint)` → ТО `window(hints-window)`, `custom: «рівень назавжди позначено, його очки ділитимуться навпіл»`.
- Перемога: зібрано всі осколки веселки. · Поразка: нема — лише рестарт. · Рахунок: у кожного рівня запас очок, що тане з кожним рухом і швидким збереженням; нуль не зупиняє гру; залишок додається до суми.

## Керування і ввід
- Хрестовина — біг ліво/право; кнопка стрибка; кнопка «усмоктати/виплюнути» — одна дія за станом дзьоба (?).
- Швидке збереження — окрема дія (?); Start — меню з підказкою (у товарній версії) і, після секрету, з «відповіддю».
- На Wii U — перепризначення клавіш.

## Вікна, меню, HUD
- `splash-screen` → `map-window`: чотири острови (しあわせ島, のんびり島, ほんわか島, どきどき火山島), хатинка Хаккуна, музична хатинка.
- `level-select` — рівні острова з позначками «підказку переглянуто».
- `game-screen` — рівень; HUD — запас очок рівня, що тане (`score`), осколки (?).
- `pause-menu` (Start): підказка (`hints-window`), «відповідь» (`solutions-window`) після секрету, вихід (?).
- `mode-select` — тайм-атака після 100 рівнів (цільовий і найкращий час на рівень).
- `custom-window` — перегони з фіолетовим Маккуном.
- `leaderboard` — рейтинги Satellaview (повтори топ-1–5 і 100-го місця) (цифрова трансляція).
- Переходи: map-window → level-select → game-screen → (усі осколки) → level-select; 100 рівнів → тайм-атака; поріг очок → Extra.

## Фічі поза полем
- `world-map`: 100 рівнів на 4 островах (товарна версія); Extra — 10 рівнів після 100 рівнів і порогу очок, без тайм-атаки й підказок.
- `hint` і `show-solution` з **штрафом**: переглянута підказка назавжди ділить очки рівня навпіл; часті підказки міняють текст на екрані збереження.
- `mode-time-attack` після проходження 100 рівнів.
- `snapshots`-подібне швидке збереження всередині рівня, що коштує очок; `restart-level` після промаху.
- Satellaview: бонус-рівень після кожних 10 — з лімітом часу й умовами (усі блоки в білій рамці / пофарбувати всі блоки) → perfect-бонус; `leaderboard-online` (конкурс рейтингів).
- `remap-controls` (Wii U), `save-progress` (картридж) (?).

## Варіації й родичі
- Версії: Event Version Satellaview (1997, 50+5 бонус + 10 тренувальних) → Nintendo Power (1998) → BS Version 2 (1998, 30+3) → '98 Winter Event (1998) → картридж (1999, 100 рівнів + Extra) → Wii VC (2010), Wii U VC (2015), Switch Online (2025, перший реліз поза Японією).
- Родичі: Lode Runner (бічна пазл-кімната, «зібрати все»), Kirby (усмоктати й виплюнути), Solomon's Key (ставити блоки), Toki Tori (ставити міст/блок), Blocks That Matter (носити блоки), Baba Is You (властивість, яку переносиш з обʼєкта на обʼєкт).
- Осі варіацій:
  - **як гравець ставить опору**: створити з нічого (Solomon's Key) / перенести наявний блок (Sutte Hakkun, Block Dude) / зламати й зсунути (Popils).
  - **що задає рух платформи**: фіксовано рівнем / колір-властивість, яку переносить гравець (Sutte Hakkun) / перемикач.
  - **ціна помилки**: життя / рестарт без штрафу / очки, що тануть (Sutte Hakkun).

## Цікавинки для курсу
- Колір як переносна властивість: блок = дані {color}, ліфт рухається за таблицею «колір → вектор», висмоктування знімає стан — 📎.
- Дзьоб-інвентар на один предмет: усмоктати блок/колір/камінь, виплюнути в будь-яку клітину — 📎.
- SW-плита, що одночасно перефарбовує всі пляшки, і жовтий Маккун як «таймер» для неї — 🥉 (глобальна подія + періодичний актор).
- Злиття з Роккуном: зміна параметрів руху і нове вміння (бити скло падінням з висоти) — 🥉.
- Очки, що тануть від кожного руху, і штраф ×½ за підказку, записаний у сейв назавжди — 🌱.
- Платформа-ліфт, що везе того, хто стоїть, і пропускає збоку/знизу (one-way platform) — 🥉.
- Розвʼязувач рівня (BFS по станах: позиція, дзьоб, кольори блоків, позиції ліфтів) — 👑 (стани з безперервним рухом — дорого).

## Мапа на каталог
- Є: `move-by-input` + `gravity-fall` ↔ біг і падіння; `collect-all` + `item-pickup` ↔ осколки; `environment-death` ↔ ями й шипи (промах); `one-way-cell` ↔ односторонні підлоги; `carrier-platform` ↔ кольоровий блок везе Хаккуна; `button-toggle` ↔ SW; `enemy-patrol` + `turn-when-blocked` ↔ синій Маккун; `push-object` ↔ Букун; `cell-transform` ↔ скло → прохід; `stick-together` ↔ злиття з Роккуном; `checkpoint` ↔ швидке збереження; `restart-level`; `level-select` + `world-map` + `map-window` ↔ острови; `pause-menu` ↔ Start-меню; `event-points` ↔ очки рівня; `level-unlock` ↔ Extra і тайм-атака; `score-records` ↔ рейтинги.
- **Нема** → пропозиції карток:
  - `+inhale-and-place` «Усмоктати обʼєкт і поставити будь-де» · entities/interact · 📎 · слот {targets: block|color|creature}.
  - `+color-injection-motion` «Колір задає вектор руху блока» · entities/state · 📎 · слот {table: color → dir}.
  - `+recolor-all-switch` «Плита перефарбовує всі джерела кольору» · entities/interact · 📎.
  - `+fusion-weight` «Злиття з важким: нижчий стрибок, нова сила» · entities/state · 🥉.
  - `+break-glass-by-drop` «Скло ламається від важкого падіння з висоти» · entities/interact · 🌱.
  - `+points-decay-per-move` «Очки рівня тануть з кожним рухом» · game-logic/score · 🌱.
  - `+hint-penalty` «Підказка назавжди зменшує нагороду» · game-logic/score · 🌱.
  - `+secret-race-unlock` «Секретні перегони відкривають функцію» · levels/progression · 📎.
  - `+fake-object` «Обʼєкт-двійник, що не підкоряється дії» · entities/interact · 🌱 — Букун і Цукун.

## Пропозиції до словників
- `+feature:hint-penalty` — переглянута підказка назавжди зменшує очки рівня (у `features.md` є лише `hint` / `show-solution`).
- `+card:inhale-and-place`, `+card:color-injection-motion`, `+card:recolor-all-switch`, `+card:fusion-weight`, `+card:points-decay-per-move` — див. вище.
- Наявні слова, вжиті без пропозиції: `pickup`, `place`, `give`, `take`, `set_state`, `clear_state`, `attach`, `speed`, `checkpoint`, `supported`, `moving`, `neutral`, `hints-window`, `solutions-window`, `map-window`, `snapshots`, `mode-time-attack`, `leaderboard-online`.

## Джерела
- ⭐ [Wikipedia JA: すってはっくん](https://ja.wikipedia.org/wiki/すってはっくん) — блоки (стоїш зверху, проходиш збоку й знизу, ставиш будь-де), кольори (червоний — вертикаль, синій — горизонталь, жовтий — діагональ, до висмоктування), пляшки, SW, Маккуни трьох кольорів, Роккун, Букун, Цукун, скло, односторонні підлоги, очки й швидке збереження, підказки ×½, фіолетовий Маккун, острови, тайм-атака, Extra, бонус-рівні й рейтинги Satellaview.
- [Wikipedia: Sutte Hakkun](https://en.wikipedia.org/wiki/Sutte_Hakkun) — три дії, осколки веселки, шипи і ями, нема таймера/життів/game over, кількості рівнів у версіях, дати, розробники.
- YouTube: пошук «Sutte Hakkun gameplay».

## Непевне
- (?) Що робить кольоровий блок на упорі (розвертається чи стоїть) і в який бік рушає спершу; JA-вікі лише «рухається, доки не висмокчеш колір».
- (?) Скільки предметів тримає дзьоб (один блок або один колір?) і чи можна нести блок і колір разом.
- (?) Розкладка кнопок і як викликати швидке збереження; скільки очок знімає рух і збереження; стартовий запас очок.
- (?) Що робить впорснутий у Маккуна колір (міняє його тип?) і як саме заважає Цукун.
- (?) Чи рівні скролять, чи вміщуються в один екран; наявність окремого екрана збереження.
