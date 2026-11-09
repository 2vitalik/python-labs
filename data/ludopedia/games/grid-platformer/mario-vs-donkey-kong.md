---
title: Mario vs. Donkey Kong
slug: mario-vs-donkey-kong
aka: [マリオvs.ドンキーコング, MvDK]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2004
platforms: [GBA, Switch (ремейк 2024)]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Mario_vs._Donkey_Kong", best: true, note: "Super Mario Wiki: рухи, предмети, кольорові перемикачі, усі обʼєкти й вороги, структура рівнів, Plus/Expert, e-Reader"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mario_vs._Donkey_Kong_(video_game)", note: "5 типів рівнів, зірки й Expert, ремейк 2024: Casual/Classic, кооп, Time Attack"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mario+vs+Donkey+Kong+GBA+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, ladder-climb, key-and-door, reach-exit, item-pickup, touch-death, environment-death, player-death, time-out, time-bonus, event-points, button-toggle, carrier-platform, timed-despawn, enemy-patrol, chase-player, projectile-shot, hp-damage, checkpoint, sequential-levels, level-select, level-unlock, world-map, difficulty-levels, score-records, game-screen, end-screen, +carry-throw, +color-switch-blocks, +escort-followers, +two-phase-level, +rope-wire-swing, +handstand-shield, +observer-freeze, +bonus-roulette, +star-for-par-score, +followers-as-boss-hp, +retry-costs-life]
proposes: ["+trigger:seen_by", "+effect:follow(a, b)", "+window:bonus-game", "+window:move-demo", "+feature:retry-costs-life", "+feature:time-attack", "+card:color-switch-blocks", "+card:escort-followers", "+card:two-phase-level", "+card:followers-as-boss-hp"]
author: opus
date: 2026-11-09
---

# Mario vs. Donkey Kong — пазл-платформер: віднести ключ до дверей, звільнити міні-Маріо, а потім вести загін іграшок до скрині

## Суть
Наступник Donkey Kong (Game Boy, 1994): Маріо — акробат без апгрейдів, з одним ударом до смерті. Звичайний рівень — дві половини: у першій треба **донести ключ до замкнених дверей**, у другій — дістатись до міні-Маріо в кришталевій кулі. Пазл будується на порядку дій: кольорові перемикачі вмикають блоки й драбини свого кольору, вороги — інструменти (стати, підняти, кинути), конвеєри й ліфти міняють напрям перемикачем. Кожен 7-й рівень — «пастух»: міні-Маріо ходять за Маріо, їх треба провести до скрині; кожен врятований — 1 HP у бою з Донкі Конгом.

