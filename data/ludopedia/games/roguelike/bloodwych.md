---
title: Bloodwych
slug: bloodwych
aka: [Bloodwych Data Disks Vol 1, The Extended Levels]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: hidden
  random: runtime
  goal: state
year: 1989
platforms: [Atari ST, Amiga, ZX Spectrum, Amstrad CPC, C64, MS-DOS]
links:
  - {kind: other, url: "https://mocagh.org/miscgame/bloodwych-alt-manual.pdf", best: true, note: "мануал ST/Amiga (EN/FR/DE/IT): чемпіони, рух, книга заклинань, інвентар, бій, повне меню розмови (Recruit, Identify, Bribe, Threat, Commend, Wait, Call…)"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0000592/Bloodwych(EN).pdf", note: "мануал Spectrum/Amstrad/C64: список 32 заклинань за кольорами, коротше меню розмови"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bloodwych", note: "мета, класи × кольори, торг лестощами, Extended Levels, порти"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Bloodwych", note: "split-screen посередині, соло — пів екрана, головоломки під двох"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bloodwych+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, orientation-state, impassable-cells, key-and-door, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, hunger-clock, status-effects, unit-xp-skills, melee-vs-ranged, party-switch, stairs-levels, realtime-ai, round-currency, shop-catalog, save-game, game-pause, player-death, gui-render, player-camera, +first-person-grid, +party-formation, +local-coop, +split-screen-coop, +recruit-talk, +dialogue-phrase-menu, +haggle-price, +bribe-passage, +colour-magic-affinity, +spell-cost-dial, +learn-on-sleep, +skill-by-use, +initiative-commend, +leave-member-behind, +resurrect-chamber, +mana-pool-spells]
proposes: ["+trigger:say(phrase)", "+cond:attitude(a, op, n)", "+effect:recruit(a)", "+effect:set_initiative(a, ±n)", "+effect:cast(spell, cost)", "+effect:sleep(party)", "+role:party-member", "+role:leader", "+ui:party-portraits", "+ui:hand-slots", "+ui:movement-arrows", "+ui:transfer-slot", "+ui:reply-line", "+window:spellbook", "+window:talk-menu", "+window:character-sheet", "+window:spell-offer", "+feature:split-screen", "+axis:view=first-person"]
author: opus
date: 2026-11-09
---

# Bloodwych — два загони на розділеному екрані в одному лабіринті; з ворогами можна торгуватись і лестити

## Суть
Покроково-клітинний данжен-кроулер від першої особи в реальному часі в традиції [dungeon-master](dungeon-master.md): загін до 4 чемпіонів ходить по клітинах міста-фортеці Treihadwyl, збирає 4 кристали з веж і несе їх у пʼяту, де Зендік. Дві незвичні речі: **кооператив двох гравців на одному екрані**, розділеному навпіл (у кожного свій загін, свій курсор, спільний світ), і **меню фраз для розмов з будь-ким** — з торговцем, іншим чемпіоном і навіть з монстром посеред бою: вербувати, питати, торгуватись, хабарити, погрожувати, лестити. Магія — 32 заклинання в 4 кольорах, ціну кожного накручують стрілками, а нові заклинання продають «феї» уві сні.

## Поле і час
- Квадратна сітка поверхів; загін — одна фігура з орієнтацією; крок вперед/назад/вбік і поворот на 90°. Сходи переводять на інший поверх.
- Вид від першої особи («стоп-кадри» перспективи), мапи в грі нема — мануал радить малювати самому.
- Real-time: монстри ходять самі, бій триває, доки хтось не загине чи не втече; пауза спільна для обох гравців.
- Два гравці: екран ділиться посередині, кожен бачить свій 3D-вид і свої панелі; соло-гравець користується лише половиною екрана (DE-вікі). Багато головоломок і зустрічей розраховані на двох.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін | player | до 4 чемпіонів, орієнтація, порядок маршу | рух 6 кнопками; упор → іконка блимає, руху нема |
| Чемпіон (16 на вибір) | ally | масть (тип), колір, Level, Strength, Agility, Intelligence, Charisma, HP, Vitality, Food, spell points | діє з власної ініціативи; лише 16 чемпіонів можна завербувати |
| Лідер | player | один із загону | виконує рух і «значущі» дії; не мусить стояти попереду |
| Пікові (Spades) | ally | бійці | будь-яка зброя, обладунок, щит; найбільше HP і сили |
| Трефові (Clubs) | ally | маги | слабкі спершу, 2 заклинання за рівень; лише малі щити |
| Чирвові (Hearts) | ally | універсали | 1 заклинання за рівень; найкращі переговорники |
| Бубнові (Diamonds) | ally | лучники/асасини | удар у спину зброєю асасина — велика шкода; лідер-бубновий помічає приховане; лише малі щити |
| Монстри й «збожеволілі» громадяни | enemy | HP, ставлення | нападають, але з ними можна говорити, торгувати, підкупити, налякати |
| Торговці й NPC | neutral | товари, ціни | купують/продають/обмінюють через меню розмови |
| Spell Faery | neutral | — | приходить уві сні до того, кому належить нове заклинання; продає його |
| Зендік | boss | — | у пʼятій вежі; мета — знищити |
| Lord of Entropy | boss | — | вигнати в царство хаосу після Зендіка |
| Кристал накопичення ×4 | pickup | колір вежі | зібрати всі 4 й віднести в пʼяту вежу |
| Вежа ×5 | zone | колір | 4 кольорові з кристалами + вежа Зендіка |
| Двері | gate | відкриті / зачинені / замкнені | Door-іконка або клік у 3D; замкнені — «LOCKED», ключ або заклинання |
| Ключі (звичайні — стос) | pickup | кількість | відмикають двері |
| Сходи | static | вгору/вниз | крок на клітину — перехід; поворот на сходах — теж перехід |
| Стовп (pillar) | static | — | займає клітину, блокує |
| Ліжко | static | — | сон перед ним — кращий відпочинок |
| Regeneration Chamber | terrain | — | повертає до життя мертвого чемпіона |
| Гобелен (tapestry) | static | — | клік, стоячи впритул, — повідомлення (лише «правильний» гобелен) |
| Ями й пастки | hazard | — | згадані в порадах мануалу; деталі (?) |
| Зброя · обладунок · щит | pickup | armour rating (менше — краще) | діють лише в руці / слоті обладунку / щита |
| Лук + стріли | pickup | стріли — стос | стріляти можна, коли і лук, і стріли в руках |
| Жезл · кільце · посох | pickup | колір | лише в руці; жезл посилює заклинання свого кольору, кільце дає «безкоштовне» чаклування |
| Їжа · напій · зілля | pickup | — | спожити з transfer-слота |
| Монети | resource | стос | валюта торгу і хабарів |
| Мертвий чемпіон | container | інвентар | інвентар доступний, якщо помер у загоні; інакше тіло треба принести |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(step_forward|step_back|step_left|step_right)` → ЯКЩО `free(cell)` → ТО `move(party, dir)`; інакше `block`, `custom: «іконка руху блимає»`.
- КОЛИ `input(turn_left|turn_right)` → ТО `face(party, ±90°)`.
- КОЛИ `enter(party, stairs)` → ТО `teleport(party, other_floor)`; КОЛИ `input(turn)` на сходах → ТО теж перехід (вгору чи вниз — залежно від того, де стояв).
- КОЛИ `input(door)` → ЯКЩО `not state(door, locked)` → ТО `custom: «відчинити / зачинити»`; інакше `message(LOCKED)`.
- КОЛИ `use(leader, key)` на замкнених дверях → ТО `custom: «відімкнути»`; заклинання Magelock — те саме без ключа (?).
- КОЛИ `input(click_object_3d)` → ТО `pickup` у transfer-слот; ЯКЩО слот зайнятий → старий предмет `place` на підлогу.
- КОЛИ `input(click_item_in_transfer)` → ЯКЩО `custom: «їжа / напій / зілля»` → ТО `use`, `counter(food, +n)` чи ефект зілля.
- КОЛИ `timer(every)` → ТО `counter(food, −1)`; ЯКЩО `counter(food, <, low)` → ТО `custom: «вітальність відновлюється повільніше»`.
- КОЛИ `counter(vitality, ==, 0)` → ТО `damage(champion, n)` щотік.
- КОЛИ `contact(party, monster)` або `input(strike)` → ТО `custom: «бій: кожен діє з ініціативи за командою загону»`.
- КОЛИ `input(strike)` → ЯКЩО `custom: «чемпіон у двох передніх позиціях маршу»` → ТО `damage(enemy, n)`; ЯКЩО `has(champion, bow) and has(champion, arrows)` і `custom: «дві задні позиції»` → ТО `throw(arrow)`.
- КОЛИ `input(defend)` → ТО `set_state(party, defending)` (можна переставляти порядок маршу).
- КОЛИ `input(retreat)` → ТО `custom: «швидко відійти від супротивника»`.
- КОЛИ `custom: «бій почався»` → ЯКЩО `state(champion, spell_prepared)` → ТО `custom: «першою дією каст підготовленого»`.
- КОЛИ `input(rune)` у книзі → ЯКЩО `custom: «заклинання відоме»` → ТО `set_state(champion, spell_prepared)`; невідомі — сірі, не вибираються.
- КОЛИ `input(cost_up|cost_down)` → ТО `custom: «ціна вище — сильніше й більший шанс, але більше spell points»`.
- КОЛИ `input(star)` → ЯКЩО `counter(spell_points, >=, cost)` → ТО ЯКЩО `prob(cast_percent)` → `counter(spell_points, −cost)`, ефект заклинання, `custom: «майстерність цього заклинання +»`; інакше `message(невдача)`.
- КОЛИ `after(cast)` → ТО `set_state(caster, recovering, dur)` — штраф на всі заклинання; довше для старших.
- КОЛИ `after(cast continuous)` → ТО `custom: «іконка заклинання замінює Door-іконку; інші заклинання заблоковані, клік — скасувати»`.
- КОЛИ `custom: «колір заклинання = колір чемпіона»` → ТО `custom: «легше кастувати, швидше росте, сильніше»`.
- КОЛИ `input(sleep)` → ТО `set_state(party, sleep)`: HP, вітальність, spell points відновлюються швидше; ЯКЩО `facing(party, bed)` → ще краще.
- КОЛИ `state_on(champion, sleep)` → ЯКЩО `custom: «накопичено досвід»` → ТО `custom: «рівень +1»`; ЯКЩО `custom: «належить нове заклинання»` → ТО `window(spell-offer)`, `choose(pay | reject)`; pay → `currency(−n)`, `give(champion, spell)`.
- КОЛИ `custom: «рівень +1»` → ТО Spades/Diamonds — заклинання раз на 2 рівні; Hearts — 1; Clubs — 2.
- КОЛИ `input(talk: recruit)` → ЯКЩО `custom: «перед загоном один із 16 чемпіонів і є вільне місце»` → ТО `custom: «приєднується, якщо погодиться»`.
- КОЛИ `input(talk: offer)` → ТО `custom: «показати предмет / золото з transfer-слота»`; поза торгом — це подарунок.
- КОЛИ `input(talk: purchase | sell | exchange)` → ТО `custom: «торг: «ні» → пропонуй більше / менше / інший предмет»`; ЯКЩО `custom: «співрозмовника задобрено лестощами або Beguile»` → ТО `custom: «ціна нижча»` (Wikipedia: меч за 10 → 6–7).
- КОЛИ `input(talk: bribe)` → ТО `custom: «монстр пропускає за предмет або золото»`.
- КОЛИ `input(talk: threat)` → ЯКЩО `custom: «спрацювало»` → ТО `custom: «смертельний страх у супротивника»`.
- КОЛИ `input(talk: commend | correct)` → ТО `custom: «ініціатива члена загону + / −»` (лише поза бою).
- КОЛИ `input(talk: wait)` → ЯКЩО `free(cell_ahead)` → ТО `custom: «чемпіон лишається на місці»`; `input(talk: call)` → ЯКЩО `in_range(waiting, party, earshot)` → `custom: «повертається»`; `input(talk: view)` → `camera(eyes_of_waiting)`.
- КОЛИ `input(talk: dismiss)` → ЯКЩО `free(cell_ahead)` → ТО `custom: «назавжди покидає загін; можна завербувати іншого»`.
- КОЛИ `input(examine tapestry)` → ЯКЩО `custom: «правильний гобелен»` → ТО `message(text)`.
- КОЛИ `hp_zero(champion)` → ТО `custom: «мертвий; інвентар доступний, якщо помер у загоні»`; КОЛИ `enter(dead, regeneration_chamber)` → ТО `custom: «оживає»`.
- КОЛИ `custom: «усі 4 кристали в пʼятій вежі»` і `died(zendick)` → ТО `custom: «вигнати Lord of Entropy»`, `win`.
- Перемога: кристали + Зендік + вигнання Ентропії. Поразка: загинув увесь загін (у кожного гравця свій). Рахунку нема.

## Керування і ввід
- Курсор-стрілка (миша або джойстик, що імітує мишу): у гравця 1 синя, у гравця 2 червона; клік по іконках панелі.
- Клавіатура (ST/Amiga): гравець 1 — стрілки (крок), Insert/Home (ST) або Delete/Help (Amiga) — поворот; гравець 2 — W/S крок, Q/E поворот, A/D крок убік.
- Spectrum/Amstrad — клавіатура з перепризначенням або джойстик.
- Лідер — подвійний клік по іконці масті; порядок маршу — клік по масті (сіріє) і клік по новій позиції.
- Двоє одночасно: дії обох гравців паралельні; збереження/завантаження — лише якщо **обидва** клацнули диск.

## Вікна, меню, HUD
- `character-select` (Figure One): 16 щитів чемпіонів, Player Boxes, Character Scroll, іконки Bag → Book → Scroll, підтвердження іконкою масті; кожен гравець бере до 4.
- `game-screen` (Figure Two, на половину екрана для кожного гравця): 3D-вид, `party-portraits` (щити й масті), блок статистики лідера з трьома смугами (`hp-bar`, `energy-bar` вітальність, spell points), `movement-arrows`, Door/Star-іконка, іконки інвентаря / книги / сувою, панель статусу (вхід у розмову), Strike/Defend, два `message-log`-вікна, `reply-line` (відповідь співрозмовника червоним угорі).
- `inventory-window` (Figure Four): 12 слотів (Spectrum — 10) — `hand-slots` ×2, обладунок, щит, рюкзак ×8; armour rating; масті загону; `transfer-slot`; Exit.
- `spellbook` (Figure Three): сторінки по 4 руни, стрілки гортання, назва/колір/ціна, стрілки ціни, зірки-«каст», шанс каста, spell points.
- `character-sheet` (Character Scroll): Level, Strength, Agility, Intelligence, Charisma, HP, Vitality, Food.
- `talk-menu`: Communicate — сторінка 1: Recruit · Identify (Who goes? / Thy trade? / Name self / Reveal self) · Inquiry · Whereabouts; сторінка 2: Trading (Offer / Purchase / Exchange / Sell) · Smalltalk (лестощі, образи) · Yes & No · Bribe · Threat · Commend · Correct; також View · Wait · Dismiss · Call; перемикач сторінок — swap-іконка.
- Службові іконки панелі статусу: Exit · Disc (`save-slots`) · Pause (`pause-menu` для обох) · Sleep.
- `spell-offer`: фея уві сні пропонує заклинання — заплатити або відмовити.
- Бій: числа шкоди спалахують на щиті ураженого; статус-панель перетворюється на кольорові вертикальні смуги HP загону.

## Фічі поза полем
- `local-multiplayer` (кооп на розділеному екрані) — головна фіча; спільна пауза й спільне збереження.
- `save-slots` / `continue` (диск); перезапис на свій страх.
- Прогресія: рівні — лише уві сні; заклинання — від фей за гроші; майстерність окремо для кожного заклинання (`skill-by-use`).
- Expansion «Extended Levels» (ST/Amiga): імпорт збереження з оригіналу, сильніші вороги (рекомендований рівень 14), монстрів можна вербувати, прискорений досвід для слабших; безкоштовна брошура підказок.

## Варіації й родичі
- [dungeon-master](dungeon-master.md) — найближчий родич: загін у клітині, real-time, перша особа. Bloodwych додає кооп і розмови, віддає руни на користь книги з регулятором ціни.
- [legend-of-grimrock](legend-of-grimrock.md), [eye-of-the-beholder](eye-of-the-beholder.md) — та сама лінія «загін 2×2 на сітці».
- Сиквел Hexx: Heresy of the Wizard (1994) — без коопу, вільніший рух, більше магії, менше головоломок.
- Осі варіацій: **гравці** (один / двоє на розділеному екрані / онлайн) · **розмова** (нема / меню фраз / дерево діалогів) · **магія** (руни / книга з ціною / список) · **прогресія** (від вжитку / рівні уві сні / купівля заклинань).

## Цікавинки для курсу
- Розділений екран: два незалежні загони в одному світі, дві камери, спільна пауза й збереження за згодою обох — 🥈 (два вводи, два рендери, синхронізація).
- Меню фраз як «бойова» дія: торг з відповіддю «так/ні», ціна падає від лестощів і Charisma — 📎 (автомат станів розмови + ставлення).
- Регулятор ціни заклинання: потужність і шанс каста лінійно від витраченої мани, майстерність росте від успіхів — 🌱.
- Ініціатива члена загону (Commend / Correct) — параметр AI-союзника, яким гравець керує словами — 📎.
- Wait / Call / View: залишити члена загону на клітині й подивитись його очима — 📎 (кілька камер на одну мапу).
- Порядок маршу 2+2: передні бʼють, задні стріляють, магія з будь-якої позиції — 🌱.
- Колір магії: чемпіон, вежа, кристал, жезл одного кольору підсилюють одне одного — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `orientation-state` · `impassable-cells` (стовпи, стіни) · `key-and-door` · `hp-damage` · `inventory` / `inventory-items` / `inventory-limit` (12 слотів) · `item-pickup` · `hunger-clock` (Food) · `status-effects` (Paralyze, Confuse…) · `unit-xp-skills` · `melee-vs-ranged` (позиції маршу) · `party-switch` (лідер) · `stairs-levels` · `realtime-ai` · `round-currency` (монети) · `shop-catalog` (торговці) · `save-game` · `game-pause` · `player-death` · `gui-render` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+split-screen-coop` «Двоє на розділеному екрані в одному світі» · interface/render · 🥈.
  - `+dialogue-phrase-menu` «Розмова меню фраз з будь-якою істотою» · entities/interact · 📎.
  - `+haggle-price` «Торг: «ні» → нова пропозиція; ціна від харизми й лестощів» · game-logic/economy · 📎.
  - `+bribe-passage` «Хабар за прохід повз ворога» · entities/interact · 🌱.
  - `+spell-cost-dial` «Ціна заклинання — регулятор сили й шансу» · entities/combat · 🌱.
  - `+learn-on-sleep` «Рівні й нові заклинання лише уві сні» · entities/state · 🌱.
  - `+colour-magic-affinity` «Колір чемпіона = легша магія свого кольору» · entities/combat · 🌱.
  - `+initiative-commend` «Хвала/догана змінює ініціативу союзника» · entities/state · 📎.
  - `+leave-member-behind` «Залишити члена загону й покликати назад» · entities/move · 📎.
  - `+resurrect-chamber` «Клітина, що оживляє мертвого» · entities/interact · 🌱.
  - `+first-person-grid`, `+party-formation`, `+skill-by-use`, `+local-coop`, `+recruit-talk`, `+mana-pool-spells` — уже в корпусі.

## Пропозиції до словників
- `+trigger:say(phrase)` — гравець вимовив фразу з меню розмови (Recruit, Bribe, Threat…).
- `+cond:attitude(a, op, n)` — ставлення співрозмовника (задобрений лестощами, наляканий).
- `+effect:recruit(a)` — істота приєднується до загону; `+effect:set_initiative(a, ±n)` — ініціатива AI-союзника; `+effect:cast(spell, cost)` — каст з обраною ціною; `+effect:sleep(party)` — сон загону.
- `+role:party-member`, `+role:leader` — як у `dungeon-master`.
- `+ui:party-portraits`, `+ui:hand-slots`, `+ui:movement-arrows` — як у `dungeon-master`; `+ui:transfer-slot` — «рука курсора» для предметів; `+ui:reply-line` — рядок відповіді співрозмовника.
- `+window:spellbook` — книга заклинань сторінками; `+window:talk-menu` — дві сторінки фраз; `+window:character-sheet`; `+window:spell-offer` — пропозиція заклинання уві сні.
- `+feature:split-screen` — два гравці, екран навпіл.
- `+axis:view=first-person`; `actors: party` — уже ⏳ у classes.md, тут вжито.

## Джерела
- ⭐ [Мануал ST/Amiga (mocagh.org)](https://mocagh.org/miscgame/bloodwych-alt-manual.pdf) — повні правила англійською (і FR/DE/IT): вибір чемпіонів, атрибути, рух і клавіші двох гравців, двері, книга заклинань, інвентар, гобелени, бій, повне меню розмови, сон, поради.
- [Мануал Spectrum/Amstrad/C64 (spectrumcomputing)](https://spectrumcomputing.co.uk/zxdb/sinclair/entries/0000592/Bloodwych(EN).pdf) — 32 заклинання з поясненнями (Serpent, Moon, Dragon, Shadow), коротше меню торгу.
- [Wikipedia EN](https://en.wikipedia.org/wiki/Bloodwych) — мета, кольори, торг лестощами й Beguile, Extended Levels, розробники.
- [Wikipedia DE](https://de.wikipedia.org/wiki/Bloodwych) — split-screen посередині, соло на пів екрана, головоломки під двох, Hexx.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Bloodwych+gameplay).

## Непевне
- (?) Ями, пастки, кнопки на стінах — мануал лише радить відмічати ями й пастки на мапі; механіку не описано.
- (?) Чи можуть двоє гравців бити один одного — порада «не посваріться до вбивства» натякає, що так.
- (?) Двері, що відмикаються кристалом (брошура підказок Trazere бачилась лише в пошуку).
- (?) Що саме дає кільце («free» spellcasting — Wikipedia) — без витрати spell points чи лише ефект без вивчення.
- (?) Magelock відмикає двері («навіщо ті ключі» — опис заклинання), але чи замикає теж — не перевірено.
- (?) Четвертий колір у мануалі Spectrum зветься Shadow, у 16-бітному — Chaos (жовтий) — одна й та сама школа.
