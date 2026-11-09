---
title: Guzzler
slug: guzzler
aka: [ガズラー]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1983
platforms: [arcade, SG-1000 (Othello Multivision), Nintendo Switch, PS4]
links:
  - {kind: other, url: "https://www.arcade-history.com/game/1059/", best: true, note: "механіка води й швидкості, таблиця очок за серії в одному пострілі, літери GUZZLER ×2"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Guzzler", note: "три постріли, порожній — найшвидший, калюжі, вогні породжують монстрів, коктейль"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ガズラー", note: "32 стадії, з 17-ї — випадкові з 2–16; гейзер; бонус часу 5000–30000; літери GUZZLER; домашня версія"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/guzzler", note: "KLOV: 4 вогні на рівень, останній вогонь з очима переслідує, їжа двох розмірів, кабінет"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/arcade-archives-guzzler-switch/", note: "Arcade Archives (Hamster): налаштування складності, онлайн-рекорди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Guzzler+Tehkan+arcade", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, impassable-cells, projectile-shot, shoot-forward, spawner-entity, destroy-all-enemies, chase-player, touch-death, player-death, item-pickup, temporary-modes, event-points, escalating-kill-points, time-bonus, time-out, sequential-levels, hot-seat, difficulty-levels, leaderboard, attract-demo, game-screen, +ammo-weight-speed, +range-by-ammo, +refill-on-exhaustion, +row-letter-bonus, +avatar-gauge, +multi-kill-bonus]
proposes: ["+effect:refill", "+card:ammo-weight-speed", "+card:range-by-ammo", "+card:refill-on-exhaustion", "+card:row-letter-bonus", "+card:avatar-gauge", "+card:multi-kill-bonus", "+ui:avatar-gauge", "+window:intermission"]
author: opus
date: 2026-11-09
---

# Guzzler — пожежник-цистерна в лабіринті: вода — і набої, і вага; гаси всі вогнища, поки вони плодять монстрів

## Суть
Гравець — круглий пожежник Guzzler, що бігає однекранним лабіринтом і гасить вогнища, які безперервно породжують вогняних монстрів. Вода в ньому — єдина зброя на **три постріли**, і водночас вантаж: що менше води, то коротший постріл і **швидший** біг, а порожній Guzzler найшвидший, але беззбройний. Воду п'ють із калюж, а коли калюжі вичерпано — з гейзера. Стадію пройдено, коли погашено всі вогнища.

