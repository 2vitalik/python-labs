---
title: Lode Builder
slug: lode-builder
aka: []
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 2026
platforms: [Windows (Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3305720/Lode_Builder/", best: true, note: "опис автора: драбини, ланцюги, BigFire, ресурси, режими, редактор; демо"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=3305720", note: "той самий опис JSON-ом: дата Q4 2026, категорії, ID демо 5212370"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1845383656389411", note: "анонс демо 03.10.2026: рівні, інструменти, Arcade Mode, редактор"}
  - {kind: official, url: "https://www.lodebuilder.com", note: "сторінка-хаб посилань (Steam, VK, X)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lode+Builder+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [gravity-fall, ladder-climb, collect-all, item-pickup, inventory-items, chase-player, destroy-all-enemies, cheat-codes, difficulty-levels, in-game-editor, level-exchange, level-rating, leaderboard, mode-select, achievements-window, +build-ladder, +build-chain, +resource-unlocks-tool, +mass-burn, +invisible-enemies, +monthly-tournament]
proposes: ["+feature:tournaments", "+card:build-ladder", "+card:resource-unlocks-tool", "+card:mass-burn"]
author: opus
date: 2026-11-09
---

# Lode Builder — Lode Runner, де драбини й ланцюги будуєш сам із знайдених ресурсів

## Суть
Інді-переосмислення Lode Runner від E140Games (Steam, вихід запланований на Q4 2026, є демо з 03.10.2026): треба зібрати все золото серед роботів, але до класичного руху додано **будування** — драбина для вертикального шляху, ланцюг для горизонтального, і «масове спалення» **BigFire**, що знищує роботів і дає швидко спуститися глибше. Інструменти **не безкоштовні**: їх відкривають ресурси, знайдені на рівні, — автор пише, що з необмеженими ресурсами проходиться будь-який рівень, тому обмеження — ядро гри. Решта правил (копання, вихід, життя) у відкритих джерелах не описана — див. базовий файл `lode-runner`.

## Поле і час
- Сітка Lode Runner (вид збоку, драбини, перекладини-ланцюги, гравітація) у real-time — з жанру й тегів (Arcade, Puzzle Platformer, 2D Platformer).
- Рівень — «яскрава піксель-арт-картинка»: автор малював кампанії на полотні 23×38 пікселів і поєднував геймплей з малюнком (чи 1 піксель = 1 клітина — не сказано).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | — | бігає, лазить, збирає золото й ресурси, будує |
| Робот | enemy | видимий / невидимий (челендж) | ворог; знищується BigFire |
| Золото | pickup | — | зібрати все — мета |
| Ресурс | pickup | прихований (челендж) | відкриває інструмент на цьому рівні |
| Драбина (збудована) | static | — | вертикальний рух |
| Ланцюг (натягнутий) | static | — | горизонтальний рух через провалля |
| BigFire | — | — | масове спалення: роботи знищені, шлях униз розчищено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `picked(hero, resource)` → ТО `unlock(tool)` — драбина, ланцюг або BigFire стають доступні.
- КОЛИ `input(build_ladder)` → ЯКЩО `has(hero, ladder_resource)` → ТО `place(hero, ladder)`, `take(hero, ladder_resource)` (?).
- КОЛИ `input(build_chain)` → ЯКЩО `has(hero, chain_resource)` → ТО `place(hero, chain)` над прірвою (?).
- КОЛИ `input(bigfire)` → ЯКЩО `has(hero, fire_resource)` → ТО `custom: «спалити всіх роботів і розчистити шлях глибше»`.
- КОЛИ `picked(hero, gold)` → ТО `counter(gold, -1)`; КОЛИ `all_gone(gold)` → ТО `win` (?) — чи потрібен ще вихід, не сказано.
- КОЛИ `contact(robot, hero)` → ТО `lose` (?) — як у Lode Runner; в Unlimited Mode — безсмертя.
- Unlimited Mode: `custom: «чіт-коди IDDQD / IDKFA — безсмертя й нескінченні ресурси»`.
- Перемога: зібрати все золото. · Поразка: (?) · Рахунок: є в Arcade Mode (турніри на рекорд).

## Керування і ввід
- Клавіатура/миша; геймпади DualShock і DualSense (часткова підтримка) — за категоріями Steam.
- Окремі клавіші інструментів — (?).

## Вікна, меню, HUD
- `mode-select`: кампанії · Unlimited Mode · Extra Challenges · Arcade Mode · Player Levels (?) — режими зі сторінки, як саме подані в меню — не видно.
- `game-screen`: рівень-картинка; HUD із доступними інструментами/ресурсами (?).
- `editor-window` — вбудований редактор рівнів (є в демо).
- `leaderboard` — місячні й річні рекорди Arcade-турнірів.
- `achievements-window` — досягнення Steam.

## Фічі поза полем
- Кампанії: 150+ рівнів у трьох тематичних кампаніях (аркада + пазл).
- Arcade Mode: випадкова вибірка зі 100+ простих рівнів без складних пазлів; Arcade Tournaments — місячні й річні рекорди.
- Extra Challenges: невидимі роботи, приховані ресурси.
- Unlimited Mode: чіт-коди, безсмертя, нескінченні ресурси — вільне будування.
- `level-editor` + Steam Workshop + браузер рівнів гравців із сортуванням авторів за рейтингом.
- Steam Cloud, налаштовувана складність, керування гучністю, 5 мов.

## Варіації й родичі
- Базова гра і сиквели — `lode-runner`, `lode-runner-sequels`, `lode-runner-the-legend-returns`, `lode-runner-3d-sequels`, `battle-lode-runner`.
- Осі варіацій Lode Runner:
  - **будування**: нема, лише копання (оригінал) / драбини й ланцюги з ресурсів (Lode Builder) / вільне (Unlimited Mode);
  - **спосіб позбутись ворогів**: яма (оригінал) / масове спалення (BigFire);
  - **видимість**: усе видно / невидимі роботи (челендж).

## Цікавинки для курсу
- Будування драбини/ланцюга з лічильником ресурсу — `set_cell` + інвентар — 📎.
- Ресурс на рівні відкриває інструмент — 🌱.
- Масове спалення: прибрати всіх ворогів і зруйнувати шар поля — 📎.
- Режим «невидимі роботи» — малювання без ворогів при повній логіці — 🌱.

## Мапа на каталог
- Є: `gravity-fall`, `ladder-climb` ↔ драбини й ланцюги; `collect-all` ↔ золото; `item-pickup` + `inventory-items` ↔ ресурси й інструменти; `chase-player` ↔ роботи (?); `destroy-all-enemies` ↔ BigFire; `cheat-codes` ↔ IDDQD/IDKFA; `difficulty-levels`; `in-game-editor` + `level-exchange` + `level-rating` ↔ редактор, Workshop, рейтинг авторів; `leaderboard` ↔ турніри; `mode-select`; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+build-ladder` «Поставити драбину з запасу» · entities/interact · 📎; `+build-chain` — горизонтальний аналог.
  - `+resource-unlocks-tool` «Знайдений ресурс відкриває інструмент» · entities/state · 🌱.
  - `+mass-burn` «Одна дія знищує всіх ворогів» · entities/combat · 🌱.
  - `+invisible-enemies` «Вороги невидимі (режим-челендж)» · interface/render · 🌱.
  - `+monthly-tournament` «Періодичні турніри на рекорд» · interface/results · 📎.

## Пропозиції до словників
- `+feature:tournaments` — місячні/річні змагання на рекорд за спільним набором рівнів.
- `+card:build-ladder`, `+card:resource-unlocks-tool`, `+card:mass-burn` — див. вище.

## Джерела
- ⭐ [Steam: Lode Builder](https://store.steampowered.com/app/3305720/Lode_Builder/) — «Build, run, collect», драбини, ланцюги, BigFire, обмеження ресурсів, режими, редактор, Q4 2026.
- [Steam API appdetails](https://store.steampowered.com/api/appdetails?appids=3305720) — повний текст опису: «Players can only unlock them by finding the necessary resources on the level», полотно 23×38, категорії.
- [Анонс демо](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1845383656389411) — 03.10.2026: пазл-рівні, інструменти, Arcade Mode, редактор.
- YouTube: пошук «Lode Builder gameplay».

## Непевне
- (?) Гра ще не вийшла (Q4 2026); описано лише за маркетинговим текстом — без демо-перевірки.
- (?) Чи лишилось класичне копання ям і чи вороги потрапляють у них — у тексті нема ні слова.
- (?) Що саме руйнує BigFire, щоб «спуститися глибше» (цеглу під собою?), і чи вона одноразова.
- (?) Як витрачаються ресурси: один ресурс = одна драбина чи ресурс відкриває інструмент на весь рівень.
- (?) Поразка, життя, вихід після золота — не описані.
- (?) «Evil guards» і «mining laser» згадані лише у відкинутій казковій історії — чи є в грі, невідомо.
