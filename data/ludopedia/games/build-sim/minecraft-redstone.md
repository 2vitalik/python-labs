---
title: Minecraft — редстоун
slug: minecraft-redstone
aka: [Minecraft redstone, редстоун, червоний камінь]
family: build-sim
also: [program-robots, connect-rotate]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: none
year: 2011
platforms: [PC (Java), Bedrock (Windows, mobile, Switch, Xbox, PlayStation)]
links:
  - {kind: fandom, url: "https://minecraft.wiki/w/Redstone_mechanics", best: true, note: "сила сигналу, затухання, сильне/слабке живлення, тіки, оновлення блоків"}
  - {kind: fandom, url: "https://minecraft.wiki/w/Redstone_circuits/Advanced_circuits", note: "категорії схем: передача, логіка, імпульси, годинники, памʼять, поршні"}
  - {kind: fandom, url: "https://minecraft.wiki/w/Redstone_Repeater", note: "затримка 1–4, діод, підсилення до 15, блокування"}
  - {kind: fandom, url: "https://minecraft.wiki/w/Redstone_Comparator", note: "режими порівняння/віднімання, читання контейнерів"}
  - {kind: fandom, url: "https://minecraft.wiki/w/Redstone_Torch", note: "інверсія, перегорання"}
  - {kind: other, url: "https://esolangs.org/wiki/Minecraft_(game)", note: "редстоун як обчислення: OR + NOT, повнота за Тюрінгом умовно"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Minecraft", note: "гра загалом"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=minecraft+redstone+basics+tutorial", note: "пошук; основи"}
stage: v1
coverage: 70
mechanics: [button-toggle, push-object, pull-object, orientation-state, pipe-connectors, chain-reaction, game-loop, connectivity-check, inventory, +signal-decay, +logic-gates, +delay-line, +signal-lock, +comparator-modes, +container-level-sensor, +pulse-edge, +block-update, +burnout-limit, +quasi-connectivity, +observer-sensor, +strong-weak-power, +redstone-clock]
proposes: ["+trigger:block_update", "+cond:powered", "+effect:propagate", "+effect:set_delay", "+card:signal-decay", "+card:logic-gates", "+card:delay-line", "+card:comparator-modes", "+card:block-update", "+axis:value-domain"]
author: opus
date: 2026-11-09
---

# Minecraft (редстоун) — дріт, що несе число 0–15 і втрачає 1 на кожному блоці, плюс діоди, інвертори й компаратори

## Суть
Описано **лише шар редстоуну**: гравець ставить у воксельному світі пил-провід, джерела (важіль, кнопка, плита, факел), компоненти (репітер, компаратор, спостерігач) і механізми (поршень, двері, лампа). Сигнал — **ціле число 0–15**: пил передає його сусідам, зменшуючи на 1 за блок; репітер відновлює до 15 і затримує; факел інвертує; компаратор порівнює або віднімає. З цього збирають логічні вентилі, годинники, памʼять, автоматичні ферми й цілі компʼютери.

