---
title: Wilmot's Warehouse
slug: wilmots-warehouse
family: build-sim
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: score
year: 2019
platforms: [PC, macOS, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wilmot%27s_Warehouse", best: true, note: "цикл «доставка → службове вікно → апгрейди», зірки, кооп, Expert Mode"}
  - {kind: steam, url: "https://store.steampowered.com/app/839870/Wilmots_Warehouse/", note: "опис: штовхати, сортувати, складати; 500 товарів; кооп спліт-скрін"}
  - {kind: other, url: "https://store.steampowered.com/app/2060590/Wilmot_Works_It_Out/", note: "наступник 2024 — пазли сортування"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wilmot_Works_It_Out", note: "наступник"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wilmot%27s+warehouse+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, push-object, inventory-limit, collect-quota, time-out, time-bonus, shop-between-levels, in-round-upgrades, sequential-levels, save-progress, keyboard-controls, player-camera, +push-chain, +carry-cluster, +order-queue, +field-expansion, +self-organised-storage, +timelapse-replay, +star-currency]
proposes: ["+trigger:input", "+trigger:timer", "+trigger:schedule", "+trigger:counter", "+cond:free", "+cond:has", "+cond:same", "+effect:push", "+effect:move", "+effect:carry", "+effect:attach", "+effect:detach", "+effect:spawn_at", "+effect:take", "+effect:currency", "+effect:choose", "+effect:unlock", "+role:tile", "+role:zone", "+role:neutral", "+ui:timer-countdown", "+ui:objective-text", "+ui:progress-bar", "+window:upgrade-window", "+window:replay-window", "+feature:mode-coop", "+feature:mode-hardcore", "+feature:replay", "+axis:control", "+card:self-organised-storage"]
author: opus
date: 2026-11-02
---

# Wilmot's Warehouse — склад-сітка, на якому порядок вигадуєш ти, а клієнти перевіряють, чи ти його памʼятаєш

## Суть
Wilmot — квадратик на сітці складу: привозять вантажівку товарів-плиток (картинки без назв), гравець штовхає й переносить їх і розкладає **як хоче** (за кольором, темою, частотою). Потім відчиняється службове вікно, клієнти просять конкретні товари, і їх треба швидко знайти й принести — швидкість дає зірки, зірки купують апгрейди. Головоломка — не в полі, а в голові: гравець сам придумує систему категорій і перебудовує її, коли товарів стає сотні. Мета-пазл «організуй власну сітку»: правила гри не кажуть, що правильно.

## Поле і час
- Квадратна сітка складу; камера слідує за Wilmot-ом, видно частину складу (?) — пошук товару = памʼять + рух.
- Шари: підлога · товари (1 плитка = 1 клітина, однотипні товари — окремі копії) · стіни/колони · зона доставки (двері вантажівки) · службове вікно (прилавок).
- Real-time, «день» = фаза доставки й розкладання (обмежений час) → фаза клієнтів (кожен клієнт має свій таймер терпіння) → підсумок і апгрейди.
- Склад **росте**: апгрейд розширення відкриває нові ряди клітин.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Wilmot | player | швидкість, місткість перенесення | рух 4 напрямки; штовхає товари; підхоплює й несе групу |
| Товар | tile | тип (іконка), без назви | лежить у клітині; штовхається, переноситься; ідентичні копії взаємозамінні |
| Вантажівка / зона доставки | spawner | партія товарів | на початку дня висипає нові товари біля дверей |
| Службове вікно | zone | — | сюди треба принести запитаний товар |
| Клієнт | neutral | список запитів, таймер терпіння | стоїть у вікні, доки не отримає все або не мине час |
| Стіна / колона | static | — | непрохідна; ділить склад на проходи |
| Колега (кооп) | ally | — | другий Wilmot у кооперативі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(wilmot, dir)`; ЯКЩО попереду товар → ТО `push` (ряд товарів зсувається, якщо за ним вільно (?)); інакше `block`.
- КОЛИ `input(grab)` → ЯКЩО поруч товар і `count(carried, <, capacity)` → ТО `attach(wilmot, item)` — товар їде разом із Wilmot (група перенесення); `input(release)` → `detach` усіх (?).
- КОЛИ `schedule(day_start)` → ТО `spawn_at(batch, truck_zone)`; таймер розкладання `timer(start)`.
- КОЛИ `timer(prep) == 0` → ТО відчиняється вікно; приходять клієнти з запитами (типи й кількість).
- КОЛИ `contact(carried_item, hatch)` → ЯКЩО `same(item.type, request.type)` → ТО `take(wilmot, item)`, запит виконано; клієнт задоволений, коли всі його запити виконано.
- КОЛИ клієнт обслужений швидко → ТО `currency(stars, +n)` (більше за швидкість); `timer(customer) == 0` → клієнт іде без зірок (?).
- КОЛИ `input(buy, upgrade)` між днями → ЯКЩО `has(stars, cost)` → ТО `unlock(upgrade)`: ривок (dash), більша місткість перенесення, розширення складу, таймлапс тощо.
- Кожні кілька днів — день без ліміту часу для перебудови складу.
- Поразки нема (за звичайних правил): гірше розкладено → повільніше → менше зірок. Expert Mode додає модифікатори-обмеження.
- Рахунок: зірки (Performance/Progress Stars) за швидкість обслуговування.

## Керування і ввід
- Геймпад/клавіатура: 4 напрямки руху, кнопка «взяти/відпустити» товари, ривок (після апгрейда).
- Перенесення групою: підхоплені товари рухаються як єдине тіло з Wilmot-ом — розклад робиться «пакетами».
- Кооп: два гравці на спліт-скріні (потрібен хоч один геймпад).

## Вікна, меню, HUD
- `main-menu`: Нова гра / Продовжити, Кооп, Expert Mode, Налаштування.
- `game-screen`: склад + `timer-countdown` фази; під час клієнтів — у вікні запити картинками (`objective-text`-аналог) і таймери терпіння (`progress-bar`).
- `end-screen` дня: зірки за клієнтів, підсумок.
- `upgrade-window`: вибір апгрейдів за зірки.
- `replay-window`: **таймлапс** — прискорений повтор, як мінявся склад день за днем (купується апгрейдом).
- Переходи: main-menu → game-screen (доставка) → (таймер) → game-screen (клієнти) → end-screen → upgrade-window → наступний день.

## Фічі поза полем
- `save-progress` (кампанія з днів), `mode-coop` (спліт-скрін), Expert Mode (`mode-hardcore`-подібний з модифікаторами), таймлапс як `replay` усієї кампанії.
- Нема інструментів підказки «де лежить товар» — пошук принципово на памʼяті гравця (?).

## Варіації й родичі
- Wilmot Works It Out (2024) — той самий персонаж, пазли «сортуй предмети в кімнаті» без часу.
- Родичі: Sokoban (штовхання в сітці), Overcooked (черга замовлень + таймер), Factorio/Shapez (логістика, але автоматична), Unpacking (розкладання без правил), Moving Out.
- **Осі варіацій**: хто вирішує «правильний» порядок (гра / гравець) · як переносити (штовхати поодинці / ряд / нести групу) · тиск (таймер клієнта / без часу) · поле (фіксоване / росте) · назви товарів (є / лише картинки).

## Цікавинки для курсу
- Перенесення групи плиток як одного тіла з перевіркою, що всі клітини вільні — 🥉 (рух поліоміно, складеного на льоту).
- Черга клієнтів із таймерами терпіння й запитами за типом — 📎.
- Розширення поля апгрейдом (нові ряди сітки) — 🌱.
- Таймлапс складу: знімок поля щодня + відтворення — 📎 (`state-as-data`).
- Штовхання ряду товарів — 📎 (`+push-chain`).
- Мета-пазл «твоя власна система категорій»: генератор партій зі схожими/двозначними товарами — 🥈 (дизайн даних, не код).

## Мапа на каталог
- Є: `move-4dir` · `push-object` · `inventory-limit` (місткість перенесення) · `collect-quota` (запити клієнта) · `time-out` (фаза доставки) · `time-bonus` (зірки за швидкість) · `shop-between-levels` (апгрейди) · `in-round-upgrades` · `sequential-levels` (дні) · `save-progress` · `keyboard-controls` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+carry-cluster` «Нести групу плиток як одне тіло» · entities/move · 🥉 · слот {capacity} — родич `stick-together`.
  - `+order-queue` «Черга замовлень із таймером терпіння» · game-logic · 📎 · слоти {max_customers, patience} (Overcooked, Diner Dash).
  - `+field-expansion` «Розширення поля апгрейдом» · levels/progression · 🌱 (родич `+bag-expansion` з Backpack Hero).
  - `+self-organised-storage` «Гравець сам задає порядок, гра перевіряє швидкістю» · game-logic · 🥈.
  - `+timelapse-replay` «Таймлапс станів поля» · interface/results · 📎 — дитина `replay`.
  - `+star-currency` «Зірки за швидкість як валюта апгрейдів» · game-logic/economy · 🌱.
  - `+push-chain` (з Cell Machine) — повторно.

## Пропозиції до словників
- `+trigger:input`, `+trigger:timer` (фаза), `+trigger:schedule` (початок дня), `+trigger:counter` (усі запити виконано).
- `+cond:free`, `+cond:has` (зірки), `+cond:same` (тип товару = запит).
- `+effect:push`, `+effect:move`, `+effect:carry`, `+effect:attach`/`+effect:detach` (група перенесення), `+effect:spawn_at` (доставка), `+effect:take` (віддати клієнту), `+effect:currency`, `+effect:choose`/`+effect:unlock` (апгрейди).
- `+role:tile` (товар), `+role:zone` (вікно, зона доставки), `+role:neutral` (клієнт).
- `+ui:timer-countdown`, `+ui:objective-text` (запит картинкою), `+ui:progress-bar` (терпіння).
- `+window:upgrade-window`, `+window:replay-window` (таймлапс).
- `+feature:mode-coop`, `+feature:mode-hardcore` (Expert Mode), `+feature:replay`.
- `+axis:control` = `direct` + grab-throw-подібне перенесення.
- `+card:self-organised-storage` — див. вище.

## Джерела
- ⭐ [Wikipedia: Wilmot's Warehouse](https://en.wikipedia.org/wiki/Wilmot%27s_Warehouse) — цикл гри, апгрейди (ривок, більше перенесення, розширення, таймлапс), кооп, Expert Mode, автори (Hollow Ponds, Finji).
- [Steam](https://store.steampowered.com/app/839870/Wilmots_Warehouse/) — опис: штовхання, сортування, 500 товарів, Performance Stars.
- [Wilmot Works It Out (Steam)](https://store.steampowered.com/app/2060590/Wilmot_Works_It_Out/) · [Wikipedia](https://en.wikipedia.org/wiki/Wilmot_Works_It_Out) — наступник.
- YouTube: пошук «wilmot's warehouse gameplay».

## Непевне
- (?) Точна механіка підхоплення: чи береться весь суміжний кластер, чи по одному до ліміту; початкова місткість — з памʼяті, не перевірено.
- (?) Чи штовхається ряд товарів, чи лише один.
- (?) Що буває, коли клієнт не дочекався (штраф/нуль зірок); кількість клієнтів одночасно.
- (?) Розмір видимої області й чи є мапа складу; офіційний сайт недоступний (сертифікат), Thinky Games 403, WebSearch вичерпано.
