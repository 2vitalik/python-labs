---
title: Mr. Do!
slug: mr-do
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1982
platforms: [arcade, ColecoVision, Atari 2600, Atari 8-bit, Apple II, C64, MSX, Game Boy, SNES, Neo Geo]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mr._Do!", best: true, note: "геймплей повністю: вишні, яблука, мʼяч, EXTRA, їжа, діамант, 4 способи пройти раунд"}
  - {kind: fandom, url: "https://strategywiki.org/wiki/Mr._Do!/Gameplay", note: "StrategyWiki: керування і таблиця очок"}
  - {kind: other, url: "https://www.arcade-history.com/game/1684/mr.-do", note: "очки за яблука 1000–8000, діамант 8000 + кредит"}
  - {kind: other, url: "https://www.arcadeclub.co.uk/games/mr-do/", note: "короткий опис правил"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/mr-do", note: "KLOV: дані автомата"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mr+Do+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, gravity-fall, push-object, touch-death, environment-death, player-death, collect-all, destroy-all-enemies, chase-player, projectile-shot, combo-multiplier, event-points, temporary-modes, spawn-points, spawn-schedule, sequential-levels, progress-acceleration, score-records, status-panel, +dig-terrain, +delayed-fall, +boomerang-projectile, +multi-kill-bonus, +letter-collection, +alt-win-conditions, +enemy-mutation, +bonus-item-spawn]
proposes: ["+trigger:counter", "+trigger:all_gone", "+trigger:picked", "+effect:fall", "+effect:bounce", "+effect:freeze", "+effect:lives", "+effect:combo", "+effect:reset_combo", "+cond:chain", "+cond:prop", "+card:boomerang-projectile", "+card:multi-kill-bonus", "+card:letter-collection", "+card:alt-win-conditions", "+card:enemy-mutation", "+ui:letter-progress"]
author: opus
date: 2026-11-02
---

# Mr. Do! — клоун копає тунелі, збирає вишні й кидає мʼяч-бумеранг

## Суть
Клоун Mr. Do прокопує тунелі в саду, збирає вишні й захищається від монстрів двома способами: мʼячем, що відскакує тунелями до першого монстра, і яблуками, які падають, коли під ними прокопати. Головна новинка серед «копальних» аркад — **чотири незалежні способи пройти раунд**: зібрати всі вишні, знищити всіх монстрів, скласти слово EXTRA з букв-монстрів або знайти діамант у розбитому яблуці. Рахунок будується на ланцюжках: 8 вишень підряд, кілька монстрів під одним яблуком.

## Поле і час
- Сад — сітка землі з кількома готовими тунелями; у центрі — «гніздо», звідки виходять монстри (?) щодо точного розміру поля.
- Шари: земля/тунель (стан клітини) + обʼєкти (вишні групами по 8, яблука) + рухомі сутності.
- Real-time; монстри стають агресивнішими й швидшими з раундами (?).
- Внизу екрана — рядок EXTRA, де «світиться» поточна буква.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr. Do | player | життя | рух 4 напрямки, прокопує землю → тунель; кидає мʼяч; штовхає яблуко вбік |
| Земля | terrain | diggable | Mr. Do проходить → тунель; звичайні монстри не входять |
| Вишня | pickup | групи по 8 | збір +50; 8 з групи без паузи → +500 |
| Яблуко | object | falling (із затримкою) | підкопав — хитається й падає тунелем; падіння > власної висоти → розбивається; давить монстрів і Mr. Do |
| Діамант | pickup | — | іноді в розбитому яблуці; збір → кінець раунду, 8000 і безкоштовний кредит |
| Мʼяч сили (power ball) | projectile | затримка відновлення росте з кожним кидком | летить і відскакує по тунелях до монстра; не влучив — треба підібрати; у польоті Mr. Do беззахисний |
| Монстр (creep, червоний «динозавр») | enemy | — | гониться тунелями за Mr. Do; можуть штовхати яблука |
| Монстр-копач (multicolored) | enemy | тимчасова форма | з монстра; копає землю, «їсть» вишні на шляху; під яблуком часто гине |
| Альфа-монстр (буква EXTRA) | enemy | буква | зʼявляється на кожних 5000 очок з підсвіченою буквою; їсть яблука; знищено → буква зарахована |
| Великі сині монстри | enemy | 3 шт. | приходять разом з альфа-монстром після «їжі» |
| Гніздо / їжа | spawner → pickup | — | випускає монстрів; коли всі вийшли — стає їжею: бонус, звичайні монстри завмирають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth)` → ТО `move`, `set_cell(tunnel)`; ЯКЩО `cell(target, tunnel)` → `move`.
- КОЛИ `contact(do, cherry)` → ТО `pickup`, `score(50)`, `combo(+1)`; ЯКЩО `chain(8)` у межах групи без паузи → ТО `score(500)`; пауза → `reset_combo`.
- КОЛИ `input(fire)` → ЯКЩО `state(ball, ready)` → ТО `spawn(ball)`, `custom: «мʼяч рухається тунелями, відбиваючись від стін»`.
- КОЛИ `contact(ball, monster)` → ТО `disappear_b`, `score(500)`, мʼяч `timer(reform)` повертається до Mr. Do; кожен кидок подовжує `reform`.
- КОЛИ `custom: «мʼяч не може дістати монстра»` → ТО мʼяч лежить, доки Mr. Do його не підбере (`contact(do, ball)` → `pickup`).
- КОЛИ `contact(do|monster, apple)` збоку → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `tick` → ЯКЩО `free(below apple)` → ТО `custom: «хитання N тіків»` → `fall(apple)`.
- КОЛИ `contact(falling apple, monster|do)` → ТО `disappear_b` (Mr. Do → `lives(-1)`); монстрів забирає з собою.
- КОЛИ `custom: «яблуко впало > своєї висоти»` → ТО `disappear_a`; з ймовірністю `rng(p)` → `spawn(diamond)`.
- Очки за яблуко: 1 монстр 1000 · 2 — 2000 · 3 — 4000 · 4 — 6000 · 5+ — 8000.
- КОЛИ `counter(score, %, 5000)` → ТО `spawn(alpha_monster[current_letter])`.
- КОЛИ `contact(ball|apple, alpha_monster)` → ТО `disappear_b`, `custom: «буква EXTRA зарахована»`; ЯКЩО зібрано всі 5 → ТО `lives(+1)`, кінець раунду, катсцена.
- КОЛИ `contact(alpha_monster, apple)` → ТО `disappear_b` (зʼїв яблуко).
- КОЛИ `rng(p)` → ТО `transform(creep → digger)` (тимчасово); копач `set_cell(tunnel)` на шляху, зʼїдені вишні зменшують лічильник.
- КОЛИ `custom: «усі монстри вийшли з гнізда»` → ТО `transform(nest → food)`; КОЛИ `contact(do, food)` → ТО `score(bonus)`, `freeze(creeps)`, `spawn(alpha_monster)` (якщо нема), `spawn(blue_monster ×3)`.
- КОЛИ `all_gone(blue_monster)` | `destroyed(alpha_monster)` | `died(do)` | кінець раунду → ТО `clear_state(creeps, frozen)`; знищений альфа-монстр перетворює решту синіх на яблука.
- КОЛИ `contact(monster, do)` → ТО `lose`, `lives(-1)`.
- Перемога раунду (будь-яке): `all_gone(cherry)` · `all_gone(monsters)` · EXTRA зібрано · `picked(do, diamond)` → `next_level`.
- Поразка: 0 життів → `game_over`. Рахунок: таблиця подій, рекорди.

## Керування і ввід
- Джойстик 4 напрямки + одна кнопка (кинути мʼяч). Mr. Do рухається по сітці тунелів; поворот у землю — копання.
- Ритм гри: кинув мʼяч → беззахисний до повернення; тому ввід = вибір «бити зараз чи чекати».

## Вікна, меню, HUD
- `splash-screen` / attract mode — демо й таблиця очок.
- `game-screen`: сад + HUD: `score`, `hi-score`, `lives`, `level-number`, рядок EXTRA (`letter-progress`: зібрані букви, підсвічена поточна).
- `custom-window` — катсцена після EXTRA (мелодія Astro Boy) і заставки між раундами.
- `leaderboard` — таблиця рекордів з ініціалами (аркада).
- `end-screen` — GAME OVER.
- Переходи: attract → (монета) → раунд → (будь-яка умова перемоги) → проміжний екран → наступний раунд; смерть → той самий раунд.

## Фічі поза полем
- `levels-sequential` — раунди з наростанням складності; Electrocoin (1988) — розширена версія на 99 рівнів.
- `leaderboard-local` з ініціалами; `continue` за монету (аркада); діамант дає безкоштовний кредит.
- Hotseat на двох по черзі (?).

## Варіації й родичі
- Сиквели: Mr. Do's Castle (1983), Mr. Do's Wild Ride і Do! Run Run (1984); порти на SNES і Game Boy з новими фічами.
- Родичі: Dig Dug (копання + падаючі камені, вбивство насосом), Boulder Dash (копання + фізика без ворожих тунелів), Lady Bug (той самий автор-видавець Universal, букви EXTRA/SPECIAL).
- **Осі варіацій**: зброя — «мʼяч-бумеранг тунелями / насос впритул (Dig Dug) / лише середовище (BD)»; умова раунду — «одна / кілька альтернативних»; ворог і земля — «не копає / копає в особливій формі / проходить як привид (Dig Dug)».

## Цікавинки для курсу
- Чотири альтернативні умови перемоги раунду — 📎: ціль як список предикатів «будь-який».
- Мʼяч, що летить тунелями з відскоками й повертається із затримкою, яка росте — 🥉: рух снаряда по графу тунелів + cooldown, що зростає.
- Яблуко: хитання → падіння → розбиття від висоти + наростаючі очки за кількість розчавлених — 🥉.
- Букви EXTRA: прогрес «зібрати набір» через спеціальних ворогів, що зʼявляються на порогах очок — 📎.
- Вишні по 8 і бонус за безперервність — 🌱 (картка `combo-multiplier`).
- Гніздо → їжа → заморожування + хвиля спецворогів — 🥉: ланцюг станів.

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` (яблука) · `push-object` (яблуко вбік) · `touch-death` · `environment-death` (яблуко) · `player-death` · `collect-all` (вишні) · `destroy-all-enemies` · `chase-player` · `projectile-shot` (мʼяч) · `combo-multiplier` (8 вишень) · `event-points` · `temporary-modes` (заморожування після їжі) · `spawn-points` (гніздо) · `spawn-schedule` (альфа на 5000) · `sequential-levels` · `progress-acceleration` · `score-records` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+boomerang-projectile` «Снаряд, що повертається» · entities/combat · 🥉 · слоти {reform_delay, growth} — мʼяч сили.
  - `+multi-kill-bonus` «Наростаючі очки за кілька жертв одним ударом» · game-logic/score · 🌱 · слот {table}.
  - `+letter-collection` «Зібрати слово з букв» · game-logic/win · 📎 · слот {word}.
  - `+alt-win-conditions` «Кілька альтернативних умов перемоги» · game-logic/win · 📎.
  - `+enemy-mutation` «Ворог тимчасово змінює форму і здібності» · entities/state · 📎.
  - `+dig-terrain`, `+delayed-fall` (повтор з Dig Dug), `+bonus-item-spawn` (Dig Dug) — повтори.

## Пропозиції до словників
- `+trigger:counter` ⏳ — очки кратні 5000 → альфа-монстр.
- `+trigger:all_gone` ⏳ / `+trigger:picked` ⏳ — дві з чотирьох умов раунду.
- `+effect:fall` ⏳ · `+effect:bounce` ⏳ (мʼяч) · `+effect:freeze` ⏳ (їжа) · `+effect:lives` ⏳ (EXTRA) · `+effect:combo` / `+effect:reset_combo` ⏳ (вишні).
- `+cond:chain` ⏳ — 8 вишень поспіль.
- `+cond:prop(cell, diggable)` — земля vs тунель.
- `+ui:letter-progress` — рядок букв із зібраними/поточною (EXTRA у Mr. Do, Lady Bug).

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Mr._Do!) — вишні по 8, яблука (падіння, розбиття, діамант), мʼяч із зростаючою затримкою, копачі, альфа-монстри кожні 5000, їжа і сині монстри, чотири умови раунду, сиквели й порти.
- [StrategyWiki: Gameplay](https://strategywiki.org/wiki/Mr._Do!/Gameplay) — таблиця очок: вишня 50, 8 підряд 500, мʼяч 500 (бачив у пошуку; сторінка не відкрилась).
- [Arcade History](https://www.arcade-history.com/game/1684/mr.-do) — яблука 1000/2000/4000/6000/8000, діамант 8000 + кредит (з пошуку).
- [Arcade Club](https://www.arcadeclub.co.uk/games/mr-do/) — короткий опис правил.
- [KLOV](https://www.arcade-museum.com/Videogame/mr-do) — дані автомата.
- YouTube: пошук «Mr Do arcade gameplay».

## Непевне
- (?) Розмір поля, кількість монстрів у раунді й темп прискорення — не перевірено.
- (?) Очки за їжу і за альфа-/синіх монстрів; чи «їжа» залежить від раунду.
- (?) Чи можна штовхати яблуко крізь землю, чи лише тунелем; точна ймовірність діаманта.
- (?) Режим двох гравців по черзі — типовий для аркад, у джерелах не бачив.
- (?) StrategyWiki і Arcade History віддали 403 — значення очок взято з тексту пошукової видачі.
