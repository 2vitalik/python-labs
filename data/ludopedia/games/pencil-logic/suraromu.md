---
title: Suraromu (Slalom)
slug: suraromu
aka: [スラローム, Slalom, Circumnavi Gates, Слалом]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/suraromu/", best: true, note: "Nikoli: 4 правила, Sample → Progressing → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/slalom.js", note: "puzz.link: правила EN/JA, «Nikoli vol. 116», коди помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?slalom", note: "puzz.link: сторінка правил і плеєр (рендериться JS)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Suraromu/index.htm", note: "Janko: правила, інші назви (Slalom, Circumnavi Gates), банк 210 пазлів"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти gateRedup/gateUnpass/lrOrder/stLineNe2 .slalom"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=suraromu+slalom+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, single-loop-check, path-drawing, path-cut, edge-marking, impassable-cells, cell-click, keyboard-controls, undo-redo, in-game-editor, import-open-formats, level-bank, +ordered-checkpoints, +gate-crossing, +must-visit-checkpoints]
proposes: ["+trigger:cross(loop, gate)", "+cond:order(gate, k)", "+cond:turns", "+role:gate-line", "+card:ordered-checkpoints", "+card:gate-crossing"]
author: opus
date: 2026-11-09
---

# Suraromu — петля зі старту в колі проходить усі ворота між чорними клітинками, номеровані — у своєму порядку

## Суть
На сітці — чорні клітинки, пунктирні «ворота» між ними (або між чорною клітинкою й краєм поля) і біле коло з числом. Гравець малює одну замкнену петлю, що виходить із кола і повертається в нього, перетинаючи кожні ворота рівно раз. Число в колі — скільки воріт усього; число в чорній клітинці на кінці воріт — яким за ліком від кола їх треба перетнути. Незвичне: петля стає маршрутом із напрямком і розкладом — слалом на папері.

## Поле і час
- Прямокутна сітка; клітинки — білі (прохідні), чорні (непрохідні), коло-старт.
- Ворота — неперервний відрізок пунктиру з білих клітинок між двома чорними (або чорною й краєм) по горизонталі чи вертикалі; один відрізок = одні ворота.
- Петля — по ортогоналі через центри білих клітинок; не мусить відвідати всі клітинки.
- Напрямок обходу вибирає гравець: від кола в один бік порядок воріт має збігтися з номерами.
- Час статичний; хід = провести/стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біле коло | static | N — кількість воріт | старт і фініш петлі; у ньому рівно 2 сегменти |
| Чорна клітинка | static | номер k / «?» / порожньо | непрохідна; номер задає порядок воріт, на які вказує (стрілкою або сусідством, JA-правила) |
| Ворота | gate | клітинки відрізка, номер | петля перетинає їх рівно раз, перпендикулярно, без повороту на воротах; торкатись інакше не можна |
| Біла клітинка | terrain | — | прохідна, ≤1 відвідування |
| Сегмент петлі | mark | ребро | частина єдиної петлі |
| Петля | zone | напрям, порядок воріт | одна, замкнена, через коло |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells…)` → ТО `custom: «намалювати сегменти вздовж шляху»`; права кнопка — стерти / хрестик (?).
- КОЛИ `enter(loop, black)` → ТО `constraint_broken(on_shade)` (`lnOnShade`).
- КОЛИ `custom: «лінії перетинаються / розгалужуються / обриваються»` → ТО `constraint_broken(line)` (`lnCross`, `lnBranch`, `lnDeadEnd`).
- КОЛИ `custom: «кілька петель»` → ЯКЩО `not single_loop` → ТО `constraint_broken(many_loops)` (`lnPlLoop`).
- КОЛИ `custom: «у колі не 2 сегменти»` → ТО `constraint_broken(start)` (`stLineNe2`).
- КОЛИ `custom: «петля перетинає ворота вдруге»` → ТО `constraint_broken(gate_twice)` (`gateRedup`; `+trigger:cross`).
- КОЛИ `custom: «ворота не перетнуто»` → ТО `constraint_broken(gate_unpassed)` (`gateUnpass`).
- КОЛИ `custom: «петля йде вздовж воріт або повертає на них»` → ЯКЩО `turns(cell)` → ТО `constraint_broken(gate_touch)` (`+cond:turns`).
- КОЛИ `custom: «обхід від кола»` → ЯКЩО `custom: «k-ті перетнуті ворота мають номер ≠ k»` → ТО `constraint_broken(order)` (`lrOrder`; `+cond:order`); перевіряється хоча б один із двох напрямків (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: одна петля через коло, усі ворота рівно раз перпендикулярно, номеровані — у своєму порядку. Поразки й рахунку нема.
- Ворота без номера — у будь-якому місці порядку; «?» — номер невідомий (puzz.link).

## Керування і ввід
- puzz.link (play): drag по клітинках — лінія; права кнопка — хрестик / стирання (?).
- puzz.link (edit): чорні клітинки, ворота (горизонтальні/вертикальні), числа в чорних і в колі — з клавіатури (?).
- Папір (Nikoli): петля олівцем; номери воріт інколи записують на ворота під час розвʼязання.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, чорні клітинки з числами, пунктирні ворота, коло з числом, лінія; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` після перевірки (?).
- `editor-window` (puzz.link edit mode): розстановка чорних, воріт, кола; експорт URL.
- `help-window` — правила Nikoli / puzz.link / Janko.
- `puzzle-select` (Janko): 210 пазлів, від 10×10 до 45×31.

