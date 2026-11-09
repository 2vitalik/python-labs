---
title: Fallout 1–2 (покроковий бій)
slug: fallout-classic-combat
aka: [Fallout, Fallout 2, "Fallout: A Post Nuclear Role Playing Game", FO1, FO2, "Фоллаут"]
family: tactics
also: []
klass: avatar
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 1997
platforms: [DOS, Windows, Mac]
links:
  - {kind: wiki, url: "https://fallout.wiki/wiki/Fallout_combat", best: true, note: "сюрприз-хід, Sequence, AP, 1 AP за гекс, формули влучання і шкоди (DT, DR), прицільні постріли, черга-конус, крити і критичні промахи"}
  - {kind: wiki, url: "https://fallout.wiki/wiki/Crippled_limbs", note: "покалічені руки/ноги/очі: ефекти й лікування"}
  - {kind: wiki, url: "https://fallout.wiki/wiki/Action_Points", note: "макс. AP = 5 + Agility/2; перки на AP"}
  - {kind: other, url: "https://fodev.net/files/fo2/criticals.html", note: "таблиці критів Fallout 2: 9 зон і штрафи (голова −40, очі −60, ноги −20…), 6 рівнів крита, перевірка стату"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fallout_(video_game)", note: "SPECIAL, 18 навичок, перки, AP на дії й інвентар, дві зброї в руках, 150 днів водяного чипа"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Fallout+2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Fallout+2+combat", note: "пошук; бій"}
stage: v1
coverage: 55
mechanics: [hp-damage, projectile-shot, shoot-modes, shoot-burst, line-of-sight-attack, melee-vs-ranged, fog-of-war, inventory, inventory-items, inventory-limit, item-pickup, status-effects, unit-xp-skills, ai-opponent, realtime-ai, world-map, map-window, shop-window, save-multi-slot, difficulty-levels, time-out, player-death, message-log, hover-highlight, +action-points, +hit-chance, +body-part-targeting, +limb-disable, +critical-value, +critical-failure, +armor-absorb, +damage-threshold-resist, +friendly-fire, +realtime-to-turn-switch, +initiative-order, +surprise-attack, +hex-grid-render, +strength-requirement, +ai-companions]
proposes: ["+trigger:combat_start", "+trigger:attacked", "+cond:ap_left", "+cond:body_part", "+effect:spend_ap", "+effect:cripple", "+effect:knockdown", "+effect:critical", "+ui:ap-lights", "+ui:hit-chance", "+ui:body-part-picker", "+window:called-shot", "+window:character-sheet", "+window:pipboy", "+axis:time=hybrid-rt-turn"]
author: opus
date: 2026-11-09
---

# Fallout 1–2 — бій RPG на гексах: очки дії від спритності, прицільний постріл в очі чи ноги, крит за таблицею частини тіла

## Суть
Поза боєм — вільне дослідження в реальному часі на ізометричній (триметричній) мапі; бій вмикається атакою або ворожістю і стає **покроковим на гекс-сітці**. Гравець керує одним героєм; напарники ходять самі за AI. Кожен хід — запас **AP** (5 + Agility/2): 1 AP на гекс, близько 5 AP на постріл, AP коштують і інвентар, і перезарядка. Головна родзинка — **прицільні постріли** по 8 зонах тіла: штраф до влучання дорівнює бонусу до крита, а крит у ноги калічить (рух дорожчає), в очі — сліпить, у голову — часто вбиває. Тут описано лише бойову систему; квести, діалоги й карма — побіжно.

