---
title: Solstice
slug: solstice
aka: ["Solstice: The Quest for the Staff of Demnos"]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1990
platforms: [NES]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Solstice_(1990_video_game)", best: true, note: "250 кімнат, 6 частин посоху, 4 зілля, блоки-сходинки, ключі, бомби, портали, мапа, життя, сиквел Equinox"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Solstice+NES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [inventory, inventory-items, item-pickup, key-and-door, gravity-fall, push-object, carrier-platform, timed-despawn, touch-death, environment-death, player-death, teleport, temporary-modes, explode-area, map-window, collect-quota, game-screen, +stack-to-climb, +room-scoped-effect, +freeze-time, +reveal-invisible, +hidden-exit-after-task, +continue-token, +flip-screen-rooms]
proposes: ["+effect:freeze_all", "+effect:clear_room", "+feature:room-scoped-powerup", "+card:room-scoped-effect", "+card:freeze-time", "+card:reveal-invisible", "+card:hidden-exit-after-task", "+card:continue-token"]
author: opus
date: 2026-11-09
---

# Solstice — чарівник Шадакс проходить 250 ізометричних кімнат-головоломок, будуючи сходи з блоків і витрачаючи чотири зілля

## Суть
NES-пазл-платформер «у стилі Knight Lore»: фортеця Kâstleröck із 250 кімнат, кожна — окрема головоломка. Шадакс стрибає, бере й ставить предмети, штовхає блоки й робить з них сходинки, щоб дістатись входів і предметів. Мета — зібрати 6 частин посоху Demnos, визволити Eleanor і знищити Morbius. Ключовий ресурс — 4 види зілля з обмеженою кількістю доз, що діють лише в поточній кімнаті.

## Поле і час
- Граф із 250 кімнат-екранів; кожна — ізометрична коробка з блоків, висота — третя вісь.
- Real-time, гравітація; падаючі згори блоки; заморожений час зупиняє все рухоме.
- Інформація часткова: видно одну кімнату; частина обʼєктів невидима до зілля; деякі виходи зʼявляються лише після завдання.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шадакс | player | життя (на екрані до 10) | рух 4 напрямки ізометрії, стрибок, взяти/покласти |
| Чоботи ельфів | pickup | — | рано в грі; підвищують стрибок |
| Частина посоху | pickup | 6 штук | мета гри |
| Магічний ключ | pickup | 4 сховані | потрібні, щоб зачистити/відкрити деякі кімнати |
| Колба із зіллям | pickup | 4 види, старт по 2 дози | дози поповнюються знахідками |
| Синій гострий капелюх | pickup | +1 життя | — |
| Монета | pickup | — | після втрати всіх життів — продовжити з певної кімнати |
| Рухомий блок | object | — | лежить або падає згори; штовхається; сходинка й щит |
| Кришталева куля | object | ширяє | штовхається й везе на собі; не носиться |
| Бомба | object | детонатор у сусідній кімнаті | відкриває завалений прохід |
| Портал | static | пара | єдиний шлях у деякі кімнати |
| Конвеєр | terrain | напрямок | везе Шадакса |
| Міст/плитка, що зникає | terrain | — | зникає під героєм |
| Шипи, плаваючі міни | hazard | — | дотик — смерть |
| Троль, гігантський павук, демон | enemy | вид | дотик — смерть |
| Невидимий обʼєкт | static | невидимий | видно лише під зіллям |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(shadax, dir)`; без опори — `fall(shadax)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок; вищий, коли є чоботи»`.
- КОЛИ `input(take)` → ЯКЩО `occupied(here, object)` → ТО `pickup(shadax, item)`; повторно → `place(shadax, item)`.
- КОЛИ `contact(shadax, block)` → ЯКЩО `free(behind)` → ТО `push(block)`.
- КОЛИ `contact(shadax, crystal_ball)` → ТО `push(ball)`; стоячи на кулі — `custom: «куля везе героя»`.
- КОЛИ `spawned(falling_block)` → ТО `fall(block)`; ЯКЩО `state(room, time_frozen)` → ТО `block` — висить у повітрі як сходинка.
- КОЛИ `input(potion, kind)` → ЯКЩО `has(shadax, potion)` → ТО `take(shadax, dose)` і ефект на кімнату:
  - invincibility → `set_state(shadax, invincible)`;
  - destroy → `custom: «знищити все рухоме в кімнаті»`;
  - freeze → `set_state(room, time_frozen)`;
  - reveal → `reveal(cells)` — невидимі обʼєкти.
- КОЛИ `leave(shadax, room)` → ТО `clear_state(shadax, potions)` — зілля діють лише в кімнаті; кілька можна поєднати.
- КОЛИ `custom: «детонатор у сусідній кімнаті задіяно»` → ТО `explode(area)` — бомба розчищає прохід.
- КОЛИ `enter(shadax, portal)` → ТО `teleport`.
- КОЛИ `enter(shadax, conveyor)` → ТО `move(shadax, dir)`; КОЛИ `enter(shadax, vanishing_tile)` → ТО `custom: «плитка зникає»`.
- КОЛИ `contact(shadax, hazard|enemy)` → ЯКЩО `not state(shadax, invincible)` → ТО `lives(-1)`.
- КОЛИ `custom: «виконано завдання кімнати»` → ТО `custom: «зʼявляється прихований вихід»`.
- КОЛИ `counter(lives, =, 0)` → ЯКЩО `has(shadax, coin)` → ТО `respawn(shadax, set_room)`; інакше `restart` гри.
- КОЛИ `counter(staff_pieces, =, 6)` → ТО `custom: «посох зібрано — фінальна кімната»`, далі `win`.
- Перемога: 6 частин посоху → знищити Morbius. Поразка: життя скінчились без монети. Рахунок: відсоток відвіданих кімнат і знайдених магічних предметів.

## Керування і ввід
- Хрестовина — 4 діагональні напрямки ізометрії; кнопки — стрибок і взяти/покласти; меню — вибір і застосування зілля (?).
- Будування сходів: поклади блок, стань на нього, стрибни вище.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` (?).
- `game-screen`: кімната + HUD: життя (до 10 значків), дози зілля (?).
- `inventory-window`: зілля й предмети, відсоток відвіданих кімнат, кількість знайдених магічних предметів.
- `map-window`: відвідані кімнати й відомі виходи.
- Переходи: гра ↔ інвентар/мапа; смерть без життів → продовження з монетою або спочатку.

