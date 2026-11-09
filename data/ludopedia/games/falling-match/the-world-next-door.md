---
title: The World Next Door
slug: the-world-next-door
aka: []
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2019
platforms: [PC, macOS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_World_Next_Door_(video_game)", best: true, note: "структура: візуальна новела + данжі; три руни одного кольору — закляття, drag рун, >3 — сильніше"}
  - {kind: steam, url: "https://store.steampowered.com/app/755470/The_World_Next_Door/", note: "real-time бої, руни, Assist Mode, Versus Mode, Rose City Games / VIZ Media"}
  - {kind: official, url: "https://www.viz.com/the-world-next-door", note: "офіційна сторінка VIZ: Versus Mode, напарники"}
  - {kind: other, url: "https://spritesanddice.com/reviews/review-world-next-door/", note: "найдетальніше про бій: стати на символ, щоб узяти; fire/thunder/heal/void; Essence Runes у формі L і +; 4 напарники"}
  - {kind: other, url: "https://www.tech-gaming.com/the-world-next-door/", note: "кнопка дії на групі ≥3; 4+ рун дають спецсимволи; вороги-Grievances стріляють і бʼють впритул"}
  - {kind: other, url: "http://www.nintendoworldreport.com/review/50183/the-world-next-door-switch-review", note: "огляд Switch: червоні — fireball, зелені — лікування, 250 HP, 4 данжі з босом"}
  - {kind: other, url: "https://indiegamereviewer.com/?p=38841", note: "огляд: закляття летять / лежать пасткою / лікують; сусідні набори підсилюються; до 3 ворогів"}
  - {kind: other, url: "https://metaphorsandmoonlight.com/game-review-the-world-next-door-by-rose-city-games/", note: "огляд: Assist Mode у Settings — без шкоди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=the+world+next+door+gameplay+combat", note: "пошук; геймплей бою"}
stage: v1
coverage: 45
mechanics: [move-by-input, projectile-shot, hp-damage, status-effects, chase-player, melee-vs-ranged, destroy-all-enemies, player-death, combo-multiplier, game-screen, character-select, settings-window, +pick-up-carry-tile, +stand-on-group-cast, +connected-group-pop, +adjacent-sets-amplify, +shape-summon-ally, +assist-mode, +visual-novel-layer]
proposes: ["+cond:group_size", "+card:pick-up-carry-tile", "+card:stand-on-group-cast", "+card:adjacent-sets-amplify", "+card:shape-summon-ally", "+card:visual-novel-layer"]
author: opus
date: 2026-11-09
---

# The World Next Door — Jun бігає ареною з рун, переносить їх у групи по 3+ і, ставши на групу, кастує закляття в реальному часі

## Суть
Більшість гри — візуальна новела: школярка Jun застрягла у світі Emrys, гравець обирає репліки, з ким провести день і кого взяти в данж. Сітковий шар — бої в кімнатах святилищ: підлога арени — сітка плиток-рун, Jun ходить по ній, підбирає руну, на якій стоїть, і переносить її, щоб зібрати групу з 3+ однакових. Ставши на групу й натиснувши дію, Jun кастує закляття за кольором руни (вогняна куля, лікування, грім, «void»), а вороги-Grievances тим часом стріляють або женуться за нею. Групи з 4+ дають особливі руни; зібрані у фігуру L чи «+», вони викликають напарника.

## Поле і час
- Арена кімнати — невелика квадратна сітка плиток з рунами (розмір — ?); Jun і вороги рухаються поверх неї.
- Real-time: вороги рухаються й атакують, поки гравець переставляє руни; щоб скастувати, треба встояти на групі.
- Данж = ряд кімнат, у частині з них бої (1–3 вороги), наприкінці — бос; данжів чотири.
- Шари: плитки-руни (нижній) · Jun, вороги, снаряди, «пастки»-закляття (верхній).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Jun | player | 250 HP (NWR) | ходить ареною; бере руну під собою, несе й кладе; на групі ≥3 кастує |
| Руна | tile | колір/символ: червона, зелена, грім, фіолетова (void)… | лежить на клітині; група ≥3 однакових — готове закляття |
| Essence Rune | tile | — | зʼявляється за групу з 4+; фігура L або «+» з них — виклик напарника |
| Вогняна куля | projectile | шкода | з червоної групи летить у ворога |
| Грім | hazard | регіон групи | бʼє лише ворога, що стоїть на клітинах групи; оглушує |
| Void-сфера | projectile | шкода, сповільнення | фіолетова: шкода й коротке сповільнення цілі |
| Закляття-пастка | hazard | — | лежить на місці й бʼє ворога, що в нього входить |
| Лікування | pickup | — | зелена група відновлює частину HP Jun |
| Grievance-стрілець | enemy | HP | тримає дистанцію, кидає вогняні кулі |
| Grievance-переслідувач | enemy | HP | біжить до Jun, бʼє впритул (напр., «динозавр») |
| Бос | boss | — | додає на арену нові елементи |
| Напарник (Liza, Rainy, Horace, Cerisse) | ally | обраний перед данжем | викликається фігурою з Essence Runes: атака / лікування / вороги бʼються між собою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move)` → ТО `move(jun, dir)` ареною в реальному часі.
- КОЛИ `input(grab)` → ЯКЩО `occupied(cell_under_jun, rune)` → ТО `carry(jun, rune)` — руна їде разом із Jun.
- КОЛИ `input(drop)` → ТО `place(jun, rune)` у клітину під Jun (обмін з тією, що там лежала, — ?).
- КОЛИ `input(action)` → ЯКЩО `custom: «Jun стоїть на групі ≥3 звʼязних однакових рун»` → ТО `custom: «закляття за видом руни»`, `clear(group)` (?).
- КОЛИ `custom: «закляття червоної групи»` → ТО `spawn(fireball)`; КОЛИ `contact(fireball, enemy)` → ТО `damage(enemy, n)`, `disappear_a`.
- КОЛИ `custom: «закляття зеленої групи»` → ТО `heal(jun, n)`.
- КОЛИ `custom: «закляття грому»` → ЯКЩО `occupied(group_cells, enemy)` → ТО `damage(enemy, n)`, `stun(enemy, n)`; оглушеного легко добити снарядом.
- КОЛИ `contact(void_orb, enemy)` → ТО `damage(enemy, n)`, `speed(enemy, -k)` на мить.
- КОЛИ `contact(enemy, trap_spell)` → ТО `damage(enemy, n)` — закляття, що лежить на місці.
- КОЛИ `input(action)` → ЯКЩО `custom: «група більша за 3»` → ТО `multiplier(×k)` — сильніша шкода чи ефект.
- КОЛИ `input(action)` → ЯКЩО `custom: «кілька груп торкаються одна одної»` → ТО `multiplier(×k)` — набори підсилюють один одного.
- КОЛИ `pattern(group(4))` → ТО `spawn(essence_rune)`.
- КОЛИ `pattern(shape)` → ЯКЩО `custom: «Essence Runes утворили L або +»` → ТО `spawn(companion)`: атака, `heal(jun, n)` або `set_state(enemies, confused)` — вороги бʼються між собою й ігнорують Jun.
- КОЛИ `line_of_sight(shooter, jun)` → ТО `spawn(enemy_fireball)`; КОЛИ `contact(enemy_fireball, jun)` → ТО `damage(jun, n)`.
- КОЛИ `tick` → ТО `custom: «переслідувач іде до Jun»`; КОЛИ `adjacent(chaser, jun)` → ТО `damage(jun, n)`.
- КОЛИ `contact(enemy_attack, jun)` → ЯКЩО `mode(assist)` → ТО `custom: «шкоди нема»`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear`.
- КОЛИ `all_gone(grievances)` → ТО `custom: «кімнату очищено, далі»` (?); після боса — данж пройдено.
- КОЛИ `hp_zero(jun)` → ТО `lose`, `restart` бою (?).