## Фічі поза полем
- `auto-check` (puzz.link); `undo`/`redo`; `level-editor` + `share-code`.
- `puzzle-bank` — Janko 210 пазлів; Nikoli — у журналі й збірках.

## Варіації й родичі
- Назви: Slalom (JA, Palmer Mebane), Circumnavi Gates (Grant Fikes); «Slalom» також — інший пазл (Gokigen Naname), не плутати (Janko).
- Петлі з обовʼязковими точками: [masyu](masyu.md), [country-road](country-road.md); з напрямком і чекпоінтами — [icebarn](icebarn.md) (IN→OUT, стрілки), [nagareru-loop](nagareru-loop.md).
- **Осі варіацій**: чекпоінти (ворота / клітинки / регіони) · порядок (повний / частковий / нема) · як перетинати (перпендикулярно / будь-як) · старт (коло / будь-де).

## Цікавинки для курсу
- Виявлення воріт: зі списку чорних клітинок знайти відрізки між ними — 🌱.
- Обхід петлі від кола в обидва боки, послідовність перетнутих воріт і порівняння з номерами — 📎.
- Перпендикулярний перетин і заборона повороту на воротах — 🌱.
- Розвʼязувач: петля + перестановка воріт з частковим порядком — 🥇; генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `single-loop-check` · `path-drawing`, `path-cut`, `edge-marking` · `impassable-cells` ↔ чорні клітинки · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `level-bank` ↔ Janko · `in-game-editor`, `import-open-formats` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+must-visit-checkpoints` — уже пропоновано (Icebarn).
  - `+ordered-checkpoints` «Чекпоінти в заданому порядку від старту» · game-logic/constraints · 📎 · слот {numbered: all|some}.
  - `+gate-crossing` «Ворота-відрізок: перетнути рівно раз перпендикулярно» · entities/legality · 🌱.

## Пропозиції до словників
- `+trigger:cross(loop, gate)` — лінія перетинає відрізок-ворота.
- `+cond:order(gate, k)` — у обході від старту ворота стоять k-ми.
- `+cond:turns` — петля повертає в клітинці (повтор з Masyu/Icebarn).
- `+role:gate-line` — ворота як відрізок клітинок, а не одна клітинка (`gate` — двері зі станом).
- `+card:ordered-checkpoints`, `+card:gate-crossing` — див. мапу.

## Джерела
- ⭐ [Nikoli: Suraromu](https://www.nikoli.co.jp/en/puzzles/suraromu/) — 4 правила: петля, ворота рівно раз, коло = старт і кількість воріт, номери в чорних = порядок.
- [puzz.link slalom.js](https://puzz.link/js/pzpr-samples/slalom.js) — EN/JA, перпендикулярний перетин, «?»-ворота, коди `lnOnShade lnCross lnBranch gateRedup stLineNe2 lrOrder lnDeadEnd lnPlLoop gateUnpass`.
- [puzz.link: Slalom](https://puzz.link/rules.html?slalom) — правила й плеєр (рендериться JS).
- [Janko: Suraromu](https://www.janko.at/Raetsel/Suraromu/index.htm) — правила, назви, 210 пазлів 10×10…45×31; автор і перша публікація невідомі.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти `.slalom`.
- YouTube: пошук «suraromu slalom puzzle».

## Непевне
- (?) Рік: puzz.link — «Puzzle Communication Nikoli vol. 116», дату тому не перевіряв; Janko — автор невідомий.
- (?) Як pzpr вибирає напрям обходу для `lrOrder` — з тексту «consistent direction» не ясно, чи перевіряє обидва.
- (?) Ввід і редактор — загальна поведінка pzpr, не перевірена саме для slalom; тестів миші в slalom.js нема.
- (?) Картинки Nikoli (Sample/Solution) не бачив — лише текст.
