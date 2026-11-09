---
title: Nagareru-Loop
slug: nagareru-loop
aka: [流れるループ, Nagareru, Nagare, Flowing Loop, «Течійна петля»]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/nagareru/", best: true, note: "Nikoli: правила вітру й стрілок, Sample → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nagare.js", note: "puzz.link: правила EN/JA, «Nikoli vol. 147», коди помилок, тести миші/клавіатури"}
  - {kind: other, url: "https://puzz.link/rules.html?nagare", note: "puzz.link: сторінка правил і плеєр (рендериться JS)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nagareru/index.htm", note: "Janko: правила, назва «流れるループ», кілька пазлів"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти lrAgainstWind/lrAcrossWind/lrAcrossArrow/lrAgainstArrow .nagare"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nagareru+loop+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, single-loop-check, path-drawing, path-cut, edge-marking, impassable-cells, one-way-cell, cell-click, keyboard-controls, undo-redo, in-game-editor, import-open-formats, +directed-loop, +must-visit-checkpoints, +wind-ray, +forced-drift]
proposes: ["+cond:moving_against(wind)", "+cond:wind(cell, dir)", "+cond:turns", "+card:directed-loop", "+card:wind-ray", "+card:forced-drift"]
author: opus
date: 2026-11-09
---

# Nagareru-Loop — спрямована петля, яку вітер від вентиляторів у чорних клітинках не пускає проти себе й зносить убік

## Суть
Гравець малює одну замкнену спрямовану петлю по білих клітинках. Білі клітинки з чорними стрілками — обовʼязкові: петля проходить їх прямо в напрямку стрілки, і всі стрілки задають один напрям обходу. Чорні клітинки з білими стрілками — «вентилятори»: від них дме вітер у напрямку стрілки до наступної чорної клітинки чи краю. У смузі вітру петля не може йти проти вітру, а ввійшовши збоку, мусить повернути за вітром і пройти хоча б одну клітинку. Незвичне: «фізика» (вітер, знесення) кодується як статичне обмеження на напрямки ребер.

## Поле і час
- Прямокутна сітка; клітинки — білі (прохідні), чорні (непрохідні, можуть мати стрілку-вентилятор), білі зі стрілкою (обовʼязкові).
- Вітер — похідний шар: від кожного вентилятора промінь клітинок у напрямку стрілки до першої чорної або краю.
- Петля спрямована: кожен сегмент має напрям; обхід один для всієї петлі.
- Не мусить відвідати всі білі клітинки.
- Час статичний; хід = провести/стерти сегмент (напрям виводиться зі стрілок) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чорна клітинка | static | — | непрохідна; зупиняє промінь вітру |
| Вентилятор | static | напрям | чорна клітинка з білою стрілкою; дме вітром до наступної чорної / краю |
| Стрілка в білій | static | напрям | петля обовʼязково проходить її прямо в напрямку стрілки |
| Клітинка з вітром | terrain | напрям вітру | заборонено йти проти вітру; увійшов збоку — повертай за вітром |
| Клітинка з двома зустрічними вітрами | static | — | петля не може в неї ввійти (EN puzz.link) |
| Сегмент петлі | mark | ребро, напрям | частина єдиної спрямованої петлі |
| Петля | zone | напрям обходу | одна, без розгалужень і перетинів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells…)` → ТО `custom: «намалювати сегменти вздовж шляху»`; права кнопка — хрестик / стирання (?).
- КОЛИ `enter(loop, black)` → ТО `constraint_broken(on_shade)` (`lnOnShade`).
- КОЛИ `custom: «лінії перетинаються / розгалужуються / обриваються»` → ТО `constraint_broken(line)` (`lnCross`, `lnBranch`, `lnDeadEnd`).
- КОЛИ `custom: «стрілку в білій не пройдено»` → ТО `constraint_broken(arrow_unvisited)` (`arNoLine`).
- КОЛИ `custom: «петля на стрілці»` → ЯКЩО `turns(cell)` → ТО `constraint_broken(across_arrow)` (`lrAcrossArrow`).
- КОЛИ `custom: «петля на стрілці»` → ЯКЩО `custom: «напрям обходу протилежний стрілці»` → ТО `constraint_broken(against_arrow)` (`lrAgainstArrow`); дві стрілки з різним напрямом обходу — та сама помилка.
- КОЛИ `custom: «сегмент у клітинці з вітром»` → ЯКЩО `custom: «рух проти вітру»` → ТО `constraint_broken(against_wind)` (`lrAgainstWind`; `+cond:moving_against`).
- КОЛИ `custom: «петля входить у клітинку вітру збоку»` → ЯКЩО `custom: «не повертає за вітром»` → ТО `constraint_broken(across_wind)` (`lrAcrossWind`).
- КОЛИ `custom: «знесення за вітром»` → ЯКЩО `custom: «наступна клітинка за вітром — чорна або край»` → ТО `block`: збоку в таку клітинку не ввійти (JA, правило 5).
- КОЛИ `custom: «стрілка в білій стоїть у смузі вітру»` → ЯКЩО `custom: «стрілка проти вітру»` → ТО `constraint_broken(arrow_against_wind)` (`arAgainstWind`; перевірка коректності пазла).
- КОЛИ `custom: «кілька петель»` → ЯКЩО `not single_loop` → ТО `constraint_broken(many_loops)`; КОЛИ `custom: «ліній нема»` → ТО `constraint_broken(empty)` (`brNoLine`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: одна спрямована петля через усі стрілки в білих, без руху проти вітру й поперек нього. Поразки й рахунку нема.
- Рух за вітром і вздовж нього дозволено; вітер діє лише в клітинках променя, не за чорною.

## Керування і ввід
- puzz.link (play): drag лівою — лінія по клітинках (тест `mouse,left, 1,3, 5,3, 5,5, 3,5, 3,1` малює петлю); права кнопка — інший стан клітинки/ребра (тест `mouse,right`) (?).
- puzz.link (edit): стрілки ставляться клавіатурою зі Shift+стрілка, `q`/`w` перемикають тип клітинки (біла / чорна) (?), числа `1`, `0`.
- Папір: петля зі стрілками-напрямками.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, чорні вентилятори з білими стрілками, білі клітинки з чорними стрілками, лінія; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` після перевірки (?).
- `editor-window` (puzz.link edit mode): `newboard`, тип клітинок, стрілки; експорт URL.
- `settings-window` (puzz.link): параметр `cursor` (показ курсора клавіатури) — видно з тесту `setconfig,cursor,false`.
- `help-window` — правила Nikoli / puzz.link / Janko.

