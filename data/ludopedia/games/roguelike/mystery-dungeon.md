---
title: Mystery Dungeon (Shiren the Wanderer, Pokémon Mystery Dungeon)
slug: mystery-dungeon
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
year: 1995
platforms: [SNES (Super Famicom), Game Boy, N64, Nintendo DS, Wii, Switch, PC (Steam), GBA]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shiren_the_Wanderer", best: true, note: "серія Shiren: формат ходу, смерть = втрата всього, Melding Jar, паролі порятунку, список ігор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mystery_Dungeon", note: "уся серія від Torneko (1993) до 2026"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mystery_Dungeon", note: "PMD: напарник, рекрутинг, порятунок друзями"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mystery_Dungeon:_Red_Rescue_Team_and_Blue_Rescue_Team", note: "перша PMD: тест особистості, дошка завдань, голод"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Shiren:The_Winds_of_Kron", note: "Mystery Dungeon Wiki: вітер Крона — ліміт ходів на поверх"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Shiren:Jar", note: "глеки: сховок, злиття, ідентифікація, кидання, ловля монстрів"}
  - {kind: other, url: "https://sharksnack.github.io/shiren-6/guides/identification-guide", note: "Shiren 6: як ідентифікувати (вжиток, ціни, назви, сувій, глек)"}
  - {kind: other, url: "https://sharksnack.github.io/shiren-6/dungeons/wanderers-highway", note: "Shiren 6: приклад підземелля — вітер, будинки монстрів, крадії"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Shiren+the+Wanderer", note: "пошук; Shiren 5+/6 на PC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shiren+the+wanderer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, dungeon-generation, sequential-levels, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, chase-player, projectile-shot, round-currency, shop-catalog, player-death, save-autosave, +rescue-password, +item-identification, +hunger-clock, +permadeath, +stairs-levels, +fov-room-lit, +throw-item, +monster-house, +floor-turn-limit, +monster-level-up, +item-container]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:hunger", "+trigger:thrown(item, target)", "+trigger:revealed", "+cond:has", "+cond:identified", "+cond:cursed", "+cond:state", "+effect:identify", "+effect:steal", "+effect:set_state", "+effect:throw(item, dir)", "+effect:fuse(a, b)", "+effect:level_up(a)", "+effect:blown_out", "+role:ally", "+role:neutral", "+role:container", "+role:hazard", "+role:stairs", "+ui:status-line", "+ui:fullness-meter", "+ui:map-overlay", "+window:inventory-window", "+window:log-window", "+window:storage-window", "+window:job-board", "+window:rescue-password", "+feature:permadeath", "+feature:rescue-by-friend", "+feature:item-storage", "+axis:session"]
author: opus
date: 2026-11-02
---

# Mystery Dungeon — консольний роглайк: голод, кидання всього підряд і вітер, що виганяє з поверху

## Суть
Серія Chunsoft (Torneko 1993 → Shiren the Wanderer 1995 → Pokémon Mystery Dungeon 2005 → Shiren 6, 2024) переносить Rogue на консолі: той самий покроковий грід, невідомі предмети й голод, але під геймпад і меню. Кожна дія героя — хід, на який відповідають усі вороги; Chunsoft порівнювала це з шахами. Фірмове: **будь-який предмет можна кинути** (і ефект ляже на ціль), **будинки монстрів**, **глеки-контейнери**, **вітер**, що виганяє з поверху за затягування, і **порятунок іншим гравцем** (паролі, пізніше онлайн). Смерть у класичному Shiren — втрата всього, що мав.

