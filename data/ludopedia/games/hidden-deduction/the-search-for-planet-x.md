---
title: The Search for Planet X
slug: the-search-for-planet-x
aka: [Planet X, Search for Planet X]
family: hidden-deduction
also: [board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: setup
  goal: score
year: 2020
platforms: [board + companion app (iOS, Android, web)]
links:
  - {kind: other, url: "https://rulespal.com/the-search-for-planet-x/rulebook", best: true, note: "правила: режими 12/18 секторів, обʼєкти й логіка розміщення, 4 дії з ціною в часі, конференції, фаза теорій і peer review, кінець гри, рахунок"}
  - {kind: other, url: "https://s3.amazonaws.com/static.foxtrotgames.com/content/2020/06/FG_PX_Rulebook_P1B_web.pdf", note: "офіційний rulebook PDF (Foxtrot Games © 2020): кнопки застосунку, рівні стартової інформації, приклади термінів"}
  - {kind: official, url: "https://foxtrotgames.com/planetx/", note: "сторінка гри: 2–4 гравці, 60–75 хв, вебзастосунок, FAQ, листи нотаток"}
  - {kind: other, url: "https://foxtrotgames.com/planetx/solo/", note: "соло-бот: фільтр сумісних карт 4 446 / 1 148 272, вибір скану за очікуваним виграшем на одиницю часу"}
  - {kind: play, url: "https://web.planetxapp.com/", note: "вебверсія застосунку-ведучого"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Search+for+Planet+X+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [cell-click, wrap-edges, turn-enforcement, ai-opponent, difficulty-levels, seed-share, objective-text, game-screen, end-screen, main-menu, help-window, mode-select, difficulty-select, tutorial-window, event-points, satisfy-constraints, +range-count-query, +time-track-turns, +rotating-visible-window, +app-referee, +delayed-claim-review, +first-claim-bonus, +research-clue-shop, +public-clue-schedule, +consistent-world-filter]
proposes: ["+trigger:board_reaches", "+effect:advance_time", "+cond:in_visible_sky", "+cond:consecutive_range", "+role:sector", "+ui:time-track", "+ui:peer-review-track", "+ui:note-sheet", "+window:game-code", "+window:action-menu", "+window:starting-info", "+feature:app-referee", "+card:range-count-query", "+card:time-track-turns", "+card:rotating-visible-window", "+card:app-referee", "+card:delayed-claim-review", "+card:first-claim-bonus", "+card:research-clue-shop", "+card:public-clue-schedule", "+card:consistent-world-filter"]
author: opus
date: 2026-11-09
---

# The Search for Planet X — астрономи опитують застосунок про кільце секторів, щоб першими вирахувати, де ховається планета, що «виглядає порожньою»

## Суть
Змагальна дедукція на 2–4 гравців (плюс соло з ботом). Застосунок-ведучий генерує приховане кільце з 12 (Standard) або 18 (Expert) секторів: у кожному або один обʼєкт, або справжня порожнеча. Гравці таємно ставлять запити — «скільки комет у секторах 3–6?», «що в секторі 8?», «яке логічне правило діє в цій грі?» — і кожен запит **коштує часу**: хто витратив менше, той ходить частіше. Паралельно гравці публікують теорії «у секторі N — астероїд», які з затримкою проходять peer review. Гра закінчується, коли хтось правильно назве сектор Planet X **і** обʼєкти в обох сусідніх секторах.

## Поле і час
- Кільце секторів 1…12 / 1…18 (`field: 1d` з замиканням: сектор 12 сусідить із 1); «прямо навпроти» = через 180° (у Standard 4 ↔ 10).
- **Видиме небо** — рівно половина секторів (6 / 9), що видно у вирізі поворотної дошки Землі. Survey і Target — лише по видимому небу; теорії — на будь-який непідтверджений сектор.
- **Трек часу** по зовнішньому краю: пішак кожного гравця сунеться вперед на ціну дії. Активний — той, чий пішак **найдалі позаду**; хто приходить у сектор із чужими пішаками, стає попереду них.
- Після кожного ходу дошку Землі обертають за годинниковою до найзаднішого пішака; на шляху — іконки конференцій (X1, X2) і фаз теорій.
- Стан світу знає лише застосунок; гравці бачать свої приватні відповіді (лист нотаток за ширмою) і публічні події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Сектор | zone | номер 1–12 / 1–18 | містить рівно один обʼєкт або справді порожній |
| Астероїд | object | 4 | кожен сусідить хоча б з одним астероїдом (дві пари або група з 4) |
| Комета | object | 2 | лише в секторах 2, 3, 5, 7, 11 (Expert: + 13, 17) |
| Газова хмара | object | 2 | сусідить хоча б з одним справді порожнім сектором |
| Карликова планета | object | 1 / 4 (Expert) | не сусідить з Planet X; Expert — 4 у смузі рівно з 6 секторів, по одній на кінцях |
| Planet X | object | 1 | не сусідить з карликовою; у Survey і Target **виглядає порожньою** |
| Справжня порожнеча | static | 2 / 5 (Expert) | сектор без обʼєкта |
| Пішак гравця | player | позиція на треку часу | визначає, хто ходить |
| Дошка Землі | object | стрілка, виріз | обертається, змінює видиме небо, запускає конференції й фази теорій |
| Жетон цілі (Target) | supply | 2 на гравця | витрачається на дію Target |
| Жетон теорії | supply | 12 на гравця в його кольорі | ставиться сорочкою на трек peer review сектора |
| Трек peer review | zone | 4 клітинки на сектор | теорія входить ззовні й сунеться всередину; у центрі — перевірка |
| Тема дослідження | pickup | одна інформація | дає логічне правило саме цієї партії |
| Бот (соло) | enemy | ходи зашиті під код гри | грає справжніми діями й дедукує лише з їхніх відповідей |

## Правила (КОЛИ → ЯКЩО → ТО)
- Сетап: КОЛИ `game_start` → ТО `custom: «застосунок генерує розкладку за правилами астрономії й показує код гри; інші пристрої приєднуються за кодом»`; кожен гравець обирає рівень і отримує стартову інформацію (Beginner / Experienced / Genius).
- КОЛИ `turn_end(active)` → ТО `custom: «активним стає гравець, чий пішак найдалі позаду на треку часу»`.
- Survey: КОЛИ `input(survey, type, range)` → ЯКЩО `custom: «діапазон — послідовні сектори видимого неба, 1–6 (Expert 1–9)»` → ТО `feedback(count(type, range))` приватно; `counter(time, +4)` для 1–3 секторів, `+3` для 4–6, `+2` для 7–9.
- Survey комет: ЯКЩО `custom: «діапазон починається й закінчується на секторі, де можлива комета»` → інакше `block`.
- КОЛИ `input(survey, empty, range)` → ТО `custom: «сектор Planet X рахується як порожній»`.
- Target: КОЛИ `input(target, sector)` → ЯКЩО `has(player, target_token)` і `custom: «сектор у видимому небі»` → ТО `take(player, target_token)`, `reveal(sector)` приватно (Planet X — «порожньо»), `counter(time, +4)`.
- Research: КОЛИ `input(research, topic)` → ЯКЩО `custom: «минула дія гравця — не Research»` і `custom: «тему ще не досліджено»` → ТО `message(logic_rule)` (напр. «карликова в межах 2 секторів від комети»), `counter(time, +1)`.
- Locate: КОЛИ `input(locate, sector, left_obj, right_obj)` → ТО `feedback(correct?)`, `counter(time, +5)`; оголошується лише успіх/невдача, не сектор.
- КОЛИ `custom: «Planet X знайдено правильно»` → ТО `custom: «пішак +5 без обертання дошки»`, далі фінальні можливості й `game_over`.
- Обертання: КОЛИ `turn_end(active)` → ТО `rotate(earth_board, to_farthest_back_pawn)`.
- Конференція: КОЛИ `reach(earth_arrow, conference_icon)` → ЯКЩО `first_time` → ТО `message(planet_x_rule)` для всіх.
- Фаза теорій: КОЛИ `reach(earth_arrow, theory_icon)` → ТО кожен таємно обирає до 1 (Expert 2) теорій, `place(player, theory)` сорочкою на зовнішню клітинку треку сектора — у порядку гравців ззаду наперед; потім `custom: «усі теорії на треках зсуваються на клітинку всередину»`.
- Обмеження теорій: ЯКЩО `state(sector, confirmed)` → `block`; ЯКЩО `custom: «у гравця вже така сама теорія в цьому секторі»` → `block`; ЯКЩО `count(player_theories(type), =, 0)` → `block`.
- Peer review: КОЛИ `enter(theory, inner_space)` → ТО `reveal(theory)`; ЯКЩО правильна → ТО `set_state(sector, confirmed)`, `custom: «перевірити решту теорій сектора»`; ЯКЩО хибна → ТО `disappear(theory)`, `counter(time_of_owner, +1)` (штраф).
- Фінал: КОЛИ `game_over` → ЯКЩО `custom: «гравець позаду переможця на 1–3 сектори»` → ТО `choose(1 theory | locate)`; ЯКЩО на 4–5 → `choose(до 2 theories | locate)`; потім `reveal(all)`, хибні теорії скидаються.
- Рахунок: КОЛИ `game_over` → ТО `score(+1)` за кожен сектор, де гравець першим (або разом з першими) подав правильну теорію; `score(+2)` астероїд, `+3` комета, `+4` газова хмара, `+4` карликова (Expert `+2`); Planet X — `score(+10)` першому, іншим правильним `+2` за кожен сектор відставання (2–10).
- Нічия: більше очок за Planet X → більше бонусів першості → спільна перемога.
- Перемога: найбільше очок · Поразки як такої нема · Рахунок: як вище.

## Керування і ввід
- Настолка: гравець оголошує дію й параметри (тип і діапазон) уголос, вводить у застосунок, відповідь записує на лист нотаток за ширмою.
- Застосунок: головний екран «Start New Game» (→ режим → код) або «Enter Game Code» → «Join Game»; меню дій: Survey · Target · Research · Locate Planet X · Planet X Conference · Peer Review · Reveal Objects; соло — «Bot: Take Turn» і «Bot: Submit Theory».
- Застосунок не відстежує видиме небо й штрафи часу — це роблять гравці на дошці (FAQ).

## Вікна, меню, HUD
- `main-menu` (застосунок): Start New Game · Enter Game Code · соло-гра.
- `mode-select`: Standard / Expert. `game-code` (custom-window): код партії для інших пристроїв.
- `difficulty-select` → `starting-info` (custom-window): рівень досвіду й стартові факти, які гравець переписує в лист.
- `action-menu` (custom-window): кнопки дій; екрани вибору типу обʼєкта й діапазону секторів; екран відповіді (кількість / обʼєкт / правило / так-ні).
- `game-screen` (фізичний стіл): кільце секторів, дошка Землі з вирізом видимого неба, `time-track` з пішаками, `peer-review-track` кожного сектора, `note-sheet` за ширмою (таблиця секторів × типів, рядок рахунку).
- `end-screen`: Reveal Objects — повна розкладка; підрахунок очок на листі.
- `help-window` / `tutorial-window`: правила й відеотуторіал, на які веде сайт.
- Переходи: main-menu → mode-select → game-code → difficulty-select → starting-info → action-menu ↔ відповідь → … → Reveal Objects → end-screen.

## Фічі поза полем
- `mode-classic` (Standard, 12) і `custom-difficulty`-подібний Expert (18 секторів, більше порожнеч і карликових, до 2 теорій за фазу, Survey до 9).
- `difficulty-presets`: рівень стартової інформації окремо для кожного гравця — гандикап у змагальній грі.
- `seed-input`: код гри — той самий світ на всіх пристроях; соло-бот зашитий під код (той самий код — ті самі дії бота).
- `ai-opponent-levels` (соло): бот без стартових фактів у Standard, 4 або 8 фактів у Expert.
- Вебверсія застосунку, листи нотаток для друку.

## Варіації й родичі
- [Cryptid](cryptid.md) — дедукція прихованої клітини з запитами до суперників; [Clues by Sam](clues-by-sam.md) — логічні підказки; [Code Name: Sector](code-name-sector.md) — пошук прихованого обʼєкта запитами до машини-ведучого.
- [Battleship](battleship.md) — запит «що в клітині?» (тут Target), [Minesweeper](minesweeper.md) — «скільки в околі?» (тут Survey по діапазону).
- **Осі варіацій**: ведучий «застосунок / людина / нема»; запит «кількість у діапазоні / вміст клітини / правило»; черга «за колом / за треком часу»; заявка «миттєва / з затримкою peer review»; поле «кільце / сітка / граф».

## Цікавинки для курсу
- Генератор розкладки за правилами астрономії (комети на простих, пари астероїдів, хмара біля порожнечі…) — перебір/бектрекінг; 4 446 варіантів у Standard — 🥉.
- Фільтр сумісних світів: множина розкладок, після кожної відповіді — відкинути несумісні; хто знає Planet X — 🥈.
- Бот, що обирає скан з найкращим відношенням очікуваного виграшу до ціни часу — 🥇 (очікувана інформація / теорія рішень).
- Трек часу замість черги ходів: активний — найзадніший, тай-брейк «хто прийшов останнім, той попереду» — 📎.
- Затримана перевірка заявок (4-клітинковий трек peer review) з бонусом першості — 📎.
- Обертове видиме небо як вікно доступних запитів — 🌱.

## Мапа на каталог
- Є: `cell-click` (вибір сектора) · `wrap-edges` (кільце) · `turn-enforcement` · `ai-opponent` (соло-бот) · `difficulty-levels` (Beginner/Experienced/Genius) · `seed-share` (код гри) · `objective-text` · `event-points` (очки за теорії) · `satisfy-constraints` (правила розміщення) · `game-screen` / `end-screen` / `main-menu` / `help-window` / `mode-select` / `difficulty-select` / `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+range-count-query` «Запит: скільки обʼєктів типу в діапазоні» · game-logic/info · 🌱 · слот {range_cost}.
  - `+time-track-turns` «Черга ходів за треком часу: ходить найзадніший» · game-logic/turns · 📎.
  - `+rotating-visible-window` «Вікно доступних клітин, що обертається з часом» · field/visibility · 🌱.
  - `+app-referee` «Застосунок тримає прихований стан і відповідає на запити» · architecture · 📎.
  - `+delayed-claim-review` «Заявка перевіряється із затримкою; штраф за хибну» · game-logic/info · 📎.
  - `+first-claim-bonus` «Бонус першому, хто правильно заявив» · scoring · 🌱.
  - `+research-clue-shop` «Купити загальне правило світу за час» · game-logic/info · 🌱.
  - `+public-clue-schedule` «Публічні підказки за розкладом (конференції)» · game-logic/info · 🌱.
  - `+consistent-world-filter` «Множина сумісних світів, що звужується відповідями» · ai/logic · 🥈.

## Пропозиції до словників
- `+trigger:board_reaches` — обертова дошка/стрілка дійшла до іконки події (конференція, фаза теорій); зараз через `reach`.
- `+effect:advance_time` — пішак гравця сунеться треком часу на ціну дії (замість `counter(time, +n)`).
- `+cond:in_visible_sky` — клітина в поточному видимому вікні поля.
- `+cond:consecutive_range` — вибрані клітини утворюють неперервний діапазон.
- `+role:sector` — клітина кільця, що містить рівно один обʼєкт або порожнечу (відмінна від `zone` області).
- `+ui:time-track` — трек часу з пішаками, що визначає чергу.
- `+ui:peer-review-track` — короткий трек із 4 клітинок для кожної заявки.
- `+ui:note-sheet` — приватний лист нотаток (сектори × типи) за ширмою.
- `+window:game-code` — показ/введення коду партії для синхронізації пристроїв.
- `+window:action-menu` — меню дій застосунку-ведучого.
- `+window:starting-info` — екран стартових фактів обраного рівня.
- `+feature:app-referee` — фізична гра з цифровим ведучим прихованого стану.

## Джерела
- ⭐ [RulesPal: The Search for Planet X](https://rulespal.com/the-search-for-planet-x/rulebook) — повний конспект правил: режими, обʼєкти, дії, конференції, теорії, кінець гри, рахунок, тай-брейки, терміни.
- [Rulebook PDF (Foxtrot Games)](https://s3.amazonaws.com/static.foxtrotgames.com/content/2020/06/FG_PX_Rulebook_P1B_web.pdf) — кнопки застосунку, код гри, рівні досвіду, appears empty vs truly empty, правила подачі теорій, приклади; автори Ben Rosset і Matthew O'Malley, © 2020.
- [Foxtrot Games: сторінка гри](https://foxtrotgames.com/planetx/) і [FAQ](https://foxtrotgames.com/planetx/faq/) — 2–4 гравці, 60–75 хв, 13+; застосунок не стежить за видимим небом і штрафами.
- [Foxtrot Games: соло](https://foxtrotgames.com/planetx/solo/) — алгоритм бота, кількість сумісних розкладок, кнопки бота, версії застосунку 2020.
- YouTube: пошук «Search for Planet X how to play».

## Непевне
- (?) Перелік тем Research (скільки й з якими літерами) і правила конференцій X1/X2 — їх видає застосунок, у джерелах нема.
- (?) Склад 12 жетонів теорії за типами (ймовірно 4 астероїди, 2 комети, 2 хмари, 4 карликові — з того, що в Standard лишають 1 карликову з 4).
- (?) Скільки фактів дає кожен рівень стартової інформації і скільки іконок фаз теорій на дошці Землі.
- (?) Довжина треку часу й розташування іконок на дошці — не бачив.
- (?) Число розкладок: сторінка соло дає 4 446 (Standard) і 1 148 272 (Expert), а ранній прототип — 1 138 272.
- (?) Рік: © 2020 у rulebook; соло додано в застосунок 10.03.2020, тобто гра в руках гравців уже на початку 2020 — точну дату виходу не бачив.
