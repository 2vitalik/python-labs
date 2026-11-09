---
title: Tangledeep
slug: tangledeep
aka: []
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2018
platforms: [PC, macOS, Linux, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/628770/Tangledeep/", best: true, note: "перелік фіч: 12 джобів, 100+ навичок, 3 режими, Monster Corral з розведенням, банк і магічні дерева між персонажами, Item Dreams, daily/weekly, Workshop"}
  - {kind: other, url: "https://www.nintendo.com/us/store/products/tangledeep-switch/", note: "Switch-версія з Legend of Shara: 13 джобів, 15+ модифікаторів, реліквії, руни знань, ліміт рівня 15 → 20"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Tangledeep", note: "RogueBasin: джоби за Final Fantasy Tactics, пети з характером і стосунками, Heroic/Adventure, 7DRL 2016"}
  - {kind: steam, url: "https://store.steampowered.com/app/953080/Tangledeep_Legend_of_Shara/", note: "DLC Legend of Shara"}
  - {kind: steam, url: "https://store.steampowered.com/app/1156710/Tangledeep_Dawn_of_Dragons/", note: "DLC Dawn of Dragons"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "рядок у списку роглайків (статті нема)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tangledeep+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-8dir, cell-click, dungeon-generation, stairs-levels, hp-damage, unit-xp-skills, inventory, inventory-items, item-pickup, melee-vs-ranged, status-effects, shop-catalog, round-currency, permadeath, difficulty-levels, daily-puzzle, leaderboard, controls-remap, save-autosave, message-log, fog-of-war, run-relics, +job-system, +ability-loadout, +monster-capture, +pet-breeding, +item-dream, +shared-bank, +game-modifiers, +town-hub]
proposes: ["+feature:job-change", "+feature:monster-corral", "+feature:shared-bank", "+feature:game-modifiers", "+feature:mode-adventure", "+feature:mode-heroic", "+window:job-window", "+window:corral-window", "+window:modifier-select", "+effect:capture(a)", "+effect:breed(a, b)", "+effect:enter_dream(item)", "+trigger:dream_cleared", "+role:pet", "+ui:stamina-bar"]
author: opus
date: 2026-11-09
---

# Tangledeep — SNES-подібний роглайк: джоби, як у Final Fantasy Tactics, пети з корралю й сни всередині предметів

## Суть
Покроковий тактичний роглайк (Impact Gameworks, 2018; почався як 7DRL 2016) у стилі 16-бітних JRPG. Герой лізе вгору крізь лабіринт, що щоразу інший, до поверхні. Ядро — **система джобів** (12, з DLC 13): навички вчаться за очки джоба і змішуються між класами. Довкола — **Monster Corral** (зловити майже будь-якого монстра, ростити петом, схрещувати) і **Item Dreams** — міні-підземелля «всередині» предмета, прохід якого підсилює цей предмет.

## Поле і час
- Квадратна сітка, вид згори, піксель-арт; поверхи генеруються, напрям — **угору** до поверхні (сетинг: підземні села без памʼяті про світ нагорі).
- Хід = дія героя; тактика з наголосом на рух і використання навичок у бою (RogueBasin).
- Окремі шари світу: основний спуск-підйом поверхами; хаб-містечко; Item Dreams — тимчасові поверхи, привʼязані до предмета; з DLC — Riverstone Waterway (альтернативний старт), Wanderer's Journeys, Realm of the Gods (пост-гейм).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, стаміна, енергія (?), рівень (до 15, з DLC 20), джоб, навички | рух 8 напрямків, удар, навичка, предмет |
| Пет | ally | характеристики, вподобання/неприязні, сили, стосунки | бʼється поруч з героєм за AI |
| Монстр | enemy | рівень, HP, сили | переслідує; майже кожного можна зловити |
| Чемпіон-монстр (?) | enemy | дод. модифікатори | посилений ворог з лутом (?) |
| Бос | boss | фази (?) | на ключових поверхах |
| Сходи вгору / вниз | static | — | перехід між поверхами |
| Портал у місто / порт-камінь (?) | static | — | швидке повернення в хаб |
| Предмет-спорядження | pickup | рівень, властивості, сон | екіпірування; дає вхід у свій Item Dream |
| Реліквія (DLC) | pickup | легендарні сили, комбінуються | рідкісна річ |
| Руна знань (DLC) | pickup | навичка | навчає особливої здібності |
| Фляга/зілля, їжа | pickup | — | лікування, бафи |
| Гроші | pickup | купка | валюта крамниць |
| Корраль | zone | місткість (?) | місце в хабі, де живуть зловлені пети |
| Магічне дерево | object | посаджене гравцем | росте між сесіями; спільний прогрес між персонажами |
| Банк | static | — | гроші/речі, спільні для всіх персонажів |
| NPC міста (крамарі, майстер джобів, Mysterious Wanderer) | neutral | — | торгівля, зміна джоба, вхід у Wanderer's Journeys |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `damage(weapon)`.
- КОЛИ `input(ability, target)` → ЯКЩО `custom: «вистачає стаміни/енергії й навичка не на cooldown»` → ТО ефект навички (`damage`, `move`, `set_state`); інакше `block`.
- КОЛИ `turn_end(hero)` → ТО монстри й пети діють.
- КОЛИ `hp_zero(enemy)` → ТО `counter(xp, +n)`, `counter(jp, +n)`, `spawn(loot)`.

Джоби:
- КОЛИ `input(learn, ability)` → ЯКЩО `counter(jp, >=, cost)` → ТО `counter(jp, −cost)`, `custom: «навичка вивчена в поточному джобі»`.
- КОЛИ `input(change_job)` у хабі → ТО `custom: «новий джоб; вивчені навички інших джобів можна покласти в слоти»` (?).

Пети й корраль:
- КОЛИ `input(capture, monster)` → ЯКЩО `custom: «монстр ослаблений / виконано умову ловлі»` (?) → ТО `custom: «монстр стає петом у коррал»`.
- КОЛИ `input(breed, pet_a, pet_b)` → ТО `custom: «новий пет з рисами батьків»`.
- КОЛИ `input(take_pet, monster)` → ТО `custom: «пет іде з героєм у підземелля»`.

Item Dreams:
- КОЛИ `input(dream, item)` → ТО `custom: «вхід у тимчасовий випадковий міні-данж предмета»`.
- КОЛИ `custom: «сон пройдено»` → ТО `custom: «предмет отримує посилення»`; поразка в сні — `custom: «викидає з сну»` (?).

Смерть і режими:
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(adventure)` → ТО `custom: «повернення в місто без permadeath»`; ЯКЩО `mode(heroic)` → ТО `custom: «персонаж гине, частина прогресу лишається»`; ЯКЩО `mode(hardcore)` (?) → ТО `lose` без збережень.
- КОЛИ `custom: «персонаж загинув»` → ТО банк і магічні дерева лишаються для наступного персонажа.
- КОЛИ `reach(hero, surface)` → ТО `win` (?).
- Перемога: дістатися поверхні / перемогти фінального боса (?). Поразка: HP = 0 у режимі з permadeath. Рахунок: таблиці daily/weekly.

## Керування і ввід
- Три схеми: клавіатура (numpad — 8 напрямків), WASD-пресет, повна мишка (клік по клітині/цілі); геймпад з повним перепризначенням (Steam).
- Гарячі слоти навичок і витратних; вибір цілі для навичок з дальністю — курсором по клітинах.

## Вікна, меню, HUD
- `main-menu` → `save-slots` → створення персонажа: `character-select` (джоб), `mode-select` (Adventure / Heroic / …), `modifier-select` (15+ модифікаторів «легше / важче / дивніше»).
- `game-screen`: поле, `hp-bar`, `stamina-bar`, `energy-bar`, `skill-bar` з cooldown, `inventory-bar`, `minimap`, `message-log`, портрет пета.
- `inventory-window` + `equipment-slots`.
- `job-window` — вчити навички за JP, слоти вивчених навичок, зміна джоба (у майстра в місті).
- `corral-window` — пети: характеристики, вподобання, стосунки, розведення, взяти з собою.
- `shop-window` (крамарі хабу), банк (`custom-window`).
- `map-window` поверху (?).
- `leaderboard` — daily/weekly челенджі.
- `end-screen` — смерть / результат челенджу; `pause-menu`, `settings-window` (`options-controls`).

## Фічі поза полем
- `mode-select`: 3 режими; Adventure — без permadeath, Heroic — частина прогресу після смерті.
- `game-modifiers` (15+), `mode-daily` + тижневі челенджі з `leaderboard-online`.
- `shared-bank` і магічні дерева — «мета-прогрес» між персонажами (`meta-progression`).
- `mod-support`: Steam Workshop (монстри, предмети, спрайти, зони).
- `remap-controls`, `gamepad-support`, `mouse-and-keyboard`.
- DLC Legend of Shara (13-й джоб Calligrapher, героїня Shara, реліквії, руни, Riverstone Waterway) і Dawn of Dragons.

## Варіації й родичі
- Родичі в корпусі: [Mystery Dungeon](mystery-dungeon.md) (консольна «JRPG-шкура» роглайку, рекрутинг монстрів у PMD), [Dungeons of Dredmor](dungeons-of-dredmor.md) (клас як набір навичок), [Pixel Dungeon](pixel-dungeon.md), [Dungeon Crawl Stone Soup](dungeon-crawl-stone-soup.md).
- Далекі родичі: Final Fantasy Tactics (джоби), Disgaea (Item World — прообраз Item Dreams), Pokémon (ловля й розведення).
- Осі варіацій: **клас** (один / джоби з переносом навичок); **союзник** (нема / пет зі зловлених / загін); **посилення речі** (апгрейд-сувій / міні-данж усередині речі); **смерть** (permadeath / частковий прогрес / без смерті).

## Цікавинки для курсу
- Джоби з очками JP і перенесенням вивчених навичок у слоти іншого джоба — 🥉 (граф «джоб → навички» + loadout).
- Ловля монстра в корраль і схрещування з успадкуванням рис — 🥈 (генетика петів, стосунки).
- Item Dream: предмет як сід міні-підземелля, прохід якого змінює сам предмет — 🥉.
- Модифікатори забігу (15+ перемикачів правил) — 📎 кожен, 🥉 за систему (правила як дані).
- Банк і дерево, спільні між персонажами, — найпростіший мета-прогрес — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `cell-click` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `unit-xp-skills` · `inventory` + `inventory-items` · `item-pickup` · `melee-vs-ranged` · `status-effects` · `shop-catalog` · `round-currency` · `permadeath` · `difficulty-levels` (модифікатори/режими) · `daily-puzzle` (daily run) · `leaderboard` · `controls-remap` · `save-autosave` · `message-log` · `fog-of-war` · `run-relics` (реліквії DLC).
- **Нема** → пропозиції карток:
  - `+job-system` «Класи-джоби з окремими деревами й очками» · entities/state · 🥉 · слоти {jobs, jp_cost}.
  - `+ability-loadout` «Слоти навичок з різних джобів» · entities/state · 📎.
  - `+monster-capture` «Зловити ворога й зробити союзником» · entities/interact · 🥉.
  - `+pet-breeding` «Схрещування петів з успадкуванням рис» · entities/state · 🥈.
  - `+item-dream` «Міні-данж усередині предмета, що підсилює його» · levels/generation · 🥉.
  - `+shared-bank` «Сховище, спільне для всіх персонажів» · game-logic/save · 🌱.
  - `+game-modifiers` «Перемикачі правил забігу» · game-logic/difficulty · 🥉.
  - `+town-hub` «Місто-хаб між походами» · levels/progression · 📎.

## Пропозиції до словників
- `+feature:job-change` — зміна класу посеред гри з переносом навичок.
- `+feature:monster-corral` — колекція зловлених монстрів поза полем.
- `+feature:shared-bank` — сховище між персонажами.
- `+feature:game-modifiers` — набір перемикачів правил на старті забігу.
- `+feature:mode-adventure` / `+feature:mode-heroic` — смерть без втрати / з частковою втратою прогресу.
- `+window:job-window` — навички джоба, JP, слоти.
- `+window:corral-window` — пети, розведення.
- `+window:modifier-select` — вибір модифікаторів забігу.
- `+effect:capture(a)` — ворог стає петом гравця.
- `+effect:breed(a, b)` — нова сутність з рис двох.
- `+effect:enter_dream(item)` — перейти в рівень, згенерований з предмета.
- `+trigger:dream_cleared` — пройдено міні-данж предмета.
- `+role:pet` — союзник-монстр гравця (вужче за `ally`: зловлений, росте, розводиться).
- `+ui:stamina-bar` — окрема смуга стаміни для навичок.

## Джерела
- ⭐ [Steam: Tangledeep](https://store.steampowered.com/app/628770/Tangledeep/) — 12 джобів, 100+ навичок, 3 режими, корраль з розведенням, банк і дерева, Item Dreams, daily/weekly, керування, Workshop.
- [Nintendo eShop: Tangledeep](https://www.nintendo.com/us/store/products/tangledeep-switch/) — 13 джобів, 15+ модифікаторів, реліквії, руни, ліміт рівня, зони DLC.
- [RogueBasin: Tangledeep](https://www.roguebasin.com/index.php/Tangledeep) — FFT-джоби, пети з характером, Heroic/Adventure, історія 7DRL.
- [Steam: Legend of Shara](https://store.steampowered.com/app/953080/Tangledeep_Legend_of_Shara/) · [Steam: Dawn of Dragons](https://store.steampowered.com/app/1156710/Tangledeep_Dawn_of_Dragons/).
- YouTube: [пошук «tangledeep gameplay»](https://www.youtube.com/results?search_query=tangledeep+gameplay).

## Непевне
- (?) Статті у Wikipedia нема (404); фан-вікі (fandom 402, wiki.gg 401) не відкрились — механіки поза описами магазинів — з памʼяті.
- (?) Як саме ловиться монстр (умова слабкості, предмет), як працює зміна джоба й перенесення навичок, стаміна/енергія як два ресурси — з памʼяті.
- (?) Назва третього режиму (Hardcore?) і точні правила Heroic.
- (?) Кількість поверхів, боси, умова перемоги («поверхня»), «бойові пакунки пета» з черги — не підтверджено.
- (?) Чемпіон-монстри, портал у місто, мапа поверху — з памʼяті.
