---
title: "Valkyrie Profile: Covenant of the Plume"
slug: valkyrie-profile-covenant-of-the-plume
aka: ["Valkyrie Profile: Toga o Seou Mono", "ヴァルキリープロファイル 咎を背負う者", VPCotP]
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
year: 2008
platforms: [Nintendo DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Valkyrie_Profile:_Covenant_of_the_Plume", best: true, note: "огляд: сітка, союзники вступають у бій, кнопка на персонажа, Attack Gauge → Soul Crush, Overkill, AP, Destiny Plume, Sin, кінцівки"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ヴァルキリープロファイル_咎を背負う者", note: "JA: радіуси вступу в бій за класами, AP +10/хід, очікування ×2, магічні кристали, Active Formation, карма й Hel Stalker"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Valkyrie+Profile+Covenant+of+the+Plume+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, permadeath, unit-xp-skills, shop-between-levels, inventory-items, destroy-all-enemies, sequential-levels, main-menu, game-screen, shop-window, character-select, end-screen, +join-attack-range, +button-per-unit, +attack-gauge-finisher, +overkill-bonus, +doomed-power-up, +sin-quota-penalty, +action-points, +wait-recovers-more, +formation-bonus, +multiple-endings, +branching-recruits, +air-juggle-reward, +new-game-plus]
proposes: ["+card:join-attack-range", "+card:button-per-unit", "+card:doomed-power-up", "+card:overkill-quota", "+window:battle-cutaway", "+feature:new-game-plus"]
author: opus
date: 2026-11-09
---

# Valkyrie Profile: Covenant of the Plume — SRPG, де кожен союзник у радіусі вступає в бій на своїй кнопці, а перо богині дає силу ціною життя

## Суть
Тактика tri-Ace для DS: на сітці Вілфред і до трьох союзників ходять, як у Fire Emblem, але атака на карті відкриває окремий **бій у реальному часі в стилі Valkyrie Profile 1**: кожен союзник, у чиєму радіусі стоїть ціль, вступає в бій і бʼє на своїй кнопці (A/B/X/Y). Удари наповнюють шкалу до фінішера (Soul Crush), добивання понад нуль HP (Overkill) дає «гріх». Головна ставка — **Перо Долі**: Вілфред може віддати його союзнику, і той на кілька ходів стає в рази сильнішим, але після бою гине назавжди; частота пера визначає кінцівку.

