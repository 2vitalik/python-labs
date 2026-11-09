---
title: Mekorama
slug: mekorama
aka: [Мекорама]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2016
platforms: [iOS, Android, Google Daydream VR, web, Switch, PS4, PS Vita, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mekorama", best: true, note: "тап-до-руху, камера, механізми, редактор і QR-коди, платформи"}
  - {kind: official, url: "https://www.mekorama.com/", note: "фічі, платформи, веб-версія, Mekorama Studio"}
  - {kind: other, url: "https://www.mekorama.com/faq", note: "FAQ: QR-обмін, підказки, фізика Bullet"}
  - {kind: other, url: "https://mekoramaforum.com/posts/12827", note: "форум: поведінка R-ботів, сходи, кулі, слайдери"}
  - {kind: other, url: "https://mekoramaforum.com/posts/10708", note: "форум: eye/zapper, катання ботів один на одному, поле 16×16×16"}
  - {kind: other, url: "https://mekoramaforum.com/posts/938", note: "форум: мотори, шестерні, кулі, win-блоки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mekorama+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, gravity-fall, push-object, reach-exit, enemy-patrol, turn-when-blocked, carrier-platform, height-levels, drag-drop-piece, in-game-editor, editor-palette, editor-playtest, level-exchange, level-bank, sequential-levels, level-select, movement-animation, player-camera, +tap-to-walk, +rotate-structure, +slide-structure, +rotate-view-to-solve, +physics-body-avatar, +motor-gear, +rolling-ball, +level-as-qr, +walkability-modifier, +ride-on-bot, +paid-hint]
proposes: ["+effect:walk_path(a, cell)", "+effect:drag(part, axis, n)", "+trigger:released(part)", "+cond:walkable(cell)", "+role:mechanism", "+feature:level-qr-share", "+feature:pay-what-you-want", "+card:level-as-qr", "+card:walkability-modifier", "+card:physics-body-avatar"]
author: opus
date: 2026-11-09
---

# Mekorama — тапнув клітину, і робот B сам дибає туди крізь механічну діораму, яку ти крутиш і зсуваєш

## Суть
Гравець не керує роботом B напряму: тапає блок, і B сам іде туди найкоротшим шляхом, якщо шлях існує. Головна дія — **маніпулювати діорамою**: тягнути слайдери по рейках, крутити шестерні й частини конструкції, зсувати блоки, щоб скласти прохід до цілі. B — фізичне тіло (рушій Bullet): його можна зіштовхнути, і він падає. Поруч — автономні R/L-боти, на яких можна їхати і які можуть заважати.

## Поле і час
- Воксельна діорама в межах 16×16×16 блоків (за форумом); поза цією зоною B блоків «не бачить».
- Камера вільна: свайп — обертання навколо діорами, щипок — зум. Частина рівнів розвʼязується лише під правильним кутом огляду.
- Час — real-time з фізикою: рух ботів, кочення куль, обертання моторів відбуваються безперервно; поле при цьому клітинне (блоки, рейки, кроки по 90°).
- Гравітація вниз: без опори бот/куля падає (`gravity-fall`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| B (Bee) | player | фізичне тіло | іде до тапнутого блоку шляхом по прохідних блоках; не любить місць з блоком над головою; падає, якщо зіштовхнули |
| Звичайний блок (цегла, трава…) | static | прохідний зверху | опора для ходу |
| Кам'яний стовп | static | непрохідний для B | B на нього не стає (R-боти — лише зі сходів униз) |
| Сходи (прямі, поворотні, бокові) | terrain | напрям | переходи між висотами; B не сходить зі сходів убік |
| Win-блок (ціль) | static | — | B стає на нього → рівень пройдено; одного досить |
| Слайдер на рейці | object | рейка | гравець тягне вздовж рейки; несе на собі ботів/блоки |
| Перетягуваний блок | object | вісь | гравець тягне; R/L-бот на ньому завмирає, доки блок тримають |
| Мотор | switch | крок 90° вручну | обертає приєднані частини; вручну — кроками по 90° (?) |
| Шестерня | object | — | крутиться лише приєднана до мотора |
| Рухомий блок | object | — | B штовхає його, якщо той на шляху |
| Куля | object | фізика | котиться, відбивається від перешкод, зупиняється; може заповнити проліт (?) |
| R-бот / L-бот | enemy | напрям | іде вперед, розвертається лише коли спереду перешкода (R — праворуч, L — ліворуч (?)); може штовхати рухоме; може зіштовхнути B |
| Eye (око) | static | — | підсунуте під блок робить той блок непрохідним для всіх ботів (редакторний трюк) |
| Zapper | hazard | — | шкодить ботам (?); підсунутий під непрохідний блок робить його прохідним; R-боти до запперів стійкі (крім заппера на B) |
| Металевий стовп | static | — | з мотором дає вільне кочення / маятник (будівельний трюк спільноти) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, cell)` → ЯКЩО `path_exists(b, cell)` → ТО `custom: «B іде маршрутом до клітини»` (пропозиція `walk_path`).
- КОЛИ `input(tap, cell)` → ЯКЩО `not path_exists(b, cell)` → ТО `custom: «B іде до найближчої досяжної точки або стоїть»` (?).
- КОЛИ `input(drag, slider)` → ЯКЩО `free(rail_ahead)` → ТО `move(slider, dir)`; `carry` усіх, хто стоїть на ньому.
- КОЛИ `input(drag, draggable)` → ТО `custom: «блок зсувається за пальцем»`, `set_state(bot_on_it, frozen)`; КОЛИ `custom: «палець відпущено»` → ТО `clear_state(bot_on_it, frozen)`.
- КОЛИ `input(drag, motor)` → ТО `rotate(attached_parts, 90)`.
- КОЛИ `tick` → ЯКЩО `custom: «шестерня приєднана до мотора, що крутиться»` → ТО `rotate(gear)`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)` (B, R/L-боти, кулі).
- КОЛИ `contact(b, movable_block)` → ЯКЩО `free(cell_behind)` → ТО `push(movable_block)`.
- КОЛИ `tick` → ЯКЩО `free(ahead)` → ТО `move(r_bot, forward)`; КОЛИ `blocked(r_bot)` → ТО `face(r_bot, right)`.
- КОЛИ `contact(r_bot, b)` → ЯКЩО `custom: «B на краю»` → ТО `push(b)` → `fall(b)`.
- КОЛИ `enter(b, r_bot)` → ТО `carry`: B їде на R-боті; і навпаки — R-бот на B.
- КОЛИ `custom: «під блоком опинилось око»` → ТО `custom: «блок стає непрохідним»`; заппер — навпаки.
- КОЛИ `enter(b, win_block)` → ТО `win`, `next_level`.
- КОЛИ `edge(b)` або `custom: «B упав у прірву»` → ТО `restart` (?).
- Поразка: B упав з діорами (?) · Рахунку нема — лише пройдено/ні.

## Керування і ввід
- Тап по блоку — ціль для B (`control: indirect`).
- Перетягування механізмів пальцем: слайдер — вздовж рейки, мотор/ручка — кроками по 90°, блок — по осі.
- Свайп по порожньому — обертання камери; щипок — зум.
- У VR (Daydream) — вказівник контролера замість тапу (?).

## Вікна, меню, HUD
- `main-menu` → `level-select` (сітка рівнів-діорам з позначками пройдено) · фан-рівні · редактор.
- `game-screen`: діорама, мінімальний HUD — кнопка паузи.
- `pause-menu`: продовжити, рестарт, «Show hint?» (платна підказка) → `hints-window`.
- `editor-window`: палітра блоків, розстановка у вокселі, плейтест, збереження як картка з QR.
- `custom-window` «сканер QR»: камера пристрою або картинка з галереї → рівень у колекцію.
- `end-screen`: короткий підсумок рівня → наступний.

## Фічі поза полем
- `level-editor` з тими самими блоками, що й у кампанії; `level-sharing` як картинка з QR-кодом (будь-де, де можна запостити зображення).
- `user-levels-browser`: тисячі фан-рівнів, 25 рівнів «master makers» (за сайтом).
- `hint` за in-app покупку; модель pay-what-you-want.
- Mekorama Studio — окремий інструмент для просунутих авторів.
- Daydream-VR-версія; веб-версія.

## Варіації й родичі
- Родичі: Captain Toad (повертай камеру, щоб знайти шлях), Monument Valley (тап-до-руху + обертання структур), Lemmings/Troddlers (автономні ходоки), Fez (кут огляду як ключ).
- Осі: **керування** (пряме / тап-ціль / програма) · **маніпуляція світом** (обертання / зсув / мотори) · **фізика** (клітинна / справжнє тіло, яке можна зіштовхнути).

## Цікавинки для курсу
- Тап-до-руху: BFS по прохідних верхах блоків у 3D-сітці з правилами сходів — 🥉 (графи на вокселях).
- Слайдер на рейці, що везе ботів — 📎 (обʼєкт із пасажирами).
- Мотор + шестерні: обертання групи приєднаних блоків на 90° і перерахунок прохідності — 🥈.
- R/L-бот «вперед, при упорі поворот» — 🌱 (класичний `turn-when-blocked`).
- Рівень як QR-код: серіалізація 16³ вокселів у компактний рядок — 🥉.
- Модифікатори прохідності (око/заппер під блоком) — 📎 (властивість клітини від сусіда знизу).

## Мапа на каталог
- Є: `cell-click` ↔ тап ціль · `gravity-fall` · `push-object` ↔ рухомий блок · `reach-exit` ↔ win-блок · `enemy-patrol` + `turn-when-blocked` ↔ R/L-боти · `carrier-platform` ↔ слайдер, бот-на-боті · `height-levels` ↔ сходи · `drag-drop-piece` ↔ перетягування механізмів (наближено) · `in-game-editor`, `editor-palette`, `editor-playtest`, `level-exchange`, `level-bank` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+tap-to-walk` (як у Monument Valley) · `+rotate-structure` · `+slide-structure` · `+rotate-view-to-solve` (як у Captain Toad).
  - `+physics-body-avatar` «Аватар — фізичне тіло на клітинному полі» · entities/move · 🥈.
  - `+motor-gear` «Мотор крутить приєднані частини» · entities/move · 🥈.
  - `+rolling-ball` «Куля котиться й відбивається до зупинки» · entities/move · 📎.
  - `+level-as-qr` «Рівень як QR-код» · levels/format · 🥉.
  - `+walkability-modifier` «Блок під блоком змінює прохідність» · entities/legality · 📎.
  - `+ride-on-bot` «Їхати на іншому боті» · entities/move · 📎.
  - `+paid-hint` «Підказка за покупку» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+effect:walk_path(a, cell)` — сутність сама йде побудованим шляхом до клітини (не `move` на 1).
- `+effect:drag(part, axis, n)` — гравець тягне частину механізму вздовж осі/по колу.
- `+trigger:released(part)` — гравець відпустив частину, яку тягнув.
- `+cond:walkable(cell)` — клітину можна пройти з урахуванням модифікаторів.
- `+role:mechanism` — частина поля, якою керує гравець (слайдер, мотор), а не обʼєкт без волі.
- `+feature:level-qr-share` — обмін рівнями через QR-картинку.
- `+feature:pay-what-you-want` — гра з добровільною ціною.
- `+card:level-as-qr` · `+card:walkability-modifier` · `+card:physics-body-avatar` — див. вище.

## Джерела
- ⭐ [Wikipedia: Mekorama](https://en.wikipedia.org/wiki/Mekorama) — керування тапом і камерою, шестерні й слайдери, редактор, QR-обмін, підказки, платформи, автор Martin Magni.
- [mekorama.com](https://www.mekorama.com/) — список фіч: 50 діорам, 25 рівнів master makers, Studio, VR, веб.
- [FAQ](https://www.mekorama.com/faq) — QR-сканування, «Show hint?» у паузі, фізика Bullet, B можна зіштовхнути.
- [Форум: R-боти](https://mekoramaforum.com/posts/12827) — поведінка R-ботів на сходах, кулях, перетягуваних блоках; запери.
- [Форум: eye/zapper](https://mekoramaforum.com/posts/10708) — модифікатори прохідності, бот на боті, межа 16×16×16.
- [Форум: побажання](https://mekoramaforum.com/posts/938) — мотори й шестерні, кулі, «одного win-блоку досить».
- YouTube: пошук «mekorama gameplay».

## Непевне
- (?) Кількість рівнів: Wikipedia — 120, офіційний сайт — 50 діорам + 25 master makers, Famitsu — 100.
- (?) Точний ефект заппера на B (знищує, відкидає, зупиняє) і чи L-бот — дзеркало R-бота з поворотом ліворуч.
- (?) Що робить B, коли тапнута клітина недосяжна; чи падіння = автоматичний рестарт.
- (?) Мотор: обертається сам постійно чи лише коли тягнеш; на форумі — «вручну кроками 90°».
- (?) Керування у VR-версії.
