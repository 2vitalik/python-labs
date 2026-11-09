---
title: Combat
slug: combat
aka: [Tank, Tank-Pong, Tank Plus, Комбат]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 1977
platforms: [Atari 2600, arcade (Tank, 1974)]
links:
  - {kind: other, url: "https://atariage.com/manual_html_page.php?SoftwareLabelID=96", best: true, note: "мануал: таблиця 27 варіацій, типи ракет, Billiard Hit, поля, 2:16, перемикачі складності"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Combat_(video_game)", note: "режими Tank/Biplane/Jet, невидимі танки, хмари, історія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tank_(video_game)", note: "аркадний предок 1974: міни, два джойстики на танк, респавн на місці"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=atari+2600+combat+tank+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-auto, projectile-shot, shoot-forward, mirror-reflect, impassable-cells, touch-death, environment-death, event-points, time-out, respawn, hot-seat, rule-variants, game-settings, difficulty-levels, orientation-state, +tank-steering, +guided-missile, +ricochet-shot, +bank-shot-only, +invisible-until-fire, +hiding-cover, +numbered-variations, +formation-fire, +mine-field]
proposes: ["+effect:shoot", "+effect:steer", "+cond:bounced", "+role:cover", "+feature:numbered-variations", "+axis:control"]
author: opus
date: 2026-11-09
---

# Combat — дуель двох танків у лабіринті: керовані ракети, рикошети від стін і невидимки, хто більше влучить за 2:16

## Суть
Двоє гравців на одній консолі керують танками (або літаками) і стріляють один в одного; кожне влучання — очко, по закінченню 2 хв 16 с перемагає той, у кого більше. Гру роблять 27 пронумерованих варіацій: поле (відкрите / простий / складний лабіринт / хмари), тип ракети (пряма / керована / кулемет), рикошет від стін (Tank-Pong) і невидимі танки. Нащадок аркади Tank (1974) з мінами в центрі лабіринту.

## Поле і час
- Один екран зверху (танки, реактивні літаки) або збоку (біплани); рух вільний з поворотом корпусу на дискретні кути — `field: free`.
- Поля Tank: Open Field, Easy Maze, Complex Maze — блоки під прямими кутами; Tank-аркада — асиметричний, але завжди однаковий лабіринт з мінним полем у центрі.
- Поля літаків: Open Skies (порожньо) або Clouds (хмари, у яких ховаються).
- Real-time; раунд фіксованої тривалості (Combat — 2:16; Tank — 60 або 120 с за монету).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк ×2 | player | колір, кут корпусу | вперед / поворот на місці; стіни блокують |
| Біплан / джет ×2 (або загони 2×2, 1×3) | player | швидкість | завжди летить уперед; поворот, набір/зниження висоти |
| Ракета пряма | projectile | дальність (перемикач A/B) | летить прямо |
| Ракета керована | projectile | — | після пострілу повертає за джойстиком ліво/право |
| Кулемет | projectile | — | швидкі прямі постріли |
| Ракета Tank-Pong | projectile | — | відбивається від стін |
| Стіна лабіринту | static | — | непрохідна для танків; у Pong — відбиває ракети |
| Хмара | terrain | — | ховає літак від погляду; влучити все одно можна |
| Міна (Tank 1974) | hazard | одноразова | наїзд → танк знищено; знищена міна не повертається |

## Правила (КОЛИ → ЯКЩО → ТО)
- Танк: КОЛИ `input(forward)` → ЯКЩО `free(cell_ahead)` → ТО `move(tank, facing)`; інакше `block`. КОЛИ `input(left|right)` → ТО `rotate(tank, ±step)`. Назад — нічого.
- Літак: КОЛИ `tick` → ТО `move(plane, facing)` (завжди вперед); КОЛИ `input(left|right)` → ТО `rotate(plane, ±step)`; КОЛИ `input(stick)` → ТО `speed(plane, ±n)`.
- КОЛИ `input(fire)` → ЯКЩО `count(own_missile, ==, 0)` (?) → ТО `custom: «постріл ракетою вперед»` (`+effect:shoot`).
- КОЛИ `input(left|right)` → ЯКЩО `mode(guided)` `and count(own_missile, >, 0)` → ТО `custom: «ракета повертає за джойстиком»` (`+effect:steer`).
- КОЛИ `contact(missile, wall)` → ЯКЩО `mode(pong)` → ТО `bounce(missile)`; інакше `disappear_a`.
- КОЛИ `contact(missile, enemy_tank)` → ЯКЩО `not mode(billiard)` або `custom: «ракета вже відбилась ≥1 раз»` (`+cond:bounced`) → ТО `score(+1)` власнику ракети, `disappear_a`.
- КОЛИ `contact(missile, own_tank)` → ТО `custom: «очко супернику не дається»`.
- КОЛИ `timer(range)` → ТО `disappear(missile)` — дальність залежить від перемикача складності (A коротше, B довше).
- Невидимі танки: КОЛИ `input(fire)` або `contact(missile, tank)` → ТО `reveal(tank)` на мить; інакше `hide(tank)`.
- КОЛИ `enter(plane, cloud)` → ТО `hide(plane)`; влучання все одно рахується.
- Загони (2 vs 2, 1 vs 3): КОЛИ `input(fire)` → ТО `custom: «стріляють усі літаки загону одночасно»`.
- Tank 1974: КОЛИ `contact(tank, mine)` → ТО `disappear_both`, `score(+1)` супернику; КОЛИ `contact(shell, tank)` → ТО `score(+1)`, `custom: «пауза-вибух, суперник не стріляє»`, `respawn(tank, same_place)`.
- КОЛИ `timer(2:16)` → ТО `custom: «кінець гри»`; переможець — `counter(score)` більший.
- Перемога: більше влучань за час. Поразка: менше. Нічия можлива (?). Рахунок: 1 очко за влучання.

## Керування і ввід
- Combat: один джойстик на гравця. Танк — вперед = їхати, ліво/право = поворот, назад нічого; червона кнопка — постріл. Біплан — ліво/право = швидкість, вперед/назад = пікірування/набір; джет — вперед/назад = швидкість, ліво/право = поворот.
- Керована ракета: після пострілу ліво/право повертає ракету (і танк разом з нею (?)).
- Консоль: Game Select — номер варіації (1–27), Game Reset — старт; перемикачі Difficulty A/B для кожного гравця окремо.
- Tank 1974: по два джойстики на гравця («гусениці»): обидва вперед — їхати, назад — стоп, різно — поворот на місці / на ходу; кнопка на правому — постріл.

## Вікна, меню, HUD
- `game-screen` — поле і два рахунки вгорі кольорами гравців; номер варіації показується на місці рахунку до старту (?).
- `mode-select` — вибір варіації 1–27 перемикачем Game Select (без меню; поле одразу перемальовується).
- Tank 1974: рахунки над полем блимають останні 20 с.
- Переходи: Select (номер) → Reset → гра 2:16 → кінець (рахунок застигає) → Select / Reset.

## Фічі поза полем
- `numbered-variations` — 27 комбінацій «транспорт × поле × ракета × рикошет × невидимість» за номером: класичний `custom-rules`.
- `difficulty-presets` для кожного гравця окремо (дальність ракети, швидкість літака) — гандикап сильнішому.
- `hotseat` / `local-multiplayer` — лише 2 гравці, AI нема.
- Tank: `operator-settings` (час за монету 60/120 с).

## Варіації й родичі
- **Tank (Kee Games, 1974)** → Tank II, Tank 8 (?); Combat — домашнє переосмислення на Atari 2600 (комплектна гра консолі).
- **Combat Two** (прототип 2600), Combat-режими в Battlezone, Tank Battalion → **Battle City** (руйнівні стіни, AI-танки, база) — у корпусі.
- Wii Play Tanks!, Tank Trouble / AZ (браузер: рикошети в лабіринті) — прямі нащадки Tank-Pong.
- **Осі варіацій:** ракета (пряма / керована / кулемет) · стіни (блокують / відбивають) · влучання (будь-яке / лише після рикошету) · видимість (завжди / лише при пострілі / хмари) · транспорт (танк поворотом / літак з постійною швидкістю) · гандикап (перемикач на гравця).

## Цікавинки для курсу
- Танкове керування «поворот + вперед» замість 4 напрямків — 🌱 (кут, sin/cos).
- Рикошет ракети від стін лабіринту + режим «лише після відскоку» — 🥉 (відбиття від осьових стін і лічильник відскоків).
- Керована ракета, яку рулиш після пострілу — 📎.
- Невидимий танк, що проявляється при пострілі чи влученні — 🌱.
- 27 варіацій як матриця перемикачів — 📎 (налаштування = дані, одна гра з них збирається).
- Гандикап окремим перемикачем на кожного гравця — 🌱.
- Мінне поле в центрі, міни не відновлюються (Tank) — 🌱.

## Мапа на каталог
- Є: `move-auto` (літаки) · `projectile-shot` · `shoot-forward` · `mirror-reflect` (рикошет від стіни) · `impassable-cells` · `touch-death` · `environment-death` (міна) · `event-points` · `time-out` · `respawn` · `hot-seat` · `rule-variants` · `game-settings` · `difficulty-levels` · `orientation-state` (кут корпусу).
- **Нема** → пропозиції карток:
  - `+tank-steering` «Поворот корпусу + рух уперед» · entities/move · 🌱 · слот {angles}.
  - `+guided-missile` «Снаряд, яким кермують після пострілу» · entities/combat · 📎.
  - `+ricochet-shot` «Снаряд відбивається від стін» · entities/combat · 📎 · слот {max_bounces}.
  - `+bank-shot-only` «Очко лише після відскоку» · game-logic/score · 🌱.
  - `+invisible-until-fire` «Невидимий, доки не стріляє / не влучили» · interface/render · 🌱.
  - `+hiding-cover` «Укриття ховає, але не захищає» · entities/legality · 🌱 — хмари.
  - `+numbered-variations` «Номер гри = набір правил» · game-logic/constraints · 📎 — дитина `rule-variants`.
  - `+formation-fire` «Загін стріляє разом» · entities/combat · 🌱.
  - `+mine-field` «Одноразові міни» · entities/death · 🌱.

## Пропозиції до словників
- `+effect:shoot` — випустити снаряд (Combat, Berzerk, Battle City).
- `+effect:steer` — змінити напрям уже випущеного снаряда (керована ракета).
- `+cond:bounced` — снаряд відбився ≥ N разів (Billiard Hit).
- `+role:cover` — укриття, що ховає з поля зору (хмари).
- `+feature:numbered-variations` — пронумеровані варіації правил (Atari 2600: Combat, Maze Craze).
- `+axis:control` — `tank` (поворот + вперед) як нове значення поряд з `direct`.

## Джерела
- ⭐ [AtariAge: мануал Combat](https://atariage.com/manual_html_page.php?SoftwareLabelID=96) — керування для танка/біплана/джета, типи ракет, Billiard Hit, свій постріл не рахується, таблиця 27 варіацій, поля, 2:16, перемикачі A/B.
- [Wikipedia: Combat](https://en.wikipedia.org/wiki/Combat_(video_game)) — режими, невидимі танки «видно лише при пострілі або після влучання», хмари, постійний рух літаків.
- [Wikipedia: Tank](https://en.wikipedia.org/wiki/Tank_(video_game)) — асиметричний незмінний лабіринт, міни X у центрі, два джойстики на танк, респавн на місці, 60/120 с.
- YouTube: пошук «atari 2600 combat tank gameplay».

## Непевне
- (?) Що стається з танком при влучанні в Combat (відкидає/крутить) — мануал не описує.
- (?) Чи можна мати більше однієї ракети в польоті; чи повертається танк разом з керованою ракетою.
- (?) Чи блимає невидимий танк ще й при дотику до стіни.
- (?) Tank II / Tank 8, Combat Two, Tank Battalion, Wii Play Tanks!, Tank Trouble — родичі з памʼяті, сторінок не відкривав.
- (?) Як показано номер варіації і чи можлива нічия.
