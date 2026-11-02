---
title: Yin-Yang (Інь-Ян, Shiromaru-Kuromaru)
slug: yin-yang
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1993
platforms: [paper, web, mobile]
links:
  - {kind: other, url: "https://erikdemaine.org/fonts/yinyang/", best: true, note: "Demaine: правила, історія (Puzzler №137, 1993), похідне правило шахівниці 2×2, NP-повнота, шрифт-пазли"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/Yin_Yang", note: "WPC-вікі: правила, автор Minako Sakai, Outside Yin Yang, раунди WPC"}
  - {kind: other, url: "https://erikdemaine.org/papers/YinYang_CCCG2021/paper.pdf", note: "CCCG 2021: доведення NP-повноти, похідні правила"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/yinyang.js", note: "puzz.link: правила, 5 кодів помилок"}
  - {kind: other, url: "https://www.puzzles-mobile.com/build/partials/help-fbb989da7b.yin-yang.html", note: "puzzles-mobile: довідка до гри (цифрова версія)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cracking+the+cryptic+yin+yang+sudoku", note: "пошук; Yin-Yang як шар поверх судоку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yin+yang+logic+puzzle+how+to+solve", note: "пошук; розвʼязання класики"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, reachability-check, level-solver, unique-puzzle-generation, level-bank, import-open-formats, in-game-editor, +undo-redo, +input-scheme-toggle, +no-2x2-check, +global-connectivity, +constraint-overlay, +two-color-connectivity]
proposes: ["+trigger:pattern(checker2x2)", "+cond:border_color_changes", "+card:two-color-connectivity", "+card:perimeter-color-check"]
author: opus
date: 2026-11-02
---

# Yin-Yang — розфарбуй усе в два кольори так, щоб кожен колір був одним шматком без квадратів 2×2

## Суть
Кожна клітинка отримує чорний або білий кружечок; частина кружечків дана. Обидва кольори мусять бути **кожен** однією ортогонально звʼязною групою, і жоден квадрат 2×2 не може бути одного кольору. Незвичне: симетрична двоколірна звʼязність — на площині дві звʼязні області, що разом заповнюють прямокутник, переплітаються, як знак інь-ян; звідси сильні топологічні дедукції (шахівниця 2×2 неможлива, на периметрі колір змінюється щонайбільше двічі). Окремо живе як **шар обмежень поверх судоку** (Yin-Yang sudoku в YouTube-каналі Cracking the Cryptic) (?).

## Поле і час
- Прямокутна сітка; клітинки: дана (чорна/біла) · порожня. Вільних «нічиїх» клітинок у розвʼязку нема — заповнення повне.
- Сусідство ортогональне для звʼязності обох кольорів; квадрати 2×2 — усі вікна 2×2 сітки.
- Шари: дані кружечки (незмінні) · стан клітинки гравця: порожньо / чорний / білий.
- Час статичний; хід = зміна стану однієї клітинки.
- У судоку-накладці: те саме поле 9×9, кожна клітинка має і цифру, і колір (шейдинг) — два незалежні шари з власними обмеженнями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Даний кружечок | static | колір black / white | незмінний, задає дедукцію |
| Клітинка | mark | стан empty / black / white | клік змінює стан |
| Чорна група | zone | кількість компонент | усі чорні — одна 4-звʼязна компонента |
| Біла група | zone | кількість компонент | усі білі — одна 4-звʼязна компонента |
| Вікно 2×2 | zone | 4 клітинки | не одноколірне; шахове також неможливе (похідне правило) |
| Периметр поля | zone | цикл крайових клітинок | колір змінюється ≤ 2 разів (похідне правило) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, black)`; повтор → `unmark(cell)` (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, white)` (?).
- КОЛИ `pattern(block2x2)` — ЯКЩО `same(4 cells, color)` → ТО `constraint_broken(no_2x2)` (puzz.link `ms2x2` / `mu2x2` — окремо для двох кольорів).
- КОЛИ `constraint_broken(black_connected)` — ЯКЩО `not connected(black)` → ТО конфлікт (`msDivide`).
- КОЛИ `constraint_broken(white_connected)` — ЯКЩО `not connected(white)` → ТО конфлікт (`muDivide`).
- КОЛИ `constraint_broken(cell_empty)` — ЯКЩО `cell(x, empty)` → ТО конфлікт (`ceNoNum`: не всі клітинки заповнені).
- КОЛИ `pattern(checker2x2)` — вікно 2×2 у шаховому порядку → ТО `custom: «конфлікт: хоч один колір неминуче розірваний»` (Demaine: позначається як помилка) (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Похідне правило периметра: якщо обійти край поля, чорні й білі утворюють не більше ніж по одній дузі (інакше дві чорні дуги, розділені білими, не зʼєднати, не розрізавши білих — планарність).
- Дедукції: шахівниця 2×2 заборонена → у вікні з трьома відомими, де дві діагональні однакові, четверта визначена; клітинка, що інакше відрізала б острів свого кольору, — того самого кольору, що й острів; на периметрі заповнити проміжок між двома однаковими крайовими дугами.
- Перемога: усі клітинки заповнені, кожен колір звʼязний, нема одноколірних 2×2. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: ліва — чорний кружечок, права — білий; повтор — стерти; drag протягує (?).
- puzz.link edit: поставити дані кружечки (ті самі кнопки в edit mode) (?).
- Мобільні плеєри (puzzles-mobile): тап циклює порожньо → чорний → білий (?).
- Судоку-накладка (цифрова версія, напр. SudokuPad): цифри — клавіатурою, колір — режим «Color» з палітрою; дві різні розмітки однієї клітинки (?).

## Вікна, меню, HUD
- `game-screen`: сітка кружечків + `conflict-highlight` (одноколірний 2×2, розірвані групи, порожні клітинки).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode, експорт URL.
- `help-window` — правила (puzzles-mobile: довідка; Demaine — сторінка шрифту).
- `puzzle-select` — розміри й складності (puzzles-mobile) (цифрова версія) (?).
- `end-screen` — розвʼязано.
- Судоку-накладка: `game-screen` з `mode-toggle` (цифра / олівець / колір).

## Фічі поза полем
- `auto-check` за кнопкою; `undo`/`redo`.
- `level-editor` + `share-code` (puzz.link URL).
- `puzzle-bank` (Puzzler з 1993, WPC 2013–2019), `daily-puzzle` у мобільних колекціях (?).
- Demaine «Yin-Yang Font» — 26 пазлів з унікальним розвʼязком, де чорні утворюють літеру; текст набирається пазлами — незвичний `share-code`.

## Варіації й родичі
- **Outside Yin Yang** (Jürgen Blume-Nienhaus, WPC 2019): числа зовні — найдовша серія однієї частини в рядку/стовпці.
- Гібриди: Permaculture (з Masyu), Matchmaker (WPC 2016).
- **Yin-Yang sudoku**: класичне судоку + повне двоколірне розфарбування з правилами Yin-Yang; цифри й кольори повʼязані додатковими підказками автора (?).
- Родичі: Nurikabe (звʼязність одного кольору + нема 2×2), Tapa і LITS (стіна без 2×2), Takuzu/Unruly (два кольори без звʼязності), Hex (топологія двох кольорів).
- **Осі варіацій**: скільки кольорів звʼязні (один / обидва) · заборонений шаблон (2×2 одного кольору / шахівниця / нема) · підказки (дані кружечки / числа зовні / цифри судоку).

## Цікавинки для курсу
- Двоколірне повне заповнення з циклом станів клітинки — 🌱.
- Звʼязність кожного кольору (два flood fill) — 📎.
- Заборона одноколірних 2×2 і похідна заборона шахівниці — 🌱.
- Перевірка периметра «≤ 2 зміни кольору» — 🌱, але гарний приклад планарного аргументу.
- Розвʼязувач: локальні 2×2 + периметр + «точка розрізу» для кожного кольору — 🥇.
- Накладка поверх судоку: два шари розмітки в одній клітинці (цифра + колір) з незалежними перевірками — 🥉.
- Генератор: випадкове «дерево» чорних, доповнення якого теж звʼязне, без 2×2 + мінімізація даних (як у Demaine-шрифті) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` · `reachability-check` ↔ звʼязність кольорів · `level-solver`, `unique-puzzle-generation` ↔ Demaine-шрифт (жадібне прибирання підказок) · `level-bank` · `import-open-formats` · `in-game-editor`.
- Перевикористано: `+undo-redo`, `+input-scheme-toggle` (кнопка = колір / цикл), `+no-2x2-check` (слот shape: mono + checker), `+global-connectivity` (тут для кожного кольору), `+constraint-overlay` (з sudoku-variants: накладка на судоку).
- **Нема** → пропозиції карток:
  - `+two-color-connectivity` «Повне двоколірне заповнення, кожен колір звʼязний» · game-logic/constraints · 📎 · слот {colors: 2, full_fill: true}.
  - `+perimeter-color-check` «Кількість змін кольору вздовж периметра» · game-logic/constraints · 🌱 — похідне топологічне правило.

## Пропозиції до словників
- `+trigger:pattern(checker2x2)` — значення для `pattern(shape)`: шахове вікно 2×2.
- `+cond:border_color_changes` — скільки разів колір змінюється при обході краю поля.
- `+card:two-color-connectivity`, `+card:perimeter-color-check` — див. мапу.

## Джерела
- ⭐ [Erik Demaine: Yin-Yang Font](https://erikdemaine.org/fonts/yinyang/) — правила, Puzzler №137 (березень 1993) і №150 (квітень 1994, назва しろまるくろまる), похідне правило шахівниці, NP-повнота, 26 пазлів-літер.
- [WPC unofficial wiki: Yin Yang](https://wpcunofficial.miraheze.org/wiki/Yin_Yang) — правила, Minako Sakai, Outside Yin Yang, раунди WPC 2013–2019.
- [Demaine et al., CCCG 2021](https://erikdemaine.org/papers/YinYang_CCCG2021/paper.pdf) — стаття про складність і похідні правила.
- [puzz.link yinyang.js](https://puzz.link/js/pzpr-samples/yinyang.js) — правила, коди `ms2x2`, `mu2x2`, `msDivide`, `muDivide`, `ceNoNum`.
- [puzzles-mobile: Yin-Yang help](https://www.puzzles-mobile.com/build/partials/help-fbb989da7b.yin-yang.html) — довідка мобільної колекції.
- YouTube: пошуки «cracking the cryptic yin yang sudoku» і «yin yang logic puzzle how to solve».

## Непевне
- (?) Конкретних відео Cracking the Cryptic з Yin-Yang-судоку не бачив — WebSearch вичерпано; дано пошуковий URL; механіку накладки описано з памʼяті.
- (?) Автор Minako Sakai — WPC-вікі й результат пошуку; сторінка Demaine автора не називає, лише журнал Puzzler.
- (?) Дії мишею в puzz.link і мобільних плеєрах — тестів вводу нема; схема з інших зафарбовувань.
- (?) Чи підсвічують плеєри шахове 2×2 як помилку — Demaine пише, що в їхньому шрифті так; у puzz.link окремого коду нема.
- (?) Похідне правило периметра виведено з планарності; у джерелах лише згадка «boundary rules».
