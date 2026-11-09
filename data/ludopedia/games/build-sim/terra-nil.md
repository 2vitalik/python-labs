---
title: Terra Nil
slug: terra-nil
aka: [Терра Ніл]
family: build-sim
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: state
year: 2023
platforms: [PC, macOS, Linux, mobile, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Terra_Nil", best: true, note: "суть «зворотного ситібілдера», три фази, турбіни лише на камені, скрубери, помпи, тварини, дати"}
  - {kind: steam, url: "https://store.steampowered.com/app/1593030", note: "опис: біоми, процедурні мапи, переробка, Appreciate mode, DLC Heatwave / Vita Nova"}
  - {kind: other, url: "https://www.gamepressure.com/newsroom/terra-nil-beginners-guide-tips-and-tricks/z25355", note: "гайд: розставлення скруберів, поворот іригатора, моно-рейка й дрон, скидання останньої фази"}
  - {kind: other, url: "https://itemlevel.net/terra-nil-complete-beginners-guide/", note: "гайд: число над привидом будівлі = відновлено − ціна, дощ від температури+вологості, вимоги тварин"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=terra+nil+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cursor-place, hover-highlight, coverage-area, tile-rotate, round-currency, impassable-cells, cell-transform, objective-text, goal-counter, game-pause, save-game, save-autosave, level-unlock, world-map, map-window, achievements-window, field-scaling, +placement-requirement, +power-radius, +net-gain-preview, +phase-objectives, +fire-spread, +habitat-requirements, +cleanup-phase, +phase-reset, +weather-unlock, +area-pattern-transform, +procedural-map]
proposes: ["+effect:spread", "+cond:powered", "+cond:cell_count_in_range", "+ui:net-gain-preview", "+ui:phase-checklist", "+window:photo-mode", "+feature:phase-reset", "+feature:appreciate-mode", "+card:placement-requirement", "+card:net-gain-preview", "+card:cleanup-phase"]
author: opus
date: 2026-11-09
---

# Terra Nil — «зворотний ситібілдер»: перетворити тайли пустки на біоми машинами з радіусами, а потім розібрати всі машини й полетіти

## Суть
Гравець отримує мертву мапу (пустка, сухі русла, забруднений океан) і ставить еко-машини: турбіна на камені дає енергію в радіусі, скрубер у цьому радіусі перетворює пустку на ґрунт, іригатор — ґрунт на зелень. Кожна відновлена клітина дає ресурс на наступні будівлі, тож гра — **економна розстановка покриттів**. Далі апгрейди створюють біоми (болота, луки квітів, ліси), клімат (температура, вологість) вмикає дощ, приходять тварини. Фінал — **прибирання**: переробити всі будівлі й піти, не лишивши сліду.

## Поле і час
- Квадратна сітка тайлів з рельєфом (височини, низини, русла, океан); мапи кампанії й процедурні.
- Будівлі займають 1 (кальцифікатор) або кілька клітин (скрубер 2×2); у кожної — зона дії навколо (радіус або фігура в іригатора).
- Ефект будівлі здебільшого миттєвий у момент встановлення; у часі розгортаються вогонь, дощ, прихід тварин (real-time без тиску часу).
- Регіон проходить фази: відновлення → біоми/клімат → тварини → переробка; поточна фаза має свій список цілей.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пустка (wasteland) | terrain | — | стає ґрунтом під дією скрубера |
| Ґрунт (soil) | terrain | — | стає зеленню під дією іригатора |
| Зелень (greenery) | terrain | — | джерело ресурсу; основа біомів |
| Камінь (rock) | terrain | — | єдине місце для турбіни (і вузлів моно-рейки) |
| Русло / річка | terrain | сухе / з водою | сухе русло наповнює помпа; річку можна прокопати |
| Забруднений океан | terrain | — | у радіусі скрубера стає чистим океаном |
| Болото, луки, ліс, пляж… | zone | біом | наслідок апгрейдів; кожен біом — вимога для тварин |
| Вітрова турбіна | source | лише на камені | живить енергією будівлі в радіусі |
| Скрубер токсинів | object | 2×2, на пустці, у радіусі енергії | при встановленні: пустка → ґрунт, забруднений океан → океан у радіусі |
| Іригатор | object | 6 конфігурацій (поворот R) | ґрунт → зелень у зоні фігури |
| Помпа | object | — | наповнює сухе русло водою |
| Екскаватор | object | — | створює нове русло/річку |
| Кальцифікатор | object | 1 клітина, на воді | створює кам'яні тайли (місце для турбін) |
| Сонячний підсилювач | hazard | — | підпалює; вогонь поширюється по зелені |
| Хмаротвір (Cloud Seeder) | object | — | підвищує вологість; болота рахує як воду |
| Обсерваторія тварин | object | радар | повертає вид, якщо його вимоги до біомів виконано |
| Тварина (олень, бобер, ведмідь, птахи, риби…) | neutral | вимоги: N тайлів біому поруч | приходить і лишається, поки середовище підходить |
| Вузол моно-рейки | conduit | на камені / висоті | дорога для дрона; переносить частину будівель |
| Силос переробки | sink | — | пакує будівлі поруч у ресурс |
| Дрон переробки | object | — | рухається річками / моно-рейкою, розбирає силоси |
| Дирижабль | object | — | фінальна будівля: на ньому покидають регіон |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, turbine)` → ЯКЩО `cell(target, rock)` → ТО `place(player, turbine)`; інакше `block`.
- КОЛИ `input(place, scrubber)` → ЯКЩО `cell(target, wasteland)` and `custom: «у радіусі турбіни/геотермальної станції»` → ТО `place(player, scrubber)` (пропозиція `+cond:powered`).
- КОЛИ `spawned(scrubber)` → ТО `set_cell(in_range, soil)` для пустки і `set_cell(in_range, ocean)` для забрудненого океану.
- КОЛИ `spawned(irrigator)` → ТО `set_cell(shape, greenery)` для ґрунту в зоні; КОЛИ `input(rotate)` до встановлення → ТО `rotate(irrigator, 60)` (?) — 6 конфігурацій.
- КОЛИ `input(place, calcifier)` → ЯКЩО `cell(target, water)` → ТО `place(player, calcifier)` і `set_cell(around, rock)`.
- КОЛИ `spawned(pump)` → ТО `set_cell(riverbed, river)`; `spawned(excavator)` → ТО `custom: «прокопати нове русло»`.
- КОЛИ `custom: «клітину відновлено»` → ТО `currency(+1)` (ресурс на будівлі).
- КОЛИ `input(hover, building_ghost)` → ТО `custom: «показати число: відновлені клітини − ціна; червоне, якщо мінус»` (пропозиція `+ui:net-gain-preview`).
- КОЛИ `spawned(solar_amplifier)` → ТО `custom: «підпал»`; КОЛИ `tick` → ЯКЩО `adjacent_count(cell, fire, >=, 1)` and `cell(x, greenery)` → ТО `custom: «вогонь поширюється»` (пропозиція `+effect:spread`); зупиняють вода й височини.
- КОЛИ `tick` → ЯКЩО `custom: «температура і вологість у потрібних межах»` → ТО `custom: «вмикається дощ»`; КОЛИ `rng(p)` під дощем → ТО `set_cell(random_unrestored, greenery)`.
- КОЛИ `input(place, cloud_seeder)` → ТО `counter(humidity, +n)`; ЯКЩО `adjacent_count(cell, marsh, >=, 1)` → ТО болота рахуються як вода.
- КОЛИ `spawned(observatory)` → ЯКЩО `custom: «вимоги виду виконано (напр. бобер: ~20 тайлів річки і ~10 лісу поруч)»` → ТО `spawn_at(animal, habitat)`.
- КОЛИ `counter(phase_goals, =, all)` → ТО `custom: «відкривається наступна фаза»`; КОЛИ `phase_start(next)` → ТО `custom: «нові будівлі й цілі»`.
- КОЛИ `custom: «виконано необовʼязкову ціль регіону»` → ТО `custom: «погода регіону очищує всі тайли»`.
- КОЛИ `spawned(recycling_silo)` → ТО `custom: «будівлі поруч переробляються в ресурс»`; КОЛИ `contact(drone, silo)` → ТО `disappear(silo)`; дрон ходить лише річками / моно-рейкою.
- КОЛИ `all_gone(building)` and `input(finish)` → ТО `win` (покинути регіон на дирижаблі).
- КОЛИ `input(reset_phase)` → ТО `custom: «повернути регіон на початок поточної фази»`.
- Поразка: нема; «глухий кут» — коли ресурсу не вистачає на потрібні будівлі (тоді лише скидання фази).

## Керування і ввід
- Миша/тач: вибрати будівлю з панелі → привид із підсвіченою зоною дії й числом чистого прибутку → клік ставить.
- R — поворот іригатора (більшість будівель не повертається); Shift — ставити кілька копій без повторного вибору.
- Скидання останньої фази, якщо помилку не виправити.
- Камера: панорама, зум, поворот (?).

## Вікна, меню, HUD
- `main-menu` → `world-map` / `map-window` регіонів (у Vita Nova — 3D-глобус, який можна обертати) → `game-screen`.
- `game-screen`: поле; панель будівель з цінами; HUD — ресурс (листя (?)), `objective-text` / список цілей фази (`goal-counter`), температура й вологість, вкладка «Optional Goals».
- `custom-window` довідник/«handbook» тварин і фото (Heatwave: фоторежим з зірками за знімки).
- Appreciate mode — `custom-window`/режим огляду відновленої мапи після фіналу.
- `settings-window`, `pause-menu`, `achievements-window` (Steam).

## Фічі поза полем
- Кампанія регіонів з розблокуванням (`level-unlock`) + процедурні мапи (річки, гори, низини, океани).
- DLC/оновлення Heatwave (посушливі біоми, 10 будівель, 13 тварин, 3 мапи) і Vita Nova (нові мапи, перероблені тварини, 3D-мапа світу).
- `autosave`, `cloud-save` (Steam Cloud); `achievements`.
- Скидання фази як «undo великого кроку» (`+phase-reset`).
- Фоторежим і Appreciate mode — подача без механіки.

## Варіації й родичі
- **Осі варіацій:** перетворення клітин ланцюгом типів (пустка → ґрунт → зелень → біом) · умова місця (лише на камені / лише на воді / лише в радіусі енергії) · фігура зони (коло / шестикутні конфігурації іригатора) · завершення — прибирання за собою як окрема фаза.
- Родичі в корпусі: [dorfromantik](dorfromantik.md) (спокійне розкладання тайлів-біомів), [stardew-farm](stardew-farm.md) (спринклери-зони), [townscaper](townscaper.md) (іграшка без поразки), [mini-motorways](mini-motorways.md) (бюджет на розстановку), [acnh-flowers](acnh-flowers.md) (природа на сітці), [timberborn](timberborn.md) (вода і зрошення).
- Сусіди поза корпусом: Eco, SimEarth, Islanders (бали за розстановку).

## Цікавинки для курсу
- Ланцюг перетворень клітин зоною будівлі (A → B → C) з умовою «джерело енергії в радіусі» — 🥉.
- Превʼю чистого прибутку над привидом будівлі (скільки клітин зміниться − ціна) — 📎 (симуляція «що якщо» без застосування).
- Умова місця за типом клітини (турбіна — лише камінь, кальцифікатор — лише вода, створює камінь) — 🌱.
- Поширення вогню з бар'єрами (вода, висота) — 📎 (CA або BFS по типу клітини).
- Вимоги тварин як «N тайлів біому в радіусі» — 📎 (підрахунок у вікні).
- Фаза прибирання: дрон досяжний лише по графу річок/рейки — 🥉 (досяжність на графі).
- Скидання фази (знімок стану на початку фази) — 📎.

## Мапа на каталог
- Є: `cursor-place` · `hover-highlight` · `coverage-area` (зони машин) · `tile-rotate` (іригатор) · `cell-transform` · `round-currency` (ресурс з відновлення) · `objective-text` + `goal-counter` · `level-unlock` + `world-map` · `save-autosave` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+placement-requirement` «Будівля ставиться лише на клітину типу X / у зоні Y» · entities/legality · 🌱 · слоти {cell_type, zone}.
  - `+net-gain-preview` «Превʼю прибутку від розстановки до кліку» · interface/hud · 📎.
  - `+cleanup-phase` «Фінальна фаза: розібрати все збудоване» · game-logic/win · 📎.
  - Перевикористано: `+power-radius`, `+phase-objectives`, `+fire-spread`, `+habitat-requirements`, `+phase-reset`, `+weather-unlock`, `+area-pattern-transform`, `+procedural-map`.

