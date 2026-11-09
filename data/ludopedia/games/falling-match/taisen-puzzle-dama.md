---
title: Taisen Puzzle-dama (対戦ぱずるだま)
slug: taisen-puzzle-dama
aka: [対戦ぱずるだま, Puzzle-dama, ぱずるだま, Taisen Puzzle-Dama]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1994
platforms: [arcade, PlayStation, Super Famicom, Saturn, N64, GBA, PS2, Windows, DS, 3DS, mobile]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/対戦ぱずるだま", best: true, note: "правила: поле 6×13, пари великих/малих куль, 3+ великих, мала стає великою від сусіднього лопання, атака, спецкулі, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Taisen_Puzzle-Dama", note: "серія; малі кулі «в коробках», дія білої/чорної/їдкої кулі, список ігор 1994–2011"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Taisen+Puzzle-dama+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, chain-reaction, combo-multiplier, ai-opponent, simultaneous-versus, garbage-attack, difficulty-levels, character-select, mode-select, game-screen, end-screen, +connected-group-pop, +cascade-gravity, +garbage-adjacent-convert, +eater-piece, +special-tiles, +garbage-queue-cap, +handicap-levels]
proposes: ["+cond:adjacent_cleared", "+feature:handicap", "+card:garbage-adjacent-convert", "+card:convert-adjacent-on-land", "+card:garbage-queue-cap"]
author: opus
date: 2026-11-09
---

# Taisen Puzzle-dama — Puyo-подібна дуель, де малі кулі самі не лопаються: їх «будить» лопання великої поруч

## Суть
Konami-варіант Puyo Puyo: зверху падають пари куль — **великих** (おおだま) і **малих** (こだま). Три й більше великих одного кольору, що торкаються по сторонах, лопаються. Малі кулі самі **ніколи** не зникають: вони стають великими свого кольору, коли поруч лопнула велика, — і тоді можуть утворити новий збіг. Атака супернику — це теж малі кулі, тож сміття тут не мертвий вантаж, а сировина для чужого ланцюга.

