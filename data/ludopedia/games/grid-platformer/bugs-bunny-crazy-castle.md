---
title: The Bugs Bunny Crazy Castle
slug: bugs-bunny-crazy-castle
aka: [Roger Rabbit (FDS), ロジャー・ラビット, Mickey Mouse (Game Boy JP), ミッキーマウス, Crazy Castle]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 1989
platforms: [Famicom Disk System, NES, Game Boy]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Bugs_Bunny_Crazy_Castle", best: true, note: "без стрибка, 8 морквин, очки, предмети, таблиця ШІ ворогів (хто ходить сходами/дверима/трубами), версії й сиквели"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ロジャー・ラビット_(コンピュータゲーム)", note: "FDS Roger Rabbit: серця замість морквин, 60 стадій, пароль 4 символи, 1-Up за стадію"}
  - {kind: other, url: "https://gamesurge.com/strategies/Gameboy/Manuals/Bugsbunnycastle.shtml", note: "мануал Game Boy: кнопки, сходи/двері/труби, предмети, 5 життів, знак No Carrot, пароль, continue, VIDEO-повтор"}
  - {kind: other, url: "https://www.video-games-museum.com/en/faqs/Nes/4014-Bugs-Bunny-Crazy-Castle-The.pdf", note: "FAQ NES (Snow Dragon): розвʼязки всіх 60 рівнів, поведінка рукавиці, рожевий Сильвестр ходить лише коли ходить Бакс"}
  - {kind: other, url: "https://www.classic-games.net/nes/the-bugs-bunny-crazy-castle", note: "огляд NES: сходи проходяться автоматично, ковзання, три теми рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bugs+Bunny+Crazy+Castle+NES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, ladder-climb, gravity-fall, teleport-pair, push-object, projectile-shot, temporary-modes, chase-player, enemy-patrol, touch-death, player-death, item-pickup, collect-all, goal-counter, event-points, sequential-levels, level-password, game-over-continue, replay, game-pause, player-camera, +no-jump, +pipe-travel, +crush-by-fall, +mimic-copy, +connector-permissions, +glove-drops-at-wall, +life-per-level]
proposes: ["+trigger:pushed_off", "+cond:can_use(enemy, connector)", "+effect:copy_input", "+card:connector-permissions", "+card:no-jump", "+card:glove-drops-at-wall", "+card:life-per-level", "+window:level-clear-menu"]
author: opus
date: 2026-11-09
---

# The Bugs Bunny Crazy Castle — кролик без стрибка збирає 8 морквин у замку сходів, дверей і труб, а кожен тип ворога вміє не всі переходи

## Суть
Багатоповерховий платформер-лабіринт: Бакс (у Японії — Роджер Реббіт або Міккі) мусить зібрати всі 8 морквин рівня, але **не вміє стрибати**. Поверхи зʼєднані сходами, дверима й трубами, і головна хитрість — у тому, що **кожен тип ворога користується лише частиною переходів**: один не ходить у двері, інший не піднімається назад сходами, третій стоїть, доки не рушиш ти. Зброї за замовчуванням нема: рукавиця-снаряд, морквяний сік невразливості й важкі предмети (сейф, ящик, відро, гиря), які штовхають у ворога або скидають на нього з уступу.

## Поле і час
- Рівень — тайлова сітка поверхів збоку з горизонтальною прокруткою (EN-вікі: side-scrolling); поверхи, сходи, двері, входи труб, уступи й вузькі шахти.
- Видимість часткова: камера показує частину рівня, тож падіння з уступу іноді «наосліп» (FAQ, рівні 22–23).
- Real-time; вороги рухаються безперервно, частина — з паузами.
- Гравітація: зійшов з краю — падаєш на нижній поверх; стрибка нема.
- Три теми оформлення рівнів (огляд classic-games.net).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бакс / Роджер / Міккі | player | 5 життів (GB) | ходить ліворуч/праворуч, сходи/двері/труби — вгору/вниз; штовхає предмети; не стрибає |
| Морквина (FDS — серце) | pickup | 100 очок | 8 на рівень; остання дає 1-Up і завершує рівень |
| Сходи | terrain | — | вхід з підніжжя/верху; Бакс проходить їх автоматично майже до кінця |
| Двері | gate | — | ведуть на інший поверх (вгору/вниз біля дверей) |
| Труба | terrain | два кінці | вхід — вихід з іншого кінця; бувають кільцеві маршрути |
| Рукавиця | pickup | 500 очок за ворога | узяв — B кидає її прямо; у ворога — обидва зникають; у стіну — лягає біля неї |
| Морквяний сік | pickup | 100 очок за ворога | тимчасова невразливість: дотик вбиває ворога |
| Сейф / ящик / відро / гиря | object | 1000 очок за ворога | штовхається; б'є ворога в русі або падає на нього з уступу |
| Знак «No Carrots» | hazard | — | NES: смерть від дотику; GB: перекидає на спецрівень |
| Сірий Сильвестр | enemy | до 2 на рівень | ходить без зупинок; двері й труби — ні; під сходи не заходить |
| Зелений Сильвестр | enemy | — | вгору/вниз поверхами й трубами, двері й труби проходить, під сходи — так; без зупинок, снує між поверхами |
| Рожевий Сильвестр | enemy | — | лише вгору; двері й труби — ні; інколи завмирає й рушає туди ж, куди Бакс |
| Йосеміті Сем, Вайл І. Койот | enemy | — | двері й труби — ні; спустившись сходами, назад не піднімаються; без зупинок |
| Даффі Дак | enemy | — | як Сем, але з паузами й копіюванням напрямку Бакса |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(bugs, dir)`; стрибка нема.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, stairs_end)` → ТО `custom: «Бакс автоматично проходить сходи»`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, door)` → ТО `teleport(bugs, door_other_floor)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, pipe_mouth)` → ТО `teleport(bugs, pipe_other_end)`.
- КОЛИ `tick` → ЯКЩО `not supported(bugs)` → ТО `fall(bugs)` — сходити з уступів можна й потрібно.
- КОЛИ `contact(bugs, carrot)` → ТО `pickup`, `score(100)`, `counter(carrots, +1)`.
- КОЛИ `counter(carrots, ==, 8)` → ТО `lives(+1)`, `win`, `message(password)`, `next_level`.
- КОЛИ `picked(bugs, glove)` → ТО `give(bugs, glove)`; КОЛИ `input(B)` → ЯКЩО `has(bugs, glove)` → ТО `spawn_at(glove_shot, front)`, `custom: «летить прямо в напрямку погляду»`.
- КОЛИ `contact(glove_shot, enemy)` → ТО `disappear_both`, `score(500)`.
- КОЛИ `blocked(glove_shot)` → ТО `transform(glove_shot, glove)` — лягає біля стіни, можна підняти знову.
- КОЛИ `contact(bugs, heavy_object)` → ТО `push`.
- КОЛИ `contact(heavy_object, enemy)` → ЯКЩО `custom: «предмет у русі від поштовху»` → ТО `disappear(enemy)`, `score(1000)`.
- КОЛИ `custom: «предмет зіштовхнуто з уступу»` → ТО `fall(heavy_object)`; КОЛИ `contact(heavy_object, enemy)` → ТО `disappear(enemy)`, `score(1000)`.
- КОЛИ `picked(bugs, carrot_juice)` → ТО `set_state(bugs, invincible, n)`.
- КОЛИ `contact(bugs, enemy)` → ЯКЩО `state(bugs, invincible)` → ТО `disappear(enemy)`, `score(100)`; інакше `lives(-1)`, `restart`.
- КОЛИ `contact(bugs, no_carrot_sign)` → ЯКЩО `mode(NES)` → ТО `lives(-1)`; ЯКЩО `mode(GB)` → ТО `custom: «спецрівень: пройшов — +3 життя, ні — назад на 3 рівні»`.
- КОЛИ `enter(enemy, door|pipe)` → ЯКЩО `custom: «тип не вміє цей перехід (усі, крім зеленого Сильвестра)»` → ТО `block`.
- КОЛИ `custom: «Сем / Койот / Даффі спустилися сходами»` → ТО `custom: «назад угору цими сходами не підуть»`.
- КОЛИ `rng(p)` → ЯКЩО `custom: «рожевий Сильвестр або Даффі»` → ТО `set_state(enemy, waiting)`.
- КОЛИ `input(dir)` → ЯКЩО `state(enemy, waiting)` → ТО `clear_state(enemy, waiting)`, `custom: «ворог рушає в той самий бік, що й Бакс, якщо може»`.
- КОЛИ `custom: «ворог зайшов у трубу»` → ТО `custom: «довго кружляє трубами»` — FAQ: трубою відводять зеленого Сильвестра.
- КОЛИ `counter(lives, ==, 0)` → ТО `window(game-over-continue)` (GB): YES — з поточного рівня, інакше з рівня 1.
- Перемога: усі 8 морквин на кожному з 60 рівнів (GB — 80). · Поразка: 0 життів. · Рахунок: морквина 100, ворог соком 100, рукавицею 500, важким предметом 1000.

## Керування і ввід
- Хрестовина: ліво/право — хід; вгору/вниз — сходи, двері, труби.
- B (NES) — кинути рукавицю; на Game Boy рукавицю кидають і A, і B.
- START — пауза (GB: SELECT або START — продовжити).
- Пароль: вгору/вниз — символ, ліво/право — позиція, START — підтвердити.
- Огляд скаржиться на ковзання Бакса після кожної дії — точність руху теж частина складності.

## Вікна, меню, HUD
- `splash-screen` / титул: START.
- `main-menu` (GB): почати з рівня 1 або ввести пароль.
- `level-password`: 4 символи (FDS — буквено-цифрові).
- `game-screen`: рівень з прокруткою; HUD — очки, життя, морквини (?).
- `pause-menu`: пауза START.
- `custom-window` після рівня: пароль; GB — вибір VIDEO (миттєвий повтор) або наступний рівень → `replay-window`.
- `game-over-continue` (GB): YES / NO.
- `end-screen`: фінальна сценка, потім гра з початку.
- Переходи: титул → main-menu → (пароль) → game-screen → (8 морквин) екран пароля/VIDEO → наступний рівень; 0 життів → continue.

## Фічі поза полем
- `levels-sequential`: 60 рівнів (FDS/NES), 80 (GB); паролі на кожен рівень замість збереження.
- `continue` (GB) з поточного рівня; 1-Up за кожен пройдений рівень.
- `replay`: VIDEO-повтор щойно пройденого рівня (GB).
- Спецрівень за знак «No Carrot» (GB) як ризик-ставка: +3 життя або −3 рівні.
- Нема збереження, редактора, мультиплеєра.

## Варіації й родичі
- Версії: Roger Rabbit (FDS, 1989, серця) → The Bugs Bunny Crazy Castle (NES, 1989); Game Boy: Mickey Mouse (JP, 1989, 80 рівнів) → Bugs Bunny (1997 JP / 1998 US).
- Серія: Crazy Castle 2, 3, 4, спін-оф Woody Woodpecker in Crazy Castle 5; японська лінія Mickey Mouse II–V (EN-вікі).
- Родичі в корпусі: [Space Panic](space-panic.md) (поверхи й драбини без стрибка), [BurgerTime](burgertime.md), [Lode Runner](lode-runner.md) (без стрибка, вороги з обмеженими маршрутами), [Mappy](mappy.md) (двері як зброя й переходи між поверхами).
- Осі варіацій:
  - **переходи між поверхами**: драбини (Space Panic) / сходи + двері + труби (Crazy Castle) / батути (Mappy);
  - **хто яким переходом користується**: усі однаково / таблиця «тип ворога × перехід» (Crazy Castle);
  - **як убити ворога**: ніяк, лише втікати / снаряд / невразливість / важкий предмет (штовхнути або скинути).

## Цікавинки для курсу
- Таблиця «тип ворога × тип переходу» (сходи вгору/вниз, двері, труби) як дані для ШІ — 🥉 (граф поверхів з дозволами на ребра).
- Ворог, що чекає й рушає в той самий бік, що й гравець — 📎.
- Важкий предмет: штовхнути у ворога або зіштовхнути з уступу, щоб упав на нього — 📎.
- Рукавиця-снаряд: у ворога — зникає, у стіну — знову стає предметом — 🌱.
- Труби як мережа порталів з кільцевими маршрутами — 📎.
- Платформер без стрибка: рух лише ходою, переходами й падінням — 🌱.
- Ставка «No Carrot»: спецрівень +3 життя / −3 рівні — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `ladder-climb` (сходи як єдиний вертикальний хід, крім падіння) · `gravity-fall` · `teleport-pair` (двері й кінці труб) · `push-object` · `projectile-shot` (рукавиця) · `temporary-modes` (сік) · `chase-player` · `enemy-patrol` (сірий Сильвестр) · `touch-death` · `player-death` · `item-pickup` · `collect-all` · `goal-counter` (?) · `event-points` · `sequential-levels` · `level-password` · `game-over-continue` · `replay` · `game-pause` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+connector-permissions` «Тип ворога × перехід: хто ходить сходами, дверима, трубами» · entities/move · 🥉 · слоти {connectors, types}.
  - `+no-jump` «Платформер без стрибка» · entities/move · 🌱.
  - `+glove-drops-at-wall` «Снаряд, що влучив у стіну, лягає як предмет» · entities/combat · 🌱.
  - `+life-per-level` «1-Up за кожен пройдений рівень» · game-logic/score · 🌱.
  - `+pipe-travel` · `+crush-by-fall` · `+mimic-copy` — уже пропоновані в корпусі.

