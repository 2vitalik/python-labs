---
title: "Sudokuvania: Digits of Despair"
slug: sudokuvania
aka: [Sudokuvania, Судокуванія, Digits of Despair]
family: pencil-logic
also: [thinky]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: 2025
platforms: [web (SudokuPad)]
links:
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000MQQ", best: true, note: "LMG: правила (Gattai, Dynamic Fog, Dynamic Rules, Boss Puzzles), код розвʼязку, коментарі про структуру й час"}
  - {kind: play, url: "https://tinyurl.com/Sudokuvania", note: "грати в SudokuPad (лише десктоп, увімкнути Experimental > Test Large Puzzle UI)"}
  - {kind: other, url: "https://docs.google.com/document/d/1kkCESlLJRaIY8MzWWklGnDzqIW8SaO0cM-4QloaqN2w/edit?tab=t.0", note: "Player's Guide & FAQ: туман, Learned Rules, боси, перенесення прогресу між версіями, типи правил"}
  - {kind: other, url: "https://thinkygames.com/games/sudokuvania-digits-of-despair/", note: "Thinky Games: картка гри, схожі (Sudokuvania 2, Super Sudokoid)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sudokuvania+Digits+of+Despair", note: "пошук; розвʼязання"}
stage: v1
coverage: 55
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, pencil-marks, cell-click, multi-select, keyboard-controls, undo-redo, field-scaling, save-autosave, +fog-reveal, +rule-discovery, +overlapping-grids, +boss-puzzle, +line-constraints, +dot-constraints, +killer-cage, +rules-panel, +save-migration, +solution-code]
proposes: ["+trigger:reveal_by_correct", "+cond:rule_learned(rule)", "+cond:increasing", "+ui:rules-panel", "+ui:quest-progress", "+feature:save-migration", "+feature:solution-code", "+axis:rules", "+card:overlapping-grids", "+card:boss-puzzle", "+card:fog-reveal", "+card:rule-discovery"]
author: opus
date: 2026-11-09
---

# Sudokuvania: Digits of Despair — мапа 40×50 зі зчеплених судоку під туманом, де правила відкриваються як здібності метроїдванії

## Суть
Один гігантський пазл SkepticalMario на Logic Masters Deutschland (квітень 2025): мапа 40×50 складена з квадратних сіток різного розміру, що перекриваються (гаттай). Мапа вкрита туманом; правильні цифри в певних клітинках розвіюють його й відкривають нові підказки **та нові правила** — у панелі Learned Rules, як здібності в метроїдванії. Підказку можна використовувати лише тоді, коли її правило вже «вивчене». Частину клітинок (Boss Cells) заповнює лише розвʼязок окремого бос-пазла. Коментатори порівнюють прогрес із «замком» Zelda/метроїдванії; на проходження йде від ~10 до 80–90 годин.

