---
title: Hopping Mappy
slug: hopping-mappy
aka: [ホッピングマッピー]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: collect
year: 1986
platforms: [arcade (Namco System 86), i-appli (2005), Wii VC (2009), PS4/Switch Arcade Archives (2022)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hopping_Mappy", best: true, note: "пого-стрибки лише в центри шахових клітин, патрулі котів, 8 скарбів, прискорення ×2, Hurry Up і монета Госендзо"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ホッピングマッピー", note: "JA: 31 раунд, скарби й ціни, пари-множник, ?BOX і 8 предметів, бонус-раунд кожні 4, літери MAPPY"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hopping+Mappy+arcade", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, enemy-patrol, chase-player, touch-death, player-death, item-pickup, collect-all, combo-multiplier, temporary-modes, timeout-punisher, speed-per-type, event-points, sequential-levels, game-screen, +center-only-landing, +air-turn, +hurry-up-speedup, +rest-window-stomp, +slot-bonus, +freeze-all-enemies, +letters-extra-life, +autoscroll-bonus-round]
proposes: ["+window:bonus-round", "+effect:slot_stop", "+card:center-only-landing", "+card:air-turn", "+card:hurry-up-speedup", "+card:rest-window-stomp", "+card:slot-bonus", "+card:letters-extra-life", "+card:autoscroll-bonus-round"]
author: opus
date: 2026-11-09
---

# Hopping Mappy — пого-стрибки по центрах шахових клітин між котами-патрулями: збери 8 скарбів

## Суть
Миша-поліцейський Маппі безперервно стрибає на пого-палиці по полю за парканом і може приземлятись лише в центри шахових клітин — тож рух клітинний, хоч і плавний на вигляд. Рожеві коти Мʼюкі ходять туди-сюди однією лінією, не переслідуючи, а бос Нямко скаче сам і мусить відпочивати. Затягнеш — «Hurry Up»: коти пришвидшуються, а потім вилітає монета Госендзо, єдиний ворог, що переслідує. Ядро — прорватись крізь «стіну» котячих патрулів, вгадавши такт.

## Поле і час
- Поле на відкритому повітрі, обгороджене парканом; сітка шахових клітин, центри яких — єдині точки приземлення (EN-вікі).
- Real-time; Маппі за замовчуванням іде з тією ж швидкістю, що й коти; кнопка прискорення — удвічі швидше.
- 31 раунд; кожен 4-й — бонус-раунд з примусовою прокруткою ліворуч.
- Чи прокручується звичайний раунд — невідомо (див. «Непевне»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маппі | player | швидкість ×1 / ×2 | стрибає в 4 напрямки з центру в центр; у повітрі може розвернутись |
| Мʼюкі | enemy | на пого; вертикаль або горизонталь | ходить туди-сюди однією лінією, не переслідує |
| Нямко (Горо) | enemy | без пого | скаче сам зигзагом, через певну відстань відпочиває; стрибнути на нього під час відпочинку — 100 очок |
| Госендзо (монета-надгробок) | enemy | швидший за Маппі | зʼявляється, якщо раунд затягнувся й лишилось ≤ 2 скарбів; єдиний, хто переслідує |
| Скарби (маска лиса 10, кіт-манекі 20, Дарума 30, сніговик 40) | pickup | 4 види × 2 = 8 | зібрати всі → раунд пройдено |
| ?BOX | container | — | зʼявляється після певних пар; порожній — 50 очок |
| Синій пісочний годинник | pickup | кілька секунд | заморожує Нямко й Мʼюкі; дотик не вбиває |
| Рожевий пісочний годинник | pickup | кілька секунд | заморожує лише Мʼюкі |
| Червоний / жовтий діамант | pickup | 3- / 2-розрядний слот | зупинене число = бонусні очки |
| Червоне серце | pickup | кілька секунд | невразливість, можна знищити Нямко й Мʼюкі |
| Помаранчеве серце | pickup | кілька секунд | невразливість лише проти Мʼюкі; дотик Нямко — міс |
| Фіолетова куля | pickup | кілька секунд | сповільнює Мʼюкі |
| Синя куля | pickup | — | «пусто» |
| Літери M·A·P·P·Y | pickup | лише раунд 3 | усі пʼять → +1 життя (єдиний спосіб) |
| Повітряні кулі (малі, великі) | pickup | бонус-раунд | очки; кожні 8 малих підвищують ціну (до 5 щаблів) |
| Паркан | static | — | межа поля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(mappy, dir)` — стрибок у центр сусідньої клітини; між центрами приземлитись не можна.
- КОЛИ `input(reverse_dir)` → ЯКЩО `custom: «Маппі в повітрі»` → ТО `face(mappy, reverse)` — ухилитись від кота в тій самій колонці.
- КОЛИ `input(button)` → ТО `speed(mappy, ×2)` поки затиснуто.
- КОЛИ `tick` → ТО `move(mewky, dir)`; КОЛИ `blocked(mewky)` → ТО `face(mewky, reverse)` — патруль однією лінією.
- КОЛИ `timer(rest_every)` → ТО `set_state(nyamco, resting)`; КОЛИ `contact(mappy, nyamco)` → ЯКЩО `state(nyamco, resting)` → ТО `score(100)`.
- КОЛИ `contact(mappy, mewky|nyamco)` → ЯКЩО `not state(mappy, invincible)` and `not state(cats, frozen)` → ТО `lives(-1)`.
- КОЛИ `contact(mappy, treasure)` → ТО `pickup`, `score(base × mult)`; ЯКЩО `custom: «друга з пари»` → ТО `multiplier(+1)` (×2, ×3, …).
- КОЛИ `custom: «зібрано певну пару»` → ТО `spawn(qbox)`; КОЛИ `contact(mappy, qbox)` → ТО `custom: «вміст ?BOX»`; порожній — `score(50)`; під час серії пар — `multiplier(+1)`.
- КОЛИ `picked(mappy, blue_hourglass)` → ТО `freeze(nyamco + mewkies, n)`; рожевий — `freeze(mewkies, n)`.
- КОЛИ `picked(mappy, diamond)` → ТО `custom: «слот: 3 (червоний) або 2 (жовтий) розряди»`; КОЛИ `input(button)` → ТО `score(stopped_number)`.
- КОЛИ `picked(mappy, red_heart)` → ТО `set_state(mappy, invincible, n)`; КОЛИ `contact(mappy, cat)` → ЯКЩО `state(mappy, invincible)` → ТО `disappear(cat)`; помаранчеве серце — лише Мʼюкі, Нямко вбиває.
- КОЛИ `picked(mappy, purple_ball)` → ТО `speed(mewkies, -n)` на кілька секунд.
- КОЛИ `timer(round_too_long)` → ТО `message("Hurry Up")`, `speed(cats, =mappy×2)`.
- КОЛИ `custom: «після Hurry Up усе ще повільно»` → ЯКЩО `count(treasure, <=, 2)` → ТО `spawn(gosenzo)`; КОЛИ `tick` → ТО `custom: «Госендзо женеться за Маппі»`; КОЛИ `contact(gosenzo, mappy)` → ТО `lives(-1)`.
- КОЛИ `all_gone(treasure)` → ТО `next_level`.
- Раунд 3: КОЛИ `picked(mappy, letter)` → ЯКЩО `counter(letters, ==, 5)` → ТО `lives(+1)`.
- Бонус-раунд: КОЛИ `level_start` → ЯКЩО `level(%4, ==, 0)` → ТО `custom: «примусова прокрутка ліворуч»`; КОЛИ `contact(mappy, balloon)` → ТО `disappear(balloon)`, `counter(balloons, +1)`; КОЛИ `edge(mappy)` або `custom: «музика скінчилась»` → ТО `score(tiers + big_balloons)`, `next_level`.
- Перемога: пройти раунди (31). Поразка: дотик кота чи Госендзо; життя скінчились. Рахунок: скарби з множником пар, ?BOX, слот, 100 за Нямко на відпочинку, кулі бонус-раунду.

## Керування і ввід
- 4-позиційний важіль — напрям стрибка; розворот у повітрі — важіль у протилежний бік.
- Одна кнопка — прискорення (утримання).
- 1–2 гравці.

## Вікна, меню, HUD
- `game-screen`: поле з парканом, скарби, коти; `score`, `hi-score`, `lives`, `level-number` (раунд) (?).
- `bonus-round` — раунд з кулями й примусовою прокруткою, кожен 4-й.
- `attract-demo` (?).
- Переходи: раунд → (усі скарби) наступний → кожен 4-й бонус-раунд → (життя скінчились) кінець.

## Фічі поза полем
- Arcade Archives (PS4/Switch, 2022) — сучасне перевидання з функціями збірки (?); у Pac-Man 99 — безкоштовна DLC-тема.
- Нема збереження й прогресії поза раундами; єдиний extend — літери MAPPY.

## Варіації й родичі
- Спін-оф Mappy (1983): там Маппі стрибає на батутах у будинку з дверима — це вже `grid-platformer`; тут та сама родина персонажів на пласкій шаховій сітці.
- У корпусі: [Frogger](frogger.md) — стрибок на клітину між патрулями; [Q*bert](qbert.md) — стрибки клітина-в-клітину; [Pac-Man](pac-man.md) — бонус-предмети й прискорення ворогів; [Lady Bug](lady-bug.md), [Clu Clu Land](clu-clu-land.md) — одноекранні збирання.
- **Осі варіацій**: точки приземлення — «будь-де / лише центри клітин»; вороги — «переслідують / патрулі-лінії / зигзаг з відпочинком»; кара за повільність — «прискорення котів → невбивний переслідувач» (сходинки, як Hurry Up у Bomberman).

## Цікавинки для курсу
- Рух лише між центрами клітин з плавною анімацією стрибка й розворотом у повітрі — 📎.
- Патрулі-лінії: прорватись крізь «стіну» котів за таймінгом — 🌱 кожен, 📎 стінка з кількох.
- Двосходинкова кара за повільність: Hurry Up пришвидшує ворогів, далі переслідувач — 📎.
- Множник за пари однакових скарбів — 🌱.
- ?BOX з 8 ефектами (заморозка, слот, невразливість, сповільнення, пусто) — 🥉 як таблиця предметів.
- Слот-машина: число, що крутиться, зупиняється кнопкою — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `enemy-patrol` ↔ Мʼюкі · `chase-player` ↔ Госендзо · `touch-death` + `player-death` · `item-pickup` · `collect-all` ↔ 8 скарбів · `combo-multiplier` ↔ пари · `temporary-modes` ↔ серця, годинники · `timeout-punisher` ↔ Госендзо · `speed-per-type` · `event-points` · `sequential-levels` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+center-only-landing` «Приземлення лише в центри клітин» · entities/move · 🌱.
  - `+air-turn` «Розворот у повітрі під час стрибка» · entities/move · 🌱.
  - `+hurry-up-speedup` «Затягнув раунд — вороги пришвидшуються» · game-logic/lose · 🌱 (поруч із `timeout-punisher`).
  - `+rest-window-stomp` «Ворога можна вразити лише під час відпочинку» · entities/combat · 📎.
  - `+slot-bonus` «Слот: зупини число кнопкою» · game-logic/score · 🌱.
  - `+freeze-all-enemies` (повтор з корпусу) — пісочні годинники.
  - `+letters-extra-life` «Збери літери слова — +1 життя» · game-logic/score · 🌱.
  - `+autoscroll-bonus-round` «Бонус-раунд з примусовою прокруткою» · levels/progression · 📎.

## Пропозиції до словників
- `+window:bonus-round` (вже Amidar, Binary Land) — окремий раунд з іншими правилами.
- `+effect:slot_stop` — зупинити слот і отримати показане число.
- `+card:center-only-landing`, `+card:air-turn`, `+card:hurry-up-speedup`, `+card:rest-window-stomp`, `+card:slot-bonus`, `+card:letters-extra-life`, `+card:autoscroll-bonus-round` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Hopping Mappy](https://en.wikipedia.org/wiki/Hopping_Mappy) — пого в 4 напрямки, приземлення лише в центри шахових клітин, швидкість як у котів, прискорення ×2, Мʼюкі вертикально/горизонтально, Горо зигзагом з перервами, 8 скарбів, бонус-раунд з кулями, Hurry Up і монета Госендзо.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ホッピングマッピー) — важіль + 1 кнопка, розворот у повітрі, 31 раунд, ціни скарбів і пари-множник, ?BOX і вісім предметів, бонус-раунд кожні 4 з щаблями, літери MAPPY у раунді 3, Нямко на відпочинку — 100, умова появи Госендзо.
- YouTube: пошук «Hopping Mappy arcade».

## Непевне
- (?) Чи пара — це два однакові скарби підряд і що обриває серію множника.
- (?) Які саме пари відкривають ?BOX; чи вміст ?BOX випадковий (поставлено `random: none`).
- (?) Тривалість ефектів («кілька секунд») і час до Hurry Up / Госендзо.
- (?) Чи прокручується звичайний раунд; стартова кількість життів; HUD і введення імені в рекорди.
- (?) Що відбувається з Нямко після стрибка на нього під час відпочинку (лише очки чи оглушення).
- (?) Розворот Мʼюкі біля паркана — з опису «туди-сюди однією лінією», механізм не підтверджено.
