---
title: Triga
slug: triga
aka: []
family: thinky
also: []
klass: cursor
axes:
  field: tri
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2022
platforms: [Windows]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1890550/Triga/", best: true, note: "опис: золоті трикутники знищити або скинути з дошки; трикутні інструменти — вибух, відштовхування сусідів; ланцюгові реакції; 3 цілі на етап; скриншоти HUD і мапи"}
  - {kind: itch, url: "https://cicada-games-official.itch.io/triga", note: "та сама гра на itch (GameMaker, Windows), входить у бандл CosmOS 9"}
  - {kind: other, url: "https://cicada-games-official.itch.io/triga/devlog/384613/triga-v11-update", note: "патч v1.1 (24.05.2022): блискавка, ланцюги бомб, руйнування каменю, штовх-цеглина, «елементні цеглини», підсилювачі сигналу, секретний ключ, undo скидання"}
  - {kind: other, url: "https://itch.io/b/1394/cosmos-9", note: "бандл CosmOS 9 — 9 коротких пазлів «з інопланетної консолі»"}
  - {kind: other, url: "https://www.rockpapershotgun.com/puzzle-game-collection-cosmos-9-is-a-gentle-introduction-to-the-genre", note: "RPS 19.05.2022 про бандл CosmOS 9"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Triga+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, cursor-place, explode-area, chain-detonation, chain-reaction, destructible-blocks, collect-quota, undo-step, restart-level, world-map, level-unlock, save-progress, sound-effects, background-music, music-toggle, +triangle-grid, +tool-allotment, +single-use-tool, +knockback, +off-board-removal, +lightning-beam, +tiered-goals, +meta-currency-gates, +secret-key-level, +undo-through-restart, +multiple-endings]
proposes: ["+effect:knockback", "+effect:emit_beam", "+ui:tool-tray", "+ui:signal-meter", "+window:overspace-map", "+card:tool-allotment", "+card:tiered-goals"]
author: opus
date: 2026-11-19
---

# Triga — клади трикутні інструменти на трикутну дошку, щоб вибухами й поштовхами ланцюгом знищити золоті трикутники

## Суть
Кожен рівень — острівець трикутних клітин із плитками, серед яких кілька золотих трикутників. Гравець має обмежений набір трикутних **інструментів**; кожен тип, поставлений на дошку, діє по-своєму — вибухає, відштовхує сусідні плитки, бʼє блискавкою.

Мета — знищити або скинути з дошки якомога більше золотих: на етапі щонайменше три цілі, від «трохи» до «все» (PERFECT). Ядро — ланцюгові реакції й незвичний рух плиток на трикутній сітці.

