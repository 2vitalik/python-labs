---
title: Metavaxx
slug: metavaxx
aka: []
family: hidden-deduction
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2021
platforms: [Windows, macOS, Linux]
links:
  - {kind: itch, url: "https://punkcake.itch.io/metavaxx", best: true, note: "опис: сапер-шутер, дві стратегії очищення, умова перемоги, 25 зразків, 20 апгрейдів, 6 лабораторій, керування, патчноути"}
  - {kind: steam, url: "https://store.steampowered.com/app/2316900/Metavaxx/", note: "Steam-реліз 10.08.2023: короткий опис, теги roguelite і procedural generation"}
  - {kind: other, url: "https://bigbossbattle.com/?p=73732", note: "огляд 2021: дзеркальне зникнення частин зразка, апгрейди, лабораторії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Metavaxx+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [neighbor-count-clue, projectile-shot, move-8dir, hp-damage, in-round-upgrades, run-relics, character-select, leaderboard, game-pause, keyboard-controls, dungeon-generation, sequential-levels, game-screen, end-screen, +minesweeper-shooter, +one-type-remains-win, +survivors-score, +cell-hidden-agent, +mirrored-sample]
proposes: ["+trigger:one_type_left", "+effect:release", "+window:upgrade-window", "+window:lab-select", "+card:minesweeper-shooter", "+card:one-type-remains-win", "+card:survivors-score", "+card:cell-hidden-agent"]
author: opus
date: 2026-11-09
---

# Metavaxx — «перший сапер-шутер»: стріляй у клітини зразка, де за числами ховається вірус

## Суть
Гравець — вакцина-кораблик у пробі тканини з клітин; частина клітин інфікована, і як у сапері відкриті клітини показують, скільки інфікованих поруч. Очистити пробу можна двома шляхами: **розстріляти інфіковані клітини** разом з агентами вірусу, що в них сидять, або **ізолювати** їх, обережно прибравши лише здорові навколо. Перемога — коли лишився один тип клітин; що більше клітин уціліло, то більше очок на апгрейд вакцини. Ядро для корпусу: дедукція сапера, але «відкриття» — це постріл у реальному часі, а помилка — бій з вірусом, а не миттєвий програш.

## Поле і час
- Проба — поле клітин (схоже на сітку сапера) (?); процедурно генерується (теги roguelite / procedural generation).
- Real-time: рух кораблика і стрільба — twin-stick.
- Забіг — 25 зразків; порядок зразків обирає гравець; між зразками — вибір апгрейда.
- Інфікованість зразка обмежена (патч: стеля 75 %).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вакцина | player | апгрейди, міни | рухається, цілиться мишею, стріляє |
| Здорова клітина | tile | число сусідів-інфікованих | знищується пострілом; показує число (?) після відкриття |
| Інфікована клітина | tile | прихований агент | знищення випускає агента вірусу (?) |
| Агент вірусу | enemy | — | ховається в інфікованій клітині; його треба збити |
| Слиз, приховані й великі молекули | hazard | — | з патчноутів: снаряди, слиз, «cloaked» молекули, великі молекули, що застрягають у клітинах (?) |
| Міна | projectile | розблоковується | права кнопка — поставити/кинути міну |
| Хімічний маркер | mark | лабораторія Kerixxons | позначити клітину (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ТО `move(vaccine, dir)`; КОЛИ `input(aim_fire)` → ТО `spawn(projectile)`.
- КОЛИ `contact(projectile, healthy_cell)` → ТО `disappear(healthy_cell)`, `reveal(cell)` сусідів (?); `custom: «відкрита клітина показує кількість інфікованих сусідів»`.
- КОЛИ `contact(projectile, infected_cell)` → ТО `disappear(infected_cell)`, `custom: «агент вірусу виходить назовні»` (?).
- КОЛИ `contact(projectile, agent)` → ТО `disappear(agent)`.
- КОЛИ `contact(projectile, sample_part)` → ТО `custom: «дзеркальні частини зразка теж зникають»` (за оглядом — «мітоз»).
- КОЛИ `input(mine)` → ЯКЩО `has(vaccine, mine)` → ТО `place(vaccine, mine)`.
- КОЛИ `count(infected_cell, =, 0)` or `count(healthy_cell, =, 0)` → ТО `win` — у пробі лишився один тип.
- КОЛИ `win` → ТО `score(n)` за кількістю вцілілих клітин будь-якого типу.
- КОЛИ `level_end` → ТО `choose(upgrade)` з 20 унікальних.
- КОЛИ `game_start` → ТО `choose(lab)` — одна з 6 лабораторій з унікальним бонусом.
- КОЛИ `custom: «забіг завершено»` → ТО `custom: «вакцину "відвантажено", ціна йде в Hall of Fame»`.
- Перемога: один тип клітин · Поразка: (?) — у джерелах не описана · Рахунок: вцілілі клітини → прогрес вакцини, ціна в таблиці.

## Керування і ввід
- Клавіатура+миша: стрілки/WASD — рух, миша — приціл і постріл, ЛКМ — підтвердити, ПКМ — міна, P — пауза.
- Геймпад: лівий стік / D-pad — рух, правий стік — приціл і стрільба, A — підтвердити, B — міна.
- Пауза лише в грі; гра паузиться, коли вікно не в фокусі.

## Вікна, меню, HUD
- `main-menu`: старт забігу, Hall of Fame (`leaderboard`).
- `lab-select` (`character-select`): одна з 6 лабораторій; назвати вакцину.
- `map-window` / вибір наступного зразка (?) — порядок зразків обирає гравець.
- `game-screen`: проба, кораблик, числа на клітинах; HUD (?) — не описаний.
- `upgrade-window` після зразка: вибір з апгрейдів (слиз, Basophile-снаряди, адреналінова залоза…).
- `pause-menu`, `end-screen` (відвантаження вакцини, ціна).

## Фічі поза полем
- `meta-progression` (?) — лабораторії; `leaderboard-local` / Hall of Fame за ціною вакцини.
- `achievements`, `cloud-save` (Steam).
- `gamepad-support`.

## Варіації й родичі
- У корпусі: [minesweeper.md](minesweeper.md) — числа сусідів; [tetrisweeper.md](tetrisweeper.md), [dragonsweeper.md](dragonsweeper.md), [demoncrawl.md](demoncrawl.md) — сапер у гібридах; [mamono-sweeper.md](mamono-sweeper.md) — помилка = бій, а не смерть.
- **Осі варіацій**: «відкриття» клітини «клік / крок аватара / постріл (тут)»; помилка «миттєвий програш / шкода / бій з ворогом»; мета «відкрити всі безпечні / лишити один тип (тут)»; очки «час / вцілілі клітини».

## Цікавинки для курсу
- Умова «лишився один тип клітин» замість «відкрито все безпечне» — 🌱.
- Відкриття клітини пострілом: дедукція сапера + aim у реальному часі — 📎.
- Очки за вцілілі клітини як компроміс між безпекою й жадібністю — 🌱.
- Забіг з апгрейдами між зразками і вибором порядку — 🥉.

## Мапа на каталог
- Є: `neighbor-count-clue` · `projectile-shot` · `move-8dir` (?) · `hp-damage` (?) · `in-round-upgrades` / `run-relics` ↔ апгрейди · `character-select` ↔ лабораторія · `leaderboard` · `game-pause` · `keyboard-controls` · `dungeon-generation` ↔ процедурні зразки · `sequential-levels` · `game-screen` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+minesweeper-shooter` «Відкриття клітини пострілом у real-time» · interface/input · 📎.
  - `+one-type-remains-win` «Перемога, коли лишився один тип клітин» · game-logic/goals · 🌱.
  - `+survivors-score` «Очки за вцілілі клітини» · game-logic/score · 🌱.
  - `+cell-hidden-agent` «Клітина ховає ворога, що виходить при знищенні» · entities/spawn · 📎.
  - Також: `+mirrored-sample` (?).

## Пропозиції до словників
- `+trigger:one_type_left` — на полі лишились клітини лише одного типу (можна й `count(...) = 0` двома правилами).
- `+effect:release` — знищений контейнер випускає сутність (агент вірусу).
- `+window:upgrade-window` — повтор: вибір апгрейда між рівнями.
- `+window:lab-select` — вибір стартового бонусу забігу.

## Джерела
- ⭐ [itch.io: Metavaxx](https://punkcake.itch.io/metavaxx) — суть, дві стратегії, умова перемоги, 25 зразків, 20 апгрейдів, 6 лабораторій, керування, патчноути, теги.
- [Steam](https://store.steampowered.com/app/2316900/Metavaxx/) — реліз 2023, «world's first minesweeper shooter», порядок зразків, roguelite.
- [Big Boss Battle](https://bigbossbattle.com/?p=73732) — дзеркальне зникнення частин, апгрейди (слиз, Basophile, адреналін), лабораторії.

## Непевне
- (?) Форма поля (квадратна сітка чи круглі клітини вільно) — скріншоти не описані в джерелах.
- (?) Як саме відкриваються числа (після пострілу чи одразу) і що виходить з інфікованої клітини — «agents hidden inside them» без деталей.
- (?) Умова поразки, HP вакцини, поведінка агентів і молекул — не описані.
- (?) Що означає «дзеркальні частини зразка зникають» — лише фраза огляду.
- (?) Рік: itch.io 10.07.2021, Steam 10.08.2023.
