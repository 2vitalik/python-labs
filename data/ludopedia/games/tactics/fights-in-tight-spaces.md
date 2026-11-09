---
title: Fights in Tight Spaces
slug: fights-in-tight-spaces
aka: [FiTS, FITS]
family: tactics
also: [roguelike]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2021
platforms: [PC, Xbox One, Xbox Series, Switch, PS4, PS5]
links:
  - {kind: other, url: "https://steamah.com/fights-in-tight-spaces-tips-tricks-core-mechanics/", best: true, note: "core mechanics: фази ходу, momentum, combo, push/колізія/вихід за край, stun/throw, counter, типи атак ворогів, цілі, вузли мапи"}
  - {kind: steam, url: "https://store.steampowered.com/app/1265820", note: "200+ карт, injuries, події, daily mission з лідербордом"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fights_in_Tight_Spaces", note: "структура забігу, combo, наміри ворогів, replay, дати й платформи"}
  - {kind: other, url: "https://www.magicgameworld.com/?p=125934", note: "basic tactics: ring out, колізія, friendly fire, порядок атак при наведенні"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fights+in+Tight+Spaces+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [telegraphed-intents, telegraph-marker, threat-range, hover-highlight, legal-move-highlight, push-object, hp-damage, impassable-cells, environment-death, melee-vs-ranged, line-of-sight-attack, status-effects, temporary-modes, combo-multiplier, destroy-all-enemies, reinforcements, permadeath, run-relics, shop-between-levels, map-window, world-map, replay, daily-puzzle, leaderboard, codex-window, game-screen, main-menu, end-screen, +deck-draw, +collision-damage, +friendly-fire, +facing-hit-bonus, +momentum-energy, +combo-gated-cards, +counter-stance, +reaction-attack, +injury-cards, +card-upgrade-remove, +bonus-objectives, +protect-vip]
proposes: ["+effect:draw_card", "+effect:discard", "+effect:bump", "+trigger:attacked", "+cond:cost", "+role:card", "+ui:attack-order", "+ui:momentum-pips", "+window:card-reward", "+window:event-choice", "+window:deck-view", "+feature:fight-replay", "+axis:session"]
author: opus
date: 2026-11-09
---

# Fights in Tight Spaces — бойовик у клітинках: карти = прийоми, вороги показують удар, а ти штовхаєш їх один в одного

## Суть
Агент сам-один проти банди в тісній кімнаті на квадратній сітці. Кожен хід — рука карт-прийомів (удари, кроки, блоки, кидки, поштовхи), оплачених ресурсом **momentum**. Вороги **заздалегідь** підходять і беруть агента на приціл — видно, хто куди вдарить і в якому порядку; гравець ухиляється так, щоб удари й постріли влучили в інших ворогів, або виштовхує їх за край арени. Колода росте між боями (роглайк-забіг із розділів і босів); HP агента не відновлюється між боями.

## Поле і час
- Арена — невелика квадратна сітка (кімната, бар, вагон, дах); клітини: підлога, низькі перешкоди, високі перешкоди/стіни, смертельний край (частина позначена черепом, але не всі).
- Хід розкладено на 5 фаз: добір руки → вороги рухаються (і беруть ціль) → гравець грає карти → вороги атакують → прибуває підкріплення (steamah).
- Дальність рахується лише по прямих лініях, не по діагональній відстані; запис дальності `1`, `1-2`, `2-2` (мінімальна дальність — не бʼє впритул).
- Видимість: вороги і високі перешкоди блокують лінію; низькі перешкоди блокують ближній удар, але не постріл.
- Інформація часткова: наміри, шкода й порядок атак видно; склад підкріплення й колода — ні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент | player | HP (тягнеться між боями), momentum: місткість + регенерація, combo | грає карти з руки; рух і атаки — лише картами |
| Колода / рука / скидання | supply | рука фіксованого розміру | добір до ліміту на початку ходу; скидання повертається лише після вичерпання колоди (перетасовка) |
| Карта атаки | supply | вартість momentum, дальність, шкода | шкода, часто +combo; деякі масштабуються від combo |
| Карта руху | supply | вартість | зсуває агента; варіанти «навколо ворога» (діагональ повз сусіда), «повз ворога» / «через низьку перешкоду» (2 клітини крізь) |
| Карта блоку | supply | значення | тимчасові HP на цей хід; не скасовує поштовх |
| Карта контратаки (counter) | supply | — | стійка: удар у відповідь на кожну дію ворога, що атакує агента |
| Карта поштовху (push) | supply | — | ціль на 1 клітину геть від агента; колізія / вихід за край |
| Карта move-ефекту (swap, grapple, shove) | supply | — | змінює позицію чи напрям ворога **без** колізійної шкоди й без виходу за край |
| Combo-карта | supply | вартість 0, поріг combo | грається лише при combo ≥ порогу, combo не витрачає |
| Combo finisher | supply | — | обнуляє combo, шкода зростає від накопиченого |
| Injury | supply | — | карта-сміття, яку ворог додає в колоду; зникає після бою |
| Ворог ближнього бою | enemy | HP, шкода | підходить, бере ціль; атакує лише якщо ціль досяжна |
| Ворог-стрілець (Rifleman) | enemy | дальність | постріл летить до першої перешкоди / краю; низькі перешкоди не заважають |
| Ворог з атакою по площі | enemy | зона | бʼє все в позначеній зоні — і своїх |
| Ворог з reaction attack | enemy | ліміт за хід | бʼє після кожної карти гравця в зоні досяжності, і по зсунутих ворогах теж |
| Ворог «turn to face» | enemy | орієнтація | після руху агента повертається до нього; ззаду його вдарити важко |
| Ворог з counter attack | enemy | — | бʼє будь-кого, хто його вдарив, навіть союзника |
| Ворог-штовхач | enemy | — | поштовх агента за тими самими правилами колізії й краю |
| Ворог з регенерацією блоку | enemy | блок щохід | блок відновлюється, якщо не приголомшений |
| Бос / підбос | boss | HP, спецприйоми | кінець розділу; бій із приспішниками |
| Посол (ambassador) | ally | HP | бонус-ціль «захистити»: вороги цілять у нього, удари агента його не ранять |
| Інформатор (informant) | neutral | HP | ціль «не дати вбити»: ворог, якого вороги не чіпають, а агент мусить зберегти |
| Кейс (briefcase) | pickup | клітина | ціль «забрати за X ходів»; вороги можуть стати на клітину |
| Низька перешкода | static | — | блокує рух і ближній удар, не постріл; при зіткненні — шкода |
| Висока перешкода / стіна | static | — | блокує рух і лінію; зіткнення — шкода |
| Смертельний край | hazard | частина з черепом | виштовхнутий за край гине одразу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «добрати карти до розміру руки»`, `counter(momentum, =regen)`; невитрачений momentum згорає.
- КОЛИ `custom: «колода порожня, треба добрати»` → ТО `custom: «перетасувати скидання в колоду»`.
- КОЛИ `phase_start(enemy_move)` → ТО кожен ворог `move(enemy, to)` на позицію атаки й `set_state(enemy, target_acquired)` — намір і порядок видно (`telegraph-marker`).
- КОЛИ `input(play_card, card, cell)` → ЯКЩО `has(player, momentum, cost)` → ТО `counter(momentum, -cost)` і ефекти карти; інакше `block`.
- КОЛИ `contact(strike, enemy)` → ТО `damage(n)`, `counter(combo, +1)` за кожне влучання (багатоударна карта — швидше).
- КОЛИ `after(move(player, cell))` → ТО `counter(combo, -1)` **за кожну пройдену клітину**, не за карту.
- КОЛИ `input(play_card, combo_card)` → ЯКЩО `chain(n)` → ТО ефект без витрати momentum і без витрати combo; інакше `block`.
- КОЛИ `input(play_card, finisher)` → ТО `damage(f(combo))`, `reset_combo`.
- КОЛИ `input(play_card, push)` → ТО `push(target)` на 1 клітину напряму геть від агента.
- КОЛИ `after(push(a))` → ЯКЩО `occupied(cell_behind, obstacle)` → ТО `custom: «bump»`: `damage(4)` цілі, ціль на місці.
- КОЛИ `after(push(a))` → ЯКЩО `occupied(cell_behind, enemy)` → ТО `custom: «bump»`: `damage(4)` обом.
- КОЛИ `edge(a)` → ТО `disappear_a` (ring out = миттєва смерть, хоч скільки HP).
- КОЛИ `input(play_card, move_effect)` → ТО `move(enemy, to)` або `face(enemy, dir)` — без колізії й без смерті за краєм (custom: «move ≠ push»).
- КОЛИ `input(play_card, block)` → ТО `set_state(player, block, 1 turn)`; КОЛИ `contact(attack, player)` → ЯКЩО `state(player, block)` → ТО шкода спершу знімається з блоку; поштовх відбувається все одно; деякі вороги ігнорують блок.
- КОЛИ `custom: «агента атакують»` → ЯКЩО `state(player, counter) and in_range(player, attacker, r)` → ТО `damage(n)` атакувальнику — після атаки, раз на дію ворога, навіть якщо вся шкода заблокована; орієнтація не важить.
- КОЛИ `input(play_card, stun)` → ТО `stun(enemy, 1)`: жодних дій, навіть пасивних (регенерація блоку).
- КОЛИ `input(play_card, throw)` → ТО `set_state(enemy, downed)`: не ціль, не блокує рух і лінію, не атакує цього ходу.
- КОЛИ `turn_start(enemy)` → ЯКЩО `state(enemy, downed)` → ТО `clear_state(downed)` і `stun(enemy, 1)`; ЯКЩО `occupied(cell, unit)` → ТО `damage(5)` тому, хто стоїть на поваленому.
- КОЛИ `after(move(player))` → ЯКЩО `custom: «ворог turn-to-face»` → ТО `face(enemy, player)`; без руху агента ворог не повертається — можна бити ззаду.
- КОЛИ `after(card)` → ЯКЩО `in_range(reactor, player, r) and count(reactions, <, limit)` → ТО `damage(n)` (reaction attack; не перериває карту посередині).
- КОЛИ `phase_start(enemy_attack)` → ЯКЩО `state(enemy, target_acquired) and in_range(enemy, target, r)` → ТО атака в позначені клітини: `damage(n)` усім, хто там стоїть (вороги теж) — friendly fire.
- КОЛИ `contact(injury_attack, player)` → ТО `give(player, injury_card)`; КОЛИ `level_end` → ТО `take(player, injury_card)`.
- КОЛИ `phase_start(reinforcements)` → ТО `spawn_at(enemy, entry)`.
- КОЛИ `all_gone(enemy)` → ТО `win` (бій), нагорода → `window(card-reward)`.
- КОЛИ `hp_zero(player)` → ТО `lose`: забіг закінчено, почати заново.
- КОЛИ `level_end` → ЯКЩО `custom: «виконано бонус-ціль»` → ТО `currency(+n)` (на підбосах більше).
- Перемога: знищити всіх ворогів бою; забіг — перемогти босів розділів · Поразка: HP агента = 0 · Рахунок: гроші й бонус-цілі; у daily — онлайн-рахунок.

## Керування і ввід
- Миша: клік по карті в руці → підсвітка допустимих клітин/цілей → клік по клітині. Наведення на ворога показує HP, майбутню шкоду і **номер у черзі атак**.
- Карти грає лише агент; позиція змінюється тільки картами руху/ефектами атак.
- Кнопка кінця ходу; геймпад на консолях.

## Вікна, меню, HUD
- `main-menu`: Продовжити · Новий забіг (вибір стартової колоди (?)) · Daily mission · Компендіум (`codex-window`) · Налаштування (`settings-window`) · Вихід.
- `map-window` — мапа розділу з вузлами: Fight · Event · Gym · Medical centre · Office (після боса розділу).
- `game-screen`: арена; `pocket` (рука карт) знизу; `energy-bar` momentum (місткість/регенерація); `combo-meter`; `hp-bar` агента і ворогів; `telegraph-marker` (клітини атак), `threat-range`; `tooltip` ворога з порядком атак; `objective-text` бонус-цілей з лічильником ходів; `end-turn-button`.
- `custom-window` «card reward» — вибір 1 нової карти після бою; також HP, max HP, max combo, max momentum, гроші.
- `custom-window` «Event» — сюжетний вибір із наслідками (шкода, карти, травми, бій).
- `shop-window`-подібні: Gym (апгрейд карти за фіксовану ціну, видалення карти; повтор тієї самої опції в тому ж gym подвоює ціну) · Medical centre (лікування, +max HP, зняти довгу травму).
- `upgrade-window` — Office: вибір enhancement (4 слоти, старт з 1; повні — замінити).
- `replay-window` — після перемоги бій програється як кіно в реальному часі.
- `end-screen` — кінець забігу; `leaderboard` для daily mission.

## Фічі поза полем
- Забіг: розділи з босами; порядок боїв, вороги й нагороди змінюються щоразу (`meta-progression` — відкриття нових можливостей).
- Deckbuilding: +1 карта після бою, апгрейд кожної карти один раз, видалення карт за гроші.
- Enhancements — пасивні бонуси поза картами (4 слоти); довгі травми (long-term injuries) — пасивні штрафи з подій (дорожчий рух), знімаються в Medical centre.
- `mode-daily`: щоденна місія з онлайн-таблицею.
- Бонус-цілі бою: пройти за X ходів · забрати кейс за X ходів · досягти combo X · виштовхнути X ворогів · X ворогів мають убити інших · захистити посла · зберегти інформатора.

## Варіації й родичі
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (видимі наміри + штовхання з колізією), [hoplite](hoplite.md) (один герой, ворог бʼє за видимим правилом), [frozen-synapse](frozen-synapse.md) (планування проти видимої загрози).
- Поза корпусом: Slay the Spire (карти + наміри ворогів числами), Tactical Breach Wizards (вибивання ворогів у вікна), Superhot (бойовик як пазл).
- Сиквел: Fights in Tight Spaces 2 (?).
- **Осі варіацій**: дія — з колоди (FiTS) / з набору вмінь (ITB) · ресурс — momentum + combo / AP · поштовх — 1 клітина з колізією / ланцюг / move без колізії · смерть — HP / ring out / friendly fire.

## Цікавинки для курсу
- Push з колізією й ring out (4 шкоди об стіну, 4 обом об ворога, край = смерть) — 📎 поверх `push-object`.
- Два ресурси: momentum (поновлюється) і combo (росте від влучань, падає від кожної клітини руху) з картами-порогами й finisher-ами — 🥉.
- Фази ходу з «ціль узята на етапі руху ворога» + friendly fire в позначені клітини — 🥈 (наміри, що не перераховуються, коли агент тікає).
- Reaction attack / turn-to-face / counter attack як три різні реакції ворогів на дію гравця — 🥉 (таблиця подій → реакцій).
- Колода/рука/скидання з перетасовкою і картами-травмами — 🥉.
- Повалений ворог (throw): не блокує, не ціль, встаючи ранить того, хто на ньому — 📎.
- Кінематографічний replay бою з журналу ходів — 🥈.

## Мапа на каталог
- Є: `telegraphed-intents` + `telegraph-marker` ↔ наміри ворогів · `threat-range` · `hover-highlight` (порядок атак) · `legal-move-highlight` · `push-object` ↔ поштовх · `hp-damage` · `impassable-cells` (низькі/високі перешкоди) · `environment-death` ↔ ring out · `melee-vs-ranged` · `line-of-sight-attack` (постріл до першої перешкоди) · `status-effects` / `temporary-modes` (stun, downed, block) · `combo-multiplier` ↔ combo · `destroy-all-enemies` · `reinforcements` · `permadeath` (кінець забігу) · `run-relics` ↔ enhancements · `shop-between-levels` ↔ gym/medical · `world-map`/`map-window` ↔ мапа розділу · `replay` · `daily-puzzle` + `leaderboard` ↔ daily mission · `codex-window` ↔ компендіум.
- **Нема** → пропозиції карток:
  - `+deck-draw` «Колода / рука / скидання» · entities/state · 🥉 · слоти {hand_size, reshuffle}.
  - `+collision-damage` «Шкода від зіткнення при поштовху» · entities/combat · 📎 · {dmg: 4, both: true}.
  - `+friendly-fire` «Атака ворога ранить ворогів» · entities/combat · 🌱.
  - `+facing-hit-bonus` «Орієнтація й удар ззаду» · entities/state · 📎.
  - `+momentum-energy` «Енергія на хід із регенерацією» · game-logic/economy · 🌱 · {capacity, regen}.
  - `+combo-gated-cards` «Карти з порогом combo і finisher» · game-logic/score · 📎.
  - `+counter-stance` «Стійка контратаки» · entities/combat · 📎.
  - `+reaction-attack` «Ворог бʼє у відповідь на дію гравця» · game-logic/opponent · 🥉 · {limit}.
  - `+injury-cards` «Сміттєві карти від ворога» · entities/state · 🌱.
  - `+card-upgrade-remove` «Апгрейд і видалення карт між боями» · game-logic/economy · 📎.
  - `+bonus-objectives` «Додаткові цілі рівня з нагородою» · game-logic/win · 📎 · {list}.
  - `+protect-vip` «Захистити / зберегти NPC» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:draw_card` — добрати N карт у руку (не плутати з `draw` = нічия).
- `+effect:discard` — карта йде в скидання / зникає з руки.
- `+effect:bump` — зіткнення при поштовху в зайняте: шкода, руху нема (як в Into the Breach).
- `+trigger:attacked` — сутність стала ціллю атаки (counter-стійки, counter attack ворогів).
- `+cond:cost` — вистачає ресурсу на дію/карту (momentum, mana, AP); зараз через `has`.
- `+role:card` — карта як сутність поза полем (рука/колода).
- `+ui:attack-order` — номер черговості атак ворогів при наведенні; `+ui:momentum-pips` — шкала енергії з місткістю і регенерацією.
- `+window:card-reward` — вибір 1 з N карт після бою; `+window:event-choice` — подія з варіантами й наслідками; `+window:deck-view` — перегляд колоди/скидання.
- `+feature:fight-replay` — програвання щойно виграного покрокового бою як кіно в реальному часі.
- `+axis:session` — `run`.

## Джерела
- ⭐ [steamah: tips, tricks & core mechanics](https://steamah.com/fights-in-tight-spaces-tips-tricks-core-mechanics/) — фази ходу, momentum, combo, push/колізія 4/край, stun/throw (5 шкоди), counter, reaction/turn-to-face/counter attack, бонус-цілі, вузли мапи, enhancements.
- [Steam](https://store.steampowered.com/app/1265820) — 200+ карт, апгрейди, injuries, події, daily mission, дати релізу.
- [Wikipedia](https://en.wikipedia.org/wiki/Fights_in_Tight_Spaces) — структура забігу, combo-пороги, наміри, replay, розробник, порти.
- [MGW: Basic Tactics](https://www.magicgameworld.com/?p=125934) — ring out, колізія, friendly fire, порядок атак при наведенні.
- YouTube: пошук «Fights in Tight Spaces gameplay».

## Непевне
- (?) Розмір руки, стартова колода й вибір стартових колод/персонажів — не перевірено; «3 місткість і 3 регенерація на старті, до ~9 пізніше» — лише з фан-гайду.
- (?) Шкода колізії 4 і 5 від вставання — з фан-гайду; можуть залежати від складності / версії.
- (?) Бонус за удар ззаду — є «ззаду можна вдарити», але числа бонусу не бачив.
- (?) Undo карти/ходу — не перевірено.
- (?) Рівні складності й кількість розділів — не перевірено; сиквел FiTS 2 — з памʼяті.
