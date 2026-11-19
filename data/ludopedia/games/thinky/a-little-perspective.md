---
title: A Little Perspective
slug: a-little-perspective
aka: []
family: thinky
also: []
klass: avatar
axes:
  field: iso
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC, Mac, Linux, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3485300/A_Little_Perspective/", best: true, note: "опис і трейлери: сітка, поворот камери, лінія зору, постійність обʼєктів, 200+ пазлів, відкритий хаб; є демо"}
  - {kind: other, url: "https://www.appbank.net/2026/04/06/game/2965574.php", note: "AppBank (JA): ізометрія, мета — дійти до цілі, поворот камери відкриває невидимі звʼязки й закриває «відкриті» шляхи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A+Little+Perspective+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [move-by-input, keyboard-controls, push-object, reach-exit, height-levels, world-map, level-unlock, controls-remap, volume-control, +camera-rotate, +perspective-alignment, +invisible-not-walkable, +hint-hologram, +chapter-unlock-quota, +story-chapters]
proposes: ["+cond:visible", "+effect:rebuild_graph", "+card:invisible-not-walkable", "+card:hint-hologram"]
author: opus
date: 2026-11-19
---

# A Little Perspective — ізометрична сітка, де поворот камери змінює, куди можна пройти

## Суть
Покрокова головоломка соло-розробника Tad Cordle (Steam, 2026): персонаж іде клітинами ізометричного рівня до цілі, а гравець повертає камеру. Ракурс — частина правил: поворот створює нові проходи, дозволяє обійти перешкоди й «неможливу фізику», а може й показати, що шлях, який здавався відкритим, закритий. Тема — лінія зору й постійність обʼєктів: не можна стати на блок, якого не видно. Понад 200 пазлів у відкритому хабі, сюжет розкривається з просуванням.

## Поле і час
- Рівень — 3D-сітка блоків з висотами в ізометричній проєкції (`field: iso`); камеру можна повертати навколо рівня (крок повороту (?)).
- Звʼязність клітин залежить від того, що видно з поточного ракурсу (опис Steam і AppBank); точна модель — (?).
- Покроково: хід — крок персонажа, поштовх блока чи поворот камери (?); Steam позначає гру як «Playable without Timed Input».
- Рівні пронумеровані «світ-рівень» (у патчах — 3-6, 6-10, 10-5); тематичні зони — денне містечко, синій пейзаж, кіберпанк-ніч, темна таємнича зона (AppBank).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | клітина, висота | ходить сіткою; не сходить з обриву й не стає на невидимий блок — тоді лише хитається |
| Блок рівня | terrain | висота | опора для ходьби; чи сусідить з іншим, залежить від ракурсу (?) |
| Блок, що штовхається | object | — | зсувається поштовхом; у проєкції може накладатися на інший блок |
| Ціль | static | — | дійти — рівень пройдено |
| Голограма-підказка | mark | — | зʼявляється з меню паузи: де стати й куди подивитись |
| Міст у хабі | gate | число на мосту | відкривається прогресом (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` and `custom: «клітина видима й досяжна з поточного ракурсу»` → ТО `move(player, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, cliff)` → ТО `block`, `animate(wobble)`.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, block)` and `not custom: «блок видимий з камери»` → ТО `block`, `animate(wobble)`.
- КОЛИ `input(rotate_camera)` → ТО `camera(rotate)`, `custom: «звʼязки між клітинами перераховуються за новим видом»` (?).
- КОЛИ `contact(player, push_block)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `reach(player, goal)` → ТО `win`, `next_level` (або повернення в хаб (?)).
- КОЛИ `input(hint)` (меню паузи) → ТО `spawn_at(hologram, корисні клітини)`.
- КОЛИ `counter(solved, >=, n)` → ТО `unlock(bridge)` у хабі (?).
- Перемога: персонаж на цілі. · Поразки, схоже, нема: падіння з обриву гра не дозволяє (?). · Рахунку нема.

## Керування і ввід
- Клавіатура з перепризначенням, геймпад (DualShock, DualSense, зовнішні на Steam Deck), або лише миша (категорії Steam).
- Меню однією рукою: WASD — вибір, Space — підтвердити, Backspace — назад (патч квітня 2026).
- Конкретні клавіші ходу й повороту камери — (?).

## Вікна, меню, HUD
- `game-screen` — ізометричний рівень; підказки-голограми в самому рівні.
- `pause-menu` — серед пунктів увімкнення підказок (оновлення демо, лютий 2026).
- `settings-window` — Options › Graphics: повноекранний / безрамковий режим, вимкнення зернистої текстури; розмір тексту, гучність, субтитри (категорії Steam).
- `map-window` — відкритий хаб-світ з мостами, на яких числа; чи це окремий екран, чи прохідний рівень — (?).
- Переходи: хаб → рівень → (ціль) хаб; міст відкривається прогресом.

## Фічі поза полем
- 200+ пазлів у відкритому хабі з вільним порядком; сюжет, що розкривається з глибиною гри (`+story-chapters`).
- Підказки-голограми на вимогу; 23 досягнення Steam (Perspective, Obstruction, Perseverance, Displacement, Permanence, Descent, Transcendence та «+»-версії).
- Steam Cloud, Steam Deck, мови EN і спрощена китайська; безкоштовне демо (травень 2025).

## Варіації й родичі
- Родичі в корпусі: [Monument Valley](monument-valley.md) (шлях за збігом проєкцій), [Islands of Insight](islands-of-insight.md) (`+perspective-alignment`), [Toodee and Topdee](toodee-and-topdee.md) (перемикання проєкції), [Hoshigami](../tactics/hoshigami.md) (`+camera-rotate` у тактиці — лише огляд).
- Осі варіацій:
  - **що змінює гравець**: камеру (тут) / частини споруди (Monument Valley) / проєкцію кімнати (Toodee and Topdee);
  - **що робить ракурс**: лише показує / створює й закриває шляхи (тут);
  - **невидиме**: існує як завжди / недоступне для кроку (тут).

## Цікавинки для курсу
- Ізометрична камера з поворотом і перерахунком сусідства клітин за видом — 🥇.
- Перевірка «клітину видно з камери» (оклюзія в ізометрії) як умова кроку — 🥈.
- Хаб з мостами, що відкриваються числом розвʼязаних пазлів — 📎.
- Підказка-голограма: позначити клітину й напрям погляду — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` ↔ хід персонажа; `push-object` ↔ блоки; `reach-exit` ↔ ціль; `height-levels` ↔ висоти й обриви; `world-map` · `level-unlock` ↔ хаб і мости; `controls-remap` · `volume-control` ↔ налаштування.
- **Нема** → пропозиції карток:
  - `+invisible-not-walkable` «Не можна ступити на те, чого не видно з камери» · entities/legality · 🥈.
  - `+hint-hologram` «Підказка показує, де стати й куди дивитись» · interface/hud · 🌱.
  - `+camera-rotate` · `+perspective-alignment` · `+chapter-unlock-quota` · `+story-chapters` — уже в корпусі.

## Пропозиції до словників
- `+cond:visible` — клітина чи блок видимі з поточного ракурсу (тут `custom: «клітина видима…»`, `custom: «блок видимий з камери»`).
- `+effect:rebuild_graph` — перерахувати сусідство клітин після зміни виду (тут `custom: «звʼязки… перераховуються»`; уже пропоноване в Monument Valley).
- `+card:invisible-not-walkable`, `+card:hint-hologram` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `reach`, `counter`, `cell`, `occupied`, `animate`, `camera`, `spawn_at`, `unlock`.

## Джерела
- ⭐ [Steam: A Little Perspective](https://store.steampowered.com/app/3485300/A_Little_Perspective/) — опис (grid-based, line-of-sight, object permanence, «Rotate the camera to change your perspective — create new pathways, sidestep obstructions, and exploit impossible physics», 200+ пазлів, відкритий хаб, сюжет, керування), реліз 3.04.2026, Tad Cordle; новини Steam (через API): демо-оновлення лютого 2026 (голограми-підказки, хитання при спробі зійти з обриву чи стати на невидимий блок, числа на мостах хабу) і два патчі квітня 2026 (поштовх блока за край екрана, блоки, що накладаються, рівні 3-6, 6-10, 10-5).
- [AppBank](https://www.appbank.net/2026/04/06/game/2965574.php) — ізометрія, мета — дійти до цілі, поворот камери відкриває звʼязки й закриває «відкриті» шляхи, тематичні зони.
- Рецензія Thinky Games (квітень 2026; 403 у фетчі) — за сніпетом пошуку, згадує рівень, де розвʼязок — знайти ракурс, щоб піднятися сходоподібною спорудою.
- YouTube: [пошук](https://www.youtube.com/results?search_query=A+Little+Perspective+gameplay).

## Непевне
- (?) Головне правило — як саме вигляд задає прохідність (збіг проєкцій, як у Monument Valley, чи лише оклюзія) — джерела описують його загальними словами; правила в цьому файлі — модель, не перевірена в грі.
- (?) Крок повороту камери (90°?) і чи поворот — окремий хід.
- (?) Чи є undo й рестарт рівня, чи є поразка.
- (?) Що означають числа на мостах хабу (кількість розвʼязаних пазлів?) і як повʼязані з зонами назви досягнень.
- (?) Поведінка блока, виштовхнутого за край екрана, після патча (до нього гра падала).
