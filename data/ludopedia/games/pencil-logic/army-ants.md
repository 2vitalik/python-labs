---
title: Army Ants (Ґунтай-арі, «Армія мурах»)
slug: army-ants
aka: [ぐんたいあり, Guntai-ari, Armyants, Ameisenarmee, Wanderameisen, Армія мурах]
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
year: null
platforms: [paper, web]
links:
  - {kind: play, url: "https://puzz.link/rules.html?armyants", best: true, note: "puzz.link: сторінка правил (рендериться JS) і вхід у плеєр/редактор"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/armyants.js", note: "puzz.link: правила EN/JA, дебют у Nikoli vol.158, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kaero.js", note: "pzprjs: код перевірок armyants (граф мурах, isCmp, межі)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти кодів помилок EN"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Armyants/index.htm", note: "Janko: правила DE/EN, назви, 30 пазлів 5×5…18×10, родичі Kaero і Hebi-Ichigo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Army+Ants+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [path-drawing, path-cut, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, keyboard-controls, in-game-editor, import-open-formats, level-bank, impassable-cells, undo-redo, +numbered-path, +no-adjacent-check, +zone-bound-move, +show-final-position, +relocate-to-pattern]
proposes: ["+cond:crosses_border", "+cond:crosses", "+cond:consecutive_adjacent", "+card:relocate-to-pattern", "+card:numbered-path", "+card:no-adjacent-check", "+card:zone-bound-move", "+card:show-final-position"]
author: opus
date: 2026-11-09
---

# Army Ants — перенеси числа лініями в межах регіону, щоб склались «мурахи» 1…N, які не торкаються одна одної

## Суть
На полі з жирними межами регіонів розкидані числа. Частину з них треба перенести лініями руху (ортогонально, з поворотами, не перетинаючи жирних меж), щоб на кінцевих позиціях числа склались у «мурах» — ланцюжки 1, 2, …, N, де кожне наступне число ортогонально сусідить із попереднім. Дві різні мурахи не можуть торкатися стороною; мураха з одного «1» — легальна. Незвичне: регіони обмежують лише рух, а самі мурахи можуть лежати через межі.

## Поле і час
- Прямокутна сітка з жирними межами регіонів; банк Janko — від 5×5 до 18×10 і довільні форми ≈50/100/150 клітинок.
- Шари: регіони (незмінні) · числа на старті · лінії руху гравця · похідне: числа на кінцевих позиціях → мурахи.
- Лінія руху — шлях через центри клітинок від стартової клітинки числа до кінцевої; повороти дозволені.
- Час статичний; хід = провести або стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Число | object | 1…N | лишається на місці або переноситься лінією в межах свого регіону |
| «?» (puzz.link) | object | — | підходить на будь-який крок ланцюжка (?) |
| Мураха | zone | розмір = кількість чисел | ортогонально звʼязана група кінцевих позицій; містить рівно 1…N і шлях 1→2→…→N через сусідів |
| Лінія руху | mark | — | від числа до кінцевої клітинки; не гілкується, не перетинається, не проходить крізь числа |
| Регіон | zone | жирні межі | лінія не перетинає межу; мураха — може |
| Жирна межа | static | — | непрохідна для лінії руху |
| Хрестик на ребрі | mark | — | позначка гравця «тут лінії нема» |
| Тло клітинки | mark | 2 кольори | допоміжна заливка гравця (світло-синя / світло-жовта) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, number → cell)` → ЯКЩО `free(cell)` → ТО `mark(path, line)`; `custom: «число переноситься в кінець лінії»`.
- КОЛИ `input(drag, line)` → ЯКЩО `custom: «ребро — жирна межа»` (`+cond:crosses_border`) → ТО `block` (puzz.link `isLineNG`; у перевірці — `laOnBorder`).
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)`; на лінії — `unmark(segment)`.
- КОЛИ `input(click, cell)` → ТО `paint(cell, light_blue|light_yellow)` — допоміжне тло, на перевірку не впливає.
- КОЛИ `custom: «лінія розгалужується»` → ТО `constraint_broken(branch)` (`lnBranch`).
- КОЛИ `custom: «дві лінії в одній клітинці»` (`+cond:crosses`) → ТО `constraint_broken(cross)` (`lnCross`).
- КОЛИ `custom: «одна лінія зʼєднує два числа»` → ТО `constraint_broken(connected)` (`nmConnected`).
- КОЛИ `custom: «лінія проходить клітинку»` → ЯКЩО `occupied(cell, number)` → ТО `constraint_broken(over_number)` (`laOnNum`; чужий старт і фініш теж).
- КОЛИ `custom: «лінія не починається з числа»` → ТО `constraint_broken(isolated_line)` (`laIsolate`).
- КОЛИ `adjacent(number_a, number_b)` → ЯКЩО `custom: «|a − b| = 1 або одне з них "?"»` → ТО `custom: «вони в одній мурасі»` — так pzprjs будує граф мурах на кінцевих позиціях.
- КОЛИ `custom: «перевірка мурахи»` → ЯКЩО `not unique(ant)` → ТО `constraint_broken(dup)` (`bkDupNum`).
- КОЛИ `custom: «перевірка мурахи»` → ЯКЩО `region_size(ant, < k)` для якогось числа k у ній → ТО `constraint_broken(num_gt_size)` (`ceNumGtSize`: самотня «3» — помилка).
- КОЛИ `custom: «перевірка мурахи»` → ЯКЩО `not no_adjacent(ants)` → ТО `constraint_broken(ants_touch)` (`bsAnt`); з графа вище: сусіди з різницею ≠ 1 — це дві мурахи, що торкаються.
- КОЛИ `custom: «перевірка мурахи»` → ЯКЩО `not custom: «від 1 є шлях 2, 3, … через ортогональних сусідів, що покриває всю мураху»` (`+cond:consecutive_adjacent`) → ТО `constraint_broken(wrong_num)` (`bkWrongNum`).
- Мураха з одного числа легальна, якщо це «1» (або «?»).
- КОЛИ `custom: «на полі нема чисел»` → ТО `constraint_broken(no_numbers)` (`brNoValidNum`, для редактора).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: усі числа на кінцевих позиціях складаються в мурахи 1…N, мурахи не торкаються, лінії чисті. · Поразки й рахунку нема.

