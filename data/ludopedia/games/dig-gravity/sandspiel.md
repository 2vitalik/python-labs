---
title: Sandspiel
slug: sandspiel
aka: [sandspiel.club]
family: dig-gravity
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: none
year: 2019
platforms: [web, mobile]
links:
  - {kind: other, url: "https://maxbittker.com/making-sandspiel", best: true, note: "розбір автора: клітина 32 біти, один update на частинку, вітер на GPU, PNG-сейви, галерея"}
  - {kind: play, url: "https://sandspiel.club", note: "грати в браузері"}
  - {kind: official, url: "https://github.com/MaxBittker/sandspiel", note: "код: Rust/WASM + WebGL"}
  - {kind: other, url: "https://raw.githubusercontent.com/MaxBittker/sandspiel/master/crate/src/species.rs", note: "усі 19 елементів і їхні update-функції"}
  - {kind: itch, url: "https://maxbittker.itch.io/sandspiel", note: "сторінка на itch.io (з черги, не відкривав)"}
  - {kind: wiki, url: "https://sandboxels.wiki.gg/wiki/Falling-sand_game", note: "місце в жанрі: «Wind simulation; WebGL; custom element maker»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sandspiel+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, cell-transform, spawner-entity, game-loop, state-as-data, logic-render-split, in-game-editor, editor-palette, editor-erase, level-exchange, level-rating, cell-click, +falling-sand-cell, +density-displacement, +pressure-field, +cell-registers, +update-clock-bit, +relative-neighbor-api, +image-as-save, +cloner-element, +burn-countdown]
proposes: ["+cond:pressure", "+effect:set_wind", "+role:material", "+role:field", "+window:save-browser", "+card:cell-registers", "+card:update-clock-bit", "+card:image-as-save"]
author: opus
date: 2026-11-09
---

# Sandspiel — falling sand у браузері: кожна клітина — 4 байти, кожен елемент — одна функція update, а поверх — вітер

## Суть
Пісочниця жанру falling sand: гравець пальцем або мишею малює елементи (пісок, вода, вогонь, дерево, кислота, кліщі…) і дивиться, як вони падають, течуть, горять і реагують. Ядро — **одна функція update на вид частинки**, що раз за кадр дивиться на сусідів відносними зсувами `get(dx, dy)` / `set(dx, dy, cell)`. Незвичне: поверх сітки частинок іде **симуляція вітру** (рідина Нав'є—Стокса на GPU), і частинки її читають (тиск) та пишуть (вогонь здіймає потік). Мети нема; творіння зберігаються як PNG і викладаються в загальну галерею з голосами.

## Поле і час
- Квадратна сітка 300×300 = 90 000 клітин (була 250×250); позиція клітини не зберігається — це індекс у щільному 2D-масиві.
- Клітина — 32 біти: `species` (u8), `ra` (u8, випадкове при створенні — яскравість «зерна» і стан елемента), `rb` (u8, 0 — стан елемента), `clock` (u8 — щоб частинку не оновили двічі за тік).
- Скан зліва направо, згори вниз; без `clock` частинка, що падає, пролетіла б кілька клітин за кадр.
- Два шари: частинки (Rust/WASM) і поле вітру/тиску (WebGL, float-сітки: тиск, адвекція, дифузія); дані ходять між ними щокадру.
- Real-time 60 fps (ціль); на слабких пристроях повільніше.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Empty | terrain | — | порожнеча |
| Wall | static | — | без update |
| Sand | object | — | падає вниз, інакше по діагоналі (dx ∈ {-1,0,1} випадково); тоне у Water, Gas, Oil, Acid |
| Water | object | — | падає в Empty/Oil, розтікається діагоналлю й убік, «подвійний крок»; іноді вирівнює напрям із сусідньою водою |
| Gas | object | ra = обʼєм | блукає випадково; великі клітини діляться, малі зливаються |
| Oil | object | — | тече; від Fire/Lava горить, випускає вогонь у порожніх сусідів і здіймає вітер; вигорів → Empty |
| Fire | object | ra згасає щотік | дме вгору; підпалює Gas і Dust; гасне від Water або коли ra < 5 |
| Lava | object | — | важка рідина; підпалює Gas/Dust; Water → лава стає Stone, вода зникає |
| Wood | object | лічильник горіння | від Fire/Lava горить, іноді підпалює сусідів, вигорів → Empty; вода гасить |
| Ice | object | — | тане від Fire/Lava або тиску > 120; іноді заморожує сусідню Water |
| Stone | object | — | падає й тоне як пісок; стоїть, якщо обидві верхні діагоналі — Stone; тиск > 120 → іноді Sand |
| Dust | object | — | падає (міняється лише з Water); тиск > 120 → Fire + вибух вітру |
| Plant | object | ra | росте вниз у порожнечу, поширюється в Wood, вбирає Water/Fungus; горить |
| Seed | object | ra, rb — стадія | падає; на Sand/Plant/Fungus проростає: стебло лишає Plant, пелюстки розходяться вбік; вогонь → Fire |
| Fungus | object | ra | поширюється в порожнечу (особливо біля Wood); горить |
| Acid | object | ra = сила | тече; коли заблокована, розчиняє не-Wall сусідів, кожне розчинення −60 ra; ra < 80 → зникає |
| Mite (кліщ) | neutral | ra, rb — шлях | ходить і стрибає; їсть Plant, Wood, Seed, Dust; гине від Fire, Lava, Water, Oil |
| Cloner | spawner | rb = що клонувати | запамʼятовує перший не-порожній сусідній вид і породжує його в порожні сусідні клітини |
| Rocket | object | rb = паливо | спершу падає; запамʼятовує вид, якого торкнулась, злітає й лишає слід із нього; заблокована → Empty |
| Вітер / тиск | zone | float-сітки | рідина на GPU: несе частинки; Fire, Lava, Oil, Dust, Wood пишуть у неї, Dust/Stone/Ice читають тиск |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «clock(cell) ≠ поточний тік»` → ТО `custom: «виклик update(cell, api) свого виду»` — двіжок не знає правил, лише викликає функцію.
- КОЛИ `tick` → ЯКЩО `cell(below, empty)` → ТО `fall(sand)`; інакше ЯКЩО `free(below_diag)` → ТО `move(sand, diag)`.
- КОЛИ `tick` → ЯКЩО `occupied(below, water|gas|oil|acid)` → ТО `swap(sand, b)` — пісок тоне.
- КОЛИ `tick` → ЯКЩО `free(side)` → ТО `move(water, side)` — розтікання; `custom: «напрям іноді копіюється з сусідньої води»`.
- КОЛИ `adjacent8(fire|lava, wood|oil|plant|fungus)` → ТО `set_state(b, burning)`; `timer(…)` → `transform(b → empty)`.
- КОЛИ `adjacent8(fire, gas|dust)` → ТО `transform(b → fire)`, `custom: «поштовх у поле вітру, тиск 80»`.
- КОЛИ `adjacent8(fire, water)` → ТО `disappear_a`.
- КОЛИ `adjacent8(lava, water)` → ТО `transform(lava → stone)`, `disappear_b`.
- КОЛИ `adjacent8(ice, fire|lava)` → ТО `transform(ice → water)`; КОЛИ `adjacent8(ice, water)` → ЯКЩО `prob(p)` → ТО `transform(water → ice)`.
- КОЛИ `tick` → ЯКЩО `custom: «тиск поля > 120»` → ТО `transform(dust → fire)` / `transform(ice → water)` / `transform(stone → sand)` (з імовірністю).
- КОЛИ `blocked(acid)` → ТО `custom: «розчинити не-Wall сусіда, ra −= 60»`; ЯКЩО `custom: «ra < 80»` → ТО `disappear_a`.
- КОЛИ `contact(mite, plant|wood|seed|dust)` → ТО `disappear_b`, `move(mite)`; КОЛИ `adjacent8(mite, fire|lava|water|oil)` → ТО `disappear_a`.
- КОЛИ `tick` → ЯКЩО `free(neighbor)` → ТО `spawn_at(cloned_species, neighbor)` (Cloner).
- КОЛИ `contact(rocket, b)` → ТО `custom: «запамʼятати вид b, злетіти, лишати слід»`.
- КОЛИ `tick` → ТО `custom: «Fire/Lava/Oil пишуть вітер у поле; поле зсуває частинки»`.
- КОЛИ `input(draw)` → ТО `spawn_at(element, brush)`; стерти — `set_cell(cell, empty)` (?) щодо інструмента.
- Перемоги, поразки, рахунку нема; єдина «оцінка» — голоси в галереї.

## Керування і ввід
- Тач і миша: малювати обраним елементом по полю; інструменти й елементи — однією кнопкою, без двоступеневого вибору (на відміну від clone/firework у старих іграх).
- Pinch-zoom вимкнено; тапи, drag і скрол по полотну розрізняються окремо.
- Завантажений сейв стартує після кнопки ▷.
- Розмір пензля, пауза, очищення — є в UI (?), у джерелах не описані.

## Вікна, меню, HUD
- `game-screen`: полотно 300×300 + `element-picker` (кнопки елементів і інструментів, React) (?) щодо точного складу.
- `save-browser` — галерея: дошки завантажень, пошук за назвою, голоси; відкриття творіння → поле + ▷.
- `custom-window` «завантажити творіння» — назва, PNG-знімок поля (?) щодо полів форми.
- HUD: майже нема — полотно і панель кнопок.
- Переходи: game-screen ↔ галерея (відкрити = замінити поле).

## Фічі поза полем
- `mode-sandbox` — уся гра.
- `level-sharing` + `user-levels-browser` + `level-rating` — галерея без акаунтів: API дозволяє лише читати, вставляти й голосувати; голоси дедуплікуються за IP; чужі пости не редагуються.
- Сейв — **безвтратний PNG**: R = species, G = ra, B = rb (кодується вбудованим енкодером браузера).
- Понад 70 000 творінь: машини Руба Ґолдберґа, «домалюй картинку», вулкани; часті ремікси популярних шаблонів.

## Варіації й родичі
- Предки й сусіди: [the-powder-toy](the-powder-toy.md) (поля тиску/тепла на грубій сітці), Powder Game, Hell of Sand; [sandboxels](sandboxels.md) (поведінка як дані — сітка правил), [sandspiel-studio](sandspiel-studio.md) (елементи програмуються блоками), Orb Farm (той самий автор, акваріум).
- Попередники автора: Lua-прототип з тим самим `getNeighbor/setNeighbor`; прототип Dust (Dirt вбирає воду → бруд, Glitch).
- **Осі варіацій**: поведінка — «код на елемент (Sandspiel) / таблиця властивостей (TPT) / DSL-сітка (Sandboxels) / блоки користувача (Studio)»; поле поверх — «нема / вітер-рідина (Sandspiel) / тиск+тепло (TPT)»; сейв — «файл / PNG з даними в каналах».

## Цікавинки для курсу
- Мінімальний движок: масив клітин, `update(cell, api)` з `get/set(dx, dy)` і біт `clock` проти подвійного оновлення — 🥉.
- Клітина як 4 байти (вид + 2 регістри + clock) і рендер «без копії» — 📎 у Python (масив numpy), 🥈 з GPU.
- Сейв поля як PNG: канали RGB = дані — 📎: картинка, яку можна і подивитись, і завантажити.
- Cloner: запамʼятати перший сусідній вид і копіювати його — 🌱.
- Ракета, що лишає слід із торкнутого виду — 📎.
- Вітер як окреме поле, з яким частинки обмінюються щокадру — 🥇.
- Галерея з голосами без акаунтів (лише GET/INSERT/vote) — 🥈 як вебчастина курсу.

## Мапа на каталог
- Є: `gravity-fall` · `cell-transform` (лава → камінь, лід ↔ вода) · `spawner-entity` (Cloner) · `game-loop` · `state-as-data` (поле = масив байтів) · `logic-render-split` (WASM-симуляція / WebGL-рендер) · `in-game-editor` + `editor-palette` + `editor-erase` (уся гра — малювання) · `level-exchange` + `level-rating` (галерея з голосами) · `cell-click` (клік/тап по полотну).
- **Нема** → пропозиції карток:
  - `+falling-sand-cell` (повтор TPT) · `+density-displacement` (повтор TPT) · `+pressure-field` (повтор TPT: тут вітер-рідина).
  - `+cell-registers` «Клітина з двома байтами стану (ra, rb)» · entities/state · 📎.
  - `+update-clock-bit` «Біт тіку проти подвійного оновлення при скані» · code/python · 🌱.
  - `+relative-neighbor-api` «Правила бачать лише сусідів через get/set(dx, dy)» · entities/interact · 📎.
  - `+image-as-save` «Сейв як PNG, дані в каналах кольору» · game-logic/history · 📎.
  - `+cloner-element` «Клітина копіює сусідній вид» · entities/interact · 🌱 · `+burn-countdown` «Горіння з лічильником, потім зникнення» · entities/state · 🌱.

## Пропозиції до словників
- `+cond:pressure(cell, op, p)` — поріг поля тиску (повтор TPT).
- `+effect:set_wind(dx, dy, pressure, density)` — записати силу в поле вітру.
- `+role:material` · `+role:field` — повтор TPT: у таблиці частинки записані як `object`, вітер — як `zone`, бо точних ролей нема.
- `+window:save-browser` — онлайн-галерея творінь з голосами (повтор TPT).
- `+card:cell-registers` · `+card:update-clock-bit` · `+card:image-as-save` — див. «Мапа на каталог».

## Джерела
- ⭐ [Making Sandspiel](https://maxbittker.com/making-sandspiel) — формат клітини, update API, скан і clock, вітер з WebGL-Fluid, PNG-сейви, бекенд галереї (Firebase → Postgres), 70 000 творінь.
- [species.rs](https://raw.githubusercontent.com/MaxBittker/sandspiel/master/crate/src/species.rs) — enum 19 видів і поведінка кожного; пороги тиску 120.
- [GitHub: sandspiel](https://github.com/MaxBittker/sandspiel) — код; README: рідина з WebGL-Fluid-Simulation, мета «шерити й форкати творіння».
- [sandspiel.club](https://sandspiel.club) — гра.
- [Sandboxels wiki: Falling-sand game](https://sandboxels.wiki.gg/wiki/Falling-sand_game) — рядок жанрової таблиці.

## Непевне
- (?) Точний склад кнопок (Wind, Erase, розмір пензля, пауза, Reset) — у статті не описано; ui.js у репо не знайшовся.
- (?) Чи є в самій Sandspiel «custom element maker» (так пише таблиця жанру) — схоже, це Sandspiel Studio; README Sandspiel називає його метою на майбутнє.
- (?) Сторінка itch.io не відкривалась.
