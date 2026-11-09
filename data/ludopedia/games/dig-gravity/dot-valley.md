---
title: Dot Valley
slug: dot-valley
aka: [WebValley, DOT VALLEY]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1987
platforms: [Enterprise 128, MS-DOS, web]
links:
  - {kind: other, url: "http://www.onlinespiele.de/ANLEIT3.HTM", best: true, note: "DE: повна інструкція WebValley — кожен елемент, клавіші, ціль"}
  - {kind: other, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareMSDOS.html", note: "bd-fans: картка Dot Valley v1.20se (MS-DOS) серед BD-клонів"}
  - {kind: other, url: "https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareJava.html", note: "bd-fans: WebValley (Java), автори"}
  - {kind: other, url: "http://www.onlinespiele.de/MAKING3.HTM", note: "DE: Making of — історія 1987 → 1993 → Java, статус-рядок"}
  - {kind: play, url: "http://www.onlinespiele.de/VALLEY.htm", note: "Java-аплет WebValley (сучасні браузери Java не запускають)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dot+Valley+game", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, dig-terrain, gravity-fall, roll-off-rounded, push-object, collect-all, touch-death, environment-death, chase-greedy, spawn-random-cell, spawn-animation, spawner-entity, carrier-platform, inventory-items, explode-area, destructible-blocks, event-points, sequential-levels, status-panel, +egg-hatch, +lava-burns-above, +fire-wheel, +push-vertical-neighbour, +harmless-falling-gem, +plug-generator]
proposes: ["+trigger:hatch", "+card:egg-hatch", "+card:lava-burns-above", "+card:fire-wheel", "+card:push-vertical-neighbour", "+card:harmless-falling-gem", "+card:plug-generator", "+ui:percent-meter"]
author: opus
date: 2026-11-09
---

# Dot Valley — Boulder Dash, де алмази не вбивають, а з яєць, що зʼявляються самі, вилуплюються погоні

## Суть
Гравець копає землю, збирає всі «вільні» алмази рівня й переходить далі; камені падають і вбивають. Від [Boulder Dash](boulder-dash.md) відрізняє: **падаючий алмаз безпечний**, камінь скочується по діагоналі з будь-чого (і з гравця), а вороги не стоять на рівні з початку — **яйця самі зʼявляються в порожнечі** й вилуплюють монстрів, як у [Repton](repton.md). Нові стихії: лава спалює все над собою, конвеєри везуть обʼєкти, вогняні колеса котяться й вбивають збоку, генератори алмазів треба заткнути. Гравець може зсувати камінь, що лежить над ним або під ним.

## Поле і час
- Рівень — сітка тайлів 32×32 px зі скролом; зовнішня рамка невразлива.
- Один шар; у клітині один елемент.
- Real-time; багато каменів падає одночасно — заради цього гра й почалась на Enterprise 128 (1987).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух 4 напрямки; копає землю; штовхає камінь у порожнечу; зсуває камінь над/під собою вбік; сходить з конвеєра вгору, якщо є місце |
| Порожнеча | terrain | — | прохід для гравця й монстрів; сюди падають камені, алмази, бомби; тут самі зʼявляються яйця |
| Земля (4 види) | terrain | — | проходить лише гравець (копає); монстри не проходять; руйнує лише вибух |
| Межовий камінь (стіна) | static | рамка невразлива | внутрішні — руйнуються вибухом |
| Камінь | object | — | падає вниз; по діагоналі, якщо вільні бокова й нижня-бокова; падаючий вбиває гравця; лежачий можна підкопати знизу |
| Вільний алмаз | pickup | ціль рівня | падає як камінь, **не шкодить**; монстри їдять; лава спалює |
| Вмурований алмаз | pickup | бонусні очки | поводиться як земля; не обовʼязковий |
| Бомба | pickup → object | затримка | B — поставити; падає, якщо може; вибух знищує все поруч |
| Динаміт | pickup → object | кілька секунд | Space — поставити; не падає; вибух знищує сусідів |
| Яйце монстра | container | час до вилуплення | нешкідливе; можна підірвати або завалити каменями; перед вилупленням тремтить |
| Монстр | enemy | — | женеться за гравцем лише по прямій (горизонталь/вертикаль), не обходить перешкод; ходить по порожнечі або їсть алмази; гине від каменя, лави, вибуху |
| Вогняне колесо | hazard | — | котиться горизонтально і вниз; дотик збоку — смерть; вбиває і монстрів |
| Лава | hazard | — | миттєво спалює все безпосередньо над собою, крім землі; камінь у лаві розчиняється |
| Конвеєр | terrain | напрямок | везе все, що лежить на ньому |
| Генератор алмазів | spawner | — | породжує алмази; на деяких рівнях треба знищити або заткнути |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth|empty)` → ТО `move(player, dir)`; земля → `set_cell(empty)`.
- КОЛИ `contact(player, stone)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `input(up+left|up+right)` → ЯКЩО `occupied(above, stone)` and `free(side of stone)` → ТО `custom: «зсунути камінь над гравцем убік»`; так само `down+dir` — камінь під гравцем.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(stone|diamond|bomb)`; ЯКЩО `free(side)` and `free(side-below)` → ТО `roll(a, side)`.
- КОЛИ `contact(falling stone, player)` → ТО `lose`; КОЛИ `contact(falling diamond, player)` → ТО `block` (не шкодить).
- КОЛИ `contact(player, free_diamond)` → ТО `pickup`, `counter(diamonds, -1)`; вмурований → `pickup`, `score(bonus)`.
- КОЛИ `rng(p)` → ЯКЩО `cell(x, empty)` → ТО `spawn_at(egg, x)` (?).
- КОЛИ `timer(hatch)` → ТО `set_state(egg, wobbling)`, далі `transform(monster)`.
- КОЛИ `tick` → ЯКЩО `line_of_sight(monster, player)` → ТО `move(monster, toward player)`; інакше `custom: «не обходить перешкод — перекритий шлях зупиняє»`.
- КОЛИ `contact(monster, diamond)` → ТО `disappear_b` (зʼїдає).
- КОЛИ `contact(monster, player)` → ТО `lose`.
- КОЛИ `contact(falling stone, monster|egg)` або `enter(monster, lava)` → ТО `disappear_b`.
- КОЛИ `tick` → ТО `custom: «вогняне колесо котиться вбік і вниз»`; КОЛИ `contact(wheel, player)` збоку → ТО `lose`; з монстром → `disappear_b`.
- КОЛИ `tick` → ЯКЩО `occupied(above lava, any)` and `not cell(above, earth)` → ТО `custom: «спалити те, що над лавою»`.
- КОЛИ `tick` → ЯКЩО `occupied(on conveyor, any)` → ТО `move(a, conveyor_dir)`.
- КОЛИ `input(B)` → ЯКЩО `has(player, bomb)` → ТО `place(bomb)`; КОЛИ `timer(delay)` → `explode(around)`.
- КОЛИ `input(space)` → ЯКЩО `has(player, dynamite)` → ТО `place(dynamite)` (не падає); КОЛИ `timer(few s)` → `explode(adjacent)`.
- КОЛИ `explode` → ТО знищує все в зоні, крім зовнішньої рамки: землю, стіни, яйця, монстрів.
- КОЛИ `timer(gen)` → ЯКЩО `free(out of generator)` → ТО `spawn_at(diamond, out)`.
- КОЛИ `counter(free_diamonds, ==, 0)` and `custom: «генератори заткнуто, де треба»` → ТО `win`, `next_level`.
- КОЛИ `input(esc)` → ТО `window(main-menu)` (перервати гру).
- Перемога: усі вільні алмази зібрано. Поразка: камінь згори, монстр, вогняне колесо збоку, лава (?).

## Керування і ввід
- Стрілки — рух; Space — динаміт; B — бомба; ESC — на титул.
- Зсув каменя без кроку: спершу «вгору» (або «вниз»), потім коротко «ліво/право» — камінь над (під) гравцем іде вбік.
- WebValley: клацнути в поле, щоб аплет отримав клавіатуру.

## Вікна, меню, HUD
- `splash-screen` / `main-menu`: титул, старт; ESC повертає сюди.
- `game-screen`: поле зі скролом; статус-рядок унизу — `level-number`, `score`, час (`timer-elapsed` чи `timer-countdown` (?)), відсоток (`custom`, зміст невідомий), лічильники TNT і бомб (`inventory-bar`).
- Звуку немає («scrolling clone without sounds»).

## Фічі поза полем
- `levels-sequential`: рівні по черзі (кількість не знайшов).
- Безкоштовна гра; Java-версія WebValley після завантаження працює офлайн.

## Варіації й родичі
- Історія: Enterprise 128 (1987, Thilo Schwinn) → MS-DOS на Pascal (1993, EGA, згодом VGA) → Java WebValley (2000, Daniel Schwinn; графіка Tobias Schwinn).
- Родичі: [Boulder Dash](boulder-dash.md) (основа), [Repton](repton.md) (яйця й монстри), [Emerald Mine](emerald-mine.md) (динаміт і бомби), [Rocks'n'Diamonds](rocks-n-diamonds.md).
- **Осі варіацій**: падаючий алмаз — «вбиває (BD) / безпечний (Dot Valley, Banana)»; скочування — «лише з круглого (BD) / з будь-чого, якщо вільно збоку й знизу-збоку»; поява ворогів — «є на старті / з яєць, що зʼявляються випадково»; вибухівка — «падає (бомба) / стоїть (динаміт)».

## Цікавинки для курсу
- Яйце: поява у випадковій порожній клітині → таймер → тремтіння → монстр — 📎.
- Монстр «тільки по прямій» — 🌱: погоня без пошуку шляху, яку легко перекрити каменем.
- Лава, що спалює стовпець над собою, і конвеєр, що везе обʼєкти, — 📎 кожне.
- Зсув каменя над головою вбік — 🌱 новий вид штовхання.
- Генератор алмазів, який треба заткнути, щоб ціль «зібрати всі» стала досяжною — 📎.

## Мапа на каталог
- Є: `move-4dir` · `dig-terrain` · `gravity-fall` · `roll-off-rounded` (тут з будь-чого) · `push-object` · `collect-all` · `touch-death` · `environment-death` · `chase-greedy` ↔ монстр по прямій · `spawn-random-cell` ↔ яйця · `spawn-animation` ↔ тремтіння перед вилупленням · `spawner-entity` ↔ генератор алмазів · `carrier-platform` ↔ конвеєр · `inventory-items` ↔ бомби й динаміт · `explode-area` · `destructible-blocks` (внутрішні стіни, земля під вибухом) · `event-points` · `sequential-levels` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+egg-hatch` «Яйце вилуплює ворога» · entities/spawn · 📎 · слот {delay} — Dot Valley, Repton.
  - `+lava-burns-above` «Клітина знищує те, що над нею» · entities/interact · 🌱.
  - `+fire-wheel` «Котюча небезпека» · entities/move · 📎 — рух убік і вниз, смертельна збоку.
  - `+push-vertical-neighbour` «Зсунути сусіда над/під собою вбік» · entities/legality · 🌱.
  - `+harmless-falling-gem` «Падіння цілі не вбиває» · entities/interact · 🌱 — слот до `environment-death`.
  - `+plug-generator` «Заткнути генератор» · game-logic/win · 📎.

