---
title: Final Fantasy Tactics
slug: final-fantasy-tactics
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
year: 1997
platforms: [PS1, PSP (War of the Lions 2007), iOS, Android, PS4, PS5, Switch, Xbox Series, PC (The Ivalice Chronicles 2025)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Final_Fantasy_Tactics", best: true, note: "ізометричне поле з квадратних клітин, CT=100, джоби/JP, слоти навичок, світова мапа, версії"}
  - {kind: guide, url: "https://game8.co/games/Final-Fantasy-Tactics/archives/543470", note: "CT: ціна ходу 100/80/80/60, перенос надлишку, швидкість заклинань"}
  - {kind: guide, url: "https://StrategyWiki.org/wiki/Final_Fantasy_Tactics/Gameplay", note: "StrategyWiki: геймплей (агентові не відкрилась)"}
  - {kind: guide, url: "https://mail.cavesofnarshe.com/fft/walkthrough.php", note: "Caves of Narshe: проходження й механіки (не перевірено)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=final+fantasy+tactics"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=final+fantasy+tactics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, temporary-modes, legal-move-highlight, hover-highlight, inventory-items, shop-between-levels, shop-catalog, ai-opponent, save-multi-slot, destroy-all-enemies, player-death, game-screen, +iso-field, +movement-points, +ct-initiative, +charged-actions, +height-levels, +facing-hit-bonus, +hit-chance, +status-effects, +death-countdown, +job-system, +pilot-xp-skills, +deployment-phase]
proposes: ["+trigger:ct_full", "+trigger:charge_done", "+trigger:attacked", "+cond:prob", "+cond:facing", "+cond:status", "+effect:set_status", "+effect:face", "+effect:transform", "+role:piece", "+role:container", "+ui:turn-order", "+ui:hit-chance", "+ui:reachable-highlight", "+ui:height-label", "+window:formation", "+window:job-window", "+window:map-window", "+window:shop-window", "+axis:field=layers", "+axis:session"]
author: opus
date: 2026-11-02
---

# Final Fantasy Tactics — тактика на ізометричних висотах, де черга ходів — це швидкість, а не сторони

## Суть
Загін до 5 персонажів бʼється з ворогами на ізометричному полі з квадратних клітин різної висоти. Сторін немає: кожен юніт накопичує **Charge Time** (CT) зі швидкістю своєї Speed і ходить, коли CT ≥ 100; заклинання теж «заряджаються» і спрацьовують пізніше — ворог встигає втекти з зони. Висота обмежує, куди можна вилізти, і збільшує дальність луків; напрямок, куди дивиться ціль, змінює шанс влучання. Між боями — система професій (jobs): навички, вивчені в одній, ставляться в слоти іншої.

## Поле і час
- Поле — квадратна сітка ~10×10…20×20 з **висотою** кожної клітини (у півкроках `h`), рендер ізометричний 3D з поворотом камери на 4 кути й нахилом. Типи клітин: трава, камінь, дерево, вода різної глибини, болото, лава, дах тощо.
- Час — «годинник» (clock tick): щотіку кожен юніт отримує `CT += Speed`; хто досягнув 100 — ходить (за рівності — перший за порядком (?)). Активний хід = Move + Act у будь-якому порядку (по одному разу) + Wait із вибором напрямку.
- Заряджені дії (магія, призиви, Aim лучника) мають власну швидкість і спрацьовують через N тіків; ціль — клітина або юніт.
- Інформація повна: HP ворогів видно, видно і порядок ходів; випадковість — у шансах влучання, статусів і реакцій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рамза (герой) | piece | HP, MP, Speed, Move, Jump, Brave, Faith, зодіак | як інші; його кристалізація = поразка |
| Солдат загону | piece | job, рівень, JP, 5 слотів (job-навичка, друга навичка, Reaction, Support, Movement), спорядження | хід за CT; вчить навички за JP |
| Гість (guest) | piece | керується AI | часто треба вберегти — його загибель = поразка |
| Ворог-людина | enemy | ті самі стати й професії | AI; завжди рухається й діє, якщо може |
| Монстр (Chocobo, Goblin, Bomb, Dragon…) | enemy | без спорядження, власні навички | може бути найнятий/приручений (?) |
| Knight / Monk / Squire | piece | ближній бій | Knight «ламає» спорядження чи стати ворога |
| Archer | piece | лук, дальність росте з висотою | `Aim` — заряджений постріл, сильніший |
| Black / White / Time Mage, Summoner | piece | MP, заряджені заклинання | область дії має вертикальну межу; Time Mage — Haste/Slow/Stop |
| Dragoon | piece | Jump | стрибає вгору (зникає з поля) і падає на клітину через N тіків |
| Arithmetician (Calculator) | piece | — | бʼє всіх, у кого CT/висота/рівень/Exp кратні обраному числу; миттєво |
| Geomancer | piece | — | атака залежить від типу клітини під ним |
| Thief / Mediator / Ninja / Samurai… | piece | — | крадіжка, вербування, дві зброї, «Draw Out» мечів |
| Кристал | container | — | зʼявляється на місці остаточно загиблого; союзник, що став — вчить навички або відновлює HP/MP |
| Скриня (treasure) | container | предмет | альтернатива кристалу; ставши, отримуєш предмет |
| Вода | terrain | глибина 1–2+ | глибока вода забороняє дії (?) |
| Висока клітина / обрив | terrain | різниця висот | недоступна, якщо підйом > Jump |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО для кожного юніта `counter(CT, +Speed)` (Haste ×1,5, Slow ×0,5, Stop — 0) (?).
- КОЛИ `ct_full(u)` (CT ≥ 100) → ТО `turn_start(u)`; меню Move/Act/Wait.
- КОЛИ `turn_end(u)` → ТО `counter(CT, −cost)`: Move+Act 100 · лише Move чи лише Act 80 · нічого 60; надлишок понад 100 переноситься.
- КОЛИ `input(move, u, cell)` → ЯКЩО `custom: «шлях ≤ Move клітин і кожен крок по висоті ≤ Jump»` and `free(cell)` → ТО `move(u, cell)`.
- КОЛИ `input(act, u, skill, target)` → ЯКЩО `custom: «skill миттєвий»` → ТО ефект одразу; ЯКЩО `custom: «skill заряджений»` → ТО `set_status(u, charging)` і `custom: «запис у черзі зі своєю швидкістю»`.
- КОЛИ `charge_done(skill)` → ТО ефект на **клітину**/область у момент спрацювання (хто встиг піти — не влучений); якщо кастер отримав статус, що перериває, — дія скасовується (?).
- КОЛИ `attacked(b, a)` фізично → ТО `prob(hit)`, де ухилення цілі залежить від `facing(b)`: спереду — ухилення класу + щит + аксесуар; збоку — частина; ззаду — майже нічого (?).
- Висота: дальність луків і стрільби зростає з перевагою по висоті; заклинання з областю мають вертикальну межу; Jump обмежує підйом/спуск при русі.
- Брейв/Фейт: Brave → шанс спрацювання реакцій (Counter, Hamedo) і частина фізичної шкоди; Faith → сила магії **і в атаці, і в захисті** (віруючого легше лікувати й легше вбити магією).
- Зодіак: сумісність знаків атакувальника й цілі множить шкоду/шанс (добре / погано / найкраще) (?).
- КОЛИ `attacked` → ЯКЩО `has(b, reaction)` and `prob(Brave%)` → ТО `custom: «реакція: контратака, ухилення, лікування, втеча»`.
- Статуси (`set_status` з лічильником): Poison/Regen (±HP щоходу), Haste/Slow, Stop/Sleep/Don't Move/Don't Act, Protect/Shell, Reflect, Float (ігнор висоти й води), Charm/Confuse/Berserk (AI бере керування), Petrify (вибуває), Doom (лічильник 3 → смерть), Reraise (оживає), Undead (лікування шкодить), Frog/Chicken (низька Brave), Blind, Silence, Oil, Invite (перехід на бік противника).
- КОЛИ `hp_zero(u)` → ТО `set_status(u, dead)`, над ним лічильник 3; КОЛИ його черга мала б настати → `counter(death, −1)`; оживлення (Raise, Phoenix Down) скидає.
- КОЛИ `counter(death, ==, 0)` → ТО `transform(u, crystal)` або `transform(u, chest)`; юніт загублений назавжди.
- КОЛИ `contact(ally, crystal)` → ТО `choose(вивчити навички загиблого | відновити HP/MP)`, `disappear_b`. КОЛИ `contact(ally, chest)` → ТО `give(item)`.
- КОЛИ успішна дія → ТО `custom: «EXP і JP виконавцю; частина JP — союзникам тієї ж професії»`; КОЛИ `counter(EXP, ≥, 100)` → ТО рівень +1.
- Перемога: знищити всіх ворогів або конкретну ціль (лідера). Поразка: кристалізація Рамзи, загибель гостя, якого треба вберегти, або всі юніти загону вибули.

## Керування і ввід
- Курсор по клітинах (хрестовина/стік), поворот камери на 90° (L/R), нахил, перегляд висоти клітини.
- Меню активного юніта: **Move** (підсвічені досяжні клітини) · **Act** (Attack, навичка професії, друга навичка, Item) · **Wait** (обрати напрямок погляду стрілками) · **Status**.
- Ціль дії: курсор на клітину → вікно з шансом влучання та очікуваною шкодою → підтвердження. Для заряджених — показ області.
- Між боями — курсор по світовій мапі вздовж шляхів; меню формування загону (Party roster, Equip, Abilities, Job).

## Вікна, меню, HUD
- `main-menu` / title: New Game, Continue/Load.
- `map-window` — світова мапа Іваліс: міста, точки боїв (зелені — випадкові бої), шляхи; меню формування.
- `formation` — перед боєм розставити до 5 юнітів на стартових клітинах.
- `game-screen`: ізометричне поле; панель активного юніта (портрет, HP/MP/CT, Brave/Faith, рівень, EXP); `turn-order` (список AT — хто ходить далі, з зарядженими діями) (?); `height-label` клітини під курсором; `reachable-highlight`; `hit-chance` + прогноз шкоди при наведенні на ціль.
- `job-window` — сітка професій з рівнями й JP; дерево розблокування; список навичок кожної з ціною в JP.
- Вікно спорядження й навичок юніта (Equip/Abilities: слоти Reaction/Support/Movement).
- `shop-window` (Outfitter), Soldier Office (найм), Bar/Tavern (чутки, доручення-errands), Fur Shop (WotL: «Poacher's Den»).
- `dialogue-window` катсцени; `end-screen` перемоги з трофеями; поразка → Game Over.
- `save-slots` (запис на світовій мапі), `settings-window` (швидкість повідомлень, курсор тощо) (?).

## Фічі поза полем
- `job-system`: ~20 професій, розблокування за рівнями інших; JP ростуть у бою; комбінації навичок двох професій.
- Ростер найманців (`roster-carryover`), ризик остаточної втрати (кристал), `unlockables` професій і персонажів.
- Магазини, доручення-errands (найманці йдуть на N днів) (?), випадкові бої на світовій мапі для прокачки.
- `save-slots`; 2025 Ivalice Chronicles: повна озвучка, нові рівні складності, «Classic»-версія (?).
- War of the Lions (PSP): нові професії Dark Knight/Onion Knight, кооп і versus через Wi-Fi (`local-multiplayer`).

## Варіації й родичі
- Tactics Ogre (попередник від тих самих авторів: висота, Wait-хід), Final Fantasy Tactics Advance (закони-обмеження «Law» на бій), Disgaea (гео-панелі, кидання юнітів), Triangle Strategy (висоти, оточення).
- Осі варіацій:
  - **черга ходів**: по сторонах (Wesnoth, XCOM) / по ініціативі-CT (FFT) / по кубиках і ризику (Blood Bowl);
  - **напрямок**: нема / тил і фланг дають бонус (FFT, Tactics Ogre) / тільки укриття (XCOM);
  - **висота**: нема / шари рендеру (Into the Breach) / справжня висота з Jump і дальністю (FFT);
  - **смерть**: одразу (Fire Emblem) / лічильник до остаточної (FFT, XCOM bleed-out) / травми (Blood Bowl).

## Цікавинки для курсу
- CT-шкала: черга ходів як моделювання часу (`CT += Speed`, поріг 100, ціна дії 60/80/100) — 🥉; з прогнозом списку майбутніх ходів і зарядженими діями — 🥈.
- Заряджені дії по клітині, що спрацьовують пізніше (ворог може піти) — 📎.
- Висоти + Jump: досяжність з обмеженням перепаду — 🥉 (BFS по 2.5D).
- Напрямок погляду + бонус за удар у фланг/тил — 📎.
- Лічильник смерті 3 → кристал/скриня як нагорода тому, хто встигне стати — 📎.
- Arithmetician: ціль = усі, у кого число кратне N — 🌱 але дуже «програмістська» механіка.
- Система професій: навички вчаться в одній, ставляться в інший клас — 🥈 (дерево розблокування + слоти).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ ближній бій vs луки/магія · `temporary-modes` ↔ статуси · `legal-move-highlight` + `hover-highlight` · `inventory-items` ↔ Item-команда · `shop-between-levels` + `shop-catalog` · `ai-opponent` · `save-multi-slot` · `destroy-all-enemies` · `player-death` ↔ кристалізація Рамзи · `game-screen`/`main-menu`/`end-screen`.
- **Нема** → пропозиції карток:
  - `+iso-field` (вже з Q*bert) — ізометричний рендер із поворотом камери.
  - `+movement-points` (з Wesnoth) — Move клітин + обмеження Jump.
  - `+ct-initiative` «Черга ходів за швидкістю (CT)» · game-logic/opponent · 🥉 · слот {threshold: 100, costs: {move: 20, act: 20, base: 60}}.
  - `+charged-actions` «Відкладена дія з таймером» · entities/combat · 📎 · слот {speed}.
  - `+height-levels` «Висота клітини і стрибок» · entities/legality · 🥉 · слот {jump}.
  - `+facing-hit-bonus` «Удар у фланг/тил» · entities/combat · 📎.
  - `+hit-chance` (з Wesnoth) — тут від ухилення, напрямку, Brave/Faith, зодіаку.
  - `+status-effects` (з Wesnoth) — ~25 статусів з лічильниками.
  - `+death-countdown` «Лічильник до остаточної смерті» · entities/death · 📎 · слот {turns: 3, leaves: crystal|chest}.
  - `+job-system` «Професії і перенос навичок» · entities/state · 🥈.
  - `+pilot-xp-skills` (з Into the Breach) — EXP і JP.
  - `+deployment-phase` «Розстановка загону перед боєм» · levels/progression · 📎 · слот {slots: 5}.

## Пропозиції до словників
- `+trigger:ct_full(u)` — юніт досяг порогу ініціативи; `+trigger:charge_done(skill)` — заряджена дія спрацьовує; `+trigger:attacked` (з Wesnoth) — для реакцій.
- `+cond:prob` ⏳ (шанс влучання, реакцій), `+cond:facing` ⏳ (тил/фланг), `+cond:status` / `+effect:set_status` (з Into the Breach) — статуси з лічильниками.
- `+effect:face` ⏳ — вибір напрямку в кінці ходу; `+effect:transform` — тіло → кристал/скриня.
- `+role:container` ⏳ — скриня/кристал на місці загиблого.
- `+ui:turn-order` — список черги ходів (CT/AT, ініціатива); `+ui:hit-chance` — відсоток влучання при наведенні; `+ui:height-label` — висота клітини під курсором; `+ui:reachable-highlight` (є).
- `+window:formation` — розстановка загону перед боєм; `+window:job-window` — сітка професій і навичок; `+window:map-window` ⏳; `shop-window` ✅.
- `+axis:field=layers` ⏳ — справжня висота клітин; `+axis:session` = `campaign`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Final_Fantasy_Tactics) — CT ≥ 100 і `CT += Speed`, ізометричне поле, 20 професій, JP, слоти навичок, світова мапа й міста, версії до 2025.
- [Game8: Charge Time](https://game8.co/games/Final-Fantasy-Tactics/archives/543470) — таблиця ціни ходу 100/80/80/60, перенос надлишку CT, заряджені заклинання (Fire — 4 тіки, Bahamut — 10).
- [StrategyWiki: Gameplay](https://StrategyWiki.org/wiki/Final_Fantasy_Tactics/Gameplay) — розділ механік (знайдено пошуком; не відкрився агенту).
- [Caves of Narshe](https://mail.cavesofnarshe.com/fft/walkthrough.php) — фанатський сайт з проходженням (не перевірено).
- YouTube: пошук «final fantasy tactics gameplay».

## Непевне
- (?) Вікі FF (fandom) недоступна агенту: напрямок/ухилення (фронт/фланг/тил), лічильник смерті 3 → кристал/скриня, тривалості статусів, зодіак, Brave/Faith — з памʼяті.
- (?) Наявність окремого списку черги ходів (AT list) в оригіналі PS1 — певно в War of the Lions; у PS1 — через меню/статус.
- (?) Як саме зменшується лічильник смерті (за «чергою» юніта чи за ходами).
- (?) Глибока вода: заборона дій чи лише штраф; деталі Ivalice Chronicles 2025.
- (?) Порядок дій за рівного CT.
