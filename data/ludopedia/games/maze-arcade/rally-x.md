---
title: Rally-X
slug: rally-x
aka: [ラリーX, New Rally-X, Radar Rat Race]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1980
platforms: [arcade, VIC-20, MSX, PlayStation, Nintendo Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rally-X", best: true, note: "прапорці, S-прапорець, радар, дим, пальне, бонус-стадія, New Rally-X"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ラリーX", note: "JA: детальні правила — 3 клуби диму, очки серії, кількість машин за раундами, фланкери"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/rally-x", note: "KLOV: інструкція автомата, джойстик 4 напрямки + Smoke"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rally-x+namco+1980+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-auto, chase-player, touch-death, player-death, player-camera, minimap-radar, collect-all, combo-multiplier, event-points, time-bonus, extra-life-threshold, sequential-levels, progress-acceleration, sound-warnings, status-panel, game-screen, +fuel-as-timer, +smoke-screen-stun, +special-flag-doubler, +flank-ai, +bonus-stage-frozen-enemies, +lucky-flag-refuel, +spawn-grace]
proposes: ["+effect:refuel", "+window:bonus-round", "+card:fuel-as-timer", "+card:smoke-screen-stun", "+card:flank-ai", "+card:special-flag-doubler"]
author: opus
date: 2026-11-09
---

# Rally-X — машинка в лабіринті, більшому за екран: збери 10 прапорців за радаром, поки є пальне, і кидай дим у переслідувачів

## Суть
Синя машина безперервно їде лабіринтом, що прокручується в чотири боки; гравець лише повертає. Треба зібрати 10 жовтих прапорців, розкиданих по всій мапі, — де вони, видно тільки на **радарі** збоку. Червоні машини женуться (частина — обхідними шляхами), камені вбивають; захист — **димова завіса**, яка зупиняє переслідувача, але коштує **пального**, а пальне — це і є таймер раунду. Залишок пального в кінці раунду стає бонусом.

## Поле і час
- Клітинний лабіринт кількох екранів завбільшки; камера тримає машину гравця, скролінг у 4 напрямки.
- Радар (під індикатором пального) показує всю мапу: машину гравця, червоні машини, прапорці; **не** показує стіни й камені.
- 4 типи трас (Beginner / Intermediate / Advanced / Expert), зміна кожні 4 раунди, цикл після 16-го.
- Real-time; машина рухається завжди; пальне спадає з часом і від диму.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синя машина | player | 3 життя (стандарт); пальне | їде безперервно; джойстик змінює напрям, можна розвернутись |
| Червона машина | enemy | 3 → 8 за раундами | переслідує; непарні — напряму, парні — обхідним шляхом |
| Прапорець | pickup | 10 на раунд | очки серією 100, 200, 300…; усі → раунд пройдено |
| Спецпрапорець S | pickup | 1 на раунд | після нього очки прапорців ×2 |
| Lucky-прапорець L (New Rally-X) | pickup | — | пауза, пальне додається в очки, бак заправляється |
| Камінь | hazard | фіксовані місця траси | дотик вбиває гравця; червона машина, врізавшись, ненадовго зупиняється |
| Дим | hazard | 3 клуби на натискання | стоїть на місці; червона машина в диму зупиняється й крутиться 3 рази |
| Пальне | resource | шкала | падає з часом і від диму; 0 → машина повільна, без диму |
| Стіна | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(car, facing)` — машина їде сама.
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `face(car, dir)`; розворот на 180° дозволено.
- КОЛИ `blocked(car)` → ТО `custom: «машина повертає вздовж коридору»` (?).
- КОЛИ `input(smoke)` → ЯКЩО `counter(fuel, >, 0)` → ТО `spawn_at(smoke ×3, behind)`, `counter(fuel, −n)`.
- КОЛИ `contact(red_car, smoke)` → ТО `stun(red_car, n)`, `custom: «крутиться 3 рази»`, `disappear_b`.
- КОЛИ `contact(red_car, rock|red_car)` → ТО `stun(red_car, n)`.
- КОЛИ `contact(car, flag)` → ТО `pickup`, `score(100 × k)`, де k — номер прапорця в серії без смерті.
- КОЛИ `contact(car, special_flag)` → ТО `pickup`, `multiplier(×2)` для наступних прапорців раунду.
- КОЛИ `contact(car, red_car|rock)` → ЯКЩО `not timer(<, grace)` → ТО `lose` (життя −1), `custom: «серія очок і множник скидаються»`.
- КОЛИ `timer(every)` → ТО `counter(fuel, −1)`; ЯКЩО `counter(fuel, <, 25%)` → `sound(warning)`, шкала червона.
- КОЛИ `counter(fuel, ==, 0)` → ТО `speed(car, ↓)`, `custom: «дим недоступний»`.
- КОЛИ `all_gone(flag)` → ТО `score(fuel_left)`, `next_level`.
- КОЛИ `level_start` → ТО `spawn_at(red_cars, bottom)`; від 6 машин частина — згори; кількість +1 за раунд до 8.
- КОЛИ `level_start` → ЯКЩО `level(in, 3, 7, 11…)` → ТО `custom: «бонус-стадія: 8 машин стоять, доки не скінчиться пальне; гравець швидший, пальне витрачається швидше»`.
- КОЛИ `counter(fuel, ==, 0)` → ЯКЩО `mode(bonus)` → ТО `custom: «червоні машини рушають»`.
- КОЛИ `died(car)` → ЯКЩО `mode(bonus)` → ТО `next_level` (стадія закінчується).
- КОЛИ `counter(score, >=, 20000)` → ТО `lives(+1)`; New Rally-X — ще й на 100 000.
- КОЛИ `contact(car, lucky_flag)` → ТО `score(fuel)`, `custom: «бак заправляється»` (New Rally-X).
- Перемога: нема (цикл трас). Поразка: 0 машин. Рахунок: прапорці серією ×2 після S, залишок пального.

## Керування і ввід
- Джойстик 4 напрямки (лише поворот, газу нема) + кнопка Smoke.
- Тактика: маршрут за радаром, дим у вузькому коридорі за собою; економія пального — це і час, і бонус.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `splash-screen` / атракт (?).
- `game-screen`: ліворуч — вікно на лабіринт; праворуч — панель: `score`, `hi-score`, шкала пального (`energy-bar`), радар (`minimap`), `lives`, номер раунду (`level-number`), зібрані прапорці (?).
- Бонус-стадія — той самий екран з іншими правилами; New Rally-X — заставка стадії з кількістю ворогів і підказкою «машини стоять, доки є пальне».
- Переходи: атракт → (монета) раунд → (10 прапорців) підрахунок пального → наступний раунд / бонус-стадія → (0 машин) атракт. Без continue й вводу імені.

## Фічі поза полем
- `levels-sequential`: 4 траси × 4 раунди, цикл; бонус-стадія перед кожною зміною траси.
- `operator-settings`: кількість машин і поріг бонусу (?).
- 2 гравці по черзі (`hotseat`).
- Нема паузи, збережень.

## Варіації й родичі
- New Rally-X (1981): менше ворогів (з 1, максимум 7) і каменів, економніше пальне, ширші проходи, S блимає на радарі, Lucky-прапорець, друге бонусне життя.
- Порти й ремейки: VIC-20 (Radar Rat Race — миші й коти), MSX, Namco Museum, Rally-X Arrangement (павер-апи), Rally-X Remix (3D, Pac-Man), Rally-X Rumble (iOS, мультиплеєр), Arcade Archives.
- Родичі: Head On (попередник: машини в лабіринті), Pac-Man (та сама плата), Bomberman (бонус-стадії), Battle City.
- Осі: **поле** (екран / більше за екран + радар); **таймер** (лічильник / ресурс, що витрачається ще й на дії); **ІІ переслідувачів** (усі напряму / парні обходять); **серія очок** (зростає / скидається смертю).

## Цікавинки для курсу
- Камера за гравцем і радар, що показує лише частину шарів (машини й прапорці, без стін і каменів) — 🥉.
- Пальне як таймер і водночас ціна дії (дим) з бонусом за залишок — 📎.
- Дим: спавн перешкоди позаду, яка оглушує переслідувача — 📎.
- Два типи переслідувачів: напряму і з обходу, щоб не йти «потягом» — 🥈: різні цілі BFS для однієї погоні.
- Серія очок прапорців зі спец-множником ×2 і скиданням при смерті — 🌱.
- Бонус-стадія з інвертованим правилом (вороги стоять, доки є пальне) — 🌱.

## Мапа на каталог
- Є: `move-auto` · `chase-player` · `touch-death` · `player-death` · `player-camera` · `minimap-radar` · `collect-all` (10 прапорців) · `combo-multiplier` (серія прапорців без смерті) · `event-points` · `time-bonus` (залишок пального) · `extra-life-threshold` · `sequential-levels` · `progress-acceleration` (машин більше щораунду) · `sound-warnings` (мало пального) · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+fuel-as-timer` «Пальне — таймер і ціна дій» · entities/state · 📎 · слоти {drain, action_cost}.
  - `+smoke-screen-stun` «Дим позаду оглушує переслідувача» · entities/combat · 📎 · слот {clouds: 3}.
  - `+special-flag-doubler` «Предмет подвоює ціну наступних» · game-logic/score · 🌱.
  - `+flank-ai` «Частина ворогів іде в обхід» · entities/move · 🥈 (родич Pac-Man Pinky/Inky).
  - `+bonus-stage-frozen-enemies` «Бонус-стадія: вороги стоять до кінця ресурсу» · levels/progression · 🌱.
  - `+lucky-flag-refuel` «Предмет переводить ресурс в очки й поповнює» · entities/interact · 🌱.
  - `+spawn-grace` «Невразливість на старті раунду» · entities/state · 🌱.

## Пропозиції до словників
- `+effect:refuel` — поповнити ресурс-таймер (Lucky-прапорець).
- `+window:bonus-round` — бонус-стадія з окремими правилами.
- `+card:fuel-as-timer`, `+card:smoke-screen-stun`, `+card:flank-ai`, `+card:special-flag-doubler` — див. вище.

## Джерела
- ⭐ [Wikipedia: Rally-X](https://en.wikipedia.org/wiki/Rally-X) — прапорці, S, камені, дим, пальне, радар, бонус-стадія кожні 4 раунди, New Rally-X, порти.
- [Wikipedia JA: ラリーX](https://ja.wikipedia.org/wiki/ラリーX) — 3 клуби диму, червона машина крутиться 3 рази, серія 100/200/…, 3 машини і бонус на 20 000, 3→8 ворогів, непарні/парні, траси й цикл 16, різниця з New Rally-X.
- [KLOV: Rally-X](https://www.arcade-museum.com/Videogame/rally-x) — інструкція автомата; джойстик 4 напрямки + Smoke; S блимає на радарі.
- YouTube: пошук «rally-x namco 1980 arcade gameplay».

## Непевне
- (?) Розмір лабіринту в клітинах/екранах; чи краї мапи замкнені тором.
- (?) Камені: JA — фіксовані місця траси; KLOV — «randomly placed».
- (?) Що робить машина, впершись у стіну без вводу (повертає сама чи стоїть).
- (?) Тривалість невразливості на старті раунду й оглушення димом; витрата пального на дим.
- (?) Чи радар у оригіналі показує S окремо (JA: блимання — нововведення New Rally-X; KLOV — у інструкції оригіналу).