## Поле і час
- Трикутна сітка: клітини-трикутники вершиною вгору й униз; дошки — острівці довільної форми, іноді кілька поруч (скриншоти).
- Шари: клітина дошки / порожнеча → плитки (звичайні, камінь, бомби, елементні цеглини, золоті).
- Покроково: хід = поставити інструмент, після чого реакція розгортається сама (анімація вибухів і блискавок).
- Поза рівнями — «Overspace», мапа рівнів-вузлів; частина закрита золотом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Золотий трикутник | pickup | — | ціль: знищити вибухом чи скинути з дошки |
| Інструмент-вибух | supply | кількість у лотку | поставлений — вибухає й нищить сусідів (?) |
| Інструмент-штовхач | supply | кількість | поставлений — відштовхує сусідні плитки |
| Інструмент-блискавка | supply | кількість | бʼє лінією через дошку (?) |
| Бомба на дошці | hazard | — | вибух поруч підриває її — ланцюг |
| Камінь | object | — | руйнується вогнем (вибухом) (?) |
| Елементна цеглина (штовх-цеглина) | object | стихія | спрацьовує, коли її зачепила реакція (?) |
| Підсилювач сигналу | pickup | — | збільшує «SIGNAL %» (?) |
| Секретний ключ | pickup | — | відкриває секретний рівень |
| Клітина дошки | terrain | — | сюди ставлять інструменти; з краю дошки плитку можна скинути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `free(cell)` і `count(tool, >, 0)` → ТО `place(player, tool)`, `counter(tools, -1)`.
- КОЛИ `input(click, cell)` → ЯКЩО `cell(cell, blank)` → ТО `block` (?) — на порожнечу не ставлять.
- КОЛИ `spawned(bomb_tool)` → ТО `explode(neighbors)` (?) — форма вибуху не перевірена.
- КОЛИ `spawned(pusher_tool)` → ТО `custom: «сусідні плитки відштовхуються від нього»` (`+effect:knockback`).
- КОЛИ `spawned(lightning_tool)` → ТО `custom: «блискавка прямою лінією»` (`+effect:emit_beam`) (?).
- КОЛИ `destroyed(a)` → ЯКЩО `custom: «поруч бомба»` → ТО `explode(bomb_area)` — ланцюг бомб.
- КОЛИ `after(explode(area))` → ЯКЩО `occupied(area, stone)` → ТО `disappear(stone)` (?).
- КОЛИ `edge(tile)` → ТО `disappear(tile)` — скинута з дошки плитка зникає.
- КОЛИ `destroyed(gold)` або `edge(gold)` → ТО `counter(gold, +1)`.
- КОЛИ `counter(gold, ==, total)` → ТО `message(«PERFECT!»)`, `custom: «феєрверк»`; часткові цілі рахуються окремо.
- КОЛИ `counter(total_gold, >=, n)` → ТО `unlock(level)` — рівні на мапі закриті золотом.
- КОЛИ `picked(player, secret_key)` → ТО `unlock(secret_level)`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(reset)` → ТО `restart` — скидання теж можна скасувати undo.
- Перемога: виконати цілі етапу (3+ рівні цілей). · Поразка: нема — інструменти скінчились, результат фіксується. · Рахунок: золото рівня `x/y` і загальна сума.

## Керування і ввід
- Миша: клік по клітині дошки — поставити наступний інструмент із лотка праворуч (?); кнопки UNDO, RESET, LEVELS.
- Esc — повернутись в Overspace; після кожного поставленого інструмента коротка затримка вводу (v1.1), щоб не вийти з рівня випадково.
- Музичний плеєр унизу: попередній трек, пауза, наступний, перемішати.

## Вікна, меню, HUD
- `game-screen`: дошка; ліворуч угорі UNDO / RESET / LEVELS, по центру назва рівня, праворуч угорі лічильник трикутників (?), золото рівня `x/y`, загальне золото, «SIGNAL %»; праворуч — інструменти; унизу плеєр із назвою треку.
- `map-window` «Overspace»: трикутна мапа рівнів, на закритих — потрібне золото; MENU, QUIT.
- `end-screen`-повідомлення: «PERFECT! PRESS ESC TO RETURN TO OVERSPACE.», «сумний» феєрверк при невдачі.
- `main-menu` з титрами (v1.1); попередження про «чорну діру» (?).
- Переходи: main-menu → Overspace → рівень → (Esc) → Overspace.

## Фічі поза полем
- `world-map` + `level-unlock` золотом; секретні рівні за ключами; кілька кінцівок залежно від того, скільки досягнуто.
- `undo`, `restart-level` (скидання теж скасовне).
- Плеєр саундтреку з перемішуванням (16 треків, окремий DLC).
- Можна покинути важкий рівень і грати інші.

## Варіації й родичі
- [Bomberman](../maze-arcade/bomberman.md) — вибухи й ланцюгові детонації на квадратній сітці.
- [Spectrangle](../board-digital/spectrangle.md) — трикутні плитки й сусідство ребрами.
- **Осі варіацій:** ресурс гравця — набір інструментів (тут) / один хід за раз · ціль — усі / квота з кількома рівнями · сітка — квадрат / гекс / трикутник (рух «зигзагом»).

## Цікавинки для курсу
- Трикутна сітка: сусідство ребрами й рух плиток — 📎 (дві орієнтації клітин).
- Ланцюгові вибухи: черга подій до затухання — 🥉.
- Відштовхування сусідів і скидання з краю дошки — 📎.
- Лоток обмежених інструментів + кілька рівнів цілі — 🌱.
- Мапа рівнів, що відкриваються сумою золота — 🌱.

## Мапа на каталог
- Є: `cell-click` + `cursor-place` ↔ поставити інструмент · `explode-area` + `chain-detonation` + `chain-reaction` ↔ вибухи й ланцюги · `destructible-blocks` ↔ камінь · `collect-quota` ↔ золоті цілі · `undo-step`, `restart-level` · `world-map` + `level-unlock` ↔ Overspace · `save-progress`, `sound-effects`, `background-music`, `music-toggle`.
- **Нема** → пропозиції карток:
  - `+tool-allotment` «Лоток обмежених інструментів на рівень» · entities/legality · 🌱 · слоти {tools: list}.
  - `+tiered-goals` «Кілька рівнів цілі на етап» · game-logic/win · 🌱.
  - `+knockback` «Поставлена плитка відштовхує сусідів» · entities/interact · 📎.
  - `+off-board-removal` «Скинута за край — знищена» · entities/interact · 🌱.
  - `+triangle-grid` «Трикутна сітка» · interface/render · 📎.

## Пропозиції до словників
- `+effect:knockback(a)` — сусіди відштовхуються від A (повтор з інших файлів).
- `+effect:emit_beam(a, dir)` — дія прямою лінією через поле (блискавка; повтор з інших файлів).
- `+ui:tool-tray` — лоток інструментів, що лишились, поруч із полем.
- `+ui:signal-meter` — відсоток «сигналу», метаресурс для кінцівок (?).
- `+window:overspace-map` — мапа рівнів як окремий простір, рівні закриті сумою ресурсу.
- `+card:tool-allotment`, `+card:tiered-goals` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1890550/Triga/) — опис («each level has a few golden triangles… destroy or knock any number of them off the board»; інструменти з ефектом при постановці; ланцюгові реакції; «Each stage has 3 goals»), реліз 19.05.2022, Cicada Games, Windows; скриншоти HUD, Overspace і рівнів.
- [Девлог v1.1](https://cicada-games-official.itch.io/triga/devlog/384613/triga-v11-update) і новини Steam — блискавка, ланцюги бомб, руйнування каменю, штовх-цеглина, підсилювачі сигналу, секретний ключ, «undoing a reset», рівні, закриті золотом.
- [itch](https://cicada-games-official.itch.io/triga) — GameMaker, бандл CosmOS 9; анонс у новинах Steam: «3 or more goals», кілька кінцівок.

## Непевне
- (?) Точний набір інструментів і їхні форми дії (радіус вибуху, напрямок поштовху, лінія блискавки) — опис дає лише «вибух» і «відштовхування», решта — з назв у патчі й скриншотів.
- (?) Що робить камінь, елементні цеглини й «чорна діра»; що рахує «SIGNAL %» і лічильник трикутників у HUD.
- (?) Як саме плитки рухаються від поштовху на трикутній сітці («interesting and unexpected motion»).
- (?) Кількість рівнів і кінцівок не названо.
