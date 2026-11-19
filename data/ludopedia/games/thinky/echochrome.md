---
title: Echochrome
slug: echochrome
aka: [無限回廊, Mugen Kairō, Echochrome Micro, "無限回廊‐序曲‐"]
family: thinky
also: []
klass: hybrid
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2008
platforms: [PSP, PS3, PS4/PS5 (PS Plus Classics)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Echochrome", best: true, note: "манекен іде сам за правилом лівої руки, відлуння й фінальне відлуння, падіння на те, що видно під ним, рахунок — час; версії й кількість рівнів"}
  - {kind: other, url: "https://www.pocketgamer.com/echochrome/review/", note: "рецензія PSP: пʼять законів перспективи з англійськими назвами, режими Free-form / Atelier / Canvas, 56 пазлів, час без ліміту"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/無限回廊", note: "五大錯覚 — пʼять ілюзій, аксонометрія, камеру не можна поставити рівно згори чи збоку, правила редактора solo / pair / other"}
  - {kind: other, url: "https://www.commonsensemedia.org/game-reviews/echochrome", note: "манекена можна зупинити чи прискорити; Freeform під таймер без індикатора — лише звук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Echochrome+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-auto, wall-follower, gravity-fall, respawn, collect-quota, reach-exit, sequential-levels, level-select, mode-select, time-out, sound-warnings, score-records, in-game-editor, editor-palette, level-exchange, movement-animation, background-music, +auto-walker-guide, +perspective-alignment, +camera-orbit, +occlusion-logic, +perspective-landing, +jump-pad, +fast-forward]
proposes: ["+cond:projected_adjacent", "+cond:occluded", "+trigger:view_changed", "+effect:land_on_projection", "+axis:control", "+ui:audio-countdown", "+feature:editor-rule-presets", "+card:perspective-path", "+card:occlusion-logic"]
author: opus
date: 2026-11-19
---

# Echochrome — манекен іде сам, а шлях складає ракурс камери: що бачиш, те й існує

## Суть
Абстрактна головоломка Sony (2008): деревʼяний манекен сам крокує балками 3D-конструкції, а гравець ним не керує — лише обертає камеру і може зупинити чи прискорити ходу. Світ підкоряється пʼяти «законам перспективи»: що на екрані здається зʼєднаним, те зʼєднане; схований розрив — цілий; схований отвір — відсутній; падіння й стрибок закінчуються на тому, що на екрані опинилось під манекеном. Мета — провести його через усі «відлуння» (тіні-маркери), після чого зʼявляється останнє відлуння-фініш; клас `hybrid` — автономний аватар плюс «рука» на камері.

## Поле і час
- Рівень — конструкція з кубів і балок (воксельна 3D-сітка) у мінімалістичній подачі; у JA-вікі — аксонометрія (軸測投影図). Манекен ходить поверхнями фігур і сам із краю шляху не сходить.
- **Логічна суміжність — екранна**: звʼязки, розриви, отвори й точки приземлення визначає 2D-проєкція з поточного кута камери, а не 3D-сусідство. Граф шляху перебудовується з кожним поворотом.
- Камера обертається навколо конструкції; рівно згори, знизу чи збоку її поставити не можна — інакше гра стала б надто легкою (JA-вікі).
- Real-time: манекен іде безперервно. Atelier — без ліміту, рахується час проходження; Freeform — випадкова серія пазлів під таймер.
- Обсяг: PS3 — 56 рівнів (+1000 рівнів гравців оновленням, набір періодично змінюється); PSP (JP) — 96 у режимах solo / pair / others; Echochrome Micro (PSN) — 96, лише solo; PSP (NA) — 56 + DLC на 40.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Манекен (キャスト, cast) | player | позиція, напрям, швидкість | іде сам; на розвилці — ліворуч → прямо → праворуч → назад (край шляху тримає зліва); падає в отвір, злітає з трампліна |
| Відлуння (echo) | pickup | — | тінь манекена в точці конструкції; зникає, коли він туди доходить; порядок довільний |
| Фінальне відлуння | static | зʼявляється після останнього | дійти — рівень пройдено |
| Балка / куб | static | 3D-позиція | поверхня шляху; ближча до камери балка може закрити розрив чи отвір |
| Розрив у шляху | terrain | видимий / закритий | видимий — край шляху; закритий іншим обʼєктом — «є» (Perspective Existence) |
| Отвір (落とし穴) | terrain | видимий / закритий | видимий — манекен провалюється й падає; закритий — «нема» (Perspective Absence) |
| Трамплін (біла площадка) | terrain | — | підкидає манекена; приземлення — на шлях, що на екрані під ним (Perspective Jump) |
| Інші манекени (others) | neutral | — | окремий тип у режимі «others» і в редакторі; поведінка — (?) |
| Пара (pairA, pairB) | player | по 2 в рівні | правило «pair» (PSP) і в редакторі; мета пари — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Хода (Wikipedia: «moves autonomously … keeps the path's boundary on the character's left»):
- КОЛИ `tick` → ЯКЩО `not state(cast, stopped)` → ТО `move(cast, dir)` — крок уперед поточною швидкістю.
- КОЛИ `custom: «манекен дійшов до вузла шляху»` → ТО `face(cast, dir)` — перший можливий із «ліворуч → прямо → праворуч → назад».

Пʼять законів перспективи (назви — Pocket Gamer, JA: 五大錯覚):
- Traveling: КОЛИ `custom: «камеру повернуто»` → ЯКЩО `custom: «кінці двох шляхів збігаються на екрані»` → ТО `custom: «шляхи зʼєднано — манекен переходить з одного на інший»`.
- Existence: КОЛИ `custom: «попереду розрив»` → ЯКЩО `custom: «розрив закритий з ракурсу ближчим обʼєктом»` → ТО `move(cast, dir)` — так, ніби шлях тягнеться за перешкодою; інакше розрив — край шляху.
- Absence: КОЛИ `enter(cast, hole)` → ЯКЩО `custom: «отвір видно з ракурсу»` → ТО `fall(cast)`; інакше `move(cast, dir)` над ним.
- Jump: КОЛИ `enter(cast, jump_pad)` → ТО `custom: «злітає вгору-вперед»`.
- Landing: КОЛИ `custom: «манекен у польоті (падіння чи стрибок)»` → ЯКЩО `custom: «на екрані під ним є поверхня»` → ТО `custom: «приземлитися на неї»`, хоч у 3D вона може бути далеко.
- КОЛИ `edge(cast)` (пролетів нижній край екрана) → ТО `respawn(cast, previous_position)`.

Мета:
- КОЛИ `contact(cast, echo)` → ТО `disappear(echo)`, `counter(echoes_left, -1)`.
- КОЛИ `all_gone(echo)` → ТО `spawn(final_echo)`.
- КОЛИ `contact(cast, final_echo)` → ТО `win`, `timer(stop)`, `next_level` (у курсі з кількох рівнів).

Ввід:
- КОЛИ `input(stick)` → ЯКЩО `custom: «новий кут — не рівно згори, знизу чи збоку»` → ТО `camera(rotate)`.
- КОЛИ `input(stop)` → ТО `set_state(cast, stopped)`; повторно — `clear_state(cast, stopped)`.
- КОЛИ `input(fast)` → ТО `speed(cast, ×k)`.
- Freeform: КОЛИ `counter(time_left, <, n)` → ТО `sound(warning)`.
- Freeform: КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «серію завершено»` (?).
- Перемога: зібрано всі відлуння й досягнуто фінального. · Поразки нема: падіння за край лише повертає манекена. · Рахунок: час рівня чи курсу.

## Керування і ввід
- Аналоговий стик — обертання конструкції / камери (Pocket Gamer, Common Sense Media); манекена напряму не ведуть.
- Окремі дії — зупинити манекена і прискорити ходу (Common Sense Media); на яких кнопках — (?).
- Canvas — розстановка обʼєктів у редакторі.

## Вікна, меню, HUD
- `mode-select`: Atelier (вибір пазлів і «portfolio» своїх рівнів) · Free-form (випадкова серія) · Canvas (редактор) — Pocket Gamer; у PSP (JP) — режими solo / pair / others.
- `level-select` (Atelier): 56 пазлів.
- `game-screen`: конструкція, манекен, відлуння; у Freeform `timer-countdown` не показано — час нагадує лише звук.
- `editor-window` (Canvas): 9 типів обʼєктів, у кожного свій максимум; правило рівня (solo / pair / other) обмежує набір; готовий рівень лягає у «factory» розділу «box», звідки його грають або надсилають іншим (JA-вікі).
- `end-screen`: час проходження (?).
- Переходи: mode-select → level-select → game-screen → (фінальне відлуння) наступний рівень курсу або end-screen; Canvas → editor-window → factory → game-screen.

## Фічі поза полем
- `levels-sequential` курсами (кілька рівнів поспіль, рахується час усього курсу) + Atelier як вільний вибір пазла.
- Freeform — щось на зразок `mode-time-attack`: випадкова серія пазлів під прихований таймер.
- `level-editor` (Canvas) з пресетами правил і лімітами обʼєктів + `level-sharing`; на PS3 — 1000 рівнів гравців оновленням, набір періодично змінюється.
- `achievements`: 10 трофеїв PS3 (оновлення 11.12.2008).
- Окремі видання: Echochrome Micro (PSN, лише solo), DLC на 40 рівнів (PSP, NA).

## Варіації й родичі
- Серія: Echoshift (2009, spin-off) · Echochrome II / 無限回廊 光と影の箱 (PS3, 2010, лише PlayStation Move); пробна версія 練習曲 (Étude) і міні-гра 変奏曲 (Variation) у PlayStation Home.
- У корпусі: `games/thinky/monument-valley.md` (той самий принцип «звʼязність за проєкцією», але Іда йде на тап, а крутять частини споруди), `games/thinky/the-observers-paradox.md` (стан залежить від погляду), `games/grid-platformer/captain-toad-treasure-tracker.md` (крутити камеру, щоб побачити шлях), `games/dig-gravity/lemmings.md` (автономні ходоки).
- **Осі варіацій:** що вирішує проєкція — звʼязність / приховування / приземлення (тут усі три); хто веде героя — сам за правилом руки (Echochrome) / тап і пошук шляху (Monument Valley) / пряме керування; що крутить гравець — камеру / частину споруди / увесь світ на 90°.

## Цікавинки для курсу
- Ходок за правилом лівої руки на графі шляхів: пріоритет «ліворуч → прямо → праворуч → назад» — 📎.
- Камера-орбіта навколо 3D-сітки й ортографічна проєкція клітин на екран — 🥉.
- Звʼязність за проєкцією: дві клітини сусідні, якщо їхні проєкції торкаються; граф перебудовується з кожним поворотом — 🥇.
- Оклюзія як правило: розрив чи отвір, закритий ближчою балкою, «не існує» (буфер глибини по клітинах) — 🥇.
- Приземлення на першу поверхню вздовж екранної вертикалі під манекеном — 🥈.
- Відлуння → фінальне відлуння (квота відкриває вихід) — 🌱.
- Редактор із пресетами правил і лімітом кожного обʼєкта (валідація перед збереженням) — 🥈.

## Мапа на каталог
- Є: `move-auto` ↔ манекен іде сам, а ввід (камера) змінює, куди він потрапить; `wall-follower` ↔ правило лівої руки — тут для героя, не ворога (слот side: left); `gravity-fall` ↔ падіння в отвір; `respawn` ↔ падіння за нижній край → попередня позиція; `collect-quota` + `reach-exit` ↔ усі відлуння відкривають фінальне; `sequential-levels` ↔ курси; `level-select` + `mode-select` ↔ Atelier / Freeform / Canvas; `time-out` + `sound-warnings` ↔ Freeform без видимого таймера; `score-records` ↔ час проходження; `in-game-editor` + `editor-palette` + `level-exchange` ↔ Canvas і рівні гравців; `movement-animation`; `background-music`.
- **Нема** → пропозиції карток:
  - `+auto-walker-guide` (уже в корпусі: Lemmings, Troddlers) — тут керують не ходоком, а ракурсом.
  - `+perspective-alignment` / `+perspective-path` «Шлях за збігом проєкцій» · entities/legality · 🥇 (уже пропонувала Monument Valley).
  - `+occlusion-logic` «Що сховано від камери — того нема» · entities/legality · 🥇 · слот {what: gap|hole}.
  - `+perspective-landing` «Приземлення на те, що на екрані під тобою» · entities/move · 🥈.
  - `+camera-orbit` (уже в корпусі) — тут це головний ввід, а не огляд.
  - `+jump-pad` (уже в корпусі) · слот {landing: by-projection}.
  - `+fast-forward` (уже в корпусі) — прискорення й зупинка ходока.

## Пропозиції до словників
- `+cond:projected_adjacent` — дві клітини суміжні на екрані (у проєкції), хоча в 3D розірвані (уже пропонувала Monument Valley).
- `+cond:occluded(cell)` — клітина (розрив, отвір) закрита від камери ближчим обʼєктом.
- `+trigger:view_changed` — камеру повернуто; логіка поля, що залежить від ракурсу, перераховується.
- `+effect:land_on_projection` — приземлитися на першу поверхню під собою в екранній проєкції.
- `+axis:control` — значення `camera`: гравець керує не героєм, а ракурсом (поруч із `indirect`).
- `+ui:audio-countdown` — таймер без індикатора, лише звукове попередження (Freeform).
- `+feature:editor-rule-presets` — редактор з набором правил рівня (solo / pair / other), що обмежує палітру й кількість обʼєктів.
- `+card:perspective-path`, `+card:occlusion-logic` — механік нема в каталозі.

## Джерела
- ⭐ [Wikipedia: Echochrome](https://en.wikipedia.org/wiki/Echochrome) — автономна хода з пріоритетом «ліворуч → прямо → праворуч → назад», відлуння й фінальне відлуння, схований розрив «продовжує» шлях, падіння «to whatever appears to be below it», падіння за низ екрана → попередня позиція, рахунок за часом, версії й кількість рівнів, сиквели.
- [Pocket Gamer: review](https://www.pocketgamer.com/echochrome/review/) — Perspective Traveling / Landing / Existence / Absence / Jump, стик повертає ракурс, Free-form / Atelier / Canvas, 56 пазлів, «Time hardly plays a role».
- [Wikipedia JA: 無限回廊](https://ja.wikipedia.org/wiki/無限回廊) — 主観的移動 / 存在 / 不在 / 跳躍 / 着地, аксонометрія, заборонені ракурси, 9 типів обʼєктів і правила solo / pair / other у редакторі, «box» і «factory».
- [Common Sense Media](https://www.commonsensemedia.org/game-reviews/echochrome) — зупинка й прискорення манекена, Freeform під час без видимого таймера (лише звук), Canvas після проходження.
- YouTube: [пошук «Echochrome gameplay»](https://www.youtube.com/results?search_query=Echochrome+gameplay).

## Непевне
- (?) Що конструкції складені з одиничних кубів на сітці — з памʼяті; Wikipedia каже лише «collections of three-dimensional shapes», JA-вікі — аксонометрія.
- (?) На яких кнопках зупинка й прискорення та чи є окремий «старт ходьби».
- (?) Режими PSP «pair» і «others»: мета пар pairA / pairB і поведінка «інших» манекенів — у джерелах лише назви й ліміти редактора; решта 4 з 9 типів обʼєктів редактора не названі.
- (?) Що стається, коли у Freeform вичерпано час; чи є HUD у звичайних рівнях.
- (?) Kotaku (у пошуковому сніпеті; сторінка віддала 404): куди приземлиться манекен з білого трампліна, не завжди очевидно.
- (?) Чи звʼязність перераховується безперервно під час обертання, чи лише коли манекен підходить до краю, — модель для курсу, не перевірено.
- (?) Походження від демки Jun Fujiki «OLE Coordinate System», механіки Echoshift і Echochrome II (тіні від ліхтарика Move) — з памʼяті.
