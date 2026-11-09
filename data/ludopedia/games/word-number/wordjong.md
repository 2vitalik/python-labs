---
title: WordJong
slug: wordjong
aka: [Word Jong]
family: word-number
also: [falling-match]
klass: cursor
axes:
  field: layers
  time: turn
  opponent: none
  info: partial
  random: setup
  goal: score
year: 2007
platforms: [Nintendo DS, PC]
links:
  - {kind: other, url: "https://www.engadget.com/2007/11/02/ds-fanboy-review-wordjong/", best: true, note: "DS Fanboy 2007: стос плиток, використана плитка відкриває ту, що під нею; Daily з цільовим рахунком і календарем пропущених; Temple Challenge з XP і печивом-передбаченням; мультиплеєр — одна дошка на двох"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/WordJong", note: "маджонг + Scrabble; очистити поле всіма плитками; 100 000+ слів; 39 медальйонів; Gameblend Studios / Magellan, Destineer; DS 16.11.2007; критика — нема туторіалу й redo"}
  - {kind: other, url: "https://avclub.com/wordjong-1798213172", note: "AV Club: піраміда; щойно відкриті літери можна додати в слово, яке складаєш; рахунок за довжину й рідкісні літери; стеля 9 літер; undo в соло; онлайн — по черзі з одного стосу"}
  - {kind: other, url: "https://www.gamepressure.com/games/wordjong/zd1e6a", note: "режими: Battle проти 7 AI, Daily, Temple Challenge (ранги-медалі), local wireless / Nintendo Wi-Fi"}
  - {kind: other, url: "https://www.vgdb.co/games/word-jong", note: "бонусні плитки за слова, Control Pad і тачскрін, DS Download Play"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordjong+ds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, keyboard-controls, word-validation, event-points, undo-step, daily-puzzle, level-unlock, sequential-levels, ai-opponent, turn-enforcement, online-multiplayer, achievements-window, mode-select, game-screen, end-screen, +free-tile-rule, +layered-tile-stack, +word-from-free-tiles, +uncover-during-word, +shared-stack-versus]
proposes: ["+cond:free_tile", "+ui:word-tray", "+ui:target-score", "+window:archive-window", "+card:layered-tile-stack", "+card:word-from-free-tiles", "+card:uncover-during-word", "+card:shared-stack-versus"]
author: opus
date: 2026-11-09
---

# WordJong — маджонг-розкладка з літер: складай слова лише з відкритих плиток і розбери весь стос

## Суть
Літерні плитки лежать багатоповерховою розкладкою, як у маджонг-пасьянсі (`../falling-match/mahjong-solitaire.md`). Гравець складає слово з плиток, на яких нічого не лежить; узята плитка відкриває ту, що під нею, і нову літеру можна одразу дописати в те саме слово. Слово знімається з поля й дає очки за довжину та рідкісні літери (як у Scrabble), мета — високий рахунок і розібрати розкладку до останньої плитки. Ядро — маджонг без пар: замість «знайди дві однакові» — «склади слово з того, що відкрито».

## Поле і час
- Розкладка-піраміда в кілька шарів; форма змінюється від задачі до задачі (у Daily — протягом тижня), разом із цільовим рахунком (Engadget).
- Видно лише верхні плитки; літера під ними стає відомою, коли її відкрили (?).
- Хід = одне слово; часу в базових режимах нема (?); у Battle гравці ходять по черзі з одного спільного стосу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, вартість (рідкісна = дорожча), шар | доступна, лише коли відкрита; входить у слово й зникає з поля |
| Розкладка | zone | шари, форма | відкриває нижні плитки, коли знято верхні |
| Слово, що складається | container | ≤ 9 літер (AV Club) | приймає відкриті плитки по одній |
| Бонусна плитка | pickup | — | «making words earns bonus tiles» (vgdb); вид — (?) |
| AI-суперник (Battle) | enemy | 7 персонажів | бере плитки з того самого стосу по черзі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tile)` → ЯКЩО `custom: «на плитці нічого не лежить»` (вільна; `+cond:free_tile`) → ТО `custom: «літера йде в кінець слова, плитка зникає з розкладки»`; інакше `block`.
- КОЛИ `after(tap tile)` → ТО `reveal(tiles_below)` — щойно відкриту плитку можна взяти в це саме слово.
- КОЛИ `input(submit)` → ЯКЩО `in_dictionary(word)` (100 000+ слів) → ТО `score(length + letter values)`, `clear(word_tiles)`; бонус — `custom: «бонусна плитка»` (?).
- КОЛИ `input(submit)` → ЯКЩО `not in_dictionary(word)` → ТО `message`, `block` — плитки повертаються на місця (?).
- КОЛИ `count(word_letters, ==, 9)` → ТО `block` — довше слово не скласти.
- КОЛИ `input(undo)` → ЯКЩО соло-режим → ТО `undo(1)`; redo нема.
- КОЛИ `all_gone(tile)` → ТО `custom: «розкладку очищено»`, `window(end-screen)`; бонус за повне очищення — (?).
- КОЛИ `no_moves(me)` → ТО `custom: «кінець задачі з рештою плиток»` (?) — фінал часто дочищають короткими 2-літерними словами.
- Daily: КОЛИ `custom: «задача дня завершена»` → ЯКЩО `counter(score, >=, target)` → ТО `custom: «ціль дня взято»`.
- Temple Challenge: КОЛИ `level_end` → ТО `counter(xp, +n)`, `custom: «печиво-передбачення з бонусними очками»`, `next_level`; XP → ранг-медаль.
- Battle / мультиплеєр: КОЛИ `turn_start(side)` → ТО `custom: «гравець складає слово з того самого стосу»`; КОЛИ `custom: «узято останню плитку»` → ТО `game_over`, більше очок — `win`.
- Перемога: ціль дня / прохід рівня / більше очок у Battle · Поразка: менше очок · Рахунок: сума слів.

## Керування і ввід
- Стилус по тачскріну — тап по відкритій плитці; або хрестовина Control Pad (vgdb).
- Кнопки: подати слово, стерти слово (?), undo (лише назад).

## Вікна, меню, HUD
- `main-menu`: Solo — Daily · Temple Challenge · Battle; Multiplayer — local wireless, Nintendo Wi-Fi, DS Download Play.
- `game-screen`: розкладка на одному екрані, `word-tray` і рахунок на іншому (?); `target-score` у Daily.
- `archive-window` (Daily): календар пропущених днів, у кожного своя задача й ціль.
- `achievements-window`: 39 медальйонів (як досягнення Xbox Live).
- `end-screen`: рахунок, ціль, печиво-передбачення (Temple Challenge).
- `character-select` (?) — вибір одного з 7 AI-суперників у Battle.

## Фічі поза полем
- `mode-daily` з цільовим рахунком і календарем минулих днів; `levels-sequential` + `rank-tiers` (Temple Challenge, XP, медалі).
- `ai-opponent-levels` (7 суперників у Battle), `local-multiplayer`, `online-multiplayer` (Nintendo Wi-Fi, рейтингових суперників мало — IGN).
- `undo` без `redo`; `achievements` (39).
- Нема туторіалу (критика IGN).

## Варіації й родичі
- Mahjong Solitaire (`../falling-match/mahjong-solitaire.md`) — та сама розкладка й правило вільної плитки, але пари; Shisen-Sho (`../falling-match/shisen-sho.md`).
- Scrabble (`scrabble.md`) — вартості літер; Bookworm (`bookworm.md`), SpellTower (`spelltower.md`) — слова зі знімання плиток, але без шарів.
- WordJong Arcade та PC-версія (?) — пізніші / ранні видання; бонуси Wild Card, Time Bomb, множник Jade згадано для «деяких ігор серії» (?).
- **Осі варіацій:** доступність плитки (нічого зверху / ще й вільний бік) · чи видно нижні літери · мета (рахунок / повне очищення / ціль дня) · спільний стос у Battle vs власний.

## Цікавинки для курсу
- Розкладка шарами й перевірка «на плитці нічого не лежить» — 🌱.
- Відкриття плитки під узятою посеред складання слова (стан відкатується, якщо слово не прийнято) — 📎.
- Рахунок за довжину й вартість літер — 🌱.
- Перевірка розвʼязності: чи можна розібрати всю розкладку словами зі словника (пошук з поверненням) — 🥇.
- Battle зі спільного стосу: AI, що бере слово з найбільшими очками й найменше відкриває супернику — 🥈.

## Мапа на каталог
- Є: `cell-click` / `keyboard-controls` ↔ стилус і хрестовина · `word-validation` · `event-points` ↔ вартості літер · `undo-step` ↔ undo без redo · `daily-puzzle` · `level-unlock` / `sequential-levels` ↔ Temple Challenge · `ai-opponent` ↔ Battle · `turn-enforcement` · `online-multiplayer` · `achievements-window` ↔ 39 медальйонів · `mode-select` · `game-screen` · `end-screen`.
- Вже запропоновано в `mahjong-solitaire.md`: `+free-tile-rule`.
- **Нема** → пропозиції карток:
  - `+layered-tile-stack` «Розкладка плиток у кілька шарів» · entities/legality · 📎 · слоти {layout: file}.
  - `+word-from-free-tiles` «Слово лише з вільних плиток» · game-logic/constraints · 🌱.
  - `+uncover-during-word` «Відкрита посеред слова плитка одразу доступна» · entities/state · 📎.
  - `+shared-stack-versus` «Двоє по черзі беруть зі спільного стосу» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+cond:free_tile` — на плитці нічого не лежить (див. `mahjong-solitaire.md`).
