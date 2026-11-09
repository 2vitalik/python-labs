---
title: Puzzlejuice
slug: puzzlejuice
aka: [PuzzleJuice]
family: word-number
also: [falling-match]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2012
platforms: [iOS, Android (2020, GameClub)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzlejuice", best: true, note: "правила: тетроміно → повний ряд або група ≥4 одного кольору стає літерами, слова по 8-сусідах, довгі чистять сусідів, режими Zen/Core, множник, павер-апи"}
  - {kind: other, url: "https://www.pocketgamer.com/puzzlejuice/review/", note: "огляд: тап — поворот, свайп — рух і скид, тап по групі → білі літерні плитки, бомби, лід, дрилі"}
  - {kind: other, url: "https://kotaku.com/puzzlejuice-blends-bejeweled-tetris-and-scrabble-into-5881241", note: "огляд: ряди самі не чистяться, павер-апи bomb/freeze/driller/twister, челенджі, прискорення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzlejuice+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, piece-rotate-flip, swipe-gestures, cell-click, word-validation, combo-multiplier, progress-acceleration, time-out, explode-area, leaderboard, mode-select, difficulty-levels, tutorial-window, game-screen, end-screen, +path-trace-word, +long-word-blast, +color-group-to-letters, +full-row-to-letters, +manual-row-clear, +equip-loadout, +challenge-unlocks, +min-word-length-mode]
proposes: ["+cond:path_adjacent8", "+cond:length", "+ui:word-preview", "+window:loadout-select", "+feature:objective-unlocks", "+card:color-group-to-letters", "+card:full-row-to-letters", "+card:manual-row-clear"]
author: opus
date: 2026-11-09
---

# Puzzlejuice — Tetris, у якому ряд не зникає сам: перетвори кольори на літери й зітри їх словом, як у Boggle

## Суть
Згори падають багатоколірні тетроміно; гравець крутить і ставить їх, як у Tetris (аватар-фігура). Далі — курсорна фаза: суцільний ряд або група однакового кольору перетворюється на білі плитки з літерами, а слово, проведене пальцем по сусідніх літерах (з діагоналями), стирає їх, довге — разом із сусідами. Ряди не чистяться автоматично, тож Tetris-стек росте, доки ти не «прочитаєш» його словами; клас — `hybrid` (фігура + курсор). Автор ідеї — Asher Vollmer (Tetris + Bejeweled + Boggle); з тієї ж ідеї «Tetris + Boggle» виросла SpellTower Zach Gage.

## Поле і час
- Вертикальний колодязь-сітка з гравітацією (розміри — у «Непевне»); шари: стек кольорових блоків, білі літерні плитки, павер-апи.
- Real-time: фігури падають безперервно, темп росте, що краще ти граєш.
- Два стани клітини стеку: кольоровий блок (лише колір) → літерна плитка (лише літера); слово можна скласти лише з літер.
- Режими: Core — до переповнення; Zen — 90 секунд.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | object | форма, колір кожної клітини | падає; тап — поворот, свайп — рух, свайп униз — скид; після посадки розпадається на блоки стеку |
| Кольоровий блок | tile | колір | лежить у стеку; у групі одного кольору чи в повному ряду стає літерою |
| Літерна плитка (біла) | tile | літера | входить у слово-шлях; зникає разом зі словом |
| Шлях-слово | mark | послідовність 8-сусідів | показує слово під пальцем; відпускання — подача |
| Бомба | pickup | — | вибухає, знищуючи блоки довкола |
| Лід (freeze) | pickup | — | зупиняє появу нових фігур / час |
| Дриль (driller) | pickup | напрям (?) | зносить блоки на своєму шляху |
| Twister | pickup | — | вирівнює й перебудовує поле |
| Верх колодязя | static | лінія переповнення | стек вище → кінець Core |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; темп — за прогресом.
- КОЛИ `input(tap piece)` → ТО `rotate(piece, 90)`.
- КОЛИ `input(swipe left|right)` → ЯКЩО `free(target_cells)` → ТО `move(piece, dir)`.
- КОЛИ `input(swipe down)` → ТО `custom: «фігура падає до упору й фіксується»`.
- КОЛИ `locked(piece)` → ТО `custom: «клітини фігури стають кольоровими блоками стеку»`, `spawn_at(next_piece, top)`.
- КОЛИ `pattern(row_full)` → ТО `transform(блоки ряду, літерні плитки)`; ряд **не** зникає.
- КОЛИ `input(tap group)` → ЯКЩО `same(блоки групи, color)` і `custom: «група з ≥ 4 (за іншими джерелами ≥ 3) сусідніх блоків»` → ТО `transform(група, літерні плитки)`.
- КОЛИ `input(trace path)` → ЯКЩО `custom: «кожна наступна плитка — 8-сусід попередньої, без повторів»` → ТО `custom: «слово показується під час ведення»`.
- КОЛИ `input(release)` → ЯКЩО `in_dictionary(word)` і `custom: «довжина ≥ мінімуму режиму: 3 на легкому, 5 на складних»` → ТО `clear(path)`, `score(за довжину слова)`, `combo(+1)`; інакше `custom: «шлях скасовано»`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «слово достатньої довжини»` → ТО `clear(сусіди шляху)` — довше слово зносить більше блоків.
- КОЛИ `after(clear)` → ТО `fall(блоки над порожнечею)` (?) — блоки зсуваються, погана посадка виправляється словом.
- КОЛИ `idle(n)` → ЯКЩО `chain(1)` → ТО `reset_combo` — множник гасне, якщо довго не складати слів.
- КОЛИ `after(clear)` → ЯКЩО `custom: «павер-ап у ланцюжку блоків, що зникли»` → ТО bomb: `explode(area)` · freeze: `freeze(spawn, n)` · driller: `custom: «зносить блоки на шляху»` · twister: `custom: «вирівнює й перебудовує стек»`.
- КОЛИ `counter(progress, >=, n)` → ТО `speed(падіння, +)`.
- КОЛИ `reach(stack, top)` → ЯКЩО `mode(core)` → ТО `lose`.
- КОЛИ `timer(90)` → ЯКЩО `mode(zen)` → ТО `game_over`.
- КОЛИ `custom: «виконано багатосесійну ціль (6-літерне слово, 3+ ряди за раз …)»` → ТО `unlock(павер-ап)`.
- КОЛИ `level_start` → ТО `choose(до 3 павер-апів на гру)`.
- КОЛИ `game_over` → ТО `custom: «рахунок у Game Center»`, `window(end-screen)`.
- Перемога: нема — рекорд · Поразка: переповнення (Core) / кінець часу (Zen) · Рахунок: очки за слова × множник комбо.

## Керування і ввід
- Фаза фігури (жести): тап — поворот, свайп убік — зсув, свайп униз — скид.
- Фаза курсора: тап по групі одного кольору — перетворити на літери; провести пальцем по сусідніх літерах — слово; відпустити — подати.
- Обидві фази йдуть одночасно: поки падає фігура, можна читати стек.
- Перед грою — вибір до трьох павер-апів (`loadout-select`).

## Вікна, меню, HUD
- `game-screen`: колодязь, падаюча фігура, слово під пальцем (`word-preview`), `score`, `combo-meter` / `multiplier`, `timer-countdown` у Zen, слоти павер-апів.
- `mode-select`: Core (дві складності) · Zen.
- `loadout-select`: вибір павер-апів (до 3) перед партією.
- `tutorial-window`: механіки вводяться по одній.
- `end-screen`: рахунок, прогрес цілей (?); `leaderboard` Game Center.
- Переходи: меню → `mode-select` → `loadout-select` → `game-screen` → `end-screen` → меню.

## Фічі поза полем
- `objective-unlocks`: багатосесійні цілі (6-літерне слово, кілька рядів за раз, серії 4-літерних слів) відкривають павер-апи.
- `difficulty-presets`: мінімальна довжина слова 3 / 5.
- `mode-time-attack` (Zen, 90 с) і `mode-endless` (Core).
- `leaderboard-online` (Game Center), `tutorial`.

## Варіації й родичі
- [spelltower.md](spelltower.md) — та сама ідея «Tetris + Boggle» без фігур: слова по сусідах у вежі з гравітацією, 5+ — вибух сусідів.
- [boggle.md](boggle.md) — шлях по 8-сусідах; [bookworm.md](bookworm.md) — поле літер з падінням.
- Tetris (falling-match) — падіння й поворот фігур; тут ряд не чиститься, а «перефарбовується» в літери.
- Bejeweled (falling-match) — група однакового кольору як подія; тут її треба активувати тапом.
- Wordtris (1991) — літерні блоки в колодязі Tetris.
- **Осі варіацій:** звідки літери (одразу на плитках / з кольору після умови) · що чистить (ряд сам / лише слово) · подія «колір → літера» (повний ряд / група ≥ N / обидва) · тиск (стек / таймер).

## Цікавинки для курсу
- Двофазне поле: колір → літера як зміна стану клітини за шаблоном (`pattern(row_full)`, група ≥ N) — 📎.
- Flood fill групи одного кольору по тапу — 🌱.
- Слово-шлях по 8-сусідах + словник + очищення сусідів — 📎.
- Співіснування real-time фігури й курсорного вводу на одному тачі — 🥈.
- Комбо-множник з таймером бездіяльності — 🌱.
- Павер-апи з лоадаутом і розблокуванням цілями — 🥉.

## Мапа на каталог
- Є: `gravity-fall` · `piece-rotate-flip` · `swipe-gestures` · `cell-click` ↔ тап по групі · `word-validation` · `combo-multiplier` · `progress-acceleration` · `time-out` ↔ Zen · `explode-area` ↔ бомба · `leaderboard` · `mode-select` · `difficulty-levels` · `tutorial-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+path-trace-word`, `+long-word-blast` — див. [boggle.md](boggle.md), [spelltower.md](spelltower.md).
  - `+color-group-to-letters` «Група одного кольору за тапом стає літерами» · entities/state · 📎 · слоти {min_group}.
  - `+full-row-to-letters` «Повний ряд перетворюється, а не зникає» · entities/state · 🌱.
  - `+manual-row-clear` «Ряди не чистяться самі — лише дією гравця» · entities/interact · 🌱.
  - `+equip-loadout` — див. [bookworm-adventures.md](bookworm-adventures.md); тут — до 3 павер-апів на гру.
  - `+challenge-unlocks` «Багатосесійні цілі відкривають предмети» · levels/progression · 📎.
  - `+min-word-length-mode` «Мінімальна довжина слова як складність» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:path_adjacent8` — шлях по 8-сусідах без повторів; `+cond:length` — довжина слова ≥ N (обидва — як у spelltower.md; у реченнях тут — `custom`).
- `+ui:word-preview` — слово під пальцем під час ведення.
- `+window:loadout-select` — вибір павер-апів перед партією.
- `+feature:objective-unlocks` — цілі між сесіями відкривають предмети.
- `+card:color-group-to-letters`, `+card:full-row-to-letters`, `+card:manual-row-clear`.

## Джерела
- ⭐ [Wikipedia: Puzzlejuice](https://en.wikipedia.org/wiki/Puzzlejuice) — правила, режими, множник, павер-апи, команда (Asher Vollmer, Greg Wohlwend, Jimmy Hinson), реліз 2012-01-19, Android 2020.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/puzzlejuice/review/) — жести, тап по групі, рядок від краю до краю, бомби, лід, дрилі.
- [Kotaku: огляд](https://kotaku.com/puzzlejuice-blends-bejeweled-tetris-and-scrabble-into-5881241) — ряди чистить гравець, 4 павер-апи, челенджі, прискорення.

## Непевне
- (?) Розмір групи для перетворення: Wikipedia — ≥ 4 «що торкаються», Pocket Gamer — ≥ 3, Kotaku — «три кольори поруч».
- (?) Ширина/висота колодязя, превʼю наступної фігури, чи всі 7 тетроміно.
- (?) Чи падають блоки після стирання слова (Kotaku: «блоки, що йдуть далі, зсуваються») і чи чиститься ряд, якщо всі його літери пішли в слова.
- (?) Як павер-апи потрапляють на поле: обираються до 3 перед грою (Wikipedia), а спрацьовують у ланцюжку стертих блоків (Pocket Gamer); twister «вирівнює» — деталі невідомі.
- (?) Формула очок за довжину слова й розмір множника.
- (?) Zen з лімітом 90 с — так у Wikipedia (незвично для «zen»).
