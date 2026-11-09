---
title: Banana
slug: banana
aka: [バナナ, Mole Mole, モールモール]
family: dig-gravity
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1986
platforms: [Famicom]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Banana_(1986_video_game)", best: true, note: "правила: порядок плодів, банани-предмети, каміння, 105 етапів, редактор"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/バナナ_(ゲーム)", note: "JA: Mole Mole (1985) як основа, драбини, 3 життя, без таймера"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Banana+Famicom+1986+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, dig-terrain, gravity-fall, ladder-climb, collect-all, reach-exit, player-death, restart-level, inventory-items, wrap-edges, move-counter, sequential-levels, in-game-editor, editor-playtest, +ordered-collection, +delayed-fall, +step-penalty-score, +escort-npc]
proposes: ["+cond:next_in_order", "+card:ordered-collection", "+card:delayed-fall", "+card:step-penalty-score", "+card:escort-npc"]
author: opus
date: 2026-11-09
---

# Banana — кріт збирає їжу в правильному порядку, а камінь падає, щойно з-під нього вийдеш

## Суть
Кріт копає землю на нерухомому екрані, збирає всі плоди й овочі, забирає дружину і виходить у двері. Від [Boulder Dash](boulder-dash.md) — копання й падаюче каміння, але **ворогів і таймера нема**, а камінь не вбиває: він заважає, бо блокує шлях. Ядро — пазл на незворотність: плоди треба брати в заданому порядку, вниз копати легко, а вгору без драбини не вилізти, тож один хибний крок робить етап нерозвʼязним. Банани — особливі плоди, що дають предмет (бомбу, сегмент драбини, мотузку, камінь) для виходу із глухого кута.

