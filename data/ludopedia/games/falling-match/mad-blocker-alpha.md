---
title: Mad Blocker Alpha
slug: mad-blocker-alpha
aka: ["Mad Blocker Alpha: Revenge of the Fluzzles", "Mad Blocker HD"]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2011
platforms: [PSP, PS3]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mad_Blocker_Alpha", best: true, note: "блоки лише по горизонталі, 4+ одного кольору, ланцюг крутить рулетку бонусів, Mad / Concrete / Bomb, Bad і хворі Moke-блоки → ряд «десатуронів»"}
  - {kind: other, url: "https://www.thesixthaxis.com/?p=68542", note: "рецензія: трійки рядком, без обертання, 4 однакові, ланцюг = 8+ блоків за раз, режими Story / Endless / Tower, червона лінія"}
  - {kind: other, url: "https://www.pocketgamer.com/mad-blocker-alpha/review", note: "рецензія: «горизонтальні Columns», бонуси в майбутній трійці і на □/△/○, три ефекти бонусів, мапа Story, Tower"}
  - {kind: other, url: "https://www.thesixthaxis.com/2010/11/09/interview-mad-blocker-alpha/", note: "інтервʼю: Story 17 етапів, Endless Classic / Mad, Tower, локальні рекорди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mad+Blocker+Alpha+PSP+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [gravity-fall, keyboard-controls, next-queue, chain-reaction, blast-wave, inventory-items, event-points, score-records, leaderboard, time-out, mode-select, sequential-levels, world-map, progress-acceleration, +connected-group-pop, +horizontal-trio-reorder, +bonus-roulette, +stored-power-up, +color-clear-special, +column-drill-block, +dead-row-blocker, +chain-only-clear, +inverted-danger-line, +mission-objectives]
proposes: ["+effect:clear_color", "+ui:bonus-roulette", "+card:horizontal-trio-reorder", "+card:column-drill-block", "+card:dead-row-blocker", "+card:chain-only-clear", "+card:inverted-danger-line"]
author: opus
date: 2026-11-09
---

# Mad Blocker Alpha — «горизонтальні Columns»: трійка кольорових блоків падає рядком, збирай 4+ одного кольору, великий ланцюг крутить рулетку бонусів

## Суть
Падаючий матч від ірландської Open Emotion Studios для PlayStation Minis (сиквел флеш-гри Mad Blocker). Згори падає **горизонтальна трійка** кольорових блоків; її можна зсувати вліво-вправо й переставляти кольори всередині, але не обертати — трійка завжди лежить рядком. Група з 4+ блоків одного кольору лопає; **ланцюг** (8+ блоків за раз) крутить **рулетку** збоку екрана, що може дати бонус-блок: «шалений» (знищує свій колір), бетонний (пробиває стовпець), бомба (хрест). Проти гравця — «хворі» зелені Moke-блоки, що перетворюють цілий ряд на мертві «десатурони», які прибирає лише ланцюг.

## Поле і час
- Колодязь — квадратна сітка (розмір — (?)), трійка займає 3 сусідні клітини в ряду.
- Real-time: трійки падають безперервно; у Endless темп зростає.
- Збоку — рулетка бонусів; бонуси видно серед майбутніх трійок і в слотах під кнопками □ / △ / ○.
- Tower: окрема умова — стек має триматися **вище** червоної лінії (інвертована «межа небезпеки»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Трійка | player | 3 блоки, кольори | падає рядком; зсув вліво/вправо, перестановка кольорів; без обертання і вертикального положення |
| Кольоровий блок | tile | колір | 4+ звʼязаних одного кольору — зникають |
| Mad Block | pickup | — | знищує всі блоки кольору, на який упав |
| Concrete Block | pickup | — | пробиває вниз увесь вертикальний стовпець |
| Bomb Block | pickup | хрест | вибухає хрестом, знищуючи блоки на шляху |
| Bad Block | hazard | — | негативний блок (дія — (?)) |
| Moke (хворий зелений блок) | hazard | — | перетворює цілий ряд гравця на десатурони |
| Десатурон (мертвий блок) | static | — | не бере участі в збігах; прибирається лише ланцюгом |
| Рулетка | — (ui) | сектори бонусів | крутиться на кожен ланцюг; вирішує, чи дати бонус |
| Перешкоди Tower: бомба · важкий блок | hazard | — | падають у випадкові моменти; бомба зносить кілька рядів, важкий блок трощить усе на своєму шляху |
| Червона лінія (Tower) | zone | висота | стек опустився нижче — кінець |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `spawned(trio)` → ТО `custom: «згори зʼявляється горизонтальна трійка з 3 кольорових блоків (іноді з бонус-блоком)»`.
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(trio, down)`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target_cells)` → ТО `move(trio, dir)`.
- КОЛИ `input(reorder)` → ТО `custom: «переставити кольори всередині трійки»`; обертання нема — `block` для будь-якої спроби поставити трійку вертикально.
- КОЛИ `custom: «трійка лягла»` → ТО `custom: «lock»`, `fall(unsupported_blocks)` (?).
- КОЛИ `pattern(group(4+, same color))` → ТО `clear(group)`, `score(n)`.
- КОЛИ `settled` → ЯКЩО `pattern(group(4+, same color))` → ТО `clear(group)`, `combo(+1)` — каскад.
- КОЛИ `custom: «за раз зникло ≥ 8 блоків»` → ТО `custom: «ланцюг»`, `score(bonus)`, `custom: «рулетка обертається»`; ЯКЩО `prob(p)` → ТО `give(player, power_up)`.
- КОЛИ `input(□|△|○)` → ЯКЩО `has(player, power_up)` → ТО `use(player, power_up)` — бонус-блок іде в гру.
- КОЛИ `locked(mad_block)` → ТО `custom: «clear_color — зникають усі блоки кольору, на який упав»`.
- КОЛИ `custom: «бетонний блок падає»` → ТО `clear(column)` — пробиває вертикальну лінію до дна.
- КОЛИ `locked(bomb_block)` → ТО `explode(cross, n)`.
- КОЛИ `locked(moke)` → ТО `transform(row_blocks, desaturon)` — увесь ряд мертвіє.
- КОЛИ `custom: «ланцюг поруч із десатуроном»` → ТО `disappear(desaturon)` (?); звичайна четвірка десатурон не бере.
- **Endless**: КОЛИ `custom: «стек заповнив екран»` → ТО `lose`; КОЛИ `timer(every)` → ТО `speed(fall, +)`.
- **Story**: КОЛИ `counter(score, ≥, 10000)` → ЯКЩО `timer(>, 0)` → ТО `win`; інша ціль — `counter(chains, ≥, 5)` → ТО `win`; час вийшов — `lose`.
- **Tower**: КОЛИ `rng(p)` → ТО `spawn_at(obstacle(bomb|heavy), top)`; КОЛИ `custom: «верх стеку нижче червоної лінії»` → ТО `lose`; КОЛИ `custom: «ціль висоти досягнуто»` → ТО `custom: «вежа скидається, гра триває»`.
- Перемога: ціль етапу Story · Поразка: екран заповнено (Endless) / вежа нижче лінії (Tower) / час вийшов (Story) · Рахунок: за групи 4+, більше — за ланцюги.

## Керування і ввід
- Хрестовина (PSP/PS3): зсув трійки вліво-вправо; окрема дія — переставити кольори в трійці (яка саме кнопка — (?)).
- □ / △ / ○ — застосувати збережені бонуси.
- Рецензенти скаржаться на трохи повільний зсув на високій швидкості.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story · Endless (Classic / Mad) · Tower.
- `map-window` (Story): мапа світу з етапами, прогрес; перед етапом — ціль (`objective-text`).
- `game-screen`: колодязь, майбутня трійка (`next-piece-preview` (?)), `score`, `timer-countdown` (етапи Story), рулетка збоку (`+ui:bonus-roulette`), слоти бонусів під □/△/○ (`inventory-bar`); Tower — червона лінія (`danger-line`).
- `leaderboard` — локальні таблиці рекордів.
- `dialogue-window` — сюжет Story «з недомовками» (світ, отруєний Moke).
- `end-screen` — Game Over / ціль виконано.
- Переходи: main-menu → mode-select → (Story: map-window →) game-screen → end-screen.

## Фічі поза полем
- `levels-sequential` + `world-map`: Story — 17 етапів з різними цілями (очки до кінця таймера, кількість ланцюгів).
- `mode-endless`: Classic — налаштування як у старій флеш-грі; Mad — новий інтерфейс і нові можливості Alpha (які саме — (?)).
- Tower — окремий режим «будуй вгору».
- `leaderboard-local`.

## Варіації й родичі
- Mad Blocker (флеш-оригінал) → Mad Blocker Alpha (2011, PSP/PS3 Minis) → Mad Blocker HD (порт для PS Vita).
- **Осі «форма падаючої фігури»**: вертикальна трійка з циклом кольорів (Columns `columns`) / горизонтальна трійка з перестановкою (тут) / пара з обертанням (Puyo `puyo-puyo`, Dr. Mario `dr-mario`) / тетроміно (`tetris`).
- **Осі «бонус за великий збіг»**: спецплитка на місці збігу (Bejeweled `bejeweled`) / випадкова рулетка (тут) / сміття супернику (Puyo).
- **Осі «межа поразки»**: стек вище лінії — програш (звичайно) / стек нижче лінії — програш (Tower).
- Родичі: Columns, Puyo Puyo, Magical Drop (`magical-drop`).

## Цікавинки для курсу
- Горизонтальна трійка з перестановкою кольорів замість обертання — 🌱.
- Звʼязні групи 4+ (flood fill) з каскадом після осідання — 📎.
- Ланцюг ≥ 8 → зважена рулетка бонусів → слоти під трьома кнопками — 📎.
- Три бонус-блоки: колір (усі такого кольору), стовпець, хрест — 🌱 кожен, 📎 разом.
- Moke: мертвий ряд, який прибирає лише ланцюг (окремий тип клітини з особливим правилом очищення) — 📎.
- Tower: інвертована межа (тримати стек вище лінії) + випадкові перешкоди — 🥉 (баланс).

## Мапа на каталог
- Є: `gravity-fall`; `keyboard-controls` ↔ хрестовина й кнопки; `next-queue` ↔ майбутня трійка; `chain-reaction` ↔ каскади; `blast-wave` ↔ Bomb Block хрестом; `inventory-items` ↔ збережені бонуси під кнопками; `event-points`; `score-records` + `leaderboard` ↔ локальні рекорди; `time-out` ↔ етапи Story на час; `mode-select`; `sequential-levels` + `world-map` ↔ 17 етапів Story на мапі; `progress-acceleration` ↔ Endless.
- Уже пропоновані: `+connected-group-pop` (n = 4), `+bonus-roulette`, `+stored-power-up`, `+color-clear-special` (Mad Block), `+mission-objectives`.
- **Нема** → пропозиції карток:
  - `+horizontal-trio-reorder` «Падає рядок із 3; лише зсув і перестановка» · entities/move · 🌱.
  - `+column-drill-block` «Блок пробиває стовпець донизу» · entities/combat · 🌱.
  - `+dead-row-blocker` «Ворожий блок мертвить цілий ряд» · entities/interact · 📎.
  - `+chain-only-clear` «Клітини, які прибирає лише ланцюг» · entities/interact · 📎.
  - `+inverted-danger-line` «Програш, коли стек нижче лінії» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:clear_color` — знищити всі клітини кольору (вже пропонувалось у `bejeweled`, `columns`; тут — Mad Block).
- `+ui:bonus-roulette` — рулетка, що визначає бонус після події.
- `+card:horizontal-trio-reorder`, `+card:column-drill-block`, `+card:dead-row-blocker`, `+card:chain-only-clear`, `+card:inverted-danger-line`.

## Джерела
- ⭐ [Wikipedia: Mad Blocker Alpha](https://en.wikipedia.org/wiki/Mad_Blocker_Alpha) — горизонтальний рух, 4+ однакових, ланцюги й рулетка, Mad / Concrete / Bomb, Bad Blocks і Moke → ряд десатуронів, що чистяться лише ланцюгами; розробка й дати.
- [The Sixth Axis: рецензія](https://www.thesixthaxis.com/?p=68542) — трійки рядком, без обертання, ланцюг = 8+ блоків за раз, Story з цілями (10 000 очок до таймера, 5 ланцюгів), Endless, Tower з червоною лінією й перешкодами.
- [Pocket Gamer: рецензія](https://www.pocketgamer.com/mad-blocker-alpha/review) — «горизонтальні Columns», бонуси серед майбутніх трійок і на □/△/○, три ефекти, мапа світу Story, Tower зі скиданням вежі.
- [The Sixth Axis: інтервʼю](https://www.thesixthaxis.com/2010/11/09/interview-mad-blocker-alpha/) — 17 етапів Story, Endless Classic / Mad, Tower, локальні рекорди, вороги Moke.
- YouTube: пошук «Mad Blocker Alpha PSP gameplay».

## Непевне
- (?) Розмір колодязя і чи розпадається трійка після посадки (кожен блок падає окремо, як у Columns), — не описано.
- (?) Як саме переставляються кольори в трійці (цикл, обмін пари) і якою кнопкою.
- (?) «Ланцюг»: The Sixth Axis — «8+ блоків за раз»; Wikipedia — «складати багато блоків, щоб запускати великі ланцюги» (можливо, каскади); визначення можуть не збігатися.
- (?) Що робить Bad Block і як саме ланцюг прибирає десатурони (сусідство чи будь-де на полі).
- (?) Чи бонуси приходять лише з рулетки, чи й у потоці трійок — Pocket Gamer каже «серед майбутніх трійок», Wikipedia — «рулетка вирішує».
- (?) Tower: чи збіги шкодять висоті вежі й що саме «скидає» вежу; Pocket Gamer і The Sixth Axis описують по-різному.
- (?) Mad Blocker HD для PS Vita — лише за заголовком новини Push Square, не відкривав.
