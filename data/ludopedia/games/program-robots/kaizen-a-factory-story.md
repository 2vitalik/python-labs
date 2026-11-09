---
title: "Kaizen: A Factory Story"
slug: kaizen-a-factory-story
aka: [Kaizen]
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC, Mac, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kaizen:_A_Factory_Story", best: true, note: "Coincidence (Зак Барт, екс-Zachtronics), 14.07.2025; маніпулятори штовхають/тягнуть, візуальна програма на таймлайні, квота виробів, глобальні таблиці, пасьянс-пачинко"}
  - {kind: steam, url: "https://store.steampowered.com/app/2275490/", note: "Steam: weld, rivet, cut, drill; GIF-експорт; Pachi-Sol; Steam Leaderboards"}
  - {kind: official, url: "https://www.coincidence.games/kaizen", note: "сайт студії: flip, weld, cut; гістограми, перемотування й редагування в реальному часі"}
  - {kind: other, url: "https://nygamecritics.com/2025/09/04/the-insight-kaizen-a-factory-story-fills-jatin-with-enthusiasm-and-bemusement/", note: "огляд: руки push/pull, клепання й зварювання спрацьовують самі, таймлайн червоніє на помилці"}
  - {kind: other, url: "https://vaporlens.app/app/2275490/kaizen_a_factory_story", note: "зведення відгуків Steam: квадратна сітка, руки не обертаються, метрики час/площа/ціна, нема undo й редактора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaizen+a+factory+story+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, step-execution, stick-together, multi-cell-size, cell-transform, drag-drop-piece, hover-highlight, collect-quota, sequential-levels, level-unlock, level-select, leaderboard, rewind, game-screen, end-screen, tutorial-window, achievements-window, +instruction-timeline, +swarm-separate-programs, +piston-extend, +auto-join-on-contact, +cut-part, +drill-hole, +flip-part, +molecule-match-output, +input-respawn, +collision-halt, +solution-metrics, +metric-histograms, +gif-export, +live-edit-while-running, +solitaire-minigame]
proposes: ["+trigger:cycle_end", "+cond:aligned(a, b, joint)", "+effect:weld(a, b)", "+effect:cut(part, line)", "+effect:drill(part)", "+effect:flip(part)", "+effect:extend", "+effect:retract", "+effect:grab", "+effect:release", "+window:metric-histograms", "+ui:instruction-timeline", "+ui:metric-panel", "+feature:solution-metrics", "+feature:gif-export", "+feature:live-edit"]
author: opus
date: 2026-11-09
---

# Kaizen: A Factory Story — лінія з маніпуляторів на таймлайні збирає виріб із деталей; оптимізуєш час, площу й ціну

## Суть
Гравець проєктує автоматичну виробничу лінію на сітці: ставить маніпулятори (руки, що штовхають і тягнуть деталі), інструменти, що зварюють, клепають, ріжуть і свердлять, і задає кожному пристрою команди на спільному **таймлайні**. Лінія циклічно бере деталі зі входів, складає з них виріб (калькулятор, рисоварку, іграшкового робота) і здає на вихід; рівень пройдено, коли зроблено потрібну кількість виробів. Це наступник Opus Magnum від тієї ж команди: та сама формула «будь-яке рішення + метрики + гістограми», але квадратна сітка, простіші руки без обертання й перемотування часу з правкою «на ходу».

## Поле і час
- Квадратна 2D-сітка («зелена монтажна сітка» з огляду); деталі — плоскі багатоклітинні блоки; за відгуками, гра відійшла від гексів Zachtronics і прибрала обертання.
- Шари: монтажна сітка з пристроями (основа руки, інструменти, входи/виходи) · деталі й зібрані вузли зверху.
- Час `programmed`: такт = одна клітинка таймлайну; на кожному такті кожен пристрій виконує свою команду, програма повторюється по колу, доки не здано квоту.
- Повний детермінізм; помилка (зіткнення, недопустима дія) зупиняє лінію, а таймлайн підсвічує невалідний крок червоним.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рука-маніпулятор | player | основа, напрямок, хід | висувається/втягується вздовж осі, штовхає або тягне деталь; не обертається |
| Захват (grabber) | player | — | тримає деталь, щоб рука тягла її за собою (?) |
| Зварювальник | terrain | позиція, вісь | коли дві деталі зіставлено — звʼязує їх у вузол (спрацьовує сам) |
| Клепальник | terrain | позиція | як зварювальник, інший тип зʼєднання (метал/пластик (?)) |
| Ніж / лезо | terrain | лінія розрізу | ділить деталь на дві |
| Свердло | terrain | позиція | робить отвір у деталі (?) |
| Перевертач (flip) | terrain | вісь | дзеркально перевертає деталь (?) |
| Вхід деталі | spawner | шаблон деталі | щойно місце вільне — подає нову копію |
| Вихід виробу | static | шаблон виробу, квота | приймає вузол, що точно збігається зі шаблоном, рахує |
| Деталь | object | форма, матеріал | рухається лише від руки; після зварювання — разом з вузлом |
| Вузол (зібране) | object | граф зʼєднань | рухається як ціле |
| Таймлайн-доріжка | mark | рядок команд пристрою | показує команду на кожен такт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(cmd)` (такт настав, у доріжці пристрою є команда) → ТО пристрій виконує її; усі пристрої — одночасно.
- КОЛИ `exec(push)` → ЯКЩО `occupied(ahead, part)` and `free(cell_behind)` → ТО `push` (деталь зсувається на 1 разом з вузлом).
- КОЛИ `exec(pull)` → ЯКЩО `custom: «рука тримає деталь»` → ТО `pull(b)`.
- КОЛИ `exec(extend|retract)` → ТО `custom: «рука змінює довжину на 1 вздовж своєї осі»`; push і retract — окремі команди (огляд NYGC).
- КОЛИ `custom: «кінець такту»` → ЯКЩО `custom: «дві деталі стикуються на клітині зварювальника/клепальника»` → ТО `attach(a, b)` — без окремої команди; огляд скаржиться, що іноді це зʼєднує непотрібне.
- КОЛИ `exec(cut)` → ЯКЩО `occupied(blade_cell, part)` → ТО `split(a)` (деталь ділиться за лінією).
- КОЛИ `exec(drill)` → ТО `custom: «отвір у деталі»` (?).
- КОЛИ `exec(flip)` → ТО `custom: «деталь перевертається дзеркально»` (?).
- КОЛИ `custom: «на вході вільне місце»` → ТО `spawn(part)`.
- КОЛИ `custom: «на виході вузол, що точно збігся з шаблоном виробу»` → ТО `disappear_a`, `counter(produced, +1)`.
- КОЛИ `counter(produced, ==, quota)` → ТО `win`, `window(end-screen)` з метриками й гістограмами.
- КОЛИ `custom: «дві деталі/пристрої в одній клітині або неможливий рух»` → ТО `crash`: лінія зупиняється, крок таймлайну червоний.
- Перемога: квота виробів · Поразка: нема, лише зупинка симуляції · Рахунок: три метрики — **час** (такти до квоти), **площа/розмір** лінії, **ціна** (сума пристроїв); огляди називають їх «money, time and space».

## Керування і ввід
- Палітра пристроїв → drag на клітину сітки; орієнтація задається при розстановці (поворотів деталей у грі нема).
- Таймлайн знизу: рядок на кожен пристрій, клітина = такт; команди перетягуються з палітри в клітини.
- Запуск/пауза/крок; **перемотування** вперед-назад по тактах і **редагування в реальному часі** — змінена програма одразу перераховує симуляцію (сайт студії).
- Відгуки: undo для правок нема; підправити одну ділянку таймлайну складно, бо крок привʼязаний до фізичного положення пристроїв.

## Вікна, меню, HUD
- `main-menu`: продовжити, розділи, Pachi-Sol, налаштування (?).
- `level-select` — список замовлень (to-do list), що росте з прогресом; після N замовлень — нова локація/цех.
- `game-screen`: монтажна сітка; `tool-palette` пристроїв; `instruction-timeline` знизу з `instruction-highlight`; `objective-text` (деталі → виріб, квота); `metric-panel` (час, площа, ціна); кнопки Play / Step / перемотування.
- `end-screen` + `metric-histograms`: «детальний звіт: час, ефективність, прибуток», позиція на гістограмах серед гравців; кнопка експорту GIF.
- `dialogue-window` — візуальна новела між замовленнями (вибір з двох реплік, вечори з колегами, листи родині); `tutorial-window` — перші замовлення як навчання.
- `custom-window` — пасьянс-пачинко Pachi-Sol (три варіанти).
- `settings-window`, `achievements-window` (Steam).
- Переходи: замовлення → сітка → Play → квота → звіт-гістограми → наступне замовлення / діалог.

## Фічі поза полем
- `solution-metrics` у трьох вимірах + `leaderboard-online` (Steam Leaderboards) як гістограми — головна повторна гра.
- `rewind` + `live-edit`: перемотування симуляції й правка програми без перезапуску.
- `gif-export` розвʼязку, `cloud-save`, `achievements` (більшість — за пачинко, за відгуками).
- Нема `level-editor`/Workshop і нема undo (скарги у відгуках).
- `localization`: англійська + 10 мов.

## Варіації й родичі
- Попередники тієї ж команди: [opus-magnum](opus-magnum.md) (гекс, обертання рук, гліфи-трансмутатори), [spacechem](spacechem.md) (вальдо в реакторі), Infinifactory (3D-конвеєри, описує C030), Shenzhen I/O, Exapunks; у кожній — пасьянс-мінігра.
- Інші «фабрики з програмою»: [manufactoria](manufactoria.md), [7-billion-humans](7-billion-humans.md).
- Осі варіацій: **поле** (гекс / квадрат / 3D); **рука** (обертається / лише висувається); **зʼєднання** (командою / автоматично на контакті / гліфом); **зворотний звʼязок** (перезапуск / крок / перемотування з правкою наживо); **метрики** (1–3 + гістограми спільноти).

## Цікавинки для курсу
- Синхронний таймлайн кількох пристроїв: одна доріжка на пристрій, спільний такт, виявлення зіткнень — 🥇.
- Автозварювання на контакті: деталі як граф, вузол рухається як ціле, звірка з шаблоном виробу — 🥈.
- Розріз деталі ножем (поліоміно ділиться на дві компоненти звʼязності) — 🥉.
- Перемотування детермінованої симуляції: стан на такт N перераховується з нуля або з чекпойнтів — 🥈; правка наживо поверх цього — 🥇.
- Три метрики + гістограма розвʼязків групи — 📎 (дані) / 🥉 (з графіком).
- Експорт анімації рішення в GIF — 🥉.

## Мапа на каталог
- Є: `command-program` (команди пристроїв) · `step-execution` · `stick-together` (зварені вузли) · `multi-cell-size` (деталі) · `cell-transform` (інструменти на клітинах) · `drag-drop-piece` · `hover-highlight` · `collect-quota` (квота виробів) · `sequential-levels` / `level-unlock` / `level-select` · `leaderboard` · `rewind` · `game-screen` · `end-screen` · `tutorial-window` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+instruction-timeline`, `+swarm-separate-programs`, `+piston-extend`, `+molecule-match-output`, `+input-respawn`, `+collision-halt`, `+solution-metrics`, `+metric-histograms`, `+gif-export`, `+solitaire-minigame` — уже запропоновані з Opus Magnum; тут ще одне підтвердження.
  - `+auto-join-on-contact` «Зʼєднання спрацьовує саме, коли деталі зіставлено на інструменті» · entities/interact · 🥉.
  - `+cut-part` «Розріз багатоклітинної деталі на дві» · entities/interact · 🥉.
  - `+drill-hole` «Позначка-отвір як властивість деталі» · entities/state · 🌱 (?).
  - `+flip-part` «Дзеркальне перевертання фігури» · entities/move · 📎.
  - `+live-edit-while-running` «Правка програми з миттєвим перерахунком симуляції» · game-logic/program · 🥇.

## Пропозиції до словників
- `+trigger:cycle_end` — кінець такту: момент автоматичних зʼєднань і перевірки виходів (вже просили з Opus Magnum).
- `+cond:aligned(a, b, joint)` — дві деталі стикуються на клітині інструмента.
- `+effect:weld(a, b)` — постійне зʼєднання (окремий від `attach` тип звʼязку); `+effect:cut(part, line)`; `+effect:drill(part)`; `+effect:flip(part)`.
- `+effect:extend` / `+effect:retract` — довжина руки; `+effect:grab` / `+effect:release` — утримання деталі.
- `+window:metric-histograms`; `+ui:instruction-timeline`; `+ui:metric-panel`.
- `+feature:solution-metrics`, `+feature:gif-export`, `+feature:live-edit` — правка програми під час симуляції.
- Осі (вже є в `classes.md`, не пропоную): `control` = `programmed`, `actors` = `party` (кілька пристроїв, кожен зі своєю доріжкою).

## Джерела
- ⭐ [Wikipedia: Kaizen: A Factory Story](https://en.wikipedia.org/wiki/Kaizen:_A_Factory_Story) — розробник, дата, маніпулятори push/pull/rotate (?), візуальна мова на таймлайні, квота, таблиці, пасьянс-пачинко.
- [Steam 2275490](https://store.steampowered.com/app/2275490/) — weld/rivet/cut/drill, GIF, Pachi-Sol, Leaderboards/Cloud/Achievements.
- [Coincidence: Kaizen](https://www.coincidence.games/kaizen) — flip/weld/cut, гістограми, rewinding, real-time editing.
- [NY Game Critics](https://nygamecritics.com/2025/09/04/the-insight-kaizen-a-factory-story-fills-jatin-with-enthusiasm-and-bemusement/) — руки push/pull з окремим retract, клепальники й зварювальники спрацьовують самі, ножі, таймлайн червоніє.
- [Vaporlens](https://vaporlens.app/app/2275490/kaizen_a_factory_story) — зведення відгуків: квадратна сітка, без обертання, метрики, гістограми, нема undo/редактора, 3 варіанти пасьянсу.
- [Ladies Gamers](https://ladiesgamers.com/kaizen-a-factory-story-review/) — звіт «час, ефективність, прибуток», замовлення-туторіал, нові локації.

## Непевне
- (?) Точний список пристроїв і команд: окремий «захват», перевертач, свердло (лише слово drill на Steam) — семантику не бачив.
- (?) Wikipedia згадує руки, що «rotate» деталі, а зведення відгуків — що руки не обертаються; ймовірно, обертають/перевертають деталі окремі пристрої.
- (?) Steam-тег «Hex Grid» суперечить «квадратній сітці» з відгуків і огляду NYGC; узято квадрат.
- (?) Чи приймає вихід виріб лише в точній позиції шаблону; чи є стартова квота однакова для всіх рівнів — не бачив.
- (?) Точні назви й формули метрик (cycles / area / cost) — огляди називають «money, time and space» і «efficiency, cost, size».
- (?) Меню й структура розділів — з оглядів, без скріншотів.
