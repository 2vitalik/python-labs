---
title: Critter Crunch
slug: critter-crunch
aka: []
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: collect
year: 2007
platforms: [BREW, J2ME, iOS, PS3, PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/61730/Critter_Crunch/", best: true, note: "опис: язик хапає з лоз, годуй менших більшим до вибуху, самоцвіти, ланцюги; 4 соло-режими, co-op і versus; трейлер"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Critter_Crunch", note: "стаб: «у дусі Magical Drop», Capybara Games, платформи й дати"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=critter+crunch+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, keyboard-controls, collect-quota, chain-reaction, progress-acceleration, event-points, score-records, mode-select, simultaneous-versus, garbage-attack, online-multiplayer, hot-seat, +column-grab-throw, +food-chain-feed, +size-tier-eat, +ceiling-push]
proposes: ["+effect:grab", "+cond:greater", "+card:food-chain-feed", "+card:size-tier-eat"]
author: opus
date: 2026-11-09
---

# Critter Crunch — язиком знімаєш звіра знизу стовпчика й кидаєш угору: більший зʼїдає меншого і лопається

## Суть
Аркадний match-пазл Capybara Games «у дусі Magical Drop»: згори на лозах звисають стовпчики звірят, а внизу ходить Біггс. Він хапає довгим липким язиком нижнього звіра стовпчика і кидає його в інший стовпчик — **менший звір годує більшого**. Нагодований звір лопається і сипле самоцвіти, які Біггс збирає; довший «харчовий ланцюг» дає більше нагороди. Лози з часом опускаються; якщо звірята дістануть Біггса — поразка (?).