## Поле і час
- Тайловий 2D-платформер збоку; рівень — одна-дві кімнати, ширші за екран (камера за Маріо).
- Real-time; таймер рівня. На 30 с — попередження «Hurry!», на 0 — втрата життя.
- Час, що лишився з першої половини, додається до ліміту другої; смерть у другій половині повертає очки до кінця першої.
- 6 світів × 8 рівнів (1–6 двофазні, 7 — міні-Маріо, 8 — бос) + 6 Plus-світів + 12 Expert-рівнів. Ремейк 2024 — понад 130 рівнів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маріо | player | 1 удар = смерть | біг, стрибок, потрійний стрибок, стійка на руках, сальто назад, лазіння, ношення й кидок |
| Ключ | pickup | — | носять у руках; відмикає двері до другої половини |
| Замкнені двері | gate | — | відкриваються ключем у руках Маріо |
| Міні-Маріо в кулі | static | — | ціль другої половини: розбити кулю — рівень пройдено |
| Міні-Маріо (іграшка) | ally | — | ходить за Маріо; гине від небезпек; у Plus несе ключ |
| Скриня іграшок (Toy Box) | sink | закрита / відкрита | ціль рівнів міні-Маріо; відкривається літерами T-O-Y |
| Літери T, O, Y | pickup | — | зібрати всі три → скриня відкрита |
| Подарунки (червоний, жовтий, синій) | pickup | колір | очки; усі три → бонус-гра |
| 1-Up гриб | pickup | — | +1 життя |
| Молот | pickup | — | знищує ворогів (напр. Oil); можна підкинути й зловити |
| Сміттєбак | object | — | носять і кидають; стають на ньому; ним переходять шипи |
| Help Box | static | — | нагадує, як виконати рух |
| Кольоровий перемикач | switch | червоний / жовтий / синій | вмикає платформи, Color Blocks і драбини свого кольору |
| Кольоровий блок | gate | колір; суцільний / порожній | стіна чи платформа залежно від активного кольору |
| Кольорова драбина | terrain | колір | працює лише при активному кольорі |
| Конвеєр | terrain | напрямок | везе Маріо й ключ; напрям — Direction Switch |
| Перемикач напрямку | switch | — | міняє напрям конвеєрів і ліфтів |
| Ліфт | platform | траєкторія, напрямок | їде лінією; напрям — Direction Switch |
| Пружина | object | — | вищий стрибок; працює і для міні-Маріо |
| Donut Block | terrain | — | падає, якщо на ньому стояти задовго |
| Crumble Block | terrain | — | розсипається, коли на ньому стоять |
| Дріт / мотузка / ланцюг | terrain | — | хапатись, лізти, розгойдуватись; дві мотузки одночасно |
| Драбина | terrain | — | вертикальний рух |
| Шипи | hazard | — | смерть при дотику |
| Thwomp-платформа | platform | цикл | падає й піднімається за патерном; на ній стоять |
| Лавовий гейзер | terrain | — | тримає платформи на струмені |
| Shy Guy / Polterguy | enemy | — | ходять туди-сюди; на них стають, їх піднімають і кидають; Polterguy стає блоком від перемикача свого кольору |
| Boo | enemy | — | наближається, коли Маріо дивиться геть; завмирає, коли дивиться |
| Spear Guy | enemy | спить / погоня | прокидається поруч з Маріо й переслідує; засинає на краю платформи |
| Brickman | enemy | — | кидає ряд із трьох цеглин під свою платформу; проти — стійка на руках |
| Bob-omb | enemy | запал | падає з роздавача, запалюється біля Маріо, вибухає; руйнує Bob-omb Blocks |
| Monchee / Robo Kikki | enemy | — | висить під платформою; хвіст — мотузка, тіло смертельне |
| Snapjaw | enemy | — | лізе мотузками; гине лише від падаючого фрукта |
| Thwomp / Thwimp | enemy | — | намагаються розчавити; дотик смертельний |
| Інші (Bat, Bird, Fireball, Laser, Cannon, Ninji, Podoboo, RamRam, Bucket Man, Sir Shovalot, Spark, Falling Spike…) | enemy / hazard | — | кожен — один простий патерн (див. Super Mario Wiki) |
| Донкі Конг | boss | HP | бос 8-го рівня кожного світу, атакує щоразу інакше; кидає бочки з шипами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(player, dir)`; КОЛИ `input(jump)` → ТО `custom: «стрибок; серія з трьох — потрійний»`.
- КОЛИ `input(down+jump)` → ТО `set_state(player, handstand)`; КОЛИ `contact(brick, player)` → ЯКЩО `state(player, handstand)` → ТО `block` (цеглини зверху не шкодять).
- КОЛИ `input(back+jump)` → ТО `custom: «сальто назад — високий стрибок»`.
- КОЛИ `contact(player, enemy)` → ЯКЩО `custom: «Маріо стоїть на ворогові»` і `input(grab)` → ТО `carry(player, enemy)`; КОЛИ `input(grab)` → ЯКЩО `has(player, carried)` → ТО `throw(carried, facing)`.
- КОЛИ `contact(thrown, enemy)` → ТО `disappear_b`, `score(n)`.
- КОЛИ `contact(player, key)` → ТО `carry(player, key)`; КОЛИ `contact(player, locked_door)` → ЯКЩО `has(player, key)` → ТО `custom: «друга половина рівня»`, `timer(+left)`.
- КОЛИ `contact(player, crystal_ball)` → ТО `win`, `next_level`.
- КОЛИ `contact(player, color_switch)` → ТО `set_state(color, active)`; `set_cell(color_blocks, solid)` для активного кольору й `set_cell(…, empty)` для решти.
- КОЛИ `state_on(color, active)` → ТО `transform(polterguy_of_color)` у блок.
- КОЛИ `contact(player, direction_switch)` → ТО `custom: «розвернути напрям конвеєрів і ліфтів»`.
- КОЛИ `tick` → ЯКЩО `custom: «стоїть на конвеєрі/ліфті»` → ТО `carry(platform, a)` — так і ключ, і Маріо.
- КОЛИ `timer(n)` → ЯКЩО `occupied(donut_block, player)` → ТО `fall(donut_block)`; КОЛИ `enter(player, crumble_block)` → ТО `disappear_b`.
- КОЛИ `contact(player, enemy)` → ТО `lives(-1)` (якщо не стоїть на ньому зверху); КОЛИ `contact(player, spikes)` → ТО `lives(-1)`.
- КОЛИ `custom: «Маріо приземлився на спину після падіння з висоти»` → ТО `stun(player, n)`.
- КОЛИ `custom: «Маріо дивиться на Boo»` → ТО `freeze(boo)`; інакше `move(boo, toward player)`.
- КОЛИ `contact(player, present)` → ТО `pickup`, `score(n)`; КОЛИ `counter(presents, ==, 3)` → ТО `window(bonus-game)` після рівня.
- КОЛИ `timer(every)` → ТО `counter(time, -1)`; КОЛИ `counter(time, ==, 30)` → ТО `sound(hurry)`; КОЛИ `counter(time, ==, 0)` → ТО `lives(-1)`.
- Рівень міні-Маріо: КОЛИ `tick` → ТО `custom: «кожен міні-Маріо йде за Маріо»`; КОЛИ `contact(mini, hazard)` → ТО `disappear_a`.
- КОЛИ `picked(player, toy_letters)` → ЯКЩО `counter(letters, ==, 3)` → ТО `set_state(toy_box, open)`; КОЛИ `enter(mini, toy_box)` → ТО `counter(saved, +1)`.
- КОЛИ `level_start` (бос) → ТО `hp(player, saved)`; якщо рівень міні-Маріо не пройдено — `hp(player, 4)`.
- Plus-рівень: КОЛИ `enter(mini_with_key, door)` → ТО `win`; КОЛИ `died(player)` або `died(mini)` → ТО `lives(-1)`, `restart`.
- Expert / ретрай: КОЛИ `input(restart)` → ТО `lives(-1)`.
- КОЛИ `level_end` → ЯКЩО `counter(score, >=, par)` → ТО `custom: «зірка рівня»`; зірки відкривають Expert-рівні.
- Перемога: пройти всі світи й бій з ДК; далі Plus і Expert. Поразка: 0 життів. Рахунок: подарунки, вороги, залишок часу; зірка за перевищення еталонного рахунку.

## Керування і ввід
- D-pad — рух, лазіння; A — стрибок; ↓+A — стійка на руках (A у стійці — стрибок, повтор після приземлення — подвійний); ←+A (обличчям вправо) — сальто назад; B — підняти / кинути.
- Мотузки й дроти: хват автоматичний при контакті; на дроті — обертання (Wire Spin) і викид угору.
- Кожен рівень починається автоматичною демонстрацією потрібного руху.
- Ремейк 2024: другий гравець — Тоад (локальний кооп).

## Вікна, меню, HUD
- `main-menu` → вибір світу/рівня (`level-select`, `world-map` (?)).
- `+window:move-demo` — показ потрібного руху перед рівнем.
- `game-screen`: кімната + HUD: `lives`, `score`, `timer-countdown`, зібрані подарунки (3 слоти), у рівнях міні-Маріо — літери T-O-Y і лічильник врятованих (`remaining-counter`), у боса — HP (`hp-bar`).
- `+window:bonus-game` — рулетка-бонус після рівня з трьома подарунками: 1-Up, 2 Up, 3 Up, 5 Up або голова ДК (нуль).
- `end-screen` — підсумок рівня з рахунком і зіркою; game over.
- `custom-window` — режим e-Reader (картки з рівнями; лише Японія).
- Переходи: меню → світ → рівень (демо → гра) → підсумок/бонус → наступний; 0 життів → game over → повтор світу.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: світи 1–6 → Plus-світи (після ДК) → Expert (за кількістю зірок).
- `stars-rating`: зірка за рівень, якщо побито еталонний рахунок.
- `+feature:retry-costs-life`: в Expert вихід або рестарт до першого проходження коштує життя.
- e-Reader: до 12 додаткових рівнів у форматі Expert, безмежні життя.
- Ремейк 2024: `assist-mode` (Casual: без ліміту часу, checkpoint-и, 5 ударів до втрати життя) проти Classic; `mode-coop`; `+feature:time-attack` після проходження; 2 нові світи (Merry Mini-Land, Slippery Summit) з Plus-парами.

## Варіації й родичі
- Предок: Donkey Kong (Game Boy, 1994) — той самий акробатичний набір рухів і ключ до дверей.
- Серія: March of the Minis (2006) — повністю «пастуші» рівні, керування стилусом, редактор; Minis March Again!, Mini-Land Mayhem!, Minis on the Move, Tipping Stars.
- Родичі в корпусі: [mario-and-wario](mario-and-wario.md) і [troddlers](troddlers.md) (вести автоходців), [lode-runner](lode-runner.md), [solomons-key](solomons-key.md) (ключ → двері), [wrecking-crew](wrecking-crew.md).
- Осі: **хто несе ключ** (Маріо / конвеєр / міні-Маріо); **фази рівня** (одна кімната / ключ + куля / пастух); **колір-перемикач** (3 кольори, один активний / незалежні); **ворог як інструмент** (стати / кинути / заморозити в блок).

## Цікавинки для курсу
- Ключ у руках + двері: предмет-носій, якого не можна просто «зібрати» — 🌱.
- Три кольорові перемикачі, активний колір вмикає блоки/драбини (і перетворює ворогів) — 📎.
- Взяти ворога й кинути як снаряд — 📎.
- Загін послідовників, що ходить за аватаром і гине від небезпек; врятовані = HP боса — 🥉.
- Boo: рухається лише, коли гравець дивиться геть — 🌱.
- Двофазний рівень з перенесенням часу й відкатом очок до першої фази — 📎.
- Рулетка-бонус за повний набір подарунків — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `ladder-climb` · `key-and-door` · `reach-exit` · `item-pickup` · `touch-death` · `environment-death` · `player-death` · `time-out` · `time-bonus` · `event-points` · `button-toggle` (кольорові й напрямні перемикачі) · `carrier-platform` (конвеєри, ліфти) · `timed-despawn` (Donut/Crumble) · `enemy-patrol` · `chase-player` (Spear Guy, Boo) · `projectile-shot` (кидок) · `hp-damage` (бій з ДК) · `checkpoint` (ремейк) · `sequential-levels` · `level-select` · `level-unlock` · `world-map` · `difficulty-levels` · `score-records` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+color-switch-blocks` «Перемикач активного кольору робить блоки свого кольору суцільними» · entities/interact · 📎 · слот {colors}.
  - `+escort-followers` «Загін іде за аватаром, треба довести до цілі» · entities/move · 🥉.
  - `+two-phase-level` «Рівень з двох фаз з перенесенням часу» · levels/progression · 📎.
  - `+followers-as-boss-hp` «Врятовані в рівні стають HP у наступному» · game-logic/score · 🌱.
  - `+carry-throw`, `+observer-freeze`, `+handstand-shield`, `+rope-wire-swing`, `+bonus-roulette`, `+star-for-par-score`, `+retry-costs-life` — див. правила.

