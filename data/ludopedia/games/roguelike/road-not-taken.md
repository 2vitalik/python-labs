---
title: Road Not Taken
slug: road-not-taken
aka: [RNT]
family: roguelike
also: [push-slide, falling-match]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2014
platforms: [PS4, PC, macOS, iOS, Android]
links:
  - {kind: other, url: "https://www.engadget.com/2014-08-05-road-not-taken-review-take-it.html", best: true, note: "огляд: левітація 4 сусідів, кидок по прямій, енергія 100, числа на блоках, doom spirits, вівтар, роки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Road_Not_Taken", note: "історія, платформи, патч 12.2014"}
  - {kind: steam, url: "https://store.steampowered.com/app/293740/Road_Not_Taken/", note: "Steam: Spry Fox, 5.08.2014, левітація обʼєктів, діти, створіння"}
  - {kind: other, url: "https://www.denofgeek.com/games/road-not-taken-review", note: "огляд: двері за групою обʼєктів, рецепти (2 колоди → вогонь), 15 років кар'єри, charms"}
  - {kind: other, url: "https://www.gameinformer.com/games/road_not_taken/b/pc/archive/2014/08/05/roguish-puzzling.aspx", note: "огляд: енергія від холоду й ноші, їжа й діти відновлюють, особливі обʼєкти"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "рядок у списку роглайків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Road+Not+Taken+Spry+Fox+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, swipe-gestures, impassable-cells, floor-types, interaction-table, swap-on-contact, chase-player, hp-damage, item-identification, permadeath, checkpoint, dungeon-generation, sequential-levels, collect-quota, reach-exit, run-relics, shop-between-levels, codex-window, +lift-adjacent-objects, +throw-line, +carry-energy-cost, +group-n-opens-gate, +recipe-by-collision, +low-energy-hunters, +career-years, +ban-from-pool]
proposes: ["+trigger:low_energy(n)", "+effect:lift(around)", "+ui:recipe-book", "+feature:career-years", "+card:group-n-opens-gate", "+card:carry-energy-cost"]
author: opus
date: 2026-11-09
---

# Road Not Taken — роглайк-сокобан: підняти все навколо, кинути по прямій, зібрати групу

## Суть
Рейнджер з чарівним посохом щозими йде в ліс рятувати загублених дітей. Він не штовхає, а **левітує**: піднімає всі обʼєкти в чотирьох сусідніх клітинах і **кидає** їх по прямій у бік погляду. Двері між екранами відкриваються, коли поруч зібрано потрібну кількість однакових обʼєктів; діти рятуються, коли опиняються поруч з батьками. Ходьба з ношею коштує енергії; енергія 0 — кар'єра починається спочатку. Назначення обʼєктів гра не пояснює — їх відкривають досвідом, як предмети в роглайку.

## Поле і час
- Ліс — сітка екранів-кімнат; кімната — квадратна сітка клітин, виходи на краях; рух на 1 клітину в 4 напрямки.
- Покрокова: кожен крок — хід; створіння ходять у відповідь (?).
- Рівень = один рік; набір кімнат, дітей і перешкод генерується випадково (поєднано з ручними пазлами); кар'єра — 15 років.
- Невідоме: рівень відкривається екран за екраном; що робить новий обʼєкт — невідомо до першої взаємодії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рейнджер | player | енергія (старт 100), вік | рух 4 напрямки; левітує 4 сусідів; кидає по прямій |
| Дитина | object | — | її теж носять і кидають; поруч з батьком — врятована |
| Мати / батько | static | — | на краю лісу; ціль для дитини |
| Блок-перешкода з числом (дерево «2»…) | gate | N | відкриває прохід, коли поруч N однакових обʼєктів |
| Дерево, камінь, кущ | object | тип | будівельний матеріал груп; деякі колючі |
| Колючий кущ | hazard | — | підняти/кинути — коштує енергії |
| Колода | object | — | 2 колоди → вогонь (рецепт) |
| Вогонь | object | — | на екрані з ним переміщення без витрати енергії |
| Сокира + сухе дерево | object | — | разом дають колоди |
| Вулик | object | — | у збігу випускає бджіл |
| Бджоли · єнот · вовк · яструб | enemy | — | шкодять енергії; поведінка за типом (?) |
| Ведмідь (з Triple Town) | enemy | — | перешкода, що рухається (?) |
| Бик | object | — | кинутий — вибиває блоки з місця |
| Тварина-обмінник | object | — | влучивши, міняється місцями з обʼєктом |
| Камінь-хамелеон | object | колір | змінює колір, коли кинутий у певному напрямку |
| Магнітний камінь (lodestone) | object | — | притягує блоки по лінії до рейнджера |
| Духи / doom spirits | enemy | — | при енергії ≤ 10 стають doom spirits: переслідують і замикають |
| Сніговий екран | terrain | — | кожен крок коштує енергії навіть без ноші |
| Їжа | pickup | — | відновлює енергію |
| Зілля (рецепт) | pickup | — | дає підняти один «непідйомний» блок за енергію |
| Вівтар (сірий) | switch | ціна | checkpoint: за пожертву предметів — відродження на рівні |
| Мер | neutral | — | на старті рівня; можна телепортуватись до нього, якщо замкнувся |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(lift)` → ТО `custom: «підняти всі обʼєкти в 4 сусідніх клітинах»` (`+effect:lift(around)`), `carry(objects)`.
- КОЛИ `input(throw)` → ЯКЩО `state(player, carrying)` → ТО `throw(objects, facing)` по прямій до упору (?).
- КОЛИ `input(move dir)` → ЯКЩО `state(player, carrying)` → ТО `counter(energy, −1)`.
- КОЛИ `input(lift)` → ЯКЩО `occupied(adjacent, hazard)` → ТО `counter(energy, −n)`; інші підйом і кидок — без витрати.
- КОЛИ `enter(player, snow)` → ТО `counter(energy, −1)`.
- КОЛИ `pattern(group(n))` → ЯКЩО `same(objects, type)` і `adjacent(group, gate)` (?) → ТО `disappear(gate)`, прохід відкрито.
- КОЛИ `contact(a, b)` → ЯКЩО `custom: «пара є в рецептах»` → ТО `merge(a, b → c)` (колоди → вогонь, сокира + сухе дерево → колоди), рецепт записується в книгу.
- КОЛИ `custom: «на екрані горить вогонь»` → ТО `custom: «левітація без витрати енергії»`.
- КОЛИ `pattern(group(beehive))` → ТО `spawn(bees)`.
- КОЛИ `contact(swapper, x)` → ТО `swap(swapper, x)`.
- КОЛИ `contact(bull, block)` → ТО `push(block)` (?).
- КОЛИ `adjacent(child, parent)` → ТО `disappear(child)`, `counter(rescued, +1)`, `custom: «енергія відновлюється»`.
- КОЛИ `picked(player, food)` → ТО `counter(energy, +n)`.
- КОЛИ `contact(enemy, player)` → ТО `counter(energy, −n)`.
- КОЛИ `counter(energy, <=, 10)` → ТО `transform(spirit, doom_spirit)`, `custom: «doom spirits переслідують і замикають»` (`+trigger:low_energy(n)`).
- КОЛИ `counter(energy, <=, 0)` → ТО `lose`, `custom: «кар'єра з початку»`.
- КОЛИ `input(return)` → ТО `teleport(player, mayor)` (вихід із глухого кута).
- КОЛИ `contact(player, altar)` → ЯКЩО `has(player, offering)` → ТО `take(player, offering)`, `checkpoint`.
- КОЛИ `level_end` → ЯКЩО `counter(rescued, >=, half)` → ТО `next_level`, `custom: «минув рік, рейнджер старіє»`; ЯКЩО загинув на останній дитині — `custom: «втратити майно і кілька рівнів»`.
- КОЛИ `counter(years, >=, 15)` → ТО `custom: «відставка, кар'єра закінчена»`.

## Керування і ввід
- Стрілки / стік — рух на 1 клітину; кнопка дії — підняти все навколо / кинути по прямій у бік погляду; на мобільних — свайпи (?).
- Окрема дія — повернутись до мера на початок рівня.
- Неточний кидок легко робить пазл нерозвʼязним: undo нема (?), відкат — лише через вівтар або мера.

## Вікна, меню, HUD
- `game-screen`: кімната-сітка, лічильник енергії, рятовані діти.
- `recipe-book` (`+ui:recipe-book`) — книга таємниць: відкриті рецепти і обʼєкти; як вікно — `codex-window`.
- Екран «Another year has passed» між рівнями — `end-screen` рівня.
- Село: дім рейнджера, жителі, обмін ресурсами — `custom-window` (хаб між роками).
- `main-menu` · `settings-window` (?).

## Фічі поза полем
- `permadeath` кар'єри: енергія 0 — новий рейнджер з року 1.
- `meta-progression`: charms (більше енергії, заборона певних обʼєктів у лісі) переходять між рятувальними походами; у домі можна «зберігати» тварин і предмети, щоб їх не було в лісі (`ban-from-pool`).
- Соціальна гра в селі: дружба й шлюб за ресурси (зайці, ягоди, рис, їжа, гроші) → charms і секретні рецепти; лікар коментує, скільки лишилось років.
- Патч 12.2014 змінив баланс складності (після скарг на PS4).

## Варіації й родичі
- Triple Town (`falling-match/triple-town`) — той самий студійний ДНК: групи однакових, ведмеді; тут групування відкриває двері, а не зливає в краще.
- Sokoban (`push-slide`) — замість «штовхнути 1» тут «підняти все навколо й кинути»; деадлоки ті самі.
- Роглайк-рамка: перманентна смерть, невідомі предмети (як `roguelike/rogue`), випадкові рівні.
- **Осі варіацій**: захоплення — 1 обʼєкт / усі 4 сусіди; кидок — на 1 / до упору; ціна — хід / енергія за ношу; мета групи — злиття (Triple Town) / ключ до дверей (тут).

## Цікавинки для курсу
- Підняти всі 4 сусіди і кинути по прямій — 🌱 (рух групи з різними точками зупинки — 📎).
- Блок «N однакових поруч» як замок: перевірка групи сусідів біля клітини — 📎.
- Енергія лише за ходьбу з ношею: вільний рух і дорогий транспорт — 🌱.
- Рецепти зіткненням пар із книгою відкриттів — 🌱 (таблиця взаємодій).
- Поріг енергії перемикає поведінку духів на переслідування — 📎.
- Кар'єра на 15 років + charms між походами — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `swipe-gestures` · `impassable-cells` · `floor-types` (сніг) · `interaction-table` (рецепти пар) · `swap-on-contact` (тварина-обмінник) · `chase-player` (doom spirits) · `hp-damage` (енергія як HP) · `item-identification` (обʼєкти невідомі до першої взаємодії) · `permadeath` · `checkpoint` (вівтар) · `dungeon-generation` · `sequential-levels` (роки) · `collect-quota` (половина дітей) · `reach-exit` · `run-relics` (charms) · `shop-between-levels` (обмін у селі) · `codex-window`.
- **Нема** → пропозиції карток:
  - `+lift-adjacent-objects` «Підняти всі обʼєкти навколо» · entities/interact · 🌱.
  - `+throw-line` «Кидок по прямій до упору» · entities/move · 🌱.
  - `+carry-energy-cost` «Ноша коштує ресурсу за крок» · entities/state · 🌱.
  - `+group-n-opens-gate` «N однакових поруч відкривають прохід» · entities/legality · 📎.
  - `+recipe-by-collision` «Два обʼєкти разом → новий» · entities/interact · 🌱.
  - `+low-energy-hunters` «Низький ресурс вмикає мисливців» · entities/ai · 📎.
  - `+career-years` «Забіг з N років-рівнів» · levels/progression · 🌱.
  - `+ban-from-pool` «Прибрати тип обʼєкта з генерації» · levels/generation · 🌱.

## Пропозиції до словників
- `+trigger:low_energy(n)` — ресурс гравця опустився до порогу (частковий випадок `counter`, але вартий окремого слова для роглайтів).
- `+effect:lift(around)` — підняти всі обʼєкти навколо (до `carry`, що везе один).
- `+ui:recipe-book` — книга відкритих рецептів/взаємодій.
- `+feature:career-years` — забіг розбитий на роки з віком героя.
- `+card:group-n-opens-gate` · `+card:carry-energy-cost`.

## Джерела
- ⭐ [Engadget: огляд](https://www.engadget.com/2014-08-05-road-not-taken-review-take-it.html) — левітація 4 сусідів, кидок по прямій, енергія 100, числа на блоках, doom spirits, бик, lodestone, вівтар, роки, село.
- [Den of Geek: огляд](https://www.denofgeek.com/games/road-not-taken-review) — двері за групою, діти до батьків, рецепти (колоди → вогонь), сніг, мер, 15 років, charms.
- [Game Informer: огляд](https://www.gameinformer.com/games/road_not_taken/b/pc/archive/2014/08/05/roguish-puzzling.aspx) — енергія, їжа й діти відновлюють, тварина-обмінник, камінь-хамелеон.
- [Wikipedia](https://en.wikipedia.org/wiki/Road_Not_Taken) — платформи, дати, патч.
- [Steam](https://store.steampowered.com/app/293740/Road_Not_Taken/) — опис, Spry Fox.
- YouTube: [пошук «Road Not Taken gameplay»](https://www.youtube.com/results?search_query=Road+Not+Taken+Spry+Fox+gameplay).

## Непевне
- (?) Точне правило групи: «N однакових на сусідніх клітинах блока» (Engadget) чи «N однакових поруч одне з одним» (Den of Geek); чи зникає сама група.
- (?) Кидок летить до упору чи на фіксовану відстань; що, коли кинуто кілька обʼєктів одразу.
- (?) Поведінка кожного створіння (вовк, яструб, єнот) і чи вони ходять після кожного кроку.
- (?) Скільки енергії відновлює дитина, їжа; скільки забирає колючий кущ.
- (?) Чи сімʼя — `roguelike` чи `push-slide`: черга позначила межовим випадком; лишив тут через роглайк-структуру (кар'єра, permadeath, невідомі обʼєкти), `also: [push-slide]`.
- (?) Вікна меню й налаштувань — не бачив.
