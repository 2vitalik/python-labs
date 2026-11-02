# Сімʼї-теки корпусу

Сімʼя = домінантна **лінія гри** (звідки вона родом і що робить гравець найчастіше), одна на гру — це тека в `games/`. Межі нечіткі навмисно; гра з двома лініями — у теку головної, другу — в `also:`. Класи за актором і осі — окремі поля шапки ([systems.md](systems.md)).

| Тека | Сімʼя | Дієслово | Еталони | Межа з сусідом |
|---|---|---|---|---|
| `push-slide` | штовхання і ковзання | штовхнути, зсунути | Sokoban, Rush Hour, Pengo, Inertia, Loopover | якщо ядро — «правила як обʼєкти» чи рекурсія → `thinky` |
| `dig-gravity` | копання і клітинна фізика | копати, падати | Boulder Dash, Supaplex, Repton, Dig Dug, falling sand | падіння лише плиток → `falling-match` |
| `maze-arcade` | лабіринтні й клітинні аркади real-time | бігти, тікати, їсти | Pac-Man, Bomberman, Snake, Frogger, Xonix, Q*bert, Chip's Challenge | з гравітацією і платформами → `grid-platformer` |
| `grid-platformer` | платформери з клітинною логікою | лазити, ставити блоки | Lode Runner, Toki Tori, Solomon's Key, Catrap, Fire 'n Ice, Boxboy | без гравітації → `push-slide` / `maze-arcade` |
| `falling-match` | падаючі блоки, збіги, злиття | скласти, зібрати 3 | Tetris, Puyo, Bejeweled, 2048, Lines 98, Puzznic | статична розмітка без падіння → `pencil-logic` |
| `thinky` | сучасні thinky-головоломки | думати, відкривати правило | Baba Is You, Snakebird, Parabox, Sausage Roll, DROD, Cosmic Express | класичне штовхання без «відкриття» → `push-slide` |
| `pencil-logic` | паперові логічні пазли | розмітити за обмеженнями | судоку й варіанти, Nikoli, Picross, Tatham | приховане поле з ризиком → `hidden-deduction` |
| `hidden-deduction` | приховане поле й дедукція | відкрити, вгадати безпечно | Minesweeper, Dragonsweeper, Hexcells, Battleship, Mastermind, Voltorb Flip | усе видно → `pencil-logic` |
| `chess-abstract` | шахи, варіації й абстрактні стратегії | ходити фігурою, бити | шахи, го, шашки, Hex, Hive, Onitama, Ataxx | загони з HP/ландшафтом → `tactics` |
| `tactics` | покрокові тактики на сітці/гексах | рухати загін, атакувати | Into the Breach, Fire Emblem, Advance Wars, Wesnoth, Disgaea, Hoplite | один герой у підземеллі → `roguelike` |
| `roguelike` | роглайки й клітинні данжен-кроулери | досліджувати, виживати | Rogue, DCSS, NecroDancer, Desktop Dungeons, Magic Tower, Grimrock | загін і карта битви → `tactics` |
| `tower-lanes` | tower defense і смугові поля | ставити, захищати | PvZ, Fieldrunners, Isle of Arrows, Inscryption, Wildfrost, auto chess | економіка/ферма без ворогів → `build-sim` |
| `build-sim` | будування, ферми, автоматизація, автомати | ставити, вирощувати, крутити | Factorio, Mindustry, Stardew, Townscaper, Dorfromantik, Life, Backpack Hero | програма команд → `program-robots` |
| `program-robots` | програмування на сітці | написати програму | Karel, Lightbot, RoboRally, 7 Billion Humans, Opus Magnum, The Farmer Was Replaced, Advent of Code | ручне керування → інші |
| `connect-rotate` | зʼєднання, труби, обертання, лазери | зʼєднати, повернути, відбити | Pipe Mania, Infinity Loop, Flow Free, Deflektor, Khet, Laser Tank, Lyne | зʼєднання як обмеження на папері → `pencil-logic` |
| `board-digital` | сучасні настільні ігри з сіткою | викласти плитку, заповнити | Blokus, Patchwork, Azul, Sagrada, Tiny Towns, Kingdomino, Labyrinth, Quoridor | абстрактні класики → `chess-abstract` |
| `word-number` | словесні й числові сіткові | вгадати, скласти слово | Wordle, Waffle, Scrabble, Boggle, Letterpress, Sumplete, Connections | числова дедукція без слів → `pencil-logic` |

Правило вибору теки: спитати «що гравець робить 80 % часу і з якої класики це виросло». Якщо дві відповіді однаково сильні — `klass: hybrid` і тека за першою згаданою в «Суті».
