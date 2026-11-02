---
title: Shattered Pixel Dungeon (і Pixel Dungeon)
slug: pixel-dungeon
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2012
platforms: [Android, iOS, Windows, macOS, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1769170/Shattered_Pixel_Dungeon/", best: true, note: "трейлер + повний перелік: 6 героїв, 26 поверхів, 300+ предметів, 30 пасток, 9 випробувань"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shattered_Pixel_Dungeon", note: "форк Pixel Dungeon, 6 героїв, підкласи, GPLv3, релізи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pixel_Dungeon", note: "оригінал Watabou 2012: регіони, боси кожні 5 поверхів, ідентифікація, голод"}
  - {kind: official, url: "https://shatteredpixel.com/shatteredpd/", note: "офіційна сторінка гри"}
  - {kind: other, url: "https://github.com/00-Evan/shattered-pixel-dungeon", note: "відкритий код (Java, libGDX), лінки на всі магазини"}
  - {kind: other, url: "https://raw.githubusercontent.com/00-Evan/shattered-pixel-dungeon/master/core/src/main/assets/messages/journal/journal.properties", note: "тексти вбудованого посібника: пошук, ідентифікація, голод, алхімія, раптові атаки"}
  - {kind: play, url: "https://play.google.com/store/apps/details?id=com.shatteredpixel.shatteredpixeldungeon", note: "Android (безкоштовно)"}
  - {kind: play, url: "https://shattered-pixel.itch.io/shattered-pixel-dungeon", note: "itch.io, ПК"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shattered+pixel+dungeon+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, cell-click, dungeon-generation, hp-damage, inventory-items, item-pickup, key-and-door, chase-player, shop-catalog, player-death, save-autosave, score-records, difficulty-levels, +item-identification, +hunger-clock, +permadeath, +search-hidden, +stairs-levels, +item-upgrade, +talent-tree, +alchemy-recipes, +boss-floors, +surprise-attack, +throw-item, +tap-to-path]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:hunger", "+trigger:revealed", "+trigger:noticed(a, b)", "+cond:has", "+cond:identified", "+cond:cursed", "+cond:state", "+cond:str_req(item)", "+effect:identify", "+effect:upgrade(item, +1)", "+effect:brew(ingredients)", "+effect:set_state", "+effect:set_cell", "+role:terrain", "+role:hazard", "+role:boss", "+role:neutral", "+role:stairs", "+ui:quickslots", "+ui:danger-indicator", "+ui:buff-icons", "+ui:examine-button", "+window:inventory-window", "+window:hero-select", "+window:journal-window", "+window:hero-info", "+window:talent-window", "+window:challenges-window", "+feature:permadeath", "+feature:challenges", "+feature:daily-run", "+feature:seed-input", "+axis:control=indirect"]
author: opus
date: 2026-11-02
---

# Shattered Pixel Dungeon — роглайк під палець: тапни клітину, герой іде; 26 поверхів, 5 босів, сувої покращення

## Суть
Pixel Dungeon (2012, Oleg «Watabou» Dolya) — класичний покроковий роглайк, перекладений на сенсорний екран: тапаєш клітину — герой сам іде найкоротшим шляхом, тапаєш ворога — атакує. Мета як у Rogue: спуститися на 26-й поверх по Амулет Йендора; смерть остаточна. Shattered Pixel Dungeon (Evan Debenham) — головний відкритий форк: 6 героїв з підкласами й талантами, алхімія, понад 300 предметів, 30 пасток, вбудований каталог і посібник. Ядро — розподіл обмеженого ресурсу (сувої покращення, їжа, сила) між спорядженням, якого ще не ідентифіковано.

