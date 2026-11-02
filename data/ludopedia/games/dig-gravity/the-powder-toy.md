---
title: The Powder Toy
slug: the-powder-toy
family: dig-gravity
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2008
platforms: [Windows, macOS, Linux, Android, Steam]
links:
  - {kind: official, url: "https://powdertoy.co.uk/", best: true, note: "офіційний сайт: що симулюється, завантаження, браузер сейвів спільноти"}
  - {kind: official, url: "https://github.com/The-Powder-Toy/The-Powder-Toy", note: "код (GPL-3.0) і повний список клавіш у README"}
  - {kind: other, url: "https://raw.githubusercontent.com/The-Powder-Toy/The-Powder-Toy/master/src/simulation/elements/WATR.cpp", note: "елемент як запис властивостей: Weight, Falldown, HeatConduct, переходи за температурою, реакції"}
  - {kind: other, url: "https://raw.githubusercontent.com/The-Powder-Toy/The-Powder-Toy/master/src/simulation/elements/SPRK.cpp", note: "іскра: як струм біжить провідниками"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Powder_Toy", note: "історія, 258 елементів (2025), Lua, сервер сейвів, Steam 2024"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Falling-sand_game", note: "жанр falling-sand: Hell of Sand → Powder Game → TPT → Noita"}
  - {kind: fandom, url: "https://powdertoy.co.uk/Wiki/W/Main_Page.html", note: "офіційна вікі елементів (захищена anti-bot перевіркою)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=The+Powder+Toy", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Powder+Toy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, cell-transform, interaction-table, chain-detonation, game-pause, game-loop, state-as-data, in-game-editor, editor-palette, editor-draw-tools, editor-erase, editor-undo, level-exchange, level-rating, field-scaling, particles, theme-select, save-game, +falling-sand-cell, +density-displacement, +heat-diffusion, +phase-transition, +pressure-field, +electric-signal, +edge-mode, +newtonian-gravity, +stamps, +element-property-flags, +game-of-life-wall, +frame-step, +view-modes]
proposes: ["+trigger:tick", "+trigger:adjacent8", "+cond:temp", "+cond:pressure", "+cond:prob", "+cond:adjacent_count", "+effect:transform", "+effect:fall", "+effect:swap", "+effect:diffuse", "+effect:explode", "+role:material", "+role:field", "+ui:element-menu", "+ui:brush-cursor", "+window:save-browser", "+window:console", "+feature:mode-sandbox", "+feature:scripting", "+axis:goal-sandbox", "+axis:field-layers"]
author: opus
date: 2026-11-02
---

# The Powder Toy — пісочниця «падаючого піску»: кожен піксель — частинка з фізикою

## Суть
Гравець не має аватара й мети: мишею малює частинки сотень елементів (порошки, рідини, гази, тверді, вибухівка, електроніка, радіоактивні) і дивиться, як вони падають, течуть, горять, плавляться, проводять струм і вибухають. Кожна клітина-піксель живе за правилами свого елемента, а поверх частинок рахуються **поля** — тиск і швидкість повітря, температура, гравітація. Це крайня точка сімʼї dig-gravity: те, що в Boulder Dash було 15 елементами з падінням, тут — клітинна фізика з таблицею властивостей і переходами станів (вода → лід/пара, лава застигає в камінь).

