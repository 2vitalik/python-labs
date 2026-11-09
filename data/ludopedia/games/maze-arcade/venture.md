---
title: Venture
slug: venture
aka: [Венчур]
family: maze-arcade
also: [roguelike]
klass: avatar
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 1981
platforms: [arcade, Atari 2600, ColecoVision, Intellivision]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Venture_(video_game)", best: true, note: "коридори й кімнати, Hallmonsters, трупи, 3 рівні × 4 кімнати"}
  - {kind: play, url: "https://archive.org/details/arcade_venture", note: "Internet Arcade — грати; опис кімнат, трупів, рухомих стін"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/venture", note: "KLOV: 8-напрямний джойстик + постріл, заборона повторного входу, множник за час"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=venture+exidy+1981+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-8dir, projectile-shot, shoot-forward, touch-death, player-death, chase-player, enemy-patrol, timeout-punisher, timed-despawn, time-bonus, event-points, collect-all, sequential-levels, progress-acceleration, status-panel, game-screen, +hub-and-rooms-zoom, +invincible-chaser, +lethal-corpse-decay, +room-reentry-ban, +trapped-treasure, +moving-walls]
proposes: ["+effect:decay", "+effect:reset_decay", "+cond:just_left", "+card:hub-and-rooms-zoom", "+card:lethal-corpse-decay", "+card:room-reentry-ban"]
author: opus
date: 2026-11-09
---

# Venture — карта коридорів із кімнатами-скарбницями: зайди, вкради, вийди раніше, ніж прийде невбивний сторож

## Суть
Колобок Winky з луком ходить коридорами підземелля й заходить у кімнати; вхід перемикає вид на збільшену кімнату. У кожній кімнаті — один скарб і монстри зі своїм патерном; скарб треба взяти, монстрів бити необовʼязково. Тиск часу — **Hallmonsters**: невбивні щупальцеві сторожі коридорів, один з яких заходить у кімнату, якщо Winky затримався. Убиті монстри лишають **трупи, що повільно розкладаються і вбивають дотиком**, — можуть закрити вихід.

## Поле і час
- Два масштаби: **коридори** (оглядова карта рівня з 4 кімнатами) і **кімната** (зум на весь екран). Перемикання — вхід/вихід через двері кімнати.
- Рух вільний (не клітинний), 8 напрямків; стіни — непрохідні.
- 3 рівні по 4 кімнати; після 3-го — ті самі плани швидше й з іншими скарбами.
- Real-time; час у кімнаті — прихований лічильник до появи Hallmonster.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Winky | player | життя | рух 8 напрямків; стріляє стрілою в бік руху |
| Стріла | projectile | — | летить прямо; вбиває монстра; у труп — відкочує розклад |
| Hallmonster | enemy | невбивний | патрулює коридори; заходить у кімнату, якщо Winky затримався; переслідує |
| Монстр кімнати (змії, гобліни, скелети, тролі, дракон…) | enemy | вид кімнати; ухильність | патерн руху, може відхилитись і гнатись; дотик вбиває |
| Труп | hazard | фаза розкладу | після вбивства; повільно зникає; дотик вбиває; може загородити вихід |
| Скарб | pickup | 1 на кімнату | мета кімнати; частина скарбів — пастки |
| Двері кімнати | gate | — | вхід/вихід, перемикають масштаб |
| Стіна | static | — | непрохідна; у деяких кімнатах рухається або зникає, випускаючи монстрів |
| Етіни (Two-Headed Room) | enemy | — | зʼявляються, коли взято скарб-пастку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «нема стіни»` → ТО `move(winky, dir)`; інакше `block`.
- КОЛИ `input(fire)` → ТО `spawn(arrow)` у напрямку руху.
- КОЛИ `contact(arrow, monster)` → ТО `transform(corpse)`, `score(n)`, `disappear_a`.
- КОЛИ `timer(every)` → ТО `custom: «труп переходить у наступну фазу розкладу»`; остання фаза → `disappear`.
- КОЛИ `contact(arrow, corpse)` → ТО `custom: «труп повертається до ранішої фази розкладу»`.
- КОЛИ `contact(winky, monster|hallmonster|corpse)` → ТО `lose` (життя −1).
- КОЛИ `enter(winky, room)` → ТО `camera(zoom_room)`.
- КОЛИ `enter(winky, room)` → ЯКЩО `custom: «щойно вийшов з цієї кімнати»` → ТО `custom: «Hallmonster убиває Winky»` (KLOV).
- КОЛИ `timer(room_time)` → ЯКЩО `custom: «Winky досі в кімнаті»` → ТО `spawn_at(hallmonster, room_door)`, `custom: «гониться за Winky»`.
- КОЛИ `picked(winky, treasure)` → ТО `pickup`, `score(n)`.
- КОЛИ `picked(winky, treasure)` → ЯКЩО `custom: «кімната Two-Headed»` → ТО `spawn(ettin ×2)`.
- КОЛИ `custom: «скарби всіх 4 кімнат узято»` → ТО `score(×speed)`, `next_level`; після 3-го — повтор швидше.
- Hallmonster: `enemy-patrol` коридорами; нічим не зупиняється.
- Монстри кімнати: патерн + `chase-player` при відхиленні; ухильність від стріл залежить від виду (змії погано, тролі добре).
- Перемога: нема (цикл рівнів). Поразка: 0 життів. Рахунок: монстри, скарби, множник за швидкість рівня.

## Керування і ввід
- Джойстик 8 напрямків + 1 кнопка «постріл».
- Тактика: швидкий вхід за скарбом, стріляти лише в тих, хто на шляху; не вбивати біля дверей, бо труп закриє вихід.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `splash-screen` / атракт (?).
- `game-screen` у двох масштабах: карта коридорів і збільшена кімната; HUD: `score`, `hi-score` (?), `lives`, `level-number` (?).
- Переходи: атракт → (монета) коридори ↔ (двері) кімната → (4 скарби) наступний рівень → (0 життів) атракт.

## Фічі поза полем
- `levels-sequential` з циклом після 3-го рівня й прискоренням.
- 2 гравці по черзі (`hotseat`).
- Нема паузи, збережень, налаштувань у грі.

## Варіації й родичі
- Порти: ColecoVision (стартова гра консолі, хвалили графіку й музику), Atari 2600 (CommaVid), Intellivision.
- Родичі: Berzerk (Evil Otto — невбивний таймер-переслідувач), Adventure (Atari) і роглайки (кімнати й скарби), Gauntlet.
- Осі: **таймер рівня** (лічильник / невбивний ворог-кара); **масштаб** (одне поле / хаб + кімнати із зумом); **що лишає вбитий ворог** (нічого / предмет / небезпечний труп).

## Цікавинки для курсу
- Хаб і кімнати: два масштаби з перемиканням виду і збереженим станом кімнат — 🥉.
- Hallmonster: прихований таймер кімнати, після якого спавниться невбивний переслідувач — 📎.
- Труп із фазами розкладу, смертельний дотиком; стріла відкочує фазу — 📎: скінченний автомат стану.
- Заборона повторного входу в щойно покинуту кімнату — 🌱.
- Скарб-пастка, що викликає нових ворогів при взятті — 🌱.
- Монстри з різною ухильністю від снарядів — 🥉: передбачення траєкторії.

## Мапа на каталог
- Є: `move-8dir` · `projectile-shot` · `shoot-forward` · `touch-death` · `player-death` · `chase-player` · `enemy-patrol` (Hallmonsters) · `timeout-punisher` (Hallmonster за затримку) · `timed-despawn` (трупи) · `time-bonus` (множник за швидкість) · `event-points` · `collect-all` (усі скарби рівня) · `sequential-levels` · `progress-acceleration` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+hub-and-rooms-zoom` «Хаб-карта з кімнатами, вхід = зум» · interface/render · 🥉.
  - `+invincible-chaser` «Невбивний переслідувач» · entities/move · 🌱 (Evil Otto, Hallmonster).
  - `+lethal-corpse-decay` «Смертельний труп із фазами розкладу» · entities/death · 📎 · слот {phases}.
  - `+room-reentry-ban` «Не можна одразу повернутись у кімнату» · entities/legality · 🌱.
  - `+trapped-treasure` «Предмет-пастка спавнить ворогів» · entities/spawn · 🌱.
  - `+moving-walls` «Стіни кімнати рухаються/зникають» · entities/move · 📎.

## Пропозиції до словників
- `+effect:decay` — сутність переходить у наступну фазу розпаду (труп).
- `+effect:reset_decay` — відкотити фазу розпаду (стріла в труп).
- `+cond:just_left(a, zone)` — A щойно вийшов із зони (заборона повторного входу).
- `+card:hub-and-rooms-zoom`, `+card:lethal-corpse-decay`, `+card:room-reentry-ban` — див. вище.

## Джерела
- ⭐ [Wikipedia: Venture](https://en.wikipedia.org/wiki/Venture_(video_game)) — коридори й кімнати із зумом, Hallmonsters (як Evil Otto), трупи й постріл у труп, 12 кімнат, порти.
- [Internet Arcade: Venture](https://archive.org/details/arcade_venture) — грати; рухомі й зникаючі стіни, формат автомата (8 напрямків, 1 кнопка).
- [KLOV: Venture](https://www.arcade-museum.com/Videogame/venture) — заборона повторного входу, множник за час, 1–2 гравці по черзі.
- YouTube: пошук «venture exidy 1981 arcade gameplay».

## Непевне
- (?) Скільки секунд у кімнаті до появи Hallmonster; кількість Hallmonsters у коридорах.
- (?) Очки за монстрів і скарби, формула множника за час; стартові життя, бонусне життя.
- (?) Які саме кімнати мають рухомі/зникаючі стіни (ймовірно Wall Room).
- (?) Чи стріла летить у бік руху чи в бік останнього напрямку джойстика; чи є обмеження на одну стрілу.
- (?) Чи монстри кімнат відроджуються при повторному вході.
- (?) `random: runtime` — за «можуть відхилитися від патерну, щоб гнатись»; чи це випадково, не підтверджено.
