# Thinky Games — перевірений дамп (хвиля 4, 2026-11-19, T364)

145 назв з `_thinky-dump-2026-11-09.tsv` (дамп хвилі 3, яких не було ні в корпусі, ні в чергах) перевірили два агенти дампу: 23 рядки злито в черги сімей (секції «Хвиля 4»), решту відсіяно — список нижче з причинами. `scripts/known_names.py` додає ці назви в `index/known-names.txt` (`skipped:`), щоб пошукові агенти не брали їх знову.

## Зріз 1

### Нотатки

- Зріз здебільшого відсіявся: 21 дубль черг і корпусу, 20 не-сіткових. Thinky-теги `record-and-replay` і `word` тут майже цілком 3D-ігри від першої особи або текстові.
- Найпродуктивніші джерела: Steam `api/storesearch` (id за один дешевий запит) і `confoundingcalendar.itch.io` — близько 250 пазлів на один екран за 2021–2025 з авторами й URL; варто окремо звірити їх із `known-names.txt`.
- Жанр «правила не сказано — вивести з єдиності розвʼязку» (FMTC, One to Three; родичі `thinky/understand`, LOK) у корпусі майже порожній. FMTC та In a Pickle («огірки штовхати, острів скидати локально») мають лише Thinky-сторінки — варто зняти через Chrome.
- DROD: `drod.md` описує лише набір King Dugan's Dungeon. Сиквели (JtRH, TCB, GatEB, TSS) варто давати підрозділами; правила є в бестіарії Caravel.
- Сумніви черги: «Transmission» з Thinky — імовірно, та сама гра, що «Transmission: Information Age» (loju) у `connect-rotate`; Fish Fillets 2 у `fish-fillets.md` записано «з памʼяті (?)».
- Не додав навмисно: 5 нонограм без нового правила, Proverbs (це Fill-a-Pix) і Voxelgram 2 (дві барви — як Picross 3D Round 2).

### Пропущено

