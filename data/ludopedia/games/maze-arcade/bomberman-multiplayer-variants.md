---
title: Bomberman — мультиплеєрні гілки (Dyna Blaster, Saturn Bomberman, Atomic Bomberman, Bomberman Blast)
slug: bomberman-multiplayer-variants
aka: [Dyna Blaster, Dynablaster, Saturn Bomberman, Bomberman SS, Atomic Bomberman, Bomberman Blast, Wi-Fi 8-Nin Battle Bomberman]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: setup
  goal: survive
year: 1992
platforms: [Amiga / Atari ST / MS-DOS (Dyna Blaster, 1992), Sega Saturn (1996), Windows (Atomic, 1997), Wii / WiiWare (Blast, 2008)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Saturn_Bomberman", best: true, note: "10 гравців: мультитапи 2 / 6 / 10, широка арена понад 8, динозаври з яєць, Master mode, NetLink"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Atomic_Bomberman", note: "PC 1997: 10 гравців, одна розкладка клавіатури на гравця, LAN, схеми .sch, Powerup Manager"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman_Blast", note: "Wii 2008: 8 гравців офлайн/онлайн з рейтингами, ракета й щит, предмети на трусіння пульта, Mii, самоцвіти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bomberman_(1990_video_game)", note: "розділ Dyna Blaster: Ubi Soft, Amiga з комплектним адаптером на 5 гравців, DOS на 4"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dynablaster", note: "сторінка-неоднозначність назви Dyna Blaster"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=saturn+bomberman+10+player+battle", note: "пошук; 10 гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bomberman+blast+wii+8+player+gameplay", note: "пошук; Blast"}
stage: v1
coverage: 60
mechanics: [move-4dir, bomb-fuse, blast-wave, destructible-blocks, hidden-under-block, in-round-upgrades, item-pickup, touch-death, ai-opponent, realtime-ai, online-multiplayer, rating-system, field-scaling, match-setup, avatar-picker, in-game-editor, editor-palette, rule-variants, shop-catalog, round-currency, tutorial-window, score-records, leaderboard, destroy-all-enemies, reach-exit, keyboard-controls, +shared-field-versus, +rideable-mount, +mount-absorbs-hit, +player-count-scales-arena, +powerup-manager, +motion-activated-item, +shrinking-arena]
proposes: ["+effect:mount", "+effect:dismount", "+cond:riding", "+card:rideable-mount", "+card:mount-absorbs-hit", "+card:player-count-scales-arena", "+card:powerup-manager", "+card:motion-activated-item", "+feature:emotes", "+feature:crossplay"]
author: opus
date: 2026-11-09
---

# Bomberman, мультиплеєрні гілки — більше гравців на одному полі: 5 (Amiga), 10 (Saturn, PC), 8 онлайн (Wii), і що для цього змінювалось

## Суть
Чотири відгалуження, де головне — масштаб versus-режиму. Правила бомби й вибуху — як у `bomberman`, арена «останній вижилий» — як у `bomberman-battle-mode`; тут — лише те, що ці гри додали. Saturn Bomberman довів локальну гру до 10 людей і для цього змінив саме поле (широка арена, дрібніші клітини, частина підсилень вимикається), плюс додав динозаврів, яких осідлують. Atomic Bomberman відкрив правила гравцям: схема арени й «менеджер підсилень» у файлі. Bomberman Blast — 8 гравців онлайн з рейтингом і предметами, що вмикаються трусінням пульта.

## Поле і час
- Арена = один екран сітки з колонами й цеглою, як у базовій грі; real-time.
- Saturn: понад 8 гравців → широка арена, персонажі й блоки дрібніші (масштаб поля залежить від кількості гравців).
- Atomic: арена і щільність цегли задаються схемою (файл `.sch`); стартові позиції — кольори 0–9.
- Blast: 10 арен (WiiWare) / 12 (retail).
- Dyna Blaster: поле і рівні PC Engine-оригіналу (8 світів по 8 етапів), зміни портів не задокументовано (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бомбермен | player | bombs, fire, speed | як у `bomberman` |
| CPU-бомбермен | enemy | — | заповнює вільні слоти (Saturn, Atomic — мінімум 1 людина) |
| Цегла | object | ховає предмет | руйнується вибухом; Saturn — може містити яйце динозавра |
| Яйце динозавра (Saturn) | pickup | — | дає маунта або вирощує наявного (battle) |
| Динозавр-маунт (Saturn) | ally | розмір: малюк / підліток / дорослий | несе гравця; витримує 1 удар замість вершника |
| Зарф (Saturn, story) | object | — | стовп з червоною кулею; знищити всі — відкриється вихід |
| Вихід | static | — | після всіх зарфів → наступний рівень |
| Ракета (Blast) | pickup | — | дає політ (?) |
| Щит (Blast) | pickup | — | захист (?) |
| Предмет на трусіння (Blast) | pickup | — | активується трусінням Wii Remote |
| Самоцвіт (Blast retail) | pickup | — | валюта для покупки Hearts / Fire Up / Bomb Up / Speed Up |
| Bomb Spooge / Power Glove (Atomic) | pickup | — | приклади підсилень, конфлікт яких задає схема |

## Правила (КОЛИ → ЯКЩО → ТО)
- Бомба, вибух, руйнування, базові підсилення — як у `bomberman`; вибування, трофеї, нічия — як у `bomberman-battle-mode`.
- Saturn: КОЛИ `game_start` → ЯКЩО `count(players, >, 8)` → ТО `custom: «широка арена, дрібніші клітини, частина підсилень і динозаври вимкнені»`.
- Saturn: КОЛИ `contact(blast, soft_block)` → ЯКЩО `custom: «у блоці яйце»` → ТО `disappear_b`, `spawn(egg)`.
- Saturn: КОЛИ `contact(player, egg)` → ЯКЩО `custom: «гравець пішки»` → ТО `spawn(dino)`, `custom: «гравець сідає верхи»` (`+effect:mount`).
- Saturn battle: КОЛИ `contact(player, egg)` → ЯКЩО `custom: «гравець верхи»` (`+cond:riding`) → ТО `grow(dino, 1)` (малюк → підліток → дорослий).
- Saturn story: КОЛИ `picked(player, power_up)` → ТО `counter(dino_meter, +1)`; КОЛИ `counter(dino_meter, ==, full)` → ТО `grow(dino, 1)`.
- Saturn: КОЛИ `contact(blast, player)` → ЯКЩО `custom: «гравець верхи»` → ТО `custom: «динозавр гине, вершник цілий»`; інакше — вибування.
- Saturn: КОЛИ `input(dismount)` → ЯКЩО `custom: «гравець верхи»` → ТО `custom: «злізти з динозавра»` (`+effect:dismount`).
- Saturn story: КОЛИ `all_gone(zarf)` → ТО `custom: «вихід відкрито»`; КОЛИ `contact(player, exit)` → ТО `next_level`.
- Saturn Master: КОЛИ `level_end` → ТО `custom: «наступний рівень серії без паузи»`; КОЛИ `custom: «серію пройдено»` → ТО `custom: «ранг за часом»`, `window(leaderboard)`.
- Atomic: КОЛИ `game_start` → ТО `custom: «цегла за DENSITY схеми, гравці на стартах кольорів 0–9»`.
- Atomic: КОЛИ `game_start` → ТО `custom: «набір підсилень, частота і руйнованість — за Powerup Manager»`.
- Atomic: КОЛИ `picked(player, item_a)` → ЯКЩО `has(player, item_b)` → ТО `custom: «розвʼязати конфлікт за правилом схеми (Bomb Spooge vs Power Glove)»`.
- Blast: КОЛИ `input(shake)` → ЯКЩО `has(player, motion_item)` → ТО `custom: «активувати предмет»`.
- Blast: КОЛИ `contact(player, rocket)` → ТО `pickup`, `custom: «політ над полем»` (?).
- Blast: КОЛИ `contact(player, shield)` → ТО `set_state(player, shield)` (?).
- Blast retail: КОЛИ `contact(player, gem)` → ТО `currency(+1)`; КОЛИ `input(buy)` → ЯКЩО `has(player, gems)` → ТО `take(player, gems)`, `give(player, upgrade)`.
- Blast online: КОЛИ `game_over` → ТО `custom: «оновити світовий рейтинг»`.
- Перемога: останній вижилий (battle) · вихід після зарфів (Saturn story) · найкращий час (Saturn Master) · Поразка: вибування · Рахунок: трофеї, рейтинг Blast, таблиця часу Master.

## Керування і ввід
- Saturn: без мультитапа — 2 гравці, 1 мультитап — 6, 2 мультитапи — 10; NetLink (NA) — онлайн до 4, по 2 на консоль.
- Atomic: клавіатура — одна розкладка на одного гравця на комп'ютері; більше людей — локальна мережа.
- Dyna Blaster Amiga: адаптер-мультитап у коробці → до 5 гравців; DOS — до 4 одночасно.
- Blast: Wii Remote боком (NES-стиль) + GameCube-контролери: 4 + 4 = 8 офлайн; трусіння — активація предметів; Classic Controller не підтримується.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Saturn: Normal / Master / Battle; Blast retail: Story / Battle / Bomberman for Beginners; WiiWare — лише Battle).
- `match-setup` — кількість гравців людина/CPU, арена; Atomic — classic / enhanced, вибір схеми.
- `editor-window` — прихований редактор схем Atomic: розміщення, DENSITY, Powerup Manager, 2 візуальні теми.
- `avatar-picker` — Mii у Blast.
- `lobby-window` — онлайн-матчі Blast (8 гравців, рейтинг).
- `tutorial-window` — Bomberman for Beginners (Blast retail).
- `leaderboard` — таблиця часу Master mode (Saturn).
- `shop-window` — покупка апгрейдів за самоцвіти (Blast retail) (?: де саме).
- `game-screen`; HUD — `player-portraits` (?); `end-screen` раунду.

## Фічі поза полем
- `local-multiplayer` 5 / 10 / 8 · `online-multiplayer` (NetLink 4; Blast 8 зі світовим рейтингом) · `ai-opponent-levels` (CPU).
- `+feature:crossplay` — retail- і WiiWare-версії Blast грають разом онлайн.
- `+feature:emotes` — «appeal motions» у Blast: 10 (WiiWare) / 20 (retail).
- `level-editor` + `custom-rules` — Atomic: схеми `.sch` і Powerup Manager.
- `mode-speedrun` — Saturn Master mode (ранг за часом, таблиця).
- Blast story: 5 світів, 39 етапів, 31 ворог, 5 босів.

## Варіації й родичі
- `bomberman` — база; `bomberman-battle-mode` — Super Bomberman / R / R Online / R 2 (до 64 гравців, Battle 64, Castle).
- PC Engine Bomberman (1990) — battle до 5 через мультитап, лише Bomb і Fire, Skull Mode (див. `bomberman-battle-mode`); Dyna Blaster — його європейські порти під іншою назвою (ім'я «Bomberman» уникали через асоціацію з терактами).
- Atomic Bomberman зібрано на коді Super Bomberman 3 за ліцензією Hudson.
- Маунти: Louie (кенгуру) у пізніших частинах (?) — той самий принцип «маунт = зайве життя».
- **Осі варіацій:** гравців на полі 4 / 5 / 8 / 10 / 64 · масштаб поля фіксований / залежить від кількості гравців · правила підсилень зашиті / у файлі схеми · маунт: нема / динозавр, що росте · ввід: кнопки / жест (трусіння).

## Цікавинки для курсу
- Арена, що масштабується від кількості гравців (понад 8 → ширше поле, менше підсилень) — 📎: параметри поля від налаштувань матчу.
- Маунт як зайвий удар + ріст від яєць — 🌱: стан «верхи», ефект поглинає шкоду.
- Схема арени й «менеджер підсилень» у текстовому файлі — 🥉: правила й контент як дані, конфлікти предметів.
- Одна розкладка клавіатури — один гравець: кілька гравців на одній клавіатурі — 🌱.
- Онлайн до 8 з рейтингом — 🥇: синхронізація real-time поля.

## Мапа на каталог
- Є: `move-4dir` · `bomb-fuse` · `blast-wave` · `destructible-blocks` · `hidden-under-block` · `in-round-upgrades` · `item-pickup` · `touch-death` · `ai-opponent`, `realtime-ai` · `online-multiplayer` · `rating-system` (Blast) · `field-scaling` (широка арена) · `match-setup` · `avatar-picker` (Mii) · `in-game-editor`, `editor-palette` (Atomic) · `rule-variants` (Powerup Manager, classic/enhanced) · `shop-catalog`, `round-currency` (самоцвіти) · `tutorial-window` · `score-records`, `leaderboard` (Master) · `destroy-all-enemies`/`reach-exit` (зарфи → вихід) · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+shared-field-versus`, `+shrinking-arena` — уже запропоновані в `blockade` / `bomberman`; підтверджую.
  - `+rideable-mount` «Осідлати маунта» · entities/state · 🌱.
  - `+mount-absorbs-hit` «Маунт приймає удар замість вершника» · entities/state · 🌱.
  - `+player-count-scales-arena` «Розмір арени від кількості гравців» · levels/format · 📎 · слот {threshold: 8}.
  - `+powerup-manager` «Таблиця підсилень: частота, руйнованість, конфлікти» · game-logic/constraints · 🥉.
  - `+motion-activated-item` «Предмет вмикається жестом/рухом контролера» · interface/input · 📎.

## Пропозиції до словників
- `+effect:mount` / `+effect:dismount` — сісти на / злізти з сутності-носія, що рухається з гравцем і має власне HP.
- `+cond:riding` — гравець зараз верхи.
- `+feature:emotes` — жести/репліки в мультиплеєрі (appeal motions).
- `+feature:crossplay` — різні видання/платформи в одному матчі.
- `+card:rideable-mount`, `+card:mount-absorbs-hit`, `+card:player-count-scales-arena`, `+card:powerup-manager`, `+card:motion-activated-item` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Saturn Bomberman](https://en.wikipedia.org/wiki/Saturn_Bomberman) — 10 гравців, мультитапи, широка арена понад 8, динозаври (3 розміри, 1 удар), Zarf, Master mode, NetLink, дати.
- [Wikipedia: Atomic Bomberman](https://en.wikipedia.org/wiki/Atomic_Bomberman) — 10 гравців, розкладки клавіатури, LAN, classic/enhanced, редактор схем, DENSITY, Powerup Manager, код SB3.
- [Wikipedia: Bomberman Blast](https://en.wikipedia.org/wiki/Bomberman_Blast) — 8 гравців (4 Wii Remote + 4 GC), онлайн-рейтинг, арени 10/12, appeal motions, ракета, щит, трусіння, самоцвіти, Mii, story 5×39.
- [Wikipedia: Bomberman (1990)](https://en.wikipedia.org/wiki/Bomberman_(1990_video_game)) — Dyna Blaster від Ubi Soft (Amiga/ST/DOS, 1992), 5 гравців на Amiga з адаптером, DOS на 4.
- [Wikipedia: Dynablaster](https://en.wikipedia.org/wiki/Dynablaster) — неоднозначність назви.

## Непевне
- (?) Які саме предмети Blast активуються трусінням; що дає ракета (політ над стінами?) і щит (скільки ударів).
- (?) Повний список підсилень Saturn і Atomic (kick, punch, хвороби-черепи) — у відкритих статтях не перелічено.
- (?) Чи має Dyna Blaster відмінні від PC Engine рівні/правила; паролі.
- (?) Чи можна заповнити CPU усі 10 слотів Saturn і як налаштовується сила CPU.
- (?) Рік у черзі «1991» — за Wikipedia порти Dyna Blaster вийшли у 1992 (Франція — січень 1992).
- (?) Louie як маунт пізніших частин — з памʼяті, не перевірено.
