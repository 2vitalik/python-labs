# Черга: program-robots — програмування на сітці

Сид куратора (Fable, 2026-11-02), розширено пошуковим агентом 2026-11-02. Пріоритет: 1 — обовʼязково описати, 2 — бажано, 3 — коли дійдуть руки.

Лінки: усі URL відкриті й перевірені (статус 200 і заголовок сторінки); де точну сторінку не бачив — пошук Steam/YouTube за брифом. WebSearch вичерпався посеред роботи, тож частину років і механік узято з памʼяті. Такі місця позначено `(?)`, описовому агенту їх треба перевірити.

## Освітні виконавці (робот на клітинному полі)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Karel the Robot | 1981 | канон: move/turnLeft/putBeeper, стіни й біпери; мінімальний набір команд | https://en.wikipedia.org/wiki/Karel_(programming_language) | https://cs.stanford.edu/people/eroberts/karel-the-robot-learns-java.pdf | 1 |
| Reeborg's World | 2013 (?) | Karel у браузері на справжньому Python, світи з автоперевіркою мети | https://reeborg.ca/reeborg.html | — | 1 |
| Kara (SwissEduc) | 1999 (?) | сонечко програмується скінченним автоматом: стан × сенсори → дії | https://www.swisseduc.ch/informatik/karatojava/ | https://www.swisseduc.ch/informatik/karatojava/turingkara/index.html | 1 |
| TuringKara | 2000-ні (?) | машина Тюрінга з головкою на 2D-сітці замість стрічки | https://www.swisseduc.ch/informatik/karatojava/turingkara/index.html | https://www.swisseduc.ch/informatik/karatojava/multikara/index.html (кілька сонечок, синхронізація) | 2 |
| RoboMind | 2005 (?) | власна мова; робот фарбує клітини, бачить фарбу сенсорами, носить маяки | https://www.robomind.net/ | — | 3 |
| Lightbot / Lightbot Jr | 2008 | іконки-команди, процедури P1/P2, висота клітин, стрибок, лампи-цілі | https://lightbot.com/ | https://en.wikipedia.org/wiki/Lightbot | 1 |
| RoboZZle | 2009 | команди з кольоровою умовою клітини, рекурсія F1→F1, ліміт слотів | http://robozzle.com/ | https://www.youtube.com/results?search_query=robozzle+gameplay | 1 |
| Cargo-Bot | 2012 | кран над стовпчиками ящиків, умова «що в клешні», рекурсія; першу гру зроблено в Codea на iPad (?) | https://www.youtube.com/results?search_query=cargo-bot+gameplay | — | 2 |
| Blockly Games: Maze | 2012 (?) | блоки замість тексту, бюджет блоків, умова «шлях попереду» | https://blockly.games/maze | https://en.wikipedia.org/wiki/Blockly | 2 |
| Code.org Classic Maze (Hour of Code) | 2013 | масовий шкільний формат: 20 рівнів-лабіринтів, блоки з `repeat until` | https://studio.code.org/s/hourofcode | https://en.wikipedia.org/wiki/Code.org | 2 |
| CodeCombat | 2013 | справжній Python/JS керує героєм у бою: вороги, монети, `findNearestEnemy` | https://codecombat.com/ | https://en.wikipedia.org/wiki/CodeCombat | 2 |
| Swift Playgrounds (Byte) | 2016 | 3D-сітка: перемикачі, портали, рухомі платформи, кілька персонажів | https://en.wikipedia.org/wiki/Swift_Playgrounds | https://www.apple.com/swift/playgrounds/ | 2 |
| Robot Turtles | 2013 | настолка для дошкільнят: карти-команди, лазер плавить лід, ящики, кнопка «баг» | https://en.wikipedia.org/wiki/Programming_game | https://www.youtube.com/results?search_query=robot+turtles+board+game | 2 |
| Code Master (ThinkFun) | 2015 (?) | соло-настолка: програма токенами-діями по карті-графу з кристалами | https://www.youtube.com/results?search_query=thinkfun+code+master | — | 3 |
| Robot Karol | 2000-ні (?) | Karel з висотою: цеглини стопками, робот кладе й лізе нагору; ізометрія | https://www.youtube.com/results?search_query=robot+karol | — | 3 |
| Wumpus world | 1970-ті / AIMA | агент на 4×4 з сенсорами вітру й смороду, висновок логікою, а не командами | https://en.wikipedia.org/wiki/Wumpus_world | https://en.wikipedia.org/wiki/Hunt_the_Wumpus | 2 |

