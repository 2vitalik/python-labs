---
title: Desperatea
slug: desperatea
aka: [desperatea classic]
family: push-slide
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [web (itch.io, HTML5), Android, PC (Steam, анонс на 2027)]
links:
  - {kind: itch, url: "https://kr0tyara.itch.io/desperatea", best: true, note: "desperatea classic — грати в браузері; керування (стрілки/WASD/свайпи, H — підказка, Z/Y — undo/redo, R — рестарт), девлоги, коментарі"}
  - {kind: steam, url: "https://store.steampowered.com/app/5277890/Desperatea/", note: "повна версія (анонс, 2027): 60+ рівнів, ланцюгові реакції, щури Monty і Bill; 6 знімків"}
  - {kind: other, url: "https://kr0tyara.itch.io/desperatea/devlog/808317/mobile-support", note: "девлог: «чайний сервіз слухається тебе», свайпи, цукор, що тане"}
  - {kind: other, url: "https://kr0tyara.itch.io/desperatea/devlog/1672126/wishlist-desperatea-on-steam", note: "девлог: classic → повна гра з новими зонами й механіками"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.kr0tyara.desperatea", note: "Google Play (безкоштовно, без реклами)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Desperatea+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, move-4dir, push-object, impassable-cells, all-on-targets, environment-death, carrier-platform, undo-redo, redo, restart-level, move-counter, sequential-levels, level-select, level-unlock, save-progress, keyboard-controls, swipe-gestures, main-menu, settings-window, confirm-dialog, about-window, game-screen, language-picker, volume-control, movement-animation, +broadcast-move, +control-by-state, +pour-into-vessel, +pour-through-chain, +axis-locked-move, +target-locks-piece, +dissolve-block, +npc-tips]
proposes: ["+effect:pour", "+effect:melt", "+ui:speech-bubble", "+feature:flush-progress", "+card:control-by-state", "+card:pour-into-vessel", "+card:pour-through-chain", "+card:target-locks-piece", "+card:dissolve-block", "+card:npc-tips"]
author: opus
date: 2026-11-19
---

# Desperatea — «соко-бан» з чаєм: усе, у чому є чай, рухається разом, а чайник розливає чай гостям на тарілки

## Суть
Гравець керує не героєм, а **«вуликом» чайного сервізу**: один ввід зсуває одразу всі посудини, у яких є чай (крім сонних склянок). Чайник, упершись у порожню посудину, наливає в неї чай — і вона приєднується до вулика; закінчився чай — чайник більше не слухається. Мета — на кожній тарілці має стояти посудина з чаєм; посудина на тарілці завмирає й стає стіною.

Безкоштовна desperatea classic (itch.io, травень 2024; Google Play — вересень 2025) має 27 названих рівнів (частина, можливо, секретні (?)). Повна версія в Steam (2027) обіцяє 60+ рівнів, нові зони й механіки та щурів Monty і Bill.

