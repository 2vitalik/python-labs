---
title: Minesweeper Together
slug: minesweeper-together
aka: []
family: hidden-deduction
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: coop
  info: hidden
  random: setup
  goal: state
year: 2025
platforms: [PC (Steam, Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3550060/Minesweeper_Together/", best: true, note: "опис: co-op і versus до 8 гравців онлайн, офлайн, 5 складностей + власна, no-guess для Easy–Hard, малювання, кастомізація, Workshop; реліз 16.05.2025"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3550060&count=30&maxlength=4000", note: "патчноути v1.1.0–v1.5.3: versus, життя, блокування після міни, кольори винуватця, XP, лобі, курсори з іменами, глядач"}
  - {kind: other, url: "https://steamcommunity.com/stats/3550060/achievements", note: "11 досягнень: Flagless, Lucky Number 8, Winning Together, On Top…"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Minesweeper+Together+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, chord-click, neighbor-count-clue, flood-reveal, no-guess-generation, difficulty-levels, field-size-picker, online-multiplayer, lobby-window, simultaneous-versus, seed-share, restart-level, field-scaling, mode-select, tutorial-window, achievements-window, profile-stats, theme-select, avatar-picker, background-music, game-screen, settings-window, +shared-board-coop, +remote-cursors, +blame-colors, +mistake-lockout, +free-draw-notes, +player-elimination, +spectate-after-elimination, +xp-from-clues]
proposes: ["+effect:lock_input", "+ui:remote-cursor", "+ui:live-ranking", "+feature:free-draw-notes", "+feature:blame-colors", "+card:shared-board-coop", "+card:remote-cursors", "+card:blame-colors", "+card:mistake-lockout", "+card:spectate-after-elimination", "+card:xp-from-clues"]
author: opus
date: 2026-11-09
---

# Minesweeper Together — сапер на до 8 гравців онлайн: спільне поле в кооперативі або гонка на однакових полях

## Суть
Класичний [minesweeper](minesweeper.md), у який грають разом: у **co-op** усі гравці клацають по одному полю, бачать курсори одне одного з іменами й малюють поверх поля плани. У **versus** кожен отримує своє поле з тим самим сідом і тією самою відкритою стартовою клітиною — перемагає той, хто перший очистить поле, або найбільший рахунок. Нове для корпусу — соціальний шар сапера: хто помилився, видно кольором його аватара, а після міни все поле на мить блокується для всіх.

## Поле і час
- Квадратна сітка; 5 пресетів Easy / Medium / Hard / Insane / Diabolical задають ширину, висоту й кількість мін (числа на сторінці не названі) + власний розмір.
- Камера: панорама WASD/стрілками або середньою кнопкою миші — поле може бути більшим за екран.
- Час: гравці діють одночасно, без ходів і без таймера ходу («Playable without Timed Input»); versus — гонка.
- На старті відкривається випадкова клітина (у versus — однакова для всіх).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | tile | — | відкривається кліком будь-якого гравця |
| Число | mark | 0–8 | кількість мін серед 8 сусідів; 0 — каскад |
| Міна | hazard | — | відкрита — фарбується кольором винуватця; забирає життя (якщо ввімкнено) |
| Прапорець | mark | хто поставив | хибний прапорець фарбується кольором того, хто поставив (коли саме видно — (?)) |
| Глагл (аватар гравця) | player | обличчя, колір, рівень | курсор з іменем на спільному полі |
| Малюнок | mark | лінії | вільне малювання поверх поля; гумка |
| Поле суперника (versus) | zone | рахунок, мін лишилось | своє поле на кожного, той самий сід |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `reveal(random cell)` (у versus — та сама клітина для всіх).
- КОЛИ `input(reveal, cell)` → ЯКЩО `not occupied(cell, mine)` → ТО `reveal(cell)`, `set_value(cell, adjacent_count(cell, mine))`.
- КОЛИ `after(reveal)` → ЯКЩО `adjacent_count(cell, mine, ==, 0)` → ТО `reveal(neighbors8)` (каскад).
- КОЛИ `input(flag, cell)` → ЯКЩО `custom: «цю клітину щойно позначив або зняв інший гравець»` → ТО `block` (буфер прапорців, v1.4.4); інакше `mark(cell, flag)` / `unmark(cell)`.
- КОЛИ `input(chord, number)` (пробіл або клік по числу) → ЯКЩО `custom: «прапорців довкола стільки ж, скільки число»` → ТО `reveal(unflagged neighbors)` (?).
- КОЛИ `input(reveal, cell)` → ЯКЩО `occupied(cell, mine)` → ТО `paint(cell, player_color)`, `lives(-1)` (якщо життя ввімкнено); у co-op — `custom: «усі гравці на мить не можуть діяти на полі»` (`+effect:lock_input`).
- КОЛИ `custom: «міна забрала останнє життя»` → ТО `custom: «обвідка BOOM на цій міні»`.
- Versus: КОЛИ `counter(lives, ==, 0)` → ТО `custom: «гравець вибуває до кінця партії й стає глядачем (Q/E — між полями)»` (`+effect:eliminate`).
- КОЛИ `counter(closed_safe, ==, 0)` → ТО `win` (co-op — усім; versus — першому).
- Versus: КОЛИ `custom: «вибули всі»` → ТО `custom: «перемагає найбільший рахунок»`.
- КОЛИ `game_over` → ТО `custom: «XP = сума всіх видимих чисел на полі × множник складності (1 / 1,25 / 1,5 / 1,75 / 2); при поразці ÷2»`.
- КОЛИ `counter(xp, >=, next_level)` → ТО `unlock(frame|nameplate)` — поріг росте логарифмічно, рівні без стелі.
- КОЛИ `input(B)` → ТО `set_state(player, draw_mode)`; у ньому `input(drag)` → `custom: «лінія поверх поля»`; малювання знімає залік «Flagless».
- КОЛИ `input(R)` → ТО `restart`.
- Перемога: поле очищено · Поразка: скінчились життя / (у класиці) відкрита міна (?) · Рахунок: у versus — смуга рахунків унизу (як нараховується — (?)).

## Керування і ввід
- ЛКМ — відкрити; ПКМ — прапорець; пробіл — прапорець або акорд залежно від клітини.
- WASD / стрілки або середня кнопка — рух камери; B — режим малювання (лінії, гумка-коло); R — рестарт; M — звук; Q/E — переглядати поля інших, коли вибув.
- Можна грати лише мишею; розмір власного курсора 1×–8×, шрифт імен на курсорах (0 — сховати).

## Вікна, меню, HUD
- `main-menu`: рівень і XP гравця, Play → створити / знайти лобі або офлайн-гра; Customize; налаштування; туторіал.
- `lobby-window`: список публічних лобі з оновленням кожні 5 с; хост кікає й банить кліком по імені; видимість лобі.
- `match-setup` (налаштування гри хоста): режим co-op / versus, складність або власний розмір, no-guess, життя, сід.
- `game-screen`: поле, курсори гравців з іменами, малюнки; у versus — `+ui:live-ranking` (смуга рахунків, перемикається на «мін лишилось»); `remaining-counter` (?).
- `tutorial-window`: Professor Grey вчить правилам, малюванню й камері.
- `settings-window`: відео (курсор, монітор), звук, Stats, Workshop-предмети, фон.
- `skin-select` / Customize: 16+ облич глагла будь-якого кольору (hex), 39 фонів, 24+ тем поля (темна, High Contrast).
- `achievements-window` — 11 досягнень Steam; `stats-window` — перемоги за режимом і складністю, відкриті клітини, прапорці, підірвані міни, рекорди.

## Фічі поза полем
- `mode-coop`, `mode-versus`, офлайн-гра; `online-multiplayer` до 8 гравців; `spectator` після вибування.
- `difficulty-presets` + `custom-difficulty`; no-guess для Easy–Hard; `seed-input` (з сідом більшість досягнень вимкнено).
- `xp-level` з косметичними нагородами (рамки, таблички), без мікроплатежів; `achievements` (Flagless — без прапорців і малювання; Lucky Number 8 — знайти вісімку); `stats`.
- `mod-support` (Steam Workshop: теми поля, фони, обличчя; окремий Uploader), `custom-skins`, `high-contrast`, `sound-toggle`, `tutorial`.
- `+feature:free-draw-notes` — малювання поверх поля; `+feature:blame-colors` — помилка фарбується кольором гравця.

## Варіації й родичі
- База — [minesweeper](minesweeper.md); змагальний сапер з відсівом — [boomboombattle](boomboombattle.md); сапер, де міну шукають разом, — [bomb-busters](bomb-busters.md) (настільна команда).
- Спільне поле з кількома курсорами в корпусі — [pac-man-battle-royale](../maze-arcade/pac-man-battle-royale.md) (спільна арена, інше ядро).
- **Осі варіацій «мультиплеєр сапера»:** одне поле на всіх (co-op) / однакові поля кожному (versus із сідом) / різні поля однакової складності (BoomBoomBattle); ціна міни — кінець гри / життя з лічильником / блокування поля на мить; комунікація — нічого / курсори з іменами / малювання / чат (?).

## Цікавинки для курсу
- Однаковий сід → однакове поле кожному гравцеві, плюс однакова стартова клітина — 🌱.
- XP як сума видимих чисел на полі з множником складності — 🌱.
- Кольори винуватця: зберігати в клітині id гравця, що її відкрив/позначив — 🌱.
- Блокування поля після міни й буфер прапорців (щоб двоє не перемикали той самий прапорець) — 📎.
- Вільне малювання поверх поля шаром, що не впливає на логіку, + гумка — 📎.
- Глядач після вибування з перемиканням між полями Q/E — 📎.
- Спільне поле для 8 гравців онлайн із синхронізацією кліків і першого кліку — 🥇 (картка `online-multiplayer`).

## Мапа на каталог
- Є: `cell-click`, `chord-click`, `neighbor-count-clue`, `flood-reveal`, `no-guess-generation`; `difficulty-levels` + `field-size-picker` ↔ 5 пресетів і власний розмір; `online-multiplayer` + `lobby-window`; `simultaneous-versus` ↔ versus з одним сідом; `seed-share` ↔ ввід сіду; `restart-level` ↔ R; `field-scaling` ↔ камера по великому полю; `mode-select`; `tutorial-window`; `achievements-window`; `profile-stats`; `theme-select` ↔ теми поля; `avatar-picker` ↔ глагли; `background-music` ↔ окрема музика versus; `game-screen`; `settings-window`.
- **Нема** → пропозиції карток:
  - `+shared-board-coop` «Кілька гравців одночасно на одному полі» · game-logic/opponent · 🥈.
  - `+remote-cursors` «Курсори інших гравців з іменами» · interface/hud · 📎.
  - `+blame-colors` «Помилка фарбується кольором того, хто її зробив» · interface/hud · 🌱.
  - `+mistake-lockout` «Після помилки поле на мить блокується для всіх» · game-logic/opponent · 🌱 · слот {duration}.
  - `+free-draw-notes` (вже пропонована як фіча) — малювання поверх поля.
  - `+player-elimination` (вже пропонована) — вибування у versus.
  - `+spectate-after-elimination` «Вибулий дивиться за іншими, перемикаючи поля» · game-logic/opponent · 📎.
  - `+xp-from-clues` «Досвід = сума видимих підказок × складність» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:lock_input` — на N с заборонити дії на полі (усім або одному гравцеві).
- `+ui:remote-cursor` — чужий курсор з іменем і кольором; `+ui:live-ranking` — смуга рахунків суперників (уже пропонувався).
- `+feature:free-draw-notes` — малювання поверх поля (уже пропонувався); `+feature:blame-colors` — підсвітка винуватця помилки.
- `+card:shared-board-coop`, `+card:remote-cursors`, `+card:blame-colors`, `+card:mistake-lockout`, `+card:spectate-after-elimination`, `+card:xp-from-clues`.

## Джерела
- ⭐ [Steam: Minesweeper Together](https://store.steampowered.com/app/3550060/Minesweeper_Together/) — режими, до 8 гравців, офлайн, пресети, no-guess, малювання, глагли, фони, теми, Workshop; розробник anchikai, 16.05.2025.
- [Steam News API: патчноути](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3550060&count=30&maxlength=4000) — v1.1.0 (кольори винуватця, BOOM, малювання, пробіл для прапорця й акорду), v1.4.4 (буфер прапорців), v1.5.0 (versus, життя, глядач, XP і рівні, лобі, курсори з іменами, статистика, блокування після міни).
- [Steam: досягнення](https://steamcommunity.com/stats/3550060/achievements) — 11 досягнень з описами.
- YouTube: пошук «Minesweeper Together gameplay».

## Непевне
- (?) Розміри й кількість мін у пресетах — на сторінці не названі.
- (?) Як нараховується рахунок у versus (окремо від XP) і що буде в co-op, коли скінчаться спільні життя чи відкрита міна без життів — кінець гри для всіх?
- (?) Чи життя спільні в co-op, чи в кожного свої (патч каже про власні життя лише у versus).
- (?) Чи малюнки видно всім гравцям; чи є чат.
- (?) Правило акорду (класичне «прапорців = числу») — припущення; патч каже лише «flag and chord with spacebar».