## Поле і час
- Поверх ~56×32 (?) клітин: прямокутні кімнати + коридори, генеруються щоразу; сходи вниз у випадковій кімнаті. Підземелля — 25–99 поверхів; назад піднятися не можна (лише вниз або вихід предметом).
- Камера за героєм (видно частину поверху); окремий шар-мапа (оверлей або верхній екран DS) показує розвідане: кімнати, сходи, предмети, видимих монстрів.
- Видимість: увійшов у кімнату — бачиш її всю; у коридорі — лише сусідні клітини. Пастки невидимі, доки не спрацюють або не виявлені.
- Час: 1 дія = 1 хід; монстри бувають швидкі (2 дії за хід) і повільні (раз на 2 ходи). Глобальний лічильник ходів поверху живить голод, регенерацію, спавн нових монстрів і вітер.
- Діагональ: 8 напрямків, але **не можна зрізати кут стіни** — ні ходом, ні ударом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Shiren / покемон-гравець) | player | Lv, HP, сила (Shiren), ситість %, напрям погляду | 8 напрямків; удар — у клітину перед собою; кидає, використовує, ставить предмети |
| Напарник (Koppa — лише коментує; Asuka, Sensei; PMD — партнер і рекрути) | ally | HP, рівень, тактика (PMD) | ходить слідом, бʼється сам за AI; у PMD до 4 у команді |
| Монстр (Mamel, Tainted Insect…, покемони) | enemy | Lv, HP, атака, швидкість, спецздібність | спить або бродить; помітивши — переслідує; деякі крадуть, іржавлять, кидають, ловлять кинуте |
| Монстр, що вбив іншого монстра | enemy | Lv + 1 | `level_up` у сильнішу форму виду (Mamel → більший Mamel) |
| Крамар (Shiren; PMD — Kecleon) | neutral | дуже сильний | стоїть біля входу крамниці; при неоплаті — атакує разом з охороною |
| Будинок монстрів | zone | кімната | повна сплячих монстрів і предметів; усі прокидаються при вході |
| Сходи | static | — | `next_level`; тут безпечно тестувати невідоме (можна втекти) |
| Пастка | hazard | тип; прихована | яма (падіння на поверх нижче), міна (вибух), сон, сплутаність, голод, іржа (−зброя), виклик монстрів, стріла, Wonder Tile (PMD) |
| Зброя / щит | pickup | назва відома; +N і прокляття невідомі; «печатки» (?) | екіпірування; проклятий не знімається |
| Стріли / камені | projectile | кількість у пачці | стріляють по прямій у бік погляду |
| Посох (staff) | pickup | заряди невідомі | постріл чарами по прямій: сон, телепорт геть, перетворення, обмін місцями… |
| Сувій | pickup | назва випадкова за забіг | одноразовий ефект; ідентифікується вжитком |
| Трава / насіння | pickup | назва випадкова | зʼїсти — ефект на себе; кинути — ефект на ціль |
| Глек (jar/pot) | container | місткість N слотів | покласти предмети; більшість не віддає назад, доки не розбити кидком |
| Браслет | pickup | ефект пасивний | надягти; часто з побічкою (ситість падає швидше) |
| Їжа (рисова кулька, яблуко) | pickup | +50 / +100 ситості | у повному шлунку — підвищує максимум |
| Гроші (gitan, Poké) | pickup | купка | валюта для крамниць |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` and `not cuts_corner` → ТО `move(hero, dir)`, `face(hero, dir)`; інакше `block`.
- КОЛИ `input(attack)` → ТО `custom: «удар у клітину перед собою; кидок на влучання»` → `damage(n)`; повітря — теж хід.
- КОЛИ `turn_end(hero)` → ТО усі монстри роблять свої дії (швидкі — дві).
- КОЛИ `hp_zero(enemy)` від героя → ТО `counter(xp, +n)`; КОЛИ `hp_zero(enemy)` від іншого монстра → ТО `level_up(killer)`.

Кидання (ядро консольної серії):
- КОЛИ `input(throw, item)` → ТО `throw(item, facing)`: летить по прямій до першого монстра або стіни; ЯКЩО влучив → ТО ефект предмета на ціль (`damage` для зброї/каменю, ефект трави/зілля, глек — `disappear_a` з вивільненням вмісту); ЯКЩО промах → ТО падає на підлогу.
- КОЛИ кинута трава лікування влучає в монстра → ТО `heal(monster)` — тобто кидок не завжди на користь.
- КОЛИ `thrown(item, catcher_monster)` → ТО `custom: «ловить і забирає / кидає у відповідь»`.
- КОЛИ `input(staff)` → ТО `custom: «промінь по прямій»` → перший монстр отримує ефект; `counter(charges, −1)`; порожній посох теж можна кинути.

Предмети й ідентифікація:
- КОЛИ `contact(hero, item)` → ЯКЩО `count(bag, <, limit)` → ТО `pickup`; інакше `message(«сумка повна»)`, предмет лишається.
- КОЛИ `input(use, item)` → ЯКЩО `not identified(type)` → ТО ефект + `identify(type)` (сувої, трава); глеки «натисни» — ідентифікуються при натисканні.
- КОЛИ крамар називає ціну → ТО `custom: «ціна → кандидати типу»` (ціна продажу = 40 % купівлі; благословенне ×2, прокляте −13 % у Shiren 6).
- КОЛИ `input(name, type)` → ТО `custom: «гравець дає свою назву невідомому типу»` (Checklist).
- КОЛИ `input(put, item, identify_jar)` → ТО `identify(item)` (дістати — лише розбивши глек).
- КОЛИ `input(put, weapon_a, melding_jar)` + ще `weapon_b` → ТО `fuse(a, b)`: здібності («печатки») переходять в одну зброю.

Голод:
- КОЛИ `timer(every N ходів)` → ТО `counter(fullness, −1)` (браслети/пастка голоду — швидше).
- КОЛИ `counter(fullness, ==, 0)` → ТО `hp(hero, −1)` щоходу (?) до смерті.
- КОЛИ `input(eat, riceball)` → ТО `counter(fullness, +50)`; ЯКЩО вже ситий → ТО `custom: «максимум ситості +3»` (велика кулька +100 / +4).

Вітер Крона (ліміт ходів на поверх):
- КОЛИ `level_start` → ТО `timer(start, 1000…2000)` залежно від підземелля/поверху.
- КОЛИ `timer(==, 300|200|100)` → ТО `message(попередження вітру)`.
- КОЛИ `timer(==, 0)` → ТО `blown_out`: героя виносить з підземелля — це поразка (Shiren); у PMD — провал завдання (?).
- КОЛИ `input(stairs)` → ТО лічильник скидається на новому поверсі.

Будинки монстрів і крамниці:
- КОЛИ `enter(hero, monster_house)` → ТО `set_state(all_in_room, awake)`; часто з пастками й купою предметів.
- КОЛИ `input(put, sanctuary_scroll)` на підлогу → ТО `custom: «монстри не атакують героя на цій клітині»`.
- КОЛИ `leave(hero, shop)` → ЯКЩО `has(unpaid)` → ТО `custom: «крамар і охорона ворожі»`; крадіжка можлива телепортом, ямою, моржевим глеком.

Пастки:
- КОЛИ `enter(hero, trap)` → ТО `reveal(trap)` + ефект: яма → `next_level` з шкодою, міна → `damage` і вибух сусіднього, сон → `stun(hero, n)`, іржа → `custom: «зброя/щит −1»`, виклик → `spawn_at(monsters, around)`.
- Монстри пасток не активують (?) — але героя чи монстра можна на них зіштовхнути/кинути.

Смерть і порятунок:
- КОЛИ `hp_zero(hero)` → ТО `lose`: Shiren — втрата всіх предметів і рівня, повернення в село; PMD — втрата грошей і частини предметів, ЯКЩО не врятований.
- КОЛИ `lose` → ЯКЩО гравець надіслав SOS (пароль / онлайн) and інший гравець пройшов той поверх → ТО `custom: «відродження на тому ж поверсі з усім спорядженням»`.
- Перемога: дійти до останнього поверху / виконати завдання (PMD: врятувати клієнта, доставити предмет, дійти до мети). Рахунок: явного нема — записи пригод і глибина.

## Керування і ввід
- Хрестовина — крок у 8 напрямків; кнопка-модифікатор «лише діагоналі» (стрілки показують дозволені напрямки); кнопка «повернутися без кроку» (змінити погляд, не витрачаючи хід (?)); біг (dash) до розвилки/предмета.
- Кнопка атаки — удар у бік погляду; кнопка стріляти екіпірованими стрілами; утримання двох кнопок — пропуск ходів на місці (відпочинок, витрачає вітер і ситість).
- Меню (Start/X): Сумка → предмет → Use/Throw/Put/Equip/Name/Info; «Під ногами» (footing) — предмет або пастка, на якій стоїш; Статус; Мапа/Checklist.
- PMD: кнопка ходів-атак (4 прийоми з PP), тактика для напарників, меню команди.

## Вікна, меню, HUD
- `splash-screen` → `main-menu` (продовжити, нова пригода, порятунок/пароль, налаштування).
- Хаб поза підземеллям (село Shiren / база команди PMD) — `custom-window`: склад (`storage-window`), крамниці, NPC, дошка завдань (`job-board` у PMD), поштова скринька (SOS/A-OK листи).
- `game-screen` підземелля: поле + рядок `status-line` (поверх `5F`, `Lv`, `HP поточне/макс`, гроші), смужка HP; `message-log` знизу 2–3 рядки; `map-overlay` (прозора схема поверху поверх поля або на верхньому екрані DS).
- `inventory-window` (сумка): список предметів, невідомі — іншим кольором (жовтим), з підменю дій; `custom: «Checklist»` — каталог знайдених типів з власними назвами.
- `stats-window` (статус): рівень, сила, ситість %, екіпірування, ходи.
- Діалог крамаря — ціна, купити/продати; `confirm-dialog` на сходах «Спуститися?».
- `end-screen` смерті: причина, поверх, підсумок; у Shiren — запис у «пригоди» (adventure log); у PMD — запропонувати SOS.
- `rescue-password` — введення довгого пароля (Wonder Mail / паролі порятунку) — вікно-клавіатура символів.
- `codex-window` — колекція монстрів (Shiren 2+) і довідка предметів.
- Переходи: хаб → вибір підземелля → `game-screen` поверх за поверхом → (вихід/смерть/вітер) → `end-screen` → хаб.

## Фічі поза полем
- `permadeath`-подібна смерть (втрата предметів і рівнів), але з **метапрогресом через склад**: речі, залишені в селі, переживають смерть (?) — і через злиття зброї гравець «вирощує» її між забігами.
- `rescue-by-friend`: паролі (GB2, PMD Wonder Mail), пізніше онлайн-порятунок і тижневі/челендж-підземелля.
- `save-autosave` (сейв при вході на поверх, призупинення в підземеллі).
- `puzzle-bank`: «Fay's Puzzles» — пазли-задачі на механіки, без вітру (Shiren DS).
- `mode-*`: багато підземель з власними правилами — без предметів на старті, «рівень 1 при вході», без ідентифікації, підземелля лише посохів і сувоїв.
- PMD: тест особистості на старті (`custom: «вибір героя через опитувальник»`), рекрутинг монстрів у команду, ранги рятувальної команди.

## Варіації й родичі
- Torneko's Great Adventure (1993, Dragon Quest) — перший Mystery Dungeon; Chocobo's Mysterious Dungeon (1997) — спрощений; Etrian Mystery Dungeon (2015) — загін з кількох; Mystery Chronicle: One Way Heroics — примусовий скрол.
- Родичі: Rogue / NetHack (джерело), Pixel Dungeon (мобільний аналог), Azure Dreams (підземелля + містобудування).
- Осі варіацій: **що губиш при смерті** (усе / гроші й половину / нічого, якщо врятували); **команда** (сам / напарник / 4 покемони з AI); **ліміт часу** (вітер / голод / нічого); **ідентифікація** (усе невідоме / зброя завжди відома / лише ціни); **рівень героя** (з 1 на кожне підземелля / накопичується).

## Цікавинки для курсу
- Вітер Крона: прихований лічильник ходів поверху з попередженнями 300/200/100 і виносом — простий анти-гринд — 🌱.
- `throw-item` універсальний: будь-який предмет летить по прямій, ефект визначається класом предмета на цілі — 🥉 (таблиця «клас предмета × ціль»).
- Монстр, що вбив монстра, підвищує рівень — гравець свідомо уникає «живих щитів» — 📎.
- Будинок монстрів: кімната-засідка, що прокидається разом — 📎.
- Глеки-контейнери з різними правилами (сховати / злити / ідентифікувати / вибухнути / зловити монстра) — 🥈 (рекурсивний інвентар + правила виймання).
- Порятунок іншим гравцем паролем: стан «пригоди» кодується в рядок, інший гравець його закриває — 🥇 (серіалізація + перевірка + зворотний пароль).

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `sequential-levels` (поверхи) · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `chase-player` · `projectile-shot` (стріли, посохи) · `round-currency` (gitan) · `shop-catalog` · `player-death` · `teleport-random-exit` (сувій/пастка) · `save-autosave`.
- Спільні з Rogue/NetHack: `+item-identification`, `+hunger-clock`, `+permadeath`, `+stairs-levels`, `+fov-room-lit`.
- **Нема** → пропозиції карток:
  - `+throw-item` «Кинути будь-який предмет» · entities/combat · 🥉 · слоти {range, effect_by_class}.
  - `+monster-house` «Кімната-засідка зі сплячими монстрами» · levels/generation · 📎.
  - `+floor-turn-limit` «Ліміт ходів на поверсі з попередженнями» · game-logic/lose · 🌱 · слоти {turns, warnings}.
  - `+monster-level-up` «Монстр росте, вбиваючи інших» · entities/state · 📎.
  - `+item-container` «Контейнер у інвентарі з власними правилами» · entities/state · 🥈 · слоти {capacity, extract: free|break}.
  - `+rescue-password` «Порятунок паролем від іншого гравця» · game-logic/save · 🥇.

## Пропозиції до словників
- `+trigger:thrown(item, target)` — кинутий предмет влучив у сутність (окремо від `contact`, бо ефект залежить від предмета, а не від кидаючого).
- `+effect:throw(item, dir)` — випустити предмет по прямій до першої перешкоди.
- `+effect:fuse(a, b)` — злиття двох предметів з передачею властивостей (Melding Jar).
- `+effect:level_up(a)` — сутність переходить у сильнішу форму виду.
- `+effect:blown_out` — примусовий вихід з рівня з поразкою (вітер).
- `+role:container` (глек), `+role:ally` (напарник), `+role:neutral` (крамар), `+role:hazard`, `+role:stairs`.
- `+ui:fullness-meter` — ситість у відсотках; `+ui:map-overlay` — прозора мапа поверху поверх поля.
- `+window:storage-window` (склад у хабі) · `+window:job-board` (дошка завдань PMD) · `+window:rescue-password` (ввід пароля порятунку).
- `+feature:rescue-by-friend` · `+feature:item-storage` (речі переживають смерть) · `+feature:permadeath`.
- `+trigger:input` · `+trigger:enter` · `+trigger:hunger` · `+trigger:revealed` · `+cond:has` · `+cond:identified` · `+cond:cursed` · `+cond:state` · `+effect:identify` · `+effect:steal` · `+effect:set_state` · `+ui:status-line` · `+axis:session` — як у Rogue/NetHack.

## Джерела
- ⭐ [Wikipedia: Shiren the Wanderer](https://en.wikipedia.org/wiki/Shiren_the_Wanderer) — серія, формат ходу, смерть, Melding Jar, паролі порятунку, список ігор і платформ.
- [Wikipedia: Mystery Dungeon](https://en.wikipedia.org/wiki/Mystery_Dungeon) — уся серія, порівняння з шахами, штрафи за смерть.
- [Wikipedia: Pokémon Mystery Dungeon](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mystery_Dungeon) · [Red/Blue Rescue Team](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mystery_Dungeon:_Red_Rescue_Team_and_Blue_Rescue_Team) — напарник, рекрути, дошка завдань, голод, провал місії.
- [Mystery Dungeon Wiki: The Winds of Kron](https://mysterydungeonwiki.com/wiki/Shiren:The_Winds_of_Kron) — 1000–2000 ходів, попередження 300/200/100, винос = поразка.
- [Mystery Dungeon Wiki: Jar](https://mysterydungeonwiki.com/wiki/Shiren:Jar) — чотири категорії глеків.
- [Shiren 6 Identification Guide](https://sharksnack.github.io/shiren-6/guides/identification-guide) — вжиток, ціни, Checklist, сувій/глек ідентифікації, злиття.
- [Shiren 6: Wanderers' Highway](https://sharksnack.github.io/shiren-6/dungeons/wanderers-highway) — приклад підземелля з вітром на 700 ходах і крадіями.
- YouTube: [пошук «shiren the wanderer gameplay»](https://www.youtube.com/results?search_query=shiren+the+wanderer+gameplay).

## Непевне
- (?) Розмір поверху (~56×32) і швидкість падіння ситості («−1 % за 10 ходів», «−1 HP щоходу на нулі») — з памʼяті, не перевірено (Bulbapedia й StrategyWiki не відкрились).
- (?) PMD: точні тексти попереджень вітру й те, що винос = провал місії; паролі Wonder Mail/SOS — з памʼяті.
- (?) Монстри не активують пастки — з памʼяті про Shiren.
- (?) «Печатки» (seals) на зброї й склад, що переживає смерть, — з памʼяті про Shiren DS/5; Wikipedia згадує лише Melding Jar і втрату всього.
- (?) Розкладка кнопок (діагональ-модифікатор, поворот без ходу) різна між іграми; описано узагальнено.
