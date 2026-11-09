# Картки каталогу (автоген)

Джерело: `data/catalog/tasks.yaml` · 360 карток. Теги `mechanics` у шапці гри — ці slug-и; нове — з `+`.

| slug | Назва | Зона/підзона | Монетка | Батько | Слоти | Опис |
|---|---|---|---|---|---|---|
| `projectile-shot` | Постріл | entities/combat | bronze |  |  | Снаряд як сутність, летить по прямій. |
| `shoot-modes` | Режими стрільби | entities/combat | tin |  |  | Сімʼя: вперед / черга / дріб / cooldown. |
| `shoot-forward` | Вперед | entities/combat | tin | shoot-modes |  |  |
| `shoot-burst` | Черга | entities/combat | tin | shoot-modes | shots |  |
| `shoot-spread` | Дріб | entities/combat | tin | shoot-modes | rays |  |
| `shoot-cooldown` | Cooldown | entities/combat | tin | shoot-modes | cooldown |  |
| `projectile-collision` | Зіткнення снарядів | entities/combat | tin |  |  | Анігіляція чи проліт. |
| `blast-wave` | Вибухова хвиля | entities/combat | bronze |  | radius | Хрест на N клітин. |
| `chain-detonation` | Ланцюгова детонація | entities/combat | bronze |  | delay | Вибух підриває сусідні бомби. |
| `piece-capture` | Взяття фігури | entities/combat | tin |  |  | Зняття з поля при ході на зайняту клітину. |
| `melee-vs-ranged` | Атака впритул проти дистанційної | entities/combat | bronze |  |  | Правила по типу ворога. |
| `explode-area` | Вибух площею ✍️ | entities/combat | bronze |  | shape, into | Сімʼя з blast-wave (хрест): тут — квадрат 3×3 / радіус; слот — форма; продукт вибуху — окремий слот. |
| `beam-tracing` | Трасування променя по сітці ✍️ | entities/combat | bronze |  |  | Deflektor, Khet, LaserTank, Light Up: промінь іде до перешкоди, дзеркала/поляризатори міняють шлях. |
| `line-of-sight-attack` | Атака по лінії бачення ✍️ | entities/combat | bronze |  |  | Lolo (Медуза), DROD, Hoplite (лучник): ворог бʼє, коли гравець на одній лінії без перешкод. |
| `tower-placement` | Розстановка веж на сітці ✍️ | entities/combat | bronze |  |  | Вежа займає клітини, має вартість, часом формує лабіринт (Fieldrunners). |
| `tower-range` | Радіус/форма дії вежі ✍️ | entities/combat | tin |  | shape |  |
| `bomb-fuse` | Бомба із запалом ✍️ | entities/combat | bronze |  | fuse, max_bombs | Кладеться на свою клітину, вибухає за N тіків; ліміт активних бомб. |
| `touch-death` | Смерть від дотику | entities/death | wood |  |  | Ворог/пастка вбиває. |
| `environment-death` | Смерть від середовища | entities/death | tin |  |  | Вода без колоди, вибух, камінь згори. |
| `respawn` | Респавн | entities/death | tin |  | delay | Повернення після смерті (дім привидів, checkpoint). |
| `timed-despawn` | Зникнення за часом | entities/death | wood |  | lifetime | Тимчасові предмети і платформи. |
| `death-animation` | Анімація смерті | entities/death | tin |  |  | Ефект перед зникненням. |
| `item-pickup` | Збирання | entities/interact | tin |  |  | Предмет зникає, ефект гравцеві. |
| `interaction-table` | Таблиця взаємодій | entities/interact | silver |  |  | «Що стається, коли X наступає на Y» як дані. |
| `key-and-door` | Ключ і двері | entities/interact | bronze |  |  | Сімʼя способів відкриття. |
| `teleport` | Телепорт | entities/interact | bronze |  |  | Парні портали. |
| `teleport-pair` | Парні портали | entities/interact | bronze | teleport |  |  |
| `teleport-one-way` | Односторонні | entities/interact | tin | teleport |  |  |
| `teleport-cooldown` | З cooldown | entities/interact | tin | teleport |  |  |
| `teleport-random-exit` | Випадковий вихід | entities/interact | tin | teleport |  |  |
| `floor-types` | Типи підлоги | entities/interact | silver |  |  | Лід (ковзання), вода (потрібні ласти), вогонь (Chip's Challenge). |
| `stick-together` | Злипання | entities/interact | silver |  |  | Сутності зчіплюються при контакті і рухаються разом (Sokobond). |
| `cell-transform` | Трансформація | entities/interact | tin |  |  | Клітина-перетворювач змінює тип обʼєкта (Emerald Mine). |
| `destructible-blocks` | Руйновані блоки ✍️ | entities/interact | wood |  | drops | Цегла Bomberman, стіни Wrecking Crew, гриби Centipede; слот — що лишається. |
| `dig-terrain` | Копання: земля → порожня клітина ✍️ | entities/interact | tin |  |  | Boulder Dash, Dig Dug, Mr. Do!: аватар робить тунель; земля не падає. |
| `fill-hole` | Блок засипає дірку ✍️ | entities/interact | tin |  |  | Kwirk, Pokémon Strength, A Monster's Expedition: обʼєкт у дірці стає підлогою. |
| `button-toggle` | Кнопка/важіль перемикає стан цілей ✍️ | entities/interact | bronze |  | targets | Зелена кнопка Chip's Challenge, плити Zelda, важелі Railbound; слот — цілі. |
| `mirror-reflect` | Дзеркало відбиває промінь/снаряд ✍️ | entities/interact | tin |  |  | Deflektor, LaserTank, Khet: кут дзеркала визначає новий напрямок. |
| `thief` | Злодій забирає предмети ✍️ | entities/interact | tin |  |  | Chip's Challenge (черевики), Gauntlet, NetHack: контакт = втрата інвентаря. |
| `freeze-into-block` | Ворог → блок ✍️ | entities/interact | bronze |  |  | Kickle Cubicle, Toki Tori: заморожений ворог стає обʼєктом, який можна штовхати/ставати. |
| `crush-by-slide` | Розчавити ковзним обʼєктом ✍️ | entities/interact | tin |  |  | Pengo, Kickle: блок, що ковзає, вбиває ворога на шляху. |
| `swap-on-contact` | Обмін місцями при вході ✍️ | entities/interact | tin |  |  | Baba (SWAP), Khet (скарабей): сутності міняються клітинами замість блокування. |
| `line-match-clear` | Лінія з N однакових зникає ✍️ | entities/interact | tin |  |  | Lines 98, Dr. Mario, match-3: перевірка ліній після кожного ходу. |
| `dig-hole` | Копання ями збоку-знизу ✍️ | entities/interact | tin |  |  | Аватар риє клітину по діагоналі вниз. |
| `hole-refill` | Яма заростає і ловить ✍️ | entities/interact | tin |  |  | Викопана клітина відновлюється за N тіків; хто всередині — гине. |
| `hidden-under-block` | Схований під блоком вихід або бонус ✍️ | entities/interact | wood |  |  | Видно лише після руйнування блоку зверху. |
| `periodic-sink` | Платформа періодично зникає ✍️ | entities/interact | tin |  |  | Черепахи пірнають кожні N тіків на M. |
| `stop-cell` | Клітина-гальмо ✍️ | entities/interact | wood |  |  | Зупиняє ковзання з будь-якого напрямку. |
| `shovel` | Лопата: прибрати свою рослину ✍️ | entities/interact | wood |  |  |  |
| `last-line-defense` | Остання лінія оборони ✍️ | entities/interact | tin |  |  | Газонокосарка: разове очищення смуги. |
| `placement-cooldown` | Пауза між посадками одного типу ✍️ | entities/interact | wood |  |  | Кулдаун картки рослини. |
| `impassable-cells` | Непрохідні клітини | entities/legality | wood |  |  | Стіни для всіх або для типу сутності. |
| `piece-move-patterns` | Патерни ходів фігур | entities/legality | bronze |  |  | Кінь/тура/слон як правила на сітці. |
| `legal-move-highlight` | Підсвітка легальних ходів | entities/legality | tin |  |  | Показати дозволені клітини обраної фігури. |
| `no-move-into-check` | Заборона ходу під шах | entities/legality | gold |  |  | Хід, що підставляє короля, недопустимий. |
| `tile-merge` | Злиття однакових | entities/legality | bronze |  |  | Плитки обʼєднуються за правилом. |
| `push-object` | Штовхання | entities/legality | bronze |  |  | Обʼєкт зсувається, якщо за ним вільно. |
| `pull-object` | Тягнення обʼєкта ✍️ | entities/legality | tin |  |  | Протилежність штовханню; Pushmo, Baba (PULL), Sokoban-варіант. |
| `one-way-cell` | Одностороння клітина ✍️ | entities/legality | wood |  |  | Порти Supaplex, поляризатори Deflektor, стрілки Lolo: прохід лише в одному напрямку. |
| `height-levels` | Клітини з висотою ✍️ | entities/legality | silver |  |  | Final Fantasy Tactics, Lightbot, Sausage Roll: стрибок лише на ±1 рівень, падіння з висоти. |
| `polyomino-placement` | Викладання поліоміно на сітку ✍️ | entities/legality | bronze |  |  | Blokus, Patchwork, Rampart, Tiny Towns: фігура з кількох клітин, перевірка накладання й сусідства. |
| `piece-rotate-flip` | Поворот і віддзеркалення фігури перед ходом ✍️ | entities/legality | tin |  |  | Blokus, Tetris-подібні, Ubongo. |
| `pawn-promotion` | Перетворення фігури на останньому ряду ✍️ | entities/legality | tin |  |  | Шахи, шашки (дамка), сьоґі (зона перетворення). |
| `piece-drop` | Дроп узятої фігури на поле ✍️ | entities/legality | silver |  |  | Crazyhouse, сьоґі: взяте стає своїм і ставиться з руки; рука як окрема зона. |
| `move-limit` | Ліміт ходів на рівень ✍️ | entities/legality | tin |  |  | XOR, Helltaker, Hitman GO: лічильник ходів, 0 = провал. |
| `castling` | Рокіровка ✍️ | entities/legality | tin |  |  | Король і тура одним ходом за умовами. |
| `en-passant` | Взяття на проході ✍️ | entities/legality | tin |  |  | Пішак бере пішака, що щойно пройшов повз. |
| `cursor-place` | Поставити обʼєкт курсором на вільну клітину ✍️ | entities/legality | bronze |  |  | Перевірка вільності й легальності місця. |
| `swipe-all-shift` | Один хід зсуває всі плитки ✍️ | entities/legality | tin |  |  | Увесь ряд/стовпець до упору за один ввід. |
| `merge-once-per-move` | Плитка зливається раз за хід ✍️ | entities/legality | wood |  |  | Щойно злита не зливається вдруге в тому ж ході. |
| `move-by-input` | Рух за вводом | entities/move | bronze |  |  | 4 напрямки; ввід керує переміщенням аватара. |
| `move-4dir` | 4 напрямки | entities/move | bronze | move-by-input |  |  |
| `move-8dir` | 8 напрямків (діагоналі) | entities/move | bronze | move-by-input |  |  |
| `move-auto` | Автоматичний рух, ввід змінює напрям | entities/move | bronze | move-by-input |  |  |
| `inertia-slide` | Інерція | entities/move | bronze |  |  | Ковзання до упору. |
| `gravity-fall` | Гравітація | entities/move | bronze |  |  | Падіння без опори. |
| `enemy-patrol` | Патрулювання | entities/move | bronze |  |  | Ворог туди-сюди / по маршруту. |
| `random-walk` | Випадкове блукання | entities/move | tin |  |  | З забороною розвороту на місці. |
| `chase-player` | Погоня за гравцем | entities/move | bronze |  |  | Жадібна (крок у бік цілі). |
| `chase-greedy` | Жадібна (крок у бік цілі) | entities/move | bronze | chase-player |  |  |
| `chase-bfs` | Пошук шляху BFS/A* | entities/move | gold | chase-player |  |  |
| `chase-double-move` | Два ходи ворога на один хід гравця (Theseus) | entities/move | bronze | chase-player |  |  |
| `pattern-automaton` | Патерн-автомат | entities/move | bronze |  | pattern | Жорсткий цикл ходів (слайм квадратом, скелет через такт). |
| `row-conveyor` | Конвеєрний рух ряду | entities/move | bronze |  |  | Вся смуга зсувається разом. |
| `body-queue` | Тіло-черга | entities/move | bronze |  |  | Хвіст повторює шлях голови. |
| `wrap-edges` | Тор: вихід за край → протилежний бік ✍️ | entities/move | wood |  |  | Тунель Pac-Man, Life на торі, Labyrinth; 8 ігор корпусу. |
| `wall-follower` | Ворог тримається стіни ✍️ | entities/move | bronze |  | side | Жук/парамеція Chip's Challenge, світлячки Boulder Dash; слот — якого боку. |
| `turn-when-blocked` | Поворот при упорі ✍️ | entities/move | tin |  | turn | Що робить ворог, впершись у перешкоду — сімʼя з 7 поведінок однією карткою. |
| `carrier-platform` | Платформа везе того, хто стоїть ✍️ | entities/move | tin |  |  | Колоди Frogger, плоти A Monster's Expedition, конвеєри. |
| `ladder-climb` | Драбини і перекладини ✍️ | entities/move | tin |  |  | Вертикальний рух лише по драбині; перекладини — рух руками. |
| `party-switch` | Кілька аватарів з перемиканням ✍️ | entities/move | bronze |  |  | XOR, Catrap, Kwirk: активний персонаж змінюється клавішею, решта стоять. |
| `descend-and-reverse` | Строй: біля краю | entities/move | tin |  |  | вниз і розворот ✍️ — Space Invaders, Centipede: група рухається як одне ціле. |
| `roll-off-rounded` | Камінь скочується з округлого ✍️ | entities/move | tin |  |  | Падаючий обʼєкт зсувається вбік, якщо під ним округлий обʼєкт і поруч вільно. |
| `self-collision` | Зіткнення з власним тілом ✍️ | entities/move | wood |  |  | Голова вʼїжджає у хвіст: смерть / обрізати хвіст / ігнорувати. |
| `no-reverse-turn` | Заборона розвороту на 180° ✍️ | entities/move | wood |  |  | Поворот назад ігнорується; буфер вводу наступного повороту. |
| `diagonal-gap-pass` | Діагональний прохід між кутами стін ✍️ | entities/move | tin |  |  | Ковзання по діагоналі між двома стінами, що торкаються кутами. |
| `visited-trail` | Слід пройдених клітин ✍️ | entities/move | wood |  |  | Відвідані клітини позначаються; зникає з рівня N. |
| `facing-icon` | Іконка за напрямом руху ✍️ | entities/move | bronze |  |  | Спрайт або символ сутності залежить від того, куди вона дивиться. |
| `spawn-random-cell` | Спавн у випадковій клітині | entities/spawn | wood |  |  | З перевіркою, що клітина вільна. |
| `spawn-schedule` | Спавн за розкладом | entities/spawn | tin |  | every, max_alive | Кожні N тіків / за подією. |
| `spawn-points` | Точки спавну | entities/spawn | wood |  |  | Фіксовані місця рівня (дім привидів). |
| `spawn-animation` | Поява з анімацією | entities/spawn | tin |  |  | Сутність «проявляється» кілька тіків. |
| `spawner-entity` | Сутність-генератор ✍️ | entities/spawn | bronze |  |  | Gauntlet, Chip's Challenge (клон-машина), Rogue: породжує ворогів, доки її не знищено/не натиснуто. |
| `scatter-chase-schedule` | Розклад режимів ворогів ✍️ | entities/spawn | bronze |  |  | Таймлайн розсіювання/погоні з розворотом на кожній зміні. |
| `ghost-house-release` | Вихід ворогів із дому за лічильником ✍️ | entities/spawn | tin |  |  | Випуск за кількістю зʼїдених точок або таймером простою. |
| `weighted-spawn` | Спавн зі зваженою ймовірністю ✍️ | entities/spawn | wood |  |  | Двійка з шансом 90 %, четвірка — 10 %. |
| `drop-on-death` | Знищений ворог лишає предмет ✍️ | entities/spawn | tin |  |  | Випадковий бонус із «червоного» танка. |
| `hp-damage` | HP і шкода | entities/state | tin |  | hp, who | Замість миттєвої смерті. |
| `inventory` | Інвентар | entities/state | bronze |  |  | Предмети з застосуванням. |
| `inventory-items` | Предмети з застосуванням | entities/state | bronze | inventory |  |  |
| `inventory-limit` | Ліміт місткості | entities/state | silver | inventory | capacity |  |
| `inventory-duration` | Час дії | entities/state | bronze | inventory | duration |  |
| `temporary-modes` | Тимчасові режими | entities/state | bronze |  | duration | Сила після енерджайзера, щит, переляк ворогів. |
| `speed-per-type` | Швидкість за типом | entities/state | tin |  |  | Різний темп сутностей (тіки через раз). |
| `multi-cell-size` | Розмір понад клітину | entities/state | gold |  |  | Обʼєкт 1×2/2×2, рух уздовж осі (Rush Hour). |
| `orientation-state` | Орієнтація як стан | entities/state | gold |  |  | Обʼєкт перекочується, боки різні (Sausage Roll). |
| `tile-rotate` | Поворот плитки ✍️ | entities/state | wood |  |  | Infinity Loop, Net, Dorfromantik: плитка має орієнтацію, поворот — хід або підготовка ходу. |
| `pipe-connectors` | Плитка-зʼєднувач з портами ✍️ | entities/state | wood |  |  | Pipe Mania, Net, Zenji: у плитки 1–4 виходи; звʼязок = порти збігаються. |
| `coverage-area` | Зона покриття навколо сутності ✍️ | entities/state | tin |  | shape, size | Спринклери Stardew, стовпи Factorio, опудала; слот — форма. |
| `status-effects` | Статуси зі стеками й тіком ✍️ | entities/state | bronze |  |  | Отрута, заморозка, щит на N ходів; Wildfrost, Backpack Hero, роглайки. |
| `item-identification` | Невідомі предмети до використання ✍️ | entities/state | tin |  |  | Rogue, NetHack, DCSS, Cinco Paus: назва розкривається дією. |
| `hunger-clock` | Голод як таймер ✍️ | entities/state | tin |  |  | Роглайки: лічильник падає щохід, їжа відновлює, 0 = шкода. |
| `unit-xp-skills` | Юніт набирає досвід і навички ✍️ | entities/state | bronze |  |  | Fire Emblem, Into the Breach (пілоти), Wesnoth: XP → рівень → нові вміння. |
| `blob-growth` | Аміба росте ✍️ | entities/state | bronze |  |  | Випадковий ріст; завелика → каміння, замкнена → діаманти. |
| `magic-wall-timer` | Чарівна стіна з таймером ✍️ | entities/state | tin |  |  | Стани: спить → працює → вичерпана. |
| `markup-validity` | Валідність розмітки | game-logic/constraints | bronze |  |  | Конфлікти рядка/стовпця/регіону. |
| `completion-detection` | Виявлення завершення | game-logic/constraints | tin |  |  | Всі обмеження виконані. |
| `check-stalemate` | Шах / пат | game-logic/constraints | gold |  |  | Виявлення загрози і безвиході. |
| `deadlock-detection` | Виявлення deadlock | game-logic/constraints | gold |  |  | Ящик у глухому куті. |
| `connectivity-check` | Перевірка звʼязності ✍️ | game-logic/constraints | bronze |  |  | Hashi, Net, Nurikabe, Hive: усі острови/труби/камені — одна компонента (BFS). |
| `single-loop-check` | Перевірка однієї петлі ✍️ | game-logic/constraints | bronze |  |  | Slitherlink, Masyu, Yajilin: ребра утворюють рівно один цикл. |
| `neighbor-count-clue` | Число = кількість сусідів виду ✍️ | game-logic/constraints | wood |  |  | Сапер, Light Up, Life: підказка рахує 4/8 сусідів. |
| `line-sum-clue` | Підказка на лінії ✍️ | game-logic/constraints | tin |  |  | Kakuro, Hexcells, Voltorb Flip, Skyscrapers: сума/кількість у рядку чи діагоналі. |
| `word-validation` | Перевірка слова словником ✍️ | game-logic/constraints | bronze |  |  | Scrabble, Wordle, Boggle: слово є в словнику; завантаження словника, пошук. |
| `rule-variants` | Конструктор варіантів правил ✍️ | game-logic/constraints | bronze |  |  | Lichess-варіанти, Tatham-параметри, Life B/S: набір перемикачів правил у налаштуваннях. |
| `run-length-clues` | Підказки довжин блоків ✍️ | game-logic/constraints | tin |  |  | Nonogram: числа рядка і стовпця. |
| `difficulty-levels` | Рівні складності | game-logic/difficulty | tin |  |  | Розмір поля, кількість мін/ворогів. |
| `cheat-codes` | Чіт-коди | game-logic/difficulty | tin |  |  | Безсмертя, відкриття рівнів (для демонстрації і налагодження). |
| `game-pause` | Пауза | game-logic/difficulty | wood |  |  | Заморозка тіків. |
| `skip-level` | Пропуск рівня з лімітом ✍️ | game-logic/difficulty | wood |  |  | Supaplex, Pushmo, Helltaker: N пропусків на гру. |
| `round-currency` | Валюта в раунді | game-logic/economy | bronze |  |  | Сонця/монети: генерація і витрати. |
| `shop-between-levels` | Магазин між рівнями | game-logic/economy | bronze |  |  | Покупка апгрейдів. |
| `shop-catalog` | Вітрина товарів | game-logic/economy | wood | shop-between-levels |  | Список із цінами й описами. |
| `shop-preview` | Превʼю товару | game-logic/economy | tin | shop-between-levels |  | Що дасть покупка, до покупки. |
| `shop-sales` | Знижки й розпродажі | game-logic/economy | tin | shop-between-levels |  | Тимчасові ціни, акції. |
| `shop-buyback` | Продаж назад | game-logic/economy | tin | shop-between-levels |  | Повернути куплене за частину ціни. |
| `in-round-upgrades` | Апгрейди в раунді | game-logic/economy | tin |  |  | Радіус вибуху, кількість бомб. |
| `run-relics` | Реліквії забігу ✍️ | game-logic/economy | bronze |  |  | Роглайти: пасивні предмети, що міняють правила до кінця забігу. |
| `undo-redo` | Undo/redo ходів гри | game-logic/history | tin |  |  | Сімʼя: один крок / без ліміту / redo / rewind / рестарт; 41 гра корпусу просить. |
| `undo-step` | Один крок назад | game-logic/history | tin | undo-redo |  |  |
| `undo-unlimited` | Без ліміту (стек станів) | game-logic/history | bronze | undo-redo |  |  |
| `redo` | Повернути скасоване | game-logic/history | wood | undo-redo |  |  |
| `rewind` | Безперервне перемотування часу | game-logic/history | silver | undo-redo |  | Catrap, Toki Tori, Braid-подібне |
| `restart-level` | Рестарт рівня з початку | game-logic/history | wood | undo-redo |  |  |
| `move-notation` | Запис ходів у нотації ✍️ | game-logic/history | bronze |  |  | Список ходів, перегляд назад, експорт PGN/LURD. |
| `seed-share` | Показати/ввести seed рівня ✍️ | game-logic/history | tin |  |  | Hexcells Infinite, Tatham game ID, роглайки: той самий рівень у друга. |
| `state-string` | Стан гри як рядок-код ✍️ | game-logic/history | tin |  |  | Sokoban RLE, Rush Hour 36 символів, Bloxorz level codes: копіювання й відновлення. |
| `player-death` | Смерть гравця | game-logic/lose | wood |  | lives | З варіантом кількох життів. |
| `time-out` | Вичерпано час | game-logic/lose | wood |  | limit | Таймер рівня. |
| `enemy-reached-base` | Ворог дійшов до краю/бази | game-logic/lose | wood |  |  |  |
| `no-moves-left` | Нема ходів | game-logic/lose | tin |  |  | Глухий кут. |
| `wrong-mark-lose` | Помилкова розмітка | game-logic/lose | tin |  |  | Поразка при невірно заповненій клітині (режим «like paper»). |
| `permadeath` | Одне життя, сейв стирається ✍️ | game-logic/lose | wood |  |  | Роглайки, Fire Emblem (юніт), hardcore-режими. |
| `timeout-punisher` | Карателі замість програшу по часу ✍️ | game-logic/lose | wood |  |  | Вичерпаний час спавнить сильних ворогів. |
| `hot-seat` | Hot-seat на двох | game-logic/opponent | tin |  |  | Черга ходів за однією клавіатурою. |
| `turn-enforcement` | Заборона позачергового ходу | game-logic/opponent | wood |  |  | Контроль сторони. |
| `move-timer` | Таймер ходу / шаховий годинник | game-logic/opponent | tin |  | per_move |  |
| `ai-opponent` | AI-суперник | game-logic/opponent | tin |  |  | Сімʼя за силою: випадковий → жадібний → minimax. |
| `ai-random` | Випадковий | game-logic/opponent | tin | ai-opponent |  |  |
| `ai-greedy` | Жадібний | game-logic/opponent | bronze | ai-opponent |  |  |
| `ai-minimax` | Minimax | game-logic/opponent | gold | ai-opponent | depth |  |
| `realtime-ai` | AI в реальному часі | game-logic/opponent | gold |  |  | Виживання проти Tron-змійки. |
| `pass-turn` | Пас, коли нема ходів ✍️ | game-logic/opponent | wood |  |  | Reversi, Ataxx, Onitama, го: хід переходить без дії. |
| `repetition-draw` | Нічия повторенням позиції ✍️ | game-logic/opponent | tin |  |  | Триразове повторення, ко в го, правило 50 ходів. |
| `garbage-attack` | Сміття супернику у versus ✍️ | game-logic/opponent | silver |  |  | Tetris, Puyo, Dr. Mario: ланцюг у гравця → рядки/краплі у суперника; offset. |
| `simultaneous-versus` | Два поля одночасно ✍️ | game-logic/opponent | silver |  |  | Puyo, Tetris 99, Take It Easy: однакові умови, перемога за швидкістю/виживанням. |
| `async-multiplayer` | Хід поштою ✍️ | game-logic/opponent | silver |  |  | Letterpress, Words With Friends: партія триває днями, нотифікації про хід. |
| `online-multiplayer` | Онлайн-партія ✍️ | game-logic/opponent | gold |  |  | Синхронізація стану через сервер/сокет; лобі, рейтинг — окремі картки. |
| `command-program` | Програма команд для сутності ✍️ | game-logic/program | bronze |  |  | Karel, Lightbot: список команд виконується після запуску. |
| `user-procedures` | Власні процедури/функції ✍️ | game-logic/program | silver |  |  | Lightbot P1/P2, RoboZZle F1–F5, рекурсія. |
| `sensor-predicates` | Сенсори-умови ✍️ | game-logic/program | bronze |  |  | frontIsClear, onBeeper, колір плитки: розгалуження в програмі. |
| `step-execution` | Покрокове виконання з підсвіткою команди ✍️ | game-logic/program | tin |  |  | Крок/пауза/швидкість, поточна команда підсвічена. |
| `fsm-program` | Програма як скінченний автомат ✍️ | game-logic/program | gold |  |  | Kara: стан × сенсори → дії + наступний стан. |
| `save-game` | Збереження гри | game-logic/save | silver |  |  | Продовжити пізніше. |
| `save-single-slot` | Один слот | game-logic/save | silver | save-game |  |  |
| `save-multi-slot` | Кілька слотів | game-logic/save | silver | save-game |  |  |
| `save-autosave` | Автосейв | game-logic/save | silver | save-game |  |  |
| `save-progress` | Збереження рекордів і прогресу | game-logic/save | bronze |  |  | Між сесіями. |
| `event-points` | Очки за події | game-logic/score | wood |  |  | Таблиця вартостей дій. |
| `combo-multiplier` | Комбо-серії | game-logic/score | tin |  |  | Множник за неперервність (Mr. Do!). |
| `time-bonus` | Бонус за час | game-logic/score | wood |  |  | Швидше = більше. |
| `score-records` | Рекорди | game-logic/score | tin |  |  | Локальна таблиця найкращих. |
| `chain-reaction` | Каскад і ланцюг ✍️ | game-logic/score | bronze |  | multiplier | Збіги після осідання, детонації сусідніх, ланцюг Puyo; слот — множник. |
| `extra-life-threshold` | Життя за пороги очок ✍️ | game-logic/score | wood |  | every |  |
| `leftover-penalty` | Штраф за залишок ✍️ | game-logic/score | wood |  |  | Blokus, Azul, Scrabble: наприкінці мінус за невикладені фігури / порожні клітини. |
| `escalating-kill-points` | Очки подвоюються в серії ✍️ | game-logic/score | wood |  |  | 200 → 400 → 800 → 1600 за одну серію. |
| `enemy-waves` | Хвилі ворогів | game-logic/waves | bronze |  | waves, final_wave | Розклад появи, фінальна хвиля. |
| `reinforcements` | Підкріплення | game-logic/waves | wood |  |  | +1 ворог за знищеного. |
| `progress-acceleration` | Прискорення прогресу | game-logic/waves | wood |  |  | Темп росте з рівнем/довжиною. |
| `collect-all` | Зібрати все | game-logic/win | wood |  |  | Точки/призи/золото. |
| `collect-quota` | Зібрати квоту | game-logic/win | wood |  | quota | N алмазів відкривають вихід. |
| `reach-exit` | Дійти до фінішу | game-logic/win | wood |  |  | Клітина виходу. |
| `destroy-all-enemies` | Знищити всіх ворогів | game-logic/win | wood |  |  |  |
| `all-on-targets` | Усі обʼєкти на цілях | game-logic/win | wood |  |  |  |
| `satisfy-constraints` | Задовольнити всі обмеження | game-logic/win | tin |  |  | Пазл розвʼязано. |
| `checkmate` | Мат | game-logic/win | gold |  |  | Король суперника без порятунку. |
| `home-slots` | Заповнити N домівок по разу ✍️ | game-logic/win | tin |  |  | Вхід у вже зайняту — смерть. |
| `keep-playing-after-win` | Грати далі після перемоги ✍️ | game-logic/win | wood |  |  | Мʼяка перемога: можна продовжити. |
| `level-bank` | Банк рівнів із прогресом | levels/bank | bronze |  |  | Список «розвʼязано / ні». |
| `daily-puzzle` | Щоденний пазл | levels/bank | tin |  |  | Рівень дня з фіксованим seed. |
| `level-rating` | Рейтинг рівнів | levels/bank | tin |  |  | Сортування за складністю в банку. |
| `in-game-editor` | Редактор у грі | levels/editor | silver |  |  | Розстановка елементів курсором, збереження у файл. |
| `editor-palette` | Палітра елементів | levels/editor | wood | in-game-editor |  | Вибір елемента для розстановки. |
| `editor-draw-tools` | Інструменти малювання | levels/editor | bronze | in-game-editor |  | Прямокутник, лінія, заливка — не лише по клітині. |
| `editor-erase` | Гумка | levels/editor | wood | in-game-editor |  | Видалення елементів з мапи. |
| `editor-undo` | Undo/redo | levels/editor | bronze | in-game-editor |  | Скасування і повернення дій. |
| `editor-playtest` | Плейтест | levels/editor | bronze | in-game-editor |  | Запуск рівня одразу з редактора. |
| `editor-map-check` | Перевірка мапи редактором | levels/editor | bronze |  |  | Не дає зберегти непрохідне. |
| `level-exchange` | Обмін рівнями | levels/editor | tin |  |  | Експорт/імпорт файла іншому студенту. |
| `level-from-txt` | Рівень із txt-файла | levels/format | bronze |  |  | Символьна мапа, парсер. |
| `import-open-formats` | Імпорт відкритих форматів | levels/format | bronze |  |  | .xsb, судоку-стрічки, формати Tatham. |
| `map-validation` | Валідація мапи | levels/format | tin |  |  | Зрозуміла помилка на битому файлі. |
| `level-metadata` | Метадані рівня | levels/format | wood |  |  | Назва, автор, складність у заголовку файла. |
| `maze-generation` | Генерація лабіринту | levels/generation | gold |  | algo | Прохідний лабіринт (DFS/Прима). |
| `mines-after-first-click` | Розкидання мін після першого кліку | levels/generation | tin |  |  | Перший клік завжди безпечний. |
| `dungeon-generation` | Генерація підземель | levels/generation | gold |  |  | Кімнати + коридори (роглайк). |
| `unique-puzzle-generation` | Генерація пазла з унікальним розвʼязком | levels/generation | crown |  |  | Головне золото пазл-гілки. |
| `infinite-field` | Нескінченне поле вперед | levels/generation | gold |  |  | Генерація на льоту (Crossy Road). |
| `difficulty-rating` | Оцінка складності згенерованого | levels/generation | gold |  |  | Рейтинг за технікою розвʼязання. |
| `no-guess-generation` | Генерація без вгадування ✍️ | levels/generation | gold |  |  | Hexcells, Kaboom, Tatham Mines: розвʼязується лише логікою. |
| `sequential-levels` | Кілька рівнів послідовно | levels/progression | tin |  |  | Перехід після перемоги. |
| `level-unlock` | Розблокування | levels/progression | tin |  |  | Наступний відкривається після попереднього. |
| `level-select` | Вибір рівня | levels/progression | tin |  |  | Меню зі списком і статусом. |
| `checkpoint` | Checkpoint | levels/progression | bronze |  |  | Продовження з середини після смерті. |
| `world-map` | Мапа світу з вузлами-рівнями ✍️ | levels/progression | bronze |  |  | Baba, Snakebird, Candy Crush saga: вузли відкриваються, видно прогрес. |
| `stairs-levels` | Поверхи через сходи ✍️ | levels/progression | wood |  |  | Роглайки, Magic Tower: вниз/вгору, рівень лишається або генерується знову. |
| `reachability-check` | Перевірка досяжності | levels/solvability | gold |  |  | Чи існує шлях до всіх цілей (flood fill / BFS). |
| `level-solver` | Розвʼязувач | levels/solvability | gold |  |  | Авторозвʼязання рівня (Sokoban, судоку). |
| `unsolvable-states` | Виявлення нерозвʼязних станів | levels/solvability | gold |  |  | Deadlock під час гри. |
| `movement-animation` | Анімація руху | interface/graphics | bronze |  |  | Плавний зсув між клітинами (GUI). |
| `event-effects` | Ефекти подій | interface/graphics | tin |  |  | Вибух, збирання, відкриття дверей. |
| `idle-animation` | Анімація очікування | interface/graphics | tin |  |  | «Дихання» спрайтів на місці. |
| `particles` | Частинки | interface/graphics | bronze |  |  | Прості системи часток на подіях. |
| `status-panel` | Панель стану | interface/hud | tin |  |  | Життя, рахунок, час, запас бомб/щитів. |
| `goal-counter` | Лічильник цілей | interface/hud | wood |  |  | Скільки лишилось зібрати/знищити. |
| `mode-indicator` | Індикатор режиму | interface/hud | wood |  |  | Енерджайзер активний, чий хід. |
| `telegraphed-intents` | Телеграфовані наміри | interface/hud | bronze |  |  | Показати наступний хід ворога (Into the Breach). |
| `highlights` | Підсвітки на полі ✍️ | interface/hud | tin |  |  | Сімʼя: виділення, легальні ходи (є), конфлікти, останній хід, досяжність, загроза, телеграф, шлях. |
| `selection-highlight` | Виділена клітина/фігура | interface/hud | wood | highlights |  |  |
| `conflict-highlight` | Конфлікти розмітки | interface/hud | tin | highlights |  |  |
| `last-move-highlight` | Останній хід суперника | interface/hud | wood | highlights |  |  |
| `reachable-highlight` | Досяжні клітини за хід | interface/hud | tin | highlights |  |  |
| `threat-range` | Зона ураження ворога | interface/hud | tin | highlights |  |  |
| `telegraph-marker` | Куди вдарить ворог наступного ходу | interface/hud | tin | highlights |  | Into the Breach |
| `path-preview` | Превʼю шляху до цілі | interface/hud | tin | highlights |  |  |
| `move-counter` | Лічильник ходів/поштовхів ✍️ | interface/hud | wood |  |  |  |
| `remaining-counter` | Лишилось: мін/точок/ворогів ✍️ | interface/hud | wood |  |  |  |
| `next-queue` | Черга наступних фігур/плиток ✍️ | interface/hud | wood |  |  | Tetris next, Lines 98 превʼю кольорів. |
| `pocket` | Рука/взяті фігури ✍️ | interface/hud | tin |  |  | Сьоґі, Crazyhouse, Hive: панель фігур поза полем. |
| `message-log` | Журнал подій ✍️ | interface/hud | tin |  |  | Роглайки: рядок/список повідомлень про події тіку. |
| `objective-text` | Поточна ціль словами ✍️ | interface/hud | wood |  |  |  |
| `popup-text` | Спливний текст над клітиною ✍️ | interface/hud | wood |  |  | +100, Combo ×3, шкода. |
| `push-counter` | Лічильник поштовхів ✍️ | interface/hud | wood |  |  | Окремо від лічильника ходів. |
| `face-button` | Смайлик стану з рестартом ✍️ | interface/hud | wood |  |  | Показує стан гри, клік перезапускає. |
| `keyboard-controls` | Керування клавіатурою | interface/input | bronze |  |  | Рух, дії, перепризначення клавіш. |
| `cell-click` | Клік по клітині | interface/input | wood |  |  | Базова курсорна дія. |
| `hover-highlight` | Виділення і наведення | interface/input | tin |  |  | Підсвітка клітини під курсором. |
| `drag-drop-piece` | Drag-n-drop фігури | interface/input | bronze |  |  | Перетягнути на легальну клітину. |
| `pencil-marks` | Олівцеві нотатки | interface/input | bronze |  |  | Pencil marks: кандидати в клітині. |
| `chord-click` | Акорд-клік | interface/input | tin |  |  | Комбінована дія на числі. |
| `swipe-gestures` | Жести-свайпи | interface/input | bronze |  |  | Хід свайпом (тач/мобільний варіант). |
| `path-drawing` | Малювання шляху drag-ом ✍️ | interface/input | tin |  |  | Flow Free, Cosmic Express, LYNE, Puzzle & Dragons: шлях по сусідніх клітинах. |
| `path-cut` | Відкат шляху до клітини ✍️ | interface/input | tin |  |  | Повернення по своєму шляху стирає хвіст; перетин чужого обриває його. |
| `multi-select` | Виділення кількох клітин ✍️ | interface/input | tin |  |  | SudokuPad, Tatham: групове введення/зафарбовування. |
| `edge-marking` | Розмітка ребер ✍️ | interface/input | tin |  |  | Slitherlink, Masyu: клік по ребру, хрестик «нема ребра». |
| `dot-mark` | Крапка/знак питання на клітині ✍️ | interface/input | wood |  |  | Невпевнена позначка, не впливає на перевірку. |
| `flag-cycle` | Правий клік по колу ✍️ | interface/input | wood |  |  | Прапорець → знак питання → порожньо. |
| `flood-reveal` | Каскадне відкриття нулів ✍️ | interface/input | tin |  | neighborhood | Клік по порожній клітині відкриває сусідні, доки є нулі. |
| `main-menu` | Головне меню | interface/menus | tin |  |  | Нова гра, продовжити, вихід. |
| `pause-menu` | Пауза-меню | interface/menus | tin |  |  | З продовженням і рестартом. |
| `confirm-dialog` | Діалог підтвердження | interface/menus | wood |  |  | Вихід без збереження. |
| `end-screen` | Екран перемоги/поразки | interface/menus | tin |  |  | З підсумком і переходом далі. |
| `game-screen` | Ігровий екран | interface/menus | wood |  |  | Головне вікно з полем гри; сам рендер поля — картки підзони «Поле і рендер». |
| `splash-screen` | Заставка/лого | interface/menus | tin |  |  | Екран із назвою і логотипом при запуску. |
| `settings-window` | Вікно налаштувань | interface/menus | tin |  |  | Окреме вікно під елементи налаштувань. |
| `shop-window` | Вікно магазину | interface/menus | tin |  |  | Вітрина крамниці; сама механіка покупок — у «Економіці». |
| `help-window` | Вікно довідки | interface/menus | tin |  |  | Правила гри і керування зсередини гри. |
| `about-window` | Вікно «Про гру» | interface/menus | wood |  |  | Автор, версія, подяки. |
| `custom-window` | Нестандартне вікно | interface/menus |  |  |  | Вікно поза типами; ціну і зарахування уточнює викладач. |
| `editor-window` | Вікно редактора рівнів | interface/menus | silver |  |  | Окремий екран з палітрою й інструментами (функції — підзона levels/editor). |
| `stats-window` | Статистика гравця | interface/menus | wood |  |  | Перемоги, час, серії, найкращі результати. |
| `mode-select` | Вибір режиму | interface/menus | wood |  |  | Класика / на час / нескінченний / versus. |
| `map-window` | Карта світу або підземелля | interface/menus | tin |  |  | На весь екран; мінікарта — HUD. |
| `difficulty-select` | Вибір складності | interface/menus | wood |  |  |  |
| `puzzle-select` | Сітка пазлів зі статусами | interface/menus | tin |  |  | Банк рівнів: розвʼязано / ні / зірки. |
| `lobby-window` | Лобі мультиплеєра | interface/menus | tin |  |  |  |
| `tutorial-window` | Навчання | interface/menus | tin |  |  | Покрокове пояснення правил у перших рівнях. |
| `replay-window` | Перегляд повтору / історії ходів | interface/menus | tin |  |  |  |
| `codex-window` | Бестіарій / енциклопедія елементів | interface/menus | tin |  |  | Картки сутностей гри з правилами — паспорт гри всередині гри. |
| `achievements-window` | Досягнення | interface/menus | wood |  |  |  |
| `character-select` | Вибір персонажа / загону | interface/menus | wood |  |  |  |
| `game-over-continue` | «Продовжити?» з лічильником | interface/menus | wood |  |  | Аркадний екран після смерті. |
| `level-password` | Вхід на рівень за паролем | interface/menus | wood |  |  | Chip's Challenge, Bomberman, Lolo. |
| `match-setup` | Налаштування партії | interface/menus | tin |  |  | Сторони, AI/людина, час, арена, кількість раундів. |
| `attract-demo` | Demo-режим «гра грає сама» | interface/menus | tin |  |  | Аркадний attract mode: показ правил без вводу. |
| `placement-screen` | Розстановка перед партією | interface/menus | tin |  |  | Battleship, Stratego, Khet: сховати своє поле від суперника. |
| `pass-device` | «Передай пристрій» для hot-seat | interface/menus | wood |  |  | Екран-завіса між ходами з прихованою інформацією. |
| `code-editor-window` | Редактор програми | interface/menus | silver |  |  | Karel, Lightbot, 7 Billion Humans: список команд, запуск, крок. |
| `console-render` | Консольний рендер | interface/render | bronze |  |  | Поле символами/емодзі, перемальовка кадру. |
| `gui-render` | GUI-рендер | interface/render | silver |  |  | Те саме поле спрайтами; спільний двіжок із консоллю. |
| `field-scaling` | Масштабування поля | interface/render | bronze |  |  | Розмір під вікно, скрол великих мап. |
| `player-camera` | Камера за гравцем | interface/render | bronze |  |  | Вʼюпорт менший за мапу. |
| `minimap-radar` | Мінімапа/радар | interface/render | bronze |  |  | Огляд великої мапи або невидимих ворогів. |
| `fog-of-war` | Туман війни ✍️ | interface/render | bronze |  |  | Advance Wars, Wesnoth, роглайки: видно лише в радіусі своїх сутностей; запамʼятована мапа. |
| `leaderboard` | Таблиця рекордів | interface/results | tin |  |  | Топ-N з іменами. |
| `profile-stats` | Статистика профілю | interface/results | tin |  |  | Партії, перемоги, найкращий час. |
| `replay` | Replay | interface/results | silver |  |  | Перегляд запису проходження. |
| `share-result` | Поділитись результатом ✍️ | interface/results | tin |  |  | Wordle-сітка емодзі, код результату в буфер. |
| `streak-stats` | Серії й статистика щоденних ✍️ | interface/results | wood |  |  | Streak, розподіл спроб. |
| `rating-system` | Рейтинг гравців ✍️ | interface/results | silver |  |  | Elo/Glicko для партій проти людей або AI. |
| `game-settings` | Налаштування гри | interface/settings | bronze |  |  | Складність, розмір поля, звук; збереження між сесіями. |
| `theme-select` | Вибір теми | interface/settings | tin |  |  | Набори символів/спрайтів. |
| `settings-elements` | Елементи налаштувань | interface/settings | tin |  |  | Сімʼя інтерфейсних контролів; кожен елемент у вікні — окрема заявка. |
| `volume-control` | Гучність | interface/settings | tin | settings-elements |  | Слайдер або кнопки рівня звуку. |
| `music-toggle` | Перемикач музики | interface/settings | wood | settings-elements |  | Увімк/вимк фонової музики. |
| `avatar-picker` | Вибір аватару | interface/settings | tin | settings-elements |  | Персонаж/скін гравця. |
| `field-size-picker` | Розмір поля | interface/settings | tin | settings-elements |  | Розмір або масштаб поля. |
| `language-picker` | Вибір мови | interface/settings | tin | settings-elements |  | Перемикання мови інтерфейсу. |
| `controls-remap` | Перепризначення клавіш | interface/settings | bronze | settings-elements |  | Зміна розкладки керування. |
| `sound-effects` | Звукові ефекти подій | interface/sound | tin |  |  | Кроки, постріл, збирання. |
| `background-music` | Фонова музика | interface/sound | tin |  |  | З вимикачем у налаштуваннях. |
| `sound-volume` | Застосування гучності | interface/sound | wood |  |  | Рівень звуку реально впливає на ефекти й музику. |
| `sound-warnings` | Звукові попередження | interface/sound | wood |  |  | Таймер добігає, шах. |
| `logic-render-split` | Розділення логіки і рендера | code/architecture | bronze |  |  | Двіжок не знає, консоль це чи GUI (вимога спільного двіжка). |
| `dual-frontends` | Два фронтенди на одному двіжку | code/architecture | silver |  |  | Консоль + GUI перемикаються. |
| `state-as-data` | Стан гри як дані | code/architecture | bronze |  |  | Серіалізований стан (основа збережень і replay). |
| `game-loop` | Цикл tick/update/render | code/architecture | tin |  |  | Явний ігровий цикл. |
| `commit-history` | Історія комітів | code/git | wood |  |  | Осмислені повідомлення, без сміття в репо. |
| `project-readme` | README проєкту | code/git | wood |  |  | Як запустити, керування, скриншоти. |
| `version-tags` | Теги версій | code/git | wood |  |  | Зріз на кожну лабораторну. |
| `requirements-pyproject` | Requirements/pyproject | code/packaging | wood |  |  | Відтворюване середовище. |
| `single-command-run` | Запуск однією командою | code/packaging | wood |  |  | python -m game без танців. |
| `exe-build` | Збірка в exe | code/packaging | tin |  |  | pyinstaller для демонстрації без Python. |
| `typing-mypy` | Типізація | code/python | bronze |  |  | Анотації + перевірка mypy. |
| `dataclass-entities` | Dataclass-сутності | code/python | tin |  |  | Моделі елементів поля. |
| `generators-iterators` | Генератори та ітератори | code/python | tin |  |  | Обхід поля, хвилі. |
| `custom-exceptions` | Виключення | code/python | tin |  |  | Власні класи помилок, охайна обробка. |
| `std-collections` | Стандартні колекції | code/python | tin |  |  | deque для тіла змійки, heapq для A*. |
| `unit-tests` | Юніт-тести логіки | code/tests | bronze |  |  | Рух, взаємодії, перемога без рендера. |
| `fixture-level-tests` | Тест на рівнях-фікстурах | code/tests | bronze |  |  | Мапа з очікуваним результатом. |
| `property-tests` | Property-тести | code/tests | gold |  |  | Генератор завжди видає розвʼязне. |
| `player-guide` | Інструкція гравця | support/docs | wood |  |  | Правила і керування. |
| `architecture-doc` | Опис архітектури | support/docs | tin |  |  | Схема модулів для захисту. |
| `dev-log` | Журнал розробки | support/docs | tin |  |  | Короткий devlog по тижнях. |
| `game-page` | Сторінка гри | support/sites | tin |  |  | Опис, скриншоти, посилання на репозиторій. |
| `video-channel` | Канал/плейліст | support/sites | tin |  |  | Зібрані демки по лабораторних. |
| `itchio-publish` | Itch.io-публікація | support/sites | bronze |  |  | Гра, доступна для запуску іншим. |
| `feature-demo` | Демка фічі | support/video | tin |  |  | Короткий запис однієї можливості до захисту. |
| `game-trailer` | Трейлер гри | support/video | bronze |  |  | Зведене відео з монтажем. |
| `demo-effects` | Ефекти демки | support/video | tin |  |  | Титри, прискорення, зум на момент. |
