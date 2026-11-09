---
title: Puzzle Bobble / Snood / Frozen Bubble
slug: puzzle-bobble
aka: [Bust-a-Move, Bubble Buster, Snood, Frozen Bubble, bubble shooter]
family: falling-match
also: []
klass: avatar
axes:
  field: hex
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1994
platforms: [arcade, SNES, Neo Geo CD, Game Gear, 3DO, PC, PSP, iOS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Bobble", best: true, note: "правила оригіналу: прицілювання, рикошет, 3+ зникають, обвал підвішених, стеля, автопостріл"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Bobble_2", note: "турнір versus проти CPU, розгалужена мапа, Another World, time trial"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Snood_(video_game)", note: "Danger Meter, спецснуди: Numbskull, Stone, Wildcard, Rowbuilder"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frozen_Bubble", note: "вільний клон (GPL): 100 рівнів, редактор, мережа 2–5, опція chain reaction"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzle+bobble+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [projectile-shot, gravity-fall, connectivity-check, chain-reaction, next-queue, event-points, sequential-levels, simultaneous-versus, garbage-attack, ai-opponent, in-game-editor, online-multiplayer, score-records, game-over-continue, level-select, time-bonus, +wall-bounce-shot, +hex-snap, +hanging-drop, +descending-ceiling, +danger-meter, +wildcard-tile, +auto-fire]
proposes: ["+effect:snap", "+ui:danger-meter", "+ui:aim-guide", "+feature:auto-fire"]
author: opus
date: 2026-11-09
---

# Puzzle Bobble — стріляєш кульками під кутом з рикошетом; 3+ одного кольору лопаються, відірвані від стелі падають

## Суть
Зі стелі звисає купа кольорових кульок, щільно упакованих (гекс). Гравець внизу крутить стрілку-пускач і стріляє кулькою: вона летить прямо, відбивається від бічних стін і прилипає там, де торкнулась. Якщо утворилась звʼязана група 3+ одного кольору — вона лопається, а все, що після цього більше не тримається за стелю, падає (головне джерело очок). Кожні кілька пострілів стеля опускається; кулька за нижньою лінією — програш. Мета рівня — очистити поле.

## Поле і час
- Вузька «колба»: гексагональна упаковка (ряди зсунуті на пів кульки), стеля зверху, нижня лінія програшу; пускач у центрі внизу.
- Real-time: політ кульки фізичний (пряма + дзеркальні відбиття від стін), але решта поля статична між пострілами; тиск — стеля, що опускається за кількістю пострілів, і автопостріл при бездіяльності.
- Versus — два поля поруч; Frozen Bubble — до 5 полів у мережі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пускач (стрілка) | player | кут | обертається ліворуч/праворуч; стріляє поточною кулькою |
| Летюча кулька | projectile | колір, напрям | летить прямо; від бічної стіни — відбиття; торкнулась кульки/стелі → прилипає |
| Кулька на полі | tile | колір | у гекс-клітині; група 3+ одного кольору лопається; без звʼязку зі стелею — падає |
| Стеля | static | позиція | опускається на ряд кожні кілька пострілів; тягне всі кульки з собою |
| Нижня лінія | static | — | кулька за нею → програш |
| Наступна кулька | spawner | колір | колір випадковий з тих, що ще є на полі |
| Numbskull (Snood) | hazard | — | не стріляється; лише з Wildcard; треба відрізати й скинути |
| Stone (Snood) | object | — | вибиває сусідні снуди там, де впав |
| Wildcard (Snood) | tile | — | замінює будь-який колір; зʼєднав кілька наборів — зникають усі; ні з чим — падає |
| Rowbuilder (Snood) | tile | — | заповнює один горизонтальний ряд звичайними снудами |
| Danger Meter (Snood) | mark | рівень | росте з кожним пострілом; повний → усе на рівень нижче; знищення снудів зменшує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(aim_left|aim_right)` → ТО `rotate(launcher, ±deg)` у межах дозволеного кута (?).
- КОЛИ `input(fire)` → ТО `throw(bubble, angle)`, `custom: «наступна кулька стає поточною; нова — колір з наявних на полі»`.
- КОЛИ `idle(n)` → ТО `throw(bubble, angle)` — автопостріл.
- КОЛИ `tick` → ТО `move(bubble, dir)`; КОЛИ `contact(bubble, side_wall)` → ТО `bounce(bubble)`.
- КОЛИ `contact(bubble, field_bubble)` or `reach(bubble, ceiling)` → ТО `custom: «snap — прилипає в найближчу вільну гекс-клітину»`, `attach(bubble, field)`.
- КОЛИ `pattern(group(3+, same_color, adj6))` → ТО `clear(group)`, `score(n)`.
- КОЛИ `after(clear)` → ЯКЩО `not connected(bubble, ceiling)` → ТО `fall(bubble)`, `score(n)` (за кожну впалу — більше, ніж за лопнуту (?)).
- КОЛИ `counter(shots, >=, k)` → ТО `shift(all, down)` — стеля на ряд нижче; `k` залежить від кількості кольорів на полі.
- КОЛИ `reach(bubble, bottom_line)` → ТО `lose` (аркада: `game-over-continue`).
- КОЛИ `all_gone(bubble)` → ТО `win`, `next_level`; бонус за швидкість (?).
- Snood: КОЛИ `input(fire)` → ТО `counter(danger, +1)`; КОЛИ `counter(danger, ==, max)` → ТО `shift(all, down)`; КОЛИ `after(clear)` → ТО `counter(danger, -n)`.
- Snood: КОЛИ `custom: «Wildcard прилип»` → ЯКЩО `custom: «торкається кількох наборів»` → ТО `clear(all_sets)`; ЯКЩО жодного → ТО `fall(wildcard)`.
- Snood: КОЛИ `custom: «Stone прилип»` → ТО `clear(adjacent)`; КОЛИ `custom: «Rowbuilder прилип»` → ТО `spawn_at(regular_snoods, row)`.
- Snood: КОЛИ `reach(snood, bottom)` → ТО `lives(-1)`, усі снуди → Numbskull.
- Versus: КОЛИ `after(fall)` → ТО `send_garbage(n)` супернику (кульки додаються до його поля) (?).
- Frozen Bubble (опція chain reaction): КОЛИ `after(fall)` → ЯКЩО `custom: «впала кулька може добудувати трійку»` → ТО `custom: «злітає назад угору й прилипає»`, `combo(+1)`.

## Керування і ввід
- Аркада: ←/→ — поворот стрілки, кнопка — постріл. Часто — тримання для плавного повороту.
- Мишка/тач у клонах (Snood, Frozen Bubble, мобільні): навести/торкнутись — постріл у точку.
- Рикошетні («банкові») постріли — ключова навичка: ціль за кутом через стіну.

## Вікна, меню, HUD
- `attract-demo` і `splash-screen` (аркада) → `main-menu`: 1P Puzzle · 2P Versus · (PB2) VS CPU турнір · Time Attack · Options.
- `game-screen`: колба з кульками, пускач, поточна й наступна кулька (`next-tile-preview`), `score`, `level-number`, `danger-line`; у Snood — `custom: «danger-meter»`; у пізніх клонах — `custom: «aim-guide»` (прицільна лінія з рикошетом).
- `map-window` — розгалужена мапа рівнів (PB2: вибір однієї з двох груп по 5 рівнів).
- `level-password` / код «Another World» (PB2) — розблокування складніших рівнів.
- `end-screen` (рівень пройдено / Game Over), `game-over-continue`, `leaderboard`.
- Frozen Bubble: `editor-window`, `lobby-window` (мережа), `settings-window` (колірна палітра/звук).

## Фічі поза полем
- `levels-sequential` (30 рівнів аркади; 100 у Frozen Bubble), розгалуження маршруту (PB2).
- `mode-versus` + `ai-opponent-levels` (турнір проти CPU-персонажів), `local-multiplayer`, `online-multiplayer` (Frozen Bubble 2.0: LAN/інтернет, 2–5 гравців).
- `mode-time-attack` (PB2 PlayStation; Snood Time Attack — єдиний режим з таймером).
- `level-editor` (Frozen Bubble), налаштування частоти спецснудів (зареєстрований Snood).
- Музика пришвидшується, коли кульки близько до лінії.

## Варіації й родичі
- Bubble Bobble (1986) — джерело персонажів. Puzzle Bobble 2–4, Bust-a-Move DS/Universe, Everybubble! (2023).
- Snood (1996, Dave Dobson) — Danger Meter замість лічильника пострілів, спецснуди. Frozen Bubble (2002, GPL) — вільний клон з редактором і мережею.
- Родичі: Zuma / Puzz Loop (постріл у ланцюг на кривій), Magical Drop (вертикальний «постріл» без рикошету), Puyo Puyo (групи й гравітація).
- **Осі варіацій**: тиск (стеля за пострілами / Danger Meter / таймер) · сусідство (гекс-6 / квадрат) · траєкторія (пряма з рикошетом / гравітація) · обвал (без звʼязку зі стелею падає / не падає) · спецкульки (wildcard, камінь, незнищенні) · versus (сміття за впалі / нема).

## Цікавинки для курсу
- Політ кульки з відбиттям від стін і пошук першого зіткнення з колами — 🥉.
- «Snap» вільної позиції у найближчу клітину гекс-сітки (зсунуті ряди) — 📎.
- Обвал підвішених: BFS від стелі, усе непосяжне — падає — 📎.
- Стеля, що опускається за пострілами / Danger Meter — 🌱.
- Колір наступної кульки лише з наявних на полі — 🌱.
- Прицільна лінія з передбаченням рикошету — 📎.
- Versus зі сміттям за впалі кульки — 🥉.

## Мапа на каталог
- Є: `projectile-shot` · `gravity-fall` (обвал) · `connectivity-check` (звʼязок зі стелею) · `chain-reaction` (Frozen Bubble) · `next-queue` · `event-points` · `sequential-levels` · `simultaneous-versus` · `garbage-attack` · `ai-opponent` · `in-game-editor` · `online-multiplayer` · `score-records` · `game-over-continue` · `level-select` · `time-bonus`.
- **Нема** → пропозиції карток:
  - `+wall-bounce-shot` «Постріл з рикошетом від стін» · entities/combat · 📎.
  - `+hex-snap` «Прилипання до гекс-сітки» · entities/move · 📎.
  - `+hanging-drop` «Відірване від опори падає» · entities/interact · 📎 · слоти {anchor: ceiling|floor}.
  - `+descending-ceiling` «Стеля опускається за лічильником» · game-logic/waves · 🌱 · слоти {every_n_shots}.
  - `+danger-meter` «Шкала небезпеки росте з ходами» · interface/hud · 🌱.
  - `+wildcard-tile` «Плитка-джокер підходить до будь-якого кольору» · entities/legality · 🌱.
  - `+auto-fire` «Автохід при бездіяльності» · game-logic/turns · 🌱.

## Пропозиції до словників
- `+effect:snap` — сутність з вільними координатами прилипає до найближчої вільної клітини сітки (bubble shooter).
- `+ui:danger-meter` — шкала, що росте з кожним ходом і при заповненні запускає штраф (Snood).
- `+ui:aim-guide` — прицільна лінія з передбаченням відбиттів (ширше за `path-preview`: траєкторія снаряда).
- `+feature:auto-fire` — гра сама робить хід після N секунд бездіяльності.

## Джерела
- ⭐ [Wikipedia: Puzzle Bobble](https://en.wikipedia.org/wiki/Puzzle_Bobble) — прицілювання, рикошет, прилипання, 3+ зникають, обвал, стеля за пострілами (інтервал залежить від кольорів), лінія програшу, автопостріл, 30 рівнів, Taito 1994.
- [Wikipedia: Puzzle Bobble 2](https://en.wikipedia.org/wiki/Puzzle_Bobble_2) — турнір VS CPU, розгалужена мапа, Another World, time trial.
- [Wikipedia: Snood](https://en.wikipedia.org/wiki/Snood_(video_game)) — Danger Meter, Numbskull/Stone/Wildcard/Rowbuilder, втрата життя, Time Attack.
- [Wikipedia: Frozen Bubble](https://en.wikipedia.org/wiki/Frozen_Bubble) — 100 рівнів, редактор, мережа 2–5, chain reaction з v2.0, GPL.

## Непевне
- (?) Очки за впалі кульки (подвоєння за кожну наступну) — з памʼяті, Wikipedia не уточнює.
- (?) Сміття у versus (впалі кульки летять супернику) — з памʼяті; статті не описують.
- (?) Спецкульки Puzzle Bobble 2+ (райдужна, зірка, металева) — не підтверджено.
- (?) Межі кута пускача, превʼю наступної кульки в оригіналі 1994 — не перевірено.
- (?) Офіційний сайт Frozen Bubble нині редиректить на сторонній ресурс — у лінки не клав.