## Програмувальні головоломки й ігри

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| 7 Billion Humans | 2018 | одна програма на десятки працівників одночасно, `nearest`, `shout/listen` | https://store.steampowered.com/app/792100/7_Billion_Humans/ | https://en.wikipedia.org/wiki/7_Billion_Humans | 1 |
| Human Resource Machine | 2015 | асемблер: inbox → регістри-підлога → outbox, 1D; згадати як предка 7BH | https://store.steampowered.com/app/375820/Human_Resource_Machine/ | https://en.wikipedia.org/wiki/Human_Resource_Machine | 2 |
| The Farmer Was Replaced | 2023 EA / 2025 | Python-подібна мова, дрон на фермі-сітці, мова розблоковується як тех-дерево | https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/ | — | 1 |
| Robo Instructus | 2019 | текстова мова; одна програма мусить пройти кілька варіантів мапи | https://store.steampowered.com/app/1032170/Robo_Instructus/ | — | 2 |
| Untrusted | 2014 (?) | редагуєш JS-код самого рівня, щоб пройти roguelike-карту | https://alexnisnevich.github.io/untrusted/ | — | 1 |
| Manufactoria | 2010 | конвеєри й зчитувачі кольорової черги = автомат з чергою на сітці | https://www.youtube.com/results?search_query=manufactoria+gameplay | — | 1 |
| RoboRally | 1994 | 5 регістрів картами, одночасне виконання, конвеєри, шестерні, лазери, штовхання | https://en.wikipedia.org/wiki/RoboRally | https://www.youtube.com/results?search_query=roborally+how+to+play | 1 |
| Duskers | 2016 | консольні команди дронам у сітці кімнат; двері, енергія, вороги в темряві | https://en.wikipedia.org/wiki/Duskers | https://en.wikipedia.org/wiki/Quadrilateral_Cowboy | 2 |
| Autonauts | 2019 | бот вчиться повтором дій гравця, запис стає блоками | https://store.steampowered.com/app/979120/Autonauts/ | — | 2 |
| Craftomation 101 | 2022 (?) | гекс-поле планети, роботи з блоковими програмами крафту (?) | https://store.steampowered.com/search/?term=Craftomation+101 | — | 3 |
| Robot Odyssey | 1984 | схеми з логічних вентилів усередині роботів керують їхніми сенсорами й рушіями | https://en.wikipedia.org/wiki/Robot_Odyssey | https://en.wikipedia.org/wiki/Rocky%27s_Boots | 2 |
| Carnage Heart | 1995 | мех програмується сіткою чипів-умов зі стрілками переходів | https://en.wikipedia.org/wiki/Carnage_Heart | — | 2 |
| Gladiabots | 2018 | дерево умов і дій на команду ботів, PvP-арена | https://store.steampowered.com/app/871930/ | https://gladiabots.com/ | 2 |
| Screeps | 2016 | MMO-RTS на JS, код працює й без гравця, кімнати-сітки | https://screeps.com/ | https://store.steampowered.com/app/464350/Screeps_World/ | 2 |
| Befunge | 1993 | мова, де програма — це 2D-сітка: вказівник їде клітинами, стрілки повертають | https://esolangs.org/wiki/Befunge | https://en.wikipedia.org/wiki/Befunge | 1 |
| Core War | 1984 | програми-воїни переписують одна одну в кільцевій памʼяті (1D) | https://en.wikipedia.org/wiki/Core_War | — | 2 |
| Wireworld | 1987 | 4-станний клітинний автомат-електроніка: провід, голова й хвіст електрона | https://en.wikipedia.org/wiki/Wireworld | — | 2 |

