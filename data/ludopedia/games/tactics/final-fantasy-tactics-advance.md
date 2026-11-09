---
title: Final Fantasy Tactics Advance
slug: final-fantasy-tactics-advance
aka: [FFTA, FFT Advance, "Final Fantasy Tactics A2: Grimoire of the Rift"]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2003
platforms: [GBA, Wii U VC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Final_Fantasy_Tactics_Advance", best: true, note: "закони й суддя, жовта/червона картка, Judge Points, тотеми, KO і відродження, раси й професії, місії, мапа з символами, link-кабель"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=final+fantasy+tactics+advance+laws+judge+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, height-levels, status-effects, unit-xp-skills, inventory-items, shop-between-levels, shop-catalog, ai-opponent, world-map, map-window, sequential-levels, save-multi-slot, destroy-all-enemies, player-death, legal-move-highlight, game-screen, +battle-laws, +law-penalty-cards, +judge-points, +law-cards-edit, +lawless-zone-permadeath, +gear-learned-abilities, +race-job-tree, +mp-from-zero, +dispatch-missions, +map-tile-placement, +clan-encounters, +combo-attack, +summon-creature, +job-system]
proposes: ["+trigger:rule_violated", "+cond:law_active", "+effect:give_card", "+effect:jail", "+effect:set_law", "+effect:remove_law", "+role:judge", "+ui:law-panel", "+ui:jp-counter", "+window:law-window", "+window:mission-board", "+window:map-placement", "+feature:dispatch", "+feature:link-trade", "+card:battle-laws", "+card:judge-points"]
author: opus
date: 2026-11-09
---

# Final Fantasy Tactics Advance — тактика FFT, де кожен бій має «закон», а суддя карає за порушення

## Суть
Покрокова тактика загону на ізометричній сітці з висотою — та сама основа, що у [final-fantasy-tactics](final-fantasy-tactics.md); тут описані лише **відмінності**. Над боєм стоїть нейтральний **суддя** (Judge), який оголошує **закони** (Laws) — заборони певних дій (заклинання, предмети, зброя певного типу). Порушник отримує картку: жовту (штраф) або червону (вилучення з бою). Дотримання законів і KO ворогів дають **Judge Points**, за які купують комбо-атаки й виклик тотемів. Смерті в звичайних боях немає — суддя оживляє всіх після бою.

## Поле і час
- Поле — ізометрична сітка з різнотипним рельєфом і висотою (як у FFT, `field: layers`); між боями — мапа Іваліса з областей, які гравець **сам розставляє**.
- Хід: кожен юніт має **один хід** — рух і дію; черговість за швидкістю (?) (CT-шкали FFT зі зарядженими заклинаннями тут немає або вона спрощена (?)).
- **MP починається з нуля** і росте щоходу — сильну магію не можна кинути в першому ході.
- Бій іде під одним набором законів; суддя «живе» на полі як нейтральна сутність.
- Окремі області — **без суддів** (Jagd (?)): закони не діють.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Марш (лідер клану) | piece | HP, MP (від 0), раса, професія | як інші; його ув'язнення = кінець гри |
| Юніт клану | piece | раса, професія, спорядження, вивчені навички | один хід: рух + дія; вчить навички через спорядження |
| Ворожий юніт / клан-суперник | enemy | ті самі стати | AI; теж підкоряється законам (?) |
| Монстр | enemy | — | AI, без професій (?) |
| Суддя (Judge) | neutral (`+role:judge`) | список законів бою | спостерігає; при порушенні видає картку; рахує JP |
| Закон (Law) | zone | що заборонено / що рекомендовано | діє на весь бій; порушення → картка |
| Жовта картка | mark | — | штраф порушнику (за Wikipedia — нижчий шанс влучання) |
| Червона картка | mark | — | вилучення з поля (вʼязниця) |
| Тотема | ally | вимагає JP | виклик-«саммон» за Judge Points |
| Карта законів (Law Card) | pickup | — | пізніше в грі: додати новий закон або стерти чинний |
| Символ області на мапі | tile | тип (місто, ліс, пустеля…) | гравець кладе на мапу Іваліса; розташування дає предмети |
| Рельєф і висота | terrain | висота, тип | як у FFT |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ЯКЩО `custom: «область під суддею»` → ТО `custom: «суддя оголошує закон(и) бою»`, `window(law-window)` (?).
- КОЛИ `input(act, u, ability, target)` → ЯКЩО `custom: «дія заборонена чинним законом»` → ТО `custom: «суддя видає картку»` (дію виконано, але покарано (?)).
- КОЛИ `custom: «перше / легке порушення»` → ТО `set_state(u, yellow_card)`; юніт отримує штраф (нижчий шанс влучання).
- КОЛИ `custom: «повторне / тяжке порушення»` → ТО `set_state(u, red_card)`, `disappear_a` — юніт вилучено з бою й відправлено до вʼязниці.
- КОЛИ `custom: «червону картку отримав Марш»` → ТО `game_over`.
- КОЛИ `hp_zero(enemy)` → ЯКЩО `custom: «вбивця не порушував законів»` → ТО `counter(JP, +1)` (?).
- КОЛИ `custom: «юніт дотримується закону / виконує рекомендовану дію»` → ТО `counter(JP, +n)` (?).
- КОЛИ `input(combo, u)` → ЯКЩО `has(JP, cost)` → ТО `counter(JP, −cost)`, `damage(n)` — спецатака, підсилена союзниками поряд (?).
- КОЛИ `input(totema, u)` → ЯКЩО `has(JP, cost)` and `custom: «тотему раси здобуто»` → ТО `spawn(totema)` / `custom: «атака тотеми по області»` (?).
- КОЛИ `turn_start(u)` → ТО `hp(u.MP, +n)` — MP від нуля росте щоходу.
- КОЛИ `hp_zero(u)` → ТО `set_state(u, ko)`; ЯКЩО `custom: «область під суддею»` → ТО після бою `heal(u, all)` — постійної смерті нема.
- КОЛИ `hp_zero(u)` → ЯКЩО `custom: «область без судді»` → ТО `custom: «юніт може загинути назавжди, якщо не оживити до кінця бою»` (?).
- КОЛИ `input(law_card, add|remove)` → ТО `custom: «додати новий закон або стерти чинний»` — гравець сам змінює правила бою.
- КОЛИ `custom: «бій виграно»` → ТО `give(u, AP)` юнітам; КОЛИ `counter(AP, ≥, cost)` → ТО `unlock(ability)` — навичка лишається назавжди (вчиться через спорядження).
- КОЛИ `custom: «освоєно потрібні навички / рівень»` → ТО `unlock(job)` — нова професія для раси.
- КОЛИ `custom: «місію виконано»` → ТО `currency(+gil)`, `give(item)`; деякі предмети — `custom: «символ нової області на мапу»`.
- КОЛИ `input(place, area_symbol, map_slot)` → ТО `place(area_symbol)`; ЯКЩО `custom: «вдале розташування за умовою»` → ТО `give(item)`.
- Перемога: умова місії (знищити всіх, лідера тощо) · Поразка: зазвичай місія просто «провалена»; кінець гри — якщо впали всі юніти в критичній місії або Марша ув'язнено · Рахунок — немає.

## Керування і ввід
- Курсор по ізометричній сітці (хрестовина GBA), поворот поля відсутній або обмежений (?).
- Меню активного юніта: Move · Action (атака, навички професії, друга навичка, предмет) · Wait з вибором напрямку.
- Перед боєм — перегляд законів судді; під час бою — перевірка, чи дія не порушує закону (попередження?) (?).
- Між боями: вибір місії на дошці таверни, розстановка символів областей, екіпірування, вибір професій.

## Вікна, меню, HUD
- `main-menu`: нова гра / продовжити.
- `map-window` — мапа Іваліса з областями; `+window:map-placement` — вибір місця для нового символу області.
- `+window:mission-board` — дошка місій у пабі: бойові, «dispatch» (відправити юніта без бою), Encounter з кланами.
- `+window:law-window` — закони дня: заборонене і рекомендоване (?).
- `formation` (як у FFT) — розстановка загону.
- `game-screen`: поле; панель юніта (HP/MP, професія, раса); `hit-chance`; `+ui:law-panel` (чинні закони); `+ui:jp-counter`; картка над порушником.
- `shop-window` — спорядження й предмети; вікно професій і навичок юніта.
- `end-screen` бою: здобуті AP/EXP, предмети; повідомлення про вʼязницю.
- `save-slots`; меню link-кабелю: обмін юнітами й предметами, кооп- і versus-місії.

## Фічі поза полем
- `job-system` з прив'язкою до раси: п'ять рас, частина професій — лише для однієї раси; нові професії відкриваються вивченими навичками.
- Навички вчаться через **спорядження**: носиш зброю N боїв → навичка твоя назавжди і лишається після зміни професії.
- Місії: бойові (сюжет), dispatch (юніт іде на кілька днів, повертається з нагородою), Encounter з кланами-суперниками; деякі вимагають предмета.
- Мапа світу, яку будує гравець символами областей; вдала розстановка — бонусні предмети.
- Пізні Law Cards: гравець сам додає чи прибирає закон бою — правила як інвентар.
- Мультиплеєр через link-кабель GBA (обмін, кооп, versus), ексклюзивні предмети.

## Варіації й родичі
- Основа — [final-fantasy-tactics](final-fantasy-tactics.md) (висоти, професії, слоти навичок); відмінність — закони, JP, відсутність permadeath у суддівських боях, MP від 0, вивчення через спорядження.
- Сиквел FFTA2: Grimoire of the Rift (DS, 2007) — закони з бонусом за дотримання, без вʼязниці (?).
- Родичі в корпусі: [tactics-ogre](tactics-ogre.md), [disgaea](disgaea.md) (гео-панелі — теж «правила поля»), [fire-emblem](fire-emblem.md) (протилежна полярність: permadeath).
- Осі варіацій:
  - **обмеження бою**: нема / сценарні умови місії / закон-заборона на всіх з картками (FFTA) / закон як бонус за дотримання (FFTA2);
  - **смерть**: остаточна (Fire Emblem) / лічильник → кристал (FFT) / KO з відродженням після бою, крім беззаконних зон (FFTA);
  - **ресурс спецдій**: MP / MP від нуля щоходу / окремі очки судді (JP).

## Цікавинки для курсу
- Закони бою: перевірка кожної дії проти списку заборон (предикат над дією) — 📎; з рекомендованими діями й очками — 🥉.
- Жовта → червона картка: скінченний автомат порушень на юніта — 🌱.
- Law Cards: правила як предмети інвентаря, які гравець вмикає/вимикає — 🥉 («мета-правила», ріднить з Baba Is You).
- MP від нуля, +n щоходу: темп сильних дій — 🌱.
- Вивчення навички через спорядження за AP — 📎.
- Розстановка символів областей на мапі з умовними нагородами — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `height-levels` · `status-effects` · `unit-xp-skills` ↔ AP і навички · `inventory-items` · `shop-between-levels` + `shop-catalog` · `world-map` + `map-window` · `destroy-all-enemies` · `player-death` ↔ вʼязниця Марша · `legal-move-highlight` · `save-multi-slot`.
- **Нема** → пропозиції карток:
  - `+battle-laws` «Закони бою: заборонені дії» · game-logic/constraints · 📎 · слоти {forbidden[], recommended[]}.
  - `+law-penalty-cards` «Картки за порушення (жовта/червона)» · entities/state · 🌱.
  - `+judge-points` «Очки за дотримання правил» · game-logic/economy · 🌱.
  - `+law-cards-edit` «Гравець додає/стирає закон» · game-logic/constraints · 🥉.
  - `+lawless-zone-permadeath` «Смерть остаточна лише в зонах без судді» · game-logic/lose · 🌱.
  - `+gear-learned-abilities` «Навичка вчиться носінням спорядження» · entities/state · 📎 · слот {ap_cost}.
  - `+race-job-tree` «Професії, доступні за расою» · entities/state · 📎.
  - `+mp-from-zero` «MP від нуля, росте щоходу» · entities/state · 🌱.
  - `+dispatch-missions` «Відправити юніта на місію без бою» · levels/progression · 📎.
  - `+map-tile-placement` «Гравець розставляє області на мапі світу» · levels/progression · 🥉.
  - `+clan-encounters`, `+combo-attack`, `+summon-creature` (з Gloomhaven), `+job-system` (з FFT).

## Пропозиції до словників
- `+trigger:rule_violated(u, law)` — дія порушила чинний закон бою.
- `+cond:law_active(law)` — закон увімкнено в цьому бою.
- `+effect:give_card(u, color)` — суддя видає картку; `+effect:jail(u)` — вилучення з бою у вʼязницю.
- `+effect:set_law(law)` / `+effect:remove_law(law)` — додати/стерти закон картою.
- `+role:judge` — нейтральний арбітр на полі, що перевіряє правила.
- `+ui:law-panel` — чинні закони на екрані бою; `+ui:jp-counter` — очки судді.
- `+window:law-window` — оголошення законів; `+window:mission-board` — дошка місій; `+window:map-placement` — розстановка областей.
- `+feature:dispatch` — фонова місія юніта; `+feature:link-trade` — обмін юнітами через кабель.
- `+card:battle-laws`, `+card:judge-points`.

## Джерела
- ⭐ [Wikipedia: Final Fantasy Tactics Advance](https://en.wikipedia.org/wiki/Final_Fantasy_Tactics_Advance) — суддя й закони, жовта/червона картка, JP на комбо й тотеми, KO і відродження після бою, MP від нуля, раси/професії, навички через спорядження, типи місій, символи областей на мапі, link-кабель.
- [final-fantasy-tactics](final-fantasy-tactics.md) — спільна основа (поле, висоти, професії).
- YouTube: пошук «final fantasy tactics advance laws judge gameplay».

## Непевне
- (?) Вікі серії недоступна (fandom; finalfantasywiki.com — цикл редиректів): точні ціни JP, кількість законів на бій, правила вʼязниці й викупу, анти-закони (antilaws), нарахування JP за «рекомендовані» дії — з памʼяті.
- (?) Беззаконні області (Jagd) і остаточна смерть там — з памʼяті; Wikipedia лише каже, що поза суддями закони не діють.
- (?) Порядок ходів (за швидкістю) і чи є заряджені заклинання, як у FFT.
- (?) Назви п'яти рас (Human, Bangaa, Nu Mou, Viera, Moogle) — Wikipedia повністю їх не перелічує.
- (?) Чи ворожі юніти теж отримують картки; чи гра попереджає перед порушенням.
