---
title: Shisen-Sho / Onet (Сісен-сьо, «зʼєднай пару»)
slug: shisen-sho
aka: [四川省, Four Rivers, Onet, Onet Connect, Mahjong Connect, Nikakudori, KShisen]
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: setup
  goal: state
year: 1989
platforms: [arcade, Amiga, Atari ST, PC, Linux, Switch, mobile, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shisen-Sho", best: true, note: "правило шляху ≤2 повороти по порожніх клітинах, квіти/сезони, кінець гри, список ігор (Four Rivers, Nikakudori, Mahjong Connect)"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kshisen/kshisen/rules_and_tips.html", note: "KShisen: правила, очки за час і кількість плиток, гравітація ×2, undo/hint знімають з рекордів"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kshisen/kshisen/interface.html", note: "KShisen: меню Game / Move / Settings"}
  - {kind: other, url: "https://docs.kde.org/stable_kf6/en/kshisen/kshisen/configuration.html", note: "KShisen: гравітація, тільки розвʼязні, повідомлення «вже не розвʼязати», варіант «ковзання + 2 відрізки», розмір і складність"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shisen-sho+gameplay", note: "пошук; геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=onet+connect+gameplay", note: "пошук; Onet з тваринками"}
stage: v1
coverage: 75
mechanics: [cell-click, selection-highlight, chase-bfs, reachability-check, gravity-fall, undo-redo, restart-level, game-pause, score-records, leaderboard, time-bonus, no-moves-left, unsolvable-states, difficulty-levels, field-size-picker, theme-select, sound-effects, game-screen, end-screen, settings-window, +pair-match-removal, +bend-limited-path, +hint-pair, +solvable-deal, +unsolvable-warning]
proposes: ["+cond:path_turns", "+effect:draw_path", "+card:bend-limited-path", "+card:unsolvable-warning", "+ui:connection-line"]
author: opus
date: 2026-11-09
---

# Shisen-Sho — знімай пари однакових плиток, якщо їх можна зʼєднати лінією з не більш ніж двома поворотами

## Суть
Плитки маджонгу (або картинки) лежать прямокутником в один шар. Дві однакові плитки знімаються, якщо між ними є ламана лише з горизонтальних і вертикальних відрізків — **не більше трьох відрізків (≤2 повороти)**, — що проходить тільки порожніми клітинами. Мета — зняти всі плитки; гра закінчується, коли ходів нема. На відміну від Mahjong Solitaire, тут усе видно, а складність — у геометрії шляхів і порядку зняття. Onet / Mahjong Connect — мобільна гілка з тваринками, таймером і гравітацією за рівнем.

## Поле і час
- Квадратна сітка, один шар, усе видно (`info: full`); розмір змінюється (у KShisen — повзунок «Board Size»).
- Зовнішнє кільце порожніх клітин: шлях може огинати поле ззовні (?).
- Покрокова, хід = знята пара; час іде для рекорду (KShisen) або як ліміт рівня (Onet (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | малюнок; звичайно 4 копії | знімається парою з однаковою при наявності шляху |
| Квітка / сезон | tile | по 1 копії | «Chinese style»: будь-яка квітка з будь-якою квіткою, сезон — з сезоном |
| Порожня клітина | — | — | по ній іде шлях |
| Вибрана плитка | tile (стан) | — | підсвічена, чекає пару |
| Лінія зʼєднання | — (ui) | ≤3 відрізки | гра малює її при знятті, потім пара зникає |
| Підказка | — (ui `hint-marker`) | — | показує дві плитки, які можна зняти |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click tile)` → ТО `set_state(tile, selected)`.
- КОЛИ `input(click tile2)` → ЯКЩО `state(tile1, selected) and same(tile1, tile2, face) and path_exists(tile1, tile2)` з `custom: «path_turns ≤ 2 — лише горизонталь/вертикаль, лише порожні клітини»` → ТО `custom: «draw_path — показати лінію»`, `disappear(tile1)`, `disappear(tile2)`.
- Інакше → `clear_state(tile1, selected)` (пара не знімається).
- КОЛИ `input(click tile2)` → ЯКЩО `same(tile1, tile2, group)` (квіти або сезони) і `mode(chinese_style)` → ТО як для однакових.
- Гравітація (опція): КОЛИ `after(disappear)` → ЯКЩО `mode(gravity)` → ТО `fall(tiles_above)` — усі плитки над знятою опускаються на одну клітину; очки ×2.
- Варіант «ковзання» (опція KShisen): плитку можна зсунути в порожнє місце її рядка/стовпчика, але шлях — лише 1–2 відрізки.
- КОЛИ `all_gone(tile)` → ТО `win`; очки — за час, більші розкладки дають більше.
- КОЛИ `no_moves(player)` → ТО `game_over` (плитки лишились); опція «Show message if board can no longer be solved» — `message(...)` ще до повного глухого кута, коли виграти вже неможливо.
- КОЛИ `input(hint)` або `input(undo)` → ТО `set_state(game, assisted)`; КОЛИ `win` → ЯКЩО `state(game, assisted)` → ТО рекорд не зараховується.
- КОЛИ `level_start` → ЯКЩО `mode(solvable_only)` → ТО `custom: «генерувати лише розвʼязну розкладку»` (виграти все одно можна не за будь-якого порядку).
- Перемога: поле порожнє · Поразка: нема пари зі шляхом · Рахунок: час × розмір × (гравітація ×2).

## Керування і ввід
- Миша / тач: клік по першій, клік по другій плитці; лінію гра малює сама.
- KShisen: Ctrl+N нова, F5 рестарт, P пауза (зупиняє таймер), Ctrl+H рекорди, Ctrl+Z / Ctrl+Shift+Z undo/redo, H підказка.

## Вікна, меню, HUD
- `game-screen`: прямокутник плиток, `selection-highlight`, `custom: «connection-line»` при знятті, `timer-elapsed`, `remaining-counter` плиток (?), `hint-marker`.
- Game: New · Restart Game · Pause · Show High Scores (`leaderboard`, топ-10) · Quit.
- Move: Undo · Redo · Hint.
- Settings: Play Sounds (клік по плитці, падіння при гравітації) · Configure → `settings-window`: Gravity · Create solvable games only · Show message if board can no longer be solved · Use Chinese style · «Tiles can slide, connect only in 2 lines» · Board Difficulty (наскільки перемішано) · Piece Removal Speed · Board Size · вкладка Tiles and Background (`theme-select`).
- `end-screen`: перемога з очками / «нема ходів».

## Фічі поза полем
- `custom-difficulty` (розмір поля, ступінь перемішування), `custom-rules` (гравітація, ковзання, Chinese style), `theme-select`.
- `undo` / `redo` / `hint` (знімають з рекордів), `restart-level`, `pause`, `leaderboard-local`.
- Onet: рівні з таймером, на кожному рівні — інший напрям гравітації (вліво, вгору, до центру…), обмежені shuffle (?).

## Варіації й родичі
- Аркадні Shisen-Sho 1989 (Dynax «Dragon Punch», Irem «Shisen-Sho: Joshiryo-hen / Match It»), Turn It (Amiga/Atari ST); KShisen; Shisen-Sho Nikakudori (Switch, 2020); мобільні Onet / Mahjong Connect / Pikachu (?).
- Родичі: Mahjong Solitaire (той самий набір, але шари), Lines 98 (шлях по порожніх клітинах), Flow Free (лінії між парами).
- **Осі варіацій**: ліміт поворотів (2 / 1 / без ліміту) · шлях за межею поля (так / ні) · гравітація (нема / вниз / свій напрям на рівень) · ковзання плиток · таймер (рекорд / ліміт) · набір (маджонг / картинки).

## Цікавинки для курсу
- Перевірка шляху з ≤2 поворотами: три випадки (пряма, 1 кут, 2 кути) — 📎.
- Загальний BFS по станах (клітина, напрям, поворотів) — 🥉; з кільцем поза полем — +🌱.
- Гравітація після зняття, що міняє геометрію шляхів — 📎.
- Детектор «є знімна пара?» + підказка — 📎.
- Генератор розвʼязної розкладки (зворотна побудова з перевіркою шляхів) — 🥇.
- Анімація лінії зʼєднання — 🌱.

## Мапа на каталог
- Є: `cell-click` · `selection-highlight` · `chase-bfs` (пошук шляху) · `reachability-check` · `gravity-fall` (опція) · `undo-redo` · `restart-level` · `game-pause` · `score-records` / `leaderboard` / `time-bonus` (очки за час) · `no-moves-left` · `unsolvable-states` (повідомлення «вже не розвʼязати») · `difficulty-levels` · `field-size-picker` · `theme-select` · `sound-effects` · `game-screen` · `end-screen` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+pair-match-removal` «Зняти пару однакових» (спільна з Mahjong Solitaire) · entities/interact · 🌱.
  - `+bend-limited-path` «Шлях з обмеженням поворотів» · entities/legality · 🥉 · слот {max_turns: 2, outside: true}.
  - `+hint-pair` «Підказати доступну пару» · interface/hud · 🌱.
  - `+solvable-deal` «Гарантовано розвʼязна роздача» · levels/generation · 🥇.
  - `+unsolvable-warning` «Попередити, що виграти вже неможливо» · levels/solvability · 🥇 (потрібен розвʼязувач на кожному ході).

## Пропозиції до словників
- `+cond:path_turns` — існує шлях між A і B з ≤N поворотами (Shisen-Sho; розширює `path_exists`).
- `+effect:draw_path` — показати лінію шляху перед дією (Shisen-Sho, Onet).
- `+ui:connection-line` — лінія, що зʼєднує зняту пару.
- Вжито вже наявні `path_exists`, `same(..., group)`, `mode`, `fall`, `all_gone`, `no_moves`, `message`.

## Джерела
- ⭐ [Wikipedia: Shisen-Sho](https://en.wikipedia.org/wiki/Shisen-Sho) — правило шляху «must not exceed two turns», квіти/сезони, кінець гри, список ігор.
- [KShisen: Rules and Tips](https://docs.kde.org/stable_kf6/en/kshisen/kshisen/rules_and_tips.html) — ≤3 відрізки, лише порожніми клітинами, очки за час і розмір, гравітація ×2, undo/hint без рекорду.
- [KShisen: Interface](https://docs.kde.org/stable_kf6/en/kshisen/kshisen/interface.html) — меню й клавіші.
- [KShisen: Configuration](https://docs.kde.org/stable_kf6/en/kshisen/kshisen/configuration.html) — усі опції: гравітація, розвʼязні, Chinese style, ковзання, складність, розмір.

## Непевне
- (?) Чи може шлях виходити за межу прямокутника — у більшості реалізацій так, але відкриті джерела цього не кажуть.
- (?) Розмір класичного поля (часто 8×18 = 144 плитки) — не звірено.
- (?) Onet: напрям гравітації за рівнем, таймер, ліміт shuffle, назва «Pikachu» — з памʼяті.
- (?) Перший Shisen-Sho (Tamtex, 1989) — Wikipedia в списку цього не підтверджує; рік 1989 — за аркадними записами списку.
- (?) Лічильник лишку плиток у HUD — не згадано в доках KShisen.
