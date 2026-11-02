---
title: Tsuro (+ Indigo)
slug: tsuro
family: connect-rotate
also: [board-digital]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: hotseat
  info: partial
  random: runtime
  goal: survive
year: 2004
platforms: [board, iOS, Android, PC (Steam)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tsuro", best: true, note: "правила Tsuro: 6×6, 35 плиток, хід, виліт, зіткнення, Dragon tile, версії й розширення"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Indigo_(board_game)", note: "Indigo (Knizia, 2012): самоцвіти, ворота, зіткнення, очки"}
  - {kind: other, url: "https://spotlight.histmyst.org/rules/indigo.html", note: "повні правила Indigo: 54 плитки × 3 шляхи, ворота за кількістю гравців, варіант із 2 плитками"}
  - {kind: other, url: "https://www.dover.nh.gov/Assets/government/city-operations/library/borrow/library-of-things/Tsuro_Rules.pdf", note: "PDF правил Tsuro (скан, текст не витягнувся)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Tsuro", note: "пошук; цифрова версія Thunderbox"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Tsuro", note: "пошук BGG; сторінки віддають 403"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tsuro+how+to+play", note: "пошук; правила за 3 хв"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Indigo+Knizia+how+to+play", note: "пошук; Indigo"}
stage: v1
coverage: 75
mechanics: [hot-seat, turn-enforcement, ai-opponent, movement-animation, game-screen, end-screen, main-menu, help-window, event-points, +tile-rotate, +pipe-connectors, +path-follow, +edge-exit-elimination, +path-collision, +hand-of-tiles, +forbidden-suicide, +shared-goal, +last-standing, +tile-catalog-enumeration]
proposes: ["+role:supply", "+role:sink", "+role:conduit", "+trigger:after", "+trigger:edge", "+cond:has_alternative", "+effect:place", "+effect:follow_path", "+effect:draw", "+effect:give", "+ui:pocket", "+ui:path-preview", "+window:match-setup", "+card:path-follow", "+card:edge-exit-elimination", "+card:path-collision", "+card:hand-of-tiles", "+card:shared-goal"]
author: opus
date: 2026-11-02
---

# Tsuro (+ Indigo) — кладеш плитку-шлях, і фішку тягне по ньому; вилетів за край — вибув

## Суть
2–8 гравців, кожен має фішку на краю дошки 6×6 і 3 плитки в руці. Хід — покласти плитку на клітину **перед своєю фішкою**; фішка (і всі чужі, що стоять біля цієї плитки) одразу їдуть шляхом до кінця, доки не впруться в порожню клітину або край. Хто виїхав за край чи зіткнувся з іншою фішкою — вибуває; виграє останній. Ти не ходиш фігурою — ти будуєш дорогу, а рух робить гра. Indigo (Knizia, 2012) — та сама ідея на гексах, але по шляхах котяться не фішки гравців, а спільні самоцвіти, і їх треба загнати у свої ворота.

## Поле і час
- Tsuro: квадрат 6×6; на кожному боці клітини — 2 точки входу (8 на плитку); край дошки має 12 насічок на сторону — стартові точки фішок.
- Фішка завжди стоїть **на ребрі** клітини, а не в клітині: це точка між плитками, де шлях обірвався.
- Indigo: гекс-поле; у центрі — скарб-плитка, по краю 6 скарб-плиток, між ними — 6 воріт (по 6 виходів), пофарбованих у кольори власників.
- Покроково, гравці по черзі за годинниковою стрілкою; хід = покласти → рух усіх зачеплених → добрати. Рух — каскад у межах одного ходу.
- Німецьке видання (Kosmos 2007): двобічна дошка з боком 7×7, 64 плитки, з яких випадково беруть 35.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка гравця (Tsuro) | player | колір; позиція на точці ребра | рухається лише шляхами плиток; виліт → вибуває |
| Плитка-шлях (Tsuro) | tile | 4 шляхи, що попарно зʼєднують 8 точок; поворот 0/90/180/270 | 35 різних плиток = всі розбиття 8 точок на пари з точністю до повороту |
| Рука | supply (custom) | 3 плитки, приховані | поповнюється після ходу |
| Колода | supply (custom) | закрита | випадкове добирання |
| Плитка «Дракон» | static | 1 шт., для 3+ гравців | черга добирання, коли колода порожня |
| Край дошки | hazard | 12 точок на бік | фішка, що доїхала сюди, вибуває |
| Самоцвіт (Indigo) | object | сапфір 3 · смарагд 2 · бурштин/топаз 1 | котиться шляхом до кінця; не повертає й не їде назад |
| Плитка-шлях (Indigo) | tile | гекс, 3 окремі шляхи | крива не може закрити одразу два виходи |
| Скарб-плитка центр (Indigo) | spawner | 1 сапфір + 5 смарагдів | кожна прикладена плитка випускає смарагд; сапфір — останнім |
| Скарб-плитка край (Indigo) | spawner | 1 бурштин | випускає камінь, коли до неї прикласти шлях |
| Ворота (Indigo) | sink | 6 виходів; власник 1 або 2 гравці | камінь, що доїхав, іде власнику (спільні — обом) |
| Запас каменів (Indigo) | supply (custom) | 12 шт. | дублікати для спільних воріт |

## Правила (КОЛИ → ЯКЩО → ТО)
- Tsuro, старт: кожен ставить фішку на будь-яку насічку краю; роздати по 3 плитки.
- КОЛИ `input(place, tile, rot)` → ЯКЩО `turn_of(p)` → ТО `place(tile, cell_in_front_of(p))` — лише клітина, до якої впирається фішка гравця.
- КОЛИ `input(place)` → ЯКЩО `custom: «шлях веде фішку p за край»` and `has_alternative(p)` → ТО `block` (заборона самогубства; якщо інших варіантів нема — дозволено).
- КОЛИ `after(place)` → ТО для кожної фішки, що торкається нової плитки: `follow_path(token)` — рух від точки до точки через усі зʼєднані плитки, доки не порожня клітина або край.
- КОЛИ `edge(token)` → ТО `disappear_a`, `custom: «гравець вибуває»`; його невикористані плитки — в колоду, `shuffle`.
- КОЛИ `contact(token_a, token_b)` (зустрілись на одному шляху / в одній точці) → ТО `disappear_both`, обидва гравці вибувають.
- КОЛИ `turn_end` → ТО `draw(p)` до 3 плиток; ЯКЩО колода порожня → `custom: «гравець бере Дракона й добирає першим, щойно плитки повернуться»`.
- КОЛИ `count(tokens, ==, 1)` → ТО `win(last)`; КОЛИ всі останні вибули одночасно → `draw` (нічия, ?); КОЛИ плитки скінчились і на дошці >1 фішки → `custom: «спільна перемога»` (?).
- Indigo: КОЛИ `input(place, tile)` → ЯКЩО `free(cell)` and `not custom: «крива закриває два виходи»` → ТО `place` (будь-де, не обовʼязково поруч).
- КОЛИ `after(place)` → ТО кожен самоцвіт, чий шлях тепер продовжено, `follow_path(gem)` до кінця; скарб-плитки, торкнуті новою, випускають камінь.
- КОЛИ `contact(gem_a, gem_b)` на одному шляху → ТО `disappear_both` (ні в кого).
- КОЛИ `edge(gem)` у воротах g → ТО `give(owner(g), gem)`; ЯКЩО ворота спільні → `give(coowner, copy_from_supply)`.
- Indigo, кінець: КОЛИ `all_gone(gem)` → ТО `score(3/2/1)`; виграє більший рахунок, далі — більше каменів, далі — спільна перемога.
- Перемога: останній на дошці (Tsuro) / найбільше очок (Indigo) · Поразка: виліт за край або зіткнення (Tsuro) · Рахунок: лише Indigo.

## Керування і ввід
- Настолка: вибрати плитку з руки, повернути, прикласти до клітини перед фішкою; рух фішок — руками всіх гравців.
- Цифрова версія Tsuro: клік по плитці в руці → обертання кнопками/жестом → `path-preview` показує, куди поїде фішка → підтвердити; рух — анімацією.
- Indigo: клік по будь-якій вільній гекс-клітині, обертання на 60°; варіант «2 плитки в руці».

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Грати → `match-setup` (2–8 гравців, людина/AI, колір), Онлайн, Правила (`help-window`), Налаштування.
- `game-screen`: дошка 6×6 з фішками, `pocket` — 3 плитки руки з кнопками повороту, `path-preview` шляху власної фішки, `turn-indicator`, список гравців із вибулими.
- `end-screen`: переможець(і), повтор партії (?).
- Indigo (цифрова версія): `game-screen` з воротами в кольорах власників, `score` прихований за «ширмою» (`pocket` каменів), `end-screen` з підрахунком 3/2/1.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `hotseat` на 2–8, `ai-opponent-levels` і `online-multiplayer` у цифровій Tsuro (Thunderbox, ?).
- `custom-rules`: Tsuro of the Seas (кайдзю-плитки рухаються за кидком кубика й зносять фішки), Veterans of the Seas (портал, цунамі, вир, гармата), Phoenix Rising (центральні й крайові плитки, зірки), Asteroid Escape (астероїди), 7×7 (Kosmos).
- Indigo: `custom-rules` — 2 плитки в руці (стратегічний варіант), кілька раундів із сумою очок, альтернативний розподіл воріт для 3 гравців.

## Варіації й родичі
- Предок — Squiggle (патент Tom McMurchie, 1979); родичі: Psyche-Paths/Kaliko, Trax, Tantrix, Metro (Dorra, — колії до станцій).
- Indigo — «Tsuro без аватарів»: рухаються спільні обʼєкти, а боротьба — за спрямування їх у свої/спільні ворота.
- Осі варіацій: **що їде шляхом: своя фішка / спільний камінь / ворог (кайдзю)** · **де можна класти: лише перед собою / будь-де** · **топологія: квадрат з 8 точками / гекс з 6** · **зіткнення: обидва вибувають / обидва знищені** · **край: смерть / приз власнику воріт**.

## Цікавинки для курсу
- Рух по шляхах плиток: точка (клітина, бік, № точки) → через таблицю зʼєднань плитки → вихідна точка → сусідня клітина; ітерувати, доки є плитка — 🥉.
- Поворот плитки як зсув номерів точок на 2 за модулем 8 — 🌱; генерація всіх 35 унікальних плиток (розбиття 8 точок на пари мод поворот) — 🥈.
- Заборона самогубства: перебрати всі (плитка × поворот) з руки і перевірити, чи є хід без вильоту — 📎.
- Зіткнення двох рухомих по одному шляху (фішки / самоцвіти) — 📎.
- Indigo: каскад руху кількох самоцвітів після однієї плитки + спільні ворота з дублікатом — 🥉.
- AI для Tsuro: жадібний «вибери хід, після якого моїй фішці найдовше до краю» — 📎; minimax на 2 гравців — 🥇.

## Мапа на каталог
- Є: `hot-seat` · `turn-enforcement` · `ai-opponent` · `movement-animation` (проїзд шляхом) · `event-points` (Indigo 3/2/1) · `game-screen` · `end-screen` · `main-menu` · `help-window`.
- **Нема** → пропозиції карток:
  - `+tile-rotate` «Обертання плитки» · entities/state · 🌱 · слот {step: 90|60}.
  - `+pipe-connectors` «Плитка-зʼєднувач з портами» · entities/state · 🌱 — тут 8 портів (2 на бік).
  - `+path-follow` «Рух по шляхах плиток до обриву» · entities/move · 🥉 · слоти {who: own|shared, stop: empty|edge|collision}.
  - `+edge-exit-elimination` «Виліт за край = вибування» · game-logic/lose · 🌱.
  - `+path-collision` «Зіткнення на шляху знищує обох» · entities/combat · 📎.
  - `+hand-of-tiles` «Рука плиток із добиранням» · game-logic · 📎 · слоти {hand: 1|2|3, deck: shuffled}.
  - `+forbidden-suicide` «Заборона самогубного ходу за наявності іншого» · entities/legality · 📎.
  - `+shared-goal` «Спільні ворота двох гравців» · game-logic/score · 🌱.
  - `+last-standing` «Перемагає останній» · game-logic/win · 🌱.
  - `+tile-catalog-enumeration` «Генерація всіх унікальних плиток» · levels/generation · 🥈.

## Пропозиції до словників
- `+role:supply` — рука/колода/запас каменів; `+role:sink` — ворота Indigo; `+role:conduit` — плитка-шлях як провідник руху.
- `+trigger:after` ⏳ — рух фішок одразу після розміщення; `+trigger:edge` ⏳ — вихід за край дошки.
- `+cond:has_alternative(p)` — у гравця є інший легальний хід (для заборони самогубства).
- `+effect:place` ⏳; `+effect:follow_path(a)` — рух сутності шляхом плиток до обриву; `+effect:draw(p)` — добрати плитку з колоди; `+effect:give` ⏳ — камінь власнику воріт.
- `+ui:pocket` (рука плиток, ×3 у корпусі), `+ui:path-preview` (куди поїде фішка).
- `+window:match-setup` — кількість гравців і хто AI.

## Джерела
- ⭐ [Wikipedia: Tsuro](https://en.wikipedia.org/wiki/Tsuro) — 6×6, 35 плиток + Дракон, хід у 3 кроки, самогубство заборонене, зіткнення, Squiggle 1979, видання й розширення, Thunderbox.
- [Wikipedia: Indigo](https://en.wikipedia.org/wiki/Indigo_(board_game)) — Knizia 2012, Ravensburger, самоцвіти, ворота, зіткнення, сапфір після смарагдів, 3/2/1.
- [Правила Indigo (histmyst)](https://spotlight.histmyst.org/rules/indigo.html) — 54 плитки × 3 шляхи, 7 скарб-плиток, ворота за кількістю гравців, заборона кривої на два виходи, варіант 2 плиток.
- [PDF правил Tsuro](https://www.dover.nh.gov/Assets/government/city-operations/library/borrow/library-of-things/Tsuro_Rules.pdf) — скан, текст не прочитано.
- Steam / BGG / YouTube — пошукові лінки.

## Непевне
- (?) Кінець, коли плитки скінчились, а фішок кілька — спільна перемога (з памʼяті, PDF не прочитався); одночасне вибування всіх останніх — нічия (?).
- (?) Точний механізм зіткнення: «дві фішки опинились на одному шляху» за Wikipedia; чи вибувають, коли лише стикаються в одній точці без руху — не звірено.
- (?) Рік: Wikipedia пише і 2004 (категорія), і «released in 2005».
- (?) Цифрові версії (AI, онлайн, preview шляху) — Wikipedia лише згадує Thunderbox; вікна описані як «(цифрова версія)».
- (?) Назва каменів Indigo: Wikipedia — topaz, правила — amber (бурштин); на картці 1 очко.