## Керування і ввід
- Геймпад/клавіатура: рух Jun ареною · кнопка взяти/покласти руну, на якій стоїш · кнопка дії — кастувати групу під собою.
- Рецензенти скаржаться на «flimsy» розпізнавання: треба стояти точно на символі, легко схопити чи покласти не ту руну.
- Новельна частина: вибір реплік і того, з ким провести день.

## Вікна, меню, HUD
- `game-screen` (бій): арена-сітка рун, Jun і вороги; `hp-bar` Jun (?); напарник у загоні (?).
- `dialogue-window` — сцени новели з вибором реплік.
- `character-select` — вибір напарника на данж (Wikipedia: «pick who assists in dungeons»).
- `custom-window` — вибір, з ким провести день (?).
- `settings-window` — перемикач Assist Mode.
- `main-menu` → сюжет · Versus Mode (?).
- Переходи: новела → данж (кімнати) → бій у кімнаті → бос → новела.

## Фічі поза полем
- `assist-mode` — у Settings: Jun не отримує шкоди, бій без стресу.
- `mode-versus` — змагання з другом (деталі не знайдено).
- Репутація з персонажами залежить від вибору реплік (Steam); прокачки заклять і статів нема (Tech-Gaming).
- Сюжетний ліміт часу: повернути Jun додому, «поки не сплив час».

## Варіації й родичі
- Родичі в корпусі: `puzzle-and-dragons` (тягнеш одну кулю полем), `bejeweled` / `candy-crush` (збіг ≥3), `dungeon-raid` (збіг як атака), `puyo-puyo` (звʼязна група).
- Межа сімʼї: тут нема падіння й досипання, плитки лежать на підлозі арени; ядро — real-time бій аватара з match-3 як «магазином» заклять.
- **Осі варіацій**: хто переставляє плитки (курсор / **аватар носить, стоячи на плитці**) · як активується збіг (сам / **дія аватара, що стоїть на групі**) · ефект групи (очки / **закляття за кольором: снаряд, пастка, регіон, лікування**) · бонус (довжина / **сусідні групи / фігура L або +**).

