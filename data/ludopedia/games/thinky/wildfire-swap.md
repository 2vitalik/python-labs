---
title: Wildfire Swap
slug: wildfire-swap
aka: []
family: thinky
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1216030/Wildfire_Swap/", best: true, note: "опис і трейлер: міняти плитки, робити просіки; вогонь не гасиш, кожен хід він шириться; 120+ рівнів, B-side світи"}
  - {kind: official, url: "https://wildfire.fun/presskit", note: "пресскіт: Bejeweled-обмін + Game of Life, прототип LD41, команда, GIF геймплею"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/wildfire-swap-review", note: "рецензія: дерево передає вогонь через хід, трава й сіно — одразу, вітер — через 1 порожню; undo без ліміту, reset, мапа світів, B-sides"}
  - {kind: other, url: "https://www.gamesxtreme.com/game/wildfire-swap", note: "обмін двох сусідніх плиток за хід, після кожного обміну всі вогні ширяться"}
  - {kind: other, url: "https://buried-treasure.org/?p=3729", note: "огляд: трава горить миттєвими ланцюгами, порожня земля — просіка"}
  - {kind: itch, url: "https://rmkubik.itch.io/wildfire-jam", note: "прототип Ludum Dare 41: «Game of Life + обмін плиток», врятувати якомога більше будинків"}
  - {kind: itch, url: "https://rmkubik.itch.io/wildfire-swap-development", note: "девлог 2020: вітряки й попіл, світи 2–4, inferno mode, challenge world"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Wildfire+Swap+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, selection-highlight, chain-reaction, reachability-check, completion-detection, undo-redo, undo-unlimited, restart-level, world-map, level-unlock, level-select, music-toggle, +fire-spread, +adjacent-swap, +move-burning-tile, +spread-delay-by-type, +wind-carry, +burn-out, +firebreak-win, +protect-houses, +b-side-worlds, +hidden-levels, +alternative-path-levels]
proposes: ["+effect:spread", "+cond:flammable", "+feature:b-side-worlds", "+card:fire-spread", "+card:adjacent-swap"]
author: opus
date: 2026-11-09
---

# Wildfire Swap — міняєш місцями сусідні плитки лісу, трави й будинків, а після кожного обміну пожежа шириться далі: збудуй просіку, поки вогонь не дійшов до домів

## Суть
Покрокова головоломка Ryan Kubik, Drew Gingerich, Wes Mueller: на маленькому острові-сітці горить ліс, гасити вогонь не можна — тільки **переставляти плитки**. За хід гравець міняє місцями дві сусідні плитки (будинок, дерево, траву, порожню землю, навіть палаючу), після чого **всі вогні ширяться** на горючих сусідів. Мета — розірвати горючі звʼязки так, щоб вогню стало нікуди йти, а будинки лишились цілі. Ядро — «Bejeweled-обмін + клітинний автомат вогню» (пресскіт).

## Поле і час
- Квадратна сітка-острів довільної форми (у рецензії — поля близько 8×4), окремі «острівці» з розривами; поза плитками — небо/порожнеча.
- Хід = один обмін гравця → фаза вогню (`time: turn`); без обміну вогонь стоїть.
- Шари: плитка-основа (пісок/земля/трава) · обʼєкт на ній (дерево, сіно, будинок) · стан «горить» · вітер над рядом/стовпцем.
- Поширення — на ортогональних сусідів (у GIF вогонь не стрибає по діагоналі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дерево (ліс) | tile | горить / ні | горюче; запалене, передає вогонь сусідам лише наступного ходу |
| Трава | tile | — | горюча; спалахує й одразу (того ж ходу) запалює горючих сусідів — ланцюг; швидко вигорає |
| Сіно | tile | — | як трава: миттєвий ланцюг |
| Будинок | object | — | те, що рятуємо; можна переставляти обміном; загорівся — поразка (?) |
| Порожня земля / пісок | terrain | — | не горить — матеріал просіки |
| Вогонь (палаюча плитка) | hazard | вік горіння | щоходу підпалює горючих сусідів; палаючу плитку теж можна обміняти |
| Вітер | zone | напрям | у пізнішому світі: вогонь перестрибує 1 порожню клітину за вітром |
| Вітряк | static | напрям вітру (?) | з девлогу: попіл за вітром від вітряка знову спалахує (?) |
| Попіл | terrain | — | вигоріла плитка; може знову зайнятись від вітряка (?) |
| Камінь / гора | static | — | непрохідне тло (на мапі світу й у рівнях) (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile_a)` → ТО `set_state(tile_a, selected)`.
- КОЛИ `input(click tile_b)` → ЯКЩО `state(tile_a, selected)` and `custom: «tile_b — ортогональний сусід tile_a»` → ТО `swap(tile_a, tile_b)`, `end_turn`.
- КОЛИ `turn_end(player)` → ТО `custom: «фаза вогню: усі вогні ширяться одночасно»`.
- КОЛИ `phase_start(fire)` → ЯКЩО `state(tree, burning)` and `custom: «горить з минулого ходу»` → ТО `custom: «підпалити горючих сусідів»` (`+effect:spread`).
- КОЛИ `state_on(grass|hay, burning)` → ТО `custom: «миттєво підпалити горючих сусідів»` (`after` — ланцюг у тому самому ході).
- КОЛИ `state_on(grass, burning)` → ТО `set_cell(grass, ash)` після вигоряння (за 1 хід (?)).
- КОЛИ `phase_start(fire)` → ЯКЩО `custom: «вітер дме від вогню; через одну порожню клітину — горюче»` → ТО `set_state(target, burning)`.
- КОЛИ `phase_start(fire)` → ЯКЩО `custom: «попіл за вітром від вітряка»` → ТО `set_state(ash, burning)` (?).
- КОЛИ `custom: «вогонь дійшов до будинку»` → ТО `lose`, `message("Game Over")` (?).
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «жоден вогонь не має горючого сусіда (нікуди йти)»` and `not path_exists(fire, house)` → ТО `win`, `message("The fire is controlled!")`.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту) · КОЛИ `input(reset)` → ТО `restart`.
- Перемога: вогонь локалізовано, будинки цілі. · Поразка: згорів будинок (?) — далі undo/reset. · Рахунок: нема.

## Керування і ввід
- Лише мишею: клік по плитці виділяє (жовта рамка), клік по сусідній — обмін.
- Кнопки-таблички Reset і Undo під полем; на мапі світу — клік по вузлу рівня.
- Повноекранний режим вмикається руками (відгук).

## Вікна, меню, HUD
- `map-window` / `level-select`: мапа світу з вузлами-рівнями, стежками, замками й горами; назва рівня — підказка до розвʼязку; приховані рівні показують назву після проходження.
- `game-screen`: острів-поле, `undo-button`, `restart-button` (Reset), `selection-highlight`; тло змінює колір за світом.
- `end-screen` (оверлей): «The fire is controlled! Click to return to world.» з феєрверком; повідомлення Game Over (?).
- `settings-window`: вимкнення музики; інше (?).
- Переходи: мапа → рівень → (локалізовано) мапа; B-side світи — окремі гілки мапи.

## Фічі поза полем
- `world-map` з `level-unlock`: на стежках зазвичай два альтернативні пазли — застряг на одному, можна взяти інший.
- П'ять світів (?) з різними середовищами (ліс, трава, вітер…), до кожного — B-side з новою механікою й важчими пазлами; приховані рівні.
- `undo` без ліміту, `restart-level`; `cloud-save` (крос-платформний Steam Cloud); `music-toggle`.

## Варіації й родичі
- Прототип **Wildfire** (Ludum Dare 41, тема «змішати два несумісні жанри»): ті самі обміни, але рівні генерувались випадково й рахувались урятовані будинки.
- Осі варіацій «вогонь як клітинний автомат»: затримка поширення — однакова / за типом (дерево 1 хід, трава миттєво) / ймовірнісна ([forest-fire-model](../build-sim/forest-fire-model.md)); дальність — сусіди / +1 за вітром; дія гравця — обмін плиток (тут) / гасіння агентами (Flash Point) / нічого (модель).
- Родичі: match-3 обмін ([bejeweled](../falling-match/bejeweled.md)) без збігів; [flash-point-fire-rescue](../board-digital/flash-point-fire-rescue.md); у теці — [chomp-garden](chomp-garden.md), [mycelium-heaven](mycelium-heaven.md) (поширення по сітці).

## Цікавинки для курсу
- Обмін двох сусідніх плиток з виділенням кліком — 🌱.
- Поширення вогню з різною затримкою за типом плитки (дерево — наступний хід, трава — ланцюг того ж ходу через чергу BFS) — 📎.
- Вітер: перестрибування однієї порожньої клітини в напрямку — 📎.
- Перевірка перемоги «вогню нікуди йти / до будинків нема шляху» (BFS по горючих) — 📎.
- Undo без ліміту як стек станів поля — 🌱.
- Розвʼязувач: пошук мінімальної послідовності обмінів при динамічному вогні — 🥈.

## Мапа на каталог
- Є: `cell-click` + `selection-highlight` ↔ виділення й обмін; `chain-reaction` ↔ трава горить ланцюгом; `reachability-check` + `completion-detection` ↔ «вогонь локалізовано»; `undo-redo` + `undo-unlimited` + `restart-level` ↔ Undo/Reset; `world-map` + `level-unlock` + `level-select` ↔ мапа світів; `music-toggle`.
- **Нема** → пропозиції карток:
  - `+fire-spread` (є в корпусі) — вогонь щоходу на горючих сусідів.
  - `+adjacent-swap` «Обмін двох сусідніх плиток як хід» · entities/interact · 🌱 (без умови збігу, на відміну від `+match-3-swap`).
  - `+spread-delay-by-type` «Затримка поширення за типом клітини» · entities/state · 📎.
  - `+wind-carry` «Вітер переносить ефект через N порожніх клітин» · 📎.
  - `+move-burning-tile` — палаючу плитку можна переставити; `+burn-out` — вигоряє в попіл.
  - `+firebreak-win` / `+protect-houses` — перемога, коли загроза не має шляху до цілей · 🥉.
  - `+b-side-worlds`, `+hidden-levels`, `+alternative-path-levels` — прогресія мапи.

## Пропозиції до словників
- `+effect:spread` — стан переходить на сусідів за правилом (вогонь, зараза).
- `+cond:flammable` — клітина горюча за типом.
- `+feature:b-side-worlds` — світ-дзеркало з новою механікою й важчими рівнями.
- `+card:fire-spread`, `+card:adjacent-swap`.

## Джерела
- ⭐ [Steam: Wildfire Swap](https://store.steampowered.com/app/1216030/Wildfire_Swap/) — суть, «вогонь не загасити, лише стримати», 120+ рівнів, B-side світи, трейлер і скріншоти (Reset/Undo, трава, вітер, мапа).
- [Пресскіт](https://wildfire.fun/presskit) — Bejeweled + Game of Life, прототип LD41 з випадковими рівнями, команда, GIF геймплею (обмін будинку, палаюче дерево, «The fire is controlled!»).
- [GameGrin](https://www.gamegrin.com/reviews/wildfire-swap-review) — затримки дерева й трави/сіна, вітер через 1 клітину, undo без ліміту, reset, мапа з альтернативними пазлами, B-sides.
- [GamesXtreme](https://www.gamesxtreme.com/game/wildfire-swap) — обмін двох сусідніх плиток, після кожного обміну шириться весь вогонь, перемога = просіка між усіма будинками й вогнем.
- [Buried Treasure](https://buried-treasure.org/?p=3729) — дерево 1 клітина за хід, трава — миттєвий ланцюг, порожня земля — просіка.
- [Wildfire (LD41)](https://rmkubik.itch.io/wildfire-jam) · [Девлог 2020](https://rmkubik.itch.io/wildfire-swap-development) — прототип; вітряки й попіл, inferno mode.
- YouTube: пошук «Wildfire Swap gameplay».

## Непевне
- (?) Чи будинок справді горить і це поразка, чи гра просто не зараховує рівень; патч-ноти згадують повідомлення Game Over.
- (?) Перемога: «вогню нікуди йти взагалі» (GameGrin) чи «до будинків нема шляху» (GamesXtreme) — у GIF збігаються.
- (?) Що лишає вигоріла трава (попіл/порожнє), чи вигорає дерево; роль вітряків і повторного спалаху попелу.
- (?) Точна кількість світів (5 — з одного відгуку) і назви механік B-side.
- (?) Чи можна обмінювати неортогональні або несусідні плитки — у GIF і описах лише сусідні.
