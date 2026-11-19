---
title: Star Stuff
slug: star-stuff
aka: [Star Stuff Edu]
family: program-robots
also: [thinky]
klass: hybrid
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC, Mac, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1955110/Star_Stuff/", best: true, note: "Ánimo Games Studio / Exothermic, 07.06.2024; 150+ пазлів зоряної фабрики: програмуєш ботів і сам ходиш поруч, синхронно з ними; reset / undo; знімки: ізометричні кімнати, панель програми «V1 = Nearest», «if V1 is on», «jump to», клавіші z rewind / shift fast forward / space interact / r reset"}
  - {kind: wiki, url: "https://starstuff.exothermic.wiki/Levels", note: "розділи й секції: Nebula Nook (Orientation, Hold On, Teamwork) … Blue Luminous Sector (Branching, Monitoring, Parallel Processing)"}
  - {kind: wiki, url: "https://starstuff.exothermic.wiki/Puzzle_Guides:Nebula_Nook", note: "команди go to / pick up at / drop at / wait for; Walker і Grabber; кнопки, перемикачі, air bump, мости, ліфти"}
  - {kind: wiki, url: "https://starstuff.exothermic.wiki/Puzzle_Guides:Blue_Luminous_Sector", note: "умови if holding / if lasering / if X is on, цикли jump to, паралельні програми кількох ботів"}
  - {kind: wiki, url: "https://starstuff.exothermic.wiki/Puzzle_Guides:Red_Giant_Room", note: "змінні d1 = nearest X, Spawner Bot і spawn, сфери-орби, фінал"}
  - {kind: play, url: "https://www.starstuffedu.org", note: "Star Stuff Edu — безкоштовна браузерна версія для шкіл; WASD / стрілки, Space — взаємодія й запуск коду, Shift — швидше, Z — перемотка, P — пауза / вихід з термінала, TAB — інший бот"}
  - {kind: official, url: "https://www.animogames.org", note: "студія: Star Stuff Edu, превʼю на CrazyGames, нагорода GEE"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Star+Stuff+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [command-program, sensor-predicates, step-execution, code-editor-window, button-toggle, carrier-platform, beam-tracing, destructible-blocks, spawner-entity, rewind, restart-level, undo-redo, keyboard-controls, sequential-levels, game-screen, +avatar-plus-bots, +named-target-commands, +wait-for-condition, +jump-labels, +nearest-variable, +swarm-same-program, +carry-object, +bot-breakdown, +jump-pad, +hub-world, +edu-version]
proposes: ["+effect:wait", "+effect:jump(step)", "+effect:assign(var, nearest(kind))", "+window:terminal", "+ui:key-hints-bar", "+feature:edu-version", "+axis:control", "+axis:actors", "+card:avatar-plus-bots"]
author: opus
date: 2026-11-19
---

# Star Stuff — пишеш ботам програму з іменованими цілями, а сама біжиш кімнатою й допомагаєш їм у реальному часі

## Суть
Затишний пазл про зоряну фабрику: героїня Mija, новенька інженерка, проходить ізометричні кімнати-діорами з ящиками, кнопками, мостами, ліфтами й лазерами. Ботам (ходок, вантажник, лазерний, спавнер) вона пише короткі програми з командами на кшталт `pick up at: A button`, `wait for: C switch`, `jump to: step 1`, а потім **сама діє в кімнаті одночасно з ними**: стає на кнопки, переносить ящики, блокує тілом промінь чи шлях бота. Рівень пройдено, коли Mija дійшла до виходу. Огляд GEE називає гру «Sokoban-style» з псевдокодом; клас `hybrid` — аватар плюс програмовані помічники.

## Поле і час
- Кожен пазл — одна кімната-діорама з квадратних плит на кількох висотах (ліфти, драбини, мости), камера ізометрична; обʼєкти стоять на плитах. Цілі програм — іменовані місця: «A button», «C position», «B crate pad», «D hopper».
- Шари: плити й прірви · кнопки, майданчики, air bump, електричні майданчики · ящики й аерогель · боти й Mija.
- Час `realtime`: програми ботів ідуть безперервно, поки Mija рухається; є прискорення (Shift), перемотка назад (Z), пауза, скидання (R).
- Детерміновано; один автор вікі пише, що одне розвʼязання з таймінгом аерогелю «спрацьовує не завжди».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mija | player | — | ходить, бере й несе ящик або аерогель, ставить на кнопку чи майданчик, тисне перемикачі, їздить ліфтами, злітає з air bump; тілом блокує промінь і шлях бота |
| Walker Bot | ally | програма | `go to` / `wait for`; стоїть на кнопці; ламається, якщо його заблокувати чи він став на електричний майданчик, і далі стоїть як перешкода |
| Grabber Bot | ally | програма | `pick up at` / `drop at`: переносить ящики, аерогель і навіть Mija; може застрягти над кнопкою й тримати її |
| Laser Bot | ally | напрямок | `turn: clockwise / counter-clockwise`; промінь плавить аерогель, бачить ящики й цілі, може спалити бота; ящик, бот чи Mija промінь перекривають |
| Spawner Bot | spawner | програма | `spawn` — створює нових ботів, часто після `wait for` |
| Ящик | object | — | несуть Mija і грабер; тисне кнопку; перекриває промінь і прохід |
| Аерогель | object | — | переноситься; під променем лазера з часом тане |
| Кнопка (A…F) | switch | літера | увімкнена, поки на ній стоїть Mija, бот чи ящик; вмикає мости й ліфти |
| Перемикач (C…F) | switch | літера | Mija перемикає; змінює мости, лазери, ліфти |
| Майданчик, бункер, ціль, позиція | zone | літера | місця доставки й маршруту; стан «on», коли зайняті |
| Міст | gate | світиться / ні; деякі обвалюються чи перекидаються | прохідний, коли світиться |
| Ліфт | platform | — | возить між висотами; деякі опускаються від стану лазера чи кнопки |
| Air bump | terrain | — | підкидає Mija, ящик чи бота в інше місце |
| Електричний майданчик | hazard | — | ходок на ньому ламається |
| Сфера (orb) | switch | літера | розділ Starburst: переносить Mija чи ботів між секціями |
| Вихід (goal) | static | — | Mija дійшла — рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(go to: X)` → ТО `move(bot, X)` — бот сам іде до іменованого місця.
- КОЛИ `exec(pick up at: X)` → ЯКЩО `occupied(X, crate|aerogel|mija)` → ТО `pickup(bot, item)`, `carry(bot, item)`.
- КОЛИ `exec(drop at: X)` → ЯКЩО `has(bot, item)` → ТО `place(bot, item)` у X.
- КОЛИ `exec(wait for: X)` → ТО `custom: «бот стоїть, доки X не стане on»`.
- КОЛИ `state_on(X, on)` → ЯКЩО `state(bot, waiting_for_X)` → ТО `custom: «бот іде до наступного кроку»`.
- КОЛИ `exec(turn: clockwise)` → ТО `rotate(laser_bot, 90)`; `counter-clockwise` — у протилежний бік.
- КОЛИ `exec(jump to: step N)` → ТО `custom: «перейти на крок N»` — так робляться цикли.
- КОЛИ `exec(if C)` → ЯКЩО `has(bot, item)` / `line_of_sight(laser_bot, target|crate)` / `state(X, on)` (і заперечення `not`) → ТО виконати вкладені кроки; інакше пропустити їх.
- КОЛИ `exec(d1 = nearest K)` → ТО `custom: «змінна d1 = найближчий обʼєкт виду K»`; далі d1 стає ціллю команд go to чи pick up at.
- КОЛИ `exec(spawn)` → ТО `spawn(bot)`.
- КОЛИ `line_of_sight(laser_bot, aerogel)` → ТО `custom: «аерогель тане»` → `disappear(aerogel)`; ящик, бот чи Mija на лінії → `block` (промінь далі не йде).
- КОЛИ `contact(mija|bot|crate, button)` → ТО `set_state(button, on)`.
- КОЛИ `leave(mija|bot|crate, button)` → ТО `clear_state(button, on)`.
- КОЛИ `input(interact, switch)` → ТО `set_state(switch, toggle)` → міст, лазер або ліфт міняє стан.
- КОЛИ `state_on(bridge, lit)` → ТО міст прохідний; темний — `block`.
- КОЛИ `enter(walker, electric_pad)` або `blocked(walker)` → ТО `set_state(walker, broken)` — стоїть і перекриває шлях чи промінь.
- КОЛИ `enter(a, air_bump)` → ТО `throw(a, landing)` — Mija, ящик чи бот летить в інше місце.
- КОЛИ `enter(mija, goal)` → ТО `win`, `next_level`.
- Перемога: Mija на виході після того, як кімната приведена в потрібний стан · Поразка: нема — «фабрика дуже поблажлива»: перемотка, undo, reset · Рахунок: нема (?).

## Керування і ввід
- Рух Mija — WASD / стрілки або геймпад (повна підтримка контролерів); Space — взаємодіяти (взяти, покласти, перемкнути) і запустити код; Z — перемотати назад; Shift — прискорити; R — скинути; P — пауза / вийти з термінала; TAB — перейти до іншого бота (Edu).
- Редактор програми: блоки команд перетягуються в пронумеровані рядки; у слоти команди ставиться ціль — літера місця, іконка виду обʼєкта або змінна; вкладені `if` і стрілка `jump to` видні в рядках.
- Програма бота відкривається через термінал у кімнаті (Edu: «P — вийти з термінала»).
- Steam радить грати разом з кимось поруч; формального мультиплеєра нема.

## Вікна, меню, HUD
- `game-screen`: кімната в ізометрії; знизу `custom: «смуга підказок клавіш»` (z rewind · shift fast forward · space interact · r reset); бульбашки «…» над ботами.
- `code-editor`: праворуч панель програми — іконка бота, лічильник «11 / 11», пронумеровані рядки («V1 = Nearest [іконка]», «if V1 is on», «pick up at V1», «drop at V2», «wait for V2», «jump to»), кнопка Reset; кольорові мітки біля номерів рядків — `instruction-highlight` поточної команди кожного бота (у ботів кольорові кільця).
- `dialogue-window`: NPC і сюжет фабрики (додано в оновленні 2024).
- Хаб фабрики з входами в кімнати («рівні мають входи», патчі про The Core і Goo Dam); `credits-window` — титри.
- Переходи: хаб → вхід у кімнату → game-screen ↔ термінал / code-editor → вихід → хаб.

## Фічі поза полем
- Пʼять розділів по 3–4 секції: Nebula Nook (Orientation, Hold On, Teamwork) → T-Tauri Terrace (Beams, Interference, Loops) → Protostar Passage (Gone Rogue, Heavy Lifting, Electricity) → Blue Luminous Sector (Branching, Monitoring, Parallel Processing) → Red Giant Room (Nearest, Spawn, The Core, Starburst, фінал Astral Ascent); 150+ пазлів.
- Кожна секція вводить одне поняття програмування: послідовність, очікування, кілька ботів, цикли, розгалуження, моніторинг, паралельність, змінні, породження.
- `rewind` (перемотка часу назад), `restart-level`, `undo`, `speed-control`.
- Star Stuff Edu: безкоштовна браузерна версія, 11 занять по 6–7 рівнів (~70), вбудовані підказки, матеріали для вчителів, ліцензія CC BY-NC-ND 4.0, вік 10+.
- `gamepad-support`, Steam Deck; досягнення й Steam Cloud; саундтрек окремим DLC.

## Варіації й родичі
- [7-billion-humans](7-billion-humans.md), [human-resource-machine](human-resource-machine.md) — новини Steam порівнюють підхід до коду; 7 Billion Humans теж має одну програму на багато однакових виконавців і `nearest`.
- [cargo-bot](cargo-bot.md), [lightbot](lightbot.md) — команди для одного робота без аватара гравця.
- [sokoban](../push-slide/sokoban.md) — «Sokoban-style» за оглядом GEE; [captain-toad-treasure-tracker](../grid-platformer/captain-toad-treasure-tracker.md) — ізометричні кімнати-діорами.
- [cosmic-express](../connect-rotate/cosmic-express.md) — продається в бандлі, механіка інша.
- Осі варіацій: **де гравець** (поза полем — лише код / на полі як ще один виконавець у реальному часі); **ціль команди** (крок на клітину / іменоване місце / змінна `nearest`); **хто виконує програму** (один бот / кілька однакових / різні типи паралельно).

## Цікавинки для курсу
- Аватар у реальному часі плюс боти з програмами в тій самій кімнаті — 🥇: синхронізація, перемотка назад вимагає знімків стану.
- Команди з іменованою ціллю (`go to: A button`) — бот сам шукає шлях — 🥉 (BFS до цілі).
- Маленький інтерпретатор: `wait for`, `if`, `jump to`, змінні `nearest` — 🥉.
- Одна програма на кілька однакових ботів з окремими вказівниками інструкцій — 🥈.
- Промінь лазера з перешкодами й таймер танення аерогелю — 🥉.
- Ходок, що ламається й стає перешкодою, як ресурс розвʼязку — 📎.
- Air bump: кидок обʼєкта в задану точку — 📎.

## Мапа на каталог
- Є: `command-program` ↔ програма бота · `sensor-predicates` ↔ `if holding` / `if lasering` / `if X is on` · `step-execution` ↔ мітки поточних команд, пауза, прискорення · `code-editor-window` ↔ панель програми · `button-toggle` ↔ кнопки й перемикачі → мости, ліфти · `carrier-platform` ↔ ліфти, грабер несе Mija · `beam-tracing` ↔ промінь Laser Bot · `destructible-blocks` ↔ аерогель тане · `spawner-entity` ↔ Spawner Bot · `rewind` ↔ Z · `restart-level` ↔ R · `undo-redo` · `keyboard-controls` · `sequential-levels` ↔ розділи · `game-screen`.
- **Нема** → пропозиції карток:
  - `+avatar-plus-bots` «Аватар діє в реальному часі поруч із програмованими ботами» · game-logic/program · 🥇.
  - `+named-target-commands` «Команди з іменованою ціллю замість кроків» · game-logic/program · 🥉 · слот {targets: letter|kind|var}.
  - `+wait-for-condition` «Команда чекає, доки обʼєкт стане on» · game-logic/program · 📎.
  - `+nearest-variable` «Змінна = найближчий обʼєкт виду» · game-logic/program · 🥉.
  - `+bot-breakdown` «Бот ламається й лишається перешкодою» · entities/state · 📎.
  - `+edu-version` «Окрема безкоштовна версія для шкіл» · project · 🌱.
  - Повтори: `+jump-labels` (HRM), `+swarm-same-program` (7 Billion Humans), `+carry-object`, `+jump-pad`, `+hub-world`.

## Пропозиції до словників
- `+effect:wait` — команда чекання на подію; `+effect:jump(step)` — перехід на крок програми.
- `+effect:assign(var, nearest(kind))` — записати в змінну найближчий обʼєкт виду.
- `+window:terminal` — програму бота редагують через термінал у світі гри (як у Hard Chip).
- `+ui:key-hints-bar` — постійна смуга з клавішами внизу екрана.
- `+feature:edu-version` — окрема освітня збірка з матеріалами для вчителя.
- `+axis:control` — `direct` (Mija) + `programmed` (боти) одночасно; `+axis:actors` — `party`: кілька ботів різних типів.
- `+card:avatar-plus-bots`.

## Джерела
- ⭐ [Steam: Star Stuff](https://store.steampowered.com/app/1955110/Star_Stuff/) — опис, 150+ пазлів, боти з різними здібностями, «work in sync with your bots», reset / undo, теги (3D, Third Person, Puzzle Platformer); знімки: кімнати з плит, панель програми з `Nearest`, `if … is on`, `jump to`, «11 / 11», смуга клавіш.
- Steam News (ISteamNews API): оновлення 2023–2024 — блок `nearest`, перетягування блоків коду, лазери, перемотка, NPC і титри, Steam Deck, порівняння з Human Resource Machine.
- [Вікі: Levels](https://starstuff.exothermic.wiki/Levels) і гайди розділів: [Nebula Nook](https://starstuff.exothermic.wiki/Puzzle_Guides:Nebula_Nook), [T-Tauri Terrace](https://starstuff.exothermic.wiki/Puzzle_Guides:T-Tauri_Terrace), [Protostar Passage](https://starstuff.exothermic.wiki/Puzzle_Guides:Protostar_Passage), [Blue Luminous Sector](https://starstuff.exothermic.wiki/Puzzle_Guides:Blue_Luminous_Sector), [Red Giant Room](https://starstuff.exothermic.wiki/Puzzle_Guides:Red_Giant_Room) — усі команди, боти, обʼєкти й приклади програм.
- [Star Stuff Edu](https://www.starstuffedu.org) і [сторінка для вчителів](https://www.starstuffedu.org/educators) — керування, ~70 рівнів, концепції, ліцензія.
- [GEE Awards: стаття](https://www.geeawards.com/blog/exploring-the-cosmic-puzzles-of-star-stuff-a-fun-and-engaging-adventure-7p5re) — «Sokoban-style», псевдокод, таймінг рухів із роботами, одна кімната на пазл.
- [Ánimo Games](https://www.animogames.org) — студія, Edu, превʼю на CrazyGames.
- YouTube: пошук «Star Stuff gameplay».

## Непевне
- (?) Чи Mija ходить по клітинах кроками, чи вільно (аналоговий стік) — кімнати складені з квадратних плит, але про крок по сітці джерела мовчать; `field: iso` — за виглядом.
- (?) Кут повороту Laser Bot — 90° (з того, що «двічі за годинниковою» розвертає промінь назад), не перевірено.
- (?) Що означає «11 / 11» на панелі програми — використані рядки з ліміту?
- (?) Чи кілька однакових ботів справді виконують одну спільну програму (кольорові мітки на рядках) — висновок з одного знімка.
- (?) Як саме запускаються програми: Space біля термінала (Edu) чи одразу з входом у кімнату.
- (?) Що стається з ботом, якого «спалив» лазер; як обвалюються мости.
- (?) Метрик і таблиць рекордів не знайшов; Steam згадує «local multiplayer» у фічах, а в категоріях — лише Single-player.
