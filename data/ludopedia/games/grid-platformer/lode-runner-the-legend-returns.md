---
title: "Lode Runner: The Legend Returns"
slug: lode-runner-the-legend-returns
aka: [LRLR, Lode Runner TLR, "Lode Runner: The Legend Returns & Lode Runner Extra"]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1994
platforms: [MS-DOS, Windows, Mac OS, PlayStation, Sega Saturn]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner:_The_Legend_Returns", best: true, note: "інструменти, типи ґрунту, ченці, 10 світів, нічні рівні, дуо-рівні, редактор"}
  - {kind: other, url: "https://global.tozaigames.com/loderunner/history", note: "історія серії від правовласника: список пристроїв, бедрок, телепорти, трюк- і липкі блоки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lode_Runner_Online:_The_Mad_Monks%27_Revenge", note: "наступник: фазові блоки, бомби-таймери, кольорові предмети, кілька виходів"}
  - {kind: other, url: "https://32bits.substack.com/p/under-the-microscope-lode-runner", note: "Saturn-версія: меню Construction, секретні імена"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lode+Runner+The+Legend+Returns+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, ladder-climb, gravity-fall, collect-all, reach-exit, touch-death, environment-death, player-death, chase-player, respawn, cell-transform, timed-despawn, impassable-cells, destructible-blocks, explode-area, floor-types, speed-per-type, temporary-modes, teleport, inventory-items, inventory-limit, sequential-levels, world-map, in-game-editor, editor-palette, editor-playtest, theme-select, background-music, cheat-codes, status-panel, +dig-hole, +hole-refill, +trapdoor-fake-floor, +single-use-tool, +ceiling-rockfall, +sticky-floor, +darkness-light-radius, +local-coop-versus]
proposes: ["+effect:dig", "+effect:restore_cell", "+effect:use_item", "+effect:spill(cell, type)", "+cond:tool_power", "+trigger:all_collected", "+role:ladder", "+feature:night-levels", "+feature:level-packs", "+card:single-use-tool", "+card:ceiling-rockfall"]
author: opus
date: 2026-11-09
---

# Lode Runner: The Legend Returns — класичний Lode Runner плюс одноразові пристрої: бомби, пастки, газ, відбійник, кирка-завал і відро клею

## Суть
Ремейк Lode Runner (Presage / Sierra, 1994): той самий екран із ґрунту, драбин і перекладин, той самий бластер, що пропалює яму вбік-униз, і ті самі вартові — тепер «Божевільні ченці» (Mad Monks). Нове ядро — **пристрої на полі**: бігун підбирає один пристрій за раз і застосовує його, щоб змінити ґрунт або знешкодити ченців. До цього додано нові типи ґрунту (бедрок, фальш-ґрунт, липкий ґрунт), телепорти, нічні рівні з колом світла і дуо-рівні на двох.

