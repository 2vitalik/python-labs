---
title: Blockade (Блокада)
slug: blockade
aka: [Блокада, Gremlin Blockade]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: none
  goal: survive
year: 1976
platforms: [arcade (Gremlin), Noval 760]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Blockade_(video_game)", best: true, note: "правила, ліміт зіткнень 3–6, клони й нащадки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Surround_(video_game)", note: "Surround (Atari 2600, 1977): до 10 очок, 4 варіації правил"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=blockade+1976+gremlin+arcade+gameplay", note: "пошук; аркада"}
stage: v1
coverage: 75
mechanics: [move-auto, move-4dir, touch-death, impassable-cells, event-points, sound-effects, wrap-edges, progress-acceleration, move-8dir, rule-variants, ai-opponent, +trail-wall, +no-reverse-turn, +crash-count-limit, +shared-field-versus, +operator-settings, +trail-toggle]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+card:trail-wall", "+card:crash-count-limit", "+card:shared-field-versus", "+card:trail-toggle"]
author: opus
date: 2026-11-09
---

# Blockade — перша «змійка»: дві стрілки лишають стіни, хто врізався — дає очко суперникові

## Суть
Два гравці керують стрілками, що безупинно рухаються по полю й лишають за собою суцільний слід із блоків. Слід — назавжди стіна; врізався в будь-яку стіну (свою, чужу чи рамку) — суперник отримує очко. Гра закінчується, коли в когось набереться задана оператором кількість аварій (3–6). Це родоначальник жанру Snake і предок Tron Light Cycles.

## Поле і час
- Клітинне поле в рамці-барʼєрі; клітина = один блок сліду.
- Real-time: обидві стрілки роблять крок одночасно на кожен тік; під час руху лунають електронні «біпи».
- Раунд триває до першої аварії; після неї поле очищається і починається новий раунд (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стрілка гравця 1 / 2 | player | напрям | щотік крок уперед; кнопки задають новий напрям з 4 |
| Слід (блоки) | static | власник | клітина, яку пройшла стрілка; стіна до кінця раунду |
| Барʼєр (рамка) | static | — | дотик = аварія |
| Лічильник аварій / очок | — | ліміт 3–6 (оператор) | досягнув ліміту → кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(arrow, dir)`, `custom: «клітина позаду стає блоком сліду»` (`+effect:leave_trail`).
- КОЛИ `input(dir)` → ЯКЩО `not moving(arrow, opposite(dir))` → ТО `face(arrow, dir)` (?).
- КОЛИ `contact(arrow, trail|barrier)` → ТО `sound(explosion)`, `flash`, `score(+1)` суперникові, `custom: «новий раунд, сліди зникають»` (?).
- КОЛИ `contact(arrow_1, arrow_2)` → ТО `custom: «аварія обох (?)»`.
- КОЛИ `counter(crashes, ==, limit)` → ТО `game_over`; переможець — суперник.
- Перемога: менше аварій до ліміту · Поразка: набрати ліміт аварій · Рахунок: очко за аварію суперника.

## Керування і ввід
- Кожен гравець має блок кнопок напрямків (вгору/вниз/ліворуч/праворуч) — абсолютні напрямки, не «ліво/право відносно руху».
- Обидва грають одночасно за одним автоматом.

## Вікна, меню, HUD
- `game-screen`: поле з рамкою, рахунок обох гравців угорі (?).
- `attract-demo` — автомат у режимі очікування (?).
- `end-screen` — після досягнення ліміту аварій (?).
- HUD: `score` ×2; звук — біпи руху і вибух при аварії.

## Фічі поза полем
- `operator-settings`: оператор автомата обирає ліміт аварій від 3 до 6.
- Більше налаштувань і режимів нема; одиночної гри проти AI в оригіналі нема (?).

## Варіації й родичі
- CoMotion (Gremlin, 1976) — версія на 4 гравців; клони: Dominos (Atari), Barricade (Ramtek), Checkmate (Bally), Bigfoot Bonkers (Meadows).
- Surround (Atari 2600, 1977): гра до 10 очок, режим проти компʼютера і варіації Speed Up (прискорення з часом), Diagonal Movement (8 напрямків), Erase (кнопка тимчасово не лишає слід), Wraparound (тор).
- Нащадки: Tron Light Cycles (див. `tron-light-cycles`), Snake (див. `snake` — хвіст рухається), Achtung, die Kurve! (див. `achtung-die-kurve` — вільний кут і дірки).
- **Осі варіацій:** гравців 2 / 4 · напрямки 4 / 8 · слід вічний / з «гумкою» · краї стіна / тор · швидкість стала / зростає · мета ліміт аварій / перший до 10.

## Цікавинки для курсу
- Слід = стіна з двома одночасними гравцями на одній клавіатурі — 🌱: найпростіша real-time PvP.
- Одночасність кроків: що як обидва входять в одну клітину в той самий тік — 📎: явне правило розвʼязання колізій.
- Варіації Surround як перемикачі правил (тор, діагональ, гумка, прискорення) — 🥉: `rule-variants` на одному рушії.
- Простий AI «обирай напрям із найбільшою вільною площею» (flood fill) — 🥉.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` · `touch-death` · `impassable-cells` · `event-points` · `sound-effects` · (Surround) `wrap-edges`, `move-8dir`, `progress-acceleration`, `ai-opponent`, `rule-variants`.
- **Нема** → пропозиції карток:
  - `+trail-wall` (запропоновано в `tron-light-cycles`).
  - `+no-reverse-turn` (запропоновано в `snake`).
  - `+crash-count-limit` «Гра до N аварій» · game-logic/lose · 🌱 · слот {limit: 3–6}.
  - `+shared-field-versus` «Кілька гравців на одному полі одночасно» · game-logic/opponent · 📎 — на відміну від `simultaneous-versus` (два поля).
  - `+trail-toggle` «Кнопка тимчасово вимикає слід» · entities/move · 🌱 (Surround Erase).
  - `+operator-settings` — DIP-налаштування оператора (слово вже 🔥 у features.md; картки нема).

## Пропозиції до словників
- `+effect:leave_trail` — клітина позаду стає слідом власника (підтверджую пропозицію з `tron-light-cycles`).
- `+effect:clear_trail` — прибрати сліди між раундами.
- `+card:trail-wall`, `+card:crash-count-limit`, `+card:shared-field-versus`, `+card:trail-toggle`.

## Джерела
- ⭐ [Wikipedia: Blockade (video game)](https://en.wikipedia.org/wiki/Blockade_(video_game)) — дві стрілки, слід блоків, аварія = очко суперникові, ліміт 3–6 від оператора, CoMotion і клони.
- [Wikipedia: Surround](https://en.wikipedia.org/wiki/Surround_(video_game)) — до 10 очок, гра проти компʼютера, 4 варіації.
- YouTube: пошук «blockade 1976 gremlin arcade gameplay».

## Непевне
- (?) Чи очищається поле після кожної аварії, чи сліди накопичуються — Wikipedia не каже прямо.
- (?) Чи можна розвернутися на 180° (у себе ж) і що буває при зіткненні лоб у лоб.
- (?) Наявність attract-режиму й екрана кінця гри; розміщення рахунку.
- (?) Розмір поля і швидкість руху — у джерелах нема.