## Керування і ввід
- Папір (Nikoli): стрілка від числа до нової клітинки — може згинатися, не перетинає жирних меж, інших стрілок і чисел (puzz.link JA).
- puzz.link play: drag лівою від числа — лінія руху; права кнопка (drag) — хрестики на ребрах; клік по клітинці — циклічне тло (ліва 0→1→2, права у зворотний бік).
- puzz.link edit: drag — жирні межі; клік / цифри з клавіатури — числа (до розміру поля, максимум 999); є «?» (значення −2).
- Опція `dispmove`: малювати рамку числа на кінцевій позиції замість стартової — гравець бачить готових мурах.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з жирними межами, числа, лінії руху, хрестики, тло; `check-button`, `undo-button`, `redo-button` (?); `conflict-highlight` клітинок з помилкою після перевірки.
- `editor-window` (puzz.link edit mode): розмір поля, межі, числа; експорт у URL.
- `settings-window` (puzz.link): перемикач `dispmove` (?) — де саме в меню, не перевірено.
- `help-window`: сторінка правил puzz.link / Janko.
- `puzzle-select` (Janko): 30 пазлів за розміром і складністю (Easy, рівні 1–5).
- Переходи: rules → URL пазла → game-screen → Check → повідомлення з першим кодом помилки або «розвʼязано».

## Фічі поза полем
- `auto-check` за кнопкою: перший знайдений код помилки зі списку (puzz.link).
- `undo` / `redo` (pzpr) (?).
- `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` (Janko: 30 пазлів; ті, що мають покроковий логічний розвʼязок, підсвічені).
- Відображення `dispmove` — рендер кінцевих позицій.

## Варіації й родичі
- Janko: **Kaero** — те саме перенесення лініями, але літер у блоки; у pzprjs обидва (і Oyakodori) в одному файлі `kaero.js`.
- [hebi-ichigo](hebi-ichigo.md) — «змійки» 1…5, що не торкаються, але без руху; [hidato](hidato.md) — ланцюжок 1…N через сусідів на всьому полі.
- [satogaeri](satogaeri.md) — рух лише по прямій на N клітинок, ціль «по одному в країні»; [herugolf](herugolf.md) — удари коротшають, ціль — лунка.
- [oyakodori](oyakodori.md) — рух у гнізда, правило руху залежить від виду птаха.
- **Осі варіацій**: форма лінії (пряма / з поворотами) · довжина (рівно N / будь-яка) · обмеження руху (у регіоні / через межу) · ціль кінцевих позицій (по одному в регіоні / ланцюжки / пари в гніздах / лунки) · чи може обʼєкт лишитись.

