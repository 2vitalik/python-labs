---
title: SILO 7
slug: silo-7
aka: [Silo 7]
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: itch, url: "https://lythande.itch.io/silo-7", best: true, note: "опис: Boulder Dash-правила в ядерній шахті, паливні комірки → люк, монітори падають, RECYCLER з 20-с вікном, 40 секторів, 3 ворота, керування, 3 життя, бонус за час"}
  - {kind: other, url: "https://lythande.itch.io/silo-7/devlog/1697535/silo-7-is-live", note: "devlog: світлячки й метелики, 40 секторів ORIENTATION → LAST CIRCUIT, 3 ворота, HUD таймера vs панелі RECYCLER"}
  - {kind: other, url: "https://lythande.itch.io/silo-7/devlog/1667381/the-silo-7-demo-is-out", note: "devlog демо: вікно 20 с після першого монітора, фінал 45 → 80 с, вибір рівня з 1–3 зірками в наступному оновленні"}
  - {kind: other, url: "https://lythande.itch.io/silo-7/devlog/1601050/devlog-post-jam-note", note: "devlog: GMTK Game Jam 2026, тема COUNT DOWN"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SILO+7+lythande+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, dig-terrain, push-object, gravity-fall, collect-quota, reach-exit, time-out, time-bonus, touch-death, player-death, enemy-patrol, restart-level, sequential-levels, level-select, score-records, movement-animation, event-effects, sound-warnings, tutorial-window, game-pause, volume-control, language-picker, +recycler-conversion, +timing-window, +retry-costs-life, +progression-gates, +practice-continue]
proposes: ["+effect:convert", "+ui:window-timer", "+feature:practice-continue", "+card:recycler-conversion", "+card:retry-costs-life"]
author: opus
date: 2026-11-09
---

# SILO 7 — Boulder Dash під відліком: збери паливні комірки, не потрап під монітори й вибирайся з шахти до нуля

## Суть
Аркадний пазл за правилами Boulder Dash у ядерній шахті, що от-от вибухне. Науковець копає землю, збирає квоту паливних комірок, щоб відімкнути аварійний люк, і вилазить, поки відлік не дійшов нуля. Замість каменів — CRT-монітори («ШІ, що падає на тебе»): вони падають у порожнечу, їх можна штовхати вбік. Нова механіка — RECYCLER: монітори, скинуті в машину протягом 20-секундного вікна, перетворюються на додаткові комірки.

