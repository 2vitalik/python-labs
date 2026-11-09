---
title: "King's Bounty: The Legend (King's Bounty. Легенда о рыцаре)"
slug: kings-bounty-the-legend
aka: [KB, KBTL, "King's Bounty: Легенда", "Легенда о рыцаре", "King's Bounty: Armored Princess", "King's Bounty: Crossworlds"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2008
platforms: [PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/King%27s_Bounty:_The_Legend", best: true, note: "real-time мапа пригод і покроковий бій, до 5 загонів, Leadership обмежує розмір загону, Rage і чотири духи, класи, руни, дружина"}
  - {kind: other, url: "https://www.mogelpower.de/manuals/Kings_Bounty_The_Legend_Manual_Englisch.pdf", note: "мануал (EN, PDF): параметри загону, ініціатива, Speed = AP, мораль, типи шкоди й опори, таланти, інтерактивні обʼєкти арени, духи гніву, книга заклинань"}
  - {kind: steam, url: "https://store.steampowered.com/app/25900/", note: "сторінка гри"}
  - {kind: other, url: "https://www.gamebanshee.com/kingsbountythelegend/walkthrough/introduction.php", note: "вступ гайду: бій як у HoMM, поради з лідерства і класів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=King%27s+Bounty+The+Legend+combat+gameplay", note: "пошук; бій"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, piece-move-patterns, reachable-highlight, legal-move-highlight, destroy-all-enemies, ai-opponent, realtime-ai, status-effects, inventory-items, world-map, map-window, shop-window, round-currency, unit-xp-skills, save-game, difficulty-levels, multi-cell-size, explode-area, item-pickup, chase-player, +hex-grid-render, +unit-stack-count, +leadership-cap, +initiative-order, +speed-as-ap, +retaliation, +morale-states, +race-relations-morale, +elemental-resistance, +talent-charges, +hero-spell-per-round, +mana-pool-spells, +scroll-or-learned-spell, +rage-meter, +summon-creature, +arena-interactive-objects, +arena-terrain-bonus, +flying-move, +retreat-surrender, +living-item-morale]
proposes: ["+trigger:round_start", "+trigger:attacked", "+cond:leadership_ok", "+effect:counterattack", "+effect:spend_ap", "+effect:gain_rage", "+role:stack", "+ui:stack-count", "+ui:turn-order-bar", "+ui:rage-bar", "+ui:mana-bar", "+window:spellbook", "+window:rage-box", "+window:army-window", "+window:creature-info", "+feature:garrison"]
author: opus
date: 2026-11-09
---

# King's Bounty: The Legend — гекс-бій загонів-стеків: кількість у загоні обмежує лідерство героя, а гнів і мана — дві паралельні «руки» героя

## Суть
Герой не бʼється сам: він веде **до 5 загонів** («стеків») істот, і скільки істот можна тримати в загоні, визначає його **Leadership** (кожна істота має ціну лідерства). Бій — на гекс-арені, загони ходять за ініціативою, **Speed = очки дії** (1 гекс = 1 AP, атака/талант забирає всі). Раз за хід свого загону герой може скористатись **книгою заклинань** (мана) і **скринькою гніву** (Rage → удари чотирьох духів). Ядро — бій «без втрат»: загиблих істот не повернеш даром, а поразка забирає всю армію. Тут описано бойову систему; мапа пригод — побіжно.

## Поле і час
- Мапа пригод — у реальному часі з паузою (Space), день і ніч; ворожі армії стоять або йдуть до героя; контакт → бій.
- Арена — гекс-сітка різної форми й розміру залежно від місця (галявина, мури замку, палуба корабля, «нутро» живого предмета); перешкоди низькі (зупиняють піших) і високі (непрохідні навіть для летючих).
- Раунд: усі загони обох сторін ходять по одному **в порядку ініціативи**; коли всі сходили — новий раунд.
- Освітлення і тип арени міняють параметри: нежить сильніша вночі й на цвинтарі, демони — на лаві, слабшають на снігу.
- Інформація повна: параметри ворожих загонів відкриті (кількість вороже — приблизна (?)).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загін (стек) гравця | piece | раса, Leadership за одиницю, кількість, HP/шкода на одиницю, Attack, Defence, Initiative, Speed, мораль, опори до 4 типів шкоди, риси, до 3 талантів | ходить, атакує, застосовує талант; гине, коли вбито останню істоту |
| Ворожий загін | enemy | те саме | AI; може мати героя-командира |
| Стрілець (лучники, гноми-гармаші) | piece | набої (?) | атака на відстань |
| Летючий (грифон, дракон) | piece | — | перелітає низькі перешкоди |
| Великий загін (дракон, ент) | piece | 2 гекси (?) | займає кілька клітин |
| Герой | player | клас (воїн / паладин / маг), Attack/Defence (додаються загонам), Intellect, Mana, Rage, Leadership, руни Might/Mind/Magic | поза полем: раз за хід — закляття або дух гніву |
| Дух гніву (Zerock, Sleem, Lina, Reaper) | ally | 4 уміння, досвід, відпочинок N ходів | удар за Rage; сильні вміння «сплять» 6–8 ходів |
| Призвана істота (крижана куля, Gizmo, скелети з труни) | ally | — | бʼється за того, хто призвав / розбив труну |
| Скриня на арені | pickup | — | бере будь-який загін, що стоїть поруч |
| Барикада | gate | HP | перешкода для піших, доки не зламана (замкові арени) |
| Міна / порохова бочка | hazard | — | при руйнуванні вибухає, бʼє всіх навколо |
| Труна | container | — | розбили → скелети за сторону, що розбила |
| Свята статуя / проклятий хрест / осине гніздо / вівтар блискавки / вулкан / крижана статуя | spawner | зона дії | щоходу кидає благословення/прокляття/шкоду на випадковий загін у зоні |
| Кам'яна стіна, крижані шипи (духи) | static | час життя | тимчасові перешкоди на 3 гекси |
| Перешкода низька / висока | static | висота | блокує піших / усіх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(hire, unit, n)` → ЯКЩО `custom: «n × лідерство одиниці ≤ Leadership героя»` and `counter(gold, ≥, price)` → ТО `custom: «додати n у загін»`, `currency(−price)`; загонів — до 5.
- КОЛИ `custom: «загін перевищив Leadership (втрата лідерства, приєднання)»` → ТО `set_state(stack, out_of_control)` — `custom: «бʼє найближчого, свого чи чужого»` (?).
- КОЛИ `contact(hero, enemy_army)` на мапі → ТО `custom: «перехід на арену бою; тип арени — за місцем зустрічі»`.
- КОЛИ `phase_start(round)` → ТО `custom: «черга загонів за Initiative, рівні — за Speed (?)»`.
- КОЛИ `turn_start(stack)` → ТО `counter(ap, =Speed)`.
- КОЛИ `input(move, stack, hex)` → ЯКЩО `path_exists(stack, hex)` and `counter(ap, ≥, len)` → ТО `move(stack, hex)`, `counter(ap, −1)` за гекс; летючий — над низькими перешкодами.
- КОЛИ `input(attack, stack, target)` → ЯКЩО `adjacent(stack, target)` або `custom: «стрілець»` → ТО `damage(target, n)`, `counter(ap, =0)`.
- Шкода: `custom: «шкода одиниці × кількість; Attack > Defence цілі — більше, менше — менше; тип шкоди × (1 − опір цілі), опір < 0 — більше»`; КОЛИ `custom: «сумарна шкода ≥ HP верхньої одиниці»` → ТО `counter(count, −k)` — гинуть цілі одиниці.
- КОЛИ `custom: «атаковано впритул»` → ЯКЩО `not custom: «атакувальник має «без відповіді»»` → ТО `custom: «відповідь (retaliation)»` (кількість відповідей за раунд — (?)).
- Мораль: ЯКЩО `state(stack, high_morale)` → ТО Attack/Defence ↑, частіші крити; ЯКЩО `state(stack, low_morale)` → ТО параметри ↓, критів нема; мораль псують неприязні раси в армії (люди не люблять орків, нежить, демонів).
- Крити: `custom: «шанс крита росте з моралі і рівня Rage героя»`.
- КОЛИ `input(talent, stack)` → ЯКЩО `counter(charges, >, 0)` або `not state(talent, cooldown)` → ТО ефект таланту, `counter(ap, =0)` (крім талантів на швидкість); `counter(charges, −1)` або `set_state(talent, cooldown, n)`.
- КОЛИ `input(spell, hero, target)` → ЯКЩО `custom: «книгу ще не відкривали цього ходу»` and (`has(hero, scroll)` або `counter(mana, ≥, cost)`) → ТО ефект; сувій зникає, вивчене закляття — `counter(mana, −cost)`; маг з Higher Magic — двічі.
- Сила закляття: `custom: «+10 % шкоди за 1 Intellect, +1 хід тривалості за 10 Intellect; рівні I–III»`.
- КОЛИ `custom: «загони обмінялись ударами»` → ТО `counter(rage, +n)`; КОЛИ `died(stack)` (весь загін) → ТО `counter(rage, +2n)`.
- КОЛИ `input(rage_box, hero, skill)` → ЯКЩО `counter(rage, ≥, cost)` and `not state(spirit, resting)` → ТО ефект духа, `counter(rage, −cost)`, `set_state(spirit, resting, n)`.
- КОЛИ `adjacent(stack, chest)` → ТО `pickup(chest)` для сторони загону.
- КОЛИ `destroyed(keg)` → ТО `explode(area)`; КОЛИ `destroyed(coffin)` → ТО `spawn_at(skeletons, coffin)` за сторону руйнівника.
- КОЛИ `turn_start(statue)` → ЯКЩО `in_range(statue, stack, r)` → ТО `custom: «закляття на випадковий загін у зоні»`.
- КОЛИ `all_gone(enemy_stacks)` → ТО `win` бою: досвід, золото; КОЛИ `all_gone(own_stacks)` або `input(flee)` → ТО `custom: «втрачено всі загони, ні досвіду, ні золота, герой у столиці»` — гра триває.
- Між боями: КОЛИ `custom: «бій скінчився»` → ТО `custom: «мана відновлюється, Rage згасає до 0»`.
- Перемога: виконати сюжетні квести королівства · Поразка: бій — втрата армії; гри — фактично лише через ліміти (?) · Рахунок: досвід, титули, лідерство.

## Керування і ввід
- Мапа: клік-куди-йти конем/кораблем, пауза Space; лопата — викопати скарб поруч.
- Бій: виділено поточний загін; клік по гексу — рух, по ворогу — атака (курсор показує напрям удару і прогноз втрат (?)); кнопки талантів загону; кнопки книги заклинань і скриньки гніву; «чекати», «захист» (?), авто-бій (?).
- Наведення на загін — підказка параметрів, ефекти іконками з кількістю ходів (зелені — добрі, червоні — погані).

## Вікна, меню, HUD
- `main-menu`: New Game → `character-select` (воїн / паладин / маг) і `difficulty-select`; Load; Settings; Exit.
- `game-screen` (мапа пригод): герой, армії, скарби; `minimap`; панель армії; кнопки книги, квестів, героя.
- `game-screen` (бій): гекс-арена, `+ui:stack-count` під кожним загоном, `+ui:turn-order-bar` (?), `+ui:rage-bar`, `+ui:mana-bar`, `ability-buttons` талантів, `reachable-highlight`.
- `+window:spellbook` — сувої й вивчені закляття трьох шкіл (Order, Distortion, Chaos ~ по 20); `+window:rage-box` — чотири духи і їхні вміння.
- `+window:army-window` / `custom-window` героя — параметри, «лялька» з 8 слотами (шолом, зброя, щит, броня, пояс, взуття, регалії, артефакти), рюкзак, руни, дерево навичок (3 гілки, 36 навичок), дружина й діти.
- `+window:creature-info` — повна картка загону; `shop-window` замку (загони, предмети, заклинання) і гарнізон на 2 загони.
- `map-window` — світова мапа; `dialogue-window` квестів; `end-screen` бою (досвід, золото, втрати).

## Фічі поза полем
- Прогресія: досвід → рівень → руни класу; титули від короля дають Leadership і доступ до сильніших загонів; прапори на мапі — +Leadership назавжди.
- Предмети (~200), набори; **живі предмети** з мораллю: вийшли з-під контролю — придушити боєм з Гремлінами-Хранителями на арені всередині предмета.
- Дружина: 4 слоти, до 4 дітей (кожна дитина займає слот назавжди); розлучення забирає частку золота і її спорядження.
- `difficulty-presets`, `save-slots`, `autosave` (?).

## Варіації й родичі
- Попередник: King's Bounty (1990, New World Computing) — звідти виросли [Heroes of Might and Magic 3](heroes-of-might-and-magic-3.md).
- Наступники: Armored Princess (2009), Crossworlds (2010), Warriors of the North (2012), Dark Side (2014), King's Bounty II (2021).
- Відмінності від [HoMM3](heroes-of-might-and-magic-3.md): розмір стека обмежений **Leadership героя** (не приростом міст), Speed як AP з «атака забирає все», **Rage-духи** як друга рука героя, інтерактивні обʼєкти арени, тип арени впливає на раси, немає міст-будівництва.
- **Осі варіацій**: обмеження армії — Leadership (KB) / приріст і гроші (HoMM) / лише кількість слотів · рука героя — 1 заклинання за раунд (HoMM) / заклинання + дух гніву (KB) · арена — порожня з перешкодами / з інтерактивними обʼєктами.

## Цікавинки для курсу
- Leadership-ліміт: кількість у стеку ≤ лідерство / ціна одиниці — 🌱.
- Стек як одна фігура: HP пулом, шкода × кількість, гинуть цілі одиниці — 📎.
- Ініціатива + Speed-як-AP, атака обнуляє AP — 📎.
- Rage-економіка: росте від обміну ударами, ×2 за знищений загін, витрачається на духів з відпочинком — 📎.
- Інтерактивні обʼєкти арени, які бʼють випадковий загін у зоні (будь-чий) — 📎.
- Опори до 4 типів шкоди (від'ємна опора = вразливість) — 🌱.
- Тип арени і час доби як модифікатори рас — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `piece-move-patterns` ↔ піші/летючі · `reachable-highlight` · `destroy-all-enemies` · `ai-opponent` · `realtime-ai` ↔ армії на мапі · `chase-player` ↔ армії біжать до героя · `status-effects` · `inventory-items` · `world-map` / `map-window` · `shop-window` · `round-currency` ↔ золото · `unit-xp-skills` ↔ духи · `multi-cell-size` · `explode-area` ↔ бочка · `item-pickup` ↔ скриня · `save-game` · `difficulty-levels`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render`, `+unit-stack-count`, `+retaliation`, `+initiative-order`, `+morale-states`, `+elemental-resistance`, `+hero-spell-per-round`, `+mana-pool-spells`, `+summon-creature`, `+flying-move`, `+retreat-surrender` — уже в корпусі.
  - `+leadership-cap` «Розмір стека ≤ лідерство героя / ціна одиниці» · entities/state · 🌱 · слот {leadership}.
  - `+speed-as-ap` «Speed = AP; атака забирає всі» · game-logic/opponent · 🌱.
  - `+race-relations-morale` «Раси в армії псують мораль одна одній» · entities/state · 📎.
  - `+talent-charges` «Уміння з зарядами або перезарядкою в ходах» · entities/state · 🌱.
  - `+scroll-or-learned-spell` «Сувій одноразовий, вивчене — за ману» · game-logic/economy · 📎.
  - `+rage-meter` «Гнів росте від бою і живить духів з відпочинком» · game-logic/economy · 📎.
  - `+arena-interactive-objects` «Обʼєкти арени діють на випадковий загін у зоні» · entities/interact · 📎.
  - `+arena-terrain-bonus` «Тип арени й доба змінюють параметри рас» · entities/state · 🌱.
  - `+living-item-morale` «Предмет з мораллю, що бунтує» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:round_start` — початок раунду (ініціативна черга); `+trigger:attacked` — загін атаковано (відповідь).
- `+cond:leadership_ok` — стек укладається в лідерство.
- `+effect:counterattack` — відповідь захисника; `+effect:spend_ap`; `+effect:gain_rage` — приріст гніву.
- `+role:stack` — фігура-загін з кількістю.
- `+ui:stack-count` — кількість під загоном; `+ui:turn-order-bar` — черга ініціативи; `+ui:rage-bar`, `+ui:mana-bar`.
- `+window:spellbook`, `+window:rage-box`, `+window:army-window`, `+window:creature-info`.
- `+feature:garrison` — залишити загони в замку.

## Джерела
- ⭐ [Wikipedia: King's Bounty: The Legend](https://en.wikipedia.org/wiki/King%27s_Bounty:_The_Legend) — мапа в реальному часі, до 5 загонів, Leadership, Rage і 4 духи, ресурси, класи, руни, дружина й діти.
- [Мануал (PDF, EN)](https://www.mogelpower.de/manuals/Kings_Bounty_The_Legend_Manual_Englisch.pdf) — параметри загону (Leadership, мораль, Attack/Defence, Initiative, Speed = AP, 1 AP за клітину, атака — усі AP), 4 типи шкоди й опори, ефекти, таланти з зарядами, інтерактивні обʼєкти, перешкоди, арени, книга заклинань (+10 %/Intellect), духи гніву (×2 Rage за загін, сон 6–8 ходів), поразка/втеча, живі предмети, гарнізон 2 загони, дружина 4 слоти.
- [Steam: King's Bounty: The Legend](https://store.steampowered.com/app/25900/) — 3 класи, real-time → покроковий бій.
- [GameBanshee: вступ](https://www.gamebanshee.com/kingsbountythelegend/walkthrough/introduction.php) — бій як у HoMM, Higher Magic двічі за хід, поради з лідерства.
- YouTube: пошук «King's Bounty The Legend combat gameplay».

## Непевне
- (?) Що стається з загоном понад Leadership: за загальною вікі серії — «виходить з-під контролю й бʼє найближчого, навіть свого»; у мануалі The Legend не бачив.
- (?) Скільки відповідей (retaliation) за раунд і чи є «чекати»/«захист» як у HoMM.
- (?) Розмір і форма арен, розмір великих істот (2 гекси?).
- (?) Тай-брейк ініціативи за Speed — з аналізу іншої гри серії.
- (?) Чи видно точну кількість у ворожих загонах.
