---
title: Dofus (бойова система)
slug: dofus
aka: [DOFUS, "Dofus 2.0", "Dofus 3.0", "Dofus Unity"]
family: tactics
also: []
klass: avatar
axes:
  field: iso
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2004
platforms: [web (Flash), Windows, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dofus", best: true, note: "MMO в цілому: бої покрокові, ОД на дії, ОР на рух, закляття крадуть ОД/ОР; 19 класів з ролями; Dofus 3.0 на Unity (2024)"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Dofus", note: "PA/PM, тацкл і втеча, режими PvP, Колізей з рейтингом і лігами, енергія, сервери з permadeath"}
  - {kind: other, url: "https://dofus.jeuxonline.info/article/1720/bases-combat", note: "основи бою: 6 ОД / 3 ОР, +1 ОД на 100 рівні, криткі, опори, характеристики"}
  - {kind: other, url: "https://dofus.jeuxonline.info/actualite/30452/devblog-tacle-deterministe", note: "девблог 2011: детермінований тацкл, формула (Fuite+2)/(2·(Tacle+2))"}
  - {kind: other, url: "https://dofus.jeuxonline.info/actualite/32817/devblog-mode-tactique", note: "девблог 2011: тактичний режим — плоскі клітини, блокери огляду, фаза підготовки"}
  - {kind: other, url: "https://dofus.jeuxonline.info/article/7786", note: "челенджі: випадкова умова на бій, бонус 1–250 % до досвіду й здобичі"}
  - {kind: other, url: "https://everquest.allakhazam.com/wiki/Combat", note: "стара вікі: ~30 с на хід, ОД/ОР скидаються щоходу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dofus+combat+gameplay", note: "пошук; бої"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, move-timer, turn-enforcement, online-multiplayer, rating-system, permadeath, unit-xp-skills, placement-screen, lobby-window, game-screen, end-screen, +action-points, +movement-points, +ap-mp-drain, +tackle-escape, +initiative-order, +spell-range-min-max, +spell-line-of-sight, +critical-hit, +elemental-resistance, +summon-ally, +optional-challenge, +tactical-view-toggle, +energy-on-defeat, +multi-account-team, +invisibility]
proposes: ["+trigger:cast", "+effect:spend_ap", "+effect:summon", "+cond:visible", "+ui:turn-order-bar", "+ui:spell-bar", "+ui:challenge-icon", "+window:battle-screen", "+window:fight-results", "+feature:tactical-mode", "+feature:mode-ranked", "+card:tackle-escape", "+card:ap-mp-drain"]
author: opus
date: 2026-11-09
---

# Dofus — MMO, де кожен бій — покрокова тактика на ізосітці з окремими очками дії й руху

## Суть
Dofus (Ankama, 2004) — браузерна, згодом клієнтська MMORPG; описано лише її бойовий шар. Напад на групу монстрів переносить у закриту бойову копію карти, де персонажі (до 8 гравців) і монстри ходять по черзі на клітинній ізометричній карті. Кожен має **очки дії (ОД/PA)** на закляття й удари і **очки руху (ОР/PM)** на кроки — окремі бюджети, що щоходу відновлюються. Багато заклять б'ють не по HP, а по цих бюджетах: знімають ворогу ОД чи ОР; а **тацкл** — сусідство з ворогом — «з'їдає» частку ОД і ОР у того, хто намагається відійти.