## Поле і час
- Поле частинок 612×384 (одна частинка на піксель, до 235 008 частинок).
- **Два масштаби сітки**: частинки — по пікселю; повітря, тиск, стіни й гравітація — сітка 153×96 клітин по 4×4 пікселі.
- Шари: частинки (по одній на піксель, плюс енергетичні — фотони, нейтрони — окремо (?)), стіни (4×4), поля тиску/швидкості/гравітації, температура в кожній частинці, шар декорації (колір).
- Real-time: тік = кадр симуляції; пауза (Space) і крок по кадру (F).
- Межа поля: режими void / solid / loop (Ctrl+E) (?) щодо назв — тор як опція.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порошок (SAND, DUST, SALT…) | material | Falldown=1, Weight | падає, осипається по діагоналі, тоне в легшому |
| Рідина (WATR, LAVA, OIL…) | material | Falldown=2, Weight (WATR 30, LAVA 45) | падає й розтікається вбік; важча витісняє легшу |
| Газ (GAS, WTRV, CO2…) | material | Diffusion, HotAir | дифундує, рухається з повітрям |
| Тверде (METL, STNE, GLAS, WOOD…) | material | Hardness, Meltable | нерухоме; плавиться/ламається тиском |
| Вибухівка (GUN, C-4, NITR…) | material | Explosive, Flammable | від вогню/тиску → вибух: вогонь + стрибок тиску |
| Провідник (METL, PSCN, NSCN, INST, SWCH…) | material | PROP_CONDUCTS | передає іскру SPRK сусідам за правилами пар |
| Іскра SPRK | material | life=4, ctype = провідник | біжить провідником, за 4 кадри повертається в ctype; у воді 64 кадри |
| Ізолятор (INSL) | material | — | блокує провідність |
| Вогонь / плазма | material | life | гріє, підпалює Flammable, гасне водою |
| Радіоактивні (URAN, PLUT, NEUT, PHOT…) | material | — | частинки-енергія летять, ініціюють розпад/реакції |
| Game of Life (GOL і варіанти) | material | правило автомата | живуть за клітинним автоматом |
| Стіни (WALL, FAN, DETECTOR, LIQUID WALL, GAS WALL, GRAVITY WALL, STASIS WALL…) | field | блок 4×4 | фільтрують, що проходить; вентилятор дме; детектор шле іскру |
| Інструменти HEAT/COOL/AIR/VAC/WIND/PGRV/NGRV/PROP | field | сила | змінюють поля або властивість частинок під пензлем |
| Поле тиску / швидкості повітря | field | на клітину 4×4 | вибух піднімає тиск; повітря несе гази й порошки (Advection, AirDrag) |
| Поле гравітації | field | режим | вертикальна / вимкнена / радіальна (?); ньютонівська — маса притягує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `prop(a, powder)` and `free(below)` → ТО `fall(a)`; ЯКЩО зайнято → `custom: «спроба по діагоналі вниз»`.
- КОЛИ `tick` → ЯКЩО `prop(a, liquid)` → ТО `fall(a)`, інакше `custom: «розтікання вбік»`.
- КОЛИ `tick` → ЯКЩО `occupied(below, b)` and `custom: «Weight(a) > Weight(b)»` → ТО `swap(a, b)` — важче тоне.
- КОЛИ `tick` → ТО `diffuse(temp)` між сусідами з вагою HeatConduct; `custom: «повітря переносить частинки (Advection) і гальмує (AirDrag)»`.
- КОЛИ `tick` → ЯКЩО `cond:temp(a, <, LowTemperature)` → ТО `transform(LowTemperatureTransition)`: WATR < 273,15 K → ICEI.
- КОЛИ `tick` → ЯКЩО `temp(a, >, HighTemperature)` → ТО `transform(HighTemperatureTransition)`: WATR > 373 K → WTRV (пара).
- КОЛИ `tick` → ЯКЩО `temp(lava, <, точка застигання ctype)` → ТО `transform(ctype)` — лава памʼятає, з чого розплавилась (камінь, метал), і застигає назад; вода біля лави її охолоджує й сама кипить.
- КОЛИ `adjacent8(watr, salt)` → ТО `transform(watr → sltw)` (солона вода); `adjacent8(watr, sltw)` → вода теж стає солоною.
- КОЛИ `adjacent8(watr, rock)` → ЯКЩО `custom: «швидкість води ≥ 0,5»` and `prob(1/1000)` → ТО `transform(rock → sand|stone)` — ерозія.
- КОЛИ `adjacent8(fire, flammable)` → ЯКЩО `prob(Flammable)` → ТО `transform(fire)`, тепло вгору.
- КОЛИ `custom: «вибухівка підпалена або тиск ≥ поріг»` → ТО `explode`: вогонь + `custom: «стрибок тиску в полі повітря»` → `chain-detonation`.
- КОЛИ `cond:pressure(cell, >, HighPressure(a))` → ТО `transform(HighPressureTransition)` (напр., скло трощиться).
- КОЛИ `adjacent8(sprk, conductor)` (у вікні 5×5) → ЯКЩО `custom: «пара відправник→отримувач дозволена (PSCN не бере від NSCN, INSL блокує)»` and `state(conductor, life == 0)` → ТО `transform(conductor → sprk, life=4, ctype=conductor)`.
- КОЛИ `timer(life)` у SPRK = 0 → ТО `transform(ctype)` (повернення в провідник).
- КОЛИ `timer(…)` для GOL → ТО `custom: «правило автомата за кількістю сусідів (adjacent_count)»`.
- КОЛИ `input(draw)` → ТО `spawn_at(element, brush_area)`; правою кнопкою — `disappear` (стирання); інструмент — змінює поле/властивості.
- Перемоги, поразки, рахунку нема. «Ціль» — побудувати пристрій чи сцену й поділитись сейвом; голоси спільноти — єдина оцінка.

