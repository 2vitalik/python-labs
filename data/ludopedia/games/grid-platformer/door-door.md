---
title: Door Door
slug: door-door
aka: [ドアドア, Doa Doa, Door Door mkII]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1983
platforms: [PC-8801, PC-8001mkII, PC-6001, PC-9801, Sharp MZ-2000, Sharp X1, FM-7, FM-77, Pasopia 7, Hitachi S1, MSX, Famicom, mobile (2004)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Door_Door", best: true, note: "двері з ручкою, чотири прибульці з різним переслідуванням, бомби й цвяхи, бонус за кількох за одними дверима, приклади рівнів-задач"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Door+Door+Famicom+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, gravity-fall, ladder-climb, chase-player, chase-greedy, touch-death, player-death, item-pickup, timed-despawn, event-points, escalating-kill-points, extra-life-threshold, sequential-levels, keep-playing-after-win, status-panel, game-screen, +trap-behind-door, +door-handle-side, +enemy-shadows-jump, +roundabout-chaser, +sacrifice-life-reset]
proposes: ["+trigger:all_trapped", "+cond:from_side(a, door, side)", "+effect:close_door(door)", "+role:door", "+card:trap-behind-door", "+card:door-handle-side", "+card:enemy-shadows-jump"]
author: opus
date: 2026-11-09
---

# Door Door — Чун заманює прибульців за розсувні двері на поверхах із драбинами й зачиняє їх, поки ті не вибігли

## Суть
Однокадрова головоломка-платформер Коїті Накамури (Enix, 1983; від імені героя пізніше названо Chunsoft). Чун бігає поверхами, лазить драбинами й стрибає; за ним женуться прибульці, кожен зі своїм правилом погоні. Зброї нема: треба **відчинити двері з боку ручки, заманити прибульця всередину й зачинити**. За кількох прибульців за одними дверима — більше очок, тож рівень — це задача про те, як зібрати переслідувачів у купу.

## Поле і час
- Один нескролений екран: платформи-поверхи, звʼязані драбинами; на поверхах — двері, кожна з ручкою з одного боку.
- Real-time; прибульці рухаються за власними правилами; бомби, цвяхи й солодощі зʼявляються й зникають з часом.
- Двері мають стан: зачинені / відчинені / зачинені з полоненими (назавжди).
- Після останнього рівня гра йде з рівня 1 зі збереженим рахунком; кінця нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чун | player | 3 життя; +1 на 10 000, далі кожні 20 000 | біг, стрибок, лазіння драбинами; відчиняє й зачиняє двері |
| Платформа-поверх | terrain | — | опора |
| Драбина | terrain | — | рух між поверхами |
| Двері | gate | бік ручки; стан | відчиняються пробіжкою з боку ручки; зачинені з прибульцем не відчиняються більше |
| Намегон (Namegon) | enemy | — | найпряміший шлях до Чуна |
| Амечан (Amechan) | enemy | — | теж найпряміший шлях до Чуна |
| Інвекун (Invekun) | enemy | — | обхідні маршрути драбинами |
| Отапйон (Otapyon) | enemy | — | повторює стрибки Чуна |
| Бомба | hazard | зʼявляється | дотик — смерть |
| Цвях | hazard | зʼявляється | дотик — смерть |
| Солодощі (льодяник, ескімо, торт, морозиво, плитка маджонгу…) | pickup | зʼявляються і зникають | бонусні очки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(chun, dir)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` → ТО `move(chun, dir)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок»`; КОЛИ `custom: «Чун стрибнув»` → ТО `custom: «Отапйон теж стрибає»`.
- КОЛИ `tick` → ЯКЩО `not supported(a)` → ТО `fall(a)` (?).
- КОЛИ `contact(chun, door)` → ЯКЩО `custom: «Чун біжить з боку ручки»` і `state(door, closed)` → ТО `set_state(door, open)`.
- КОЛИ `contact(alien, door)` → ЯКЩО `state(door, open)` → ТО `set_state(alien, inside)` — прибулець забігає за двері.
- КОЛИ `custom: «Чун зачиняє двері»` → ЯКЩО `occupied(door, alien)` → ТО `set_state(door, sealed)`, `score(n × k)` — більше за кількох одразу.
- КОЛИ `contact(chun, door)` → ЯКЩО `state(door, sealed)` → ТО `block` — двері з полоненими більше не відчинити.
- КОЛИ `tick` → ЯКЩО `state(alien, inside)` і `state(door, open)` → ТО `custom: «прибулець вибігає назад»` (?) — зачинити треба вчасно.
- КОЛИ `tick` → ТО `custom: «Намегон і Амечан — найкоротший шлях до Чуна»`; `custom: «Інвекун — обхід драбинами»`.
- КОЛИ `contact(chun, alien)` → ЯКЩО `not state(alien, inside)` → ТО `lose`, `lives(-1)`.
- КОЛИ `contact(chun, bomb)` або `contact(chun, nail)` → ТО `lose`, `lives(-1)`.
- КОЛИ `rng(p)` → ТО `spawn_at(sweet, where)`; через час `disappear_a`.
- КОЛИ `contact(chun, sweet)` → ТО `pickup`, `score(n)`.
- КОЛИ `died(chun)` → ЯКЩО `counter(lives, >, 0)` → ТО `restart` — полонені прибульці зникають з рівня, усі двері знову доступні.
- КОЛИ `custom: «усіх прибульців зачинено»` → ТО `next_level`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over` — назад на рівень 1.
- КОЛИ `counter(score, >=, 10000)` → ТО `lives(+1)`; далі — кожні 20 000.
- Перемога рівня: усі прибульці за дверима · Поразка: дотик прибульця, бомби чи цвяха · Рахунок: зачинені прибульці (бонус за групу) + солодощі.

## Керування і ввід
- Рух ліво/право, вгору/вниз драбиною, кнопка стрибка (Famicom — хрестовина + кнопка (?)).
- Двері — без окремої кнопки: відчиняються пробіжкою через них з боку ручки.

## Вікна, меню, HUD
- `game-screen`: поле-екран; HUD — `score`, `hi-score`, `level-number`, `lives`.
- `splash-screen` / `main-menu` (?) — старт гри.
- Door Door mkII: вибір старту з рівня 51 (`level-select` з двох точок).
- Переходи: рівень → (усі прибульці зачинені) наступний; смерть → рестарт рівня; життя скінчились → рівень 1.

## Фічі поза полем
- `levels-sequential` з циклом по колу зі збереженим рахунком.
- Door Door mkII (1985) — 100 рівнів, старт з 51-го.

## Варіації й родичі
- Door Door mkII (1985, PC-порти й MSX) — новий набір рівнів.
- Родичі в сімʼї: [space-panic](space-panic.md) (ловити ворогів у пастку замість стрілянини), [lode-runner](lode-runner.md) (вороги падають у ями), [kickle-cubicle](kickle-cubicle.md) (ворог стає частиною рішення), [mario-and-wario](mario-and-wario.md).
- Поза сімʼєю: Pac-Man (`maze-arcade`) — різні правила погоні в кожного ворога.
- Осі: **як знешкодити ворога** (яма / двері / заморозка / ніяк); **правило погоні** (жадібне / обхідне / дзеркалить гравця); **що лишається після смерті** (прогрес зберігається / рівень з нуля / полонені зникають).

## Цікавинки для курсу
- Двері з ручкою: відчинити можна лише з одного боку, зачинені з полоненим — назавжди — 📎.
- Бонус за групу: кілька ворогів за одними дверима множать очки — 🌱.
- Чотири правила погоні: жадібне, обхідне драбинами, «повторює стрибки» — 🥉 (Pac-Man-ідея на платформах з гравітацією).
- Рівні-задачі, де треба навмисно відпустити ворога, щоб звести двох разом (рівень 10) — 🥉 як дизайн рівня.
- Смерть як свідомий рестарт: рівень можна зробити непрохідним, вихід — втратити життя — 🌱 (стан «нерозвʼязний» без undo).
- Тимчасові бонусні предмети з появою за таймером — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `ladder-climb` · `chase-player` · `chase-greedy` (Намегон, Амечан) · `touch-death` · `player-death` · `item-pickup` (солодощі) · `timed-despawn` (солодощі, бомби) · `event-points` · `escalating-kill-points` (кілька за одними дверима) · `extra-life-threshold` · `sequential-levels` · `keep-playing-after-win` (цикл з рахунком) · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+trap-behind-door` «Заманити ворога за двері й зачинити» · entities/interact · 📎 · слот {reopenable}.
  - `+door-handle-side` «Двері відчиняються лише з одного боку» · entities/legality · 🌱.
  - `+enemy-shadows-jump` «Ворог повторює дії гравця» · entities/move · 🌱.
  - `+roundabout-chaser` «Ворог іде обхідним маршрутом» · entities/move · 📎.
  - `+sacrifice-life-reset` «Втрата життя як скидання непрохідного рівня» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+trigger:all_trapped(kind)` — усі вороги виду знешкоджені (не знищені: лишаються на полі за дверима).
- `+cond:from_side(a, door, side)` — сутність підходить до обʼєкта з певного боку.
- `+effect:close_door(door)` — зачинити двері, запечатавши тих, хто всередині.
- `+role:door` — двері зі станом і боком (або `gate` з параметром «бік ручки»).
- `+card:trap-behind-door`, `+card:door-handle-side`, `+card:enemy-shadows-jump` — див. вище.

## Джерела
- ⭐ [Wikipedia: Door Door](https://en.wikipedia.org/wiki/Door_Door) — Чун, драбини, чотири прибульці з різними правилами погоні, двері з ручкою, зачинені з полоненими не відчиняються, бомби й цвяхи, солодощі, бонус за групу, 3 життя, +1 на 10 000 і кожні 20 000, рестарт рівня зі зникненням полонених, цикл без фіналу, mkII зі 100 рівнями, порти.
- YouTube: пошук «Door Door Famicom gameplay».

## Непевне
- (?) Як саме зачиняються двері (пробіжка назад, окрема дія, автоматично) — Wikipedia: «shut the door before it escapes».
- (?) Чи прибулець сам вибігає з відчинених дверей і за скільки часу.
- (?) Кількість рівнів оригіналу (mkII — 100); очки за прибульця, групу й солодощі.
- (?) Гравітація для прибульців (падіння з поверху) і висота стрибка Чуна.
- (?) Як працює «рестарт»: полонені «зникають» — тобто зараховані й прибрані, чи рівень з нуля.
- (?) Назва четвертого прибульця «Amechan» — за англійською Вікіпедією; в інших джерелах склад ворогів може відрізнятись.
- (?) Меню й вибір складності у версіях — не знайдено.