## Пропозиції до словників
- `+trigger:hatch(egg)` — контейнер дозрів і випускає вміст (яйця Dot Valley, Repton).
- `+ui:percent-meter` — відсоток на статус-рядку (зміст у Dot Valley невідомий; кандидат «% зібраного»).

## Джерела
- ⭐ [onlinespiele.de: Spielanleitung WebValley](http://www.onlinespiele.de/ANLEIT3.HTM) — DE: ціль, клавіші, кожен елемент (камінь по діагоналі, яйця, монстр по прямій, колесо, лава, конвеєр).
- [bd-fans: Freeware MS-DOS clones](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareMSDOS.html) — картка Dot Valley v1.20se: «falling diamonds are not deadly», генератори алмазів.
- [bd-fans: Freeware Java](https://www.artsoft.org/rocksndiamonds/levels/martijnmooij/2010-03-16/www.bd-fans.com/FreewareJava.html) — WebValley, «objects roll off grass and the player».
- [onlinespiele.de: Making of](http://www.onlinespiele.de/MAKING3.HTM) — автори, 1987/1993/2000, тайли 32×32, статус-рядок.
- [onlinespiele.de: WebValley](http://www.onlinespiele.de/VALLEY.htm) — сторінка аплета, керування стрілками.

## Непевне
- (?) Чи яйця зʼявляються випадково (інструкція: «spontan» у порожнечі) чи їх «скидають» обʼєкти (bd-fans: «hatch from dropped eggs»); `random: runtime` тримається на цьому.
- (?) Що означає відсоток на статус-рядку і чи час — ліміт.
- (?) Кількість рівнів, життя, очки за алмаз — у джерелах нема.
- (?) Чи вбиває лава гравця (сказано «спалює все над собою, крім землі»).
- (?) Як саме «заткнути» генератор — камінь перед виходом (?).
- (?) Рік 1987 — початок роботи на Enterprise; завершена DOS-гра — 1993.
