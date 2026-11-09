---
title: Tapper
slug: tapper
aka: [Root Beer Tapper]
family: maze-arcade
also: [tower-lanes]
klass: avatar
axes:
  field: 1d
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1983
platforms: [arcade, Atari 2600, Atari 8-bit, ColecoVision, C64, Apple II, ZX Spectrum, MSX, IBM PC, Amstrad CPC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tapper_(video_game)", best: true, note: "керування, 4 стійки, відкидання клієнтів, 3 способи втратити життя, чайові й танцівниці, бонус з банками, 4 рівні, Root Beer Tapper"}
  - {kind: other, url: "https://www.arcade-history.com/game/2834/", note: "очки аркади (50/75/100/150, кухоль 100, чайові 1500, бонус 3000), поради, attract-пасхалка"}
  - {kind: other, url: "https://www.pixelatedarcade.com/games/tapper/documents/instruction-manual/782/", note: "мануал домашньої версії: очки, бонусні життя, 4 складності, Soda Bandit"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tapper+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-by-input, wrap-edges, projectile-shot, enemy-reached-base, player-death, spawn-points, progress-acceleration, item-pickup, temporary-modes, event-points, extra-life-threshold, sequential-levels, difficulty-levels, score-records, attract-demo, hot-seat, +lane-serve-pushback, +catch-return, +hold-to-charge, +distraction-show, +shell-game-bonus, +loop-harder]
proposes: ["+axis:field=lanes", "+role:lane", "+cond:lane_has", "+effect:knockback", "+effect:catch", "+card:lane-serve-pushback", "+card:catch-return", "+card:shell-game-bonus", "+card:distraction-show", "+window:bonus-round"]
author: opus
date: 2026-11-09
---

# Tapper — бармен на чотирьох стійках: кухлі ковзають до клієнтів, порожні летять назад, і жоден не має впасти

## Суть
Чотири барні стійки — чотири смуги. Клієнти заходять з дверей і сунуть до кранів; бармен наливає кухоль і пускає його по стійці назустріч. Кухоль відкидає клієнта: біля дверей той виходить, інакше пʼє й пускає порожній кухоль назад, який треба зловити. Програти можна трьома способами — клієнт дійшов до крана, повний кухоль злетів у дверях, порожній розбився біля крана. Межова гра сімʼї: замість лабіринту — смуги з потоком в обидва боки, близько до tower defense.

## Поле і час
- 4 горизонтальні стійки одна над одною; на одному кінці кожної — кран, на іншому — двері. Бармен або біжить уздовж своєї стійки, або перестрибує до крана сусідньої (з обгортанням зверху вниз).
- На стійці одночасно до 4 клієнтів, кілька кухлів у обидва боки.
- Real-time. Рівень = 2–4 екрани; що довше на рівні, то швидші клієнти й кухлі. Після 4-го рівня гра починається знову, складніше.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бармен | player | 3 або 5 життів (дом. версія, за складністю) | біг уздовж стійки; перехід до крана сусідньої; наливає й пускає кухоль |
| Стійка ×4 | zone | до 4 клієнтів | смуга від дверей до крана |
| Кран | static | на кінці кожної стійки | тут наливають; сюди ж летять порожні кухлі |
| Двері | spawner | на дальньому кінці | звідси заходять клієнти |
| Клієнт | enemy | тип за рівнем: ковбой / спортсмен / панк / прибулець | сунеться до крана; ловить кухоль і відкочується; пʼє й повертає порожній |
| Повний кухоль | projectile | — | ковзає від крана до дверей |
| Порожній кухоль | projectile | — | ковзає назад до крана; треба зловити |
| Чайові | pickup | — | інколи лишаються на стійці; останній клієнт у ряду майже завжди лишає |
| Танцівниці | neutral | кілька секунд | відволікають частину клієнтів — ті стоять |
| Банка ×6 (бонус) | object | 5 струшених, 1 ні | вибір після перемішування |
| Тип у масці (Soda Bandit) | neutral | — | струшує 5 банок і тасує їх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ТО `move(bartender, dir)` уздовж стійки.
- КОЛИ `input(up|down)` → ТО `teleport(bartender, keg_of_next_bar)`; з крайньої стійки — `wrap(bartender)`.
- КОЛИ `input(tap_hold)` → ТО `custom: «бармен біжить до крана й наливає; доки кухоль не повний — стоїть»`.
- КОЛИ `input(tap_release)` → ЯКЩО `custom: «кухоль повний»` → ТО `spawn(full_mug)` — ковзає до дверей.
- КОЛИ `tick` → ЯКЩО `not state(customer, distracted)` → ТО `move(customer, to_keg)`.
- КОЛИ `contact(full_mug, customer)` → ТО `disappear(full_mug)`, `custom: «клієнт відкочується до дверей»` — `+effect:knockback`.
- КОЛИ `custom: «відкат завершився»` → ЯКЩО `custom: «клієнт дістав дверей»` → ТО `disappear(customer)`, `score(50|75|100|150)` за типом; інакше `spawn(empty_mug)` назад до крана, клієнт знову сунеться.
- КОЛИ `contact(bartender, empty_mug)` → ТО `pickup`, `score(100)`.
- КОЛИ `reach(empty_mug, keg_end)` → ТО `lives(-1)` — кухоль розбився.
- КОЛИ `reach(full_mug, door_end)` → ТО `lives(-1)` — нікого не зустрів і розбився.
- КОЛИ `reach(customer, keg_end)` → ТО `lives(-1)` — клієнт хапає бармена й пускає його стійкою за двері.
- КОЛИ `rng(p)` → ТО `spawn(tip)` на стійці.
- КОЛИ `contact(bartender, tip)` → ТО `score(1500)`, `spawn(dancers)`, `set_state(customers, distracted, dur)` — ЯКЩО `state(customer, drinking|pushed_back)` → не діє.
- КОЛИ `all_gone(customer)` → ТО `score(1000)` (дом. версія), `custom: «бармен пʼє свій кухоль — комічна сценка»`, наступний екран.
- КОЛИ `level_end` → ТО `window(bonus-round)`: `custom: «5 з 6 банок струшено, банки перемішано»`.
- КОЛИ `input(pick_can)` → ЯКЩО `custom: «банка не струшена»` → ТО `score(3000)`; інакше `custom: «бризк в обличчя»`, `reveal(unshaken_can)`.
- КОЛИ `timer(n)` → ТО `speed(customers, +n)`, `speed(mugs, +n)` — затягувати рівень дедалі небезпечніше.
- КОЛИ `level_start` → ТО `custom: «клієнти частіші, швидші, відкат коротший»`.
- КОЛИ `counter(score, >=, 20000|+50000)` → ТО `lives(+1)` (дом. версія).
- Перемога екрана: усі клієнти вийшли. · Поразка: три способи вище, життя скінчились. · Рахунок: клієнт за двері 50–150 за типом, зловлений порожній кухоль 100, чайові 1500, бонус 3000; порада: клієнт, що випив, дає 100 за порожній кухоль замість 50 за вихід.

## Керування і ввід
- Аркада: 4-позиційний джойстик і кран-ручка (дві ручки на корпусі — на двох гравців (?)). Тягнеш ручку — бармен біжить до крана й наливає; відпускаєш — кухоль іде по стійці.
- Утримання ручки = час наливу: поки кухоль не повний, бармен стоїть (вхід із зарядом).
- Домашні версії: джойстик + кнопка дії; перемикач кількості гравців (1/2) і складності.

## Вікна, меню, HUD
- `attract-demo`: слово «Tapper» наповнюється пивом; пасхалка з іменами авторів.
- `game-screen`: 4 стійки з дверима й кранами; HUD — `score`, `lives` (?).
- Сценка між екранами (бармен пʼє свій кухоль) — `custom-window`.
- `custom-window` → `+window:bonus-round`: 6 банок на стійці, тасування, вибір.
- `difficulty-select` (дом. версія): Beginner / Intermediate / Arcade / Expert.
- Переходи: attract → game-screen → (екран очищено) сценка → наступний екран → (рівень закінчено) bonus-round → новий рівень; після 4-го — знову перший, складніше.

## Фічі поза полем
- `levels-sequential`: салун (2 екрани) → спорт-бар (3) → панк-бар (4) → космобар (4), далі цикл з вищою складністю.
- `difficulty-presets` (дом.): 3 або 5 життів × повільні або швидкі клієнти.
- `hotseat`: два гравці по черзі.
- Root Beer Tapper — переодягнення без алкоголю; механіка та сама.

## Варіації й родичі
- Root Beer Tapper (1984): містер-содовщик і рутбір замість пива; домашні версії — переважно під цією назвою.
- Корпус-кабінет у вигляді бару: латунна підставка для ніг, ручки-крани (у пивній версії — бренд Budweiser).
- Родичі: [`domino-man`](domino-man.md) (схожий герой від Bally Midway), [`plants-vs-zombies`](../tower-lanes/plants-vs-zombies.md) (смуги, вороги йдуть до бази), [`zoop`](../falling-match/zoop.md) (стрілок пускає постріл уздовж смуги, ряди повзуть назустріч).
- Осі варіацій «смуга і снаряд»: снаряд знищує (PvZ) / відкидає й повертається порожнім (Tapper) / міняє колір (Zoop). Вісь «хто програє на смузі»: ворог дійшов до бази / твій снаряд пролетів мимо / твій снаряд не зловили на поверненні — у Tapper усі три.

## Цікавинки для курсу
- Двосторонній потік на одній смузі: повні кухлі туди, порожні назад, зловити або втратити — 🥉.
- Відкидання з порогом «дістав дверей → вийшов, інакше пʼє» — 📎.
- Утримання кнопки як час наливу: заряджений ввід, під час якого аватар стоїть — 🌱.
- Чайові → тимчасовий стан «відволікся» для частини ворогів, крім тих, що пʼють або відкочуються — 📎.
- Бонус-раунд «шулерські банки»: анімація тасування, пошук однієї правильної — 📎.
- 4 смуги з телепортом бармена між кранами й обгортанням — 🌱.

## Мапа на каталог
- Є: `move-by-input` ↔ біг і перехід між стійками; `wrap-edges` ↔ обгортання зверху вниз; `projectile-shot` ↔ кухоль; `enemy-reached-base` ↔ клієнт дійшов до крана; `player-death` ↔ 3 способи; `spawn-points` ↔ двері; `progress-acceleration` ↔ швидше з часом і рівнем; `item-pickup` + `temporary-modes` ↔ чайові й танцівниці; `event-points` ↔ таблиця очок; `extra-life-threshold` ↔ 20k/+50k; `sequential-levels` ↔ 4 бари; `difficulty-levels` ↔ 4 складності; `score-records`; `attract-demo` ↔ «Tapper» наливається; `hot-seat` ↔ 2 гравці по черзі.
- **Нема** → пропозиції карток:
  - `+lane-serve-pushback` «Снаряд відкидає ворога по смузі» · entities/combat · 📎 · слот {push_dist}.
  - `+catch-return` «Повернутий снаряд треба зловити» · entities/interact · 📎 — не зловив = поразка.
  - `+hold-to-charge` «Утримання = заряд дії» · interface/input · 🌱.
  - `+distraction-show` «Відволікання частини ворогів» · entities/state · 📎.
  - `+shell-game-bonus` «Бонус: знайди одну серед перемішаних» · game-logic/score · 📎.
  - `+loop-harder` «Після останнього рівня — знову з початку, складніше» · levels/progression · 🌱.

## Пропозиції до словників
- `+axis:field=lanes` — паралельні смуги з переходом між ними (уже ×2: Clash Royale, Swords & Soldiers).
- `+role:lane` — смуга як сутність поля з власною чергою (уже ×9 🔥).
- `+cond:lane_has` — на смузі є сутність виду (уже ×5 🔥).
- `+effect:knockback` — відкидання на N уздовж смуги.
- `+effect:catch` — гравець ловить снаряд, що летить до нього (уже пропонував Klax).
- `+card:lane-serve-pushback`, `+card:catch-return`, `+card:shell-game-bonus`, `+card:distraction-show` — див. вище.
- `+window:bonus-round` — бонус-раунд між рівнями (уже ×4 🔥).

## Джерела
- ⭐ [Wikipedia: Tapper](https://en.wikipedia.org/wiki/Tapper_(video_game)) — джойстик і кран, 4 стійки з обгортанням, відкидання клієнтів, 3 способи втратити життя, чайові й танцівниці, бонус з банками, 4 рівні й цикл, Root Beer Tapper.
- [Arcade-History: Tapper](https://www.arcade-history.com/game/2834/) — очки аркади, поради (останній клієнт лишає чайові; що довше — то швидше), attract-пасхалка, корпус.
- [Pixelated Arcade: мануал](https://www.pixelatedarcade.com/games/tapper/documents/instruction-manual/782/) — домашня версія: очки, 1000 за екран, бонусні життя 20k/+50k, складності Beginner…Expert, Soda Bandit.
- YouTube: пошук «Tapper arcade gameplay».

## Непевне
- (?) Мануал з Pixelated Arcade описує домашню версію (кнопка, Soda Bandit, перемикачі складності) — значення 1000 за екран і пороги життів можуть відрізнятися від аркади.
- (?) З якого боку кран, а з якого двері, і чи бармен може налити не біля крана — описано за Wikipedia («біжить до крана»).
- (?) Дві ручки-крани на корпусі — для двох гравців чи одна для обох рук; HUD (рахунок, життя) — не перевірено.
- (?) Імовірність появи чайових і тривалість танцю — без чисел.
