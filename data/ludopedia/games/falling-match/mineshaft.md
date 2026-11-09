---
title: Mineshaft
slug: mineshaft
aka: []
family: falling-match
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3076100/Mineshaft/", best: true, note: "опис: з падаючих блоків крафтити лопати, кирки, бомби; монети на апгрейди; біоми; PvP зі сміттям; 6 скриншотів — панель рецептів, Coin Store, мапа"}
  - {kind: other, url: "https://www.gamingonlinux.com/2025/05/mineshaft-is-a-tough-but-unique-tetris-like-with-crafting-and-mining-for-gems/", note: "огляд: фігури з ресурсами всередині, фізика зсипання, крафт-комбо, ~64 локації, складність"}
  - {kind: other, url: "https://voxodyssey.com/mineshaft", note: "опис-агрегатор: crafting/digging combos, 64 локації, 27 апгрейдів, біоми"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3076100&count=30&maxlength=0", note: "новини: 5 класів гравця, патч 0.9.2 (кирка, пріоритет ресурсів фігури, магія)"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=DtHGHOPsgeo", note: "трейлер, вбудований у GamingOnLinux"}
stage: v1
coverage: 40
mechanics: [gravity-fall, piece-rotate-flip, keyboard-controls, dig-terrain, explode-area, destructible-blocks, chain-reaction, round-currency, shop-between-levels, shop-window, world-map, map-window, character-select, garbage-attack, simultaneous-versus, game-screen, +recipe-pattern-craft, +resource-in-piece, +topple-physics, +tool-upgrade-tree, +run-artifacts]
proposes: ["+effect:craft", "+effect:dig", "+effect:topple", "+cond:recipe_match", "+role:tool", "+window:crafting-window", "+ui:recipe-table", "+ui:resource-counters", "+card:recipe-pattern-craft"]
author: opus
date: 2026-11-09
---

# Mineshaft — Tetris із шахти: фігури з ресурсами складаються у візерунки-рецепти, з них крафтяться лопата, кирка, гиря, бомба й монета, якими копаєш глибше

## Суть
Падають фігури з клітин ґрунту, у які вкраплені ресурси (дерево, камінь, вугілля, золото). Гравець кладе їх так, щоб ресурси на полі склали візерунок одного з рецептів — тоді крафтиться інструмент або монета. Інструменти копають шари шахти під полем (там самоцвіти й нові ресурси), а копання й крафт дають каскади-комбо. Фігури не фіксуються цілими: впавши на один блок, решта клітин зсипається по боках. Між локаціями — мапа квесту з біомами, магазин апгрейдів за монети й класи гравця. Сітковий шар — крафт за візерунком на полі падіння; решта — мета-оболонка.

