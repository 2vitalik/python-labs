---
title: Mappy
slug: mappy
aka: [マッピー]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1983
platforms: [arcade (Namco), Famicom, MSX, Game Gear, Game Boy, PlayStation (Namco Museum Vol. 2), Switch/PS4 (Arcade Archives)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mappy", best: true, note: "батути на 4 відскоки, двері оглушують, мікрохвильові двері, Горо, Мʼюкі, Госендзо, пари предметів і множник, дзвін, hurry, бонус-раунд"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%83%E3%83%94%E3%83%BC", note: "JA: 6 поверхів, кольори батута, ціни предметів і котів, 4 силові двері, дзвони з раунду 8–10, люки з 12–14, бонус кожні 3, 256 раундів, extend 20k/70k"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mappy+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, chase-player, pattern-automaton, touch-death, player-death, item-pickup, collect-all, combo-multiplier, escalating-kill-points, event-points, timeout-punisher, extra-life-threshold, sequential-levels, difficulty-levels, attract-demo, game-screen, status-panel, +trampoline-bounce-limit, +door-swing-stun, +microwave-door, +rising-only-landing, +air-floor-select, +enemy-learns-detour, +hurry-up-speedup, +crush-by-fall, +trapdoor-fake-floor, +bonus-stage, +invuln-while-bouncing]
proposes: ["+trigger:bounce_count", "+effect:sweep_line", "+cond:rising", "+card:trampoline-bounce-limit", "+card:door-swing-stun", "+card:microwave-door", "+card:rising-only-landing", "+card:enemy-learns-detour", "+window:bonus-round"]
author: opus
date: 2026-11-09
---

# Mappy — миша-поліцейський стрибає батутами між поверхами особняка, оглушує котів дверима й змітає їх мікрохвилями, збираючи вкрадене

## Суть
Маппі збирає 10 вкрадених речей (5 пар) у шестиповерховому особняку котів. Між поверхами — лише **батути** в прольотах, і кожен ламається на 4-й поспіль відскок; приземлитися на поверх можна тільки **на підйомі**, а в польоті Маппі невразливий. Двері — головна зброя: відчинені в бік кота, вони його **оглушують**, а блимаючі **мікрохвильові двері** випускають хвилю, що змітає всіх котів у ряду. Затягнеш — HURRY: котів більшає й вони швидшають, а далі вилітає монета-привид Госендзо.