## Поле і час
- Ізометрична 3D-сітка з поворотною камерою; кожна мапа — окрема тема середовища (EN Wikipedia).
- Покроково за фазами сторін: юніт рухається на свою дальність, потім атакує / вміння / предмет / чекає.
- Бій-вставка: окремий екран, де вступили всі союзники в радіусі; удари в реальному часі (натискання й таймінг), потім повернення на мапу.
- Партія — ромб-формація 4 юнітів: вона ж задає стартові позиції на мапі й місця (кнопки) у бою (JA).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вілфред | piece | лідер | єдиний, хто використовує перо; загибель — кінець гри |
| Легкий / важкий воїн | piece | вступ: 8 сусідів | до 3 ударів за бій (залежить від зброї) |
| Списник | piece | вступ: квадрат 5×5 | — |
| Лучник | piece | вступ: 9×9 без 8 сусідів | бʼє з відстані, впритул — ні |
| Маг | piece | вступ: 7×7 | заклинання, задане заздалегідь; фінішер — посилене закляття |
| Злодій / кулачник | piece | вступ: 4 сусіди | — |
| Ворожий юніт | enemy | клас, HP | ті самі правила; невербовані союзники пізніше стають ворогами |
| Лідер ворогів | boss | — | ціль мапи (?) |
| Hel Stalker | boss | дуже сильний | зʼявляється на наступній мапі, якщо не набрано квоту гріха |
| Перо Долі (女神の羽) | supply | — | у Вілфреда; дає союзнику ×10 характеристик і унікальне вміння |
| Магічний кристал (魔晶石) | pickup | — | випадає з ударів по підкинутому ворогу; +досвід після бою |
| Фіолетовий камінь (紫炎石) | pickup | — | з удару по поваленому ворогу; відновлює кількість атак |
| Спорядження й предмети | pickup | — | у крамницях, трофеї бою |
| AP юніта | resource | +10 за хід | витрачається на предмети, вміння, магію (звичайна атака — безкоштовна) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, unit, cell)` → ЯКЩО `legal(path ≤ move)` → ТО `move(unit, cell)`.
- КОЛИ `input(attack, unit, enemy)` → ЯКЩО `in_range(unit, enemy, class_shape)` → ТО `window(battle_cutaway)`.
- КОЛИ `custom: «бій почався»` → ЯКЩО `in_range(ally, enemy, class_shape)` → ТО `custom: «союзник вступає в бій»` (навіть якщо вже ходив цього ходу).
- КОЛИ `input(button_A|B|X|Y)` → ЯКЩО `custom: «персонаж на цій позиції ромба має удари»` → ТО `damage(enemy, n)`, `counter(attack_gauge, +n)`.
- КОЛИ `counter(attack_gauge, >=, 100)` → ТО `custom: «Soul Crush — фінішер персонажа»`; ланцюг фінішерів — `custom: «кожен наступний стартує з меншим зарядом»`.
- КОЛИ `custom: «удар по підкинутому ворогу»` → ТО `spawn(magic_crystal)` → після бою `counter(exp, +n)`.
- КОЛИ `custom: «удар по поваленому ворогу»` → ТО `spawn(purple_flame_stone)` → `custom: «+атаки цьому бою»`.
- КОЛИ `counter(enemy_hp, <=, 0)` → ЯКЩО `custom: «удари тривають»` → ТО `custom: «Overkill»`, `counter(sin, +n)`.
- КОЛИ `custom: «бій почався»` → ЯКЩО `custom: «союзники стоять з чотирьох боків ворога»` → ТО `multiplier(gauge|drop_rate)` (Active Formation).
- КОЛИ `input(plume, ally)` → ЯКЩО `turn_of(wylfred)` → ТО `set_state(ally, plumed)` (характеристики ×10, унікальне вміння), `counter(sin, +n)`, `counter(plume_uses, +1)`.
- КОЛИ `level_end` або `counter(plume_turns, ==, 0)` → ЯКЩО `state(ally, plumed)` → ТО `disappear_a` назавжди, `give(wylfred, weakened_skill)`.
- КОЛИ `level_end` → ЯКЩО `counter(sin, <, quota)` → ТО `spawn_at(hel_stalker, next_map)`; ЯКЩО `counter(sin, >=, 2×quota)` → ТО `give(party, strong_gear)`; ЯКЩО `counter(sin, >=, quota)` → ТО `give(party, items)` (нагорода богині після мапи).
- КОЛИ `input(item|field_skill|magic)` → ЯКЩО `counter(ap, >=, cost)` → ТО `counter(ap, -cost)` і ефект; `custom: «більше AP — сильніший ефект»`.
- КОЛИ `turn_end(unit)` → ЯКЩО `custom: «лише чекав»` → ТО `counter(ap, +20)`; інакше `counter(ap, +10)`.
- КОЛИ `input(change_weapon)` → ТО `end_turn` (для цього юніта).
- КОЛИ `destroyed(enemy)` → ТО `counter(exp, +n)` активним юнітам.
- КОЛИ `hp_zero(wylfred)` → ТО `lose` → завантаження збереження.
- КОЛИ `counter(plume_uses, >, limit)` → ТО `lose` (Фрея перемагає Вілфреда).
- КОЛИ `custom: «кінець глави 5»` → ЯКЩО `counter(plume_uses, ==, 0)` → ТО `custom: «кінцівка A»`; `==1` → B; більше → C.
- КОЛИ `custom: «вибір шляху в сюжеті»` → ТО `custom: «союзника завербовано або він стане ворогом»`.
- Перемога мапи: розбити ворогів / лідера (?) · Поразка: загибель Вілфреда або забагато пер · Рахунок: досвід, гріх, трофеї.

## Керування і ввід
- Карта: D-pad / стилус (?) — вибір юніта, клітини, дії з меню: Move · Attack · Wait · Change Weapon · Item · Field Skill · Magic (маги) · Plume (Вілфред).
- Бій: A, B, X, Y — удари персонажів у відповідних позиціях ромба; воїни мають до 3 ударів, порядок налаштовується заздалегідь; таймінг для підкидання й добивання поваленого.
- Підготовка партії: ромб-формація, бойові вміння (вмикаються самі в бою).

## Вікна, меню, HUD
- `main-menu`: New Game · Continue · (після проходження) New Game+.
- `game-screen` — ізометрична мапа: юніти, дальність руху/атаки (?), меню дій, HP і AP юніта.
- `custom-window` «бій» — окрема арена: портрети союзників на кнопках, `hp-bar` ворога, `combo-meter` (Attack Gauge до 100), лічильник ударів.
- `character-select` — підготовка: склад і ромб-формація, бойові вміння, спорядження.
- `shop-window` — крамниці в містах; `custom-window` «таверна» — лор і побічні завдання з другорядними ворогами.
- `end-screen` — підсумок мапи: досвід (із кристалами), гріх/карма, нагорода за квоту.
- `dialogue-window` — сюжетні сцени між мапами; `save-slots` (?).

## Фічі поза полем
- Три кінцівки (A/B/C) за кількістю використань пера до глави 5 + «Game Over» за надто часте перо.
- `xp-level` юнітів; Skill Books (купити, трофей, нагорода) — вміння поля й бою.
- New Game+ (переносяться вміння, сюжет той самий); Seraphic Gate — секретне підземелля після всіх трьох кінцівок, з унікальними юнітами.
- Вербування залежить від сюжетних виборів; невзяті союзники зустрічаються ворогами.

## Варіації й родичі
- Valkyrie Profile (1999) — той самий бій на 4 кнопки, але без сітки; Valkyrie Profile 2 — інший бій.
- Родичі за механіками: [Fire Emblem](fire-emblem.md) (сітка, перманентна смерть), [Yggdra Union](yggdra-union.md) (союзники у формації вступають у бій), [Knights in the Nightmare](knights-in-the-nightmare.md) (жертва юнітів), [Persona 5 Tactica](persona-5-tactica.md) (спільна атака), [Tactics Ogre](tactics-ogre.md) (кінцівки за вибором).
- **Осі варіацій**: хто бʼється — атакувальник сам / усі союзники в радіусі (VPCotP) / формація · бій — розрахунок / окремий real-time міні-бій · смерть юніта — тимчасова / перманентна / **свідома жертва за силу**.

## Цікавинки для курсу
- Вступ у бій за формою радіуса класу (4 сусіди, 8 сусідів, 5×5, 7×7, 9×9 без кільця) — 📎 (перевірка «чи ціль у фігурі навколо юніта»).
- Одна кнопка — один персонаж: бій як ритмічна послідовність натискань зі шкалою фінішера — 🥉.
- Перо Долі: стан «сильний, але приречений» з перманентною загибеллю і передачею вміння лідеру — 📎; лічильник використань → кінцівка — 🌱.
- Квота гріха за мапу (оверкіли) з покаранням-босом на наступній мапі — 🥉 (стан, що переходить між рівнями).
- AP: +10 за хід, очікування — ×2 — 🌱.
- Active Formation: оточення ворога з 4 боків до бою дає бонус — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (радіуси класів) · `permadeath` (перо) · `unit-xp-skills` · `shop-between-levels` · `inventory-items` (Skill Books, предмети за AP) · `destroy-all-enemies` (?) · `sequential-levels` · вікна.
- **Нема** → пропозиції карток:
  - `+join-attack-range` «Союзники в радіусі вступають у бій» · entities/combat · 📎 · слот {shape per class}.
  - `+button-per-unit` «Кожен юніт — на своїй кнопці» · interface/input · 🥉.
  - `+doomed-power-up` «Підсилення ціною перманентної загибелі» · entities/state · 📎 · слот {mult, turns}.
  - `+overkill-bonus` · `+sin-quota-penalty` «Квота оверкілів, недобір — сильний ворог далі» · game-logic/score · 🥉.
  - `+formation-bonus` «Бонус за оточення з 4 боків» · entities/combat · 📎.
  - `+wait-recovers-more` · `+air-juggle-reward` · `+branching-recruits` · `+multiple-endings` · `+new-game-plus`.

## Пропозиції до словників
- `+card:join-attack-range` — союзник, у чиєму радіусі ціль, приєднується до атаки (без витрати свого ходу).
- `+card:button-per-unit` — у бою кожен учасник привʼязаний до окремої кнопки.
- `+card:doomed-power-up` — юніт отримує множник сили на N ходів і гине після бою.
- `+card:overkill-quota` — квота «понад смерть» на мапу; недобір → сильний ворог на наступній.
- `+window:battle-cutaway` — окремий екран бою, що відкривається з карти (VPCotP, анімації Fire Emblem, Yggdra Union).
- `+feature:new-game-plus` — повторне проходження з перенесенням прогресу (пропонує й Persona 5 Tactica).

## Джерела
- ⭐ [Wikipedia (EN)](https://en.wikipedia.org/wiki/Valkyrie_Profile:_Covenant_of_the_Plume) — бойова система, Soul Crush, Overkill, AP, Destiny Plume, Sin, кінцівки, дати.
- [Wikipedia (JA)](https://ja.wikipedia.org/wiki/ヴァルキリープロファイル_咎を背負う者) — радіуси вступу за класами, AP +10, очікування ×2, кристали й камені, Active Formation, карма, Hel Stalker.
- YouTube: пошук «Valkyrie Profile Covenant of the Plume gameplay».

## Непевне
- (?) Висота клітин і вплив терену — у джерелах нема.
- (?) Умова перемоги мапи (усі вороги / лідер / інше) — у джерелах не названа.
- (?) «100 AP спільного пулу, розділеного на старті» (JA) — незрозуміло, чи це пул на юніта, чи на сторону; беру «на юніта».
- (?) Скільки ходів діє перо (EN: «a few turns»); точна межа «забагато пер».
- (?) Керування стилусом і подвійний екран DS — не перевірено.
- (?) EN «Sin» і JA «карма» — одна механіка: гріх/карма за перо та оверкіли.
