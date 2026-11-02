---
title: A Monster's Expedition
slug: a-monsters-expedition
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2020
platforms: [PC, Mac, Linux, iOS, Android, Switch, PS4, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/A_Monster%27s_Expedition", best: true, note: "механіки колод, мости й плоти, undo/reset острова, поштові скриньки, розробка"}
  - {kind: official, url: "https://www.monsterexpedition.com/", note: "сайт гри з лінками на всі магазини"}
  - {kind: official, url: "https://www.monsterexpedition.com/press", note: "прескіт: опис, трейлери"}
  - {kind: steam, url: "https://store.steampowered.com/app/1052990/"}
  - {kind: other, url: "https://draknek.itch.io/a-monsters-expedition", note: "itch.io"}
  - {kind: youtube, url: "http://www.youtube.com/watch?v=4LH1I6qdanU", note: "Launch Trailer (з прескіту)"}
  - {kind: other, url: "https://www.wurb.com/stack/?p=6262", note: "есей: reset острова повертає всі його колоди, undo на плоту"}
  - {kind: other, url: "https://thinkygames.com/games/a-monsters-expedition", note: "Thinky Games: картка гри"}
stage: v1
coverage: 75
mechanics: [move-4dir, push-object, multi-cell-size, orientation-state, inertia-slide, cell-transform, impassable-cells, reach-exit, item-pickup, keyboard-controls, swipe-gestures, movement-animation, save-autosave, help-window, +fell-tree, +log-roll-tip, +fill-hole, +carrier-platform, +undo-redo, +reset-zone, +fast-travel-points, +open-world-puzzles, +exhibit-collectible]
proposes: ["+trigger:input", "+trigger:enter", "+cond:free", "+cond:facing", "+effect:move", "+effect:slide", "+effect:set_cell", "+effect:transform", "+effect:roll", "+effect:tip", "+effect:carry", "+effect:reset_zone", "+role:terrain", "+role:platform", "+window:exhibit-card", "+window:map-window", "+feature:reset-zone", "+feature:fast-travel", "+axis:undo", "+axis:session"]
author: opus
date: 2026-11-02
---

# A Monster's Expedition — звали дерево, покоти колоду, перекинь міст на сусідній острів

## Суть
Маленький монстр мандрує архіпелагом із сотень острівців; між ними — вода, якою він ходити не може. Єдиний інструмент — штовхнути: дерево від поштовху падає й стає колодою, а колода залежно від того, з якого боку її штовхнули, **котиться** (поштовх збоку) або **перекидається торцем через себе** (поштовх уздовж). Колода, що впала у воду, стає мостом між островами або плотом. Ядро — орієнтація двоклітинного обʼєкта як стан (як у Sausage Roll), а відкритий світ без «рівнів» замінює меню вибору: кожен острів — пазл, розвʼязання якого прокладає шлях далі.

## Поле і час
- Квадратна сітка; світ — один безперервний архіпелаг із сотень острівців, згрупованих у візуально різні біоми (механічно не розділені). Камера йде за монстром, видно кілька островів навколо.
- Шари клітини: тип (суша / вода / вершина-обрив) + обʼєкт (дерево, пеньок, колода, експонат, скринька). Колода в воді — окремий стан клітини: міст/пліт.
- Покроково: тік = один ввід гравця; анімації (котіння колоди, дрейф плоту) — наслідок одного ходу, ворогів і таймера нема.
- Динамічний саундтрек реагує на дії (поштовх колоди грає ноту, undo — тихий удар тарілки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Монстр | player | — | рух 4 напрямки; у воду не заходить; ходить по колодах-мостах і плотах |
| Дерево | object | висота: мале / велике (?) | від поштовху падає в напрямку поштовху → колода; пеньок лишається (?) |
| Колода мала | object | 1×2, орієнтація: лежить уздовж X / уздовж Y / стоїть | поштовх збоку — котиться до упору; поштовх у торець — перекидається на 1 крок (лежача → стоїть → лежача) |
| Колода велика | object | довша за малу (?) | лише котиться; торцем не перекидається |
| Вода | terrain | — | непрохідна для монстра; колода, що впала в неї, стає мостом або плотом |
| Колода-міст | terrain | застрягла між берегами | по ній ходять; далі не рухається |
| Пліт | terrain + platform | колода у відкритій воді | стаєш на нього й штовхаєшся від берега — пливе до упору, везучи монстра |
| Суша / обрив | static | — | межі острова; колода, що скотилася за край, падає у воду |
| Скеля, валун, кущ (?) | static | — | непрохідні для монстра й колод |
| Експонат | pickup | текст | «людський» предмет з кумедним описом; ціль збирання |
| Поштова скринька | static | — | точка швидкого переміщення до інших відкритих скриньок |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(monster, dir)`; якщо попереду вода без мосту — `block`.
- КОЛИ `contact(monster, tree)` → ТО `transform(log)`, `custom: «дерево падає в напрямку поштовху і лягає колодою уздовж цього напрямку»`; ЯКЩО місця падіння нема — `block` (?).
- КОЛИ `contact(monster, log)` → ЯКЩО `facing` перпендикулярний осі колоди → ТО `roll(log, dir)` = `slide(log, dir)`: котиться, доки `blocked(log)` або доки не зірветься у воду.
- КОЛИ `contact(monster, log)` → ЯКЩО `facing` уздовж осі, `free(cell_ahead)` і колода мала → ТО `tip(log, dir)`: лежача стає вертикальною (1 клітина), вертикальна падає й лягає (2 клітини).
- КОЛИ `contact(monster, big_log)` уздовж осі → ТО `block`.
- КОЛИ `enter(log, water)` → ЯКЩО обидва кінці спираються на сушу/перешкоду → ТО `set_cell(bridge)`; інакше `set_state(log, raft)`.
- КОЛИ `contact(monster, raft)` з берега і рух від берега → ТО `carry(raft+monster, dir)`, `slide` до наступної суші/перешкоди.
- КОЛИ `contact(monster, log)` на плоту/мосту → ТО звичайні правила поштовху (колоду можна перекотити через пліт на інший острів).
- КОЛИ `contact(monster, exhibit)` → ТО `message(exhibit_text)`, `counter(exhibits, +1)`.
- КОЛИ `contact(monster, mailbox)` → ТО `window(map-window)` → `teleport(monster, chosen_mailbox)`.
- КОЛИ `input(undo)` → ТО `custom: «відкотити один хід»` (необмежено, миттєво, навіть посеред плавання плоту).
- КОЛИ `input(reset)` → ТО `reset_zone(current_island)`: усі колоди, що **походять** з цього острова, телепортуються на старт, де б не були.
- Перемога: нема рахунку й поразки; формальна ціль — дістатися фінального острова й корабля додому, неформальна — зібрати експонати. Поразки нема взагалі: глухий кут знімається undo/reset.

## Керування і ввід
- Стрілки/WASD/стік (на тачі — свайпи) — рух на 1 клітину; дія «штовхнути» = піти в обʼєкт, окремої кнопки нема.
- `Undo` (Z/Backspace) — необмежений покроковий відкат; `Reset` (R) — скинути лише поточний острів.
- Без вибору рівнів: маршрут обирається ногами по світу.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Продовжити, Налаштування, Вихід.
- `game-screen`: поле без HUD (лише натяки кнопок undo/reset на тачі як `undo-button`, `restart-button`).
- `exhibit-card` (custom): ілюстрація предмета + «експертний» опис з точки зору монстрів.
- `map-window` (поштова скринька): вибір іншої відкритої скриньки для переміщення.
- `pause-menu`: Продовжити, Налаштування (`settings-window`: гучність музики/ефектів, керування), Вийти в меню.
- Переходи: main-menu → game-screen (автосейв місця); game-screen → exhibit-card (дотик до експоната) → назад; game-screen → map-window (скринька) → game-screen в іншій точці.

## Фічі поза полем
- `autosave` безперервний; нема рівнів і `level-select` — їх роль бере `world-map` (відкритий світ) + `fast-travel` скриньками.
- `undo` ∞ і `reset-zone` (скидання частини світу, а не всього) — ключова фіча дизайну, хвалена рецензентами.
- `collectibles` — експонати; «Museum Update» (2021) додав музей, де їх виставлено.
- Немає журналу, підказок, досягнень у базовій версії (рецензенти відзначали).
- `touch-controls`, `gamepad-support`; динамічна музика.

## Варіації й родичі
- Попередники Draknek: A Good Snowman Is Hard to Build (сніжки ростуть, котячись), Sokobond, Cosmic Express; продовження — The Electrifying Incident: A Monster Mini-Expedition (2025).
- Родичі за механікою: Sausage Roll / Stephen's Sausage Roll (орієнтація двоклітинного обʼєкта), Bloxorz (перекидання бруска торцем), Isles of Sea and Sky (відкритий світ Sokoban-кімнат).
- Осі варіацій: **що буває з обʼєктом при поштовху** — зсув на 1 / котіння до упору / перекидання торцем / залежить від орієнтації; **куди падає обʼєкт за краєм** — зникає / заповнює яму / стає мостом / плотом; **скидання** — увесь рівень / зона / жодного.

## Цікавинки для курсу
- Колода 1×2 з трьома орієнтаціями: котіння збоку vs перекидання торцем — 🥈 (стан орієнтації + різна фізика за напрямком поштовху).
- Дерево → колода: падіння обʼєкта, що займає нові клітини, з перевіркою місця — 🥉.
- Колода у воді → міст або пліт за умовою «обидва кінці на березі» — 🥉.
- Пліт, що везе гравця до упору (кілька сутностей рухаються як одна) — 🥉.
- Reset лише поточного острова з поверненням «рідних» колод, навіть якщо вони вже деінде — 🥈 (треба памʼятати походження кожного обʼєкта).
- Необмежений undo на історії станів — 📎 (з `state-as-data` — тривіально, без — 🥉).

## Мапа на каталог
- Є: `move-4dir` · `push-object` · `multi-cell-size` (колода 1×2) · `orientation-state` (лежить/стоїть) · `inertia-slide` (котіння до упору) · `cell-transform` (дерево → колода, вода → міст) · `impassable-cells` · `reach-exit` (фінальний корабель) · `item-pickup` (експонати) · `keyboard-controls` · `swipe-gestures` · `movement-animation` · `save-autosave` · `help-window`.
- **Нема** → пропозиції карток:
  - `+fell-tree` «Звалити дерево» · entities/interact · 📎 — статичний обʼєкт від поштовху стає рухомим багатоклітинним.
  - `+log-roll-tip` «Котити або перекидати» · entities/state · 🥈 · слот {tip: yes|no} — фізика за орієнтацією (дитина `orientation-state`).
  - `+fill-hole` «Обʼєкт заповнює яму/воду» · entities/interact · 📎 · слот {result: floor|bridge|raft}.
  - `+carrier-platform` «Платформа везе гравця» · entities/move · 🥉 (є як пропозиція з Frogger).
  - `+undo-redo` «Undo/redo ходів» · game-logic · 🥉 (є як пропозиція з Sokoban).
  - `+reset-zone` «Скидання зони, а не рівня» · levels/progression · 🥈.
  - `+fast-travel-points` «Точки швидкого переміщення» · levels/progression · 📎.
  - `+open-world-puzzles` «Відкритий світ пазлів замість списку рівнів» · levels/progression · 🥈.
  - `+exhibit-collectible` «Колекційні предмети з текстом» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:roll` — обʼєкт котиться до упору, лишаючи орієнтацію (колода, сніжка); `+effect:tip` — обʼєкт перекидається торцем через себе, змінюючи кількість зайнятих клітин.
- `+effect:carry` — платформа переносить того, хто на ній (пліт); `+effect:reset_zone` — скинути стан частини світу.
- `+role:platform` — рухома опора, на якій стоять (пліт; є з Frogger).
- `+window:exhibit-card` — картка колекційного предмета з текстом; `+window:map-window` — карта скриньок для переміщення.
- `+feature:reset-zone` — reset острова/кімнати замість рівня; `+feature:fast-travel` — переміщення між відкритими точками.
- `+axis:undo` = `unlimited`; `+axis:session` = `open-world` (нове значення: нема дискретних рівнів).
- ⏳-слова, вжиті тут: `input`, `enter`, `free`, `facing`, `move`, `slide`, `set_cell`, `transform`, `terrain`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/A_Monster%27s_Expedition) — колоди (малі котяться й перекидаються, великі лише котяться), котіння до упору чи у воду, мости, плоти, undo/reset острова, скриньки, розробка (прототип у PuzzleScript).
- [Офіційний сайт](https://www.monsterexpedition.com/) і [прескіт](https://www.monsterexpedition.com/press) — платформи, трейлери.
- [Launch Trailer](http://www.youtube.com/watch?v=4LH1I6qdanU) — геймплей: падіння дерев, котіння, плоти.
- [Steam](https://store.steampowered.com/app/1052990/) · [itch.io](https://draknek.itch.io/a-monsters-expedition).
- [wurb.com «A Monster’s Expedition: Final Words»](https://www.wurb.com/stack/?p=6262) — reset повертає всі колоди острова, undo посеред плавання, звук на кожну дію.
- [Thinky Games](https://thinkygames.com/games/a-monsters-expedition) — картка гри.

## Непевне
- (?) Точна геометрія падіння дерева (яку клітину займає колода, чи лишається пеньок і чи він перешкода) — з памʼяті, у джерелах не описано.
- (?) Довжина «великої» колоди і чи бувають колоди довжини 1 — Wikipedia каже лише «small/large».
- (?) Умова «міст vs пліт» сформульована з памʼяті: міст — колода між двома берегами, пліт — у відкритій воді.
- (?) Чи можна штовхнути колоду, що стоїть вертикально, у воду і що з неї стає (стовпчик-сходинка?).
- (?) Розкладка клавіш undo/reset.
