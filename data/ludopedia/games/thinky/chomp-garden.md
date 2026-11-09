---
title: Chomp Garden
slug: chomp-garden
aka: [Garden Escape]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows, macOS), web (itch HTML5)]
links:
  - {kind: play, url: "https://lunardust.itch.io/chomp-garden", best: true, note: "грати в браузері: WASD — рух, Tab — оглянутись, Esc — налаштування; коментарі про штовхання стебла й горщика"}
  - {kind: steam, url: "https://store.steampowered.com/app/4457150/Chomp_Garden/", note: "опис: лампа, Chomp Plants ростуть до світла, Thief Plants тікають від нього, Hidey Bushes ховають світло; відгуки"}
  - {kind: other, url: "https://steamcommunity.com/id/chaotic_iak/recommended/4457150/", note: "відгук: світлячки → світло → хижі рослини; штовхання рослин; живопліт гасить світло; ~50 пазлів; undo ∞"}
  - {kind: itch, url: "https://lunardust.itch.io/sunflower", note: "прототип Garden Escape (2025): WASD, R — рестарт, Z — undo; девлог про кущі"}
  - {kind: other, url: "https://lunardust.itch.io/chomp-garden/devlog", note: "девлог 2026: світлячка можуть зʼїсти рослини, червоний ключ і замок, сейви, буферизація вводу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chomp+Garden+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, move-4dir, keyboard-controls, push-object, impassable-cells, item-pickup, key-and-door, touch-death, reach-exit, undo-unlimited, restart-level, world-map, player-camera, save-progress, +light-radius, +light-attract-grow, +flee-light, +light-hide-bush, +carry-goal-object, +collectible-secrets, +fast-travel-points]
proposes: ["+card:light-attract-grow", "+card:flee-light", "+card:light-hide-bush", "+ui:light-rays", "+feature:fast-travel"]
author: opus
date: 2026-11-09
---

# Chomp Garden — маленька лампа водить хижі рослини світлом: ті ростуть до нього, злодійки тікають, кущ ховає

## Суть
Короткий Sokoban-подібний пазл (1–2 години, близько 50 кімнат): гравець — лампа, що шукає свого песика в саду дивних рослин. Лампа збирає світлячків, і що більше їх несе, то далі світить; на світло реагують рослини. **Chomp Plants** ростуть стеблом до світла й можуть зʼїсти лампу, **Thief Plants** відступають від світла, **Hidey Bushes** ховають світло, поки лампа в кущі. Гравець не керує рослинами напряму — лише світлом, і ними ж будує проходи («shape plants with light»).

## Поле і час
- Квадратна сітка; кімнати-рівні з кольоровими стінами зʼєднані доріжками спільної мапи-саду (overworld, як у A Good Snowman за відгуком).
- Хід = крок лампи; рослини реагують після кроку (покроково, з буферизацією вводу).
- Світло малюється хрестом-променями від лампи вздовж рядка і стовпця (скриншоти); довжина = радіус світла 0–3 (за відгуком: 0 — світло не діє, 1 — сусідні квіти можуть зʼїсти, 2 — безпечна відстань для приманювання, 3 — максимум).
- Камера слідує за лампою; Tab — оглянути мапу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лампа | player | радіус світла 0–3 | крок у 4 напрямки; несе світлячків; світить хрестом |
| Світлячок | pickup | — | підібраний — радіус +1, лампа світиться; рослина може його зʼїсти |
| Місце світлячка (кільце) | zone | — | світлячків треба повернути на місця, щоб відкрити прохід (?) |
| Chomp Plant — голова | enemy | напрям росту | у промені світла росте на клітину до лампи; поруч зі світлою лампою — зʼїдає її |
| Chomp Plant — стебло | static | — | лишається за головою; блокує рух; штовхається (?) |
| Горщик | object | — | корінь рослини; штовхається; у пізніх рівнях відокремлюється від квітки |
| Thief Plant | enemy | — | у промені відходить від світла (?) |
| Hidey Bush (живопліт) | terrain | — | лампа всередині не світить |
| Стіна кімнати | static | — | непрохідна; пізня «особлива» стіна — у 1–2 пазлах (?) |
| Вихід кімнати (зірка в стіні?) | gate | закрито / відкрито | відкривається, коли світлячки на місцях (?) |
| Ключ / замок | pickup / gate | колір | замок на доріжці мапи відкривається ключем |
| Секрет | pickup | — | приховані колекційні предмети на мапі |
| Песик | neutral | — | мета сюжету в кінці саду |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(lamp, dir)`.
- КОЛИ `contact(lamp, pot|stem)` → ЯКЩО `free(cell_behind)` → ТО `push` (?) — рослини «штовхуються»; інакше `block`.
- КОЛИ `contact(lamp, firefly)` → ТО `pickup`, `counter(light_radius, +1)`.
- КОЛИ `turn_end(lamp)` → ЯКЩО `line_of_sight(chomp_head, lamp)` і `in_range(lamp, chomp_head, light_radius)` → ТО `move(chomp_head, toward_lamp)`, `grow(chomp, 1)` — за головою лишається стебло.
- КОЛИ `adjacent(chomp_head, lamp)` → ЯКЩО `counter(light_radius, >=, 1)` і `not state(lamp, hidden)` → ТО `lose` — лампу зʼїдено; далі undo/рестарт.
- КОЛИ `adjacent(chomp_head, firefly)` → ТО `disappear(firefly)` (?) — девлог: «firefly eaten by plants».
- КОЛИ `turn_end(lamp)` → ЯКЩО `line_of_sight(thief, lamp)` і `in_range(lamp, thief, light_radius)` → ТО `move(thief, away_from_lamp)` (?).
- КОЛИ `enter(lamp, bush)` → ТО `set_state(lamp, hidden)` — світло не діє; КОЛИ `leave(lamp, bush)` → ТО `clear_state(lamp, hidden)`.
- КОЛИ `contact(lamp, stem)` → ЯКЩО `not free(cell_behind)` → ТО `block` — стебло як стіна, якою рослину й «будують» у міст/барʼєр.
- КОЛИ `counter(fireflies_home, ==, all)` → ТО `set_state(exit, open)` (?) — «collect all the fireflies to open the exit path».
- КОЛИ `contact(lamp, key)` → ТО `pickup`; КОЛИ `contact(lamp, lock)` → ЯКЩО `has(lamp, key)` → ТО `disappear(lock)`.
- КОЛИ `reach(lamp, exit)` → ТО `custom: «кімнату пройдено, лампа виходить на доріжку мапи»`.
- КОЛИ `input(undo)` → ТО `undo(1)` (лише в межах кімнати); КОЛИ `input(restart)` → ТО `restart`.
- Перемога: кімната — вихід відкрито й досягнуто; гра — дійти до песика. · Поразка: лампу зʼїли → undo. · Рахунку нема.

## Керування і ввід
- WASD / стрілки — крок; Tab — оглянутись (камера); Esc — налаштування; undo і рестарт (прототип: Z, R).
- Кнопка бігу й швидке переміщення по мапі (відгук), геймпад (Steam-тег Controller).
- Ввід буферизується (v0.7.0); друга клавіша під час руху в ранній версії зупиняла лампу.

## Вікна, меню, HUD
- `main-menu` (?) з продовженням сейва (сейви — з v0.7.0).
- `map-window` / overworld: сад із кімнатами, доріжками, замками; приховані колекційні предмети видно на мапі.
- `game-screen`: кімната; промені світла на полі; HUD мінімальний (?).
- `settings-window` (Esc): мова (EN, JA, китайська), звук.
- `end-screen` фіналу з підказкою про секрети (v0.6.17 «Ending Screen Hint»); з нього Esc — грати далі.

## Фічі поза полем
- `world-map` (спільний сад), `collectibles` (секрети), опційні складні пазли.
- `undo` ∞ у межах кімнати, `restart-level`; підказок нема.
- `autosave`/`continue` (система збережень з v0.7.0), `cloud-save` у Steam, досягнення.
- Швидке переміщення між точками мапи, біг (відгук) — пропозиція `+feature:fast-travel`.
- `localization`: англійська, японська, китайська.

## Варіації й родичі
- Garden Escape (itch, 2025, прототип: рестарт R, undo Z, кущі) → Chomp Garden (itch HTML5, 2026) → Steam (23.09.2026, PawPaw Games).
- Родичі: `games/thinky/a-good-snowman-is-hard-to-build.md` (сад-overworld), `games/thinky/snakebird.md` (тіло-черга), вороги, що реагують на гравця, — `games/thinky/drod.md`; приманювання — Paquerette Down the Bunburrows (кролики тікають).
- **Осі варіацій:** реакція на світло — рости до / тікати / ігнорувати; світло — хрест / коло / промінь у напрямку погляду; що ховає світло — кущ / стіна; стебло — тверде / штовхуване; горщик — привʼязаний / окремий.

## Цікавинки для курсу
- Радіус світла = кількість світлячків, промені хрестом до перешкоди — 📎.
- Рослина-змійка: голова росте на 1 до світла, стебло лишається перешкодою — 🥉 (тіло-черга без руху хвоста).
- «Тікає від світла» як дзеркальна поведінка тієї ж умови — 📎.
- Кущ як стан «приховано», що вимикає всі реакції — 🌱.
- Небезпека на відстані 1 при радіусі ≥1: тонка межа «приманити, але не підійти» — 📎.
- Розвʼязувач BFS по станах (лампа, світлячки, голови й стебла) — 🥈.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` + `keyboard-controls`; `push-object` ↔ горщики/рослини; `impassable-cells` ↔ стіни, стебла; `item-pickup` ↔ світлячки, секрети; `key-and-door` ↔ ключ і замок; `touch-death` ↔ зʼїдена лампа; `reach-exit`; `undo-unlimited` + `restart-level`; `world-map`; `player-camera`; `save-progress`.
- Уже пропоновані іншими файлами: `+light-radius`, `+carry-goal-object`, `+collectible-secrets`, `+fast-travel-points`.
- **Нема** → пропозиції карток:
  - `+light-attract-grow` «Сутність росте до джерела світла» · entities/move · 🥉 · слот {range: light_radius}.
  - `+flee-light` «Сутність відступає від світла» · entities/move · 📎.
  - `+light-hide-bush` «Клітина, що ховає світло гравця» · entities/state · 🌱.

## Пропозиції до словників
- `+card:light-attract-grow`, `+card:flee-light`, `+card:light-hide-bush` — механік нема в каталозі.
- `+ui:light-rays` — промені світла, намальовані на полі (довжина = радіус).
- `+feature:fast-travel` — швидке переміщення між відкритими точками мапи-світу.

## Джерела
- ⭐ [Chomp Garden на itch](https://lunardust.itch.io/chomp-garden) — грати в браузері; клавіші; 13 рівнів у ранній збірці; коментарі (штовхання стебла, рестарт/undo).
- [Steam: Chomp Garden](https://store.steampowered.com/app/4457150/Chomp_Garden/) — опис трьох рослин і лампи; відгуки (радіус 0–3, стебла блокують, горщики окремо від квітів, «Thief flower», пізня стіна, ~1–2 год).
- [Відгук chaotic_iak](https://steamcommunity.com/id/chaotic_iak/recommended/4457150/) — світлячки дають світло, рослини приманюються й їдять; штовхання рослин; живопліт гасить світло; ~50 пазлів; undo ∞ у кімнаті; без підказок.
- [Garden Escape (прототип)](https://lunardust.itch.io/sunflower) — керування прототипу, девлог (кущі, мапа, undo).
- [Девлог Chomp Garden](https://lunardust.itch.io/chomp-garden/devlog) — зʼїдений світлячок, червоний ключ і замок, сейви, японська мова.

## Непевне
- (?) Світлячки: досить зібрати всіх чи треба віднести на «місця відпочинку» (кільця на скриншотах) — джерела розходяться.
- (?) Thief Plant: лише відступає від світла чи ще й краде (світлячків); на скриншотах — фіолетові «котячі» голови.
- (?) Чи промені зупиняються на стінах/стеблах і чи ростуть рослини на кожен хід, поки в промені.
- (?) Що саме штовхається — горщик, стебло чи вся рослина; що означає «квітка з хрестиками-очима» на скриншоті.
- (?) Роль «підказки-черв'яка» й метелика з девлогу.