## Поле і час
- Поле 6 стовпців × 13 рядів (SFC «Tsuyoshi» — 6 × 12); два поля поруч — тільки дуель 1 на 1 (людина або CPU).
- Поразка — кулі заповнили верхню клітину точки появи (3-й стовпець зліва).
- Real-time падіння пари; після приземлення — осідання, лопання, осідання (каскад), потім падає атака суперника.
- 4 кольори великих куль: червоний, синій, жовтий, зелений.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пара куль | player | 2 кулі: велика/мала, кольори | зсув і обертання; після приземлення кулі падають окремо |
| Велика куля (おおだま) | tile | колір (4) | 3+ того ж кольору, звʼязані по вертикалі/горизонталі (у т. ч. Г-подібно), лопаються; діагональ не рахується |
| Мала куля (こだま) | tile | колір; у «коробці» | сама не лопається; сусіднє (по сторонах) лопання великої → стає великою свого кольору |
| Куля атаки (こうげきだま) | hazard | патерн персонажа | падає в поле суперника як мала куля |
| Біла куля (ぜんだま) | tile | — | одразу зникає; сусідні малі → великі |
| Чорна куля (あくだま) | hazard | — | одразу зникає; сусідні великі → малі |
| Їдка куля (くいだま) | tile | напрям | після приземлення йде вперед, поїдаючи малі кулі; стоп на краю чи великій кулі; стає великою кулею (кольору останньої зʼїденої) |
| Чарівна куля (まほうだま) | tile | різні ефекти | лише в «Mirmo de Pon!» (GBA), до 3 за бій |
| Точка появи (3-й стовпець, верх) | static | — | зайнята → поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(pair, down)`.
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(pair, dir)`.
- КОЛИ `input(rotate)` → ЯКЩО `free(new_cell)` → ТО `rotate(pair, ±90)`.
- КОЛИ `locked(pair)` → ТО `fall(each_ball)` окремо до опори.
- КОЛИ `pattern(group(3))` → ЯКЩО `same(big_balls, color)` and `connected(big_balls)` (4-сусідство) → ТО `clear(group)`.
- КОЛИ `after(clear)` → ЯКЩО `adjacent_count(cleared, small_ball, ≥, 1)` → ТО `transform(small_ball, big_ball)` того ж кольору.
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`; ЯКЩО `pattern(group(3))` → ТО `clear`, `combo(+1)` — ланцюг (нові великі з малих теж дають збіги).
- КОЛИ `custom: «каскад закінчився»` → ЯКЩО `chain(2)` або `custom: «6+ куль одночасно»` → ТО `send_garbage(attack_balls)` супернику за візерунком свого персонажа.
- КОЛИ `custom: «пара суперника приземлилась»` → ЯКЩО `count(incoming, >, 0)` → ТО `spawn_at(small_balls, top)`: до 24 за раз, решта — після наступної пари.
- КОЛИ `locked(white_ball)` → ТО `disappear`, `transform(adjacent_small, big)`.
- КОЛИ `locked(black_ball)` → ТО `disappear`, `transform(adjacent_big, small)`.
- КОЛИ `locked(eater_ball)` → ТО `custom: «рух уперед у своєму напрямку, поїдаючи малі кулі»`; ЯКЩО `blocked(eater_ball)` (край або велика куля) → ТО `transform(eater_ball, big_ball)`.
- КОЛИ `spawned(pair)` → ЯКЩО `occupied(spawn_cell)` → ТО `lose`; суперник — `win` раунду.
- Перемога: суперник переповнився. · Рахунок: у першій грі — лише перемоги раундів; систему очок додано в «Susume!» (1996).

## Керування і ввід
- ←/→ — зсув пари; ↓ — прискорене падіння (?); кнопки — поворот пари (за/проти годинникової) (?).
- Дві людини на одному автоматі/консолі — кожна своє поле; або проти CPU.
- Під час каскаду ввід, як у Puyo, ймовірно, вимкнено (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` / `mode-select`: сюжет проти CPU з босами · 1P проти CPU (3 складності) · тренування · режим для сильних гравців · 2P.
- `character-select` — персонажі (Penclaw, Mayu Sawada, Yumi-chan, Don Van Jiro…), у кожного свій візерунок атаки; боси (Tonosama).
- `match-setup` для 2P — 7 рівнів гандикапу.
- `game-screen`: два поля 6×13, `next-piece-preview` (?), лічильник ланцюга (`popup-text`) (?), `garbage-meter` вхідних куль (?).
- `end-screen` раунду → наступний суперник; `game-over-continue` в аркаді.

## Фічі поза полем
- `mode-versus`, `ai-opponent-levels` (3 складності), `mode-practice` (тренування), сюжетний режим з босами.
- `+feature:handicap` — 7 рівнів гандикапу для двох гравців.
- Серія — франшизні ремікси тих самих правил: персонажі Konami (TwinBee, Tokimeki Memorial, Castlevania), «Chibi Maruko-chan», «Mirmo de Pon!».

## Варіації й родичі
- Серія: аркада 1994 (Konami), PS «TwinBee Taisen Puzzle-dama» (1994), SFC «Tsuyoshi Shikkari Shinasai» (1994), «Tokimeki Memorial Taisen Puzzle-dama» (1995), «Susume! Taisen Puzzle-dama» (1996, боси й очки; N64 1998), «Pop'n Taisen Puzzle-dama Online» (PS2, 2004), «Castlevania Puzzle: Encore of the Night» (iOS, 2010), «Magical Academy» (2011, мобільна). Спін-оф «Taisen Toss-dama» — інша механіка.
- Родичі в корпусі: [Puyo Puyo](puyo-puyo.md) (сміття зникає від сусіднього лопання), [Super Puzzle Fighter II Turbo](super-puzzle-fighter-ii-turbo.md) (сміття-лічильник, що стає звичайним), [Panel de Pon](panel-de-pon.md) (сміття перетворюється на панелі), [Cosmo Gang the Puzzle](cosmo-gang-the-puzzle.md) (фігура-пожирач).
- **Осі варіацій**:
  - **що робить сусіднє лопання зі сміттям**: стирає (Puyo) / перетворює на звичайну кулю (Puzzle-dama, Panel de Pon);
  - **поріг групи**: 3 (Puzzle-dama) / 4 (Puyo);
  - **спецкулі**: поліпшити сусідів (біла) / погіршити (чорна) / рухатись і їсти (їдка);
  - **ліміт сміття за раз**: 30 (Puyo) / 24 (Puzzle-dama).

