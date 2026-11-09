---
title: Bombergirl (ボンバーガール)
slug: bombergirl
aka: [ボンバーガール, Bomber Girl, Bombergirl Konaste, ボンバーガール コナステ, Bombergirl Rainbow]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: state
year: 2018
platforms: [arcade (Японія), Windows (Konaste, 2021)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bombergirl", best: true, note: "4×4, зруйнувати базу суперника, уміння героїнь, рівні ростуть у матчі й відкривають спецатаки"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ボンバーガール_(ゲーム)", note: "чотири ролі: Bomber / Attacker / Shooter / Blocker; блоки, предмети, база; оновлення Rainbow"}
  - {kind: official, url: "https://p.eagate.573.jp/game/eacbg/bg/info/howto.html", note: "Konaste: режими, рейт-ранги, таблиця керування (бомба, 2 уміння, підрив вежі/бази, повернення на базу, чат)"}
  - {kind: official, url: "https://p.eagate.573.jp/game/bombergirl/bg/p/howto.html", note: "аркадне «як грати»: розділи про обʼєкти, предмети, уміння, чат, Rush Time, результати, гачу (текст — картинками)"}
  - {kind: other, url: "https://www.4gamer.net/games/546/G054691/20220914114/", note: "перехід на free-to-play: режими, рейт F–SS, гача й CP-магазин"}
  - {kind: youtube, url: "https://youtu.be/1jzlqOHrcuM", note: "офіційне промо-відео (посилання з офіційного сайту)"}
stage: v1
coverage: 45
mechanics: [move-4dir, bomb-fuse, blast-wave, destructible-blocks, item-pickup, in-round-upgrades, unit-xp-skills, melee-vs-ranged, projectile-shot, ai-opponent, realtime-ai, online-multiplayer, rating-system, character-select, tutorial-window, controls-remap, keyboard-controls, minimap-radar, +team-play, +character-classes, +base-destruction, +place-block, +word-of-recall, +gacha-draw, +xp-level-up]
proposes: ["+card:base-destruction", "+effect:detonate", "+role:base", "+role:tower", "+window:chat-wheel", "+feature:rank-seasons"]
author: opus
date: 2026-11-09
---

# Bombergirl — Bomberman як MOBA: дві команди по четверо ламають блоки, качаються в матчі й підривають вежі та базу суперника

## Суть
Аркада Konami (2018): дві команди по 4 гравці на одній сітковій мапі. Бомби ламають блоки, з блоків — предмети; ціль не «останній вижилий», а **знищити базу** суперника. Кожна героїня належить до однієї з чотирьох ролей (Bomber — багато бомб і широкі вибухи; Attacker — ближній бій і швидкість; Shooter — дальні атаки; Blocker — ставить блоки, захищає, лікує) і має два уміння. Рівень героїні росте прямо в матчі й відкриває спецатаки (промінь-меч, вогняний меч).

