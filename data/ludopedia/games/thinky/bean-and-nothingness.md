---
title: Bean and Nothingness
slug: bean-and-nothingness
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
year: 2021
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1706090/Bean_and_Nothingness/", best: true, note: "суть: боби на траві + постріл паличкою = монстр за рецептом; roller і bomb; тріснуті блоки; 180+ пазлів; редактор, Workshop, режим для дальтоніків"}
  - {kind: other, url: "https://weloveit.io/game/1706090/", note: "агрегатор: той самий опис, теги Level Editor, Difficult"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bean+and+Nothingness+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, push-object, line-of-sight-attack, chase-player, explode-area, destructible-blocks, touch-death, player-death, reach-exit, sequential-levels, in-game-editor, level-exchange, controls-remap, achievements-window, save-progress, +recipe-spawn, +wand-cast, +helper-hazard-monsters, +colorblind-shapes]
proposes: ["+trigger:cast", "+cond:recipe", "+effect:summon", "+feature:colorblind-shapes", "+window:recipe-panel", "+card:recipe-spawn"]
author: opus
date: 2026-11-09
---

# Bean and Nothingness — склади боби за рецептом, вдар паличкою — і отримай монстра, що відкриє шлях або вбʼє тебе

## Суть
Складна покрокова головоломка на клітинах від RBOR Games. Гравець розкладає боби різних кольорів на трав'яних клітинах і стріляє в них магічною паличкою: правильна комбінація бобів за рецептом рівня перетворюється на монстра. Монстри — і інструмент, і загроза: roller котиться на героя, щойно його побачить, bomb вибухає; обидва ламають тріснуті блоки на шляху до цілі. Ядро — спланувати, які монстри потрібні, де їх «виростити» і як не стати їхньою жертвою.