## Поле і час
- Поле — 3D-сітка блоків; редстоун-пил лежить на верхній грані блока, з'єднується з сусідами в 4 сторони і по сходинці вгору/вниз через провідні блоки. Провідний блок над місцем зʼєднання розриває його, непровідний (скло) — ні.
- Тік гри = 1/20 с; **редстоун-тік** (термін спільноти) = 2 ігрові тіки = 0,1 с. Пил оновлюється щотіку. Bedrock має власні «produce/consume» тіки — поведінка відрізняється від Java.
- Стан блока, що визначає схему: рівень сигналу (0–15), «живлений сильно / слабко», орієнтація компонента, стан механізму.
- Оновлення блоків поширюються: пил, факели й рейки оновлюють блоки до 2 кроків манхеттенської відстані; кнопки, важелі, плити, репітери, компаратори, спостерігачі — сусідів і сусідів свого опорного блока.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | інвентар блоків | ставить/ламає блоки, натискає «використати» |
| Редстоун-пил | conduit | рівень 0–15 | рівень = max(рівень сусідніх джерел) − 1; передає до 15 блоків |
| Провідний блок | object | сильно / слабко живлений | сильно живлений живить пил поруч; слабко (лише від пилу) — ні, але вмикає механізми й компоненти |
| Непровідний блок (скло) | object | — | не живиться, не розриває пил |
| Важіль | source | увімк/вимк | перемикає вихід 15/0 |
| Кнопка | source | тривалість імпульсу | дає 15 на короткий час, потім сама вимикається |
| Нажимна плита | source | — | 15, доки на ній сутність |
| Редстоун-факел | source | горить/погас, лічильник перемикань | NOT: гасне, коли живлений блок, до якого прикріплений; горить — 15; сильно живить блок над собою |
| Блок редстоуну | source | — | постійне джерело (?) |
| Репітер | conduit | напрям · затримка 1–4 р-тіки · заблоковано | діод (лише ззаду наперед); будь-який вхід → вихід 15 через затримку; сильно живить блок спереду |
| Компаратор | conduit | режим compare/subtract · задній вхід · 2 бокові | вихід за формулою режиму; читає контейнери й інші блоки ззаду |
| Спостерігач | source | напрям | бачить зміну блока перед «обличчям», дає імпульс з тильного боку |
| Поршень / липкий поршень | object | напрям | живлення → висуває й штовхає ряд блоків; липкий при втягуванні тягне блок |
| Двері, люк, лампа, TNT, диспенсер, дропер | sink | — | дія за типом при живленні |
| Мідна лампа | sink | світить/ні | перемикає стан на кожен фронт сигналу |
| Контейнер (скриня, бочка, піч, дозатор) | container | заповненість слотів | для компаратора — джерело рівня |
| Торт · казан · рамка | object | шматки / рівень / поворот | компаратор читає: торт 2 за шматок (повний 14), казан 0–3, рамка 1–8 за поворот 45° |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `set_value(dust, strongest_neighbor − 1)` (максимум сусідніх джерел мінус 1); на межі 0 сигнал зникає (15 блоків пилу — максимум).
- КОЛИ `input(use, lever)` → ТО `set_state(lever, on|off)`, `set_value(lever, 15|0)`.
- КОЛИ `input(use, button)` → ТО `set_state(button, pressed, duration)`, `set_value(button, 15)`; після тривалості — `clear_state(button, pressed)`.
- КОЛИ `enter(entity, pressure_plate)` → ТО `set_value(plate, 15)`.
- КОЛИ `leave(entity, pressure_plate)` → ТО `set_value(plate, 0)`.
- КОЛИ `state_on(torch_block, powered)` → ТО `clear_state(torch, lit)` через 1 р-тік.
- КОЛИ `state_off(torch_block, powered)` → ТО `set_state(torch, lit)` (вхід 0 дає 15, вхід 1–15 дає 0).
- КОЛИ `counter(torch_turnoffs, >, 8)` → ЯКЩО `timer(<=, 60)` (ігрових тіків) → ТО `set_state(torch, burnt_out)`; ігнорує зміни, доки за останні 60 тіків їх не стане менше 8.
- КОЛИ `state_on(repeater_back, powered)` → ЯКЩО `not state(repeater, locked)` → ТО `set_value(repeater_out, 15)` через delay р-тіків.
- КОЛИ `input(use, repeater)` → ТО `custom: «delay = delay mod 4 + 1» (1 → 2 → 3 → 4 → 1)`.
- КОЛИ `state_on(repeater_side, powered)` → ЯКЩО `custom: «джерело збоку — репітер або компаратор»` → ТО `set_state(repeater, locked)`: вихід замерзає; знято живлення збоку — `clear_state(repeater, locked)`.
- КОЛИ `tick` → ЯКЩО `state(comparator, compare)` and `custom: «left ≤ rear and right ≤ rear»` → ТО `set_value(comparator_out, rear)`; інакше `set_value(comparator_out, 0)`.
- КОЛИ `tick` → ЯКЩО `state(comparator, subtract)` → ТО `set_value(comparator_out, rear − strongest_side)`, не менше 0 (напр., 9 − max(2, 5) = 4).
- КОЛИ `input(use, comparator)` → ТО `set_state(comparator, compare|subtract)` (передній факелик опущено / піднято).
- КОЛИ `tick` → ЯКЩО `occupied(comparator_back, container)` → ТО `set_value(rear, fullness_level)`, де рівень = floor(1 + середня заповненість слотів × 14); порожній контейнер — 0 (300 блоків у 9-слотовому дозаторі → 8).
- КОЛИ `custom: «змінився блок перед спостерігачем»` → ТО `set_state(observer_back, pulse, 1)` (імпульс на 1 р-тік (?)).
- КОЛИ `state_on(piston, powered)` → ЯКЩО `custom: «ряд перед поршнем рухомий і не довший за ліміт»` → ТО `push(row)`; інакше `block`.
- КОЛИ `state_off(piston, powered)` → ЯКЩО `state(piston, sticky)` → ТО `pull(front_block)`.
- КОЛИ `state_on(block_above_piston, powered)` → ЯКЩО `mode(java)` → ТО `custom: «поршень/диспенсер/дропер вважаються живленими (quasi-connectivity), але спрацюють лише після оновлення блока»`.
- КОЛИ `state_on(copper_bulb, powered)` → ТО `set_state(copper_bulb, toggle)` — лише на передньому фронті.
- КОЛИ `state_on(mechanism, powered)` → ТО `custom: «дія за типом: двері відчиняються, лампа світить, TNT запалюється, дропер викидає»`; типи активації — лише фронт / фронт і спад / змішані.
- КОЛИ `custom: «репітер, факел або компаратор живить блок»` → ТО `set_state(block, strongly_powered)`; КОЛИ `custom: «блок живиться лише пилом»` → ТО `set_state(block, weakly_powered)` — він не живить пил далі.
- Перемоги/поразки/рахунку нема: шар — пісочниця схем; «мета» — працююча схема (ферма, двері, обчислювач).

