---
title: EXAPUNKS
slug: exapunks
aka: [Exapunks, EXA, Trash World News]
family: program-robots
also: [thinky]
klass: cursor
axes:
  field: graph
  time: programmed
  opponent: ai
  info: full
  random: both
  goal: state
year: 2018
platforms: [PC, Mac, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Exapunks", best: true, note: "EXA-агенти, самокопіювання, 100 сценаріїв, метрики cycles/size/activity, битви, зін, редактор, Redshift, пасьянс"}
  - {kind: steam, url: "https://store.steampowered.com/app/716490/EXAPUNKS/", note: "фічі: level editor, Workshop, лідерборди, мультиплеєрні битви"}
  - {kind: official, url: "https://www.zachtronics.com/exapunks/", note: "офіційна сторінка: зін TRASH WORLD NEWS, ПАСЬЯНС, HACK*MATCH, TEC Redshift"}
  - {kind: official, url: "http://www.zachtronics.com/virtualnetwork/", note: "API редактора Axiom VirtualNetwork+: хости, лінки, файли, регістри, цілі, таблиці I/O"}
  - {kind: other, url: "https://izzzzzzzzzzy.blogspot.com/2025/02/revisiting-exapunks-part-05-instruction.html", note: "огляд усіх інструкцій і регістрів X/T/F/M"}
  - {kind: other, url: "https://www.reddit.com/r/exapunks", note: "спільнота, розвʼязки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=exapunks+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [command-program, step-execution, code-editor-window, sensor-predicates, sequential-levels, level-unlock, puzzle-select, leaderboard, in-game-editor, level-exchange, random-walk, game-screen, end-screen, help-window, +swarm-separate-programs, +self-replicating-agent, +agent-kill, +host-network-links, +cell-capacity-host, +held-file-cursor, +port-blocking-message, +local-global-channel, +hardware-registers, +io-test-streams, +random-test-cases, +solution-metrics, +metric-histograms, +leave-no-trace, +agent-battle, +solitaire-minigame, +sandbox-mode, +printed-manual, +runtime-error-stop, +puzzle-scripting-api]
proposes: ["+effect:link(a, id)", "+effect:kill(b)", "+effect:jump(to)", "+effect:send(port, v)", "+effect:recv(port)", "+effect:wait", "+cond:host_has_space(host)", "+role:host", "+role:file", "+role:register", "+window:zine", "+window:battle-setup", "+feature:leave-no-trace", "+feature:puzzle-scripting-api"]
author: opus
date: 2026-11-09
---

# EXAPUNKS — пишеш агентів-EXA, які стрибають між хостами мережі, копіюють себе, тягають файли й убивають чужих агентів

## Суть
Zachtronics-пазл про хакінг 1997 року: гравець пише код для **EXA** (EXecution Agent) — агента з крихітним асемблером, двома регістрами й однією рукою для файла. EXA ходить мережею хостів через лінки за номерами, бере, редагує й видаляє файли, читає/пише апаратні регістри (банкомат, табло, власне тіло героя) і **реплікує** себе (`REPL`), щоб працювати паралельно. Кількість агентів необмежена, але памʼяті мало, тож агенти координуються через спільний канал `M`. Розвʼязок мусить пройти 100 випадкових сценаріїв, потім — оптимізація за трьома метриками; окремо — битви EXA проти EXA суперника.

## Поле і час
- Поле — **граф хостів**: кожен хост — маленька квадратна сітка клітин; хости зʼєднані лінками з номерами на кожному кінці (`LINK 800` — номер з боку відправника); номер `-1`/відсутній = одностороння чи закрита дорога (?).
- Клітина хоста вміщує одну сутність: EXA або файл (або апаратний регістр на фіксованому місці) — хост має **місткість**.
- Час `programmed`: цикл — усі EXA паралельно виконують по інструкції; `M`-обмін блокує писача до читача; `NOOP` — пропуск циклу.
- Сценарій (test run) — та сама мережа з іншими даними; 100 сценаріїв на розвʼязок, частина випадкова.
- Випадковість і в рантаймі: `RAND`, `KILL` при кількох кандидатах обирає випадково.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| EXA гравця | player | код, `X` (число/слово), `T` (true/false), `F` (курсор файла), `M` (канал), рука для 1 файла | виконує свій код; копіюється `REPL`; гине при помилці (?) |
| EXA суперника / захисні EXA | enemy | свій код | у битвах і в деяких мережах: рухаються, шукають, вбивають (?) |
| Хост | zone | сітка W×H, імʼя | місце для EXA й файлів; `HOST` пише імʼя в регістр |
| Лінк | conduit | ID на кожному кінці | `LINK id` переносить EXA в сусідній хост, якщо там є місце |
| Файл | object | ID, вміст — список чисел/слів | береться `GRAB id`, створюється `MAKE`, видаляється `WIPE`, кладеться `DROP` |
| Заблокований файл | static | ID | лишається у своєму хості, не переноситься |
| Апаратний регістр `#NAME` | conduit | 4 символи, read/write | читання/запис керує пристроєм (рахунок, дисплей, мотор…) |
| Канал `M` | conduit | режим global / local | запис чекає читача; global — у всій мережі, local — у межах хоста |
| Хост гравця | static | — | точка старту; з нього стартує перша EXA |
| Таблиця I/O | source / sink | вхідні й очікувані стовпці | вхід читається з регістрів, вихід перевіряється з очікуваним |
| Інструкції даних | — | `COPY` · `ADDI SUBI MULI DIVI MODI` · `SWIZ` · `RAND` | арифметика на 3 операнди; `SWIZ` — перестановка цифр |
| Інструкції керування | — | `MARK` · `JUMP` · `TJMP` · `FJMP` · `TEST =/</>` · `HALT` · `NOTE` · `NOOP` | мітки, стрибки за `T`, порівняння пише 0/1 в `T` |
| Інструкції мережі | — | `LINK` · `HOST` · `REPL` · `KILL` · `MODE` · `VOID M` · `TEST MRD` | рух, копія, вбивство, режим каналу, «чи є що читати» |
| Інструкції файлів | — | `MAKE` · `GRAB` · `FILE` · `SEEK` · `VOID F` · `DROP` · `WIPE` · `TEST EOF` | робота з файлом у руці через курсор `F` |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «кожна EXA, що не чекає, виконує одну інструкцію»`.
- КОЛИ `exec(LINK id)` → ЯКЩО `custom: «з цього хоста є лінк id»` and `custom: «у цільовому хості є вільна клітина»` → ТО `custom: «link: EXA переходить у сусідній хост»`; інакше `crash` (?) / чекає (?).
- КОЛИ `exec(REPL label)` → ЯКЩО `custom: «поруч є вільна клітина»` → ТО `clone(exa)`; копія стартує з `label`, з копією `X`/`T` (?).
- КОЛИ `exec(KILL)` → ЯКЩО `count(exa, >=, 2)` у хості → ТО `custom: «знищити іншу EXA в хості, випадкову, якщо їх кілька»`.
- КОЛИ `exec(GRAB id)` → ЯКЩО `occupied(host, file id)` and `not has(exa, file)` → ТО `pickup`; інакше `crash`.
- КОЛИ `exec(MAKE)` → ЯКЩО `not has(exa, file)` → ТО `spawn(file)` у руці EXA.
- КОЛИ `exec(DROP)` → ЯКЩО `custom: «є вільна клітина»` → ТО `place(file, here)`.
- КОЛИ `exec(WIPE)` → ТО `disappear_b` (файл у руці зникає).
- КОЛИ `custom: «читання F»` → ТО `custom: «значення під курсором → регістр, курсор +1»`; запис у `F` — `set_value` / дописування в кінець.
- КОЛИ `exec(SEEK n)` → ТО `custom: «курсор ±n, з обмеженням початком/кінцем файла»`.
- КОЛИ `exec(TEST EOF)` → ТО `custom: «T = курсор у кінці файла»`.
- КОЛИ `exec(COPY v M)` → ТО `custom: «EXA чекає, доки інша EXA прочитає M (global — будь-де, local — у хості)»`.
- КОЛИ `exec(TEST MRD)` → ТО `custom: «T = у каналі M є значення для читання»`.
- КОЛИ `exec(TEST a op b)` → ТО `set_value(T, 0|1)`; КОЛИ `exec(TJMP|FJMP)` → ЯКЩО `state(T, true|false)` → ТО `custom: «перехід на мітку»`.
- КОЛИ `exec(ADDI|SUBI|MULI|DIVI|MODI a b r)` → ТО `set_value(r, a op b)`; ЯКЩО `custom: «ділення на 0 / не число»` → ТО `crash` (?).
- КОЛИ `custom: «запис у #REG»` → ТО `custom: «пристрій реагує (виплата, піксель, лічильник)»`; читання → `custom: «поточне значення пристрою»`.
- КОЛИ `crash` (помилка інструкції) → ТО `disappear_a` (EXA гине; файл у руці падає на місце (?)).
- КОЛИ `exec(HALT)` або `program_end` → ТО `disappear_a` (EXA зникає з мережі).
- КОЛИ `custom: «усі цілі сценарію виконано (файли створено/переміщено/змінено/видалено, вихідні стовпці правильні)»` → ТО `custom: «наступний сценарій»`.
- КОЛИ `custom: «ціль "leave no trace"»` → ЯКЩО `custom: «у мережі лишилась EXA або файл гравця»` → ТО `custom: «сценарій не зараховано»` (?).
- КОЛИ `custom: «пройдено 100 сценаріїв»` → ТО `win`, `window(end-screen)` з гістограмами.
- Битва: КОЛИ `custom: «спільна мережа з EXA суперника»` → ТО `custom: «бали за захоплені цілі»`; переможець — більше балів за ліміт циклів (?).
- Перемога: усі 100 сценаріїв · Поразка: нема — невдалий сценарій показує, де зламалось · Рахунок: **cycles** (найдовший сценарій (?)), **size** (інструкцій у всіх EXA), **activity** (кількість `LINK` і `KILL`) — менше краще.

## Керування і ввід
- Клік «нова EXA» → вкладка з текстовим редактором; набір асемблера з клавіатури; кілька EXA — кілька вкладок.
- Кнопки RUN, STEP (один цикл), FAST, STOP; номер сценарію можна перемикати для дебагу.
- Під час виконання видно кожну EXA в хості, її регістри, файл у руці з курсором, значення `M` «в польоті».
- Документація — зін *TRASH WORLD NEWS* (читати в грі або роздрукувати).
- Редактор пазлів — JavaScript-скрипт мережі (`createHost`, `createLink`, `createNormalFile`, `createRegister`, `requireMoveFile`, `addTableOutput`…).

## Вікна, меню, HUD
- `puzzle-select`: «робочий стіл» героя — чат з EMBER-2 і список хакерських замовлень (банк, університет, ТБ, банкомат, власне тіло), відкриваються послідовно.
- `game-screen`: мапа мережі (хости-сітки з лінками й номерами, файли, регістри, EXA) + `code-editor` з вкладками EXA + панель цілей + таблиця I/O (якщо є) + кнопки RUN/STEP/FAST/STOP.
- HUD: `instruction-highlight` у кожній EXA, значення X/T/F/M, лічильник циклів, номер сценарію.
- `end-screen` з `metric-histograms` (cycles/size/activity) і друзями.
- `zine` (custom): зін TRASH WORLD NEWS, випуски 1 і 2.
- `battle-setup` (custom): битви проти хакерів-NPC і друзів.
- `editor-window`: Axiom VirtualNetwork+ — свої мережі, Workshop.
- Міні-ігри як окремі вікна: ПАСЬЯНС (пасьянс), HACK\*MATCH (match-гра на консолі Sawayama WonderDisc), TEC Redshift (кишенькова консоль для власних ігор).
- `dialogue-window`: чати сюжету між пазлами.

## Фічі поза полем
- `solution-metrics` + гістограми + `leaderboard-online` (друзі Steam).
- `random-test-cases`: 100 сценаріїв на розвʼязок.
- `level-editor` (JavaScript API) + `level-sharing` через Steam Workshop; відкривається після частини сюжету.
- `mode-versus`: битви EXA проти EXA (NPC-хакери, друзі).
- `mode-sandbox`: TEC Redshift — програмувати власні ігри; безкоштовний Redshift Player для них.
- Міні-ігри: пасьянс, HACK\*MATCH.
- `rules-page`: зін як друкований мануал; `achievements`, `cloud-save`.

## Варіації й родичі
- [tis-100](tis-100.md) — паралельні вузли з портами, але вузли нерухомі; в EXAPUNKS виконавці самі ходять мережею й копіюються.
- [human-resource-machine](human-resource-machine.md) і [7-billion-humans](7-billion-humans.md) — асемблер/багато виконавців для новачків; [core-war](core-war.md) — агенти-програми, що вбивають чужі (EXA-битви — його нащадок).
- SHENZHEN I/O (мікроконтролери), [opus-magnum](opus-magnum.md), [spacechem](spacechem.md) — сімʼя Zachtronics з тими ж метриками.
- Осі варіацій: **виконавці** (нерухомі вузли / агенти, що ходять і копіюються); **памʼять** (регістри / файл у руці з курсором); **звʼязок** (сусідні порти / глобальний і локальний канал); **суперник** (нема / NPC-захист / EXA гравця-друга); **ціль** (вихідні потоки / стан файлів / «не лишити слідів»).

## Цікавинки для курсу
- Інтерпретатор EXA-асемблера (`COPY`, арифметика, `TEST/TJMP/FJMP`, мітки) — 🥉.
- Мережа хостів-сіток з лінками і місткістю: `LINK` не проходить у повний хост — 🥈.
- `REPL` — агент копіює себе з іншої мітки; дерево процесів, що росте експоненційно — 🥈.
- Файл у руці з курсором `F`, `SEEK`, `TEST EOF` — модель «рука + стрічка» — 📎.
- Канал `M` з global/local і блокуванням до читача — 🥇 (рандеву між довільними агентами).
- Перевірка на 100 випадкових сценаріях + метрики cycles/size/activity — 🥉.
- Цілі як дані (`requireMoveFile`, `requireDeleteFile`, таблиця I/O) — редактор пазлів через API — 🥈.
- Битва двох програм у спільній мережі з `KILL` — 🥇.

## Мапа на каталог
- Є: `command-program` · `step-execution` · `code-editor-window` · `sensor-predicates` (`TEST`, `TEST MRD`, `TEST EOF`) · `sequential-levels` / `level-unlock` / `puzzle-select` · `leaderboard` · `in-game-editor` + `level-exchange` (Workshop) · `random-walk` (агенти NPC, `RAND`) (?) · `game-screen` · `end-screen` · `help-window` (зін).
- **Нема** → пропозиції карток:
  - `+swarm-separate-programs`, `+port-blocking-message`, `+io-test-streams`, `+random-test-cases`, `+solution-metrics`, `+metric-histograms`, `+solitaire-minigame`, `+sandbox-mode`, `+printed-manual`, `+runtime-error-stop` — уже пропоновані в сімʼї.
  - `+self-replicating-agent` «Агент копіює себе з іншої точки програми» · game-logic/program · 🥈.
  - `+agent-kill` «Агент знищує іншого агента в тій самій зоні» · entities/combat · 📎.
  - `+host-network-links` «Граф кімнат-сіток з нумерованими лінками» · levels/structure · 🥈.
  - `+cell-capacity-host` «Зона з місткістю: не ввійти в повну» · entities/legality · 📎.
  - `+held-file-cursor` «Предмет у руці — список значень з курсором» · entities/state · 📎.
  - `+local-global-channel` «Канал повідомлень з режимом local/global» · game-logic/program · 🥈.
  - `+hardware-registers` «Регістри-пристрої: запис керує світом» · entities/interact · 📎.
  - `+leave-no-trace` «Ціль: наприкінці не лишити своїх сутностей» · game-logic/win · 🌱.
  - `+agent-battle` «Дві програми в спільній мережі за бали» · game-logic/opponent · 🥇.
  - `+puzzle-scripting-api` «Пазл описується скриптом з API» · levels/editor · 🥈.

## Пропозиції до словників
- `+effect:link(a, id)` — перехід агента в сусідню зону за номером лінка.
- `+effect:kill(b)` — знищити іншого актора-програму (ширше за `disappear_b`: обирає ціль у зоні).
- `+effect:jump(to)`, `+effect:send(port, v)`, `+effect:recv(port)`, `+effect:wait` — як у TIS-100 (повтор для підрахунку).
- `+cond:host_has_space(host)` — у зоні є вільна клітина.
- `+role:host` (зона-кімната з місткістю), `+role:file` (дані-обʼєкт), `+role:register` (пристрій-порт).
- `+window:zine` — зін-мануал у грі; `+window:battle-setup` — вибір суперника для битви.
- `+feature:leave-no-trace`, `+feature:puzzle-scripting-api`.

## Джерела
- ⭐ [Wikipedia: Exapunks](https://en.wikipedia.org/wiki/Exapunks) — EXA, самокопіювання, обмежена памʼять, 100 сценаріїв, метрики (цикли, розмір, рух і вбивства), битви, зін TRASH WORLD NEWS, редактор + Workshop, Redshift, пасьянс і tile-matching, 2018.
- [Steam: EXAPUNKS](https://store.steampowered.com/app/716490/EXAPUNKS/) — level editor, Workshop, лідерборди, мультиплеєрні битви, міні-ігри.
- [Zachtronics: EXAPUNKS](https://www.zachtronics.com/exapunks/) — EXA «move through networks, replicate, trash files, terminate other EXAs», ПАСЬЯНС, HACK\*MATCH, Redshift, зіни.
- [Axiom VirtualNetwork+](http://www.zachtronics.com/virtualnetwork/) — модель світу: хости на сітці з W×H, лінки з ID на кінцях, звичайні й заблоковані файли, регістри з 4-символьними іменами, типи цілей, таблиці I/O, випадковість.
- [Revisiting EXAPUNKS: instruction overview](https://izzzzzzzzzzy.blogspot.com/2025/02/revisiting-exapunks-part-05-instruction.html) — регістри X/T/F/M і всі інструкції з описом.
- [r/exapunks](https://www.reddit.com/r/exapunks) — спільнота.

## Непевне
- (?) Що буває при невдалому `LINK` / `REPL` у повний хост — помилка чи очікування; з памʼяті — EXA гине при більшості помилок.
- (?) Правило «leave no trace» і чи всі пазли його мають — з памʼяті.
- (?) Метрика cycles — найгірший чи середній сценарій; Wikipedia лише називає метрики.
- (?) Номери лінків (800 — вхідний, −1 — назад) — з памʼяті; API підтверджує лише «ID на кожному кінці».
- (?) Правила битв (бали, ліміт циклів, стартові позиції) — джерела кажуть лише «EXA проти агентів суперника».
- (?) Діапазон значень −9999…9999 — бачив лише в пошуковому сніпеті.