## Поле і час
- Квадратна сітка, вид збоку; сектор займає один екран у рамці сталевих стін (зі скриншотів).
- Real-time з плавним рухом «від клітини до клітини» для героя, моніторів і комірок.
- Відлік сектора T-mm:ss — головний тиск; в останні секунди червона пульсація й трясіння екрана. Фінал — довший відлік (45 → 80 с у devlog-у).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Науковець | player | 3 життя на забіг | рух 4 напрямки, копає землю, штовхає монітори вбік |
| Земля | terrain | — | прокопується в порожнечу |
| Сталева стіна | static | — | непрохідна, не копається |
| Монітор (CRT) | object | — | падає в порожнечу за BD-правилами; штовхається вбік; може падати стосом |
| Паливна комірка | pickup | квота на сектор | лічильник CELLS x / N; рухається клітинами (?) |
| Аварійний люк | gate | закритий / відкритий | відкривається після квоти; вихід із сектора |
| RECYCLER | sink | вікно 20 с | монітор, що потрапив у машину, → додаткова комірка |
| Світлячок | enemy | — | патрулює; змушує вчасно копати |
| Метелик | enemy | — | патрулює (інший тип маршруту (?)) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(next, dirt|empty)` → ТО `move(scientist, dir)`; земля → `set_cell(next, empty)`.
- КОЛИ `contact(scientist, monitor)` по горизонталі → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(monitor)`; стос моніторів падає разом, коли зникає опора.
- КОЛИ `contact(falling monitor, scientist)` → ТО `lives(-1)`, `restart` (?).
- КОЛИ `contact(scientist, enemy)` → ТО `lives(-1)`, `restart` (?).
- КОЛИ `tick` → ТО `custom: «світлячок і метелик ходять своїми маршрутами»` (BD-логіка вздовж стін — (?)).
- КОЛИ `contact(scientist, fuel_cell)` → ТО `pickup`, `counter(cells, +1)`.
- КОЛИ `counter(cells, >=, quota)` → ТО `set_state(hatch, open)`.
- КОЛИ `contact(scientist, hatch)` → ЯКЩО `state(hatch, open)` → ТО `win`, `score(time_left)`, `next_level`.
- КОЛИ `enter(monitor, recycler)` → ЯКЩО `first_time` → ТО `timer(start, 20)`, `custom: «монітор → додаткова комірка»`.
- КОЛИ `enter(monitor, recycler)` → ЯКЩО `timer(>, 0)` → ТО `custom: «монітор → додаткова комірка»`, `counter(cells, +1)` (?); після вікна — переробки нема (?).
- КОЛИ `tick` → ЯКЩО `timer(<=, last_seconds)` → ТО `flash`, `shake` — червона пульсація й трясіння.
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` — спроба сектора закінчена.
- КОЛИ `input(R)` → ТО `restart`, `lives(-1)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over` (?).
- Перемога (сектор): квота комірок + вихід через люк до нуля. · Поразка: монітор зверху, ворог, нуль на відліку → −життя. · Рахунок: бонус за кожну збережену секунду; найкращий рахунок повного забігу.

## Керування і ввід
- Стрілки — рух / копання / штовхання моніторів убік.
- Enter — підтвердити; Esc — пауза; R — переграти сектор (коштує життя); F11 — повний екран.

## Вікна, меню, HUD
- `game-screen`: сектор; HUD — `lives` (3 квадрати), позначка режиму PRACTICE, `remaining-counter` CELLS x / N, `timer-countdown` T-mm:ss зі смугою, назва сектора, `score`; на секторах з переробником — панель RECYCLER із власним відліком вікна (`window-timer`).
- `tutorial-window`: ілюстроване пояснення перед сектором з RECYCLER і перед фіналом.
- `pause-menu` (Esc).
- `end-screen`: рахунок забігу; кінцевий ролик з чотирьох сцен (`custom-window`).
- `level-select` з найкращим часом і 1–3 зірками — заявлено на наступне оновлення (?).
- `settings-window`: мова EN / IT / FR, окремі гучності музики й ефектів, повний екран.
- Переходи: main-menu (?) → game-screen → (люк) наступний сектор / (нуль) повтор сектора → … → кінцевий ролик.

## Фічі поза полем
- `levels-sequential`: 40 секторів, кожен про одну задачу (почекати падіння, обрати маршрут, штовхати монітори, стоси, що падають разом, таймінг патрулів, «майстерні» сетапи); три ворота прогресу на шляху вниз.
- 3 життя на забіг; R коштує життя; найкращий рахунок повного забігу; час рівнів демо переноситься в повну гру.
- Continue — продовжити з найвищого сектора як тренування (PRACTICE).
- Демо — перші 10 секторів; джем-версія — коротша.
- `localization` (EN / IT / FR), `volume-sliders`, `fullscreen`.

## Варіації й родичі
- У сімʼї: [boulder-dash](boulder-dash.md) (квота → вихід → таймер, світлячки й метелики, бонус за час), [supaplex](supaplex.md), [emerald-mine](emerald-mine.md), [dome-keeper](dome-keeper.md) (копання під відліком), [diamond-rush](diamond-rush.md).
- **Осі варіацій**: що падає — камінь (BD) / монітор (SILO 7); падаючий обʼєкт — лише загроза (BD) / ресурс, який можна переробити (SILO 7); таймер — фон (BD) / головна тема з візуальною тривогою (SILO 7).

## Цікавинки для курсу
- RECYCLER: перший скинутий монітор запускає 20-секундне вікно, у ньому кожен монітор → комірка — 📎.
- Квота + люк + відлік з бонусом за залишок часу — 🌱.
- Рестарт сектора за ціну життя (R) — 🌱.
- Стос моніторів, що падає разом після прибирання опори (порядок обходу при падінні) — 🥉.
- Червона пульсація й трясіння в останні секунди — 🌱.
- Режим Continue/Practice з найвищого сектора — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `dig-terrain` ↔ земля; `push-object` ↔ монітори вбік; `gravity-fall` ↔ монітори; `collect-quota` + `reach-exit` ↔ комірки й люк; `time-out` + `time-bonus` ↔ відлік і бонус; `touch-death` + `player-death` ↔ життя; `enemy-patrol` ↔ світлячки й метелики; `restart-level` ↔ R; `sequential-levels` ↔ 40 секторів; `level-select` ↔ заявлений вибір рівня; `score-records` ↔ найкращий забіг; `movement-animation` ↔ плавний рух; `event-effects` + `sound-warnings` ↔ пульсація й трясіння; `tutorial-window` ↔ пояснення; `game-pause`, `volume-control`, `language-picker`.
- Повтори з корпусу: `+timing-window` (вікно переробника).
- **Нема** → пропозиції карток:
  - `+recycler-conversion` «Переробник: загрозливий обʼєкт → ресурс у часовому вікні» · entities/interact · 📎 · слоти {window: 20, from: monitor, to: fuel_cell}.
  - `+retry-costs-life` «Рестарт рівня коштує життя» · game-logic/lose · 🌱.
  - `+progression-gates` «Ворота між блоками рівнів» · levels/progression · 🌱 (?).
  - `+practice-continue` «Продовжити з найвищого рівня як тренування» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:convert` — обʼєкт одного виду → ресурс іншого (повтор з корпусу).