## Пропозиції до словників
- `+trigger:seen_by(a, b)` — B у полі зору / A дивиться на B (Boo; Head over Heels).
- `+effect:follow(a, b)` — A йде за B (міні-Маріо).
- `+window:bonus-game` — бонус-гра між рівнями.
- `+window:move-demo` — автодемонстрація руху перед рівнем.
- `+feature:retry-costs-life` — рестарт рівня коштує життя.
- `+feature:time-attack` — режим «пройди якнайшвидше» після кампанії.
- `+card:color-switch-blocks`, `+card:escort-followers`, `+card:two-phase-level`, `+card:followers-as-boss-hp`.

## Джерела
- ⭐ [Super Mario Wiki: Mario vs. Donkey Kong](https://www.mariowiki.com/Mario_vs._Donkey_Kong) — керування, повний список предметів, обʼєктів, ворогів, структура світів (6×8), таймер, міні-Маріо, бос, Plus/Expert, e-Reader.
- [Wikipedia: Mario vs. Donkey Kong](https://en.wikipedia.org/wiki/Mario_vs._Donkey_Kong_(video_game)) — 5 типів рівнів, зірки, ремейк 2024 (Casual/Classic, кооп з Тоадом, Time Attack, нові світи, >130 рівнів).
- YouTube: пошук «Mario vs Donkey Kong GBA gameplay».

## Непевне
- (?) Чи повертається кинутий ключ на місце через кілька секунд (памʼять, у відкритих джерелах не бачив).
- (?) Еталонний рахунок для зірки на кожному рівні й кількість зірок для кожного Expert-рівня.
- (?) Скільки життів на старті; ліміт часу рівнів (крім боса Plus: 120 с, DK Plus: 300 с).
- (?) Чи є окрема мапа світу (`world-map`) чи лише меню вибору.
- (?) Як саме міні-Маріо «йдуть за» Маріо: копіюють шлях чи рухаються в бік Маріо; що робить міні-Маріо, коли Маріо зупинився.
