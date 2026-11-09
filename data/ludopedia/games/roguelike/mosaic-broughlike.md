---
title: Mosaic (7DRL 2022)
slug: mosaic-broughlike
aka: [Mosaic]
family: roguelike
also: [falling-match]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: score
year: 2022
platforms: [web, mobile]
links:
  - {kind: itch, url: "https://zunil.itch.io/mosaic", best: true, note: "грати в браузері; опис, керування, коментарі про кемпфаєр і бонуси"}
  - {kind: other, url: "https://itch.io/jam/7drl-challenge-2022/rate/1437759", note: "сторінка 7DRL 2022: опис і коментарі про шкоду, що падає в нижню сітку"}
  - {kind: other, url: "https://thinkygames.com/features/mosaic-a-rather-puzzling-broughlike/", note: "Thinky Games, стаття (403 для ботів; бачив лише сніпет пошуку)"}
  - {kind: other, url: "https://itch.io/games/tag-broughlike", note: "тег broughlike на itch.io — Mosaic, Magpie та інші ігри sunil."}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mosaic+broughlike+7DRL+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, keyboard-controls, swipe-gestures, hp-damage, line-match-clear, gravity-fall, run-relics, in-round-upgrades, permadeath, dungeon-generation, sequential-levels, score-records, leaderboard, +damage-as-garbage-tile, +column-overflow-lose]
proposes: ["+card:damage-as-garbage-tile", "+card:column-overflow-lose"]
author: opus
date: 2026-11-09
---

# Mosaic — broughlike, де кожен отриманий удар падає плиткою в match-3 знизу

## Суть
Крихітний роглайк у стилі Michael Brough: герой ходить мікро-сіткою з ворожими кольоровими плитками і «збирає плитки». Під полем — друга сітка, як колодязь Tetris: туди падають зібрані плитки **і отримані удари** у вигляді сірих сердець. Три й більше однакових у ряд — зникають, і серця теж можна збирати в ряди; переповнена колонка або забагато розбитих сердець — смерть. Тому шкода — не лише втрата, а ресурс для збігів: інколи вигідно підставитись.

## Поле і час
- Верхнє поле — маленька квадратна сітка-кімната (broughlike); нижнє — колодязь-сітка для match-3.
- Покроково: хід героя → хід ворогів (?); рух 4 напрямки.
- Кімнати процедурні; між ними — кемпфаєр з бонусом (boon).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | «HP» = серця в нижній сітці | ходить по верхній сітці, збирає плитки |
| Ворожа кольорова плитка | enemy | колір, тип атаки (?) | атакує героя; що далі, то різноманітніші й численніші |
| Кольорова плитка (зібрана) | tile | колір | падає в нижню сітку |
| Сіре / розбите серце | tile | — | падає в нижню сітку від кожного удару; матчиться як звичайна |
| Колонка нижньої сітки | zone | висота | переповнення — поразка |
| Кемпфаєр | container | — | бонус-здібність; відкриває бічну панель здібностей |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`.
- КОЛИ `custom: «герой збирає плитку»` → ТО `spawn_at(tile, lower_grid)`, `fall(tile)`.
- КОЛИ `custom: «ворог влучив»` → ТО `spawn_at(grey_heart, lower_grid)`, `fall(grey_heart)`.
- КОЛИ `pattern(line(3))` → ЯКЩО `same(tiles, color)` → ТО `clear(line)`, `score(n)` (?).
- КОЛИ `custom: «колонка переповнена»` → ТО `lose`.
- КОЛИ `custom: «забагато розбитих сердець унизу»` → ТО `lose` (?).
- КОЛИ `all_gone(enemy)` → ТО `next_level` (?).
- КОЛИ `contact(player, campfire)` → ТО `choose(boon)`, `custom: «здібність у бічній панелі»`.
- Рахунок: high score з онлайн-таблицею (власний API автора).

## Керування і ввід
- WASD / стрілки / свайп — рух; одна рука на тачі.
- Туторіалу нема навмисно: «вчитися грати — частина гри» (відповідь автора в коментарях).

## Вікна, меню, HUD
- `game-screen`: верхня мікро-сітка + нижній колодязь плиток; бічна панель здібностей після першого boon; рахунок.
- `leaderboard` — high scores.
- `end-screen` (?).

## Фічі поза полем
- `permadeath`, короткі сесії «кілька хвилин»; `colorblind-palette` (позначено на itch).
- `leaderboard-online`.

## Варіації й родичі
- Broughlikes корпусу: `roguelike/868-hack`, `roguelike/twinfold`, `roguelike/pawnbarian`; `roguelike/magpie-broughlike` — той самий автор.
- Шкода як «сміття» в колодязі — родич garbage-атак Puyo/Tetris (`falling-match`), але сміття насилаєш собі сам.
- **Осі варіацій**: HP — число / плитки в окремому полі (тут); сміття — від суперника / від власних помилок; збіг — 3 в ряд / групою.

## Цікавинки для курсу
- Два поля: дія вгорі породжує плитки внизу — 📎 (звʼязка двох модулів через чергу подій).
- Шкода = сіре серце, яке можна зматчити: здоровʼя як ресурс — 🌱.
- Поразка за переповненням колонки замість HP 0 — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `swipe-gestures` · `hp-damage` · `line-match-clear` · `gravity-fall` (нижня сітка) · `run-relics` (boons) · `in-round-upgrades` · `permadeath` · `dungeon-generation` · `sequential-levels` · `score-records` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+damage-as-garbage-tile` «Отримана шкода падає плиткою в колодязь» · entities/combat · 📎.
  - `+column-overflow-lose` «Переповнена колонка — поразка» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+card:damage-as-garbage-tile` · `+card:column-overflow-lose`.

## Джерела
- ⭐ [itch.io: Mosaic](https://zunil.itch.io/mosaic) — грати в браузері; «A small roguelike in the broughlike style. Collect tiles and seek ancient wisdom.»; sunil. і Corey Hardt, 7DRL 2022.
- [7DRL 2022: сторінка оцінок](https://itch.io/jam/7drl-challenge-2022/rate/1437759) — коментарі: шкода падає в нижню сітку, серця матчаться, смерть від переповнення.
- [Thinky Games: стаття](https://thinkygames.com/features/mosaic-a-rather-puzzling-broughlike/) — «simple, yet challenging match-3 puzzler»; удари ворогів дають сірі серця внизу (за сніпетом пошуку).
- YouTube: [пошук](https://www.youtube.com/results?search_query=Mosaic+broughlike+7DRL+gameplay).

## Непевне
- (?) Як саме «збираються» плитки вгорі (вбивство ворога? прохід по клітині?) і які кольори/типи ворогів.
- (?) Розмір обох сіток, правило падіння (колонка = позиція героя? як у Tetris?).
- (?) Що дають збіги — очки, лікування, ефект кольору.
- (?) Умова кінця кімнати і що таке «ancient wisdom» механічно.
- (?) Ефекти boons (гравці питають про «три діагональні клітини» — гра їх не пояснює).
- (?) Місця в 7DRL (за сніпетом: #3 загалом, #2 roguelikeness) не перевірені.