## Поле і час
- Один нерухомий екран на етап (fixed-screen), вид збоку з гравітацією.
- Real-time рух без таймера і без ворогів — фактично покроковий пазл.
- Останні два етапи — тор по горизонталі: вихід за лівий край → правий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кріт (Mole) | player | 3 життя | копає землю; вгору — лише драбиною, не вище її верху |
| Земля | terrain | — | викопується; тримає камінь і крота |
| Камінь | object | стан: лежить / тремтить / падає | не штовхається; під ним пройшов → тремтить; вийшов з-під нього → падає разом зі стосом над ним; не вбиває |
| Плід / овоч | pickup | номер у порядку | зібрати всі; не по черзі — можна застрягти |
| Банан | pickup | предмет: бомба / драбина / мотузка / камінь | дає предмет для порятунку |
| Драбина | terrain | — | дає підйом; сегмент можна поставити з банана |
| Мотузка | terrain | — | з банана; спосіб пройти вертикаль (?) |
| Бомба | object | — | з банана; розчищає завал (?) |
| Дружина (Kiko) | neutral | — | треба «забрати» до виходу |
| Двері (вихід) | gate | — | вихід, коли все зібрано; камінь на дверях → глухий кут |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, earth|empty)` → ТО `move(mole, dir)`; земля → `set_cell(empty)`.
- КОЛИ `input(up)` → ЯКЩО `not cell(here, ladder)` → ТО `block`.
- КОЛИ `enter(mole, under rock)` → ТО `set_state(rock, shaking)`.
- КОЛИ `leave(mole, under rock)` → ЯКЩО `state(rock, shaking)` → ТО `fall(rock)` і всіх каменів стосу над ним.
- КОЛИ `contact(falling rock, mole)` → ТО `block` — камінь не вбиває (en-WP).
- КОЛИ `contact(mole, fruit)` → ЯКЩО `custom: «next_in_order: це наступний плід за порядком етапу»` → ТО `pickup`; інакше `custom: «порядок порушено — етап може стати нерозвʼязним»`.
- КОЛИ `contact(mole, banana)` → ТО `pickup`, `give(mole, bomb|ladder|rope|rock)`.
- КОЛИ `input(use)` → ЯКЩО `has(mole, item)` → ТО `place(item, here)`.
- КОЛИ `contact(mole, wife)` → ТО `custom: «дружина йде за кротом / зарахована»`.
- КОЛИ `all_gone(fruit)` and `custom: «дружину забрано»` → ТО `set_state(door, open)`.
- КОЛИ `contact(mole, door)` → ЯКЩО `state(door, open)` → ТО `win`, `score(-steps)`, `next_level`.
- КОЛИ `edge(mole)` → ЯКЩО `level(>=, 104)` → ТО `wrap(mole)`.
- КОЛИ `input(give_up)` → ТО `lives(-1)`, `restart` (застряг); 0 життів → `game_over`, «まいった!».
- Перемога: усе зібрано + двері. Поразка: лише «застряг» → рестарт за життя. Рахунок: кроки підсумовують у кінці етапу, більше кроків — менше очок.

## Керування і ввід
- Хрестовина: 4 напрямки; кнопка — застосувати предмет з банана (?).
- Рестарт етапу, коли застряг (?) — комбінація кнопок не знайдена.

## Вікна, меню, HUD
- `main-menu`: Гра · Edit-режим (`editor-window`).
- `game-screen`: один екран; HUD — `lives`, `score`, `move-counter` (?), предмет з банана (`inventory-bar`).
- `custom-window` «підсумок етапу»: кроки → очки.
- `editor-window`: розстановка всіх видів їжі, розмір мапи регулюється; одразу «грати».
- `end-screen`: game over.

## Фічі поза полем
- `levels-sequential`: 105 етапів, складність росте.
- `level-editor`: усі обʼєкти, регульований розмір мапи; збереження на касету Famicom Data Recorder; `editor-playtest` — грати відразу.
- `restart-level` за ціну життя.

## Варіації й родичі
- Основа — Mole Mole (1985, Victor / Cross Media Soft, ПК; переможець конкурсу ПЗ Harajuku 1984) і Mole Mole 2 (з «дитячим» режимом).
- Родичі: [Boulder Dash](boulder-dash.md) (копання й падіння), Lode Runner (вид екрана, драбини), [Mole Mania](mole-mania.md) (кріт-пазл), [Earth Shaker](earth-shaker.md) (без ворогів).
- **Осі варіацій**: падіння — «миттєве (BD) / після того, як гравець вийде з-під каменя (Banana)»; камінь — «вбиває / лише блокує»; порядок збору — «будь-який / заданий»; вертикаль для гравця — «вільна / лише драбиною».

## Цікавинки для курсу
- Камінь-«тремтун»: стан shaking і падіння всього стосу, коли гравець вийшов — 🌱.
- Збір у заданому порядку з перевіркою «наступний» — 🌱; плюс детектор глухого кута — 🥇.
- Незворотний рух (вниз легко, вгору лише драбиною) як основа пазла — 📎.
- Предмети-«рятівники» з бананів, що ставляться в клітину — 📎.
- Редактор з регульованим розміром мапи й миттєвим плейтестом — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `dig-terrain` · `gravity-fall` · `ladder-climb` · `collect-all` · `reach-exit` · `player-death` (3 життя) · `restart-level` · `inventory-items` ↔ предмети з бананів · `wrap-edges` (останні етапи) · `move-counter` · `sequential-levels` · `in-game-editor` + `editor-playtest`.
- **Нема** → пропозиції карток:
  - `+ordered-collection` «Збір у заданому порядку» · game-logic/win · 🌱 · слот {order}.
  - `+delayed-fall` «Падіння з затримкою» · entities/move · 🌱 · слот {trigger: leave|timer} — камінь тремтить, падає, коли під ним пусто.
  - `+step-penalty-score` «Кроки зменшують рахунок» · game-logic/score · 🌱.
  - `+escort-npc` «Забрати NPC до виходу» · game-logic/win · 📎.

## Пропозиції до словників
- `+cond:next_in_order(item)` — предмет наступний у заданій послідовності (Banana; кандидат для «збери 1→N»).

## Джерела
- ⭐ [Wikipedia (EN)](https://en.wikipedia.org/wiki/Banana_(1986_video_game)) — порядок збору, банани → 4 предмети, тремтіння й падіння каміння, 105 етапів, тор у двох останніх, штраф за кроки, редактор з касетою.
- [Wikipedia (JA)](https://ja.wikipedia.org/wiki/バナナ_(ゲーム)) — Mole Mole як основа, вгору лише драбиною, без ворогів і таймера, 3 життя.

## Непевне
- (?) Чи падає сам кріт (гравітація на гравця) — JA каже лише «вгору без драбини не можна».
- (?) Як працюють мотузка, бомба й камінь з банана; чи банан дає фіксований чи випадковий предмет.
- (?) Як «забирається» дружина і чи вона ходить за кротом.
- (?) Як здатися/рестартнути етап і чи це коштує життя; JA: «застряг» = фактично програш.
- (?) Порядок плодів показано на екрані чи його треба вгадати.
- (?) EN-WP: «камінь не вбиває»; JA описує, що камінь «перекриває шлях» — смерті від нього не згадує, але й не виключає.
