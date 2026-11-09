---
title: Pipe Push Paradise
slug: pipe-push-paradise
aka: [PPP]
family: push-slide
also: [connect-rotate, thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2018
platforms: [Windows, macOS, Linux, Switch, PS4, Xbox One, iOS]
links:
  - {kind: other, url: "https://www.electrondance.com/?p=13960", best: true, note: "Electron Dance: як труби перекочуються (2 поштовхи на перевертання), ротатори, ями, магнітні труби, зони, обмежений undo"}
  - {kind: steam, url: "https://store.steampowered.com/app/721390/Pipe_Push_Paradise/", note: "Corey Martin і Teo Zamudio, 18.01.2018; push, flip and roll pipes, open world"}
  - {kind: official, url: "https://pipepushparadise.com/", note: "офіційний сайт"}
  - {kind: itch, url: "https://coreymartin.itch.io/pipe-push-paradise", note: "itch.io: клавіатура/геймпад, devlog про новий набір рівнів 1.2.0"}
  - {kind: other, url: "https://www.thexboxhub.com/pipe-push-paradise-review/", note: "огляд: 47 пазлів, Easy–Expert, острів-хаб, ротатори, ями, стекування, undo/redo/reset"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pipe+Push+Paradise+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, keyboard-controls, push-object, orientation-state, height-levels, pipe-connectors, connectivity-check, stick-together, fill-hole, completion-detection, unsolvable-states, undo-redo, undo-step, redo, restart-level, level-unlock, difficulty-levels, achievements-window, +rotator-pad, +hub-island, +flow-goal-3d]
proposes: ["+effect:lift", "+effect:tip_over", "+cond:ports_aligned", "+role:rotator", "+feature:hub-world", "+card:rotator-pad", "+card:hub-island", "+card:flow-goal-3d"]
author: opus
date: 2026-11-09
---

# Pipe Push Paradise — Sokoban, де ящики — це труби у 3D: перекочуй, вертай і складай їх, щоб зʼєднати вхід води з виходом

## Суть
Острів без води: гравець ходить між окремими «протіканнями» й у кожному мусить скласти з труб звʼязний трубопровід від входу (inlet) до виходу (outlet). Труби — тривимірні: прямі й коліна, які від поштовху **перекочуються** через ребро, змінюючи орієнтацію (щоб перевернути, треба два поштовхи), або просто зсуваються. Далі додаються **ротатори** (підіймають трубу й повертають на 90° довкола вертикалі), **ями**, у які труба провалюється, **магнітні труби**, що зчіплюються кінцями, і стекування труб, бо входи бувають над головою. Типова для Sokoban пастка: заштовхнув не так — пазл нерозвʼязний, лише undo/reset.

## Поле і час
- Квадратна сітка з висотою: острів — набір окремих ділянок-пазлів у ізометричному вигляді; труби займають клітини й можуть лежати одна на одній (`field: 3d`).
- Хід = крок гравця з можливим поштовхом; без вводу нічого не рухається (`time: turn`).
- Острів — хаб: можна вільно ходити між пазлами; завершення відкриває нові зони, фінальний рівень Apogee — після всіх інших.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (дівчина-сантехнік) | player | — | рух 4 напрямки; штовхає трубу перед собою |
| Пряма труба | object | орієнтація в 3D, довжина (?) | від поштовху перекочується або ковзає на клітину |
| Коліно (curved) | object | орієнтація в 3D | так само; часто треба перевернути на 180° — два поштовхи |
| Магнітна труба | object | орієнтація | кінці, що зустрілись, зчіплюються; зчеплене рухається разом і «дивно» |
| Inlet (вхід води) | source | висота, напрям | початок трубопроводу; буває над головою |
| Outlet (вихід / протікання) | sink | висота, напрям | кінець трубопроводу |
| Ротатор | terrain | — | підіймає трубу, що на ньому, і повертає на 90° довкола вертикалі |
| Яма (ditch / hole) | terrain | — | труба, заштовхнута сюди, провалюється вниз |
| Земля, стіни, обриви | static | висота | обмежують, куди можна ходити й штовхати |
| Жителі острова | neutral | — | дають контекст/підказки (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, pipe)` → ЯКЩО `free(cell_behind)` and `custom: «орієнтація труби дозволяє перекинутись через ребро в напрямку поштовху»` → ТО `rotate(pipe, 90)`, `move(pipe, dir)` (перекочування).
- КОЛИ `contact(player, pipe)` → ЯКЩО `free(cell_behind)` and not `custom: «перекидання можливе»` → ТО `push` (ковзання без зміни орієнтації) (?).
- КОЛИ `contact(player, pipe)` → ЯКЩО not `free(cell_behind)` → ТО `block`.
- КОЛИ `enter(pipe, rotator)` → ТО `custom: «підняти трубу»`, `rotate(pipe, 90)` довкола вертикальної осі; якщо під піднятою трубою щось опинилось — труба лишається на висоті.
- КОЛИ `enter(pipe, hole)` → ТО `fall(pipe)`; труба в ямі може продовжити трубопровід над прірвою (?).
- КОЛИ `custom: «труба заштовхнута на іншу трубу/підставку»` → ЯКЩО `supported(pipe)` → ТО `custom: «лежить на висоті +1»` (стекування до inlet над головою).
- КОЛИ `adjacent(magnet_pipe_end, pipe_end)` → ТО `attach(a, b)`.
- КОЛИ `turn_end` → ЯКЩО `connected(inlet, outlet)` → ТО `custom: «вода тече»`, `win` (пазл позначено розвʼязаним).
- КОЛИ `input(undo)` → ТО `custom: «скасувати один хід»`; КОЛИ `input(reset)` → ТО `restart`.
- КОЛИ `counter(solved, =, all_but_final)` → ТО `unlock(apogee)`.
- Перемога (пазлу): безперервний трубопровід від inlet до outlet. · Поразка: нема; нерозвʼязна позиція → undo/reset. · Рахунок: нема.

## Керування і ввід
- Клавіатура або геймпад: стрілки/стік/D-pad — крок (поштовх — крок у трубу); на мобільному — свайпи, один свайп може дати кілька кроків.
- Кнопки undo (по одному ходу), redo, reset пазлу.
- Рецензенти скаржаться: героїня рухається швидко, легко «проскочити» зайву клітину — undo постійно.

## Вікна, меню, HUD
- `main-menu` (?): продовжити / налаштування.
- `game-screen`: ізометричний острів; HUD мінімальний — кнопки undo/redo/reset (на тачі).
- `map-window` / хаб: сам острів, по якому ходиш між пазлами; позначки складності Easy / Medium / Hard / Expert (?).
- `settings-window`: звук, керування (?).
- `achievements-window` — Steam-досягнення.
- Переходи: хаб → зайти в зону пазлу → розвʼязано (вода тече) → хаб, відкриваються нові ділянки.

## Фічі поза полем
- `undo` по одному ходу + `redo` + `restart-level`.
- Відкритий острів-хаб (`world-map`-подібна прогресія без окремої карти), `level-unlock`: нові зони після розвʼязання, фінал Apogee — після всіх.
- Позначки складності пазлів; додатковий набір рівнів в оновленні 1.2.0.
- Steam: досягнення, хмарні збереження; повна підтримка геймпада.

## Варіації й родичі
- Автор Corey Martin пізніше зробив [Bonfire Peaks](../thinky/bonfire-peaks.md) (видавець Draknek) — та сама лінія «3D-обʼєкти перекочуються від поштовху».
- Родичі: [sokoban](sokoban.md); Stephen's Sausage Roll (перекочування, висоти); [bloxorz](bloxorz.md) (перекидання бруска через ребро); Pipe Mania / Net (зʼєднання портів, але плитки обертаються кліком, не поштовхом).
- Осі варіацій:
  - **що робить поштовх з обʼєктом**: зсув (Sokoban) / перекочування зі зміною орієнтації (PPP, Bloxorz, Sausage Roll) / обертання на місці (Kwirk);
  - **мета**: ящики на цілях / звʼязний граф портів (PPP);
  - **висота**: пласка сітка / стекування й ями;
  - **зчеплення**: нема / магнітні кінці (PPP) / злипання (Sokobond).

## Цікавинки для курсу
- Орієнтація труби в 3D як (вісь, порти) і перекочування через ребро: таблиця «стан × напрямок → новий стан» — 🥈.
- Перевірка трубопроводу: BFS від inlet по суміжних портах з урахуванням висоти — 🥉.
- Ротатор: поворот обʼєкта з портами на 90° довкола вертикалі (перестановка напрямків портів) — 📎.
- Магнітні труби: група, що рухається разом після зчеплення, перевірка вільності для всієї групи — 🥈.
- Undo як стек станів (дешево, бо стан малий) — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object`; `orientation-state` ↔ перекочування; `height-levels` ↔ стек і ями; `pipe-connectors` ↔ порти труб; `connectivity-check` ↔ inlet→outlet; `stick-together` ↔ магнітні труби; `fill-hole` ↔ труба в ямі (?); `completion-detection`; `unsolvable-states` ↔ глухі кути; `undo-redo` + `undo-step` + `redo` + `restart-level`; `level-unlock` ↔ нові зони й Apogee; `difficulty-levels` ↔ Easy–Expert; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+rotator-pad` «Клітина-ротатор повертає обʼєкт на собі на 90° довкола вертикалі» · entities/interact · 📎.
  - `+hub-island` «Відкритий світ-хаб замість меню рівнів: ходиш між пазлами» · levels/progression · 🥉.
  - `+flow-goal-3d` «Мета — звʼязний трубопровід у 3D від джерела до стоку» · game-logic/win · 🥉.

## Пропозиції до словників
- `+effect:lift` — підняти обʼєкт на висоту +1 (ротатор, стекування).
- `+effect:tip_over` — перекинути обʼєкт через ребро в напрямку руху (зміна орієнтації + зсув); зараз — `rotate` + `move`.
- `+cond:ports_aligned` — порти двох сусідніх труб дивляться один на одного (база `connected`).
- `+role:rotator` — плитка-механізм, що змінює орієнтацію обʼєкта на ній.
- `+feature:hub-world` — прогресія через вільний світ, а не список рівнів.
- `+card:rotator-pad`, `+card:hub-island`, `+card:flow-goal-3d`.

## Джерела
- ⭐ [Electron Dance](https://www.electrondance.com/?p=13960) — inlet→outlet, перекочування (2 поштовхи на перевертання) або ковзання, ротатори, ями, магнітні труби, зони, Apogee, undo на один хід.
- [Steam](https://store.steampowered.com/app/721390/Pipe_Push_Paradise/) — автори, дата, «push, flip and roll pipes», open world, досягнення, хмара, геймпад.
- [Офіційний сайт](https://pipepushparadise.com/), [itch.io](https://coreymartin.itch.io/pipe-push-paradise) — опис, вводи, devlog 1.2.0.
- [TheXboxHub](https://www.thexboxhub.com/pipe-push-paradise-review/) — 47 пазлів, складності, острів-хаб, ротатори, ями, стекування, undo/redo/reset.
- YouTube: пошук «Pipe Push Paradise gameplay».

## Непевне
- (?) Точне правило «перекочується чи ковзає»: Electron Dance каже, що можна й ковзати замість перекочування — від чого це залежить (форма, напрям, висота), не перевірено.
- (?) Кількість пазлів: 47 (TheXboxHub) / 50 (інший огляд) / «dozens» (Steam).
- (?) Що стається з трубою в ямі (стає мостом, лишається частиною трубопроводу) — огляди кажуть лише «ями поглинають труби».
- (?) Довжини прямих труб, наявність T-трійників; чи є головне меню й окремі налаштування; роль жителів.
- (?) Платформи консолей/iOS — з огляду пошуку, сторінки магазинів не відкривав.
