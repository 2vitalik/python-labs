---
title: Magiciban
slug: magiciban
aka: []
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
year: 2022
platforms: [web]
links:
  - {kind: itch, url: "https://auroriax.itch.io/magiciban", best: true, note: "грати в браузері; керування, натхнення (15 Puzzle, Sliding Ground)"}
  - {kind: other, url: "https://api.github.com/gists/d96dc0f496fabac68ffc9fa4ee2ea7ad", note: "вихідний код PuzzleScriptPlus (gist): обʼєкти, правила зсуву, 14 рівнів"}
  - {kind: other, url: "https://auroriax.github.io/PuzzleScript/editor.html?hack=d96dc0f496fabac68ffc9fa4ee2ea7ad", note: "код у редакторі PuzzleScriptPlus"}
  - {kind: other, url: "https://github.com/Auroriax/PuzzleScriptPlus", note: "форк рушія автора: level_select, tween"}
  - {kind: itch, url: "https://rosden.itch.io/sliding-ground", note: "натхнення: Sliding Ground (Rosden)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magiciban+puzzlescript", note: "пошук; проходження"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, push-object, row-conveyor, impassable-cells, all-on-targets, undo-unlimited, restart-level, level-select, level-unlock, sequential-levels, keyboard-controls, sound-effects, movement-animation, highlights, +floor-shift-into-gap, +ride-on-tile, +floating-target]
proposes: ["+card:floor-shift-into-gap", "+card:ride-on-tile", "+card:floating-target", "+window:title-screen", "+window:message-screen"]
author: opus
date: 2026-11-09
---

# Magiciban — фокусник зсуває сцену під собою, як пʼятнашки, щоб поставити кроликів під капелюхи

## Суть
Sokoban, у якому підлога — це рухомі плитки, а між ними — порожнеча. Крок з плитки в порожнечу не падіння, а зсув: плитка під фокусником їде разом з ним, а за нею — увесь суцільний ряд плиток позаду, як рядок пʼятнашок, що заїжджає в дірку. Усе, що стоїть на цих плитках (кролики), їде теж. Мета — кролики під капелюхами, які висять над сценою й можуть бути навіть над порожнечею.

## Поле і час
- Квадратна сітка, один екран на рівень; 12 основних рівнів («Opening Act» … «Grand Finale», підписані таймкодами 0:00–1:15 як номери шоу) + «Credits» + 2 «Encore».
- Шари колізій (з коду): фон → плитка / антиплитка → декор → тінь капелюха → гравець і кролики → капелюх (`Target`) → стрілки-підказки → службовий `Temp`.
- Три типи клітин підлоги: **плитка** (`Tile`), **порожнеча** (нема ні плитки, ні антиплитки — сюди можна зсувати), **антиплитка** (`AntiTile` — дірка, куди плитка не заїде; гравець теж не заходить).
- Покроково: тік = ввід. Прапорці коду: `noaction`, `run_rules_on_level_start`, `tween_length 0.05` (плавний зсув).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фокусник (`player`, Spectacular Spade ♠) | player | — | ходить по плитках; крок у порожнечу зсуває плитку під собою разом з рядом позаду |
| Плитка сцени (`Tile`) | terrain | — | рухома підлога: їде, коли її тягне фокусник або сусідня плитка; везе все, що на ній |
| Порожнеча (нема `Tile`) | terrain | — | гравець і кролики стояти тут не можуть; плитка може заїхати |
| Антиплитка (`AntiTile`, `AntiTileHor/Ver`) | static | лише вигляд відрізняє Hor/Ver | непрохідна для гравця й плиток |
| Кролик (`NormalRabbit` / `HappyRabbit` / `SurprisedRabbit`) | object | настрій | штовхається на 1, лише на плитку; їде разом з плиткою; настрій — лише вигляд |
| Капелюх (`Target` + `TargetShadow`) | static | — | висить над клітиною (з плиткою чи без); ціль для кролика |
| Декор плитки (`TileDeco1/2`) | static | — | випадковий візерунок, їде з плиткою, на правила не впливає |
| Стрілки (`FeedbackU/L/R/D`) | mark | — | службові підказки: куди зараз можна зсунути сцену |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(cell_ahead, tile)` and `free(cell_ahead)` → ТО `move(player, dir)` — звичайний крок.
- КОЛИ `input(dir)` → ЯКЩО `cell(cell_ahead, antitile)` → ТО `block`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «попереду порожнеча (ні плитки, ні антиплитки)»` → ТО `move(player, dir)`, `custom: «плитка під гравцем їде разом з ним»`, `sound(shift)`.
- КОЛИ `custom: «плитка рушає геть від сусідньої нерухомої плитки позаду»` → ТО `custom: «сусідня плитка рушає слідом»` — ланцюг до першої щілини: зсувається суцільний відрізок ряду/стовпця за гравцем.
- КОЛИ `custom: «плитка рушає»` → ТО `custom: «кролик / гравець / декор на ній рушають з нею»`.
- КОЛИ `contact(player, rabbit)` → ЯКЩО `cell(cell_behind, tile)` and `free(cell_behind)` → ТО `push`, `sound(push)`; інакше `block` (кролик не зіштовхується в порожнечу).
- КОЛИ `custom: «гравець не зрушив з місця»` → ТО `block` — хід без руху скасовано (`require_player_movement`).
- КОЛИ `after(move)` → ТО `custom: «стрілки-підказки в сусідніх порожніх клітинах навколо гравця»` і стрілка «назад» на клітині, яку він щойно звільнив.
- КОЛИ `after(push)` → ЯКЩО `occupied(cell, target)` → ТО `set_state(rabbit, happy)`; інакше `set_state(rabbit, surprised)` — лише вигляд.
- КОЛИ `all_on(rabbit, target)` → ЯКЩО `custom: «під кожним капелюхом кролик»` → ТО `win`, `next_level` (умови коду: «all target on Rabbit», «all Rabbit on target», «some target»).
- Перемога: кожен кролик під капелюхом і кожен капелюх з кроликом · Поразки нема · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок або зсув сцени (залежить від того, що попереду); `noaction` — дії нема.
- `Z` — undo, `R` — рестарт, `Esc` — вибір рівня (з опису на itch).

