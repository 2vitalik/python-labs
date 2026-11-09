---
title: Virtual Circuit Board (VCB)
slug: virtual-circuit-board
aka: [VCB]
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: 2023
platforms: [PC (Windows, Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1885690/", best: true, note: "Reverie Foundry; пісочниця-симулятор логіки малюванням; потактовий сигнал; асемблер і Virtual Memory; шари декорацій"}
  - {kind: other, url: "https://github.com/kittybupu/openVCB", note: "openVCB — відкрита реалізація читача, асемблера й симулятора VCB (C++)"}
  - {kind: other, url: "https://raw.githubusercontent.com/kittybupu/openVCB/HEAD/openVCBPreprocessing.cpp", note: "як пікселі стають схемою: 4-звʼязні групи, Read/Write, Cross, Bundle"}
  - {kind: other, url: "https://raw.githubusercontent.com/kittybupu/openVCB/HEAD/openVCBSim.cpp", note: "такт: черга подій, правила вентилів, латч, годинник, VMem"}
  - {kind: other, url: "https://pkg.go.dev/github.com/paperdev-code/vcbtool@v0.0.0-20220529232843-2099c2063c39/pkg/vcb", note: "формат blueprint: список чорнил з кольорами, шари Logic / DecorOn / DecorOff, base64"}
  - {kind: other, url: "https://steamcommunity.com/app/1885690/guides/", note: "гайди спільноти: The Basics, blueprints, User Guide"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Virtual+Circuit+Board+VCB+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [in-game-editor, editor-palette, editor-draw-tools, cell-click, state-string, level-exchange, mode-indicator, game-screen, +logic-gates, +signal-propagation, +pixel-circuit-drawing, +crossing-bridge, +trace-bundle, +custom-assembly-language, +virtual-memory-bus, +decoration-state-layers, +self-built-cpu-runs-program, +mode-sandbox-only]
proposes: ["+trigger:signal(net)", "+cond:powered(net)", "+effect:power(net)", "+effect:toggle(a)", "+role:wire", "+window:assembly-editor", "+feature:blueprints", "+feature:breakpoints", "+axis:field-pixel", "+card:pixel-circuit-drawing", "+card:trace-bundle", "+card:virtual-memory-bus", "+card:decoration-state-layers"]
author: opus
date: 2026-11-09
---

# Virtual Circuit Board — малюєш схему пікселями кольорових «чорнил»: дроти, вентилі, латчі, а сигнал іде від компонента до компонента потактово; поверх — власний асемблер і віртуальна памʼять

## Суть
Пісочниця цифрової логіки від Reverie Foundry без рівнів, туторіалів і задач: гравець сам ставить собі ціль (лічильник, ALU, процесор). Схема — це піксельний малюнок: кожен колір-«чорнило» означає тип (дріт, вентиль, латч, годинник, світлодіод), а однокольорові сусідні пікселі злипаються в один компонент. Симулятор потактовий, до мільйонів оновлень на секунду; є редактор асемблера з власними інструкціями, програма якого лягає у «Virtual Memory», доступну схемі. Гра для тих, хто вже знає вентилі.

## Поле і час
- Полотно — піксельна сітка; клітина = піксель одного чорнила; звʼязність — лише 4 сусіди (діагональ не зʼєднує).
- Шари: логічний (чорнила) + два шари декорацій On / Off, що перекривають кольори залежно від стану компонента.
- Два режими: редагування (інструменти малювання, редактор асемблера) і симуляція (дивитись, клацати, бачити виконання інструкцій).
- Тік: сигнал переходить з компонента в компонент за один такт (у openVCB — два півкроки на такт, черга подій лише для змінених груп).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Trace (дріт) | terrain | 16 кольорів | 4-звʼязна група одного кольору — один провідник |
| Read | terrain | — | частина дроту; передає його стан сусіднім компонентам (вхід) |
| Write | terrain | — | частина дроту; отримує вихід сусідніх компонентів |
| Cross | static | — | сигнал проходить прямо крізь, не зливаючись з перпендикулярним дротом |
| Buffer | object | — | вмикається, якщо є будь-який активний вхід (затримка на такт) |
| OR / NOR | object | — | будь-який вхід / жоден вхід |
| AND / NAND | object | кількість входів | усі входи / не всі |
| XOR / XNOR | object | — | непарна / парна кількість активних входів |
| NOT | object | — | увімкнений, коли жоден вхід не активний |
| Latch | switch | стан on/off | перемикається, коли надходить непарне число фронтів; клік у симуляції перемикає |
| Clock | spawner | період | вмикається раз на період тактів |
| LED | static | палітра | світиться від входу — дисплей |
| Bundle (шина) | terrain | канали за кольором дроту | багатоканальний дріт: зʼєднує лише дроти однакового кольору |
| Filler / Annotation | mark | — | заповнювач і нотатки; без логіки |
| VMem | container | шина адреси + шина даних (латчі) | зміна адреси → дані з памʼяті; стабільна адреса → запис даних щотакту |
| Blueprint | container | base64-рядок, один шар | копія фрагмента схеми для вставки й обміну |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «на полотні намальовано чорнило»` → ТО `custom: «пікселі одного чорнила, що торкаються сторонами, — одна група-компонент»`.
- КОЛИ `custom: «змінився стан дроту»` → ЯКЩО `custom: «піксель Read цього дроту торкається вентиля»` → ТО `custom: «вентиль отримує подію на наступному півкроці»`.
- КОЛИ `custom: «змінився вихід вентиля»` → ЯКЩО `custom: «вентиль торкається пікселя Write дроту»` → ТО `custom: «дріт отримує новий стан»`.
- КОЛИ `tick` → ЯКЩО `custom: «тип OR/Buffer і ≥1 активний вхід»` → ТО `set_state(gate, on)`; NOR/NOT — `custom: «0 активних»`.
- КОЛИ `tick` → ЯКЩО `custom: «AND: активні всі входи»` → ТО `set_state(gate, on)`; NAND — навпаки.
- КОЛИ `tick` → ЯКЩО `custom: «XOR: непарна кількість активних; XNOR: парна»` → ТО `set_state(gate, on)`.
- КОЛИ `tick` → ЯКЩО `custom: «на латч прийшла непарна кількість зростаючих фронтів»` → ТО `set_state(latch, flip)`; спадні фронти ігноруються.
- КОЛИ `timer(period)` → ТО `set_state(clock, on)` на один такт.
- КОЛИ `custom: «сигнал дійшов до Cross»` → ТО `custom: «продовжує в тому ж напрямку через піксель»`.
- КОЛИ `custom: «дріт торкається Bundle»` → ТО `custom: «зʼєднаний з усіма дротами того ж кольору на кінцях шини»`.
- КОЛИ `custom: «змінилась адреса на латчах VMem»` → ТО `custom: «латчі даних = vmem[адреса]»`; ЯКЩО `custom: «адреса стабільна»` → ТО `custom: «vmem[адреса] = латчі даних»`.
- КОЛИ `input(assemble)` → ТО `custom: «текст асемблера з інструкціями гравця → вміст VMem»`.
- КОЛИ `input(click, latch)` (режим симуляції) → ТО `set_state(latch, flip)` — кнопки й перемикачі.
- КОЛИ `custom: «стан компонента змінився»` → ТО `custom: «показати піксель шару декорації On або Off»`.
- Перемога: нема — пісочниця · Поразка: нема · Рахунок: нема (міряють такти й розмір самі).

## Керування і ввід
- Малювання мишею: олівець вибраним чорнилом, інструмент Array — кілька паралельних дротів за раз, виділення й копіювання (?).
- Blueprints: фрагмент схеми як base64-рядок — вставити, поділитися.
- Перемикання режимів редагування / симуляції; у симуляції клік по компонентах, швидкість симуляції (?), точки зупинки (є в openVCB (?)).
- Редактор асемблера: гравець визначає власні інструкції та їхнє кодування.

## Вікна, меню, HUD
- `game-screen`: полотно, палітра чорнил (`element-picker`), панель режимів (`mode-toggle`).
- `assembly-editor` (custom): текст програми + опис інструкцій; виконання видно в симуляції.
- `help-window`: вбудований User Guide з розділами (за назвою гайда спільноти) (?).
- `settings-window` (?) — опису нема.

## Фічі поза полем
- `mode-sandbox` — єдиний режим: «no tutorials, levels or challenges».
- Шари декорацій On/Off для кнопок, підписів, дисплеїв, що реагують на стан.
- Обмін схемами через blueprint-рядки; спільнота робить набори компонентів (гайди «Advanced component blueprints», «Kyt's component toolkit»), мод-переклади.
- Ранній доступ з 20.05.2022, реліз 06.10.2023; бандл «Circuits & Assembly» з Mnemonimov.

## Варіації й родичі
- Логіка на пікселях: [wireworld](../build-sim/wireworld.md) (клітинний автомат), [kohctpyktop](kohctpyktop.md) (шари кремнію), [minecraft-redstone](../build-sim/minecraft-redstone.md).
- Драбина «вентилі → CPU → асемблер»: [turing-complete](turing-complete.md) (з рівнями й тестами); маршрутизатори чисел замість вентилів — [prime-mover](prime-mover.md).
- **Осі варіацій:** як будуєш (піксель-малюнок / компоненти на сітці / шари) · мета (пісочниця / рівні з тестами) · хто задає ISA (гравець / гра) · затримка (на компонент / на клітину / нуль).

## Цікавинки для курсу
- Парсер картинки: 4-звʼязні групи однакового кольору → граф компонентів — 🥉.
- Подієвий симулятор вентилів з лічильником активних входів (AND як «скільки ще бракує») — 🥈.
- Cross і Bundle: перетин без злиття й шина за кольором — 📎.
- Латч на фронтах і годинник з періодом — 📎.
- VMem: памʼять, що читається зміною адреси й пишеться стабільною адресою — 🥈.
- Асемблер з інструкціями гравця → памʼять схеми — 🥇.
- Blueprint: фрагмент полотна як base64-рядок — 🌱.

## Мапа на каталог
- Є: `in-game-editor` (уся гра — редактор) · `editor-palette` (чорнила) · `editor-draw-tools` (Array) · `cell-click` · `state-string` (blueprint-рядки) · `level-exchange` (обмін схемами) · `mode-indicator` (редагування / симуляція) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+pixel-circuit-drawing` «Схема — малюнок; колір пікселя = тип компонента» · interface/input · 🥉.
  - `+trace-bundle` «Шина: кілька каналів за кольором дроту» · game-logic/program · 📎.
  - `+virtual-memory-bus` «Памʼять, підключена до латчів адреси й даних» · game-logic/program · 🥈.
  - `+decoration-state-layers` «Шари декору On/Off за станом компонента» · interface/graphics · 📎.
  - `+mode-sandbox-only` «Гра без рівнів — лише пісочниця» · levels/progression · 🌱.
  - `+logic-gates`, `+signal-propagation`, `+crossing-bridge`, `+custom-assembly-language`, `+self-built-cpu-runs-program` — підтвердження.

## Пропозиції до словників
- `+trigger:signal(net)`, `+cond:powered(net)`, `+effect:power(net)` — підтвердження (Kohctpyktop, Turing Complete).
- `+effect:toggle(a)` — перемкнути двостанову сутність (латч).
- `+role:wire` — підтвердження.
- `+window:assembly-editor` — підтвердження (Turing Complete).
- `+feature:blueprints` — фрагменти як рядки для копіювання й обміну.
- `+feature:breakpoints` — зупинка симуляції на зміні стану.
- `+axis:field-pixel` — поле з пікселів, де сутність — злиплі однокольорові пікселі (підтвердження).
- `+card:pixel-circuit-drawing`, `+card:trace-bundle`, `+card:virtual-memory-bus`, `+card:decoration-state-layers` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Virtual Circuit Board](https://store.steampowered.com/app/1885690/) — «sandbox-only drawing-based logic simulator»; потактовий сигнал, асемблер і VMem, режими редагування/симуляції, Array, шари декорацій; дати раннього доступу й релізу.
- [openVCB](https://github.com/kittybupu/openVCB) — відкрита реалізація, сумісна з VCB; [Preprocessing](https://raw.githubusercontent.com/kittybupu/openVCB/HEAD/openVCBPreprocessing.cpp) (групи, Read/Write, Cross, Bundle) · [Sim](https://raw.githubusercontent.com/kittybupu/openVCB/HEAD/openVCBSim.cpp) (такт, правила вентилів, VMem) · [openVCB.h](https://raw.githubusercontent.com/kittybupu/openVCB/HEAD/openVCB.h) (перелік чорнил).
- [vcbtool (Go)](https://pkg.go.dev/github.com/paperdev-code/vcbtool@v0.0.0-20220529232843-2099c2063c39/pkg/vcb) — чорнила з кольорами (2022), шари Logic/DecorOn/DecorOff, blueprint base64.
- [Гайди Steam](https://steamcommunity.com/app/1885690/guides/) — список: The Basics, blueprints, User Guide, набори компонентів (самі гайди не відкрились — 429).

## Непевне
- (?) Семантика вентилів і такту взята з openVCB, а не з самої гри; автори openVCB заявляють сумісність, але точність не перевірено.
- (?) Чорнила пізніх версій (таймер, random, тунелі, mesh, бездротові, breakpoint) — у списках 2022 року їх нема; чи зʼявились до релізу 2023 — не знайдено.
- (?) Період годинника за замовчуванням (у openVCB — 2) і чи його можна змінити.
- (?) Інструменти редактора крім олівця й Array (заливка, виділення, undo), швидкість і крок симуляції.
- (?) Вбудований User Guide — існування видно лише з назви гайда спільноти.