## Цікавинки для курсу
- Аватар підбирає плитку під собою й кладе в іншому місці — 🌱.
- Пошук звʼязної групи ≥3 під аватаром і каст за кнопкою — 📎 (flood fill + стан «стоїть на групі»).
- Закляття за кольором: снаряд, пастка на місці, удар по клітинах групи, лікування — 🥉 (кілька моделей ефекту).
- Підсилення від дотичних груп і розміру групи — 📎.
- Розпізнавання фігури (L, «+») з особливих рун як виклик напарника — 📎.
- Real-time вороги двох типів (стрілець і переслідувач) поверх пазлового поля — 🥉.

## Мапа на каталог
- Є: `move-by-input` ↔ рух Jun · `projectile-shot` ↔ вогняна куля, void-сфера · `hp-damage` · `status-effects` ↔ оглушення, сповільнення · `chase-player` ↔ переслідувач · `melee-vs-ranged` ↔ два типи Grievances · `destroy-all-enemies` ↔ кімнату очищено (?) · `player-death` · `combo-multiplier` ↔ більша група / сусідні групи · `game-screen` · `character-select` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+pick-up-carry-tile` «Аватар несе плитку, на якій стоїть» · entities/interact · 🌱.
  - `+stand-on-group-cast` «Активувати групу, стоячи на ній» · entities/interact · 📎 · слоти {min: 3, adjacency: 4 (?)}.
  - `+connected-group-pop` — підтверджую (група ≥3 одного виду; тут знімається дією аватара).
  - `+adjacent-sets-amplify` «Дотичні групи підсилюють одна одну» · game-logic/score · 🌱.
  - `+shape-summon-ally` «Фігура з особливих плиток викликає союзника» · entities/spawn · 📎 · слоти {shapes: [L, plus]}.
  - `+assist-mode` — підтверджую (режим без шкоди).
  - `+visual-novel-layer` «Новельний шар між рівнями» · interface/menus · 🥉.

## Пропозиції до словників
- `+cond:group_size` — розмір звʼязної групи однакових плиток порівняно з N (≥3 для касту, >3 — підсилення); уже пропонувалось з SameGame.
- `+card:pick-up-carry-tile` — аватар підбирає плитку під собою й кладе в іншу клітину.
- `+card:stand-on-group-cast` — збіг не зникає сам, його активує аватар, що стоїть на групі.
- `+card:adjacent-sets-amplify` — групи, що торкаються, кастуються разом і сильніше.
- `+card:shape-summon-ally` — фігура заданої форми з особливих плиток викликає союзника.
- `+card:visual-novel-layer` — сюжетний шар з виборами між ігровими рівнями (The World Next Door).

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/The_World_Next_Door_(video_game)) — новела + данжі, «steps on three runes of the same color», drag рун, >3 — сильніше; Rose City Games / VIZ Media, Unity, березень 2019.
- [Steam](https://store.steampowered.com/app/755470/The_World_Next_Door/) — real-time бої, руни й допомога друзів, репутація, Assist Mode, Versus Mode.
- [VIZ](https://www.viz.com/the-world-next-door) — офіційна сторінка: Versus Mode, напарники Liza і Horace.
- [Sprites and Dice](https://spritesanddice.com/reviews/review-world-next-door/) — стояти на символі, щоб узяти; fire, thunder (регіон, оглушення), heal, void (шкода + сповільнення); Essence Runes у формі L і +; 4 напарники; Assist Mode.
- [Tech-Gaming](https://www.tech-gaming.com/the-world-next-door/) — кнопка дії на групі ≥3, 4+ рун дають спецсимволи, вороги стріляють і бʼють впритул, без прокачки.
- [Nintendo World Report](http://www.nintendoworldreport.com/review/50183/the-world-next-door-switch-review) — 3 червоні — вогняна куля, 3 зелені — лікування, 250 HP, 4 данжі з босом, 2–3 вороги.
- [Indie Game Reviewer](https://indiegamereviewer.com/?p=38841) — закляття летять / лежать / лікують, сусідні набори підсилюються, малі арени, до 3 ворогів.
- [Metaphors and Moonlight](https://metaphorsandmoonlight.com/game-review-the-world-next-door-by-rose-city-games/) — Assist Mode у Settings: без шкоди.

## Непевне
- (?) Розмір арени й сітки рун, сусідство групи (4 чи 8), чи рух Jun покроковий по клітинах, чи вільний (Tech-Gaming: «walk around freely»).
- (?) Що відбувається, коли кладеш руну на зайняту клітину (обмін чи заборона), і чи руни після касту зникають і досипаються.
- (?) Wikipedia формулює «steps on three runes» — можливо, у ранній версії збіг рахувався за пройденими рунами; огляди описують перенесення й кнопку дії.
- (?) Відповідність кольорів і заклять поза червоним (вогонь), зеленим (лікування), фіолетовим (void); точний ефект кожного з чотирьох напарників.
- (?) Кімната завершується знищенням усіх ворогів, програш — рестарт бою: прямо не підтверджено.
- (?) Як влаштований Versus Mode (спільна арена чи два поля).
- (?) Вісь `random: runtime` — припущення (вороги рухаються самі; випадковість розкладу рун не підтверджено).
