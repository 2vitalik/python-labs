---
title: Upwords
slug: upwords
aka: [Scrabble Upwords, Topwords, Crucimaster, Betutorony, Palabras Arriba, Stapelwoord]
family: word-number
also: [board-digital]
klass: cursor
axes:
  field: layers
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 1981
platforms: [board, PC, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Upwords", best: true, note: "правила: стос до 5, заборона накрити все слово, очки 2/1, Qu, бонус 20, штраф −5; розподіл плиток 8×8 і 10×10"}
  - {kind: official, url: "https://instructions.hasbro.com/en-us/instruction/upwords-game", note: "сторінка Hasbro: склад (100 плиток, 4 тримачі), 2–4 гравці; повні правила — у PDF"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=upwords", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=upwords+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [height-levels, word-validation, turn-enforcement, hot-seat, ai-opponent, pass-turn, event-points, leftover-penalty, score-records, drag-drop-piece, legal-move-highlight, game-screen, end-screen, help-window, settings-window, +tile-rack, +tile-bag-draw, +line-placement, +cross-word-scoring, +bingo-bonus, +tile-exchange, +stack-overwrite, +stack-height-scoring, +stack-limit]
proposes: ["+cond:stack_height", "+cond:keeps_tile", "+effect:stack", "+ui:stack-height-badge", "+card:stack-overwrite", "+card:stack-height-scoring"]
author: opus
date: 2026-11-09
---

# Upwords — Scrabble у висоту: літеру можна покласти поверх чужої, змінивши слово; стос до 5

## Суть
Як у Scrabble, гравці по черзі викладають на спільну дошку слова з 7 плиток руки. Головна відмінність — плитку можна класти **поверх** наявної, перетворюючи слово (CATER → LATER) без розширення поля; висота стосу до 5. Нема премійних клітин: слово без надбудов дає 2 очки за плитку, слово зі стосами — за загальною висотою. Ядро — поле як 2.5D (сітка + висота), де «редагування» слова суперника — легальний хід.

## Поле і час
- Дошка 8×8 (оригінал, 64 плитки) або 10×10 (Hasbro Europe, 100 плиток; світова версія). Старт — одна з центральних клітин e5, e6, f5, f6 (8×8).
- Шари: клітина має стос висотою 0–5; видно верхню літеру і висоту.
- Хід = одна дія гравця (викласти / обміняти одну плитку / пас), за годинниковою стрілкою.
- Прихована інформація: руки суперників і порядок у мішку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера; усі вартості однакові | мішок → рука → поле; на полі може бути накрита іншою |
| Плитка Qu | tile | 1 плитка = 2 літери | у слові без стосів дає бонус |
| Стос | zone | висота 1–5, верхня літера | читається лише верх; висота йде в очки |
| Мішок (купа) | container | 64 / 100 плиток | видає плитки наосліп |
| Рука (тримач) | container | 7 плиток | поповнюється до 7 після ходу |
| Центральні клітини | zone | 4 клітини (8×8) | перше слово мусить зачепити одну |
| Гравець | player | рахунок, рука | 2–4 сторони |

Розподіл 8×8: F J K Qu V W X Z ×1 · B C G H R Y ×2 · D L M N P S U ×3 · I O T ×4 · A ×5 · E ×6. Розподіл 10×10: J Qu V X Z ×1 · K W Y ×2 · B F G H P ×3 · C ×4 · D L M N R T U ×5 · S ×6 · A I O ×7 · E ×8.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен тягне плитку; найближчий до A ходить першим; плитки назад»`, `give(each, 7 tiles)`.
- КОЛИ `input(play)` → ЯКЩО перший хід → ТО слово мусить покрити центральну клітину.
- КОЛИ `input(play)` → ЯКЩО `legal(move)` → ТО `place(player, tiles)`, `score(…)`, `give(player, draw до 7)`, `end_turn`; інакше `block`.
- `legal(move)`: усі плитки ходу в одному рядку або стовпці, суцільною лінією; слова читаються зліва направо і зверху вниз; кожне утворене слово — `in_dictionary`.
- КОЛИ `input(place on stack)` → ЯКЩО `custom: «висота стосу < 5»` → ТО `custom: «плитка лягає зверху, висота +1»`; інакше `block`.
- КОЛИ `input(place on stack)` → ЯКЩО `same(tile, top, letter)` → ТО `block` — не можна класти літеру на таку саму.
- КОЛИ `input(play)` → ЯКЩО `custom: «накрито всі літери наявного слова»` → ТО `block` — хоча б одна плитка/стос слова лишається незмінною.
- Заборонені слова: власні назви, з дефісом/апострофом, абревіатури, несамостійні префікси й суфікси; плюралізація додаванням S — лише якщо S одночасно частина іншого цілого слова цього ходу.
- КОЛИ ходом змінено два слова одночасно → ЯКЩО `not in_dictionary(any)` → ТО `block`.
- Очки: слово без стосів (усі висоти 1) → `score(2 × плиток)`; слово зі стосами → `score(1 × кожна плитка в кожному стосі слова)`.
- КОЛИ `custom: «Qu у слові без стосів»` → ТО `score(+2)`.
- КОЛИ `count(tiles_played, ==, 7)` → ТО `score(+20)`.
- КОЛИ `input(exchange)` → ТО `take(player, 1 tile)`, `give(player, 1 tile)`, `end_turn` — замість ходу.
- КОЛИ `input(pass)` → ТО `pass_turn`.
- КОЛИ `custom: «мішок порожній»` → ЯКЩО `custom: «рука гравця порожня»` or `custom: «усі пасували за коло»` → ТО `game_over`.
- КОЛИ `game_over` → ТО `score(−5 × плиток у руці)` кожному.
- Перемога: найбільше очок · Поразка: менше · Нічия: однакові очки (?).

## Керування і ввід
- Настільна: кладеш плитки з тримача на дошку чи поверх стосів; гумові ніжки й рельєф тримають стоси.
- Цифрова (iOS 2013, Android 2014; ранній Microsoft-порт 1990-х): drag плитки з руки на клітину або на стос; кнопки Play / Swap / Pass / Shuffle (?); висота показується числом/тінню.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: дошка з `stack-height-badge` на кожному стосі, `tile-rack`, рахунки, `turn-indicator`, `tiles-left`, превʼю очок ходу (?).
- (цифрова версія) `main-menu`: гра проти AI · hot-seat / онлайн (?) · `help-window`.
- (цифрова версія) `end-screen`: фінальний рахунок зі штрафами.
- Переходи: `main-menu` → `game-screen` → `game_over` → `end-screen`.

## Фічі поза полем
- `ai-opponent-levels` (?) у застосунках · `hotseat` у настільній.
- `custom-rules`: варіант кінця гри (деякі видання — лише коли всі пасують або всі плитки зіграні).
- Розмір поля 8×8 / 10×10 залежить від видання.

## Варіації й родичі
- Scrabble (`scrabble.md`) — та сама рука/мішок/лінія, але премії замість висоти і плитки незмінні.
- Letterpress (`letterpress.md`) — теж «переписує» поле, але кольором власності, не висотою.
- Mathable (`mathable.md`) — числова рука-мішок на дошці.
- **Осі варіацій:** розмір (8×8 / 10×10) · ліміт стосу (5 / без) · очки (висота / вартість літер / премії) · заборона «накрити все слово» · правило S-множини.

## Цікавинки для курсу
- Поле як `list[list[list[str]]]` (стос на клітині) і рендер верхньої літери + висоти — 🌱.
- Перевірка ходу: одна лінія, суцільність, ліміт 5, заборона тієї самої літери і «накрити все» — 📎.
- Збір усіх утворених слів (головне + перпендикулярні) і рахунок 2/1 з бонусами — 🥉.
- AI: перебір ходів з урахуванням надбудов (комбінаторно більше за Scrabble) — 🥇.
- Кінець гри і штраф за залишок — 🌱.

## Мапа на каталог
- Є: `height-levels` ↔ стос як висота клітини · `word-validation` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `pass-turn` · `event-points` ↔ 2/1 за плитку · `leftover-penalty` ↔ −5 за плитку · `score-records` · `drag-drop-piece` · `legal-move-highlight` · `game-screen` · `end-screen` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+tile-rack`, `+tile-bag-draw`, `+line-placement`, `+cross-word-scoring`, `+bingo-bonus`, `+tile-exchange` — див. `scrabble.md`.
  - `+stack-overwrite` «Плитка лягає поверх, змінюючи літеру клітини» · entities/legality · 📎 · слоти {max_height}.
  - `+stack-height-scoring` «Очки слова за висотою стосів» · game-logic/score · 🌱.
  - `+stack-limit` «Ліміт висоти стосу» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:stack_height` — висота стосу клітини порівняно з N (Upwords; висоти в тактиках).
- `+cond:keeps_tile` — хід лишає незмінною хоча б одну плитку наявного слова.
- `+effect:stack` — покласти плитку поверх наявної, висота +1 (на відміну від `place` у порожню).
- `+ui:stack-height-badge` — число висоти на клітині.
- `+card:stack-overwrite`, `+card:stack-height-scoring` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Upwords](https://en.wikipedia.org/wiki/Upwords) — правила, розподіл 8×8/10×10, очки, кінець гри, назви, автор Elliot Rudell, Milton Bradley.
- [Hasbro: Upwords Game](https://instructions.hasbro.com/en-us/instruction/upwords-game) — склад: 100 плиток, 4 тримачі, 2–4 гравці, «чим вище стос, тим більше очок»; правила в PDF.
- BGG і YouTube — пошукові URL.

## Непевне
- (?) Очки слова зі стосами: Wikipedia пише «1 point per tile», але її приклад BELATED = 9 очок при 7 літерах — тобто рахується кожна плитка в стосах (сума висот); прийняв це тлумачення.
- (?) Рік: категорія Wikipedia — 1981, інфобокс — 1982.
- (?) Сучасні правила Hasbro (10×10) можуть відрізнятись бонусами — PDF не відкривав.
- (?) Інтерфейс цифрових версій (кнопки, превʼю очок, онлайн) — не бачив.
- (?) Тай-брейк при рівних очках — у джерелі нема.
