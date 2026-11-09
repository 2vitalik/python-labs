---
title: "Hoshigami: Ruining Blue Earth"
slug: hoshigami
aka: [Hoshigami, ホシガミ 沈みゆく蒼き大地, "Hoshigami: Ruining Blue Earth Remix"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2001
platforms: [PS1, DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hoshigami:_Ruining_Blue_Earth", best: true, note: "RAP-шкала 0→100 %, Shoot штовхає на 2 клітини, Session і фасинг, монети Coinfeigm, шість богів"}
  - {kind: other, url: "https://www.rpgfan.com/review/hoshigami-ruining-blue-earth/", note: "огляд PS1: Defend vs Session, монета 20/40, 100 очок відданості → навичка, Tower of Trial, смерть остаточна"}
  - {kind: other, url: "https://www.rpgfan.com/review/hoshigami-ruining-blue-earth-remix/", note: "огляд DS Remix: складності, гравіювання печаток, до 4 монет, поворот мапи на 90°"}
  - {kind: other, url: "https://ps2.psillustrated.com/gamevortex/soft_rev.php/310", note: "огляд: Shoot відкидає на кілька клітин, сесії, крадіжка предметів, печатки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hoshigami+Ruining+Blue+Earth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [hp-damage, ai-opponent, impassable-cells, permadeath, unit-xp-skills, inventory-items, shop-between-levels, difficulty-levels, game-screen, +action-points, +initiative-order, +knockback, +session-relay, +facing-redirect, +combo-steal, +spell-coins, +seal-engrave, +deity-devotion, +elemental-resistance, +training-tower, +camera-rotate]
proposes: ["+effect:knockback", "+effect:delay_turn", "+trigger:collide", "+ui:turn-order-bar", "+ui:rap-gauge", "+window:temple", "+axis:turn-structure=time-track"]
author: opus
date: 2026-11-09
---

# Hoshigami — покрокова тактика, де постріл відкидає ворога на 2 клітини, а союзник у «сесії» відбиває його далі у свій бік

## Суть
Тактика на квадратній 3D-сітці (PS1): черговість ходів задає **RAP-шкала** кожного персонажа — дії її наповнюють, і що більше витратив, то пізніше ходиш знову. Головна незвичність — **Shoot**: слабкий удар, що відкидає ціль на дві клітини, і **Session**: персонаж, залишений у цьому стані з певним фасингом, при влучанні в нього відкинутого ворога бʼє його й **відбиває у напрямку, куди сам дивиться**. Так до шести членів загону складають «більярдні» ланцюги. Магія — монети Coinfeigm із запасом заряду; класи замінено відданістю одному з шести богів.

## Поле і час
- Квадратна сітка з ландшафтом і перешкодами (рівнини, ліси, фортеці); камеру повертають плечовими кнопками на 90°.
- Хід персонажа починається, коли його RAP = 0 %; кожна дія додає RAP, на 100 % хід закінчується. Перебір понад 100 % відсуває наступний хід, економія — наближає (`turn-structure: time-track`).
- Після ходу можна долити RAP в окрему шкалу, щоб самому призначити момент наступного ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж загону | piece | HP, RAP, бог, відданість, ≤ 4 монети (Remix) | ходить, бʼє, стріляє, чаклує; на кінці ходу — Defend або Session |
| Персонаж у Session | piece | фасинг | приймає відкинутого ворога, бʼє і відбиває його у свій бік |
| Хост сесії | piece | — | той, хто першим зробив Shoot у союзника-сесію |
| Ворог | enemy | HP, бог/елемент | ШІ; може носити предмети, які крадуть комбо |
| Монета Coinfeigm | resource | вартість чару, запас CP | закляття (лікування або атаки); CP повний на старті бою, поповнюється з ходами |
| Печатка (seal) | pickup | елемент | вигравіювати на монету → змінює її характеристики |
| Сфера (orb) | pickup | — | змінює дальність, вартість, запас і швидкість монети |
| Перешкода, ландшафт | static | розмір | займає клітини, заважає руху й відкиданню (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `counter(rap[a], ==, 0)` → ТО `custom: «хід персонажа a починається»`; швидші ходять раніше.
- КОЛИ `input(move|attack|coin|item)` → ТО `counter(rap[a], +cost)`; далекий рух лишає мало RAP на дії, стояння на місці — 2–3 атаки підряд.
- КОЛИ `counter(rap[a], ≥, 100)` → ТО `end_turn`; надлишок → `custom: «наступний хід пізніше»`.
- КОЛИ `input(defend)` → ТО `set_state(a, defend)`, `end_turn`; невитрачений RAP → наступний хід раніше.
- КОЛИ `input(session, dir)` → ТО `face(a, dir)`, `set_state(a, session)`, `end_turn` — більш вразливий, ніж у Defend.
- КОЛИ `input(attack, enemy)` → ТО `damage(enemy, n)`.
- КОЛИ `input(shoot, unit)` → ТО `damage(unit, small)`, `custom: «відкинути на 2 клітини від атакувальника»` — і ворога, і союзника.
- КОЛИ `contact(shot_enemy, ally)` → ЯКЩО `state(ally, session)` → ТО `damage(enemy, n)`, `custom: «відкинути ворога на 2 клітини в напрямку фасингу ally»`.
- КОЛИ `after(session_shot)` → ЯКЩО `custom: «на шляху наступний союзник у Session»` → ТО `trigger(session_rule)` — ланцюг до шести учасників.
- КОЛИ `custom: «ланцюг сесії закінчився вдало»` → ТО `take(enemy, equipped_item)`, `give(party, item)` (?).
- КОЛИ `input(coin, target)` → ЯКЩО `counter(coin_cp, ≥, cost)` → ТО `custom: «закляття монети»`, `counter(coin_cp, -cost)`; монета 20/40 — два чари поспіль, 20/30 — один.
- КОЛИ `turn_end(holder)` → ТО `counter(coin_cp, +n)`; КОЛИ `level_start` → ТО `set_value(coin_cp, max)`.
- КОЛИ `input(engrave, seal → coin)` → ТО `custom: «змінити характеристики монети»`; Remix — `prob(p)`: результат випадковий, монета може погіршитись.
- КОЛИ `input(attach, orb → coin)` → ТО `custom: «дальність / вартість / запас / швидкість монети»`.
- КОЛИ `custom: «персонаж бʼється»` → ТО `counter(devotion, +n)`; КОЛИ `counter(devotion, ≥, 100)` → ТО `give(a, next_deity_skill)`.
- Сумісність богів: ЯКЩО `custom: «боги атакувальника й цілі сумісні / протилежні»` → ТО `custom: «сильно змінює шкоду й влучність»` (200 vs 16 у прикладі огляду).
- КОЛИ `hp_zero(ally)` → ТО `disappear(ally)` — персонаж утрачений.
- Перемога / поразка: умови мапи (?) · Рахунок: нема; здатися посеред бою швидко не можна.

## Керування і ввід
- Курсор по сітці, меню дій: Move · Attack · Shoot · Coinfeigm · Item · кінець ходу Defend або Session (з вибором фасингу).
- Плечові кнопки — поворот мапи на 90° (PS1 і DS).
- Remix (DS): ті самі меню; стилус в оглядах не згаданий (?).

## Вікна, меню, HUD
- `game-screen`: ізометрична сітка, RAP-шкала активного персонажа (`+ui:rap-gauge`), порядок ходів (`+ui:turn-order-bar`) (?), HP.
- `custom-window` «Session/Defend»: вибір стану й напрямку в кінці ходу.
- `custom-window` монети: CP, вартість, печатки й сфери; гравіювання.
- `shop-window` у містах: монети й сфери; `+window:temple` — зміна бога.
- `map-window` світу з містами й Tower of Trial (?); `dialogue-window`; `end-screen`.
- `difficulty-select` (Remix): Easy / Normal / Hard.

## Фічі поза полем
- `difficulty-presets` (Remix): Hard = оригінал PS1; Easy — вороги без Coinfeigm.
- Remix: сюжет розгалужується від виборів (інші бої й союзники).
- `xp-level` + відданість богам замість класів; гринд у Tower of Trial.
- Збереження в місті / між боями (?); у Remix радять часто зберігатися через ризик гравіювання.

## Варіації й родичі
- Hoshigami: Ruining Blue Earth Remix (DS, 2007, Arc System Works) — складності, розгалуження, оновлена графіка.
- Родичі в корпусі: [into-the-breach](into-the-breach.md) (штовхання як головна зброя), [final-fantasy-tactics](final-fantasy-tactics.md) і [tactics-ogre](tactics-ogre.md) (ізометрія, шкала часу ходу), [jeanne-darc](jeanne-darc.md) (позиційні бонуси).
- **Осі варіацій**: черговість — фаза сторони / шкала часу (RAP, CT) · відкидання — нема / 1 клітина / 2 клітини / ланцюг через союзників · хто задає напрям — атакувальник / фасинг приймача · магія — MP / заряди / монети із запасом.

## Цікавинки для курсу
- RAP-шкала: витрати на дії відсувають наступний хід, перебір карає — 🥉 (черга пріоритетів за часом).
- Shoot на 2 клітини + Session-приймач, що відбиває у свій фасинг — 🥈 (траєкторія з перенаправленнями, ланцюг до 6).
- Монета з запасом і вартістю (20/40 → два чари), поповнення з ходами — 📎.
- Гравіювання печаток з випадковим результатом — 📎.
- Відданість богові: 100 очок → наступна навичка, бог змінюється в храмі — 📎.

## Мапа на каталог
- Є: `hp-damage` · `ai-opponent` · `impassable-cells` (перешкоди) · `permadeath` · `unit-xp-skills` · `inventory-items` · `shop-between-levels` · `difficulty-levels` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+action-points` · `+initiative-order` · `+knockback` · `+elemental-resistance` — уже в корпусі (тут RAP поєднує обидва перші).
  - `+session-relay` «Союзник-приймач продовжує відкидання» · entities/combat · 🥈 · слот {max_chain: 6}.
  - `+facing-redirect` «Фасинг задає новий напрям руху цілі» · entities/move · 🥉 — спільне з [la-pucelle-tactics](la-pucelle-tactics.md).
  - `+combo-steal` «Комбо краде предмет» · entities/interact · 🌱.
  - `+spell-coins` «Закляття-заряди з запасом» · entities/state · 📎.
  - `+seal-engrave` «Модифікація предмета з випадковим результатом» · game-logic/economy · 📎.
  - `+deity-devotion` «Відданість фракції відкриває навички» · entities/state · 📎.
  - `+training-tower` «Необовʼязкові бої для прокачки» · levels/progression · 🌱.
  - `+camera-rotate` «Поворот ізокамери на 90°» · interface/render · 📎.

## Пропозиції до словників
- `+effect:knockback` — відкинути сутність на N клітин від джерела (уже пропоновано в корпусі).
- `+effect:delay_turn` — відсунути наступний хід на шкалі часу (уже пропоновано).
- `+trigger:collide` — відкинута сутність врізалась в іншу (уже пропоновано).
- `+ui:turn-order-bar` — черга ходів (уже пропоновано); `+ui:rap-gauge` — шкала витрат ходу з порогом 100 %.
- `+window:temple` — зміна фракції/бога персонажа.
- `+axis:turn-structure=time-track` — черговість за накопиченим часом дій.

## Джерела
- ⭐ [Wikipedia: Hoshigami](https://en.wikipedia.org/wiki/Hoshigami:_Ruining_Blue_Earth) — RAP 0→100 %, Shoot на 2 клітини, Session і фасинг, до шести учасників, Coinfeigm, шість богів, Remix.
- [RPGFan (PS1)](https://www.rpgfan.com/review/hoshigami-ruining-blue-earth/) — Defend vs Session, крадіжка в комбо, монети 20/40, 100 очок відданості, Tower of Trial, остаточна смерть.
- [RPGFan (DS Remix)](https://www.rpgfan.com/review/hoshigami-ruining-blue-earth-remix/) — складності, гравіювання, до 4 монет, поворот мапи.
- [PS Illustrated](https://ps2.psillustrated.com/gamevortex/soft_rev.php/310) — Shoot, сесії, печатки, Tower of Trial, ландшафт.
- YouTube: пошук «Hoshigami Ruining Blue Earth gameplay».

## Непевне
- (?) Відстань Shoot: Wikipedia — 2 клітини, RPGFan — «2–3», PSIllustrated — «кілька».
- (?) Смерть: RPGFan — без відновлення взагалі; Wikipedia — утрачений, якщо не оживити до кінця бою.
- (?) Умови перемоги й поразки мап — джерела не описують; що стається при відкиданні в перешкоду чи за край.
- (?) Крадіжка предметів: «якщо виконати правильно» — умова не ясна.
- (?) HUD черги ходів і екран світу — з загального досвіду жанру, не підтверджено.
