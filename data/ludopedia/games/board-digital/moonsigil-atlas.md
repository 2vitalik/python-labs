---
title: Moonsigil Atlas
slug: moonsigil-atlas
aka: [月之魔印]
family: board-digital
also: [tower-lanes]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2026
platforms: [PC, Linux, Steam Deck]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3284290/Moonsigil_Atlas/", best: true, note: "опис: «no energy», карти-сигіли форм на сітці, руни, сусідство, накладання, 250+ карт, 3 персонажі, Титани"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=3284290", note: "Steam JSON: повний опис, категорії, 31 досягнення"}
  - {kind: official, url: "https://moonsigil.com/presskit", note: "пресскіт: Geometric Magic, Runes of Power, 3 персонажі, 3 акти, команда"}
  - {kind: other, url: "https://rogueliker.com/moonsigil-atlas-review-impressions/", note: "огляд: трикутна сітка з сегментами, поворот, розміщення без відкату, руни діють у своєму сегменті, ворожі фігури"}
  - {kind: other, url: "https://www.gamingonlinux.com/2026/06/moonsigil-atlas-is-a-genuine-delight-that-makes-you-rethink-deckbuilders/", note: "огляд: добір 5 карт, Wards і щити в зонах атаки, ворожі сигіли, персонажі Feldryn/Aladara/Tark'thul"}
  - {kind: other, url: "https://steamcommunity.com/app/3284290/reviews/?browsefilter=toprated", note: "відгуки: 4 акти, апгрейди ×2 і самоцвіти, вороги блокують поворот"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Moonsigil+Atlas+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [polyomino-placement, piece-rotate-flip, multi-cell-size, cursor-place, hp-damage, status-effects, telegraphed-intents, run-relics, permadeath, world-map, map-window, character-select, codex-window, achievements-window, difficulty-levels, save-game, game-screen, main-menu, settings-window, end-screen, +deck-builder, +deck-draw, +boss-fight, +adjacency-buff, +card-keywords, +meta-unlocks, +choose-upgrade, +space-as-energy, +overlap-bonus, +hostile-sigils, +card-reshape, +region-runes, +shield-zones, +run-history]
proposes: ["+axis:field=tri", "+effect:draw_card", "+effect:discard", "+effect:reshuffle", "+trigger:covered", "+cond:overlaps", "+cond:in_region", "+ui:card-hand", "+card:space-as-energy"]
author: opus
date: 2026-11-09
---

# Moonsigil Atlas — деквілдер без енергії: кожна карта — сигіл-фігура, і грати можна, доки фігури вміщаються на Місяць

## Суть
Роглайт-деквілдер у дусі Slay the Spire, де замість енергії — **місце на полі**: кожна карта є сигілом певної форми, і за хід можна зіграти скільки завгодно карт, поки їхні фігури вміщаються на сітку-«Місяць». Сила комбінацій — у геометрії: **руни** на фігурі діють, лише якщо лягли в потрібний сегмент поля; деякі карти отримують бонус за **сусідство** або **накладання** на вже використані клітини; частина сигілів лишається між ходами. Вороги кладуть на Місяць власні фігури (накрий — або отримаєш шкоду), атакують певні зони, а Титани змінюють саме поле.

## Поле і час
- Поле — «Місяць»: круглий/шестикутний регіон на трикутній сітці, поділений на сегменти (`field: graph`, пропозиція `+axis:field=tri`).
- Шари: клітини поля + сигіли гравця (тимчасові й постійні) + ворожі сигіли + зони атаки ворогів.
- Бій покроковий: хід гравця (добір 5 карт, викладання, кінець ходу) → дії ворогів (атаки, статуси, нові ворожі сигіли).
- Забіг: мапа вузлів (вибір смуги) у 3 актах + прихований 4-й бос; смерть = кінець забігу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маг (Feldryn / Aladara / Tark'thul) | player | HP Місяця (Aladara — 58), колода, артефакти | грає карти; програє, коли HP = 0 |
| Карта-сигіл | piece | форма (n клітин), руни, ключові слова, ефект | кладеться на вільні клітини Місяця з поворотом; потім зазвичай іде у відбій |
| Постійний сигіл | piece | тривалість | лишається на полі між ходами з тривалим ефектом |
| Руна | mark | тип (атака, щит…), положення на фігурі | спрацьовує, лише якщо стоїть у «своєму» сегменті поля |
| Сегмент Місяця | zone | привʼязка до ворога / зони атаки (?) | визначає, куди йде щит/удар руни |
| Клітина Місяця | static | вільна / зайнята / ворожа | місце для сигілів — заміна енергії |
| Ворог (астральна сутність) | enemy | HP, намір, статуси | атакує зону, накладає статуси, кладе ворожі сигіли |
| Ворожий сигіл | hazard | форма, правило | «накрий мене — інакше шкода в кінці ходу» / «+1 сила ворогу за кожну зіграну карту» / Shackle (еліта) |
| Титан | boss | фази | змінює поле (форму, сітку), власні умови перемоги |
| Singularity | piece | накопичені ключові слова й руни | зʼявляється в руці від Accumulate, розряджається одним великим ходом |
| Артефакт | pickup | пасивний бонус | постійний ефект до кінця забігу |
| Astral Gem | resource | 3 потрібні | відкривають бій із фінальним босом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «добрати 5 карт»` (+effect:draw_card); колода порожня → `custom: «перетасувати відбій у колоду»` (+effect:reshuffle).
- КОЛИ `input(drag(card, cells))` → ЯКЩО `fits(card, cells)` → ТО `place(player, card)`, `custom: «ефект карти»`; інакше карту не зіграти.
- КОЛИ `input(rotate)` → ЯКЩО `not state(card, rotation_locked)` → ТО `rotate(card, step)` (деякі вороги забороняють поворот).
- Відкату розміщення нема: зіграна карта лишається зіграною.
- Руна: КОЛИ `after(place(card))` → ЯКЩО `custom: «руна лежить у своєму сегменті»` (+cond:in_region) → ТО `custom: «ефект руни (шкода, щит)»`.
- Сусідство: КОЛИ `after(place(card))` → ЯКЩО `adjacent_count(card, sigil, >=, 1)` → ТО `custom: «бонус сусідства з тексту карти»`.
- Накладання: КОЛИ `after(place(card))` → ЯКЩО `custom: «фігура накриває вже використані клітини»` (+cond:overlaps) → ТО `custom: «посилення карти»`.
- Ward: КОЛИ `after(place(ward))` → ЯКЩО `custom: «щит лежить у зоні, куди бʼє ворог»` → ТО `set_state(zone, shield, n)`.
- Видалення: КОЛИ `after(place(removal))` → ТО `disappear(target_sigil)` (звільнити місце; пара з Ward для стеку щитів).
- КОЛИ `turn_end(player)` → ТО `custom: «скинути руку, крім Retain»` (+effect:discard), `custom: «тимчасові сигіли зникають, постійні лишаються»`.
- Ворожий сигіл «накрий»: КОЛИ `turn_end(player)` → ЯКЩО `custom: «ворожа клітина не накрита»` (+trigger:covered — подія накриття) → ТО `damage(player, n)` за кожну.
- Ворожий сигіл «сила»: КОЛИ `input(play_card)` → ТО `custom: «ворог +1 сила»`.
- Атака ворога: КОЛИ `turn_start(enemy)` → ТО `damage(player, attack − shield_in_zone)`; або `set_state(player, status)` (Exposed, Burn…).
- Накопичення: КОЛИ `after(place(accumulate_card))` → ТО `custom: «Singularity в руку (якщо нема) і + ключове слово/руна на неї»`; Decumulate — витратити накопичене.
- КОЛИ `hp_zero(enemy)` для всіх ворогів → ТО `win` бою, `choose(reward)` (карта, видалення, апгрейд…).
- КОЛИ `hp_zero(player)` → ТО `lose`, кінець забігу.
- Фінальний бос: КОЛИ `custom: «зібрано 3 Astral Gems»` → ТО `custom: «бій на двох Місяцях, форма яких задається пожертвуваними картами»`.
- Перемога: пройти 3 акти (і, за бажання, прихований бос) · Поразка: HP Місяця = 0 · Рахунок: — (історія забігів).

## Керування і ввід
- Миша: перетягнути карту з руки на Місяць, поворот кнопкою; превʼю розміщення (тінь фігури) перед відпусканням.
- Повна підтримка геймпада (DualShock/DualSense), Steam Deck.
- Кнопка «кінець ходу»; підказки-тултипи на ключових словах і ворогах.

## Вікна, меню, HUD
- `main-menu`: Continue / New Run / Compendium / Settings.
- `character-select`: три маги (наступний відкривається після повного забігу попереднім), стартова колода (альтернативні — з рівнем майстерності), рівень Eclipse.
- `map-window`: мапа вузлів акту — бої, еліти, нагороди картами, видалення карти, видалення клітини з карти, апгрейд ключовим словом, лікування, Astral Card Packs, обмін форм, дублювання.
- `game-screen`: Місяць у центрі, вороги з наміром і HP (`telegraph-marker`), `+ui:card-hand`, лічильники колоди/відбою, HP мага, статуси.
- `upgrade-window`: апгрейд карти — змінити форму, вписати руну, додати ключове слово.
- `codex-window`: Compendium (карти, вороги, Moon Blade…).
- `end-screen`/підсумок забігу (run summary з рівнем Eclipse); `stats-window` — історія забігів.
- `settings-window`: мова, гучність, керування; Save and Quit → main-menu.
- `achievements-window` (Steam, 31).

## Фічі поза полем
- `meta-progression`: майстерність персонажа відкриває нові карти, стартові колоди (Accumulate — рівень 7), артефакти (рівень 8).
- `difficulty-presets` як Eclipse-рівні (модифікатори ворогів) після першої перемоги.
- `save-slots`-подібне «Save Anytime», `cloud-save`, `history` (run history), `codex`, `localization` (12 мов).
- Forbidden Cards — рідкісні сильні карти для будь-якого персонажа; starting boons; Astral Dust (?).

## Варіації й родичі
- Осі варіацій: **ресурс ходу** (енергія — Slay the Spire / площа поля — Moonsigil / слоти рюкзака — Backpack Hero) · **сітка** (квадратна — Backpack Hero / трикутна, кругла — Moonsigil) · **живучість фігури** (одноразова / постійна) · **вплив ворога на поле** (атака зон / ворожі фігури / зміна форми поля Титаном).
- Родичі в корпусі: `build-sim/backpack-hero.md`, `build-sim/backpack-battles.md` (предмети-фігури в сітці, бонус сусідства); `patchwork.md`, `blokus.md` (поліоміно на сітці); `tower-lanes/inscryption.md` (картковий бій на полі).

## Цікавинки для курсу
- «Місце замість енергії»: рука карт-фігур, хід триває, доки щось вміщається — перевірка `fits` для кожної карти руки — 🥉.
- Трикутна сітка: координати трикутників, поворот фігури на 60° — 🥈.
- Руни, що діють лише в «своєму» сегменті поля, + щити по зонах атаки — 🥉.
- Ворожі сигіли з правилами («накрий мене», «+1 сила за карту») як дані — 📎.
- Апгрейд «змінити форму карти / прибрати клітину» — редагування поліамонда — 📎.
- Мапа вузлів з актами й нагородами (як у Slay the Spire) — 🥉.

## Мапа на каталог
- Є: `polyomino-placement` + `piece-rotate-flip` + `multi-cell-size` ↔ сигіли на Місяці; `cursor-place`; `hp-damage`; `status-effects` (Exposed, Burn); `telegraphed-intents` ↔ зони атаки; `run-relics` ↔ артефакти; `permadeath` ↔ кінець забігу; `world-map` + `map-window` ↔ мапа вузлів; `character-select`; `codex-window` ↔ Compendium; `difficulty-levels` ↔ Eclipse; `achievements-window`, `save-game`, `game-screen`, `main-menu`, `settings-window`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+space-as-energy` «Зіграти карту = вмістити її фігуру на поле; ліміту енергії нема» · game-logic/economy · 🥉.
  - `+region-runes` «Ефект частини фігури діє лише в певному сегменті поля» · entities/interact · 📎.
  - `+hostile-sigils` «Ворог кладе фігури на поле гравця з правилами» · entities/interact · 📎.
  - `+overlap-bonus` «Посилення за накладання на використані клітини» · entities/legality · 📎.
  - `+card-reshape` «Апгрейд змінює форму карти» · game-logic/economy · 🥉.
  - `+shield-zones` · `+run-history` — дрібні, теги.

## Пропозиції до словників
- `+axis:field=tri` — трикутна сітка (поліамонди: Moonsigil Atlas).
- `+effect:draw_card` — добір карт у руку на початку ходу.
- `+effect:discard` — скинути руку у відбій у кінці ходу.
- `+effect:reshuffle` — перетасувати відбій у колоду.
- `+trigger:covered` — клітину/сигіл накрито фігурою гравця.
- `+cond:overlaps` — фігура лягає на вже використані клітини.
- `+cond:in_region` — частина фігури (руна) у вказаному сегменті поля.
- `+ui:card-hand` — рука карт.
- `+card:space-as-energy` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Moonsigil Atlas](https://store.steampowered.com/app/3284290/Moonsigil_Atlas/) — «no energy… as long as they fit», сигіли з формою, ключовими словами й ефектами; руни, сусідство, накладання, постійні ефекти; 250+ карт, 3 персонажі, Титани; реліз 28.05.2026.
- [Steam JSON](https://store.steampowered.com/api/appdetails?appids=3284290) — повний опис, категорії (контролер, Save Anytime), 31 досягнення.
- [Пресскіт](https://moonsigil.com/presskit) — Geometric Magic, Runes of Power, 200+ карт у 3 актах, команда Snake Tower Games.
- [Rogueliker](https://rogueliker.com/moonsigil-atlas-review-impressions/) — трикутна сітка з сегментами, поворот, «If the shape can't fit… you can't play it», без відкату, руни в сегменті, ворожі фігури.
- [GamingOnLinux](https://www.gamingonlinux.com/2026/06/moonsigil-atlas-is-a-genuine-delight-that-makes-you-rethink-deckbuilders/) — добір 5, відбій, Wards і щити, ворожі сигіли, Feldryn/Aladara/Tark'thul, майстерність.
- Steam-новини розробників (через ISteamNews API) — Accumulate/Singularity, Retain, Prepared, Bolster, Exposed, Eclipse, Astral Gems/Dust, Compendium, HP Aladara 58.
- [Steam-відгуки](https://steamcommunity.com/app/3284290/reviews/?browsefilter=toprated) і гайд «Key things the game doesn't tell you» — 4-й бос за 3 Astral Gems, два Місяці фіналу.

## Непевне
- (?) Точна геометрія Місяця: «triangular grid divided into segments» (Rogueliker), «circular moon» (Noobfeed), «standard 6 triangle circle» (гайд) — розмір і кількість сегментів не перевірено.
- (?) Сегменти привʼязані до ворогів (щит «у правильному регіоні») — висновок з оглядів і патч-нотів.
- (?) Як саме працює поворот (крок 60°? кнопка?) і чи є віддзеркалення.
- (?) Чи тимчасові сигіли зникають у кінці ходу (схоже на те, бо «постійні» виділяють окремо).
- (?) Ліміт апгрейдів карти (2, самоцвітами до 4) — лише з відгуків.
- (?) Burn як статус — з відгуків; повний список ключових слів не знайдено.
- (?) Аліас «月之魔印» — з назви китайського гайда в Steam.
