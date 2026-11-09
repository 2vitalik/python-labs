---
title: Stoneman's Adventure
slug: stonemans-adventure
aka: [小石头人踏上旅程, "Stoneman's Adventure (Prototype)"]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC, Mac, Linux, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2434860/", best: true, note: "опис: сокобан + малювання одним розчерком; «Generate stones, push stones, build shapes!»; оверворлд, демо"}
  - {kind: itch, url: "https://akacmd.itch.io/stoneman-adventure", note: "повна гра (Unity), web-збірка, девлоги 2022–2025"}
  - {kind: play, url: "https://akacmd.itch.io/stonemans-adventure", note: "прототип 2021 на PuzzleScript: 15 рівнів, повні правила в коді сторінки"}
  - {kind: other, url: "https://steamcommunity.com/app/2434860/reviews/?browsefilter=toprated&l=english", note: "відгуки: attach/break, досягнення «без каменів», збереження оверворлду при вході в рівень"}
  - {kind: other, url: "https://akacmd.itch.io/stoneman-adventure/devlog/481795/update-log-2023127", note: "девлог: undo після GameOver, «pedometer», помаранчевий слайм"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Stoneman%27s+Adventure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, push-object, stick-together, impassable-cells, fill-hole, cell-transform, button-toggle, touch-death, environment-death, chase-player, undo-redo, restart-level, +open-world-puzzles, achievements-window, save-progress, +trail-to-objects, +form-swap-pad, +crumbling-floor, +row-column-chase, +blockable-leap, +multi-agent-sync, +per-character-hazard, +no-trail-challenge]
proposes: ["+effect:leave_trail", "+trigger:aligned", "+role:transform-pad", "+card:trail-to-objects", "+card:form-swap-pad", "+card:row-column-chase", "+card:per-character-hazard"]
author: opus
date: 2026-11-09
---

# Stoneman's Adventure — кам'яний чоловічок лишає за собою ряд каменів, а людина штовхає їх цілими зліпками

## Суть
«Сокобан + малювання одним розчерком»: Кам'яний чоловічок за кожним кроком лишає камінь у клітині, з якої пішов, — шлях стає ланцюгом каменів, і самого себе він перетнути не може. Друга форма героя — людина: вона не творить каміння, а штовхає його, причому камені, що торкаються ребрами, злиплись і рухаються одним жорстким тілом. Перемикання форм — на спеціальних клітинах; камені засипають воду, ламкий ґрунт за спиною провалюється, гобліни кидаються по прямій. Повна гра (3D-воксельний острів з оверворлдом) виросла з PuzzleScript-прототипу 2021 р., правила якого відкриті.

