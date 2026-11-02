---
title: NYT Connections (+ Strands)
slug: nyt-connections
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: none
  goal: state
year: 2023
platforms: [web, mobile (NYT Games app)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_New_York_Times_Connections", best: true, note: "правила Connections, кольори складності, червоні оселедці, Sports edition, спецвипуски"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_New_York_Times_Strands", note: "Strands: 6×8, спанграма, кожна літера рівно в одному слові, підказка за 3 нетемні слова"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_New_York_Times_Games", note: "контекст: Wordle, Spelling Bee, Digits, Crossplay, статистика ігор"}
  - {kind: play, url: "https://www.nytimes.com/games/connections", note: "грати Connections; fetch-ем не перевірено (NYT блокує)"}
  - {kind: play, url: "https://www.nytimes.com/games/strands", note: "грати Strands; fetch-ем не перевірено"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nyt+connections+how+to+play", note: "пошук; правила й геймплей"}
stage: v1
coverage: 65
mechanics: [daily-puzzle, cell-click, completion-detection, profile-stats, end-screen, game-screen, help-window, level-bank, event-effects, +group-partition, +mistake-limit, +near-miss-hint, +shuffle-board, +difficulty-tiers, +share-result, +streak-stats, +path-trace-word, +exact-cover-words, +hint-meter, +spanning-word]
proposes: ["+trigger:input", "+cond:same_group", "+cond:in_dictionary", "+cond:path_adjacent8", "+effect:feedback", "+effect:reveal", "+effect:message", "+effect:shake", "+effect:counter", "+role:tile", "+role:zone", "+ui:mistake-counter", "+ui:solved-group-bar", "+ui:hint-meter", "+ui:theme-clue", "+window:stats-window", "+window:archive-window", "+feature:share-result", "+feature:streaks", "+feature:mistake-limit", "+axis:session"]
author: opus
date: 2026-11-02
---

# NYT Connections — розбий 16 слів на 4 приховані четвірки за ≤4 помилки (+ Strands: знайди тематичні слова-шляхи в сітці літер)

## Суть
**Connections:** на полі 4×4 — 16 слів; їх треба розбити на 4 групи по 4 за прихованою ознакою (категорія, гра слів, спільне продовження). Гравець виділяє 4 плитки й надсилає; вірна група «знімається» з поля й показує назву категорії та колір складності. Головна складність — «червоні оселедці»: слова, що на вигляд пасують до кількох груп. **Strands** (той самий щоденний NYT-формат): у сітці 6×8 літер знайти тематичні слова, що разом покривають усю сітку, плюс спанграму — слово-тему, що перетинає поле від краю до краю.

## Поле і час
- Connections: 16 плиток 4×4; геометрія не має значення (сусідство не важить), сітка — лише розкладка. Після кожної вгаданої групи поле стискається: група стає смугою зверху, решта плиток переукладається.
- Strands: сітка 6 стовпців × 8 рядків літер; сусідство — 8 напрямків (?), слово = шлях по суміжних клітинах, може гнутись у будь-який бік.
- Обидві: хід = одна спроба (група / слово), часу нема; одна задача на день (сезон — дата). Connections Sports Edition додала опційний таймер.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-слово (Connections) | tile | текст, прихована група | виділяється/знімається; зникає в смугу групи, коли група вгадана |
| Група | zone (прихована) | 4 слова, категорія, колір yellow/green/blue/purple | відкривається вгадуванням або в кінці гри |
| Лічильник помилок | static | 4 | −1 за невірну четвірку; 0 → програш |
| Літера (Strands) | tile | літера, стан none/theme/spangram/hinted | належить рівно одному слову розвʼязку |
| Тематичне слово (Strands) | zone (приховане) | шлях по клітинах | фарбується в синій, коли знайдене |
| Спанграма (Strands) | zone (прихована) | шлях від краю до протилежного краю | фарбується жовтим; описує тему |
| Нетемне слово (Strands) | — | ≥ 4 літери, у словнику | не фарбується, але наповнює лічильник підказки |

## Правила (КОЛИ → ЯКЩО → ТО)
Connections:
- КОЛИ `input(tap tile)` → ЯКЩО `count(selected, <, 4)` або плитка вже виділена → ТО `custom: «перемкнути виділення»`; п'ятої виділити не можна.
- КОЛИ `input(submit)` → ЯКЩО `count(selected, ==, 4) and same_group(selected)` → ТО `reveal(group: color + category)`, `custom: «плитки злітають у смугу групи зверху»`.
- КОЛИ `input(submit)` → ЯКЩО не одна група → ТО `counter(mistakes_left, -1)`, `shake`; ЯКЩО 3 з 4 з однієї групи → ТО `message("One away...")`.
- КОЛИ `input(submit)` → ЯКЩО цю саму четвірку вже надсилали → ТО `message("Already guessed!")`, помилка не рахується.
- КОЛИ `input(shuffle)` → ТО `custom: «перемішати порядок невгаданих плиток»` (на логіку не впливає).
- КОЛИ `input(deselect all)` → ТО зняти виділення.
- КОЛИ `count(groups_found, ==, 4)` → ТО `win`, `window(end-screen)`; КОЛИ `counter(mistakes_left, ==, 0)` → ТО `lose`, `reveal(all groups)`.
- Кольори складності: yellow (найпростіша) → green → blue → purple (найскладніша, часто гра слів); у кожному випуску — рівно по одній групі кожного кольору.
- Рахунок: перемога/поразка + кількість помилок; порядок знайдених груп видно в share-сітці (purple першою — «хизування»).

Strands:
- КОЛИ `input(trace path)` → ЯКЩО `path_adjacent8(path) and count(path, >=, 4)` → ТО перевірка слова.
- КОЛИ `custom: «шлях = тематичне слово з розвʼязку»` → ТО `paint(path, blue)`, `counter(theme_found, +1)`; КОЛИ шлях = спанграма → ТО `paint(path, yellow)`.
- КОЛИ слово `in_dictionary`, але не тематичне → ТО `counter(hint_meter, +1)`; КОЛИ `counter(hint_meter, ==, 3)` → ТО кнопка Hint активна.
- КОЛИ `input(hint)` → ТО `custom: «підсвітити літери одного тематичного слова (без порядку)»`, `counter(hint_meter, =0)`; повторна підказка на те саме слово показує порядок літер (?).
- Спанграма торкається двох протилежних країв сітки (лівий–правий або верх–низ); може починатись не з краю.
- Слова розвʼязку не перетинаються, кожна літера сітки — рівно в одному слові (точне покриття сітки шляхами).
- КОЛИ `all_constraints_met` (усі тематичні слова + спанграма) → ТО `win`; програшу нема — лише кількість використаних підказок.

## Керування і ввід
- Connections: тап по плитці — виділити/зняти; кнопки Shuffle, Deselect All, Submit (активна лише при 4 виділених).
- Strands: drag пальцем/мишею по суміжних літерах; або тап по літерах по черзі й повторний тап по останній для підтвердження (?). Кнопка Hint.
- Клавіатурного вводу нема.

## Вікна, меню, HUD
- Connections `game-screen`: «Create four groups of four!», сітка 4×4, `solved-group-bar` (смуги вгаданих груп кольором з категорією), `mistake-counter` («Mistakes remaining: ● ● ● ●»), кнопки Shuffle / Deselect All / Submit, `toast` («One away…», «Already guessed!»).
- Strands `game-screen`: `theme-clue` («Today's theme: …»), сітка 6×8, поточне слово над сіткою, «N of M theme words found», `hint-meter` + кнопка Hint.
- `help-window` («How to play»): правила з прикладами категорій (Connections) / спанграми (Strands).
- `end-screen`: результат + `share-button`; Connections — сітка спроб кольоровими квадратами 🟨🟩🟦🟪 (рядок = одна спроба); Strands — ряд кружечків 🔵 тема, 🟡 спанграма, 💡 підказка в порядку подій (?).
- `stats-window` (Connections): Completed · Win % · Current Streak · Max Streak · Perfect Puzzles · розподіл помилок (?).
- `archive-window`: архів Connections для передплатників; архів Strands — з вересня 2025.
- Переходи: вхід → `help-window` (перший раз) → `game-screen` → `end-screen` → `stats-window`.

## Фічі поза полем
- `mode-daily` / `daily-puzzle`: одна задача на день; редактори — Wyna Liu (Connections), Tracy Bennett (Strands, і Wordle).
- `share-result` — спойлер-вільна сітка/ряд емодзі; `streaks`, `stats`, `cloud-save` через акаунт NYT.
- `mistake-limit` (4) як головне обмеження Connections; у Strands — немає програшу, «ціна» — підказки.
- Спецвипуски Connections: емодзі (1 квітня 2024), символи й літери (2025), ребуси (2026), Sports Edition (The Athletic, з таймером), Soccer Edition (2026).
- `puzzle-bank` (архів) — платна фіча.

## Варіації й родичі
- Connecting Wall з британського квізу *Only Connect* — прямий предок Connections (16 підказок → 4 групи, ліміт часу й спроб).
- Strands — нащадок word search і Boggle, але з точним покриттям сітки (як пентаміно/Numberlink для слів).
- Інші NYT: Wordle, Spelling Bee (слова ≥ 4 літер з 7 літер «стільника», панграми), Digits (6 чисел і арифметика → ціль, 2023), Crossplay (Scrabble-подібна, 2025–2026).
- **Осі варіацій:** що групуємо (слова / емодзі / числа) · розмір групи й кількість груп · бюджет помилок (4 / без ліміту + підказки) · фідбек близькості («One away» / нічого) · просторове обмеження (нема в Connections / шлях суміжності в Strands).

## Цікавинки для курсу
- Connections: розбиття 16 на 4×4 з перевіркою четвірки, «One away», «Already guessed», ліміт помилок — 🌱 (усе з даних головоломки).
- Shuffle і стиснення поля після кожної групи (переукладання) — 🌱.
- Share-сітка кольорів у порядку спроб + серії — 📎.
- Strands: трасування слова по 8-суміжних клітинах без повтору клітини — 🥉.
- Лічильник підказки за нетемні слова (словник + «3 → 1 підказка») — 📎.
- Перевірка спанграми (шлях торкається протилежних країв) — 🌱.
- Генератор Strands: покрити 6×8 непересічними шляхами-словами заданої теми — 👑 (дитина `unique-puzzle-generation`, задача точного покриття).

## Мапа на каталог
- Є: `daily-puzzle` · `cell-click` ↔ виділення плиток · `completion-detection` ↔ 4 групи / всі слова · `profile-stats` · `level-bank` ↔ архів · `end-screen` · `game-screen` · `help-window` · `event-effects` ↔ злітання групи, трясіння на помилці.
- **Нема** → пропозиції карток:
  - `+group-partition` «Розбити набір на приховані групи» · game-logic/win · 📎 · слоти {groups: 4, size: 4}.
  - `+mistake-limit` «Ліміт помилок» · game-logic/lose · 🌱 · слоти {mistakes: 4} (близька до `wrong-mark-lose`).
  - `+near-miss-hint` «Підказка близькості (One away)» · game-logic/constraints · 🌱.
  - `+shuffle-board` «Перемішати розкладку» · interface/input · 🌱.
  - `+difficulty-tiers` «Кольорові рівні складності груп» · interface/hud · 🌱.
  - `+share-result`, `+streak-stats` — див. wordle.md.
  - `+path-trace-word` «Слово трасуванням по суміжних клітинах» · interface/input · 🥉 · слоти {adjacency: 4|8} — Strands, Boggle.
  - `+exact-cover-words` «Слова покривають усе поле без перетинів» · game-logic/constraints · 🥉.
  - `+hint-meter` «Підказка, зароблена побічними діями» · game-logic/difficulty · 📎 · слоти {cost: 3}.
  - `+spanning-word` «Слово-перетин від краю до краю» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+trigger:input` — tap / submit / shuffle / drag-path / hint.
- `+cond:same_group` — усі виділені з однієї прихованої групи; `+cond:in_dictionary`; `+cond:path_adjacent8` — шлях по 8-суміжних клітинах без повторів.
- `+effect:feedback`, `+effect:reveal` (⏳), `+effect:message`, `+effect:shake`, `+effect:counter` (⏳).
- `+role:tile`, `+role:zone` (група/слово як прихована область).
- `+ui:mistake-counter` (⏳) — крапки помилок; `+ui:solved-group-bar` — смуга вгаданої групи з категорією; `+ui:hint-meter` — шкала заробленої підказки; `+ui:theme-clue` — текст теми.
- `+window:stats-window`; `+window:archive-window`.
- `+feature:share-result`, `+feature:streaks`, `+feature:mistake-limit` (⏳).
- `+axis:session` — `daily`.

## Джерела
- ⭐ [Wikipedia: The New York Times Connections](https://en.wikipedia.org/wiki/The_New_York_Times_Connections) — правила, кольори складності (рівно одна група кожного), червоні оселедці, Only Connect, Sports Edition, спецвипуски.
- [Wikipedia: The New York Times Strands](https://en.wikipedia.org/wiki/The_New_York_Times_Strands) — сітка 6×8, слова ≥ 4, спанграма між протилежними краями, точне покриття, підказка за 3 нетемні слова.
- [Wikipedia: The New York Times Games](https://en.wikipedia.org/wiki/The_New_York_Times_Games) — контекст NYT-ігор, Digits, Crossplay, архів Strands.
- [NYT Connections](https://www.nytimes.com/games/connections) і [NYT Strands](https://www.nytimes.com/games/strands) — грати (fetch заблоковано).
- YouTube: пошук «nyt connections how to play».

## Непевне
- (?) Тексти «One away...», «Already guessed!», кнопки Shuffle/Deselect All/Submit, «Mistakes remaining» — з памʼяті; NYT-сторінки не відкрились, а WebSearch вичерпано. Вікі каже лише «чотири спроби».
- (?) Поля `stats-window` Connections (Perfect Puzzles, розподіл помилок) — з памʼяті.
- (?) Strands: 8-сусідство (вікі: «у будь-якому напрямку»), повторна підказка показує порядок літер, введення тапами, емодзі share-рядка — з памʼяті.
- (?) Чи можна вручну переставляти плитки Connections (drag) — у деяких версіях застосунку, не перевірено.
