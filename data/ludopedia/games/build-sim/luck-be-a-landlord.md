---
title: Luck be a Landlord
slug: luck-be-a-landlord
family: build-sim
also: [roguelike, board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2021
platforms: [PC, Mac, Linux, Android, iOS, Switch, PlayStation, Xbox]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Luck_Be_a_Landlord", note: "огляд: 12 оплат ренти = перемога, символ після кожного спіну, коти пʼють молоко"}
  - {kind: other, url: "https://gamepretty.com/luck-be-a-landlord-symbol-item-guide/", best: true, note: "гайд символів і предметів: графік ренти, рідкості, хто кого знищує/перетворює (версія 2021)"}
  - {kind: steam, url: "https://store.steampowered.com/app/1404850/Luck_be_a_Landlord/", note: "Steam: EA 2021, реліз 06.01.2023"}
  - {kind: other, url: "https://blog.trampolinetales.com/luck-be-a-landlord-on-mobile-facts/", note: "блог розробника (мобільна версія)"}
  - {kind: other, url: "https://indiecator.org/2021/04/11/indietail-luck-be-a-landlord/", note: "рецензія: вибір 1 з 3 предметів після ренти, removal/reroll"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=luck+be+a+landlord+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [spawn-random-cell, round-currency, event-points, combo-multiplier, cell-transform, inventory, inventory-items, shop-preview, time-out, collect-quota, difficulty-levels, sequential-levels, save-autosave, help-window, +slot-spin-layout, +adjacency-buff, +symbol-destroy, +symbol-transform, +rent-deadline, +draft-pick, +removal-token, +reroll-token, +passive-items, +bag-of-symbols, +rarity-weights]
proposes: ["+trigger:input", "+trigger:adjacent", "+trigger:counter", "+trigger:after", "+trigger:rng", "+cond:adjacent_count", "+cond:has", "+cond:count", "+cond:prob", "+cond:same", "+effect:currency", "+effect:multiplier", "+effect:transform", "+effect:give", "+effect:take", "+effect:choose", "+effect:counter", "+role:tile", "+role:resource", "+ui:coins", "+ui:turn-counter", "+ui:objective-text", "+ui:popup-text", "+ui:tooltip", "+window:upgrade-window", "+window:inventory-window", "+window:codex-window", "+feature:mode-endless", "+feature:difficulty-presets", "+feature:unlockables", "+card:adjacency-buff", "+card:slot-spin-layout"]
author: opus
date: 2026-11-02
---

# Luck be a Landlord — слот-машина 5×4, де символи заробляють за сусідами, а рента росте

## Суть
У гравця «мішок» символів (монета, вишня, кіт, молоко, бджола, квітка, шахтар, руда…). Кожен спін розкидає їх у **випадкові клітини** поля 5×4; кожен символ дає монети, а **сусідні символи змінюють одне одного**: кіт зʼїдає молоко за великий бонус, шахтар розбиває руду, бджола множить квіти. Кожні кілька спінів треба заплатити ренту, що росте; після кожного спіну — вибір 1 з 3 нових символів. Гра — роглайк-деклбілдер, де «колода» викладається на сітку випадково, і вся стратегія — щільність корисних сусідств.

## Поле і час
- Поле 5 стовпців × 4 рядки = 20 клітин; символів у мішку може бути більше 20 — тоді на поле потрапляє випадкова двадцятка; менше — решта клітин «Empty».
- Сусідство — 8 клітин (з діагоналями) (?); деякі ефекти — «у тому самому рядку/стовпці», «будь-де на полі».
- Хід = один спін (кнопка); після нього — фаза розрахунку (символи по черзі тригерять ефекти, анімація монет) і фаза вибору.
- Рента: N спінів на оплату; 12 оплат — перемога; потім нескінченний режим.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина слота | static | позиція 5×4 | місце для одного символу на цей спін |
| Символ (загалом) | tile | базова вартість, рідкість (common/uncommon/rare/very rare), теги (фрукт, тварина, руда…) | дає монети щоспіну; ефекти залежать від сусідів |
| Empty | tile | 0 | заповнює клітину, коли символів <20 |
| Монета (Coin) | tile | 1 | просто 1 монета |
| Кіт + Молоко | tile | — | кіт знищує сусіднє молоко й отримує бонус за кожне (?) |
| Шахтар + Руда | tile | — | шахтар знищує сусідню руду за бонус; руда при знищенні може дати самоцвіт/перлину |
| Бджола + Квітка | tile | бджола 1 | сусідні квіти/вулики/мед дають більше; бджола росте від них |
| Сонце, Дощ + Квітка | tile | сонце 3, дощ 2 | множать сусідні квіти; дощ пришвидшує проростання насіння (?) |
| Мавпа + Банан/Кокос | tile | — | мавпа зʼїдає фрукти; кокос → дві половинки |
| Пес → Вовк, Яйце → Курка | tile | — | перетворення з часом/за шансом |
| Курка | spawner | — | з шансом зносить яйце (новий символ у мішок) (?) |
| Гробниця, Урна → Дух | spawner | — | породжують духів; духи самознищуються |
| Злодій, Мисливець за головами | tile | — | мисливець знищує сусіднього злодія за бонус |
| Скриня / Сейф + Ключ | tile | — | ключ відкриває сусідню скриню → монети |
| Void Stone / Void Creature | tile | — | самознищуються за 8 монет (за умови пустот поруч) (?) |
| Хекси (Hex of …) | tile | — | негативні символи; свята вода їх нейтралізує |
| Предмет (Item) | pickup | рідкість | пасивний ефект на весь забіг (Black Cat ×3 котам, Lucky Carrot ↑рідкісні, Cardboard Box — removal token кожні 9 спінів…) |
| Essence | pickup | — | особливий тип предмета, відкривається після перемог (?) |
| Removal token | resource | кількість | прибрати будь-який символ з мішка |
| Reroll token | resource | кількість | перевибрати трійку символів для вибору |
| Орендодавець | static | графік ренти | раз на N спінів вимагає суму |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(spin)` → ТО `custom: «перемішати мішок; узяти до 20 символів; розкласти у випадкові клітини 5×4; решта — Empty»`, `counter(spins_left, -1)`.
- КОЛИ `after(spin)` для кожного символу → ТО `currency(+base_value)` з урахуванням множників.
- КОЛИ `adjacent(a, b)` ЯКЩО пара «їдець → їжа» (кіт → молоко, шахтар → руда, мавпа → банан, мисливець → злодій) → ТО `disappear_b`, `currency(+bonus)` або постійне `set_value(a, +n)`.
- КОЛИ `adjacent(a, b)` ЯКЩО пара «підсилювач → ціль» (сонце/дощ/бджола → квітка) → ТО `multiplier(b, ×k)` на цей спін.
- КОЛИ `adjacent_count(a, kind, >=, n)` → ТО бонус, що росте з кількістю сусідів виду (бджола від квітів).
- КОЛИ `rng(p)` для символу-перетворювача → ТО `transform(a → b)` (пес → вовк, яйце → курка, руда → самоцвіт) або `spawn(entity)` у мішок (курка → яйце, гробниця → дух).
- КОЛИ `destroyed(a)` → ТО ефекти «за знищення» (Black Pepper — монети за знищені символи; руда/скриня — нагорода).
- КОЛИ `after(payout)` → ТО `choose(3 random symbols | skip)` з вагами рідкості; `input(reroll)` ЯКЩО `has(reroll_token)` → нова трійка.
- КОЛИ `input(remove, symbol)` ЯКЩО `has(removal_token)` → ТО `take(bag, symbol)`, `counter(removal_tokens, -1)`.
- КОЛИ `counter(spins_left, ==, 0)` → ЯКЩО `has(coins, >=, rent)` → ТО `currency(-rent)`, `choose(1 of 3 items)`, наступний рядок графіка (рента більша; графік у версії 2021: 25/5, 50/5, 100/6, 150/6, 225/7, 275/7, 325/6, 375/8, 500/9, 550/9, 650/10, 777/10 — сума/спіни); інакше `lose`.
- КОЛИ `counter(rent_paid, ==, 12)` → ТО `win`; далі — нескінченний режим (?).
- Перемога: 12 оплат ренти. Поразка: не вистачило монет у день ренти. Рахунку нема, крім грошей.

## Керування і ввід
- Одна кнопка SPIN (пробіл/клік).
- Вибір символу: клік по одній з трьох карток або Skip; Reroll (якщо є токен).
- Перегляд мішка (inventory) і прибирання символу removal-токеном.
- Наведення на символ — підказка з описом і поточною вартістю.

## Вікна, меню, HUD
- `main-menu`: Play, Floors/складність (?), Collection/енциклопедія (?), Settings, Quit.
- `game-screen`: сітка 5×4, кнопка SPIN, `coins`, `turn-counter` «спінів до ренти», `objective-text` «рента N через K спінів», панель предметів, лічильники токенів, `popup-text` монет над символами, `tooltip`.
- `upgrade-window` — вибір 1 з 3 символів після спіну; окремо — вибір 1 з 3 предметів після ренти.
- `inventory-window` — мішок символів з кількостями й removal.
- «Лист від орендодавця» (`custom-window`) — нагадування про ренту і дедлайн.
- `end-screen` — виселення (поразка) / перемога; `codex-window` — колекція відкритих символів і предметів (?).
- `settings-window`, `help-window` (?).
- Переходи: main-menu → game-screen ⇄ (спін) вибір символу ⇄ (рента) вибір предмета → end-screen.

## Фічі поза полем
- `difficulty-presets` — «поверхи» складності після першої перемоги (?); `mode-endless` після 12-ї ренти.
- `unlockables` — нові символи/предмети/essence відкриваються з прогресом.
- `autosave` забігу; досягнення Steam.

## Варіації й родичі
- Balatro (натхненний LBaL у частині «роглайк із азартної механіки»), Dicey Dungeons, Backpack Hero (`build-sim` корпусу — сусідство в сітці, але розміщення робить гравець).
- Осі варіацій: **хто розкладає** — випадковість (LBaL) / гравець (Backpack Hero, Dorfromantik); **сусідство** — 4 / 8 / рядок / все поле; **вид взаємодії** — множник / поїдання з бонусом / перетворення / спавн у мішок.

## Цікавинки для курсу
- Випадкове розкладання мішка на 5×4 + підрахунок виплати за сусідами (8) — 📎: чиста функція «поле → монети», ідеальна для юніт-тестів.
- Пари «їдець → їжа» і «підсилювач → ціль» як таблиця взаємодій — 🥉 (картка `interaction-table`).
- Рента-дедлайн із зростаючим графіком (сума за N ходів) — 🌱.
- Драфт «1 з 3» із вагами рідкості, що зсуваються з прогресом — 📎.
- Порядок розрахунку ефектів (хто кого зʼїв першим, множники після знищень) — 🥈: детермінований порядок обходу і тести на граничні випадки.
- Токени прибирання/перевибору як керування «колодою» — 🌱.

## Мапа на каталог
- Є: `spawn-random-cell` (розкладання символів) · `round-currency` (монети) · `event-points` (вартість символів) · `combo-multiplier` (множники сусідів — близько) · `cell-transform` (пес → вовк, руда → самоцвіт) · `inventory` + `inventory-items` (мішок, предмети) · `shop-preview` (опис символу до вибору) · `time-out` + `collect-quota` (рента: сума за N спінів) · `difficulty-levels` (поверхи) · `sequential-levels` (12 рент) · `save-autosave` · `help-window`.
- **Нема** → пропозиції карток:
  - `+slot-spin-layout` «Мішок розкладається у випадкові клітини» · entities/spawn · 📎 · слоти {w:5, h:4, empty_fill}.
  - `+adjacency-buff` (як у Backpack Hero) — тут без вибору місця.
  - `+symbol-destroy` «Сусід-їдець знищує ціль за бонус» · entities/interact · 📎.
  - `+symbol-transform` «Перетворення символу з шансом/часом» · entities/state · 📎 — дитина `cell-transform`.
  - `+rent-deadline` «Сума до дедлайну, графік зростає» · game-logic/lose · 🌱 · слоти {schedule}.
  - `+draft-pick` «Вибір 1 з 3 або пропуск» · game-logic/economy · 📎 · слоти {options, rarity_weights}.
  - `+removal-token` / `+reroll-token` «Токени керування колодою» · game-logic/economy · 🌱.
  - `+passive-items` «Пасивні предмети на весь забіг» · game-logic/economy · 📎.
  - `+bag-of-symbols` «Мішок-колода, що росте» · entities/state · 🌱.
  - `+rarity-weights` «Ваги рідкості, що зсуваються з прогресом» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:input` (spin), `+trigger:adjacent` (основа всього), `+trigger:counter` (спіни до ренти), `+trigger:after` (розрахунок після розкладання), `+trigger:rng` (перетворення).
- `+cond:adjacent_count`, `+cond:has` (токени, монети ≥ рента), `+cond:count` (символів у мішку), `+cond:prob`, `+cond:same` (теги: фрукт, тварина).
- `+effect:currency`, `+effect:multiplier`, `+effect:transform`, `+effect:give`/`+effect:take` (мішок), `+effect:choose`, `+effect:counter`.
- `+role:tile` (символ), `+role:resource` (токени).
- `+ui:coins`, `+ui:turn-counter`, `+ui:objective-text`, `+ui:popup-text`, `+ui:tooltip`.
- `+window:upgrade-window` (драфт), `+window:inventory-window` (мішок), `+window:codex-window`.
- `+feature:mode-endless`, `+feature:difficulty-presets`, `+feature:unlockables`.
- `+card:adjacency-buff`, `+card:slot-spin-layout`.

## Джерела
- ⭐ [GamePretty: Symbol & Item Guide](https://gamepretty.com/luck-be-a-landlord-symbol-item-guide/) — графік ренти, рідкості, пари символів, хто кого знищує/перетворює, предмети (версія 2021, частина значень могла змінитись).
- [Wikipedia](https://en.wikipedia.org/wiki/Luck_Be_a_Landlord) — 12 оплат ренти, символ після кожного спіну, коти/молоко, бджоли/квіти, Godot, дати релізів.
- [Steam](https://store.steampowered.com/app/1404850/Luck_be_a_Landlord/) — TrampolineTales, EA 08.01.2021, реліз 06.01.2023.
- [Indietail review](https://indiecator.org/2021/04/11/indietail-luck-be-a-landlord/) — вибір 1 з 3 предметів після ренти, removal/reroll, Geologist.
- [Блог TrampolineTales](https://blog.trampolinetales.com/luck-be-a-landlord-on-mobile-facts/) — мобільна версія.
- YouTube: пошук «luck be a landlord gameplay».

## Непевне
- (?) Сусідство з діагоналями (8) — з памʼяті; джерела, що відкрились, не кажуть.
- (?) Точні тексти пар: кіт/молоко, шахтар/руда (бонус за знищення) — з памʼяті й Wikipedia (кіт пʼє молоко); числа не перевірено.
- (?) Графік ренти — з гайду 2021 року; у релізі 1.0 міг змінитись.
- (?) Як здобуваються Essence і токени essence (джерела суперечать: «відкриваються після 7 перемог» vs «орендодавець забирає essence-токени»).
- (?) «Поверхи» складності, нескінченний режим, вікно колекції — з памʼяті.
