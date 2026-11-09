---
title: "Sandman: Every Death Builds"
slug: sandman-every-death-builds
aka: [Sandman]
family: dig-gravity
also: [grid-platformer]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4484250/Sandman_Every_Death_Builds/", best: true, note: "єдиний опис механіки: тіло → пісок, що падає, накопичується й ущільнюється; X — смерть на місці; 50 одноекранних стадій"}
  - {kind: other, url: "https://steamcommunity.com/app/4484250", note: "хаб спільноти: «that pile is now a floor», порівняння з Lemmings"}
  - {kind: other, url: "https://nodal.gg/game/sandman-every-death-builds-4484250", note: "агрегатор: реліз 2026-07-31, теги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sandman+Every+Death+Builds", note: "пошук; трейлер і геймплей"}
stage: v1
coverage: 35
mechanics: [player-death, respawn, gravity-fall, environment-death, cell-transform, keyboard-controls, reach-exit, leaderboard, +self-destruct, +persistent-object, +falling-sand-cell, +fill-hole, +corpse-terrain]
proposes: ["+card:corpse-terrain"]
author: opus
date: 2026-11-09
---

# Sandman: Every Death Builds — кожна смерть лишає купу піску, і з цих куп ти будуєш шлях

## Суть
Двовимірний пазл-платформер з одноекранними стадіями, де смерть — інструмент. Тіло загиблого героя на тому самому місці стає піском: пісок падає, накопичується й ущільнюється в новий рельєф, який лишається на стадії для наступних спроб. Купами можна засипати пастки, зробити уступ чи заповнити небезпечну яму; кнопка X убиває героя одразу там, де він стоїть, тож пісок кладеш свідомо. Для сімʼї це межовий випадок: платформер з вільним рухом, де «копання» замінене насипанням клітинного піску (?).