## Поле і час
- Розріз особняка збоку: аркада — 6 поверхів (порти — 4–5); з 4-го раунду відкрито горище — ще один поверх.
- Груба сітка «поверх × проліт»: поверхи — горизонтальні коридори з дверима; між ділянками поверхів — вертикальні прольоти з батутом на дні. Сітковий шар — дискретні поверхи й позиції дверей/батутів; уздовж поверху рух плавний.
- Real-time; раунд закінчується, коли зібрано всі 10 предметів.
- Падіння в проліт без батута — до низу екрана, втрата життя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маппі | player | життя | ходить поверхом; падає в проліт на батут; на підйомі обирає поверх; відчиняє/зачиняє двері перед собою |
| Батут | terrain | колір: зелений → синій → жовтий → червоний | кожен відскок Маппі +1; на червоному ще раз — ламається; на поверсі — скидається; коти не псують |
| Двері | gate | відчинено / зачинено; бік ручки | відчиняються в бік ручки; хто стоїть з того боку — відкинутий і оглушений |
| Мікрохвильові (силові) двері | gate | 4 на раунд, блимають | відчиняє лише Маппі (і Госендзо); хвиля змітає котів у ряду; далі — звичайні двері |
| Вкрадена річ | pickup | касетник 100 · ТБ 200 · компʼютер 300 · Мона Ліза 400 · сейф 500 | 5 пар; пара блимає після першої — множник |
| Мʼюкі (Meowky) | enemy | кількість і швидкість ростуть | переслідують Маппі; батутами стрибають; після блоку дверима вчаться обхідних шляхів |
| Нямко / Горо | enemy | бос | ходить фіксованим зигзагом, не переслідує; ховається за предметом — взяв предмет: Нямко завмирає, 1000 |
| Госендзо (монета-привид) | enemy | після HURRY | вбиває навіть у польоті; мікрохвилі й дзвін не діють; сам відчиняє силові двері |
| Дзвін | object | з раунду 8–10, по одному з боків стелі | Маппі збиває відскоком; падає на котів — оглушує (Мʼюкі 300, Нямко 1000); раз на бік за раунд |
| Люк | terrain | з раунду 12–14 | відчиняється після проходу Маппі, згодом зачиняється; кіт падає оглушений (300/1000); Маппі — смерть |
| Повітряна кулька | pickup | бонус-раунд: 15 червоних по 200 + велика з Нямко 2000 | лопається від дотику |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(mappy, dir)`.
- КОЛИ `custom: «Маппі ступив у проліт»` → ЯКЩО `occupied(below, trampoline)` → ТО `bounce(mappy)`, `counter(bounces, +1)`, `score(10)`; інакше `fall(mappy)` → `lives(-1)`.
- КОЛИ `counter(bounces, ==, 4)` → ТО `disappear(trampoline)` (зламався) → `fall(mappy)`; ЯКЩО нижче є інший батут — підхопить.
- КОЛИ `enter(mappy, floor)` → ТО `counter(bounces, =0)` — батут знову зелений.
- КОЛИ `input(left|right)` → ЯКЩО `custom: «Маппі на підйомі в прольоті»` → ТО `custom: «зійти на обраний поверх»`; на спуску — не можна.
- КОЛИ `contact(cat, mappy)` → ЯКЩО `custom: «Маппі у прольоті на батуті»` → ТО `block` — у польоті невразливий.
- КОЛИ `contact(mewky|nyamco, mappy)` → ЯКЩО `not state(cat, stunned)` and `custom: «Маппі на поверсі»` → ТО `lives(-1)`.
- КОЛИ `input(button)` → ЯКЩО `facing(mappy, door)` → ТО `custom: «двері відчиняються/зачиняються»`.
- КОЛИ `custom: «двері відчинились у бік сутності»` → ТО `stun(target, n)`, `score(50)` за кота; Маппі може так «вистрілити» себе (без керування й без збору).
- КОЛИ `input(button)` → ЯКЩО `facing(mappy, power_door)` → ТО `custom: «мікрохвильова хвиля по горизонталі»`, `transform(power_door, door)`.
- КОЛИ `contact(microwave, cat)` → ТО `custom: «кота знесено з екрана»`, `score(200, 400, 800 … 5000 за серію)`; Нямко ×2; КОЛИ `timer(delay)` → ТО `spawn_at(cat, top)`.
- КОЛИ `blocked(mewky)` → ЯКЩО `cell(front, closed_door)` → ТО `custom: «наступного разу шукає обхід»`.
- КОЛИ `contact(mappy, item)` → ТО `pickup`, `score(price × mult)`; КОЛИ `picked(mappy, item)` → ТО `custom: «пара предмета блимає»`.
- КОЛИ `picked(mappy, flashing_item)` → ТО `multiplier(+1)` (від ×2 до ×6); нова пара не по черзі — множник скидається (?).
- КОЛИ `picked(mappy, item_hiding_nyamco)` → ТО `stun(nyamco, n)`, `score(1000)`.
- КОЛИ `custom: «Маппі відскочив під дзвоном»` → ЯКЩО `custom: «цей бік ще не використано в раунді»` → ТО `fall(bell)`; КОЛИ `contact(bell, cat)` → ТО `stun(cat, n)`, `score(300|1000)`.
- КОЛИ `leave(mappy, trapdoor)` → ТО `set_cell(trapdoor, hole)`; КОЛИ `timer(close)` → ТО `set_cell(trapdoor, floor)`; КОЛИ `enter(cat, hole)` → ТО `fall(cat)`, `stun(cat, n)`, `score(300|1000)`; КОЛИ `enter(mappy, hole)` → ТО `lives(-1)`.
- КОЛИ `timer(round_too_long)` → ТО `message("HURRY")`, `spawn_at(mewky ×2, top)`, `speed(cats, +n)`.
- КОЛИ `timer(after_hurry)` → ТО `spawn(gosenzo)`; КОЛИ `contact(gosenzo, mappy)` → ТО `lives(-1)`.
- КОЛИ `all_gone(item)` → ТО `win`, `next_level`.
- Бонус-раунд: КОЛИ `level_start` → ЯКЩО `custom: «кожен 3-й раунд (після першого циклу — кожен 2-й)»` → ТО `window(bonus-round)`; КОЛИ `contact(mappy, balloon)` → ТО `disappear(balloon)`, `score(200)`; велика — `score(2000)`; усі — `score(5000)`; кінець — музика стихла, Маппі випав або лопнула велика; промах не забирає життя.
- КОЛИ `counter(score, >=, 20000|70000)` → ТО `lives(+1)` (аркада за замовчуванням).
- Перемога раунду: усі 10 речей. · Поразка: 0 життів. · Рахунок: речі × множник пари, оглушення, мікрохвилі, дзвін, люк, відскоки по 10.

## Керування і ввід
- Двопозиційний важіль: ліво/право; на підйомі нахил обирає, на який поверх зійти.
- Одна кнопка: відчинити/зачинити двері, до яких повернутий Маппі (найближчі в його напрямку — навіть здалеку).
- 1–2 гравці по черзі (?).

## Вікна, меню, HUD
- `attract-demo` — аркадний показ (?).
- `game-screen`: розріз особняка; HUD — `score`, `hi-score`, `lives`, номер раунду (`level-number`), предмети, що лишилися (?).
- `custom-window` бонус-раунду: стіни, стеля, батути й кульки, без поверхів.
- `end-screen` — game over; таблиця рекордів (?).
- Переходи: монета → раунд → (10 речей) наступний раунд / бонус-раунд → … → раунд 16 → цикл з раунду 17 (швидші коти, коротший HURRY) → (0 життів) game over.

## Фічі поза полем
- `levels-sequential`: цикл 16 раундів, усього 256; складність росте до третього циклу.
- `operator-settings`: 8 рівнів складності, пороги extend (за замовчуванням 20 000 і 70 000; Famicom — 20 000, далі кожні 70 000).
- Бонус-раунд кожні 3 раунди, 4 розкладки; у розкладках 3–4 частину кульок лопає Нямко.
- Порти з власними режимами: Game Gear — «виклик Госендзо» і versus на двох.
- Збережень і меню нема (аркада).

## Варіації й родичі
- Сиквели: [Hopping Mappy](../maze-arcade/hopping-mappy.md) (1986, пого по шаховій сітці — уже `maze-arcade`), Mappy-Land (1986, Famicom), Mappy Kids (1989), мобільні Mappy.
- Родичі в корпусі: [The Bugs Bunny Crazy Castle](bugs-bunny-crazy-castle.md) (двері й переходи між поверхами, без стрибка), [Space Panic](space-panic.md), [BurgerTime](burgertime.md), [Chuckie Egg](chuckie-egg.md).
- Осі варіацій:
  - **як потрапити на інший поверх**: драбина (Space Panic) / сходи-двері-труби (Crazy Castle) / батут з лічильником зносу (Mappy);
  - **двері**: прохід / зброя-оглушення / зброя площею (мікрохвилі);
  - **таймер раунду**: нема / HURRY з підсиленням і невбивним ворогом (Mappy, Hopping Mappy).

## Цікавинки для курсу
- Батут з лічильником відскоків, кольором стану й скиданням на поверсі — 🌱.
- Приземлення лише на підйомі + вибір поверху нахилом у польоті — 📎.
- Двері, що відчиняються в бік ручки й оглушують того, хто з того боку — 📎 (стан дверей + напрям).
- Мікрохвильові двері: хвиля по рядку зі зростаючими очками за серію — 📎.
- Вороги, що «вчаться» обходити зачинені двері — 🥉.
- Пари предметів з множником ×2…×6 — 🌱.
- HURRY → більше котів, швидше, потім невбивний переслідувач — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `chase-player` (Мʼюкі) · `pattern-automaton` (зигзаг Нямко) · `touch-death` · `player-death` · `item-pickup` · `collect-all` · `combo-multiplier` (пари) · `escalating-kill-points` (мікрохвилі 200 → 5000) · `event-points` · `timeout-punisher` (Госендзо) · `extra-life-threshold` · `sequential-levels` · `difficulty-levels` (DIP) · `attract-demo` · `game-screen` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+trampoline-bounce-limit` «Батут ламається на N-й поспіль відскок, скидається на землі» · entities/move · 🌱 · слот {limit: 4}.
  - `+door-swing-stun` «Двері відчиняються в бік ручки й оглушують» · entities/interact · 📎.
  - `+microwave-door` «Двері-зброя: хвиля по рядку змітає ворогів» · entities/combat · 📎.
  - `+rising-only-landing` «Приземлитися на платформу можна лише на підйомі» · entities/move · 📎.
  - `+air-floor-select` «Нахил у польоті обирає поверх» · entities/move · 🌱.
  - `+enemy-learns-detour` «Ворог запамʼятовує блок і шукає обхід» · entities/move · 🥉.
  - `+invuln-while-bouncing` «Невразливість у польоті» · entities/state · 🌱.
  - `+hurry-up-speedup` · `+crush-by-fall` · `+trapdoor-fake-floor` · `+bonus-stage` — уже пропоновані в корпусі.

