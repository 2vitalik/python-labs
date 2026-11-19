---
title: A Slug's Dream
slug: a-slugs-dream
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2023
platforms: [PC (Windows, macOS, Linux)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2303290/A_Slugs_Dream/", best: true, note: "опис: зʼїсти всі квіти й дійти до виходу; штовхати, тягнути й обертати матеріали (глина, камінь), портали, ріки, жар, ненадійний ґрунт; трейлер і 11 знімків"}
  - {kind: itch, url: "https://marcosd.itch.io/a-slugs-dream", note: "та сама гра на itch (Windows/macOS/Linux); спільнота: рівні «Well», «Wake Up», нелінійний доступ"}
  - {kind: other, url: "https://devuego.lat/bd/en/presskit/a-slugs-dream", note: "прескіт DeVuego: опис і ключові фічі"}
  - {kind: other, url: "https://gamebrain.co/game/a-slugs-dream", note: "зведення відгуків: портали, які можна штовхати, кілька розвʼязків, мало підказок"}
  - {kind: other, url: "https://thinkygames.com/games/a-slugs-dream", note: "картка Thinky Games"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A+Slug%27s+Dream+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-by-input, move-4dir, push-object, pull-object, multi-cell-size, height-levels, teleport-pair, collect-all, reach-exit, environment-death, undo-redo, restart-level, keyboard-controls, world-map, game-screen, +pushable-portals, +rotate-by-push, +fall-into-water, +crumbling-floor, +fragile-target]
proposes: ["+effect:climb", "+effect:eat", "+effect:dissolve", "+role:portal", "+trigger:crushed", "+card:pushable-portals", "+card:rotate-by-push", "+card:fragile-target"]
author: opus
date: 2026-11-19
---

# A Slug's Dream — голодний слимак зʼїдає всі квіти на острівцях і йде до виходу, штовхаючи камінь, глину й портали

## Суть
Покроковий 3D-Sokoban на острівцях серед води: слимак має зʼїсти всі квіти рівня, а потім дістатися виходу. Перешкоди — блоки з різних матеріалів (камінь, глина), які можна штовхати, тягнути й обертати, і **портали-бруски, які самі є рухомими блоками**: їх штовхають і повертають, змінюючи, куди веде прохід. Жар обпікає, розчавлена блоком квітка — провал, а механіки гра не пояснює: їх відкривають, переходячи між рівнями нелінійної мапи.

## Поле і час
- Воксельні острівці з клітин різної висоти над водою; слимак повзе по клітинах і, ймовірно, лізе на уступи — на кадрах він то лежить, то стоїть вертикально біля стінки (?).
- Хід = один крок слимака; світ стоїть без вводу.
- Шари: клітини острова (трава, жар, ненадійний ґрунт, ріка) · блоки й портали · квіти · вихід; навколо — вода.
- Камера 3D під кутом; чи обертається — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слимак | player | довжина ~2 клітини; лежить / стоїть (?) | повзе 4 напрямки; штовхає, тягне, обертає блоки; заходить у портали |
| Квітка | pickup | — | зʼїдається при контакті; розчавлена блоком — провал |
| Вихід (сірий куб із хвилястою білою гранню) | static | — | доступний після всіх квітів (?) |
| Камінь (світлий, зокрема L-подібний) | object | форма | штовхається; від поштовху в край повертається (трейлер) (?) |
| Глина (помаранчевий брусок) | object | — | штовхається; у воді розсипається (трейлер) (?) |
| Цегла | static | — | стіни й арки рівня (?) |
| Портал (зелений / червоний / синій брусок із хвилястою гранню) | object | колір пари | вхід у хвилясту грань → вихід із грані пари; брусок можна штовхати й обертати |
| Жар (червоні вуглики) | hazard | — | слимак на ньому — «fire burns you!» |
| Ріка | terrain | течія | «manipulate rivers» — потік, який можна змінити блоками (?) |
| Ненадійний ґрунт | terrain | — | «tread carefully» — руйнується (?) |
| Вода навколо | hazard | — | що падає за край, утрачено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(slug, dir)`.
- КОЛИ `contact(slug, block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «блок притиснутий до слимака ззаду»` → ТО `pull(block)` (?) — як саме тягнути, в джерелах не сказано.
- КОЛИ `contact(slug, block)` → ЯКЩО `custom: «поштовх у край довгого блока»` → ТО `rotate(block, 90)` (?).
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду уступ»` → ТО `custom: «вилізти вертикально»` (?).
- КОЛИ `enter(slug, portal_face)` → ТО `teleport(slug, pair_face)`; так само переносяться обʼєкти («transport objects») (?).
- КОЛИ `contact(slug, portal)` → ЯКЩО `free(cell_behind)` → ТО `push` — портал рухається, як блок.
- КОЛИ `contact(slug, flower)` → ТО `pickup`, `counter(flowers_left, -1)`.
- КОЛИ `contact(block, flower)` → ТО `lose`, `message("you crushed a flower! Z to undo, R to restart")`.
- КОЛИ `enter(slug, embers)` → ТО `lose`, `message("fire burns you! Z to undo, R to restart")`.
- КОЛИ `enter(clay, water)` → ТО `disappear_a` (?).
- КОЛИ `leave(slug, soil)` → ТО `set_cell(soil, hole)` (?).
- КОЛИ `contact(slug, exit)` → ЯКЩО `counter(flowers_left, ==, 0)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі квіти зʼїдено, слимак на виході. · Поразка: жар, розчавлена квітка (далі — Z або R, гра чекає). · Рахунок: нема.

## Керування і ввід
- Клавіатура: рух слимака; Z — undo; R — рестарт (підказка в банері після провалу).
- Часткова підтримка геймпада (категорія Steam).
- Нема окремих кнопок «тягнути» чи «обертати» в джерелах — (?).

## Вікна, меню, HUD
- `game-screen`: 3D-острівець без HUD (на знімках нічого, крім поля); банер угорі з причиною провалу й підказкою Z / R.
- `map-window`: мапа світу (overworld), з якої заходять у рівні; оновлення 2023 прибрало глухі кути на ній.
- Головне меню, налаштування — (?).
- Переходи: мапа → рівень → (вихід) мапа; провал → банер → undo або рестарт.

## Фічі поза полем
- Нелінійна мапа: рівні відкриваються не строго по черзі, складні бувають раніше простих (відгуки).
- `undo` (Z), `restart-level` (R); Steam Cloud.
- Ні досягнень, ні редактора в категоріях Steam.
- Механіки не пояснюються: гравець відкриває їх сам, повертаючись між рівнями (коментар Nifflas на itch).

## Варіації й родичі
- [Stephen's Sausage Roll](../thinky/stephens-sausage-roll.md) — відгуки порівнюють дизайн; жар і вода як небезпеки.
- [Snakebird](../thinky/snakebird.md) — істота-тіло, зʼїсти все й вийти.
- [Magnet Block](magnet-block.md), [An Architect's Adventure](an-architects-adventure.md), [Pipe Push Paradise](pipe-push-paradise.md) — 3D-Sokoban на острівцях.
- [A Monster's Snowball](a-monsters-snowball.md) — острівці, вода й предмети, що стають мостом.
- [Sokoban](sokoban.md) — основа.
- Осі варіацій:
  - **портал**: нерухома клітина / рухомий блок, який штовхають і обертають;
  - **матеріал блока**: однаковий / за матеріалом (глина у воді розсипається (?));
  - **ціль**: дійти / зібрати все й дійти / нічого не розчавити по дорозі.

## Цікавинки для курсу
- Портал-брусок: пара проходів, які самі є рухомими блоками з орієнтацією — 🥈 (телепорт + штовхання + поворот грані).
- Зібрати все, а потім до виходу (вихід «вмикається» лічильником) — 🌱.
- Квітка, яку можна розчавити: ціль, що робить частину ходів програшними — 📎.
- Поворот довгого блока від поштовху в край — 🥉.
- Висоти острова й підйом на уступ — 📎.
- Розвʼязувач BFS для острова з порталами, що рухаються — 🥇.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` ↔ крок; `push-object` / `pull-object` ↔ «push, pull»; `multi-cell-size` ↔ довгі й L-подібні блоки, тіло слимака; `height-levels` ↔ уступи острова; `teleport-pair` ↔ портали одного кольору; `collect-all` + `reach-exit` ↔ квіти, потім вихід; `environment-death` ↔ жар; `undo-redo` + `restart-level` ↔ Z / R; `keyboard-controls`; `world-map` ↔ overworld; `game-screen`.
- **Нема** → пропозиції карток:
  - `+fall-into-water`, `+crumbling-floor` — уже в корпусі.
  - `+pushable-portals` «Портали — рухомі блоки: їх штовхають і обертають» · entities/interact · 🥈 · слот {pair: color}.
  - `+rotate-by-push` «Поштовх у край довгого блока повертає його» · entities/move · 🥉.
  - `+fragile-target` «Ціль, яку можна знищити (розчавити) — провал» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:climb` — вилізти на уступ (слимак стає вертикально).
- `+effect:eat` — зʼїсти ціль (квітку); відмінне від `pickup` тим, що ціль — їжа, а не предмет в інвентар.
- `+effect:dissolve` — обʼєкт розпадається в середовищі (глина у воді) (?).
- `+role:portal` — портал як обʼєкт із гранню входу.
- `+trigger:crushed` — сутність розчавлено (квітка під блоком).
- `+card:pushable-portals`, `+card:rotate-by-push`, `+card:fragile-target` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: A Slug's Dream](https://store.steampowered.com/app/2303290/A_Slugs_Dream/) — опис і ключові фічі; трейлер і 11 знімків (переглянуто покадрово: портали-бруски, L-камінь, глина у воді, жар, банери «fire burns you!», «you crushed a flower!», «Z to undo, R to restart»); новини (overworld, softlocks).
- [itch.io: A Slug's Dream](https://marcosd.itch.io/a-slugs-dream) — опис, теги, спільнота (рівні «Well», «Wake Up»; механіки відкриваються самостійно).
- [DeVuego: прескіт](https://devuego.lat/bd/en/presskit/a-slugs-dream) — опис, дата 03.08.2023.
- [GameBrain](https://gamebrain.co/game/a-slugs-dream) — зведення відгуків: портали можна штовхати, кілька розвʼязків, нелінійний вибір рівнів.
- [Thinky Games](https://thinkygames.com/games/a-slugs-dream) — картка гри (лінк із результатів пошуку; сам сайт за брифом не фетчиться).
- YouTube: пошук «A Slug's Dream gameplay».

## Непевне
- (?) Тіло слимака: 2 клітини чи 1; як він лізе на уступи й чи може впасти з краю.
- (?) Як саме тягнути й обертати блоки; чим камінь відрізняється від глини, крім розпаду глини у воді.
- (?) Що можна робити з рікою; що відбувається з ненадійним ґрунтом; чи вода навколо — смерть.
- (?) Сірий куб із хвилястою гранню — вихід (так виглядає, по одному на рівень), але не підтверджено текстом.
- (?) Чи переносять портали блоки, як слимака; що буде, якщо грань порталу закрита.
- (?) Чим розчавлюється квітка — блоком (кадр трейлера з каменями між квітами) чи й самим слимаком.
- (?) Кількість рівнів не вказана ніде.
