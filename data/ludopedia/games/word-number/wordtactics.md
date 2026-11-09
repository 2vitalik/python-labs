---
title: WordTactics
slug: wordtactics
aka: [Word Tactics]
family: word-number
also: [falling-match]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2020
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1463350/WordTactics/", best: true, note: "опис, «How To Play», стратегія, скриншоти з Tile Key і таблицями рекордів"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2345629870", note: "Developer's Strategy Guide: трей входу, сітка, трей виходу, 5 режимів з розмірами сіток і квотами рівня, кислота/вогонь/дерево/камінь"}
  - {kind: other, url: "https://steamcommunity.com/stats/1463350/achievements", note: "досягнення: довжина слова, бали за слово й партію, рівні, швидкість"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=WordTactics+steam+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [drag-drop-piece, cell-click, gravity-fall, word-validation, next-queue, event-points, score-records, leaderboard, profile-stats, stats-window, achievements-window, sequential-levels, progress-acceleration, mode-select, explode-area, destructible-blocks, no-moves-left, completion-detection, game-screen, main-menu, help-window, settings-window, codex-window, +path-trace-word, +word-length-scoring, +bonus-tile-tier, +hold-word-grow, +prefix-only-input, +letter-tray-drop, +wildcard-tile, +acid-tile, +double-letter-tile, +stone-blocker-tile, +game-comparison]
proposes: ["+cond:is_prefix", "+cond:path_adjacent6", "+ui:word-preview", "+ui:level-progress", "+ui:input-tray", "+window:game-comparison", "+feature:game-length", "+card:hold-word-grow", "+card:prefix-only-input", "+card:letter-tray-drop", "+card:acid-tile", "+card:wildcard-tile"]
author: opus
date: 2026-11-09
---

# WordTactics — кидай літери з трею в стовпці, складай слова з сусідніх плиток і не здавай їх, поки не виростуть

## Суть
Пасьянс-словесник: у треї до 6 випадкових літер, гравець обирає будь-яку і кидає в стовпець сітки, де вона падає донизу. Слово складають кліками по сусідніх плитках; здане слово зникає, решта осідає. Головна тактика — не здавати готове слово, а тримати його на полі й нарощувати (TALK → TALKED), бо довжина множить рахунок. Кожен рівень додає новий тип спецплитки — бонусні, руйнівні й плитки-сміття, а камінь урешті заповнює сітку й закінчує гру.

## Поле і час
- Сітка зі стовпців, зсунутих на пів клітини через один (як у Bookworm): «торкаються» — сусіди у своєму й сусідніх стовпцях, тобто фактично гекс-сусідство.
- Розміри за режимом (з гайда розробника): Short — 5 стовпців висотою 5/4 (23 клітини); Medium — 6 стовпців 6/5 (33); Long — 7 стовпців 6/5 (39); Infinite і Survival — велика сітка «7×6».
- Гравітація вниз: кинута літера падає на найвищу зайняту клітину стовпця; після зарахування слова плитки над ним падають.
- Хід = одна дія: кинути літеру з трею або здати слово. Таймера нема, але час партії пишеться в статистику й досягнення («Speedy Speller» — 2000 очок швидше за 30 хв).
- Рівні всередині партії: після N зарахованих літер — новий рівень (Short — 12, Medium і Long — 19, Infinite — 50, Survival — 19).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайна літера | tile | буква, цінність (у куті: S 2, A 3, K 15, X 17…) | падає в стовпець; бере участь у слові |
| ? (джокер) | tile | цінність 0 | замінює будь-яку літеру, очок не додає |
| Подвійна літера (синя буква) | tile | цінність ×2 | у слові дає вдвічі більше очок |
| Зелена плитка | tile | +0.5 | додає 0.5 до бонусу слова |
| Синя плитка | tile | +1.0 | додає 1.0 до бонусу слова |
| Фіолетова плитка | tile | +1.5 | додає 1.5 до бонусу слова |
| Кислотна плитка | hazard | літера + кислота | коли падає на плитку, знищує плитку під собою й займає її місце |
| Вогняна плитка | hazard | літера + полумʼя | коли бере участь у зарахованому слові — вибухає й знищує сусідні плитки |
| Дерево | object | не літера | у слово не входить; руйнується кислотою й вибухом |
| Камінь | static | не літера | у слово не входить і не руйнується; поступово заповнює сітку |
| Трей входу | spawner | до 6 плиток | кожне кидання додає нову випадкову плитку (літеру чи спецплитку) |
| Трей виходу | zone | приймає будь-яку довжину | показує вибрані літери; приймає лише початок справжнього слова |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `spawn_at(tile, input_tray)` — до 6 плиток.
- КОЛИ `input(drag tile → column)` → ЯКЩО `free(column)` → ТО `place(player, tile)`, `fall(tile)`, `spawn_at(tile, input_tray)`.
- КОЛИ `input(click tile)` → ЯКЩО `custom: «плитка торкається попередньо вибраної»` and `custom: «вибрані літери — початок слова зі словника»` → ТО `custom: «плитка йде у трей виходу»`; інакше `block`.
- КОЛИ `input(click tile in output tray)` → ТО `custom: «зняти вибір з неї і всіх наступних»`.
- КОЛИ `input(score word)` → ЯКЩО `in_dictionary(word)` → ТО `score(custom: «сума цінностей × множник довжини + бонуси спецплиток»)`, `clear(word)`, `fall(tiles above)`, `counter(level_letters, +len)`.
- КОЛИ `input(score word)` → ЯКЩО `custom: «гравець не здає слово»` → ТО `custom: «слово лишається на полі; до нього можна докидати літери й здати довше»`.
- КОЛИ `input(select ?)` → ТО `custom: «джокер грає роль будь-якої літери, цінність 0»`.
- КОЛИ `custom: «у слові подвійна літера»` → ТО `custom: «цінність цієї літери ×2»`.
- КОЛИ `custom: «у слові зелена / синя / фіолетова плитка»` → ТО `counter(word_bonus, +0.5 / +1.0 / +1.5)`.
- КОЛИ `contact(acid, tile_below)` → ЯКЩО `custom: «кислота впала на плитку»` → ТО `disappear(tile_below)`, `fall(acid)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «у зарахованому слові була вогняна плитка»` → ТО `explode(adjacent, 1)` — гинуть сусіди, крім каменю.
- КОЛИ `input(click wood or stone)` → ТО `block` — не входять у слова.
- КОЛИ `contact(acid, stone)` → ТО `block` — камінь не руйнується; кислоту можна «скинути» на камінь, щоб звільнити трей.
- КОЛИ `counter(level_letters, >=, quota)` → ТО `counter(level, +1)`, `custom: «у розподілі зʼявляється новий тип плитки, розподіл літер гіршає»`.
- КОЛИ `no_moves(player)` → ЯКЩО `custom: «сітка повна — плитку з трею нікуди кинути»` → ТО `game_over`, `window(game-comparison)`.
- КОЛИ `game_start` → ЯКЩО `mode(infinite)` → ТО `custom: «каменю нема — гра може тривати безкінечно»`.
- КОЛИ `game_start` → ЯКЩО `mode(survival)` → ТО `custom: «рівень 1 має розподіл літер і спецплиток рівня 14»`.
- Перемога: нема — рахунок проти рекордів · Поразка: сітка повна · Рахунок: сума за слова; довжина — мультиплікативний бонус («подовжити на 2 літери — подвоїти»).

## Керування і ввід
- Миша: перетягнути плитку з трею входу на верх стовпця (можна будь-яку з 6, решта чекає).
- Клік по плитках сітки по черзі — набір слова; клік по літері у треї виходу — відкат вибору до неї.
- Кнопка зарахування під треєм виходу; поруч — превʼю очок поточного слова.
- Кнопки вгорі ліворуч: вихід, налаштування, ? (Tile Key), книжка (?), круговий значок (рестарт або undo, ?).

## Вікна, меню, HUD
- `main-menu`: вибір режиму (Short / Medium / Long / Infinite / Survival).
- `game-screen`: сітка ліворуч, трей входу (похилий, 6 плиток) праворуч угорі, великий загальний `score`, трей виходу внизу праворуч, `word-preview` з очками слова, кнопка зарахування; угорі — зірка з номером рівня і `level-progress`.
- `help-window` / `codex-window`: Tile Key — 9 типів плиток з описом (джокер, ×2, +0.5, +1.0, +1.5, кислота, вогонь, дерево, камінь).
- `settings-window`: кнопка зі «слайдерами» (зміст не перевірено).
- `game-comparison`: «Your Last Game» проти «Selected Game» — тип, рахунок, рівень, слова, літери, найкраще слово, час, літер/слово, очок/слово, очок/літера; кнопки ▶ і «поділитись» (?); «Return to Main Menu».
- `leaderboard`: вкладки режимів і «найкращі слова»; фільтри «усі / друзі / мої партії».
- `achievements-window`: досягнення Steam (68).
- Переходи: `main-menu` → `game-screen` → (сітка повна) → `game-comparison` + `leaderboard` → `main-menu`.

## Фічі поза полем
- `mode-select` + `game-length`: чотири «довжини» партії (30 хв — кілька годин) і Survival.
- `leaderboard-online`: Steam-таблиці на кожну довжину й «найкращі слова»; асинхронне змагання з друзями.
- `stats`: порівняння останньої партії з будь-якою з таблиці.
- `achievements`: «Seven Letter Word»…«Ten Letter Word», «No Two Letter Words», «Timely / Speedy / Sprinter Speller» (за час), «Slow Poke» (понад 90 хв).
- `codex`: Tile Key.

## Варіації й родичі
- Режими: Short / Medium / Long — розмір сітки й квота рівня; Infinite — без каменю, квота 50; Survival — одразу пізній розподіл.
- Родичі в корпусі: Bookworm (`bookworm.md`) — зсунуті стовпці, вогняні плитки, бонусні тири; SpellTower (`spelltower.md`) — слово з сусідніх, гравітація, плитки-перешкоди; Alphabear (`alphabear.md`) — розмір і розміщення як ресурс.
- **Осі варіацій:** звідки літери (уже на полі / трей, який кидаєш сам) · коли зникає слово (одразу / коли гравець вирішить) · спецплитки (бонус / руйнівна / сміття) · кінець (час / заповнене поле).

## Цікавинки для курсу
- Падіння в зсунутих стовпцях і гекс-сусідство для вибору шляху — 📎.
- Трей виходу, що приймає лише префікс слова: префіксне дерево (trie) над словником — 🥉.
- «Не здавати, а нарощувати»: слово як живий обʼєкт на полі, перевірка після кожного кидка — 📎.
- Кислота, вогонь, дерево, камінь: таблиця взаємодій 4×N — 📎.
- Порівняння двох партій з метриками (літер/слово, очок/літеру) — 🌱.
- AI-порадник «куди кинути літеру»: оцінка майбутніх слів за частотами біграм — 🥇.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ кидання плитки з трею · `cell-click` ↔ набір слова · `gravity-fall` ↔ падіння в стовпці · `word-validation` ↔ словник · `next-queue` ↔ трей входу з 6 плиток · `event-points` ↔ цінності літер · `score-records` / `leaderboard` / `profile-stats` / `stats-window` ↔ таблиці й Game Comparison · `achievements-window` ↔ 68 досягнень · `sequential-levels` / `progress-acceleration` ↔ рівні з новими плитками · `mode-select` ↔ 5 режимів · `explode-area` ↔ вогняна плитка · `destructible-blocks` ↔ дерево · `no-moves-left` ↔ повна сітка · `codex-window` ↔ Tile Key.
- **Нема** → пропозиції карток:
  - `+hold-word-grow` «Готове слово можна тримати на полі й нарощувати» · game-logic/score · 📎.
  - `+prefix-only-input` «Ввід приймає лише префікс слова зі словника» · game-logic/constraints · 🥉.
  - `+letter-tray-drop` «Трей із N плиток: обери будь-яку й кинь у стовпець» · entities/spawn · 🌱 · слоти {tray_size}.
  - `+acid-tile` «Плитка, що при падінні знищує плитку під собою» · entities/interact · 🌱.
  - `+wildcard-tile` «Джокер: будь-яка літера, 0 очок» · entities/state · 🌱.
  - `+double-letter-tile`, `+bonus-tile-tier` (як у Bookworm), `+stone-blocker-tile` «Незнищенна плитка-сміття заповнює поле» · entities/state · 🌱.
  - `+game-comparison` «Порівняння партії з вибраною з таблиці» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:is_prefix` — вибрані літери є початком хоча б одного слова словника.
- `+cond:path_adjacent6` — наступна клітина шляху торкається попередньої в гекс-сусідстві (Bookworm, WordTactics).
- `+ui:word-preview` — поточне слово з очками до зарахування; `+ui:level-progress` — смуга до наступного рівня; `+ui:input-tray` — трей наступних плиток, з якого обираєш будь-яку.
- `+window:game-comparison` — дві колонки метрик: остання партія проти вибраної.
- `+feature:game-length` — режими, що різняться лише розміром поля й квотою, як вибір тривалості партії.
- `+card:hold-word-grow`, `+card:prefix-only-input`, `+card:letter-tray-drop`, `+card:acid-tile`, `+card:wildcard-tile` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: WordTactics](https://store.steampowered.com/app/1463350/WordTactics/) — опис, How To Play, стратегія, 4 довжини партій, таблиці, скриншоти (Tile Key, Game Comparison, таблиці рекордів).
- [Steam Community: Developer's Strategy Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2345629870) — три зони екрана, падіння, сусідство, трей виходу з префіксами, 5 режимів з розмірами й квотами, стратегії з кислотою, вогнем, деревом, каменем.
- [Steam: Achievements](https://steamcommunity.com/stats/1463350/achievements) — довжини слів, бали, рівні, часові досягнення.
- YouTube: пошук «WordTactics steam gameplay».

## Непевне
- (?) Точна формула рахунку: як множник довжини поєднується з бонусами +0.5/+1.0/+1.5 і з ×2 літери.
- (?) Чи можна вживати одну плитку двічі в слові й чи сусідство справді 6-клітинне (виведено зі зсунутих стовпців на скриншотах і слова «touches» у гайді).
- (?) Чи кислота знищує й звичайні літери (гайд радить кидати на дерево або «на ту саму літеру»; Tile Key — «знищує плитку під собою») — найпевніше, будь-яку, крім каменю.
- (?) Значення кнопок «книжка» і кругова стрілка у верхньому лівому куті; зміст налаштувань; що роблять кнопки ▶ і «поділитись» у Game Comparison.
- (?) Гра закінчується, коли сітка повна навіть за наявності слів на полі, чи лише коли нема куди кинути й нема слів.