## Пропозиції до словників
- `+trigger:bounce_count(a, n)` — сутність відскочила N разів поспіль (батути Mappy).
- `+cond:rising(a)` — сутність рухається вгору (приземлення лише на підйомі).
- `+effect:sweep_line(dir)` — хвиля по рядку змітає ворогів (мікрохвильові двері).
- `+window:bonus-round` — окремий бонус-раунд з іншими правилами (Mappy, Hopping Mappy).
- `+card:…` — сім карток вище.

## Джерела
- ⭐ [Wikipedia: Mappy](https://en.wikipedia.org/wiki/Mappy) — керування, батути (4 відскоки, колір, невразливість), двері й мікрохвильові двері, Горо/Мʼюкі/Госендзо, 10 речей, множник пар до 6, дзвін, люки, HURRY, бонус-раунд, втрата життя, сиквели.
- [Wikipedia JA: マッピー](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%83%E3%83%94%E3%83%BC) — 6 поверхів і горище, кольори батута, 10 очок за відскок, очки за котів у дверях/мікрохвилях/дзвоні/люці, 4 силові двері на раунд, навчання Мʼюкі, ціни речей, бонус-раунд (15 + 1 кульки), цикл 16 раундів, 256 раундів, 8 складностей, extend.
- YouTube: пошук «Mappy arcade gameplay».

## Непевне
- (?) Чи прокручується аркадний особняк по горизонталі (тоді `info: partial`); у джерелах — лише «розріз збоку».
- (?) Чи скидається множник, коли береш річ не з блимаючої пари; деталь «Госендзо на батуті — промах, якщо це не остання річ» з JA-вікі не розібрана.
- (?) Режим на двох гравців в аркаді; таблиця рекордів і вміст HUD — з памʼяті.
- (?) Сітковість: поверхи й прольоти дискретні, але рух уздовж поверху піксельний — гра межова для сімʼї.