## Керування і ввід
- ПКМ (використати) — поставити блок/компонент; на компоненті — дія: важіль перемкнути, кнопку натиснути, репітеру змінити затримку, компаратору режим.
- ЛКМ — зламати. Орієнтація компонента — за напрямком погляду гравця під час встановлення (репітер, компаратор, спостерігач, поршень).
- Ввід «від світу»: стати на плиту, кинути предмет у контейнер (компаратор прочитає), змінити блок перед спостерігачем.

## Вікна, меню, HUD
- `game-screen`: світ від першої/третьої особи; HUD — `inventory-bar` (хотбар 9 слотів), приціл.
- `inventory-window` — інвентар; у творчому режимі вкладка «Redstone» з усіма компонентами.
- `custom-window` — debug-оверлей F3 (Java): координати, блок під прицілом і його стани (рівень сигналу, орієнтація) — головний інструмент налагодження схем.
- `pause-menu` → `settings-window`; `main-menu` → `save-slots` (світи) → `game-screen`.
- Переходи: game-screen ↔ inventory-window (E); F3 — оверлей поверх game-screen.

## Фічі поза полем
- `mode-sandbox` (творчий режим: безкінечні блоки, політ) — головне середовище схем; `save-slots` (світи), `autosave`.
- `seed-input` — генерація світу за сідом; світ-«flat» для схем.
- `mod-support` / `custom-rules` — правила гри (gamerules), датапаки; дві редакції (Java/Bedrock) з різною редстоун-фізикою — фактично два набори правил.
- `online-multiplayer` — сервери з загальними схемами.

## Варіації й родичі
- Java vs Bedrock — одна механіка, різна фізика: quasi-connectivity лише Java, інші тіки, інший порядок оновлень.
- Родичі в корпусі: `wireworld` (провідник/голова/хвіст електрона), `cell-machine`, `factorio-belts` (мережа сигналів у Factorio — числа на дротах), `game-of-life` (обчислення локальними правилами).
- Поза корпусом: Logic World, Turing Complete (вентилі як гра), Infinifactory.
- Осі варіацій:
  - **значення сигналу:** 1 біт / 0–15 зі затуханням / ціле без меж (Factorio);
  - **затримка:** миттєва / фіксована / налаштовувана (репітер 1–4);
  - **напрямок:** ненапрямлений пил / діод (репітер) / сенсор (спостерігач);
  - **сенсори світу:** плита, спостерігач, компаратор-контейнер — схема читає стан гри.

## Цікавинки для курсу
- Сигнал 0–15 з затуханням −1 на клітину: заливка максимумом від джерел (BFS по сітці) — 📎.
- Репітер-діод із затримкою 1–4 і факел-NOT: на них уже будуються вентилі AND/OR/XOR — 🥉 (подієва модель з чергою запланованих оновлень).
- Компаратор: compare/subtract + читання заповненості контейнера формулою — 🌱 як функція, 🥉 у схемі.
- Блокування репітера збоку = засувка (latch) — 📎.
- Перегорання факела (>8 гасінь за 60 тіків) — захист від нескінченного годинника — 🌱.
- Порядок оновлень і quasi-connectivity: чому однакова схема поводиться по-різному — 🥇 (детермінізм симуляції залежить від порядку обробки).
- Повний «процесор» з редстоуну як завдання-шоукейс — 👑.

