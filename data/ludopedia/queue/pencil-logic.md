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
| Zebra (Einstein) puzzle | — | дедукція в таблиці атрибутів, а не на полі гри | — | — | 2 |
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
| Sandwich Sudoku | — | ззовні сума між 1 і 9 у рядку | — | — | 2 |
| Fog of War | — | поле під туманом розкривається правильними цифрами | — | — | 1 |
| Jigsaw / Samurai (Gattai) | — | нерегулярні блоки; пʼять сіток, що перекриваються | https://en.wikipedia.org/wiki/Sudoku | cp:sudoku | 2 |
| Anti-knight / Anti-king (Miracle) | — | шахові ходи як обмеження на цифри | — | — | 2 |
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
