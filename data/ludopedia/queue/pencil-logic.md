# Черга: pencil-logic — паперові логічні пазли

Сид куратора (Fable, 2026-11-02) розширено пошуковим агентом (2026-11-02). Пріоритет: 1 — обовʼязково описати, 2 — бажано, 3 — коли дійдуть руки.

Джерела, які агент реально відкрив: список жанрів puzz.link (244 id з `pzpr.js`; тексти правил — з `puzz.link/js/pzpr-samples/<id>.js`, сторінка правил — `https://puzz.link/rules.html?<id>`), офіційний список Nikoli EN, Wikipedia «List of Nikoli puzzle types», «Sudoku» (Variants), «Killer sudoku», колекція Тетема, каталог Conceptis, категорії судоку GM Puzzles, головна Cracking the Cryptic. Вебпошук вичерпав ліміт сесії — сторінки Logic Masters Germany і правила окремих варіантів CtC не відкривались; там, де лінка не бачив, стоїть «—». Рік: точний — лише коли певний; `Nikoli vol.N` — з тексту правил puzz.link; `—` — не перевірено.

Скорочення лінків: `pz:<id>` = `https://puzz.link/rules.html?<id>` · `nk:<slug>` = `https://www.nikoli.co.jp/en/puzzles/<slug>/` · `st:<name>` = `https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/<name>.html` · `cp:<name>` = `https://www.conceptispuzzles.com/index.aspx?uri=puzzle/<name>` · `gm:<cat>` = `https://www.gmpuzzles.com/blog/category/sudoku/<cat>/`.

## Зафарбовування клітинок (shading)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Nurikabe | — | острови-числа в морі; звʼязність моря, заборона 2×2 | nk:nurikabe | pz:nurikabe · cp:nurikabe | 1 |
| Hitori | — | викреслити повтори; білі звʼязні, чорні не сусідять | nk:hitori | st:singles · cp:hitori | 1 |
| Heyawake | — | кімнати з лічильником; біла смуга не перетинає дві межі | nk:heyawake | pz:heyawake | 2 |
| LITS | — | у кожній кімнаті тетраміно; однакові не торкаються | nk:lits | pz:lits | 2 |
| Kurodoko | — | число = скільки білих видно по прямих | nk:kurodoko | st:range · pz:kurodoko | 2 |
| Tapa | 2007 | підказка-набір довжин чорних блоків навколо клітинки | pz:tapa | — | 1 |
| Cave | — | печера: біла область звʼязна, видимість як у Kurodoko | pz:cave | — | 2 |
| Aquarium | — | вода тече рівнем у резервуарах — гравітація на папері | pz:aquarium | — | 2 |
| Yin-Yang | — | два кольори, обидва звʼязні, без 2×2 | pz:yinyang | — | 2 |
| Nonogram / Picross | 1987 | розфарбувати за довжинами серій — малюнок-винагорода | pz:nonogram | st:pattern · cp:pic-a-pix | 1 |
| Picross-варіанти (Mega, Color, Clip, 3D) | 2009 (3D) | кольорові серії, мега-підказки на 2 рядки, 3D-куб видалення | — | — | 2 |
| Fill-a-Pix / Mosaic | — | число = чорні в 3×3 навколо, разом із собою | cp:fill-a-pix | st:mosaic | 2 |
| Takuzu / Binairo / Unruly / Tic-Tac-Logic | — | бінарне поле: рівна кількість, без трійок, рядки різні | st:unruly | cp:tic-tac-logic | 1 |
| Shakashaka | — | чорні трикутники-половинки клітинки; білі — прямокутники під 45° | nk:shakashaka | pz:shakashaka | 1 |
| Sto-stone | — | блоки після «падіння» вниз заповнюють рівно нижню половину | nk:sto_stone | pz:stostone | 1 |
| Nuri-Maze (Nurimeizu) | — | зафарбуванням будуєш лабіринт з єдиним шляхом S→G | nk:nurimeizu | pz:nurimaze | 2 |
| Nurimisaki | — | білі мисоподібні кінці; число = довжина огляду мису | nk:nurimisaki | pz:nurimisaki | 3 |
| Context | — | колір клітинки-підказки міняє її сенс: орто vs діагональ | pz:context | — | 2 |
| Snake | — | одна змійка без самодотику; кінці й середини, лічильники рядків | pz:snake | — | 2 |
| Ququ | — | поле з трикутників; блоки, що торкаються кутом, різної форми | pz:ququ | — | 2 |
| Nondango | Nikoli vol.152 | перефарбувати кружечки; без трійок, включно з діагоналями | pz:nondango | — | 3 |

