---
title: Specter Ops
slug: specter-ops
aka: []
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: state
year: 2015
platforms: [board (Plaid Hat Games)]
links:
  - {kind: other, url: "https://rulespal.com/specter-ops/rulebook", best: true, note: "правила: прихований рух на листі, бачення по рядку й стовпцю, last seen, атака кубиком, авто, сенсор руху, 40 раундів, варіанти на 4 і 5"}
  - {kind: other, url: "https://www.analog.games/gameItem/show/419cd83f9659632e0196596a80d6029f/specter-ops?lang=en", note: "картка гри: Specter Ops (2015)"}
  - {kind: other, url: "https://gamingtrend.com/reviews/one-mans-espionage-agent-anothers-freedom-fighter-specter-ops-review", note: "огляд"}
  - {kind: other, url: "https://tabletopgaming.co.uk/reviews/specter-ops-broken-covenant-review", note: "огляд самостійного продовження Broken Covenant (2018)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Specter+Ops+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [move-8dir, impassable-cells, hp-damage, status-effects, inventory-items, collect-quota, reach-exit, time-out, hot-seat, turn-enforcement, character-select, match-setup, pass-device, objective-text, game-screen, end-screen, +hidden-movement, +team-vs-one, +rook-line-vision, +last-seen-marker, +motion-sensor-direction, +attack-roll-vs-distance, +road-vehicle, +equipment-charges, +objectives-then-escape, +secret-traitor, +belief-set-tracking]
proposes: ["+effect:secret_move", "+effect:roll_dice", "+effect:place_marker", "+cond:visible_rowcol", "+cond:moved_at_least", "+ui:movement-sheet", "+ui:last-seen-token", "+ui:round-track", "+window:movement-sheet", "+card:rook-line-vision", "+card:last-seen-marker", "+card:motion-sensor-direction", "+card:attack-roll-vs-distance", "+card:road-vehicle", "+card:equipment-charges", "+card:objectives-then-escape", "+card:secret-traitor"]
author: opus
date: 2026-11-09
---

# Specter Ops — агент таємно крадеться координатною сіткою бази, а мисливці бачать лише вздовж свого рядка й стовпця до першої будівлі

## Суть
Один гравець — агент A.R.K., який записує свій маршрут на секретному листі; решта — мисливці корпорації Raxxon. Агентові треба виконати 3 з 4 місій і втекти через точку евакуації до кінця 40-го раунду; мисливці виграють, якщо зведуть його HP до 0 або час вийде. Ключова механіка видимості — **«як тура»**: мисливець бачить свій рядок і стовпець до будівлі; агент, що опинився в полі зору, ставить фігурку на дошку, а якщо лише проскочив повз — лишає жетон «last seen». `klass: hybrid`: агент — **avatar** з прихованою позицією, мисливці — **figure** (команда фігур із різними здібностями).

## Поле і час
- Квадратна сітка з координатами літера × число (A1… W3, K23); клітини без координат — будівлі (structures), непрохідні й непрозорі.
- Дороги — координати біля пунктирних ліній; ними їздить авто мисливців, вздовж них мисливець бачить далі.
- Раунд: хід агента, потім кожен гравець-мисливець у вибраному ними порядку; ліміт — 40 раундів.
- Позиція агента — лише на його листі; на дошці — фігурка, коли видно, або жетон last seen.
- Перевірка видимості — лише наприкінці руху кожного мисливця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент (Spider, Cobra, Orangutan, Blue Jay) | player | 4 HP (більшість), здібність, 3 картки спорядження | таємно рухається до 4 клітин (ортогонально/діагонально), не крізь мисливців і будівлі; виконує місії, тікає |
| Мисливець (The Prophet, The Beast, The Gun, The Puppet) | enemy | здібності (The Beast — рух 5; The Gun — 2 кубики атаки…) | рух до 4 клітин; бачить по рядку й стовпцю; атакує видимого агента |
| Будівля | static | без координат | непрохідна, блокує бачення |
| Дорога | terrain | клітини біля пунктиру | авто їздить лише нею; мисливець на дорозі бачить уздовж ділянки |
| Авто | platform | до 10 клітин за раунд, старт K17 | везе мисливців; не блокує бачення; у ньому не можна атакувати й бути оглушеним; замість руху — сенсор руху |
| Місія (жетон) | zone | 4 на дошці, синій/червоний бік | агент, що почав хід поруч (8 сусідів), може виконати → червоний бік |
| Точка евакуації | zone | стрілки біля A3, N1, W3 (+H1 у грі на 4–5) | після 3 місій — завершити рух тут; мисливець на ній блокує |
| Жетон last seen | mark | одна позиція | остання видима клітина агента, коли той сховався |
| Картка спорядження | resource | заряди; розкрита / таємна | 1 за хід до або після руху (Tangle Line, Holo Decoy, Flash Bang, Smoke Grenade…) |
| Жетон оглушення | mark | до кінця ходу мисливця | оглушений не атакує й ходить ≤2 |
| Лист руху агента | zone | рядок на раунд | координата зупинки + ініціали спорядження, HP, обрані місії |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «агент кидає кубик на кожну з 4 місій і обводить їх»`, `place(mission_token)`; авто на K17 з мисливцями; агент таємно на N1.
- КОЛИ `input(move, agent, to)` → ЯКЩО `custom: «≤4 клітин ортогонально/діагонально»` і `custom: «не крізь мисливців і будівлі»` → ТО `custom: «записати to на лист»` (прихований хід).
- КОЛИ `input(move, agent)` → ЯКЩО `custom: «кінець руху у полі зору мисливця»` → ТО `reveal(agent)` (фігурка на дошку).
- КОЛИ `input(move, agent)` → ЯКЩО `custom: «проходив видимими клітинами, але закінчив поза зором» або «стартував видимим і пішов»` → ТО `custom: «last seen + фігурка на останню видиму клітину»`.
- КОЛИ `turn_end(hunter)` → ЯКЩО `line_of_sight(hunter, agent)` (рядок / стовпець до будівлі; на дорозі — уздовж ділянки) → ТО `reveal(agent)`; інакше агент каже «clear».
- КОЛИ `input(attack, hunter)` → ЯКЩО `line_of_sight(hunter, agent)` → ТО `custom: «кидок ≥ відстані — влучання; 1 — промах завжди; 6 — докинути й додати»`, `damage(agent, 1)`; на одній клітині — автоматичне влучання.
- КОЛИ `hp_zero(agent)` → ТО `lose` (агент), `win` (мисливці).
- КОЛИ `turn_start(agent)` → ЯКЩО `adjacent(agent, mission)` (8 сусідів) → ТО `set_state(mission, done)`.
- КОЛИ `enter(agent, escape_point)` → ЯКЩО `counter(missions_done, >=, 3)` і `custom: «на точці нема мисливця»` → ТО `win` (агент).
- КОЛИ `counter(round, >, 40)` → ТО `win` (мисливці).
- КОЛИ `input(drive, hunter_in_car)` → ЯКЩО `custom: «лише дорогою, ≤10 за раунд»` → ТО `move(car, to)`; посадка/висадка завершує рух мисливця.
- КОЛИ `input(sensor, hunter_in_car)` → ЯКЩО `custom: «агент минулого ходу пройшов ≥3»` → ТО `custom: «агент оголошує напрям компаса»`; інакше «no motion»; сенсор і рух авто — не в одному раунді.
- КОЛИ `input(equipment, card)` → ЯКЩО `has(agent, charge)` → ТО ефект картки, `custom: «ініціали на лист»`; Tangle Line: `stun(hunter, 1)` на кидку ≥ відстані; Holo Decoy: `custom: «фальшивий last seen у межах 4 клітин»`.
- КОЛИ `custom: «мисливець закінчив рух на Cobra / поруч ортогонально»` → ТО `stun(hunter, 1)` (поруч — на 4+).
- Варіант на 5: `custom: «таємний зрадник серед мисливців не мусить показувати агента у своєму полі зору»`; викритий → `set_side(traitor, ark)`, 4 HP (6 за Orangutan), 2 картки.
- Перемога агента: 3 місії + евакуація до кінця 40-го раунду · Перемога мисливців: HP агента 0 або час · Рахунок: нема.

## Керування і ввід
- Агент: пише координату зупинки на лист (прикриває від інших), за потреби — ініціали спорядження; ставить фігурку / last seen за правилами; оголошує «clear».
- Мисливці: радяться, у якому порядку ходити; рух фігури або авто; атака кубиком; сенсор.
- Цифрова версія (нема офіційної): клік по клітині для руху з підсвіткою досяжних, `pass-device` для агента, автоматичний розрахунок видимості.

## Вікна, меню, HUD
- `match-setup` (цифрова версія): кількість гравців 2–5, варіант (місії відкриті / таємні, зрадник).
- `character-select`: агент (Spider, Cobra, Orangutan, Blue Jay) + 3 картки спорядження; мисливці (The Prophet, The Beast, The Gun, The Puppet).
- `game-screen`: сітка з координатами, будівлі, дороги, авто, місії, точки евакуації; `movement-sheet` агента (лише для нього); `last-seen-token`; `round-track` до 40; HP агента; `objective-text` (місії виконано 0–3).
- `pass-device` (цифрова версія) — між ходом агента й мисливців.
- `end-screen`: переможець + повний маршрут агента з листа (цифрова версія).

## Фічі поза полем
- `custom-rules`: гра на 2–3 (місії відкриті), на 4 (місії таємні, 3 мисливці, +2 HP і 5 карток агенту, додаткова евакуація H1), на 5 (таємний зрадник, голосування за позбавлення доступу до авто).
- Асиметричні персонажі з унікальними картками (працюють лише для власника).
- Продовження Specter Ops: Broken Covenant (2018) — самостійна гра (за оглядом Tabletop Gaming).

## Варіації й родичі
- [Scotland Yard](scotland-yard.md) — прихований рух на графі з розкладом появ; тут — сітка й видимість за геометрією.
- [Fury of Dracula](fury-of-dracula.md) — прихований слід і пастки; [Mr. Jack](mr-jack.md) — видимість від ліхтарів; [Captain Sonar](captain-sonar.md) — виведення маршруту з оголошень; [Stop Thief](stop-thief.md) — прихований втікач без людини-супротивника.
- **Осі варіацій**: що видно між появами «нічого / last seen / тип транспорту»; бачення «радіус (fog of war) / рядок-стовпець до перешкоди / ліхтарі»; ціль втікача «вижити N раундів / виконати місії й утекти»; команда «чесна / з таємним зрадником»; сенсори «нема / напрям руху / близькість».

## Цікавинки для курсу
- Бачення «як тура» до першої будівлі + продовження вздовж дороги — 📎.
- Прихований рух з листом і правило last seen (остання видима клітина на шляху) — 🥉: треба трасувати весь шлях, а не лише кінець.
- Атака кубиком проти відстані з вибуховою шісткою — 🌱.
- Сенсор руху: напрям, якщо пройдено ≥3 — 🌱.
- Множина можливих позицій агента з урахуванням «clear» від кожного мисливця — 🥈.
- AI-агент, що мінімізує видимість і максимізує невизначеність — 🥇.
- Таємний зрадник і умова його викриття — 📎.

## Мапа на каталог
- Є: `move-8dir` ↔ рух на 4 клітини з діагоналями; `impassable-cells` ↔ будівлі; `hp-damage` ↔ HP агента; `status-effects` ↔ оглушення; `inventory-items` ↔ спорядження; `collect-quota` ↔ 3 з 4 місій; `reach-exit` ↔ евакуація; `time-out` ↔ 40 раундів; `hot-seat` + `turn-enforcement` ↔ черга агент → мисливці; `character-select` + `match-setup` ↔ вибір персонажів і варіанту; `pass-device` ↔ прихований хід за одним екраном; `objective-text`; `game-screen` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+hidden-movement`, `+team-vs-one`, `+belief-set-tracking` (Scotland Yard).
  - `+rook-line-vision` «Бачення по рядку й стовпцю до перешкоди» · interface/render · 📎.
  - `+last-seen-marker` «Жетон останньої видимої позиції на шляху» · game-logic/info · 🥉.
  - `+motion-sensor-direction` «Сенсор: напрям, якщо ціль пройшла ≥N» · game-logic/info · 🌱.
  - `+attack-roll-vs-distance` «Влучання, якщо кидок ≥ відстані» · entities/combat · 🌱.
  - `+road-vehicle` «Спільний транспорт лише по дорогах, везе фігури» · entities/move · 📎.
  - `+equipment-charges` «Спорядження із зарядами, розкрите або таємне» · entities/state · 🌱.
  - `+objectives-then-escape` «Виконати K з N місій, потім дійти до виходу» · game-logic/win · 🌱.
  - `+secret-traitor` «Таємний зрадник у команді» · game-logic/players · 📎.

## Пропозиції до словників
- `+effect:secret_move` — прихований рух (запис на лист).
- `+effect:roll_dice` — кидок кубика як частина ефекту (атака, оглушення).
- `+effect:place_marker` — поставити жетон-позначку позиції (last seen).
- `+cond:visible_rowcol` — ціль на рядку/стовпці без будівель між.
- `+cond:moved_at_least` — сутність минулого ходу пройшла ≥N клітин.
- `+ui:movement-sheet` — секретний лист маршруту.
- `+ui:last-seen-token` — жетон останньої видимої позиції.
- `+ui:round-track` — лічильник раундів до ліміту.
- `+window:movement-sheet` — лист агента на весь екран (цифрова версія).

## Джерела
- ⭐ [RulesPal: Specter Ops](https://rulespal.com/specter-ops/rulebook) — сетап на 2–3, рух агента й мисливців, лист, last seen, бачення, атака, оглушення, авто й сенсор, спорядження, місії, евакуація, 40 раундів, варіанти на 4 і 5.
- [analog.games: Specter Ops (2015)](https://www.analog.games/gameItem/show/419cd83f9659632e0196596a80d6029f/specter-ops?lang=en) — рік.
- [Gaming Trend: огляд](https://gamingtrend.com/reviews/one-mans-espionage-agent-anothers-freedom-fighter-specter-ops-review), [Tabletop Gaming: Broken Covenant](https://tabletopgaming.co.uk/reviews/specter-ops-broken-covenant-review).
- YouTube: пошук «Specter Ops board game how to play».

## Непевне
- (?) Розмір дошки: координати в правилах доходять до W і 23 — сітка щонайменше A–W × 1–23; точно не перевірено.
- (?) Здібності The Prophet, The Puppet, Spider (крім Tangle Line), Orangutan і ефекти Flash Bang, Adrenal Surge, Smoke Grenade, Stealth Field — у переказі правил не описані.
- (?) Enhanced Senses The Beast («близько», якщо агент у межах 4 після короткого руху) — формулювання переказу неоднозначне.
- (?) Дизайнер Emerson Matsuuchi, видавці Plaid Hat Games / Nazca Games — за пошуковою видачею, не з правил.
- (?) Що саме змінює Broken Covenant — не перевіряв.
