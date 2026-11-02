---
title: Carto
slug: carto
family: thinky
also: [board-digital]
klass: hybrid
axes:
  field: layers
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 2020
platforms: [PC, Mac, PS4, Xbox One, Switch]
links:
  - {kind: other, url: "https://www.gameinformer.com/review/carto/carto-review-putting-the-pieces-together", best: true, note: "найкраще пояснення ядра: ребра тайлів мають збігатися, зміни мапи миттєво міняють світ, можна перенести тайл разом із собою, пізніше — тетроміно-тайли"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Carto_(video_game)", note: "Sunhead Games, Humble Games, натхнення Carcassonne"}
  - {kind: steam, url: "https://store.steampowered.com/app/1172450/Carto/", note: "демо, 5–7 годин"}
  - {kind: official, url: "http://www.sunheadgames.com/", note: "студія"}
  - {kind: other, url: "https://www.siliconera.com/review-carto-combines-environmental-storytelling-literal-world-building/", note: "NPC-запити «побудуй місце», нагорода — нові тайли, Story Chalet"}
  - {kind: other, url: "https://www.nme.com/reviews/carto-review-a-map-making-puzzler-where-whimsy-turns-finicky-2804939", note: "топографічні правила: дорога до дороги, море не можна замкнути в суші"}
  - {kind: other, url: "https://www.nintendoworldreport.com/review/55335", note: "обертання лісових тайлів, лабіринт, сюжетні віньєтки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Carto+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, impassable-cells, item-pickup, inventory-items, drag-drop-piece, game-screen, help-window, save-progress, settings-window, sequential-levels, player-camera, +world-map, +tile-edge-matching, +map-is-world, +carry-tile-with-player, +tile-rotate, +polyomino-tiles, +layout-request, +tile-reveal-reward]
proposes: ["+trigger:input", "+trigger:pattern", "+trigger:layout_formed", "+cond:edges_match", "+cond:fits", "+cond:occupied", "+effect:rotate", "+effect:place", "+effect:move", "+effect:spawn_at", "+effect:give", "+effect:message", "+role:tile", "+role:neutral", "+role:zone", "+window:map-window", "+window:dialogue-window", "+window:inventory-window", "+ui:tile-tray", "+feature:onboarding-hints", "+axis:field-scale"]
author: opus
date: 2026-11-02
---

# Carto — перекладай шматки карти, і світ навколо героїні перебудовується: «Carcassonne, по якому ходиш»

## Суть
Дівчинка-картографка Карто ходить світом, складеним із квадратних **тайлів карти**. Відкривши карту, гравець переставляє й обертає тайли — і світ миттєво стає саме таким: нові береги, дороги, проходи. Тайли можна ставити лише так, щоб **ребра збігалися** (дорога до дороги, річка до річки, ліс до лісу), як у Carcassonne. Пазли — запити мешканців («живу посеред найбільшого лісу», «зустрінемось на північному причалі») і загадки з підказок у світі; розвʼязок дає нові тайли. Клас — **hybrid**: аватар ходить по світу (avatar), карта редагується «рукою» (cursor).

## Поле і час
- **Два масштаби одного поля** (`field: layers`): макро-сітка тайлів (карта, кілька клітин на кілька) і мікро-світ усередині кожного тайла, де героїня вільно ходить (top-down, real-time).
- Тайл = квадратна ділянка з чотирма ребрами; кожне ребро має тип рельєфу (вода, пісок/берег, трава, ліс, дорога, сніг…). Пізніше — тайли-поліоміно (форми тетрісу) і тайли з особливими правилами руху.
- Межа світу = межа зібраних тайлів: за край не пройти.
- Час real-time для ходьби; редагування карти відбувається у вікні карти (світ стоїть).
- Видимість частково обмежена: невідомі тайли ще треба знайти; є «туманні» загадки (ліс-лабіринт).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карто | player | позиція у світі, тайл під нею | ходить у 4/8 напрямках (?), говорить, збирає, відкриває карту |
| Тайл карти | tile | 4 ребра з типами рельєфу, орієнтація, форма (квадрат/поліоміно) | переміщується й обертається на карті; його вміст = ділянка світу |
| Тайл під Карто | tile | — | переноситься **разом із героїнею** (швидке переміщення) |
| Ребро тайла | zone | тип рельєфу | має збігатися з ребром сусіда; море не можна «замкнути» в суші |
| Новий тайл (знахідка) | pickup | — | зʼявляється як нагорода за пазл/запит, додається на карту |
| Мешканець (NPC) | neutral | запит-умова на розкладку | дає загадку/підказку; зʼявляється в місці, яке ти «збудував» |
| Ключовий предмет | pickup | — | переноситься автоматично до місця призначення; інвентар рідко потрібен |
| Обʼєкт довкілля (річкове гирло, квіти, різьблення) | static | — | зʼявляється/міняється, коли склалася певна розкладка (напр. гирло річки → квіти) |
| Перешкода (скелі, вода, край) | static | — | непрохідна для героїні |
| Story Chalet | static | — | хаб-будинок: записи про світ і найкращі (опційні) пазли |
| Предмет швидкості | pickup | — | пізніше пришвидшує ходу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open_map)` → ТО `window(map-window)`; світ на паузі.
- КОЛИ `input(drag tile → slot)` → ЯКЩО `cond: edges_match(tile, neighbours)` і `free(slot)` → ТО `place(tile, slot)`; інакше `block` (тайл не стає).
- КОЛИ `input(rotate tile)` → ТО `rotate(tile, 90)`; далі ті самі перевірки ребер.
- КОЛИ `input(drag tile_under_player)` → ТО `move(tile, slot)`, `move(player, with tile)` — героїня переїжджає разом із ділянкою.
- КОЛИ `custom: «карту закрито»` → ТО `custom: «світ перебудовано за розкладкою миттєво»` (карта = світ).
- КОЛИ `contact(player, tile_edge)` → ЯКЩО `occupied(neighbour_slot, tile)` і ребра сумісні → ТО `move(player, into neighbour)`; інакше `block` (край світу).
- КОЛИ `layout_formed(pattern)` → ЯКЩО `custom: «збігається з запитом NPC / різьбленням»` → ТО `spawn_at(npc|object, place)`, `give(player, new_tile)`.
- КОЛИ `pattern(river_mouth)` → ТО `spawn_at(flowers, mouth)` — природа реагує на рельєф.
- КОЛИ `contact(player, npc)` → ТО `message(hint|request)` (діалог емодзі/репліками).
- КОЛИ `contact(player, item)` → ТО `pickup`; ключові предмети — `custom: «автоматично доставити»`.
- КОЛИ `custom: «зібрано всі тайли розділу й виконано сюжетну умову»` → ТО `next_level` (наступний розділ/острів).
- Пізніше: обертання самої карти/тайлів як кодовий замок; ліс-лабіринт, де правильний поворот тайлів веде до виходу; тайли-поліоміно (`cond: fits`).
- Перемога: розділ завершено · Поразка: нема (смерті нема) · Рахунок: нема.

## Керування і ввід
- Геймпад/клавіатура: рух героїні; кнопка — відкрити карту.
- На карті: курсор → взяти тайл → перетягнути (drag) у вільний слот → кнопка обертання (90°) → покласти; невалідне місце не приймає тайл.
- Миша на PC: drag-n-drop тайлів (?).
- Діалоги: кнопка взаємодії біля NPC; підказки можна питати в мешканців.

## Вікна, меню, HUD
- `splash-screen` — лого Sunhead / Humble.
- `main-menu` — Continue · New Game · Settings · Exit (?).
- `game-screen` — світ зверху; HUD мінімальний: іконка карти, підказка кнопки взаємодії, емодзі-бульбашки героїні.
- `map-window` — **ключове вікно**: сітка слотів, зібрані тайли, `tile-tray` (ще не розміщені тайли), позначка тайла з Карто, кнопки обертання.
- `dialogue-window` — репліки NPC, емодзі Карто.
- `inventory-window` — предмети (рідко потрібні).
- `settings-window` — звук, мова (9), керування (?).
- Story Chalet — внутрішньоігрова «бібліотека» розділів (як `codex-window`).
- Переходи: game-screen ⇄ map-window (кнопка); розділ → катсцена → наступний розділ.

## Фічі поза полем
- Розділи-віньєтки (острови/біоми: луки, ліс, пустеля, що зсувається, мерзлота, бібліотека-лабіринт); `levels-sequential`.
- `autosave`, `cloud-save`, `achievements`.
- `onboarding-hints` через мешканців (питати підказку), без окремої кнопки hint.
- Нема undo як такого — розкладка карти сама оборотна (перекласти назад).
- Story Chalet — опційні пазли й лор.

## Варіації й родичі
- Предок ідеї — **Carcassonne** (тайли з ребрами, що мають збігатися), Dorfromantik (той самий принцип, будування), Kingdomino.
- Родичі «редагуй рівень, у якому стоїш»: Gorogoa (панелі), Patrick's Parabox (рекурсія), Islanders, Tametsi-like map puzzles; Legend of Zelda «Lost Woods» — ліс-лабіринт.
- **Осі варіацій:** ребра — без правил / тип має збігатися / дорога-річка мають продовжуватися; хто в тайлі — нікого / аватар переїжджає з тайлом / аватар блокує переміщення; форма тайлів — квадрат / поліоміно; реакція світу — лише прохідність / зʼява обʼєктів за патерном.

## Цікавинки для курсу
- Тайл з 4 типізованими ребрами + перевірка сумісності при вставці + обертання (зсув масиву ребер) — 🥉.
- Два масштаби: макро-сітка тайлів і мікро-сітка всередині, перехід героїні між тайлами через сумісні ребра — 🥈.
- Переміщення тайла разом із гравцем (координати гравця відносно тайла) — 📎.
- Детектор патернів розкладки («найбільший ліс», «гирло річки») → подія — 🥈 (flood fill по типах ребер).
- Тайли-поліоміно на тій самій карті — 🥇 разом з edge-matching.
- Ліс-лабіринт, де поворот тайла змінює шлях — 📎.

## Мапа на каталог
- Є: `move-4dir` ↔ ходьба; `impassable-cells` ↔ край світу/вода; `item-pickup` + `inventory-items` ↔ предмети; `drag-drop-piece` ↔ тайли на карті; `sequential-levels` ↔ розділи; `player-camera` ↔ камера світу; `game-screen`, `help-window` (підказки NPC), `settings-window`, `save-progress`.
- **Нема** → пропозиції карток:
  - `+world-map` «Мапа світу з вузлами-рівнями» · levels/progression · 🥉 — тут мапа сама є світом (варіант).
  - `+tile-edge-matching` «Плитки з ребрами, що мають збігатися» · entities/legality · 🥉 · слот {edge_types: list}.
  - `+tile-rotate` «Обертання плитки на 90°» · entities/state · 📎.
  - `+map-is-world` «Карта = рівень, редагування карти міняє світ» · levels/format · 🥈.
  - `+carry-tile-with-player` «Тайл переїжджає разом із аватаром» · entities/move · 📎.
  - `+polyomino-tiles` «Тайли-поліоміно» · entities/state · 🥈.
  - `+layout-request` «Запит NPC на розкладку (детектор патерну)» · game-logic/win · 🥈.
  - `+tile-reveal-reward` «Новий тайл — нагорода за пазл» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:input(open_map|drag|rotate)`; `+trigger:pattern(river_mouth|largest_forest)` (🔥 ×9 уже); `+trigger:layout_formed(pattern)` — розкладка тайлів збіглася з умовою.
- `+cond:edges_match(tile, neighbours)` — сумісність ребер; `+cond:fits(shape, cells)` (поліоміно); `+cond:occupied`.
- `+effect:rotate`, `+effect:place` (покласти тайл із запасу), `+effect:move` (тайл разом із гравцем), `+effect:spawn_at`, `+effect:give(player, tile)`, `+effect:message`.
- `+role:tile` (тайл карти), `+role:neutral` (мешканці), `+role:zone` (ребро/біом).
- `+window:map-window` — тут редактор світу, не лише огляд; `+window:dialogue-window`; `+window:inventory-window`.
- `+ui:tile-tray` — лоток нерозміщених тайлів біля сітки карти.
- `+feature:onboarding-hints` — підказки через NPC.
- `+axis:field-scale` — `single` · `nested` (макро-сітка тайлів + мікро-світ усередині: Carto, Parabox).

## Джерела
- ⭐ [Game Informer review](https://www.gameinformer.com/review/carto/carto-review-putting-the-pieces-together) — ребра мають збігатися (як Carcassonne), зміни миттєво в світі, перенесення тайла з собою, тетроміно-тайли, обертання як замок.
- [Wikipedia](https://en.wikipedia.org/wiki/Carto_(video_game)) — студія, видавець, «Carcassonne, по якому можна ходити».
- [Steam](https://store.steampowered.com/app/1172450/Carto/) — опис, тривалість, мови.
- [Siliconera](https://www.siliconera.com/review-carto-combines-environmental-storytelling-literal-world-building/) — запити NPC, нагороди-тайли, Story Chalet, підказки від мешканців.
- [NME](https://www.nme.com/reviews/carto-review-a-map-making-puzzler-where-whimsy-turns-finicky-2804939) — дорога до дороги, море не замкнути, біоми.
- [Nintendo World Report](https://www.nintendoworldreport.com/review/55335) — обертання лісових тайлів, віньєтки.
- YouTube: [пошук «Carto gameplay»](https://www.youtube.com/results?search_query=Carto+gameplay).

## Непевне
- (?) Точне правило сумісності: чи має збігатися **кожне** спільне ребро, чи тайл можна поставити окремо від решти (острівцем).
- (?) Кількість розділів (дванадцять?) і точні біоми кожного — не перевірено.
- (?) Рух героїні 4 чи 8 напрямків; мишаче керування на PC.
- (?) Тайл під героїнею: Game Informer каже, що його можна переносити разом із собою; чи є тайли, які переносити не можна.
- (?) Пункти головного меню й налаштувань — з памʼяті.