## Поле і час
- Локація — гекс-сітка, видима як триметрична проєкція; камера прокручується мишею; темні зони знижують влучання.
- Поза боєм: реальний час, NPC блукають; бій — **черга за Sequence** (вищий ходить раніше); перший хід — **сюрприз**: ходить той, хто напав, потім ціль, далі за правилами.
- Хід учасника — витрата AP у будь-якому порядку дій; лишок AP пропадає (?) або йде в AC.
- Огляд: бачиш лише в полі зору героя (Perception); за стінами — нічого.
- Світова мапа між локаціями — подорож у реальному часі з випадковими зустрічами (?); глобальний годинник: 150 днів на пошук водяного чипа (Fallout 1).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Vault Dweller / Chosen One) | player | SPECIAL 1–10 (сума ≤ 40), 18 навичок у %, HP, AP, AC, DT/DR за типами шкоди, Sequence, Critical Chance, перки, риси | ходить, стріляє, бʼє, користується інвентарем |
| Напарник (Ian, Tycho, Dogmeat, Katja…) | ally | як NPC | ходить сам за AI; черга може зачепити |
| Ворог (рейдер, мутант, тварина, робот) | enemy | HP, AC, DT/DR, зброя, навичка | атакує, тікає при малому HP (?) |
| Нейтральний NPC | neutral | — | стає ворогом, якщо зачепити |
| Вогнепальна зброя | pickup | шкода min–max, дальність, AP за режим, режими single/aimed/burst, обойма, вимога Strength | постріл з формулою влучання |
| Холодна зброя / кулаки | pickup | шкода + бонус Strength | swing/thrust; удар кулаком дешевший |
| Набої (JHP, AP тощо) | pickup | модифікатор шкоди DM і DR (у Fallout 1 не працює) | заряджають зброю |
| Броня | pickup | AC, DT і DR за типами | віднімає шкоду |
| Стимулятор / аптечка / Doctor's Bag | pickup | — | лікує HP / покалічення з навичкою Doctor |
| Стіна, двері, контейнер | static / gate / container | — | блокують огляд і рух; двері відчиняються |
| Темна зона | terrain | −10 % влучання далі 4 гексів | ніч і підземелля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(attack, a, b)` поза боєм або `custom: «ворог помітив і ворожий»` → ТО `custom: «бій: сюрприз-хід для нападника, далі черга за Sequence»`.
- КОЛИ `turn_start(u)` → ТО `counter(ap, =max)`, де max = 5 + Agility/2 (+ перки).
- КОЛИ `input(move, u, hex)` → ЯКЩО `path_exists(u, hex)` and `counter(ap, ≥, len)` → ТО `move(u, hex)`, `counter(ap, −1)` за гекс; ЯКЩО `state(u, crippled_leg)` → ТО `custom: «більше AP за гекс»`.
- КОЛИ `input(attack, u, t)` → ЯКЩО `counter(ap, ≥, cost)` (типово 5) and `line_of_sight(u, t)` → ТО `counter(ap, −cost)`; ЯКЩО `prob(bth)` → ТО `damage(t, n)`.
- Влучання впритул: `custom: «навичка зброї − AC цілі»`.
- Влучання на відстані: `custom: «(навичка − 30) + (PE − 2) × 8|16 − 4 × гекси − AC − 10 у темряві далі 4 гексів»`; кожна бракуюча одиниця Strength — ще −20; ЯКЩО `custom: «BTH ≤ 0»` → ТО `block` (постріл неможливий).
- Шкода: `custom: «(сира × DM − DT) − ⌊(DR + DRM) × (сира × DM − DT)⌋»` — спершу поріг DT, потім відсоток DR.
- КОЛИ `input(aimed, u, t, part)` → ЯКЩО `not custom: «зброя лише чергою або риса Fast Shot»` → ТО `custom: «штраф до влучання за зоною: голова −40, очі −60, пах −30, руки −30, ноги −20, торс 0»`, Critical Chance +той самий штраф, `counter(ap, −(cost+1))` (?).
- КОЛИ `prob(critical_chance)` після влучання → ТО `custom: «рівень крита = rng(1..100) + Better Criticals → таблиця зони (6 рівнів)»`: множник шкоди, `stun`/`custom: «збиття з ніг, нокаут, обхід броні, миттєва смерть»`.
- КОЛИ `custom: «рядок таблиці має перевірку стату»` → ЯКЩО `custom: «ціль провалила кидок Endurance / Agility / Luck»` → ТО `set_state(t, crippled_leg | crippled_arm | blinded)`.
- `state(crippled_arm)`: менша точність і шкода впритул, без дворучної зброї; обидві руки — лише кулаки · `state(blinded)`: точність різко ↓ усіма видами зброї.
- КОЛИ `input(burst, u, t)` → ЯКЩО `has(u, automatic)` → ТО `custom: «конус з N куль; кожна куля окремо влучає і може критнути, зачіпає напарників і нейтралів»`, більше AP і набоїв.
- КОЛИ `custom: «критичний промах»` (частіше з рисою Jinxed) → ТО `custom: «вдарив іншого / впустив зброю / заклинило / зброя зламалась / поранив себе»`.
- КОЛИ `input(inventory|reload|use, u)` → ТО `counter(ap, −cost)`; КОЛИ `input(swap_hand, u)` → ТО `custom: «перемкнути одну з двох активних зброї»`.
- КОЛИ `custom: «шкода ≥ поточних HP»` → ТО `disappear(t)` з анімацією смерті за типом удару (?); герой — `lose`.
- КОЛИ `custom: «ворожих у полі зору нема»` → ЯКЩО `input(end_combat)` → ТО `custom: «повернення в реальний час»`.
- КОЛИ `counter(day, >, 150)` → ЯКЩО `not has(hero, water_chip)` → ТО `lose` (Fallout 1).
- Перемога: сюжет (чип, Майстер, ГЕКК у FO2) · Поразка: смерть героя, ліміт днів (FO1) · Рахунок: досвід → рівень → навички й перк кожні 3 рівні.

## Керування і ввід
- Миша: курсор-рух (шестикутник під курсором і шлях) і курсор-приціл (ПКМ перемикає); клік по ворогу — атака поточним режимом зброї.
- Режим зброї — клік по слоту руки: single → aimed → burst / swing → thrust; aimed відкриває вікно зон тіла.
- Кнопки бою: End Turn, End Combat; перемикач рук; інвентар, навички (Skilldex), персонаж, Pip-Boy, мапа.
- Наведення на ціль показує шанс влучання (?), у вікні прицілу — % по кожній зоні.

## Вікна, меню, HUD
- `main-menu`: New Game → `character-select` (готові герої або створення), Load Game, Options, Credits, Exit.
- `+window:character-sheet` — SPECIAL, навички з тегами, риси, перки, HP/AC/DT/DR.
- `game-screen`: ізометрична мапа; нижня панель — `message-log` подій бою, `hp-bar` числом, AC, `+ui:ap-lights` (лампочки AP), два слоти рук з режимом і AP-ціною, кнопки End Turn / End Combat.
- `+window:called-shot` (`+ui:body-part-picker`): силует цілі, 8 зон і `+ui:hit-chance` для кожної.
- `inventory-window` — рюкзак, руки, броня; `custom-window` бартеру (`shop-window`) з торговцями.
- `+window:pipboy` — квести, нотатки, час, будильник.
- `map-window` — світова мапа з подорожжю; `dialogue-window` з «talking heads».
- `pause-menu`/`settings-window`: складність бою, швидкість, насильство, автосейв; `save-slots`.

## Фічі поза полем
- Прогресія: досвід → рівень → очки навичок; перк кожні 3 рівні (кожні 4 з рисою Skilled); 48 перків з вимогами.
- Карма/репутація відкриває або закриває гілки і кінцівки.
- `difficulty-presets` — окремо гри і бою (?); `save-slots`; час з будильником (Pip-Boy).
- Fallout 2: керування поведінкою напарника через діалог (дистанція, черга, тікати при HP) (?).

## Варіації й родичі
- Наступники з цією системою: Fallout 2 (1998), Fallout Tactics (2001, загін, режими ходу), Wasteland 2/3, Underrail, ATOM RPG.
- Fallout 3+ — V.A.T.S.: пауза з прицілом по частинах тіла як нащадок called shot.
- Родичі в корпусі: [Jagged Alliance 2](jagged-alliance-2.md) (AP, real-time ↔ turn, частини тіла), [Silent Storm](silent-storm.md), [Laser Squad](laser-squad.md).
- **Осі варіацій**: актор — один герой + AI-напарники (Fallout) / загін (Fallout Tactics, JA2) · приціл — 8 зон зі штрафом-бонусом до крита (Fallout) / 3 зони (JA2) / вільне прицілювання (Phoenix Point) · шкода — DT-поріг + DR-% / лише броня-відсоток.

## Цікавинки для курсу
- AP від стату + ціни дій і інвентаря в AP — 🌱.
- Штраф до влучання = бонус до крита за зоною тіла — 📎 (рівновага ризику).
- Таблиця критів: зона × рівень (rng + бонус) → множник, прапори ефектів, перевірка стату — 🥉 (табличний движок ефектів).
- DT/DR: поріг, потім відсоток — 🌱.
- Черга-конус, де кожна куля влучає окремо і може вбити напарника — 📎.
- Перемикання real-time ↔ покроковий бій з чергою Sequence і сюрприз-ходом — 🥉.
- Глобальний ліміт днів (150) над усією грою — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `projectile-shot` · `shoot-modes` ↔ single/aimed/burst · `shoot-burst` · `line-of-sight-attack` · `melee-vs-ranged` · `fog-of-war` ↔ поле зору · `inventory*` · `item-pickup` · `status-effects` ↔ покалічення, отрута, радіація · `unit-xp-skills` ↔ рівні й перки · `ai-opponent` / `realtime-ai` · `world-map` / `map-window` · `shop-window` ↔ бартер · `save-multi-slot` · `difficulty-levels` · `time-out` ↔ 150 днів · `player-death` · `message-log` · `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+action-points`, `+hit-chance`, `+body-part-targeting`, `+limb-disable`, `+critical-value`, `+armor-absorb`, `+friendly-fire`, `+realtime-to-turn-switch`, `+initiative-order`, `+surprise-attack`, `+hex-grid-render` — уже в корпусі.
  - `+critical-failure` «Критичний промах: заклинило, впустив, влучив у себе» · entities/combat · 🌱.
  - `+damage-threshold-resist` «Броня: поріг DT, потім відсоток DR» · entities/combat · 🌱.
  - `+strength-requirement` «Брак Strength — штраф до влучання» · entities/state · 🌱.
  - `+ai-companions` «Напарники ходять самі за правилами поведінки» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+trigger:combat_start` — перехід з реального часу в бій; `+trigger:attacked` — ціль атакована.