- `+ui:window-timer` — окрема смуга відліку часового вікна механіки (RECYCLER 17s) поруч з головним таймером.
- `+feature:practice-continue` — продовжити з найвищого досягнутого сектора як тренування (не `mode-practice`: доступ лише до вже пройденого максимуму).
- `+card:recycler-conversion`, `+card:retry-costs-life` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: SILO 7](https://lythande.itch.io/silo-7) — опис, мета, монітори, RECYCLER і 20-с вікно, 40 секторів і їхні задачі, 3 ворота, керування, 3 життя, бонус за час, Continue, мови, скриншоти HUD.
- [Devlog: SILO 7 is live](https://lythande.itch.io/silo-7/devlog/1697535/silo-7-is-live) — світлячки й метелики, сектори ORIENTATION → LAST CIRCUIT, ворота, HUD.
- [Devlog: демо](https://lythande.itch.io/silo-7/devlog/1667381/the-silo-7-demo-is-out) — вікно після першого монітора, фінал 45 → 80 с, «чекати падіння», стоси, зірки в наступному оновленні.
- [Devlog: post-jam note](https://lythande.itch.io/silo-7/devlog/1601050/devlog-post-jam-note) — GMTK Game Jam 2026, тема COUNT DOWN.
- YouTube: пошук «SILO 7 lythande gameplay».

## Непевне
- (?) Чи монітори скочуються з «круглих» обʼєктів, як камені BD; чи є окремі валуни (тег «falling boulders» — можливо, про ті ж монітори).
- (?) Маршрути світлячків і метеликів (BD-обхід стін?) і чи вбиває дотик; чи комірки падають, як алмази BD.
- (?) Що відбувається після закінчення 20-с вікна переробника; скільки комірок дає один монітор.
- (?) Чи нуль на відліку забирає життя, як R; що буде при 0 життів.
- (?) Розміри секторів; чи камера скролить великі сектори.