## Zachtronics і спадкоємці

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| KOHCTPYKTOP: Engineer of the People | 2009 | шари кремнію n/p і металу на сітці, транзистори з перетину | https://www.zachtronics.com/kohctpyktop-engineer-of-the-people/ | — | 2 |
| SpaceChem | 2011 | два вальдо на треках 10×8, bond/sync, паралельні потоки | https://store.steampowered.com/app/92800/SpaceChem/ | https://en.wikipedia.org/wiki/SpaceChem | 1 |
| Infinifactory | 2015 | 3D-блоки: конвеєри, зварювачі, поршні; програма — розстановка | https://store.steampowered.com/app/300570/Infinifactory/ | https://en.wikipedia.org/wiki/Infinifactory | 2 |
| TIS-100 | 2015 | сітка асемблерних вузлів 4×3, обмін лише через порти | https://store.steampowered.com/app/370360/TIS100/ | https://en.wikipedia.org/wiki/TIS-100 | 2 |
| Opus Magnum | 2017 | гекс-сітка, руки з таймлайном команд, рахунок cost/cycles/area | https://store.steampowered.com/app/558990/Opus_Magnum/ | https://en.wikipedia.org/wiki/Opus_Magnum_(video_game) | 1 |
| Exapunks | 2018 | агенти-EXA ходять між хостами-сітками файлів, копіюють себе | https://store.steampowered.com/app/716490/EXAPUNKS/ | https://en.wikipedia.org/wiki/Exapunks | 3 |
| MOLEK-SYNTEZ | 2019 | гекс, емітери обертають і зсувають молекулу, а не носять атоми | https://store.steampowered.com/app/1168880/MOLEKSYNTEZ/ | https://www.zachtronics.com/molek-syntez/ | 2 |
| Kaizen: A Factory Story | 2025 | маніпулятори на таймлайні збирають виріб з деталей (Coincidence, Зак Барт) | https://en.wikipedia.org/wiki/Kaizen:_A_Factory_Story | https://store.steampowered.com/search/?term=Kaizen+A+Factory+Story | 2 |

## Логіка в будівельних іграх

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Minecraft redstone | 2010 | сигнал у 3D-блоках: сила 0–15, затримка ретрансляторів у тіках, поршні | https://minecraft.wiki/w/Redstone_circuits | — | 3 |
| Factorio circuit network | 2016 | комбінатори над сигналами-векторами, дроти двох кольорів | https://wiki.factorio.com/Circuit_network | — | 3 |
| Mindustry logic | 2020 (?) | процесори з асемблером керують юнітами й будівлями на мапі | https://mindustrygame.github.io/wiki/logic/0-introduction/ | https://en.wikipedia.org/wiki/Mindustry | 3 |
| Turing Complete | 2021 (?) | від NAND до власного CPU, схеми на сітці | https://store.steampowered.com/app/1444480/Turing_Complete/ | — | 3 |

## Змагання ботів

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| CodinGame: Tron Battle | 2013 (?) | світлові цикли 2–4 ботів, слід стає стіною; ідеальний перший бот | https://www.codingame.com/multiplayer/bot-programming/tron-battle | https://en.wikipedia.org/wiki/Tron_(video_game) | 1 |
| CodinGame: Ultimate Tic-Tac-Toe | 2016 (?) | 9 вкладених полів, твоя клітина визначає поле суперника | https://www.codingame.com/multiplayer/bot-programming/tic-tac-toe | https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe | 2 |
| CodinGame: Ocean of Code | 2020 | підводний човен, рух ворога видно лише напрямками, сонар і торпеда | https://www.codingame.com/multiplayer/bot-programming/ocean-of-code | — | 2 |
| CodinGame: Spring Challenge 2020 (Pac-Man) | 2020 | загони пакменів, камінь-ножиці-папір між ними, туман | https://www.codingame.com/multiplayer/bot-programming/spring-challenge-2020 | — | 2 |
| CodinGame: Spring Challenge 2021 (Photosynthesis) | 2021 | гекс-ліс, сонце обходить поле, тінь від дерев | https://www.codingame.com/multiplayer/bot-programming/spring-challenge-2021 | — | 2 |
| CodinGame: Hypersonic | 2016 (?) | Bomberman для ботів: ящики, бонуси, ланцюгові вибухи | https://www.codingame.com/multiplayer/bot-programming/hypersonic | — | 2 |
| CodinGame: Keep Off the Grass (Fall 2022) | 2022 | переробники зʼїдають клітини, поле зменшується, роботи захоплюють територію | https://www.codingame.com/multiplayer/bot-programming/keep-off-the-grass | https://www.codingame.com/multiplayer/bot-programming/fall-challenge-2022 | 2 |
| CodinGame: The Great Escape | 2015 (?) | Quoridor на трьох-чотирьох: біг до краю й стіни на шляху інших | https://www.codingame.com/multiplayer/bot-programming/great-escape | — | 3 |
| Google AI Challenge: Ants | 2011 | мурахи на тороїдальній сітці, туман, бій за кількістю сусідів | https://www.youtube.com/results?search_query=ai+challenge+ants+2011 | — | 2 |
| Halite (Two Sigma) | 2016 | тороїдальна сітка ресурсу; кораблі збирають і везуть на базу | https://www.kaggle.com/competitions/halite | — | 2 |
| Lux AI | 2021 | Kaggle-змагання: сітка ресурсів, цикл день/ніч, міста гинуть без палива | https://www.lux-ai.org/ | https://www.kaggle.com/competitions/lux-ai-season-3 | 2 |
| Battlecode (MIT) | 2001 | RTS з автономними ботами, ліміт байткоду на хід, спільна памʼять-масив | https://battlecode.org/ | — | 2 |