## Петлі й лінії (loop / path)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Slitherlink | 1989 | петля по ребрах сітки; число = ребра навколо клітинки | nk:slitherlink | st:loopy · cp:slitherlink · pz:slither | 1 |
| Masyu | — | перли: на білій прямо, на чорній поворот | nk:masyu | st:pearl · pz:mashu | 1 |
| Yajilin | — | стрілки-лічильники чорних; петля через усі білі | nk:yajilin | pz:yajilin | 2 |
| Country Road | — | петля заходить у кожну країну раз; число = клітинки петлі | pz:country | — | 2 |
| Numberlink (≈ Flow Free) | — | зʼєднати пари однакових чисел без перетинів | nk:numberlink | pz:numlin | 1 |
| Hashiwokakero (Bridges) | — | мости 1–2 між островами, граф звʼязний | nk:Hashiwokakero | st:bridges · cp:hashi · pz:hashikake | 1 |
| Icebarn | — | лід: на льоду не повертаєш, перетин дозволений; стрілки-однобічки | pz:icebarn | — | 1 |
| Suraromu (Slalom) | — | спрямована петля проходить ворота в заданому порядку | nk:suraromu | pz:slalom | 2 |
| Nagareru-Loop | — | вітер: стрілки-вентилятори в чорних задають напрям руху | nk:nagareru | pz:nagare | 2 |
| Reflect Link | — | трикутники-дзеркала відбивають лінію; перехрестя дано | pz:reflect | — | 2 |
| Moon or Sun | — | у сусідніх регіонах петля чергує місяці й сонця | nk:moon_or_sun | pz:moonsun | 2 |
| Kin-Kon-Kan | — | дзеркала в регіонах; промені з країв з довжиною | pz:kinkonkan | — | 2 |
| Tracks | — | колія від A до B з лічильниками рядків і стовпців | st:tracks | — | 2 |
| Signpost | — | шлях 1…N, кожна клітинка-стрілка вказує на наступну | st:signpost | — | 2 |
| Hidato | 2008 | ланцюжок 1…N крізь сусідів, включно з діагоналлю | — | — | 2 |
| Slant (Gokigen Naname) | — | діагональ у кожній клітинці, без циклів; число = кути у вершині | st:slant | pz:gokigen | 2 |

## Розміщення чисел (number placement)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Судоку класичне (Number Place) | 1979 | база сімʼї; pencil marks, highlight, auto-check у плеєрах | nk:sudoku | st:solo · cp:sudoku · https://www.gmpuzzles.com/blog/sudoku-rules-and-info/ | 1 |
| Kakuro (Cross Sums) | — | кросворд із сум без повторів | nk:kakuro | cp:kakuro · pz:kakuro | 1 |
| KenKen / Keen / CalcuDoku | 2004 | латинський квадрат з арифметичними клітками (+−×÷) | st:keen | cp:calcudoku | 1 |
| Futoshiki / Unequal | — | латинський квадрат зі знаками > між клітинками | st:unequal | pz:minarism | 2 |
| Skyscrapers / Towers | — | висоти; підказка ззовні = скільки веж видно | st:towers | cp:skyscrapers · pz:skyscrapers | 1 |
| Ripple Effect | — | однакові N у рядку не ближче ніж N клітинок | nk:ripple_effect | pz:ripple | 2 |
| Str8ts | — | чорні клітинки розривають ряди на «стрити» послідовних | — | — | 2 |
| Suguru / Tectonic | — | 1…N у регіоні розміру N; сусіди, включно з діагоналлю, різні | https://en.wikipedia.org/wiki/Sudoku | — | 2 |
| Easy as ABC | — | літери + порожні; ззовні — перша видима літера | pz:easyasabc | — | 2 |
| Doppelblock | — | дві чорні в рядку; ззовні сума між ними | pz:doppelblock | — | 2 |
| Bosanowa | Nikoli vol.119 | поле з кружечків; число = сума різниць із сусідами | pz:bosanowa | — | 2 |
| Magic / Latin squares | — | класична математика: суми рядків/діагоналей, латинськість | — | — | 3 |
| ~~Zebra (Einstein) puzzle~~ | — | дедукція в таблиці атрибутів, а не на полі гри | — | — · ⊘ 2026-11-19: покрито `pencil-logic/zebra-puzzle` | 2 |
| Sherlock | 1992 | 6×6 атрибутів, підказки «поруч/лівіше/між» | — | — | 2 |

## Поділ на області (region division)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Shikaku | — | розрізати на прямокутники з площею-числом | nk:shikaku | st:rect · pz:shikaku | 1 |
| Fillomino | — | число = розмір поліоміно; однакові не торкаються | nk:fillomino | st:filling · pz:fillomino | 1 |
| Tentai Show (Galaxies) | — | області центрально-симетричні навколо точок | nk:tentai_show | st:galaxies · pz:tentaisho | 1 |
| Palisade | — | рівні за розміром області; число = межі клітинки | st:palisade | — | 2 |
| Pentominous | — | поділ на пентаміно; однакові не торкаються | pz:pentominous | — | 2 |
| Double Choco | — | кожна область: біла й сіра половини однакові за формою | nk:double_choco | pz:dbchoco | 2 |
| Araf | — | у кожній області два числа, розмір строго між ними | pz:araf | — | 3 |
| Tachiawase Block | — | дві сітки з однаковим набором блоків, накладка без збігів | pz:tachibk | — | 2 |
| Dominosa | — | розкласти повний набір доміно по полю чисел | st:dominosa | — | 2 |
| Map | — | розфарбування карти 4 кольорами | st:map | — | 2 |