- `+ui:word-tray` — слово, що складається (див. `letterpress.md`); `+ui:target-score` — цільовий рахунок задачі дня.
- `+window:archive-window` — календар минулих щоденних задач.
- `+card:layered-tile-stack`, `+card:word-from-free-tiles`, `+card:uncover-during-word`, `+card:shared-stack-versus` — див. «Мапа на каталог».

## Джерела
- ⭐ [DS Fanboy (Engadget): WordJong review](https://www.engadget.com/2007/11/02/ds-fanboy-review-wordjong/) — стос і відкриття плиток, Daily, календар, Temple Challenge, мультиплеєр на одній дошці.
- [Wikipedia: WordJong](https://en.wikipedia.org/wiki/WordJong) — мета, словник, медальйони, розробники, дати, рецепція.
- [AV Club](https://avclub.com/wordjong-1798213172) — піраміда, відкриті літери в поточне слово, рахунок, 9 літер, undo, онлайн.
- [GamePressure](https://www.gamepressure.com/games/wordjong/zd1e6a) — режими, 7 AI.
- [vgdb](https://www.vgdb.co/games/word-jong) — бонусні плитки, керування, Download Play.
- YouTube: пошук «wordjong ds gameplay».

## Непевне
- (?) Чи для доступності плитки потрібен ще й вільний бік (як у маджонгу), чи досить «нічого зверху» — джерела кажуть лише «tiles under it».
- (?) Чи видно літери нижніх плиток до відкриття.
- (?) Бонусні плитки: vgdb каже «earn bonus tiles», а Wild Card / Time Bomb / Jade-множник — з результату пошуку про серію WordJong (статтю Washington Times не відкрито), можливо, з PC- або Arcade-версії.
- (?) Чи дає бонус повне очищення: Wikipedia — «clear the board using every tile», прев'ю DS (Nintendo World Report, не відкрито) — нібито бонусу за очищення нема.
- (?) Battle: за змушений пас суперника — бонусне очко й право стерти літеру — лише з результату пошуку, джерело не відкрито.
- (?) Рік і назва PC-оригіналу (Engadget: «began as a PC downloadable title»).
- GameSpot-огляд (⭐ черги) віддав 403 — у шапку не взято.
