---
title: Cataclismo
slug: cataclismo
aka: []
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: ai
  info: partial
  random: setup
  goal: survive
year: 2025
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cataclismo", best: true, note: "Digital Sun / Hooded Horse; ранній доступ 22.07.2024, реліз 20.03.2025; 100+ деталей у стилі Lego, власна стійкість кожної, обвали, день/ніч, Horrors, цитадель, кисень"}
  - {kind: steam, url: "https://store.steampowered.com/app/1422440/", note: "дерево vs камінь, несучі колони, падіння деталей вбиває своїх і чужих, висота для стрільців, бійниці, режими Campaign / Skirmish / Challenge, редактор мап, креслення"}
  - {kind: other, url: "https://www.avclub.com/cataclismo-review-early-access", note: "огляд: будування з базових блоків у зупиненому часі, вищі стіни — міцніші й дорожчі, кисень, Prosperity, точки перемотки"}
  - {kind: other, url: "https://www.gog.com/game/cataclismo", note: "опис GOG: модульне будування по деталі або за кресленням"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cataclismo+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [destructible-blocks, height-levels, enemy-waves, hp-damage, melee-vs-ranged, tower-range, game-pause, difficulty-levels, in-game-editor, level-exchange, rewind, +day-night-cycle, +structural-support, +crush-by-falling, +tower-on-wall, +blueprints, +piece-palette-categories, +material-tiers, +build-in-paused-time, +workshop-sharing]
proposes: ["+trigger:support_lost", "+effect:collapse", "+role:block", "+ui:stability-overlay", "+window:blueprint-library", "+feature:time-freeze-build", "+card:structural-support"]
author: opus
date: 2026-11-09
---

# Cataclismo — RTS-оборона, де стіни складаєш з деталей, як з Lego: кожна має власну стійкість, а обвал давить і своїх, і чужих

## Суть
Real-time стратегія з елементами TD: удень збираєш дерево й камінь, будуєш поселення й фортецю, уночі хвилі Horrors (мутантів із Туману) йдуть на цитадель. Межова для сімʼї: бій і рух — вільні, а **сітковий шар** — конструктор укріплень з понад 100 деталей (блоки, сходи, дахи, бійниці), що кладуться впритул одна до одної й мають власні правила стійкості. Тут описано лише цей шар; економіка, кисень і дослідження — абзацом тут.

## Поле і час
- Укріплення — обʼємна збірка деталей на рельєфі (`field: 3d`): деталі стають на інші деталі або на землю, висота дає перевагу стрільцям.
- Будувати можна в зупиненому часі (вільне будування з базових блоків); бій — real-time, удень дрібні вилазки, вночі — повна атака.
- Карти Challenge/Survival — процедурні (seed); частина світу відкривається експедиціями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Деталь з дерева | static (`+role:block`) | дешева, швидка | несе вагу слабше за камінь |
| Деталь з каменю | static (`+role:block`) | міцна, з кар'єрів | основа високих стін |
| Категорії деталей | — | Primary · Secondary · Stairs · Advanced · Roofs · Tactical (?) | палітра будування |
| Несуча колона | static | — | тримає деталі над собою |
| Бійниця / пілбокс | tower | висота | стрільці (лучники, канонири, метальники) бʼють з висоти |
| Пастки, вогняні стріли, горщики з отрутою | hazard | — | на вузьких місцях і з бійниць |
| Цитадель | static | HP | знищено — поразка |
| Будинки | static | — | другий рубіж, якщо стіни впали |
| Horrors | enemy | типи зʼявляються з часом | ідуть на цитадель, бʼють стіни |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place_piece, spot)` → ЯКЩО `supported(piece)` and `has(player, wood|stone)` → ТО `place(player, piece)`, `currency(-cost)`; інакше `block`.
- КОЛИ `destroyed(piece)` → ЯКЩО `not supported(piece_above)` → ТО `fall(piece_above)` — ланцюг обвалу.
- КОЛИ `contact(falling_piece, unit)` → ТО `damage(unit, n)` — і для своїх, і для Horrors.
- КОЛИ `contact(horror, piece)` → ТО `damage(piece, n)`; КОЛИ `hp_zero(piece)` → ТО `custom: «деталь кришиться, інколи обвалюється вся споруда»`.
- КОЛИ `in_range(archer, horror, range)` → ЯКЩО `custom: «стрілець вище за ціль»` → ТО `damage(horror, n)` з бонусом висоти (?).
- КОЛИ `custom: «настала ніч»` → ТО `wave_start`; КОЛИ `hp_zero(citadel)` → ТО `lose`.
- Перемога: пережити ночі / виконати місію · Поразка: знищено цитадель · Рахунок: — .

## Керування і ввід
- Мишею: палітра деталей → поставити деталь на деталь; креслення (свої або спільноти) ставляться цілком; час можна зупинити на час будування.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Campaign (11 місій) · Skirmish · Challenge/Survival (нескінченні хвилі).
- `game-screen`: поле, палітра деталей за категоріями, ресурси (дерево, камінь, кисень), таймер до ночі, `+ui:stability-overlay` (?).
- `+window:blueprint-library` — креслення фортець (свої й Workshop); `editor-window` — редактор мап Skirmish.

## Фічі поза полем
- `level-editor` + `level-sharing` (мапи й креслення через Steam Workshop), `seed-input` для власних Survival-мап, точки перемотки (одноразові швидкі збереження), `difficulty-presets`.

## Варіації й родичі
- Родичі в сімʼї: [they-are-billions](they-are-billions.md) (стіни проти орд, без фізики), [thronefall](thronefall.md) (день/ніч), [rampart](rampart.md) (будуєш стіни з фігур на сітці), [emberward](emberward.md) (стіни-тетроміно).
- Поза сімʼєю: [cataclysm-dark-days-ahead](../roguelike/cataclysm-dark-days-ahead.md) — інша гра, лише схожа назва.
- **Осі варіацій**: стіна — клітина без ваги / фігура-поліоміно / деталь зі стійкістю й обвалом.

## Цікавинки для курсу
- Стійкість блоків: «опора знизу» як граф, від якого рахуємо, що впаде після руйнування — 🥉 (BFS від землі по деталях).
- Обвал як зброя: падаючі деталі бʼють усіх під собою — 📎.
- Матеріали з різною міцністю й ціною (дерево/камінь) — 🌱.

## Мапа на каталог
- Є: `destructible-blocks` ↔ деталі кришаться; `height-levels` ↔ висота стрільців; `enemy-waves`, `hp-damage`, `melee-vs-ranged`, `tower-range`; `game-pause` ↔ будування в паузі; `difficulty-levels`; `in-game-editor` + `level-exchange` ↔ редактор і Workshop; `rewind` ≈ точки перемотки.
- Уже в корпусі як `+`: `+day-night-cycle`, `+structural-support`, `+crush-by-falling`, `+tower-on-wall`, `+blueprints`, `+workshop-sharing`.
- **Нема**: `+piece-palette-categories` «Палітра деталей за категоріями» · interface/input · 🌱; `+material-tiers` «Матеріали з різною міцністю й ціною» · game-logic/economy · 🌱; `+build-in-paused-time` «Будування в зупиненому часі» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:support_lost` — деталь утратила опору; `+effect:collapse` — ланцюгове падіння всього, що трималось на зруйнованій деталі.
- `+role:block` — будівельна деталь з матеріалом і HP.
- `+ui:stability-overlay` — підсвітка стійкості деталей; `+window:blueprint-library` — бібліотека креслень.
- `+feature:time-freeze-build` — пауза для будування; `+card:structural-support`.

