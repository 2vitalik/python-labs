// plain symbols for games drawn with text (T309): CLDR does not know them, so the names and the words are ours. A block —
// the words every row of it shares, then rows «symbol | назва | name | слова | words». A symbol that also has an emoji
// look wears U+FE0E, so that it stays text
const T = '︎'

export const SYMBOLS = [
  { uk: 'блок клітинка квадрат заливка', en: 'block cell square fill', rows: `
█ | суцільний блок | full block | стіна | wall solid
▓ | темна штриховка | dark shade | стіна туман | wall fog
▒ | середня штриховка | medium shade | туман пісок | fog sand
░ | світла штриховка | light shade | підлога туман пил | floor fog dust
▀ | верхня половина блока | upper half block
▄ | нижня половина блока | lower half block
▌ | ліва половина блока | left half block
▐ | права половина блока | right half block
■ | чорний квадрат | black square | квадратик плитка | tile
□ | білий квадрат | white square | квадратик порожня | empty
▢ | квадрат із круглими кутами | rounded square | квадратик порожня | empty
▣ | квадрат у квадраті | square in square | ящик ціль | crate target
▤ | квадрат у смужку | striped square | сходи драбина | ladder
▥ | квадрат у вертикальну смужку | vertically striped square | ґрати двері | bars door
▦ | квадрат у клітинку | grid square | ґрати решітка | grate
▧ | квадрат зі штрихом | hatched square
▨ | квадрат зі зворотним штрихом | back hatched square
▩ | квадрат у сіточку | crosshatched square | ґрати | grate
▬ | чорний прямокутник | black rectangle | платформа міст | platform bridge
▭ | білий прямокутник | white rectangle | платформа | platform
▮ | вертикальний прямокутник | vertical rectangle | двері колона | door pillar
▯ | порожній вертикальний прямокутник | white vertical rectangle | двері | door
▰ | паралелограм | parallelogram | смужка життя | health bar
▱ | порожній паралелограм | white parallelogram | смужка життя порожня | health bar empty
⊞ | квадрат із плюсом | squared plus | аптечка вікно | medkit window
⊟ | квадрат із мінусом | squared minus
⊠ | квадрат із хрестом | squared times | ящик | crate
⊡ | квадрат із крапкою | squared dot | ціль кнопка | target button
☐ | порожня позначка | ballot box
☒ | позначка з хрестом | ballot box with x | закрито | closed` },
  { uk: 'круг коло кружечок кружок', en: 'circle round', rows: `
● | чорний круг | black circle | куля камінь шашка фішка | ball stone piece dot
○ | білий круг | white circle | порожній камінь шашка фішка | ring empty stone piece
◉ | круг у колі | fisheye | ціль око | target eye
◎ | подвійне коло | bullseye | ціль мішень | target
◌ | пунктирне коло | dotted circle | привид слід | ghost trace
◍ | коло зі штриховкою | shaded circle
◐ | коло з чорною лівою половиною | circle with left half black
◑ | коло з чорною правою половиною | circle with right half black
◒ | коло з чорною нижньою половиною | circle with lower half black
◓ | коло з чорною верхньою половиною | circle with upper half black
◯ | велике коло | large circle | кільце | ring
• | жирна крапка | bullet | їжа точка крапка | pellet dot food
∙ | маленька крапка | small bullet | їжа точка крапка | pellet dot food
° | знак градуса | degree | бульбашка | bubble
⊙ | коло з крапкою | circled dot | кнопка ціль | button target
⊚ | коло в колі | circled ring | портал | portal
⊕ | коло з плюсом | circled plus | аптечка лікування | heal medkit
⊖ | коло з мінусом | circled minus
⊗ | коло з хрестом | circled times | міна заборона | mine` },
  { uk: 'трикутник', en: 'triangle', rows: `
▲ | трикутник угору | up triangle | шип гора | spike mountain
△ | порожній трикутник угору | white up triangle | гора | mountain
▼ | трикутник униз | down triangle | шип | spike
▽ | порожній трикутник униз | white down triangle
◄ | трикутник ліворуч | left pointer
► | трикутник праворуч | right pointer
◁ | порожній трикутник ліворуч | white left triangle
▷ | порожній трикутник праворуч | white right triangle
◢ | кут унизу праворуч | lower right triangle | схил | slope
◣ | кут унизу ліворуч | lower left triangle | схил | slope
◤ | кут угорі ліворуч | upper left triangle | схил | slope
◥ | кут угорі праворуч | upper right triangle | схил | slope
▴ | малий трикутник угору | small up triangle
▾ | малий трикутник униз | small down triangle
◂ | малий трикутник ліворуч | small left triangle
▸ | малий трикутник праворуч | small right triangle` },
  { uk: 'ромб ромбик', en: 'diamond rhombus', rows: `
◆ | чорний ромб | black diamond | кристал алмаз | gem crystal
◇ | білий ромб | white diamond | кристал порожній | gem empty
◈ | ромб у ромбі | diamond in diamond | кристал | gem
❖ | ромб із чотирьох | four diamonds
◊ | вузький ромб | lozenge` },
  { uk: 'зірка зірочка', en: 'star', rows: `
★ | чорна зірка | black star | бонус очки | bonus score
☆ | біла зірка | white star | порожня бонус | empty bonus
✦ | чотирикутна зірка | four pointed star | іскра блиск | sparkle
✧ | порожня чотирикутна зірка | white four pointed star | іскра блиск | sparkle
✪ | зірка в колі | circled star | медаль жетон | medal token
✯ | зірка-вертушка | pinwheel star
✶ | шестикутна зірка | six pointed star
✹ | дванадцятикутна зірка | twelve pointed star | вибух | explosion
✺ | шістнадцятикутна зірка | sixteen pointed star | вибух сонце | explosion sun
❂ | сонце в колі | circled sun star | сонце | sun
✱ | жирна зірочка-сніжинка | heavy asterisk | сніжинка | snowflake
❋ | зірочка з пелюсток | teardrop asterisk | квітка | flower
☼ | сонце з променями | sun with rays | сонце | sun
☾ | півмісяць | crescent moon | місяць ніч | night
☽ | півмісяць ліворуч | first quarter moon | місяць ніч | night` },
  { uk: 'масть карти', en: 'suit card', rows: `
♥${T} | чирва, чорне серце | heart suit | серце серденько сердечко життя | heart life hp
♡ | порожнє серце | white heart | серце серденько сердечко життя порожнє | heart life empty
♠${T} | піка | spade suit
♤ | порожня піка | white spade
♦${T} | бубна | diamond suit | ромб | diamond
♢ | порожня бубна | white diamond suit | ромб | diamond
♣${T} | трефа | club suit
♧ | порожня трефа | white club
❥ | серце-завиток | rotated heart | серце серденько | heart
❦ | серце-листок | floral heart | серце серденько | heart` },
  { uk: 'шахи фігура', en: 'chess piece', rows: `
♔ | білий король | white king
♕ | білий ферзь | white queen | королева
♖ | біла тура | white rook | вежа | tower
♗ | білий слон | white bishop | офіцер
♘ | білий кінь | white knight
♙ | білий пішак | white pawn | пішка
♚ | чорний король | black king
♛ | чорний ферзь | black queen | королева
♜ | чорна тура | black rook | вежа | tower
♝ | чорний слон | black bishop | офіцер
♞ | чорний кінь | black knight
♟${T} | чорний пішак | black pawn | пішка` },
  { uk: 'шашки шашка', en: 'checkers draughts', rows: `
⛀ | біла шашка | white draughts man
⛁ | біла дамка | white draughts king
⛂ | чорна шашка | black draughts man
⛃ | чорна дамка | black draughts king` },
  { uk: 'кубик кістка гральна', en: 'die dice', rows: `
⚀ | кубик: один | die face 1
⚁ | кубик: два | die face 2
⚂ | кубик: три | die face 3
⚃ | кубик: чотири | die face 4
⚄ | кубик: пʼять | die face 5
⚅ | кубик: шість | die face 6` },
  { uk: 'стрілка напрямок', en: 'arrow direction', rows: `
← | стрілка ліворуч | left arrow | вліво | left
↑ | стрілка вгору | up arrow | вверх | up
→ | стрілка праворуч | right arrow | вправо | right
↓ | стрілка вниз | down arrow | вниз | down
↔${T} | стрілка ліворуч-праворуч | left right arrow
↕${T} | стрілка вгору-вниз | up down arrow
↖${T} | стрілка вгору ліворуч | up left arrow
↗${T} | стрілка вгору праворуч | up right arrow
↘${T} | стрілка вниз праворуч | down right arrow
↙${T} | стрілка вниз ліворуч | down left arrow
⇐ | подвійна стрілка ліворуч | left double arrow | конвеєр | conveyor
⇑ | подвійна стрілка вгору | up double arrow | конвеєр | conveyor
⇒ | подвійна стрілка праворуч | right double arrow | конвеєр | conveyor
⇓ | подвійна стрілка вниз | down double arrow | конвеєр | conveyor
⇦ | порожня стрілка ліворуч | left white arrow
⇧ | порожня стрілка вгору | up white arrow
⇨ | порожня стрілка праворуч | right white arrow
⇩ | порожня стрілка вниз | down white arrow
➤ | наконечник стрілки | arrowhead | снаряд куля корабель | bullet ship
➜ | жирна стрілка праворуч | heavy right arrow
↺ | поворот проти годинникової | anticlockwise arrow | обертання | rotate
↻ | поворот за годинниковою | clockwise arrow | обертання | rotate
⇄ | стрілки туди й назад | right over left arrows | обмін | swap
⇅ | стрілки вгору й униз | up down arrows | обмін ліфт | swap lift
↯ | стрілка-блискавка | zigzag arrow | блискавка удар | lightning` },
  { uk: 'стіна рамка лінія лабіринт', en: 'wall box line border maze', rows: `
─ | горизонтальна лінія | horizontal line
│ | вертикальна лінія | vertical line
┌ | кут: униз і праворуч | corner down right
┐ | кут: униз і ліворуч | corner down left
└ | кут: угору і праворуч | corner up right
┘ | кут: угору і ліворуч | corner up left
├ | трійник праворуч | tee right
┤ | трійник ліворуч | tee left
┬ | трійник униз | tee down
┴ | трійник угору | tee up
┼ | перехрестя | cross
═ | подвійна горизонтальна лінія | double horizontal line
║ | подвійна вертикальна лінія | double vertical line
╔ | подвійний кут: униз і праворуч | double corner down right
╗ | подвійний кут: униз і ліворуч | double corner down left
╚ | подвійний кут: угору і праворуч | double corner up right
╝ | подвійний кут: угору і ліворуч | double corner up left
╠ | подвійний трійник праворуч | double tee right
╣ | подвійний трійник ліворуч | double tee left
╦ | подвійний трійник униз | double tee down
╩ | подвійний трійник угору | double tee up
╬ | подвійне перехрестя | double cross
╭ | круглий кут: униз і праворуч | round corner down right | труба | pipe
╮ | круглий кут: униз і ліворуч | round corner down left | труба | pipe
╯ | круглий кут: угору і ліворуч | round corner up left | труба | pipe
╰ | круглий кут: угору і праворуч | round corner up right | труба | pipe
╱ | діагональ угору | diagonal up
╲ | діагональ униз | diagonal down
╳ | діагональний хрест | diagonal cross | хрестик | x mark` },
  { uk: 'текстова гра рогалик', en: 'ascii roguelike text', rows: `
@ | равлик | at sign | гравець герой | player hero
# | решітка | hash | стіна | wall
. | крапка | full stop | підлога порожньо | floor empty
, | кома | comma | трава | grass
" | лапки | quotation mark | трава кущ | grass bush
' | апостроф | apostrophe | відчинені двері | open door
+ | плюс | plus | двері аптечка | door medkit
- | мінус | minus | двері стіна | door wall
= | дорівнює | equals | кільце міст | ring bridge
| | вертикальна риска | vertical bar | двері стіна | door wall
/ | скісна риска | slash | меч посох | sword staff
\\ | зворотна скісна риска | backslash | меч | sword
_ | підкреслення | underscore | підлога вівтар | floor altar
~ | тильда | tilde | вода лава хвиля | water lava wave
^ | дашок | caret | пастка шип гора | trap spike mountain
$ | долар | dollar | золото гроші монета | gold money coin
% | відсоток | percent | їжа | food
& | амперсанд | ampersand | демон монстр | demon monster
* | зірочка | asterisk | камінь коштовність вибух сніжинка | gem explosion snowflake
! | знак оклику | exclamation mark | зілля | potion
? | знак питання | question mark | сувій секрет | scroll secret
< | менше | less than | сходи вгору | stairs up
> | більше | greater than | сходи вниз | stairs down
: | двокрапка | colon | каміння | rubble
; | крапка з комою | semicolon` },
  { uk: 'цифра число', en: 'digit number', rows: `
0 | нуль | zero
1 | один | one
2 | два | two
3 | три | three
4 | чотири | four
5 | пʼять | five
6 | шість | six
7 | сім | seven
8 | вісім | eight
9 | девʼять | nine
① | один у колі | circled one
② | два в колі | circled two
③ | три в колі | circled three
④ | чотири в колі | circled four
⑤ | пʼять у колі | circled five
⑥ | шість у колі | circled six
⑦ | сім у колі | circled seven
⑧ | вісім у колі | circled eight
⑨ | девʼять у колі | circled nine
⑩ | десять у колі | circled ten
❶ | один у чорному колі | negative circled one
❷ | два в чорному колі | negative circled two
❸ | три в чорному колі | negative circled three
❹ | чотири в чорному колі | negative circled four
❺ | пʼять у чорному колі | negative circled five
❻ | шість у чорному колі | negative circled six
❼ | сім у чорному колі | negative circled seven
❽ | вісім у чорному колі | negative circled eight
❾ | девʼять у чорному колі | negative circled nine
❿ | десять у чорному колі | negative circled ten` },
  { uk: 'знак', en: 'sign mark', rows: `
☺${T} | усмішка | smiling face | гравець | player
☻ | чорна усмішка | black smiling face | гравець ворог | player enemy
♪ | нота | note | звук музика | sound music
♫ | ноти | notes | звук музика | sound music
✓ | галочка | check mark | так готово | yes done
✗ | хрестик | ballot x | ні промах | no miss
✘ | жирний хрестик | heavy ballot x | ні промах | no miss
✕ | хрест | x | хрестик промах закрити | cross miss close
✚ | жирний плюс | heavy plus | аптечка лікування хрест | medkit heal cross
† | хрест-кинджал | dagger | могила меч | grave sword
¤ | знак валюти | currency sign | монета | coin
§ | параграф | section sign | змія | snake
∞ | нескінченність | infinity
≈ | хвилі | almost equal | вода | water waves
≋ | потрійні хвилі | triple tilde | вода | water waves
≡ | три риски | triple bar | сходи драбина міст | ladder bridge
± | плюс-мінус | plus minus
× | множення | multiplication | хрестик | cross
÷ | ділення | division
√ | корінь | square root | галочка | check
¦ | розірвана риска | broken bar | двері | door
⌂ | будиночок | house | дім база | home base
⚑ | чорний прапор | black flag | прапорець міна | mine marker
⚐ | білий прапор | white flag | прапорець | marker
⌖ | приціл | position indicator | ціль курсор | crosshair cursor target` },
]
