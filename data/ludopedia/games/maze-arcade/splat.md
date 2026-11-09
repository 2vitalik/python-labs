---
title: Splat!
slug: splat
aka: [Splat, The Splat Challenge]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: survive
year: 1983
platforms: [ZX Spectrum 48K, Commodore 64 (1984), Amstrad CPC (1985), SAM Coupé (1991)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Splat!_(video_game)", best: true, note: "Zippy, лабіринт скролиться у випадкових напрямках, край кадру вбиває, трава й сливи, 7 рівнів зі скороченням часу, «Yippee!», конкурс £500"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxsr.php?id=4767", note: "тексти оглядів CRASH, PCN, PCG, C&VG: річки з 2-го рівня, шипи з 3-го, невидима трава з біпом, 3 життя, час рівня у %"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/4767/ZX-Spectrum/Splat", note: "картка ZXDB: керування, вкладка касети (7 рівнів, Progress %, High Score, User Defined Controls), скани оглядів"}
  - {kind: other, url: "https://everygamegoing.com/larticle/gameplay-spectrum-48k-splat/2485", note: "огляд Personal Computer News #29: як саме ходить лабіринт, Hi-код після 500 очок"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-extras/Splat_CompetitionInstructions.png", note: "правила конкурсу £500: Hi-Code за рекорд понад 500 очок, порада шукати невидиму траву"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/pub/sinclair/games-info/s/Splat(System4).pdf", note: "іспанська інструкція перевидання: клавіші Spectrum/Amstrad/C64, мета — телепорт, вода й кнопки-шипи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Splat+ZX+Spectrum+1983", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, keyboard-controls, impassable-cells, item-pickup, event-points, environment-death, player-death, sequential-levels, progress-acceleration, score-records, game-pause, help-window, game-screen, status-panel, +scroll-death-edge, +invisible-pickup, +survive-timer-level, +score-verification-code]
proposes: ["+trigger:view_edge", "+feature:score-verification-code", "+card:survive-timer-level", "+card:score-verification-code"]
author: opus
date: 2026-11-09
---

# Splat! — лабіринт сам їде екраном у випадкові боки; доторкнешся до рамки кадру — розчавлений

## Суть
Гравець веде Zippy (X-подібного «чотириногого павука») лабіринтом, значно більшим за екран, і їсть траву та сливи заради очок. Головне: камеру веде не гравець, а гра — лабіринт разом із Zippy зсувається вгору, вниз, ліворуч чи праворуч на випадковий час, а нерухома цегляна рамка екрана вбиває при дотику. Тож гравець весь час іде проти течії, щоб утриматись у кадрі, а стіна лабіринту між ним і рамкою — смертельна пастка. Рівень пройдено, якщо протримався відведений час; 7 рівнів — це послідовні частини одного лабіринту.

## Поле і час
- Поле — вид згори, лабіринт зі стінами, набагато більший за екран; кожен рівень — продовження того самого лабіринту (Wikipedia).
- Вʼюпорт обведено нерухомою цегляною рамкою; лабіринт плавно скролиться під нею в одному з 4 напрямків «на різні проміжки часу» (PCN) і може змінити напрям будь-коли (CRASH).
- Zippy стоїть у лабіринті, тому скрол несе його до рамки; рух гравця — відносно лабіринту.
- Real-time. Час рівня показано відсотком прогресу: 100 % — рівень пройдено. З кожним рівнем інтервал між кроками скролу коротшає, а сам рівень коротший: перший ≈ 2 хв, сьомий ≈ 40 с (Wikipedia).
- Шари: підлога (прохід / річка / міст) + стіни + предмети й шипи + Zippy; рамка кадру — окремий шар поверх, привʼязаний до екрана.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Zippy | player | 3 життя (CRASH) | рух 4 напрямки відносно лабіринту; скрол несе його разом з лабіринтом |
| Стіна лабіринту | static | — | блокує Zippy; притиснути ним до рамки — смерть |
| Цегляна рамка кадру | hazard | привʼязана до екрана, не до лабіринту | дотик Zippy = «Splat!», мінус життя |
| Трава | pickup | — | зʼїсти — очки; частина кущиків у тупиках |
| Невидима трава | pickup | не видно до зʼїдання | зʼїсти — очки й біп (CRASH); порада конкурсу — шукати її |
| Слива | pickup | переважно з 2-го рівня | бонусні очки |
| Річка | hazard | з 2-го рівня | Zippy не вміє плавати — тоне |
| Міст | terrain | — | єдиний спосіб перетнути річку |
| Шипи (червоні кнопки) | hazard | з 3-го рівня | дотик — смерть |
| Вихід (телепорт) | static | на останньому рівні | мета гри; меню каже «No chance!» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(zippy, dir)`; інакше `block`.
- КОЛИ `timer(scroll_step)` → ТО `camera(scroll, scroll_dir)` — лабіринт разом із Zippy зсувається відносно рамки.
- КОЛИ `rng(p)` → ТО `custom: «новий напрям скролу (вгору/вниз/ліворуч/праворуч) і нова тривалість»`.
- КОЛИ `custom: «Zippy торкнувся рамки кадру»` (`+trigger:view_edge`) → ТО `lives(-1)`, `sound(splat)`.
- КОЛИ `enter(zippy, river)` → ТО `lives(-1)` — тоне.
- КОЛИ `contact(zippy, spikes)` → ТО `lives(-1)`.
- КОЛИ `contact(zippy, grass)` → ТО `disappear_b`, `score(grass)`.
- КОЛИ `contact(zippy, invisible_grass)` → ТО `disappear_b`, `score(grass)`, `sound(bleep)`.
- КОЛИ `contact(zippy, plum)` → ТО `disappear_b`, `score(plum)`.
- КОЛИ `timer(level_tick)` → ТО `counter(progress, +1)` — відсоток часу рівня.
- КОЛИ `counter(progress, >=, 100)` → ТО `sound(«Yippee!»)`, `score(level_bonus)`, `next_level`.
- КОЛИ `level_start` → ТО `speed(scroll, +n)`, `custom: «коротший рівень»`; ЯКЩО `level(>=, 2)` → річки й сливи; ЯКЩО `level(>=, 3)` → шипи.
- КОЛИ `reach(zippy, exit)` → ЯКЩО `level(==, 7)` → ТО `win`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- КОЛИ `game_over` → ЯКЩО `counter(score, >, 500)` and `custom: «новий рекорд»` → ТО `message(hi_code)` — код-підтвердження рекорду для конкурсу.
- Перемога: дійти до виходу на 7-му рівні · Поразка: втрата 3 життів (рамка, річка, шипи) · Рахунок: трава, сливи, бонус за кожен пережитий рівень.

## Керування і ввід
- 4 напрямки; Spectrum: 5/6/7/8 (стрілки на цифрах), ENTER — пауза; Amstrad: стрілки курсора, пробіл — пауза; C64: A/Z угору/вниз, F1–F7 — пауза, джойстик у порту 2 (іспанська інструкція).
- У меню Spectrum: 2 — перепризначити клавіші, 3 — Kempston, 4 — AGF; у CRASH згадано ще Protek. Amstrad: D — клавіші, I — інструкції, Del — зміна кольорів.
- Дії, крім руху, нема: ні стрільби, ні стрибка.

## Вікна, меню, HUD
- `main-menu` (Spectrum): вибір інтерфейсу (клавіші / Kempston / AGF), перепризначення клавіш, старт; репліка «No chance!» про 7-й рівень (PCN).
- `options-controls` — редагування клавіш («User Defined Controls» на вкладці).
- `help-window` — «On Screen Instructions» (вкладка, PCN).
- `game-screen`: кадр лабіринту в цегляній рамці; `score`, `hi-score`, `progress-bar` (Progress %), `lives`, `level-number` (?).
- `pause-menu` — простий стан паузи.
- `end-screen` — після гри: якщо рекорд понад 500 очок, показує Hi-Code.
- Переходи: main-menu → game-screen → (100 %) «Yippee!» → наступний рівень → … → (0 життів) end-screen → main-menu.

## Фічі поза полем
- `levels-sequential` на 7 рівнів з `progress-acceleration` (швидший скрол, коротший рівень).
- `leaderboard-local`: «High Score Feature» на вкладці.
- `+feature:score-verification-code` — Hi-Code: гра сама генерує кодове слово для рекорду понад 500 очок; щоб виграти £500, слали на листівці очки й код (конкурс до 14.01.1984, переміг James Tant, 112 930).
- `remap-controls`, `gamepad-support` (Kempston, AGF), `pause`, зміна кольорів на Amstrad.

## Варіації й родичі
- Порти: C64 (Steve Zodiac), Amstrad CPC (Paul Shirley), SAM Coupé (Colin Jordan); перевидання у збірці 4-Most Thrillers (1992) та іспанське System 4.
- Не плутати з `pencil-logic/slant` (паперова головоломка) — автоматика черги їх зіставила хибно.
- Огляди порівнювали з `hungry-horace` (трава, лабіринт; у Splat! лабіринт значно більший за екран) і з Mined-Out (`hidden-deduction/mined-out`).
- Родичі за рухомою межею: `entombed` (лабіринт скролиться вниз, край вбиває), `falling-match/10000000` (рухома межа екрана), `pac-man-sequels` (лабіринт ширший за екран, але камера за гравцем), `maziacs`.
- **Осі варіацій:** хто веде камеру: гравець / фіксований напрям / випадковий напрям і тривалість · межа кадру: безпечна / вбиває · мета: зібрати все / протриматись час · предмети: видимі / невидимі.

## Цікавинки для курсу
- Автономна камера з випадковим напрямом і тривалістю плюс рамка-вбивця: світ і вʼюпорт — дві системи координат — 📎.
- «Притиснули стіною до рамки»: смерть як наслідок руху камери, а не ворога — 🌱 поверх попереднього.
- Невидимі предмети, які видно лише в момент поїдання (біп) — 🌱.
- Рівень на виживання: таймер у відсотках і прискорення скролу з рівнем — 🌱.
- Hi-Code: контрольний код від рахунку, щоб рекорд не підробили (хеш із секретом) — 📎.
- Рівні як частини одного великого лабіринту замість окремих карт — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` (перепризначення клавіш) · `impassable-cells` · `item-pickup` (трава, сливи) · `event-points` · `environment-death` (річка, шипи) · `player-death` (3 життя) · `sequential-levels` · `progress-acceleration` · `score-records` · `game-pause` · `help-window` · `game-screen` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+scroll-death-edge` (вже `entombed`, `10000000`) — рухома межа екрана вбиває; тут зі слотом {dir: random, duration: random}.
  - `+invisible-pickup` (вже `gyromite`) — невидимий предмет на клітині.
  - `+survive-timer-level` «Рівень пройдено, якщо протримався N секунд» · game-logic/win · 🌱 · слот {duration, shrink_per_level}.
  - `+score-verification-code` «Код-підтвердження рекорду» · game-logic/score · 📎 — код від очок із секретом, перевіряється поза грою.

## Пропозиції до словників
- `+trigger:view_edge` — сутність торкнулась межі вʼюпорта, що рухається незалежно від неї (Splat!, Entombed); відрізняється від `edge`, бо поле більше за кадр.
- `+feature:score-verification-code` — гра видає код для перевірки рекорду поза грою (Splat!, конкурси Incentive).
- `+card:survive-timer-level`, `+card:score-verification-code` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Splat!](https://en.wikipedia.org/wiki/Splat!_(video_game)) — Zippy, випадковий скрол, рамка-вбивця, вода й шипи, трава (частина невидима), сливи, 7 рівнів від ≈2 хв до ≈40 с, «Yippee!», конкурс.
- [Spectrum Computing: огляди](https://spectrumcomputing.co.uk/zxsr.php?id=4767) — CRASH (3 життя, невидима трава з біпом), PCN, PCG, C&VG: річки з мостами з 2-го рівня, шипи з 3-го, час у %, вихід на 7-му рівні.
- [Spectrum Computing: картка гри](https://spectrumcomputing.co.uk/entry/4767/ZX-Spectrum/Splat) — керування (курсор, Kempston, перепризначення), вкладка касети, список оглядів.
- [Personal Computer News #29](https://everygamegoing.com/larticle/gameplay-spectrum-48k-splat/2485) — «Bounded on all sides by a fixed wall, it swings up, down, left and right, for varying durations»; Hi-код після 500 очок.
- [Правила конкурсу £500](https://spectrumcomputing.co.uk/pub/sinclair/games-extras/Splat_CompetitionInstructions.png) — Hi-Code, поради «шукай невидиму траву».
- [Інструкція System 4 (ES, PDF)](https://spectrumcomputing.co.uk/pub/sinclair/games-info/s/Splat(System4).pdf) — таблиця клавіш трьох платформ, телепорт як мета, кнопки-шипи, «нестабільний матеріал».
- YouTube: пошук «Splat ZX Spectrum 1983».

## Непевне
- (?) Чи рух Zippy і скрол поклітинні: огляди хвалять «smooth scrolling», розмір клітини й лабіринту не названо.
- (?) Мета: англомовні джерела — вихід на 7-му рівні, іспанська інструкція — «телепорт на поверсі 8».
- (?) «Material inestable» з іспанської інструкції — окремий тип небезпечної клітини чи інша назва невидимої трави, не зʼясовано.
- (?) Що стається після втрати життя: рестарт того ж рівня з центру чи продовження з місця.
- (?) Вартість трави, сливи й бонусу за рівень не знайдено; чи зʼявляється на екрані лічильник життів і номер рівня.
- (?) Як саме обирається новий напрям скролу (рівноймовірно чи з обмеженнями, щоб не загнати в безвихідь).
