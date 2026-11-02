---
title: Baba Is You
slug: baba-is-you
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [PC, Switch, Android, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Baba_Is_You", best: true, note: "суть «правила = блоки», приклади ROCK IS FLAG / WALL IS STOP, умова перемоги, 481 рівень, редактор 2021"}
  - {kind: other, url: "https://esolangs.org/wiki/Baba_Is_You", note: "гра як мова: іменники ALL/TEXT/LEVEL/GROUP, таблиця властивостей, порядок парсингу тексту"}
  - {kind: official, url: "https://hempuli.com/baba/", note: "офіційна сторінка, лінки на всі магазини"}
  - {kind: steam, url: "https://store.steampowered.com/app/736260/Baba_Is_You/"}
  - {kind: play, url: "https://hempuli.itch.io/baba", note: "itch.io"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=baba+is+you+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 65
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, interaction-table, teleport-random-exit, touch-death, environment-death, reach-exit, enemy-patrol, gravity-fall, level-unlock, in-game-editor, level-exchange, +undo-redo, +rules-as-objects, +rule-parser, +property-flags, +noun-transform, +conditional-rules, +pull-object, +swap-on-contact, +grow-spread, +world-map, +level-as-object]
proposes: ["+trigger:overlap", "+trigger:rule_formed", "+trigger:rule_broken", "+effect:set_property", "+role:word", "+ui:rules-list", "+axis:rules", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Baba Is You — правила гри лежать на полі як блоки-слова, і їх можна штовхати

## Суть
Кожен рівень — один екран-сітка, на якому, крім обʼєктів, лежать **текстові блоки**: іменники (BABA, WALL, FLAG), дієслова (IS, HAS, MAKE) і властивості (YOU, WIN, STOP, PUSH…). Рядок із трьох блоків «ІМЕННИК IS ВЛАСТИВІСТЬ», прочитаний зліва направо або згори вниз, — чинне правило рівня; розірвав рядок — правило зникло. Гравець штовхає слова, щоб переписати фізику: зняти STOP зі стін, зробити себе WIN, перетворити скелі на прапорці. Ядро гри — **таблиця взаємодій як дані, що редагуються на ходу**.

## Поле і час
- Квадратна сітка (розмір задає рівень (?)), один статичний екран; межа рівня завжди непрохідна.
- Шарів немає явно: у клітині може стояти скільки завгодно обʼєктів (і текстів) одночасно; взаємодії визначаються властивостями, а не типом клітини. FLOAT додає умовний «другий ярус».
- Покроково: хід = одне натискання напрямку або «чекати». Між ходами нічого не відбувається (немає real-time), але обʼєкти з MOVE/SHIFT/FALL діють щоходу.
- Порядок у межах ходу (спрощено, `(?)` — див. «Непевне»): рух YOU → рух MOVE/AUTO → SHIFT → перечитати правила → перетворення `X IS Y` → HAS/MAKE → знищення (DEFEAT, SINK, HOT/MELT, OPEN/SHUT, WEAK, EAT) → TELE → перевірка WIN.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Обʼєкт (Baba, Keke, Me, Flag, Wall, Rock, Water, Lava, Skull, Key, Door, Grass, Tile, Belt, Love…) | object | тип-іменник, напрям погляду, колір | сам нічого не робить; поведінка = набір властивостей із чинних правил |
| Текст-іменник (BABA, WALL, FLAG…) | object | слово | завжди PUSH (неявне правило); суб'єкт або об'єкт правила |
| Спец-іменники: TEXT · ALL · EMPTY · LEVEL · CURSOR · GROUP | object | — | TEXT — усі тексти; ALL — усі не-текстові обʼєкти; EMPTY — порожні клітини; LEVEL — сам рівень (на мапі — рівні); GROUP — збірна категорія |
| Дієслово IS | object | — | `X IS PROP` — дати властивість; `X IS Y` — перетворити всі X на Y; `X IS X` — заборонити перетворення X |
| Дієслово HAS | object | — | X при знищенні лишає Y |
| Дієслово MAKE | object | — | X щоходу створює Y у своїй клітині, якщо там ще нема Y |
| Дієслова EAT · FEAR · FOLLOW | object | — | EAT — X знищує Y у своїй клітині; FEAR — X відходить від Y; FOLLOW — X повертається до найближчого Y |
| Оператори AND · NOT | object | — | AND — кілька субʼєктів/властивостей в одному рядку; NOT — заперечення, має пріоритет над стверджувальним правилом |
| Умови ON · NEAR · FACING · LONELY | object | — | `X ON Y IS P` — лише X, що стоять на Y; NEAR — у 8-сусідстві; FACING — дивиться на Y; LONELY — X сам у клітині (префікс) |
| YOU | — (властивість) | — | обʼєкт рухається від вводу гравця; YOU може бути кілька обʼєктів одночасно — рухаються синхронно |
| WIN | — | — | YOU у клітині з WIN → рівень пройдено |
| STOP | — | — | у клітину не можна увійти |
| PUSH | — | — | зсувається при вході в нього; ланцюг PUSH зсувається цілим, якщо в кінці вільно |
| PULL | — | — | тягнеться за тим, хто відходить від нього; в нього не можна увійти |
| SINK | — | — | при спільній клітині з іншим обʼєктом зникають обидва |
| DEFEAT | — | — | знищує YOU-обʼєкти у своїй клітині |
| HOT / MELT | — | — | HOT знищує MELT у своїй клітині |
| OPEN / SHUT | — | — | OPEN і SHUT в одній клітині знищують одне одного |
| MOVE | — | — | щоходу крок уперед за поглядом; уперся — розворот |
| SHIFT | — | — | зсуває всі обʼєкти у своїй клітині в напрямку свого погляду (конвеєр) |
| SWAP | — | — | хто входить у клітину SWAP-обʼєкта, міняється з ним місцями |
| TELE | — | ≥2 обʼєкти того самого типу | обʼєкт, що став на TELE, переноситься на інший екземпляр цього типу |
| FLOAT | — | — | взаємодії «у спільній клітині» (WIN, DEFEAT, SINK, HOT, TELE, SHIFT…) діють лише між однаково FLOAT-обʼєктами; PUSH/STOP не зачіпає |
| WEAK | — | — | знищується, коли в нього входять або він упирається |
| MORE | — | — | щоходу розростається в сусідні вільні клітини |
| FALL | — | — | рухається вниз до упору (у редакторі — і в інших напрямках (?)) |
| UP · DOWN · LEFT · RIGHT | — | — | примусово повертає погляд обʼєкта |
| SLEEP | — | — | обʼєкт не рухається (навіть YOU/MOVE) |
| HIDE · SAFE · BOOM · WORD · BEST · RED/BLUE · BONUS · DONE · END | — | — | невидимий · незнищенний (крім виходу за межі) · знищує все в квадраті навколо, розмір — за кількістю BOOM · обʼєкт працює як слово своєї назви (?) · косметика/колір (?) · спецефекти мапи й фіналу (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Мета-правила (як гра читає слова):
- КОЛИ `after(move)` → ТО `custom: «перечитати всі рядки текстів зліва направо і згори вниз; кожна валідна послідовність ІМЕННИК [AND ІМЕННИК] [умова] ДІЄСЛОВО ВЛАСТИВІСТЬ|ІМЕННИК [AND …] — чинне правило»`.
- КОЛИ `after(custom: «перечитати правила»)` → ЯКЩО `custom: «чинне X IS P»` → ТО `set_state(X, P)` для всіх X; правило зникло → `clear_state(X, P)`.
- КОЛИ `after(custom: «перечитати правила»)` → ЯКЩО `custom: «чинне X IS Y, нема X IS X»` → ТО `transform(X → Y)` для всіх X.
- КОЛИ `after(custom: «перечитати правила»)` → ЯКЩО `custom: «чинні X IS NOT P і X IS P»` → ТО заперечення перемагає: P знято (?).
- Неявні правила: `TEXT IS PUSH`, межа рівня — STOP; на мапі `CURSOR IS SELECT` (?).

Рух і зіткнення:
- КОЛИ `input(dir)` → ТО `move(YOU, dir)` для всіх YOU-обʼєктів; `input(wait)` → хід без руху.
- КОЛИ `contact(a, b)` → ЯКЩО `state(b, STOP)` → ТО `block`.
- КОЛИ `contact(a, b)` → ЯКЩО `state(b, PUSH)` → ЯКЩО `free(cell_behind)` (з урахуванням ланцюга) → ТО `push`; інакше `block`.
- КОЛИ `leave(a, cell)` → ЯКЩО `occupied(cell_behind_a, PULL)` → ТО `pull(b)`.
- КОЛИ `contact(a, b)` → ЯКЩО `state(b, SWAP)` → ТО `swap(a, b)`.
- КОЛИ `tick` → ЯКЩО `state(a, MOVE)` → ТО `move(a, facing)`; `blocked(a)` → `face(a, reverse)`.
- КОЛИ `tick` → ЯКЩО `state(s, SHIFT)` → ТО `move(all_in_cell(s), facing(s))`.
- КОЛИ `tick` → ЯКЩО `state(a, FALL)` → ТО `fall(a)`.
- КОЛИ `tick` → ЯКЩО `state(a, MORE)` → ТО `spawn_at(copy(a), free_neighbors4)`.

Знищення (на кінець ходу, спільна клітина — `contact` у сенсі «спільна клітина», з урахуванням FLOAT):
- КОЛИ `contact(you, defeat)` → ТО `disappear_a` (YOU).
- КОЛИ `contact(sink, any)` → ТО `disappear_both`.
- КОЛИ `contact(melt, hot)` → ТО `disappear_a` (MELT).
- КОЛИ `contact(open, shut)` (або вхід одного в інший) → ТО `disappear_both`.
- КОЛИ `contact(weak, any)` або `blocked(weak)` → ТО `disappear_a`.
- КОЛИ `contact(x, y)` → ЯКЩО `custom: «чинне X EAT Y»` → ТО `disappear_b`.
- КОЛИ `destroyed(x)` → ЯКЩО `custom: «чинне X HAS Y»` → ТО `spawn(Y)` у клітині X.
- КОЛИ `tick` → ЯКЩО `custom: «чинне X MAKE Y»` і `not occupied(cell_x, Y)` → ТО `spawn(Y)`.
- КОЛИ `contact(a, tele)` → ТО `teleport(a, other_instance_of(tele_kind))`.

Перемога/поразка:
- КОЛИ `contact(you, win)` або `state(a, YOU) and state(a, WIN)` → ЯКЩО однаковий FLOAT → ТО `win`, `next_level` (повернення на мапу).
- ЯКЩО `custom: «чинне LEVEL IS WIN»` → ТО `win` одразу (?); `LEVEL IS X` на мапі — перетворює сам рівень.
- Поразки як події нема: коли `count(YOU, ==, 0)` — гра триває, але ходити нікому → `custom: «застряг: лише undo або restart»`. Деякі правила (MOVE/SHIFT) можуть самі відновити `X IS YOU`.
- Рахунку нема; прогрес — кількість пройдених рівнів і бонусів на мапі.

## Керування і ввід
- Стрілки/WASD — крок YOU-обʼєктів (усіх одночасно); Space — пропустити хід (обʼєкти з MOVE/SHIFT ходять).
- Z — undo без обмежень (до самого старту); R — рестарт рівня (рестарт сам скасовується через Z).
- Esc — пауза; на мапі стрілки рухають курсор-рамку між рівнями, Enter — увійти.
- Геймпад і тач (мобільні — екранні стрілки/свайпи) (?).

## Вікна, меню, HUD
- `splash-screen` — лого Hempuli / назва.
- `main-menu` — Play · Play levels (рівні спільноти, після оновлення 2021) · Level editor · Settings · Credits · Exit.
- `save-slots` — три слоти збереження з прогресом; вибір пакета (Baba Is You / New Adventures / Museum) (?).
- `map-window` — світова мапа: острови-зони, рівні як клітинки з назвою, лічильник пройдених і бонусів; мапа — сама сітка з правилами (`CURSOR IS SELECT`), яку пізніше можна переписувати як рівень.
- `game-screen` — поле на весь екран; HUD мінімальний: назва рівня на вході; при відсутності YOU — підказка про undo/restart (?).
- `pause-menu` — Resume · Restart · Return to map · Settings · Return to menu, плюс **список чинних правил рівня** (`rules-list`).
- `settings-window` — гучність музики/звуків, повноекранний режим, ремап керування, вимкнення «хитання» спрайтів/частинок, вищий контраст, сітка (?).
- `editor-window` — редактор: палітра обʼєктів і слів, розміщення по клітинах, властивості рівня (назва, розмір, палітра, музика), тест-запуск, публікація з кодом рівня.
- `level-select` для рівнів спільноти — введення коду рівня, вибрані/featured рівні.
- Переходи: main-menu → save-slots → map-window → (Enter на рівні) game-screen → (WIN) map-window з відкритими сусідніми рівнями; Esc → pause-menu → map-window.

## Фічі поза полем
- `undo` ∞ + `restart-level` (undoable) — без них гра неможлива, бо смерть YOU = глухий кут.
- `world-map` з `level-unlock`: пройдений рівень відкриває сусідні клітинки мапи; зони відкриваються порогом кількості пройдених; бонус-сфери; фінальні рівні змінюють саму мапу.
- `autosave` прогресу в слотах; `achievements` (Steam).
- `level-editor` + `level-sharing` (2021): спільнотні рівні з кодами, `user-levels-browser`; додаткові паки New Adventures і Museum.
- `animation-toggle` (хитання спрайтів), `remap-controls`, `fullscreen`.

## Варіації й родичі
- Пакети: основна гра (231 рівень), Museum (88), New Adventures (162) — нові слова й умови.
- Предки: PuzzleScript-рівні з правилами-об'єктами, «Nomic»-ідея гри, де правила змінюються ходами; спадкоємці — Hempuli-джеми, ігри «rule-editing» (Is This Game?, LOK — слова як команди).
- **Осі варіацій:** звідки правила — фіксовані в коді / лежать на полі / в інвентарі; читання — лише горизонталь / гориз.+верт.; граматика — `X IS P` / + `HAS/MAKE` / + умови `ON/NEAR/FACING`; хто YOU — один / клас / жоден (пазл на «відновити YOU»).
- Тест на межу сімʼї: штовхання тут — інструмент, ядро — «відкрити правило», тому `thinky`, а не `push-slide`.

## Цікавинки для курсу
- Властивості як прапорці на типі обʼєкта + перевірки «на вході в клітину» (STOP/PUSH) і «на кінець ходу в спільній клітині» (DEFEAT/SINK/HOT) — 🥈: дві фази, порядок, FLOAT як фільтр.
- Парсер правил із сітки слів (рядки й стовпці, AND, NOT, пріоритет заперечення) — 🥇: граматика + повторний розбір після кожного ходу.
- `X IS Y` — масова трансформація з блокуванням `X IS X` — 🥉.
- Ланцюгове штовхання з PULL і SWAP в одному ході — 🥈: черга переміщень, конфлікти.
- Undo ∞ через знімки стану (`state-as-data`) — 📎, але обовʼязкове, бо поразка = «застряг».
- Мапа світу як рівень із тими самими правилами (`LEVEL IS …`) — 👑 як ідея самовкладеності; для курсу — 🥉 за просту мапу з відкриттям сусідів.
- MORE (розростання) і MAKE (генерація щоходу) — 📎 кожне.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ рух YOU; `push-object` ↔ PUSH (з ланцюгом); `impassable-cells` ↔ STOP і межа; `interaction-table` ↔ серце гри — таблиця «властивість × властивість», тут редагована; `teleport` + `teleport-random-exit` ↔ TELE; `touch-death` ↔ DEFEAT; `environment-death` ↔ SINK, HOT/MELT; `reach-exit` ↔ YOU на WIN; `enemy-patrol` ↔ MOVE (туди-сюди); `gravity-fall` ↔ FALL; `sequential-levels` + `level-unlock` + `level-select` ↔ мапа; `in-game-editor` + `editor-palette` + `editor-playtest` + `level-exchange` ↔ редактор 2021 з кодами; `save-progress` ↔ слоти; `state-as-data` ↔ undo; `movement-animation` + `idle-animation` ↔ «хитання» спрайтів; `game-pause` + `settings-window`.
- **Нема** → пропозиції карток:
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 · слот {depth: ∞} — як у Sokoban.
  - `+rules-as-objects` «Правила як обʼєкти на полі» · game-logic/rules · 🥇 — правило існує, доки рядок слів складено.
  - `+rule-parser` «Розбір правил із сітки слів» · game-logic/rules · 🥇 · слот {grammar: is|is+has|is+cond} — дитина `rules-as-objects`.
  - `+property-flags` «Поведінка = набір властивостей типу» · entities/state · 🥈 — замість класу на кожен обʼєкт.
  - `+noun-transform` «Масове перетворення типу X → Y» · entities/state · 🥉.
  - `+conditional-rules` «Умовні правила ON/NEAR/FACING» · game-logic/rules · 🥈.
  - `+pull-object` «Тягнення» · entities/legality · 📎 — вже запропоновано в Sokoban.
  - `+swap-on-contact` «Обмін місцями при вході» · entities/interact · 📎.
  - `+grow-spread` «Розростання в сусідні клітини (MORE)» · entities/spawn · 📎.
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉.
  - `+level-as-object` «Рівень як обʼєкт на мапі, що підпадає під правила» · levels/progression · 👑.
  - `+wait-turn` «Пропуск ходу» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:overlap(a, b)` — спільна клітина **на кінець ходу** (відрізняється від `contact`, що спрацьовує при вході й може блокувати).
- `+trigger:rule_formed(rule)` / `+trigger:rule_broken(rule)` — правило зʼявилось/зникло після перечитування тексту.
- Вжито наявні `input`, `state`, `facing`, `adjacent_count`, `transform`, `pull`, `swap`, `fall`, `face`, `spawn_at`, `map-window`, `editor-window`, `undo`, `level-sharing`, `world-map` — без нових пропозицій.
- `+effect:set_property(kind, prop)` — дати властивість усім обʼєктам типу (на відміну від `set_state` однієї сутності).
- `+role:word` — текстовий блок, що одночасно обʼєкт на полі (PUSH) і токен граматики правил.
- `+ui:rules-list` — список чинних правил у паузі (гра підказує, що зараз «закон»).
- `+axis:rules` — `fixed` (класика) · `mutable` (гравець змінює правила під час гри: Baba).
- `+axis:undo` — тут `unlimited`, і рестарт теж скасовується.

## Джерела
- ⭐ [Wikipedia: Baba Is You](https://en.wikipedia.org/wiki/Baba_Is_You) — суть механіки, приклади правил (WALL IS STOP, ROCK IS FLAG, ROCK IS ROCK), умова перемоги, «рівні не провалюються», 481 рівень (231 + 88 + 162), Baba Make Level (17.11.2021), мобільні версії 22.06.2021.
- [Esolangs: Baba Is You](https://esolangs.org/wiki/Baba_Is_You) — гра як мова: спец-іменники TEXT/ALL/LEVEL/GROUP/EMPTY, таблиця властивостей (YOU, PUSH, PULL, STOP, MOVE, SHIFT, FALL, DEFEAT, HOT/MELT, OPEN/SHUT, SINK, BOOM, SAFE, FLOAT, HIDE, PHANTOM, REVERSE, AUTO); дієслів і умов не описує.
- [Офіційна сторінка](https://hempuli.com/baba/) — магазини (Steam, itch, Humble, eShop, Google Play, App Store), прескіт; зроблено в Multimedia Fusion 2.
- [Steam](https://store.steampowered.com/app/736260/Baba_Is_You/) — «over 200 levels», досягнення, реліз 13.03.2019.
- YouTube: [пошук «baba is you gameplay»](https://www.youtube.com/results?search_query=baba+is+you+gameplay).

## Непевне
- (?) Описи дієслів і умов (HAS, MAKE, EAT, FEAR, FOLLOW, ON, NEAR, FACING, LONELY), пріоритет NOT, `X IS X`, `TEXT IS PUSH`, `LEVEL IS WIN`, а також WEAK, MORE, SWAP, SLEEP, TELE, WORD — з памʼяті: Wikipedia й esolangs їх не розписують, Baba Is Wiki (fandom) віддає 402, StrategyWiki — 403.
- (?) Межа рівня: у грі блокує рух; esolangs згадує знищення обʼєкта, що виходить за межі (SAFE не рятує) — можливо, лише для зміни розміру рівня.
- (?) Точний порядок фаз у межах ходу (MOVE до/після YOU, коли саме TELE і перетворення) — з памʼяті; на fandom-вікі є сторінка про порядок, але вона недоступна.
- (?) SHUT не є STOP сам по собі — на рівнях двері зазвичай мають окреме `DOOR IS STOP` або лише SHUT; не перевірено.
- (?) TELE з ≥3 екземплярами — випадковий вихід (тоді `random: runtime` для таких рівнів).
- (?) Набір слів пізніх паків (WORD, BOOM, POWER/POWERED, IDLE, WITHOUT, ABOVE/BELOW, SEEING, WRITE, AUTO, YOU2, GROUP) — частина є лише в New Adventures / редакторі; esolangs згадує FALL з напрямком і NUDGE — можливо, з редактора/модів.
- (?) Пункти settings-window і підказка «Z — undo» при втраті YOU — з памʼяті.
- Вікіпедія суперечить сама собі щодо кількості нових рівнів в оновленні 2021 (150 vs 250).
