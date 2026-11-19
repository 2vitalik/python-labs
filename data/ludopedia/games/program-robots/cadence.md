---
title: Cadence (Made With Monster Love)
slug: cadence
aka: []
family: program-robots
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows), macOS, iOS (iPhone/iPad)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/362800/Cadence/", best: true, note: "опис режимів Puzzle / Sandbox, Тюрінг-повна логіка, Workshop; відео Gameplay & Overview"}
  - {kind: other, url: "https://www.thegeeklygrind.com/all-posts/cadence-review", note: "огляд 2026: напрямлені зʼєднання, блок «з двох боків», затримки, ворота на N кіл, Workshop"}
  - {kind: other, url: "https://www.pocketgamer.biz/cadence-musical-playgrounds-is-a-time-capsule-to-how-games-used-to-be-13-years-in-the-making/", note: "інтервʼю: блок = тон, 5 зон / 60 рівнів, редактор (2 синти + драм-машина, 4 доріжки, ноти з гами), відмова від «нескінченних петель»"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=362800&count=30&maxlength=3000", note: "Steam News (JSON): перехід 3D → 2D-сітка, Generator, Validator, instant lines, ~60 рівнів"}
  - {kind: other, url: "https://games.jayisgames.com/review/cadence.php", note: "огляд альфи 2014: 3D-вузли, конуси, мелодія-петля без початку й кінця, вузол тріскає від резонансу"}
  - {kind: other, url: "https://gamingonphone.com/news/cadence-lets-you-solve-circuits-and-compose-music-in-a-unique-minimalist-puzzle-experience-now-available-on-ios", note: "реліз на iOS: free-to-try, редактор із тими самими логічними плитками"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cadence+Made+With+Monster+Love+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, in-game-editor, editor-palette, sequential-levels, world-map, tutorial-window, settings-window, volume-control, game-screen, +signal-propagation, +logic-gates, +delay-line, +coincidence-gate, +loop-count-gate, +pulse-generator, +order-validator, +instant-line, +procedural-music, +scale-locked-notes, +multitrack-sequencer, +sandbox-mode, +workshop-sharing, +tooltips, +loop-detection, +live-edit-while-running]
proposes: ["+role:token", "+cond:simultaneous", "+feature:free-to-try-unlock", "+axis:signal", "+card:coincidence-gate", "+card:loop-count-gate", "+card:order-validator", "+card:scale-locked-notes"]
author: opus
date: 2026-11-19
---

# Cadence — схема з плиток на сітці: сигнал біжить зʼєднаннями, кожна плитка звучить нотою, а розвʼязаний пазл стає мелодією

## Суть
Мінімалістична головоломка соло-розробника Made With Monster Love (Peter Cardwell-Gardner, 12–13 років розробки): гравець складає з плиток схему, по якій біжить сигнал, і кожна плитка, яку сигнал проходить, звучить тоном — робоча схема й є мелодією. Мета рівня — добудувати схему так, щоб сигнал пройшов від початку до кінця й «розбудив» кота Рен у навушниках.

Плитки мають логіку: одні спрацьовують лише від сигналу з двох боків одночасно, інші затримують, треті тримають сигнал, доки той не пройде заданого числа кіл; є генератори й валідатори порядку. Поза кампанією — пісочниця-секвенсор до 4 доріжок і, за словами автора, Тюрінг-повна логіка.

## Поле і час
- З 2025 року — 2D-сітка плиток (раніше — абстрактне 3D-поле вузлів); автор: сітка зробила рівні «infinitely more readable», великі рівні розвʼязуються «one unit at a time».
- Сигнал іде напрямленими зʼєднаннями між плитками; крім звичайних, є «миттєві лінії» (instant lines) (?).
- Час `programmed`: схема працює сама (сигнал, затримки, кола); правити її можна, поки вона грає, — розвʼязок налагоджують наживо.
- Кампанія: 5 зон, ~60 рівнів (2–4 години); прогрес — на оверворлді режиму Play.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сигнал (імпульс) | object | позиція, напрям | біжить зʼєднаннями; проходячи плитку, змушує її звучати |
| Плитка-нота (блок) | conduit | тон (у пісочниці — автоматично з гами) | звучить, коли сигнал проходить, і передає його далі |
| Зʼєднання (лінія) | conduit | напрям; звичайне / миттєве | веде сигнал від плитки до плитки |
| Генератор | spawner | — | породжує сигнал; якщо вихід заблоковано — показує це |
| Блок «з двох боків» | switch | — | спрацьовує, лише коли сигнал приходить із двох боків одночасно |
| Затримка | conduit | тривалість (?) | тримає сигнал і відпускає пізніше |
| Ворота-лічильник | gate | N кіл | не пропускають сигнал, доки той не пройде N кіл |
| Перемикач | switch | стан | змінює шлях сигналу; анімується під час роботи схеми (?) |
| Тригер-плитка | switch | — | (?) спрацьовує від сигналу й діє на інші плитки |
| Валідатор | gate | очікуваний порядок | перевіряє, що секції зіграно в правильному порядку, «інакше…» |
| Рен (кіт у навушниках) | neutral | — | ціль рівня: прокидається від завершеної схеми; коментує після рівня; реагує на курсор |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tile)` → ЯКЩО `free(cell)` → ТО `place(player, tile)`; у пісочниці — `custom: «плитка сама бере ноту з обраної гами»`.
- КОЛИ `input(drag, tile_a → tile_b)` → ТО `custom: «напрямлене зʼєднання А → Б»`.
- КОЛИ `input(activate, tile)` → ТО `spawn_at(signal, tile)` — «увімкнути плитку» й нарощувати схему (?).
- КОЛИ `timer(every)` → ТО `spawn_at(signal, generator)`; ЯКЩО `not free(generator_out)` → ТО `custom: «генератор показує, що заблокований»`.
- КОЛИ `enter(signal, note_tile)` → ТО `sound(note)`, `move(signal, connection)`.
- КОЛИ `enter(signal, delay)` → ТО `stun(signal, n)` (?).
- КОЛИ `enter(signal, coincidence_block)` → ЯКЩО `custom: «другий сигнал прийшов з іншого боку в той самий момент»` → ТО `move(signal, out)`; інакше `custom: «чекає або гасне»` (?).
- КОЛИ `enter(signal, loop_gate)` → ЯКЩО `counter(loops, <, n)` → ТО `block`, `counter(loops, +1)`; інакше `move(signal, out)`.
- КОЛИ `enter(signal, validator)` → ЯКЩО `custom: «секції зіграно в правильному порядку»` → ТО `move(signal, out)`; інакше `custom: «збій схеми (or else…)»` (?).
- КОЛИ `custom: «сигнал згас або застряг, не дійшовши до мети»` → ТО `custom: «рішення зупиняється на півдорозі»` — гравець править схему наживо.
- КОЛИ `custom: «схема завершена — сигнал доходить до мети»` → ТО `win`, `custom: «відкривається мелодія рівня»`, `message(коментар Рен)` (можна пропустити), `unlock(next_levels)`.
- Альфа 2014: КОЛИ `input(click, node)` → ТО `sound(note)`, `spawn_at(pulse, node)`; конус — `custom: «шле імпульс лише до одного заданого вузла»`.
- Альфа 2014: КОЛИ `pattern(loop_closed)` (усі вузли збуджують один одного без кінця) → ТО `win`; КОЛИ `custom: «резонанс без виходу накопичився у вузлі»` → ТО `destroyed(node)`, `lose`.
- Перемога: завершена схема, Рен прокинувся · Поразка: формально нема — схема «зупиняється», правиш далі · Рахунок: не згадано (?).

## Керування і ввід
- Миша (PC), тач (iPhone, iPad); огляд 2026 грали на Steam Deck.
- Розстановка плиток на сітку й напрямлені зʼєднання; в альфі 2014 — протяг лінії мишею між вузлами й клік, що «пінгує» вузол.
- Схему правлять, поки вона грає.
- Підказки-тултіпи на всіх плитках у Play-режимі (баченні запамʼятовуються між сесіями); кнопка Help показує або ховає тултіпи.
- Рен реагує на курсор — його можна погладити.

## Вікна, меню, HUD
- `map-window` — оверворлд режиму Play: зони й рівні, прогрес.
- `game-screen`: сітка плиток, `tool-palette`, `tooltip`, кнопка Help, Рен.
- `editor-window` — пісочниця (Creative / Sandbox): до 4 доріжок, 2 синтезатори й драм-машина, пресети синтезатора Helm; ті самі логічні плитки, «graph-based sequencing».
- `settings-window`: повзунки гучності, скидання прогресу.
- `credits-window` — титри (з 2025).
- `custom-window` Workshop — імпорт рівнів спільноти одним кліком (Steam).
- `dialogue-window` — філософські коментарі Рен після рівня, їх можна пропустити.

## Фічі поза полем
- `levels-sequential` (5 зон, ~60 рівнів) + `world-map` (оверворлд).
- `mode-sandbox` / `level-editor` + `level-sharing` (Steam Workshop; на iOS обміну поки нема).
- `tutorial`, `onboarding-hints` — тултіпи плиток.
- `volume-sliders`, скидання прогресу; `localization` — 7 мов (EN, FR, DE, JA, PT-BR, RU, ZH-CN).
- iOS — безкоштовна частина й одноразова покупка повної гри.
- Undo, метрики рішення й рахунок у джерелах не згадано (?).

## Варіації й родичі
- Історія: прототип Synesthesis (Ludum Dare) → альфа 2014 (браузерне демо, 3D-вузли, ціль — нескінченна петля) → Steam-демо 2021 і бета з Workshop → 2025: 2D-сітка, Generator, instant lines, Validator → реліз 12.02.2026 (Steam, iOS).
- Автор відмовився від «петлі як мети»: код виявлення циклів був, але гравцям це було «too abstract and confusing».
- У корпусі: [Turing Tumble](turing-tumble.md) — механічний компʼютер, де сигнал (кулька) проходить деталь і перемикає її; [Factorio circuit network](factorio-circuit-network.md) і [Minecraft — редстоун](../build-sim/minecraft-redstone.md) — затримки, вентилі, памʼять; [Wireworld](../build-sim/wireworld.md) — сигнал провідником.
- Осі варіацій: мета «нескінченна петля (альфа) / сигнал доходить до мети (реліз)»; нота «вузол за кліком / плитка під сигналом»; логіка «І за збігом / лічильник кіл / затримка / валідатор порядку»; поле «3D-граф вузлів (альфа) / 2D-сітка (реліз)».

## Цікавинки для курсу
- Сигнал як токен, що біжить напрямленим графом плиток, і кожна плитка грає ноту — 🥉 (симуляція + звук).
- Вентиль «І» за збігом двох сигналів в один момент — 📎.
- Ворота-лічильник «пропустити після N кіл» і затримка — 📎 кожне.
- Валідатор порядку секцій (перевірка послідовності подій) — 🥉.
- Виявлення нескінченної петлі в графі вузлів (мета альфи) — 🥉.
- Секвенсор пісочниці: 4 доріжки, ноти автоматично з гами — 🥈.
- Калькулятор із плиток як доказ Тюрінг-повноти — 👑.

## Мапа на каталог
- Є: `cell-click` ↔ розстановка плиток · `in-game-editor` + `editor-palette` ↔ пісочниця · `sequential-levels` + `world-map` ↔ 5 зон / ~60 рівнів на оверворлді · `tutorial-window` ↔ навчання · `settings-window` + `volume-control` ↔ гучність, скидання прогресу · `game-screen`.
- **Нема** → пропозиції карток:
  - `+signal-propagation` · `+logic-gates` · `+delay-line` (повтори).
  - `+coincidence-gate` «Плитка спрацьовує від двох сигналів одночасно» · game-logic · 📎.
  - `+loop-count-gate` «Ворота пропускають після N кіл сигналу» · entities/state · 📎 · слот {n}.
  - `+pulse-generator` «Генератор імпульсів із видимим блокуванням» · entities/spawn · 🌱.
  - `+order-validator` «Перевірка порядку подій» · game-logic/win · 🥉.
  - `+instant-line` «Миттєве зʼєднання поряд із тактовим» · entities/move · 🌱.
  - `+procedural-music` (повтор) — схема = мелодія.
  - `+scale-locked-notes` «Плитки самі беруть ноти з гами» · interface/sound · 📎.
  - `+multitrack-sequencer` «Секвенсор до N доріжок» · interface/sound · 🥈 · слот {tracks: 4}.
  - `+sandbox-mode` · `+workshop-sharing` · `+tooltips` · `+loop-detection` (повтори).
  - `+live-edit-while-running` «Правка схеми під час виконання» · game-logic/program · 📎.

## Пропозиції до словників
- `+role:token` — сигнал чи імпульс як рухома сутність без волі (повтор із Turing Tumble).
- `+cond:simultaneous` — два сигнали прийшли в той самий момент (повтор із Trainyard).
- `+feature:free-to-try-unlock` — безкоштовна частина гри й одноразова покупка решти (iOS).
- `+axis:signal` — гра про проходження сигналу полем (значення ще не усталені).
- `+card:coincidence-gate`, `+card:loop-count-gate`, `+card:order-validator`, `+card:scale-locked-notes` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Cadence](https://store.steampowered.com/app/362800/Cadence/) — Puzzle Mode (мелодії будять Рен), Sandbox Mode (повний редактор), Тюрінг-повна логіка, Workshop; відео «Cadence Gameplay & Overview».
- [The Geekly Grind: огляд](https://www.thegeeklygrind.com/all-posts/cadence-review) — напрямлені зʼєднання від початку до кінця, блоки «з двох боків», затримки, ворота на N кіл, перемикачі, налагодження наживо, Workshop.
- [PocketGamer.biz: інтервʼю](https://www.pocketgamer.biz/cadence-musical-playgrounds-is-a-time-capsule-to-how-games-used-to-be-13-years-in-the-making/) — «each block creates a musical tone», 5 зон / 60 рівнів, відмова від нескінченних петель, редактор: 2 синти + драм-машина, 4 доріжки, ноти з гами.
- [Steam News (JSON)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=362800&count=30&maxlength=3000) — девлоги 2018–2026: 3D → 2D-сітка, Generator, Validator, instant lines, trigger tiles, тултіпи, Helm, Рен.
- [JayIsGames (2014)](https://games.jayisgames.com/review/cadence.php) — альфа: 3D-вузли з нотами, конуси, петля без початку й кінця, руйнування вузла резонансом, прототип Synesthesis.
- [Gaming on Phone](https://gamingonphone.com/news/cadence-lets-you-solve-circuits-and-compose-music-in-a-unique-minimalist-puzzle-experience-now-available-on-ios) — iOS-реліз, free-to-try, редактор із тими самими логічними плитками.
- [Pocket Gamer: превʼю](https://www.pocketgamer.com/cadence/cadences-abstract-musical-puzzles-are-hard-to-explain-but-a-joy-to-listen-to) — сфери й квадрати, звʼязані лініями; розвʼязок — нескінченна музична петля; розвʼязків кілька.
- [Electron Dance](https://www.electrondance.com/?p=18571) — коментар до демо: петля, що безперервно живить кота ритмом; «loads of block types».
- YouTube: пошук «Cadence Made With Monster Love gameplay».

## Непевне
- (?) Повний список плиток релізу: огляди описують поведінку без назв; назви Generator, Validator, trigger tiles, switch, instant lines — з девлогів, без точних правил.
- (?) Як іде сигнал: потактово (у ритмі) чи безперервно; що саме робить «миттєва лінія».
- (?) Точна умова перемоги релізу — «сигнал від початку до кінця» (огляд 2026) чи «петля, що грає безперервно» (коментар до демо).
- (?) Що відбувається при помилці валідатора («or else…»).
- (?) Чи зʼєднання лише між сусідніми клітинами, чи довільні лінії (тоді поле — радше граф поверх сітки).
- (?) Android: Pocket Gamer згадує, а розробник у червні 2025 писав, що це «залежить від запуску».
- (?) Наявність undo, метрик рішення, рахунку.
- (?) Правила альфи 2014 (конуси, резонанс) — з одного огляду; у релізі їх, імовірно, нема.
