---
title: Lethal Geometry
slug: lethal-geometry
aka: []
family: tower-lanes
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2026
platforms: [PC, Linux, web]
links:
  - {kind: itch, url: "https://stoneforgelabs.itch.io/lethal-geometry", best: true, note: "безкоштовне демо (Windows, Linux, HTML5): сектор Training, мапи Relay і Crossfire, Intensity до 3; суть «TD без веж»"}
  - {kind: steam, url: "https://store.steampowered.com/app/5325830/Lethal_Geometry/", note: "повна гра (Coming soon): типи ворогів, драфт 24 карт, Lab, лумени, мутатори, Intensity 1–10, Endless, швидкості 1/2/4/10×; скриншоти HUD"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lethal+Geometry+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [beam-tracing, mirror-reflect, tower-placement, enemy-waves, spawn-points, enemy-reached-base, hp-damage, round-currency, shop-buyback, run-relics, difficulty-levels, rule-variants, level-select, game-pause, restart-level, score-records, +beam-splitter, +choose-upgrade, +speed-control, +meta-unlocks, +loadout-select, +mutators-score-multiplier, +beam-power-drain, +device-flip-midwave, +device-disruptor-enemy, +directional-shield]
proposes: ["+role:device", "+trigger:beam_hit", "+effect:absorb", "+effect:sell", "+cond:beam_power", "+ui:beam-stats", "+ui:wave-roster", "+ui:device-toolbar", "+window:upgrade-draft", "+feature:intensity-steps", "+card:beam-power-drain", "+card:device-flip-midwave", "+card:device-disruptor-enemy"]
author: opus
date: 2026-11-09
---

# Lethal Geometry — TD без веж: один лазер, дзеркала, спліттери й лінзи на сітці, а кожен ворог «пʼє» промінь

## Суть
Ворожі колони йдуть доріжкою до ядра, а в гравця нема веж — лише лазер-емітер і бюджет у кредитах. Він ставить на клітини дзеркала, спліттери й лінзи, прокладаючи промінь так, щоб той накривав якомога більше доріжки. Головна механіка — **промінь слабшає**: кожен ворог, крізь якого він проходить, поглинає частку потужності (дрон — 25 %, броньований — 65 % і ще й закриває тих, хто позаду), а голі дзеркала втрачають силу з відстанню. Тому важливо, де розщепити промінь і з якого боку вдарити колону — у хвіст, а не в лоб.

## Поле і час
- Квадратна сітка ~14×10 (?); доріжка ворогів — канал зі стрілками від точки спавну (червоне коло) до ядра (блакитний кристал).
- Емітер стоїть на краю поля й світить уздовж ряду; на мапі Prism Core емітерів два (скриншот).
- Пристрої займають клітину; дзеркало стоїть по діагоналі й повертає промінь на 90°, промінь іде прямими рядами/стовпцями сітки до краю поля.
- Real-time з паузою й швидкостями 1×/2×/4×/10×; між хвилями — фаза винагороди з вибором апгрейда. Хвиль на мапі 10–12 (скриншоти), HP ворогів росте множником (×1.0 … ×2.6).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лазер-емітер | source | потужність | випускає промінь в один бік уздовж ряду |
| Промінь (гілка) | projectile | потужність, % | летить прямо, шкодить усім ворогам на шляху, слабшає від кожного й з відстанню |
| Дзеркало | conduit | 30 cr, орієнтація | повертає промінь на 90°; клік — перекинути на іншу діагональ |
| Спліттер | conduit | 80 cr | ділить промінь на гілки (з апгрейдом Prism Splitters — третя гілка на 25 %) |
| Лінза | conduit | 120 cr (60 cr на одному скриншоті) | відновлює/фокусує потужність променя |
| Доріжка | terrain | напрям | шлях колон від спавну до ядра |
| Точка спавну | spawner | — | випускає хвилю колоною |
| Ядро (core) | static | HP 100 | ворог дійшов — шкода ядру; 0 — поразка (?) |
| Дрон | enemy | поглинає 25 % | базовий ворог, іде колоною |
| Броньований (Armored) | enemy | поглинає 65 % | закриває від променя тих, хто йде за ним |
| Рефлектор | enemy | поглинає 30 %, фронтальний щит | щит відкидає промінь, що бʼє в лоб |
| Саботажник | enemy | поглинає 20 % | збиває сусідні дзеркала й спліттери з лінії («Saboteur flipped 1 device!») |
| Глушник (Jammer) | enemy | — | блокує цілу гілку променя |
| Warden | boss | HP 1440, поглинає 50 % | на 75 / 50 / 25 % HP перемішує всі дзеркала поблизу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `wave_start` → ТО `spawn_at(column, spawn_point)`; КОЛИ `tick` → ТО `move(enemy, next_on_path)`.
- КОЛИ `input(place, device, cell)` → ЯКЩО `counter(credits, >=, cost)` and `free(cell)` and `custom: «клітина не на доріжці»` (?) → ТО `place(device)`, `currency(-cost)`.
- КОЛИ `input(rotate|flip, device)` → ТО `rotate(device, 90)` — і під час хвилі.
- КОЛИ `input(sell, device)` → ТО `disappear`, `currency(+refund)`.
- КОЛИ `tick` → ТО `custom: «трасувати промінь від емітера: прямо до перешкоди/краю, з усіма розгалуженнями»`.
- КОЛИ `custom: «промінь входить у клітину з дзеркалом»` → ТО `bounce(beam)` під 90° за діагоналлю дзеркала.
- КОЛИ `custom: «промінь входить у спліттер»` → ТО `split(beam)` на гілки, потужність ділиться.
- КОЛИ `custom: «промінь входить у лінзу»` → ТО `custom: «потужність гілки відновлюється»`.
- КОЛИ `custom: «промінь проходить N клітин після голого дзеркала»` → ТО `custom: «потужність падає з відстанню»`.
- КОЛИ `custom: «промінь проходить крізь ворога»` → ТО `damage(enemy, power)`, `custom: «потужність гілки × (1 − absorb ворога)»`.
- КОЛИ `custom: «промінь бʼє рефлектор»` → ЯКЩО `facing(reflector, toward_beam)` → ТО `custom: «промінь відкинуто, шкоди нема»`; інакше `damage(n)`.
- КОЛИ `in_range(saboteur, device, r)` → ТО `rotate(device, 90)`, `message(«Saboteur flipped 1 device!»)`.
- КОЛИ `custom: «на шляху гілки глушник»` → ТО `block` — гілка обривається.
- КОЛИ `counter(warden_hp, <=, 75|50|25 %)` → ТО `custom: «перемішати орієнтації всіх дзеркал поблизу»`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear`, `score(n)`, `currency(+n)` (?).
- КОЛИ `reach(enemy, core)` → ТО `damage(core, n)`; КОЛИ `hp_zero(core)` → ТО `lose` (?).
- КОЛИ `wave_cleared` → ТО `window(upgrade-draft)`, `choose(1 of 5 upgrade cards)`.
- КОЛИ `custom: «остання хвиля мапи пройдена»` → ТО `win`; `custom: «лумени за рахунок»`, відкривається Endless.
- Перемога: вистояти всі хвилі мапи · Поразка: ядро зруйноване (?) · Рахунок: очки за знищених і хвилі; Intensity і мутатори підвищують рахунок.

## Керування і ввід
- Миша й клавіатура (контролера нема): вибрати пристрій на панелі (1 — дзеркало, 2 — спліттер, 3 — лінза) і клітину; клік по пристрою — вибрати / перекинути дзеркало.
- R — повернути, X — продати; P — пауза, F — швидкість, N — рестарт мапи, M — мапи.
- Ремонт посеред хвилі: саботажник збив дзеркало — схопити його й поставити назад.

## Вікна, меню, HUD
- `game-screen`: угорі — «WAVE 6 / 10», назва мапи, стан фази (WAVE / REWARD); праворуч від них — смуга CORE з HP 100/100, кредити (cr), Score, поточна швидкість, Pause (P); праворуч — `+ui:wave-roster` («WAVE IN PROGRESS / NEXT WAVE», множник HP ворогів, скільки на полі й час, список ворогів із кількістю й % поглинання, «NEW» і підказка до нового), `+ui:beam-stats` «BEAM 9 branches · 43% path · 0 at cap», список узятих апгрейдів, блок SELECTED із кнопками Rotate/Sell; унизу — `+ui:device-toolbar` (Mirror 30 cr, Splitter 80 cr, Lens 120 cr з гарячими клавішами), Speed / Restart / Maps, рядок TIP.
- На полі: `toast` «Saboteur flipped 1 device!», знак «!» над збитими пристроями, `hp-bar` боса з поділками 25/50/75 %, кола радіусу ворогів-диверсантів.
- `+window:upgrade-draft` «Choose an upgrade»: 5 карт із лічильником стеку (0/1, 0/2) — Prism Splitters, Pulse Emitter, Heat-up, Afterburn, Anchored Mounts.
- `level-select` (Maps): 10 мап у 3 секторах; `custom-window` Lab (карти, лоадаути, перки Workshop); `stats-window`/вехи (39 milestones) (?).

## Фічі поза полем
- `+feature:intensity-steps`: Intensity 1–10 на кожній мапі (у демо — до 3) — жорсткіші хвилі за більший рахунок; `mode-endless` на виграних мапах.
- Роглайт-драфт: між хвилями — одна з 24 карт, що міняють поведінку світла (afterburn, ланцюгові дуги, гарячі дзеркала, відбивні стіни, ефективніші спліттери); рестарт мапи з тим самим або перетасованим драфтом.
- `meta-progression`: лумени за рахунок забігу (і при поразці) → Lab: нові карти, лоадаути «одна сила за іншу», перки Workshop; стакові мутатори за більший рахунок.
- `speed-control` 1/2/4/10×, `pause`, `restart-level`; демо — HTML5 у браузері.

## Варіації й родичі
- Межа сімей `tower-lanes` і `connect-rotate`: трасування променя з дзеркалами й спліттерами — як у [Deflektor](../connect-rotate/deflektor.md)-подібних пазлах, але ціль — накрити рухомих ворогів, а не освітити мішень.
- TD-родичі: [desktop-tower-defense](desktop-tower-defense.md) (вежі на сітці), [gemcraft](gemcraft.md) (один ресурс на все), [infinitode-2](infinitode-2.md), [rogue-tower](rogue-tower.md) (драфт апгрейдів між хвилями).
- **Осі варіацій**: шкода — вежі / один промінь, що ділиться · ресурс шкоди — нескінченний / «випивається» ворогами · ворог проти будови — нічого / збиває пристрої / перемішує все (бос).

## Цікавинки для курсу
- Трасування променя по сітці з дзеркалами й спліттерами, потужність як число на гілці — 🥉 (рекурсивне розгалуження + захист від циклів).
- Поглинання: кожен ворог на шляху множить потужність на (1 − absorb), броньований закриває тих, хто позаду — 🥉 (порядок ворогів уздовж променя).
- Напрямний щит рефлектора: шкода лише ззаду чи збоку — 📎.
- Саботажник: ворог, що міняє стан будов гравця, і ремонт посеред хвилі — 📎.
- Метрика «% доріжки під променем» як живий показник якості розстановки — 🥈 (покриття доріжки трасою).
- Драфт апгрейдів, що міняють фізику променя (третя гілка спліттера, пульс, нагрів) — 🥉.

## Мапа на каталог
- Є: `beam-tracing` ↔ промінь по сітці · `mirror-reflect` ↔ дзеркала · `tower-placement` ↔ пристрої на клітинах · `enemy-waves` · `spawn-points` · `enemy-reached-base` ↔ ядро · `hp-damage` · `round-currency` ↔ кредити · `shop-buyback` ↔ Sell (X) · `run-relics` ↔ апгрейди драфту до кінця забігу · `difficulty-levels` ↔ Intensity · `rule-variants` ↔ мутатори · `level-select` ↔ Maps · `game-pause` · `restart-level` · `score-records`.
- **Нема** → пропозиції карток:
  - `+beam-power-drain` «Промінь слабшає від кожного ворога й з відстанню» · entities/combat · 🥉 · слот {absorb_per_type}.
  - `+device-flip-midwave` «Перекинути дзеркало кліком посеред хвилі» · interface/input · 🌱.
  - `+device-disruptor-enemy` «Ворог збиває/перемішує будови гравця» · entities/interact · 📎.
  - `+directional-shield` «Щит лише спереду: шкода з тилу чи флангу» · entities/combat · 📎.
  - уже вживані: `+beam-splitter`, `+choose-upgrade`, `+speed-control`, `+meta-unlocks`, `+loadout-select`, `+mutators-score-multiplier`.

## Пропозиції до словників
- `+role:device` — оптичний пристрій гравця на клітині (дзеркало, спліттер, лінза), що не стріляє сам, а змінює промінь.
- `+trigger:beam_hit` — промінь увійшов у клітину з сутністю (вже 🔥 у пропозиціях — тут ще одне вживання).
- `+effect:absorb` — сутність поглинає частку потужності променя.
- `+effect:sell` — прибрати пристрій із поверненням кредитів.
- `+cond:beam_power` — потужність гілки ≥ / ≤ N (капи, «0 at cap»).
- `+ui:beam-stats` — «гілок · % доріжки · на капі»; `+ui:wave-roster` — склад поточної/наступної хвилі з % поглинання; `+ui:device-toolbar` — пристрої з цінами й гарячими клавішами.
- `+window:upgrade-draft` — вибір 1 з 5 карт між хвилями з лічильником стеку.
- `+feature:intensity-steps` — 10 сходинок складності на мапу з множником рахунку.
- `+card:beam-power-drain`, `+card:device-flip-midwave`, `+card:device-disruptor-enemy`.

## Джерела
- ⭐ [itch.io: Lethal Geometry](https://stoneforgelabs.itch.io/lethal-geometry) — демо (Training: Relay, Crossfire, Intensity ≤ 3), «tower defense without towers», один лазер і бюджет, дрони й броньовані «пʼють» промінь, «where you strike a column», план EA 2027 / $9.99, Godot.
- [Steam](https://store.steampowered.com/app/5325830/Lethal_Geometry/) — саботажники, рефлектори, глушники, Warden; голі дзеркала втрачають силу з відстанню, лінзи відновлюють; будувати/перекидати/продавати посеред хвилі; 24 карти драфту; 10 мап / 3 сектори; Intensity, Endless, швидкості; лумени, Lab, лоадаути, мутатори, 39 вех; 4 скриншоти HUD, боса й вікна «Choose an upgrade».
- YouTube: пошук «Lethal Geometry gameplay».

## Непевне
- (?) Розмір сітки (~14×10 зі скриншоту) і чи можна ставити пристрої на клітини доріжки.
- (?) Як саме ворог шкодить ядру (скільки HP) і чи поразка — лише ядро = 0; HUD показує CORE 100/100.
- (?) Звідки кредити посеред гри (за вбивства, за хвилю?) і частка повернення при продажу.
- (?) Скільки гілок дає спліттер без апгрейда (на скриншоті промінь іде з нього і вперед, і вбік) і що саме робить лінза (підсилення чи фокус).
- (?) Ціна лінзи 60 cr на одному скриншоті проти 120 cr на інших — ймовірно, лоадаут або перк.
- (?) Рік: демо 2026 (версія 0.6.0 на itch), Steam EA заплановано на 2027; гра «один лазер», але на мапі Prism Core емітерів два.