## Поле і час
- Ізометрична карта з клітин; бій іде на тій самій карті світу, що й ходіння, але в окремій копії, куди інші гравці не входять.
- Два типи клітин для бою: прохідні і такі, що блокують і рух, і огляд (тактичний режим показує лише їх, «на одній висоті»).
- Перед боєм — фаза підготовки: гравці розставляються на стартових клітинах (?) і можуть увімкнути тактичний режим.
- Хід — черга бійців за ініціативою (?); на хід дається ліміт часу (стара вікі: близько 30 с), після нього невитрачені ОД і ОР згорають.
- Інформація: усе видно, крім невидимих бійців (невидимка не тацклить і завжди може втекти) — тому `partial`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж гравця | player | клас (19); HP; ОД 6 (+1 на 100 рівні); ОР 3; Тацкл; Втеча; ініціатива; шанс крита; опори стихій | ходить за ОР, б'є заклинаннями й зброєю за ОД |
| Союзник | ally | інший гравець або персонаж того ж гравця | ходить у свою чергу |
| Монстр | enemy | ОР за расою; набір заклять | ходить за ШІ |
| Бос | boss | — | у підземеллях; деякі вимикають певні челенджі |
| Виклик (summon) | ally | — | створюється закляттям (Осамодас), діє за ШІ (?) |
| Прохідна клітина | terrain | — | кроки за ОР |
| Перешкода | static | — | блокує рух і лінію огляду |
| Стартова клітина | zone | дві команди | місця для розстановки в фазі підготовки (?) |
| Закляття | supply | ціна в ОД; дальність min–max; потреба в огляді; ефект | шкода/лікування/баф/зняття ОД чи ОР/переміщення/виклик |
| Зброя ближнього бою | supply | ціна в ОД; дальність | удар за ОД, теж може кританути |
| Челендж | mark | умова на бій | виконано — бонус до досвіду й здобичі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(attack, player, monster_group)` → ТО `window(battle)`: бойова копія карти, `custom: «бій закрито для сторонніх»`.
- КОЛИ `phase_start(preparation)` → ТО `custom: «кожен ставить персонажа на стартову клітину своєї команди»` (?), `custom: «тактичний режим доступний»`.
- КОЛИ `phase_start(fight)` → ТО `custom: «черга бійців за ініціативою, від найбільшої»` (?), `rng` → `custom: «випадковий челендж бою»`.
- КОЛИ `turn_start(fighter)` → ТО `counter(ap, =base)`, `counter(mp, =base)`.
- КОЛИ `input(move, fighter, cell)` → ЯКЩО `counter(mp, >=, path_len)` і `path_exists(fighter, cell)` → ТО `move(fighter, cell)`, `counter(mp, -path_len)`.
- КОЛИ `input(cast, spell, target)` → ЯКЩО `counter(ap, >=, cost)` і `in_range(caster, target, min..max)` і `line_of_sight(caster, target)` → ТО ефект закляття, `counter(ap, -cost)`; закляття «без огляду» — без умови `line_of_sight`.
- КОЛИ `input(cast, spell, target)` → ЯКЩО `prob(crit_rate)` → ТО `custom: «критична версія ефекту»` (шанс ≤ 100 %).
- КОЛИ `input(cast, damage_spell, target)` → ТО `damage(target, n)` зменшено `custom: «опором цілі до стихії закляття»`.
- КОЛИ `input(cast, drain_spell, target)` → ТО `counter(target.ap, -n)` або `counter(target.mp, -n)`, зменшено `custom: «Мудрість цілі зменшує втрати ОД/ОР»`.
- КОЛИ `leave(fighter, cell)` → ЯКЩО `adjacent_count(fighter, enemy, >=, 1)` і `not state(fighter, invisible)` → ТО `custom: «лишається (Втеча+2)/(2·(Тацкл+2)) від ОД і ОР; кілька тацклерів — частки множаться»`.
- КОЛИ `custom: «тацкл»` → ЯКЩО `state(tackler, invisible)` → ТО `custom: «тацкл не діє»`.
- КОЛИ `input(cast, summon_spell, cell)` → ЯКЩО `free(cell)` → ТО `spawn(summon, cell)`.
- КОЛИ `input(cast, move_spell, target)` → ТО `teleport(caster, cell)` або `custom: «переміщення цілі»` (телепорт, штовхання).
- КОЛИ `timer(turn_limit)` → ТО `end_turn`, `custom: «невитрачені ОД і ОР згорають»`.
- КОЛИ `input(end_turn)` → ТО `end_turn`.
- КОЛИ `hp_zero(fighter)` → ТО `disappear(fighter)`; ЯКЩО `count(team_alive, ==, 0)` → ТО `lose` для команди.
- КОЛИ `all_gone(enemy_team)` → ТО `win`, `custom: «досвід і здобич»` (залежать від Мудрості, Удачі-проспекції, розміру групи).
- КОЛИ `constraint_broken(challenge)` → ТО `custom: «челендж провалено, бій триває зі звичайною нагородою»`.
- КОЛИ `all_gone(enemy_team)` → ЯКЩО `custom: «челендж виконано»` → ТО `multiplier(1..250 %)` до досвіду й здобичі.
- Приклади челенджів (умови на бій): Zombie — `custom: «лише 1 ОР за хід»`; Statue — `custom: «закінчити хід на стартовій клітині»`; Nomade — `custom: «витратити всі ОР»`, тацкл-втрата ОР провалює; Hardi — закінчити хід поруч з ворогом; Pusillanime — ніколи не закінчувати хід поруч з ворогом; Intouchable — не отримати жодної шкоди.
- КОЛИ `custom: «команду гравця переможено»` → ТО `counter(energy, -n)` (шкала енергії 10 000; з оновлення 3.3 не падає нижче 1).
- Перемога: знищити всю ворожу команду · Поразка: уся команда без HP · Рахунок: досвід і здобич, бонус челенджу; у Колізеї — рейтинг.

## Керування і ввід
- Миша: клік по клітині — рух (шлях по прохідних клітинах за ОР); вибір закляття в панелі → клік по цілі; кнопка завершення ходу.
- Фаза підготовки: клік по стартовій клітині, кнопка «готово» (?); кнопки біля центрального медальйону — тактичний режим і режим невидимості інших гравців.
- Наведення на монстра показує його опори (атакувати найслабшу) і очікуваний досвід.
- Мультиакаунт: один гравець може вести кілька своїх персонажів у бою (FR-Wikipedia: проблема «monocomptes / multicomptes» у PvP).

## Вікна, меню, HUD
- `+window:battle-screen` — бойова копія карти: `turn-indicator`, `+ui:turn-order-bar` (черга бійців), `+ui:spell-bar` (закляття й зброя), `action-points` і лічильник ОР, `hp-bar`, `end-turn-button`, `+ui:challenge-icon` (поточний челендж), `chat-box`, `timer-countdown` ходу.
- `placement-screen` — фаза підготовки з кнопками тактичного режиму й невидимості.
- `+window:fight-results` — кінець бою: досвід, здобич, бонус челенджу.
- `lobby-window` — Колізей: черга на 1×1 і 3×3, рейтинг, ліги.
- Переходи: світ → (напад) → placement-screen → battle-screen → fight-results → світ.

## Фічі поза полем
- PvP: Колізей (з 2.4, 2011): 1×1, 2×2, 3×3, рейтинг `Puissance − 3 × Incertitude`, ліги Бронза → Срібло → Золото → Кристал → Діамант → Легенда; AvA за території альянсів (призма), бої за сторону Бонта/Бракмар.
- Типи серверів: Classic, Monoaccount, Epic (permadeath проти монстрів), Heroic (permadeath проти всіх), Tournament.
- Енергія 10 000: поразка зменшує; до 3.2 на нулі персонаж ставав привидом і мусив дійти до статуї Фенікса.
- Тактичний режим (2011): спрощена плоска карта лише з двома типами клітин — для читання ліній огляду.
- Прогресія поза боєм: рівні, характеристики (Сила/Інтелект/Удача/Спритність → шкода стихій; Спритність → тацкл і втеча; Мудрість → опір зняттю ОД/ОР і досвід), спорядження, закляття з квестів.

## Варіації й родичі
- Dofus Arena (2006 за вступом Wikipedia) — PvP-відгалуження: 12 класів по 10 заклять, команда в бюджеті 6000 кам, бонус-карти й карти подій, **удар у бік +20 %, у спину +40 %**, шкода від поштовху об перешкоду (FAQ 2.10a).
- Wakfu — продовження у тому самому світі (клас Еліотроп у Dofus — відгалуження еліатропів Wakfu).
- Родичі за механіками: [Final Fantasy Tactics](final-fantasy-tactics.md) (класи на ізосітці), [D&D-бій на сітці](dnd-grid-combat.md) (рух + дія за хід, атака з нагоди), [Hero Academy](hero-academy.md) (бюджет дій на хід).
- **Осі варіацій**: бюджет ходу — одна дія (FE) / дві дії (XCOM) / окремі ОД і ОР (Dofus) · зона контролю — нема / блок руху / детермінована частка втрат ОД і ОР за формулою (Dofus з 2011) / ймовірнісний тацкл (Dofus до 2011).

## Цікавинки для курсу
- Два бюджети ходу (ОД і ОР), що скидаються щоходу, і закляття, що їх знімають ворогу — 📎 (дві змінні + ефект «мінус ресурс»).
- Детермінований тацкл: частка `(Втеча+2)/(2·(Тацкл+2))`, добуток для кількох тацклерів — 🥉 (формула + сусідство + «+2» проти нуля).
- Закляття з дальністю min–max і перевіркою лінії огляду на сітці — 🥈 (Брезенгем/supercover по ізоклітинах).
- Випадковий челендж на бій з умовою на поведінку і множником нагороди — 🥉 (перевірка обмеження щоходу).
- Тактичний режим: та сама карта як плоска схема «прохідно / блокує» — 📎.
- Таймер ходу, що спалює невитрачені ОД/ОР — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (зброя / закляття) · `move-timer` (ліміт часу на хід) · `turn-enforcement` · `online-multiplayer` · `rating-system` (Колізей) · `permadeath` (сервери Epic/Heroic) · `unit-xp-skills` · `placement-screen` · `lobby-window` · вікна.
- **Нема** → пропозиції карток:
  - `+action-points` + `+movement-points` «Окремі бюджети дії й руху» · game-logic/opponent · 📎.
  - `+ap-mp-drain` «Закляття знімає ОД/ОР ворогу» · entities/combat · 📎.
  - `+tackle-escape` «Тацкл: відхід від ворога коштує частку ОД/ОР» · entities/combat · 🥉 · слот {formula}.
  - `+spell-range-min-max` «Дальність від–до» · entities/combat · 🌱.
  - `+spell-line-of-sight` «Ціль лише в полі зору» · entities/combat · 🥈.
  - `+initiative-order` «Черга ходів за ініціативою» · game-logic/opponent · 🌱.
  - `+optional-challenge` «Випадковий челендж на бій» · game-logic/score · 🥉.
  - `+tactical-view-toggle` «Спрощений вид поля» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:cast` — бієць застосував закляття (точка для реакцій і челенджів).