## Розміщення обʼєктів і рух (object placement / moving)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Light Up (Akari) | — | лампи освітлюють рядки до стін; лампи не бачать одна одну | nk:akari | st:lightup · pz:lightup | 1 |
| Star Battle | — | N зірок у рядку, стовпці, регіоні; без дотику | pz:starbattle | — | 1 |
| Tents | — | намет поруч з кожним деревом, пара 1:1 | st:tents | pz:tents | 2 |
| Battleships | — | флот у сітці з лічильниками рядків | cp:battleships | pz:battleship | 1 |
| Statue Park | — | розставити банк фігур; білі звʼязні | pz:statuepark | — | 2 |
| Magnets | — | доміно-магніти: однакові полюси не поруч | st:magnets | pz:magnets | 2 |
| Undead | — | привиди, вампіри, зомбі — видимість через дзеркала | st:undead | — | 1 |
| Dosun-Fuwari | Nikoli vol.151 | гравітація: ядра вниз, кульки вгору | nk:dosun_fuwari | pz:dosufuwa | 1 |
| Evolmino | — | фігура росте на клітинку вздовж стрілки | nk:evolomino | pz:evolmino | 2 |
| Pentopia | — | стрілки вказують на найближчу фігуру з банку | pz:pentopia | — | 2 |
| Pencils | — | олівці з вістрям, від вістря — лінія-«почерк» | nk:pencils | pz:pencils | 2 |
| N-queens / Knight's tour | — | класичні шахові задачі розміщення й обходу | — | — | 2 |
| Yajisan-Sokoban | — | рух ящиків малюєш лініями — сокобан як статичний пазл | pz:yajisoko | — | 1 |
| Herugolf | — | мʼяч котиться, кожен удар на клітинку коротший | nk:herugolf | pz:herugolf | 1 |
| Rectangle-Slider | — | зсунути панелі так, щоб склались у прямокутники | pz:rectslider | — | 2 |
| Tren | — | вагончики 1×2/1×3; число = на скільки може зсунутись | pz:tren | — | 2 |

## Варіанти судоку (sudoku variants)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Sudoku-variants (парасоля): Killer, Thermo, Arrow, Sandwich, Kropki, German Whispers, Renban, Little Killer, X-Sums, Skyscraper, Fog of War, Yin-Yang, Between Lines, Palindrome, XV, Odd/Even, Anti-knight/Anti-king, Jigsaw, Samurai, Region Sum, Zipper, Entropy, Nabner, Doublers, Schrödinger | — | одна гра, сотні обмежень-модулів на тій самій сітці | https://crackingthecryptic.com/ | https://www.gmpuzzles.com/blog/sudoku-rules-and-info/ | 1 |
| Killer Sudoku | 2005 (The Times) | клітки з сумою — Kakuro всередині судоку | https://en.wikipedia.org/wiki/Killer_sudoku | gm:killer-sudoku | 1 |
| Thermo Sudoku | — | термометр: цифри строго ростуть від колби | gm:thermo-sudoku | — | 1 |
| Arrow Sudoku | — | сума на стрілці = цифра в кружку | gm:arrow-sudoku | — | 1 |
| Kropki | — | білі крапки — сусідні цифри, чорні — подвоєння | pz:kropki | gm:consecutive-pairs-sudoku | 1 |
| German Whispers | — | сусіди на лінії різняться щонайменше на 5 | — | — | 1 |
| Renban | — | лінія містить послідовні цифри в будь-якому порядку | — | — | 2 |
| ~~Sandwich Sudoku~~ | — | ззовні сума між 1 і 9 у рядку | — | — · ⊘ 2026-11-19: покрито `pencil-logic/sudoku-variants` | 2 |
| Fog of War | — | поле під туманом розкривається правильними цифрами | — | — | 1 |
| Jigsaw / Samurai (Gattai) | — | нерегулярні блоки; пʼять сіток, що перекриваються | https://en.wikipedia.org/wiki/Sudoku | cp:sudoku | 2 |
| ~~Anti-knight / Anti-king (Miracle)~~ | — | шахові ходи як обмеження на цифри | — | — · ⊘ 2026-11-19: покрито `pencil-logic/sudoku-variants` | 2 |
| Battleship Sudoku | — | судоку + флот у тій самій сітці | gm:battleship-sudoku | — | 3 |

