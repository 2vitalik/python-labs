---
title: Magpie (7DRL 2023)
slug: magpie-broughlike
aka: [Magpie]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: score
year: 2023
platforms: [web, mobile]
links:
  - {kind: itch, url: "https://zunil.itch.io/magpie", best: true, note: "грати в браузері; опис, керування, версії джему"}
  - {kind: other, url: "https://zunil.itch.io/magpie/comments", note: "коментарі-гайди: Inkwell, слоти, монети, яйця, персонажі"}
  - {kind: other, url: "https://itch.io/post/7479932/view-in-topic", note: "сторінка 7DRL 2023: «permadeath, turn-based, grid-based, non-modal», PCG рівнів, ворогів і пропозицій дрібничок"}
  - {kind: other, url: "https://itch.io/games/tag-broughlike", note: "тег broughlike на itch.io"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magpie+broughlike+7DRL+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [move-4dir, keyboard-controls, swipe-gestures, hp-damage, inventory-items, inventory-limit, key-and-door, destructible-blocks, round-currency, item-pickup, permadeath, dungeon-generation, sequential-levels, reach-exit, character-select, score-records, leaderboard, +slot-direction-weapons, +items-as-hp, +coins-upgrade-items]
proposes: ["+role:slot", "+card:slot-direction-weapons", "+card:items-as-hp"]
author: opus
date: 2026-11-09
---

# Magpie — broughlike, де дрібнички довкола сороки — і зброя, і щит, і здоровʼя

## Суть
Сорока ходить мікро-сіткою і збирає блискучі дрібнички. Кожна дрібничка займає **бік** сороки й атакує клітини за власним патерном у тому напрямку; вона ж — щит: удар з того боку знищує саме її. Окремого HP нема: інвентар, позиціонування і здоровʼя — одна механіка. Монети потрібні для очок і для покращення дрібничок, але підбирати їх доводиться тим самим слотом, що тримає цінну зброю.

## Поле і час
- Маленька квадратна сітка-рівень з виходом на краю; рух 4 напрямки.
- Покроково: «turn-based, grid-based, non-modal» (опис автора на 7DRL).
- Генеруються макети рівнів, спавн ворогів і пропозиції дрібничок; у персонажа Wasp рівні менші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сорока (або Wasp / Robin / Crow) | player | слоти з боків | хід = крок; дрібнички бʼють за патернами |
| Inkwell | pickup | — | центральна дрібничка: підсилює ті, що бʼють багато клітин; найвразливіша спереду |
| Candelabra · Stapler · Cross | pickup | патерн | дальні / багатоклітинні атаки (?) |
| Paperclip | pickup | шкода 2 | ставлять навпроти Inkwell |
| Glasses | pickup | — | слабкі в коридорі; зсувають слабке місце Inkwell |
| Keys | pickup | — | удар по замкнених дверях відкриває їх — переносить вихід |
| Clippers | pickup | — | ріжуть зелені перешкоди |
| Credit Card | pickup | — | знищена — дає монету |
| Mirror · Clock · Seashell | pickup | ціна | особливі ефекти (не перевірено) |
| Монети (золота, срібна, сіра) | resource | цінність | очки; ціна дрібничок 1–3 золоті |
| Яйце | pickup | випадкове | +HP або очки |
| Щур · кіт | enemy | — | атакують; де вбити — важливо, бо лишають/вимушують підбирати |
| Замкнені двері | gate | — | відкриваються ключем |
| Зелена перешкода | static | — | рветься Clippers |
| Вихід | static | на краю | напрям виходу підказує, звідки прийде небезпека |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; `custom: «дрібнички атакують клітини за своїми патернами»` (?).
- КОЛИ `contact(enemy, player)` → ТО `custom: «удар знищує дрібничку з того боку»`; ЯКЩО `custom: «бік без дрібнички»` → ТО `lose`.
- КОЛИ `picked(player, trinket)` → ТО `custom: «дрібничка займає слот з боку підходу»` (?) (`+role:slot`).
- КОЛИ `picked(player, coin)` → ТО `score(value)`, `custom: «монета займає слот / витрачається на покращення»` (?).
- КОЛИ `custom: «зібрано ціну дрібнички (1–3 золоті)»` → ТО `give(player, trinket)` (?).
- КОЛИ `destroyed(credit_card)` → ТО `currency(+1)`.
- КОЛИ `contact(keys, locked_door)` → ТО `disappear(locked_door)`, `custom: «вихід переноситься»`.
- КОЛИ `contact(clippers, green_obstacle)` → ТО `disappear(green_obstacle)`.
- КОЛИ `reach(player, exit)` → ТО `next_level`.
- Рахунок: монети; онлайн-таблиця рекордів.

## Керування і ввід
- WASD / стрілки / свайп — рух; гарячі клавіші старту й рестарту (додані на прохання гравців).

## Вікна, меню, HUD
- `game-screen`: мікро-сітка, сорока з дрібничками по боках, рахунок.
- `character-select`: Magpie · Wasp (+1 шкоди, малі рівні) · Robin (пасивка) · Crow.
- Пропозиції дрібничок між рівнями — `shop-window` (?); `leaderboard`.

## Фічі поза полем
- `permadeath`; короткі забіги; `leaderboard-online`.
- Безкоштовна браузерна гра; дві версії джему (10 і 12.03.2023).

## Варіації й родичі
- `roguelike/mosaic-broughlike` — той самий автор, теж «здоровʼя = щось інше»; `roguelike/868-hack`, `roguelike/pawnbarian` — інші broughlikes.
- Зброя за боками фігури — родич `roguelike/shogun-showdown` (напрям удару) і щитів Hoplite.
- **Осі варіацій**: HP — число / предмети (тут) / плитки (Mosaic); слоти — за боками / вільні; монети — валюта / займають місце.

## Цікавинки для курсу
- Дрібнички за боками: атака патерном відносно напрямку слоту — 📎 (поворот патерну за боком).
- Предмет = HP: удар знищує предмет з того боку — 🌱.
- Монети, що конкурують зі зброєю за слоти, — 🌱 (жадібність проти безпеки).
- Ключ переносить вихід — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `swipe-gestures` · `hp-damage` · `inventory-items` · `inventory-limit` (слоти) · `key-and-door` · `destructible-blocks` (зелені перешкоди) · `round-currency` (монети) · `item-pickup` · `permadeath` · `dungeon-generation` · `sequential-levels` · `reach-exit` · `character-select` · `score-records` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+slot-direction-weapons` «Зброя в слоті з боку, патерн за напрямком» · entities/combat · 📎.
  - `+items-as-hp` «Предмети замість HP» · entities/state · 🌱.
  - `+coins-upgrade-items` «Монети покращують предмети» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+role:slot` — позиція відносно гравця (бік), що тримає предмет.
- `+card:slot-direction-weapons` · `+card:items-as-hp`.

## Джерела
- ⭐ [itch.io: Magpie](https://zunil.itch.io/magpie) — грати в браузері; «You are a curious magpie who loves to collect shiny trinkets.»
- [Коментарі itch.io](https://zunil.itch.io/magpie/comments) — гайди гравців: Inkwell, Paperclip, Keys, Clippers, монети, яйця, персонажі.
- [7DRL 2023](https://itch.io/post/7479932/view-in-topic) — роглайк-елементи й PCG за описом автора; «weapon durability as health».
- YouTube: [пошук](https://www.youtube.com/results?search_query=Magpie+broughlike+7DRL+gameplay).

## Непевне
- (?) Скільки слотів (4 боки?) і як предмет потрапляє в слот (з боку підходу?).
- (?) Чи атака відбувається автоматично після кожного кроку, чи лише при русі в ворога.
- (?) Як саме монети покращують/купують дрібнички (у джерелах: «ціна 1–3 золоті», «3 золоті → яйце»).
- (?) Патерни Candelabra, Stapler, Cross, Mirror, Clock, Seashell.
- (?) Що означає «яйця дають +HP», якщо HP = дрібнички.