## Поле і час
- Квадратна сітка; повна гра — 3D-воксельний вигляд згори (Steam-теги Voxel, Top-Down, Grid-Based Movement), острів-оверворлд, що звʼязує рівні.
- Покроково: один ввід — один крок; вороги ходять у тому ж тіку.
- Клітина має шари (з коду прототипу): підлога (ламкий ґрунт, шипи) · кнопка/мокрий камінь · камінь/вороги · ціль · вода/стіна/двері/герой. Камінь і герой — у різних шарах, але стояти разом не можуть (хід скасовується).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кам'яний чоловічок | player | форма = stoneman | крок у вільну клітину → у покинутій лишається камінь; у камінь не входить, не штовхає; шипи не шкодять |
| Людина (Operator) | player | форма = human | штовхає камені; на шипах гине |
| Клітина перемикання | terrain | — | стати → stoneman ↔ людина |
| Камінь | object | злипається | штовхається людиною; уся звʼязна по ребрах група рухається разом |
| Мокрий камінь | terrain | — | камінь у воді → прохідна підлога (міст) |
| Вода | static | — | непрохідна для героя й гоблінів; камінь її засипає |
| Ламкий ґрунт | terrain | — | хто з нього зійшов (герой чи камінь) — клітина стає водою |
| Стіна | static | — | непрохідна; зупиняє групу каменів |
| Шипи | hazard | — | убивають людину; чоловічок проходить |
| Кнопка | switch | — | камінь або герой на ній → усі двері відчинені; зійшли — зачинені |
| Двері | gate | open / closed | зачинені — як стіна для героя й каменів |
| Ціль | static | — | усі герої мають стояти на цілях |
| Гоблін | enemy | — | гравець у тому ж рядку/стовпці → крок до нього; у воду не входить; дотик — смерть |
| Гоблін-привид | enemy | досяжність 4 кл. | гравець на прямій без перешкод → стрибок у його клітину, смерть |
| Помаранчевий слайм | enemy | — | лише у повній грі; механіка «плутана» (девлог) (?) |
| Качки | pickup | — | приховані колекційні (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(player, stoneman)` and `free(cell_ahead)` → ТО `move(player, dir)`, `spawn(stone, prev_cell)`.
- КОЛИ `contact(stoneman, stone)` → ТО `block` — шлях не перетинає сам себе (одним розчерком).
- КОЛИ `contact(human, stone)` → ЯКЩО `custom: «уся звʼязна група каменів має куди зсунутись»` → ТО `push(stone_group)`; інакше `block`.
- КОЛИ `after(push(stone))` → ЯКЩО `connected(stone)` → ТО `custom: «сусідні по ребру камені рухаються разом як одне тіло»`.
- КОЛИ `custom: «камінь опинився б на герої, стіні або дверях»` → ТО `block` (увесь хід скасовано).
- КОЛИ `enter(stone, water)` → ТО `transform(stone, wet_stone)` — клітина стає прохідною.
- КОЛИ `leave(player|stone, broken_ground)` → ТО `set_cell(broken_ground, water)`.
- КОЛИ `enter(player, shift_point)` → ТО `transform(stoneman, human)` або `transform(human, stoneman)`.
- КОЛИ `enter(human, spike)` → ТО `disappear(human)`; КОЛИ `enter(stoneman, spike)` → ТО нічого.
- КОЛИ `enter(stone|player, button)` → ТО `set_state(doors, open)`; КОЛИ `leave(stone|player, button)` → ТО `clear_state(doors, open)`.
- КОЛИ `custom: «гравець у тому ж рядку чи стовпці, що й гоблін»` → ТО `move(goblin, toward_player)`; ЯКЩО `cell(ahead, water)` → ТО `block`.
- КОЛИ `in_range(ghost, player, 4)` → ЯКЩО `custom: «на прямій між ними лише вільні клітини»` → ТО `teleport(ghost, player_cell)`.
- КОЛИ `contact(goblin|ghost, player)` → ТО `disappear(player)`.
- КОЛИ `enter(goblin|ghost, water)` → ТО `disappear(goblin)` (?).
- КОЛИ `input(dir)` → ЯКЩО `count(player, >, 1)` → ТО `custom: «усі герої рухаються одночасно, кожен за своєю формою»` (рівень «Imitation»).
- КОЛИ `all_on(player, target)` → ТО `win`, `next_level`.
- КОЛИ `count(player, ==, 0)` → ТО `lose` → undo або рестарт (у повній грі undo працює й після GameOver).
- Перемога: усі герої на цілях. Поразка: загибель героя. Рахунку нема; є досягнення за фінальний рівень без жодного каменя.

## Керування і ввід
- Стрілки/WASD — крок; прототип PuzzleScript: Z — undo, R — рестарт.
- Повна гра: клавіатура й миша (рекомендовано), будь-який геймпад (itch); `reset` зони в оверворлді (девлог про патч).
- Форма героя змінюється лише клітинами перемикання (у прототипі опис: «You can switch between two characters»).

## Вікна, меню, HUD
- `game-screen`: воксельне поле рівня згори; опція сітки (девлог 2022: налаштування сітки не зберігалось).
- Оверворлд — острів, яким ходять між рівнями (`map-window` не окремий: світ і є меню) (?).
- `settings-window`: сітка, звук (?); UI оновлено в лютому 2024.
- `achievements-window` (Steam Achievements); «pedometer» — тригер досягнення за кроки (?).
- Переходи: оверворлд → вхід у рівень (тут зберігається прогрес) → ціль → оверворлд.

## Фічі поза полем
- `undo`, `restart-level`, скидання зони оверворлду.
- `world-map` у вигляді відкритого острова (`open-world-puzzles`); пройти всі рівні набору не обовʼязково, щоб іти далі (відгук).
- `autosave` при вході в рівень (за відгуком — забудеш увійти, втратиш хід оверворлду).
- `achievements` (зокрема «без каменів»), `cloud-save`, `localization` (EN, 简体).

## Варіації й родичі
- Прототип 2021 (PuzzleScript, 15 рівнів: гобліни, привиди, ламкий ґрунт, шипи, двері) → повна гра 2023 (3D, оверворлд, attach/break, слайм, качки). Третє місце «Best Game» CUSGA 2022 (itch, китайською).
- Родичі: [Sokobond](sokobond.md) (злипання), [A Monster's Expedition](a-monsters-expedition.md) (острів-оверворлд), [Snakebird](snakebird.md) (тіло як шлях), Tron-подібні `trail-wall` (слід як стіна).
- **Осі варіацій**: слід героя — нічого / стіна / рухомі обʼєкти (тут) · злипання — нема / за кольором / усі сусіди · форми героя — одна / дві з перемиканням на клітині / одночасні копії.

## Цікавинки для курсу
- Слід як камені: `spawn(stone, prev_cell)` на кожен крок + заборона входу в камінь — 🌱.
- Жорстке штовхання звʼязної групи: flood fill групи, перевірка всіх клітин попереду, атомарний зсув — 🥉.
- Ламкий ґрунт і засипання води каменем — 📎 (дві трансформації клітини).
- Дві форми героя з різними правилами (хто творить, хто штовхає, кому шкодять шипи) — 📎.
- Гоблін «бачить» уздовж усього рядка/стовпця, привид стрибає до 4 клітин — 📎.
- Розвʼязувач з умовою «не створити жодного каменя» (досягнення) — 🥈.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls` · `push-object` · `stick-together` ↔ злиплі камені · `impassable-cells` · `fill-hole` ↔ камінь у воді · `cell-transform` ↔ ламкий ґрунт → вода · `button-toggle` ↔ кнопка й двері · `touch-death` ↔ гобліни · `environment-death` ↔ шипи · `chase-player` ↔ гоблін · `undo-redo`, `restart-level` · `achievements-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+trail-to-objects` «Слід аватара стає рухомими обʼєктами» · entities/move · 📎.
  - `+form-swap-pad` «Клітина перемикає форму героя з іншими правилами» · entities/state · 📎.
  - `+row-column-chase` «Ворог рушає, коли гравець у тому ж рядку/стовпці» · entities/move · 🌱.
  - `+per-character-hazard` «Пастка шкодить лише одній формі» · entities/death · 🌱.
  - `+open-world-puzzles`, `+crumbling-floor`, `+blockable-leap`, `+multi-agent-sync` — є в інших файлах корпусу; `+no-trail-challenge` — досягнення «без каменів».

## Пропозиції до словників
- `+effect:leave_trail` — у покинутій клітині лишається сутність (підтверджую; у `vocab/` ще нема).
- `+trigger:aligned` — сутності в одному рядку чи стовпці, без огляду на перешкоди.
- `+role:transform-pad` — клітина, що змінює форму/тип того, хто на неї став.
- `+card:trail-to-objects`, `+card:form-swap-pad`, `+card:row-column-chase`, `+card:per-character-hazard` — див. вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/2434860/) — «unique combination of sokoban and one-line drawing», «Generate stones, push stones, build shapes!», оверворлд, платформи, мови, демо.
- [Прототип на itch (PuzzleScript)](https://akacmd.itch.io/stonemans-adventure) — 15 рівнів; вихідний код гри у сторінці: правила створення й злипання каменів, вода, ламкий ґрунт, шипи, кнопки/двері, гобліни, привиди, умова перемоги.
- [itch, повна гра](https://akacmd.itch.io/stoneman-adventure) — платформи, ввід (клавіатура, миша, геймпад), CUSGA 2022, хронологія девлогів.
- [Відгуки Steam](https://steamcommunity.com/app/2434860/reviews/?browsefilter=toprated&l=english) — attach/break, досягнення без каменів, збереження при вході в рівень, нелінійний прогрес.
- [Девлог 2023/1/27](https://akacmd.itch.io/stoneman-adventure/devlog/481795/update-log-2023127) — undo після GameOver, «pedometer», помаранчевий слайм.
- YouTube: пошук «Stoneman's Adventure gameplay».

## Непевне
- Правила вище — з коду прототипу 2021; повна 3D-гра їх розвиває, але точні відмінності не задокументовані.
- (?) Що таке «attach/break» у повній грі: ручне розʼєднання злиплих каменів чи окремі «липкі» камені (у прототипі злипаються всі).
- (?) Помаранчевий слайм, качки, «дірки» (з опису в агрегаторі), «pedometer» — механіки повної гри без опису.
- (?) Чи гоблін тоне, якщо вода зʼявилась під ним (у коді є правило зникнення, але ворог у воду не ходить).
- Розробник: Steam — Minda Chen, itch — TrioDuckk/AkaCMD (той самий автор, різні псевдоніми) (?).
