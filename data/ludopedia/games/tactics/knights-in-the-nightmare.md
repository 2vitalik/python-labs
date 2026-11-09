---
title: Knights in the Nightmare
slug: knights-in-the-nightmare
aka: [ナイツ・イン・ザ・ナイトメア, KitN, Dept. Heaven Episode IV]
family: tactics
also: []
klass: hybrid
axes:
  field: iso
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2008
platforms: [DS, PSP, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knights_in_the_Nightmare", best: true, note: "Wisp, діагональне прицілювання, Time gauge, Rush Count, Enemy Matrix «хрестики-нулики», Vitality"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ナイツ・イン・ザ・ナイトメア", note: "JA: напрямки атак класів, Law/Chaos, Dur зброї, Effective, Trans-Soul, умови перемоги/поразки"}
  - {kind: other, url: "https://www.cgmagonline.com/review/game/knights-in-the-nightmare/", note: "60-секундні ходи, зброя з чотирьох кутів екрана, матриця 3×3 / 4×4 / 5×5"}
  - {kind: other, url: "https://www.rpgfan.com/review/knights-in-the-nightmare/", note: "рухаються лише дуелянт і лансер, самоцвіти → MP, речі з обʼєктів"}
  - {kind: other, url: "http://worthplaying.com/article/2010/12/16/reviews/78899-psp-review-knights-in-the-nightmare/", note: "PSP: туман Law/Chaos, graze → XP, слот-машина ворогів, керування PSP"}
  - {kind: other, url: "https://nintendoworldreport.com/review/19055", note: "раунди з квотою ворогів, рулетка, ~100 туторіалів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Knights+in+the+Nightmare+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, projectile-shot, time-out, permadeath, unit-xp-skills, item-pickup, inventory-items, drop-on-death, destructible-blocks, placement-screen, difficulty-levels, level-unlock, tutorial-window, game-screen, game-pause, +bullet-dodge-cursor, +graze-reward, +action-costs-time, +charge-attack, +attack-pattern-by-class, +polarity-switch, +resource-transfer, +line-win, +enemy-roulette, +weapon-durability, +unit-vitality-cost, +soul-transfer, +recruit-ally, +rush-count-triggers, +turn-limit-objectives, +elemental-resistance]
proposes: ["+trigger:graze", "+effect:sacrifice", "+effect:recruit", "+ui:enemy-matrix", "+ui:phase-indicator", "+ui:time-gauge", "+window:roulette", "+axis:control=pointer-avatar"]
author: opus
date: 2026-11-09
---

# Knights in the Nightmare — курсор-вогник ухиляється від куль і запускає нерухомих лицарів; перемога — три вбивства в ряд

## Суть
Гібрид `cursor` + `figure`: гравець веде стилусом **Wisp** — душу-курсор, — який торкається лицарів, розставлених на ізометричній сітці, і запускає їхні атаки; у цей час вороги стріляють патернами куль **у Wisp**, а не в лицарів (bullet hell). Хід триває 60 с, але час списується лише за дії (заряд атаки) і за влучання куль. Перемога на звичайній мапі — не «вбити всіх», а **скласти лінію** з убитих ворогів на окремій «Enemy Matrix», як у хрестиках-нуликах; яких ворогів і в які клітини матриці отримаєш — вирішує рулетка між ходами.

## Поле і час
- Ізометрична сітка (`field: iso`); стартові позиції своїх і ворогів фіксовані для мапи — лицарів ставлять під напрямки їхніх атак.
- Хід = до 60 с «часу дії»: таймер тече під час заряду атак і падає за кожне влучання кулі у Wisp; ухилятися можна безкоштовно. Між ходами — рулетка; мапа має ліміт ходів.
- Дві фази поля — **Law** і **Chaos**, перемикаються будь-коли (як полярність Ikaruga): змінюють патерни атак, доступну зброю й ціну MP.
- Окрема від поля **Enemy Matrix** (3×3, 4×4, 5×5): кожен ворог привʼязаний до клітини матриці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Wisp | player | без HP | курсор-душа; торкається лицарів, підбирає самоцвіти; влучання кулі = мінус час |
| Лицар | piece | рівень, Vitality, елемент, фазова схильність, клас | стоїть; атакує за патерном класу в поточній фазі |
| Duelist | piece | атака вперед | може рухатися вперед |
| Warrior | piece | атака вперед | руйнує перешкоди |
| Knight-класи | piece | атака вперед | нерухомі |
| Lancer Knight | piece | вперед і назад | ходить у всіх напрямках |
| Hermit · Archer · Priestess · Wizard | piece | атака назад | нерухомі |
| Valkyrie · Ashtarote (· La Pucelle на PSP) | piece | вперед і назад | — |
| Ворог | enemy | HP, елемент, клітина матриці | стріляє патернами куль у Wisp; деякі (типу hellhound) бʼють лицарів |
| Куля | projectile | — | летить патерном; торкнулась Wisp → мінус час |
| Бос | boss | велика смуга HP | без матриці; багато патернів куль |
| Обʼєкт поля | static | руйнований | розбити → зброя, предмет або особиста річ для вербування |
| Зброя | pickup | Dur, елемент, фаза, до 3 Effective | перетягується на лицаря з кутового слота; дає Skill Attack |
| Особиста річ лицаря | pickup | — | віддати душі → лицар приєднується назавжди |
| Самоцвіт (кристал) | pickup | — | випадає від звичайної атаки; Wisp збирає → MP |
| Магічний туман | resource | обсяг Law / Chaos | атаки висмоктують туман поточної фази → MP; висмоктане переходить у протилежну |
| Клітина матриці | mark | KILL / порожня | ставиться при смерті «свого» ворога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «вороги випускають патерни куль у бік Wisp»`.
- КОЛИ `contact(bullet, wisp)` → ТО `timer(-n)`, `disappear(bullet)`.
- КОЛИ `custom: «куля пройшла впритул до Wisp»` → ТО `counter(xp, +n)` (graze).
- КОЛИ `input(hold, knight)` → ТО `custom: «заряд атаки»`, `timer(-n)` поки триває заряд.
- КОЛИ `input(release, dir)` → ЯКЩО `custom: «dir — один із 4 діагональних напрямків, дозволений класу»` → ТО `custom: «атака за патерном класу в поточній фазі»`, `damage(enemies_in_pattern, n)`.
- КОЛИ `custom: «звичайна атака без зброї влучила»` → ТО `spawn(gem)`, `counter(fog[phase], -n)`, `counter(fog[other_phase], +n)`.
- КОЛИ `contact(wisp, gem)` → ТО `pickup(wisp, gem)`, `counter(mp, +n)`.
- КОЛИ `input(drag, weapon → knight)` → ЯКЩО `custom: «зброя доступна класу у фазі»` і `counter(mp, ≥, cost)` → ТО `custom: «Skill Attack»`, `counter(mp, -cost)`, `counter(weapon_dur, -1)`, `counter(knight_vit, -n)`.
- Заряд довше → `custom: «спецприйом; ще довше — вищий спецприйом»`.
- КОЛИ `counter(weapon_dur, ==, 0)` → ТО `disappear(weapon)`.
- КОЛИ `counter(knight_vit, ==, 0)` → ТО `disappear(knight)` назавжди.
- КОЛИ `input(switch_phase)` → ТО `set_state(field, law|chaos)`: інші патерни, інша зброя, інша ціна MP.
- КОЛИ `custom: «довго в одній фазі»` → ТО `custom: «туман фази вичерпується — MP не поповнюється»` (змушує перемикатись).
- Елементи: ЯКЩО `custom: «елемент зброї слабкий проти елемента ворога»` → ТО `custom: «мало шкоди»`.
- Rush Count: КОЛИ `custom: «удар по ворогу»` → ТО `counter(rush, +1)`; ЯКЩО `custom: «номер серії = умова Effective-трейту»` → ТО `custom: «ефект трейту: лікування лицаря, повне відновлення ворога…»` (на Easy шкідливі не спрацьовують).
- КОЛИ `destroyed(object)` або `died(enemy)` → ТО `spawn(item)` (зброя / особиста річ) — не завжди.
- КОЛИ `input(drag, keepsake → soul)` → ТО `custom: «лицар вербується назавжди»`.
- КОЛИ `died(enemy)` → ТО `mark(matrix_cell, KILL)`.
- КОЛИ `pattern(line(n))` на матриці → ЯКЩО `counter(lines, ≥, required)` → ТО `win` (звичайна мапа).
- КОЛИ `all_gone(enemy_on_field)` або `counter(time_left, ==, 0)` → ТО `end_turn`.
- КОЛИ `input(convert_time)` (меню паузи) → ТО `custom: «залишок часу → XP або MP»`, `end_turn`.
- КОЛИ `turn_end` → ТО `custom: «рулетка»`: гравець зупиняє її — `spawn_at(enemy, matrix_cell)` наступного ходу; вороги відроджуються кожен раунд.
- КОЛИ `hp_zero(boss)` → ТО `win`; HP боса після поразки на Easy/Normal зберігається для повтору.
- КОЛИ `counter(turn, >, limit)` → ЯКЩО `not custom: «лінії складено / бос убитий»` → ТО `lose`; КОЛИ `died(protagonist)` (де є на мапі) → ТО `lose`.
- Setup: КОЛИ `input(transoul, a → b)` → ТО `disappear(a)`, `heal(b_vit, n)` або стати b ↑ (ветеран дає більше).
- Setup: КОЛИ `input(level_up, knight)` → ЯКЩО `counter(xp_pool, ≥, cost)` → ТО `custom: «рівень, трохи Vitality, доступ до вищої зброї»` (до межі рівня).
- Перемога: N ліній на матриці / бос · Поразка: ліміт ходів, загибель протагоніста · Рахунок: XP і MP із залишку часу.

## Керування і ввід
- DS: стилус веде Wisp (рух = ухилення), торкання лицаря + утримання = заряд, відпускання в одному з 4 діагональних секторів = напрям атаки; перетягування зброї з кутових слотів на лицаря.
- Кнопка R — перемкнути Law/Chaos; пауза — меню з конвертацією часу.
- PSP: аналоговий стік замість стилуса (повільніше, менш точно); Switch — ремастер.
- Між раундами (без ліміту часу): спорядити зброю, підготувати предмети, змінити лицарів.

## Вікна, меню, HUD
- `custom-window` «Setup» (початок розділу): розподіл пулу XP, апгрейд зброї з ризиком, злиття однакової зброї (Dur), Trans-Soul.
- `placement-screen` «Tactics Screen»: вибір лицарів, предметів, зброї, стартової фази; інформація про ворогів.
- `game-screen` «Battle»: ізосітка, `+ui:time-gauge`, MP-шкала, `+ui:phase-indicator` Law/Chaos, 4 кутові слоти зброї, `+ui:enemy-matrix` з KILL-позначками, лічильник Rush, `turn-counter`; на боса — `hp-bar`.
- `custom-window` «Roulette» (`+window:roulette`): слот-машина ворогів і клітин матриці між ходами.
- `pause-menu`: конвертація залишку часу в XP/MP (кінець ходу).
- `tutorial-window`: близько сотні туторіалів (понад годину); `difficulty-select`: Normal → Hard → Nightmare відкриваються проходженням.
- `dialogue-window` — сюжет із флешбеками; `end-screen` — поразка.

## Фічі поза полем
- `difficulty-presets` з відкриттям: Normal → Hard → Nightmare; на DS прокачка на Hard+ вимкнена, на PSP — ні.
- `level-unlock` + повтор пройдених не-босових мап для XP і зброї.
- Прокачка лише в Setup із пулу XP; межа рівня в кожного лицаря; Trans-Soul як «обмін душі на Vitality».
- `tutorial` величезний; ремастер на Switch (2022).

## Варіації й родичі
- Dept. Heaven: [yggdra-union](yggdra-union.md) (ep. II), Riviera, Gungnir; La Pucelle — гостьовий клас на PSP (див. [la-pucelle-tactics](la-pucelle-tactics.md)).
- Родичі за механіками: [into-the-breach](into-the-breach.md) (нерухоме мислення патернами атак), [fire-emblem](fire-emblem.md) (permadeath), shmup-и Ikaruga (перемикання полярності) і Touhou (graze).
- **Осі варіацій**: хто отримує шкоду — юніти / курсор-гравець · час ходу — без ліміту / таймер, що тече лише від дій · умова перемоги — убити всіх / лінія на матриці / бос · ресурс фази — один / два сполучені (туман перетікає).

## Цікавинки для курсу
- Курсор-аватар ухиляється від куль, влучання списують час ходу — 🥈 (real-time шар поверх покрокового).
- Матриця ворогів як «хрестики-нулики» N×N + рулетка, що призначає клітини — 🥉 (перевірка ліній + випадкове призначення).
- Перемикання фаз Law/Chaos зі змінними патернами атак і спільним туманом, що перетікає — 🥉.
- Graze: близький проліт кулі дає XP — 📎 (відстань до курсора ≤ порогу).
- Таймер, що тече лише під час дій — 📎.
- Rush Count з трейтами, що спрацьовують на конкретному номері серії — 📎.
- Vitality як ціна дії + Trans-Soul (пожертвувати одного, щоб відновити іншого) — 📎.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` (кулі) · `time-out` (60 с) · `permadeath` (Vitality 0) · `unit-xp-skills` · `item-pickup` · `inventory-items` · `drop-on-death` · `destructible-blocks` (обʼєкти) · `placement-screen` · `difficulty-levels` · `level-unlock` · `tutorial-window` · `game-screen` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+bullet-dodge-cursor` «Курсор ухиляється від куль» · entities/combat · 🥈.
  - `+graze-reward` «Нагорода за близький проліт» · entities/combat · 📎 · слот {radius}.
  - `+action-costs-time` «Час ходу тече лише від дій» · game-logic/lose · 📎.
  - `+charge-attack` «Заряд атаки утриманням» · interface/input · 📎 · слот {levels: 3}.
  - `+attack-pattern-by-class` «Патерн атаки класу за фазою» · entities/combat · 🥉.
  - `+polarity-switch` «Перемикання фази поля» · entities/state · 📎.
  - `+resource-transfer` «Ресурс перетікає між фазами» · game-logic/economy · 📎.
  - `+line-win` «Лінія на матриці — перемога» · game-logic/win · 🥉 (уже в корпусі).
  - `+enemy-roulette` «Рулетка призначає ворогів і клітини» · entities/spawn · 📎.
  - `+unit-vitality-cost` «Кожна дія витрачає життя юніта» · entities/state · 📎.
  - `+soul-transfer` «Пожертвувати юніта заради іншого» · entities/state · 📎.
  - `+rush-count-triggers` «Ефекти на N-му ударі серії» · game-logic/score · 📎.
  - `+weapon-durability` · `+recruit-ally` · `+turn-limit-objectives` · `+elemental-resistance` — уже в корпусі.

## Пропозиції до словників
- `+trigger:graze` — снаряд пройшов у радіусі від гравця, не влучивши.
- `+effect:sacrifice` — прибрати свою сутність заради бонусу іншій (Trans-Soul; уже пропоновано).
- `+effect:recruit` — новий юніт приєднується до загону (уже пропоновано).
- `+ui:enemy-matrix` — сітка N×N з позначками вбитих; `+ui:phase-indicator` — поточна фаза (уже пропоновано); `+ui:time-gauge` — шкала часу ходу, що падає від дій.
- `+window:roulette` — слот-машина призначення ворогів між ходами.
- `+axis:control=pointer-avatar` — курсор водночас є аватаром, якого атакують.

## Джерела
- ⭐ [Wikipedia: Knights in the Nightmare](https://en.wikipedia.org/wiki/Knights_in_the_Nightmare) — три екрани, Wisp, діагональне прицілювання, Time gauge, Rush Count, Enemy Matrix, Vitality/Durability.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/ナイツ・イン・ザ・ナイトメア) — напрямки атак за класами, три види атак, Dur, Effective, Trans-Soul, умови перемоги/поразки, складності.
- [CGMagazine](https://www.cgmagonline.com/review/game/knights-in-the-nightmare/) — 60-секундні ходи, кутові слоти зброї, матриця 3×3 / 4×4 / 5×5.
- [RPGFan](https://www.rpgfan.com/review/knights-in-the-nightmare/) — рухливі класи, самоцвіти, речі з обʼєктів, злиття зброї.
- [Worthplaying (PSP)](http://worthplaying.com/article/2010/12/16/reviews/78899-psp-review-knights-in-the-nightmare/) — туман, graze, слот-машина, Vitality і Trans-Soul, PSP-керування.
- [Nintendo World Report](https://nintendoworldreport.com/review/19055) — раунди, рулетка, туторіали.
- YouTube: пошук «Knights in the Nightmare gameplay».

## Непевне
- (?) Dur зброї: JA — «кожен хід мінус 1», EN — витрачається за використання; тут записано «за використання».
- (?) Скільки ліній треба для перемоги — залежить від мапи; чи бувають вимоги «ворог певного типу» (NWR згадує).
- (?) Точні ціни часу за заряд і влучання, обсяг MP, радіус graze.
- (?) Чи бачить гравець наперед патерни куль і чи є `info: partial`.
- (?) Як саме рухаються Duelist і Lancer (на скільки клітин, чи коштує це час).
