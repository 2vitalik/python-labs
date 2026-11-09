---
title: H5mota (H5魔塔广场) — спільнота веб-веж
slug: h5mota
aka: [H5魔塔广场, H5 Mota Square, mota-js, HTML5魔塔样板]
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: score
year: 2017
platforms: [web (HTML5), mobile web, Android (APP)]
links:
  - {kind: play, url: "https://h5mota.com/", best: true, note: "H5魔塔广场: 2000+ веж онлайн, рейтинги за рахунком, форум, редактор без програмування"}
  - {kind: official, url: "https://github.com/ckcz123/mota-js", note: "рушій «HTML5 魔塔样板» (BSD-3): редактор, реплеї, плагіни, історія версій 2017–2023"}
  - {kind: other, url: "https://raw.githubusercontent.com/ckcz123/mota-js/master/README.md", note: "README: перевірка реплеїв бекендом, завантаження рахунку, анти-чит, мобільний редактор"}
  - {kind: other, url: "https://raw.githubusercontent.com/ckcz123/mota-js/master/project/functions.js", note: "формула бою getDamageInfo — спільна для всіх веж"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=h5mota+%E9%AD%94%E5%A1%94", note: "пошук; проходження веж"}
stage: v1
coverage: 60
mechanics: [move-4dir, key-and-door, hp-damage, item-pickup, stairs-levels, save-multi-slot, save-autosave, replay, replay-window, leaderboard, rating-system, in-game-editor, editor-palette, editor-draw-tools, editor-undo, editor-playtest, level-exchange, level-bank, level-metadata, difficulty-levels, state-as-data, logic-render-split, keyboard-controls, cell-click, path-preview, codex-window, +deterministic-combat, +damage-preview, +replay-verified-score, +event-scripting, +plugin-api, +anti-cheat-upload]
proposes: ["+feature:replay-verification", "+feature:score-upload", "+feature:plugin-api", "+feature:event-editor", "+feature:left-hand-mode", "+window:tower-list", "+window:event-editor", "+window:floor-select", "+card:replay-verified-score", "+card:event-scripting"]
author: opus
date: 2026-11-09
---

# H5mota — платформа й корпус фанатських Magic Tower: один рушій, тисячі веж, рекорд підтверджує реплей

## Суть
H5魔塔广场 (h5mota.com) — сайт, де живе китайська спільнота «魔塔» (Magic Tower, див. [magic-tower](magic-tower.md)): **понад 2000 веж**, кожну можна грати в браузері без завантаження. Усі вежі зроблені на одному відкритому рушії **mota-js «HTML5 魔塔样板»** (автор ckcz123 / 艾之葵), тож мають спільні правила бою, предмети, гарячі клавіші й оболонку. Для курсу це еталон не гри, а **платформи**, як [tatham-collection](../pencil-logic/tatham-collection.md): спільне ядро + дані рівня + редактор + реплей, що **перевіряє рекорд на сервері**. Рейтинг вежі — рахунок (зазвичай HP наприкінці), і він чесний лише тому, що бій детермінований.

## Поле і час
- Кожна вежа — набір поверхів-сіток (класика 13×13 з рамкою (?)); з V2.7 (2020) рушій тримає великі карти до 128×128, з V2.9 — прямокутні види.
- Шари клітини: підлога/стіна · обʼєкт (монстр, двері, предмет, NPC) · подія (скрипт на клітині); рушій має плагін «п'ять шарів» (2020).
- Покроково; вороги стоять (за замовчуванням), хід = крок героя; `random: none` у рушії — бій за формулою.
- Корпус веж різнорідний: класичні вежі-ресурсні пазли, сюжетні, «змагальні» вежі на рахунок; частина веж змінює правила плагінами.

## Сутності
Сутності рушія (спільні для більшості веж); повний перелік предметів і спецздібностей — у [magic-tower](magic-tower.md).

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, ATK, DEF, MDEF, золото, XP, ключі | рух 4 напрямки; бій «наступанням» |
| Монстр | enemy | HP, ATK, DEF, золото, XP, спецздібності | стоїть; бій детермінований |
| Двері / ключі | gate / pickup | колір | ключ кольору відчиняє двері |
| Самоцвіти, зілля | pickup | +ATK/+DEF/+HP × множник області | постійне посилення / лікування |
| Інструменти | pickup | кирка, бомба, транспортер поверхів, книга монстрів | дії поза кроком |
| NPC / крамниця | neutral | — | діалог, продаж, подія |
| Подія-клітина | zone | скрипт | спрацьовує при вході (засідка, діалог, відкриття воріт) |
| Вежа | container | автор, поверхи, складності, рейтинг | одиниця корпусу: дані + скрипти + плагіни |
| Реплей (录像) | object | список дій | детермінований запис проходження; основа рекорду |
| Плагін | object | код `plugins.js` | змінює правила/UI окремої вежі |

## Правила (КОЛИ → ЯКЩО → ТО)
Правила бою/ключів — як у [magic-tower](magic-tower.md). Тут — правила платформи.
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`.
- КОЛИ `contact(hero, monster)` → ТО `custom: «бій за формулою getDamageInfo»`, `damage(hero, n)`; ЯКЩО `hp_zero(hero)` → `lose`.
- КОЛИ `contact(hero, door)` → ЯКЩО `has(hero, key)` → ТО `take(hero, key)`, `disappear(door)`; інакше `block`.
- КОЛИ `enter(hero, event_cell)` → ТО `custom: «виконати скрипт події»` (діалог, `spawn`, `set_cell`, вибір).
- КОЛИ `input(action)` → ТО `custom: «дописати дію в реплей»`.
- КОЛИ `level_end` → ЯКЩО `custom: «гравець залогінений і консоль браузера закрита»` → ТО `custom: «завантажити рахунок і реплей (base64)»`; анонімний забіг — лише найнижчий рахунок.
- КОЛИ `custom: «сервер отримав рекорд»` → ТО `custom: «відтворити реплей і порахувати рахунок»`; ЯКЩО `custom: «результат збігся»` → ТО `custom: «запис у рейтинг вежі»`.
- КОЛИ `custom: «у реплеї бракує запису вибору»` → ТО `custom: «бекенд обирає останній варіант»`.
- КОЛИ `custom: «HP понад ефективний максимум»` → ТО `custom: «рахунок обрізається»` (анти-чит).
- КОЛИ `level_start` → ТО `choose(difficulty)` — гілки складності як події (з V2.7).
- КОЛИ `input(load)` → ТО `custom: «відновити сейв / автосейв»`; `A` — відкат до автосейву.
- Перемога: пройти вежу (фінальний бос/вихід). Поразка: HP = 0 або софтлок (ресурсів не вистачає). Рахунок: формула вежі (класично — HP наприкінці) → рейтинг.

## Керування і ввід
- Стрілки/WASD; клік/тап по клітині — автошлях з показом маршруту; ліворукий режим (V2.7.3).
- Гарячі клавіші рушія (книга монстрів, транспортер, сейв/завантаження, `A` — відкат, `R` — реплей зі швидкістю 1–6) — див. [magic-tower](magic-tower.md).
- Редактор: малювання тайлів палітрою, перетягування подій, автодоповнення скриптів, Ctrl+Z / Ctrl+Y; окрема мобільна версія.

## Вікна, меню, HUD
- `tower-list` (сайт) — список веж (玩塔), вхід у вежу онлайн; форум (论坛), логін (登录), «стати автором» (成为作者).
- `game-screen` — поверх, `stat-panel`, ключі, `inventory-bar`, `damage-preview` на монстрах.
- `codex-window` (книга монстрів), `floor-select` (транспортер), `shop-window`, `dialogue-window`, `save-slots`.
- `replay-window` — перегляд/перемотка реплею; `leaderboard` — рейтинг вежі (榜单).
- `difficulty-select` — вибір складності вежі.
- `editor-window` — карта + палітра (`editor.html`), `event-editor` — скрипти подій; мобільний редактор (`editor-mobile.html`).
- Переходи: `tower-list` → `game-screen` → `end-screen` (рахунок → завантаження) → `leaderboard`.

## Фічі поза полем
- `user-levels-browser` (2000+ веж), `level-editor` без програмування, `level-sharing` (публікація на сайт), `leaderboard-online` з перевіркою реплеєм (`+feature:replay-verification`).
- `replay` з перемоткою; `save-slots`, `autosave`, локальні офлайн-сейви (V2.8.2); `difficulty-presets` у межах однієї вежі.
- `mod-support` — плагіни на вежу (`plugins.js`, з V2.0.1, 2018); вбудовані плагіни.
- Спільнота: форум, QQ-група, конкурси проходження й будування веж.
- Доступність: HD UI, emoji, ліворукий режим.

## Варіації й родичі
- [magic-tower](magic-tower.md) — жанр і механіка; [tactical-nexus](tactical-nexus.md) — комерційна сучасна вежа з undo/redo; Flash-вежі 2000-х (新新魔塔 тощо) — попередники платформи.
- Як платформа — родич [tatham-collection](../pencil-logic/tatham-collection.md) (спільна оболонка) і веб-хабів рівнів (puzz.link, Sokoban-колекції).
- Осі варіацій веж у корпусі: **розмір карти** (класичний поверх / великі карти) · **правила** (чистий рушій / плагіни) · **складність** (одна / гілки) · **мета** (дійти / максимізувати рахунок).

## Цікавинки для курсу
- Рекорд, що перевіряється відтворенням реплею на сервері (детермінізм → лог дій = доказ) — 🥈.
- Вежа як дані: карта + таблиця монстрів + скрипти подій; рушій окремо — 🥉 (розділення логіки й контенту).
- Редактор подій на клітинах (діалог, засідка, відкриття) з малою мовою команд — 🥈.
- Плагін-API: вежа міняє правила без форку рушія — 🥇.
- Анти-чит: обрізання HP, блок завантаження з відкритою консоллю, анонім = мінімум — 📎 (корисний урок, чому клієнту не можна довіряти).
- Каталог веж із рейтингами, автором і складністю — 🥉 (бекенд + фільтри).

## Мапа на каталог
- Є: `move-4dir` · `key-and-door` · `hp-damage` · `item-pickup` · `stairs-levels` · `save-multi-slot` + `save-autosave` · `replay` + `replay-window` · `leaderboard` · `rating-system` · `in-game-editor` + `editor-palette` + `editor-draw-tools` + `editor-undo` + `editor-playtest` · `level-exchange` (публікація) · `level-bank` (2000+ веж) · `level-metadata` · `difficulty-levels` · `state-as-data` · `logic-render-split` · `keyboard-controls` · `cell-click` · `path-preview` (автошлях) · `codex-window`.
- **Нема** → пропозиції карток:
  - `+deterministic-combat`, `+damage-preview` — як у [magic-tower](magic-tower.md).
  - `+replay-verified-score` «Сервер перевіряє рекорд відтворенням реплею» · platform/online · 🥈.
  - `+event-scripting` «Скрипти подій на клітинах у редакторі» · levels/editor · 🥈.
  - `+plugin-api` «Плагіни рівня змінюють правила рушія» · platform/arch · 🥇.
  - `+anti-cheat-upload` «Обмеження на завантаження рахунку» · platform/online · 📎.

## Пропозиції до словників
- `+feature:replay-verification` — рекорд приймається лише після серверного відтворення реплею.
- `+feature:score-upload` — завантаження рахунку з клієнта (з обмеженнями анти-читу).
- `+feature:plugin-api` — плагіни на рівень (ширше за `mod-support`: правила, а не скіни).
- `+feature:event-editor` — редактор подій/скриптів клітин поруч із редактором карт.
- `+feature:left-hand-mode` — дзеркальне розташування елементів керування.
- `+window:tower-list` — каталог користувацьких рівнів на сайті (якщо не вистачить `user-levels-browser`-фічі).
- `+window:event-editor` — вікно скриптів події.
- `+window:floor-select` — вибір відвіданого поверху для телепорту (транспортер рушія).
- `+card:replay-verified-score`, `+card:event-scripting` — див. картки.

## Джерела
- ⭐ [H5魔塔广场](https://h5mota.com/) — 2000+ веж онлайн, система рахунку й рейтинги, редактор без програмування, форум, конкурси.
- [mota-js на GitHub](https://github.com/ckcz123/mota-js) — рушій, автор, BSD-3, редактори, плагіни.
- [mota-js README](https://raw.githubusercontent.com/ckcz123/mota-js/master/README.md) — історія версій 2017–2023, реплей-перевірка бекендом, base64-рахунок, анти-чит, великі карти, ліворукий режим.
- [mota-js functions.js](https://raw.githubusercontent.com/ckcz123/mota-js/master/project/functions.js) — формула бою (опрацьовано в [magic-tower](magic-tower.md)).

## Непевне
- (?) Moegirl-стаття з черги (`zh.moegirl.org.cn/魔塔`) рендериться скриптом — текст недоступний; історію Flash-веж і термінологію спільноти не перевірено.
- (?) Сторінка списку веж (`h5mota.com/games/`) віддала 503 — фільтри, теги, сортування каталогу не підтверджені.
- (?) Класичний розмір поверху 13×13 (11×11 поле + рамка) — з памʼяті.
- (?) Рік старту сайту h5mota.com; 2017 — рік V1.0 рушія (9 грудня).
- (?) Чи всі вежі мають рейтинг, чи лише «змагальні»; формула рахунку задається автором вежі (?).