- Islanders: New Shores — сиквел `build-sim/islanders` (field: free, сиквел там згадано); поле вільне
- The Looker — пародія на The Witness від першої особи; лінію панелей уже покриває `thinky/taiji-witness-panels`
- Transmission — дубль черги `connect-rotate` «Transmission: Information Age» (loju, 2014)
- Super Sudokoid: Final Transmission — уже aka в `pencil-logic/super-sudokoid`
- Picross S9 — серія Picross S уже в `pencil-logic/picross-variants` і `nonogram`; нових режимів не видно
- Automate It — дубль черги `program-robots` «Automate It: Factory Puzzle»
- The Sequence [2] — уже в рядку черги `program-robots` «[the Sequence]» (інші лінки: нові модулі)
- A Man Walks into a Scrollbar — є `thinky/a-man-walks-into-a-scrollbar`
- Bubble Sort — дубль черги `thinky` «Bubble Sort (Patrick Traynor)»
- Microban — дубль черги `push-slide` «Microban / Sokoban Plus»
- Nuworm — дубль черги `thinky` «nuworm (noa)»
- Push Blox — дубль черги `push-slide` «Push Blox 2 / Push Blox»
- Shall We Golf? — дубль черги `push-slide` (nebu soku)
- Two Worlds — дубль черги `thinky` «Two Worlds (nebu soku)»
- Humbug — дубль черги `push-slide` «Humbug (+ Humbug 2)»
- N Step Steve: Part 2 — дубль черги `thinky` «N Step Steve (Part 1–2)»
- Spelling Bee — дубль черги `word-number` «NYT Spelling Bee»
- Snakebird Complete — збірка Snakebird + Primer; Snakebird є в `thinky/snakebird`
- Bonfire Peaks: Lost Memories — DLC до `thinky/bonfire-peaks`
- Fish Fillets 2 — сиквел `thinky/fish-fillets` із тим самим ядром (?)
- SteamWorld Heist II — сиквел `tactics/steamworld-heist`: нові професії й морська мапа в реальному часі, бій на полі той самий
- Braid — платформер з вільною фізикою
- MotionRec — 2D-платформер з вільною фізикою (записує траєкторію стрибків)
- Hourglass — 3D від першої особи (Cyberwave, 2021)
- Playback Loop — 3D від першої особи (MapPack, 2024)
- The Entropy Centre — 3D від першої особи, фізика
- Lingo 2 — 3D від першої особи (?)
- Lenrual — середовищна 3D-головоломка в дусі The Witness, сітки не видно
- Shadow Gambit: The Cursed Crew — стелс-тактика в реальному часі з вільним рухом (?)
- Ouros — криві-сплайни через цілі, без сітки
- MHRD — текстова мова опису апаратури (?)
- NandGame — схема на вільному полотні (?); драбина NAND → CPU та сама, що в `program-robots/turing-complete`
- SIC-1 — текстовий асемблер SUBLEQ (?)
- Harmless Drudge — стекова езотерична мова (визначення слів, тест-кейси), сітки нема
- Birdigo — слова з колоди карт-літер, поля нема
- We Surrender! — закляття словами з клавіатури, сітки нема
- Fourteen Definitions — дописати бракуючі частини 14 визначень, сітки нема
- trms — знайти звʼязок між рядками слів без голосних, сітки нема
- Parseword — розбір однієї криптичної підказки на день, сітки нема (сторінка лише JS, ?)
- Rita — 3D-платформер зі збіркою класичних словесних пазлів (кросворд, пошук слів, ребус, анаграми)
- Decipher The Deck — карткова гра на відкриття правил; поля-сітки на сторінці нема (?)
- Murder by Numbers — візуальна новела + стандартні нонограми (`pencil-logic/nonogram`)
- Piczle Cross Adventure — пригода зі стандартними нонограмами
- Squeakross: Home Squeak Home — нонограми (сторінку не відкривав)
- Logiart Grimoire — нонограми (logiart — японська назва жанру; сторінку не відкривав)
- UFO 50 Nonograms — нонограми (сторінку не відкривав)
- Juufuutei Raden's Guide for Pixel Museum — стандартні нонограми Jupiter (5×5…40×30), мегапазли з кількох
- Voxelgram 2 — двоколірна 3D-нонограма, як Picross 3D Round 2 (`pencil-logic/picross-variants`)
- Proverbs — правила Fill-a-Pix (`pencil-logic/fill-a-pix`) на одному полотні з 54 000 клітин
- Rodocodo: Code Hour — дитяча гра в дусі Lightbot (`program-robots/lightbot`); правил на сторінці нема
- Thinky Dailies — щоденні пазли самого Thinky Games (сайт віддає 403)
- FMTC — лише Thinky (403): вивести правила сіткових пазлів з єдиності розвʼязку; сторінки автора не знайшов (Steam FMTC — інша гра, шутер)
- Blobs — сторінки гри не знайшов
- Witless - A Puzzling Journey — сторінки гри не знайшов
- In a Pickle — лише Thinky: штовхати огірки, локально скидати острів; сторінку itch не знайшов
- Perimeter — метроїдбрейнія-ARG з різнотипних логічних сіток (суми, KenKen-подібні) від Sufferbox; правил на сторінці нема

## Зріз 2

### Нотатки