- `+effect:spend_ap` — списати ОД/ОР за дію.
- `+effect:summon` — створити підконтрольну сутність закляттям (не `spawn`, бо є власник і ліміт викликів).
- `+cond:visible` — бієць видимий (невидимий не тацклить, його не таргетять).
- `+ui:turn-order-bar` — смуга черги бійців; `+ui:spell-bar` — панель заклять з ціною в ОД; `+ui:challenge-icon` — іконка поточного челенджу.
- `+window:battle-screen` — окремий бойовий екран поверх карти світу; `+window:fight-results` — підсумок бою з досвідом і здобиччю.
- `+feature:tactical-mode` — перемикач спрощеного виду поля; `+feature:mode-ranked` — рейтингові бої з лігами.
- `+card:tackle-escape`, `+card:ap-mp-drain` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Dofus](https://en.wikipedia.org/wiki/Dofus) — бої покрокові, ОД/ОР, закляття знімають ОД/ОР, 19 класів, історія версій.
- [Wikipedia FR: Dofus](https://fr.wikipedia.org/wiki/Dofus) — PA/PM, тацкл і втеча, PvP-режими, Колізей і ліги, енергія, типи серверів.
- [JeuxOnLine: основи бою](https://dofus.jeuxonline.info/article/1720/bases-combat) — 6 ОД / 3 ОР, криткі, опори, характеристики, досвід.
- [JeuxOnLine: девблог «Tacle déterministe»](https://dofus.jeuxonline.info/actualite/30452/devblog-tacle-deterministe) — формула тацкла, приклади, множення для кількох тацклерів, невидимість.
- [JeuxOnLine: девблог «Mode tactique»](https://dofus.jeuxonline.info/actualite/32817/devblog-mode-tactique) — тактичний режим, фаза підготовки.
- [JeuxOnLine: челенджі](https://dofus.jeuxonline.info/article/7786) — випадковий челендж, бонус 1–250 %, список умов.
- [Allakhazam: Combat](https://everquest.allakhazam.com/wiki/Combat) — стара вікі: ~30 с на хід, скидання ОД/ОР.

## Непевне
- (?) Черга за ініціативою підтверджена лише для Dofus Arena (Wikipedia, FAQ); для Dofus — з памʼяті.
- (?) Стартові клітини двох команд і кнопка «готово» у фазі підготовки — джерела згадують лише саму фазу.
- (?) Ліміт ходу 30 с — зі старої вікі; у сучасній версії може відрізнятись.
- (?) Деякі «непрохідні» клітини не блокують огляд (сніпет вікі Dofus на fandom, сторінка не відкрилась) — розходиться з двома типами клітин тактичного режиму.
- (?) Чи виклики керуються гравцем, чи ШІ, — у Dofus Arena ними керує ШІ.
- (?) Шкода від поштовху й бонуси в бік/спину — лише з FAQ Dofus Arena; у Dofus правила поштовху інші.
