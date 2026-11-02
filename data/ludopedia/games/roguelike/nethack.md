---
title: NetHack
slug: nethack
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
year: 1987
platforms: [Unix, Linux, Windows, macOS, MS-DOS, Amiga, web (публічні сервери)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/NetHack", best: true, note: "за 10 хвилин: мета, підземелля, ідентифікація, улюбленець, bones, інтерфейси"}
  - {kind: official, url: "https://www.nethack.org/", note: "офіційний сайт DevTeam; 5.0.0 від 2026-05-02, завантаження"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Elbereth", note: "NetHack Wiki: Elbereth — хто поважає, як стирається, чим гравіювати"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Sokoban", note: "гілка Sokoban: валуни, ями, штраф удачі, приз"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Luck", note: "прихована удача: джерела, спад, вплив"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Sacrifice", note: "вівтарі: жертва трупів, дари, навернення"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Shopkeeper", note: "крамарі: кирка, ціни, крадіжка, копи"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Pet", note: "улюбленці: слідують сходами, крадуть, тестують прокляття"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Polymorph", note: "поліморф себе, монстрів, предметів; пастки"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Cockatrice", note: "петрифікація: дотик, труп як зброя, ліки"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Dip", note: "занурення: Excalibur, свята вода, алхімія"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Nutrition", note: "голод: пороги, витрати, вдавитися"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Boulder", note: "валуни: штовхання, ями, протиснутися"}
  - {kind: wiki, url: "https://nethackwiki.com/wiki/Light", note: "світло/темрява, що видно, памʼять мапи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nethack+gameplay+beginner", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [interaction-table, move-8dir, dungeon-generation, push-object, hp-damage, inventory-items, item-pickup, touch-death, floor-types, console-render, save-single-slot, score-records, +item-identification, +hunger-clock, +permadeath, +remembered-map, +pet-ally, +engrave-ward, +dip-combine, +polymorph-anything, +hidden-luck, +altar-sacrifice, +shopkeeper-shop, +bones-level, +conducts]
proposes: ["+trigger:input", "+trigger:enter", "+trigger:hunger", "+trigger:revealed", "+trigger:apply(item, target)", "+cond:has", "+cond:state", "+cond:identified", "+cond:cursed", "+cond:buc(item, s)", "+cond:luck(op, n)", "+cond:respects(a, ward)", "+effect:identify", "+effect:steal", "+effect:set_state", "+effect:set_cell", "+effect:message", "+effect:polymorph(a)", "+effect:bless(item, ±1)", "+effect:erode(cell|item)", "+effect:luck(±n)", "+role:terrain", "+role:hazard", "+role:ally", "+role:neutral", "+role:stairs", "+role:altar", "+ui:status-line", "+ui:more-prompt", "+ui:farlook", "+window:tombstone", "+window:discoveries", "+window:dungeon-overview", "+window:character-create", "+feature:permadeath", "+feature:save-and-quit", "+feature:bones", "+feature:conducts", "+axis:session"]
author: opus
date: 2026-11-02
---

# NetHack — роглайк, де «DevTeam подумала про все»: кожен предмет взаємодіє з кожним

## Суть
Нащадок Rogue через Hack: `@` спускається ~50 поверхами Підземель Долі по Амулет Йендора, щоб піднестися на Астральний план і віддати його своєму богові. Ядро — не бій, а **таблиця взаємодій «усе з усім»**: занурити меч у фонтан, вигравіювати Elbereth у пилюці, вдягти рукавиці й битися трупом кокатрикса, нагодувати кошеня, щоб воно крало з крамниці, поліморфнути купу каблучок. Будь-яка дія з будь-яким предметом на будь-якій клітині має правило — і часто повідомлення-жарт. Смерть остаточна; рівень загибелі може повернутися в чужу гру як «кістки».

## Поле і час
- Мапа поверху 80×21 клітина в терміналі: рядок повідомлень зверху, два рядки статусу знизу. Камера статична — поверх уміщається на екран.
- Поверх: кімнати + коридори (як у Rogue), але є **спецрівні** з фіксованих мап (Оракул, Sokoban, Мінтаун, Велика кімната, Медуза, Замок, Долина…) і **гілки**: Гномські копальні, Sokoban, Форт Ludios, квест ролі, Gehennom. Поверх генерується при першому вході й **зберігається** — можна повернутися.
- Клітина шарувата: тип рельєфу (підлога, коридор, двері, вода, лава, лід, вівтар, фонтан, трон, мийка, дерево) + пастка + гравіювання + купа предметів + монстр. Кожен шар має власні правила.
- Хід дискретний, але не «1 дія = 1 тік»: швидкість у рухових очках (норма 12); швидкий монстр ходить двічі за хід гравця, повільний — через раз. Лічильник ходів `T:` — глобальний годинник (голод, спад удачі, регенерація, вік трупів).
- Видимість: освітлені кімнати видно цілком з лінії зору; темні клітини й коридори — лише сусідні 8. Що бачив — **запамʼятовується** на мапі (рельєф, предмети), але монстрів поза зором не видно; памʼять може застаріти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой `@` | player | роль (13), раса, стать, світогляд; St Dx Co In Wi Ch; HP, Pw, AC, Xp, удача (прихована), ситість | 8 напрямків; атака входом у клітину монстра; сотні дій-команд |
| Монстр (літера `a`–`Z`, `@`, `&`, `'`, `;`…) | enemy | ~380 видів, рівень, швидкість, атаки, резисти, розмір | більшість переслідує; багато мають спецатаки (крадуть, іржавлять, висмоктують рівень, ковтають) |
| Улюбленець (кошеня `f`, песик `d`, поні `u`) | ally | ручність 0–20, голод | слідує, бʼється сам, росте у старшу форму, не ступає на прокляте |
| Крамар `@` | neutral | рівень 12, гаманець, ключ | тримає двері, рахує ціни, при крадіжці — смертельний ворог |
| Священик храму `@` | neutral | бог вівтаря | продає захист за пожертву |
| Валун `0` / `` ` `` | object | — | штовхається, якщо за ним вільно; засипає яму/воду |
| Стіна, скеля | static | копана / некопана | непрохідна; кирка або жезл копання — прохід |
| Двері `+` `|` `-` | gate | відчинені / зачинені / замкнені / зламані / таємні | відкрити `o`, вибити `^D`, відімкнути ключем/відмичкою, через двері не можна по діагоналі |
| Сходи `<` `>` | static | — | перехід між поверхами; монстри поруч ідуть слідом |
| Пастка `^` | hazard | ~20 типів; прихована | спрацьовує при вході: стріла, капкан, яма, діра/люк (падіння нижче), телепорт, поліморф, магічна, пожежна, іржава, кротова нора рівня… |
| Вода `}` / лава `}` | terrain | — | без левітації/водоходів — тонеш / згораєш; предмети мокнуть |
| Лід `.` | terrain | — | ковзання (?) і падіння; тане від вогню |
| Вівтар `_` | terrain | світогляд | кинутий предмет «спалахує» — показує благословення/прокляття; жертва трупів |
| Фонтан `{` | terrain | — | пити `q`, занурити `#dip`: бажання, водяні мокасини, німфи, Excalibur |
| Трон `\` · мийка `#` · дерево `#` · могила `|` | terrain | — | сісти / кинути каблучку в мийку (ідентифікація) / трусити плоди / копати могилу |
| Гравіювання | terrain | текст, тип: пил / напівпостійне / постійне | читається при вході; слово Elbereth лякає більшість монстрів |
| Предмети (`)` `[` `!` `?` `/` `=` `"` `(` `%` `*` `$` `+`) | pickup | клас, вага, BUC (благословенний / звичайний / проклятий), зачарування ±N, заряди, ерозія, ідентифікованість | зникають у рюкзаку; кожна дія з ними — окреме правило |
| Труп `%` | pickup | вид монстра, вік у ходах | їжа; дає резисти; старіє і гниє; на вівтар — свіжий ≤50 ходів |
| Кокатрикс `c` | enemy | дотик кам'янить | дотик голою рукою до нього чи трупа = камінь; шипіння — відкладена петрифікація |
| Німфа `n` · леприкон `l` | enemy | — | крадуть предмет / золото й телепортуються |
| Кістки (bones) | spawner | рівень з чужої гри | привид, проклятий спадок і вбивця попереднього героя |
| Амулет Йендора `"` | pickup | вартує Верховний жрець Молоха | ціль; несучи — повільніше відновлення, ловить увагу Чарівника |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(move dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, monster)` → ТО `custom: «атака: d20 + удача + бонуси проти AC»`; ЯКЩО `occupied(cell, pet)` → ТО `swap(hero, pet)`; ЯКЩО `occupied(cell, peaceful)` → ТО `window(confirm-dialog)` «Really attack?».
- КОЛИ `input(move diag)` → ЯКЩО `cell(from|to, door)` → ТО `block` (через двері лише ортогонально).
- КОЛИ `contact(hero, boulder)` → ЯКЩО `free(cell_behind)` → ТО `push`; ЯКЩО за ним яма/діра → ТО `disappear_a`, `set_cell(floor)`; інакше ЯКЩО рюкзак майже порожній → ТО `custom: «протиснутися»`, інакше `block`.
- КОЛИ `enter(hero, trap)` → ТО ефект типу (`damage`, `stun`, `teleport(random)`, `custom: «падіння на поверх нижче»`, `polymorph(hero)`, `custom: «іржа на обладунку»`), `reveal(trap)`.
- КОЛИ `hp_zero(monster)` → ТО `disappear_b`, `spawn(corpse)` з імовірністю, `counter(xp, +n)`.

Elbereth (оберіг гравіюванням):
- КОЛИ `input(E, text)` → ТО `set_cell(engraving{text, type})`; тип залежить від інструмента: палець/більшість жезлів — пил, атам/жезл копання — напівпостійне, жезл вогню/блискавки — постійне (горить).
- КОЛИ `adjacent(monster, hero)` → ЯКЩО `cell(hero, engraving == «Elbereth»)` and `respects(monster)` → ТО `set_state(monster, fleeing)`, `custom: «не атакує впритул»`; не поважають `@`, `A`, мінотаври, крамарі, сліпі, Вершники.
- КОЛИ `input(attack)` → ЯКЩО `cell(hero, Elbereth)` → ТО `set_cell(engraving=∅)`, `custom: «−5 alignment»`.
- КОЛИ монстр тікає від Elbereth → ТО `erode(engraving)` з імовірністю (пил 100 %, напівпостійне 1/26, постійне 1/52); пил стирається й від ходіння.

Гравіювання-ідентифікація:
- КОЛИ `apply(wand, engrave)` → ТО повідомлення за типом жезла; копання, вогонь, блискавка (?) і заряджений жезл бажань — автоідентифікація; решта лише натякає повідомленням (гравіювання зникло / змінилось).

Занурення (`#dip`):
- КОЛИ `apply(long_sword, fountain)` → ЯКЩО `alignment == lawful` and `xp_level >= 5` → ТО `transform(Excalibur)`.
- КОЛИ `apply(item, holy_water)` → ТО `bless(item, +1)` (проклятий → звичайний → благословенний); unholy — навпаки.
- КОЛИ `apply(scroll, water)` → ТО `transform(blank_scroll)`; книга заклять → порожня; зілля → розбавлене → вода.
- КОЛИ `apply(item, potion_of_polymorph)` → ТО `polymorph(item)` (той самий клас).
- КОЛИ `apply(unicorn_horn, potion_of_sickness)` → ТО `transform(fruit_juice)`; сліпоти/сплутаності → вода.
- КОЛИ `apply(potion, potion)` → ТО `custom: «алхімія — таблиця пар дає нове зілля»`; стріли в отруту → отруєні.

Вівтарі, удача, молитва:
- КОЛИ `drop(item, altar)` → ТО `custom: «чорний спалах = прокляте, бурштиновий = благословенне»`, `identify(buc)`.
- КОЛИ `input(#offer, corpse)` → ЯКЩО `age(corpse) <= 50` → ТО за вартістю: зменшити гнів бога, `luck(+)`, шанс артефакту-дару; на чужому вівтарі — спроба навернення (`(XL+2)/(XL+8)`).
- КОЛИ `input(#offer, corpse_of_own_race)` → ТО хаотичному — бонус; законному/нейтральному — `luck(−5)`, гнів, вівтар стає хаотичним.
- КОЛИ `input(#pray)` → ЯКЩО `prayer_timeout == 0` and `luck >= 0` and `in_trouble` → ТО `custom: «бог лікує біду (голод, HP<1/7, камʼяніння, прокляття)»`; інакше — `custom: «гнів: прокляття, блискавка, мінус удача»`.
- Удача −10…+10 (±3 з luckstone): впливає на влучання, молитву, бажання, пошук таємних дверей. Джерела: повний місяць +1, розбите дзеркало −2, вбивство улюбленця −1, жертва, Sokoban-«чіти» −1; кожні 600 ходів спадає до бази.

Улюбленці:
- КОЛИ `input(<|>)` → ЯКЩО `adjacent(pet, hero)` and `not state(pet, eating)` → ТО `custom: «улюбленець переходить з героєм»`.
- КОЛИ `contact(pet, item)` → ЯКЩО `cursed(item)` → ТО `custom: «уникає клітини»` → гравцеві знак, що предмет проклятий.
- КОЛИ `pet` несе предмет з крамниці за двері → ТО `custom: «предмет твій, крамар не сердиться»` (класична крадіжка через улюбленця).
- КОЛИ `contact(pet, food)` → ЯКЩО їжа безпечна → ТО `custom: «їсть, ручність +»`; голодний 500+ ходів — `set_state(pet, confused)`, потім дичавіє.
- КОЛИ `hp_zero(enemy)` від улюбленця → ТО `counter(pet_xp, +)`; КОЛИ `level(pet) >= threshold` → ТО `transform(pet, grown_form)` (кошеня → кіт → великий кіт).
- КОЛИ `input(attack, pet)` → ТО ручність −; вбивство — `luck(−1)`, `custom: «−15 alignment»`.

Крамниці:
- КОЛИ `enter(hero, shop_door)` → ЯКЩО `has(hero, pick-axe)` → ТО `block`, `message(«Will you please leave your pick-axe outside?»)`.
- КОЛИ `input(,)` у крамниці → ТО `message(ціна)` → `custom: «за ціною вгадують тип невідомого предмета»`.
- КОЛИ `leave(hero, shop)` → ЯКЩО `has(unpaid)` → ТО `custom: «крамар нападає (два удари 4d4)»`, `spawn_at(keystone_kops, around)`.
- КОЛИ `damage(shop_wall)` → ТО рахунок за ремонт; відмова платити — ворожнеча.

Кокатрикс і поліморф:
- КОЛИ `contact(hero_bare_hand, cockatrice|corpse)` → ЯКЩО `not has(gloves)` and `not state(stone_res)` → ТО `lose` («turned to stone»).
- КОЛИ `input(wield, cockatrice_corpse)` → ЯКЩО `has(gloves)` → ТО атака `custom: «миттєво камʼянить ціль»`; КОЛИ падаєш у яму/діру з ним у руці → ТО `lose`.
- КОЛИ `contact(cockatrice, hero)` шипить → ТО `set_state(hero, stoning, 5)`; КОЛИ `input(eat, lizard|acidic)` → ТО `clear_state(hero, stoning)`.
- КОЛИ `enter(a, polymorph_trap)` → ТО `polymorph(a)`; герой — нова форма: HP форми, обладунок може тріснути, без рук — зброя падає; через 500–1000 ходів назад.
- КОЛИ `zap(polymorph, item_pile)` → ТО кожен предмет `transform(random_same_class)`, частина зникає; поліморф монстра — випадковий вид (шанс системного шоку 1/25).

Голод:
- КОЛИ `turn_end` → ТО `counter(nutrition, −1)`; каблучки/амулет — ще −1 кожні 20 ходів кожен. Пороги: Satiated ≥1000, Hungry <150, Weak <50, Fainting <0 (випадкові непритомності), смерть ≈ −100−10·Co. Старт 900.
- КОЛИ `input(eat)` → ЯКЩО `state(hero, satiated)` and їжа штовхає за 2000 → ТО `custom: «вдавився — смерть»` (шанс 1/20 вирвати).
- Труп: дає поживність, вид → можливий резист (вогонь, отрута, телепатія з плаваючого ока); старий — харчове отруєння.

Sokoban (гілка-головоломка):
- 4 поверхи над Оракулом; КОЛИ `input(move diag)` → ЯКЩО `contact(hero, boulder)` → ТО `block` (лише ортогональне штовхання до розвʼязання).
- КОЛИ ламаєш/поліморфиш валун, протискаєшся, стрибаєш, читаєш scroll of earth → ТО `luck(−1)`; телепорт заборонено, стіни некопані.
- КОЛИ всі ями засипано на верхньому поверсі → ТО доступ до призу: bag of holding або amulet of reflection у «зоопарку».

Світло:
- КОЛИ `enter(hero, lit_room)` → ТО `reveal(room)`; у темряві — `reveal(adjacent8)`; scroll/жезл світла — `set_cell(lit)` назавжди; проклятий/сплутаний — темрява.
- КОЛИ `set_state(hero, blind)` → ТО мапа лише з памʼяті й дотику; телепатія показує розуми монстрів на всьому поверсі.

Кінець гри:
- Перемога: піднятися з Амулетом через Площини стихій і віддати його на вівтарі свого бога на Астральному плані (ascension).
- Поразка: HP = 0, голод, камʼяніння, слиз, утоплення, задушення, «killed by a falling rock»… — понад сотню причин у тексті надгробка. Смерть остаточна; поверх смерті з імовірністю зберігається як bones.
- Рахунок: очки за досвід, золото, глибину, Амулет; топ-лист машини; «conducts» (без бажань, вегетаріанець, атеїст) — додатковий престиж.

## Керування і ввід
- Рух: `h j k l y u b n` (vi-ключі) або numpad; `Shift`/`G` + напрямок — біг до цікавого; `_` — travel (обрати клітину курсором, герой іде сам); лічильник-префікс (`20s` — шукати 20 ходів).
- Дії однією клавішею (регістр важливий): `,` підняти, `d` кинути, `i` інвентар, `e` їсти, `q` пити, `r` читати, `z` жезл, `Z` заклинання, `w` взяти зброю, `W`/`T` вдягти/зняти, `P`/`R` каблучка/амулет, `t` метнути, `f` стріляти з сагайдака, `a` застосувати інструмент, `E` гравіювати, `s` шукати, `.` чекати, `o`/`c` відчинити/зачинити, `^D` копнути, `<`/`>` сходи, `:` що тут, `;` farlook (курсор → що це), `^X` атрибути, `^P` попередні повідомлення, `S` зберегти й вийти, `O` опції, `?` довідка.
- Розширені команди `#`: `#dip`, `#pray`, `#offer`, `#chat`, `#loot`, `#force`, `#enhance`, `#sit`, `#turn`, `#ride`, `#name`, `#overview`, `#terrain`, `#conduct`.
- Після вибору дії гра питає предмет за літерою інвентаря (`What do you want to eat? [fg or ?*]`) і напрямок (`In what direction?`); `?`/`*` — меню.
- `--More--` — повідомлення не вмістилось, натисни, щоб далі; `ESC` гасить хвіст.

## Вікна, меню, HUD
- `character-create` (діалог старту): «Shall I pick character's race, role, gender and alignment for you? [ynaq]» → меню ролі (Archeologist…Wizard), раси, статі, світогляду.
- `game-screen`: мапа ASCII (або тайли в GUI-портах); `message-log` одним рядком зверху з `--More--`; два рядки `status-line` знизу: імʼя, St/Dx/Co/In/Wi/Ch, світогляд; `Dlvl`, `$`, `HP(max)`, `Pw(max)`, `AC`, `Xp`, `T:`, голод (Hungry/Weak), стани (Blind, Conf, Stun, Hallu, Stone, Slime, Burdened…).
- `inventory-window` (`i`): список за класами, кожен предмет з літерою `a`–`zA–Z`, BUC-позначкою якщо відомо, «(weapon in hand)», «(being worn)».
- Меню вибору (`pick-list`): підняти з купи, `#loot` контейнер, `#enhance` навички — оверлеї зі списком і літерами.
- `log-window` (`^P`): історія повідомлень.
- `discoveries` (`\`): усі вже ідентифіковані типи й ваші власні назви (`#name`) невідомих.
- `dungeon-overview` (`^O`/`#overview`): список відвіданих поверхів з помітними обʼєктами (вівтарі, крамниці, фонтани).
- `stats-window` (`^X`): атрибути, резисти, світогляд, божество.
- `help-window` (`?`): меню довідки — команди, клавіші, опції, історія, ліцензія.
- `settings-window` (`O`): булеві й рядкові опції (autopickup, pickup_types, number_pad, symset, runmode…), частина — лише у файлі `.nethackrc`.
- `end-screen`: «Do you want your possessions identified?» (DYWYPI) → інвентар з повною ідентифікацією → атрибути → «vanquished creatures» → conducts → `tombstone` (ASCII-надгробок RIP з причиною смерті) → `leaderboard` (топ-лист з вашим місцем).
- Переходи: старт → `character-create` → вступний текст про бога → `game-screen`; `S` → збереження і вихід; смерть → DYWYPI → надгробок → рекорди.

## Фічі поза полем
- `permadeath` + `save-and-quit` (один сейв, видаляється при завантаженні; save scumming — чітерство за звичаєм).
- `bones`: рівень смерті може потрапити в наступну гру того ж сервера з привидом, проклятими речами й убивцею.
- `conducts` — добровільні обмеження, які гра відстежує й показує (`#conduct`): pacifist, atheist, vegan, wishless, illiterate…
- `leaderboard-local` (record), `history`; на публічних серверах — онлайн-рекорди, турніри, перегляд чужих ігор у прямому ефірі (`spectator`).
- Конфіг `.nethackrc`: опції, `symset` (DECgraphics, IBMgraphics), кольори, `menucolors`, `autopickup` за класами — `custom-rules` у масштабі UX.
- Інтерфейси: tty (ASCII), curses, X11/Qt/Windows з тайлами — `dual-frontends` на одному двіжку (window-port API).
- Explore mode (`-X`, без перманентної смерті) і wizard mode (налагодження) — `mode-zen` і `cheat-codes`.
- Нема undo, підказок, редактора; генерація поверхів + спецрівні з `.des`-файлів (мова опису рівнів) — `level-from-txt`.

## Варіації й родичі
- Предки: Rogue (1980) → Hack (1982) → NetHack (1987); 3.4.3 (2003) — довга «класична» версія; 3.6 (2015); 3.7 у розробці; 5.0.0 (2026).
- Варіанти (форки): SLASH'EM, UnNetHack, SporkHack, dNetHack, xNetHack, EvilHack, GruntHack — кожен міняє таблицю взаємодій (зношення жезлів, інші вівтарі, Elbereth).
- Родичі: ADOM, Dungeon Crawl Stone Soup (протилежна філософія — «без нудних взаємодій»), Angband (без постійних поверхів), Brogue, Caves of Qud (теж «системна» глибина).
- Осі варіацій: **поверхи постійні / генеруються заново** (NetHack / Angband); **ідентифікація повна / часткова / відсутня**; **взаємодії «системні» (усе з усім) / кураторські (мало, але чесно)**; **сейв: один і стирається / вільний**.

## Цікавинки для курсу
- `interaction-table` як дані: словник `(дія, предмет, ціль) → ефект` замість if-ів — занурення, гравіювання, кидання на вівтар, поліморф. Кожен рядок — тест. 🥇 (архітектура «системних» взаємодій без комбінаторного вибуху коду).
- Elbereth: клітина-оберіг з ерозією (пил/напівпостійне/постійне) і списком винятків — 🥉.
- Улюбленець-ally з власним AI: слідує, їсть, росте, уникає проклятого (гравець читає це як інформацію!) — 🥈.
- Ідентифікація: перемішані назви на партію + BUC + перевірка на вівтарі + ціни в крамниці як дедукція — 🥈 (див. також Rogue).
- Шарована клітина (рельєф + пастка + гравіювання + купа предметів + монстр) і памʼять мапи, що може застаріти — 🥈.
- Sokoban всередині роглайка: штовхання лише ортогонально + штраф удачі за «чіти» — 📎 (повторне використання `push-object` у новому контексті).
- Bones-файли: рівень з чужої смерті в новій партії — 🥇 (серіалізація стану поверху + підміна генерації).

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `interaction-table` (головна) · `push-object` (валуни, Sokoban) · `hp-damage` · `inventory-items` + `inventory-limit` (вага, Burdened) · `item-pickup` · `floor-types` (вода, лава, лід) · `key-and-door` (ключ, відмичка, кредитка) · `teleport-random-exit` (пастка телепорту) · `touch-death` (кокатрикс) · `environment-death` · `temporary-modes` (швидкість, невидимість, левітація з таймером) · `round-currency` (золото) · `deadlock-detection` (Sokoban — гравець сам) · `console-render` + `gui-render` (tty/тайли) · `save-single-slot` · `score-records` · `keyboard-controls`.
- Спільні з Rogue пропозиції: `+item-identification`, `+hunger-clock`, `+permadeath`, `+remembered-map`, `+fov-room-lit`, `+search-hidden`, `+stairs-levels`, `+curse-item`, `+message-line`.
- **Нема** → пропозиції карток:
  - `+pet-ally` «Улюбленець-союзник з AI» · entities/move · 🥈 · слоти {follow_stairs, eats, grows}.
  - `+engrave-ward` «Клітина-оберіг» · entities/interact · 🥉 · слоти {respecters, erosion}.
  - `+dip-combine` «Застосувати предмет до предмета/клітини» · entities/interact · 🥉 · слот {table} — dip, apply, rub.
  - `+polymorph-anything` «Поліморф істоти/предмета у випадковий вид класу» · entities/state · 🥉.
  - `+hidden-luck` «Прихована характеристика, що зсуває всі кидки» · game-logic/difficulty · 📎 · слот {decay}.
  - `+altar-sacrifice` «Вівтар: перевірка BUC, жертва, дар» · entities/interact · 🥉.
  - `+shopkeeper-shop` «Крамниця на мапі з крамарем-охоронцем» · game-logic/economy · 🥈 — ціни, борг, крадіжка, копи.
  - `+bones-level` «Рівень з попередньої смерті» · levels/generation · 🥇.
  - `+conducts` «Добровільні обмеження, що відстежуються» · interface/results · 📎.

## Пропозиції до словників
- `+trigger:apply(item, target)` — гравець застосував предмет до предмета/клітини/монстра (dip, engrave, offer, rub, apply) — центральний тригер «системних» ігор.
- `+trigger:input` · `+trigger:enter` · `+trigger:hunger` · `+trigger:revealed` — як у Rogue/Chip's Challenge.
- `+cond:buc(item, s)` — благословенний/звичайний/проклятий; `+cond:luck(op, n)` — прихована удача; `+cond:respects(a, ward)` — чи поважає монстр оберіг; `+cond:has`, `+cond:state`, `+cond:identified`, `+cond:cursed`.
- `+effect:polymorph(a)` — випадкова зміна виду в межах класу (відмінно від детермінованого `transform`); `+effect:bless(item, ±1)` — зсув BUC; `+effect:erode(cell|item)` — псування гравіювання, іржа, гниль; `+effect:luck(±n)`; `+effect:identify`, `+effect:steal`, `+effect:set_state`, `+effect:set_cell`, `+effect:message`.
- `+role:ally` (улюбленець), `+role:neutral` (крамар, жрець, мирні), `+role:altar`, `+role:stairs`, `+role:terrain`, `+role:hazard`.
- `+ui:status-line` (два рядки статусу), `+ui:more-prompt` (`--More--`), `+ui:farlook` — курсор-«що це» по будь-якій клітині.
- `+window:tombstone` · `+window:discoveries` (список ідентифікованого) · `+window:dungeon-overview` (зведення поверхів) · `+window:character-create` (роль/раса/стать/світогляд).
- `+feature:permadeath` · `+feature:save-and-quit` · `+feature:bones` · `+feature:conducts`.
- `+axis:session` — тут `run` (одна довга партія з одним сейвом).

## Джерела
- ⭐ [Wikipedia: NetHack](https://en.wikipedia.org/wiki/NetHack) — мета, будова підземелля, ідентифікація, BUC, улюбленці, bones, інтерфейси, версії.
- [nethack.org](https://www.nethack.org/) — офіційні релізи (5.0.0, 2026-05-02), документація.
- [NetHack Wiki: Elbereth](https://nethackwiki.com/wiki/Elbereth) — точні правила оберегу.
- [NetHack Wiki: Sokoban](https://nethackwiki.com/wiki/Sokoban) — гілка, штрафи удачі, приз.
- [NetHack Wiki: Luck](https://nethackwiki.com/wiki/Luck) · [Sacrifice](https://nethackwiki.com/wiki/Sacrifice) · [Shopkeeper](https://nethackwiki.com/wiki/Shopkeeper) · [Pet](https://nethackwiki.com/wiki/Pet) · [Polymorph](https://nethackwiki.com/wiki/Polymorph) · [Cockatrice](https://nethackwiki.com/wiki/Cockatrice) · [Dip](https://nethackwiki.com/wiki/Dip) · [Nutrition](https://nethackwiki.com/wiki/Nutrition) · [Boulder](https://nethackwiki.com/wiki/Boulder) · [Light](https://nethackwiki.com/wiki/Light) — по одній взаємодії на сторінку, з числами.
- YouTube: [пошук «nethack gameplay beginner»](https://www.youtube.com/results?search_query=nethack+gameplay+beginner).

## Непевне
- (?) Перевірка BUC на вівтарі (чорний/бурштиновий спалах) — з памʼяті; сторінка Sacrifice цього не описує.
- (?) Перелік жезлів, що автоідентифікуються гравіюванням (копання, вогонь, блискавка), — з памʼяті; сторінка Engrave-identification не відкрилась (404).
- (?) Ковзання на льоду героя — з памʼяті; точні умови не перевірено.
- (?) Чи «падіння зі сходів з трупом кокатрикса» камʼянить — сторінка Cockatrice згадує лише ями/діри/люки.
- (?) Символ валуна: у вікі `0`, у коді за замовчуванням ще `` ` `` — залежить від конфігу.
- (?) Число ролей (13) і видів монстрів (~380) — з памʼяті для 3.6.