## Поле і час
- Один екран-сітка («single frame»), без скролу; клітина — тип ґрунту або предмет.
- Real-time; клітинна гравітація як у Lode Runner: без опори сутність падає.
- Шари: ґрунт (з таймером відновлення після копання), предмети (золото, пристрої, вихід), сутності (бігун, ченці).
- 10 світів-тайлсетів (Moss Caverns, Fungus Delvings, Lost City of Ur, Crystal Hoard, Winter's Dungeon, Skeleton's Keep, Inferno's Playground, Shimmering Caverns, Shadowlands, Meltdown Metropolis) — лише оформлення.
- Інформація часткова: фальш-ґрунт виглядає як звичайний; у Shadowlands уночі весь екран чорний, крім кола світла, що рухається з гравцем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джейк Перил (Jake Peril) | player | несе ≤ 1 пристрій | біг, лазіння, висіння, падіння; бластер копає ґрунт вбік-униз; дотик ченця — смерть |
| Вес Рекліс (Wes Reckless) | player | лише дуо-рівні | другий бігун (синій костюм); кооператив або змагання |
| Божевільний чернець | enemy | — | переслідує бігуна; падає в ями; дотик — смерть бігуна |
| Ґрунт (turf) | terrain | цілий / яма (таймер) | копається бластером, з часом відновлюється; велика бомба знищує назавжди |
| Бедрок | static | — | бластер не бере; лише відбійник або велика бомба |
| Фальш-ґрунт (trapdoor turf) | terrain | виглядає як ґрунт | порожнеча: усі провалюються |
| Липкий ґрунт (gooey turf) | terrain | — | сповільнює і бігуна, і ченців |
| Драбина | terrain | — | рух угору/вниз; опора |
| Перекладина | terrain | — | рух уздовж «руками» |
| Телепорт | static | — | переносить сутність (?) у парну точку |
| Золото (скарб) | pickup | — | треба зібрати все |
| Вихід | static | не руйнується навіть великою бомбою | дійти після збору скарбів |
| Пастка-сильце (snare trap) | pickup | одноразова | ставиться на шляху; чернець застрягає (?) |
| Газ / спрей (befuddlement gas) | pickup | одноразовий | тимчасово виводить ченця з ладу |
| Відбійник (jackhammer) | pickup | одноразовий | пробиває бедрок |
| Мала бомба | pickup | одноразова | руйнує ґрунт поруч тимчасово (?) |
| Велика бомба | pickup | одноразова | руйнує ґрунт, бедрок і предмети назавжди; вихід вцілює |
| Кирка (pickaxe) | pickup | одноразова | обвалює зі стелі купу каменю — стіна проти ченців |
| Відро клею (bucket of goo) | pickup | одноразове | вкриває поверхню клеєм: хто йде по ній — повільніше |
| Купа каменю | static | від кирки | блокує прохід ченцям (?) і бігуну |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` (для вгору — `cell(here, ladder)`) → ТО `move(runner, dir)`; на перекладині — лише вліво/вправо.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)` — і бігун, і ченці.
- КОЛИ `enter(a, trapdoor_turf)` → ТО `fall(a)` — фальш-ґрунт не опора.
- КОЛИ `input(dig_left|dig_right)` → ЯКЩО `cell(below_side, turf)` → ТО `set_cell(below_side, hole)`, `custom: «яма відновлюється через N тіків»`.
- КОЛИ `input(dig_left|dig_right)` → ЯКЩО `cell(below_side, bedrock)` → ТО `block`.
- КОЛИ `timer(refill)` для ями → ТО `set_cell(hole, turf)`; ЯКЩО `occupied(hole, monk)` → ТО `disappear_b`, `respawn(monk, spawn_point)` (?); ЯКЩО `occupied(hole, runner)` → ТО `lose`.
- КОЛИ `enter(monk, hole)` → ТО `set_state(monk, trapped)`; бігун може пройти по голові застряглого (?).
- КОЛИ `contact(runner, monk)` → ЯКЩО `not state(monk, trapped)` і `not state(monk, stunned)` → ТО `lose`, `lives(-1)`, `restart`.
- КОЛИ `contact(runner, gold)` → ТО `pickup`, `counter(gold_left, -1)`.
- КОЛИ `contact(runner, device)` → ЯКЩО `not has(runner, device)` → ТО `pickup` — несе лише один пристрій.
- КОЛИ `input(use)` → ЯКЩО `has(runner, jackhammer)` і `cell(target, bedrock)` → ТО `set_cell(target, hole)`, `take(runner, jackhammer)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, small_bomb)` → ТО `explode(area, hole)` для ґрунту, `custom: «ями відновлюються»` (?), `take(runner, small_bomb)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, big_bomb)` → ТО `explode(area, empty)` — ґрунт, бедрок і предмети зникають назавжди, крім виходу; `take(runner, big_bomb)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, pickaxe)` → ТО `custom: «зі стелі падає купа каменю»`, `spawn_at(rock_pile, ahead)` (?), `take(runner, pickaxe)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, goo_bucket)` → ТО `set_cell(surface, gooey_turf)` (?), `take(runner, goo_bucket)`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, snare)` → ТО `place(snare, here)` (?), `take(runner, snare)`.
- КОЛИ `contact(monk, snare)` → ТО `set_state(monk, trapped, duration)` (?), `disappear_b`.
- КОЛИ `input(use)` → ЯКЩО `has(runner, gas)` і `in_range(runner, monk, n)` → ТО `stun(monk, n)` (?), `take(runner, gas)`.
- КОЛИ `enter(a, gooey_turf)` → ТО `speed(a, ×k)` — сповільнення для всіх.
- КОЛИ `enter(a, teleport)` → ТО `teleport` (?).
- КОЛИ `contact(rock_pile, monk)` → ТО `block`.
- КОЛИ `counter(gold_left, ==, 0)` → ТО `custom: «вихід стає доступним»` (?).
- КОЛИ `contact(runner, exit)` → ЯКЩО `counter(gold_left, ==, 0)` → ТО `win`, `next_level`.
- Поразка: дотик ченця або яма відновилась над бігуном → життя −1, рівень заново (?). Перемога: усе золото + вихід.
- Дуо-рівні: кооператив — обидва бігуни працюють на спільну мету; змагання (head-to-head) — `custom: «хто більше / хто перший»` (?).

## Керування і ввід
- Клавіатура або геймпад: рух 4 напрямки, дві кнопки копання (ліворуч/праворуч униз), кнопка «застосувати пристрій» (?).
- Дуо-рівні — два гравці одночасно за одним пристроєм (локально).
- Saturn/PS: на екрані імені — секретні імена, далі утримання L + Start відкриває спецрівень.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: гра (одиночна / дуо), Construction (редактор), введення імені гравця.
- `game-screen` — поле + `status-panel`: золото, життя, рівень, поточний пристрій (?).
- `map-window` / вибір світу (?) — 150 рівнів згруповано в 10 світів.
- `editor-window` (Construction): палітра тайлів, вибір тайлсету, день/ніч, музика, групування рівнів у набори.
- `pause-menu`; на Saturn у паузі приймається чит-послідовність.
- `end-screen` — фінальні ролики й титри.
- Переходи: main-menu → game-screen → (вихід) наступний рівень; main-menu → editor-window → (тест) game-screen.

## Фічі поза полем
- `levels-sequential`: 150 одиночних рівнів у 10 світах + 30 дуо-рівнів.
- `mode-coop` і `mode-versus` на двох (локально, Джейк і Вес).
- `level-editor`: тайлсет, день/ніч, музика незалежно від тайлсету, групування рівнів.
- Нічні рівні (Shadowlands): видно лише коло навколо гравця.
- `cheat-codes`: секретні імена на Saturn/PS відкривають спецрівень і пропуск до фіналу.

## Варіації й родичі
- Предок: [lode-runner](lode-runner.md) (1983) — копання, золото, вартові; тут вартові → ченці, драбина-вихід → вихід-обʼєкт (?).
- Наступник: Lode Runner Online: The Mad Monks' Revenge (1995) — мережева гра, фазові блоки за таймером (давлять того, хто стоїть усередині), бомби, що самі вибухають і зʼявляються знову, предмети, які бере лише гравець відповідного кольору, кілька виходів із переходом у різні рівні набору.
- Lode Runner Extra (Saturn/PS) — додатковий набір рівнів.
- Родичі в сімʼї: [wrecking-crew](wrecking-crew.md) (бомби руйнують стіни), [toki-tori](toki-tori.md) (одноразові інструменти з запасом), [kings-valley](kings-valley.md) (витратна кирка), [solomons-key](solomons-key.md) (створення/руйнування блоків).
- Осі: **хто дає інструмент** (лежить на полі, один у руках / запас на рівень / нескінченний); **сила руйнування** (ґрунт тимчасово / ґрунт назавжди / бедрок); **кого зачіпає ґрунт** (лише гравця / усіх — липкий ґрунт сповільнює обох).

## Цікавинки для курсу
- Рука на один пристрій: підняти, застосувати, зникає; новий не взяти, доки не використав — 📎.
- Ієрархія міцності клітин (ґрунт → бедрок) і пристрої різної сили: бластер / відбійник / мала / велика бомба — 🥉 (таблиця «інструмент × клітина → результат»).
- Кирка-завал: спавн непрохідної купи як стіни проти ворогів — 🌱.
- Липкий ґрунт і відро клею: модифікатор швидкості, однаковий для гравця й ворогів — 📎.
- Нічний рівень: рендер лише в радіусі гравця — 🥉.
- Дуо на одній клавіатурі (кооп і змагання) — 🥉.
- Редактор з тайлсетом, днем/ніччю й музикою як властивостями рівня — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `ladder-climb` · `gravity-fall` · `collect-all` · `reach-exit` · `touch-death` · `environment-death` · `player-death` · `chase-player` · `respawn` · `cell-transform` · `timed-despawn` (яма) · `impassable-cells` (бедрок) · `destructible-blocks` · `explode-area` (бомби) · `floor-types` (липкий / фальш-ґрунт) · `speed-per-type` · `temporary-modes` (оглушений чернець) · `teleport` · `inventory-items` · `inventory-limit` (1) · `sequential-levels` · `world-map` (?) · `in-game-editor` · `editor-palette` · `editor-playtest` (?) · `theme-select` · `background-music` · `cheat-codes` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+dig-hole` «Копання ями вбік-вниз» · entities/interact · 🥉 (як у lode-runner).
  - `+hole-refill` «Яма відновлюється за таймером» · entities/interact · 📎.
  - `+trapdoor-fake-floor` «Фальшпідлога» · entities/legality · 🌱.
  - `+single-use-tool` «Одноразовий пристрій у руці» · entities/state · 📎 · слоти {capacity: 1, tools}.
  - `+ceiling-rockfall` «Завал зі стелі блокує ворогів» · entities/interact · 🌱.
  - `+sticky-floor` «Липка підлога сповільнює всіх» · entities/interact · 🌱.
  - `+darkness-light-radius` «Темрява, коло світла навколо гравця» · interface/render · 🥉 · слот {radius}.
  - `+local-coop-versus` «Два аватари на одному екрані: кооп / змагання» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+effect:dig(cell, side)` — пропалити ґрунт збоку внизу (тимчасово); ⏳ у lode-runner.
- `+effect:restore_cell(cell, after)` — повернути тип клітини через N тіків.
- `+effect:use_item(item)` — застосувати предмет з руки (ефект залежить від предмета, потім `take`).
- `+effect:spill(cell, type)` — розлити покриття на поверхню (клей).
- `+cond:tool_power(tool, cell)` — інструмент достатньо сильний для типу клітини (бластер < відбійник < велика бомба).
- `+trigger:all_collected(kind)` — зібрано весь скарб (частину можуть нести вороги).
- `+role:ladder` — драбина/перекладина як окрема роль або `terrain` з прапорцем «лізти».
- `+feature:night-levels` — рівень у темряві з колом світла.
- `+feature:level-packs` — групування власних рівнів у набір у редакторі.
- `+card:single-use-tool`, `+card:ceiling-rockfall` — див. вище.

## Джерела
- ⭐ [Wikipedia: Lode Runner: The Legend Returns](https://en.wikipedia.org/wiki/Lode_Runner:_The_Legend_Returns) — один пристрій за раз, список пристроїв, кирка-завал, клей, бедрок/фальш-/липкий ґрунт, ченці, 150 рівнів у 10 світах, нічні рівні, 30 дуо-рівнів, редактор.
- [Tozai Games: історія Lode Runner](https://global.tozaigames.com/loderunner/history) — «befuddlement gas», малі й великі бомби, бедрок лише відбійником / великою бомбою, телепорти, трюк- і липкі блоки, кооп і head-to-head.
- [Wikipedia: Lode Runner Online](https://en.wikipedia.org/wiki/Lode_Runner_Online:_The_Mad_Monks%27_Revenge) — що додав наступник.
- [32bits: Lode Runner TLR & Extra на Saturn](https://32bits.substack.com/p/under-the-microscope-lode-runner) — меню Construction, секретні імена.
- YouTube: пошук «Lode Runner The Legend Returns gameplay».

## Непевне
- (?) Точна дія сильця, газу й малої бомби (тривалість, площа, чи відновлюються ями від малої бомби) — джерела називають пристрої, але не описують.
- (?) Чи ченці несуть золото, як вартові оригіналу; де вони відроджуються; чи можна стояти на голові застряглого.
- (?) Як працюють телепорти (парні / односторонні) і чи є ключі й двері — у джерелах лише згадка «teleports».
- (?) Вигляд виходу: двері, що зʼявляються після збору золота, чи драбина, як в оригіналі; Wikipedia каже лише «reach the exit».
- (?) Чи купа каменю блокує й бігуна і чи її можна прокопати.
- (?) Правила змагального дуо-режиму й лічба очок, кількість життів, клавіші — не знайдено.
- (?) `random: none` — ченці можуть мати випадковий вибір; не перевірено.