## Поле і час
- Поле — ряд вертикальних стовпчиків-лоз над Біггсом; ширина й висота — (?). Біггс рухається лише по нижній лінії, по одному стовпчику.
- Real-time: стовпчики періодично опускаються (новий ряд зверху) (?), темп росте.
- Інформація повна: видно всі стовпчики; випадковість — у нових рядах звірят.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біггс | player | позиція (стовпчик); тримає ≤1 звіра (?) | ходить вліво/вправо; язиком хапає нижнього звіра стовпчика; кидає його вгору |
| Малий звір | tile | розмір S, вид/колір (?) | їжа для більшого; нагодувати нікого не може (?) |
| Середній звір | tile | розмір M | їсть малого; сам їжа для великого (?) |
| Великий звір | tile | розмір L | їсть середнього (?) |
| Самоцвіт | pickup | — | випадає з лопнутого звіра; Біггс збирає — заповнює шкалу рівня (?) |
| Спеціальні звірята | hazard | види — (?) | «додають нові виклики» (Steam); поведінка не перевірена |
| Павер-апи | pickup | види — (?) | «додають різноманіття» (Steam) |
| Лоза-стовпчик | zone | висота | опускається з часом; низ стовпчика — те, що можна схопити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(biggs, dir)` на один стовпчик.
- КОЛИ `input(tongue)` → ЯКЩО `custom: «Біггс нічого не тримає»` → ТО `custom: «язик хапає нижнього звіра стовпчика»`, `carry(biggs, critter)`.
- КОЛИ `input(tongue)` → ЯКЩО `has(biggs, critter)` → ТО `throw(critter, up)` — звір летить до низу поточного стовпчика.
- КОЛИ `contact(thrown, bottom_critter)` → ЯКЩО `custom: «нижній більший за кинутого на один розмір»` → ТО `disappear_a` (зʼїдено), `custom: «нижній лопається»`, `spawn(gem)`.
- КОЛИ `contact(thrown, bottom_critter)` → ЯКЩО `custom: «нижній не більший»` → ТО `custom: «кинутий приєднується до стовпчика знизу»` (?).
- КОЛИ `destroyed(critter)` → ЯКЩО `custom: «поруч такий самий звір»` → ТО `trigger(той самий вибух)` — харчовий ланцюг (?); `combo(+1)`.
- КОЛИ `after(chain)` → ТО `score(n·chain)` — довший ланцюг, більша нагорода.
- КОЛИ `contact(biggs, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `counter(gems, >=, quota)` → ТО `win` (рівень Adventure) (?).
- КОЛИ `timer(drop)` → ТО `shift(all_columns, down)` (?).
- КОЛИ `reach(critter, biggs_row)` → ТО `lose` (?).
- Versus: КОЛИ `after(chain)` → ТО `send_garbage(opponent, rows)` (?).

## Керування і ввід
- Ліво/право — крок Біггса між стовпчиками; одна кнопка — язик: перше натискання хапає, друге кидає (?).
- Вісь `control: grab-throw` (як Magical Drop).
- PS3/PC — геймпад або клавіатура; iOS — тач (схема — (?)).

## Вікна, меню, HUD
- `game-screen`: стовпчики звірят, Біггс, шкала самоцвітів (`progress-bar`), `score`; у versus — два поля.
- `mode-select`: Adventure · Puzzle · Challenge · Survival · Co-op · Versus.
- `level-select` / `map-window` для Adventure — (?).
- `end-screen` — рахунок, рекорди; `leaderboard` (Steam Leaderboards).
- `pause-menu`, `settings-window` — (?).

## Фічі поза полем
- Режими: Adventure (кампанія з рівнями), Puzzle (задані розкладки), Challenge, Survival (`mode-endless`).
- `mode-coop` і `mode-versus` — локально й онлайн (`local-multiplayer`, `online-multiplayer`).
- `achievements`, `cloud-save`, `leaderboard-online` (Steam); локалізація EN + 4 мови.

## Варіації й родичі
- Прямий предок механіки: [magical-drop](magical-drop.md) (схопити знизу стовпчика і кинути назад); також [money-puzzle-exchanger](money-puzzle-exchanger.md).
- Від Magical Drop відрізняється правилом збігу: не «3 однакові в стовпчику», а **розмірна ієрархія** — менший годує більшого.
- Родичі за ієрархією: [suika-game](suika-game.md), [triple-town](triple-town.md) (сходинки розмірів/рівнів).
- **Осі варіацій**: що вирішує збіг (колір / розмір-ієрархія) · скільки тримає рука (1 / стос однакових) · як росте поле (опускається / виштовхується знизу) · мета рівня (квота самоцвітів / очищення / виживання).

## Цікавинки для курсу
- Схопити нижнього зі стовпчика й кинути в інший — 🌱 (стек-операції pop/push над стовпчиками).
- Правило «їсть лише на розмір більший» — 🌱 (порівняння тиру замість рівності).
- Ланцюгові вибухи сусідніх однакових — 📎 (flood fill + каскад).
- Опускання лоз за таймером з поразкою при дотику до низу — 🌱.
- Versus на двох полях зі сміттям — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `keyboard-controls` · `collect-quota` (самоцвіти) · `chain-reaction` (харчовий ланцюг) · `progress-acceleration` · `event-points` · `score-records` · `mode-select` · `simultaneous-versus` · `garbage-attack` (?) · `online-multiplayer` · `hot-seat`.
- **Нема** → пропозиції карток:
  - `+column-grab-throw` — підтверджую (Magical Drop, Money Puzzle Exchanger, Critter Crunch).
  - `+food-chain-feed` «Менший годує більшого — більший лопається» · entities/interact · 🌱.
  - `+size-tier-eat` «Взаємодія за ієрархією розмірів (S < M < L)» · entities/legality · 🌱.
  - `+ceiling-push` — підтверджую (стовпчики опускаються).

## Пропозиції до словників
- `+effect:grab` — схопити сутність на відстані (язик, Magical Drop) — підтверджую.
- `+cond:greater(a, b, prop)` — A більше за B за властивістю (розмір, тир; дзеркально до `same`).
- `+card:food-chain-feed` — нагодований звір лопається і дає нагороду.
- `+card:size-tier-eat` — правило збігу за розмірним тиром.

## Джерела
- ⭐ [Steam: Critter Crunch](https://store.steampowered.com/app/61730/Critter_Crunch/) — язик хапає з лоз, годування менших більшим до вибуху, самоцвіти, харчовий ланцюг, павер-апи, 4 соло-режими, co-op/versus онлайн і локально.
- [Wikipedia: Critter Crunch](https://en.wikipedia.org/wiki/Critter_Crunch) — «у дусі Magical Drop», Capybara Games, IGF Mobile 2007, платформи.
- YouTube: пошук «critter crunch gameplay».

## Непевне
- Джерела бідні (Wikipedia — стаб, IGN/fandom/StrategyWiki не відкрились, WebSearch вичерпано); багато — з памʼяті.
- (?) Кількість розмірів (3?) і чи важить колір/вид, а не лише розмір.
- (?) Чи лопається звір від одного годування, чи треба кілька; чи йде ланцюг на сусідніх однакових.
- (?) Що буває при кидку в звіра не того розміру.
- (?) Мета рівня Adventure (квота самоцвітів у шлунок Біггса) і умова поразки.
- (?) Види спеціальних звірят і павер-апів; механіка атаки у versus.
