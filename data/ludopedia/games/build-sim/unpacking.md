---
title: Unpacking
slug: unpacking
aka: [Розпакування]
family: build-sim
also: [thinky]
klass: cursor
axes:
  field: free
  time: static
  opponent: none
  info: partial
  random: none
  goal: state
year: 2021
platforms: [PC, macOS, Linux, Switch, Xbox One, PS4, PS5, iOS, Android]
links:
  - {kind: official, url: "https://www.unpackinggame.com/", best: true, note: "офіційний сайт: суть, червоний контур неправильних місць, доступність, «Allow items anywhere»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Unpacking_(video_game)", note: "8 переїздів (1997–2018), 35 кімнат, обовʼязкові місця для частини речей"}
  - {kind: steam, url: "https://store.steampowered.com/app/1135690", note: "фічі: без таймерів, лічильників і рахунку; досягнення, Cloud"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=unpacking+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [drag-drop-piece, cell-click, hover-highlight, multi-cell-size, completion-detection, satisfy-constraints, conflict-highlight, sequential-levels, achievements-window, controls-remap, field-scaling, volume-control, music-toggle, sound-effects, +unpack-queue, +surface-slots, +stack-on-item, +allowed-zone-per-item, +room-switch, +validate-on-finish, +allow-anywhere-mode]
proposes: ["+cond:allowed_spot", "+trigger:all_placed", "+ui:item-hand", "+ui:room-tabs", "+feature:allow-anywhere", "+feature:motion-toggle", "+feature:outline-color", "+card:allowed-zone-per-item"]
author: opus
date: 2026-11-09
---

# Unpacking — дістаєш речі з коробок по одній і розкладаєш по полицях; рівень закритий, коли кожна річ на «своєму» місці

## Суть
Медитативний «block-fitting» пазл + декор: у кожному з восьми переїздів героїні (1997 → 2018) треба розпакувати коробки й розмістити всі речі в кімнатах — від однієї спальні до цілого будинку. Річ береться з відкритої коробки, кладеться на поверхню (полиця, шафа, підлога, стіна) або в іншу річ і має вміститися. Більшість речей можна класти будь-де, але **частина має призначене місце** (зубна щітка — у ванну, сковорідка — на кухню): поки вона не там, рівень не закривається, а помилка підсвічується червоним контуром. Правило «де місце речі» — головна механіка-перевірка; історія розповідається самими речами.

## Поле і час
- Кімната — піксельна сцена з набором **поверхонь** (полиці, стільниці, шухляди, гачки, підлога, стіни); кожна поверхня — горизонтальний відрізок/прямокутник, де річ займає ширину й висоту (`field: free`, але фактично «полиці-слоти» з колізією).
- Кілька кімнат на рівень (переміщення між ними з анімацією), усього 35 кімнат на 8 рівнів.
- Коробки стоять у кімнатах; вміст невідомий, доки не дістанеш (`info: partial`).
- Часу нема: без таймерів, лічильників і рахунку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Коробка | container | вміст (черга речей), кімната | клік — дістає наступну річ у руку; порожню можна прибрати |
| Річ | object | розмір, дозволені місця (або «будь-де») | кладеться на поверхню чи в контейнер, якщо вміщується |
| Річ із призначеним місцем | object | зона дозволу (кімната/тип поверхні) | не там — червоний контур, рівень не закривається |
| Поверхня (полиця, стільниця, підлога) | terrain | ширина, висота | приймає речі; річ, що не вміщується, не ставиться |
| Стіна | terrain | — | приймає настінні речі (картини, постери) |
| Меблі-контейнери (шафа, шухляда, холодильник) | container | місткість | відкриваються, мають внутрішні поверхні |
| Річ-підставка (тарілка, стос) | object | — | на неї можна класти/ставити інші речі (стос тарілок, книжки) |
| Кімната | zone | набір поверхонь | одиниця, між якими перемикається камера |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click box)` → ЯКЩО `count(item-in-box, >, 0)` → ТО `give(hand, item)` (наступна річ із коробки).
- КОЛИ `input(drop item on surface)` → ЯКЩО `fits(item, cell)` and `free(cell)` → ТО `place(hand, item)`; інакше `block`.
- КОЛИ `input(drop item on item)` → ЯКЩО `custom: «нижня річ — підставка/контейнер і є місце»` → ТО `place(hand, item)` (стос, річ у шухляду).
- КОЛИ `input(pick placed item)` → ТО `pickup(hand, item)` — переставити можна будь-коли.
- КОЛИ `input(drop item)` → ЯКЩО not `custom: «місце дозволене для цієї речі»` → ТО `custom: «червоний контур на речі»`.
- КОЛИ `all_gone(item-in-box)` → ЯКЩО `all_on(item, allowed-spot)` → ТО `win` (рівень закрито, наступний переїзд).
- КОЛИ `all_gone(item-in-box)` → ЯКЩО not `all_on(item, allowed-spot)` → ТО `custom: «підсвітити всі речі не на своїх місцях червоним; рівень не закривається»`.
- КОЛИ `input(open furniture)` → ТО `reveal(cell)` (внутрішні поверхні шафи/шухляди).
- КОЛИ `input(switch room)` → ТО `camera(room)` (з анімацією, її можна вимкнути).
- КОЛИ `mode(allow-items-anywhere)` → ТО `custom: «перевірка місць вимкнена — рівень закривається, коли розпаковано все»`.
- Перемога: усі речі розпаковані й ті, що мають місце, — на дозволених місцях · Поразки нема · Рахунку нема.

## Керування і ввід
- Миша/тач/геймпад: клік по коробці — дістати річ; drag — нести; клік/відпускання на поверхні — покласти; клік по покладеній — взяти знову.
- Обертання/перевертання частини речей (?); зум екрана; перемикання кімнат.
- Перепризначення клавіш, збільшені кнопки UI.

## Вікна, меню, HUD
- `main-menu`: Грати / продовжити → `level-select` (рівні-роки), Налаштування → `settings-window`, Вихід (?).
- `game-screen`: кімната, коробки, річ у руці, перемикач кімнат (`+ui:room-tabs`).
- `settings-window`: гучність музики й ефектів окремо, remap, розмір кнопок, зум, вимкнення анімації переходу кімнат, колір контуру помилки, «Allow items anywhere».
- `end-screen` рівня: фото/полароїд кімнати (?).
- `achievements-window` — досягнення Steam (за дрібні дії з речами (?)).
- HUD: `conflict-highlight` (червоний контур), `+ui:item-hand`.

## Фічі поза полем
- `levels-sequential` — 8 переїздів у хронологічному порядку.
- Доступність: `remap-controls`, `font-scale` ≈ більші кнопки, `+feature:motion-toggle`, `+feature:outline-color`, `+feature:allow-anywhere` (знімає пазл).
- `volume-sliders` (музика й ефекти окремо), `cloud-save` (Steam Cloud), `achievements`.
- Без таймерів, рахунку, штрафів.

## Варіації й родичі
- A Little to the Left (`a-little-to-the-left.md`) — те саме «прибирання», але правило приховане й варіантів розвʼязку кілька.
- Wilmot's Warehouse (`wilmots-warehouse.md`) — свої правила розкладу обирає гравець, гра їх не перевіряє.
- Save Room (`save-room.md`), Backpack Hero (`backpack-hero.md`) — вміщення в інвентар-сітку; тут — у сцену.
- Осі варіацій: **хто задає правило місця** (гра, явно / гра, приховано / гравець) · **поле** (полиці-відрізки / сітка інвентаря / вільне) · **перевірка** (одразу / наприкінці / ніколи).

## Цікавинки для курсу
- Черга речей у коробці + «рука» + перестановка покладеного — 🌱.
- Поверхня як відрізок із колізією ширин і стосування (річ на річ) — 📎.
- Таблиця «річ → дозволені зони» як дані + перевірка в кінці з підсвіткою — 📎.
- Кілька кімнат-сцен з перемиканням і спільним станом рівня — 🥉.
- Режим «Allow items anywhere» — один прапорець, що вимикає правило перемоги — 🌱 (вчить відокремлювати правила від двіжка).

## Мапа на каталог
- Є: `drag-drop-piece` · `cell-click` + `hover-highlight` · `multi-cell-size` (річ займає кілька «клітин» полиці) · `completion-detection` + `satisfy-constraints` · `conflict-highlight` (червоний контур) · `sequential-levels` · `achievements-window` · `controls-remap` · `field-scaling` (зум) · `volume-control` · `music-toggle` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+unpack-queue` «Коробка-черга речей» · entities/spawn · 🌱.
  - `+surface-slots` «Полиці-відрізки з колізією» · entities/legality · 📎.
  - `+stack-on-item` «Річ на річ» · entities/legality · 📎.
  - `+allowed-zone-per-item` «Дозволені місця речі» · game-logic/constraints · 📎 · слот {zones}.
  - `+room-switch` «Перемикання кімнат-сцен» · levels · 🥉.
  - `+validate-on-finish` «Перевірка лише в кінці» · game-logic/win · 🌱.
  - `+allow-anywhere-mode` «Вимкнути перевірку» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:allowed_spot` — сутність стоїть у дозволеній для неї зоні (Unpacking, A Little to the Left).
- `+trigger:all_placed` — запас/черга вичерпано (останню річ розпаковано); зараз пишеться через `all_gone(item-in-box)`.
- `+ui:item-hand` — річ «у руці» біля курсора; `+ui:room-tabs` — перемикач сцен.
- `+feature:allow-anywhere`, `+feature:motion-toggle`, `+feature:outline-color` — доступність.
- `+card:allowed-zone-per-item` — див. «Мапа на каталог».

## Джерела
- ⭐ [unpackinggame.com](https://www.unpackinggame.com/) — суть, червоний контур неправильного місця, доступність і «Allow items anywhere», платформи.
- [Wikipedia: Unpacking](https://en.wikipedia.org/wiki/Unpacking_(video_game)) — 8 етапів-років, 35 кімнат, обовʼязкові місця, дати, Witch Beam.
- [Steam](https://store.steampowered.com/app/1135690) — фічі: без таймерів/лічильників/рахунку, stack/hang/arrange, досягнення, Cloud.

## Непевне
- (?) Обертання речей і повна механіка стосування — у відкритих джерелах не описано.
- (?) Фінальний «полароїд» кімнати, фотоальбом і досягнення «за дрібні дії» — з памʼяті.
- (?) Пункти головного меню — не перевірено.
- (?) Наскільки поверхні справді дискретні (сітка в пікселях) — з власних спостережень, не з джерела.