## Інструменти й банки

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| SudokuPad / f-puzzles / Penpa+ | — | редактори-плеєри: pencil marks, кольори, обмеження-шари, лінки | — | — | 1 |
| puzz.link (pzprv3) | — | 244 жанри в одному плеєрі з автоперевіркою правил | https://puzz.link/list.html | https://puzz.link/rules.html | 1 |
| Simon Tatham's Portable Puzzle Collection | — | 40 ігор з генераторами й гарантією єдиного розвʼязку | https://www.chiark.greenend.org.uk/~sgtatham/puzzles/ | — | 1 |
| Conceptis (Pic-a-Pix, Link-a-Pix, Sym-a-Pix, Maze-a-Pix, Dot-a-Pix…) | — | «картинкові» сімʼї логіки: малюнок як результат | https://www.conceptispuzzles.com/index.aspx?uri=puzzle | cp:link-a-pix · cp:sym-a-pix | 2 |
| Logic Pic / Krazydad | — | банки пазлів з друком і рівнями складності | — | — | 3 |

## Відкладені (бачені в puzz.link / GM, у таблицю не ввійшли — механіка повторює наявні)

Norinori, Kurotto, Coral, Kurochute, Mannequin Gate, Canal View, Ant Mill, Choco Banana (зафарбовування) · Double Back, Castle Wall, Balance Loop, Onsen-meguri, Dotchi-Loop, Mid-loop, Hotaru Beam (петлі) · Makaro, Nanro (числа) · Sashigane, Tatamibari, Uso-tatami, Snake Pit, Voxas (поділ) · Heyapin, Toichika, Wittgenstein Briquet, Kissing Polyominoes, Return Home (обʼєкти) · Tight Fit, Sudo-Kurve, Outside Sudoku (судоку, GM). Лінки — за схемою `pz:<id>` / `nk:<slug>` / `gm:<cat>`.

## Межові випадки

- Hexcells / Tametsi → `hidden-deduction` (поле приховане, відкриваєш поступово).
- Minesweeper (Tatham Mines, puzz.link `mines`) → `hidden-deduction`.
- Black Box, Guess (Tatham) → `hidden-deduction` (промені й Mastermind).
- Inertia, Fifteen, Sixteen, Twiddle, Cube (Tatham) → `push-slide`.
- Net, Netslide, Untangle (Tatham), Flow Free → `connect-rotate` (Numberlink лишається тут як паперовий жанр).
- Flip (Tatham, Lights Out) → `thinky` / `connect-rotate` — вирішити при описі.
- Flood, Same Game (Tatham) → `falling-match`.
- Pegs (Tatham, peg solitaire) → `chess-abstract`.
- Yajisan-Sokoban, Herugolf, Rectangle-Slider, Tren — «рухові» жанри puzz.link: тут, бо розвʼязок статичний на папері; друга лінія — `push-slide` (`also:`).
- Icebarn — лінія на льоду; друга лінія — `push-slide` (ковзання по льоду).
- Sumplete → `word-number`.
- Sherlock (1992) — дедукція атрибутів на сітці; якщо підказки відкриваються з часом → `hidden-deduction`.

## Хвиля 3 — 2026-11-09: нові кандидати (пошукові агенти Opus)