## Поле і час
- Квадратна сітка: кілька столів-скатертин (кольорові клітини) з проміжками підлоги між ними; стін у частині рівнів нема («There are no walls here…»).
- Хід = один крок вулика; без вводу нічого не рухається («Playable without Timed Input»).
- Шари: стіл (клітини, на які можна ставати) · тарілки на столі · посудини й предмети · порожнеча за краєм столу.
- Персонажі-посудини говорять бульбашками: підказка рівня з'являється за H.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чайник | piece | запас чаю; кришка запаяна | рухається з вуликом, доки має чай; упершись у посудину — наливає; порожнім не слухається, його можна штовхати; назад у нього не наллєш |
| Чашка (рожева, одне око) | piece | порожня / з чаєм | з чаєм — у вулику; порожню можна штовхнути |
| Склянка (сонне обличчя) | object | порожня / з чаєм | сама не ходить навіть із чаєм; налиту можна штовхати |
| Миска (два ока) | piece | — | склянки й миски штовхають одна одну |
| Посудина «лише вертикально» / «лише горизонтально» | piece | вісь | з чаєм ходить тільки вздовж своєї осі; штовхнути можна будь-куди (?) |
| Тарілка | zone | порожня / з посудиною | ціль; посудина з чаєм на ній завмирає, працює як стіна; крізь неї можна лити чай |
| Цукор (кубик) | object | цілий / розтанув | перешкода; чай, налитий на нього, його розтоплює |
| Щур із тацею | neutral | — | «Hop onto my tray!» — везе посудину на таці (?) |
| Край столу | hazard | — | посудина за краєм падає й розбивається (?) |
| Стіна | static | — | є не в усіх рівнях; блокує |
| Портал | terrain | пара (?) | є в коді гри (`Portal`); правило — (?) |
| Келих з оком, соусник, фруктова гірка, крижаний кубик з усмішкою | object | — | лише на знімках повної версії; правила — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(vessel, has_tea)` і `not state(vessel, on_plate)` → ТО `move(vessel, dir)` — для всіх таких посудин одночасно, крім склянок.
- КОЛИ `input(dir)` → ЯКЩО `custom: «dir поперек осі посудини»` → ТО `block` для цієї посудини (вертикальна / горизонтальна).
- КОЛИ `contact(teapot, vessel)` → ЯКЩО `state(vessel, empty)` → ТО `custom: «налити чай»`, `counter(teapot_tea, -1)`, `set_state(vessel, has_tea)`.
- КОЛИ `contact(teapot, vessel)` → ЯКЩО `state(vessel, full)` → ТО `custom: «чай іде крізь повну посудину до порожньої за нею»` (?) — ланцюг «доміно».
- КОЛИ `counter(teapot_tea, ==, 0)` → ТО `clear_state(teapot, controlled)` — порожній чайник штовхається, як предмет.
- КОЛИ `contact(vessel, other)` → ЯКЩО `state(other, empty)` і `free(cell_behind)` → ТО `push` (?).
- КОЛИ `contact(vessel, glass)` → ЯКЩО `state(glass, has_tea)` і `free(cell_behind)` → ТО `push`.
- КОЛИ `enter(vessel, plate)` → ЯКЩО `state(vessel, has_tea)` → ТО `set_state(vessel, on_plate)` — більше не рухається з вуликом.
- КОЛИ `custom: «чай налито на цукор»` → ТО `disappear_b` (тане).
- КОЛИ `edge(vessel)` → ТО `custom: «падає зі столу й розбивається»` (?).
- КОЛИ `enter(vessel, tray)` → ТО `carry(rat, vessel)` (?).
- КОЛИ `custom: «на кожній тарілці — посудина з чаєм»` → ТО `win`, `next_level`.
- КОЛИ `input(hint)` → ТО `message(tip)` — репліка персонажа («Push me against a vessel to pour tea into it»).
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(redo)` → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(restart)` → ТО `restart`.
- КОЛИ `counter(levels_done, >=, n)` → ТО `unlock(hall)`, `message("Hall {Zone} unlocked!")`.
- Перемога: на всіх тарілках — посудини з чаєм. · Поразка: формально нема; розбита посудина чи порожній чайник — глухий кут → undo / рестарт (?). · Рахунок: нема; лічильник кроків — опція.

## Керування і ввід
- Стрілки / WASD — крок вулика; свайпи на телефоні (з жовтня 2024); утримання напрямку повторює крок (`HoldDirection` у коді) (?).
- H — підказка-репліка; Z — undo; Y — redo; R — рестарт; ті самі кнопки на екрані.
- Повна версія в Steam: окремо лише клавіатура, лише миша, лише дотик (категорії Steam).

## Вікна, меню, HUD
- `splash-screen`: власний екран завантаження замість стандартного Unity.
- `main-menu`: Play · Settings · Credits.
- `level-select`: зали з рівнями; закритий зал пише «Complete N more levels to unlock»; відкриття — «Hall N unlocked!».
- `game-screen`: столи на тлі; HUD — `restart-button` (R), `undo-button` (Z), `redo-button` (Y), `pause-button`; бульбашки реплік (+ui `speech-bubble`); `move-counter` — якщо ввімкнено.
- `settings-window`: гучність музики й звуків, мова EN/RU, «Display steps counter», «Flush progress» → `confirm-dialog` «Are you sure?».
- `about-window`: Credits — автор, плейтестери, звуки, музика.
- `end-screen`: «All levels completed! Thank you for playing!».
- Переходи: меню → зал → рівень → (усі тарілки) наступний рівень → … → фінальний екран.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: зали відкриваються за кількістю пройдених рівнів; у коді є «секретні рівні» (?).
- `undo` + `redo` + `restart-level`; `hint` — смішні репліки, «здебільшого марні, але з характером» (опис itch).
- Налаштування: гучність, мова, лічильник кроків, скидання прогресу (`+feature:flush-progress`).
- Платформи: браузер (itch, 2024), Android (Google Play, 2025), Steam — повна версія з новими зонами й механіками (2027).

## Варіації й родичі
- [A Directionless Cycle](a-directionless-cycle.md) — один ввід рухає всі фігури, що реагують на нього; тут реагують ті, у кого є чай.
- [Block in the Lock](block-in-the-lock.md), [Singleton Traffic](singleton-traffic.md) — «вулик» плиток під одним вводом.
- [Nekograms](nekograms.md) — фігури, що ходять лише вздовж своєї осі.
- [Delicious Donut](delicious-donut.md) — острівці-столи, з яких не можна впустити.
- [Sokoban](sokoban.md) — посудини на тарілки як ящики на цілі («soak-oban»).
- Осі варіацій:
  - **хто під керуванням**: один аватар / усі однакові / усі зі станом «є чай» (змінюється під час гри);
  - **як предмет стає керованим**: ніколи / коли в нього налили;
  - **ціль**: стати на мітку / стати на мітку з потрібним станом (посудина з чаєм).

## Цікавинки для курсу
- Вулик за станом: множина керованих сутностей = всі з `has_tea`; поповнюється наливанням, зменшується на тарілках — 🥉.
- Одночасний крок кількох сутностей з перевіркою колізій між собою (хто кого штовхає, хто впирається) — 🥉.
- Наливання крізь повну посудину до першої порожньої (ланцюг) — 📎.
- Посудина на тарілці стає стіною — «ціль, що змінює поле» — 🌱.
- Цукор тане від чаю: перешкода, яку прибирає дія, а не поштовх — 🌱.
- Undo/redo як стек знімків стану всіх посудин і запасу чаю — 📎.
- Розвʼязувач BFS: стан = позиції + чай у кожній посудині + запас чайника — 🥇.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` ↔ крок вулика; `push-object` ↔ штовхання склянок і порожніх; `impassable-cells` ↔ стіни; `all-on-targets` ↔ посудини з чаєм на тарілках; `environment-death` ↔ падіння зі столу (?); `carrier-platform` ↔ щур із тацею (?); `undo-redo` + `redo` + `restart-level` ↔ Z / Y / R; `move-counter` ↔ лічильник кроків; `sequential-levels` + `level-select` + `level-unlock` + `save-progress` ↔ зали; `keyboard-controls` + `swipe-gestures`; `main-menu`, `settings-window`, `confirm-dialog`, `about-window`, `game-screen`, `language-picker`, `volume-control`, `movement-animation`.
- **Нема** → пропозиції карток:
  - `+broadcast-move`, `+axis-locked-move` — уже в корпусі.
  - `+control-by-state` «Під керуванням усі сутності з певним станом; стан змінюється — змінюється й набір» · entities/move · 🥉 · слот {state: has_tea}.
  - `+pour-into-vessel` «Наливання: аватар віддає рідину сусідній посудині, витрачаючи запас» · entities/interact · 📎 · слот {supply: n}.
  - `+pour-through-chain` «Рідина проходить крізь повні посудини до першої порожньої в ряду» · entities/interact · 📎.
  - `+target-locks-piece` «Фігура на цілі завмирає й стає стіною» · game-logic/win · 🌱.
  - `+dissolve-block` «Перешкода зникає від рідини» · entities/interact · 🌱.
  - `+npc-tips` «Підказка рівня — репліка персонажа за кнопкою» · interface/hud · 🌱.

