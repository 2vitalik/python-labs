---
title: Quadrax
slug: quadrax
aka: [Quadrax I, Kvadrax]
family: grid-platformer
also: [thinky, push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1994
platforms: [ZX Spectrum, DOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quadrax", best: true, note: "суть: двоє мусять зійтися на цільовій платформі; камені, важелі, двері, ліфти; смерть від пастки, падіння, каменя; DOS — телепорти й магнітні блоки; версії й фан-сиквели"}
  - {kind: other, url: "https://cs.wikipedia.org/wiki/Quadrax", note: "чеська Вікіпедія: режими 1 гравець / кооп, без ліміту часу, 50 і 100 рівнів, автори"}
  - {kind: other, url: "https://www.spectrumcomputing.co.uk/reviews/9403", note: "огляд ZX Spectrum: ходять і лізуть, не стрибають; клавіша перемикання; біла платформа зі стрілками; важелі, двері, підлоги, телепорти, ліфти"}
  - {kind: other, url: "https://retro-replay.com/db/dos/quadrax", note: "огляд DOS-версії: штовхання й залізання на камені, пастки, 100 рівнів"}
  - {kind: official, url: "https://quadrax.cz/", note: "сайт серії (при перевірці — лише логотип)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Quadrax+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [party-switch, push-object, gravity-fall, button-toggle, carrier-platform, teleport, all-on-targets, environment-death, player-death, impassable-cells, sequential-levels, game-screen, +step-climb-1, +fall-damage-by-height, +crush-by-falling-stone, +coop-split-control, +magnet-block, +hidden-lever-link]
proposes: ["+trigger:landed", "+card:coop-split-control", "+card:hidden-lever-link"]
author: opus
date: 2026-11-09
---

# Quadrax — двоє археологів допомагають одне одному каменями, важелями й ліфтами, щоб обоє стали на цільову платформу

## Суть
Кооперативний пазл-платформер з ZX Spectrum: два персонажі, кожен рухається окремо (одним гравцем по черзі або двома одночасно). Обоє вміють ходити й лазити, але не стрибають. Один тримає важіль чи стоїть на ліфті, другий проходить; камені штовхають і використовують як сходинки. Рівень пройдено, коли **обидва** стоять на білій платформі зі стрілками. Ліміту часу нема, але один неправильний крок може зробити рівень непрохідним.

## Поле і час
- Один статичний екран збоку на рівень: платформи, стіни, блоки, драбини (?).
- Real-time без таймера: персонажі ходять анімовано, механізми рухаються, але час не тисне.
- Гравітація: персонажі й камені падають; падіння з великої висоти вбиває; камінь, що впав на персонажа, розчавлює.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж 1, 2 | player | активний / ні | ходить, лізе (на камінь, уступ); штовхає камені; не стрибає |
| Кам'яний блок | object | — | штовхається; падає, якщо нема опори; на нього залазять |
| Стіна / платформа | static | — | непрохідна; опора |
| Важіль (switch) | switch | вкл / викл | перемикає повʼязані двері, підлоги, ліфти; звʼязок іноді треба запамʼятати |
| Розсувні двері | gate | відкриті / закриті | керуються важелем |
| Висувна підлога | gate | є / нема | керується важелем |
| Ліфт | platform | — | везе персонажа або камінь; керується важелем |
| Телепорт | static | — | переносить персонажа (DOS-версія; в огляді Spectrum теж згадано) |
| Магнітний блок | object | — | DOS-версія (?) — поведінка в джерелах не описана |
| Пастка / яма з шипами | hazard | — | смерть персонажа |
| Цільова платформа | static | біла, стрілки | обидва на ній — рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(switch_character)` → ТО `custom: «активним стає інший персонаж»`.
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(active, dir)`.
- КОЛИ `blocked(active)` → ЯКЩО `occupied(next, stone)` і `free(cell_behind)` → ТО `push(stone)`; інакше `block`.
- КОЛИ `input(up)` → ЯКЩО `custom: «перед персонажем камінь або уступ висотою 1»` → ТО `custom: «залізти»`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)` — для персонажів і каменів.
- КОЛИ `custom: «персонаж приземлився з великої висоти»` → ТО `lose` рівня.
- КОЛИ `contact(falling_stone, character)` → ТО `lose` рівня.
- КОЛИ `contact(character, trap)` → ТО `lose` рівня.
- КОЛИ `input(use)` → ЯКЩО `occupied(here, lever)` → ТО `set_state(lever, toggled)`, `custom: «повʼязані двері/підлога/ліфт міняють стан»`.
- КОЛИ `contact(a, lift)` → ЯКЩО `custom: «стоїть на ліфті»` → ТО `carry(lift, a)`.
- КОЛИ `enter(character, teleport)` → ТО `teleport(character)`.
- КОЛИ `all_on(character, target)` → ТО `win`, `next_level`.
- Перемога: обидва на цілі. Поразка: смерть будь-кого → рестарт рівня. Рахунок: нема.

## Керування і ввід
- Клавіші руху для активного персонажа; окрема клавіша (налаштовна) — перемкнути персонажа.
- Кооп: два гравці керують кожен своїм персонажем одночасно.
- Дія з важелем — клавіша дії (?).

## Вікна, меню, HUD
- `main-menu` (?): 1 гравець / 2 гравці.
- `game-screen`: статичний екран рівня; позначка активного персонажа (?).
- `level-password` (?) — вхід на рівень кодом (не підтверджено).
- DOS: анімовані вставки сюжету (`dialogue-window`).

## Фічі поза полем
- `levels-sequential`: 50 рівнів (Spectrum), 100 (DOS); складність зростає, нові елементи вводяться поодинці.
- `mode-coop`: два гравці на одній клавіатурі.
- Без ліміту часу; рестарт рівня після помилки.

## Варіації й родичі
- Версії: ZX Spectrum (1994, David Durčák і Marián Ferko, Ultrasoft), DOS (1995/1996, Cauldron) з телепортами й магнітними блоками; фан-сиквели Josefa Kreutzera (Return to Quadrax, Quadrax III 2000, IV 2008 і далі) — третій персонаж, скарби для збору, приховані пастки, що стріляють.
- Натхнення: Sokoban і Thunderbirds.
- Родичі в корпусі: [catrap](catrap.md) (два персонажі з перемиканням), [head-over-heels](head-over-heels.md) (два героя з різними здібностями), [block-dude](block-dude.md) (сходинка з блока, без стрибка), [lode-runner](lode-runner.md).
- Осі (вісь `actors: party` уже в `classes.md`): **кількість аватарів** (2 / 3); **розподіл ролей** (однакові / різні вміння); **керування** (по черзі одним гравцем / одночасно двома).

## Цікавинки для курсу
- Двоє аватарів з перемиканням і спільна ціль «обоє на цілі» — 📎.
- Штовхання каменя з гравітацією: камінь падає в яму й стає містком/сходинкою — 📎.
- Важелі з неочевидним звʼязком «важіль → механізм» (таблиця звʼязків рівня) — 🌱.
- Смерть від висоти й від каменя згори — порядок обробки падіння — 📎.
- Кооп: два гравці одночасно на одному полі — 🥉 (одночасний ввід, конфлікти клітин).

## Мапа на каталог
- Є: `party-switch` · `push-object` · `gravity-fall` · `button-toggle` (важелі) · `carrier-platform` (ліфти) · `teleport` · `all-on-targets` (обидва на цілі) · `environment-death` · `player-death` · `impassable-cells` · `sequential-levels` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+coop-split-control` «Два гравці керують двома аватарами одночасно; соло — перемикання» · entities/move · 🥉.
  - `+hidden-lever-link` «Звʼязок важіль→механізм не показано, гравець його відкриває» · entities/interact · 🌱.
  - `+step-climb-1`, `+fall-damage-by-height`, `+crush-by-falling-stone`, `+magnet-block` — див. правила.

## Пропозиції до словників
- `+trigger:landed` — приземлення після падіння з висотою (смерть від висоти).
- `+card:coop-split-control`, `+card:hidden-lever-link`.

## Джерела
- ⭐ [Wikipedia: Quadrax](https://en.wikipedia.org/wiki/Quadrax) — правила, смерті, DOS-нововведення, версії й сиквели.
- [Wikipedia CS: Quadrax](https://cs.wikipedia.org/wiki/Quadrax) — режими, 50/100 рівнів, автори, «немає ліміту часу».
- [Spectrum Computing: огляд](https://www.spectrumcomputing.co.uk/reviews/9403) — ходять і лізуть без стрибка, клавіша перемикання, біла платформа зі стрілками, важелі-«тест памʼяті».
- [Retro Replay: Quadrax (DOS)](https://retro-replay.com/db/dos/quadrax) — штовхання й залізання на камені, пастки, 100 рівнів.

## Непевне
- (?) Магнітні блоки DOS-версії: що притягують і як рухаються — не знайшов опису.
- (?) Чи можна нести камінь, чи лише штовхати; чи штовхають удвох важкий камінь.
- (?) Паролі рівнів / збереження; Retro Replay згадує «save-and-undo» — не підтверджено іншими джерелами.
- (?) Чи є драбини, чи «лазіння» — лише залізання на блок висотою 1.
- (?) Рік: Wikipedia EN — інфобокс 1995 і текст 1994 (Spectrum); DOS — 1995 або 1996.
