---
title: "Super Sudokoid: Dark Inversion"
slug: super-sudokoid
aka: [Super Sudokoid, "Super Sudokoid: Final Transmission", Супер Судокоїд]
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
year: 2026
platforms: [web (SudokuPad)]
links:
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000SQ0", best: true, note: "LMG: правила Dark Inversion (16 секторів 4×4, туман, HUD, боси, апгрейди, стіни), код розвʼязку, версії, коментарі"}
  - {kind: play, url: "https://sudokupad.app/xfq6z64i66?setting-arrowsabovelines=1", note: "Dark Inversion у SudokuPad (лише десктоп)"}
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000RPZ", note: "LMG: Final Transmission — перша частина (сектори, що перекриваються, Learnt Rules, евакуаційна лінія)"}
  - {kind: play, url: "https://sudokupad.app/bidav30cfk?setting-arrowsabovelines=1", note: "Final Transmission у SudokuPad"}
  - {kind: other, url: "https://skaldlab.studio/Metrosudokuvania/", note: "Metrosudokuvania (Skald) — вебпроєкт, куди автор дозволив включити пазли"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Super+Sudokoid", note: "пошук; розвʼязання"}
stage: v1
coverage: 50
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, pencil-marks, cell-click, multi-select, keyboard-controls, undo-redo, field-scaling, save-autosave, world-map, +fog-reveal, +rule-discovery, +boss-puzzle, +overlapping-grids, +rules-panel, +solution-code, +save-migration, +line-constraints, +story-journal, +hud-cells, +wall-cells]
proposes: ["+trigger:reveal_by_correct", "+cond:rule_learned(rule)", "+ui:rules-panel", "+ui:hud-cells", "+feature:save-migration", "+feature:solution-code", "+axis:rules", "+card:hud-cells", "+card:wall-cells"]
author: opus
date: 2026-11-19
---

# Super Sudokoid: Dark Inversion — 16 судоку-секторів під туманом, HUD із клітинок, боси й апгрейди як у метроїдванії

## Суть
Великий пазл The M на Logic Masters Deutschland (травень 2026), сиквел Super Sudokoid: Final Transmission (березень 2026) і наступник жанру Sudokuvania. Поле — 16 секторів-судоку 9×9 у сітці 4×4 під туманом: правильні цифри знімають туман і відкривають нові правила, апгрейди, події та сюжет («загублений світ раси Puzzlo»). Уся службова інформація живе в **HUD із клітинок на правому краї поля**: клік по відкритій HUD-клітинці дописує новий розділ в опис пазла. Боси — окремі пазли; їхні цифри вписують у HUD, і з них складається код розвʼязку. Складність 5/5; проходження в коментарях — від ~28 годин до тижня.

## Поле і час
- Dark Inversion: 16 секторів у сітці 4×4, кожен — окреме класичне судоку 9×9; інші правила можуть охоплювати кілька секторів і діють на всі задіяні клітинки.
- Межі регіонів видно завжди (коментар), решту поля ховає туман.
- HUD — клітинки на правому краї поля: відкриті несуть інформацію; закриті натискати не радять — це спойлер майбутніх відкриттів.
- Шари клітинки: туман · цифра / олівці / колір · елементи правил (лінії, кружки, емодзі) · спецклітинки: стіна, рожева «косметична», жовтий кружок апгрейда, біс-бос.
- Final Transmission: сектори частково **перекриваються** — спільна клітинка належить обом; цифри різних секторів не конфліктують навіть в одному рядку чи стовпці.
- Час статичний; хід = цифра чи позначка. Версії Dark Inversion 1.0.0…1.0.5, Final Transmission — до 1.1.2.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сектор | zone | 9×9, номер 1–16 | рядки, стовпці й блоки 3×3 без повторів у межах сектора |
| Клітинка | mark | цифра 1–9 · олівці · колір | приймає цифру; може лежати під туманом |
| Туман | hazard | закриті клітинки | ховає цифри, правила, спецклітинки; правильні цифри його знімають |
| HUD-клітинка | switch | відкрита / закрита | клік по відкритій дописує розділ в опис пазла |
| Бос (емодзі-біс) | boss | клітинка в секторі + клітинка HUD | після цифри в секторі HUD-клітинка веде на бос-пазл |
| Бос-пазл | boss | окремий пазл за посиланням з HUD | розвʼязок дає цифру для HUD-клітинки боса |
| Апгрейд (жовтий кружок) | pickup | — | після заповнення в HUD зʼявляється нове |
| Стіна | static | напр. фіолетові клітинки внизу | звичайні правила судоку не діють; її правило — в описі |
| Рожева клітинка | terrain | косметика | вважати такою самою, як сусіди |
| Правило-підказка | mark | тип: thermo, renban, Fillomino, змія, Wits… | обмежує цифри; відкривається по ходу (?) |
| Ключі й руни | pickup | — | збираються; ведуть нелінійне проходження (коментарі) |
| Журнал (Log NN) | container | номер | сюжетна подія; щонайменше 28 сюжетних моментів (коментар) |

