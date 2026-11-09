---
title: Otomata
slug: otomata
aka: [Otomata DX (ремейк ANARKO), otomata-js]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: rhythm
  opponent: none
  info: full
  random: none
  goal: none
year: 2011
platforms: [web, iOS]
links:
  - {kind: official, url: "http://earslap.com/page/otomata.html", best: true, note: "сторінка автора (Batuhan Bozkurt): 4 стани клітини, рух щотакту, удар об стіну — нота за позицією, зіткнення — поворот за годинниковою, посилання на твір"}
  - {kind: play, url: "https://elanarko.itch.io/otomata-dx", note: "Otomata DX (HTML5): клік — нова клітина вгору, повторні кліки — вправо/вниз/вліво/стерти"}
  - {kind: other, url: "https://raw.githubusercontent.com/stelabouras/Otomata/master/script.js", note: "HTML5-порт (реверс-інжиніринг): сітка 9×9, порядок кроку, нота за стовпцем/рядком, правило зіткнення"}
  - {kind: other, url: "https://raw.githubusercontent.com/marwahaha/otomata/master/scales.txt", note: "JS-версія, сумісна з посиланнями Flash: 40 ладів по 9 нот"}
  - {kind: other, url: "https://github.com/archiloque/otomata-js", note: "ще один JS-порт (сітка 9, 57 ладів)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=otomata+generative+sequencer", note: "пошук; відео творів"}
stage: v1
coverage: 80
mechanics: [cell-click, hover-highlight, orientation-state, facing-icon, move-auto, turn-when-blocked, sound-effects, game-loop, game-pause, state-string, keyboard-controls, +cellular-automaton-rule, +grid-sequencer, +pitch-by-position, +collision-rotate, +click-cycle-direction, +scale-select, +step-run-speed]
proposes: ["+card:grid-sequencer", "+card:pitch-by-position", "+trigger:converge(cell)", "+ui:scale-picker"]
author: opus
date: 2026-11-09
---

# Otomata — генеративний секвенсор: клітини-стрілки їздять сіткою 9×9, удар об стіну грає ноту, зустріч — поворот

## Суть
Музична іграшка-автомат Батухана Бозкурта (earslap): гравець ставить на сітку клітини зі стрілкою (вгору/вправо/вниз/вліво) і натискає Play. Щотакту кожна клітина робить крок у свій бік; та, що вперлась у край, **розвертається й грає ноту**, висота якої залежить від місця удару, а клітини, що зійшлись в одній клітинці, **повертаються за годинниковою**. З кількох стрілок виростають осцилятори й довгі непередбачувані цикли — мелодія. Мети нема; результат — посилання на твір.

## Поле і час
- Квадратна сітка 9×9 (у портах `divisions = 9`); 9 нот ладу = 9 рядків/стовпців.
- Один шар: клітина порожня або має живу клітину з напрямком; кілька клітин можуть тимчасово стояти в одній клітинці (після зіткнення).
- Тік = такт: усі клітини рухаються одночасно (`time: rhythm`). Темп — регулятор у другій версії оригіналу (у порті stelabouras — фіксований, крок кожні 12 кадрів).
- Край поля — стіна-«струна»: не пропускає й не загортає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жива клітина | object | напрям: up / right / down / left | щотакту крок у свій напрям; біля стіни розвертається з нотою; у зіткненні повертається на 90° за год. |
| Стіна (край поля) | static | позиція удару | дає висоту ноти: верх/низ — за стовпцем, ліво/право — за рядком |
| Клітинка поля | terrain | — | підсвічується під курсором і в момент зіткнення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, empty_cell)` → ТО `spawn(cell_up, cell)`.
- КОЛИ `input(click, cell)` → ЯКЩО `facing(cell, left)` → ТО `disappear(cell)`; інакше `rotate(cell, 90)` (цикл up → right → down → left → порожньо).
- КОЛИ `tick` → ЯКЩО `facing(cell, out_of_field)` (клітина на краю й дивиться назовні) → ТО `bounce(cell)` (напрям на протилежний), `sound(note)`.
- Нота: вертикальний удар (верх/низ) — `custom: «нота = стовпець x»`; горизонтальний (ліво/право) — `custom: «нота = 8 − рядок y»`; ноти беруться з обраного ладу (9 щаблів).
- КОЛИ `tick` → ТО `move(cell, facing)` для всіх клітин одночасно (після відбиття — вже в новий бік).
- КОЛИ `custom: «дві й більше клітин цілять в одну клітинку в цьому такті»` → ТО `move` усіх туди, `rotate(each, 90)` за год. стрілкою (порт stelabouras: поворот після кроку).
- Зустрічні сусіди (A → B, B → A) у порті не вважаються зіткненням — міняються місцями «крізь» одна одну (?).
- Клітина, що заходить на місце клітини, яка саме йде геть, — не зіткнення.
- КОЛИ `input(play_pause)` → ТО `custom: «старт/пауза автомата»`.
- КОЛИ `input(clear)` → ТО `custom: «стерти всі клітини й зупинити»`.
- КОЛИ `custom: «змінилось поле»` → ТО `custom: «оновити посилання на твір (стан у URL)»`.
- Перемоги, поразки й рахунку нема (`goal: none`).

## Керування і ввід
- Миша: клік по порожній клітинці — нова клітина вгору; повторні кліки по клітині — поворот за годинниковою; клік по клітині «вліво» — стерти.
- Play/Pause; у порті stelabouras — Space (пуск/пауза), `c` (очистити), тач на iOS — той самий цикл кліків.
- Друга версія оригіналу: вибір ладу і темпу.

## Вікна, меню, HUD
- `game-screen`: сітка 9×9 з клітинами-стрілками, підсвітка клітинки під курсором (`hover-highlight`) і білим — місць зіткнень; рядки/стовпці, що прозвучали, підсвічуються.
- Контроли: Play/Pause, Clear, вибір ладу (`+ui:scale-picker`), регулятор темпу (`speed-slider`), поле «Copy Piece Link» з посиланням на твір.
- Інших вікон нема: усе на одному екрані.

## Фічі поза полем
- `share-code`: твір = посилання з параметром (`?q=…` в оригіналі; у порті — Base64-JSON клітин у `#cells=`); JS-версія marwahaha приймає посилання з Flash-версій.
- `speed-control` (темп) і вибір ладу; `sound-toggle` — (?).
- Немає рівнів, збереження поза посиланням, undo.

