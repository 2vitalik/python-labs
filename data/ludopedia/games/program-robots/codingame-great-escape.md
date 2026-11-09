---
title: "CodinGame: The Great Escape"
slug: codingame-great-escape
aka: [The Great Escape, Great Escape]
family: program-robots
also: [chess-abstract]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: race
year: 2015
platforms: [web]
links:
  - {kind: play, url: "https://www.codingame.com/multiplayer/bot-programming/great-escape", best: true, note: "арена CodinGame (сторінка на JS, автоматично не читається): дракони Codincarachas тікають через поле"}
  - {kind: other, url: "https://forum.codingame.com/t/the-great-escape-strategies/592", note: "розбори топ-гравців: 2 або 3 гравці, minimax/alpha-beta, paranoid, «path area», генетичний підбір ваг, конкурс лютий–березень 2015"}
  - {kind: other, url: "https://www.codingame.com/blog/the-great-escape-top-codingamers-code-reviews/", note: "огляд коду 1-го і 3-го місць (сторінка на JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codingame+the+great+escape", note: "пошук; реплеї"}
stage: v1
coverage: 60
mechanics: [move-4dir, reachability-check, chase-bfs, ai-minimax, ai-greedy, realtime-ai, move-timer, turn-enforcement, replay, leaderboard, +edge-walls, +wall-supply, +reach-row-win, +move-or-build, +text-io-protocol, +turn-time-limit, +league-boss-promotion, +three-player-race, +finish-order-ranking]
proposes: ["+trigger:timeout(bot)", "+effect:eliminate(bot)", "+cond:path_exists", "+cond:wall_between", "+effect:place_wall", "+card:finish-order-ranking"]
author: opus
date: 2026-11-09
---

# CodinGame: The Great Escape — Quoridor для ботів на двох або трьох: біжи до протилежного краю, стінами подовжуй шлях іншим

## Суть
Бот-арена CodinGame за мотивами [Quoridor](../chess-abstract/quoridor.md): кожен бот керує драконом, що стартує біля свого краю поля й мусить дійти до протилежного. Щоходу бот або крокує на сусідню клітину, або ставить стіну довжиною у дві клітини, що перегороджує шлях суперникам, але не може відрізати комусь вихід повністю. Відмінності від настільного оригіналу: гравці — програми з лімітом часу на хід, у матчі 2 або 3 боти (не 2/4), третій гравець біжить перпендикулярно (?), рейтинг — за порядком фінішу. Рамка арен (протокол stdin/stdout, ліги, реплеї) — у [bot-arenas](bot-arenas.md).