## Поле і час
- Одна сітка 40×50 клітинок у SudokuPad; усередині — квадратні «кімнати»-сітки зі стороною N (N свій для кожної сітки), пронумеровані (Grid 2, Grid 8, Grid 9, Grid 10, Grid Z…), плюс названі зони (Throne Room, Golden Temple, courtyard, hall of illusions — з коментарів).
- Сітки перекриваються: клітинка на перетині підкоряється правилам кожної сітки, до якої належить.
- Шари клітинки: туман (над усім) · цифра/олівці/колір · елементи підказок (лінії, крапки, клітки, стрілки) · Boss Cell з емодзі-бісом.
- Час статичний; хід = вписати цифру або позначку. Туман знімають лише окремі тригери, а не кожна правильна цифра (FAQ).
- Клітинка r40c1 показує версію пазла (поточна 1.1.1).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка мапи | mark | цифра 1…N своєї сітки · олівці · колір | приймає цифру; може належати кільком сіткам |
| Квадратна сітка (Grid) | zone | сторона N; номер; лінк на бос-пазл | рядки, стовпці й регіони містять 1…N без повторів |
| Регіон сітки | zone | N клітинок; бувають нерегулярні | без повторів (Gattai Sudoku) |
| Туман | hazard | закриті клітинки | ховає цифри, підказки й правила; знімається тригерами |
| Клітинка-тригер туману | mark | прихований тригер | правильна цифра в ній розвіює заданий сетером шматок туману |
| Правило (Learned Rule) | pickup | текст + деталі по кліку | зʼявляється в панелі, коли відкрито; дозволяє користуватися підказками свого типу |
| Елемент підказки (лінія, крапка, клітка, стрілка, ліхтар, кодекс) | mark | тип правила | обмежує цифри, але «мертвий», доки правило не вивчене |
| Boss Cell | mark | емодзі-біс; одна на сітку з босом | цифру дає екран успіху бос-пазла |
| Бос-пазл | boss | окремий пазл на LMG | розвʼязок → цифра для Boss Cell; публікувались щоп'ятниці |
| Приховані пазли / сайд-квести | container | напр. «title puzzle» | бонусні завдання поза основним шляхом |
| Throne Room | zone | фінальна сітка | її 2-й рядок входить у код розвʼязку |

