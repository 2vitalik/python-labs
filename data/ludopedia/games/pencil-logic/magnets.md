---
title: Magnets (Tatham)
slug: magnets
aka: [Магніти]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/magnets.html", best: true, note: "мануал Tatham: правила, цикли кліків, параметри (Strip clues)"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html", note: "грати в браузері (JS-версія колекції)"}
  - {kind: other, url: "https://puzz.link/rules.html?magnets", note: "puzz.link: правила (сторінка рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simon+tatham+magnets+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, line-sum-clue, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, rule-variants, seed-share, save-game, undo-redo, +domino-slot-fill, +pole-repulsion, +click-cycle-states, +clue-done-toggle]
proposes: ["+cond:count_in(line, kind, op, n)", "+effect:flip(a)", "+ui:clue-done-mark", "+ui:not-blank-mark", "+window:params-dialog", "+window:game-id-dialog", "+card:domino-slot-fill", "+card:pole-repulsion", "+card:click-cycle-states"]
author: opus
date: 2026-11-09
---

# Magnets — заповни задані доміно магнітами (+/−) або нейтральними так, щоб однакові полюси не стикались

## Суть
Поле вже поділене на доміно-слоти (видно лише силуети). Гравець вирішує для кожного слота: магніт з полюсами + і − (і в який бік) або нейтральне доміно. Числа на краях кажуть, скільки + і скільки − у рядку чи стовпці. Однакові полюси не можуть стояти поруч по ребру — вони відштовхуються; нейтральні клітинки можна ставити будь-де. Незвичне: у кожного рішення три стани (магніт ↔, магніт ↔ навпаки, нейтраль), і кожен магніт одразу ставить дві протилежні мітки.

## Поле і час
- Прямокутна сітка W×H, повністю розбита на доміно (W·H/2); якщо W·H непарне, одна клітинка лишається порожньою.
- Підказки: окремо кількість + і кількість − для рядків і стовпців (частину може бути прибрано параметром Strip clues).
- Шари: силуети доміно (незмінні) · вміст слота (порожньо / магніт / нейтраль / «??» не-нейтраль) · сірі «виконані» підказки.
- Час статичний; хід = змінити стан одного доміно. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Доміно-слот | zone | 2 клітинки, орієнтація | має один стан: порожньо · магніт · нейтраль · «??» |
| Магніт | mark | полярність (+− або −+) | два протилежні полюси в клітинках слота |
| Нейтральне доміно | mark | зелене | дві нейтральні клітинки; сусідять з будь-чим |
| Мітка «??» | mark | — | нотатка «це точно магніт, полярність невідома» |
| Полюс + / − | mark | знак | не торкається по ребру полюса того ж знака |
| Підказка + / − лінії | mark | N або нема | кількість полюсів знака в рядку/стовпці; клік — «виконано» |
| Залишкова клітинка | static | — | при непарному W·H; поза будь-яким доміно |
| Курсор | mark | клітинка | керування з клавіатури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, slot)` → ЯКЩО `custom: «слот порожній»` → ТО `mark(slot, magnet)`.
- КОЛИ `input(left_click, slot)` → ЯКЩО `custom: «у слоті магніт, ще не перевернутий»` → ТО `custom: «перевернути полярність»` (`+effect:flip`).
- КОЛИ `input(left_click, slot)` → ЯКЩО `custom: «магніт уже перевертали»` → ТО `unmark(slot)`.
- КОЛИ `input(right_click, slot)` → ТО `custom: «цикл: порожньо → нейтраль → «??» → порожньо»` (`mark(slot, neutral)` / `mark(slot, not_blank)` / `unmark(slot)`).
- КОЛИ `input(left_click, clue)` → ТО `set_state(clue, done)`; повторний клік — `clear_state(clue, done)`.
- КОЛИ `constraint_broken(repel)` → ЯКЩО `same(pole_a, pole_b, sign)` and `custom: «сусіди по ребру»` → ТО `custom: «пазл не розвʼязано»`.
- Нейтраль: ЯКЩО `custom: «одна з клітинок нейтральна»` → ТО `custom: «сусідство дозволене»`.
- КОЛИ `constraint_broken(line_count)` → ЯКЩО `custom: «кількість + (або −) у лінії ≠ підказці»` (`+cond:count_in`) → ТО `custom: «пазл не розвʼязано»`.
- Відсутня підказка: ЯКЩО `custom: «підказку прибрано (Strip clues)»` → ТО `custom: «лінія не обмежена»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «кожен слот — магніт або нейтраль»` → ТО `win`.
- Дедукція «повна лінія»: якщо + і − у лінії разом дорівнюють її довжині — нейтралей у ній нема.
- Дедукція «нуль»: лінія з 0 + і 0 − — усі доміно, що її перетинають, нейтральні.
- Дедукція «сусід магніту»: поряд з + по ребру може бути лише − або нейтраль, тож відома полярність одного доміно «штовхає» полярність сусідніх.
- Дедукція Tricky: міркування про кількість нейтральних доміно й лічильники рядків/стовпців разом (з мануалу).
- Перемога: усі слоти вирішено, однакові полюси не торкаються, усі наявні підказки збігаються. Поразки й рахунку нема.

## Керування і ввід
- Ліва кнопка по слоту — цикл: магніт → магніт навпаки → порожньо.
- Права кнопка по слоту — цикл: нейтраль → «??» (не може бути нейтраллю) → порожньо.
- Ліва кнопка по підказці — посірити («виконано»), ще раз — повернути.
- Клавіатура: стрілки — курсор; Return — цикл магніту; Space — цикл нейтралі/«??».
- Спільні дії колекції Tatham (розд. 2.1): undo/redo, нова гра, рестарт, solve.

## Вікна, меню, HUD
- `game-screen`: сітка з силуетами доміно, полюси +/−, зелені нейтралі, «??», підказки + і − на краях (виконані — сірі), курсор.
- Веб-версія: кнопки New game · Restart game · Undo move · Redo move · Solve game; меню Game: Enter game ID… · Enter random seed… · Download / Upload save file… · Preferences….
- Меню Type: пресети; Custom… → `params-dialog` (Width, Height, Difficulty, Strip clues).
- `game-id-dialog` — Specific / Random Seed; `help-window` — розділ мануалу.
- Переходи: game-screen → Type → Custom → params-dialog → новий пазл.

## Фічі поза полем
- Генератор з єдиним розвʼязком; складність до Tricky (більше дедукцій про нейтралі й лічильники).
- Strip clues — генератор прибирає частину підказок, пазл стає важчим (`rule-variants`).
- Поле з непарним виміром зазвичай легше (з мануалу).
- `undo` ∞ + `redo`, `restart-level`, `auto-solve`, `seed-display` / `seed-input` / `share-code`, збереження у файл.

## Варіації й родичі
- Мануал: жанр — від Janko, у колекцію додав James Harvey.
- У сімʼї: [Tatham collection](tatham-collection.md) (оболонка), [Takuzu](takuzu.md) (двоколірне заповнення з лічильниками), [Tents](tents.md) і [Tracks](tracks.md) (лічильники на краях), [Shikaku](shikaku.md) (поділ на прямокутники — тут поділ уже даний).
- Схожі «доміно»-жанри: Dominosa у колекції Tatham (знайти поділ на доміно) (?).
- **Осі варіацій**: поділ на доміно (даний / треба знайти) · типи плиток (магніт + нейтраль / лише магніти) · підказки (усі / частина / у регіонах) · відштовхування (по ребру / і по діагоналі).

## Цікавинки для курсу
- Модель «доміно-слот зі станом», з якого виводяться значення двох клітинок — 🌱.
- Клік-цикли трьох станів на двох кнопках і «виконана» підказка — 🌱.
- Перевірка відштовхування й лічильників + і − з підсвіткою — 📎.
- Генерація розбиття сітки на доміно (випадкове паросполучення клітинок без «сиріт») — 🥉.
- Розвʼязувач пропагацією «сусід магніту» + лічильників і генератор зі Strip clues — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `line-sum-clue` ↔ підказки + і − · `cell-click`, `keyboard-controls` · `unique-puzzle-generation`, `difficulty-levels`, `difficulty-rating`, `level-solver` · `field-size-picker`, `game-settings`, `rule-variants` (Strip clues) · `seed-share`, `save-game`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+domino-slot-fill` «Поле з даних слотів-доміно; кожен слот — один з кількох типів» · entities/state · 🌱.
  - `+pole-repulsion` «Однакові полюси не стоять поруч; нейтраль сусідить з усім» · game-logic/constraints · 🌱.
  - `+click-cycle-states` «Клік перебирає 3+ стани клітинки/слота по колу» · interface/input · 🌱.
  - `+clue-done-toggle` «Клік по підказці сірить її як виконану» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:count_in(line, kind, op, n)` — повтор (кількість виду в лінії).
- `+effect:flip(a)` — перевернути орієнтацію/полярність сутності без руху (магніт, плитка, монета).
- `+ui:clue-done-mark` — повтор: підказку позначено виконаною.
- `+ui:not-blank-mark` — мітка «точно не порожньо, значення невідоме» («??»).
- `+window:params-dialog`, `+window:game-id-dialog` — повтори з Tatham collection.
- `+card:domino-slot-fill`, `+card:pole-repulsion`, `+card:click-cycle-states` — див. мапу.

## Джерела
- ⭐ [Tatham: Magnets (мануал)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/magnets.html) — правила (магніти й нейтралі, підказки +/−, однакові полюси не поруч), цикли лівої/правої кнопки, клік по підказці, параметри Width/Height/Difficulty/Strip clues, Janko і James Harvey.
- [Tatham: Magnets (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/magnets.html) — коротка інструкція, меню Game, кнопки.
- [puzz.link: Magnets](https://puzz.link/rules.html?magnets) — сторінка правил; текст рендериться JS і через WebFetch не читається.
- YouTube: пошук «simon tatham magnets puzzle».

## Непевне
- (?) Розташування підказок + і − (які краї) не перевірено.
- (?) Назва нижчого рівня (Easy?) і пресети Type не бачив; мануал згадує лише Tricky.
- (?) Підсвітка помилок (однакові полюси поруч, перевищення лічильника) — у мануалі не описана.
- (?) Оригінальна назва в Janko (ймовірно нім. «Magnete») і рік додавання в колекцію не перевірено (`year: null`).
- (?) Dominosa як родич — з памʼяті.