## Поле і час
- Поверх ~32×32 клітини (?) з кімнатами 100+ типів (сади, сховища, вівтарі, крамниці), коридорами, дверима; камера за героєм, пінч-зум.
- 5 регіонів по 5 поверхів: Каналізація → Вʼязниця → Печери → Місто гномів → Демонічні зали; бос на кожному 5-му поверсі; 26-й — Амулет. Поверхи **постійні**: можна підніматися назад.
- Видимість: поле зору з тінями (стіни, висока трава, двері закривають); побачене запамʼятовується; монстрів поза зором не видно.
- Хід: 1 дія = 1 хід (атака/крок мають «вартість» у часі, залежну від зброї й швидкості); вороги бувають швидшими (2 дії) чи повільнішими.
- Шари клітини: рельєф (підлога, трава, вода, прірва, вугілля, двері, таємні двері) + пастка + предмет/купа + монстр + газ/вогонь.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Warrior, Mage, Rogue, Huntress, Duelist, Cleric) | player | HP, STR (10 на старті), рівень, таланти, підклас, броньова здібність | 8 напрямків; іде за тапом; атакує ближньо або кидком |
| Монстр (60+ видів) | enemy | HP, атака, захист, ухилення, швидкість, стан сон/блукає/полює | помітивши — переслідує; деякі стріляють, крадуть (злодій), тікають |
| Бос (Goo, Tengu, DM-300, Dwarf King, Yog-Dzewa) | boss | фази | окрема арена на 5/10/15/20/25 поверсі; закриває двері до перемоги |
| NPC-квест (Sad Ghost, Old Wandmaker, Troll Blacksmith, Ambitious Imp) | neutral | — | дає завдання регіону, нагорода — вибір спорядження |
| Крамар | neutral | — | продає і купує; напад — тікає й забирає крамницю (?) |
| Двері / замкнені двері / таємні двері | gate | ключ / прихованість | замкнені — залізним ключем цього поверху; таємні — видно після пошуку |
| Скриня / кришталева скриня / гробниця | container | ключ золотий / кришталевий | відкривається ключем; кришталева — видно вміст (?) |
| Висока трава | terrain | — | закриває огляд; топчеться в низьку; з неї падають роса й насіння |
| Вода | terrain | — | гасить горіння; ворогам під водою… (?) |
| Прірва | terrain | — | стрибнути — падіння на поверх нижче з шкодою |
| Пастка (30 типів) | hazard | видима / прихована | спрацьовує при вході кого завгодно: отруйний дротик, вогонь, телепорт, тривога, параліч, виклик монстрів, гравітація… |
| Сходи вниз/вгору | static | — | перехід поверхів; на нових поверхах — підбирати сили |
| Алхімічний котел | static | — | зілля з насіння, енергія з непотребу |
| Колодязь здоровʼя / усвідомлення · жертовний вогонь · статуя | static | одноразові | лікує / відкриває мапу / нагорода за вбивство поруч / оживає й атакує |
| Зілля `!` | pickup | колір = тип, випадковий на забіг | випити або кинути (розбивається, газ/ефект на клітини) |
| Сувій | pickup | руна = тип | прочитати; upgrade +1, identify, remove curse, телепорт, магічне картографування… |
| Насіння | pickup | — | посадити → рослина-пастка з ефектом; інгредієнт алхімії |
| Зброя / броня | pickup | тир 1–5, STR-вимога, рівень +N, зачарування/гліф або прокляття | невідомі до ідентифікації: рівень `?`, можливе прокляття |
| Каблучка / жезл / артефакт | pickup | рівень; жезли з зарядами, що відновлюються | пасив / постріл / росте від використання |
| Метальна зброя (дротики, сюрикени) | projectile | кількість, зношення | кинути — шкода, частина ламається |
| Їжа (раціон, мʼясо, пасти) | pickup | ситість | скидає голод |
| Ключі (залізний / золотий / кристалічний / скелетний) | pickup | привʼязка до поверху | відкривають відповідні двері/скрині |
| Анкх | pickup | — | рятує від смерті раз |
| Амулет Йендора | pickup | 26 поверх | перемога |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(tap cell)` → ТО `custom: «шлях A*; герой іде по клітині за хід»`; зупиняється, ЯКЩО зʼявився ворог або щось помічено.
- КОЛИ `input(tap enemy)` → ЯКЩО `adjacent8(hero, enemy)` → ТО атака: `custom: «точність проти ухилення»` → `damage(n)`; інакше — іти до нього.
- КОЛИ атакує герой → ЯКЩО `state(enemy, sleeping|lost_sight)` → ТО `custom: «раптова атака — завжди влучає»` (у т.ч. одразу після дверей).
- КОЛИ `noticed(enemy, hero)` → ТО `set_state(enemy, hunting)`; сон/блукання змінюються на переслідування.
- КОЛИ `hp_zero(enemy)` → ТО `counter(xp, +n)`, `spawn(drop)` з імовірністю; КОЛИ `counter(xp, >=, next)` → ТО рівень +1, `heal`, точка таланту.

Голод:
- КОЛИ `timer(every turn)` → ТО `counter(satiety, −1)`; пороги: Hungry → Starving.
- КОЛИ `state(hero, starving)` → ТО `custom: «регенерації нема, HP повільно тане»`; інакше — HP регенерує.
- КОЛИ `input(eat)` → ТО `counter(satiety, +n)`; поради гри: не їсти на повному HP — пропадає регенерація.

Пошук і пастки:
- КОЛИ `input(search)` (лупа двічі) → ТО `reveal(hidden in adjacent / радіус)` — таємні двері й пастки; є й пасивний шанс помітити.
- КОЛИ `enter(any, trap)` → ТО ефект типу, `set_cell(trap→used)`; видимі пастки можна обходити або заманювати на них ворогів.
- КОЛИ `enter(hero, chasm)` (з підтвердженням) → ТО `next_level`, `damage(fall)`.
- КОЛИ `enter(any, tall_grass)` → ТО `set_cell(short_grass)`, `rng` → роса/насіння.

Ідентифікація, сила, покращення:
- КОЛИ `input(drink|read, item)` → ЯКЩО `not identified(type)` → ТО ефект + `identify(type)`.
- КОЛИ `input(equip, item)` → ЯКЩО `cursed(item)` → ТО `custom: «не знімається; негативне зачарування»`; інакше після N ходів/вбивств носіння — `identify(item)`.
- КОЛИ `str_req(item) > STR` → ТО штраф точності/швидкості (зброя) чи ухилення (броня); надлишок STR — бонус.
- КОЛИ `input(read, upgrade_scroll, item)` → ТО `upgrade(item, +1)`, `custom: «знімає прокляття / ослаблює»` (?); сувоїв на забіг обмежено.
- КОЛИ `input(drink, strength_potion)` → ТО `STR +1` (обмежено на забіг).

Ключі й скрині:
- КОЛИ `contact(hero, locked_door)` → ЯКЩО `has(iron_key, this_floor)` → ТО `disappear_b`, `take(key)`; інакше `block`.
- КОЛИ `contact(hero, chest)` → ЯКЩО `has(golden_key)` → ТО `custom: «відкрити»`.

Алхімія:
- КОЛИ `input(brew, alchemy_pot, 3 seeds)` → ТО `brew(seeds)` → випадкове зілля, імовірніше з тих, що відповідають насінню.
- КОЛИ `input(brew, consumable)` → ТО `counter(alchemy_energy, +n)`; енергія — валюта складних рецептів (екзотичні зілля, бомби, заклинання).

Таланти й підкласи:
- КОЛИ рівень +1 → ТО `custom: «точка таланту поточного тиру»`; КОЛИ `picked(hero, tome_of_mastery)` (після боса) → ТО `choose(subclass ×2)`; пізніше — `choose(armor_ability ×3)`.

Кінець гри:
- КОЛИ `hp_zero(hero)` → ЯКЩО `has(ankh)` → ТО `custom: «відродження»`, `take(ankh)`; інакше `lose`, `window(end-screen)`.
- КОЛИ `contact(hero, amulet)` → ТО `win` (з можливістю піднятися на поверхню за кращий результат (?)).
- Рахунок: місце в «Рейтингу» за прогресом, глибиною, золотом, вбивствами босів (?).

## Керування і ввід
- Тач: тап по клітині — йти (пошук шляху), тап по ворогу — атакувати, тап по предмету — підійти й підняти; довгий тап — опис.
- Кнопки внизу (toolbar): **чекати** (тап — 1 хід, утримання — відпочинок до відновлення), **лупа** (1 тап — оглянути клітину/обʼєкт, 2 тапи — пошук довкола), **рюкзак**, **швидкі слоти** (кидки, жезли, зілля одним тапом + ціль).
- Ціль для кидка/жезла: тап по ворогу; автонаведення на найближчого.
- ПК/геймпад: клавіші руху (8 напрямків), гарячі клавіші для слотів і дій, миша — як тап.
- Інтерфейс має режими для великого і малого екрана (Steam: «interface modes for large and small screens»).

## Вікна, меню, HUD
- `splash-screen` → `main-menu` («Enter the Dungeon», Rankings, Badges, Journal, News, Settings, About) → `hero-select` (6 героїв з описом, кнопки випробувань і seed (?)).
- `game-screen`: поле; зліва вгорі — портрет героя (`hp-bar`, XP-смужка, рівень, `buff-icons` — голод, отрута, горіння…); справа вгорі — глибина, кнопки журналу й меню; справа — `danger-indicator` (кількість видимих ворогів, тап — перемикає ціль), кнопка атаки, «підняти»/«продовжити шлях»; знизу — `toolbar` + `quickslots`; `message-log` кількома рядками.
- `inventory-window`: сітка рюкзака з вкладками контейнерів (мішечок насіння, тримач сувоїв, бандольєр зілль, кобура жезлів); тап на предмет → меню дій (вдягнути, кинути, прочитати, у слот, інфо).
- `hero-info` (тап на портрет): характеристики, бафи, вкладка `talent-window` (тири талантів з точками).
- `journal-window`: Guide (Tome of Dungeon Mastery), Alchemy Guide, Notes (орієнтири поверхів, невикористані ключі), Catalog (~500 записів — відомі типи предметів), Bestiary (монстри, боси, пастки, рослини), Documents (листи, щоденники — лор).
- `alchemy-window` (`custom-window`): слоти інгредієнтів, підказка рецепту, енергія.
- `shop-window` — тап на товар у крамниці → ціна, купити; продаж — з рюкзака.
- `pause-menu` (кнопка меню): Settings, Rankings, Challenges, Restart, Main menu, Exit.
- `settings-window`: дисплей (повний екран, яскравість, сітка), інтерфейс (розмір, режим), вводу, звуку, мови.
- `end-screen` смерті: причина → `leaderboard` (Rankings — локальні з деталями забігу).
- `achievements-window` (Badges) — 100+ досягнень.
- Переходи: main-menu → hero-select → game-screen; сходи → loading-screen → game-screen; смерть → end-screen → rankings.

## Фічі поза полем
- `permadeath` + `autosave` (сейв поверху при переході, призупинення у будь-який момент).
- `challenges`: 9 модифікаторів, що вмикаються разом (без їжі, без броні, без ідентифікації, сильніші боси, темрява…) — `custom-difficulty`.
- `unlockables`: герої відкриваються умовами; бейджі; каталог і бестіарій заповнюються між забігами.
- `daily-run` і `seed-input` (?) — повторюваний забіг за кодом.
- `rankings` (локальні рекорди з повним описом героя), `stats`.
- `localization` десятками мов (спільнота), `remap-controls`, тач/клавіатура/геймпад.
- Відкритий код (GPLv3) → `mod-support` де-факто: сотні форків.

## Варіації й родичі
- Pixel Dungeon (2012, Watabou; 4 класи, 25 рівнів + амулет) → Shattered (з 2014; 1.0 у 2021). Інші форки: Remixed, Rat King, Experienced, SPD-модифікації.
- Родичі: Rogue/NetHack (джерело), Mystery Dungeon (консольний аналог), Brogue (теж «чесний» роглайк з чистим UI).
- Осі варіацій: **ввід** (клавіатура-напрямок / тап з пошуком шляху); **покращення** (сувої = обмежений ресурс / знайдене спорядження); **ідентифікація** (вжиток / носіння N ходів / сувій); **повернення назад** (поверхи постійні / одноразові).

## Цікавинки для курсу
- Тап-до-клітини з A* і переривання ходу при появі ворога — 🥇 (пошук шляху + правило зупинки).
- Раптова атака по сплячому/«загубленому» ворогу завжди влучає — стани ворога sleep/wander/hunt — 🥉.
- Обмежені сувої покращення + невідоме спорядження: в що вкласти — 📎 (механіка), 🥈 з UI порівняння предметів.
- Алхімія: 3 насінини → зілля зі зваженою випадковістю, енергія з непотребу — 🥉.
- Журнал-каталог, що заповнюється між забігами (бестіарій, предмети, документи) — 🥈 (`codex-window` + збереження прогресу).
- Висока трава й двері як блокатори огляду, засідка за дверима — 📎.

## Мапа на каталог
- Є: `move-8dir` · `cell-click` (тап-хід) · `dungeon-generation` · `hp-damage` · `inventory-items` · `item-pickup` · `key-and-door` (залізні/золоті/кристалічні ключі) · `chase-player` · `shop-catalog` · `player-death` · `save-autosave` · `score-records` (Rankings) · `difficulty-levels` (випробування).
- Спільні з Rogue/NetHack/Mystery Dungeon: `+item-identification`, `+hunger-clock`, `+permadeath`, `+search-hidden`, `+stairs-levels`, `+throw-item`.
- **Нема** → пропозиції карток:
  - `+tap-to-path` «Тап по клітині — автошлях із перериванням» · interface/input · 🥇 · слот {interrupt_on}.
  - `+item-upgrade` «Покращення предмета +1 обмеженим ресурсом» · entities/state · 📎.
  - `+talent-tree` «Таланти за рівні, тири, підкласи» · game-logic/economy · 🥈.
  - `+alchemy-recipes` «Котел: інгредієнти → предмет» · entities/interact · 🥉 · слоти {recipes, energy}.
  - `+boss-floors` «Бос кожні N поверхів з ареною» · game-logic/waves · 🥈.
  - `+surprise-attack` «Атака по сплячому/непомітному завжди влучає» · entities/combat · 📎.

## Пропозиції до словників
- `+trigger:noticed(a, b)` — ворог помітив героя (стан сну/блукання → полювання).
- `+cond:str_req(item)` — вимога сили спорядження порівняно з STR героя.
- `+effect:upgrade(item, +1)` · `+effect:brew(ingredients)`.
- `+role:boss` · `+role:neutral` (NPC-квести, крамар) · `+role:terrain` (трава, вода, прірва) · `+role:hazard` · `+role:stairs`.
- `+ui:quickslots` (швидкі слоти з ціллю) · `+ui:danger-indicator` (лічильник видимих ворогів + перемикання цілі) · `+ui:buff-icons` · `+ui:examine-button` (лупа: огляд/пошук).
- `+window:hero-select` · `+window:journal-window` (посібник + каталог + бестіарій + нотатки) · `+window:hero-info` · `+window:talent-window` · `+window:challenges-window`.
- `+feature:challenges` (стекабельні модифікатори) · `+feature:daily-run` · `+feature:seed-input` · `+feature:permadeath`.
- `+axis:control=indirect` — тап задає ціль, хід іде сам; клавіатура — `direct`.
- `+trigger:input` · `+trigger:enter` · `+trigger:hunger` · `+trigger:revealed` · `+cond:has` · `+cond:identified` · `+cond:cursed` · `+cond:state` · `+effect:identify` · `+effect:set_state` · `+effect:set_cell` — як у Rogue/NetHack.

## Джерела
- ⭐ [Steam: Shattered Pixel Dungeon](https://store.steampowered.com/app/1769170/Shattered_Pixel_Dungeon/) — трейлер і перелік вмісту (герої, підкласи, таланти, регіони, пастки, боси, випробування, каталог).
- [Wikipedia: Shattered Pixel Dungeon](https://en.wikipedia.org/wiki/Shattered_Pixel_Dungeon) — історія форку, 6 героїв, платформи, ліцензія.
- [Wikipedia: Pixel Dungeon](https://en.wikipedia.org/wiki/Pixel_Dungeon) — оригінал: регіони, боси кожні 5 рівнів, ідентифікація, голод.
- [GitHub: shattered-pixel-dungeon](https://github.com/00-Evan/shattered-pixel-dungeon) — код і лінки на магазини.
- [journal.properties](https://raw.githubusercontent.com/00-Evan/shattered-pixel-dungeon/master/core/src/main/assets/messages/journal/journal.properties) — тексти вбудованого посібника й категорії журналу (першоджерело для UI-описів).
- [Офіційна сторінка](https://shatteredpixel.com/shatteredpd/) · [Google Play](https://play.google.com/store/apps/details?id=com.shatteredpixel.shatteredpixeldungeon) · [itch.io](https://shattered-pixel.itch.io/shattered-pixel-dungeon).
- YouTube: [пошук «shattered pixel dungeon gameplay»](https://www.youtube.com/results?search_query=shattered+pixel+dungeon+gameplay).

## Непевне
- (?) Розмір поверху, пороги голоду (Hungry/Starving у ходах), точна механіка пошуку (сусідні клітини vs радіус) — з памʼяті; фан-вікі (fandom) не відкрилась.
- (?) Імена босів і їх поверхи — з памʼяті (Wikipedia їх не наводить); Steam каже «10 bosses» — схоже, з альтернативними варіантами.
- (?) Сувій покращення знімає прокляття; ідентифікація спорядження носінням; крамар тікає при нападі; daily-run і seed-input — з памʼяті.
- (?) Типи ключів (залізний/золотий/кристалічний/скелетний) і їхні замки — з памʼяті.
- (?) Підйом на поверхню з Амулетом і формула рахунку Rankings — з памʼяті про версії 2.x.