### Типи правил, що відкриваються (з FAQ і коментарів)
| Правило | Обмеження |
|---|---|
| Whisper Dash line | сусідні цифри на лінії різняться щонайменше на 5, навіть через розриви лінії |
| Zipline | пари клітинок лінії в сумі дають цифру центральної клітинки |
| Thermo | цифри строго зростають від колби |
| Guide Thermo | термометри, де на кожній лінії рівно одна колба (?) деталі |
| Sum Whip · Roaming Lines · Serpent lines · Scry-peeper clues | назви з FAQ; точний текст правил під туманом (?) |
| Arrow · Kropki dots · Killer cages · Lanterns · Codex cells (Grid 10) | згадані в коментарях/FAQ |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit d)` → ЯКЩО `not unique(row|col|region)` у будь-якій сітці, що містить клітинку → ТО `constraint_broken(gattai)`.
- КОЛИ `input(digit d)` → ЯКЩО `custom: «d > N сітки клітинки»` → ТО `constraint_broken(range)`.
- КОЛИ `input(digit d)` → ЯКЩО `custom: «клітинка — тригер туману»` and `custom: «d = розвʼязок»` → ТО `reveal(cells_by_setter)`.
- КОЛИ `reveal(cells)` → ЯКЩО `custom: «серед відкритого є нове правило»` → ТО `unlock(rule)` у панелі Learned Rules.
- КОЛИ `input(digit d)` біля підказки → ЯКЩО `not custom: «правило підказки вже в Learned Rules»` → ТО `custom: «підказку ігнорувати»` (чесне правило гравця, програма не перевіряє).
- КОЛИ `input(select cell)` → ТО `custom: «панель правил показує деталі сітки й лінк на її бос-пазл»` (Dynamic Rules).
- КОЛИ `input(select cell)` під туманом → ТО `custom: «можна, але автор просить не підглядати»` — правила оновлюються без урахування туману.
- КОЛИ `input(select rule)` у Learned Rules → ТО `message(rule_details)`.
- Whisper Dash: КОЛИ `input(digit)` на лінії → ЯКЩО `custom: «|a − b| < 5 для сусідів на лінії»` → ТО `constraint_broken(whisper)`.
- Zipline: КОЛИ `input(digit)` на лінії → ЯКЩО `not sum(pair, center)` → ТО `constraint_broken(zipline)`.
- Thermo: КОЛИ `input(digit)` на термометрі → ЯКЩО `not custom: «строго більша за попередню від колби»` → ТО `constraint_broken(thermo)`.
- КОЛИ `all_constraints_met` (бос-пазл) → ТО `window(end-screen)` з цифрою → гравець `mark(boss_cell, d)`.
- КОЛИ `custom: «усі клітинки мапи заповнені правильно»` → ТО `win`, `message(success)`.
- Перемога: уся мапа розвʼязана; для LMG — код із 9 цифр Boss Cells у порядку сіток + 2-й рядок Throne Room. Поразки й рахунку нема.

## Керування і ввід
- SudokuPad: клік/drag — виділити клітинки; цифри з клавіатури або екранної панелі; режими Digit / Corner / Centre / Colour; undo/redo.
- Велика мапа: увімкнути «Experimental > Test Large Puzzle UI»; зум — колесо миші або два пальці на тачпаді; панорамування drag-ом (у деяких браузерах не працює).
- Клік по правилу в Learned Rules — деталі; клік по клітинці мапи — дані її сітки й лінк на боса.
- Продуктивність: автор радить вимкнути conflict checker, калькулятор кліток і «outlines on elements».

## Вікна, меню, HUD
- `game-screen` (SudokuPad): мапа 40×50, `fog-overlay`, `+ui:rules-panel` з динамічним текстом, панель Learned Rules (вгорі ліворуч), `+ui:quest-progress` (Quest Progress, з 1.1.1 — цифри босів), цифрова панель, `undo-button`, `redo-button`, `timer-elapsed`.
- `settings-window` (SudokuPad): Experimental, conflict checker, вимкнення обводок.
- `end-screen`: повідомлення про успіх мапи; окремі екрани успіху бос-пазлів показують цифру для Boss Cell.
- Сторінка LMG пазла: правила, лінки, введення коду розвʼязку, коментарі.
- Переходи: мапа → (клік по клітинці сітки) лінк → бос-пазл у новій вкладці → цифра → назад на мапу.

## Фічі поза полем
- `autosave` прогресу в браузері (SudokuPad); оновлення пазла скидає прогрес → `+feature:save-migration`: у FAQ таблиця «alias → upgrade link», що переносить цифри в нову версію.
- `+feature:solution-code` — перевірка на LMG за кодом (цифри босів + рядок).
- Епізодичний контент: нові бос-пазли виходили на LMG щоп'ятниці.
- Player's Guide & FAQ — окремий документ (`rules-page`); приховані квести (title puzzle) і «sequence break» у Grid 2 (цифру боса можна вивести без боса).
- Нема підказок, рівнів складності, генерації — ручна робота сетера.

## Варіації й родичі
- [sudoku-variants](sudoku-variants.md) — модуль Fog of War (CtC) — прямий предок туману; [sudoku-line-dot-variants](sudoku-line-dot-variants.md) — Thermo, Arrow, Kropki, Whispers поодинці; [sudoku](sudoku.md) — гаттай-сітки (Samurai) як клас.
- [sudoku-mansion](sudoku-mansion.md) — комерційна гра того ж жанру: кімнати-судоку на мапі, класи-правила, боси.
- Sudokuvania 2: Lineage of Logic (2026) і Super Sudokoid: Final Transmission / Dark Inversion — наступники «великих мап» (Thinky Games); Sudokuvania: Digits Without Despair — легша версія (?).
- Осі варіацій: **як сходить туман** (8 сусідів / лінії видимості / сценарій сетера) · **як приходять правила** (усі відомі / відкриваються туманом / обираються класом) · **структура мапи** (окремі кімнати / гаттай-перекриття / одна сітка) · **ключі** (цифра з бос-пазла, приховані квести).

## Цікавинки для курсу
- Гаттай-мапа: сітки різного N перекриваються, клітинка перевіряється в кожній своїй сітці — 🥉 (індекс «клітинка → сітки», перевірка без повторів по всіх).
- Туман, що сходить від правильної цифри в клітинці-тригері — 🥉 (треба зберігати розвʼязок і таблицю «тригер → клітинки»).
- Правила як здібності: панель Learned Rules і «мертві» підказки до вивчення — 🥈 (стан відкритих правил + рендер/перевірка лише активних).
- Бос-клітинка: цифру дає окремий пазл — 📎 (звʼязка «рівень → ключ для іншого рівня»).
- Динамічна панель правил за вибраною клітинкою — 📎.
- Перенесення прогресу між версіями пазла — 🥈 (міграція збереження, коли змінились дані рівня).

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `conflict-highlight` · `pencil-marks` · `cell-click` · `multi-select` · `keyboard-controls` · `undo-redo` (SudokuPad) · `field-scaling` (зум і скрол мапи 40×50) · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+fog-reveal` «Туман, що сходить від правильної цифри» · game-logic/constraints · 🥉 · слот {reveal: neighbours|sightlines|scripted} (повтор із sudoku-variants).
  - `+rule-discovery` «Правила відкриваються по ходу гри» · game-logic/constraints · 🥈 (повтор; тут — явна панель вивчених правил).
  - `+overlapping-grids` «Перекриті сітки (гаттай) на одній мапі» · game-logic/constraints · 🥉 · слот {sizes: same|mixed}.
  - `+boss-puzzle` «Клітинка-ключ з розвʼязку окремого пазла» · levels/progression · 📎.
  - `+line-constraints` · `+dot-constraints` · `+killer-cage` — повтор із sudoku-variants.
  - `+rules-panel` «Панель правил поруч з полем» · interface/hud · 🌱.
  - `+save-migration` «Перенесення збереження в нову версію рівня» · game-logic/save · 🥈.
  - `+solution-code` «Код розвʼязку для перевірки на сайті» · levels/bank · 🌱.

