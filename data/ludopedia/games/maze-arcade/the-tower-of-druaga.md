---
title: The Tower of Druaga
slug: the-tower-of-druaga
aka: [ドルアーガの塔, Tower of Druaga, Druaga]
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1984
platforms: [arcade, Famicom, MSX, PC Engine, FM-7, X1, Game Boy, Windows, Virtual Console, Arcade Archives, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Tower_of_Druaga", best: true, note: "60 поверхів, ключ і двері, прихований скарб на кожному поверсі, меч і щит, Will-o-Wisps за затримку, кирка/чоботи/свічка"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ドルアーガの塔", note: "JA: детальна механіка — меч-утримання, щит, HP-обміни, умови скарбів, таймер 20000 → червоний 60, ZAP, 59-й поверх з приманками, рахунок, продовження"}
  - {kind: strategywiki, url: "https://strategywiki.org/wiki/The_Tower_of_Druaga/Monsters", note: "монстри аркадної версії, вогники при червоному таймері (бачив у пошуку; агентам закрито)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tower+of+Druaga+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, key-and-door, reach-exit, stairs-levels, maze-generation, hp-damage, melee-vs-ranged, projectile-shot, line-of-sight-attack, touch-death, player-death, item-pickup, inventory-items, destructible-blocks, timeout-punisher, time-bonus, event-points, extra-life-threshold, game-over-continue, level-select, sequential-levels, game-screen, +secret-condition-treasure, +shield-facing-block, +sword-drawn-state, +item-tier-replace, +reveal-invisible, +ghost-phase, +required-item-chain, +zap-demotion, +boss-fight, +decoy-boss-sequence, +limited-use-tool]
proposes: ["+trigger:secret_met", "+effect:zap", "+ui:timer-color-phase", "+card:secret-condition-treasure", "+card:shield-facing-block", "+card:sword-drawn-state", "+card:item-tier-replace", "+card:required-item-chain", "+card:zap-demotion", "+card:decoy-boss-sequence", "+card:limited-use-tool"]
author: opus
date: 2026-11-09
---

# The Tower of Druaga — 60 поверхів-лабіринтів: ключ, двері й прихований скарб, що зʼявляється лише від таємної дії

## Суть
Лицар Гільгамеш (Гіл) проходить 60 поверхів башти: на кожному — лабіринт, ключ, двері нагору й захована скриня зі скарбом. Скриня зʼявляється лише після таємної дії, своєї на кожному поверсі (вбити N певних ворогів, стати в певне місце, натиснути Start, посмикати важіль). Частина скарбів обовʼязкова: без них не вбити приманки й Друагу на 59-му, і гра стає непрохідною. Бій — не атака кнопкою, а «наїзд» з витягнутим мечем з обміном HP, а щит ловить закляття, лише якщо повернутий до них.

## Поле і час
- Кожен поверх — прямокутний лабіринт на сітці коридорів із зовнішньою стіною; лабіринти випадкові на кожне проходження (EN-вікі), позиції ворогів на старті поверху — випадкові (JA-вікі).
- Гіл стартує біля дверей попереднього поверху; скриня, коли зʼявиться, — у точці старту (EN-вікі).
- Real-time. Таймер поверху стартує з 20000 (білий) і спадає; на нулі стає червоним і йде від 60; червоний нуль — міс (JA-вікі).
- Видимість повна, крім привидів (невидимі без свічки) і самої скрині до виконання умови.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гільгамеш | player | HP, меч, щит, обладунок | рух 4 напрямки коридорами; меч витягнутий, поки затиснута кнопка |
| Ключ | pickup | 100 очок | потрібен для дверей |
| Двері | gate | — | з ключем — на наступний поверх |
| Скриня зі скарбом | container | умова поверху | прихована; зʼявляється за таємною дією; дає предмет (деякі шкідливі) |
| Стіна | static | внутрішня / зовнішня | внутрішню ламає кирка; зовнішню — ні |
| Слайм | enemy | 1 удар | повзе лабіринтом; гине від одного проходу мечем |
| Лицар | enemy | HP, кілька ударів | обмін ударами: кожен прохід мечем знімає HP обом |
| Маг | enemy | закляття | кидає закляття по лабіринту; блокується щитом |
| Привид | enemy | невидимий без свічки | дух мага, проходить крізь стіни; дотик не шкодить |
| Ропер | enemy | — | дотик скидає HP Гіла до мінімуму; без меча повторний дотик — міс |
| Дракон (Квокс та ін.) | enemy | вогонь | дихає вогнем — міс; дотик висмоктує HP |
| Вогняний елементаль | enemy | — | його вогонь — міс, крім намиста |
| Блукаючий вогник (синій / червоний) | enemy | невбивний | зʼявляється, коли таймер червоний; синій повертає ліворуч, червоний — праворуч; дотик — міс; кільце робить безпечним |
| Сукуба (57-й) | enemy | камʼяна на старті | меч вбиває; дотик без меча швидко знімає HP |
| Друага | boss | ≈10+ проходів мечем | 59-й поверх; стріляє закляттям крізь стіни, на одній лінії з Гілом телепортується до нього; вразливий лише з усіма обовʼязковими предметами |
| Приманки Друаги (Гіпер-лицар, 4 чарівники, Квокс) | boss | по черзі | гіпер-лицар вирівнюється з Гілом і таранить; з 4 чарівників справжній один; Квокса вбиває лише рубінова булава |
| Кі | neutral | 60-й поверх, скамʼяніла | мета гри; удар мечем — ZAP |
| Іштар (ілюзія) | neutral | 60-й поверх | удар мечем — ZAP |
| Кирка (mattock) | pickup | 2–5 використань | ламає внутрішню стіну; удар у зовнішню ламає кирку |
| Свічка | pickup | на кілька поверхів / назавжди | показує привидів |
| Намисто | pickup | 27-й або 46-й | вогонь елементаля й драконів не шкодить |
| Кільце | pickup | 21-й, 39-й, 54-й | відповідний вогник безпечний |
| Зілля лікування / висмоктування | pickup | — | лікує (лише вперше) / скидає HP майже до мінімуму |
| Синій обладунок | pickup | 52-й | переживає одне закляття, HP — до мінімуму |
| Рубінова булава | pickup | обовʼязкова | вбиває приманку-Квокса одним ударом |
| Закляття | projectile | — | летить коридором; щит у бік закляття — блок, інакше міс |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(button)` → ТО `set_state(gil, sword_drawn)`; КОЛИ `custom: «кнопку відпущено»` → ТО `clear_state(gil, sword_drawn)`; у момент витягання/ховання Гіл беззахисний.
- КОЛИ `contact(gil, enemy)` → ЯКЩО `state(gil, sword_drawn)` → ТО `damage(enemy, n)`, `damage(gil, m)` — обмін ударами; слайм гине за раз, лицар — за кілька.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `score(0–5000)`.
- КОЛИ `contact(spell, gil)` → ЯКЩО `facing(shield, spell)` → ТО `disappear(spell)`, `score(10–40)`; інакше `lives(-1)`. Щит дивиться вперед, коли меч сховано, і ліворуч, коли витягнуто.
- КОЛИ `contact(gil, roper|druaga)` → ТО `hp(gil, min)`; ЯКЩО `not state(gil, sword_drawn)` and `custom: «дотик повторно»` → ТО `lives(-1)`.
- КОЛИ `contact(gil, dragon)` → ТО `hp(gil, -n)` щотік; КОЛИ `contact(gil, fire)` → ЯКЩО `not has(gil, necklace)` → ТО `lives(-1)`.
- КОЛИ `contact(gil, wisp)` → ЯКЩО `not has(gil, ring[wisp])` → ТО `lives(-1)`.
- КОЛИ `hp_zero(gil)` → ТО `lives(-1)`.
- КОЛИ `contact(gil, key)` → ТО `pickup`, `score(100)`.
- КОЛИ `contact(gil, door)` → ЯКЩО `has(gil, key)` → ТО `score(timer_left)` (якщо таймер не червонів), `next_level`; інакше `block`.
- КОЛИ `custom: «виконано таємну умову поверху»` → ТО `spawn_at(treasure_box, start_point)`. Приклади умов: `counter(kills[type], ==, n)`; `reach(gil, cell)`; `input(start)`; `custom: «важіль у кожен бік N разів»`; `blocked(gil)` об нижню зовнішню стіну (11-й) чи об ліву й праву (16-й); блок закляття з витягнутим мечем.
- КОЛИ `contact(gil, treasure_box)` → ТО `give(gil, item)`; ЯКЩО `has(gil, same_category)` → ТО `custom: «старший предмет заміняє молодший: зелений → червоний → синій»`.
- КОЛИ `input(button)` → ЯКЩО `has(gil, mattock)` and `blocked(gil)` → ТО `set_cell(wall, floor)`, `counter(mattock_uses, -1)`; ЯКЩО `cell(wall, outer)` → ТО `block`, `take(gil, mattock)`.
- КОЛИ `tick` → ЯКЩО `has(gil, candle)` → ТО `reveal(ghosts)`; інакше `hide(ghosts)`.
- КОЛИ `counter(timer, ==, 0)` → ТО `custom: «таймер червоніє і йде від 60»`, `spawn_at(wisp, maze)` повторно, поки червоний (StrategyWiki).
- КОЛИ `counter(red_timer, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `tick` → ТО вогники: `custom: «синій повертає ліворуч, червоний — праворуч»`; привиди: `custom: «крізь стіни»`.
- 59-й поверх: КОЛИ `level_start` → ТО `spawn(hyper_knight)`; КОЛИ `destroyed(hyper_knight)` → ТО `spawn(wizard×4)` (справжній один); КОЛИ `destroyed(real_wizard)` → ТО `disappear(other_wizards)`, `spawn(quox_decoy)`; КОЛИ `contact(gil, quox_decoy)` → ЯКЩО `has(gil, ruby_mace)` → ТО `disappear(quox_decoy)`, `spawn(druaga)`.
- КОЛИ `contact(gil, druaga)` → ЯКЩО `state(gil, sword_drawn)` and `custom: «усі обовʼязкові предмети»` → ТО `damage(druaga, 1)`; інакше `custom: «невразливий»`.
- КОЛИ `line_of_sight(druaga, gil)` → ТО `teleport(druaga, ближче до gil)`.
- ZAP: КОЛИ `contact(gil, door)` на 59-му → ЯКЩО `not custom: «Друага переможений»` → ТО `custom: «YOU ZAPPED TO…»`, `take(gil, some_items)`, `teleport(gil, випадковий поверх 6–18)`; на 60-му — так само за злам стіни, удар мечем по Кі чи Іштар, міс або час.
- КОЛИ `custom: «Кі врятовано на 60-му»` → ТО `score(500000)`, `win`, `game_over` (фінал).
- КОЛИ `counter(score, >=, 50000)` → ТО `lives(+1)` (один раз).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`; КОЛИ `input(coin + button + start)` → ТО `window(level-select)` — старт з будь-якого поверху ≤ найвищого досягнутого, предмети зберігаються.
- Перемога: пройти 60 поверхів і врятувати Кі (без обовʼязкових предметів — неможливо). Поразка: закляття, вогонь, вогник, нуль HP, червоний таймер. Рахунок: вороги 0–5000, блок закляття 10–40, ключ 100, залишок таймера 10–20000, 60-й — 500000; поверх після продовження — (номер − 1) × 20000.

## Керування і ввід
- 4-позиційний важіль — рух коридорами (і в комбінаціях — таємні умови скринь).
- Одна кнопка: натиснути — витягнути меч, тримати — меч уперед, відпустити — сховати; зупинитись лицем до стіни й натиснути з киркою — проламати стіну.
- Start — теж буває таємною умовою; продовження — монета + утримання кнопки меча + Start.

## Вікна, меню, HUD
- `game-screen`: лабіринт поверху; `score`, `hi-score`, `level-number` (поверх), `timer-countdown` (білий → червоний), `lives`, зібрані предмети (`equipment-slots`) (?).
- `level-select` — після продовження: вибір стартового поверху від 1 до найвищого досягнутого (після ZAP — до поверху падіння).
- `custom-window` «YOU ZAPPED TO…» з номером поверху, куди впав Гіл.
- `end-screen` — фінал після 60-го поверху; `game-over-continue` — запрошення продовжити.
- `attract-demo` (?).
- Переходи: поверх → (ключ + двері) наступний; міс → той самий поверх (?); ZAP → нижній поверх; game over → продовження з вибором поверху.

## Фічі поза полем
- `continue` з вибором поверху й збереженням предметів — рання аркадна «прогресія»; бонус за продовження ламає рахунок як мірило вміння.
- Таємні умови скринь передавались гравцями з уст в уста й через журнали — гра, розрахована на спільноту (EN-вікі).
- Порти: Famicom, MSX, PC Engine (з окремим «hard»-режимом), Game Boy та ін.

## Варіації й родичі
- Серія «Babylonian Castle Saga»: The Return of Ishtar (продовження вдвох), The Quest of Ki (передісторія), The Nightmare of Druaga (роглайк, де предмети втрачаються зі смертю).
- У корпусі: [Atari Adventure](atari-adventure.md), [Venture](venture.md) — кімнати й скарби; [Gauntlet](gauntlet.md) — підземелля з ключами й дверима; [Wizard of Wor](wizard-of-wor.md) — лабіринт з невидимими ворогами; [Chip's Challenge](chips-challenge.md) — ключ/двері й предмети-дозволи.
- **Осі варіацій**: відкриття скарбу — «видно / під блоком / таємна дія»; бій — «постріл / удар кнопкою / наїзд з витягнутим мечем»; захист — «нема / щит у бік загрози»; кара за повільність — «програш / невбивні переслідувачі (вогники) → програш»; втрата — «життя / ZAP вниз з конфіскацією».

## Цікавинки для курсу
- Прихований скарб з таємною умовою поверху (лічильник убивств, клітина, натискання, комбінація важеля) як дані рівня — 🥉.
- Меч як стан «витягнутий / схований» і бій-наїзд з обміном HP — 📎.
- Щит працює лише проти загрози, до якої повернутий, і змінює бік від стану меча — 📎.
- Ланцюг обовʼязкових предметів, без яких бос невразливий, і перевірка «гра стала непрохідною» — 🥈.
- ZAP: падіння на випадковий нижчий поверх з конфіскацією предметів — 📎.
- Двофазний таймер: білий (очки) → червоний (вогники, потім міс) — 🌱.
- Генерація 60 лабіринтів поверхів з фіксованими точками ключа/дверей — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `key-and-door` · `reach-exit` ↔ двері нагору · `stairs-levels` ↔ поверхи · `maze-generation` · `hp-damage` · `melee-vs-ranged` ↔ меч проти заклять · `projectile-shot` ↔ закляття · `line-of-sight-attack` ↔ Друага, гіпер-лицар · `touch-death` + `player-death` · `item-pickup` + `inventory-items` · `destructible-blocks` ↔ кирка · `timeout-punisher` ↔ вогники · `time-bonus` ↔ залишок таймера · `event-points` · `extra-life-threshold` ↔ 50000 · `game-over-continue` + `level-select` ↔ продовження · `sequential-levels` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+secret-condition-treasure` «Скарб зʼявляється від таємної дії поверху» · entities/spawn · 🥉 · слот {condition: kills|cell|button|input_seq|touch_wall}.
  - `+shield-facing-block` «Щит блокує загрозу лише з боку погляду» · entities/combat · 📎.
  - `+sword-drawn-state` «Зброя як стан: витягнута шкодить при контакті» · entities/combat · 📎.
  - `+item-tier-replace` «Предмет старшого рівня заміняє молодший у категорії» · entities/state · 🌱.
  - `+reveal-invisible` (повтор) — свічка показує привидів; `+ghost-phase` (повтор) — привиди крізь стіни.
  - `+required-item-chain` «Без обовʼязкових предметів фінал неможливий» · levels/solvability · 🥈.
  - `+zap-demotion` «Кара: скинути на нижчий рівень і забрати предмети» · game-logic/lose · 📎.
  - `+boss-fight` (повтор) · `+decoy-boss-sequence` «Приманки по черзі перед справжнім босом» · game-logic/waves · 📎.
  - `+limited-use-tool` «Інструмент на N використань» · entities/state · 🌱 (кирка).

## Пропозиції до словників
- `+trigger:secret_met` — виконано таємну умову поверху (обгортка над різними тригерами).
- `+effect:zap` — скинути на інший рівень з конфіскацією предметів.
- `+ui:timer-color-phase` — таймер, що змінює колір і сенс (очки → кара).
- `+card:secret-condition-treasure`, `+card:shield-facing-block`, `+card:sword-drawn-state`, `+card:item-tier-replace`, `+card:required-item-chain`, `+card:zap-demotion`, `+card:decoy-boss-sequence`, `+card:limited-use-tool` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: The Tower of Druaga](https://en.wikipedia.org/wiki/The_Tower_of_Druaga) — 60 поверхів, ключ і двері, вороги (слайми, лицарі, маги з закляттями, привиди крізь стіни, дракони), меч і щит, прихований скарб за таємною дією, кирка/чоботи/свічка, обовʼязкові предмети, Will-o-Wisps за затримку, випадкові лабіринти, скарб у точці старту.
- [Wikipedia JA: ドルアーガの塔](https://ja.wikipedia.org/wiki/ドルアーガの塔) — важіль + 1 кнопка, меч-утримання, щит вперед/ліворуч, HP-обміни, ропер і Друага, умови скринь, категорії предметів зелений → червоний → синій, кирка, намисто, кільця, обладунок, таймер 20000 → червоний 60, ZAP, 59-й і приманки, 60-й, рахунок, extend 50000, продовження.
- [StrategyWiki: Monsters](https://strategywiki.org/wiki/The_Tower_of_Druaga/Monsters) — бачив у пошуку: вогники постійно зʼявляються, поки таймер червоний; синій повертає ліворуч, червоний — праворуч; поверхи 11 і 16 — свічки й умови «торкнись зовнішньої стіни».
- YouTube: пошук «Tower of Druaga gameplay».

## Непевне
- (?) Вогники в аркаді: StrategyWiki — при червоному таймері; JA-вікі повʼязує їх лише з hard-режимом PC Engine.
- (?) Чи маги телепортуються (зʼявляються-зникають) — з памʼяті, у відкритих джерелах лише «кидають закляття».
- (?) JA-вікі: слайм, у якого Гіл врізається в русі, — міс навіть з мечем; механізм неясний.
- (?) Розмір лабіринту поверху, кількість життів на старті, швидкість Гіла.
- (?) Після міса — повтор поверху з початку чи продовження з місця; чи червоний нуль — одразу кінець гри.
- (?) Ефекти чобіт (джет-чоботи на 25-му в коді не зʼявляються), перлини, синього кришталевого жезла, рукавиць, шолома.
- (?) Склад HUD (чи показані предмети на екрані).
