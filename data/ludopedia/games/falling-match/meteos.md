---
title: Meteos (Метеос)
slug: meteos
aka: [メテオス, "Meteos: Disney Magic", Meteos Wars, Meteos Online]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2005
platforms: [Nintendo DS, mobile, PC (Meteos Online), Xbox 360 (Meteos Wars)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Meteos", best: true, note: "запуск блоків угору лінією 3+, гравітація планети, банк блоків, режими Star Trip/Simple/Deluge/Time, мультиплеєр на 4, сиквели"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/メテオス", note: "зсув лише вгору-вниз у стовпці, повторне запалювання (boost), «попіл» і його відновлення, відправка суперникам, ширина поля 7–11, Time Attack 2/5 хв і 100/1000 метеосів"}
  - {kind: other, url: "https://strategywiki.org/wiki/Meteos/Walkthrough", note: "планети, базова Geolyte; сторінка не відкрилась (403), бачена в пошуку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=meteos+nintendo+ds+gameplay", note: "пошук; геймплей DS"}
stage: v1
coverage: 60
mechanics: [gravity-fall, line-match-clear, chain-reaction, garbage-attack, simultaneous-versus, ai-opponent, drag-drop-piece, rule-variants, character-select, world-map, mode-select, time-out, collect-quota, score-records, difficulty-levels, game-settings, game-pause, end-screen, +launch-stack, +column-shift-drag, +reignite-boost, +per-level-physics, +cinder-recovery, +material-bank-unlocks, +item-blocks]
proposes: ["+effect:launch", "+effect:boost", "+cond:airborne", "+feature:material-bank", "+window:synthesis-window", "+axis:gravity"]
author: opus
date: 2026-11-09
---

# Meteos — збери 3 в лінію, і блоки разом зі стосом над ними злітають ракетою в космос, до суперника

## Суть
На планету сипляться метеоси (кольорові блоки різних стихій). Стилусом блок зсувають **лише вгору або вниз у своєму стовпці**; лінія 3+ однакових по горизонталі чи вертикалі **запалюється** і злітає разом з усім, що на ній лежить. Важкий стос злітає недалеко — його підпалюють знизу ще раз (boost), доки він не вилетить за верх поля. Вилетілі блоки летять на планету суперника. Ядро — фізика запуску: у кожної планети своя гравітація, сила вибуху й ширина поля.

