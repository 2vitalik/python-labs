---
title: Puyo Puyo (Пуйо Пуйо)
slug: puyo-puyo
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
year: 1991
platforms: [MSX2, Famicom Disk System, arcade, Mega Drive, Super Famicom, PC, Switch, PS4, Steam]
links:
  - {kind: fandom, url: "https://puyonexus.com/wiki/Basic_rules", best: true, note: "Puyo Nexus — базові правила: поле, X-клітина, фігури, лопання, ланцюги, сміття"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Scoring", note: "формула очок, бонуси кольору й групи, перетворення очок у сміття"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/List_of_attack_powers", note: "chain power для кожної гри"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Offset_rule", note: "гасіння вхідного сміття"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Margin_time", note: "зменшення target points з часом"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Nuisance_queue", note: "черга сміття, іконки, ліміт 30 на раз"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Types_of_Puyo", note: "кольорові, сміття, тверді, point, sun, iron, block"}
  - {kind: fandom, url: "https://puyonexus.com/wiki/Puyo_Puyo_Tsu", note: "Tsu (1994) — канонічні змагальні правила"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puyo_Puyo", note: "історія серії, версії й режими"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Puyo+Puyo+Tetris", note: "пошук; Puyo Puyo Tetris 1/2, Puyo Puyo Champions"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puyo+puyo+tsu+chain+gameplay", note: "пошук; ланцюги Tsu"}
stage: v1
coverage: 70
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, event-points, combo-multiplier, ai-opponent, ai-greedy, hot-seat, time-bonus, score-records, game-pause, end-screen, +connected-group-pop, +chain-reaction, +cascade-gravity, +next-queue, +garbage-attack, +garbage-offset, +garbage-adjacent-clear, +all-clear-bonus, +margin-time, +double-rotation, +nuisance-queue-icons]
proposes: ["+trigger:locked", "+trigger:settled", "+effect:send_garbage", "+effect:offset_garbage", "+cond:adjacent_cleared", "+ui:garbage-meter", "+ui:action-text", "+window:character-select", "+feature:mode-puzzle", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# Puyo Puyo — пари кольорових слимаків; 4 звʼязані лопаються, ланцюги засипають суперника сміттям

## Суть
Зверху падає пара пуйо (дві кольорові кульки); гравець зсуває й обертає її, а після приземлення кожна кулька падає окремо. 4+ звʼязаних по сторонах однакових кольорів лопаються, усе вище осідає — і якщо утворились нові групи, лопається знову: це **ланцюг**. Гра — дуель: ланцюг перетворюється на сміттєві пуйо у суперника, а його атаку можна погасити своїм ланцюгом (offset). Майстерність — заздалегідь будувати 10+-ланцюги «сходинками».

## Поле і час
- Поле 6 стовпців × 12 видимих рядів на гравця; два поля поруч у versus. Клітина поразки — 3-й стовпець, верхній ряд (у пре-Fever іграх немарковано; з Fever позначено червоним X).
- Real-time падіння пари; після приземлення гра переходить у **фазу розвʼязання**: окреме падіння кульок → пошук груп → лопання → осідання → повтор, доки нема груп. Під час фази ввід вимкнено.
- Шари: поле кольорових/сміттєвих пуйо + активна пара + черга сміття над полем (видно іконками).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пара пуйо | player | 2 кольори, вісь (нижня) + сателіт, орієнтація 4 | зсув, обертання навколо осі, soft drop; приземлення → розпадається на 2 окремі пуйо |
| Кольорове пуйо | tile | колір (3–5 у матчі) | падає до опори окремо; 4+ звʼязаних (4-сусідство) того ж кольору → лопається |
| Сміттєве (nuisance, ojama) пуйо | hazard | прозоре/сіре | не групується; зникає, коли поруч (4-сусідство) лопається кольорова група |
| Тверде (hard) пуйо | hazard | 2 «життя» | перше сусіднє лопання → звичайне сміття (варіант правил) |
| Point puyo | hazard | +50 (зазвич.) | сміття, що додає очки ланцюгу при знищенні |
| Sun puyo (Sun) | tile | — | лопання додає сміття суперникові без очок |
| Iron / Block puyo | hazard | — | не знищується звичайно / не падає (окремі ігри) |
| X-клітина | static | (3,1) | заповнена → поразка |
| Черга сміття | spawner | к-сть, іконки 1/6/30/180/360/720/1440 | падає після твого ходу, якщо не погашена; ≤30 за раз (5 рядів) |
| Черга next | spawner | 2 пари видно | джерело наступних пар |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(pair, down)`; утримання ↓ — швидше (soft drop, очки за клітину).
- КОЛИ `input(shift)` → ЯКЩО `free(target_cells)` → ТО `move(pair, dir)`.
- КОЛИ `input(rotate_cw|ccw)` → ЯКЩО `free(new_satellite_cell)` → ТО `rotate(pair, ±90)`; інакше ЯКЩО вільно з протилежного боку → ТО `custom: «кік — пара відштовхується від стіни/стеку»`.
- КОЛИ `input(rotate)` двічі → ЯКЩО `not free(left) and not free(right)` → ТО `rotate(pair, 180)` (quick turn / double rotation, Tsu).
- КОЛИ `custom: «landed(pair)»` → ТО `custom: «розщепити»`, `fall(each_puyo)` (кожне окремо до опори).
- КОЛИ `pattern(group(4+, same_color, adj4))` → ТО `clear(group)`, `clear(adjacent_nuisance)`; кілька груп за один крок — одночасне лопання (той самий крок ланцюга).
- КОЛИ `after(clear)` → ТО `fall(all_unsupported)`, ЯКЩО `pattern(group(4+))` → ТО `combo(+1)` (крок ланцюга) і повтор; нема груп → кінець ланцюга.
- Рахунок кроку: `score(10 × PC × (CP + CB + GB))`, де PC — лопнуті пуйо, CP — chain power (Tsu: 0, 8, 16, 32, 64, 96, 128 … +32), CB — бонус кольорів у кроці (1:0, 2:3, 3:6, 4:12, 5:24), GB — бонус розміру групи (4:0, 5:2, 6:3 … 10:7, 11+:10); множник обмежено 1..999.
- КОЛИ `after(score)` → ТО `custom: «send_garbage — NP = очки / TP + залишок; ціла частина летить, дробова переноситься»`; TP (target points) = 70 у Tsu.
- КОЛИ `custom: «send_garbage»` → ЯКЩО `count(own_incoming, >, 0)` → ТО `custom: «offset — гасить вхідну чергу, надлишок летить супернику»` (Tsu).
- КОЛИ `custom: «chain ended»` → ЯКЩО `count(incoming, >, 0)` → ТО `spawn_at(nuisance, top)`, ≤ 30 за раз, рівномірно по стовпцях, падають як звичайні пуйо.
- КОЛИ `after(chain)` → ЯКЩО `count(puyo_on_field, ==, 0)` → ТО `custom: «all clear — +30 сміття (один «камінь») до наступної атаки»` (Tsu).
- КОЛИ `timer(margin, elapsed)` → ТО `custom: «margin time — TP × 0.75, далі кожні 16 с зменшення з округленням донизу; стоп на 1 або після 14 кроків»` — пізня гра агресивніша.
- КОЛИ `spawned(pair)` → ЯКЩО `occupied(x_cell)` → ТО `lose` у суперника — `win` тобі; у раунд-системі — рахунок перемог.
- Одиночний режим (класика): КОЛИ рахунок ≥ порогу (`counter`) → наступний суперник (Puyo Puyo 2 рулетка); Endless — до поразки на очки.

## Керування і ввід
- ←/→ — зсув; ↓ — прискорене падіння; кнопки A/B — поворот за/проти годинникової; подвійне натискання у вузькому колодязі — розворот на 180°. Hard drop — лише у пізніх іграх (?).
- Versus: два гравці одночасно на одному екрані (кожен свій контролер) або проти CPU.
- Під час фази ланцюга ввід ігнорується — гравець дивиться на каскад.

## Вікна, меню, HUD
- `splash-screen` / title → `main-menu`: Story/Single · Versus (2P) · Endless · Mission/Nazo Puyo · Options.
- `custom: «character-select»` (у пізніх іграх; персонаж = суперник CPU або набір правил/дропсет у Fever).
- `game-screen`: два поля 6×12, між ними `next-piece-preview` (2 пари) для кожного, `score` під полем, `custom: «garbage-meter»` — ряд іконок над полем (маленька 1, велика 6, камінь 30, зірка 180 …), `popup-text` «N Rensa!/N-chain» біля поля, лічильник перемог у матчі.
- `end-screen` раунду (Win/Lose, анімація персонажа) → наступний раунд/суперник; `game-over-continue` у Story.
- `pause-menu`; `settings-window` — складність CPU, к-сть перемог у матчі, к-сть кольорів, «Rule Henka» (сміття → тверді/point, Tsu).
- Переходи: main-menu → (Story) рулетка/вибір суперника → game-screen → end-screen → наступний; Versus → game-screen → … → підсумок матчу.

## Фічі поза полем
- `mode-versus` + `local-multiplayer`/`online-multiplayer` (сучасні), `ai-opponent-levels` (CPU-персонажі різної сили).
- `mode-endless`, `mode-puzzle` — Nazo Puyo: задане поле, «зроби N-ланцюг / прибери все».
- Puyo Puyo 2: рулетка суперників + пороги очок; Tsu: варіант правил Rule Henka як `custom-rules`.
- `leaderboard-local` (Endless), `stats`/рейтинг онлайн у сучасних.
- `colorblind-palette` (?) — у сучасних іграх можна міняти скіни пуйо (`theme-select`).

## Варіації й родичі
- Puyo Puyo Tsu (1994) — стандарт змагань: offset, margin time, all clear, quick turn. Puyo Puyo Sun — sun puyo. Puyo Pop Fever (2003) — Fever-режим (готові ланцюги), фігури з 3–4 пуйо (L, II, O), позначені X. Puyo Puyo Tetris — Puyo проти Tetris в одній партії.
- Родичі: Dr. Mario (4 в ряд, а не групою), Columns (3 у лінію з діагоналями), Super Puzzle Fighter (crash gems), Baku Baku.
- **Осі варіацій**: умова лопання (група ≥4 / лінія ≥4 / лінія ≥3) · сусідство (4 / 8 / діагоналі) · гравітація (кожна кулька окремо — cascade) · фігура (пара / L / 2×2) · сміття (зникає від сусіда / тверде / незнищенне) · захист (без offset / з offset) · антизатягування (margin time / нема).

## Цікавинки для курсу
- Пошук звʼязаної групи одного кольору (flood fill, 4-сусідство) — 📎.
- Цикл «падіння → групи → лопання → осідання» до стабілізації з лічильником кроків — 🥉 (стан-машина фаз + анімація по кроках).
- Формула очок з chain power, бонусами кольору й групи — 📎 (дані-таблиці).
- Сміття з дробовим залишком, offset і чергою з іконками — 🥉.
- Margin time — сила атаки росте з часом — 🌱.
- CPU-суперник, що будує ланцюг (перебір позицій пари на 1–2 ходи вперед з оцінкою ланцюга) — 🥇.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (пара 1×2) · `keyboard-controls` · `event-points` · `combo-multiplier` (ланцюг) · `ai-opponent` + `ai-greedy` · `hot-seat` (тут — одночасно, не по черзі; найближча картка) · `time-bonus` (margin time — бонус за час навпаки) · `score-records` · `game-pause` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` «Лопання звʼязаної групи» · entities/legality · 📎 · слоти {min: 4, adjacency: 4|8}.
  - `+chain-reaction` «Ланцюгова реакція збігів» · game-logic/score · 🥉 — повтор пошуку після осідання, лічильник кроку.
  - `+cascade-gravity` «Кожна клітина падає окремо» · entities/move · 📎 (на відміну від наївної гравітації Tetris).
  - `+next-queue` «Черга наступних» · interface/hud · 🌱 (спільна з Tetris).
  - `+garbage-attack` / `+garbage-offset` · game-logic/opponent · 🥉/📎 (спільні з Tetris).
  - `+garbage-adjacent-clear` «Сміття зникає від сусіднього збігу» · entities/interact · 🌱.
  - `+all-clear-bonus` «Бонус за порожнє поле» · game-logic/score · 🌱.
  - `+margin-time` «Атака сильнішає з часом» · game-logic/opponent · 🌱 · слоти {start, step, factor}.
  - `+double-rotation` «Розворот 180° у вузькому місці» · entities/legality · 🌱.
  - `+nuisance-queue-icons` «Черга атаки іконками-номіналами» · interface/hud · 📎.

## Пропозиції до словників
- `+trigger:locked` — пара приземлилась (спільне з Tetris); `+trigger:settled` — поле стабілізувалось (нема падінь і груп) — кінець ланцюга, момент падіння сміття.
- `+effect:send_garbage`, `+effect:offset_garbage` — як у Tetris; тут з дробовим залишком.
- `+cond:adjacent_cleared` — поруч лопнула група (умова зникнення сміття).
- `+ui:garbage-meter` — іконки вхідного сміття над полем; `+ui:action-text` — «N-chain!».
- `+window:character-select` — ⏳ підтверджую (вибір персонажа/суперника).
- `+feature:mode-puzzle` — ⏳ підтверджую (Nazo Puyo).
- `+axis:gravity` — `cascade` тут (кожна кулька окремо).

## Джерела
- ⭐ [Puyo Nexus: Basic rules](https://puyonexus.com/wiki/Basic_rules) — поле, X-клітина, типи фігур, лопання, ланцюги, сміття.
- [Puyo Nexus: Scoring](https://puyonexus.com/wiki/Scoring) — формула 10×PC×(CP+CB+GB), бонуси, TP=70, перенесення залишку.
- [Puyo Nexus: List of attack powers](https://puyonexus.com/wiki/List_of_attack_powers) — chain power Tsu.
- [Puyo Nexus: Offset rule](https://puyonexus.com/wiki/Offset_rule) · [Margin time](https://puyonexus.com/wiki/Margin_time) · [All clear](https://puyonexus.com/wiki/All_clear) · [Nuisance queue](https://puyonexus.com/wiki/Nuisance_queue) · [Types of Puyo](https://puyonexus.com/wiki/Types_of_Puyo).
- [Puyo Nexus: Puyo Puyo Tsu](https://puyonexus.com/wiki/Puyo_Puyo_Tsu) — 1994, нові механіки, режими, Rule Henka.
- [Wikipedia: Puyo Puyo](https://en.wikipedia.org/wiki/Puyo_Puyo) — серія, роки, платформи.

## Непевне
- (?) Прихований 13-й ряд (можна класти, але не лопається) і 14-й «привид» — відомо з памʼяті про Tsu, Puyo Nexus Basic rules не підтвердив.
- (?) Тривалість margin time у Tsu (96 с?) — на сторінці лише в підписі до картинки; і чергування ×0.75/×2/3 — у джерелі суперечність.
- (?) Hard drop і точні правила кіку пари від стіни — залежать від гри, не перевірено.
- (?) Очки soft drop, бонус all clear в очках — не перевірено.