Джерела: puzz.link — `list.html` (245 data-pid) + таблиця назв у `js/pzpr.js` (247 id) + правила й автори з `js/pzpr-samples/<id>.js` для 130 кандидатів; Janko — `Raetsel/index.htm` (350 жанрів) + 238 сторінок жанрів без збігів (правила EN/DE, «Lexikon» з автором і роком); Nikoli EN — список 47 жанрів і сторінки Kuralin, Nuritwin, Nansuke; Wikipedia — API `Category:Logic_puzzles`, статті Goishi Hiroi, Shinro, Survo puzzle, Stained Glass, Yajisan-Kazusan · Не відкрилось: `puzz.link/list.html` через WebFetch (сторінку малює JS, тому id взято з `pzpr.js`) · WebSearch: 0. Скорочення не вжиті: усі лінки повні. `https://puzz.link/rules.html?<id>` — сторінка правил puzz.link, текст правил з якої я читав у `pzpr-samples/<id>.js`.

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Hitori-Ribashi (ひとりリバーシ) | 2006 | пасьянс-реверсі: кожен хід мусить захопити білі; число = номер ходу захоплення | https://www.janko.at/Raetsel/Hitori-Ribashi/index.htm | https://www.youtube.com/results?search_query=Hitori+Ribashi+puzzle | 1 |
| Saltatori | ? | тварини стрибають на відстань свого виду; кожну клітинку зайняти чи перестрибнути раз | https://www.janko.at/Raetsel/Saltatori/index.htm | — | 1 |
| Goishi Hiroi (Hiroimono, 碁石ひろい) | 1727 | зібрати всі камені ланцюгом: до найближчого по прямій, без розвороту назад | W:Goishi_Hiroi | https://puzz.link/rules.html?goishi · https://www.janko.at/Raetsel/Hiroimono/index.htm | 1 |
| Satogaeri (さとがえり) | Nikoli vol.99 | кружки ковзають прямо рівно на N клітинок; у кожному регіоні рівно один | https://www.nikoli.co.jp/en/puzzles/satogaeri/ | https://puzz.link/rules.html?satogaeri · https://www.janko.at/Raetsel/Satogaeri/index.htm | 1 |
| Kouchoku (交差は直角に限る) | Nikoli vol.133 | петля прямими відрізками між вузлами під будь-яким кутом; перетин лише під 90° | https://puzz.link/rules.html?kouchoku | — | 1 |
| Building Walk (ビルウォーク) | Nikoli vol.174 | шлях крізь багатоповерховий будинок: ліфти, стрілки вгору/вниз, число = поверх | https://puzz.link/rules.html?bdwalk | — | 1 |
| Tawamurenga (たわむれんが) | Nikoli vol.127 | цегляна кладка замість квадратів; чорна цеглина мусить спиратися на нижню | https://puzz.link/rules.html?tawa | https://www.janko.at/Raetsel/Tawa/index.htm | 1 |
| Usowan (Usoone, ウソワン) | Nikoli vol.151 | у кожній кімнаті рівно одна числова підказка бреше | https://www.nikoli.co.jp/en/puzzles/usowan/ | https://puzz.link/rules.html?usoone · https://www.janko.at/Raetsel/Usoone/index.htm | 1 |
| Yajisan-Kazusan (やじさんかずさん) | ? | стрілка-лічильник може брехати лише тоді, коли її клітинку зафарбовано | W:Yajisan-Kazusan | https://puzz.link/rules.html?yajikazu · https://www.janko.at/Raetsel/Yajisan-Kazusan/index.htm | 1 |
| Hinge (Chōtsugai, Chiyotsui, ちょうつがい) | Nikoli vol.159 | блок, розтятий межею кімнат, дзеркально симетричний відносно цієї межі | https://puzz.link/rules.html?hinge | https://www.janko.at/Raetsel/Chiyotsui/index.htm | 1 |
| Compass | ? | компас в області: скільки її клітинок лежить далі за кожен напрямок | https://puzz.link/rules.html?compass | https://www.janko.at/Raetsel/Compass/index.htm | 1 |
| Haisu | ? | шлях S→G крізь усі клітинки; число N — клітинка проходиться на N-му візиті регіону | https://puzz.link/rules.html?haisu | — | 1 |
| Guide Arrow (ガイドアロー) | ? | білі клітинки — дерево; стрілка = єдиний можливий перший крок до зірки | https://puzz.link/rules.html?guidearrow | — | 1 |
| Hebi-Ichigo (へびいちご) | Nikoli vol.126 | змійки 1–5 з головою; голова не може дивитися на іншу змійку | https://www.nikoli.co.jp/en/puzzles/hebi/ | https://puzz.link/rules.html?hebi · https://www.janko.at/Raetsel/Hebi-Ichigo/index.htm | 1 |
| Polyominos (сума 10) | ? | оптимізація замість єдиного розвʼязку: поліоміно із сумою 10, мінімум зайвих клітинок (перевірити: ≈ `pentominous`) | https://www.janko.at/Raetsel/Polyominos/index.htm | — | 1 |
| Army Ants (ぐんたいあり) | Nikoli vol.158 | перенести числа лініями так, щоб склались ланцюжки 1…N, що не торкаються | https://puzz.link/rules.html?armyants | https://www.janko.at/Raetsel/Armyants/index.htm | 2 |
| Oyakodori (おやこどり) | ? | малий і великий птах летять у гніздо; один межі не перетинає, інший мусить | https://puzz.link/rules.html?oyakodori | — | 2 |
| Suraido | ? | судоку, де дані цифри спершу треба зсунути в сусідні клітинки | https://www.janko.at/Raetsel/Suraido/index.htm | — | 2 |
| Detektivschach (Detective Chess) | ? | розставити дані шахові фігури; число = скільки фігур атакує клітинку | https://www.janko.at/Raetsel/Detektivschach/index.htm | — | 2 |
| Karakiri | ? | поле з кіл і прямих ліній: на кожній лінії кожне число рівно раз | https://www.janko.at/Raetsel/Karakiri/index.htm | — | 2 |
| Mäander (Meander) | ? | річка сталої ширини, береги — діагоналі клітинок; ззовні лічильники берегів | https://www.janko.at/Raetsel/Maeander/index.htm | — | 2 |
| Crossstitch | ? | дві петлі з діагоналей, що можуть перетинати одна одну; стрілки рахують перетини | https://puzz.link/rules.html?crossstitch | — | 2 |
| SquarO | ? | фарбуються вузли сітки, а не клітинки; число = скільки кутів клітинки чорні | https://www.janko.at/Raetsel/SquarO/index.htm | — | 2 |
| Ziegelmauer (Brick Wall) | ? | латинський квадрат з цеглин «парне + непарне»; півцеглини країв рядка зшиваються | https://www.janko.at/Raetsel/Ziegelmauer/index.htm | — | 2 |
| Zahlenlabyrinth (Magic Labyrinth) | ? | латинський квадрат, де вздовж шляху лабіринту числа йдуть циклом 1…N | https://www.janko.at/Raetsel/Zahlenlabyrinth/index.htm | — | 2 |
| Sukoro (数コロ) | Nikoli vol.40 | число = скільки сусідніх клітинок теж мають число; усі числа звʼязні | https://puzz.link/rules.html?sukoro | https://www.janko.at/Raetsel/Sukoro/index.htm | 2 |
| Zeiger | ? | число в стрілці = скільки різних чисел лежить у напрямку стрілки | https://www.janko.at/Raetsel/Zeiger/index.htm | — | 2 |
| Arofuro (Arrow Flow) | 2008 | стрілка в кожній клітинці; число = скільки стрілок ведуть сюди, зокрема ланцюжком | https://www.janko.at/Raetsel/Arofuro/index.htm | — | 2 |
| Mirror Block (ミラーブロック) | Nikoli vol.177 | товста лінія-дзеркало: області обабіч неї — дзеркальні копії | https://puzz.link/rules.html?mirrorbk | — | 2 |
| Chained Block (チェンブロ) | Nikoli vol.173 | блоки, що торкаються кутами, утворюють ланцюг без однакових форм | https://www.nikoli.co.jp/en/puzzles/chained-block/ | https://puzz.link/rules.html?chainedb · https://www.janko.at/Raetsel/Chained-Blocks/index.htm | 2 |
| Curve Data (カーブデータ) | ? | фігура з ліній топологічно збігається зі схемою-підказкою; довжини відрізків гнучкі | https://puzz.link/rules.html?curvedata | — | 2 |
| Remembered Length | ? | спрямована петля: число регіону задає довжину візиту в наступний регіон | https://puzz.link/rules.html?remlen | — | 2 |
| Pipelink (パイプリンク) | Nikoli vol.45 | петля крізь усі клітинки з прямими перехрестями будь-де; дано шматки труб | https://puzz.link/rules.html?pipelink | https://www.janko.at/Raetsel/Pipelink/index.htm | 2 |
| Nagenawa (なげなわ) | Nikoli vol.123 | кілька прямокутних петель-ласо, що перетинаються; число = клітинки петель у кімнаті | https://puzz.link/rules.html?nagenawa | https://www.janko.at/Raetsel/Nagewawa/index.htm | 2 |
| Myopia | ? | петля по ребрах; стрілки показують напрям(и) до найближчого відрізка петлі | https://puzz.link/rules.html?myopia | — | 2 |
| Look-Air (るっくえあ) | Nikoli vol.136 | чорні блоки — квадрати; два рівні квадрати не бачать один одного по прямій | https://puzz.link/rules.html?lookair | https://www.janko.at/Raetsel/Rukkuea/index.htm | 2 |
| No Three (ノースリー) | Nikoli vol.158 | будь-які три чорні підряд по лінії мають різні проміжки між собою | https://puzz.link/rules.html?nothree | — | 2 |
| One Room One Door (ワンルームワンドア) | Nikoli vol.169 | між двома кімнатами щонайбільше одні «двері» — пара білих через межу | https://puzz.link/rules.html?oneroom | https://www.janko.at/Raetsel/Wanrumuwandoa/index.htm | 2 |
| Kuralin | ? | петля, решта клітинок чорна; кружок торкається більше клітинок свого кольору | https://www.nikoli.co.jp/en/puzzles/kuralin/ | — | 2 |
| Tenner Grid (Zehnergitter) | ? | у кожному рядку 0–9, однакові не торкаються навіть кутом; суми стовпців | https://www.janko.at/Raetsel/Zehnergitter/index.htm | — | 2 |
| Survo puzzle | 2006 | розставити 1…m×n по разу, щоб збіглися суми рядків і стовпців | W:Survo_puzzle | — | 2 |
| Shinro | 2007 | 12 лунок на полі 8×8; кожна стрілка вказує хоча б на одну | W:Shinro | — | 2 |
| Trilogik | ? | три символи; трійка підряд, з діагоналями, ні однакова, ні вся різна | https://www.janko.at/Raetsel/Trilogik/index.htm | — | 2 |
| KaitoRamma (快刀乱麻) | Nikoli vol.123 | розрізи — лише прямі від краю до краю; білі й чорні кружки розділені | https://puzz.link/rules.html?kramma | — | 2 |
| Deddoanguru (Dead Angle) | 2003 | «око» дивиться в 4 боки до межі; число = клітинки області поза зором | https://www.janko.at/Raetsel/Deddoanguru/index.htm | — | 2 |
| Scrin (スクリン) | Nikoli vol.165 | прямокутники, що торкаються кутами, утворюють одну замкнену петлю | https://puzz.link/rules.html?scrin | https://www.janko.at/Raetsel/Scrin/index.htm | 2 |
| Ichimaga (イチマガ) | Nikoli vol.35 | лінії з не більше ніж одним поворотом зʼєднують кружки в мережу; число = степінь | https://puzz.link/rules.html?ichimaga | https://www.janko.at/Raetsel/Ichimaga/index.htm | 2 |
| Coffee Milk (コーヒー牛乳) | Nikoli vol.156 | групи кружків прямими лініями: один сірий, білих і чорних порівну | https://puzz.link/rules.html?coffeemilk | https://www.janko.at/Raetsel/Milchkaffee/index.htm | 2 |
| Molekularis | ? | атоми з валентністю H1 O2 N3 C4: звʼязки 1–4 лінії, молекула звʼязна | https://www.janko.at/Raetsel/Molekularis/index.htm | — | 2 |
| Stitches | ? | кожну пару сусідніх регіонів зшити рівно одним стібком довжини 1 | https://www.janko.at/Raetsel/Stitches/index.htm | — | 2 |
| Türen (Doors, Seethrough) | ? | вирішити, які двері між кімнатами відчинені; число = скільки кімнат видно | https://www.janko.at/Raetsel/Tueren/index.htm | — | 2 |
| Angle Loop (鋭直鈍ループ) | ? | петля по точках: трикутник — гострий кут, квадрат — прямий, пʼятикутник — тупий | https://puzz.link/rules.html?angleloop | — | 3 |
| Kuroclone (クロクローン) | Nikoli vol.153 | у кімнаті два чорні блоки однакової форми; стрілка — розмір сусіднього блока | https://puzz.link/rules.html?kuroclone | https://www.janko.at/Raetsel/Kuroclone/index.htm | 3 |
| Train Stations | ? | петля крізь усі клітинки; усі перехрестя дано; станції по зростанню, без поворотів | https://puzz.link/rules.html?trainstations | — | 3 |
| Creek (クリーク) | Nikoli vol.110 | підказки у вузлах сітки: скільки з чотирьох клітинок навколо зафарбовано | https://puzz.link/rules.html?creek | https://www.janko.at/Raetsel/Creek/index.htm | 3 |
| Aqre | ? | жодних 4 однакових кольорів підряд; чорні звʼязні; лічильники кімнат | https://puzz.link/rules.html?aqre | https://www.janko.at/Raetsel/Aqre/index.htm | 3 |
| Tilepaint (タイルペイント) | Nikoli vol.53 | плитки фарбуються цілком; какуро-підказки рахують чорні до наступної підказки | https://www.nikoli.co.jp/en/puzzles/tilepaint/ | https://puzz.link/rules.html?tilepaint · https://www.janko.at/Raetsel/Tairupeinto/index.htm | 3 |
| Cake Table | ? | три кольори; число = скільки клітинок того ж кольору в 3×3 навколо | https://www.janko.at/Raetsel/Cake-Table/index.htm | — | 3 |
| Knossos | ? | розбити на області; єдине число в області = її периметр | https://www.janko.at/Raetsel/Knossos/index.htm | — | 3 |

