---
title: Flip and Flop
slug: flip-and-flop
aka: [Flip & Flop]
family: maze-arcade
also: []
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1983
platforms: [Atari 8-bit, Atari 5200, C64]
links:
  - {kind: other, url: "https://www.atarimania.com/games/atari-400-800-xl-xe-games-flip-and-flop-2021", best: true, note: "скани мануалу (правила, очки, рівні, липкі клітини, клавіші) + огляд Electronic Games 1984"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flip_and_Flop", note: "суть, герої, переслідувачі, липкі клітини, 13-й рівень — максимальне поле"}
  - {kind: other, url: "https://www.atarimagazines.com/compute/issue43/253_2_NEWS_PRODUCTS_Games_For_Atari_64_VIC_And_Color_Computer.php", note: "COMPUTE! 1983: анонс, 36 рівнів, скролінг"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Flip+and+Flop+1983", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, environment-death, touch-death, player-death, chase-player, time-out, time-bonus, event-points, collect-all, sequential-levels, level-select, difficulty-levels, progress-acceleration, hot-seat, game-pause, sound-warnings, splash-screen, game-screen, end-screen, mode-select, +iso-field, +paint-cell, +paint-cycle-rules, +flip-view-alternate, +sticky-trap-cell, +continue-in-place, +intermission-every-n, +hold-to-repeat-move]
proposes: ["+card:flip-view-alternate", "+card:sticky-trap-cell", "+card:continue-in-place", "+card:intermission-every-n", "+card:hold-to-repeat-move", "+window:intermission"]
author: opus
date: 2026-11-09
---

# Flip and Flop — Q*bert у цирку: кенгуру перевертає плитки згори, а мавпа — та сама мапа догори дном

## Суть
Ізометричний лабіринт із платформ-плиток, зʼєднаних драбинками-містками. Мета рівня — **перевернути всі позначені плитки**, ставши на кожну (у пізніх — двічі). Головна родзинка: непарні рівні проходить кенгуру Фліп, стрибаючи **по** платформах, а парні — мавпа Мітч на тій самій мапі, що **перевертається догори дном**: Мітч висить під платформами й перехоплюється з плитки на плитку. Переслідувачів (доглядача й летючий сачок) можна заманити на **липкі клітини**, що на кілька секунд тримають будь-кого — і героя теж.

## Поле і час
- Ізометрична скрольована сітка квадратів-плиток; платформи зʼєднані містками-драбинками — перейти з платформи на платформу можна лише там, де є місток. Поза плитками — порожнеча.
- Перші 13 рівнів лабіринт росте до максимального розміру; далі — ускладнення візерунків. Усього 36 рівнів.
- Real-time з годинником рівня: більший лабіринт — більше часу.
- Парний рівень = той самий лабіринт, що й попередній непарний, але перевернутий: «інша ілюзія перспективи», герой під платформою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фліп (кенгуру) | player | непарні рівні | стрибає з плитки на плитку зверху платформ |
| Мітч (мавпа) | player | парні рівні | висить під платформами, перехоплюється з плитки на плитку |
| Позначена плитка | tile | одинарна / подвійна | перевертається, коли на неї стали; подвійна — спершу «X», вдруге перевертається |
| Звичайна плитка | terrain | — | просто опора |
| Місток-драбинка | terrain | — | єдиний перехід між платформами |
| Порожнеча за краєм | hazard | — | крок за край — падіння, спроба втрачена |
| Липка клітина | hazard | час утримання меншає з рівнем; з рівня 25 нема | тримає героя чи переслідувача кілька секунд; використана — стає звичайною |
| Доглядач зоопарку | enemy | з рівня 3 | женеться за Фліпом |
| Летючий сачок | enemy | з рівня 4 | женеться за Мітчем |
| Чарівна драбина | gate | кожен 5-й рівень | веде героя до цирку — інтермедія |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(diag_dir)` → ЯКЩО `cell(target, tile|bridge)` → ТО `move(hero, dir)`; утримання рукоятки — повтор кроків (можна пробігти платформу, місток і наступну платформу одним рухом).
- КОЛИ `input(diag_dir)` → ЯКЩО `cell(target, void)` → ТО `custom: «падіння з лабіринту»`, `lives(-1)`.
- КОЛИ `enter(hero, marked_tile)` → ЯКЩО `state(tile, double) and not state(tile, x)` → ТО `mark(tile, X)`.
- КОЛИ `enter(hero, marked_tile)` → ЯКЩО `not state(tile, double) or state(tile, x)` → ТО `set_state(tile, flipped)`, `score(25)`.
- КОЛИ `all_gone(marked_tile)` → ТО `score(5 × seconds_left)`, `lives(+1)`, `next_level`.
- КОЛИ `level_start` → ЯКЩО `custom: «рівень парний»` → ТО `camera(flip_vertical)`, `custom: «той самий лабіринт; герой — Мітч під платформами»`.
- КОЛИ `tick` → ЯКЩО `level(>=, 3)` → ТО `custom: «доглядач (рівні Фліпа) або сачок (рівні Мітча, з 4-го) крокує до героя»`.
- КОЛИ `contact(zookeeper, flip)` → ТО `lives(-1)`, `custom: «гра триває з того ж місця; перевернуті плитки лишаються»`.
- КОЛИ `contact(net, mitch)` → ТО `lives(-1)`, `custom: «гра триває з того ж місця»`.
- КОЛИ `enter(hero, sticky_tile)` → ТО `stun(hero, n)`, `set_cell(tile, plain)`.
- КОЛИ `enter(zookeeper|net, sticky_tile)` → ТО `stun(a, n)`, `set_cell(tile, plain)` — пауза в погоні.
- КОЛИ `state_off(hero, stuck)` → ТО `sound(cymbal)` — можна рухатись.
- КОЛИ `counter(clock, ==, 0)` → ЯКЩО `counter(lives, >, 1)` → ТО `lives(-1)`, `restart`, `timer(reset, full)`; інакше `game_over`.
- КОЛИ `level_end` → ЯКЩО `custom: «номер рівня кратний 5»` → ТО `window(intermission)` — анімація цирку; кнопка її пропускає.
- КОЛИ `level_start` → ЯКЩО `level(>=, 25)` → ТО `custom: «липких клітин нема»`.
- Перемога рівня: усі позначені плитки перевернуто. Поразка: спроби вичерпано (зловили, впав, скінчився час). Рахунок: 25 за плитку + 5 за кожну секунду, що лишилась.

## Керування і ввід
- Джойстик тримати **по діагоналі** (кнопкою до екрана) — 4 діагональні напрямки ізометрії; утримання повторює кроки вздовж лінії.
- Atari: START — грати; SELECT — рівень складності (стартовий рівень 1–13); OPTION — кількість гравців (1 гравець/1 джойстик · 2/1 · 2/2); пробіл — пауза; OPTION у будь-який момент — назад на екран опцій. C64: F1/F3/F5 замість START/SELECT/OPTION.
- На екрані фінального рахунку кнопка або START — рестарт з обраного раніше рівня.

## Вікна, меню, HUD
- `splash-screen` — титульна послідовність (музика — «Вхід гладіаторів» Фучика).
- Екран опцій/вибору (`mode-select` + `difficulty-select`): стартовий рівень, кількість гравців і джойстиків.
- `game-screen`: ізометричний скрольований лабіринт; `score`, `hi-score` унизу екрана, `timer-countdown` годинника рівня, `lives` (спроби).
- `pause-menu` — пробіл (без меню, лише стоп).
- `+window:intermission` — 7 анімованих цирків-нагород, по одній кожні 5 рівнів; кнопка пропускає.
- `end-screen` — фінальний рахунок з рестартом з того ж рівня.
- Переходи: титул → опції → рівень → (усі плитки) → наступний рівень (кожен 5-й — інтермедія) → … → спроби 0 → фінальний рахунок → опції/рестарт.

## Фічі поза полем
- `level-select` — старт з будь-якого з перших 13 рівнів; з 13-го далі — лише перемогою.
- `hotseat` — 2 гравці по черзі на одному або двох джойстиках; `pause`.
- `levels-sequential` (36 рівнів) з 7 інтермедіями; бонусна спроба за кожен пройдений рівень.
- Рівні 1–2 без переслідувачів — вбудований тренувальний режим.

## Варіації й родичі
- [`qbert`](qbert.md) — ізометричне фарбування стрибком; тут поле — платформи з містками, а не піраміда, і є «двічі» як у вищих рівнях Q*bert-а.
- [`frostbite`](frostbite.md) — інший гібрид Q*bert-а 1983 року (ряди крижин).
- [`amidar`](amidar.md), [`pac-man`](pac-man.md) — «обійти все» в лабіринті з переслідувачами.
- **Осі варіацій**: правило плитки — «раз / двічі (X → перевернуто) / туди-назад (Q*bert)»; вид — «звичайний / та сама мапа догори дном іншим героєм»; пастка — «лише для героя / для всіх, одноразова (липка клітина)».

## Цікавинки для курсу
- Та сама мапа двічі: вдруге — перевернута, з іншим героєм (трансформація поля + камери) — 🥉.
- Подвійні плитки: X → перевернуто (лічильник відвідин клітини) — 🌱.
- Липка клітина для всіх: заманити переслідувача, одноразова, час утримання меншає з рівнем, звук-сигнал звільнення — 📎.
- Містки як єдині зʼєднання платформ (граф поверх сітки) — 📎.
- Смерть без скидання прогресу + таймер, що скидає рівень — 📎: два різні покарання.
- Утримання рукоятки = серія кроків через кілька платформ — 🌱.

## Мапа на каталог
- Є: `move-4dir` (діагоналі ізометрії) · `impassable-cells` (порожнеча, переходи лише містками) · `environment-death` (падіння) · `touch-death` · `player-death` · `chase-player` · `time-out` · `time-bonus` (5 за секунду) · `event-points` · `collect-all` · `sequential-levels` · `level-select` · `difficulty-levels` · `progress-acceleration` · `hot-seat` · `game-pause` · `sound-warnings` (цимбали) · `splash-screen` · `game-screen` · `end-screen` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+flip-view-alternate` «Той самий рівень удруге — перевернутий, іншим героєм» · interface/render · 🥉.
  - `+sticky-trap-cell` «Одноразова липка клітина для всіх» · entities/interact · 📎 · слоти {hold, decay_by_level}.
  - `+continue-in-place` «Смерть без скидання прогресу рівня» · game-logic/lose · 🌱.
  - `+intermission-every-n` «Інтермедія кожні N рівнів із пропуском» · levels/progression · 🌱.
  - `+hold-to-repeat-move` «Утримання = серія кроків» · interface/input · 🌱.
  - Повтори з `qbert`: `+iso-field`, `+paint-cell`, `+paint-cycle-rules`.

## Пропозиції до словників
- `+window:intermission` — анімована перерва між рівнями як нагорода (кожні N рівнів), пропуск кнопкою; ширше за `dialogue-window`.

## Джерела
- ⭐ [Atarimania: Flip and Flop](https://www.atarimania.com/games/atari-400-800-xl-xe-games-flip-and-flop-2021) — скани мануалу First Star: The Game, Obstacles (рівень 3/4, липкі клітини, час), Levels (36, 13, подвійні плитки), Scoring (25 і 5/с), Intermissions (7), Function Keys, Strategy/Tips; огляд Electronic Games (березень 1984): 5 спроб, +1 за рівень.
- [Wikipedia: Flip and Flop](https://en.wikipedia.org/wiki/Flip_and_Flop) — герої, переслідувачі, липкі клітини, максимальне поле з 13-го рівня, порт C64 (Statesoft, 1984).
- [COMPUTE! № 43 (1983)](https://www.atarimagazines.com/compute/issue43/253_2_NEWS_PRODUCTS_Games_For_Atari_64_VIC_And_Color_Computer.php) — анонс: 36 рівнів, скролінг, шість анімацій.
- YouTube: пошук «Flip and Flop 1983».

## Непевне
- (?) Чи інвертується керування на перевернутих рівнях Мітча (мануал говорить лише про «ілюзію перспективи»).
- (?) Чи доглядач з рівня 3 лишається й на рівнях Мітча (мануал: доглядач — за Фліпом, сачок — за Мітчем).
- (?) Кількість інтермедій: мануал — 7, COMPUTE! — «шість анімацій».
- (?) Алгоритм погоні переслідувачів і точні тривалості утримання — не описано.
