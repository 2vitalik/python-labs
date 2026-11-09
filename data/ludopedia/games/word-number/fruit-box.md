---
title: Fruit Box (Apple Game)
slug: fruit-box
aka: [Apple Game, Fruits Box, Make 10]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: score
year: null
platforms: [web (Flash → HTML5), mobile browser]
links:
  - {kind: official, url: "https://en.gamesaien.com/game/fruit_box/", best: true, note: "оригінал Game Saien: грати; «обведи мишею яблука з сумою 10», 1 очко за яблуко, опція Light Colors"}
  - {kind: other, url: "https://playpile.gg/games/fruit-box", note: "картка гри: HTML5, таймер, розробник GameSaien"}
  - {kind: other, url: "https://oshizi.com/research/analyzing-board-generation/", note: "аналіз генератора: 17×10, цифри 1–9 рівномірно, сума поля кратна 10"}
  - {kind: other, url: "https://oshizi.com/blog/solving-apple-game-optimally/", note: "оптимальний розвʼязок: B&B, ILP, greedy і beam search; NP-подібна структура"}
  - {kind: other, url: "https://oshizi.com/apple-game-plus/", note: "клон Apple Game Plus: раунд 2 хв, мультиплеєр до 512 гравців на одному полі"}
  - {kind: other, url: "https://github.com/kevinychen/fruit-box-bot", note: "бот Python + Rust; ідеальний рахунок 170"}
  - {kind: itch, url: "https://pancelor.itch.io/make-ten", note: "Make Ten — оммаж: 2 хв; Deluxe — без таймера, daily, гравітація"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fruit+box+apple+game+sum+10", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [multi-select, selection-highlight, time-out, event-points, completion-detection, game-screen, game-settings, +rect-sum-clear, +empty-cells-zero, +board-sum-multiple, +shared-board-race]
proposes: ["+ui:selection-rect", "+ui:time-bar", "+feature:light-colors", "+card:rect-sum-clear", "+card:empty-cells-zero", "+card:board-sum-multiple"]
author: opus
date: 2026-11-09
---

# Fruit Box — 170 яблук-цифр і дві хвилини: обведи прямокутником групу з сумою рівно 10, і вона зникне

## Суть
Поле 17×10 заповнене яблуками з цифрами 1–9. Гравець тягне мишею прямокутник; якщо цифри всередині дають у сумі рівно 10, ці яблука зникають і дають по очку. Порожні місця лишаються дірками (нічого не падає), тож пізніше прямокутник може «перестрибнути» через порожнечу до далеких цифр. За 120 секунд треба зняти якомога більше; ідеал — 170, але не на кожному полі він можливий.

## Поле і час
- Сітка 17×10 = 170 клітин, у кожній — яблуко з цифрою 1–9 (за аналізом — незалежно й рівномірно).
- Сума всього поля кратна 10 (вимога генератора за аналізом oshizi); ідеальна очистка все одно не гарантована — бот перезапускає поле, доки 170 стане можливим.
- Шари: клітина (яблуко / порожньо) + прямокутник виділення поверх.
- Час: реальний, раунд 2 хвилини; хід = один прямокутник, без обмеження кількості.
- Гравітації нема: знята клітина назавжди порожня.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Яблуко | tile | цифра 1–9 | потрапляє у виділення; зникає разом з групою, що дає 10 |
| Порожня клітина | terrain | значення 0 | лишається після яблука; у прямокутнику нічого не додає (?) |
| Прямокутник виділення | mark | кут натиску + кут курсора | вибирає яблука всередині; знімається при відпусканні |
| Таймер раунду | zone | 120 с | спадає безперервно; 0 — кінець |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `spawn(яблуко × 170)` у сітці 17×10, `custom: «цифри 1–9; сума поля кратна 10»`, `timer(start, 120)`.
- КОЛИ `input(press + drag)` → ТО `custom: «малюється прямокутник від точки натиску до курсора; яблука всередині підсвічуються»`.
- КОЛИ `input(drag)` → ТО `custom: «яблуко вибране, якщо його центр усередині прямокутника»` (?).
- КОЛИ `input(release)` → ЯКЩО `sum(selection, 10)` → ТО `clear(selection)`, `score(+1)` за кожне яблуко; інакше `custom: «виділення зникає без наслідків»`.
- КОЛИ `input(release)` → ЯКЩО `occupied(cell_in_rect, empty)` → ТО `custom: «порожня клітина додає 0»` (?) — тому прямокутник через дірки зʼєднує далекі цифри.
- Одне яблуко не дає 10 (цифри 1–9), тож кожен успішний хід знімає ≥ 2 яблука; 9 знімається лише з 1 (або з 1 через порожнечу).
- КОЛИ `after(clear)` → ТО `custom: «нічого не падає і не зсувається»`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`, `custom: «показати рахунок»`.
- КОЛИ `all_gone(яблуко)` → ТО `game_over` (ідеал — 170).
- КОЛИ `no_moves` → ТО `custom: «раунд не завершується сам — таймер добігає»` (?).
- КОЛИ `input(Light Colors)` → ТО `custom: «світліша палітра яблук і поля»`.
- Перемога: нема — рекорд · Поразка: нема · Рахунок: кількість знятих яблук (макс. 170).

## Керування і ввід
- Миша: натиснути, протягнути прямокутник, відпустити — подати; тач на мобільному браузері — так само пальцем.
- Перед грою — чекбокс Light Colors, кнопка старту (?).
- Клавіатури й undo нема.

## Вікна, меню, HUD
- `game-screen`: поле 17×10, прямокутник виділення (`selection-rect`), `score`, смуга часу (`time-bar`) (?).
- `settings-window`-елемент на тій самій сторінці: Light Colors.
- `end-screen`: рахунок після 120 с (?).
- Переходи: сторінка гри → старт → `game-screen` → час вийшов → рахунок → знову (?).

## Фічі поза полем
- `light-colors`: світла палітра як доступність.
- Офіційного лідерборду, daily чи режимів у джерелах нема; їх додають клони (див. нижче).

## Варіації й родичі
- Make Ten (pancelor) — оммаж: 2 хв; Deluxe — режим без таймера, daily, режими з гравітацією та ще 35+ правил.
- Apple Game Plus (oshizi) — той самий генератор; мультиплеєр до 512 гравців на одному полі: хто зняв більше, той виграв (`shared-board-race`).
- [number-match.md](number-match.md) — пари з сумою 10 у лінії з переходом рядків; [sumplete.md](sumplete.md) — суми рядів через викреслення; [nyt-digits.md](nyt-digits.md) — арифметика до цілі; [countdown-numbers.md](countdown-numbers.md).
- Сусід з `pencil-logic`: Shikaku — прямокутники заданої площі; тут прямокутник заданої суми.
- **Осі варіацій:** форма виділення (прямокутник / пара / шлях) · ціль (рівно 10 / кратне / задане число) · порожнеча (0 / розриває виділення) · гравітація (нема / падіння) · час (120 с / без таймера / daily) · гравці (соло / одне поле на сотні).

## Цікавинки для курсу
- Сума в прямокутнику за O(1) через 2D-префіксні суми — 🌱 (класика обчислювальної геометрії сітки).
- Виділення drag-прямокутником з підсвіткою «що всередині» — 🌱.
- Генератор: 170 цифр, сума кратна 10, оцінка, чи можлива повна очистка — 🥈.
- Жадібний бот проти beam search: максимізувати знятих за порядком ходів (кожен хід змінює наступні легальні) — 🥇.
- Точний розвʼязувач (B&B / ILP) для малих полів і доказ складності — 👑 (відкрите питання NP-повноти).
- Мультиплеєр на одному полі: конфлікт двох одночасних виділень — 🥈.

## Мапа на каталог
- Є: `multi-select` ↔ прямокутне виділення · `selection-highlight` · `time-out` ↔ 120 с · `event-points` ↔ 1 за яблуко · `completion-detection` ↔ поле порожнє · `game-screen` · `game-settings` ↔ Light Colors.
- **Нема** → пропозиції карток:
  - `+rect-sum-clear` «Прямокутник із сумою рівно N знімає клітини» · entities/interact · 🌱 · слоти {target: 10}.
  - `+empty-cells-zero` «Порожні клітини у виділенні дають 0» · game-logic/constraints · 🌱.
  - `+board-sum-multiple` «Генератор: сума поля кратна цілі» · levels/generation · 🌱.
  - `+shared-board-race` «Багато гравців знімають з одного поля» · game-logic/opponent · 🥈 (клони).

## Пропозиції до словників
- `+ui:selection-rect` — прямокутник виділення поверх поля; `+ui:time-bar` — смуга часу, що спадає.
- `+feature:light-colors` — світла палітра (опція доступності).
- `+card:rect-sum-clear`, `+card:empty-cells-zero`, `+card:board-sum-multiple`.

## Джерела
- ⭐ [Game Saien: Fruit Box](https://en.gamesaien.com/game/fruit_box/) — оригінал у браузері: правило суми 10, 1 очко за яблуко, Light Colors.
- [oshizi: аналіз генерації](https://oshizi.com/research/analyzing-board-generation/) — 17×10, 1–9 рівномірно, сума кратна 10.
- [oshizi: оптимальний розвʼязок](https://oshizi.com/blog/solving-apple-game-optimally/) — формалізація, B&B, beam search.
- [oshizi: Apple Game Plus](https://oshizi.com/apple-game-plus/) — 2 хв, мультиплеєр.
- [kevinychen/fruit-box-bot](https://github.com/kevinychen/fruit-box-bot) — бот, ідеал 170, перезапуск поля до можливого ідеалу.
- [pancelor: Make Ten](https://pancelor.itch.io/make-ten) — оммаж, 2 хв, Deluxe-режими.
- [PlayPile: Fruit Box](https://playpile.gg/games/fruit-box) — картка гри.

## Непевне
- (?) Тривалість 120 с — з клонів і оммажів (oshizi, pancelor), сторінка Game Saien часу не називає.
- (?) Правило «центр яблука всередині прямокутника» — з опису клону; як рахує оригінал, не перевірено.
- (?) Що порожні клітини в прямокутнику дозволені й дають 0 — з опису клону; аналіз oshizi формулює ходи без цього.
- (?) Кнопки Reset / BGM, вигляд екрана результату, чи гра закінчується, коли ходів нема.
- (?) Рік виходу й платформа Flash: сайт Game Saien датований ©2007–2024; ModDB-сторінка (лінк черги) — 403.
- (?) Корейська назва «사과 게임» і популярність у Кореї — у відкритих джерелах не підтверджено.