## Пропозиції до словників
- `+trigger:reveal_by_correct` — правильна цифра як подія (повтор із sudoku-variants); тут ще й лише в клітинці-тригері.
- `+cond:rule_learned(rule)` — правило вже відкрите в панелі (умова користування підказкою).
- `+cond:increasing` — строге зростання вздовж лінії (Thermo; повтор).
- `+ui:rules-panel` — текст правил пазла поруч з полем (повтор); `+ui:quest-progress` — панель прогресу квесту (цифри босів).
- `+feature:save-migration` — перенести прогрес у нову версію пазла; `+feature:solution-code` — код розвʼязку для перевірки.
- `+axis:rules` — нове значення `unlocked`: правила відомі не з початку, а відкриваються як здібності (поруч із `fixed` / `mutable` / `discovered`).
- `+card:overlapping-grids` · `+card:boss-puzzle` · `+card:fog-reveal` · `+card:rule-discovery` — див. мапу.

## Джерела
- ⭐ [LMG: Sudokuvania: Digits of Despair](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000MQQ) — повний текст правил, код розвʼязку, примітки до версій, коментарі (час, боси, «Learned Rules»).
- [Player's Guide & FAQ](https://docs.google.com/document/d/1kkCESlLJRaIY8MzWWklGnDzqIW8SaO0cM-4QloaqN2w/edit?tab=t.0) — туман і тригери, Boss Cells, таблиця оновлень, Whisper Dash, Zipline, Guide Thermo, Codex.
- [SudokuPad](https://tinyurl.com/Sudokuvania) — сам пазл.
- [Thinky Games](https://thinkygames.com/games/sudokuvania-digits-of-despair/) — картка гри і родичі (бачив у пошуку).
- YouTube: [пошук](https://www.youtube.com/results?search_query=Sudokuvania+Digits+of+Despair).

## Непевне
- (?) Точні тексти Sum Whip, Roaming Lines, Serpent, Scry-peeper, Lanterns, Codex — ховаються під туманом; у файлі лише назви.
- (?) Guide Thermo: «на кожній лінії одна колба» — з FAQ, повного формулювання не бачив.
- (?) Розміри окремих сіток (4×4…9×9) — сторінка дає лише «N = сторона сітки».
- (?) Пошуковий опис «туман сходить навколо правильної цифри» суперечить FAQ («лише певні тригери») — у файлі версія FAQ.
- (?) Sudokuvania: Digits Without Despair — легша версія згадана в Reddit-треді, статус не перевірено.