## Фічі поза полем
- `auto-check` (puzz.link); `undo`/`redo`; `level-editor` + `share-code`.
- `puzzle-bank` — Janko (кілька пазлів), Nikoli — журнал і збірки.

## Варіації й родичі
- [icebarn](icebarn.md) — спрямована лінія через стрілки й «лід, де не повертаєш»; тут замість льоду — вітер, що повертає примусово.
- [suraromu](suraromu.md) — петля з напрямком, заданим порядком воріт; [masyu](masyu.md), [yajilin](yajilin.md) — петлі з локальними підказками.
- Цифрові родичі «примусового руху»: конвеєри й вітер у `push-slide`/`maze-arcade` — там симулюється, тут лише перевіряється.
- **Осі варіацій**: джерело напрямку (стрілки / порядок / вітер) · вплив поля (заборона проти / примусовий поворот / прямо) · хто задає силу (промінь до стіни / радіус) · спрямованість (петля / шлях IN→OUT).

## Цікавинки для курсу
- Промені вітру: від кожного вентилятора йти до стіни й записати напрям у клітинки; зустрічні вітри → клітинка заборонена — 🌱.
- Перевірка спрямованої петлі: обхід з напрямом, порівняння з кожною стрілкою, один напрям для всіх — 📎.
- Правило знесення: вхід збоку → обовʼязковий поворот за вітром + перевірка, що попереду не стіна — 📎.
- Розвʼязувач: локальні заборони ребер від вітру + одна спрямована петля — 🥇; генератор — 👑.
- Візуалізація вітру як шару підсвітки клітинок — 🌱 (`logic-render-split`).

## Мапа на каталог
- Є: `single-loop-check` · `path-drawing`, `path-cut`, `edge-marking` · `impassable-cells` ↔ чорні · `one-way-cell` ↔ стрілки й вітер (прохід лише в напрямку) · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `in-game-editor`, `import-open-formats` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+must-visit-checkpoints` — уже пропоновано (Icebarn).
  - `+directed-loop` «Спрямована петля: один напрям обходу, узгоджений з усіма стрілками» · game-logic/constraints · 📎.
  - `+wind-ray` «Промінь впливу від джерела до перешкоди (вітер, світло)» · entities/state · 🌱 · слот {dir, stop: black|edge}.
  - `+forced-drift` «Вхід збоку в потік → обовʼязковий поворот за потоком» · entities/legality · 📎.

## Пропозиції до словників
- `+cond:wind(cell, dir)` — у клітинці дме вітер у напрямку (похідний шар від вентиляторів).
- `+cond:moving_against(dir)` — сегмент іде проти заданого напрямку (`moving` + протилежний).
- `+cond:turns` — петля повертає в клітинці (повтор з Masyu/Icebarn).
- `+card:directed-loop`, `+card:wind-ray`, `+card:forced-drift` — див. мапу.

## Джерела
- ⭐ [Nikoli: Nagareru-Loop](https://www.nikoli.co.jp/en/puzzles/nagareru/) — правила: петля з одним напрямом, обовʼязкові стрілки, вітер від чорних зі стрілками, знесення щонайменше на клітинку.
- [puzz.link nagare.js](https://puzz.link/js/pzpr-samples/nagare.js) — EN (6 правил, зокрема зустрічні вентилятори) і JA (5 правил), «Nikoli vol. 147», 11 кодів помилок, тести миші/клавіатури.
- [puzz.link: Nagare](https://puzz.link/rules.html?nagare) — правила й плеєр (рендериться JS).
- [Janko: Nagareru](https://www.janko.at/Raetsel/Nagareru/index.htm) — правила, назва 流れるループ, автор невідомий.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти `.nagare`.
- YouTube: пошук «nagareru loop puzzle».

## Непевне
- (?) EN puzz.link: «увійшла у вітер — одразу повертає»; JA і Nikoli: «знесе щонайменше на 1 клітинку» — суть та сама, формулювання різні.
- (?) Правило «два зустрічні вентилятори → клітинка закрита» є лише в EN puzz.link; у JA/Nikoli — як наслідок інших правил (?).
- (?) Чи гравець задає напрям сегментів сам, чи pzpr виводить його зі стрілок — не перевірив; значення клавіш `q`/`w` — з тестів, без опису.
- (?) Рік: «Nikoli vol. 147», дату не перевіряв. Картинки Nikoli не бачив.