- `+cond:ap_left` — лишилось AP; `+cond:body_part` — обрана зона тіла.
- `+effect:spend_ap` — списати AP; `+effect:cripple` — покалічити кінцівку/очі; `+effect:knockdown` — збити з ніг; `+effect:critical` — застосувати рядок таблиці критів.
- `+ui:ap-lights` — лампочки AP; `+ui:hit-chance`; `+ui:body-part-picker` — силует з зонами.
- `+window:called-shot` — вікно прицільного пострілу; `+window:character-sheet`; `+window:pipboy` — журнал/годинник/мапа.
- `+axis:time=hybrid-rt-turn` — реальний час поза боєм, покроковий у бою.

## Джерела
- ⭐ [Fallout Wiki: Fallout combat](https://fallout.wiki/wiki/Fallout_combat) — сюрприз-хід, Sequence, 1 AP/гекс, 5 AP атака, формули BTH і шкоди, Strength −20 %, черга, прицільні постріли, крити й критичні промахи.
- [Fallout Wiki: Crippled limbs](https://fallout.wiki/wiki/Crippled_limbs) — руки, ноги, очі; лікування навичкою Doctor.
- [Fallout Wiki: Action Points](https://fallout.wiki/wiki/Action_Points) — 5 + Agility/2.
- [Critical Hit Tables (fodev)](https://fodev.net/files/fo2/criticals.html) — 9 зон і штрафи, 6 рівнів, Better Criticals, прапори ефектів, перевірки Endurance/Agility/Luck.
- [Wikipedia: Fallout](https://en.wikipedia.org/wiki/Fallout_(video_game)) — SPECIAL, 18 навичок, 16 рис, 48 перків, AP на інвентар і перезарядку, дві зброї, 150 днів.
- Steam: пошук «Fallout 2»; YouTube: пошук «Fallout 2 combat».

## Непевне
- (?) Додаткова ціна AP прицільного пострілу (+1?) і точні ціни AP інвентаря/перезарядки (2?).
- (?) Чи невитрачені AP додаються до AC до наступного ходу — відомо з памʼяті, у відкритих джерелах не бачив.
- (?) Формула Sequence (2 × Perception?) і Critical Chance (= Luck %?).
- (?) Штрафи зон взято з таблиць Fallout 2; у Fallout 1 можуть відрізнятися.
- (?) Умова завершення бою (кнопка End Combat, якщо ворогів поруч нема) — з памʼяті.
- (?) Випадкові зустрічі на світовій мапі й налаштування поведінки напарників у FO2 — джерела цього не описують.