## Поле і час
- Вертикальна вузька шахта-колодязь (квадратна сітка): зверху небо, де падає фігура, знизу — рельєф і шари ґрунту/каменю з ресурсами й самоцвітами.
- Real-time падіння, тінь-превʼю місця приземлення (скриншот).
- Два поля поруч — режим двох гравців (split-screen PvP).
- Шари: ґрунт (коричневий), камінь (сірий), поверхня з травою/снігом/піском за біомом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Падаюча фігура | player | форма поліоміно, 1–3 ресурси всередині | рухається, падає; при посадці клітини без опори зсипаються |
| Клітина ґрунту / каменю | terrain | тип, ресурс (або порожня) | частина рельєфу; викопується інструментом |
| Ресурс: дерево / камінь / вугілля / золото | resource | тип | лічиться при викопуванні; бере участь у рецептах |
| Самоцвіт | pickup | — | глибоко в шарах; ціль копання (?) |
| Лопата | object | рецепт: 2 дерева над каменем у стовпчик | копає (вниз; апгрейд — двічі) |
| Кирка | object | рецепт: 2 дерева над рядом з 3 каменів | копає камінь; апгрейди Side (+2 блоки каменю з боків), Dirt |
| Гиря | object | рецепт: 2×2 каменів | дія — (?); апгрейди 2x/3x, Items |
| Бомба | object | рецепт: «плюс» з вугіллям у центрі | вибух; апгрейди Big, Items, Stone |
| Монета | resource | рецепт: «плюс» із золотом у центрі | валюта Coin Store |
| Сміття | object | — | приходить від суперника за комбо (PvP) |
| Артефакт | pickup | 8 видів (компас, ліхтар, ключ, кришталева куля …) | пасивний бонус забігу (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ТО `fall(piece)` на 1; КОЛИ `input(left|right)` → ЯКЩО `free(cell)` → ТО `move(piece, dir)`; `input(rotate)` → `rotate(piece, 90)` (?).
- КОЛИ `blocked(piece)` → ЯКЩО `custom: «під частиною клітин фігури порожньо»` → ТО `custom: «клітини без опори зсипаються по боках, фігура не тримається цілою»`, `fall(all_unsupported)`.
- КОЛИ `settled` → ЯКЩО `custom: «ресурси на полі складають візерунок рецепта (лопата, кирка, гиря, бомба, монета)»` → ТО `custom: «клітини рецепта зникають»`, `give(player, tool|coin)`; ресурси щойно покладеної фігури мають пріоритет (0.9.2).
- КОЛИ `settled` → ЯКЩО `chain(n)` and `custom: «після крафту склався ще рецепт»` → ТО повтор крафту, `combo(+1)` — crafting combo.
- КОЛИ `input(down)` → ЯКЩО `has(player, shovel)` → ТО `use(player, shovel)`, `custom: «викопати клітини під собою»`; апгрейд — утримувати ↓ для другого копання.
- КОЛИ `input(tool)` (?) → ЯКЩО `has(player, pickaxe)` → ТО `use(player, pickaxe)`, `custom: «викопати камінь»`; ЯКЩО апгрейд Side → `custom: «+2 блоки каменю з кожного боку»`.
- КОЛИ `input(tool)` (?) → ЯКЩО `has(player, bomb)` → ТО `use(player, bomb)`, `explode(area)`; апгрейд Big — більша площа, Stone — бере камінь (?).
- КОЛИ `destroyed(cell)` → ЯКЩО `occupied(cell, resource)` → ТО `pickup(player, resource)`, `counter(resource, +1)`.
- КОЛИ `destroyed(cell)` → ТО `fall(all_unsupported)`; нові рецепти після осідання → digging combo, `combo(+1)`.
- КОЛИ `chain(n)` → ЯКЩО `mode(versus)` → ТО `send_garbage(n)` на поле суперника.
- КОЛИ `custom: «стос дійшов до верху колодязя»` → ТО `lose` (?).
- КОЛИ `custom: «умову локації виконано (глибина / самоцвіти)»` → ТО `win`, `window(map-window)` (?).
- КОЛИ `input(buy, upgrade)` → ЯКЩО `has(player, coins)` → ТО `take(player, coins)`, `custom: «апгрейд інструмента / фігури / мапи / магії»`.
- Перемога: пройти локацію квесту (?) · Поразка: (?) · Рахунок: ресурси й монети, прогрес мапою.

## Керування і ввід
- Клавіатура або геймпад (повна підтримка, геймпад рекомендовано): ←/→ — рух фігури, ↓ — прискорити/застосувати інструмент (апгрейд «утримувати ↓»), поворот — (?).
- Цифри 1–5 біля рецептів на панелі — гарячі клавіші вибору інструмента чи просто нумерація — (?).

## Вікна, меню, HUD
- `game-screen`: колодязь; ліворуч `+ui:recipe-table` — 5 кругів «1 Shovel · 2 Pickaxe · 3 Weight · 4 Bomb · 5 Coin» з візерунками; праворуч `+ui:resource-counters` (камінь, дерево, вугілля, золото); `coins` угорі; тінь фігури.
- `map-window`: мапа квесту — граф вузлів-локацій по біомах (ліс, пустеля, гори, вулкан); підказка вузла «Forest» з рейтингом ресурсів зірками (дерево ★★★★★, камінь ★★★, вугілля ★★, золото ★★, самоцвіт ★).
- `shop-window` «Coin Store»: вкладки Tools · Piece · Map · Magic; дерево апгрейдів інструментів з описом («Pickaxe v4 — Additionally dig two stone blocks on either side»).
- `custom-window` «Artifacts»: 8 артефактів, кнопки ALL / NONE.
- `character-select` — 5 класів гравця на старті квесту.
- Split-screen на двох гравців.

## Фічі поза полем
- `world-map` з 64 локаціями; біом визначає, яких ресурсів більше.
- `meta-progression` / магазин між рівнями: 27 апгрейдів і здібностей (ефективність крафту, швидкість копання, перетворення ресурсів).
- Класи гравця зі стартовим інвентарем і артефактами (квітень 2025).
- `mode-versus` (локальний split-screen PvP; Remote Play Together), co-op у тегах Steam (?).
- Early Access; заплановано процедурні локації й PvP на 4.

## Варіації й родичі
- Родичі в корпусі: [tetris](tetris.md) (падіння фігур), [tricky-towers](tricky-towers.md) (фізика стосу), [puyo-puyo](puyo-puyo.md) (сміття супернику), [triple-town](triple-town.md) (крафт злиттям), [puzzle-quest](puzzle-quest.md) (пазл → ресурси → прогрес); сімʼя `dig-gravity` — копання шарів.
- **Осі варіацій**: що зникає (повний рядок / група кольору / **візерунок рецепта**) · що дає збіг (очки / **предмет-інструмент**) · фіксація фігури (ціла / **зсипається по боках**) · куди йде прогрес (рахунок / **глибина шахти + мапа**).

## Цікавинки для курсу
- Пошук візерунка-рецепта (поліоміно з типами клітин) на сітці після осідання — 📎; з поворотами/віддзеркаленнями рецепта — 🥉.
- Фігура, що «розсипається» при посадці на виступ, — 📎.
- Інструменти як ефекти з формою (лопата — під собою, кирка Side — ±2 з боків, бомба — площа) — 🥉.
- Каскад «крафт → копання → осідання → новий рецепт» — 🥉.
- Дерево апгрейдів у Coin Store з мапою квесту — 🥈 (мета-оболонка, не сітковий шар).

## Мапа на каталог
- Є: `gravity-fall`; `piece-rotate-flip` (?); `keyboard-controls`; `dig-terrain` ↔ копання шарів; `explode-area` ↔ бомба; `destructible-blocks` ↔ камінь/ґрунт; `chain-reaction` ↔ crafting/digging combos; `round-currency` + `shop-between-levels` + `shop-window` ↔ монети й Coin Store; `world-map` + `map-window` ↔ мапа квесту; `character-select` ↔ класи; `garbage-attack` + `simultaneous-versus` ↔ PvP; `game-screen`.
- **Нема** → пропозиції карток:
  - `+recipe-pattern-craft` «Візерунок клітин на полі → предмет» · entities/interact · 🥉 · слоти {recipes: shape+types}.
  - `+resource-in-piece` «Ресурси вкраплені у клітини фігури» · entities/spawn · 🌱.
  - `+topple-physics` «Фігура не тримається цілою, клітини зсипаються з виступу» · entities/move · 📎.
  - `+tool-upgrade-tree` «Дерево апгрейдів інструмента» · game-logic/economy · 📎.
  - `+run-artifacts` (родич `run-relics`) «Артефакти, що вмикаються на забіг» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+effect:craft` — набір клітин/ресурсів перетворюється на предмет (уже пропонувалось у корпусі).
- `+effect:dig` — інструмент прибирає клітини рельєфу заданої форми.
- `+effect:topple` — клітини фігури без опори зсипаються вбік.
- `+cond:recipe_match` — на полі склався візерунок рецепта.
- `+role:tool` — сутність-інструмент, що застосовується до клітин.
- `+window:crafting-window` — панель рецептів як окреме вікно (тут — постійно на екрані).
- `+ui:recipe-table`, `+ui:resource-counters`.
- `+card:recipe-pattern-craft` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Mineshaft](https://store.steampowered.com/app/3076100/Mineshaft/) — опис, PvP зі сміттям, біоми, категорії (контролер, split-screen), дата 20.04.2025; 6 скриншотів: панель 5 рецептів, Coin Store з деревом апгрейдів, Artifacts, мапа квесту, split-screen, вибух.
- [GamingOnLinux, 19.05.2025](https://www.gamingonlinux.com/2025/05/mineshaft-is-a-tough-but-unique-tetris-like-with-crafting-and-mining-for-gems/) — фігури з ресурсами, фізика зсипання, комбо, ~64 локації, монети на апгрейди.
- [Voxodyssey: Mineshaft](https://voxodyssey.com/mineshaft) — crafting/digging combos, 64 локації, 27 апгрейдів, біоми, план 4-гравцевого PvP.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3076100&count=30&maxlength=0) — «Player Classes», «Version 0.9.2».
- [Відгуки Steam](https://steamcommunity.com/app/3076100/reviews/?browsefilter=toprated&p=1) — «manipulate the terrain blocks into certain shapes, in order to craft tools and coins».

## Непевне
- (?) Точні типи ресурсів у рецептах: на панелі дві різні сірі іконки (уламок і камінець) — камінь і залізо? Рецепти записано за формою, а типи — наближено.
- (?) Чи рецепт шукається з поворотами; чи кристали — ціль локації; умова поразки.
- (?) Як саме діють інструменти (куди копає лопата, що робить гиря) — бачено лише описи апгрейдів.
- (?) Чи фігуру можна обертати; призначення цифр 1–5 на панелі рецептів.
- (?) Платформи: Steam — лише Windows; Voxodyssey пише ще macOS.
