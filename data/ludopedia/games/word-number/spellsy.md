---
title: Spellsy
slug: spellsy
aka: []
family: word-number
also: [thinky]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC, macOS, Linux, Steam Deck, web (демо)]
links:
  - {kind: play, url: "https://youre-a-lemon-games.itch.io/spellsy", best: true, note: "веб-демо в браузері (Godot HTML5, 41 рівень): рівні Warm Up за 5 хвилин показують шлях-слово, міцність, бомби, штовхачі"}
  - {kind: steam, url: "https://store.steampowered.com/app/4171910/Spellsy/", note: "повна гра 28.07.2026: 150+ пазлів, undo без штрафу, безлімітні підказки, без таймера й очок"}
  - {kind: other, url: "https://playtester.io/spellsy", note: "опис плейтесту: зʼєднуй літери в будь-якому напрямку, очисти поле за мінімум ходів"}
  - {kind: other, url: "https://steamcommunity.com/stats/4171910/achievements", note: "досягнення: назви 17 світів повної гри, 3 зірки на кожен рівень, слова 7–10+ літер"}
  - {kind: other, url: "https://youre-a-lemon-games.itch.io/spellsy/devlog/1130146/patch-v003", note: "devlog демо: Warm Up 2 вчить undo, вибір літер мишею"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spellsy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [word-validation, path-drawing, path-cut, cell-click, keyboard-controls, controls-remap, destructible-blocks, push-object, inertia-slide, explode-area, chain-detonation, undo-unlimited, undo-step, restart-level, level-solver, unsolvable-states, completion-detection, sequential-levels, level-unlock, level-select, puzzle-select, save-progress, game-settings, settings-window, volume-control, background-music, field-scaling, achievements-window, game-screen, main-menu, end-screen, splash-screen, +path-trace-word, +word-reuse-ban, +stars-rating, +hint-solution-steps, +multi-hit-block, +found-words-list, +clear-all-goal, +tile-power-on-use]
proposes: ["+cond:path_adjacent8", "+cond:word_unused", "+cond:length", "+ui:word-preview", "+ui:found-words-list", "+ui:star-preview", "+ui:durability-number", "+feature:input-mode"]
author: opus
date: 2026-11-19
---

# Spellsy — очисти сітку літерних плиток найменшою кількістю слів: міцні плитки, бомби й штовхачі

## Суть
Логічна словесна головоломка без таймера й очок: на малій сітці лежать плитки-літери, гравець веде шлях по сусідніх (з діагоналями) плитках і подає слово — кожна плитка слова отримує «удар». Мета — прибрати всі плитки; зірки залежать від того, чи вклався в кількість слів авторського розвʼязку. Ядро — не словниковий запас, а планування: плитки мають міцність 1–3, бомби бʼють сусідів 3×3 і детонують ланцюгом, штовхачі зсувають сусіда до упору, тож порядок слів і порядок літер у слові змінюють поле.

## Поле і час
- Квадратна сітка 2×2 … 5×5 (у веб-збірці — фони `bg_2x2` … `bg_5x5`); частина клітин порожня від початку (Shifting Sands 3: поле 4×4 з 9 плитками).
- Гравітації нема: прибрана плитка лишає порожню клітину; плитки рухаються лише від штовхачів.
- Хід = одне слово. Дії плиток слова виконуються по черзі, у порядку виділення, з анімацією; під час виконання ввід заблоковано.
- Часу нема; налаштування «швидкість гри» прискорює анімації аж до миттєвої.
- Фон — містечко зі зміною дня й ночі (декор, без впливу на правила).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера (глина) | tile | літера, міцність 1 | вжита в слові або зачеплена вибухом → −1 міцності → зникає |
| Деревʼяна плитка | tile | літера, міцність 2 | витримує два удари; число міцності видно на плитці |
| Камʼяна плитка | tile | літера, міцність 3 | три удари; «стіна» з літерою, яку треба вжити тричі |
| Бомба | tile | літера, міцність, тип BOMB | спрацьовує: удар собі + удар усім 8 сусідам; сусідні бомби вибухають ланцюгом |
| Штовхач | tile | літера, стрілка → ↓ ← ↑ | спрацьовує: сусідня плитка за стрілкою ковзає до іншої плитки чи краю; потім удар штовхачу |
| Коренева бомба (повна гра) | tile | — | нова бомба світу Rootin Tootin; поведінка (?) |
| Шлях-слово | mark | список клітин | кожна наступна — 8-сусід попередньої, без повторів |
| Еталон рівня | static | список слів зі шляхами | кількість слів авторського розвʼязку — поріг 3 зірок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag|tap tile)` → ЯКЩО `custom: «плитка — 8-сусід останньої в шляху й ще не в ньому»` → ТО `custom: «плитка додається до шляху»`; повернення на передостанню → `custom: «хвіст шляху відкочується»`; несусідня плитка в режимі тапу → `custom: «шлях скидається»`.
- КОЛИ `input(submit)` → ЯКЩО `custom: «≥ 3 літер»` і `in_dictionary(word)` і `custom: «слово ще не вжито на рівні»` → ТО `custom: «плитки слова спрацьовують по черзі, у порядку виділення»`; інакше `message("too few letters (3+)" / "not in word list" / "already used this word")`, `block`.
- КОЛИ `custom: «спрацьовує звичайна плитка»` → ТО `damage(tile, 1)`.
- КОЛИ `hp_zero(tile)` → ТО `disappear(tile)` (клітина лишається порожньою).
- КОЛИ `custom: «спрацьовує бомба»` → ТО `damage(bomb, 1)`, `explode(3×3)`: `damage(сусід, 1)` для кожної з 8 сусідніх плиток, крім бомб.
- КОЛИ `after(explode)` → ЯКЩО `occupied(сусідня клітина, bomb)` → ТО `custom: «та бомба вибухає теж; кожна бомба — раз за хід»` (ланцюг).
- КОЛИ `custom: «спрацьовує штовхач»` → ЯКЩО `occupied(клітина за стрілкою, tile)` → ТО `push`, `slide(tile, dir)` до наступної плитки або краю; потім `damage(штовхач, 1)`. Сусіда нема → лише удар.
- КОЛИ `all_gone(tile)` → ТО `win`, `window(end-screen)`.
- КОЛИ `level_end` → ЯКЩО `counter(words, <=, words_in_solution)` → ТО `set_value(stars, 3)`; на 1 слово більше → 2; інакше 1. Три зірки без підказок і undo — «FLAWLESS!», з ними — «PERFECT!», менше — «CLEARED!».
- КОЛИ `input(undo)` → ТО `undo(1)`: слово повертається в обіг, знищені плитки відроджуються з попередньою міцністю, зсунуті — на місце.
- КОЛИ `input(reset)` → ТО `restart` (= undo усіх слів).
- КОЛИ `input(hint)` → ЯКЩО `custom: «фоновий розвʼязувач знайшов продовження з поточного стану»` → ТО `reveal(cells)` по кроках: 1 — перша плитка наступного слова, 2 — усі його плитки, 3 — лінія шляху в порядку; інакше `custom: «підсвітити кнопку undo»`.
- КОЛИ `counter(levels_completed, >=, N)` → ТО `unlock(світ)` (веб-збірка: Dry Run 4, Just Deserts 8, Kadune 16, Shifting Sands 25).
- Перемога: поле порожнє · Поразка: нема (глухий кут лікується undo, підказка сама радить undo) · Рахунок: очок нема, лише 1–3 зірки за кількість слів.

## Керування і ввід
- Миша: затиснути й вести по плитках (drag), відпустити — подати; або тап по кожній плитці й повторний тап по останній — подати. Налаштування «режим миші»: drag / tap / обидва.
- Клавіатура й геймпад: стрілки / D-pad водять фокус по сітці, одна кнопка — «додати або подати», інша — «прибрати останню літеру».
- Гарячі клавіші: undo, список слів, підказка, скинути поле, на мапу, налаштування; клавіші перепризначаються.
- Steam Deck: D-pad, стік, трекпад і тач.

## Вікна, меню, HUD
- `splash-screen` (Godot) → `main-menu` → мапа світів `puzzle-select`: панелі світів із блоками рівнів у 4 станах (закритий / доступний / пройдений / ідеальний — 3 зірки); на закритому — замок і «N to unlock».
- `game-screen`: поле; над ним — поточне слово з причиною відмови й трусінням (word-preview); панель дій: `undo-button`, список вжитих слів, `hint-button`; навбар: додому, налаштування; превʼю можливих зірок (з патча 0.1.7); туторіальні підказки на рівнях Warm Up («Drag to spell a word», «Earn more stars by using fewer words»).
- `end-screen`: 1–3 зірки з анімацією, лічильники слів / підказок / undo, слово-вердикт FLAWLESS / PERFECT / CLEARED, кнопки Retry і Next level.
- `settings-window` з вкладками: Game (швидкість гри, трусіння екрана, показ міцності), Audio (загальна гучність / музика / ефекти, вибір пісні), Visual (повний екран, піксельний шрифт, масштаб, ігровий курсор), Controls (режим миші, підказки геймпада, перепризначення).
- `credits-window` (музика RAVAGES).
- Переходи: мапа → рівень → end-screen → наступний рівень або повтор; кінець світу → мапа.

## Фічі поза полем
- `levels-sequential` у світах + `level-unlock` за кількістю пройдених рівнів; 150+ рівнів і 17 світів у повній грі (назви з досягнень: Warm Up, Dry Run, Just Deserts, Kadune, Shifting Sand(s), Growing Pains, Bare Bones, Rootin Tootin, Heat Check, Full House, Fired Up, Big Shot, Dune Deal, Pushed Around, Always Greener, End of the Line, Pyroglyph); демо — 40+ рівнів.
- `stars-rating` (1–3) + `undo` ∞ + `restart-level` + `hint` безлімітний (до 3 кроків на хід) + `show-solution` (підказка на старті рівня відкриває весь 3-зірковий розвʼязок, патч 1.0.0).
- `autosave` зірок рівнів і останнього світу; Steam Cloud; `achievements` (3 зірки на всі рівні світу, слова 7 / 8 / 9 / 10+ літер, «Team Effort» — відкрити підказками весь розвʼязок, «Outside The Lines» — скласти слово, відмінне від відкритої підказки).
- `speed-control` (аж до миттєвої), `screen-shake-toggle`, `volume-sliders`, `fullscreen`, `remap-controls`, `gamepad-support`, `touch-controls` (Deck).
- Словник: курований список для розвʼязувача і повний — для гравця; патчі додають і прибирають слова (Yeet +, Enuf −).

## Варіації й родичі
- Корпус: SpellTower (`spelltower.md` — шлях-слово + гравітація + довгі слова «вибухають»), Boggle (`boggle.md` — шлях по 8-сусідах без змін поля), Bookworm (`bookworm.md` — плитки падають, спецплитки), Squaredle (`squaredle.md` — шлях-слово на малих сітках), Wormspell (`wormspell.md` — заборона повторного слова).
- Поза сімʼєю: ланцюг бомб — як у Bomberman (`maze-arcade`); ковзання «до упору» — як лід у Sokoban-варіантах (`push-slide`).
- **Осі варіацій:** що робить вжита плитка (зникає / міцність N / спецсила) · гравітація (SpellTower — так, Spellsy — ні) · що оцінюється (очки за довжину / кількість слів-зірки) · штовхач (на 1 клітину / до упору) · вибух (хрест / 3×3 / ланцюг).

## Цікавинки для курсу
- Слово як конвеєр дій: кожна літера — команда (удар / вибух / поштовх), виконання по черзі з анімацією — 🥉 (Command + черга).
- Undo на рівні дій: удар памʼятає стан плитки й відроджує знищену, поштовх повертає назад — 🥉.
- Вибух 3×3 з ланцюгом без повторних детонацій (множина вже вибухлих) — 📎.
- Штовхач «до упору» з перевіркою меж і зайнятих клітин — 🌱.
- Зірки за кількістю слів проти авторського розвʼязку — 🌱.
- Підказка з фоновим розвʼязувачем: DFS по шляхах з відсіканням префіксів словника, хеш стану поля, евристика «спершу бомби, штовхачі, міцні», скасування потоку на кожен новий хід — 🥇.
- Відкриття світів за порогом пройдених рівнів (4 / 8 / 16 / 25) — 🌱.

## Мапа на каталог
- Є: `word-validation` ↔ 3+ літери й словник · `path-drawing` + `path-cut` ↔ drag-шлях з відкатом · `cell-click` ↔ режим тапу · `keyboard-controls` + `controls-remap` · `destructible-blocks` ↔ плитки зникають · `push-object` + `inertia-slide` ↔ штовхач до упору · `explode-area` (3×3) + `chain-detonation` ↔ бомби · `undo-unlimited` + `undo-step` + `restart-level` · `level-solver` + `unsolvable-states` ↔ підказки й «радить undo» · `completion-detection` ↔ порожнє поле · `sequential-levels` + `level-unlock` + `level-select` + `puzzle-select` ↔ мапа світів · `save-progress` · `game-settings` + `settings-window` + `volume-control` + `background-music` + `field-scaling` (масштаб) · `achievements-window` · `game-screen` · `main-menu` · `end-screen` · `splash-screen`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+word-reuse-ban`, `+stars-rating`, `+hint-solution-steps`, `+multi-hit-block`, `+found-words-list`, `+clear-all-goal` — уже є в корпусі; тут: підказка в 3 кроки, міцність {1, 2, 3}, зірки {3: ≤ еталону, 2: +1 слово, 1: інакше}.
  - `+tile-power-on-use` «Літера в слові запускає силу своєї плитки» · entities/interact · 📎 · слоти {power: hit|push|explode, order: selection}.

