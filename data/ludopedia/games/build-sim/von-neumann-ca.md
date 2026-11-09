---
title: Von Neumann cellular automaton (автомат фон Неймана, 29 станів) і Codd's CA
slug: von-neumann-ca
aka: [JvN29, «29-станний автомат», von Neumann universal constructor, «універсальний конструктор», Nobili32, Hutton32, Codd's cellular automaton, «автомат Кодда», Devore's CA]
family: build-sim
also: [program-robots]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: none
year: 1966
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Von_Neumann_cellular_automaton", best: true, note: "29 станів (U, 8 сенситивних, 4 конфлюентні, 8+8 передавальних), OR/AND, дерево будівництва, руйнування, Nobili32, Hutton32"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Von_Neumann_universal_constructor", note: "A конструктор, B копіювальник, C контролер, D допоміжний, Φ стрічка; реалізації 1995–2012 з розмірами; hashlife у Golly"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Codd%27s_cellular_automaton", note: "Codd 1968: 8 станів, поворотна симетрія, дріт 1 в оболонці 2, поїзди сигналів extend/retract/mark/sense…, Devore 1973, Hutton 2009, таблиця самовідтворювачів"}
  - {kind: official, url: "https://golly.sourceforge.io/Help/Algorithms/JvN.html", note: "Golly: алгоритм JvN з правилами JvN29, Nobili32, Hutton32 і зразками (read-arm-demo, sphinx, NP-replicator)"}
  - {kind: other, url: "https://github.com/GollyGang/ruletablerepository/wiki/CoddsDesign", note: "реалізація машини Кодда (Hutton): контрольна частина, гейти, стрічки M/P/D, рукав, 16 інструкцій як W-машина Ванга"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=von+Neumann+universal+constructor+Golly", note: "пошук; відтворення в Golly"}
stage: v1
coverage: 60
mechanics: [game-loop, game-pause, state-as-data, level-from-txt, import-open-formats, cell-click, editor-palette, orientation-state, field-scaling, rule-variants, logic-render-split, unit-tests, fixture-level-tests, +cellular-automaton-rule, +multi-state-cell, +rule-table-file, +rotational-symmetry, +signal-propagation, +self-replication, +step-run-speed, +pattern-library, +logic-circuit-wiring, +universal-constructor, +construction-arm, +state-construction-tree, +mutual-destruction, +hashlife]
proposes: ["+cond:input_history", "+effect:construct_cell", "+card:universal-constructor", "+card:construction-arm", "+card:state-construction-tree", "+card:hashlife", "+axis:symmetry"]
author: opus
date: 2026-11-09
---

# Von Neumann CA — 29 станів: дроти, вентилі й рукав, що за стрічкою-описом будує копію машини разом зі стрічкою

## Суть
Перший клітинний автомат (Джон фон Нейман за ідеєю Станіслава Улама, 1940-ві; книга з Артуром Бьорксом — 1966) створено, щоб зрозуміти, яка мінімальна складність потрібна машині для **самовідтворення**. 29 станів клітини утворюють «електроніку»: спрямовані дроти двох типів, вентилі-конфлюенти й порожнечу, з якої сигнали певного ритму **будують** нові клітини. Машина-конструктор читає стрічку-опис, рукавом збудовує на відстані таку саму машину, копіює їй стрічку й запускає. Едгар Кодд (1968) повторив універсальність на 8 станах із поворотною симетрією; з Кодда виросли [Langton's loops](langtons-loops.md).

## Поле і час
- Нескінченна квадратна сітка однакових скінченних автоматів; сусідство фон Неймана (4 ортогональні); усі клітини оновлюються синхронно за спільним годинником.
- JvN29 — **без симетрії**: стан має напрям (північ, південь, захід, схід), правило залежить від того, куди дивиться сусід.
- Codd — 8 станів із поворотною симетрією (запис правила діє в усіх 4 поворотах).
- Масштаби величезні: тіло реплікатора — тисячі клітин, стрічка — десятки й сотні тисяч, відтворення — мільярди тіків (див. «Варіації»).
- Тік = одне оновлення; сигнал проходить звичайним дротом 1 клітину за тік, конфлюентом — із додатковою затримкою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожнеча U (ground) | terrain | — | тло; отримавши вхід, стає сенситивною і починає «будуватись» |
| Сенситивні стани S, S0, S00, S000, S01, S1, S10, S11 | mark | історія входів | проміжні: записують, був чи не був вхід на кожному тіку; гілка дерева будівництва |
| Конфлюент C00, C01, C10, C11 | switch | поточне й наступне збудження | AND входів; затримка на 1 тік довша; міст між звичайними й спеціальними дротами; не передає конфлюенту |
| Звичайний передавальний (ordinary, OTS) | conduit | N / S / W / E × спокій / збуджений | OR входів, що вказують на нього; передає в напрямку, куди дивиться |
| Спеціальний передавальний (special, STS) | conduit | N / S / W / E × спокій / збуджений | те саме, але для «будівельних» сигналів; руйнує звичайні клітини |
| Сигнал (імпульс) | tile | 1 біт | збуджений стан, що біжить дротом; ритм бітів кодує команди |
| Стрічка-опис Φ | container | рядок клітин | як стрічка Тюрінга: інструкції по одній; її копіюють, а не будують |
| Універсальний конструктор A | object | — | читає Φ і будує машину, яку Φ описує (без стрічки) |
| Копіювальник B | object | — | робить копію Φ і віддає нащадку |
| Контролер C | object | — | керує A і B, запускає нащадка |
| Допоміжний автомат D | object | — | будь-яка функція поза відтворенням; мутації в його описі — шлях до еволюції |
| Рукав (construction arm) | object | — | дріт, що висувається з машини й будує клітини на відстані |
| Зчитувальний рукав (read arm) | object | — | ходить уздовж стрічки й читає біти (зразок Golly `read-arm-demo`) |
| Codd: тло 0, дріт 1, оболонка 2, сигнали 4–7 | conduit | 8 станів | сигнали-пари «s 0» біжать дротом 1 в оболонці 2 |
| Codd: гейт | gate | відкритий / закритий | маршрутизує сигнали від періодичного емітера до стрічок і назад |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «новий стан = f(стан, 4 сусіди з їх напрямками)», синхронно для всіх`.
- Передача (OR): КОЛИ `tick` → ЯКЩО `state(x, transmission)` and `custom: «хоч один вхід, що вказує на x, був збуджений»` → ТО `set_state(x, excited)`; інакше `set_state(x, quiescent)`.
- КОЛИ `tick` → ЯКЩО `facing(receiver, sender)` → ТО `custom: «дані зникають»` — дріт, що дивиться назад, не приймає.
- Конфлюент (AND): КОЛИ `tick` → ЯКЩО `state(x, confluent)` and `custom: «збуджені всі звичайні входи, що вказують на x»` → ТО `custom: «через тік збуджуються вихідні дроти, що дивляться геть від x»`.
- КОЛИ `tick` → ЯКЩО `state(x, confluent)` and `custom: «нема вихідного дроту, крім тих, що вказують на x»` → ТО `custom: «збережений біт втрачено»`.
- Будівництво: КОЛИ `contact(signal, ground)` → ТО `transform(ground, S)`.
- КОЛИ `tick` → ЯКЩО `state(x, sensitised)` → ТО `custom: «наступний стан за деревом: 1 — був вхід, 0 — не було»`.
- Дерево: `10000` → OTS схід (за замовчуванням: 1 вхід і 4 тіки тиші) · `10001` → OTS північ · `1001` → OTS захід · `1010` → OTS південь · `1011` → STS схід · `1100` → STS північ · `1101` → STS захід · `1110` → STS південь · `1111` → конфлюент C00 — разом 9 типів, які можна збудувати.
- Руйнування: КОЛИ `contact(special_signal, ordinary_or_confluent)` → ТО `transform(cell, ground)`.
- КОЛИ `contact(ordinary_signal, special)` → ТО `transform(cell, ground)` — два типи дротів взаємно руйнівні.
- Отже рукав будує так: висуває дріт, «стріляє» серією бітів у порожню клітину (будує), або сигналом іншого типу стирає її (відступає).
- Конструктор: КОЛИ `exec(instruction)` → ТО `custom: «рукав: висунути / відвести / повернути / побудувати клітину типу k»` — інструкції йдуть зі стрічки по одній.
- КОЛИ `program_end` (опис прочитано) → ТО `clone(tape)` (копіювальник B), `custom: «копію віддати нащадку»`, `custom: «запустити нащадка»` → нащадок відтворюється далі.
- Чому окремий копіювальник: `custom: «опис не може містити інструкцій побудувати стрічку такого ж розміру»` — тому стрічку копіюють пасивно (як реплікація ДНК), а машину будують активно (як трансляція).
- КОЛИ `custom: «мутація в описі D»` → ТО `custom: «нащадок інший, але відтворюється»` — ідея еволюції; на практиці більшість збурень ламає машину.
- Nobili32: + 3 стани — конфлюент може **перехрещувати** сигнали й зберігати інформацію; реплікатор різко менший.
- Hutton32: та сама множина станів, трохи змінена таблиця — зациклена стрічка відтворюється, як петлі Ленгтона.
- Codd: КОЛИ `reach(signal_7_0, wire_end)` → ТО `custom: «кінець дроту оголюється»`.
- Codd: КОЛИ `reach(signal_6_0, wire_end)` → ТО `custom: «кінець знову в оболонці»` → дріт довший на 1.
- Codd, поїзди сигналів: extend `70116011` · extend_left `4011401150116011` · extend_right `5011501140116011` · retract `4011501160116011` · retract_left `5011601160116011` · retract_right `4011601160116011` · mark `701160114011501170116011` · erase `601170114011501160116011` · sense `70117011` · cap `40116011` · inject_sheath `701150116011` · inject_trigger `60117011701160116011`; між деякими треба два порожні (стан 1) кроки, інакше заважають.
- Codd, машина: КОЛИ `exec(f_k)` (одна з 16 декодованих інструкцій) → ТО `custom: «мікропрограма відкриває гейти; сигнал емітера йде на стрічки M / P / D або в рукав»` — потужність W-машини Ванга.
- Перемоги, поразки й рахунку нема.

## Керування і ввід
- Golly: алгоритм JvN, правило JvN29 / Nobili32 / Hutton32; відкрити зразок, Run/Pause, Step, швидкість, зум.
- Палітра 29 (32) станів, клік — поставити стан; на практиці машини вантажать готовими файлами (`.rle`, `.mc.gz`).
- Кнопка `i` — інформація про патерн (опис зразка).
- Codd: правило з Rule Table Repository; повна машина Хаттона — архів ≈13 MB (Codd-self-rep.zip).

## Вікна, меню, HUD
- `game-screen` (Golly): поле з кольорами станів, `speed-slider`, `step-button`, `zoom-control`; рядок покоління й популяції (`generation-counter`).
- `element-picker` — палітра станів (?).
- `custom-window` бібліотеки патернів (Patterns → Self-Rep / JvN: counter-demo, cell-coders-demo, read-arm-demo, sphinx, construction-arm-demo, NP-replicator, golly-constructor, Hutton-replicator).
- `help-window` алгоритму JvN і `about-window` патерна (кнопка `i`).

## Фічі поза полем
- `custom-rules`: JvN29 / Nobili32 / Hutton32; Codd і Devore — таблицями правил.
- `+hashlife`: з 2008 року hashlife у Golly для 29 і 32 станів — відтворення, раніше непрактичне, займає хвилини на звичайному ПК (але багато памʼяті).
- `export-import` патернів (RLE, macrocell `.mc`), `step-mode`, `speed-control`, `pause`.
- Рівнів, рахунку, збережень прогресу нема.

## Варіації й родичі
- **Осі варіацій:** кількість станів (29 / 32 / 8 / 2–4) · симетрія (нема — JvN / повороти — Codd, Devore, Langton / повороти й відображення — Banks) · перехрещення сигналів (нема / конфлюент-перехрестя — Nobili) · стрічка (лінійна / зациклена — Hutton32) · універсальність (так / ні — Langton) · синхронний / асинхронний автомат (Nehaniv 2002, Takada 2004).
- Таблиця самовідтворювачів (Wikipedia, стаття Codd): фон Нейман — 29 станів, без симетрій, універсальний, 130 622 клітини · Codd — 8, повороти, універсальний, 283 126 588 · Devore (1973) — 8, повороти, універсальний, 94 794 · Banks IV — 2–4, повороти й відображення, універсальний, ≈10¹¹ · Langton — 8, повороти, **не** універсальний, 86.
- Реалізації універсального конструктора (тіло / стрічка): Nobili — Pesavento 1995, 32 стани, 6 329 / 145 315, ≈63 млрд тіків, не повертається до початкового стану · Nobili 2007, 5 313 / 56 325 (run-length-кодування стрічки) · Buckley 2008 codon5, 3 343 / 44 155 · Buckley 2008 replicator.mc, 29 станів, 18 589 / 294 844 · Goucher і Buckley 2012, 3 957 / 8 920.
- Codd: задумав універсальну машину на основі W-машини Ванга, але не реалізував; Тім Хаттон зібрав її у 2009 (стаття 2010), виправивши дрібні помилки Кодда (гейти t12 і A).
- Нащадки в корпусі: [langtons-loops](langtons-loops.md) (Codd → 86 клітин без універсальності), [wireworld](wireworld.md) (дроти й вентилі як стани), [game-of-life](game-of-life.md) (2 стани, теж універсальний), [cell-machine](cell-machine.md), [minecraft-redstone](minecraft-redstone.md) (логіка сигналами по клітинах).

## Цікавинки для курсу
- Двіжок JvN29: 29 станів, напрямки, OR / AND, затримка конфлюента — 🥉 (таблиця станів + юніт-тести на кожне правило).
- Дерево будівництва: автомат «історія входів → тип клітини» і тест «10000 → дріт на схід» — 📎.
- Взаємне руйнування двох типів дротів і рукав «висунь / побудуй / відведи» на малому полі — 🥈.
- Codd: генератор поїздів сигналів (extend, retract…) з вставкою пауз — 📎.
- Програвач готових машин Golly (`.rle` / `.mc`) + лічильник поколінь — 🥉.
- Hashlife для багатостанового автомата — 👑.

## Мапа на каталог
- Є: `game-loop` + `game-pause` · `state-as-data` · `level-from-txt` + `import-open-formats` (RLE, macrocell) · `cell-click` + `editor-palette` (29 станів) · `orientation-state` (напрям передавальних станів) · `field-scaling` · `rule-variants` (JvN29 / Nobili32 / Hutton32 / Codd) · `logic-render-split` · `unit-tests` + `fixture-level-tests`.
- Перевикористано з корпусу: `+cellular-automaton-rule`, `+multi-state-cell`, `+rule-table-file`, `+rotational-symmetry` (Codd), `+signal-propagation`, `+self-replication`, `+step-run-speed`, `+pattern-library`, `+logic-circuit-wiring`.
- **Нема** → пропозиції карток:
  - `+universal-constructor` «Машина будує будь-яку описану конфігурацію за стрічкою» · game-logic · 👑 · слоти {tape, arm}.
  - `+construction-arm` «Рукав висувається й ставить клітини на відстані» · game-logic · 🥈.
  - `+state-construction-tree` «Тип нової клітини визначає ритм вхідних бітів» · game-logic · 📎 · слоти {tree}.
  - `+mutual-destruction` «Два типи сигналів стирають клітини одне одного» · game-logic · 🌱.
  - `+hashlife` «Мемоізоване квадродерево для гігантських поколінь» · code/architecture · 👑.

## Пропозиції до словників
- `+cond:input_history` — послідовність «був / не був вхід» за останні тіки (дерево будівництва JvN).
- `+effect:construct_cell` — сигнал у порожню клітину робить її клітиною заданого типу (будівельний рукав); `transform` не каже, що тип задає ритм.
- `+axis:symmetry` — `none` / `rotations` / `rotations+reflections` (JvN, Codd, Banks); у CA-файлах корпусу це вже ключова різниця.
- `+card:universal-constructor`, `+card:construction-arm`, `+card:state-construction-tree`, `+card:hashlife` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Von Neumann cellular automaton](https://en.wikipedia.org/wiki/Von_Neumann_cellular_automaton) — сітка й сусідство, 29 станів поіменно, правила OR / AND, «дані зникають, якщо приймач дивиться назад», дерево будівництва з бінарними рядками, руйнування, Nobili32 і Hutton32, Golly; Von Neumann і Burks 1966.
- [Wikipedia: Von Neumann universal constructor](https://en.wikipedia.org/wiki/Von_Neumann_universal_constructor) — A / B / C / D / Φ, рукав, чому окремий копіювальник, еволюційність, лекції 1949, таблиця реалізацій 1995–2012 з розмірами, hashlife у Golly з 2008.
- [Wikipedia: Codd's cellular automaton](https://en.wikipedia.org/wiki/Codd%27s_cellular_automaton) — 8 станів, поворотна симетрія, дріт 1 в оболонці 2, сигнали «7-0» і «6-0», таблиця поїздів сигналів, W-машина Ванга, Hutton 2009/2010, Devore 1973, Banks 1971, Langton 1984, таблиця самовідтворювачів.
- [Golly Help: JvN](https://golly.sourceforge.io/Help/Algorithms/JvN.html) — правила JvN29 / Nobili32 / Hutton32, список зразків, кредити (Nobili 1994, Hutton 2008).
- [Rule Table Repository: CoddsDesign](https://github.com/GollyGang/ruletablerepository/wiki/CoddsDesign) — будова машини Кодда в реалізації Хаттона: мікропрограма, гейти, стрічки M / P / D, емітер, декодер, 16 інструкцій.
- YouTube: пошук «von Neumann universal constructor Golly».

## Непевне
- (?) Точні умови виходу конфлюента (які саме сусіди отримують сигнал, чи може він живити спеціальний дріт) — у статті лише «міст між звичайними й спеціальними лініями».
- (?) Ролі станів Кодда 3–7 поодинці — у джерелах лише «дріт 1, оболонка 2» і сигнали 4–7 у поїздах; стан 3 не описаний.
- (?) Розмір 130 622 клітини для фон Неймана в таблиці Codd-статті не збігається з жодним рядком таблиці реалізацій (?).
- (?) Вигляд палітри станів у Golly й кнопка `i` — з довідки Golly для зразків, інтерфейс не бачив.
- (?) Рік: 1966 — книга Бьоркса; сам автомат — кінець 1940-х (лекції 1949); Codd — 1968.
