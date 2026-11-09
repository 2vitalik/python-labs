---
title: Forager
slug: forager
aka: [Форажер]
family: build-sim
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: none
year: 2019
platforms: [PC, Switch, PS4, Xbox One, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Forager_(video_game)", best: true, note: "геймплей: ресурси, крафт, сітка перків, золото → купівля нових земель"}
  - {kind: steam, url: "https://store.steampowered.com/app/751780/Forager/", note: "опис: купівля землі для розширення території, пазли, секрети, підземелля, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Forager+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-8dir, item-pickup, inventory, inventory-items, round-currency, spawn-random-cell, hp-damage, map-window, level-unlock, save-game, achievements-window, +land-purchase, +escalating-price, +land-rights, +perk-grid, +resource-respawn, +craft-structures, +biome-lands]
proposes: ["+effect:buy_land", "+cond:adjacent_owned", "+ui:land-price-tag", "+window:land-map", "+card:land-purchase", "+card:escalating-price", "+card:perk-grid"]
author: opus
date: 2026-11-09
---

# Forager — світ як сітка ділянок-островів: заробляєш золото й купуєш наступну клітину мапи

## Суть
Інкрементальна 2D-гра «збирай-крафти-розширюйся»: аватар бʼє дерева, камені й руду, крафтить споруди й інструменти, качає перки, а зароблене золото витрачає на **купівлю нових земель**. Кожна нова земля відкриває нові ресурси, ворогів, NPC, пазли й підземелля. Тут описано лише сітковий шар — **мапу земель і їх купівлю**; решта гри (крафт-ланцюги, фермерство, бій, автоматизація) — фон.

## Поле і час
- Світ — **сітка земель** (ділянок-островів) на воді; на старті куплена одна, решта видно на мапі як недоступні (`info: partial`: що на землі — дізнаєшся після купівлі (?)).
- Кожна земля всередині — тайлова ділянка з ресурсами й спорудами; аватар ходить вільно (8 напрямків), межі землі — вода.
- Час — реальний: ресурси відроджуються з часом на куплених землях; темп збору зростає з рівнем і кількістю земель.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар (Forager) | player | HP, енергія (?) | ходить, бʼє ресурси/ворогів, ставить споруди |
| Земля (land) | zone | біом, ціна, куплена/ні | клітина мапи світу; куплена — стає частиною світу |
| Вода між землями | static | — | межа; переходу на некуплену землю нема (?) |
| Ресурс (дерево, камінь, руда, кущ) | resource | HP | удар → дроп предмета, XP; відроджується на вільній клітині |
| Споруда (піч, кузня, ринок, ферма…) | object | вартість матеріалів, розмір | крафт, переробка, продаж; частина — автоматизує збір |
| Ворог | enemy | HP, шкода | атакує при контакті |
| NPC | neutral | квест | просить предмети, дає нагороду |
| Пазл / підземелля на землі | zone | — | спецземля з розвʼязком і скринею-нагородою |
| Золото (монети) | resource | — | валюта купівлі земель |
| Перк | mark | клітина сітки навичок | відкривається за рівень, дає інструмент/рецепт/бонус |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, land)` у мапі земель → ЯКЩО `custom: «земля межує з уже купленою»` (?) and `has(player, coins_price)` → ТО `currency(-price)`, `custom: «земля стає частиною світу»`, `reveal(land)`.
- КОЛИ `after(buy_land)` → ТО `custom: «ціна кожної наступної землі зростає»`.
- КОЛИ `input(click, land)` → ЯКЩО `not has(player, coins_price)` → ТО `block`.
- КОЛИ `input(hit, resource)` → ТО `hp(resource, -n)`.
- КОЛИ `hp_zero(resource)` → ТО `disappear_b`, `give(player, item)`, `counter(xp, +n)`.
- КОЛИ `timer(every)` → ЯКЩО `custom: «земля куплена»` and `free(cell)` and `prob(p)` → ТО `spawn_at(resource, random_cell)`; тип ресурсу — за біомом землі.
- КОЛИ `counter(xp, >=, threshold)` → ТО `choose(perk)` — нова клітина сітки перків.
- КОЛИ `input(place, structure)` → ЯКЩО `has(player, materials)` and `fits(structure, cells)` → ТО `take(player, materials)`, `place(structure)`.
- КОЛИ `input(sell, item)` → ЯКЩО `custom: «поруч ринок»` (?) → ТО `currency(+n)`.
- КОЛИ `contact(enemy, player)` → ТО `damage(n)`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «земля-пазл»` → ТО `custom: «скриня / нагорода відкривається»`.
- Перемога: нема фіксованої (`goal: none`; цілі ставить гравець) · Поразка: смерть аватара (наслідки (?)) · Рахунок: нема; прогрес — кількість земель, рівень, досягнення.

## Керування і ввід
- Клавіатура/стик — рух у 8 напрямках; миша/кнопка — удар по ресурсу/ворогу під курсором.
- Режим будівництва: обрати споруду → поставити на вільні клітини землі.
- Мапа земель: відкрити → клік по землі → підтвердити купівлю.

## Вікна, меню, HUD
- `game-screen`: поточна земля, аватар, HUD — `hp-bar`, `energy-bar` (?), `coins`, `inventory-bar`, `popup-text` (+XP, дроп).
- `map-window` / `+window:land-map`: сітка земель, куплені й ні, ціна на кожній (`+ui:land-price-tag`).
- `custom-window` — сітка перків; меню будівництва (`custom-window`); `inventory-window`.
- `main-menu`, `settings-window`, `save-slots` (?), `achievements-window` (Steam).
- Переходи: game-screen ↔ map-window (купівля) · game-screen ↔ сітка перків · game-screen → меню будівництва.

## Фічі поза полем
- `save-game` (Steam Cloud), `achievements`, Steam Workshop (моди), `leaderboard-online` (Steam-лідерборди за чим саме — (?)).
- Прогресія: `xp-level` + сітка перків; землі — головний «рівень» гри.

## Варіації й родичі
- Корпус: `cities-skylines-zoning` (купівля сусідніх ділянок мапи за гроші й milestones), `stardew-farm` (ресурси, що відроджуються), `dorfromantik` і `islanders` (світ росте клітинами).
- Осі «розширення поля»: купити за валюту (Forager, Cities: Skylines) / вибрати клітини за рівень (Backpack Hero) / покласти тайл (Dorfromantik) / право на землю як товар (RollerCoaster Tycoon — `land-rights`).
- Осі «ціна розширення»: фіксована / зростає з кожною купівлею (Forager) / залежить від положення.

## Цікавинки для курсу
- Мапа-сітка земель з купівлею сусідніх і зростаючою ціною — 🌱 (масив прапорців + формула ціни).
- Відродження ресурсів на вільних клітинах куплених земель з таблицею за біомом — 📎.
- Сітка перків: клітина відкривається, якщо сусідня відкрита (?) — 📎.
- Інкрементальний баланс «збір → золото → земля → швидший збір» — 🥉 (крива ціни vs дохід).

## Мапа на каталог
- Є: `move-8dir` · `item-pickup` + `inventory` + `inventory-items` · `round-currency` (золото) · `spawn-random-cell` (ресурси) · `hp-damage` · `map-window` · `level-unlock` (землі відкривають нове) · `save-game` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+land-purchase` «Купівля нової клітини мапи світу» · levels/progression · 🌱 · слоти {adjacency, price} — Forager, Cities: Skylines.
  - `+escalating-price` «Ціна зростає з кожною покупкою» · game-logic/economy · 🌱.
  - `+perk-grid` «Сітка перків, що відкриваються за рівні» · levels/progression · 📎.
  - `+resource-respawn` «Ресурси відроджуються на вільних клітинах» · entities/spawn · 🌱.
  - `+craft-structures`, `+biome-lands` — споруди з рецептів; земля визначає набір ресурсів.

## Пропозиції до словників
- `+effect:buy_land` — купити клітину мапи світу (зараз `currency(-n)` + `custom`).
- `+cond:adjacent_owned` — клітина межує з уже належною гравцеві (Forager, Cities: Skylines).
- `+ui:land-price-tag` — ціна на некупленій ділянці мапи.
- `+window:land-map` — мапа ділянок світу з купівлею (варіант `map-window`).
- `+card:land-purchase`, `+card:escalating-price`, `+card:perk-grid` — див. вище.

## Джерела
- ⭐ [Wikipedia: Forager](https://en.wikipedia.org/wiki/Forager_(video_game)) — HopFrog, 18.04.2019; ресурси, крафт, сітка перків, золото → купівля землі відкриває нові ресурси, ворогів, NPC, пазли, підземелля.
- [Steam: Forager](https://store.steampowered.com/app/751780/Forager/) — купівля землі для розширення, рівні → навички й креслення, пазли, секрети, Workshop, лідерборди.
- YouTube: пошук «Forager gameplay».

## Непевне
- (?) Розмір сітки земель і їх кількість; формула зростання ціни — у відкритих джерелах нема (fandom віддав 402, WebSearch вичерпано).
- (?) Чи купувати можна лише сусідню землю; чи видно вміст землі до купівлі.
- (?) Набір біомів (луг, пустеля, зима, цвинтар, вогонь — з памʼяті); енергія аватара й їжа.
- (?) Наслідки смерті аватара; чи продаж іде лише через ринок.
- (?) Сітка перків: правило сусідства для відкриття — з памʼяті.
