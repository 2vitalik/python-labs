---
title: Coffee Milk (コーヒー牛乳, Milchkaffee)
slug: coffee-milk
aka: [コーヒー牛乳, Kōhī gyūnyū, Milchkaffee, Coffee With Milk, Кава з молоком]
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?coffeemilk", best: true, note: "puzz.link: 4 правила з прикладом і вхід у плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/coffeemilk.js", note: "правила EN/JA текстом, «Nikoli vol. 156», 7 тестових станів з кодами помилок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Milchkaffee/index.htm", note: "Janko: правила DE/EN/JA, приклад 10×10 з розвʼязком, родич Milchtee"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/wblink.js", note: "код pzprjs: Coffee Milk живе у файлі Shirokuro-link (wblink)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Coffee+Milk+puzzle+nikoli", note: "пошук"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, completion-detection, markup-validity, path-drawing, edge-marking, conflict-highlight, undo-redo, in-game-editor, import-open-formats, keyboard-controls, +bridge-connect, +crossing-detection, +group-color-balance, +link-pair-ban, +trial-mode]
proposes: ["+cond:region_has", "+cond:straight_line", "+cond:crosses", "+card:group-color-balance", "+card:link-pair-ban", "+ui:loop-color-coding"]
author: opus
date: 2026-11-19
---

# Coffee Milk — зʼєднай кружки прямими лініями в групи: у кожній один сірий, а білих і чорних порівну

## Суть
На полі розкидані білі, чорні й сірі кружки. Гравець зʼєднує їх горизонтальними й вертикальними лініями без поворотів і перетинів; звʼязані кружки утворюють групу. У кожній групі рівно один сірий кружок, а білих і чорних — порівну; білий і чорний не можна зʼєднати напряму. Незвичне: мета — не одна мережа, а **розбиття на групи заданого складу**.