## Джерела
- ⭐ [Wikipedia: Cataclismo](https://en.wikipedia.org/wiki/Cataclismo) — жанр, 100+ деталей, стійкість за висотою й матеріалом, обвали, день/ніч, цитадель, режими, дати.
- [Steam](https://store.steampowered.com/app/1422440/) — дерево/камінь, несучі колони, падіння вбиває всіх, висота, бійниці, режими, редактор, креслення.
- [AV Club: огляд раннього доступу](https://www.avclub.com/cataclismo-review-early-access) — базові блоки в зупиненому часі, висота стін і ціна, ресурси, точки перемотки, 11 місій.
- [GOG](https://www.gog.com/game/cataclismo) — опис модульного будування.
- YouTube: пошук «Cataclismo gameplay».

## Непевне
- (?) Чи деталі стають у тривимірну сітку (snap до клітин), чи вільно; у джерелах лише «Lego», «блок за блоком», «деталі защіпаються» (пошуковий фрагмент Sportskeeda, сторінка не відкрилась).
- (?) Категорії деталей (Primary…Tactical) — з того ж фрагмента.
- (?) Як саме рахується стійкість (числа, підсвітка) і бонус висоти; чи Horrors лізуть на стіни.
- (?) Усі числа (HP деталей, ціни) — не бачив.