## Пропозиції до словників
- `+effect:pour` — налити рідину з однієї посудини в сусідню (зменшує запас джерела).
- `+effect:melt` — перешкода тане від рідини (цукор від чаю).
- `+ui:speech-bubble` — бульбашка репліки над персонажем на полі.
- `+feature:flush-progress` — скинути весь прогрес із підтвердженням.
- `+card:control-by-state`, `+card:pour-into-vessel`, `+card:pour-through-chain`, `+card:target-locks-piece`, `+card:dissolve-block`, `+card:npc-tips` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch.io: desperatea classic](https://kr0tyara.itch.io/desperatea) — гра в браузері, керування, коментарі (рівні 25–26 найважчі), девлоги; з веб-збірки прочитано англійські рядки гри: 27 назв рівнів, підказки персонажів (правила чайника, склянок, тарілок, цукру, осьових посудин, щура з тацею), меню й налаштування.
- [Steam: Desperatea](https://store.steampowered.com/app/5277890/Desperatea/) — повна версія: 60+ рівнів, ланцюгові реакції, Monty і Bill; категорії вводу; 6 знімків (кнопки R / Z / Y, нові посудини).
- [Девлог: mobile support](https://kr0tyara.itch.io/desperatea/devlog/808317/mobile-support) — сервіз, що слухається, свайпи, баг із танучим цукром.
- [Девлог: wishlist on Steam](https://kr0tyara.itch.io/desperatea/devlog/1672126/wishlist-desperatea-on-steam) — classic і повна версія.
- [Google Play](https://play.google.com/store/apps/details?id=com.kr0tyara.desperatea) — мобільна версія (сторінка у фетчі порожня).
- YouTube: пошук «Desperatea gameplay».

## Непевне
- (?) Що відбувається з порожньою посудиною, коли в неї впирається налита чашка (а не чайник): поштовх чи наливання; чи наливають чашки.
- (?) Точне правило «доміно»: чи тече чай крізь кілька повних посудин і крізь посудини на тарілках у будь-якому напрямку.
- (?) Чи падіння за край столу — програш, чи посудина просто зникає; чи є стіни-краї в усіх залах.
- (?) Як працює щур із тацею, портал і `TimeLock` (назви з коду гри); що вміють нові предмети повної версії.
- (?) Мета формулюється як «посудина з чаєм на кожній тарілці» — зі слів тарілок у підказках; «гості» з опису Steam — ймовірно, тарілки.
- (?) Рік: classic — травень 2024 (перші коментарі на itch); повна версія в Steam — 2027 за сторінкою.
