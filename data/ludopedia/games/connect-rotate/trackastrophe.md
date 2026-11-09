---
title: Trackastrophe!
slug: trackastrophe
aka: [Trackastrophe]
family: connect-rotate
also: [program-robots]
klass: cursor
axes:
  field: iso
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3419850/Trackastrophe/", best: true, note: "опис: плитки напрямку й руху, GO-важіль, вагони, тунелі, портали, лід, підказки"}
  - {kind: steam, url: "https://store.steampowered.com/app/3542440/Trackastrophe_Demo/", note: "безкоштовне демо"}
  - {kind: itch, url: "https://kinoko-studio.itch.io/trackastrophe-demo", note: "демо, лише миша"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3419850&count=15&maxlength=4000", note: "девлоги Steam: стрибуни 1/2/3 клітини, тунелі, портали, клонери"}
  - {kind: other, url: "https://news.instant-gaming.com/en/articles/22674-trackastrophe-review-a-puzzle-game-on-tracks", note: "огляд: 5 біомів по ~20 рівнів, стрілки, тунелі, телепорти, камені"}
  - {kind: other, url: "https://ladiesgamers.com/trackastrophe-review/", note: "огляд: вагони, вихід, підказки кладуть колію"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Trackastrophe+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, teleport-pair, impassable-cells, reach-exit, inertia-slide, restart-level, sequential-levels, level-unlock, level-select, world-map, avatar-picker, language-picker, volume-control, save-progress, game-screen, settings-window, end-screen, +run-simulation, +hint-reveal, +jump-pad, +portal-keep-direction, +train-clone-merge, +wagon-collect-grow, +crash-on-obstacle]
proposes: ["+effect:jump", "+effect:lay_track", "+ui:go-lever", "+feature:cosmetic-hats", "+card:jump-pad", "+card:train-clone-merge", "+card:wagon-collect-grow"]
author: opus
date: 2026-11-09
---

# Trackastrophe! — розклади плитки руху, смикни GO-важіль, і потяг сам прокладає колію до виходу, збираючи вагони

## Суть
Ізометричний пазл Kinoko Studio про потяг-персонажа, що сам кладе рейки перед собою. Гравець аналізує мапу й розставляє **плитки напрямку й руху** (повороти, стрілки), потім тягне GO-важіль і дивиться, чи потяг доїде до виходу, підібравши по дорозі вагони. Кожен біом додає свою механіку: тунелі, стрибуни через прірви, лід, портали, клонери, істоти на шляху.

## Поле і час
- Ізометрична квадратна сітка, невеликі мапи з урвищами, каменями, водою (?).
- Дві фази: **планування** (статична розстановка плиток) і **виконання** після GO (`programmed`): потяг рушає по клітинах, лишаючи за собою рейки.
- 100+ рівнів у кількох біомах; огляд Instant Gaming: 5 біомів по ~20 рівнів, з бонусними. Біоми в девлогах: грибний, підводний, «Fauxrest Inc» (ліс на будівництві), «Prehistoric Chaos»; плюс таємний міні-біом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Потяг (локомотив) | player | напрям, довжина складу | після GO їде сам, кладе рейку перед собою; повертає на плитках руху |
| Вагон | pickup | — | збирається проїздом; склад довшає |
| Плитка напрямку / руху | object | вид (поворот, стрілка, …) (?) | ставиться гравцем до запуску; змінює напрям потяга |
| Вихід | static | — | кінцева точка рівня |
| Урвище / камінь | static | — | непрохідне; урвище долають стрибуном |
| Стрибун (Jumper) | terrain | колір: червоний 1, синій 2, помаранчевий 3 клітини | потяг з вагонами перестрибує N клітин (переважно урвищ) |
| Тунель | terrain | пара входів | миттєво переносить потяг з A до B |
| Портал | terrain | пара; вхід з будь-якого боку | телепортує до пари, напрям руху зберігається |
| Клонер | spawner | пара клонерів | перший роздвоює потяг; обидва мають заїхати в другий, щоб злитись і завершити рівень |
| Лід | terrain | — | слизький: потяг ковзає (?) |
| Істота-перешкода (Fauxrest Inc) | neutral | — | стоїть на шляху; як обійти — (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tile, cell)` → ЯКЩО `free(cell)` → ТО `place(player, tile)` (фаза планування).
- КОЛИ `input(go_lever)` → ТО `custom: «фаза виконання»`; потяг рушає.
- КОЛИ `tick` → ТО `move(train, facing)`, `custom: «потяг кладе рейку перед собою»`; вагони повторюють шлях (`body-queue`).
- КОЛИ `enter(train, direction_tile)` → ТО `face(train, tile_dir)`.
- КОЛИ `contact(train, wagon)` → ТО `attach(wagon, train)`, `grow(train, 1)`.
- КОЛИ `enter(train, jumper[c])` → ТО `custom: «стрибок через 1/2/3 клітини за кольором»`.
- КОЛИ `enter(train, tunnel)` → ТО `teleport(train, tunnel_pair)`.
- КОЛИ `enter(train, portal)` → ТО `teleport(train, portal_pair)`, напрям той самий.
- КОЛИ `enter(train, cloner_1)` → ТО `clone(train)`; КОЛИ `all_on(train_copy, cloner_2)` → ТО `merge(train, train_copy, train)`.
- КОЛИ `enter(train, ice)` → ТО `slide(train, facing)` (?).
- КОЛИ `blocked(train)` (камінь, урвище без стрибуна, кінець мапи) → ТО `crash`, `restart` (повтор без ліміту) (?).
- КОЛИ `reach(train, exit)` → ЯКЩО `custom: «вагони зібрано»` (?) → ТО `win`, `unlock(next_level)`.
- Перемога: потяг на виході (з вагонами; у клонер-рівнях — злитий). · Поразка: аварія — без покарання, назад у планування. · Рахунку нема (?).

## Керування і ввід
- Миша (демо — «лише миша»), повна підтримка геймпада в релізі.
- Розстановка плиток кліком по клітинах, потім GO-важіль; повтор після невдачі.
- Підказка кладе шматки колії прямо на мапу.

## Вікна, меню, HUD
- `main-menu` → `map-window` / `level-select`: меню біомів і рівнів з відкритими/закритими.
- `game-screen`: мапа, набір плиток (?), `go-lever`, кнопка підказки.
- `custom-window` кастомізації локомотива: кольори й капелюхи.
- `settings-window`: гучність, мова (11 мов).
- `end-screen`: рівень пройдено → наступний.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map`-подібний вибір біомів; бонусні рівні; таємний міні-біом.
- `hint` (кладе частину колії); `restart-level` без ліміту; `achievements`, `cloud-save` (Steam).
- `custom-skins`: кольори й капелюхи локомотива; `localization`; `gamepad-support`.

## Варіації й родичі
- Родичі: Railbound і Trainyard (план → запуск), Cosmic Express (одна колія), Train Valley, «стрілкові» пазли на кшталт Lightbot (плитки команд на клітинах).
- Осі варіацій: **що ставить гравець**: рейки (Railbound) / плитки-команди, а рейки кладе сам потяг (Trackastrophe) · **переходи між точками**: тунель (A→B) / портал (будь-який бік, напрям зберігається) / стрибун (через N клітин) · **кількість потягів**: один / клон і злиття.

## Цікавинки для курсу
- План → запуск симуляції → повернення в план при аварії — 🥉 (стан як дані).
- Плитки-команди на клітинах, що повертають «програму»-потяг — 📎.
- Стрибун на 1/2/3 клітини з перевіркою клітини приземлення — 📎.
- Портал із збереженням напряму проти тунелю — 🌱.
- Клонер: роздвоєння потяга й злиття в другому клонері — 🥉.
- Склад, що росте з кожним вагоном і повторює шлях голови — 📎 (картка `body-queue`).

## Мапа на каталог
- Є: `cell-click` ↔ розстановка; `teleport-pair` ↔ тунелі й портали; `impassable-cells` ↔ камені, урвища; `reach-exit`; `inertia-slide` ↔ лід (?); `restart-level`; `sequential-levels` + `level-unlock` + `level-select` + `world-map` ↔ біоми; `avatar-picker` ↔ капелюхи й кольори; `language-picker`, `volume-control`; `save-progress`; `game-screen`, `settings-window`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+run-simulation` «План → запуск симуляції» · game-logic · 🥉 (є в сімʼї).
  - `+hint-reveal` «Підказка ставить частину розвʼязку» · interface/hud · 🌱.
  - `+jump-pad` «Стрибун через N клітин» · entities/move · 📎 · слот {n: 1|2|3}.
  - `+portal-keep-direction` «Портал із збереженням напряму» · entities/interact · 🌱 (дитина `teleport`).
  - `+train-clone-merge` «Роздвоєння й злиття» · entities/spawn · 🥉.
  - `+wagon-collect-grow` «Склад росте з кожним вагоном» · entities/state · 📎.
  - `+crash-on-obstacle` «Аварія зупиняє симуляцію» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:jump` — перестрибнути N клітин (тут — `custom`).
- `+effect:lay_track` — сутність кладе колію перед собою.
- `+ui:go-lever` — кнопка-важіль запуску симуляції.
- `+feature:cosmetic-hats` — косметика локомотива (кольори, капелюхи).
- `+card:jump-pad`, `+card:train-clone-merge`, `+card:wagon-collect-grow`.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/3419850/Trackastrophe/) — плитки напрямку й руху, GO-важіль, вагони, 100+ рівнів, тунелі, портали, лід, підказки, кастомізація; реліз 28.05.2026.
- Девлоги Steam ([стрічка новин](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3419850&count=15&maxlength=4000)) — стрибуни 1/2/3, тунель A→B, портали з будь-якого боку зі збереженням напряму, клонери, потяг кладе рейки сам, «Fauxrest Inc» з істотами.
- [Instant Gaming](https://news.instant-gaming.com/en/articles/22674-trackastrophe-review-a-puzzle-game-on-tracks) — 5 біомів по ~20 рівнів, «turnouts, tunnels, teleporters, rocky obstacles».
- [LadiesGamers](https://ladiesgamers.com/trackastrophe-review/) — вагони, вихід, повтор без обмежень, підказки кладуть колію.
- [Демо на itch](https://kinoko-studio.itch.io/trackastrophe-demo), [демо на Steam](https://store.steampowered.com/app/3542440/Trackastrophe_Demo/).

## Непевне
- (?) Точний набір плиток: «direction & movement tiles», «turnouts»; пошук згадав «повороти й відбивачі» — на сторінках цього не бачив.
- (?) Чи кількість плиток обмежена; чи потяг стоїть до GO (Steam) чи вже їде (LadiesGamers: «класти шматки, доки не скінчилась колія»).
- (?) Чи всі вагони обовʼязкові для перемоги; що робить лід і як обійти істот.
- (?) Чи є undo, зірки чи інший рахунок.
