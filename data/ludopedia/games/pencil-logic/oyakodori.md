---
title: Oyakodori (Оякодорі, «Батьки й пташенята»)
slug: oyakodori
aka: [おやこどり, Оякодорі, Parents and Children, Батьки й пташенята]
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
  - {kind: play, url: "https://puzz.link/rules.html?oyakodori", best: true, note: "puzz.link: сторінка правил (рендериться JS) і вхід у плеєр/редактор"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/oyakodori.js", note: "puzz.link: правила EN/JA, автор Subaru Saito, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kaero.js", note: "pzprjs: код перевірок oyakodori (гнізда, перетин меж, кольори)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти кодів помилок EN"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Oyakodori/index.htm", note: "Janko: 6 правил DE/EN, значення назви, 5 пазлів 6×6…10×10"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Oyakodori+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [path-drawing, path-cut, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, all-on-targets, cell-click, keyboard-controls, in-game-editor, import-open-formats, level-bank, impassable-cells, undo-redo, +relocate-to-pattern, +kind-specific-move-rule, +zone-bound-move, +show-final-position]
proposes: ["+cond:crosses_border", "+cond:crosses", "+cond:region_has", "+card:kind-specific-move-rule", "+card:relocate-to-pattern", "+card:zone-bound-move", "+card:show-final-position"]
author: opus
date: 2026-11-09
---

# Oyakodori — посади в кожне гніздо батька й пташеня: пташеня не перелітає меж регіону, батько мусить перелетіти хоч одну

## Суть
На полі з жирними межами регіонів є білі кружки (батьки, великі птахи), чорні кружки (пташенята, малі птахи) і гнізда — сірі доміно з двох сусідніх клітинок. Кожного птаха треба провести лінією польоту в гніздо так, щоб у гнізді опинились один білий і один чорний. Лінії не перетинаються й не проходять крізь птахів і гнізда. Родзинка — правило руху залежить від виду: чорний не перетинає жодної жирної межі, білий зобовʼязаний перетнути хоча б одну.

## Поле і час
- Прямокутна сітка, розбита жирними межами на регіони; гнізда — пари сірих клітинок; банк Janko — 6×6, 8×8, 10×10, тест puzz.link — 4×4.
- Шари: регіони (незмінні) · гнізда (сірі клітинки) · птахи на старті · лінії польоту гравця · похідне: птахи на кінцевих позиціях.
- Лінія польоту — шлях через центри клітинок від птаха до клітинки гнізда; повороти дозволені.
- Час статичний; хід = провести або стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Батько (великий птах) ○ | object | білий кружок | летить лінією в гніздо; на шляху мусить перетнути ≥1 жирну межу |
| Пташеня (малий птах) ● | object | чорний кружок | летить лінією в гніздо; не перетинає жодної жирної межі — лишається у своєму регіоні |
| Гніздо | zone | 2 сірі сусідні клітинки | приймає рівно одного білого й одного чорного; лінія може лише закінчитись у ньому |
| Регіон | zone | жирні межі | межа руху для пташенят, обовʼязкова до перетину для батьків |
| Лінія польоту | mark | — | від птаха до клітинки гнізда; не гілкується, не перетинається, не проходить крізь птахів |
| Жирна межа | static | — | лінія через неї проходить, але це рахується як «перетин» |
| Хрестик на ребрі | mark | — | позначка гравця «тут лінії нема» |
| Тло клітинки | mark | 2 кольори | допоміжна заливка гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, bird → nest_cell)` → ТО `mark(path, line)`; `custom: «птах переноситься в кінець лінії»`.
- КОЛИ `input(drag, line)` → ЯКЩО `custom: «птах чорний»` and `custom: «ребро — жирна межа»` (`+cond:crosses_border`) → ТО `block` — лише з опцією `dispmove`; без неї помилку ловить перевірка.
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)`; на лінії (без `dispmove`) — `unmark(segment)`.
- КОЛИ `input(click, cell)` → ТО `paint(cell, color_1|color_2)` — допоміжне тло.
- КОЛИ `custom: «лінія розгалужується»` → ТО `constraint_broken(branch)` (`lnBranch`).
- КОЛИ `custom: «дві лінії в одній клітинці»` (`+cond:crosses`) → ТО `constraint_broken(cross)` (`lnCross`).
- КОЛИ `custom: «одна лінія зʼєднує двох птахів»` → ТО `constraint_broken(connected)` (`nmConnected`).
- КОЛИ `custom: «лінія проходить клітинку»` → ЯКЩО `occupied(cell, bird)` → ТО `constraint_broken(over_bird)` (`laOnNum`).
- КОЛИ `custom: «лінія проходить крізь клітинку гнізда, а не закінчується в ній»` → ТО `constraint_broken(through_nest)` (`laOnIce`).
- КОЛИ `custom: «перевірка гнізда»` → ЯКЩО `custom: «у гнізді > 2 птахів»` (`+cond:region_has`) → ТО `constraint_broken(gt2)` (`nmGt2`).
- КОЛИ `custom: «лінія чорного птаха»` → ЯКЩО `custom: «перетинає жирну межу»` (`+cond:crosses_border`) → ТО `constraint_broken(black_crosses)` (`laShadeOnBorder`).
- КОЛИ `custom: «лінія білого птаха закінчилась у гнізді»` → ЯКЩО `not custom: «перетнула ≥1 жирну межу»` (`+cond:crosses_border`) → ТО `constraint_broken(white_no_cross)` (`laUnshadeNoBorder`).
- КОЛИ `custom: «перевірка гнізда»` → ЯКЩО `custom: «у гнізді рівно один птах»` (`+cond:region_has`) → ТО `constraint_broken(lonely)` (`nmLt2`).
- КОЛИ `custom: «у гнізді два птахи»` → ЯКЩО `same(bird_a, bird_b, color)` → ТО `constraint_broken(same_kind)` (`nmNumberEq`).
- КОЛИ `custom: «лінія птаха закінчилась»` → ЯКЩО `not cell(end, nest)` → ТО `constraint_broken(out_of_nest)` (`nmOutOfBk`).
- КОЛИ `custom: «лінія не починається з птаха»` → ТО `constraint_broken(isolated_line)` (`laIsolate`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: кожен птах у гнізді, у кожному зайнятому гнізді — білий і чорний, правила перетину меж виконано. · Поразки й рахунку нема.

## Керування і ввід
- Папір: лінія від кружка до клітинки гнізда по вертикалях і горизонталях через центри клітинок (puzz.link JA).
- puzz.link play: drag лівою від птаха — лінія польоту; права кнопка (drag) — хрестики на ребрах; клік — циклічне тло; палітра режимів `line` / `peke` / `clear`.
- puzz.link edit: drag лівою — жирні межі; права кнопка (drag) — сірі клітинки гнізд; клік або клавіші `1` (білий) / `2` (чорний) — птах; `q` — перемкнути гніздо в клітинці; «?» вимкнено; палітра `border` / `circle-shade` / `circle-unshade` / `shade` / `clear`.
- Опція `dispmove`: рендер птахів у кінцевих позиціях і заборона чорному перетинати межу ще під час малювання.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з жирними межами, сірі гнізда, білі й чорні кружки, лінії польоту; `mode-toggle` (line/peke/clear), `check-button`, `undo-button`, `redo-button` (?); `conflict-highlight` після перевірки.
- `editor-window` (puzz.link edit mode): розмір, межі, гнізда, птахи; `tool-palette` режимів; експорт у URL.
- `settings-window` (puzz.link): перемикач `dispmove` (?).
- `help-window`: сторінка правил puzz.link / Janko.
- `puzzle-select` (Janko): 5 пазлів із розвʼязками.
- Переходи: rules → URL пазла → game-screen → Check → перший код помилки або «розвʼязано».

## Фічі поза полем
- `auto-check` за кнопкою: перший знайдений код помилки (puzz.link).
- `undo` / `redo` (pzpr) (?).
- `level-editor` + `share-code` — пазл як URL puzz.link.
- `puzzle-bank` (Janko: 5 пазлів).
- Відображення `dispmove` — кінцеві позиції й раннє блокування ліній.

## Варіації й родичі
- [army-ants](army-ants.md) — той самий рух лініями, межі регіонів заборонені для всіх, ціль — ланцюжки 1…N; у pzprjs обидва (і Kaero) в одному `kaero.js`.
- [satogaeri](satogaeri.md) — рух по прямій на N, по одному в країні; [herugolf](herugolf.md) — удари в лунку; Yosenabe (Janko) — перенести числа в «каструлі» з сумою.
- [dosun-fuwari](dosun-fuwari.md), [moon-or-sun](moon-or-sun.md) — інші пазли, де білі й чорні кружки підкоряються різним правилам.
- **Осі варіацій**: правило руху (однакове для всіх / за видом обʼєкта) · межа (заборонена / обовʼязкова / байдужа) · ємність цілі (1 / пара / сума) · склад пари (будь-які / різного виду) · чи можна лишити ціль порожньою.

## Цікавинки для курсу
- Правило руху за видом: порахувати жирні межі на шляху (перетин списку ребер лінії з множиною меж) — 🌱; та сама функція дає і заборону, і обовʼязок.
- Перевірка гнізд: згрупувати кінцеві позиції по гніздах, ≤2, різні кольори, не самотній — 🌱.
- Валідація ліній: без гілок, перетинів, не крізь птахів і гнізда — 📎.
- Раннє блокування ходу (`dispmove`) проти пізньої перевірки — 📎: дві стратегії валідації в одному інтерфейсі.
- Розвʼязувач: розподіл птахів по гніздах (парування) + неперетинні лінії з умовами меж — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing`, `path-cut` ↔ лінії польоту · `satisfy-constraints`, `markup-validity`, `conflict-highlight`, `completion-detection` ↔ перевірка puzz.link · `all-on-targets` ↔ усі птахи в гніздах · `cell-click`, `keyboard-controls` ↔ редактор · `in-game-editor`, `import-open-formats` ↔ URL · `level-bank` ↔ Janko · `impassable-cells` ↔ гнізда для прольоту · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+kind-specific-move-rule` «Правило руху залежить від виду обʼєкта: один не може перетнути межу, інший мусить» · entities/legality · 🌱 · слот {межа: заборонена | обовʼязкова ≥ n}.
  - `+relocate-to-pattern` (повтор із Army Ants; слот «пари в гніздах»), `+zone-bound-move` (повтор: пташеня не покидає регіон), `+show-final-position` (повтор із Herugolf).

## Пропозиції до словників
- `+cond:crosses_border(line, op, n)` — лінія руху перетинає жирну межу N разів (повтор із Army Ants; тут і `= 0`, і `≥ 1`).
- `+cond:crosses` — дві лінії перетинаються / накладаються (повтор із корпусу).
- `+cond:region_has(nest, kind, op, n)` — у зоні N обʼєктів виду (повтор із корпусу).
- `+card:kind-specific-move-rule`, `+card:relocate-to-pattern`, `+card:zone-bound-move`, `+card:show-final-position` — див. мапу.

## Джерела
- ⭐ [puzz.link: Oyakodori](https://puzz.link/rules.html?oyakodori) — сторінка правил і плеєр (текст рендериться JS, дані брав із samples).
- [puzz.link oyakodori.js](https://puzz.link/js/pzpr-samples/oyakodori.js) — правила EN (5 пунктів: «Every used nest must receive one small bird and one large bird», «Black (small) birds cannot fly over borders», «White (large) birds must fly over at least one border») і JA (○ батьки, ● пташенята), автор 齋藤スバル (Subaru Saito), коди `lnBranch lnCross nmConnected laOnNum laOnIce nmGt2 laShadeOnBorder laUnshadeNoBorder nmLt2 nmNumberEq nmOutOfBk laIsolate`.
- [pzprjs kaero.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/kaero.js) — `@oyakodori`: гніздо = звʼязні сірі клітинки без жирної межі між ними; 1 = білий, 2 = чорний; `checkBlackIntersect` / `checkWhiteNoIntersect` по ребрах шляху; prehook `dispmove`; клавіші `1`, `2`, `q`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — «A black bird goes over a border», «A white bird does not go over a border», «There is a lonely bird», «Two identical birds are in the same nest».
- [Janko: Oyakodori](https://www.janko.at/Raetsel/Oyakodori/index.htm) — 6 правил, «oyakodori ≈ батьки й діти», автор і перша публікація невідомі, 5 пазлів 6×6…10×10.
- YouTube: пошук «Oyakodori puzzle».

## Непевне
- (?) Автор: puzz.link — Subaru Saito; Janko — «не знаємо, хто вигадав і де вперше надруковано». Рік ніде не названо.
- (?) Порожні гнізда: puzz.link EN — «every *used* nest», код їх не забороняє; Janko — «кожне сіре доміно отримує по білому й чорному» (тобто всі гнізда зайняті?).
- (?) У коді гніздо з одним птахом легальне, якщо гніздо — одна клітинка (`checkSingleCircle`); чи бувають однокліткові гнізда в пазлах — не бачив.
- (?) Чи може птах стояти без лінії (вже в гнізді на старті) — у правилах не сказано; у тестових пазлах усі птахи поза гніздами.
- (?) Undo/redo, меню з `dispmove` і повідомлення «розвʼязано» — загальна поведінка pzpr, не перевірена саме для Oyakodori.