## Поле і час
- Квадратна сітка, кружки в клітинках; приклад Janko — 10×10, лінії сітки на картинці не намальовані.
- Лінія — прямий відрізок по центрах сусідніх клітинок між двома кружками; на першому кружку в напрямку вона закінчується (puzz.link протягує її до наступного кружка сама).
- Група — компонента звʼязності «кружки + лінії»; сірий кружок може лишитися сам — група з одного сірого (0 білих = 0 чорних).
- Шари: кружки трьох кольорів (незмінні) · лінії · хрестики «лінії нема» на межах (puzz.link `peke`).
- Час статичний; хід = провести або стерти лінію між двома кружками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Білий кружок | static | колір | має ≥ 1 лінію; напряму — лише з білим або сірим |
| Чорний кружок | static | колір | має ≥ 1 лінію; напряму — лише з чорним або сірим |
| Сірий кружок | static | колір | щонайбільше один у групі; може бути без ліній |
| Лінія | mark | пряма, кратність 1 | зʼєднує два кружки; не повертає, не перетинає інші лінії |
| Група | zone | склад | 1 сірий; білих = чорних |
| Хрестик | mark | на межі клітинок | «тут лінії нема», допоміжний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, circle → circle)` → ТО `mark(segment, line)` — увесь прямий відрізок до наступного кружка; повтор → `unmark(segment)` (puzz.link) (?).
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)` і `unmark(line)` на цій межі (puzz.link, режим peke) (?).
- КОЛИ `constraint_broken(cross)` → ЯКЩО `custom: «у порожній клітинці лінія повертає або перетинає іншу»` (`+cond:straight_line`, `+cond:crosses`) → ТО `set_state(line, error)` («There is a crossing line»).
- КОЛИ `constraint_broken(direct)` → ЯКЩО `custom: «лінія зʼєднує білий і чорний кружок»` (`+card:link-pair-ban`) → ТО `set_state(line, error)` («A white and black circle are connected directly»).
- КОЛИ `constraint_broken(gray)` → ЯКЩО `custom: «у групі ≥ 2 сірих»` (`+cond:region_has`) → ТО `set_state(group, error)` («A group has more than one gray circle»).
- КОЛИ `constraint_broken(balance)` → ЯКЩО `not same(whites, blacks, count)` → ТО `set_state(group, error)` («A group doesn't have an equal number of white and black circles»).
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `custom: «білий або чорний кружок без жодної лінії»` → ТО `set_state(circle, error)` («A white or black circle doesn't have a line»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: кожна група — один сірий і порівну білих та чорних, лінії прямі, без перетинів і без прямих пар біле–чорне. Поразки й рахунку нема.
- Чому досить «≤ 1 сірий»: білий зʼєднується лише з білим чи сірим, чорний — з чорним чи сірим, тож група з обома кольорами обовʼязково містить сірий, а одноколірна не збалансується; pzprjs так і перевіряє.
- Дедукції: лінія між двома сірими заборонена; якщо в білого (чорного) кружка лише один можливий партнер — не протилежного кольору й без перетину, — лінія туди обовʼязкова; кожен білий мусить потрапити через сірий у групу з чорним.

## Керування і ввід
- puzz.link play: протяжка від кружка до кружка малює весь прямий відрізок (код `getlinesize` продовжує лінію до найближчого кружка); у Coffee Milk одна протяжка може пройти кілька відрізків поспіль; хрестик × на межі — `peke`, він стирає лінію там.
- puzz.link edit: клік по клітинці по колу — порожньо → білий → сірий → чорний, правий клік — назад; клавіші 1 — білий, 2 або `-` — сірий, 3 — чорний, 4 / пробіл / BS — стерти.
- Жанр має `irowake: true` — кнопка перефарбування ліній дає кожній групі свій колір, склад груп видно одразу.
- Папір: лінії олівцем між центрами кружків.

## Вікна, меню, HUD
- `game-screen` (puzz.link): кружки трьох кольорів, лінії, хрестики; кнопки Check · Undo · Redo · Erase answer · Erase marks · Irowake · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` на кружках, лінії чи групі з помилкою; `+ui:loop-color-coding`.
- `help-window` — rules.html?coffeemilk.
- `editor-window` — той самий екран у режимі Edit; `+window:game-id-dialog` — URL пазла.
- Переходи: rules → плеєр за URL → Check → «розвʼязано» або текст першої помилки.

## Фічі поза полем
- `auto-check` (off / guarded / simple) і Check з текстом першого порушеного правила.
- `undo` ∞ / `redo`, `+feature:trial-mode`, кольори груп (`irowake`).
- `level-editor` + `share-code` (URL), файли pzprv3.
- `puzzle-bank`: Janko дає лінки на базу puzz.link і Puzzle Square (kind 405).

## Варіації й родичі
- Shirokuro-link (`wblink`, той самий файл pzprjs) — кожна лінія — один прямий відрізок, і її кінці мають бути різного кольору (два білі чи два чорні — помилка); сірих лімітів і балансу нема.
- Milk Tea (ミルクティー, Janko «Milchtee», Nikoli № 158, рубрика «omopa») — трійки кружків зʼєднуються лінією-літерою «T»: кінці перекладини одного кольору, кінець ніжки — іншого.
- [Hashiwokakero](hashiwokakero.md) — прямі мости між кружками, але число = кількість мостів і одна мережа.
- [Ichimaga](ichimaga.md) — один поворот дозволено, ціль — одна мережа; Magnetic Ichimaga теж забороняє певні пари кінців.
- [Kuralin](kuralin.md) — теж кружки трьох кольорів, де сірий означає «порівну».
- **Осі варіацій**: форма лінії (пряма / ≤ 1 поворот / Т-подібна) · ціль (групи заданого складу / пари / одна мережа) · склад групи (1 сірий + баланс / біле–чорне / 2 + 1 у Т) · заборонені пари (біле–чорне / однакові кольори / рівні числа).

## Цікавинки для курсу
- Кандидати-ребра: для кожного кружка — перший кружок у кожному з 4 напрямків — 🌱.
- Групи як компоненти (union-find по лініях) + склад групи (сірих ≤ 1, білих = чорних) — 📎.
- Перетини горизонтальних і вертикальних відрізків — 🌱.
- Підсвітка забороненої пари біле–чорне ще під час протяжки — 🌱.
- Розвʼязувач: вибір підмножини ребер-кандидатів без перетинів з умовами на склад кожної компоненти — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection`, `markup-validity` · `path-drawing` ↔ протяжка лінії · `edge-marking` ↔ хрестики · `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `keyboard-controls` ↔ редактор і URL.
- Перевикористано: `+bridge-connect` (Hashi; слот {max: 1, straight: true}) · `+crossing-detection` · `+trial-mode`.
- **Нема** → пропозиції карток:
  - `+group-color-balance` «Склад кожної звʼязної групи: рівно 1 сірий, білих = чорних» · game-logic/constraints · 📎 · слот {hub: 1, balance: white=black}.
  - `+link-pair-ban` (з [Ichimaga](ichimaga.md)) — тут заборонена пара біле–чорне.

## Пропозиції до словників
- `+cond:region_has` — повтор: у групі щонайбільше / рівно один сірий.
- `+cond:straight_line` — повтор: відрізок без поворотів.
- `+cond:crosses` — повтор.
- `+card:group-color-balance`, `+card:link-pair-ban` — див. мапу.
- `+ui:loop-color-coding` — повтор: `irowake` фарбує кожну групу.

## Джерела
- ⭐ [puzz.link: Coffee Milk](https://puzz.link/rules.html?coffeemilk) — правила й приклад у браузері (текст рендериться JS), вхід у плеєр.
- [pzpr-samples/coffeemilk.js](https://puzz.link/js/pzpr-samples/coffeemilk.js) — 4 правила EN/JA (лінії прямі й «cannot turn», «Lines cannot cross each other», один сірий і порівну білих і чорних, біле–чорне напряму не можна), «Puzzle Communication Nikoli vol. 156».
- [pzprjs wblink.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/wblink.js) — перевірки `lnCross` · `lcInvalid` · `lcGrayGt` · `lcBalance` · `nmNoLine`, ввід протяжкою з `getlinesize`, цикл кольорів у редакторі, Shirokuro-link.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок Coffee Milk.
- [Janko: Milchkaffee](https://www.janko.at/Raetsel/Milchkaffee/index.htm) — правила DE/EN/JA («genau einen» сірий), приклад, лінки на puzz.link/db і Puzzle Square, родич Milchtee.
- [Janko: Milchtee](https://www.janko.at/Raetsel/Milchtee/index.htm) — Milk Tea: Т-трійки, Nikoli № 158.
- YouTube: [пошук «Coffee Milk puzzle nikoli»](https://www.youtube.com/results?search_query=Coffee+Milk+puzzle+nikoli).

## Непевне
- (?) Рік: Nikoli vol. 156 (pzprjs) — за датуванням JA-Вікіпедії (№150 — весна 2015, щокварталу) ≈ вересень 2016; Janko пише, що автор і перша публікація невідомі; `year: null`.
- (?) Образ назви (чорна кава + біле молоко, змішані через сірий) — моє прочитання; Janko пояснює лише назву Milchtee.
- (?) Кнопки миші (стерти, хрестик) — загальна схема pzpr.
- (?) Бази puzz.link/db і Puzzle Square бачив лише як лінки на Janko, не відкривав; кількість пазлів невідома.
- (?) Чи лінія може пройти «крізь» кружок — у pzprjs це просто дві лінії з нього, тобто кружок у групі; окремого правила не бачив.