## Мапа на каталог
- Є: `button-toggle` (важіль/кнопка → механізм) · `push-object` + `pull-object` (поршні) · `orientation-state` (репітер, компаратор, спостерігач) · `pipe-connectors` (компонент із входом/виходом) · `chain-reaction` (каскад оновлень) · `game-loop` (тіки) · `connectivity-check` (зʼєднання пилу) · `inventory`.
- **Нема** → пропозиції карток:
  - `+signal-decay` «Сигнал, що слабне з відстанню» · game-logic · 📎 · слоти {max: 15, decay: 1}.
  - `+logic-gates` «Логічні вентилі з клітин» · game-logic · 🥉 — NOT (факел) + OR (злиття пилу).
  - `+delay-line` «Компонент-затримка» · game-logic · 📎 · слот {delay: 1..4}.
  - `+signal-lock` «Засувка: бічний сигнал заморожує вихід» · game-logic · 📎.
  - `+comparator-modes` «Порівняння / віднімання сигналів» · game-logic · 🌱.
  - `+container-level-sensor` «Сенсор заповненості контейнера» · entities/state · 🌱.
  - `+pulse-edge` «Дія на фронті / спаді сигналу» · game-logic · 🌱.
  - `+block-update` «Поширення оновлень сусідам» · game-logic · 🥇.
  - `+burnout-limit` «Перегорання за частоту перемикань» · entities/state · 🌱.
  - `+quasi-connectivity` «Живлення через сусіда зверху» · game-logic · 🥈.
  - `+observer-sensor` «Сенсор зміни сусідньої клітини» · entities/state · 📎.
  - `+strong-weak-power` «Сильне й слабке живлення блока» · game-logic · 📎.
  - `+redstone-clock` «Годинник-генератор імпульсів» · game-logic · 📎.

## Пропозиції до словників
- `+trigger:block_update` — сусідній блок змінився й надіслав оновлення (спостерігач, quasi-connectivity).
- `+cond:powered` — блок/компонент має сигнал > 0 (зараз — `state(a, powered)`).
- `+effect:propagate` — поширити значення по провіднику з затуханням (пил), зараз — `set_value` з формулою.
- `+effect:set_delay` — задати затримку компонента (репітер), зараз — `custom`.
- `+card:signal-decay`, `+card:logic-gates`, `+card:delay-line`, `+card:comparator-modes`, `+card:block-update` — див. вище.
- `+axis:value-domain` — що несе клітина-провідник: біт / мале ціле / необмежене число (Wireworld · Minecraft · Factorio).

## Джерела
- ⭐ [Minecraft Wiki: Redstone mechanics](https://minecraft.wiki/w/Redstone_mechanics) — сила 1–15, затухання по пилу, сильне/слабке живлення, ігровий і редстоун-тік, оновлення блоків, типи активації.
- [Minecraft Wiki: Advanced circuits](https://minecraft.wiki/w/Redstone_circuits/Advanced_circuits) — ⭐ з черги: категорії схем, репітер кожні 15 блоків.
- [Redstone Repeater](https://minecraft.wiki/w/Redstone_Repeater) · [Redstone Comparator](https://minecraft.wiki/w/Redstone_Comparator) · [Redstone Torch](https://minecraft.wiki/w/Redstone_Torch) — затримки, формули режимів, читання контейнерів, перегорання.
- [Esolangs: Minecraft](https://esolangs.org/wiki/Minecraft_(game)) — OR + NOT ⇒ будь-яка булева логіка; повнота за Тюрінгом за умови нескінченної «стрічки».
- [Wikipedia](https://en.wikipedia.org/wiki/Minecraft) — гра загалом.
- YouTube: пошук «minecraft redstone basics tutorial».

## Непевне
- (?) Ліміт поршня — 12 блоків у ряд; не відкривав сторінку Piston.
- (?) Тривалість імпульсу кнопок (камʼяна ≈1 с, деревʼяна ≈1,5 с) і спостерігача (1 р-тік).
- (?) Блок редстоуну як постійне джерело 15 — з власних знань.
- (?) Точний порядок обробки оновлень у Java і відмінності Bedrock — сторінка mechanics їх не розкриває.
- (?) Деталі debug-оверлею F3 щодо показу рівня сигналу.