### Final Transmission — відмінності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сектор, що перекривається | zone | спільні клітинки | спільна клітинка підкоряється обом судоку |
| Learnt Rules | zone | список у верхньому правому куті | клік по правилу — детальний опис і базові підказки |
| Евакуаційна лінія | mark | від корабля крізь тунелі, клітки, сади | її треба провести; код — перші 3 цифри з її кінця |
| Телепорти, змія «Worm Food», огляд ферзя й слона, хмарочоси, прицільні стрілки | mark | — | правила під туманом; змія не торкається себе (коментарі) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit d, cell)` → ЯКЩО `custom: «d — правильна цифра клітинки, до якої привʼязано туман»` → ТО `reveal(cells)` (`+trigger:reveal_by_correct`).
- КОЛИ `constraint_broken(sector)` → ЯКЩО `not unique(row|col|box)` у межах сектора → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(rule)` → ЯКЩО `custom: «порушено відкрите правило, що може охоплювати кілька секторів»` → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `input(select, hud_cell)` → ЯКЩО `custom: «HUD-клітинка відкрита»` → ТО `message(new_section)` — опис пазла росте новим розділом.
- КОЛИ `input(digit, boss_cell)` → ТО `custom: «HUD-клітинка цього боса стає посиланням на бос-пазл»`.
- КОЛИ `all_constraints_met` (бос-пазл) → ТО `custom: «розвʼязок дає цифру»`, гравець `mark(hud_boss_cell, d)`.
- КОЛИ `input(digit, upgrade_cell)` → ТО `unlock(upgrade)`; автор: «перевір HUD».
- КОЛИ `input(digit, wall_cell)` → ТО `custom: «звичайні правила судоку не діють; що можна — каже правило стін»`; фіолетові стіни внизу відкритої частини автор просить не заповнювати.
- КОЛИ `input(digit, fog_cell)` → ЯКЩО `custom: «цифра вже відома логікою»` → ТО `mark(cell, d)`; вгадувати не слід (правило пазла, програма не перевіряє).
- Рожеві клітинки — косметика: для всіх правил вони «такі самі, як сусіди».
- Final Transmission: КОЛИ `input(select, rule)` у Learnt Rules → ТО `message(rule_details)`.
- Final Transmission: КОЛИ `input(digit)` біля підказки → ЯКЩО `not custom: «правило підказки вже вивчене»` → ТО `custom: «підказкою не користуватись»` (`+cond:rule_learned`).
- Final Transmission: з версії 1.1.0 повтори в рядку, стовпці й блоці підсвічуються (`conflict-highlight`).
- КОЛИ `custom: «усі сектори розвʼязано, цифри босів у HUD»` → ТО `win`; код на LMG — цифри HUD-клітинок босів у порядку босів (зліва направо, згори вниз). Final Transmission: від кінця евакуаційної лінії — перші три цифри вздовж неї.
- Поразки й рахунку нема.