## Хвиля 3 — 2026-11-09: нові кандидати (пошукові агенти Opus)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Tapa Sink (Bonpsi) | 2024 | Tapa на нескінченній сітці, видимій лише під прожектором субмарини | https://bonpsi.itch.io/tapa-sink | — | 3 |
| N-Chessmen (Ben Matthews) | 2024 | розставити різні шахові фігури: покрити всі клітини, жодна не б'є іншу | https://tsuhre.itch.io/n-chessmen | — | 3 |

## Хвиля 3 — 2026-11-09: нові кандидати (пошукові агенти Opus)

| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |
|---|---|---|---|---|---|
| Sudokuvania: Digits of Despair | 2025 | мапа 40×50 гаттай-судоку під туманом; правила відкриваються як здібності, боси-підпазли | https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000MQQ | https://www.youtube.com/results?search_query=Sudokuvania+Digits+of+Despair | 1 |
| Sudoku Mansion | 2026 | «класи» перечитують ту саму кімнату-судоку за іншим правилом (Whisper → Region Sum) | https://store.steampowered.com/app/5005590/Sudoku_Mansion/ | https://www.youtube.com/results?search_query=Sudoku+Mansion+gameplay | 1 |
| Sudoku Topology | 2024 | судоку з лініями-варіантами на сфері, торі, стрічці Мебіуса, пляшці Клейна | https://store.steampowered.com/app/3051910/Sudoku_Topology/ | https://www.youtube.com/results?search_query=Sudoku+Topology+gameplay | 1 |
| Murdoku | 2025 | підозрювані по кімнатах, один на рядок і колонку; убивця — сам на сам з жертвою | https://allthings.how/murdoku-explained-how-the-murder-mystery-sudoku-puzzle-works/ | https://murdoku.com/play | 1 |
| Nodes of a Feather | 2022 | у кожній парі ребер рівно одне, червоне чи синє; число вузла = розмір компоненти | https://sharkwithlasers.itch.io/nodes-of-a-feather | — | 1 |
| Super Sudokoid: Dark Inversion | 2026 | сиквел жанру Sudokuvania: 16 секторів 9×9 у тумані, стіни, HUD-боси дають цифри | https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000SQ0 | Final Transmission (перша частина): https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000RPZ | 2 |
| Hidden Oxygen | 2020 | кисні не торкаються навіть діагонально, лічильники рядків, кожен вуглець — 2 сусіди-кисні | https://www.crazygames.com/game/hidden-oxygen | https://www.youtube.com/results?search_query=Hidden+Oxygen+puzzle | 2 |
| 13 Sticky Notes | 2025 | 13 записок з просторовими правилами розкласти на нумеровану сітку, 2 клітини порожні | https://fachewachewa.itch.io/13-sticky-notes | — | 2 |
| Is This Seat Taken? | 2025 | розсадити персонажів у рядах місць за симпатіями й антипатіями до сусідів | https://store.steampowered.com/app/3035120/Is_This_Seat_Taken/ | https://www.youtube.com/results?search_query=Is+This+Seat+Taken+gameplay | 2 |
| CrossCells | 2017 | Matthew Brown: прибирати клітини з числами, щоб рядки й колонки дали цільові суми | https://store.steampowered.com/app/632000/CrossCells/ | https://www.youtube.com/results?search_query=CrossCells+gameplay | 2 |
| SquareCells | 2015 | гібрид нонограми й сапера: підказки рядків плюс числа клітин, без вгадування | https://store.steampowered.com/app/416770/SquareCells/ | https://www.youtube.com/results?search_query=SquareCells+gameplay | 2 |
| Liquidum | 2024 | нонограм-акваріуми: вода тече з гравітацією, діагональні стінки, човни над водою | https://store.steampowered.com/app/2716690/Liquidum/ | https://www.youtube.com/results?search_query=Liquidum+gameplay | 2 |
| Homgard | 2026 | нонограми з 6 новими правилами: кольорові клітини з іншим правилом, неквадратні поля | https://store.steampowered.com/app/4287570/Homgard/ | https://www.youtube.com/results?search_query=Homgard+gameplay | 2 |
| CiniCross | 2026 | нонограм-роглайт: кімнати-нонограми, боси міняють правила, артефакти заповнюють колонки | https://store.steampowered.com/app/3933120/CiniCross/ | https://www.youtube.com/results?search_query=CiniCross+gameplay | 2 |
| The Artisan of Glimmith | 2026 | вітражі: фарбувати, різати й зʼєднувати регіони за 20+ типами правил | https://store.steampowered.com/app/4160210/The_Artisan_of_Glimmith/ | https://www.youtube.com/results?search_query=The+Artisan+of+Glimmith+gameplay | 2 |
| Zerko | 2024 | Maciej Targoni: ставити фігури-блоки зі значеннями, щоб усі числа стали нулем | https://store.steampowered.com/app/2862990/Zerko/ | https://www.youtube.com/results?search_query=Zerko+gameplay | 2 |
| Logic Bombs | 2025 | бомби на полі: вибух кожної має зачепити рівно задану кількість ворогів | https://store.steampowered.com/app/3816700/Logic_Bombs/ | https://www.youtube.com/results?search_query=Logic+Bombs+Matthewmatosis | 2 |
| Rondoku | 2025 | числа в кругових діаграмах за трьома правилами, сусідні — не послідовні (?) | https://store.steampowered.com/app/3791600/Rondoku/ | — | 3 |
| Tatami | 2025 | поділ на прямокутники заданої площі; далі жовті клітини віднімають, від'ємні суми | https://apps.apple.com/us/app/tatami/id6575395532 | — | 3 |
| Draw a Loop! | 2025 | одна сторінка: петля на сітці без інструкцій, правило з єдиності, плюс секрет | https://xxuurruuii.itch.io/draw-a-loop | — | 3 |
| Lyth | 2025 | PDF без інструкцій: точки, числа, літери — правило виводиш з єдиності розвʼязку | https://xxuurruuii.itch.io/lyth | — | 3 |
| A Rule-Explorer's Adventure | 2025 | PDF без інструкцій за пазлом FDUPH; за описом — у кожного пазла рівно два розвʼязки | https://xxuurruuii.itch.io/a-rule-explorers-adventure | — | 3 |
| Overblock | 2025 | PDF: пакування обʼємних фігур у порожнини, фінальне розкриття | https://xxuurruuii.itch.io/overblock | — | 3 |
| Counterfill | 2025 | PDF: 20 паперових пазлів, правила замазані фарбою — відновити з єдиності | https://permatemp.itch.io/counterfill | — | 3 |
| Loopmaker | 2025 | одна картинка, 25 рівнів: петлі між синіми точками, правила відкриваєш сам | https://torcado.itch.io/loopmaker | — | 3 |
| The Domino Lockpicking Company | 2025 | PDF: лінії через доміно-сітки з очками; правила виводиш, розвʼязок не завжди єдиний | https://garth-sidious.itch.io/domino-lockpicking-company | — | 3 |
| Stencil Revamped | 2025 | архів пазлів, де правила перекреслені й дописані графіті — відновити набір | https://hutt3.itch.io/stencil-revamped | https://hutthutthuttspuzzledump.blogspot.com/2025/06/the-making-of-stencil-revamped.html | 3 |