## Advent of Code — сіткові задачі

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| AoC 2016/22 Grid Computing | 2016 | дані між вузлами-дисками = пʼятнашки з однією порожньою клітиною | https://adventofcode.com/2016/day/22 | — | 2 |
| AoC 2018/13 Mine Cart Madness | 2018 | вагонетки на рейках, на перехресті по черзі ліво/прямо/право, зіткнення | https://adventofcode.com/2018/day/13 | — | 2 |
| AoC 2018/15 Beverage Bandits | 2018 | ельфи проти гоблінів: порядок читання, BFS до ворога, HP | https://adventofcode.com/2018/day/15 | — | 1 |
| AoC 2019/24 Planet of Discord | 2019 | Life 5×5, центр — вкладена копія поля, рекурсивні рівні | https://adventofcode.com/2019/day/24 | — | 2 |
| AoC 2022/14 Regolith Reservoir | 2022 | пісок падає з джерела, сповзає по діагоналі, скелі-ламані | https://adventofcode.com/2022/day/14 | — | 2 |
| AoC 2022/17 Pyroclastic Flow | 2022 | тетріс з вітром-командами, пошук циклу на трильйоні фігур | https://adventofcode.com/2022/day/17 | — | 2 |
| AoC 2022/22 Monkey Map | 2022 | карта загортається на грані куба, рух за командами | https://adventofcode.com/2022/day/22 | — | 2 |
| AoC 2023/16 The Floor Will Be Lava | 2023 | промені, дзеркала `/` `\`, розщеплювачі (вертикальний і горизонтальний) | https://adventofcode.com/2023/day/16 | — | 2 |
| AoC 2024/6 Guard Gallivant | 2024 | вартовий повертає праворуч біля перешкоди; поставити одну, щоб зациклити | https://adventofcode.com/2024/day/6 | — | 1 |
| AoC 2024/14 Restroom Redoubt | 2024 | роботи зі швидкостями на торі; знайти мить, коли складуть ялинку | https://adventofcode.com/2024/day/14 | — | 2 |
| AoC 2024/15 Warehouse Woes | 2024 | Sokoban за командами; у частині 2 ящики 2×1 штовхають ланцюгом | https://adventofcode.com/2024/day/15 | — | 1 |
| AoC 2024/21 Keypad Conundrum | 2024 | робот керує роботом через пульти, три рівні вводу | https://adventofcode.com/2024/day/21 | — | 1 |

## Межові випадки

- Baba Is You — правила як обʼєкти на полі → `thinky` (згадати: «правило = програма»).
- Logo / turtle graphics — неперервна геометрія, не клітини → поза корпусом (https://en.wikipedia.org/wiki/Turtle_graphics).
- Scratch, Kodu Game Lab, Colobot — програмування без клітинного поля → поза корпусом.
- Shenzhen I/O, Silicon Zeroes, while True: learn() — схеми й вузли без поля-сітки → поза корпусом.
- Last Call BBS (20th Century Food Court, 2022) — фабрика з машин; інші ігри збірки (зокрема Dungeons & Diagrams (?)) → `pencil-logic` (https://store.steampowered.com/app/1511780/).
- Hack 'n' Slash, else Heart.Break(), Hackmud — злам коду світу без клітинної логіки → поза корпусом.
- Quadrilateral Cowboy — команди в консолі, 3D-рівні → поза корпусом (лишається як рядок «інші лінки» до Duskers).
- Langton's ant / AoC 2017/22 Sporifica Virus, AoC 2019/24, Wireworld — клітинні автомати → можна в `build-sim` (автомати), якщо куратор вирішить.
- AoC 2023/14 Parabolic Reflector Dish — нахил поля, камінці котяться → `push-slide`.
- AoC 2019/13 Care Package — Intcode-програма — це Breakout, гравець пише автопілот → `maze-arcade`/`falling-match` як курйоз.
- Factorio, Mindustry, Minecraft як цілі ігри → `build-sim`; тут — лише їхні логічні підсистеми.
- Robot Odyssey / Rocky's Boots — ближче до схемотехніки; Rocky's Boots → поза корпусом.
