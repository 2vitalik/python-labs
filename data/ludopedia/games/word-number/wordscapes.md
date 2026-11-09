---
title: Wordscapes
slug: wordscapes
aka: []
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: collect
year: 2017
platforms: [iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wordscapes", best: true, note: "колесо літер + кросвордна сітка, бонусні слова й монети, хінти Lightbulb/Rocket/Bullseye/Bees, 6000 рівнів + Master Levels, Brilliance, Daily Puzzle з метеликами, турніри, команди, Mt. Fortune"}
  - {kind: other, url: "https://apps.apple.com/us/app/wordscapes/id1207472156", note: "App Store: опис (6000+ кросвордів, фони-пейзажі, 5 мов), історія версій"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.peoplefun.wordcross", note: "Google Play (опис у фетчі не віддається)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordscapes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [swipe-gestures, path-drawing, word-validation, completion-detection, collect-all, sequential-levels, level-unlock, daily-puzzle, leaderboard, shop-window, game-screen, end-screen, theme-select, language-picker, +letter-wheel, +bonus-words, +shuffle-board, +paid-hint, +reveal-letter, +targeted-reveal, +coin-wallet, +brilliance-score, +monthly-reset-leaderboard, +daily-collectible-meter, +endless-after-campaign, +tournaments, +team-play, +team-hint-request, +daily-goals, +meta-minigame, +level-gated-features]
proposes: ["+effect:shuffle", "+cond:uses_each_letter_once", "+trigger:word_submitted", "+ui:letter-wheel", "+ui:coin-counter", "+ui:hint-buttons", "+window:tournament-window", "+window:team-window", "+feature:paid-hint", "+feature:team-help", "+card:letter-wheel"]
author: opus
date: 2026-11-09
---

# Wordscapes — проводиш пальцем по колесу з літер, і кожне знайдене слово само вписується в кросвордну сітку

## Суть
Внизу екрана — колесо з кількох літер, угорі — порожня кросвордна сітка, в якій заховано всі слова, що складаються з цих літер. Гравець свайпом зʼєднує літери колеса в слово; якщо воно є в сітці — вписується на своє місце, якщо це інше справжнє слово — зараховується як бонусне (монета). Рівень пройдено, коли заповнено всі клітини. Сам PeopleFun називає це сумішшю кросворда і word search; поруч — купа мета-шарів: монети й платні хінти, щоденний пазл, турніри, команди.

## Поле і час
- Два поля: **колесо** (до 7 літер на найбільших рівнях; будь-яка літера зʼєднується з будь-якою, кожна — раз) і **сітка** — кросворд-«скелет» із клітинами-слотами, довжини слів видно з форми сітки.
- Сітка — квадратна решітка з перетинами; знайдене слово відкриває літери й у перетинах інших слів.
- Тло — пейзаж, що змінюється з прогресом (фони відкриваються під час гри).
- Часу нема: «у власному темпі, з необмеженими спробами»; турніри обмежені календарем, не таймером рівня.
- Випадковість лише в хінтах (Lightbulb і Rocket відкривають випадкові клітини); рівні фіксовані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Літера колеса | tile | буква, позиція на колі | входить у шлях свайпу не більше одного разу; shuffle міняє позиції |
| Клітина сітки | tile | літера-відповідь; стан прихована / відкрита | відкривається, коли знайдено слово через неї або хінтом |
| Слово сітки | zone | довжина, напрям, клітини | заповнюється цілим, коли гравець його склав |
| Бонусне слово | pickup | слово зі словника не з сітки | +1 монета, лише при першому проходженні рівня |
| Монети | resource | лічильник | заробляються бонусними словами й подіями; витрачаються на хінти |
| Lightbulb | pickup | ціна в монетах (?) | відкриває одну випадкову клітину |
| Rocket | pickup | ціна (?) | розкидає кілька випадкових літер по сітці |
| Bullseye | pickup | ціна (?) | відкриває літеру в обраній гравцем клітині |
| Bees | pickup | — | кладуть на поле літери й монети |
| Brilliance | resource | очки | нараховується за знайдені слова (більше й довші — більше); не витрачається |
| Метелик (Daily Puzzle) | pickup | клітина на сітці | ловиться словом, що лягло через нього; випускає наступного |

## Правила (КОЛИ → ЯКЩО → ТО)
Складання слова:
- КОЛИ `input(swipe по літерах колеса)` → ЯКЩО `custom: «кожна літера колеса у шляху не більше одного разу»` → ТО `custom: «шлях = слово-кандидат»`; повернення на останню літеру знімає її (?).
- КОЛИ `custom: «палець відпущено»` → ЯКЩО `custom: «слово = незнайдене слово сітки»` → ТО `reveal(клітини слова)`, `counter(brilliance, +n)`.
- КОЛИ `custom: «палець відпущено»` → ЯКЩО `in_dictionary(word)` and `custom: «слова нема в сітці»` → ТО `custom: «зарахувати бонусне слово»`; ЯКЩО `first_time` (перше проходження рівня) → ТО `currency(+1)`.
- КОЛИ `custom: «палець відпущено»` → ЯКЩО not `in_dictionary(word)` or `custom: «власна назва»` → ТО `custom: «слово відхилено»` (власні назви не приймаються ніколи; і не кожне справжнє слово є в словнику гри).
- КОЛИ `custom: «слово вже знайдене»` → ТО `custom: «повторно не зараховується»` (?).
- Brilliance: більше слів і довші слова на рівні → більше Brilliance; таблиця глобальна й локальна, скидається щомісяця.

Хінти й shuffle:
- КОЛИ `input(shuffle)` → ТО `custom: «перемішати літери на колесі»` (безкоштовно).
- КОЛИ `input(Lightbulb)` → ЯКЩО `counter(coins, >=, ціна)` → ТО `currency(−ціна)`, `reveal(випадкова прихована клітина)`.
- КОЛИ `input(Rocket)` → ЯКЩО `counter(coins, >=, ціна)` → ТО `currency(−ціна)`, `reveal(кілька випадкових клітин)`.
- КОЛИ `input(Bullseye)` → `input(click cell)` → ТО `reveal(cell)`.
- КОЛИ `custom: «Bees»` → ТО `place(letters, coins)` на сітку (?).

Завершення і прогрес:
- КОЛИ `counter(клітини_відкрито, =, усі)` → ТО `win`, `window(end-screen)`, `next_level`.
- КОЛИ `counter(level, >, 6000)` → ТО `custom: «нескінченні Master Levels»`.
- Розмір сітки і довжина колеса зростають з номером рівня.

Daily Puzzle:
- КОЛИ `custom: «слово лягло через клітину з метеликом»` → ТО `pickup(butterfly)`, `spawn_at(butterfly, інша клітина)`, `counter(butterflies, +1)`.
- КОЛИ `counter(butterflies, >=, поріг)` → ТО `unlock(картинка)` — 4 картинки за місяць; КОЛИ `custom: «1-ше число місяця»` → ТО `custom: «шкала скидається»`.

Події й соціальне:
- КОЛИ `counter(level, >=, 65)` → ТО `unlock(турніри)`; Mt. Fortune — з рівня 62, Daily Goals — з 22, Wildlife — з 36.
- Команда: КОЛИ `input(запит хінта)` → ТО `custom: «тіммейти можуть надіслати хінт»`; КОЛИ `count(team_members, <, 10)` → ТО `custom: «командний турнір недоступний»`; призи ділять до 50 тіммейтів.
- Mt. Fortune: КОЛИ `input(відкрити подарунок)` → ЯКЩО `custom: «камінь»` → ТО `custom: «назад униз схилом»`; інакше `custom: «приз і крок угору»`.
- Перемога: усі клітини сітки відкрито · Поразки нема · Рахунок: Brilliance (місячна таблиця), монети як валюта.

## Керування і ввід
- Свайп по колу: торкнутися першої літери і, не відпускаючи, провести через наступні; відпустити — подати слово.
- Тап по кнопках: shuffle, хінти (Lightbulb, Rocket, Bullseye — потім тап по клітині).
- Навігація: тап по іконках подій, турнірів, команди, магазину (кошик).

## Вікна, меню, HUD
- `game-screen`: сітка, колесо літер (`letter-wheel`), кнопка shuffle, кнопки хінтів, `coin-counter`, індикатор бонусних слів (?), тло-пейзаж, `level-number`.
- `end-screen`: рівень пройдено, нагорода, перехід далі (?).
- `world-map`/`level-select` — прогрес за пакетами з пейзажами (?).
- `daily-window`: Daily Puzzle з метеликами й шкалою картинок місяця.
- `tournament-window` (custom-window): турніри будній (вт–чт) і вихідні (пт–нд), соло й командні; групи ~100 гравців (з 2020).
- `team-window` (custom-window): склад команди, запити хінтів.
- `leaderboard`: Brilliance глобально й локально, місячна.
- `shop-window`: монети, Piggy Bank, вимкнення реклами.
- `custom-window`: Mt. Fortune, Daily Goals, Quests, Wildlife (вилуплювати й збирати тварин; потрібен інтернет), Daily Gift.
- `settings-window` (?): мова (англійська, іспанська, німецька, французька, португальська за описом).
- Переходи: старт → `game-screen` поточного рівня → `end-screen` → наступний; з `game-screen` — іконки подій/турнірів/магазину.

## Фічі поза полем
- `levels-sequential` + `level-unlock` (6000 рівнів) + `mode-endless` (Master Levels).
- `daily-puzzle` + місячна колекція картинок; `daily-goals`, Quests, Daily Gift.
- Події за розкладом: Portrait Events (ср–чт), Butterfly Events (вт).
- `leaderboard-online` Brilliance зі щомісячним скиданням; турніри соло/командні.
- Команди: взаємні хінти, командні призи.
- Монетизація: монети, Piggy Bank, вимкнення реклами, Freecash-лінк у частині регіонів.
- `localization` (5 мов у описі), фони-пейзажі як `unlockables`.

## Варіації й родичі
- Word Cookies, Wordscapes Uncrossed (без сітки) (?) — той самий «колісний» ввід.
- Text Twist — анаграми з колеса без кросворду (?).
- Squaredle (`squaredle.md`), Boggle (`boggle.md`), Wordament (`wordament.md`) — шлях по сітці літер замість колеса (там сусідство обмежене; тут будь-яка літера з будь-якою).
- Bonza (`bonza.md`), Word search (`word-search.md`) — інші способи «заповнити сітку знайденими словами».
- **Осі варіацій:** ввід (колесо — повний граф / сітка — 8-сусідство / клавіатура) · ціль (заповнити кросворд / знайти N слів / набрати очки) · бонусні слова (монети / нема) · хінти (безкоштовні / платні монетами / від команди).

## Цікавинки для курсу
- Колесо літер: шлях свайпу по колу (кожна літера раз, повернення назад скасовує) — 📎.
- Перевірка слова: у сітці / у словнику (бонус) / відхилено — з урахуванням «вже знайдено» і «перше проходження» — 🌱.
- Генератор рівня: з набору літер знайти всі слова словника й скласти з частини з них звʼязний кросворд — 🥇.
- Хінти трьох видів (випадкова клітина, кілька випадкових, обрана) з ціною в монетах — 📎.
- Daily Puzzle з метеликом, що перескакує в нову клітину після вилову, і місячною шкалою — 🥉.
- Brilliance-таблиця зі скиданням щомісяця — 📎.

## Мапа на каталог
- Є: `swipe-gestures` + `path-drawing` ↔ свайп по колесу; `word-validation` ↔ словник і бонусні слова; `completion-detection` + `collect-all` ↔ усі слова сітки; `sequential-levels` + `level-unlock` ↔ 6000 рівнів; `daily-puzzle` ↔ Daily Puzzle; `leaderboard` ↔ Brilliance; `shop-window` ↔ монети; `theme-select` ↔ фони-пейзажі; `language-picker` ↔ 5 мов; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+letter-wheel` «Колесо літер: шлях по повному графу, кожна літера раз» · interface/input · 📎.
  - `+bonus-words` «Слова поза ціллю дають валюту» · game-logic/score · 🌱 · слот {only_first_play}.
  - `+targeted-reveal` «Хінт: відкрити обрану клітину» · game-logic/history · 🌱.
  - `+coin-wallet` «Валюта між рівнями» · game-logic/economy · 📎.
  - `+brilliance-score` «Незмінна сума очок для рейтингу» · interface/results · 🌱.
  - `+monthly-reset-leaderboard` «Таблиця зі скиданням за календарем» · interface/results · 📎.
  - `+daily-collectible-meter` «Збирати предмети в щоденних пазлах → шкала нагород місяця» · levels/bank · 📎.
  - `+endless-after-campaign` «Після кампанії — нескінченні рівні» · levels/progression · 🌱.
  - `+team-hint-request` «Попросити хінт у команди» · game-logic/opponent · 🥉.
  - `+level-gated-features` «Фічі відкриваються на рівні N» · levels/progression · 🌱.
  - `+meta-minigame` «Окрема мінігра-нагорода (Mt. Fortune)» · game-logic/economy · 🥉.
  - `+shuffle-board`, `+paid-hint`, `+reveal-letter`, `+tournaments`, `+team-play`, `+daily-goals` — уже пропоновані іншими файлами корпусу.

## Пропозиції до словників
- `+effect:shuffle` — перемішати літери/плитки без зміни їх набору.
- `+cond:uses_each_letter_once` — шлях використовує кожну літеру набору не більше разу (колесо, Boggle).
- `+trigger:word_submitted` — гравець подав слово (відпустив свайп, Enter).
- `+ui:letter-wheel` — колесо літер.
- `+ui:coin-counter` — лічильник монет.
- `+ui:hint-buttons` — ряд кнопок хінтів з цінами.
- `+window:tournament-window` — турніри з розкладом і групами.
- `+window:team-window` — команда, запити, призи.
- `+feature:paid-hint` — хінт за внутрішню валюту.
- `+feature:team-help` — взаємодопомога в команді.
- `+card:letter-wheel` — механіка вводу, якої в каталозі нема.

## Джерела
- ⭐ [Wikipedia: Wordscapes](https://en.wikipedia.org/wiki/Wordscapes) — колесо і сітка, бонусні слова (1 монета, лише перше проходження), власні назви не приймаються, хінти Lightbulb/Rocket/Bullseye/Bees, shuffle, 6000 рівнів → Master Levels, до 7 літер, Brilliance з місячним скиданням, Daily Puzzle з метеликами й 4 картинками, події, турніри з рівня 65, команди від 10 осіб і призи на 50, Mt. Fortune (62), Daily Goals (22), Wildlife (36).
- [App Store: Wordscapes](https://apps.apple.com/us/app/wordscapes/id1207472156) — опис розробника (6000+ кросвордів, фони-пейзажі, 5 мов), історія версій (Teams, Daily Gift, Wildlife).
- [Google Play: Wordscapes](https://play.google.com/store/apps/details?id=com.peoplefun.wordcross) — сторінка є, опис у фетчі не віддався.
- YouTube: пошук «wordscapes gameplay».

## Непевне
- (?) Ціни хінтів, ціна Rocket і скільки літер він розкидає, що саме роблять Bees — Wikipedia не дає чисел.
- (?) Чи є лічильник бонусних слів («банка») на `game-screen`, як виглядає відхилення слова (струс) і чи свайп назад знімає літеру — з памʼяті.
- (?) Мінімальна довжина слова (3?) і мінімальний розмір колеса — не перевірено.
- (?) Як згруповані рівні (пакети за пейзажами, екран вибору рівня) — App Store згадує лише фони, що відкриваються.
- (?) Word Cookies, Text Twist, Wordscapes Uncrossed як родичі — з памʼяті.
- (?) Поріг метеликів для картинки й поріг Brilliance — не бачив.
