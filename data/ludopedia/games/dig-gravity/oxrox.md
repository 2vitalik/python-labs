---
title: OxRox
slug: oxrox
aka: [RoX, Safrosoft RoX]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: partial
  random: none
  goal: collect
year: 2024
platforms: [PC (Windows), macOS, Linux, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2866410/OxRox/", best: true, note: "опис: ремейк RoX (2001), детермінований Boulder Dash-геймплей, кооп двох Threshers з окремими рівнями й таблицями, редактор + Workshop"}
  - {kind: official, url: "https://fatoxgames.eu/oxrox/", note: "сторінка FatOx Games: «opinionated remake», оригінальний набір RoX + нові й бонусні колекції, Workshop-таблиці"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1839041357034062", note: "Co-op Update 1.1.0: локально / онлайн, кооп-редактор, мітки Solo / Co-op"}
  - {kind: other, url: "https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1789580505380476", note: "патч 1.0.21: самознищення Esc, ґнати, павуки, генератриси, вибухи, що породжують unid-и"}
  - {kind: other, url: "https://veg.by/en/blog/2024/12/23/safrosoft-rox-portable", note: "про оригінал RoX: клон Boulder Dash і Supaplex, v1.3–1.4, 108 додаткових рівнів, Rox Editor"}
  - {kind: other, url: "https://homeoftheunderdogs.net/game.php?name=RoX", note: "огляд оригіналу: гібрид Sokoban і Boulder Dash, земля, нерухомі блоки, камені з гравітацією, «світні ядерні шматки» для збору"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=OxRox+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, dig-terrain, gravity-fall, push-object, collect-quota, reach-exit, touch-death, player-death, projectile-shot, explode-area, button-toggle, temporary-modes, checkpoint, fog-of-war, in-game-editor, editor-palette, editor-playtest, editor-map-check, editor-window, level-exchange, leaderboard, replay, replay-window, online-multiplayer, lobby-window, controls-remap, game-settings, tutorial-window, +local-coop, +workshop-sharing, +shifting-gravity, +pressure-plate, +self-destruct, +collectible-secrets, +deterministic-physics, +validation-run, +linked-gates]
proposes: ["+effect:set_gravity", "+effect:save_checkpoint_state", "+feature:workshop", "+feature:validation-run", "+card:validation-run", "+card:linked-gates", "+card:deterministic-physics"]
author: opus
date: 2026-11-09
---

# OxRox — ремейк RoX: Boulder Dash із ракетами, перемикачами гравітації й кооперативом двох Threshers

## Суть
Детермінований Boulder Dash-подібний пазл: Thresher (зубата істота-«їжак») прокопується крізь землю, збирає задану кількість unid-ів, щоб відкрити портал-вихід, і уникає каменів, що падають, та ворогів. Від класики відрізняють ракети, які збивають обʼєкти на підльоті, міни, натискні плити з воротами, перемикачі гравітації та самознищення. OxRox (2024) — «упертий» ремейк freeware-гри RoX (Safrosoft, 2001–2003) з кооперативом на двох, редактором і Steam Workshop.

## Поле і час
- Квадратна сітка блоків, вид збоку з гравітацією вниз; перемикач гравітації розвертає її (reverse gravity).
- Real-time; поведінка повністю детермінована — рівень можна вивчити напамʼять; налаштування швидкості гри.
- Видимість обмежена радіусом огляду навколо Thresher (sight range задає редактор: типово 756, раніше 512) — решта поля в темряві.
- Великі рівні — камера за героєм (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Thresher | player | невразливість (тимчасово) | рух, копання (?), штовхає камені; стріляє ракетами; гине у вибухах; самознищення |
| Земля | terrain | — | прокопується (?) |
| Нерухомий блок | static | — | непрохідний |
| Камінь | object | — | падає без опори; штовхається (правила як у RoX) |
| Unid | pickup | квота рівня | «світний ядерний шматок»; квота відкриває портал; вибухи можуть породжувати unid-и |
| Бомба | object | — | вибухає (падаючи на щось?) (?) |
| Міна | object | — | ставиться на поверхню й прилипає до неї (?) |
| Ракета | projectile | — | летить від Thresher; знищує зустрічні обʼєкти й ракети |
| Хмара (кругла / квадратна) | object | форма | поведінка (?) |
| Натискна плита | switch | — | натиснута → відкриває повʼязані ворота |
| Натискні ворота | gate | відкриті / закриті | закриваючись, знищують ключ у проході |
| Ворота з перемикачем / нейтральні | gate | звʼязок | керуються повʼязаним перемикачем |
| Ключ | pickup | — | відмикає двері (?) |
| Перемикач гравітації | switch | напрям | розвертає гравітацію |
| Портал-вихід | gate | закритий / відкритий | вихід після квоти unid-ів |
| Падаючий бонус | pickup | — | падає як обʼєкт; дає невразливість (?) |
| Чекпоінт | static | — | зберігає стан (гравітація, ворота) для відродження |
| Секретний обʼєкт | pickup | — | відкриває секретну колекцію рівнів |
| Ґнат, павук | enemy | — | поведінка (?) |
| Генератриса | spawner | — | породжує ворогів (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next, dirt|empty)` → ТО `move(thresher, dir)`; земля → `set_cell(next, empty)` (?).
- КОЛИ `contact(thresher, rock)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `not supported(rock|bomb|powerup)` → ТО `fall(a)` у напрямку поточної гравітації.
- КОЛИ `contact(falling rock, thresher)` → ТО `custom: «Thresher гине»`; КОЛИ `died(thresher)` → ЯКЩО `custom: «чекпоінт узято»` → ТО `respawn(thresher, checkpoint)`, інакше `restart` (?).
- КОЛИ `contact(thresher, enemy)` → ТО `custom: «Thresher гине»` (?).
- КОЛИ `contact(thresher, unid)` → ТО `pickup`, `counter(unids, +1)`.
- КОЛИ `counter(unids, >=, quota)` → ТО `set_state(portal, open)`.
- КОЛИ `contact(thresher, portal)` → ЯКЩО `state(portal, open)` → ТО `win`, `custom: «час рівня → таблиця рекордів»`.
- КОЛИ `input(fire)` → ТО `spawn(missile)`; КОЛИ `contact(missile, object|missile)` → ТО `disappear_both`.
- КОЛИ `custom: «бомба вибухає»` → ТО `explode(area, into: empty|unid)`; КОЛИ `died(thresher)` → ТО `explode(area)` зі струсом камери.
- КОЛИ `input(place_mine)` → ЯКЩО `custom: «під клітиною опора, над нею не падає обʼєкт»` → ТО `place(thresher, mine)` (?).
- КОЛИ `enter(object|thresher, pressure_plate)` → ТО `set_state(pressure_gate, open)`; КОЛИ `leave(…)` → ТО `set_state(pressure_gate, closed)`; ЯКЩО `occupied(gate_cell, key)` → ТО `disappear(key)`.
- КОЛИ `contact(thresher, gravity_switch)` → ТО `custom: «гравітація розвертається для всіх обʼєктів»`.
- КОЛИ `picked(thresher, powerup)` → ТО `set_state(thresher, invulnerable, dur)`.
- КОЛИ `enter(thresher, checkpoint)` → ТО `custom: «зберегти стан: гравітацію, ворота»`.
- КОЛИ `input(self_destruct)` → ТО `explode(area)`, `restart` або відродження на чекпоінті.
- Кооп: два Threshers на одному рівні; спільні перемога, поразка, рестарти (деталі — (?)).
- Перемога: квота unid-ів + портал. · Поразка: смерть Thresher (камінь, вибух, ворог?) → чекпоінт / рестарт. · Рахунок: час проходження → таблиці рекордів (свої, глобальні, з фільтром за повтором).

## Керування і ввід
- Клавіатура, миша або геймпад; повне перепризначення клавіш, зокрема для геймпада.
- Esc — самознищення (типово), Enter — старт; рух — напрямки (?), постріл і міна — окремі кнопки (?).
- Кооп: локально — два профілі вводу на одному компʼютері; онлайн — через Steam (лобі, запрошення, Remote Play Together).
- Редактор: Space — перемикання Select / Draw, пензлі, звʼязки «перемикач → ворота», Esc — скасувати.

## Вікна, меню, HUD
- `main-menu` (Home): прогрес, останні рівні, рекомендації, нещодавні повтори, ярлики редактора, добірка Workshop.
- `level-select` (Play / Browse): колекції Solo / Co-op, кнопка рівня з найкращим часом.
- `game-screen`: поле в радіусі видимості; лічильник unid-ів і час (?).
- `end-screen`: діалог «рівень пройдено» з часом, рекордами й гарячою клавішею рестарту; підказка після поразки.
- `leaderboard`: ранги, відсоток, глобальна таблиця офіційних рівнів, фільтр за наявністю повтору.
- `replay-window`: перегляд завантажених повторів.
- `editor-window`: док-панелі, пензлі, звʼязки, перевірка рівня, браузер рівнів, кошик, довідка.
- `lobby-window`: кооп-лобі й запрошення.
- `settings-window` з вкладками: гамма, мертва зона геймпада, клавіші, MSAA, масштаб UI, оригінальна музика, захоплення курсора.
- `tutorial-window`: перше знайомство з грою.
- Переходи: Home → Play → рівень → end-screen → наступний / рестарт; Home → Editor → тестовий прогін → публікація у Workshop.

## Фічі поза полем
- Колекції: оригінальний набір RoX, нові офіційні, бонусні, секретна (через секретні обʼєкти або Supporter-DLC), спільнота з Workshop.
- `level-editor` + `level-sharing`: рівні й колекції Solo / Co-op; публікація лише після перевірки проходженням; превʼю обовʼязкові; кооп-редагування на двох.
- `leaderboard-online` для кожного рівня й Workshop; `replay` з завантаженням; `cloud-save`; досягнення.
- `mode-coop`: окремі кооп-рівні, прогрес і таблиці.
- `speed-control` (швидкість гри), `remap-controls`, мови EN / DE / FR, оригінальна музика RoX за вибором.

## Варіації й родичі
- Оригінал RoX (Safrosoft, брати Сафро, 2001–2003): freeware для Windows; v1.3 — чорне тло й випадкова палітра рівня; v1.4 — фонові картинки, 108 додаткових рівнів, Rox Editor.
- У сімʼї: [boulder-dash](boulder-dash.md), [supaplex](supaplex.md) (RoX — клон BD і Supaplex), [emerald-mine](emerald-mine.md) (BD на двох), [rocks-n-diamonds](rocks-n-diamonds.md), [heartlight](heartlight.md) (інший напрям падіння).
- **Осі варіацій**: напрям гравітації — фіксований / перемикач на рівні (OxRox) / по типу обʼєкта (Heartlight); випадковість — BD-імовірності / повний детермінізм (OxRox); гравці — 1 / двоє по черзі / кооп на одному полі.

## Цікавинки для курсу
- Перемикач гравітації: усі правила падіння й штовхання мають працювати в обидва боки — 🥉.
- Детермінізм: фіксований тік, порядок обходу, рекорди за часом і повтор як список вводів — 🥈.
- Ракета, що збиває обʼєкт на підльоті (зіткнення снаряда з падаючим тілом) — 📎.
- Натискна плита + ворота, що знищують ключ при закритті; звʼязки в редакторі — 📎.
- Публікація рівня лише після проходження автором (validation run із записом повтору) — 🥉.
- Кооп на одному полі з двома профілями вводу — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `dig-terrain` ↔ земля; `gravity-fall` ↔ камені, бомби, бонуси; `push-object` ↔ камені; `collect-quota` + `reach-exit` ↔ unid-и і портал; `touch-death` + `player-death`; `projectile-shot` ↔ ракети; `explode-area` ↔ бомби й самознищення; `button-toggle` ↔ плити й ворота; `temporary-modes` ↔ невразливість; `checkpoint`; `fog-of-war` ↔ радіус видимості; `in-game-editor` + `editor-palette` + `editor-playtest` + `editor-map-check` + `editor-window` ↔ редактор; `level-exchange` ↔ Workshop; `leaderboard`, `replay`, `replay-window`; `online-multiplayer` + `lobby-window` ↔ онлайн-кооп; `controls-remap`, `game-settings`, `tutorial-window`.
- Повтори з корпусу: `+local-coop` · `+workshop-sharing` · `+shifting-gravity` · `+pressure-plate` · `+self-destruct` · `+collectible-secrets`.
- **Нема** → пропозиції карток:
  - `+deterministic-physics` «Повністю детермінована клітинна фізика (рекорди й повтори відтворювані)» · code/architecture · 🥈.
  - `+validation-run` «Рівень публікується лише після проходження автором» · levels/editor · 🥉.
  - `+linked-gates` «Звʼязки перемикач → ворота, задані в редакторі» · levels/editor · 📎.

## Пропозиції до словників
- `+effect:set_gravity` — розвернути гравітацію для всіх обʼєктів (повтор з корпусу).
- `+effect:save_checkpoint_state` — чекпоінт зберігає не лише позицію, а й стан світу (напрям гравітації, відкриті ворота); `checkpoint` у словнику — лише точка відродження.
- `+feature:workshop` — публікація й завантаження рівнів через Steam Workshop (повтор з корпусу).
- `+feature:validation-run` — публікація рівня лише після його проходження автором, із записом повтору.
- `+card:validation-run`, `+card:linked-gates`, `+card:deterministic-physics` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: OxRox](https://store.steampowered.com/app/2866410/OxRox/) — опис ремейку, детермінізм, кооп, редактор, Workshop, категорії (split-screen, Remote Play), платформи, дата 1.06.2024.
- [FatOx Games: OxRox](https://fatoxgames.eu/oxrox/) — «opinionated remake», колекції, Workshop-таблиці.
- Steam News (через `api.steampowered.com/ISteamNews`): патчі 1.0.12–1.1.9 — бомби, камені, міни, хмари, плити й ворота, ключі, перемикачі гравітації, портал, бонуси, чекпоінти, unid-и, ракети Thresher, ґнати / павуки / генератриси, самознищення, повтори, редактор; найповніші — [Co-op Update 1.1.0](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1839041357034062) і [1.0.21](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1789580505380476).
- [veg.by: Safrosoft RoX Portable](https://veg.by/en/blog/2024/12/23/safrosoft-rox-portable) — історія оригіналу, версії, Rox Editor.
- [Home of the Underdogs: RoX](https://homeoftheunderdogs.net/game.php?name=RoX) — гібрид Sokoban і BD, елементи рівнів.
- YouTube: пошук «OxRox gameplay».

## Непевне
- (?) Поведінка ворогів (ґнат, павук, генератриса) і чи дотик вбиває; чи генератриса справді породжує ворогів.
- (?) Коли вибухає бомба і яка площа вибуху; хто ставить міни (гравець?) і що вони роблять.
- (?) Що роблять хмари і навіщо дві форми (кругла / квадратна — можливо, для скочування, як «круглі» обʼєкти BD).
- (?) Чи Thresher копає землю сам (у патчах про це нема; огляд оригіналу називає землю серед елементів); чи камені штовхаються лише горизонтально.
- (?) Як працює кооп: спільна чи окрема квота unid-ів, що буде, коли гине один.
- (?) RAWG (другий лінк черги) віддав 522 — у шапку не покладено.