## Поле і час
- Стадія — один екран (50 стадій); камера не скролить.
- Два шари: статичний рівень (стіни, пастки, ями) + накопичений пісок, що переживає смерті в межах стадії.
- Real-time платформер (жанрові теги: Precision Platformer, Puzzle Platformer). Чи пісок — піксельна клітинна симуляція, чи фіксована фігура-купа, — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | — | бігає, стрибає (?); від пастки або кнопки X гине й стає піском |
| Пісок (тіло) | terrain | обʼєм одного тіла (?) | падає, накопичується, ущільнюється в опору; лишається на стадії |
| Пастка | hazard | вид (?) | убиває героя при дотику; засипана піском перестає діяти |
| Яма / провал | hazard | — | смерть або непрохідність; заповнюється піском |
| Вихід стадії | static | — | мета стадії (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(X)` → ТО `transform(hero, sand)` — `custom: «смерть на місці за бажанням»`.
- КОЛИ `contact(hero, trap)` → ЯКЩО `not occupied(trap_cell, sand)` → ТО `transform(hero, sand)`.
- КОЛИ `died(hero)` → ТО `spawn_at(sand, hero_pos)`, `respawn(hero, stage_start)` (?).
- КОЛИ `spawned(sand)` → ЯКЩО `not supported(sand)` → ТО `fall(sand)`.
- КОЛИ `settled` → ТО `custom: «пісок ущільнюється в твердий рельєф: на ньому можна стояти»`.
- КОЛИ `enter(sand, gap)` → ТО `set_cell(gap, sand)` — яма заповнена, прохід вільний.
- КОЛИ `contact(sand, trap)` → ТО `custom: «пастку засипано — більше не шкодить»`.
- КОЛИ `level_start` → ТО `custom: «піску нема; накопичене живе лише в межах стадії»` (?).
- КОЛИ `reach(hero, exit)` → ТО `win`, `next_level` (?).
- Перемога: пройти стадію (?) · Поразка: формально нема — смерть є ходом · Рахунок: Steam-таблиці лідерів; що саме рахують (смерті, час) — (?).

## Керування і ввід
- Клавіатура; X — смерть на місці. Біг і стрибок — (?) (у джерелі не названі).
- Головне рішення гравця — **де** померти: позиція тіла = позиція майбутньої купи.

## Вікна, меню, HUD
- `game-screen`: одноекранна стадія; HUD (лічильник смертей?) — (?).
- `level-select` або послідовні стадії — (?); `leaderboard` — через Steam Leaderboards.
- Інші вікна в джерелі не описані.

## Фічі поза полем
- 50 стадій (`levels-sequential` (?)); `achievements` і `stats` — Steam; `cloud-save` — Steam Cloud; `leaderboard-online` — Steam Leaderboards.

## Варіації й родичі
- У сімʼї: [lemmings](lemmings.md) (спільнота порівнює: тіла-ресурс, що змінюють рельєф для інших), [sugar-sugar](sugar-sugar.md) і [sandspiel](sandspiel.md) (пісок падає й накопичується купами), [the-powder-toy](the-powder-toy.md) (сипучі частинки).
- **Осі варіацій** «смерть як ресурс»: смерть лише скидає спробу (класичний платформер) / лишає слід без фізики / лишає тіло-обʼєкт / тіло стає сипучим рельєфом (Sandman); хто вирішує місце — випадок (пастка) / гравець (кнопка X).

## Цікавинки для курсу
- Тіло → пісок, що падає й лишається між спробами: стан стадії живе довше за аватар — 📎 (окремий шар поля, не скидається при respawn).
- Купа піску як клітинна симуляція (падіння вниз, потім по діагоналі) і «ущільнення» в тверді клітини — 🥉.
- Кнопка самогубства як свідомий інструмент + перевірка «пастку засипано» через `occupied` — 🌱.
- Розвʼязувач стадії: мінімум смертей, щоб дістатися виходу (BFS по станах «рельєф + позиція») — 🥇.

## Мапа на каталог
- Є: `player-death` ↔ смерть як дія · `respawn` ↔ нова спроба (?) · `gravity-fall` ↔ пісок падає · `environment-death` ↔ пастки · `cell-transform` ↔ тіло → пісок · `keyboard-controls` · `reach-exit` (?) · `leaderboard`.
- Повтори з корпусу: `+self-destruct` (тут не вихід з глухого кута, а інструмент) · `+persistent-object` (пісок переживає ресет спроби) · `+falling-sand-cell` · `+fill-hole` (пісок засипає яму).
- **Нема** → `+corpse-terrain` «Тіло після смерті стає рельєфом» · entities/death · 📎 · слоти {material: sand|block|platform, persist: stage|run}.

## Пропозиції до словників
- `+card:corpse-terrain` — смерть залишає на полі опору для наступних спроб (Sandman; частково Lemmings).

## Джерела
- ⭐ [Steam: Sandman: Every Death Builds](https://store.steampowered.com/app/4484250/Sandman_Every_Death_Builds/) — опис: тіло → пісок, падає, накопичується, ущільнюється; засипати пастки, зробити уступ, заповнити яму; X — смерть на місці; 50 одноекранних стадій; UNHANDLED Games, 31.07.2026.
- [Steam Community hub](https://steamcommunity.com/app/4484250) — «that pile is now a floor», порівняння з Lemmings.
- [nodal.gg](https://nodal.gg/game/sandman-every-death-builds-4484250) — дата релізу, теги.
- YouTube: пошук «Sandman Every Death Builds».

## Непевне
- (?) Керування рухом (біг, стрибок, інші кнопки), розмір і форма купи від одного тіла, чи пісок — піксельна симуляція.
- (?) Мета стадії (вихід?), відродження на старті стадії, чи є ліміт смертей або «par» смертей.
- (?) Види пасток і чи засипана пастка знешкоджена назавжди; що рахують Steam-таблиці (смерті чи час).
- Джерело механіки одне — опис Steam; відео не переглянуто.