## Фічі поза полем
- `continue` за монету з фіксованої кімнати; паролів/сейвів не згадано (?).
- Мапа автоматично малює відвідане.

## Варіації й родичі
- Equinox (1993, SNES) — 450 кімнат у 8 підземеллях, обертання камери (Mode 7).
- Попередники: [Knight Lore](knight-lore.md), [Head over Heels](head-over-heels.md); прототип вплинув на Tactics Ogre.
- Осі: **радіус дії бонусу** (кімната / до смерті / на рівень); **сходинки** (штовхані блоки / заморожені падаючі / їзда на кулі); **ресурс допомоги** (дози зілля, які легко змарнувати).

## Цікавинки для курсу
- Зілля з обмеженими дозами, що діють лише в кімнаті, і їх можна поєднувати — 📎.
- Заморозка часу, після якої падаючі блоки стають сходинками — 📎.
- Невидимі платформи, що зʼявляються від зілля — 🌱.
- Будування сходів з блоків у ізометричній сітці висот — 🥈.
- Виходи, що зʼявляються на мапі лише після завдання, і автомапа відвіданого — 🥉.
- Монета-продовження з фіксованої кімнати — 🌱.

## Мапа на каталог
- Є: `inventory` · `inventory-items` (зілля) · `item-pickup` · `key-and-door` (магічні ключі) · `gravity-fall` · `push-object` · `carrier-platform` (куля, конвеєр) · `timed-despawn` (мости) · `touch-death` · `environment-death` · `player-death` · `teleport` (портали) · `temporary-modes` (зілля) · `explode-area` (бомби) · `map-window` · `collect-quota` (6 частин) · `game-screen`.
- **Нема** → пропозиції карток:
  - `+room-scoped-effect` «Бонус діє лише до виходу з кімнати» · entities/state · 🌱.
  - `+freeze-time` «Зупинити все рухоме в кімнаті» · entities/state · 📎.
  - `+reveal-invisible` «Показати невидимі обʼєкти» · entities/state · 🌱.
  - `+hidden-exit-after-task` «Вихід зʼявляється після завдання» · levels/progression · 🌱.
  - `+continue-token` «Предмет-продовження після втрати всіх життів» · game-logic/lose · 🌱.
  - `+stack-to-climb`, `+flip-screen-rooms` — як у [Knight Lore](knight-lore.md).

## Пропозиції до словників
- `+effect:freeze_all(scope)` — зупинити всі рухомі сутності в області (Solstice).
- `+effect:clear_room` — знищити всі рухомі сутності в кімнаті.
- `+feature:room-scoped-powerup` — бонус зникає при виході з кімнати.
- `+card:room-scoped-effect`, `+card:freeze-time`, `+card:reveal-invisible`, `+card:hidden-exit-after-task`, `+card:continue-token` — див. вище.

## Джерела
- ⭐ [Wikipedia: Solstice (1990)](https://en.wikipedia.org/wiki/Solstice_(1990_video_game)) — 250 кімнат, 6 частин посоху, чоботи, 4 зілля по 2 дози, блоки й кулі, ключі, бомби, портали, пастки, вороги, життя, монети, мапа, інвентар, Equinox.
- YouTube: пошук «Solstice NES gameplay».

## Непевне
- (?) Кнопки й меню вибору зілля; чи Шадакс носить блоки, чи лише штовхає (Wikipedia: «pick up and drop objects»).
- (?) Чи є паролі; склад HUD — з памʼяті.
- (?) Чи вороги рухаються за маршрутами, чи переслідують.
- (?) Які саме кімнати потребують ключів і що значить «clear» кімнату.