## Пропозиції до словників
- `+cond:path_adjacent8` — шлях по 8-сусідах без повторів (Boggle, SpellTower, Spellsy).
- `+cond:word_unused` — слово ще не вжито на рівні (Wormspell, Spellsy).
- `+cond:length` — довжина слова ≥ N (тут 3).
- `+ui:word-preview` — поточне слово над полем з причиною відмови.
- `+ui:found-words-list` — список вжитих слів за кнопкою.
- `+ui:star-preview` — скільки зірок дає поточний стан поля.
- `+ui:durability-number` — число міцності на плитці (вимикається в налаштуваннях).
- `+feature:input-mode` — режим вводу drag / tap / обидва.

## Джерела
- ⭐ [itch.io: Spellsy (веб-демо)](https://youre-a-lemon-games.itch.io/spellsy) — грати в браузері; опис, 41 рівень, коментарі розробника (Kadune 4 — почати з CUE). Збірку `index.pck` (Godot 4.5) розібрано: скрипти правил (удар, вибух 3×3 з ланцюгом, штовхач до упору, перевірка слова 3+ / словник / повтор, зірки, кроки підказки, розвʼязувач), налаштування, маніфести світів з порогами, рівні з авторськими розвʼязками.
- [Steam: Spellsy](https://store.steampowered.com/app/4171910/Spellsy/) — опис повної гри: 150+ пазлів, без таймера й очок, undo, підказки; новини Steam (патчі 0.1.4–1.0.1: root bombs у ланцюгу, панель «already used», 3-зіркова підказка на старті, Just Deserts 9 рівнів, Kadune 12).
- [playtester.io](https://playtester.io/spellsy) — опис механіки для плейтесту.
- [Steam: досягнення](https://steamcommunity.com/stats/4171910/achievements) — 17 світів повної гри, довгі слова, підказки.
- [itch devlog v0.0.3](https://youre-a-lemon-games.itch.io/spellsy/devlog/1130146/patch-v003) — Warm Up 2 вчить undo.
- YouTube: пошук «Spellsy gameplay».

## Непевне
- (?) Повна гра може відрізнятися від веб-збірки itch: нові типи плиток у світах Rootin Tootin (root bombs), Growing Pains, Heat Check / Fired Up / Pyroglyph — назви натякають на корені, ріст і вогонь, поведінку не перевірено.
- (?) У веб-збірці підказки вимкнено; кроки підказки описано з коду, на Steam-версії не перевірено.
- (?) Максимальний розмір поля в повній грі — у веб-збірці фони до 5×5.
- (?) У коді є «монети» за слова й ціна підказки 0 — залишок старої економіки; на Steam підказки безлімітні.
- (?) У збірці є сцена редактора рівнів і генератор розвʼязних полів — чи доступні гравцеві, невідомо.
