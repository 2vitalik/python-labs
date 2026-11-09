---
title: Faeria
slug: faeria
aka: []
family: tactics
also: [build-sim]
klass: hybrid
axes:
  field: hex
  time: turn
  opponent: online
  info: hidden
  random: runtime
  goal: state
year: 2017
platforms: [PC, macOS, Linux, Xbox One, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Faeria", best: true, note: "порожнє гекс-поле, 4 криниці, колода 30, порядок ходу, Power Wheel, клади землю поруч зі своєю, режими Battle/Pandora/соло"}
  - {kind: official, url: "https://www.faeria.com/the-hub/guide/443-keywords-and-their-expanded-descriptions", note: "офіційний список ключових слів: Flying, Aquatic, Jump, Dash, Charge, Taunt, Ranged, Drowning, Production, Haste…"}
  - {kind: official, url: "https://www.faeria.com/the-hub/guide/62-terminology-and-mechanics-in-detail", note: "термінологія; коментарі про Dash по прямій і Flying над океаном"}
  - {kind: steam, url: "https://store.steampowered.com/app/397060/", note: "«живе поле»: гори, ліси, озера, пустелі; Pandora, соло, кооп, світові боси"}
  - {kind: official, url: "https://www.faeria.com/", note: "офіційний сайт; Faeria Academy, Pandora, турніри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Faeria+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, floor-types, cursor-place, piece-move-patterns, legal-move-highlight, reachable-highlight, status-effects, inventory-items, pocket, round-currency, ai-opponent, online-multiplayer, rating-system, shop-window, daily-puzzle, mode-select, tutorial-window, +deckbuilding, +card-hand-draw, +land-placement, +land-requirement, +resource-wells, +summoning-sickness, +keyword-abilities, +drowning-tiles, +draft-mode, +choose-one-action-wheel]
proposes: ["+trigger:summoned", "+trigger:combat_exchange", "+cond:lands_owned", "+cond:land_type", "+cond:keyword", "+effect:draw_card", "+effect:place_land", "+effect:harvest", "+effect:counterattack", "+effect:fight", "+effect:swallow", "+role:card", "+role:god", "+role:well", "+ui:mana-counter", "+ui:power-wheel", "+ui:land-requirement", "+window:deck-builder", "+window:pandora-draft", "+window:pack-opening", "+feature:fatigue-damage"]
author: opus
date: 2026-11-09
---

# Faeria — карткова тактика, де поле будують самі гравці: клади гекси землі, а істоти ходять лише по суші

## Суть
Дуель двох гравців-«богів» (орбів) з колодами по 30 карт на **порожньому гекс-полі** — це океан. Щоходу кожен обирає одну дію на «колесі сили»: +1 Faeria (мана), +1 карта або **покласти землю** (дві нейтральні рівнини чи одну особливу: ліс, озеро, гора, пустеля) поруч зі своєю землею чи істотою. Карти вимагають Faeria і певної кількості земель свого кольору; істоти ходять по гексах і бʼють сусідів, а без Flying/Aquatic тонуть в океані. Мета — збити здоровʼя ворожого орба до нуля. Поле росте мостами з землі, і географія стає частиною стратегії.

## Поле і час
- Гексова дошка; на старті вся порожня (океан), лише орби гравців на протилежних краях і **4 криниці Faeria** в інших кутах.
- Шар клітин: океан → земля (рівнина / ліс / озеро / гора / пустеля) з власником → істота або споруда зверху.
- Хід = хід гравця: дрібні дії в довільному порядку (колесо, карти, рух); кінець ходу — кнопкою.
- Таймер ходу онлайн (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Орб (God) гравця | player | здоровʼя (20 (?)) | нерухомий; 0 → поразка; приймає атаки сусідніх істот |
| Океан | hazard | — | порожній гекс; без Flying/Aquatic у кінці свого ходу — Drowning |
| Рівнина (Prairie) | terrain | нейтральна, власник | кладуться по 2; на будь-яку свою землю можна прикликати |
| Ліс / Озеро / Гора / Пустеля | terrain | колір, власник | 1 за дію; рахуються у вимоги карт свого кольору |
| Криниця Faeria | resource | — | своя істота поруч → +1 Faeria за хід (harvest) |
| Істота | piece | Faeria-ціна, вимога земель, атака, здоровʼя, ключові слова | рух на 1 гекс по землі + атака сусіда; обмін ударами |
| Споруда (Structure) | piece | здоровʼя | нерухома; Activate — здатність раз на хід |
| Подія (Event) | pickup | ціна | разовий ефект: шкода, бафф, дебафф |
| Карта в руці | object | — | тягнеться з колоди; гра витрачає Faeria |
| Колода | container | 30 карт | порожня → Fatigue: 1, 2, 3… шкоди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «взяти 1 карту»`, `currency(+3)`; за кожну криницю з власною істотою поруч → `currency(+1)`.
- Колесо сили: КОЛИ `input(wheel, option)` → ЯКЩО `custom: «цього ходу колесо ще не використане»` → ТО одне з: `currency(+1)` · `custom: «взяти 1 карту»` · `custom: «покласти 2 рівнини або 1 особливу землю»`.
- Земля: КОЛИ `input(place_land, hex)` → ЯКЩО `custom: «гекс — океан і сусідить із твоєю землею або твоєю істотою»` → ТО `set_cell(hex, land)`, `set_side(hex, player)`.
- Прикликання: КОЛИ `input(play, creature, hex)` → ЯКЩО `counter(faeria, ≥, cost)` і `custom: «у тебе ≥ N земель потрібного кольору»` і `custom: «гекс — твоя земля (для кольорової істоти — землі її типу)»` і `free(hex)` → ТО `place(player, creature)`, `currency(−cost)`.
- КОЛИ `spawned(creature)` → ТО `set_state(creature, summoning_sick, 1)` — не ходить, не бʼє, не збирає Faeria цього ходу; ЯКЩО `state(creature, haste)` → ТО одразу діє.
- Рух: КОЛИ `input(move, creature, hex)` → ЯКЩО `adjacent(creature, hex)` і `free(hex)` і `custom: «гекс — земля (будь-чия)»` → ТО `move`; Flying — і над океаном; Aquatic — лише океан і озера.
- Jump: ЯКЩО `state(creature, jump)` → ТО `custom: «рух до 2 гексів, через перешкоди й океан, не по прямій»`.
- Charge X / Dash X: ЯКЩО `state(creature, charge)` → ТО `custom: «рух до X по прямій»`; Dash — так само одразу при прикликанні; без Flying через океан і зайняті — ні.
- Атака: КОЛИ `input(attack, a, t)` → ЯКЩО `adjacent(a, t)` → ТО `damage(t, atk_a)` і `damage(a, atk_t)` (обмін); КОЛИ `hp_zero(x)` → ТО `disappear(x)`.
- Ranged: ЯКЩО `state(a, ranged)` → ТО `custom: «стріляє по прямій лінії гексів без ліміту дальності, якщо бачить; після звичайного руху стріляти не може; відповідь лише від сусіда або іншого Ranged»`.
- Taunt: ЯКЩО `adjacent(enemy, taunt_creature)` → ТО `custom: «ворог не може рухатись і бʼє лише Taunt»`.
- Protection: КОЛИ `custom: «перше джерело шкоди по істоті з Protection»` → ТО `block`, `clear_state(creature, protection)`.
- Deathtouch: КОЛИ `custom: «істота з Deathtouch завдала шкоди істоті»` → ТО `disappear(target)`.
- Drowning: КОЛИ `turn_end(owner)` → ЯКЩО `cell(creature, ocean)` і not `state(creature, flying|aquatic)` → ТО `disappear(creature)`; Aquatic не на озері/океані → так само.
- Орб: КОЛИ `input(attack, creature, god)` → ЯКЩО `adjacent(creature, god)` → ТО `damage(god, atk)`; КОЛИ `hp_zero(god)` → ТО `lose` власника, `win` супернику.
- Тригери карт: Gift — `spawned(card)`; Last words — `died(card)`; Production — `turn_start(owner)`; Combat — `custom: «обмін ударами з істотою, орбом або спорудою»`; Corrupt — `custom: «вперше зайшла на ворожу землю»`.
- Fatigue: КОЛИ `custom: «тягнути з порожньої колоди»` → ТО `damage(god, k)`, `counter(fatigue, +1)`.
- Перемога: орб суперника 0 · Поразка: свій орб 0 · Рахунок: рейтинг/ранг у PvP; Pandora — до 3 поразок.

## Керування і ввід
- Мишею: клік по сегменту колеса сили → клік по гексу океану, щоб покласти землю (підсвічуються дозволені).
- Drag карти з руки на свою землю — прикликання; Dash — одразу вибір цілі по прямій (правий клік скасовує).
- Клік по істоті → підсвітка гексів руху → клік/drag на ворога — атака.
- Кнопка End Turn; mulligan на старті — вибір карт на заміну.

## Вікна, меню, HUD
- `main-menu`: Battle (PvP / AI) · Pandora · Solo (кампанія, пазли, челенджі) · Co-op (?) · Collection · Shop · Tournaments.
- `custom-window` «Deck builder» — колекція, фільтр кольорів, колода 30.
- `custom-window` «Pandora draft» — вибір карт з випадкових пропозицій; лічильник перемог/поразок до 3.
- `shop-window` — паки карт, орби, криниці (косметика DLC); `custom-window` «Pack opening».
- `puzzle-select` — пазли («виграй за один хід»).
- `game-screen`: гексова дошка; `pocket` (рука); `coins`/Faeria-лічильник; колесо сили; здоровʼя орбів; лічильник колоди; `end-turn-button`; `tooltip` карт; `legal-move-highlight`.
- `end-screen` — результат і нагорода валютою.
- Переходи: main-menu → mode-select → (Pandora draft / deck select) → гра → end-screen → main-menu.

## Фічі поза полем
- Режими: PvP ranked/casual · проти ШІ · Pandora (драфт до 3 поразок) · соло-кампанія, `puzzle-bank` (пазли), челенджі · кооп-місії і світові боси (за Steam) · турніри.
- Прогресія: валюта за перемоги → паки; колекція; `rank-tiers` (?).
- `tutorial` (навчальні бої); `custom-skins` (орби й криниці).

## Варіації й родичі
- Родичі в корпусі: [duelyst](duelyst.md) (карткова тактика на сітці 9×5 з генералом), [polytopia](polytopia.md); поза корпусом: Hearthstone і Magic (ресурс + кольорові вимоги), Carcassonne і [dorfromantik](../build-sim/dorfromantik.md) (поле з плиток), Hexplore.
- Осі варіацій: поле — фіксоване / росте від гравців / росте від колоди · ресурс — щоходу +1 / колесо вибору / криниці · вимога кольору — від карт землі (Magic) / від землі на полі · рух — нема (Hearthstone) / сітка без землі (Duelyst) / лише по побудованій землі.

## Цікавинки для курсу
- Поле, яке будують гравці: клади гекс лише поруч зі своїм — 📎 (сусідство на гекс-сітці).
- Колесо: одна дія з трьох (мана / карта / земля) як ресурсний вибір ходу — 🌱.
- Вимога «≥ N земель кольору» для карти — 🌱.
- Океан і Drowning: перевірка на кінець свого ходу, Flying/Aquatic як винятки — 📎.
- Ключові слова як прапорці правил (Jump, Dash, Taunt, Ranged по лінії, Protection) — 🥉 (система тегів-модифікаторів).
- Криниці: дохід за сусідню свою істоту — 🌱.
- Драфт Pandora до 3 поразок — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` (Ranged по прямій) · `floor-types` (типи землі, океан) · `cursor-place` (покласти землю) · `piece-move-patterns` (Jump, Charge, Flying) · `legal-move-highlight` · `reachable-highlight` · `status-effects` (Protection, Taunt, summoning sickness) · `inventory-items` (події) · `pocket` (рука) · `round-currency` (Faeria) · `ai-opponent` · `online-multiplayer` · `rating-system` · `shop-window` · `daily-puzzle` (?) · `mode-select` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+deckbuilding` «Збірка колоди з колекції» · progression · 🥉.
  - `+card-hand-draw` «Колода, рука, взяти карту» · game-logic/random · 📎.
  - `+land-placement` «Гравець добудовує поле гексами» · entities/interact · 📎.
  - `+land-requirement` «Карта вимагає N земель кольору» · game-logic/legality · 🌱.
  - `+resource-wells` «Дохід від точки за сусідню свою фігуру» · game-logic/economy · 🌱.
  - `+summoning-sickness` «Нова фігура не діє цього ходу» · entities/state · 🌱.
  - `+keyword-abilities` «Ключові слова як прапорці правил» · entities/state · 🥉.
  - `+drowning-tiles` «Клітина вбиває в кінці ходу без прапорця» · entities/legality · 🌱.
  - `+draft-mode` «Драфт колоди з випадкових пропозицій» · progression · 📎.
  - `+choose-one-action-wheel` «Одна дія з колеса на хід» · game-logic/turns · 🌱.

## Пропозиції до словників
- `+trigger:summoned` — карту щойно зіграно з руки (Gift); вужче за `spawned`, бо не рахує токени (?).
- `+trigger:combat_exchange` — обмін ударами з істотою/орбом/спорудою (Combat); Last words — це наявний `died`.
- `+cond:lands_owned` — у гравця ≥ N земель кольору · `+cond:land_type` — гекс має тип землі · `+cond:keyword` — у сутності є ключове слово.
- `+effect:draw_card` (повтор) · `+effect:place_land` · `+effect:harvest` · `+effect:counterattack` (повтор) · `+effect:fight` · `+effect:swallow`.
- `+role:card` (повтор) · `+role:god` — нерухомий «аватар-HP» гравця на полі · `+role:well` — точка доходу.
- `+ui:mana-counter` · `+ui:power-wheel` · `+ui:land-requirement` (значки кольору на карті).
- `+window:deck-builder` · `+window:pandora-draft` · `+window:pack-opening`.
- `+feature:fatigue-damage` — порожня колода шкодить з наростанням.

## Джерела
- ⭐ [Wikipedia: Faeria](https://en.wikipedia.org/wiki/Faeria) — дошка, криниці, колода 30, порядок ходу, Power Wheel, правила землі, прикликання, бій, режими, дати.
- [Faeria Hub: Keywords](https://www.faeria.com/the-hub/guide/443-keywords-and-their-expanded-descriptions) — повні описи ключових слів (Flying, Aquatic, Jump, Dash, Charge, Ranged, Taunt, Drowning, Fatigue, Production…).
- [Faeria Hub: Terminology](https://www.faeria.com/the-hub/guide/62-terminology-and-mechanics-in-detail) — Dash по прямій, Flying над океаном.
- [Steam](https://store.steampowered.com/app/397060/) — опис «живого поля», режими.
- [faeria.com](https://www.faeria.com/) — Academy, Pandora, турніри.

## Непевне
- (?) Здоровʼя орба 20, ліміт копій карти в колоді — з памʼяті.
- (?) Відповідність кольорів землям (зелений — ліс, синій — озеро, червоний — гора, жовтий — пустеля) — з памʼяті.
- (?) Розмір дошки і точне розташування криниць/орбів — не бачив.
- (?) Чи можна прикликати кольорову істоту на рівнину — Wikipedia каже «лише на землю свого типу», офіційних слів не знайшов.
- (?) Кооп-місії й світові боси — лише зі Steam; таймер ходу онлайн — з памʼяті.