## Пропозиції до словників
- `+trigger:pushed_off(object)` — предмет зіштовхнуто з уступу (Crazy Castle, Fire 'n Ice).
- `+cond:can_use(enemy, connector)` — тип ворога має дозвіл на перехід (сходи/двері/труба).
- `+effect:copy_input(a)` — сутність повторює наступний напрямок гравця (рожевий Сильвестр, Даффі).
- `+window:level-clear-menu` — екран між рівнями з паролем і вибором VIDEO / далі.
- `+card:connector-permissions`, `+card:no-jump`, `+card:glove-drops-at-wall`, `+card:life-per-level` — див. вище.

## Джерела
- ⭐ [Wikipedia: The Bugs Bunny Crazy Castle](https://en.wikipedia.org/wiki/The_Bugs_Bunny_Crazy_Castle) — без стрибка, 60/80 рівнів, 8 морквин, очки, предмети, детальна таблиця ШІ ворогів, паролі, регіональні версії, сиквели.
- [Wikipedia JA: ロジャー・ラビット](https://ja.wikipedia.org/wiki/ロジャー・ラビット_(コンピュータゲーム)) — FDS: серця, 60 стадій, очки за рукавицю/предмет, 1-Up за стадію, пароль 4 символи.
- [Мануал Game Boy (GameSurge)](https://gamesurge.com/strategies/Gameboy/Manuals/Bugsbunnycastle.shtml) — кнопки, сходи/двері/труби, предмети, 5 життів, знак No Carrot і спецрівень, пароль, continue, VIDEO.
- [FAQ NES (Snow Dragon, VGM)](https://www.video-games-museum.com/en/faqs/Nes/4014-Bugs-Bunny-Crazy-Castle-The.pdf) — розвʼязки 60 рівнів; рукавиця біля стіни, сік, падіння з уступів, рожевий Сильвестр і Даффі рухаються лише разом з Баксом, «No Carrots» убиває.
- [classic-games.net: огляд NES](https://www.classic-games.net/nes/the-bugs-bunny-crazy-castle) — автоматичні сходи, ковзання, три теми.
- YouTube: пошук «Bugs Bunny Crazy Castle NES gameplay».

## Непевне
- (?) Таблиця ШІ з EN-вікі місцями суперечлива («сірий ходить лише вгору поверхом або трубою, але не проходить труби»): точне значення «bypass doors/tubes» і «go under stairs» не перевірено.
- (?) Фраза мануалу GB «safely pass... through doorways and pipes» — чи то Бакс безпечно розминається з ворогами в переходах, чи вороги проходять переходи; FAQ радить «заходити в трубу разом із зеленим Сильвестром, щоб не загинути».
- (?) Пошуковий підсумок: «гиря рухається на 1 клітину за поштовх, сейф — на 2», «морквини відкривають ключ до виходу» — не підтверджено відкритим джерелом (ключ, ймовірно, із сиквелів).
- (?) Чи шкодить падіння з великої висоти; тривалість соку; склад HUD; чи двері — пара «вгору/вниз» чи ведуть далі.
- (?) Різниця «No Carrots» між NES (смерть) і GB (спецрівень) — за двома різними джерелами; для FDS — невідомо.