## Поле і час
- Сітка з блоками, як у Bomberman; на мапі — бази команд і вежі (Konaste: «підрив — знищення вежі, бази»); з оновлення Rainbow — обʼєкт «великі ворота».
- Аркада — вертикальний екран; Konaste переробила під горизонтальний монітор. Карта масштабується клавішею, тобто видно не все поле одразу (?).
- Real-time матч з фазою Rush Time (розділ офіційного «як грати»; що саме змінюється — (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Героїня | player | роль, рівень у матчі, 2 уміння | рух стіком, бомба, уміння, підрив |
| Bomber (Shiro, Kuro, Grey, Platinum…) | player | — | кладе багато бомб, широкі вибухи |
| Attacker (Oren, Urushi, Sepia…) | player | — | ближні атаки, мобільність; Oren — швидка |
| Shooter (Emera, Papuru, Brass…) | player | — | дальні атаки; Emera — оптична зброя |
| Blocker (Momoko, Aqua, Pine, Prune, Melon…) | player | — | ставить блоки, заважає, підтримує; Momoko, Prune — лікують союзниць |
| COM-героїня | enemy | — | заповнює вільні слоти матчу |
| Бомба | object | — | вибух за Bomberman-правилами |
| Блок | object | — | руйнується бомбою; ховає предмет |
| Предмет | pickup | — | підсилення (типи — (?)) |
| Вежа | static | команда | підривається (`起爆`) |
| База | static | команда | ціль матчу; знищена — поразка її команди |
| Великі ворота (Rainbow) | gate | — | обʼєкт мапи (поведінка — (?)) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(bomb)` → ЯКЩО `free(cell)` → ТО `place(player, bomb)`; КОЛИ `timer(fuse)` → ТО `explode(cross, fire)` (як у `bomberman`).
- КОЛИ `contact(blast, block)` → ТО `disappear_b`, `custom: «може лишити предмет»`.
- КОЛИ `contact(player, item)` → ТО `pickup`, `custom: «посилення героїні»`.
- КОЛИ `custom: «героїня набрала досвід у матчі»` → ТО `custom: «рівень +1»`; КОЛИ `counter(level, >=, n)` → ТО `unlock(special_attack)`.
- КОЛИ `input(skill_1|skill_2)` → ТО `custom: «уміння ролі»`: Blocker — `place(player, block)`, `heal(ally, n)`; Attacker — `speed(player, +n)` / ближня атака; Shooter — `custom: «дальній постріл»`.
- КОЛИ `contact(attack, enemy_girl)` → ТО `damage(n)`; КОЛИ `hp_zero(girl)` → ТО `custom: «вибута; повертається за правилом відродження»` (?).
- КОЛИ `input(detonate)` → ЯКЩО `custom: «героїня у вежі/базі суперника»` (?) → ТО `custom: «підрив: вежа/база руйнується»`.
- КОЛИ `input(return)` → ТО `teleport(player, own_base)` (?).
- КОЛИ `destroyed(enemy_base)` → ТО `win` (команда).
- КОЛИ `custom: «почався Rush Time»` → ТО `custom: «фінальна фаза матчу»` (?).
- КОЛИ `input(chat_n)` → ТО `message(preset_n)`.
- КОЛИ `game_over` → ЯКЩО `mode(rank_battle)` → ТО `custom: «рейт ±, видимий ранг F…SS»`.
- Перемога: знищити базу суперника · Поразка: втратити свою базу · Рахунок: рейт у ранговому режимі; результат матчу (як судять без знищеної бази — (?)).

## Керування і ввід
- Аркада: стік — рух; 3 кнопки — бомба й два уміння.
- Konaste: WASD / лівий стік — рух; ← / кнопка 1 — бомба; ↓ / 2 — уміння ①; → / 3 — уміння ②; Enter / 6 — підрив (вежа, база); Delete / 4 — повернення на базу; цифровий ряд — чат-фрази; PageDown — масштаб карти; лівий тригер — заміна умінь, правий — вибір уміння/фрази, правий стік — чат. Миша — по іконках на екрані. Розкладку можна змінити.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: онлайн-бій (Casual / Rank), одиночний бій, «роздягальня», навчання.
- `character-select` («Bomber Girl Select») — героїня, уміння; `custom-window` «роздягальня» — уміння, вбрання, голоси чату, профіль.
- `tutorial-window` — навчальний режим.
- `game-screen` — мапа; HUD — `minimap` з масштабом (?), `skill-bar`, рівень героїні (?), чат-фрази (`+window:chat-wheel`).
- `end-screen` («Результати») — переможена команда показана з обгорілим одягом.
- `shop-window` — гача (Bomber Gacha) і CP-магазин за дублікати.
- `leaderboard` / ранги сезону — рейт у 8 щаблях SS, S, A–F.
- Переходи: вибір героїні → режим → підбір гравців (порожні слоти → COM) → бій → результати.

## Фічі поза полем
- `online-multiplayer` 4×4 з підбором; `ai-opponent-levels` нема — COM лише заповнює слоти; новачок у Casual грає зі «своїми» проти COM.
- `rank-tiers` + `+feature:rank-seasons` — сезон 1–2 місяці, рейт скидається, нагорода за щабель.
- `unlockables` через гачу (уміння, вбрання, титули, фрази чату); дублікати → CP → обмін.
- Konaste: free-to-play з 14.09.2022; дані частково спільні з аркадою; рангова стеля 120 (аркада — 150).
- `remap-controls`, `gamepad-support`, `mouse-and-keyboard`.

## Варіації й родичі
- `bomberman`, `bomberman-battle-mode` — правила бомби й вибуху; `bomberman-multiplayer-variants` — масштаб versus.
- `crazy-arcade-bnb` — інший командний «бомбермен» (рятування з бульбашки).
- **Осі варіацій:** мета — останній вижилий / знищити базу (Bombergirl) · ролі — однакові персонажі / стати / ролі з уміннями · прогресія — підсилення з блоків / рівні в матчі зі спецатаками.

## Цікавинки для курсу
- База й вежі як цілі замість «вбити всіх»: HP споруди, підрив дією гравця — 🥉.
- Чотири ролі з двома уміннями (блокерка ставить блоки й лікує) — 🥈: таблиця умінь як дані.
- Рівень у матчі відкриває спецатаку — 📎.
- Повернення на базу кнопкою — 🌱.
- Командна гра 4×4 у real-time через мережу — 👑 (синхронізація, підбір, рейт).

## Мапа на каталог
- Є: `move-4dir` · `bomb-fuse`, `blast-wave` · `destructible-blocks` · `item-pickup`, `in-round-upgrades` · `unit-xp-skills` ↔ рівні в матчі → спецатаки · `melee-vs-ranged` ↔ Attacker / Shooter · `projectile-shot` ↔ дальні атаки · `ai-opponent`, `realtime-ai` ↔ COM · `online-multiplayer` · `rating-system` ↔ рейт F–SS · `character-select` · `tutorial-window` · `controls-remap`, `keyboard-controls` · `minimap-radar` ↔ масштаб карти.
- **Нема** → пропозиції карток:
  - `+base-destruction` «Ціль — знищити базу суперника» · game-logic/win · 🥉 · слоти {towers, base_hp}.
  - З корпусу: `+team-play`, `+character-classes`, `+place-block` (блокерка), `+word-of-recall` (повернення на базу), `+gacha-draw`, `+xp-level-up`.

## Пропозиції до словників
- `+card:base-destruction` — див. вище.
- `+effect:detonate` — гравець вручну підриває споруду, у якій стоїть (起爆).
- `+role:base`, `+role:tower` — підтримую наявні пропозиції корпусу.
- `+window:chat-wheel` — набір готових фраз, що шлються однією клавішею.
- `+feature:rank-seasons` — сезонні ранги зі скиданням рейту й нагородами.

## Джерела
- ⭐ [Wikipedia: Bombergirl](https://en.wikipedia.org/wiki/Bombergirl) — 4×4, мета — база, уміння Shiro / Momoko / Oren / Emera, рівні в матчі → промінь-меч і вогняний меч, MOBA, дати й платформи.
- [Wikipedia JA: ボンバーガール (ゲーム)](https://ja.wikipedia.org/wiki/ボンバーガール_(ゲーム)) — 4 ролі й героїні, «ламати блоки бомбами, збирати предмети, знищити базу», Rainbow і «великі ворота».
- [Konaste: 遊び方](https://p.eagate.573.jp/game/eacbg/bg/info/howto.html) — режими, Casual / Rank, рейт SS–F, сезони, таблиця керування.
- [Аркадний сайт: 遊び方](https://p.eagate.573.jp/game/bombergirl/bg/p/howto.html) — назви розділів правил (обʼєкти, предмети, уміння, чат, Rush Time, результати, гача); правила — картинками.
- [4Gamer: free-to-play](https://www.4gamer.net/games/546/G054691/20220914114/) — три безкоштовні режими, ранги, гача й CP-магазин.

## Непевне
- (?) Як працює підрив: чи треба стояти на вежі/базі, скільки триває, чи вежі захищають базу — відомо лише, що є дія «підрив (вежа, база)».
- (?) Rush Time — назва фази є, зміст (прискорення? подвійна шкода по базі?) не перевірено.
- (?) HP героїнь, правило відродження, ліміт часу матчу й визначення переможця без знищеної бази.
- (?) Типи предметів з блоків і чи досвід дають предмети чи бої.
- (?) Чи рух клітинний, як у Bomberman, чи вільний по сітці.
