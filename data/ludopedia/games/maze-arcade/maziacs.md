---
title: Maziacs
slug: maziacs
aka: [Мазіаки]
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 1983
platforms: [ZX Spectrum, Commodore 64, MSX, Amstrad CPC, Commodore Plus/4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Maziacs", best: true, note: "суть: випадковий лабіринт, золото ≥200 ходів, одноразові мечі, меч і золото не разом, вʼязні, енергія і їжа, режим огляду"}
  - {kind: other, url: "https://www.spectrumcomputing.co.uk/pub/sinclair/games-info/m/Maziacs.txt", note: "інструкція ZX: повернутись на старт, сидіння, 4 рівні складності, формула очок, огляд 1/12"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/3100/ZX-Spectrum/Maziacs", note: "картка ZXDB: DK'Tronics, Don Priestley, Kempston, Currah MicroSpeech, порти, Mazogs як інша версія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mazogs", note: "попередник на ZX81 (Bug-Byte, 1982)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Maziacs+ZX+Spectrum", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, keyboard-controls, controls-remap, impassable-cells, maze-generation, player-camera, item-pickup, inventory-limit, chase-player, chase-greedy, hunger-clock, path-preview, touch-death, player-death, reach-exit, difficulty-levels, game-screen, map-window, difficulty-select, +single-use-tool, +exclusive-carry, +npc-path-hint, +far-goal-placement, +efficiency-score, +frozen-overview, +speech-output]
proposes: ["+card:exclusive-carry", "+card:npc-path-hint", "+card:far-goal-placement", "+card:efficiency-score", "+card:frozen-overview", "+card:single-use-tool", "+feature:speech-output"]
author: opus
date: 2026-11-09
---

# Maziacs — знайди золото у величезному лабіринті й донеси його на старт: у руках або меч, або золото

## Суть
Герой блукає випадковим лабіринтом, щоб знайти скарб (золото) і повернутися з ним до старту. Лабіринт патрулюють маціаки, яких надійно вбиває лише меч, а меч одноразовий і **не несеться разом із золотом** — тож маршрут планують як «спершу розчистити, потім нести». Вʼязні в стінах на кілька ходів підсвічують шлях до цілі, а енергія тане від кожного кроку й бою і поповнюється лише їжею. Гра Don Priestley для DK'Tronics — переробка його ж ZX81-гри Mazogs.

## Поле і час
- Лабіринт генерується наново для кожної гри (генерація триває помітний час); золото кладеться щонайменше за 200 ходів від старту.
- Вид згори зі скролінгом: основний екран показує ≈1/50 лабіринту, режим огляду (View) — ≈1/12; інструкція оцінює весь лабіринт як ≈64 видимих ділянки. У режимі огляду рухатись не можна.
- Інструкція каже, що лабіринт «не має країв» — див. «Непевне».
- Real-time: маціаки рухаються самі; кожен крок героя рахується (кількість ходів іде в очки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | енергія (шкала праворуч) | рух 4 напрямки; несе **або** меч, **або** золото; може «сидіти» |
| Стіна | static | — | непрохідна |
| Старт | static | — | точка, куди треба повернутись із золотом |
| Золото (скарб) | pickup | ≥200 ходів від старту | береться в руки; поки в руках — меча не взяти |
| Меч | pickup | одноразовий; на складніших рівнях менше | дає перемогу в бою з маціаком, після бою зникає |
| Маціак | enemy | кількість однакова на всіх рівнях | знає, де герой, іде найпрямішим шляхом, іноді непередбачувано; вартує золото |
| Вʼязень | static | у стіні; на рівні 4 — один раз | дотик → показує маршрут до золота, а з золотом — до старту |
| Маршрут | mark | жовтий; обмежений ходами або часом | підсвічені клітини шляху, згодом гасне |
| Їжа | pickup | на складніших рівнях менше | відновлює енергію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(hero, dir)`, `counter(moves, +1)`, `counter(energy, -1)`; інакше `block`.
- КОЛИ `contact(hero, sword)` → ЯКЩО `not has(hero, gold)` → ТО `pickup(hero, sword)`.
- КОЛИ `contact(hero, sword)` → ЯКЩО `has(hero, gold)` → ТО `place(hero, gold)`, `pickup(hero, sword)` — обмін можна робити будь-коли.
- КОЛИ `contact(hero, gold)` → ЯКЩО `has(hero, sword)` → ТО `place(hero, sword)`, `pickup(hero, gold)`; інакше `pickup(hero, gold)`.
- КОЛИ `contact(maziac, hero)` → ЯКЩО `has(hero, sword)` → ТО `disappear(maziac)`, `take(hero, sword)`, `counter(energy, -n)`.
- КОЛИ `contact(maziac, hero)` → ЯКЩО `not has(hero, sword)` → ТО `custom: «довший бій без меча, найчастіше — смерть героя»`, `counter(energy, -n)`.
- КОЛИ `contact(maziac, hero)` → ЯКЩО `state(hero, sitting)` → ТО `lose` (маціак убиває сидячого завжди).
- КОЛИ `contact(hero, food)` → ТО `disappear(food)`, `counter(energy, +n)`.
- КОЛИ `counter(energy, <=, 0)` → ТО `lose` (смерть від голоду).
- КОЛИ `contact(hero, prisoner)` → ЯКЩО `not has(hero, gold)` → ТО `mark(route_to_gold, yellow)`; ЯКЩО `has(hero, gold)` → ТО `mark(route_to_start, yellow)`.
- КОЛИ `counter(route_moves, ==, 0)` → ТО `unmark(route)` (рівні 1–2); на рівнях 3–4 — КОЛИ `timer(route_duration)` → ТО `unmark(route)`.
- КОЛИ `contact(hero, prisoner)` → ЯКЩО `difficulty(4)` and `state(prisoner, used)` → ТО `custom: «вдруге не допомагає»`.
- КОЛИ `input(view)` → ТО `camera(zoom_out)`, `custom: «рух заблоковано до будь-якої клавіші»`.
- КОЛИ `tick` → ЯКЩО `state(hero, viewing)` and `difficulty(>=2)` → ТО `counter(energy, -1)`; ЯКЩО `difficulty(>=3)` → ТО `unmark(route)` (огляд стирає маршрут).
- КОЛИ `tick` → ТО маціаки: `custom: «крок найпрямішим шляхом до героя, часом випадковий»` (`chase-greedy`).
- КОЛИ `reach(hero, start)` → ЯКЩО `has(hero, gold)` → ТО `win`, `score(min_moves / moves × 100 + bonus)`, де bonus = 0 / 10 / 20 / 30 за рівнем складності 1–4.
- Перемога: золото на старті. Поразка: бій без меча, напад на сидячого, енергія 0. Рахунок: відсоток оптимальності маршруту + бонус складності.

## Керування і ввід
- Перевизначувані клавіші; Kempston-джойстик. 4 напрямки руху.
- Клавіша огляду (View): лабіринт віддаляється до ≈1/12, рух заморожено; будь-яка клавіша — назад.
- Клавіша меню, далі «D» — вибір рівня складності 1–4.
- Підтримка синтезатора мови Currah MicroSpeech (ZX).

## Вікна, меню, HUD
- `loading-screen` — очікування генерації нового лабіринту.
- `game-screen` — ділянка ≈1/50 лабіринту з героєм у центрі; праворуч `energy-bar`; жовтий маршрут поверх підлоги (`path-preview`).
- `map-window` (View) — ділянка ≈1/12 лабіринту без руху; на рівнях 2+ коштує енергію.
- `main-menu` → `difficulty-select` (1 — легко; 2 — енергія тане під час огляду; 3 — як 2, плюс огляд гасить маршрут і маршрут тримається за часом; 4 — як 3, плюс вʼязень допомагає раз) · `options-controls` (перевизначення клавіш).
- `end-screen` — результат: відсоток оптимальності + бонус складності.
- Переходи: меню → генерація → game-screen ⇄ огляд → (золото на старті / смерть) → end-screen.

## Фічі поза полем
- `difficulty-presets` 1–4: складніші рівні мають менше мечів, їжі й вʼязнів при тій самій кількості маціаків, а огляд стає дорожчим.
- `remap-controls`, `gamepad-support` (Kempston), синтез мови (Currah MicroSpeech) — `+feature:speech-output`.
- Кожна гра — новий лабіринт: немає рівнів чи збережень, реіграбельність через генерацію.

## Варіації й родичі
- Mazogs (ZX81, 1982, Bug-Byte) — попередня версія тієї самої гри; Maziacs — переробка для Spectrum 48K; порти C64 (Andy French), MSX, Amstrad CPC, Plus/4; неофіційний Bugziacs (QL); Maziacs1 (2003, ZX 16K, Paolo Ferraris); Chuckman — гра, натхненна Maziacs (ZXDB).
- [Adventure (Atari 2600)](atari-adventure.md) — теж «одна річ у руках» (меч, ключ, чаша) і дракони-вартові; меч там вічний.
- [3D Monster Maze](3d-monster-maze.md), [Kroz](kroz.md), [Gauntlet](gauntlet.md) (їжа як ресурс життя) — сусіди за лабіринтом і виживанням.
- **Осі варіацій:** зброя — вічна (Adventure) / одноразова (Maziacs) / набої; руки — один слот із виключенням (меч XOR золото) / інвентар; підказка шляху — нема / тимчасовий маршрут від NPC / мапа; ціна огляду — безкоштовно / енергія / втрата маршруту.

## Цікавинки для курсу
- Меч і золото взаємовиключні: інвентар з одним слотом і обміном на місці — 📎 (просте правило, але змінює весь план маршруту).
- Вʼязень підсвічує найкоротший шлях до цілі на N ходів — 🥉 (BFS від героя + оверлей, що гасне за лічильником або таймером).
- Очки = мінімум ходів / фактичні ходи — 🥉 (BFS «старт → золото → старт» на згенерованому лабіринті).
- Генерація лабіринту з ціллю не ближче 200 ходів від старту — 🥈 (генерація + відстані BFS + розкладання мечів, їжі, вʼязнів за складністю).
- Енергія тане від кроків і боїв, їжа відновлює — 🌱.
- Режим огляду: віддалена камера, рух заморожено, огляд коштує енергію — 📎.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` + `controls-remap` ↔ перевизначення клавіш · `impassable-cells` ↔ стіни · `maze-generation` ↔ новий лабіринт щогри · `player-camera` ↔ скролінг за героєм · `item-pickup` ↔ меч, золото, їжа · `inventory-limit` ↔ один предмет у руках · `chase-player` + `chase-greedy` ↔ маціаки йдуть найпрямішим шляхом · `hunger-clock` ↔ енергія тане від кроків · `path-preview` ↔ жовтий маршрут вʼязня · `touch-death` + `player-death` · `reach-exit` ↔ повернення на старт · `difficulty-levels` · `game-screen` · `map-window` ↔ огляд · `difficulty-select`.
- **Нема** → пропозиції карток:
  - `+single-use-tool` (вже Lode Runner: The Legend Returns) — меч зникає після одного бою.
  - `+exclusive-carry` «Предмети, що не несуться разом» · entities/state · 📎 · слот {pairs: list} — меч XOR золото.
  - `+npc-path-hint` «NPC показує шлях до цілі на N ходів» · interface/hud · 🥉 · слоти {duration: moves|time, uses: n}.
  - `+far-goal-placement` «Ціль генерується не ближче N кроків від старту» · levels/generation · 📎 · слот {min_distance}.
  - `+efficiency-score` «Очки = оптимум / фактичні ходи» · scoring · 🥉.
  - `+frozen-overview` «Огляд мапи з паузою руху й ціною» · interface/render · 📎 · слот {cost: none|energy|lose_hint}.
  - `+speech-output` «Синтез мови для подій» · interface/sound · 🥉.

## Пропозиції до словників
- `+card:exclusive-carry`, `+card:npc-path-hint`, `+card:far-goal-placement`, `+card:efficiency-score`, `+card:frozen-overview`, `+card:single-use-tool` — див. «Мапу на каталог».
- `+feature:speech-output` — голосові повідомлення через синтезатор (Currah MicroSpeech).
- Огляд лягає на наявні `map-window` + `camera(zoom_out)`; нового слова вікна не треба.

## Джерела
- ⭐ [Wikipedia: Maziacs](https://en.wikipedia.org/wiki/Maziacs) — випадковий лабіринт, золото ≥200 ходів від старту, одноразові мечі, меч і золото не разом, вʼязні тимчасово показують шлях, енергія і їжа, екран 1/50 і огляд 1/12, Mazogs, платформи, Currah MicroSpeech.
- [Інструкція Maziacs (txt, ZX)](https://www.spectrumcomputing.co.uk/pub/sinclair/games-info/m/Maziacs.txt) — повернення на старт, обмін меча і золота будь-коли, поведінка маціаків, смерть сидячого, маршрут вʼязня (жовтий, обмежений), 4 рівні складності, формула очок, огляд без руху.
- [ZXDB: Maziacs](https://spectrumcomputing.co.uk/entry/3100/ZX-Spectrum/Maziacs) — DK'Tronics 1983, Don Priestley, Kempston і перевизначення клавіш, Currah MicroSpeech, Mazogs, порти, Bugziacs, Chuckman.
- [Wikipedia: Mazogs](https://en.wikipedia.org/wiki/Mazogs) — попередник на ZX81.
- YouTube: пошук «Maziacs ZX Spectrum».

## Непевне
- (?) «Лабіринт не має країв» — чи це тор (вихід за край → протилежний бік), чи просто нема видимої межі; не перевірено.
- (?) Коли герой «сідає» — імовірно, після бездіяльності (`idle(n)`); інструкція лише каже, що сидячого маціак убиває завжди.
- (?) Бій без меча: чи результат випадковий і з якою ймовірністю — інструкція каже лише «довше і, ймовірно, смерть».
- (?) Скільки ходів тримається маршрут на рівнях 1–2 і скільки секунд — на 3–4; скільки енергії дають їжа й забирають бій і крок.
- (?) Розбіжність у масштабі: Wikipedia — екран ≈1/50 лабіринту, інструкція — лабіринт ≈64 видимих ділянки.
- (?) Чи Wikipedia «знайти золото й покинути рівень» означає саме повернення на старт (за інструкцією — так).
