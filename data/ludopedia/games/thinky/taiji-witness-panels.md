---
title: Taiji + The Witness (панелі)
slug: taiji-witness-panels
family: thinky
also: [pencil-logic, connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [PC, Mac, Switch, PS4, Xbox One, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Witness_(2016_video_game)", best: true, note: "The Witness: шлях від кола до виходу без самоперетину, правила вчать групи панелей без тексту, кабелі, лазери, 650+ пазлів"}
  - {kind: steam, url: "https://store.steampowered.com/app/210970/The_Witness/", note: "The Witness (2016)"}
  - {kind: steam, url: "https://store.steampowered.com/app/1141580/", note: "Taiji (2022): єдиний інтерфейс — сітка плиток вкл/вимк"}
  - {kind: official, url: "https://taiji-game.com/", note: "Taiji: сайт, devlog, пресkit (400+ пазлів)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2862766202", note: "Taiji «Puzzle Mechanics Explained» — правила всіх символів по зонах (СПОЙЛЕРИ)"}
  - {kind: other, url: "https://taiji-game.com/2019/03/01/51-snake-puzzles/", note: "Taiji devlog: «змійкові» панелі, по яких ходиш, і як їх перевіряє солвер"}
  - {kind: youtube, url: "https://www.youtube.com/playlist?list=PLXiBcyk0gtydz6KwhU-4-bq3FnFyF16b0", note: "плейліст відео-девлогів Taiji"}
  - {kind: fandom, url: "https://the-witness.fandom.com/wiki/Puzzle_elements", note: "вікі елементів The Witness; не відкрилась (402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Witness+puzzle+rules+explained", note: "пошук; пояснення символів"}
stage: v1
coverage: 70
mechanics: [cell-click, satisfy-constraints, completion-detection, markup-validity, move-4dir, keyboard-controls, hover-highlight, save-progress, settings-window, game-screen, level-unlock, +world-map, +undo-redo, +rule-teaching-by-example, +region-constraints, +path-draw, +polyomino-fit, +pair-by-color, +element-eliminator, +symmetry-path, +edge-count-clue, +environment-clue, +panel-chain-unlock, +tile-toggle, +walk-on-panel]
proposes: ["+trigger:input", "+trigger:all_constraints_met", "+trigger:constraint_broken", "+cond:connected", "+cond:fits", "+cond:same", "+cond:adjacent_count", "+cond:count", "+effect:mark", "+effect:flash", "+effect:unlock", "+effect:set_state", "+role:mark", "+role:zone", "+role:conduit", "+ui:conflict-highlight", "+ui:path-preview", "+window:map-window", "+feature:onboarding-hints", "+axis:rules", "+axis:control"]
author: opus
date: 2026-11-02
---

# Taiji + The Witness — панелі-пазли, правила яких ніхто не пояснює: символ на сітці → обмеження на регіон, вивчене спостереженням

## Суть
Парасолька для двох ігор однієї лінії. **The Witness** (2016, Thekla/Jonathan Blow): на острові стоять сотні панелей; кожна — сітка, на якій треба **провести лінію** від кола-старту до заокругленого виходу; символи в клітинах і на ребрах — обмеження на регіони, які лінія відрізає. **Taiji** (2022, Matthew VanDevander, «пригодницький пазл у стилі The Witness»): ввід інший — плитки сітки **вмикаються/вимикаються** (білі/чорні), а символи вимагають певних форм регіонів однакового кольору. Спільне ядро: малий набір символів-правил, **кожна зона острова вводить один символ** серією панелей від тривіальної до складної — гравець виводить правило з прикладів, без жодного тексту. Аватар ходить світом (класи `avatar` поза панелями), але 90 % часу — `puzzle` на панелі.

## Поле і час
- **Witness:** сітка-решітка: лінія йде **ребрами й вузлами**, символи стоять у клітинах (квадрати, зірки, тетроміно, трикутники, Y) або на ребрах/вузлах (шестикутники). Розміри від 2×2 до ~7×7 і більше; бувають розірвані ребра, кілька стартів/виходів, непрямокутні форми (?).
- **Taiji:** сітка плиток (≈3×3 … 7×7 і більше (?)), кожна плитка — 2 стани (біла/чорна); деякі плитки фіксовані (пунктирна рамка) або відсутні. «Регіон» = звʼязна (4-сусідство) область одного кольору.
- Час: статичний пазл. Помилка показується лише після спроби (Witness — після завершення лінії; Taiji — індикатор розвʼязаності (?)).
- Світ: 3D острів (Witness) / 2D top-down острів (Taiji) з вільним рухом; панелі — вузли прогресу, зʼєднані кабелями/світлом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| **Witness:** Старт (велике коло) | static | — | лінія починається тут; кілька стартів — будь-який |
| Вихід (заокруглений виступ на краю) | static | — | лінія мусить закінчитись тут |
| Лінія гравця | mark | шлях по ребрах | не перетинає себе, не йде розірваними ребрами |
| Розірване ребро (gap) | static | — | лінія не проходить |
| Шестикутник (hex dot) | mark | на ребрі/вузлі; колір (у симетрії) | лінія мусить пройти через кожен; кольоровий — лише лінія відповідного кольору |
| Квадрат кольору | mark | колір | регіон з квадратами — лише одного кольору |
| Зірка | mark | колір | у регіоні рівно **2** елементи кольору зірки (зірка + 1: інша зірка чи квадрат) |
| Поліоміно (жовте) | mark | форма, повернуте/ні | регіон точно складається з усіх поліоміно в ньому; нахилене — можна обертати |
| Порожнисте синє поліоміно | mark | форма | віднімає площу (компенсує жовте); сума 0 — регіон без обмеження |
| Трикутники (1–3) | mark | N | лінія проходить рівно N ребрами цієї клітини |
| Y-елімінатор | mark | — | скасовує рівно один інший символ у своєму регіоні; мусить щось скасувати |
| Симетрична панель | static | вісь/поворот | дві лінії (синя, жовта) рухаються дзеркально; обидві мають бути валідні |
| Кабель / живлення | conduit | — | розвʼязана панель живить наступну, відчиняє двері |
| Лазер зони | switch | — | фінал зони; N лазерів відчиняють гору |
| Довкілля-підказка (тінь, відбиток, скло-фільтр, звук, дерево) | zone | — | змінює або підказує відповідь панелі; кольорове скло змінює видимі кольори |
| Прихована «панель у світі» | mark | точка огляду | лінія, складена з обʼєктів світу, видна лише з одного місця |
| **Taiji:** Плитка | tile | біла/чорна, фіксована/ні | клік перемикає стан |
| Регіон | zone | колір, розмір, форма | звʼязна область одного кольору (4-сусідство) |
| Кістяні точки (Shrine) | mark | N, колір; порожнисті = −1 | розмір регіону = сума точок; в одному регіоні лише точки одного кольору; сума 0 — без обмеження, від'ємна — невалідна |
| Діамант (Mine) | mark | колір | у регіоні рівно один **інший** елемент того ж кольору (діамант, точки, лінія, пелюстка) |
| Квітка (Garden) | mark | 0–4 помаранчевих пелюсток | кількість сусідів (4) **того ж кольору**, що й плитка квітки = к-сть помаранчевих пелюсток; край поля не рахується |
| Горизонтальна лінія (Mill) | mark | колір | усі лінії одного кольору — в регіонах однакової форми, лінія в тій самій позиції; дві однакові лінії не в одному регіоні |
| Діагональна лінія (Mill) | mark | колір | те саме, але регіон може бути повернутий на 90° навколо плитки з лінією |
| Змійкова панель («walking») | tile | — | ходиш по плитках ногами; світні плитки мають утворити шлях без глухих кутів |
| Зовнішні «мови» (Graveyard 0/1, Ruins стовпи, Orchard дерева, Plateau будинки, Gallery картини) | zone | — | розвʼязок закодовано в довкіллі: XOR-послідовності, стовп із розширенням = біла сусідня, дерево = бінарне дерево, симетрія фасадів |
| Блок-статуя (вступ) | static | — | порожня позиція отримує колір, якого менше серед сусідів |
| Телепорт-камінь | switch | символ 3×3 | намалюй символ каменю на сітці кнопки — телепорт відкрито |

## Правила (КОЛИ → ЯКЩО → ТО)
Witness (лінія):
- КОЛИ `input(start_path, start_circle)` → ТО `custom: «режим малювання: аватар стоїть, мишею/стиком веде лінію по ребрах»`.
- КОЛИ `input(extend_path)` → ЯКЩО `free(edge)` і `not custom: «вже пройдений вузол»` → ТО `mark(edge)`; інакше `block`.
- КОЛИ `reach(path, exit)` → ТО `custom: «лінія розбиває сітку на регіони (лінія + рамка)»`, перевірити всі символи.
- `hex`: КОЛИ кінець → ЯКЩО `not custom: «шлях покрив усі шестикутники»` → ТО `constraint_broken`.
- `square`: ЯКЩО `count(colors_of_squares(region), >, 1)` → `constraint_broken`.
- `star`: ЯКЩО `cond: count(region, color_of(star), !=, 2)` → `constraint_broken`.
- `polyomino`: ЯКЩО `not cond: fits(shapes(region), cells(region))` (з урахуванням обертання для нахилених і віднімання синіх) → `constraint_broken`.
- `triangle(N)`: ЯКЩО `cond: count(path_edges_of(cell), !=, N)` → `constraint_broken`.
- `Y`: КОЛИ `constraint_broken(x)` у регіоні з Y → ТО `custom: «Y анулює рівно один символ»`; ЯКЩО нічого анулювати → сам Y невалідний.
- КОЛИ `all_constraints_met` → ТО `win(panel)`, `set_state(cable, powered)`, `unlock(next_panel|door)`; КОЛИ `constraint_broken` → ТО `flash(broken symbols)`, лінія гасне — нова спроба без штрафу.
- Симетрія: КОЛИ `input(extend_path)` → ТО `move(mirror_path, mirrored)`; дві лінії не можуть перетнутися.

Taiji (плитки):
- КОЛИ `input(click tile)` → ЯКЩО `not state(tile, fixed)` → ТО `set_state(tile, toggle)`.
- КОЛИ `custom: «після кожного кліку»` → ТО перерахувати регіони (`cond: connected` одного кольору) і перевірити символи:
- точки: ЯКЩО `cond: count(cells(region), !=, sum(dots(region)))` або кольори точок різні → `constraint_broken`.
- діамант: ЯКЩО `cond: count(same-colour elements(region) except self, !=, 1)` → `constraint_broken`.
- квітка: ЯКЩО `cond: adjacent_count(flower_tile, same_colour, !=, orange_petals)` → `constraint_broken`.
- лінії: ЯКЩО форми регіонів з лініями одного кольору різні (з поворотом для діагональних) → `constraint_broken`.
- змійка: ЯКЩО `custom: «світні плитки не утворюють шлях без глухих кутів від стартової»` → `constraint_broken`.
- КОЛИ `all_constraints_met` → ТО `win(panel)`, `unlock(next)`.
- Перемога: усі обмеження панелі виконано; гра — відкриття зон, фінал за порогом зон (Witness: лазери → гора) · Поразка: нема (Witness Challenge — таймер музики) · Рахунок: нема.

## Керування і ввід
- **Witness:** WASD/стик — ходьба від першої особи; клік на панель → режим малювання (рамка навколо екрана, курсор = кінчик лінії); миша/стик веде лінію; ПКМ/кнопка — скасувати; кінець лінії на виході — перевірка.
- **Taiji:** стрілки/стик — ходьба top-down; на панелі — курсор по плитках, клік/кнопка — перемкнути; змійкові панелі — ходьба по самих плитках.
- Undo: Witness — лінію просто малюєш заново; Taiji — плитки перемикаються назад (окремого undo нема (?)).

## Вікна, меню, HUD
- `main-menu` — Continue · New Game · Load · Options · Quit (обидві ігри (?)).
- `game-screen` — світ без HUD; панель у фокусі; Witness — біла рамка режиму малювання; індикатор розвʼязаних панелей групи (лампочки на кабелі).
- `map-window` — **нема** в обох: орієнтація лише по світу (Taiji — телепорт-камені з символами).
- `settings-window` — керування, чутливість, графіка, колорблайнд-безпечні кольори (Taiji, devlog 36), мова (13 у Taiji).
- Переходи: світ → (підійти, клік) панель → (розвʼязав) світ; Taiji: камінь-телепорт → вибір символу на сітці → інша зона.

## Фічі поза полем
- `rules-page` відсутня свідомо: `onboarding-hints` = **сама послідовність панелей** (кожна наступна додає один нюанс).
- `level-unlock` ланцюжками кабелів; відкриті в будь-якому порядку зони; фінал за порогом зон (Witness: лазери зон → гора).
- `autosave`; `achievements`; Witness — Challenge-кімната з **процедурними** панелями на час (два треки музики) — єдиний випадковий режим.
- Опційні: Witness — 135 (?) середовищних «ліній у світі»; Taiji — Gallery з картинами-шифрами, секретні досягнення.
- Доступність: Taiji — колорблайнд-безпечна палітра; Witness — рамка перевірки й мигання помилки.

## Варіації й родичі
- Лінія: The Witness → Islands of Insight (MMO-панелі), Linelith, The Looker (пародія); паперові попередники — Nikoli (Slitherlink, Heyawake — регіони).
- Плитки: Taiji → Islands of Insight (logic grids), Tametsi; LOK Digital, Hexcells — «правила вивчаються»; puzz.link — ті самі обмеження як папір.
- **Осі варіацій:** ввід — провести лінію / перемкнути плитки / ходити по панелі; що символ обмежує — регіон / сусідів / ребра клітини; як вчать правило — текст / послідовність панелей / довкілля; що таке регіон — область, відрізана лінією / звʼязна область кольору.

## Цікавинки для курсу
- Розбиття сітки лінією на регіони (flood fill по клітинах, ребра лінії = стіни) — 🥉.
- Набір валідаторів «символ → обмеження на регіон» (квадрати, зірки, трикутники) — 🥈: модульна система правил, кожен символ — функція.
- Поліоміно-тайлінг регіону з поворотом і від'ємними фігурами — 🥇 (exact cover / backtracking).
- Y-елімінатор: «скасуй рівно один символ» — 🥇 (перебір, який символ анулювати).
- Taiji: регіони кольору + точки/квіти/діаманти — 🥉 (звʼязні компоненти + лічильники).
- Симетрична лінія (дві лінії одним вводом) — 📎.
- Генератор панелей з унікальним розвʼязком (Witness Challenge) — 👑.

## Мапа на каталог
- Є: `cell-click` ↔ перемикання плиток Taiji; `satisfy-constraints` + `completion-detection` + `markup-validity` ↔ перевірка панелі; `move-4dir` + `keyboard-controls` ↔ ходьба світом; `hover-highlight` ↔ фокус панелі; `level-unlock` ↔ кабелі; `save-progress`; `settings-window`; `game-screen`.
- **Нема** → пропозиції карток:
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — тут «мапа» = сам острів (як у Baba Is You).
  - `+undo-redo` «Undo ходів у грі» · game-logic/flow · 📎 — як у Baba Is You (тут неявне).
  - `+rule-teaching-by-example` «Навчання правилу без тексту» · support/docs · 🥉 (спільна з LOK, Gorogoa).
  - `+region-constraints` «Обмеження на регіони, відрізані лінією чи кольором» · game-logic/constraints · 🥈.
  - `+path-draw` «Провести лінію по ребрах решітки від старту до виходу» · interface/input · 🥉.
  - `+polyomino-fit` «Регіон точно складається з фігур» · game-logic/constraints · 🥇 · слот {rotate: yes|no, negative: yes|no}.
  - `+pair-by-color` «Пари за кольором у регіоні (зірки/діаманти)» · game-logic/constraints · 📎.
  - `+element-eliminator` «Символ, що анулює інший» · game-logic/constraints · 🥇.
  - `+symmetry-path` «Дзеркальна друга лінія» · interface/input · 📎.
  - `+edge-count-clue` «Скільки ребер клітини пройдено (трикутники)» · game-logic/constraints · 📎.
  - `+environment-clue` «Відповідь закодована в довкіллі» · levels/format · 🥉.
  - `+panel-chain-unlock` «Розвʼязана панель живить наступну» · levels/progression · 🌱.
  - `+tile-toggle` «Перемкнути плитку біла/чорна» · interface/input · 🌱.
  - `+walk-on-panel` «Панель, по якій ходиш ногами» · interface/input · 📎.

## Пропозиції до словників
- `+trigger:input(path|toggle)`, `+trigger:all_constraints_met`, `+trigger:constraint_broken` (обидва ⏳ з 🔥).
- `+cond:connected` (регіон), `+cond:fits(shapes, cells)`, `+cond:same(color)`, `+cond:adjacent_count` (квітки), `+cond:count`.
- `+effect:mark` (ребро/плитка), `+effect:flash` (мигання порушених символів), `+effect:unlock`, `+effect:set_state(cable, powered)`.
- `+role:mark` (символи-підказки), `+role:zone` (регіон), `+role:conduit` (кабель).
- `+ui:conflict-highlight` — порушені символи блимають червоним; `+ui:path-preview` — кінчик лінії під курсором.
- `+window:map-window` — свідомо **відсутнє**; варто фіксувати «нема мапи» як рішення.
- `+feature:onboarding-hints` — навчання серією панелей.
- `+axis:rules` — `discovered` (правила фіксовані, але не пояснені).
- `+axis:control` — нове значення `draw-path` (Witness) і `toggle` (Taiji).

## Джерела
- ⭐ [Wikipedia: The Witness](https://en.wikipedia.org/wiki/The_Witness_(2016_video_game)) — універсальні правила лінії, навчання групами панелей, кабелі, лазери й гора, 650+ пазлів, середовищні пазли.
- [Taiji: Puzzle Mechanics Explained (Steam guide)](https://steamcommunity.com/sharedfiles/filedetails/?id=2862766202) — правила точок, діамантів, квітів, ліній, бінарних послідовностей, стовпів, дерев, галереї (спойлери).
- [Steam: Taiji](https://store.steampowered.com/app/1141580/) і [taiji-game.com](https://taiji-game.com/) — єдиний інтерфейс плиток, 400+ пазлів, дати.
- [Taiji devlog 51: Snake puzzles](https://taiji-game.com/2019/03/01/51-snake-puzzles/) — змійкові панелі та перевірка розвʼязку.
- [Відео-девлоги Taiji](https://www.youtube.com/playlist?list=PLXiBcyk0gtydz6KwhU-4-bq3FnFyF16b0).
- [Steam: The Witness](https://store.steampowered.com/app/210970/The_Witness/).
- YouTube: [пошук «The Witness puzzle rules explained»](https://www.youtube.com/results?search_query=The+Witness+puzzle+rules+explained).

## Непевне
- (?) Правила символів The Witness (шестикутники, квадрати, зірки, поліоміно з поворотом і синіми, трикутники, Y) — з памʼяті: Wikipedia описує лише квадрати й загальні правила, fandom-вікі недоступна (402).
- (?) 11 лазерів / 7 для гори, 135 середовищних пазлів, Challenge з двома треками — з памʼяті.
- (?) Розміри сіток обох ігор; наявність окремого undo в Taiji; індикатор розвʼязаності панелі Taiji до завершення.
- (?) Зони Taiji (Shrine, Mine, Garden, Mill, Graveyard, Ruins, Orchard, Plateau, Gallery) — з одного гайду спільноти; розробник свідомо не публікує правил.
- Квітка Taiji: гайд каже «помаранчеві пелюстки = скільки сусідів мають колір квітки» — «колір квітки» трактую як колір її плитки (?).
