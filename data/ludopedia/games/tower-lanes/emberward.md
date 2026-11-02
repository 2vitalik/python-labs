---
title: Emberward
slug: emberward
family: tower-lanes
also: [roguelike, falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: survive
year: 2024
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2459550/Emberward/", best: true, note: "опис: лабіринт з тетроміно-блоків, вежі 1×3/2×2/3×3, руни, режими; EA 25.06.2024, реліз 17.09.2026"}
  - {kind: other, url: "https://www.pcgamer.com/games/strategy/drop-blocks-to-make-your-own-maze-in-the-demo-for-tower-defense-game-emberward", note: "PC Gamer про демо: «кидай блоки, будуй лабіринт»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=emberward+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [enemy-waves, enemy-reached-base, chase-bfs, reachability-check, multi-cell-size, projectile-shot, hp-damage, temporary-modes, round-currency, dungeon-generation, leaderboard, save-progress, drag-drop-piece, +polyomino-placement, +maze-by-towers, +path-recompute, +tower-placement, +tower-range, +deck-draw, +card-sigils, +run-relics, +limited-blocks, +tower-on-wall]
proposes: ["+trigger:path_changed", "+trigger:phase_start", "+cond:path_exists", "+effect:rotate", "+effect:draw", "+effect:recompute_path", "+role:tower", "+role:card", "+ui:ghost-piece", "+ui:range-circle", "+ui:path-preview", "+window:map-window", "+window:choice-window", "+window:character-select", "+feature:run-map", "+feature:meta-progression", "+axis:session"]
author: opus
date: 2026-11-02
---

# Emberward — Tetris × tower defense: лабіринт для ворогів складаєш із карт-тетроміно, вежі ставиш поруч

## Суть
Перед боєм гравець розкладає з руки **карти-блоки** — фігури-тетроміно — на сітку, будуючи лабіринт, по якому монстри підуть до цілі; блоків обмежено, тож кожна фігура — вибір: подовжити шлях чи дати місце вежі. Вежі різних форм (1×3, 2×2, 3×3) ставляться на поле як окремі карти. Між боями — роглайк-нагороди: нові блоки, вежі, реліквії та руни, що модифікують карти-блоки.

## Поле і час
- Квадратна сітка з точками появи монстрів і ціллю, яку вони атакують (?); генерована мапа на кожен забіг.
- Фаза будування — без тиску часу (?): гравець кладе блоки з руки, бачить шлях; фаза бою — real-time, монстри йдуть найкоротшим шляхом крізь лабіринт.
- Блок займає 4 клітини (тетроміно; руна може подвоїти розмір); вежа — 3–9 клітин за формою.
- Камера показує всю арену; інформація повна (шлях видно наперед).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок (тетроміно) | static | форма, руна | непрохідна стіна лабіринту; кладеться з карти |
| Блок з руною | static | ефект руни | посилює сусідні вежі / особлива здатність / подвійний розмір |
| Вежа отрути | tower | форма | ллє отруту на голови монстрів уздовж шляху |
| Вежа-дрон | tower | — | дрони переслідують ворогів |
| Вежа D20 | tower | кубик d20 | шкода залежить від випадкового кидка |
| Інші вежі | tower | 1×3 / 2×2 / 3×3 | різні типи атаки (?) |
| Монстр | enemy | HP, швидкість | іде найкоротшим шляхом крізь лабіринт |
| Бос | boss | — | кінець етапу Adventure |
| Точка появи | spawner | — | звідси виходять хвилі |
| Ціль / «вогнище» (ember) | static | життя (?) | монстр дійшов → шкода (?) |
| Реліквія (power relic) | pickup | пасив | змінює правила на весь забіг |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «phase_start(build)»` → ТО `custom: «effect draw — рука карт-блоків і веж»` (?).
- КОЛИ `input(rotate)` → ТО `rotate(piece, 90)` (?).
- КОЛИ `input(place, block_card, cells)` → ЯКЩО `free(cells)` and `custom: «cond path_exists від кожної точки появи до цілі»` → ТО `custom: «клітини стають стіною»`, `custom: «effect recompute_path»`; інакше `block`.
- КОЛИ `input(place, tower_card, cells)` → ЯКЩО `free(cells_of_shape)` → ТО `spawn(tower)` (?: на блоки чи на вільні клітини — `+tower-on-wall`).
- КОЛИ `custom: «phase_start(battle)»` → ТО `wave_start`, `spawn_at(monsters, spawn_points)`; `tick` → `move(a, next_on_path)`.
- КОЛИ `in_range(tower, monster, r)` → ТО атака за типом: отрута — `damage` з часом по клітинах шляху; дрон — переслідування; D20 — `damage(roll(1..20) × k)`.
- КОЛИ `hp_zero(monster)` → ТО `disappear_a`, винагорода (?).
- КОЛИ `reach(monster, goal)` → ТО `custom: «втрата життя/HP цілі»` (?); `counter(lives, ==, 0)` → `lose` (кінець забігу).
- КОЛИ `wave_cleared` останньої хвилі → ТО `win` етапу, `window(choice-window)`: нові вежі/блоки/реліквії; руни на блок-карти; досвід → таланти.
- Перемога: пройти етапи й босів Adventure · Поразка: ціль зруйновано · Рахунок: Endless — таблиці лідерів.

## Керування і ввід
- Миша: перетягнути карту з руки на поле; фігура-«привид» показує клітини і чи легальна позиція; поворот фігури клавішею/коліщатком (?).
- Після кожного блоку видно новий шлях монстрів (`path-preview`).
- Кнопка старту бою; пауза/прискорення (?).

## Вікна, меню, HUD
- `main-menu`: Adventure · Endless · Enigma Sanctum · таланти · налаштування.
- `+window:character-select` — вибір персонажа і «полумʼя» (flame) перед забігом.
- `+window:map-window` — етапи забігу з розгалуженням (?).
- `game-screen`: сітка, рука карт (блоки/вежі), `+ui:ghost-piece`, `+ui:path-preview`, `+ui:range-circle`, `lives` / HP цілі, `wave-counter`.
- `+window:choice-window` — нагорода після бою (вежа / блок / реліквія); вікно рун — зачарувати карту-блок.
- `leaderboard` (Endless), `achievements-window`, `end-screen`.
- Переходи: main-menu → character-select → (бій → нагорода)×N → бос → end-screen.

## Фічі поза полем
- `mode-endless` — 80+ етапів і спецмапи з онлайн-таблицями (`leaderboard-online`).
- Enigma Sanctum — режим-челендж з обмеженим набором карт (`mode-puzzle`).
- `meta-progression` — досвід за бої відкриває таланти між забігами.
- `+feature:run-map`, `+run-relics`, `cloud-save`, `achievements`.

## Варіації й родичі
- Rampart (1990) — тетроміно як стіни, але замикати територію; Desktop Tower Defense / Fieldrunners — лабіринт із самих веж; Isle of Arrows — шлях із плиток; Tetris — фігури.
- **Осі варіацій**: стіна лабіринту — вежа / окремий блок / плитка-шлях · фігури — 1×1 / тетроміно / довільні поліоміно · запас стін — необмежений за гроші / рука карт · ворог — обходить / ламає стіни.

## Цікавинки для курсу
- Розміщення тетроміно з поворотом + перевірка, що шлях не перекрито (BFS) — 🥇.
- Обмежений запас блоків з колоди: рішення «довжина шляху vs місце для вежі» — 🥉.
- Вежі різних форм (1×3, 2×2, 3×3) на тій самій сітці — 📎 (`multi-cell-size`).
- Руни-модифікатори на картах-блоках — 🥉.
- Вежа D20: шкода від кидка кубика — 🌱.

## Мапа на каталог
- Є: `enemy-waves` · `enemy-reached-base` · `chase-bfs` ↔ шлях монстрів · `reachability-check` ↔ заборона перекриття (?) · `multi-cell-size` ↔ вежі 2×2/3×3 · `projectile-shot` + `hp-damage` · `temporary-modes` ↔ отрута · `round-currency` (?) · `dungeon-generation` ↔ мапи забігу · `leaderboard` · `save-progress` · `drag-drop-piece`.
- **Нема** → пропозиції карток:
  - `+polyomino-placement` — див. rampart.
  - `+maze-by-towers`, `+path-recompute`, `+tower-placement`, `+tower-range` — див. fieldrunners (тут лабіринт із блоків, не веж).
  - `+deck-draw`, `+card-sigils` (руни) — див. inscryption; `+run-relics` — див. isle-of-arrows.
  - `+limited-blocks` «Обмежений запас стін» · game-logic/economy · 📎 · слот {hand_size}.
  - `+tower-on-wall` «Вежа ставиться на стіну / окремо від шляху» · entities/legality · 🌱 (?).

## Пропозиції до словників
- `+trigger:path_changed`, `+cond:path_exists`, `+effect:recompute_path` — підтвердження.
- `+trigger:phase_start` — будування / бій.
- `+effect:rotate` ⏳, `+effect:draw` — підтвердження.
- `+role:tower`, `+role:card` — підтвердження.
- `+ui:ghost-piece` ⏳, `+ui:range-circle`, `+ui:path-preview` ⏳ — підтвердження.
- `+window:map-window`, `+window:choice-window`, `+window:character-select` ⏳ — підтвердження.
- `+feature:run-map`, `+feature:meta-progression` ⏳ (таланти).
- `+axis:session` — `match` (забіг) і `endless`.

## Джерела
- ⭐ [Steam: Emberward](https://store.steampowered.com/app/2459550/Emberward/) — «build twisting mazes with tetromino blocks», обмежені блоки, вежі 1×3/2×2/3×3 (отрута, дрон, D20), руни на блок-картах, персонаж і полумʼя, таланти, Adventure/Endless/Enigma Sanctum; Refic Games.
- [PC Gamer](https://www.pcgamer.com/games/strategy/drop-blocks-to-make-your-own-maze-in-the-demo-for-tower-defense-game-emberward) — про демо: блоки, з яких будуєш лабіринт (бачив лише заголовок).
- YouTube: пошук «emberward gameplay».

## Непевне
- (?) Що саме захищає гравець (вогнище/ember?) і скільки в нього життя.
- (?) Чи можна повертати фігури; чи вежі ставляться на блоки чи на вільні клітини; чи заборонено повністю перекрити шлях.
- (?) Чи можна будувати під час хвилі, чи лише у фазі підготовки; чи є золото в бою.
- (?) Структура забігу (мапа з розгалуженням?) і що дає «полумʼя».
- (?) Платформи: Steam-сторінка показує лише Windows; дата — EA 2024, повний реліз 17.09.2026.
- Джерел мало (Steam-опис, заголовок PC Gamer): WebSearch вичерпано, вікі (wiki.gg) недоступна (401).
