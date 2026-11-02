---
title: Isles of Sea and Sky
slug: isles-of-sea-and-sky
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2024
platforms: [PC (Windows), Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Isles_of_Sea_and_Sky", best: true, note: "геймплей: блоки в ями, істоти котяться, зірки/метали/сфери, здібності, 4 острови-стихії, undo і reset екрана"}
  - {kind: steam, url: "https://store.steampowered.com/app/1233070/Isles_of_Sea_and_Sky/"}
  - {kind: other, url: "https://gmtk.substack.com/p/an-excellent-block-pushing-puzzler?r=4st3d", note: "GMTK (Mark Brown): ключі й замкнені блоки, зоряні ворота, черепаха, ріки, гарячі плитки"}
  - {kind: other, url: "http://www.thegeeklygrind.com/all-posts/isles-of-sea-and-sky-review", note: "рецензія: рівень води, клонування блоків, бомби, здібності копати/плавати/ламати"}
  - {kind: other, url: "https://opencritic.com/game/16761/isles-of-sea-and-sky", note: "огляд рецензій"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Isles+of+Sea+and+Sky+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, push-object, inertia-slide, floor-types, key-and-door, collect-quota, item-pickup, inventory-items, chain-detonation, cell-transform, impassable-cells, environment-death, sequential-levels, save-autosave, keyboard-controls, +fill-hole, +undo-redo, +reset-zone, +open-world-puzzles, +ability-gating, +quota-gate, +fast-travel-points, +water-level-toggle, +persistent-unlock, +world-map]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:counter", "+cond:has", "+cond:free", "+effect:move", "+effect:slide", "+effect:set_cell", "+effect:transform", "+effect:clone", "+effect:unlock", "+effect:heat", "+role:terrain", "+role:gate", "+role:hazard", "+window:map-window", "+feature:reset-zone", "+feature:ability-gating", "+axis:session"]
author: opus
date: 2026-11-02
---

# Isles of Sea and Sky — метроїдванія з Sokoban-екранів: штовхай блоки в ями, збирай зірки, відкривай острови

## Суть
Герой прокидається на березі архіпелагу без памʼяті й має зібрати сили чотирьох охоронців островів (земля, вода, вогонь, повітря), щоб відчинити велику браму. Кожен екран — Sokoban-пазл: штовхати можна лише вперед (не тягнути, не піднімати), а блоки здебільшого йдуть не на цілі, а **в ями** — щоб засипати їх і прокласти шлях до ключа, зірки чи виходу. Незвичне — **відкритий світ із гейтингом**: пазл можна побачити раніше, ніж маєш здібність чи предмет для нього, а зірки відчиняють зоряні ворота до нових частин світу. Без тексту й туторіалів — правила відкриваються спробою.

## Поле і час
- Світ — архіпелаг з дискретних екранів квадратної сітки; вихід за край екрана → сусідній екран; на більшості екранів кілька пазлів.
- Шари клітини: тип (суша, яма, вода, глибока вода, лід, гаряча плитка, ріка-течія) + обʼєкт (блок, валун, істота, ключ, зірка, замкнений блок).
- Покроково: тік = крок героя; течії, котіння й ковзання — наслідки одного ходу.
- Стан світу постійний: розвʼязані пазли, підібрані предмети й деякі прибрані перешкоди лишаються назавжди, навіть після reset екрана.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | здібності, ключі | рух 4 напрямки; штовхає, підбирає ходом у предмет; без окремої кнопки дії |
| Блок | object | — | штовхається на 1, якщо за ним вільно; у яму — засипає її |
| Яма | terrain | — | непрохідна; блок у ній → підлога (?) |
| Істота-«котик» (rolling creature) | object | — | від поштовху котиться до упору |
| Валун | static | — | непрохідний; після збору достатньої кількості сфер оживає пушабельним големом |
| Голем | object | — | штовхається як блок (?) |
| Ключ | pickup | — | відмикає замкнений блок |
| Замкнений блок | gate | — | зникає, якщо в героя є ключ |
| Зірка | pickup | — | головна валюта прогресу; рахується глобально |
| Зоряні ворота | gate | потрібно N зірок | відчиняються, коли зірок ≥ N |
| Особливий камінь (×6 на острів) | pickup | — | збирає охоронець острова (?) |
| Метал, сфера | pickup | — | відкривають окремі пазли/обʼєкти острова |
| Плавці (diving fins) | pickup | здібність | прохід підводними шляхами |
| Здібності (копати, плавати, ламати блоки) | pickup | — | відкривають раніше нерозвʼязні пазли (метроїдванія) |
| Вода | terrain | рівень | непрохідна без здібності; на водному острові рівень піднімається/опускається |
| Ріка (rapids) | terrain | напрям | несе блоки за течією |
| Водний елементаль | object | — | клонує інші типи блоків (?) |
| Лід | terrain | — | блок/герой ковзає до упору |
| Гаряча плитка | hazard | — | ранить героя; блоки від перегріву вибухають |
| Бомба-блок | object | — | вибухає ланцюгом з сусідніми бомбами |
| Вогняний елементаль | enemy | — | плюється вогнем по лінії |
| Перемикач | switch | — | натискається, коли на ньому стоїть герой/блок |
| Тунелі (гірський острів) | terrain | — | підземна мережа проходів між точками |
| Черепаха | static | — | перевозить героя між островами; відкриває карту світу |
| Велика брама | gate | сили 4 охоронців | фінальна зона з найважчими пазлами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; блок попереду і `free(cell_behind)` → `push`; інакше `block`. Тягнути не можна.
- КОЛИ `enter(block, hole)` → ТО `disappear_a`, `set_cell(floor)` — яма засипана.
- КОЛИ `contact(hero, roller)` → ТО `slide(roller, dir)` до упору.
- КОЛИ `enter(any, ice)` → ТО `slide(a, dir)`.
- КОЛИ `enter(block, rapids)` → ТО `move(block, flow_dir)` за течією (?).
- КОЛИ `contact(hero, key)` → ТО `pickup`; КОЛИ `contact(hero, locked_block)` → ЯКЩО `has(hero, key)` → ТО `disappear_b`, `take(key)`.
- КОЛИ `contact(hero, star)` → ТО `pickup`, `counter(stars, +1)`; КОЛИ `contact(hero, star_gate)` → ЯКЩО `counter(stars, ≥, N)` → ТО `unlock(gate)`.
- КОЛИ `counter(orbs, ≥, N)` → ТО `transform(boulder → golem)`.
- КОЛИ `contact(hero, ability_item)` → ТО `give(hero, ability)`: копати / плавати (плавці) / ламати блоки.
- КОЛИ `enter(hero, deep_water)` → ЯКЩО `not has(hero, fins)` → ТО `block`.
- КОЛИ `enter(hero, hot_tile)` → ТО `custom: «шкода герою»` (?); КОЛИ блок перегрівся → ТО `explode`, сусідні бомби — `chain-detonation`.
- КОЛИ `input(water_switch)` (водний острів) → ТО `custom: «рівень води піднімається/опускається — частина клітин стає прохідною або затопленою»` (?).
- КОЛИ `input(undo)` → ТО відкат ходу; КОЛИ `input(reset)` → ТО `reset_zone(screen)`, крім постійних змін світу.
- Перемога: зібрати сили 4 охоронців → брама → фінал; прогрес — зірки. Поразки як такої нема (глухий кут — reset).

## Керування і ввід
- Лише напрямки (d-pad/стрілки) — рух і всі взаємодії (штовхнути, підібрати, натиснути); undo і reset — окремі кнопки.
- Жодних текстових підказок: правила подано через поведінку обʼєктів.
- Доступність: заявлено керування для різних фізичних можливостей (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Продовжити, Нова гра, Налаштування.
- `game-screen`: екран-кімната; HUD мінімальний — зібрані зірки/предмети (`coins`-подібний лічильник) (?).
- `map-window` — карта архіпелагу (відкривається після черепахи): вибір острова, огляд секретів.
- `inventory-window` — зібрані предмети/здібності/камені (?).
- `pause-menu`: продовжити, налаштування (`settings-window`), вихід.
- Переходи: main-menu → game-screen; екран ↔ сусідній екран через край; черепаха → map-window → інший острів.

## Фічі поза полем
- `undo` ∞ (рецензенти: «infinite undos and instant room restarts»), `restart-level` = reset екрана.
- `world-map` + `fast-travel` черепахою; `open-world` порядок пазлів; `collectibles` (зірки, приховані предмети, секрети островів через уважне читання карти).
- `ability-gating` — здібності відкривають старі пазли (метроїдванія).
- `autosave` постійного стану світу.
- «Mysterious Update» (2025): нові пазли, метапазли, новий острів.

## Варіації й родичі
- Початок як клон Chip's Challenge; родичі — A Monster's Expedition (відкритий світ острівців-пазлів), Sokoban, Zelda Oracle-серії (візуальний стиль), Baba Is You/The Witness (навчання без тексту), Void Stranger (ями й плитки).
- Осі варіацій: **куди йде блок** — на ціль / у яму (засипати) / у воду (міст) / за течією; **як світ гейтить пазли** — лінійно / зірками-квотою / здібностями / ключами.

## Цікавинки для курсу
- Блок у яму → підлога: «блоки як будматеріал», а не ціль — 📎.
- Зоряні ворота з квотою + глобальний лічильник зірок — 🌱.
- Відкритий світ екранів із постійним станом і reset лише поточного екрана — 🥈.
- Здібності, що відкривають раніше нездоланні клітини (гейтинг) — 🥉.
- Перегрів блоків і ланцюгові бомби — 🥉.
- Рівень води як глобальний перемикач прохідності — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `push-object` · `inertia-slide` (лід, котики) · `floor-types` (лід, вода, гарячі плитки, ріки) · `key-and-door` · `collect-quota` (зірки) · `item-pickup` · `inventory-items` (здібності) · `chain-detonation` · `cell-transform` (валун → голем, яма → підлога) · `impassable-cells` · `environment-death` (?) · `sequential-levels` (заміщено відкритим світом) · `save-autosave` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+fill-hole` «Обʼєкт засипає яму» · entities/interact · 📎 (також A Monster's Expedition).
  - `+undo-redo` (є з Sokoban) · `+reset-zone` (є з A Monster's Expedition) · `+open-world-puzzles` (є з A Monster's Expedition) · `+fast-travel-points` (черепаха).
  - `+ability-gating` «Здібність відкриває старі перешкоди» · levels/progression · 🥉.
  - `+quota-gate` «Ворота за квотою зібраного» · entities/interact · 🌱 (дитина `collect-quota`).
  - `+water-level-toggle` «Глобальний рівень води» · entities/interact · 🥉.
  - `+persistent-unlock` «Зміни світу, що переживають reset» · levels/progression · 🥉.

## Пропозиції до словників
- `+effect:clone` (⏳ є) — водний елементаль копіює блок; `+effect:unlock` (⏳ є) — зоряні ворота; `+effect:heat` — накопичення тепла обʼєктом до вибуху.
- `+feature:reset-zone` (з A Monster's Expedition) — reset екрана, а не світу; `+feature:ability-gating` — прогресія здібностями.
- `+axis:session` = `open-world` — нема рівнів, лише безперервний світ екранів.
- ⏳-слова, вжиті тут: `input`, `enter`, `counter`, `has`, `free`, `move`, `slide`, `set_cell`, `transform`, `terrain`, `gate`, `hazard`, `map-window`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Isles_of_Sea_and_Sky) — механіки, острови-стихії, прогрес зірками/металами/сферами, плавці, валуни-големи, історія (колишня назва Akurra, старт як клон Chip's Challenge).
- [GMTK: «an excellent block pushing puzzler»](https://gmtk.substack.com/p/an-excellent-block-pushing-puzzler?r=4st3d) — ключі й замкнені блоки, зоряні ворота, черепаха, ріки, гарячі плитки, тунелі, undo/restart.
- [The Geekly Grind review](http://www.thegeeklygrind.com/all-posts/isles-of-sea-and-sky-review) — рівень води, клонування, бомби, здібності копати/плавати/ламати, постійні зміни після reset.
- [Steam](https://store.steampowered.com/app/1233070/Isles_of_Sea_and_Sky/) — опис, Cicada Games, 22.05.2024 · [OpenCritic](https://opencritic.com/game/16761/isles-of-sea-and-sky).

## Непевне
- (?) Що саме стає з ямою після блока (підлога чи «блок у ямі»), і чи потрапляють у яму котики/герой.
- (?) «Spirit forms» з брифа куратора в джерелах не знайдено: є «сили охоронців» і здібності-предмети; механіку перевтілень не описано.
- (?) Механіка водного рівня, клонування водними елементалями, перегріву блоків — лише з однієї рецензії, без деталей.
- (?) Чи може герой загинути (гарячі плитки «ранять») і що тоді — reset екрана?
- (?) Склад HUD, наявність inventory-window.
- (?) Кольорові ворота/ключі різних кольорів — у джерелах лише «ключі й замкнені блоки».
