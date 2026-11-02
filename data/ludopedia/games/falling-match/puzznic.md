---
title: Puzznic
slug: puzznic
family: falling-match
also: [push-slide, thinky]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1989
platforms: [arcade, NES, Game Boy, Amiga, Atari ST, C64, ZX Spectrum, Amstrad CPC, MS-DOS, PC Engine, PlayStation]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzznic", note: "історія, платформи, «шлях» рівнів"}
  - {kind: official, url: "https://games.speccy.cz/data/info/Puzznic.txt", best: true, note: "оригінальна інструкція (ZX): керування, правило зникнення, очки, retry-меню"}
  - {kind: fandom, url: "https://www.puzznic.com/", note: "World of Puzznic — каталог версій і клонів"}
  - {kind: play, url: "https://wizznic.org/", note: "Wizznic — відкритий клон з редактором рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzznic+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 75
mechanics: [gravity-fall, cell-click, keyboard-controls, push-object, impassable-cells, time-out, time-bonus, event-points, combo-multiplier, player-death, unsolvable-states, sequential-levels, level-select, level-from-txt, in-game-editor, game-pause, +connected-group-pop, +chain-reaction, +cascade-gravity, +carrier-platform, +clear-after-settle, +grab-and-slide, +retry-menu]
proposes: ["+trigger:input", "+trigger:settled", "+trigger:pattern", "+trigger:counter", "+cond:free", "+cond:same", "+effect:fall", "+effect:move", "+effect:clear", "+effect:restart", "+role:tile", "+role:platform", "+window:retry-menu", "+axis:gravity", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Puzznic — зсунь блок убік; однакові блоки, що стикнулись після падіння, зникають

## Суть
На екрані — стінки-лабіринт і купка блоків із візерунками. Гравець рамкою-курсором хапає блок і зсуває його вліво/вправо; підняти блок не можна, вниз його тягне гравітація. Коли все зупинилось, блоки одного візерунку, що торкаються (по горизонталі чи вертикалі), зникають. Мета — прибрати **всі** блоки до кінця таймера; якщо лишився непарний «сирота», рівень програно. Ядро — планування порядку падінь, а з трьома однаковими блоками — синхронізація, щоб усі три зійшлися одночасно.

## Поле і час
- Невеликий прямокутник (≈ 8–10 × 8–12 клітин (?)) зі стінами довільної форми; один шар блоків + стіни + (у пізніх рівнях) рухомі платформи.
- Час: зворотний таймер рівня (real-time), але самі ходи дискретні — блок зсувається рівно на одну клітину. Фізика (падіння, зникнення) відпрацьовує анімацією; поки щось падає, збігів не перевіряють.
- Платформи-ліфти рухаються самі з постійним темпом незалежно від гравця (?), що додає ходам «таймінг».
- Випадковості нема: рівні фіксовані, розвʼязок детермінований.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-рамка | player | позиція клітини | вільно ходить по полю; з затиснутою кнопкою «тримає» блок |
| Блок | tile | візерунок (≈ 8 типів: ромб, куля, піраміда, хрест…) | зсувається на 1 вбік, якщо там порожньо; падає без опори; зникає з сусідом того ж візерунку |
| Стіна | static | — | непрохідна; опора для блоків |
| Платформа-ліфт | terrain | напрям (верт./гориз.), межі ходу (?) | їздить туди-сюди; блок на ній їде разом (і так піднімається вгору) |
| Таймер рівня | — | секунди | 0 → втрата спроби |
| Лічильник спроб (lives/retries) | — | кількість (3 (?)) | зменшується за програш рівня або ручний retry |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` без кнопки → ТО `move(cursor, dir)` (4 напрямки, по клітинах).
- КОЛИ `input(fire + left|right)` → ЯКЩО `occupied(cursor, block)` `and free(side_cell)` → ТО `move(block, side)`, курсор іде за ним; інакше `block` (не штовхає інші блоки, вгору/вниз не рухає).
- КОЛИ `tick` → ЯКЩО `free(cell_below)` → ТО `fall(block)` (без опори — падає до стіни/блоку/платформи).
- Під час падіння блок, що пролітає повз однаковий, **не** зникає: перевірка лише коли все стоїть.
- КОЛИ `custom: «settled — усі блоки нерухомі»` → ЯКЩО `pattern(group(2+, same_pattern, adj4))` → ТО `clear(group)` (усі звʼязані однакові разом — так три сусіди зникають одночасно), `score(+n per block)`.
- КОЛИ `after(clear)` → ТО `fall(unsupported)`; ЯКЩО знову `pattern(group)` → ТО `clear`, `combo(+1)` — ланцюг «без участі джойстика» дає більший бонус.
- КОЛИ `pattern(group(3+))` за один раз → ТО `score(bonus)` (більше двох блоків одночасно).
- КОЛИ `tick` → ЯКЩО `occupied(platform, block)` → ТО `move(block, with platform)` (`custom: «carrier»`); блок може зісковзнути з платформи вбік, якщо його зсунути.
- КОЛИ `all_gone(block)` → ТО `win` рівня: `score(level_bonus)` + `score(time_left × k)` → `next_level`.
- КОЛИ `timer(level, ==, 0)` → ТО `lives(-1)`, `restart` рівня.
- КОЛИ `custom: «є візерунок, якого лишився рівно 1 блок»` → ТО `custom: «impossible — рівень програно»`, `lives(-1)` (?).
- КОЛИ `input(retry)` → ТО `restart` рівня з повним таймером (коштує спробу (?)).
- КОЛИ `lives == 0` → ТО `game_over` (`game-over-continue` в аркаді).
- Перемога: поле без блоків. Поразка: таймер / безвихідь / кінець спроб. Рахунок: за блок + бонуси за 3+ одночасно, за ланцюг, за рівень, за залишок часу.

## Керування і ввід
- Джойстик/стрілки — рух курсора по клітинах; утримання fire над блоком + ←/→ — зсув блоку на одну клітину (кожне натискання — крок).
- Клавіша R (ZX) — меню: продовжити / retry / вийти; на ZX можна перемкнути показ блоків цифрами чи графікою.
- Режим «програма гравітації» — Gravnic у NES-версії (окремий режим): гравець змінює напрям гравітації замість руху блоків (?).

## Вікна, меню, HUD
- `splash-screen` / attract → `main-menu` (1P / 2P по черзі (?)).
- `game-screen`: поле, `timer-countdown`, `score`, `hi-score`, `lives`, номер рівня (`level-number`), `remaining-counter` (лишилось блоків кожного типу — у деяких версіях праворуч (?)).
- `custom-window`: «retry-меню» — Continue / Retry / Quit (ZX R).
- `level-select` у формі дерева: після початкових рівнів гравець обирає наступну гілку («multiple puzzle paths»), тож застрягання не зупиняє гру.
- `end-screen` рівня з підрахунком бонусів (блоки, час) → наступний; `game-over-continue` в аркаді.
- Переходи: main-menu → game-screen ↔ retry-меню → end-screen рівня → вибір гілки → game-screen; таймер/безвихідь → «Time over / Impossible» → retry або game over.

## Фічі поза полем
- `levels-sequential` з розгалуженням (вибір шляху) — `world-map`-подібна прогресія.
- `restart-level` (retry) як обмежений ресурс — спроби.
- `leaderboard-local` (аркада).
- Клони: `level-editor` + `level-sharing` (Wizznic), паки рівнів.
- `undo` — в оригіналі нема (лише retry).

## Варіації й родичі
- Taito Flipull/Plotting — графічна і частково механічна спорідненість. Наступники-клони: Brix (Amiga, 1993), Wizznic, Th!nk Cross, Blox, Germinal, Addled (за каталогом World of Puzznic).
- Gravnic (режим NES Puzznic) — той самий збіг, але хід = зміна напряму гравітації для всіх блоків.
- Родичі за механікою: Puyo (звʼязані однакові зникають після осідання), SameGame (клік по групі), Sokoban (зсув без підйому).
- **Осі варіацій**: мінімум для зникнення (2 / 3) · хто рухає (курсор-рука / гравітація всього поля) · перевірка (після осідання / на льоту) · перешкоди (стіни / ліфти / телепорти у клонах) · програш (таймер / безвихідь / ліміт ходів) · undo (нема / retry / покроковий).

## Цікавинки для курсу
- Фазова стан-машина «хід → падіння до спокою → пошук груп → зникнення → знову падіння» — 🥉.
- Детектор безвиході: «лишився 1 блок типу» — 🌱; повний розвʼязувач рівня BFS/DFS по станах — 🥇.
- Платформа-ліфт, що везе блоки, і взаємодія з гравітацією — 🥈.
- Три однакові: синхронізація — гарний приклад, чому перевірка лише після `settled` — 📎.
- Рівні з текстового файлу + редактор (як у Wizznic) — 🥉.
- Режим Gravnic (поворот гравітації всього поля) — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `cell-click` (курсор по клітинах) · `keyboard-controls` · `push-object` (зсув блоку, без ланцюга) · `impassable-cells` · `time-out` · `time-bonus` · `event-points` · `combo-multiplier` (ланцюг) · `player-death` (спроби) · `unsolvable-states` (безвихідь «сирота») · `sequential-levels` + `level-select` (гілки) · `level-from-txt` + `in-game-editor` (клони) · `game-pause`.
- **Нема** → пропозиції карток:
  - `+connected-group-pop` — ⏳ підтверджую; тут слоти {min: 2, adjacency: 4}.
  - `+chain-reaction` · `+cascade-gravity` — ⏳ підтверджую (Puyo, Dr. Mario).
  - `+carrier-platform` — ⏳ підтверджую (Frogger): ліфт, що везе блоки.
  - `+clear-after-settle` «Збіг перевіряється лише в спокої» · game-logic/constraints · 🌱 — повз однаковий у падінні не зникає.
  - `+grab-and-slide` «Курсор хапає обʼєкт і тягне на 1» · interface/input · 📎 (відмінно від аватара-штовхача).
  - `+retry-menu` «Retry як ресурс» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:input` · `+trigger:settled` (з Puyo) · `+trigger:pattern` · `+trigger:counter` (таймер/спроби).
- `+cond:free` · `+cond:same`.
- `+effect:fall` · `+effect:move` · `+effect:clear` · `+effect:restart`.
- `+role:tile`; `+role:platform` — ліфт (кандидат з корпусу; у таблиці записано `terrain`).
- `+window:retry-menu` — Continue / Retry / Quit посеред рівня.
- `+axis:gravity` — `naive` для окремих блоків (кожен блок 1×1, тому naive = cascade); у Gravnic — `directional`.
- `+axis:undo` — `none` (лише retry).

## Джерела
- ⭐ [Інструкція Puzznic (ZX, games.speccy.cz)](https://games.speccy.cz/data/info/Puzznic.txt) — керування fire+←/→, зникнення лише після зупинки, бонуси за 3+ і ланцюг, бонус часу, R-меню.
- [Wikipedia: Puzznic](https://en.wikipedia.org/wiki/Puzznic) — Taito 1989, порти, гілки рівнів, рухомі платформи, звʼязок з Flipull.
- [World of Puzznic](https://www.puzznic.com/) — каталог версій і клонів (PS1, MAME, Th!nk Cross, Blox, Germinal, Addled).
- [Wizznic](https://wizznic.org/) — відкритий клон з редактором (блоки «важкі», лише вбік).
- YouTube: пошук «puzznic arcade gameplay».

## Непевне
- (?) Розмір поля і кількість типів блоків — з памʼяті.
- (?) Програш при «сироті» (1 блок типу) — підтверджено лише вторинним джерелом (ретейл-опис), а не інструкцією.
- (?) Скільки спроб і чи коштує retry спробу — інструкція ZX каже лише «retries».
- (?) Поведінка ліфтів (траєкторія, чи давлять блоки, чи можна зсунути на ліфт) — Wikipedia пише лише «shifting platforms».
- (?) Gravnic у NES-версії — з одного вторинного джерела.