## Керування і ввід
- Миша: ліва — малювати обраним елементом, права — стирати (?) або другий елемент; колесо — розмір пензля; Ctrl/Shift+колесо — розмір по осях.
- Інструменти: Tab — форма пензля (коло, квадрат, трикутник); Shift+drag — лінія; Ctrl+drag — прямокутник; заливка (?) — Ctrl+Shift+клік; середня кнопка / Alt+клік — піпетка елемента.
- Симуляція: Space — пауза; F — крок на кадр; W — режим гравітації; Y — режим повітря; N — ньютонівська гравітація; U — ambient heat; Ctrl+E — режим краю; = — скинути тиск; I — інвертувати тиск.
- Штампи: S — зберегти штамп, L — останній штамп, K — бібліотека штампів; Ctrl+C/V/X; R / Shift+R — поворот і дзеркало при вставці; Ctrl+Z/Y — undo/redo.
- Вигляд: 0–9 — режими відображення (тиск, тепло, швидкість…); Z — лупа; G — сітка; H — HUD; E — пошук елемента; B — декорації; ` — консоль Lua.

## Вікна, меню, HUD
- `game-screen`: поле + `element-menu` праворуч (категорії Walls, Electronics, Powered Materials, Sensors, Force, Explosives, Gases, Liquids, Powders, Solids, Radioactive, Special, Game Of Life, Tools, Favorites, Decoration tools) + рядок елементів категорії внизу; HUD: FPS, кількість частинок, під курсором — елемент, температура, тиск, `brush-cursor`.
- `save-browser` (онлайн): пошук, сортування, голоси «за/проти», теги, відкрити сейв; вхід в акаунт.
- `custom-window` «Save to server» / локальне збереження з назвою й описом.
- `custom-window` бібліотека штампів (K) — мініатюри фрагментів.
- `settings-window`: ambient heat, гравітація, повітря, межі, масштаб вікна, fullscreen.
- `console` — Lua-консоль (`).
- `help-window` — вступний текст (Ctrl+H / F1).
- Переходи: game-screen ↔ save-browser (відкрити сейв замінює поле); game-screen ↔ stamp library (вставити фрагмент під курсор).

## Фічі поза полем
- `mode-sandbox` — уся гра: нема рівнів, мети, рахунку.
- `level-sharing` + `user-levels-browser` + `level-rating` — вбудований сервер сейвів з голосуванням і модерацією.
- Штампи — частини поля як файли для повторного використання (copy/paste/rotate/mirror).
- `undo`/`redo`, `pause`, `step-mode`, `speed-control` (?).
- `mod-support` / `scripting`: Lua API, менеджер скриптів.
- Налаштування фізики: режими гравітації/повітря/межі, ambient heat, ньютонівська гравітація — `custom-rules`.
- `theme-select`-подібне: режими відображення (тиск, тепло, вогонь, blob), декорації кольором.

## Варіації й родичі
- Предки: Hell of Sand / Falling Sand Game (2005, Java-аплет), Powder Game (2007, Dan-Ball: тиск рідин, керовані бійці).
- Нащадки й сусіди: Sandspiel, Sandboxels, Noita (falling sand + роглайк), Powder Game 2; Rocks'n'Diamonds — та сама ідея «елемент = запис властивостей» у грубому масштабі (клітина = обʼєкт).
- **Осі варіацій**: роздільність — «клітина = обʼєкт (BD) / клітина = піксель (TPT)»; поля — «лише гравітація / + температура / + тиск і повітря / + ньютонівська гравітація»; мета — «рівні з квотою / пісочниця»; поведінка — «код на елемент / таблиця властивостей + переходи».

## Цікавинки для курсу
- Мінімальний falling sand: пісок, вода, стіна; падіння + діагональ + розтікання з чергуванням напрямку скану — 🥉.
- Елемент як запис (Weight, Falldown, HeatConduct, LowTemperature→, HighTemperature→) і загальний двіжок, що читає таблицю — 🥈.
- Теплопровідність і фазові переходи (вода ↔ лід ↔ пара, лава ↔ камінь через ctype) — 🥈.
- Поле тиску на грубій сітці 4×4 поверх пікселів (два масштаби) — 🥇.
- Електрика: іскра з життям 4 і ctype, напівпровідники P/N — 🥇: логічні вентилі з клітинного автомата.
- Штампи (копіювати/вставити фрагмент поля з поворотом) — 📎.
- Онлайн-сервер сейвів з голосами — 🥇 (поза межами одного курсу; локальна версія — 🥉).