## Варіації й родичі
- Порти: iOS-версія автора; JS/HTML5-порти (stelabouras, archiloque, marwahaha); Otomata DX (ANARKO, Construct 3) — нота і при ударі об стіну, і при зіткненні частинок; Chimes, AutoMusex (гекс-сітка).
- Родичі в корпусі: [langtons-ant](langtons-ant.md) (агент на сітці з поворотами), [wireworld](wireworld.md), [cell-machine](cell-machine.md) (напрямлені клітини), [game-of-life](game-of-life.md), [elementary-cellular-automata](elementary-cellular-automata.md).
- Осі варіацій:
  - **що грає ноту**: удар об стіну (Otomata) / ще й зіткнення (DX) / проходження клітинки-«ноти»;
  - **висота**: за позицією удару / за типом клітини / за рядком (Tenori-on-подібні);
  - **зіткнення**: поворот за год. / зупинка / розворот / проходження;
  - **сітка**: 9×9 квадратна / гекс / більша з кількома інструментами.

## Цікавинки для курсу
- Синхронний крок з «проєктованими рухами»: зібрати цілі всіх клітин, згрупувати за клітинкою, потім застосувати — 📎.
- Відбиття від стіни + нота за позицією (стовпець/рядок) з ладу — 🌱.
- Зіткнення як поворот за годинниковою; пошук осциляторів і довжини циклу стану — 🥉 (детекція циклу хешуванням стану).
- Стан поля в URL (Base64-JSON) — поділитись твором — 🌱.
- Звук: 9 семплів або синтез частот за ладом, кілька нот в одному такті — 📎.
- Редактор кліками з циклом станів up → right → down → left → порожньо — 🌱.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` ↔ розстановка й підсвітка; `orientation-state` + `facing-icon` ↔ напрям клітини як стрілка; `move-auto` ↔ клітини самі їдуть, клік змінює напрям; `turn-when-blocked` ↔ розворот у стіни; `sound-effects` ↔ нота на подію; `game-loop` ↔ такт; `game-pause` ↔ Play/Pause; `state-string` ↔ посилання на твір; `keyboard-controls` ↔ Space / c у порті.
- **Нема** → пропозиції карток:
  - `+grid-sequencer` «Сітка як музичний секвенсор» · interface/sound · 🥉 · слоти {scale, tempo, size: 9}.
  - `+pitch-by-position` «Висота ноти за координатою події» · interface/sound · 🌱.
  - `+collision-rotate` «Зіткнення в одній клітинці → поворот на 90°» · entities/interact · 📎.
  - `+click-cycle-direction` «Клік по колу: напрямки → стерти» · interface/input · 🌱.
  - `+scale-select`, `+cellular-automaton-rule`, `+step-run-speed` (є в корпусі).

## Пропозиції до словників
- `+card:grid-sequencer` — генеративна музика з автомата; у каталозі звук лише як ефект події.
- `+card:pitch-by-position` — відображення координати на щабель ладу.
- `+trigger:converge(cell)` — дві й більше сутностей цілять в одну клітинку в одному тіку (одночасний рух; ширше за `contact`).
- `+ui:scale-picker` — вибір ладу/набору нот.

## Джерела
- ⭐ [earslap: Otomata](http://earslap.com/page/otomata.html) — правила автора: 4 стани, рух щоциклу, стіна → нота за позицією удару й розворот, зіткнення → поворот за годинниковою, керування кліками, темп і лад у другому релізі, «Copy Piece Link», iOS.
- [stelabouras/Otomata: script.js](https://raw.githubusercontent.com/stelabouras/Otomata/master/script.js) — HTML5-порт: 9×9, порядок кроку, нота = стовпець/8 − рядок, групування за клітинкою-ціллю, цикл кліків, Space/c, стан у `#cells=`.
- [marwahaha/otomata: scales.txt](https://raw.githubusercontent.com/marwahaha/otomata/master/scales.txt) — 40 ладів по 9 нот (Otomata, Aeolian, Dorian, Hijaz, Pygmy, Blues…).
- [archiloque/otomata-js](https://github.com/archiloque/otomata-js) — порт: `numberOfCells: 9`, 57 ладів.
- [Otomata DX](https://elanarko.itch.io/otomata-dx) — ремейк: керування кліками, нота при зіткненні й при відбитті.
- YouTube: пошук «otomata generative sequencer».

## Непевне
- (?) Як оригінал обробляє зустрічних сусідів (A ↔ B): у порті stelabouras вони проходять одна крізь одну без повороту — це може бути відмінністю порту.
- (?) Порядок «поворот після кроку» і повна відповідність портів оригіналу — порти зроблено реверс-інжинірингом.
- (?) Межі темпу і точний список ладів в оригіналі (порти мають 40 і 57).
- (?) Рік iOS-версії й чи є в ній інші режими.