## Цікавинки для курсу
- Граф мурах: компоненти на кінцевих позиціях з ребром «різниця = 1» (BFS) + перевірка «сусіди з різних компонент» — 📎: одна функція дає і групи, і порушення.
- Перевірка ланцюжка 1→N у мурасі (цифри унікальні, тож досить «k і k+1 сусіди») — 🌱.
- Валідація ліній: без гілок і перетинів, не крізь числа, не через жирні межі — 📎.
- Рендер «число на кінці лінії, тінь на старті» (`dispmove`) — 🌱.
- Розвʼязувач: кожне число має багато кінцевих клітинок у регіоні, лінії з поворотами не можуть перетинатися — 🥇 (пошук з відсіканням або SAT).
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing`, `path-cut` ↔ лінії руху · `satisfy-constraints`, `markup-validity`, `conflict-highlight`, `completion-detection` ↔ перевірка puzz.link · `cell-click`, `keyboard-controls` ↔ тло й редактор · `in-game-editor`, `import-open-formats` ↔ URL · `level-bank` ↔ Janko · `impassable-cells` ↔ жирні межі для лінії · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+relocate-to-pattern` «Перенести обʼєкти лініями, щоб кінцеві позиції задовольнили обмеження» · game-logic/constraints · 📎 · слот {ціль: по одному в регіоні | ланцюжки 1…N | пари в гніздах | лунки}.
  - `+numbered-path` (повтор із Hidato), `+no-adjacent-check` (повтор із Hebi-Ichigo), `+zone-bound-move` (повтор із шахових: обʼєкт не покидає свою зону), `+show-final-position` (повтор із Herugolf).

## Пропозиції до словників
- `+cond:crosses_border(line)` — лінія руху проходить через жирну межу регіону (Army Ants — заборона; Oyakodori — заборона або обовʼязок за видом).
- `+cond:crosses` — дві лінії перетинаються / накладаються (повтор із корпусу).
- `+cond:consecutive_adjacent(k, k+1, n4)` — клітинки з послідовними числами сусідні (повтор із Hidato).
- `+card:relocate-to-pattern`, `+card:numbered-path`, `+card:no-adjacent-check`, `+card:zone-bound-move`, `+card:show-final-position` — див. мапу.

## Джерела
- ⭐ [puzz.link: Army Ants](https://puzz.link/rules.html?armyants) — сторінка правил і плеєр (текст рендериться JS, тому дані брав із samples).
- [puzz.link armyants.js](https://puzz.link/js/pzpr-samples/armyants.js) — правила EN («move some of the numbers… chains that start at 1… different chains cannot be orthogonally adjacent») і JA («мураха може бути з одного 1», «стрілки не перетинають жирних меж, інших стрілок і чисел»), дебют Nikoli vol.158, коди `lnBranch lnCross nmConnected laOnNum laOnBorder bkDupNum ceNumGtSize bsAnt bkWrongNum laIsolate brNoValidNum`.
- [pzprjs kaero.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kaero.js) — порядок перевірок `@armyants`, граф мурах (ребро при |a−b| = 1 або «?»), `isCmp` (обхід від 1), `isLineNG` на межах, `dispmove`, кольори тла.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — «A number is greater than the size of the ant», «Two ants are adjacent», «The numbers on the ant are wrong».
- [Janko: Armyants](https://www.janko.at/Raetsel/Armyants/index.htm) — правила DE/EN («змійки зростаючих чисел можуть перетинати межі регіонів»), назви, 30 пазлів, родичі Kaero і Hebi-Ichigo.
- YouTube: пошук «Army Ants puzzle nikoli».

## Непевне
- (?) Рік: puzz.link і Janko кажуть лише «Puzzle Communication Nikoli vol.158» без дати; автор не названий.
- (?) «?»-число (−2, wildcard) є в коді pzprjs; чи буває воно в оригінальних пазлах Nikoli/Janko — не бачив.
- (?) Чи може мураха згинатися довільно (напр., 1-2 / 4-3 у квадраті 2×2) — висновок з коду `isCmp` (обхід від 1 мусить покрити всю групу), у правилах словами не сказано.
- (?) Undo/redo, меню з `dispmove` і повідомлення «розвʼязано» — загальна поведінка pzpr, не перевірена саме для Army Ants.
- (?) Janko: «перенести *деякі* числа в межах регіону» — чи кожне число зобовʼязане рухатись, ніде не сказано; код не вимагає руху.