## Пропозиції до словників
- `+effect:spread` — поширення на сусідні клітини (вогонь, зелень під дощем).
- `+cond:powered` — будівля в радіусі джерела енергії.
- `+cond:cell_count_in_range` — у радіусі ≥ N клітин типу (вимоги тварин); зараз пишеться `custom`.
- `+ui:net-gain-preview` — число над привидом будівлі.
- `+ui:phase-checklist` — список цілей поточної фази.
- `+window:photo-mode` — фоторежим з оцінкою знімків.
- `+feature:phase-reset` — повернутися на початок фази.
- `+feature:appreciate-mode` — огляд завершеної мапи без цілей.
- `+card:placement-requirement`, `+card:net-gain-preview`, `+card:cleanup-phase` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Terra Nil](https://en.wikipedia.org/wiki/Terra_Nil) — фази, турбіни лише на камені, скрубери, помпи, нові річки й камінь, тварини, Free Lives / Devolver, Ludum Dare 45, дати релізів.
- [Steam](https://store.steampowered.com/app/1593030) — біоми, процедурні мапи, переробка, DLC, фоторежим, Appreciate mode.
- [Gamepressure: beginner's guide](https://www.gamepressure.com/newsroom/terra-nil-beginners-guide-tips-and-tricks/z25355) — скрубери без перекриття, поворот іригатора, моно-рейка, необовʼязкові цілі, скидання фази.
- [itemlevel: beginner's guide](https://itemlevel.net/terra-nil-complete-beginners-guide/) — число прибутку, Shift, дощ, Cloud Seeder, обсерваторія, вимоги тварин, силоси.
- Сніпети пошуку з wiki.terranil.org (скрубер 2×2 на пустці в радіусі турбіни; іригатор — 6 конфігурацій; кальцифікатор на воді) — сама вікі не відкрилась (DNS), terranil.wiki.gg — 401.

## Непевне
- (?) Назва ресурсу («листя»/leaves) — у відкритих джерелах не названо.
- (?) Кут повороту іригатора (60°) — виведено з «6 конфігурацій»; можливо, це різні фігури.
- (?) Розміри радіусів турбіни/скрубера/іригатора — у сніпетах «80+» і «200+ тайлів» зони, без радіуса в клітинах.
- (?) Точний список і порядок фаз у пізніх регіонах (клімат, тварини) — гайди описують перший регіон.
- (?) Поворот камери; поразки нема — висновок з опису, не з правил.
