---
title: CiniCross
slug: cinicross
aka: []
family: pencil-logic
also: [roguelike]
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: both
  goal: state
year: 2026
platforms: [PC (Windows, Linux, Steam Deck)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3933120/CiniCross/", best: true, note: "суть: кімнати-нонограми 5×5…20×20, гілки поверхів до боса, артефакти, перманентна смерть; трейлер, демо"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3933120&count=40&maxlength=0", note: "Steam News: патчноути — боси (Leech, Shadow, Trapper, Blaze, Black Cat, Jester), артефакти, рерол, Pacifist Timer, класи, Endless"}
  - {kind: other, url: "https://shazoo.ru/2026/02/16/179669/rogalik-prevratil-spokoinye-nonogrammy-v-smertelnyi-danzen-krouler", note: "огляд RU: після нуля часу — безперервна шкода, приклади артефактів (сфера, рукавиця, кришталевий спис)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=CiniCross+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [run-length-clues, satisfy-constraints, completion-detection, cell-click, dot-mark, hp-damage, permadeath, run-relics, round-currency, shop-between-levels, shop-catalog, inventory-items, inventory-limit, difficulty-levels, character-select, map-window, save-game, game-pause, controls-remap, language-picker, +cross-mark, +mistake-damage, +time-bank, +overtime-damage, +boss-fight, +boss-rule-modifier, +hidden-clue, +node-map-run, +shop-reroll, +consumable-items, +character-classes, +endless-levels, +performance-grade, +reward-wheel, +meta-unlocks]
proposes: ["+ui:relic-charge", "+window:reward-screen", "+card:overtime-damage", "+card:performance-grade"]
author: opus
date: 2026-11-19
---

# CiniCross — роглайт-підземелля, де кожна кімната — нонограма на час, а боси міняють правила

## Суть
Темне фентезі від Hydrobates: гравець спускається поверхами підземелля, обираючи шлях гілками мапи, і кожна кімната — згенерована нонограма. Час — спільний запас на весь забіг: він тече під час пазла, а коли закінчується, герой періодично отримує шкоду; помилкова клітина теж коштує здоровʼя. Між пазлами — нагороди (артефакти, час, золото, предмети), магазини й вогнища, наприкінці поверху — бос з особливим правилом, а смерть обнуляє забіг.

## Поле і час
- Пазл — прямокутна нонограма від 5×5 до 20×20 (також 10×5, 5×10); розмір підписано над полем; глибші поверхи — складніші пазли.
- Мапа поверху — граф вузлів знизу вгору до боса: пазли з позначкою складності (0, I, II, III), магазин, вогнище, вівтар; кожен поверх має щонайменше один шлях без пазлів, складніших за середню складність +1.
- Час реальний: запас «хв:с» із множником швидкості («x0.20 Time» … «x0.75 Time» на скриншотах), що росте; нагорода за пазл додає хвилини.
- Підпис «Floor N/M» — поверх забігу (?); кількість поверхів до фіналу не бачив.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | mark | порожня / Block / Cross / Mark | Block — зафарбувати, Cross — хрестик, Mark — нотатка |
| Підказка лінії | static | серії | як у нонограмі; виконані числа тьмяніють |
| Прихована підказка | static | — | бос Shadow ховає 30 %; кожні 3 завершені клітини відкривають одну |
| Клітина-пастка | hazard | — | боси Trapper і Blaze; що саме робить — (?) |
| Герой | player | HP (50/50, 70/70 на скриншотах), клас | не стоїть на полі; HP-сфера праворуч |
| Бос | boss | HP (напр. 225), особливе правило | зафарбовані клітини шкодять йому; правило діє весь бій |
| Час | resource | запас хв:с, множник | тече під час пазла; після нуля — періодична шкода |
| Золото | resource | — | магазин і рерол нагород |
| Артефакт | pickup | стек ×N, лічильник заряду N/M | пасивний ефект до кінця забігу; тримати стільки, скільки слотів |
| Предмет | supply | слоти | одноразово: зілля, бомби, рогатка-хрестик, «очі гобліна» |
| Компаньйон | ally | — | з v1.1, клас Tamer; механіку не бачив (?) |
| Вузол мапи | zone | тип, складність 0–III | пазл / магазин / вогнище / вівтар / бос |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(block, c)` → ЯКЩО `custom: «c зафарбована в розвʼязку»` → ТО `mark(c, filled)`; у бою — `damage(boss, n)` (на скриншоті по −1 HP за клітину, з артефактами більше).
- КОЛИ `input(block, c)` → ЯКЩО `custom: «c порожня в розвʼязку»` → ТО `damage(player, n)` (?), `counter(mistakes, +1)`.
- КОЛИ `input(cross, c)` → ТО `mark(c, x)`.
- КОЛИ `input(mark, c)` → ТО `mark(c, dot)`.
- КОЛИ `tick` → ЯКЩО `custom: «іде пазл»` → ТО `timer(-dt × multiplier)`; множник росте з глибиною (?).
- КОЛИ `timer(k)` → ЯКЩО `timer(<=, 0)` and `not mode(pacifist_timer)` → ТО `damage(player, n)` — і так доки пазл не розвʼязано.
- КОЛИ `hp_zero(player)` → ТО `lose`, `custom: «забіг закінчено, новий — з нуля»`.
- КОЛИ `all_constraints_met` → ТО `window(reward_screen)`: `give(player, time)`, `currency(+gold)`, `choose(artifact)` (барабани; з v1.1 артефакт купують, часом безкоштовно), колесо предмета; розмір нагороди — за оцінкою S–F.
- КОЛИ `input(reroll)` → ЯКЩО `counter(gold, >=, cost)` → ТО `currency(-cost)`, `custom: «нові артефакти на барабанах»`; базова ціна 15, скидається щопазла.
- КОЛИ `input(node)` → ЯКЩО `custom: «вузол — наступний на гілці»` → ТО `move(player, node)`; пазл → `window(game-screen)`; магазин → `window(shop-window)`; вівтар → `choose(artifact)`.
- КОЛИ `enter(player, campfire)` → ТО `heal(player, n)`; ЯКЩО `counter(hp, ==, max)` → ТО `give(player, healing_item)`.
- КОЛИ `hp_zero(boss)` → ТО `next_level` (наступний поверх), `checkpoint` — збереження забігу наприкінці поверху, крім поверху 0.
- Особливі правила босів:
  - Leech — КОЛИ `custom: «гравець помилився»` → ТО `heal(boss, 2 % max HP)` (не більше 100 HP);
  - Shadow — КОЛИ `level_start` → ЯКЩО `prob(30)` (для кожної підказки) → ТО `hide(clue)`; КОЛИ `counter(cells_done, ==, 3k)` → ТО `reveal(one_hidden_clue)`;
  - Trapper — КОЛИ `timer(10s)` → ТО `custom: «1–3 клітини стають пастками»`;
  - Blaze — КОЛИ `level_start` → ТО `custom: «10 % клітин — пастки, не більше 10»`;
  - Black Cat — КОЛИ `timer(20s)` → ТО `custom: «екран перевертається (через затемнення)»`;
  - Jester — `rotate(clues, deg)`: підказки обертаються;
  - Sun, Dragon, Torch, Void Worm — є в патчноутах, сили не описані (?).
- Артефакти (приклади):
  - кришталевий спис — КОЛИ `input(block, c)` → ЯКЩО `prob(5)` → ТО `fill(column(c))`;
  - сфера — КОЛИ `counter(filled, ==, N)` → ТО `reveal(random_empty_cell)`;
  - рукавиця — `custom: «прощає одну помилку раз на 20 ходів»`; Hu-Gauntlet — `prob(1)` уникнути помилки;
  - Golden Sword — `damage(boss, 15)` додатково; часові сфери (Rusty / звичайна / Refined) — `custom: «змінюють плин часу»` (?).
- Предмети: «очі гобліна» — `fill(random_cells)`; Skeleton Bombs і Cross Slingshot — `place(player, item)` на поле; червоні зілля — `heal(player, n)`.
- Перемога: пройти всі поверхи до фінального боса (?). · Поразка: HP = 0. · Рахунок: оцінка S–F за пазл, позначки пройдених складностей для кожного класу.

## Керування і ввід
- Миша: Block / Cross / Mark — підписи з піктограмами кнопок біля поля (ЛКМ / ПКМ / СКМ (?)); з v1.1.4 — перепризначення всіх чотирьох дій (з використанням предмета).
- Предмет — клік по слоту, частину кладуть на поле; рерол — важіль на екрані нагород.
- Escape — пауза; мапа — клік по вузлу; геймпад частково, макет для Steam Deck (D-pad).

## Вікна, меню, HUD
- `main-menu` (перероблене у v1.1.4) → `character-select`: клас і рівень складності, позначки пройдених складностей для кожного класу.
- `map-window`: граф вузлів поверху до боса, «Floor N/M».
- `game-screen`: розмір пазла; ліворуч панель «Info» (опис артефакта, «Special Rule» боса); угорі `inventory-bar` артефактів зі стеками ×N; колонка `+ui:relic-charge` (N/M до спрацювання); праворуч `hp-bar` («70/70 HP»), `timer-countdown` з `multiplier` («x0.20 Time»), `coins` (золото), слоти предметів, легенда Block / Cross / Mark, пауза; у бою — вертикальна `hp-bar` боса з його імʼям.
- `custom-window` — заставка боса: імʼя й особливе правило.
- `+window:reward-screen`: Artifact (барабани, важіль-рерол із ціною), Time, Gold, Stats (бос, час, «Mistake(s): PERFECT»), Item (колесо з секторами ×1 / ×3), Skip.
- `shop-window`: артефакти й предмети, «Sold» після покупки.
- `tutorial-window`: навчальний пазл 5×5 з провідником-блазнем і бульбашками («Fill in the cells in this column»).
- `pause-menu` (Escape), `settings-window`: Pacifist Timer, тряска екрана, кольори підказок, простий шрифт, клавіші, мова.
- `end-screen` (?) — смерть або фінал забігу; вигляду не бачив.
- Переходи: main-menu → character-select → map-window → game-screen → reward-screen → map-window …; бос переможений → наступний поверх; HP = 0 → кінець забігу.

## Фічі поза полем
- `mode-hardcore`-подібний забіг (`permadeath`) із `continue` — збереження наприкінці кожного поверху, Steam Cloud.
- `difficulty-presets`: рівні складності від 0 (на 0 усі артефакти безкоштовні), ціни артефактів ростуть зі складністю; пройдена складність відкриває наступну для всіх класів.
- `mode-endless`: шкода подвоєна, множник часу росте вдвічі швидше.
- `assist-mode` — Pacifist Timer: без шкоди від вичерпаного часу («не рекомендовано»).
- `meta-progression`: класи Farmer, Soldier, Archer (є в демо) і Tamer (v1.1, компаньйони) з прогресом рівня (?); ланцюжки пазлів із 3-го поверху з більшою нагородою.
- `remap-controls`, `gamepad-support` (частково), `screen-shake-toggle`, `localization` (EN, FR, DE, ZH, PL, JA), `achievements`, `stats`.

## Варіації й родичі
- База — [nonogram.md](nonogram.md); роглайт із пазлом і шкодою за помилку — Demoncrawl (`hidden-deduction/demoncrawl.md`), Dragonsweeper (`hidden-deduction/dragonsweeper.md`); скелет «мапа гілками + реліквії + магазин + вогнище» — від роглайтів на кшталт Slay the Spire.
- Інші нонограми хвилі з власними правилами — [homgard.md](homgard.md), [liquidum.md](liquidum.md); штраф часу за помилку — Mario's Picross (див. nonogram.md).
- **Осі варіацій**: ціна помилки — нічого / штраф часу / HP / поразка · час — нема / ліміт пазла / банк на весь забіг з множником · модифікатор правил — нема / бос поверху / рівень складності · нагорода — нема / вибір артефакта / колесо й барабани з реролом.

## Цікавинки для курсу
- Банк часу на забіг: множник швидкості, нагороди-хвилини, періодична шкода після нуля, опція «пацифіст» — 📎.
- Помилка = шкода по HP і бос, що лікується від помилок, — 🌱 / 📎.
- Бос як модифікатор правил пазла: сховати 30 % підказок і відкривати кожні 3 клітини, пастки раз на 10 с, переворот екрана, обертання підказок — 🥉 за набір.
- Артефакти-проки зі стеками й лічильниками заряду (шанс заповнити стовпець, кожні N клітин відкрити випадкову, прощення помилки раз на 20 ходів) — 📎 за кожен, 🥉 за систему.
- Мапа поверху: граф вузлів із гарантованим «легким» шляхом до боса — 🥉.
- Генерація нонограм під складність поверху з оцінкою складності — 🥇.
- Екран нагород: барабани з реролом, ціна росте й скидається щопазла, колесо предметів, оцінка S–F — 📎.

## Мапа на каталог
- Є: `run-length-clues`, `satisfy-constraints`, `completion-detection`; `cell-click` ↔ Block / Cross; `dot-mark` ↔ Mark; `hp-damage` ↔ HP героя й боса; `permadeath`; `run-relics` ↔ артефакти; `round-currency` ↔ золото; `shop-between-levels`, `shop-catalog`; `inventory-items`, `inventory-limit` ↔ предмети й слоти артефактів; `difficulty-levels`; `character-select` ↔ класи; `map-window` ↔ мапа поверху; `save-game` ↔ збереження наприкінці поверху; `game-pause`; `controls-remap`; `language-picker`.
- **Нема** → пропозиції карток:
  - `+cross-mark` (повтор: nonogram) · `+mistake-damage` (повтор: demoncrawl) «Помилка коштує HP, а не гру».
  - `+time-bank` (повтор; тут — запас часу на весь забіг з множником швидкості) · `+overtime-damage` «Час вичерпано — шкода періодично, доки не розвʼяжеш» · game-logic/lose · 🌱 (родич `timeout-punisher`).
  - `+boss-fight` (повтор) · `+boss-rule-modifier` (повтор) «Бос-пазл з особливим правилом» · `+hidden-clue` (повтор: polimines) — частина підказок прихована.
  - `+node-map-run` (повтор) · `+shop-reroll` (повтор) · `+consumable-items` (повтор) · `+character-classes` (повтор) · `+endless-levels` (повтор) · `+meta-unlocks` (повтор).
  - `+performance-grade` «Оцінка S–F за пазл визначає нагороду» · game-logic/score · 🌱.
  - `+reward-wheel` (повтор) — колесо предметів і барабани артефактів.

## Пропозиції до словників
- `+ui:relic-charge` — лічильник «N/M» біля артефакта: скільки дій до спрацювання.
- `+window:reward-screen` — екран нагород після пазла: артефакт, час, золото, предмет, статистика.
- `+card:overtime-damage`, `+card:performance-grade` — див. мапу.

## Джерела
- ⭐ [Steam: CiniCross](https://store.steampowered.com/app/3933120/CiniCross/) — суть, 5×5…20×20, гілки поверхів, боси, артефакти (заповнюють стовпці, більші нагороди, повільніший час), «mistakes and wasted time have a cost»; скриншоти: пазл 10×5, мапа поверху, бій із Shadow («Each clue has a 30% chance of being hidden», HP боса 72/225), екран нагород, навчання.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3933120&count=40&maxlength=0) — патчі 1.0.1–1.1.4: боси й їхні правила, Pacifist Timer, збереження наприкінці поверху, гарантований легкий шлях, рерол 30 → 15, покупка артефактів, оцінка S–F, Endless, класи Farmer / Soldier / Archer / Tamer, компаньйони, перепризначення клавіш.
- [Shazoo, огляд RU](https://shazoo.ru/2026/02/16/179669/rogalik-prevratil-spokoinye-nonogrammy-v-smertelnyi-danzen-krouler) — таймер і безперервна шкода, модифікатори босів, артефакти: сфера, рукавиця (прощає помилку раз на 20 ходів), кришталевий спис.
- YouTube: пошук «CiniCross gameplay».

## Непевне
- (?) Скільки HP коштує помилка й чи хибний хрестик теж помилка — відомо лише, що помилки мають ціну, а артефакти дають шанс її уникнути.
- (?) Кількість поверхів до фіналу й що означає друге число в «Floor N/M».
- (?) Що роблять клітини-пастки, підсвічені «золоті» клітини на скриншоті (Golden Cell дає золото?), часові сфери, Void Worm (бос чи артефакт), Sun, Dragon, Torch.
- (?) Здібності класів і механіка компаньйонів — у джерелах лише назви.
- (?) Як росте множник часу: з глибиною чи з часом забігу; кнопки миші для Block / Cross / Mark.
- (?) Чи має кожна згенерована нонограма єдиний розвʼязок (Thinky Games, за результатами пошуку, радить вгадувати під тиском часу).