## Вікна, меню, HUD
- `title-screen` (custom, PuzzleScriptPlus): назва, автор.
- `level-select` (PuzzleScriptPlus `level_select`): секції-номери шоу з таймкодами; `level_select_lock` — закриті рівні, `level_select_unlocked_rollover 5` (?).
- `game-screen`: поле без HUD; `highlights` — стрілки можливих зсувів навколо фокусника.
- `message-screen` (custom): «Tadaah! You win the game! Congrats.», кредити, вступ до Encore («extra difficult bonus puzzles that were scrapped for the base game»).
- Переходи: title → level-select ↔ game-screen; Grand Finale → Credits → Encore 1–2.

## Фічі поза полем
- `undo` ∞, `restart-level`, `level-select` з `level-unlock`.
- Бонусні рівні Encore після титрів.
- Відкритий код (форк PuzzleScriptPlus, «hack this game»).

## Варіації й родичі
- Натхнення: пʼятнашки ([sliding-tile-permutation](../push-slide/sliding-tile-permutation.md)) і Rosden «Sliding Ground».
- Родичі в корпусі: [Sokoban](../push-slide/sokoban.md); [Patrick's Parabox](patricks-parabox.md), [Toodee and Topdee](toodee-and-topdee.md) — інша логіка «поле як обʼєкт»; [Stephen's Sausage Roll](stephens-sausage-roll.md) — теж «сцена» з острівцями.
- Осі варіацій: **що рухається від кроку** — гравець (Sokoban) / підлога під ним (тут) / увесь ряд по колу (Sixteen, Loopover); **хто їде з плиткою** — нічого / усе зверху (тут); **ціль** — на підлозі / висить над клітиною і не їде (тут, капелюх).

## Цікавинки для курсу
- Зсув суцільного відрізка плиток у щілину з «пасажирами» — 🥉 (два шари: підлога і обʼєкти, рух підлоги тягне обʼєкти).
- Ціль, що не їде разом з підлогою (капелюх над сценою), — 🌱, але змінює все планування.
- Штовхання лише на плитку (кролик не падає в порожнечу) — 🌱.
- Стрілки-підказки можливих зсувів навколо гравця — 📎 (обчислення легальних «особливих» ходів).
- Розвʼязувач: стан = розкладка плиток + позиції — 🥈 (простір станів росте з кожною щілиною).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `push-object` (кролики) · `row-conveyor` (найближче: відрізок ряду зсувається разом) · `impassable-cells` (антиплитки) · `all-on-targets` · `undo-unlimited` · `restart-level` · `level-select` + `level-unlock` · `sequential-levels` · `keyboard-controls` · `sound-effects` · `movement-animation` (tween) · `highlights` (стрілки).
- **Нема** → пропозиції карток:
  - `+floor-shift-into-gap` «Крок у щілину зсуває підлогу під гравцем і ряд позаду» · entities/move · 🥉 · слоти {chain: contiguous|single}.
  - `+ride-on-tile` «Обʼєкти їдуть разом з рухомою підлогою» · entities/move · 📎 — родич `platform`-ролі.
  - `+floating-target` «Ціль висить над клітиною й не рухається з підлогою» · game-logic/win · 🌱.

## Пропозиції до словників
- `+card:floor-shift-into-gap`, `+card:ride-on-tile`, `+card:floating-target` — див. вище.
- `+window:title-screen`, `+window:message-screen` — повтор (Mirror Isles).
- ⏳-слова, вжиті тут: `input`, `cell`, `free`, `occupied`, `move`, `set_state`, `sound`, `after`, `all_on`, `next_level`, ролі `terrain`, `mark`.

## Джерела
- ⭐ [Сторінка на itch.io](https://auroriax.itch.io/magiciban) — гра, сетинг (фокусник Spectacular Spade ♠, кролики, капелюхи), керування (стрілки/WASD, Z, R, Esc), Thinky Puzzle Game Jam 2, PuzzleScriptPlus.
- [Gist з кодом через GitHub API](https://api.github.com/gists/d96dc0f496fabac68ffc9fa4ee2ea7ad) — прапорці, обʼєкти, шари, правила зсуву, штовхання, підказок, умови перемоги, 14 рівнів і повідомлення («Game by Tom Hermans for the Thinky Puzzle Jam 2 in 2022»).
- [PuzzleScriptPlus](https://github.com/Auroriax/PuzzleScriptPlus) — форк рушія з level select і tween.
- [Sliding Ground](https://rosden.itch.io/sliding-ground) — названий автором попередник ідеї.

## Непевне
- (?) Що буває, коли передній край ланцюга плиток упирається в антиплитку: код перевіряє лише клітину перед плиткою гравця; як рушій розвʼязує решту — не перевірено.
- (?) Чи гравець «носить» капелюх, стоячи під ним (з коментаря гравця) — у коді капелюх не реагує на гравця, лише на кролика; найпевніше, це лише вигляд.
- (?) `level_select_unlocked_rollover 5` — найпевніше, скільки нерозвʼязаних рівнів наперед відкрито.
- (?) Черга дала рік 2024 — код каже Thinky Puzzle Jam 2, 2022.
- (?) Чи кролик штовхає кролика ланцюгом — у фетчі правила такого нема; ймовірно, `block`.