- Найпродуктивніше: Steam-пошук → сторінка гри; хаб `confoundingcalendar.itch.io` дає itch-лінки всіх ігор календаря 2025 (знадобиться наступним дампам). WebSearch повертає переказ Thinky з механікою, але часто без лінка на саму гру.
- Зріз майже весь — дублі, клони класичних жанрів (нонограми, Fill-a-Pix, Star Battle, Nurikabe) і не-сіткові 3D/платформери: 7 рядків із 72.
- Dungeons & Diagrams досі стояв лише в «Межових» нотатках черг program-robots і hidden-deduction — тепер рядок pencil-logic. Opus Magnum: De Re Metallica (DLC 2026: 3 нові гліфи, варіант Sigmar's Garden) — кандидат у підрозділ `program-robots/opus-magnum`.
- Варті зняття через Chrome (опис є, лінка нема): Gunning for the Exit (сокобан, зайві ящики розстрілюються обмеженими набоями), Bobogram (нонограми з навмисно пропущеними правилами, 3D з кількох сіток).
- Побічно, поза зрізом: Hexcross (Steam 2127720, 2022) — схоже, гексові нонограми (?); у `known-names.txt` нема.

### Пропущено

Дублі корпусу або черг (11):
- Birds Organized Neatly — підрозділ у board-digital/cats-organized-neatly (нове лише Daily Puzzle).
- Manufactoria 2022 — описано в program-robots/manufactoria.
- Snakebird Primer — легша версія, вже в thinky/snakebird.
- Rush — у черзі program-robots як RUSH (Two Tribes).
- Boxception — у черзі thinky (joszs).
- Mimic — у черзі thinky як Mimic (Mimic Classic), ймовірно та сама гра.
- Give Up the Ghost — у черзі thinky як Give Up the Ghost: a puzzle checklist.
- Push Blox 2 — у черзі push-slide.
- Humbug 2 — у черзі push-slide (Humbug + Humbug 2).
- N Step Steve: Part 1 — у черзі thinky (Part 1–2).
- Letterlike — у черзі word-number і в word-number/paperback-adventures.

Клони наявних механік (16):
- Hexa-World-3D — Hexa Sort у 3D (Steam 3535110); є falling-match/hexa-sort.
- 2024: Mosaic Retrospective — Fill-a-Pix на одному полі ≈60 000 клітин (Steam 3380760); є pencil-logic/fill-a-pix.
- Mosaic of the Strange — той самий Fill-a-Pix автора Mark Ffrench, із сюжетом (Steam 3444650).
- Daily Akari — щоденний Light Up; є pencil-logic/light-up.
- Inkwell Stars — Star Battle (2 зірки на рядок, стовпець, регіон); є pencil-logic/star-battle.
- Nurikabe World — класичні правила Nurikabe у 3D-оформленні (Steam 2964540); є pencil-logic/nurikabe.
- Picross S+ — серія Picross S; режими Mega, Color, Clip уже в pencil-logic/picross-variants (сторінки не відкривав).
- Pictopix — нонограми (Steam 568320); є pencil-logic/nonogram.
- Pixelogic — Pixelogic: Nonograms Unlimited (Steam 3677530), класичні нонограми.
- Walfie's Nonograms — класичні нонограми (Steam-пошук порожній).
- Pepper's Puzzles — нонограми + режим Mosaic із сітки пазлів (Steam 642650).
- Voxelgram — 3D-нонограми як Picross 3D (Steam 1158470); є picross-variants.
- Yugo Puzzle — варіант Jelly no Puzzle від Qrostar (Steam 1693260), уже згаданий у thinky/jelly-no-puzzle.
- Confusion Conveyed — open-world продовження Conveyor Con-fusion (є push-slide/conveyor-confusion), ті самі конвеєри.
- The Codex of Alchemical Engineering — Flash-попередник Opus Magnum: маніпулятори переносять, трансмутують і звʼязують атоми; є program-robots/opus-magnum.
- Word Play — Balatro-подібна словесна (GMTK, Steam 3586660), сітки на сторінці нема; формат уже в word-number/wordatro.

DLC, збірки, сиквели, фан-рівні (8):
- Opus Magnum: De Re Metallica — DLC (Steam 3107410, 2026): 3 нові гліфи й варіант Sigmar's Garden; кандидат у підрозділ opus-magnum.
- Last Call BBS — збірка Zachtronics із 8 ігор (Steam 1511780); Dungeons & Diagrams винесено рядком; ChipWizard Professional ≈ KOHCTPYKTOP; 20th Century Food Court уже в нотатках черги program-robots; HACK*MATCH ≈ Magical Drop.
- Sudokuvania 2: Lineage of Logic — сиквел гігапазла LMG, уже згаданий у pencil-logic/sudokuvania; сторінки не знайшов (Steam-пошук порожній).
- DROD: The City Beneath — сиквел; Wikipedia називає лише рушій (катсцени, освітлення, змінні), нові елементи не названі.
- DROD: Gunthro and the Epic Blunder — сиквел; Wikipedia: «a couple of new game elements» без назв.
- The Descent of King Hesper — фанатський хол рівнів для DROD (Team Eclipsical), механіки DROD.
- Aha Alphabet — серія міні-ігор PuzzleScript від Toombler, по одній на літеру (напр. C is for Crab); збірка.
- Letibus Advent Calendar 2025 — за назвою адвент-календар пазлів (збірка); сторінки не відкривав.

Не сіткові (18):
- The Talos Principle 2 — first-person 3D.
- Viewfinder — first-person 3D (фото-перспектива).
- Causal Loop — first-person 3D, ехо-записи себе (Steam 3374460).
- Nomori — фізика, портали й гравітація (Steam 2932680).
- Re-Taped — real-time платформер із записом «привидів» (Steam 4192480).
- Glowkeeper — платформер «лінкування стихій» (Steam 3410660, itch oolimry); сітки джерела не підтвердили.
- Cryptmaster — first-person кроулер, бій вгадуванням слів (Steam 1885110).
- The Case of the Worst Day Ever — point-and-click детектив, висновки зі слів (Steam 3279410).
- Puzzle Spy International — 11 словесних пазлів і криптограм без сітки (Steam 3406690).
- Bracket City — текстові вкладені підказки.
- Minute Cryptic — одна криптична підказка на день, текст.
- Showy Homes — Wordle + шифр-етап, одноразова головоломка (blookerstein.itch.io/showy-homes); Wordle є.
- EmuDevz — програмування емулятора, поля нема (за тегами).
- QuantumPulse 2A — асемблер чипів із радіоканалами, поля нема (Steam 3175190).
- Shenzhen I/O — рішення куратора в черзі program-robots: схеми без поля-сітки.
- While True: Learn() — те саме рішення куратора (вузли без сітки).
- Alan's Automaton Workshop — блок-схема з вузлів і стрілок, сітки на сторінці нема (Steam 1289990).
- Songs of Conquest — HoMM-родич (уже згаданий у tactics/heroes-of-might-and-magic-3); ні Steam, ні Wikipedia гекс-бою не описують.

Одиничні пазли-картинки з прихованими правилами (3):
- Dual Threaded — одна картинка, правила треба вивести (nabokos.itch.io/dual-threaded); описувати нічого.
- Tunnels — одна мегакартинка з гліфами без правил (TheGreatEscaper); сторінки itch не знайшов.
- Rorschach's River — одна path-лінія через мешап пазлів Puzzlers Club; сторінки не знайшов.

Джерела не знайшов (10):
- Circuit Breaker — у Steam інша гра (1745960, покрокова стратегія); itch-кандидати (teethyweethy, bideogame) не схожі на line-drawing.
- Linea — у Steam інша гра (Linea, the Game — рефлекси).
- Fivefold — у Steam FIVEFOLD — інша гра (party roguelite).
- I Made Some Paper Puzzles — не шукав: WebSearch вичерпано.
- Gunning for the Exit — опис Thinky з пошуку є (сокобан + постріли по ящиках), сторінки itch не знайшов.
- Paintban — пошук нічого не дав.
- Bobogram — опис Thinky з пошуку є (нонограми з пропущеними правилами), сторінки itch не знайшов.
- How Hungry? — пошук нічого не дав.
- The Daily Spell — у Steam нема; WebSearch вичерпано.
- Type Word — у Steam нема; WebSearch вичерпано.
