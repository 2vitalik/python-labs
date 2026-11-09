---
title: Save Room – Organization Puzzle
slug: save-room
aka: [Save Room]
family: build-sim
also: [board-digital]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [PC, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1955330/Save_Room__Organization_Puzzle/", best: true, note: "опис: вмістити всі предмети, зброя заряджена, здоровʼя не низьке; комбінування трав і пороху; 40 рівнів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Save_Room_%E2%80%93_Organization_Puzzle", note: "поворот і фіксація, комбінування звільняє місце, гнила їжа, патрони на кілька гармат, консолі 11.11.2022, сиквел The Merchant"}
  - {kind: other, url: "https://indiegamesplus.com/save-room-organization-puzzle-review/", note: "огляд: 40 пазлів, суть — правильні комбінації й розміщення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Save+Room+Organization+Puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [polyomino-placement, piece-rotate-flip, drag-drop-piece, inventory-limit, multi-cell-size, satisfy-constraints, completion-detection, sequential-levels, level-select, achievements-window, hp-damage, +item-combine, +load-into-item, +use-order-frees-space, +attache-case-packing]
proposes: ["+effect:combine", "+effect:reload", "+cond:fits_all", "+ui:health-bar-item", "+ui:examine-text", "+card:item-combine", "+card:load-into-item"]
author: opus
date: 2026-11-09
---

# Save Room — кейс у стилі Resident Evil 4: вмісти всі фігурні предмети, а щоб вистачило місця — змішуй трави, заряджай гармати й лікуйся

## Суть
Чистий пазл пакування: є сітка кейса (attaché case) і набір предметів-поліміно — зброя, патрони, ліки, трави, інструменти. Мета рівня — вмістити **все**, при цьому зброя має бути заряджена, а здоровʼя — не надто низьким. Крім повороту й розміщення, предмети можна **поєднувати** (трави → ліки, порох → патрони) і **використовувати** (зарядити гармату патронами, зʼїсти/вжити ліки), і правильний порядок дій звільняє клітини. 40 рукотворних рівнів, без часу й ворогів.

## Поле і час
- Квадратна сітка кейса (розмір змінюється від рівня до рівня (?)); предмети займають прямокутні або фігурні групи клітин.
- Поза кейсом — зона, де лежать ще не розміщені предмети (`supply`).
- Часу нема: хід — розміщення, поворот, поєднання чи використання предмета; програшу нема, лише «ще не розвʼязано».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кейс | zone | сітка W×H | приймає предмети без накладання |
| Пістолет, дробовик, гвинтівка… | piece | форма, магазин | займає клітини; приймає патрони свого типу |
| Коробка патронів | piece | тип, кількість | кладеться на сумісну гармату → заряджає й зникає/зменшується |
| Порох | piece | — | два порохи → патрони |
| Трава | piece | колір | поєднується з іншою травою в лікувальний предмет |
| Лікувальний предмет (спрей, суміш трав) | piece | +здоровʼя | вжити → здоровʼя зростає, предмет зникає |
| Гнила їжа | piece | −здоровʼя | вжити → шкода (щоб потім можна було вжити ліки) |
| Інструменти / інше | piece | форма | лише розмістити |
| Здоровʼя героя | mark | рівень | обмеження: не нижче порогу; ліки не можна «витратити» на повне здоровʼя (?) |
| Зона запасу | supply | — | предмети, які ще треба вмістити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, item)` → ЯКЩО `fits(item, case_cells)` → ТО `place(player, item)`; інакше `block`.
- КОЛИ `input(rotate, item)` → ТО `rotate(item, 90)`.
- КОЛИ `input(drag, item_a, item_b)` → ЯКЩО `same(item_a, item_b, combinable)` → ТО `merge(item_a, item_b, product)` — трави → ліки, порох + порох → патрони; звільняє клітини.
- КОЛИ `input(drag, ammo, gun)` → ЯКЩО `same(ammo, gun, caliber)` → ТО `custom: «заряджає магазин»`, `disappear(ammo)` або `counter(ammo_count, -n)`.
- КОЛИ `input(use, healing_item)` → ТО `heal(hero, n)`, `disappear(healing_item)`.
- КОЛИ `input(use, rotten_food)` → ТО `damage(hero, n)`, `disappear(rotten_food)`.
- КОЛИ `input(examine, item)` → ТО `message(item_info)`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «запас порожній»` and `custom: «уся зброя заряджена»` and `custom: «здоровʼя не нижче порогу»` → ТО `win`, `next_level`.
- Перемога: усі предмети в кейсі + умови · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Миша/стик: схопити предмет → тягнути по сітці (тінь розміщення) → поворот кнопкою (?) → відпустити.
- Покласти предмет на інший — спроба поєднання або зарядження; окрема дія — використати/оглянути.

## Вікна, меню, HUD
- `game-screen`: сітка кейса, зона запасу, індикатор здоровʼя (`+ui:health-bar-item`), текст огляду предмета (`+ui:examine-text`), `drag-ghost`.
- `level-select` — 40 рівнів; `main-menu` → `level-select` → `game-screen` → `end-screen` (рівень розвʼязано) → наступний.
- `settings-window` (звук, музика); `achievements-window` (Steam).

## Фічі поза полем
- `levels-sequential` + `level-select`; досягнення Steam, картки.
- `restart-level` (?); undo — не бачив у джерелах.
- Сиквели: Save Room – The Merchant (крамниця: купити/продати предмети, щоб розвʼязати), The Auto Sort Is Broken (у бандлі; механіку не перевіряв).

## Варіації й родичі
- Родичі в корпусі: `backpack-hero` і `backpack-battles` (рюкзак-сітка, але з боєм і сусідством), `wilmots-warehouse` (склад-сітка з памʼяттю), board-digital `patchwork`, `fits`, `ubongo`, `pentomino`, `a-feast-for-odin-polyomino` (поліміно-пакування).
- Осі «пакування»: просто вмістити (Save Room базовий) / вмістити з дієсловами над предметами (поєднати, зарядити, вжити) / з цінністю й сусідством (Backpack Hero).
- Осі «зникнення предмета»: ніколи / поєднання / використання / продаж (The Merchant).

## Цікавинки для курсу
- Поліміно-пакування в прямокутник з поворотом — 🥉 (`polyomino-placement`).
- Поєднання двох предметів у третій, що займає менше — 📎 (таблиця рецептів як дані).
- Зарядження: предмет «всередину» іншого за сумісністю типу — 📎.
- Порядок дій як частина розвʼязку (спершу пошкодитись гнилою їжею, потім лікуватись) — 🥉.
- Розвʼязувач рівня (пошук розміщення + дії) — 🥇.

## Мапа на каталог
- Є: `polyomino-placement` · `piece-rotate-flip` · `drag-drop-piece` · `inventory-limit` (кейс) · `multi-cell-size` · `satisfy-constraints` + `completion-detection` · `sequential-levels` + `level-select` · `achievements-window` · `hp-damage` (здоровʼя героя як обмеження).
- **Нема** → пропозиції карток:
  - `+item-combine` «Два предмети → один» · entities/interact · 📎 · слот {recipes}.
  - `+load-into-item` «Зарядити предмет іншим» · entities/interact · 📎 · слот {compat}.
  - `+use-order-frees-space` «Використання предмета звільняє клітини» · game-logic/constraints · 🌱.
  - `+attache-case-packing` «Вмістити все в кейс» · game-logic/win · 🌱 — ціль-обмеження «запас порожній».

## Пропозиції до словників
- `+effect:combine` — два предмети стають третім за рецептом (відмінне від `merge` значень 2048 рецептурою).
- `+effect:reload` — патрони переходять у гармату за типом.
- `+cond:fits_all` — усі предмети запасу вміщаються (ціль рівня).
- `+ui:health-bar-item` — індикатор здоровʼя героя на екрані інвентаря; `+ui:examine-text` — текст огляду предмета.
- `+card:item-combine`, `+card:load-into-item` — див. вище.

## Джерела
- ⭐ [Steam: Save Room](https://store.steampowered.com/app/1955330/Save_Room__Organization_Puzzle/) — ціль (усе вмістити, зброя заряджена, здоровʼя не низьке), огляд, перезарядка, трави й порох, порядок дій звільняє місце, 40 рівнів, Fractal Projects, 28.04.2022.
- [Wikipedia](https://en.wikipedia.org/wiki/Save_Room_%E2%80%93_Organization_Puzzle) — поворот і фіксація, комбінування прибирає предмети, гнила їжа, патрони для кількох гармат типу, консолі (Ratalaika, 11.11.2022), сиквел The Merchant.
- [Indie Games Plus: огляд](https://indiegamesplus.com/save-room-organization-puzzle-review/) — 40 пазлів, складність у комбінаціях і розміщенні.
- YouTube: пошук «Save Room Organization Puzzle gameplay».

## Непевне
- (?) Розміри кейса й набір форм предметів по рівнях — у джерелах нема.
- (?) Чи предмети лише прямокутні, чи бувають L-подібні — «inventory tetris» у PC Gamer, але форми не описані.
- (?) Чи можна викинути предмет — за ціллю («усе вмістити») ні, але прямо не підтверджено.
- (?) Чи можна вжити ліки при повному здоровʼї; поріг «не надто низького» здоровʼя.
- (?) Undo і рестарт рівня — не бачив.