## Керування і ввід
- SudokuPad: клік або drag — виділити клітинки; цифри з клавіатури чи екранної панелі; режими Digit / Corner / Centre / Colour; undo / redo.
- Клік по клітинці поля безпечний (Dark Inversion); у Final Transmission він показує правила свого сектора в описі. Клік по відкритій HUD-клітинці — новий розділ опису.
- Рекомендовані налаштування SudokuPad: Draw Arrows Above Lines (вшито в посилання), Disable Emoji Replacement (у Firefox на macOS з ним зникали емодзі босів), Test Large Puzzle UI (Final Transmission); лише десктоп.
- Бос-пазли відкриваються окремими посиланнями.

## Вікна, меню, HUD
- `game-screen` (SudokuPad): поле з 16 секторів, `fog-overlay`, HUD-клітинки на правому краї (`+ui:hud-cells`), панель опису, що росте розділами (`+ui:rules-panel`), цифрова панель, `undo-button`, `redo-button`, `timer-elapsed`.
- `settings-window` (SudokuPad): стрілки над лініями, заміна емодзі, інтерфейс великого пазла.
- `end-screen`: розвʼязаний бос-пазл дає цифру для HUD (як саме показує — (?)).
- Сторінка LMG: історія-вступ, правила, посилання на старі версії й інструкція перенесення прогресу, поле коду розвʼязку, коментарі.
- Final Transmission: список Learnt Rules у верхньому правому куті — клік відкриває деталі й підказки.
- Переходи: LMG → SudokuPad-мапа → (бос відкрито) посилання в HUD → бос-пазл → цифра → назад у HUD → … → код на LMG.

## Фічі поза полем
- `autosave` у браузері (SudokuPad). Оновлення версії скидає прогрес → `+feature:save-migration`: автор описав перенесення (вписати знайдену цифру в нову версію, розвʼязати сусідню, перенести цифри назад); у Final Transmission — лишатись на старій версії.
- `+feature:solution-code` — перевірка розвʼязку кодом на LMG.
- Спільнота: CTC Discord і форум LMG як місце підказок; китайський переклад готовий, японський дозволено; ремастер Final Transmission дозволено іншому автору; автор дозволив включити пазли в Metrosudokuvania (Skald).
- Нема генерації, рівнів складності, кнопки підказки — ручна робота автора; бажане від гравців — вимикач автозняття туману (коментар).

## Варіації й родичі
- **Final Transmission** (березень 2026, 3/5, 7,5–16 год): корабель розбився на планеті Sudoku-45; сектори перекриваються, правила — списком Learnt Rules, боси за посиланням з опису сектора, евакуаційна лінія крізь тунелі, клітки й сади, телепорти, змія «Worm Food». Коментатори називають її легшою за Sudokuvania.
- **Dark Inversion** — що нового: сектори сіткою 4×4 без перекриття; правила й новини приходять HUD-клітинками; стіни, апгрейди-кружки, ключі, руни, журнали подій; складність 5/5.
- [sudokuvania](sudokuvania.md) — пряме натхнення: гаттай-мапа під туманом, Learned Rules, Boss Cells; [sudoku-mansion](sudoku-mansion.md) — комерційна гра того ж жанру; [sudoku-variants](sudoku-variants.md) — модуль туману; [sudoku-line-dot-variants](sudoku-line-dot-variants.md) — thermo, renban; [fillomino](fillomino.md) — правило Fillomino, вбудоване в судоку.
- Осі варіацій: **структура мапи** (гаттай-перекриття / сітка секторів) · **де живуть правила** (список вивчених / HUD-клітинки / панель класу) · **що рухає прогрес** (туман / апгрейди / ключі) · **що дає бос** (цифру в клітинку мапи / цифру в HUD для коду).