## Цікавинки для курсу
- Два стани кулі (велика/мала) і перетворення сусідів після лопання — ланцюг, що підживлюється сміттям — 📎.
- Біла/чорна кулі як «ауру» на сусідів після приземлення — 🌱.
- Їдка куля: рух у напрямку з поїданням до упору й перетворенням — 📎.
- Черга атаки з лімітом 24 за раз і переносом залишку — 🌱.
- Візерунок атаки за персонажем (таблиця стовпців/кольорів) — 🌱.
- CPU-суперник, що шукає ходи з перетворенням малих куль — 🥈.

## Мапа на каталог
- Є: `gravity-fall`; `multi-cell-size` ↔ пара; `keyboard-controls`; `chain-reaction` + `combo-multiplier` ↔ ланцюг; `ai-opponent` + `simultaneous-versus` ↔ дуель; `garbage-attack` ↔ кулі атаки; `difficulty-levels`; `character-select`; `mode-select`; `game-screen`; `end-screen`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` {min: 3, adjacency: 4}; `+cascade-gravity`; `+eater-piece` (Cosmo Gang) — тут {dir: facing, eats: small, ends: transform}; `+special-tiles` — уже в корпусі.
  - `+garbage-adjacent-convert` «Сміття стає звичайною плиткою від сусіднього збігу» · entities/interact · 🌱 — пара до `+garbage-adjacent-clear`.
  - `+convert-adjacent-on-land` «Спецплитка при приземленні перетворює сусідів (покращує/погіршує)» · entities/interact · 🌱.
  - `+garbage-queue-cap` «Ліміт сміття за раз, залишок — наступним ходом» · game-logic/opponent · 🌱 · слот {cap: 24}.
  - `+handicap-levels` «Гандикап для гравців у versus» · game-logic/opponent · 🌱 · слот {levels: 7}.

## Пропозиції до словників
- `+cond:adjacent_cleared` — поруч (по сторонах) щойно лопнула група (Puyo-сміття, Puzzle-dama).
- `+feature:handicap` — гандикап у versus (7 рівнів).
- `+card:garbage-adjacent-convert`, `+card:convert-adjacent-on-land`, `+card:garbage-queue-cap` — див. «Мапа на каталог».
- `send_garbage` і `locked` уже ⏳ у словниках — у реченнях вжито без пропозиції.

## Джерела
- ⭐ [Wikipedia JA: 対戦ぱずるだま](https://ja.wikipedia.org/wiki/対戦ぱずるだま) — поле 6×13 (SFC 6×12), клітина поразки, пари おおだま/こだま, 3+ без діагоналей, перетворення малих, атака (ланцюг або 6+, до 24 за раз, візерунок персонажа), ぜんだま/あくだま/くいだま/まほうだま, режими, гандикап 7, сиквели.
- [Wikipedia EN: Taisen Puzzle-Dama](https://en.wikipedia.org/wiki/Taisen_Puzzle-Dama) — малі кулі в «коробках», біла/чорна при приземленні, їдка куля — напрям, стоп на краю/великій, остання зʼїдена стає великою; список ігор.
- YouTube: пошук «Taisen Puzzle-dama gameplay».

## Непевне
- (?) Кнопки й наявність прискореного падіння, next-preview, лічильника ланцюга й індикатора вхідних куль — джерела не описують.
- (?) Їдка куля: JA — «сама стає великою кулею відповідного кольору», EN — «остання зʼїдена мала стає великою»; беру спільне — результат велика куля.
- (?) Поріг атаки «ланцюг» — з якого кроку (2-й?) і формула кількості куль атаки — не знайдено.
- (?) Колір їдкої кулі: JA — рожева, EN — фіолетова.
- (?) Чи пара може складатись з двох малих куль і як часто падають спецкулі.