## Мапа на каталог
- Є: `gravity-fall` · `cell-transform` (фазові переходи, реакції) · `interaction-table` (таблиця реакцій/властивостей) · `chain-detonation` · `game-pause` · `game-loop` · `state-as-data` (сейв — серіалізоване поле) · `in-game-editor` (вся гра — редактор) + `editor-palette` + `editor-draw-tools` (пензель, лінія, прямокутник) + `editor-erase` + `editor-undo` · `level-exchange` + `level-rating` (сервер сейвів) · `field-scaling` (лупа) · `particles` · `theme-select` (режими відображення) · `save-game`.
- **Нема** → пропозиції карток:
  - `+falling-sand-cell` «Клітина-частинка: порошок/рідина/газ» · entities/move · 🥉 · слот {falldown: powder|liquid|gas}.
  - `+density-displacement` «Важче тоне в легшому» · entities/move · 📎 · слот {weight}.
  - `+heat-diffusion` «Температура і теплопровідність» · entities/state · 🥈.
  - `+phase-transition` «Перехід стану за порогом» · entities/state · 📎 · слоти {low, high, into}.
  - `+pressure-field` «Поле тиску/вітру на грубій сітці» · entities/move · 🥇.
  - `+electric-signal` «Сигнал провідниками з затримкою» · entities/interact · 🥈 — іскра з life і ctype.
  - `+edge-mode` «Поведінка на краю поля» · entities/legality · 🌱 · слот {void|solid|loop}.
  - `+newtonian-gravity` «Маса притягує» · entities/move · 🥇.
  - `+stamps` «Штампи — фрагменти поля» · levels/editor · 📎.
  - `+element-property-flags` (повтор з Rocks'n'Diamonds) · `+game-of-life-wall` (повтор) · `+frame-step` «Крок на один тік» · interface/input · 🌱 · `+view-modes` «Режими відображення полів» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:tick` ⏳ · `+trigger:adjacent8` ⏳ — реакції з сусідом у 8 напрямках.
- `+cond:temp(a, op, T)` · `+cond:pressure(cell, op, p)` — пороги полів; `+cond:prob` ⏳ (ерозія 1/1000); `+cond:adjacent_count` ⏳ (Game of Life).
- `+effect:transform` ✅ (фазові переходи) · `+effect:fall` ⏳ · `+effect:swap` ⏳ (тонучі частинки) · `+effect:diffuse(field)` — розтікання значення поля по сусідах · `+effect:explode` — повтор.
- `+role:material` — частинка-речовина без волі й без «предметності» (пісок, вода, газ); `+role:field` — неклітинна сутність-поле (тиск, гравітація, стіна 4×4).
- `+ui:element-menu` — категорії елементів + рядок елементів; `+ui:brush-cursor` — контур пензля з розміром.
- `+window:save-browser` — онлайн-каталог збережень з голосами; `+window:console` — консоль скриптів.
- `+feature:mode-sandbox` ⏳ · `+feature:scripting` — Lua-плагіни.
- `+axis:goal-sandbox` — `goal` без мети (поставлено `state` як найближче); `+axis:field-layers` — дві роздільності сітки (піксель + 4×4).

## Джерела
- ⭐ [powdertoy.co.uk](https://powdertoy.co.uk/) — що симулюється (тиск, швидкість повітря, тепло, гравітація), завантаження, сейви спільноти, Lua.
- [GitHub README](https://github.com/The-Powder-Toy/The-Powder-Toy) — усі клавіші: пензлі, лінія, прямокутник, штампи, режими гравітації/повітря/межі, крок кадру.
- [WATR.cpp](https://raw.githubusercontent.com/The-Powder-Toy/The-Powder-Toy/master/src/simulation/elements/WATR.cpp) — властивості води й реакції (сіль, ерозія каменю, гасіння вогню).
- [SPRK.cpp](https://raw.githubusercontent.com/The-Powder-Toy/The-Powder-Toy/master/src/simulation/elements/SPRK.cpp) — іскра: life 4, ctype, правила провідності P/N/INST/INSL.
- [Wikipedia: The Powder Toy](https://en.wikipedia.org/wiki/The_Powder_Toy) — автор Skylark, 258 елементів (2025), сервер сейвів, Steam 2024.
- [Wikipedia: Falling-sand game](https://en.wikipedia.org/wiki/Falling-sand_game) — жанр і предки.
- YouTube: пошук «The Powder Toy gameplay».

## Непевне
- (?) Точні назви режимів гравітації (vertical/off/radial) і меж (void/solid/loop) — у README лише «cycle»; з памʼяті.
- (?) Клавіша заливки (flood fill) і дія правої кнопки миші — README не згадує.
- (?) Рік: Wikipedia-інфобокс 2008, стаття про жанр — 2010; енергетичні частинки (фотони, нейтрони) живуть в окремому шарі — з памʼяті.
- (?) Офіційна вікі закрита anti-bot перевіркою — категорії й назви стін взято з коду (`SimulationData.cpp`).