## Поле і час
- Однекранний лабіринт на сітці з видом згори; лабіринти різні — від заплутаних до майже порожніх кімнат.
- 32 стадії; з 17-ї стадії лабіринти беруться випадково зі стадій 2–16 (JA-вікі).
- Real-time; у нижньому рядку екрана — літери GUZZLER для бонусу.
- Кожна стадія починається з бонусу часу (5000–30000 очок), що спадає; дійшов до нуля — втрачено життя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Guzzler | player | вода 0–3 постріли; швидкість зростає, коли вода меншає | рух 4 напрямки; стріляє водою в бік погляду |
| Струмінь води | projectile | дальність меншає з кожним пострілом | гасить вогнища й монстрів на шляху |
| Вогнище (fire) | spawner | 4 на стадію (KLOV) | безперервно породжує монстрів; погасити всі = кінець стадії |
| Вогняний монстр (fireball) | enemy | — | переслідує Guzzler; дотик = втрата життя |
| Останнє вогнище «з очима» | enemy | іноді | оживає й переслідує гравця (KLOV) |
| Калюжа | pickup | велика / мала | пройти крізь неї → поповнити воду (повністю / частково) |
| Гейзер | pickup | коли калюж не лишилось | ще одне джерело води |
| Коктейль / пляшка | pickup | у центрі після двох великих калюж | повний бак, Guzzler червоніє, вогні завмирають / вороги сповільнюються |
| Літера G-U-Z-Z-L-E-R | mark | по одній на ряд, підсвічена червоною рамкою | загоряється від влучання в монстра в її ряду; усі 7 → очки ×2 |
| Стіна лабіринту | static | — | непрохідна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(guzzler, dir)`; інакше `block`.
- КОЛИ `input(fire)` → ЯКЩО `counter(water, >, 0)` → ТО `spawn(water_blast, facing)`, `counter(water, -1)`, `speed(guzzler, +1)`; інакше `block`.
- КОЛИ `spawned(water_blast)` → ТО `custom: «дальність струменя = функція залишку води: що менше, то коротше»`.
- КОЛИ `counter(water, ==, 0)` → ТО `set_state(guzzler, empty)` — порожній контур у рожевих черевиках, найшвидший, не стріляє.
- КОЛИ `contact(water_blast, fireball)` → ТО `disappear(fireball)`, `score(200)`; другий і третій монстр тим самим струменем — `score(400)`, `score(800)`.
- КОЛИ `contact(water_blast, fire)` → ТО `disappear(fire)`, `score(1000)`; разом із 1 / 2 монстрами тим самим струменем — `score(2000)` / `score(4000)`.
- КОЛИ `timer(spawn_period)` → ТО `spawn_at(fireball, fire)` для кожного живого вогнища.
- КОЛИ `count(fire, ==, 1)` → ЯКЩО `prob(p)` → ТО `set_state(fire, chasing)` — останнє вогнище з очима переслідує (KLOV).
- КОЛИ `contact(fireball, guzzler)` → ТО `lives(-1)`.
- КОЛИ `enter(guzzler, puddle)` → ТО `custom: «поповнити воду: велика калюжа — повністю, мала — частково»` (`+effect:refill`), `disappear(puddle)`.
- КОЛИ `counter(distance, >=, n)` → ТО `custom: «поповнити воду від пройденої відстані»` (JA-вікі; KLOV — «з часом»).
- КОЛИ `all_gone(puddle)` → ТО `spawn(geyser)`; КОЛИ `contact(guzzler, geyser)` → ТО `custom: «поповнити воду»`.
- КОЛИ `counter(big_puddles, ==, 2)` → ТО `spawn_at(cocktail, center)`.
- КОЛИ `contact(guzzler, cocktail)` → ТО `custom: «повний бак»`, `set_state(guzzler, red, dur)`, `freeze(fire, dur)`, `speed(fireball, -1)`.
- КОЛИ `contact(water_blast, fireball)` → ЯКЩО `custom: «літера цього ряду підсвічена червоною рамкою»` → ТО `mark(letter, lit)`.
- КОЛИ `pattern(all letters GUZZLER lit)` → ТО `multiplier(2)` для очок за влучання і бонусу кінця раунду.
- КОЛИ `timer(few_seconds)` → ТО `score(10)` (очки за виживання).
- КОЛИ `timer(1)` → ТО `counter(time_bonus, -n)`; КОЛИ `counter(time_bonus, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `all_gone(fire)` → ТО `score(time_bonus)`, `next_level`; після деяких стадій — `window(intermission)`.
- Перемога: нема — гра на очки через 32 стадії й далі. Поразка: дотик монстра або кінець бонусу часу; життя скінчились → `game_over`. Рахунок: серії в одному пострілі 200/400/800, вогнище 1000–4000, 10 за виживання, бонус часу, ×2 за GUZZLER.

## Керування і ввід
- 4-позиційний джойстик — рух; одна кнопка — постріл водою в напрямку погляду.
- 1–2 гравці по черзі (alternating).
- Arcade Archives: налаштування складності й екрана, режим онлайн-рекордів.

## Вікна, меню, HUD
- `attract-demo` — аркадний демо-цикл.
- `game-screen` — лабіринт; рівень води видно **на самому Guzzler** (зафарбований знизу вгору); рядок GUZZLER унизу; `score`, `lives`, бонус часу (`timer-countdown`).
- `intermission` — коротка сценка «монстри женуться за Guzzler» після деяких стадій.
- `end-screen` — кінець гри; KLOV згадує спосіб отримати додаткове життя після останнього (див. «Непевне»).
- Переходи: демо → (монета) гра → (усі вогнища) бонус → [вставка] → наступна стадія → (життя скінчились) кінець.

## Фічі поза полем
- `operator-settings` — DIP-налаштування автомата; Arcade Archives переносить їх у меню складності.
- `leaderboard-online` (Arcade Archives, 2021), `hotseat` для двох гравців по черзі.
- Домашня версія Othello Multivision / SG-1000 (Tsukuda Original, 1983): інші лабіринти, без музики, без бонусу GUZZLER.

## Варіації й родичі
- [Pac-Man](pac-man.md) — однекранний лабіринт і переслідувачі; тут замість точок — вогнища-генератори.
- [Gauntlet](gauntlet.md), [Dandy](dandy.md) — генератори монстрів, які треба знищити.
- [Lady Bug](lady-bug.md) — бонус за складене слово з літер (EXTRA/SPECIAL); у Guzzler літера горить, якщо влучити в її ряду в потрібний момент.
- **Осі варіацій:** набої — нескінченні / ліміт без поповнення / ліміт з поповненням на мапі (Guzzler); вага набоїв — нема / набої сповільнюють (Guzzler: порожній найшвидший); дальність пострілу — стала / залежить від залишку; джерело поповнення — калюжі → гейзер, коли калюжі скінчились.

## Цікавинки для курсу
- Ресурс із компромісом: вода = набої і вага, швидкість обернено залежить від залишку — 📎.
- Дальність струменя як функція залишку води — 🌱.
- Очки подвоюються за кожну наступну ціль того самого пострілу (200 → 400 → 800) — 📎 (картка `escalating-kill-points`).
- Вогнища-генератори, які треба погасити всі; останнє оживає — 📎.
- Резервне джерело: гейзер зʼявляється, коли всі калюжі випито — 🌱 (захист від глухого кута).
- Літери GUZZLER: підсвічена літера ряду + влучання в монстра в цьому ряду → множник — 🥉.
- Індикатор води на самому аватарі замість HUD — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `projectile-shot` + `shoot-forward` ↔ струмінь · `spawner-entity` ↔ вогнища · `destroy-all-enemies` ↔ погасити всі вогнища · `chase-player` · `touch-death` + `player-death` · `item-pickup` ↔ калюжі, коктейль · `temporary-modes` ↔ коктейль · `event-points` · `escalating-kill-points` ↔ 200/400/800 · `time-bonus` + `time-out` ↔ спадний бонус часу · `sequential-levels` ↔ 32 стадії · `hot-seat` ↔ двоє по черзі · `difficulty-levels` · `leaderboard` · `attract-demo` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+ammo-weight-speed` «Набої як вага: менше набоїв — швидший рух» · entities/state · 📎.
  - `+range-by-ammo` «Дальність пострілу від залишку набоїв» · entities/combat · 🌱.
  - `+refill-on-exhaustion` «Резервне джерело, коли звичайні вичерпано» · entities/spawn · 🌱.
  - `+row-letter-bonus` «Літера ряду загоряється від влучання в цьому ряду; слово → множник» · scoring · 🥉.
  - `+avatar-gauge` «Індикатор ресурсу на самому аватарі» · interface/render · 🌱.
  - `+multi-kill-bonus` (вже Mr. Do!) — кілька цілей одним пострілом.

## Пропозиції до словників
- `+effect:refill` (вже ×4) — поповнити ресурс (воду) до максимуму або на частку.
- `+card:ammo-weight-speed`, `+card:range-by-ammo`, `+card:refill-on-exhaustion`, `+card:row-letter-bonus`, `+card:avatar-gauge`, `+card:multi-kill-bonus` — див. «Мапу на каталог».
- `+ui:avatar-gauge` — шкала ресурсу, намальована на спрайті аватара.
- `+window:intermission` (вже Pac-Man, Pengo) — анімаційна вставка між стадіями.

## Джерела
- ⭐ [arcade-history: Guzzler](https://www.arcade-history.com/game/1059/) — три постріли, прискорення з кожним пострілом, порожній контур у рожевих черевиках, калюжі, коктейль, таблиця очок 200/400/800, 1000–4000, 10 за виживання, літери GUZZLER ×2 і правило підсвіченої літери ряду.
- [Wikipedia: Guzzler](https://en.wikipedia.org/wiki/Guzzler) — суть, вогні породжують монстрів, коктейль у центрі заморожує вогні, порти, Arcade Archives 2021.
- [Wikipedia JA: ガズラー](https://ja.wikipedia.org/wiki/ガズラー) — вода на 3 постріли, дальність меншає, поповнення калюжами або пройденою відстанню, гейзер, коктейль після двох великих калюж, бонус часу 5000–30000, 32 стадії, домашня версія.
- [KLOV: Guzzler](https://www.arcade-museum.com/Videogame/guzzler) — 4-позиційний джойстик і кнопка, 4 вогні на рівень, останній з очима, їжа двох розмірів, вставки між рівнями, вертикальний монітор, 2 гравці по черзі.
- [Nintendo eShop: Arcade Archives GUZZLER](https://www.nintendo.com/us/store/products/arcade-archives-guzzler-switch/) — налаштування складності, світові рекорди.
- YouTube: пошук «Guzzler Tehkan arcade».

## Непевне
- (?) Кількість життів на старті й пороги додаткових життів.
- (?) KLOV: «після останнього життя можна заробити ще одне, зупинившись і прокрутившись колом у правильному місці» — не підтверджено іншими джерелами.
- (?) Калюжі: KLOV називає «їжа двох розмірів»; чи мала калюжа поповнює рівно один постріл.
- (?) Коктейль: EN-вікі — заморожує вогні, JA-вікі — сповільнює ворогів; можливо, і те, і те.
- (?) Як саме поповнення «від пройденої відстані / часу» працює і з якою швидкістю.
- (?) Як часто вогнища породжують монстрів і чи є ліміт монстрів на екрані; чи останнє вогнище оживає завжди.
- (?) Межі бонусу часу 5000–30000 залежать від стадії чи від налаштувань.
