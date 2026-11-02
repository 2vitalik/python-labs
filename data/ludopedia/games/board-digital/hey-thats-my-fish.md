---
title: Hey, That's My Fish! (Packeis am Pol)
slug: hey-thats-my-fish
family: board-digital
also: [chess-abstract]
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 2003
platforms: [board, Xbox 360, mobile]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/hey-thats-my-fish/game-rules.php", best: true, note: "повні правила: 60 крижин (30/20/10), розкладка 7/8, пінгвіни за к-стю гравців, рух, збір, застряглі, тай-брейк"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hey,_That%27s_My_Fish!", note: "автори, видавець, правило про ізольовані острови"}
  - {kind: other, url: "https://www.redblobgames.com/grids/hexagons/", note: "Red Blob Games: гекс-напрямки, лінії, звʼязність — для коду"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Hey+That%27s+My+Fish", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hey+That%27s+My+Fish+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [cell-click, drag-drop-piece, legal-move-highlight, hover-highlight, turn-enforcement, hot-seat, ai-opponent, ai-greedy, ai-minimax, no-moves-left, event-points, game-settings, +hex-grid-render, +path-move-any-distance, +shrinking-arena, +leave-cell-collect, +placement-phase, +skip-blocked-player, +island-claim, +start-cell-rule]
proposes: ["+trigger:leave", "+trigger:no_moves", "+effect:move", "+effect:set_cell", "+effect:pickup", "+cond:free", "+cond:path_clear", "+cond:connected", "+role:piece", "+role:terrain", "+ui:captured-pieces", "+window:match-setup", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Hey, That's My Fish! — пінгвіни ковзають по прямій, а крижина, з якої зійшов, тоне: поле тане, хто кого відріже

## Суть
Гекс-поле з 60 крижин по 1–3 рибини. Пінгвін ходить як шаховий ферзь на гексах — по прямій у будь-якому з 6 напрямків, скільки завгодно, не перестрибуючи дір і пінгвінів. **Крижина, з якої він пішов, забирається** гравцем (її риба — його очки), і поле зменшується щоходу. Стратегія — відрізати суперника на маленькій крижині й захопити собі великий «острів».

## Поле і час
- 60 гексів у 8 рядах (по черзі 7 і 8) — приблизно квадрат; розкладка випадкова (setup).
- Поле **тане**: кожен хід прибирає одну клітину; з'являються діри, які блокують рух і розрізають поле на острови.
- Хід = перемістити одного свого пінгвіна + забрати крижину відходу. Спершу — фаза розстановки.
- Партія ~20 хв; закінчується, коли жоден пінгвін не може рухатись.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Крижина | terrain | 1 / 2 / 3 риби (30 / 20 / 10 шт.) | клітина поля; зникає, коли пінгвін іде з неї; стає трофеєм гравця |
| Діра (вода) | static | — | непрохідна; через неї не можна ковзати |
| Пінгвін | piece | колір; 4 / 3 / 2 на гравця для 2 / 3 / 4 гравців | ходить по прямій на будь-яку відстань, 6 напрямків |
| Острів | zone | множина звʼязних крижин | ізольована частина поля; без пінгвінів — прибирається (Вікі) |
| Збірка гравця | supply | стос зібраних крижин | сума риб = очки; кількість — тай-брейк |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО гравці по черзі (від наймолодшого) ставлять по одному пінгвіну на вільну крижину **з 1 рибою**, доки не розставлять усіх.
- КОЛИ `input(move(penguin, dir, n))` → ЯКЩО `path_clear(dir, n)` (усі клітини шляху й ціль — крижини без пінгвінів, без дір) → ТО `move(penguin, to)`; інакше `block`. Зміна напрямку під час руху заборонена.
- КОЛИ `leave(penguin, floe)` → ТО `pickup(floe)` гравцем, `set_cell(floe → hole)`.
- КОЛИ `turn_start(player)` → ЯКЩО `no_moves(player)` → ТО його пінгвіни знімаються разом із крижинами під ними (крижини — йому), гравець більше не ходить; ходити обовʼязково, якщо можеш.
- КОЛИ `custom: «утворився острів без жодного пінгвіна»` → ТО острів прибирається з поля (Вікі; у правилах UBG — нерозібрані крижини просто повертаються в коробку в кінці).
- КОЛИ `custom: «на полі нема пінгвінів»` → ТО `game_over`; рахунок — сума риб у зібраних крижинах; нічия → більше крижин; далі — спільна перемога.

## Керування і ввід
- Цифрова версія: клік по своєму пінгвіну → підсвітка всіх досяжних клітин 6 променями → клік по цілі (або drag). Фаза розстановки — клік по крижині з 1 рибою.
- Черга по колу; гравець без ходів пропускається автоматично.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Гра / Hot-seat / AI / Правила.
- `match-setup`: 2–4 гравці, людина/AI, рівень AI, «рівномірна розкладка» (обмін крижин за згодою — опція правил).
- `game-screen`: гекс-поле з рибами, `legal-move-highlight` (промені), `captured-pieces` (зібрані крижини й сума риб кожного), `turn-indicator`.
- `end-screen`: риба, кількість крижин, переможець.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels`, `hotseat`, `rules-page`; `seed-input` для однакової розкладки (?) — природна фіча для цифрової версії.
- Xbox Live Arcade / мобільні версії (?) — з памʼяті; онлайн-гра.

## Варіації й родичі
- Оригінал — «Packeis am Pol» (Німеччина, 2003) (?), Fantasy Flight — англомовне видання.
- Родичі: Amazons (ферзь + «спалити» клітину, поле зменшується), Isolation/Isola (хід + видалити клітину), Tron (відрізати супротивника), Onitama/шахи (фігура з патерном), Quoridor (блокування).
- **Осі варіацій**: що зникає (клітина, з якої пішов / довільна клітина / клітина, яку «стріляєш» — Amazons) · рух (по прямій до упору / на будь-яку відстань / на 1) · мета (сума цінностей зібраного / останній, хто може ходити) · поле (гекс / квадрат).

## Цікавинки для курсу
- Рух «ферзя» по 6 гекс-напрямках до першої перешкоди — 📎.
- Поле, що тане: клітина відходу → діра; плюс виявлення островів (компоненти звʼязності, flood fill) — 🥉.
- Виявлення «острів, де лише мої пінгвіни» → гарантовані очки; оцінка для AI — 🥉.
- AI minimax/MCTS з оцінкою «риба на досяжних островах» — 🥇 (гарне завдання на пошук з великим розгалуженням).
- Фаза розстановки (лише клітини з 1 рибою) окремо від фази ходів — 🌱.
- Гравець без ходів вибуває, а гра йде далі — 🌱.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `legal-move-highlight` · `hover-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `ai-greedy` · `ai-minimax` · `no-moves-left` (вибування) · `event-points` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` — див. hex.md.
  - `+path-move-any-distance` — уже в корпусі (рух на будь-яку відстань по прямій); тут 6 гекс-напрямків.
  - `+shrinking-arena` — як у Bomberman; тут поле зменшується від ходів гравців, а не від таймера.
  - `+leave-cell-collect` «Клітина, з якої пішов, зникає і стає трофеєм» · entities/interact · 🌱 — родич Amazons/Isolation.
  - `+placement-phase` «Окрема фаза розстановки фігур» · game-logic/opponent · 🌱 · слоти {allowed: one_fish}.
  - `+skip-blocked-player` — як у Blokus.
  - `+island-claim` «Ізольований острів з фігурами одного гравця — його» · levels/solvability · 🥉 — компоненти звʼязності.
  - `+start-cell-rule` — як у Blokus; тут «лише на 1-рибну крижину».

## Пропозиції до словників
- `+trigger:leave` (уже ⏳ `leave`) — ключова подія гри: зійшов → крижина тоне.
- `+trigger:no_moves` (уже ⏳ `no_moves`) — вибування гравця.
- `+effect:move` · `+effect:set_cell` (крижина → діра) · `+effect:pickup` (крижина в збірку).
- `+cond:path_clear` — усі клітини шляху вільні (рух на будь-яку відстань) — ширше за `free(cell)`.
- `+cond:connected` — острів.
- `+role:piece` · `+role:terrain` (крижина з цінністю).
- `+ui:captured-pieces` — зібрані крижини; `+window:match-setup`.
- `+axis:turn-structure` = `round-robin` з фазою розстановки.

## Джерела
- ⭐ [UltraBoardGames: Hey, That's My Fish! rules](https://www.ultraboardgames.com/hey-thats-my-fish/game-rules.php) — компоненти (30/20/10), розкладка 7/8 × 8 рядів, пінгвіни 4/3/2, розстановка на 1-рибні, рух, збір, застряглі, тай-брейки.
- [Wikipedia: Hey, That's My Fish!](https://en.wikipedia.org/wiki/Hey,_That%27s_My_Fish!) — Günter Cornett, Alveydas Jakeliunas, Fantasy Flight; ізольовані острови прибираються.
- [Red Blob Games: Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/) — напрямки, лінії, звʼязність на гексах.
- BGG: пошук «Hey That's My Fish»; YouTube: пошук «Hey That's My Fish gameplay».

## Непевне
- (?) Видалення ізольованих островів без пінгвінів: Вікі — так, правила UBG — не згадують (лише кінцеве повернення в коробку). Різниця на очки не впливає.
- (?) Цифрові версії (Xbox Live Arcade ~2007–2008, мобільні) — з памʼяті; Steam-пошук нічого не дав.
- (?) Оригінальна назва «Packeis am Pol» і видавець Phalanx/Bambus — з памʼяті.