## Поле і час
- Квадратна сітка 9×9 (?), стіни — на ребрах між клітинами, займають два сегменти.
- Гравець 0 стартує на лівому краї й біжить праворуч, гравець 1 — навпаки, гравець 2 (у трьох) — згори вниз (?).
- Хід — по черзі за `myId`; один хід = одна дія; ліміт часу на хід ~100 мс, перший хід довший (?).
- Ліміт ходів матчу (?); хто не дійшов — ранжується за… (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дракон | piece | x, y, wallsLeft | крок на 1 у 4 напрямках, якщо нема стіни між клітинами |
| Стіна | static | x, y, H/V, довжина 2 | ставиться на ребра; блокує рух; не можна перетинати іншу стіну |
| Запас стін | supply | на гравця (?) | менше стін у грі на трьох (?) |
| Цільовий край | zone | протилежна сторона | досяг будь-якої клітини краю — фініш |
| Бот | player | код, stdin/stdout | щоходу читає стан і друкує одну дію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(bot)` → ТО `custom: «бот читає позиції всіх драконів, wallsLeft і список усіх стін»`.
- КОЛИ `input(LEFT|RIGHT|UP|DOWN)` → ЯКЩО `not wall_between(cell, next)` and `free(next)` (?) → ТО `move(dragon, dir)`; інакше `eliminate(bot)` (?).
- КОЛИ `input(x y H|V)` → ЯКЩО `has(bot, wall)` and `custom: «стіна не перетинає й не накладається на іншу»` and `path_exists(each dragon, goal_edge)` → ТО `place_wall(x, y, o)`, `counter(wallsLeft, −1)`.
- КОЛИ `input(x y H|V)` → ЯКЩО `not path_exists(any dragon, goal_edge)` → ТО `block` і `eliminate(bot)` (?).
- КОЛИ `reach(dragon, goal_edge)` → ТО `custom: «дракон фінішує, отримує місце за порядком»`; решта грають далі (у трьох).
- КОЛИ `timeout(bot)` → ТО `eliminate(bot)`.
- КОЛИ `custom: «досягнуто ліміту ходів»` → ТО `custom: «ранжування тих, хто не фінішував»` (?).
- Стрибка через сусіднього дракона, як у Quoridor, нема (?).
- Перемога: першим дійти до свого краю · Поразка: невалідна дія / таймаут / пізніший фініш · Рахунок: місце в матчі → рейтинг ліги.

## Керування і ввід
- Гравець пише бота будь-якою мовою CodinGame; ввід ініціалізації — `w h playerCount myId` (?); щоходу — `x y wallsLeft` для кожного гравця й список стін `wallX wallY wallOrientation` (?).
- Вивід — один рядок: напрямок або `x y orientation`, опційно повідомлення для реплею (?).

## Вікна, меню, HUD
- `arena-ide` (рамка — [bot-arenas](bot-arenas.md)): умова, редактор, вибір мови, консоль, Play testing / Submit.
- `replay-window`: поле з драконами і стінами, прогрес-шкала ходів.
- `league-ladder`: ліги Wood → … → Legend з босом (?).

## Фічі поза полем
- `bot-upload`, `leaderboard-online`, `league-promotion` — підтвердження з інших арен.
- Конкурс лютий–березень 2015, потім — постійна арена.

## Варіації й родичі
- [quoridor](../chess-abstract/quoridor.md) — настільний оригінал (2/4 гравці, стрибок, L-стрибок).
- [codingame-hypersonic](codingame-hypersonic.md), [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md) — інші арени CodinGame.
- Стратегії топ-ботів: minimax з alpha-beta (1v1), paranoid search (суперники грають проти тебе), обмежений пошук «лише стіни біля суперника», жадібні правила-пріоритети, евристика «на скільки суперник може подовжити мій шлях», генетичний підбір ваг оцінки.
- **Осі варіацій:** кількість гравців (2 / 3 / 4) · стрибок через фігуру (є / нема) · хто ходить (людина / бот з лімітом часу) · оцінка (виграш / порядок фінішу).

## Цікавинки для курсу
- BFS довжини шляху кожного дракона + перевірка «стіна не відрізає нікого» — 📎.
- Протокол stdin/stdout і локальний рефері для 2–3 ботів — 🥉.
- Бот 1v1: minimax з alpha-beta, оцінка «різниця довжин шляху + запас стін» — 🥈.
- Бот на трьох: paranoid vs max-n, ранжування за порядком фінішу — 🥇.
- Генетичний підбір ваг оцінки через самоігри — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `reachability-check` (стіна не може відрізати вихід) · `chase-bfs` · `ai-minimax` · `ai-greedy` · `realtime-ai` · `move-timer` · `turn-enforcement` · `replay` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+edge-walls`, `+wall-supply`, `+reach-row-win`, `+move-or-build` — з Quoridor (підтвердження).
  - `+text-io-protocol`, `+turn-time-limit`, `+league-boss-promotion` — з bot-arenas (підтвердження).
  - `+three-player-race` «Перегони трьох з перпендикулярними цілями» · game-logic/opponent · 🥉.
  - `+finish-order-ranking` «Місця за порядком фінішу, гра триває для решти» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:timeout(bot)`, `+effect:eliminate(bot)` — підтвердження з bot-arenas/Hypersonic.
- `+cond:wall_between`, `+effect:place_wall` — підтвердження з Quoridor (`path_exists` уже в 🔥 умов — тут вжито як ⏳).
- `+card:finish-order-ranking`.

## Джерела
- ⭐ [CodinGame: The Great Escape](https://www.codingame.com/multiplayer/bot-programming/great-escape) — арена; сторінка рендериться JS, текст умови не прочитано.
- [Форум CodinGame: The Great Escape — Strategies](https://forum.codingame.com/t/the-great-escape-strategies/592) — 2/3 гравці, дракони, стіни, стратегії 1–3 місць, дати конкурсу.
- [Блог CodinGame: code reviews](https://www.codingame.com/blog/the-great-escape-top-codingamers-code-reviews/) — інтервʼю Recar (1) і Romka (3), сторінка на JS.
- YouTube: пошук «codingame the great escape».

## Непевне
- (?) Розмір 9×9, кількість стін (10 на двох, 6 на трьох?), напрямки старту, формат вводу/виводу, ліміти часу — з памʼяті; умову не вдалося прочитати.
- (?) Чи дракони блокують одне одного й чи є стрибок; що буває після ліміту ходів.
- (?) Черга корпусу пише «3–4 гравці» — форум говорить лише про 1v1 і 1v2 (3 гравці).
