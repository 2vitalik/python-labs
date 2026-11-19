---
title: Kukulcan
slug: kukulcan
aka: [Kukulcan: The Feathered Serpent]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [Android, iOS]
links:
  - {kind: official, url: "http://www.black-spoon.com/press/sheet.php?p=kukulcan", best: true, note: "прескіт: опис механіки (скидає частини хвоста, обмежена довжина), фічі, історія, трейлер, скриншоти"}
  - {kind: official, url: "http://black-spoon.com/", note: "сайт Black Spoon Studio: ящики, лавові озера, телепорти, «plug fountains»"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=5jb9C_utq7Y", note: "офіційний трейлер (з прескіту)"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.BlackSpoon.Kukulcan", note: "Google Play: 70+ пазлів, 5 глав, додаткові випробування, перша глава безкоштовно"}
  - {kind: other, url: "https://apps.apple.com/us/app/kukulcan/id1547283070", note: "App Store: історія версій (ліміт кроків у випробуваннях)"}
  - {kind: other, url: "https://skich.app/games/kukulcan", note: "Skich: дата релізу Android 21.01.2025, опис"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=mcdPWTFOxwI", note: "iOS gameplay (IOSTouchplayHD), лінк зі Skich"}
stage: v1
coverage: 35
mechanics: [body-queue, push-object, height-levels, teleport, move-limit, sequential-levels, +bite-tail-into-block, +length-budget, +dam-water, +optional-challenges, +story-chapters]
proposes: ["+card:length-budget", "+card:dam-water"]
author: opus
date: 2026-11-19
---

# Kukulcan — пернатий змій скидає частини хвоста, і вони стають сходами, мостами й дамбами рівня

## Суть
Мобільна пазл-гра за мотивами Snake: гравець — змій-божество Кукулькан на клітинному 3D-острові з висотами. Головне дієслово — скинути частину хвоста: відкинутий шматок лишається на полі як будівельний блок — сходинка, міст, дамба для потоку, затичка для фонтана. Довжину, яку можна використати на рівні, обмежено, тому тіло — ресурс. Додатково: ящики, лавові озера, телепорти й інші «здібності»; 70+ пазлів у 5 главах, у кожній — додаткові випробування. Black Spoon Studio (Швейцарія, випускники ZHdK), розробка з 2018, реліз 2025.

## Поле і час
- Ізометричний вигляд на тайлову сітку з рівнями висоти (тераси, уступи, стіни); на скриншотах тіло змія стоїть вертикальною колоною біля уступу («Climb obstacles») — висота важлива для руху (`field: 3d`).
- Шари: плитки підлоги різної висоти · вода (потоки, водоспади, фонтани з плиток) · лава · обʼєкти (ящики, водяне колесо, проходи-брами, золотий ідол).
- Хід — дискретний (випробування мають «limit of steps»); чи є реальний час — не видно (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кукулькан (змій) | player | довжина тіла (ліміт рівня) | рухається клітинами, тіло тягнеться слідом (від Snake); може лізти на уступи |
| Скинута частина хвоста | object | розмір шматка (?) | стає частиною рельєфу: сходинка, міст, дамба, затичка фонтана |
| Ящик | object | — | пересувний («moveable boxes») |
| Потік / водоспад | terrain | напрям | тіло чи блок у потоці його перекриває («Dam water») |
| Фонтан | terrain | — | струмінь із плитки; затикається частиною тіла |
| Лавове озеро | hazard | — | небезпека (?) |
| Телепорт | terrain | пара (?) | переносить змія |
| Золотий ідол | pickup | — | є на кожному скриншоті рівня; імовірно ціль або колекційка (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(head, dir)`, тіло слідом `custom: «кожен сегмент на місце попереднього»` (?).
- КОЛИ `input(drop_tail)` → ТО `detach(tail_part, snake)`, `transform(tail_part, block)` — шматок лишається на полі як рельєф.
- КОЛИ `custom: «довжину рівня вичерпано»` → ТО `custom: «скидати більше нічого»` — ліміт довжини на рівень.
- КОЛИ `contact(snake, box)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `custom: «скинутий шматок або тіло в потоці / на фонтані»` → ТО `block` потоку (дамба, затичка).
- КОЛИ `enter(snake, teleport)` → ТО `teleport(snake, pair)` (?).
- КОЛИ `counter(steps, >, limit)` → ТО `custom: «додаткове випробування провалено»` (ліміт кроків у випробуваннях).
- Перемога: розвʼязати пазл (ціль рівня — ймовірно дійти до ідола / виходу (?)). · Поразка: (?) · Рахунку нема; випробування — додаткові умови.

## Керування і ввід
- Сенсорний екран (Android, iOS); конкретні жести (свайп / тап по клітині, кнопка скидання) не перевірено (?).

## Вікна, меню, HUD
- `main-menu`, вибір глави й рівня (`chapter-select` / `level-select`) — за описом «five chapters» (?).
- `game-screen` — ізометричне поле; лічильник довжини / кроків випробування (?).
- `shop-window`-подібна покупка Premium (уся гра + пернаті скіни).

## Фічі поза полем
- Перша глава безкоштовно, Premium відкриває решту й скіни (`unlockables`), реклами нема.
- 5 глав, 70+ пазлів, додаткові випробування в кожній главі (ліміт кроків тощо); саундтрек, написаний для гри.

## Варіації й родичі
- [Would You Love Me If I Was a Snake?](would-you-love-me-if-i-was-a-snake.md) — відкушений хвіст стає блоком; [Snakebird](snakebird.md) — тіло як опора; [Lime Rick](lime-rick.md) — слід як опора; [Snekcross](snekcross.md) — тіло як міст.
- [A Monster's Expedition](a-monsters-expedition.md) — колода стає мостом; тут міст із власного тіла.
- Осі варіацій: **що стає з відкинутим тілом** — блок (Kukulcan, Would You Love Me…) / зникає / ворог · **ресурс тіла** — ліміт довжини на рівень / ріст від їжі · **стихії** — вода (перекрити), лава (подолати).

## Цікавинки для курсу
- Тіло як обмежений будівельний ресурс: від'єднати кінець черги-тіла й записати як статичну клітину рельєфу — 📎.
- Потік води по клітинах, який перекриває будь-яка тверда клітина (дамба / затичка) — 🥉.
- Рух змія з висотами (підйом колоною на уступ) — 🥈.

## Мапа на каталог
- Є: `body-queue` ↔ тіло змія; `push-object` ↔ ящики; `height-levels` ↔ тераси й підйом; `teleport` ↔ телепорти; `move-limit` ↔ ліміт кроків у випробуваннях; `sequential-levels` ↔ глави.
- **Нема** → пропозиції карток:
  - `+bite-tail-into-block` (є в корпусі) — тут не укус, а скидання частини хвоста.
  - `+length-budget` «Довжина тіла — бюджет рівня для будівництва» · entities/state · 🌱.
  - `+dam-water` «Тверда клітина перекриває потік / фонтан» · entities/interact · 📎.
  - `+optional-challenges`, `+story-chapters` — уже в корпусі.

## Пропозиції до словників
- Нових слів правил нема: скидання хвоста лягає в ⏳ `detach` + `transform`.
- `+card:length-budget`, `+card:dam-water` — див. «Мапа на каталог».

## Джерела
- ⭐ [Прескіт Black Spoon: Kukulcan](http://www.black-spoon.com/press/sheet.php?p=kukulcan) — опис: «drop off parts of its tail to create stairs, bridges, plug fountains», «only a limited length can be used in each level», фічі («Game character is part of the level architecture», 70+ рівнів), історія (натхнення Snake), трейлер, скриншоти рівнів.
- [Сайт black-spoon.com](http://black-spoon.com/) — «Moveable boxes, lava lakes, teleporters and further exciting abilities».
- [Google Play](https://play.google.com/store/apps/details?id=com.BlackSpoon.Kukulcan) — опис, 5 глав, додаткові випробування, Premium; скриншоти з підписами «Climb obstacles», «Dam water».
- [App Store](https://apps.apple.com/us/app/kukulcan/id1547283070) — історія версій 2025: «Fixed the limit of steps for challenge 4 in chapter 3».
- [Skich](https://skich.app/games/kukulcan) — дата релізу Android (21.01.2025), посилання на геймплейне відео.

## Непевне
- (?) Точні правила руху (як тіло лізе на висоту, чи є гравітація) — видно лише на скриншотах; трейлер і геймплей не переглянуто.
- (?) Як скидається хвіст (кнопка, жест, розмір шматка) і чи скинутий шматок зменшує довжину змія.
- (?) Що робить лава (смерть, лише прохід по мосту з тіла?) і як працюють телепорти.
- (?) Ціль рівня: золотий ідол на кожному скриншоті — ціль або колекційка.
- (?) `time: turn` — висновок з «limit of steps» у випробуваннях.