## Поле і час
- Вертикальне поле на двох екранах DS; ширина — 7–11 стовпців залежно від планети (найчастіше 9), планета Meteos — 11×23 (ja.wikipedia). Висота інших — (?).
- Real-time: метеоси падають зверху з темпом планети; запущена маса летить угору, сповільнюється і знову падає за законом планети.
- Шари: стос блоків + маси в польоті (рухаються як одне ціле) + «попіл» (згорілі блоки) + індикатор падаючих на тебе блоків.
- Фізика per-planet: одні маси летять рівномірно, інші швидко падають, інші розганяються/сповільнюються; на деяких планетах запущене зникає на місці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Метеос | tile | тип/стихія (колір) | падає; стилус зсуває вгору/вниз у стовпці; 3+ в лінію → запалюється |
| Запалений блок | tile | — | двигун: штовхає масу над собою вгору; потім стає попелом |
| Маса (катамарі) | object | розмір, швидкість | стос над запаленою лінією, рухається як одне ціле; виліт за верх → відправка |
| Попіл (згорілий блок) | tile | — | не матчиться; через час без запусків «відновлюється» в метеос |
| Планета | zone | ширина, гравітація, сила запуску, темп падіння, частки типів | задає фізику й склад блоків рівня |
| Предмет (power-up) | pickup | ефект | допомагає собі або шкодить суперникам (молот розбиває блоки) |
| Банк блоків | resource | лічильник за типом | кожен відправлений блок іде в банк; витрачається на відкриття |
| Рідкісні метали «душа», «час» | resource | — | падають лише на планеті Meteos і споріднених |
| Speeder | — | шкала | регулює темп і частоту падіння; накопичені вхідні метеоси (?) |
| Суперник | enemy | своя планета | отримує відправлені маси; ти — його |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(planet_rate)` → ТО `spawn_at(meteo, top)` з типом за частками планети; `fall(meteo)`.
- КОЛИ `input(drag(meteo, up|down))` → ЯКЩО `custom: «сусід у тому ж стовпці — метеос, не маса в польоті»` → ТО `swap(meteo, neighbor)`; горизонтально рухати не можна (оригінал).
- КОЛИ `pattern(line(3+, same_type))` → ТО `custom: «ignite — лінія запалюється»`, `custom: «launch(mass) — усе над лінією стає масою, що летить угору»`.
- КОЛИ `tick` → ЯКЩО `state(mass, airborne)` → ТО `speed(mass, −planet_gravity)`; ЯКЩО `custom: «швидкість ≤ 0»` → ТО `fall(mass)`.
- КОЛИ `pattern(line(3+, same_type))` → ЯКЩО `state(mass, airborne)` → ТО `custom: «boost — повторне запалювання знизу маси додає тягу»`, `combo(+1)`.
- КОЛИ `reach(mass, top_edge)` → ТО `disappear_a`, `send_garbage(opponents, mass_size)`, `counter(bank[type], +n)`.
- КОЛИ `custom: «маса впала й лягла назад на стос»` → ТО `custom: «блоки знову звичайні, лінії перевіряються»`.
- КОЛИ `after(launch)` → ТО `transform(ignited → cinder)`.
- КОЛИ `timer(n)` → ЯКЩО `custom: «давно не було запусків»` → ТО `transform(cinder → meteo)`.
- КОЛИ `contact(garbage, field)` → ТО `fall(garbage)` на стос (відправлене суперником).
- КОЛИ `picked(item)` → ТО `custom: «ефект предмета: молот розбиває блоки, інші — на себе або на суперників»`.
- КОЛИ `custom: «стос вище верху поля і не запускається»` → ТО `lose` («планета розбита»).
- Simple/Versus: КОЛИ `count(alive_planets, ==, 1)` → ТО `win` останньому.
- Time Attack: КОЛИ `timer(==0)` (2 або 5 хв) → ТО `game_over`, рахунок; або КОЛИ `counter(launched, ≥, 100|1000)` → ТО `win`, час — результат.
- Deluge: КОЛИ `custom: «поле повністю заповнене»` → ТО `game_over` (безкінечна злива).
- Star Trip: КОЛИ `level_end` → ЯКЩО `custom: «планету пройдено»` → ТО `custom: «вибір наступної планети на розгалуженому маршруті»`; фінал — планета Meteos.
- Поразка: стос над верхом. Рахунок: кількість відправлених блоків, швидкість (Time).

## Керування і ввід
- Стилус: торкнутись метеоса й тягнути вгору/вниз — він міняється місцями з сусідом; можна вести довго, «протягуючи» блок крізь стовпець.
- Кнопки: курсор + кнопка зсуву (альтернатива стилусу).
- Відома вада: швидке «шкрябання» стилусом по нижньому екрану випадково складає лінії (Eurogamer).
- Meteos: Disney Magic — DS боком, тягнути можна ще й ліворуч/праворуч.

## Вікна, меню, HUD
- `main-menu` з `mode-select`: Star Trip · Simple · Deluge · Time Attack · Multiplayer (Download Play) · Synthesis Room (?) · Options.
- `map-window` — маршрут Star Trip між планетами з розгалуженнями.
- `character-select` — вибір планети/прибульця (32), зі своєю фізикою.
- `match-setup` (Simple): планета, кількість життів, складність CPU, команди й 3-на-1, ліміт часу або «стоків».
- `custom: «synthesis-window»` — синтез нових планет і предметів із банку матеріалів.
- `game-screen`: поле, стовпці, маси в польоті, шкала Speeder, мініатюри полів суперників, лічильник відправлених блоків, `timer-countdown` (Time).
- `end-screen` → рекорди; `pause-menu`.

## Фічі поза полем
- Режими: Star Trip (кампанія з картою), `mode-versus` (до 4, CPU, команди), `mode-time-attack` (2/5 хв; 100/1000 метеосів), Deluge (`mode-endless`), Challenge.
- `custom: «material-bank»` — відправлені блоки накопичуються за типами й витрачаються на відкриття планет, прибульців, звуків.
- `unlockables`, `difficulty-presets`, `local-multiplayer` (Download Play: 4 гравці з одного картриджа), `leaderboard-local` за планетами.

## Варіації й родичі
- Meteos (DS, 2005, Q Entertainment + Sora) → Astro Blocks (mobile, 2006) → Disney Magic (DS, 2007: горизонтальні зсуви) → Meteos Online (PC, 2007) → Meteos Wars (XBLA, 2008).
- Родичі: Panel de Pon (курсор міняє сусідів, підйом поля), Puyo Puyo (сміття супернику), Lumines (той самий видавець Q Entertainment), Tetris 99 (кілька суперників).
- **Осі варіацій**: напрямок результату збігу (зникнути / злетіти вгору) · зсув (лише вертикальний у стовпці / будь-який) · фізика (одна / на рівень) · відправка (ряди сміття / ті самі блоки) · відновлення «попелу» (нема / за таймером).

## Цікавинки для курсу
- Запуск маси: лінія 3+ піднімає весь стос над нею як одне тіло — 🥉 (групування звʼязаних блоків у масу).
- Повторне запалювання маси в польоті (boost) з силою, що додається — 🥈.
- Параметризована фізика планети (гравітація, сила, ширина) як конфіг рівня — 📎.
- Вертикальний свап у стовпці стилусом/курсором — 🌱.
- Попіл, що відновлюється через N секунд бездіяльності — 🌱.
- Відправка тих самих блоків на поле суперника (до 4 гравців) — 🥈.
- Банк матеріалів за типами → крамниця відкриттів — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `line-match-clear` (3+ гориз./верт.) · `chain-reaction` (boost) · `garbage-attack` · `simultaneous-versus` · `ai-opponent` · `drag-drop-piece` (найближча до перетягування стилусом) · `rule-variants` (планети) · `character-select` · `world-map` (Star Trip) · `mode-select` · `time-out` · `collect-quota` (100/1000) · `score-records` · `difficulty-levels` · `game-settings` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+launch-stack` «Збіг піднімає стос над собою вгору» · entities/move · 🥉.
  - `+column-shift-drag` «Зсув блока лише в межах стовпця» · interface/input · 🌱.
  - `+reignite-boost` «Повторний збіг у польоті додає тягу» · entities/move · 🥈.
  - `+per-level-physics` «Гравітація й сила запуску — параметри рівня» · levels/format · 📎.
  - `+cinder-recovery` «Згорілі блоки відновлюються за часом» · entities/state · 🌱.
  - `+material-bank-unlocks` «Банк зібраного за типами → відкриття» · game-logic/economy · 📎.
  - `+item-blocks` «Предмети в падаючому потоці» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:launch` — надати масі/сутності імпульс угору (протилежність `fall`).
- `+effect:boost` — додати імпульс сутності, що вже рухається.
- `+cond:airborne` — сутність у польоті, не на опорі (обернене до ⏳ `supported`; можна й `not supported`).
- `+feature:material-bank` — ресурси з партій накопичуються між сесіями й витрачаються на відкриття.
- `+window:synthesis-window` — екран обміну матеріалів на планети/предмети.
- `+axis:gravity` — значення `per-level` (гравітація задається рівнем/планетою).

## Джерела
- ⭐ [Wikipedia: Meteos](https://en.wikipedia.org/wiki/Meteos) — лінія 3+ запалює й піднімає блоки, гравітація планети, банк, 32 прибульці, режими, мультиплеєр на 4, сиквели.
- [ja.wikipedia: メテオス](https://ja.wikipedia.org/wiki/メテオス) — зсув вгору/вниз у стовпці, повторне запалювання, попіл і відновлення, відправка за верх, ширина 7–11, Time Attack, Synthesis Room.
- [StrategyWiki: Meteos/Walkthrough](https://strategywiki.org/wiki/Meteos/Walkthrough) — бачена в пошуку (планети, Geolyte як еталон); 403.
- YouTube: пошук «meteos nintendo ds gameplay».

## Непевне
- (?) Висота поля стандартних планет; темп падіння.
- (?) Як саме працює Speeder: лише регулятор темпу чи ще й «спустити накопичене» тапом (так каже гайд з пошуку).
- (?) Точна формула сили запуску й boost; чи маса може «злипнутись» з іншою в польоті.
- (?) Повний список предметів і їхні ефекти (крім молота).
- (?) Склад меню DS-версії; Synthesis Room — пункт меню чи частина іншого екрана.
- (?) Розробник: Q Entertainment разом із Sora (Масахіро Сакурай) — з памʼяті.