## Цікавинки для курсу
- HUD із клітинок самого поля: клітинка-кнопка, що дописує текст опису, — 📎 (інтерфейс як частина рівня).
- Туман, що сходить від правильної цифри, і таблиця «клітинка-тригер → відкриті клітинки» — 🥉.
- Апгрейд як ключ до нових дедукцій у вже відкритих секторах (бектрекінг метроїдванії) — 🥈.
- Клітинки-стіни, на які не діють загальні правила, — 📎 (виняток у перевірці).
- Незалежні сектори + правила, що перетинають сектори, — 🥉 (кожне правило знає свої клітинки).
- Перенесення прогресу між версіями пазла — 🥈.
- Код розвʼязку з цифр босів у фіксованому порядку — 🌱.

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `conflict-highlight` · `pencil-marks` · `cell-click` · `multi-select` · `keyboard-controls` · `undo-redo` (SudokuPad) · `field-scaling` (великий пазл, зум) · `save-autosave` · `world-map` (сітка секторів, що відкриваються з туману).
- **Нема** → пропозиції карток:
  - `+hud-cells` «HUD із клітинок поля: клік дописує розділ опису» · interface/hud · 📎.
  - `+wall-cells` «Клітинки-винятки із загальних правил» · game-logic/constraints · 📎.
  - Повтори: `+fog-reveal` · `+rule-discovery` · `+boss-puzzle` · `+overlapping-grids` (Final Transmission) · `+rules-panel` · `+solution-code` · `+save-migration` · `+line-constraints` · `+story-journal`.

## Пропозиції до словників
- `+trigger:reveal_by_correct` — правильна цифра як подія, що знімає туман (повтор Sudokuvania).
- `+cond:rule_learned(rule)` — правило вже відкрите; умова користування підказкою (повтор).
- `+ui:rules-panel` — опис правил поруч з полем, що росте розділами (повтор); `+ui:hud-cells` — інформаційні клітинки на краю поля.
- `+feature:save-migration` · `+feature:solution-code` — повтори Sudokuvania.
- `+axis:rules` — значення `unlocked`: правила відкриваються як здібності.
- `+card:hud-cells` · `+card:wall-cells` — див. мапу.

## Джерела
- ⭐ [LMG: Super Sudokoid Dark Inversion](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000SQ0) — The M, 9.05.2026, 5/5, правила (сектори, туман, HUD, боси, апгрейди, стіни, рожеві клітинки), код розвʼязку, версії 1.0.0–1.0.5, коментарі (час, руни, ключі, журнали, Fillomino, thermo, renban, змія, Wits).
- [LMG: Super Sudokoid: Final Transmission](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000RPZ) — 3.03.2026, 3/5, сектори, що перекриваються, Learnt Rules, боси, евакуаційна лінія, налаштування SudokuPad.
- [SudokuPad: Dark Inversion](https://sudokupad.app/xfq6z64i66?setting-arrowsabovelines=1) · [SudokuPad: Final Transmission](https://sudokupad.app/bidav30cfk?setting-arrowsabovelines=1) — самі пазли.
- [Metrosudokuvania](https://skaldlab.studio/Metrosudokuvania/) — посилання зі сторінки LMG (сам проєкт не відкривав).
- YouTube: [пошук](https://www.youtube.com/results?search_query=Super+Sudokoid).

## Непевне
- (?) Назва «Dark Inversion» на сторінці не пояснена; механіки «інверсії» не бачив (у коментарі — лише «anti-sudoku»).
- (?) Точні правила стін, рун, ключів, Wits, змії й Fillomino — під туманом; у файлі лише назви з коментарів.
- (?) Кількість босів і HUD-клітинок не вказана (згадано щонайменше 6 босів).
- (?) Чи знімає туман кожна правильна цифра, чи лише клітинки-тригери, як у Sudokuvania, — сторінка каже «may be lifted».
- (?) Деталі Final Transmission (евакуаційна лінія, телепорти, Worm Food, ферзь і слон) — з коментарів, не з тексту правил.
- (?) Режими SudokuPad (Digit / Corner / Centre / Colour) — загальні для SudokuPad, у цьому пазлі окремо не перевіряв.
