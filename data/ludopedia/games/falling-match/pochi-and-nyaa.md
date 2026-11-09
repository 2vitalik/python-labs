---
title: Pochi and Nyaa
slug: pochi-and-nyaa
aka: [ポチッとにゃ～, "Pochi to Nyaa", "Pochitto Nyaa", "Nyoki Nyoki: Tabidachi Hen", にょきにょき たびだち編]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2003
platforms: [arcade (Neo Geo MVS), PS2, Windows (2025), 3DS (Nyoki Nyoki, 2016)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pochi_and_Nyaa", best: true, note: "поле 7×12, пари, групи без ліміту, тригер з падаючої пари, сміття й offset, череп, режими, версії"}
  - {kind: other, url: "http://ascii.jp/elem/000/000/332/332655/", note: "ASCII (JA): керування, голка はりにゃん, підпал і послідовний вибух, розгалуження, сміття, невдала голка → сміття, режими"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ポチッとにゃ～", note: "JA: 3 кнопки (поворот ×2, «はり»), 4+ кольори не зникають, лічильник сміття, череп"}
  - {kind: other, url: "https://www.arcade-history.com/game/1993/", note: "кнопки A/B/C, режими, матч до 2 перемог на одному кредиті"}
  - {kind: other, url: "https://compile0.base.shop/items/109181253", note: "Windows-версія 2025 (порт NAOMI): «зʼєднуй і підпалюй коли хочеш», гілки, клавіші"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nyoki_Nyoki:_Tabidachi_Hen", note: "3DS-наступник: поле 8×16, activator, сміття"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pochi+and+Nyaa+Neo+Geo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, chain-detonation, simultaneous-versus, garbage-attack, ai-opponent, character-select, mode-select, tutorial-window, sequential-levels, event-points, keyboard-controls, end-screen, time-out, time-bonus, +crash-gem-detonate, +player-made-detonator, +unlimited-group-hold, +branch-chain-bonus, +garbage-offset, +garbage-adjacent-clear, +dud-trigger-to-garbage, +garbage-on-lock]
proposes: ["+card:player-made-detonator", "+card:unlimited-group-hold", "+card:branch-chain-bonus", "+card:dud-trigger-to-garbage", "+card:garbage-on-lock"]
author: opus
date: 2026-11-09
---

# Pochi and Nyaa — однакові кошенята липнуть без ліміту; падаючу пару перетворюєш на голку, і вона підпалює всю групу

## Суть
Дуель на двох полях від Aiky (наступниця Compile, авторів Puyo Puyo): падають пари кольорових кошенят, і група однакових **не зникає сама** — її можна ростити як завгодно довго, з гілками. Коли зручно, гравець кнопкою перетворює падаючу пару на «голку»; голка, покладена поруч зі своїм кольором, підпалює групу, і блоки вибухають по черзі вздовж гілок. Що більша й розгалуженіша група — то більше сміття летить супернику; невдала голка сама стає сміттям.

## Поле і час
- Поле на гравця 7 × 12 (EN Wikipedia) або 7 × 13 (ASCII) клітин; два поля поруч. Верхня центральна клітина позначена черепом.
- Real-time падіння пар; вибух групи — послідовний, клітина за клітиною від точки підпалу.
- Шари: поле + активна пара/голка + лічильник вхідного сміття над полем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пара (くみにゃん; у 2P — くみわん) | player | 2 блоки, кольори з 4 (червоний, синій, зелений, жовтий) | зсув, поворот за/проти годинникової, прискорення; кнопка — стати голкою і назад |
| Голка (はりにゃんIII型 / はりわんIII型) | player | форма падаючої пари | лягла поруч з групою свого кольору → підпал |
| Блок-кошеня (にゃん / わん) | tile | колір | приземлився → зʼєднується з сусідніми того ж кольору; група росте без ліміту й сама не зникає |
| Група з гілками | zone | будь-яка довжина, розгалуження | після підпалу вибухає по черзі; гілки дають більше очок |
| Сміття (おじゃまにゃん / おじゃまわん) | hazard | — | напряму не знищується; зникає, якщо поруч вибухнула група |
| Невдала голка | hazard | — | лягла без підпалу → за короткий час стає сміттям |
| Череп | static | верхня клітина в центрі | блок дійшов сюди → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(pair, down)`; КОЛИ `input(down)` → ТО швидше падіння.
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(pair, dir)`; КОЛИ `input(A|B)` → ТО `rotate(pair, ±90)`.
- КОЛИ `input(C|up)` → ЯКЩО `state(pair, falling)` → ТО `transform(pair, needle)`; повторно — `transform(needle, pair)`.
- КОЛИ `locked(pair)` → ТО `custom: «блоки зʼєднуються з сусідніми того ж кольору; група росте без ліміту й сама не зникає»`.
- КОЛИ `locked(needle)` → ЯКЩО `adjacent(needle, group)` і `same(needle, group, color)` → ТО `explode(group)` — `custom: «блоки вибухають по черзі від точки дотику вздовж гілок»`.
- КОЛИ `custom: «вибух поруч»` → ЯКЩО `adjacent(blast, nuisance)` → ТО `disappear(nuisance)`.
- КОЛИ `locked(needle)` → ЯКЩО `not adjacent(needle, same_color_group)` → ТО `custom: «через короткий час»` `transform(needle, nuisance)`.
- КОЛИ `after(explode)` → ТО `score(n)`, `send_garbage(n = cleared)`; більша група й більше гілок → більше сміття.
- КОЛИ `custom: «до тебе летить сміття»` → ЯКЩО встиг підірвати свою групу до падіння → ТО `custom: «offset — вхідне сміття зменшується або гаситься повністю»`.
- КОЛИ `locked(pair|needle)` → ЯКЩО `counter(incoming, >, 0)` → ТО `spawn_at(nuisance, top)`.
- КОЛИ `after(explode)` → ТО `fall(all_unsupported)`.
- КОЛИ `custom: «блок досяг клітини-черепа»` → ТО `lose`; матч — до 2 перемог.
- КОЛИ `custom: «ланцюг»` → ЯКЩО `mode(attack)` → ТО `timer(+n)`; КОЛИ `timer(==, 0)` → ТО `game_over`.
- Перемога: суперник дійшов до черепа (2 раунди) · Поразка: блок у клітині-черепі · Рахунок: довгі, розгалужені групи + підпал голкою.

## Керування і ввід
- Аркада: 8-позиційний важіль + 3 кнопки — A: поворот проти годинникової, B: за годинниковою, C: «はり» (пара ↔ голка); важіль ↑ теж перемикає, ↓ — прискорення.
- Windows: стрілки — рух і прискорення, Z/X — повороти, C / ↑ — голка; клавіатура лише за P1, другий гравець — геймпад.
- Тактика: тримати велику групу й чекати на момент, коли суперник вразливий, — підпал коли хочеш, а не коли склалось.

## Вікна, меню, HUD
- `attract-demo` → `mode-select`: ポチにゃ～アタック · ひとりでポチにゃ～ (Story 8 стадій проти CPU / れんしゅう 3 стадії) · ふたりでポチにゃ～ (2P за 1 монету).
- `character-select` — у грі вдвох; у Story гравець — Prim.
- `game-screen`: два поля з черепом у центрі верху, `garbage-meter` (лічильник вхідного сміття над полем), `score`, анімація персонажів.
- `tutorial-window` — коротке пояснення правил на старті одиночних режимів.
- `end-screen` раунду / матчу; у Vs CPU поразка в раунді — кінець гри.

## Фічі поза полем
- `mode-versus` (2 гравці або CPU) · `mode-classic` → Story · `mode-practice` → れんしゅう · ポチにゃ～アタック — одиночний режим з таймером, який поповнюють ланцюги.
- PS2 (2004, Bandai): нові персонажі, кращі подача й ефекти.
- Windows (2025): порт скасованої NAOMI-версії, `fullscreen` (Alt+Enter).

## Варіації й родичі
- **Nyoki Nyoki: Tabidachi Hen** (3DS, 2016, Compile Maru / D4 Enterprise) — те саме ядро: пари «нйокі», групи без ліміту, падаючу пару перетворюєш на activator, що запускає ланцюг крізь сусідів. Відмінності: поле 8 × 16 на гравця, поразка — коли стек дійшов до верху третього стовпця. Кампанія на порт для Switch (2017) не зібрала 10 млн єн.
- [super-puzzle-fighter-ii-turbo](super-puzzle-fighter-ii-turbo.md) — найближчий родич: групи теж не зникають самі, їх підриває crash gem; але там детонатор дає випадок, а тут — гравець.
- [puyo-puyo](puyo-puyo.md) — той самий автор, протилежне правило: 4+ лопаються автоматично.
- **Осі варіацій**: хто вирішує, коли зникає група (поріг / випадковий детонатор / гравець) · ліміт групи (4 / без ліміту) · форма вибуху (одночасно / послідовно вздовж гілок) · ціна промаху (нема / невдала голка → сміття).

## Цікавинки для курсу
- Перемикач «пара ↔ голка» на падаючій фігурі — 🌱.
- Підпал групи з точки дотику і послідовний вибух хвилею по гілках (BFS з таймінгом кроків) — 🥉.
- Бонус за розгалуження: порахувати гілки й довжину звʼязаної групи — 📎 (дерево / граф компоненти).
- Невдала голка через N тіків стає сміттям — 🌱.
- Сміття, що падає після твого ходу, гаситься встиглим підпалом — 📎.
- CPU, що вирішує, коли підпалювати велику групу, — 🥈.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (пара) · `piece-rotate-flip` · `chain-detonation` (вибух біжить по групі) · `simultaneous-versus` + `garbage-attack` · `ai-opponent` · `character-select` · `mode-select` · `tutorial-window` · `sequential-levels` (Story 8 стадій) · `event-points` · `keyboard-controls` (Windows) · `end-screen` · `time-out` + `time-bonus` (режим attack).
- **Нема** → пропозиції карток:
  - `+crash-gem-detonate` «Група зникає лише від детонатора свого кольору» · entities/interact · 📎 — як у Super Puzzle Fighter.
  - `+player-made-detonator` «Гравець сам перетворює падаючу фігуру на детонатор» · entities/state · 🌱.
  - `+unlimited-group-hold` «Група росте без ліміту, поки її не підпалять» · entities/interact · 🌱.
  - `+branch-chain-bonus` «Очки/атака за кількість гілок групи» · game-logic/score · 📎.
  - `+dud-trigger-to-garbage` «Детонатор без цілі стає сміттям» · entities/state · 🌱.
  - `+garbage-on-lock` «Вхідне сміття падає, коли ти поклав фігуру» · game-logic/opponent · 🌱.
  - `+garbage-offset` · `+garbage-adjacent-clear` — як у Puyo.

## Пропозиції до словників
- `+card:player-made-detonator` · `+card:unlimited-group-hold` · `+card:branch-chain-bonus` · `+card:dud-trigger-to-garbage` · `+card:garbage-on-lock` — див. «Мапа на каталог».
- Нових слів правил не треба: `transform`, `explode`, `adjacent`, `send_garbage`, `locked` уже є.

## Джерела
- ⭐ [EN Wikipedia: Pochi and Nyaa](https://en.wikipedia.org/wiki/Pochi_and_Nyaa) — поле 7×12, пари, групи без ліміту, тригер, гілки сильніші, сміття й offset, череп, режими, версії.
- [ASCII.jp (JA)](http://ascii.jp/elem/000/000/332/332655/) — поле 7×13, 4 кольори, керування (↑/C — голка і назад), підпал і послідовний вибух, розгалуження, сміття зникає лише від вибуху поруч, невдала голка → сміття, Story 8 / れんしゅう 3 стадії.
- [JA Wikipedia: ポチッとにゃ～](https://ja.wikipedia.org/wiki/ポチッとにゃ～) — 3 кнопки, «4+ кольорів не зникають», лічильник сміття, падає після твого ходу, череп, три режими.
- [Arcade History](https://www.arcade-history.com/game/1993/) — кнопки A/B/C, Vs CPU, 2P до двох перемог за один кредит, вступне навчання.
- [Compile Maru: Windows-версія](https://compile0.base.shop/items/109181253) — порт NAOMI, «зʼєднуй і підпалюй коли хочеш», гілки, клавіші.
- [EN Wikipedia: Nyoki Nyoki: Tabidachi Hen](https://en.wikipedia.org/wiki/Nyoki_Nyoki:_Tabidachi_Hen) — 8×16, activator, сміття, 3DS 2016.
- YouTube: пошук «Pochi and Nyaa Neo Geo gameplay».

## Непевне
- (?) Розмір поля: 7×12 (EN) проти 7×13 (ASCII) — можливо, 13-й ряд прихований.
- (?) Чи падають блоки після вибуху (осідання) — прямо не сказано; правило `fall` — за аналогією з Puyo.
- (?) Arcade History описує одиночний режим з таймером, що поповнюється ланцюгами, — схоже на ポチにゃ～アタック, але назви режимів не збігаються.
- (?) Чи голка має колір кожного з двох блоків пари окремо — джерела кажуть лише «поруч з групою свого кольору».
- (?) Дата Nyoki Nyoki: 11 листопада 2016 (EN) проти 16 листопада (JA, сторінка Compile Maru).