## Поле і час
- Квадратна сітка-кімната на один екран (?), вид згори.
- Шари: підлога (трава / звичайна (?)) + блоки (тріснуті, міцні) + боби й монстри.
- Покроково: хід героя → реакція монстрів (roller, bomb) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой з паличкою | player | напрям | ходить 4 напрямки; стріляє паличкою в будь-якому з 4 напрямків |
| Біб | object | колір (червоний, жовтий, зелений, …) | розміщується на траві (штовханням (?)); сировина для рецепту |
| Трав'яна клітина | terrain | — | місце, де комбінація бобів може стати монстром |
| Рецепт | mark | інгредієнти → монстр | задається рівнем: червоний + жовтий = roller, зелений + зелений = bomb |
| Roller | enemy | — | побачивши героя по прямій, котиться на нього; наздогнав — смерть; перешкода між ними зупиняє; ламає тріснуті блоки |
| Bomb | enemy | — | вибухає; герой у зоні вибуху гине; вибух ламає тріснуті блоки |
| Тріснутий блок | static | — | перешкода; руйнується roller-ом або вибухом |
| Ціль (goal tile) | zone | — | клітина, куди треба дійти |
| Інші монстри | enemy | — | «нові монстри й механіки» в пізніших розділах (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(hero, dir)`; у біб — `push(bean)` (?).
- КОЛИ `input(wand, dir)` → ТО `custom: «постріл паличкою по лінії до першої цілі»` (?).
- КОЛИ `custom: «постріл влучив у трав'яну клітину з бобами»` → ЯКЩО `custom: «набір бобів = рецепт рівня»` → ТО `transform(beans, monster)`.
- КОЛИ `line_of_sight(roller, hero)` → ТО `slide(roller, toward_hero)`.
- КОЛИ `contact(roller, hero)` → ТО `lose`.
- КОЛИ `contact(roller, cracked_block)` → ТО `disappear(cracked_block)`.
- КОЛИ `custom: «bomb вибухає»` (?) → ТО `explode(area)`; ЯКЩО `custom: «герой у зоні вибуху»` → ТО `lose`.
- КОЛИ `explode(area)` → ЯКЩО `occupied(area, cracked_block)` → ТО `disappear(cracked_block)`.
- КОЛИ `reach(hero, goal)` → ТО `win`, `next_level`.
- Перемога: герой на цілі · Поразка: roller наздогнав / герой у вибуху · Рахунок: нема.

## Керування і ввід
- Клавіатура (розробники радять її), геймпад; керування можна перепризначити.
- Дії: крок, постріл паличкою в напрямку; undo/restart — (?).

## Вікна, меню, HUD
- `game-screen`: поле, боби, монстри, рецепти рівня (`+window:recipe-panel` — панель рецептів) (?).
- `level-select` / `puzzle-select` зі 180+ пазлів від «elementary» до «extremely challenging» (?).
- `editor-window` — вбудований редактор рівнів; Workshop — обмін рівнями.
- `settings-window`: режим для дальтоніків (боби різної форми), перепризначення керування.
- `achievements-window` (Steam).

## Фічі поза полем
- Понад 180 пазлів; `levels-sequential` з новими монстрами по ходу.
- `level-editor` + `level-sharing` (Steam Workshop); `save-progress` (Steam Cloud); `achievements`.
- `colorblind-palette` у вигляді форм бобів (`+feature:colorblind-shapes`); `remap-controls`; `gamepad-support`.

## Варіації й родичі
- Осі варіацій **породження сутностей**: монстр з'являється сам (спавнер) / гравець збирає інгредієнти за рецептом і активує (B&N, крафт-пазли) / з'являється від пострілу в обʼєкт.
- Родичі: Adventures of Lolo (вороги, що бачать по прямій, як інструмент і загроза), Bomberman (вибух руйнує блоки), Baba Is You (правила-рецепти), Sokoban.

## Цікавинки для курсу
- Рецепти: мультимножина бобів на клітині → тип монстра — 📎 (словник рецептів).
- Roller, що реагує на лінію погляду й котиться до упору — 📎.
- Вибух, що руйнує тріснуті блоки й вбиває героя в зоні — 📎.
- Монстр-інструмент, який водночас загрожує гравцю: планування черговості — 🥉.
- Редактор рівнів з палітрою бобів і монстрів — 🥉.

## Мапа на каталог
- Є: `move-4dir`, `keyboard-controls`, `push-object` (?); `line-of-sight-attack` + `chase-player` ↔ roller; `explode-area` ↔ bomb; `destructible-blocks` ↔ тріснуті блоки; `touch-death`, `player-death`; `reach-exit` ↔ goal tile; `sequential-levels`; `in-game-editor`, `level-exchange` ↔ Workshop; `controls-remap`; `achievements-window`; `save-progress`.
- **Нема** → пропозиції карток:
  - `+recipe-spawn` «Сутність з'являється з набору інгредієнтів за рецептом» · entities/spawn · 🥉 · слот {recipes}.
  - `+wand-cast` «Постріл-активація по лінії» · entities/interact · 📎.
  - `+helper-hazard-monsters` «Створені гравцем істоти допомагають і загрожують» · entities/interact · 🥉.
  - `+colorblind-shapes` «Кольори дубльовано формами» · interface/settings · 🌱.

## Пропозиції до словників
- `+trigger:cast` — гравець активував заклинання/паличку на клітину.
- `+cond:recipe` — набір сутностей у клітині відповідає рецепту.
- `+effect:summon` — породити сутність з інгредієнтів (інгредієнти зникають) — ширше за ✅ `transform`, бо з кількох в одну.
- `+feature:colorblind-shapes` — форми замість лише кольору.
- `+window:recipe-panel` — панель рецептів рівня.
- `+card:recipe-spawn` — як вище.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1706090/Bean_and_Nothingness/) — опис розробника: боби + паличка → монстр, рецепти, roller і bomb, тріснуті блоки й ціль, 180+ пазлів, редактор, Workshop, дальтонік-режим, геймпад.
- [weloveit.io](https://weloveit.io/game/1706090/) — дубль опису й теги.
- YouTube: пошук «Bean and Nothingness gameplay».

## Непевне
- (?) Як боби потрапляють на траву (штовхання, підбирання чи вже лежать); чи паличка стріляє лише вздовж лінії.
- (?) Що запускає вибух bomb і яка форма зони; чи roller котиться до упору чи на 1 клітину за хід.
- (?) Чим є «Nothingness» у назві — механіка (порожнеча?) чи лише назва; які інші монстри з'являються пізніше. Опис черги «сутності гасять одна одну» джерелами не підтверджено.
- (?) Undo, рестарт, структура меню й вибору рівнів. Wikipedia-статті нема, Thinky Games — 403, фан-вікі не знайдено.
