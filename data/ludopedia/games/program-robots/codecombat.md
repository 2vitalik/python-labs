---
title: CodeCombat
slug: codecombat
aka: [Code Combat]
family: program-robots
also: []
klass: avatar
axes:
  field: free
  time: programmed
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2013
platforms: [web]
links:
  - {kind: official, url: "https://codecombat.com/", best: true, note: "грати одразу в браузері, перший рівень без акаунта; Python і JavaScript"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/CodeCombat", note: "історія, засновники, open source 2014, 11 курсів, Ozaria"}
  - {kind: other, url: "https://codecombat.com/db/level/dungeons-of-kithgard", note: "JSON першого рівня: цілі, required/restricted методи, шипи, камені руху"}
  - {kind: other, url: "https://codecombat.com/db/level/master-of-names", note: "JSON рівня з findNearestEnemy: цілі «вижити» і «вбити трьох огрів»"}
  - {kind: other, url: "https://github.com/codecombat/codecombat", note: "код гри (MIT, арт CC-BY), рівні сайту не відкриті"}
  - {kind: other, url: "https://web.cs.wpi.edu/~rich/courses/imgd4600-c15/analyses/code-combat/index.html", note: "аналіз WPI 2015: спорядження, самоцвіти, прапорці на мапі, мультиплеєр"}
  - {kind: other, url: "https://codakid.com/codecombat-review-everything-you-need-to-know-in-2020/", note: "огляд: moveRight/Left/Up/Down, курси, підписка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=codecombat+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, sensor-predicates, code-editor-window, hp-damage, item-pickup, inventory, inventory-items, shop-between-levels, shop-catalog, shop-window, character-select, world-map, map-window, sequential-levels, level-unlock, save-progress, collect-all, destroy-all-enemies, reach-exit, environment-death, player-death, chase-player, enemy-patrol, in-game-editor, editor-window, online-multiplayer, rating-system, leaderboard, objective-text, language-picker, game-screen, end-screen, +real-language-code, +equipment-unlocks-api, +goal-checklist, +required-restricted-methods, +clean-code-bonus, +code-arena-ladder, +frame-simulation-playback, +stuck-code-warning]
proposes: ["+feature:equipment-unlocks-api", "+feature:required-restricted-methods", "+feature:clean-code-bonus", "+feature:code-arena-ladder", "+ui:goal-checklist", "+ui:method-docs-palette", "+ui:simulation-scrubber", "+cond:api_available(method)", "+trigger:goal_done(goal)"]
author: opus
date: 2026-11-09
---

# CodeCombat — герой у фентезійному данжені рухається й бʼється лише за кодом справжньою мовою (Python, JavaScript)

## Суть
Гравець пише програму справжньою мовою (Python, JavaScript; історично ще CoffeeScript, Lua, Java), де `hero` — обʼєкт з методами: `hero.moveRight()`, `hero.attack(enemy)`, `enemy = hero.findNearestEnemy()`. Натиснув Run — світ рівня симулюється покадрово, і герой виконує код серед шипів, самоцвітів і огрів. Рівень має **список цілей** («вижити», «зібрати самоцвіт», «вбити трьох огрів», бонус «чистий код»), а **спорядження героя визначає API**: предмет дає метод, без предмета рівень не пройти. Між рівнями — мапа кампанії, магазин за самоцвіти, вибір героя; окремо — арени, де код гравця бʼється з кодом інших гравців.

## Поле і час
- Поле — вид згори, **вільні координати** (у JSON рівня: герой у (6, 18), самоцвіт у (30, 5), фон 42×36 одиниць). Перший світ — коридори данжена, де рух іде між **каменями руху** (movement stones), тож він поводиться як сітка; далі (`moveXY(x, y)` (?)) — вільний рух.
- Шари: фон, перешкоди-стіни, шипи (hazard), предмети, юніти (герой, огри), невидимі тригери-цілі (goal trigger).
- Час `programmed`: код виконується, світ рахується **покадрово** (розвʼязок першого рівня — 78 кадрів), потім програється; анімація реальна, але вводу під час симуляції нема (окрім пізніх рівнів, де WPI згадує ручне керування (?)).
- Інформація повна в межах рівня; вороги з патрулем і атакою діють самі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP; слоти спорядження: торс, голова, книга програмування, права рука, очі, ноги | виконує код гравця; доступні методи = з предметів |
| Самоцвіт (gem) | pickup | — | береться дотиком; ціль «зібрати» і валюта мети |
| Шипова стіна | hazard | — | дотик шкодить/вбиває (ціль «уникай шипів») (?) |
| Перешкода / стіна | static | — | непрохідна |
| Камінь руху | terrain | позиція | точки, між якими ходять `moveRight/Left/Up/Down` (?) |
| Тригер цілі | zone | позиція | ціль `getToLocations`: герой мусить дійти |
| Огр (Thabt, Trog, Kraster…) | enemy | HP, атака, патруль | патрулює, атакує героя поруч |
| Спорядження (меч, окуляри, чоботи, молот…) | pickup | слот, методи | надягається між рівнями; дає методи (`attack`, `findNearestEnemy`…) |
| Лава, лазерні промені | hazard | — | перешкоди Kithgard (з опису в Chrome Web Store) (?) |
| Kith / статуя, referee | static | — | службові обʼєкти рівня: сценка й суддя перемоги |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(moveRight)` → ЯКЩО `free(cell)` → ТО `custom: «герой іде до наступного каменя руху праворуч»`; аналогічно `moveLeft/Up/Down`; пізніше з аргументом кроків `moveRight(3)`.
- КОЛИ `exec(moveXY(x, y))` → ЯКЩО `custom: «метод доступний (предмет є, метод не restricted)»` → ТО `move(hero, (x, y))` (?).
- КОЛИ `contact(hero, spikes)` → ТО `damage(n)` (?); ціль «humans survive» зривається, якщо `hp_zero(hero)`.
- КОЛИ `contact(hero, gem)` → ТО `pickup`, `counter(gems, +1)`.
- КОЛИ `reach(hero, goal_trigger)` → ТО `custom: «ціль getToLocations виконана»`.
- КОЛИ `exec(findNearestEnemy)` → ТО `custom: «повернути найближчого ворога або порожнє значення»` — тому в коді `if enemy:` перед атакою.
- КОЛИ `exec(attack(target))` → ЯКЩО `in_range(hero, target, n)` → ТО `damage(n)`; інакше `custom: «герой підходить до цілі»` (?).
- КОЛИ `in_range(ogre, hero, n)` → ТО `damage(n)` (огр бʼє героя).
- КОЛИ `hp_zero(ogre)` → ТО `disappear_b`, `counter(defeated, +1)`.
- КОЛИ `counter(defeated, =, quota)` → ТО `custom: «ціль killThangs виконана»` («Defeat the three ogres»).
- КОЛИ `hp_zero(hero)` → ТО `lose`.
- КОЛИ `all_constraints_met` (усі обовʼязкові цілі) → ТО `win`, `window(end-screen)`, `currency(+gems)`, `custom: «+XP»`.
- КОЛИ `custom: «у коді нема problems (помилок і попереджень)»` → ТО `custom: «прихована бонусна ціль clean-code»`.
- КОЛИ `exec(cmd)` → ЯКЩО `custom: «метода нема серед доступних: предмет не надягнуто»` → ТО `crash`, `message(помилка з підказкою)`.
- КОЛИ `custom: «рівень вимагає required-метод, а код його не викликає / викликає restricted-метод»` → ТО `message(підказка)` (?) — у JSON першого рівня: required `moveRight`, restricted `moveXY`.
- КОЛИ `custom: «код завис (нескінченний цикл)»` → ТО `message(попередження з порадами)`.
- КОЛИ `input(buy item)` → ЯКЩО `counter(gems, >=, price)` → ТО `currency(−price)`, `give(hero, item)`.
- КОЛИ `input(equip item)` → ТО `custom: «методи предмета стають доступними в коді»`.
- КОЛИ `exec(say(text))` → ТО `message(text)` (?) — у частині рівнів «сказати пароль» є ціллю (?).
- КОЛИ `exec(buildXY(kind, x, y))` → ЯКЩО `has(hero, hammer)` → ТО `spawn_at(fence|trap, (x, y))` (?).
- Арена: КОЛИ `custom: «двоє гравців подали код за людей і огрів»` → ТО `custom: «симуляція матчу, зміна рейтингу»`.
- Перемога: виконано всі обовʼязкові цілі · Поразка: герой загинув або цілі не виконані до кінця симуляції (?) · Рахунок: самоцвіти й XP; на мапі прапорець червоний = пройдено, сірий = невдала спроба.

## Керування і ввід
- Набір коду в редакторі справа (клавіатура); стартовий шаблон з коментарями («Type your code below and click Run»).
- Кнопка Run — симулювати й показати; повторні спроби з правками.
- Між рівнями: вибір героя, надягання предметів, покупка в магазині, вибір мови в меню інвентаря.
- Прямого керування героєм у кампанії нема (окремі пізні рівні — (?)).

## Вікна, меню, HUD
- `main-menu` (сайт): Play Now → `map-window` першого світу без акаунта.
- `map-window` / `world-map`: вузли-рівні з прапорцями (червоний — пройдено, сірий — невдало); зірочкові рівні за самоцвіти/підписку.
- `character-select` — вибір героя (стартові Anya Weston і Tharin Thunderfist, інші відкриваються).
- `inventory-window` — слоти спорядження героя; випадний список мови програмування.
- `shop-window` — предмети за самоцвіти.
- `game-screen`: поле зліва, `code-editor-window` справа, `goal-checklist` (цілі зі статусом), HUD `hp-bar` героя, кнопка Run; `method-docs-palette` з доступними методами (?); `simulation-scrubber` — повзунок кадрів симуляції (?).
- `help-window` / підказки рівня; попередження «код завис».
- `end-screen` — нагорода: самоцвіти, XP, іноді новий предмет.
- `editor-window` — редактор рівнів (відкритий з 2014).
- `leaderboard` — драбина арен; учительська панель — `custom-window` (курси, прогрес учнів).
- Переходи: мапа → (герой/інвентар/магазин) → рівень → Run → end-screen → мапа.

## Фічі поза полем
- `levels-sequential`, `level-unlock`, `world-map` — лінійна кампанія світами (перший — Kithgard Dungeon), ~сотні рівнів; 11 курсів (Computer Science 1–6, Web Dev 1–2, Game Dev 1–3).
- `meta-progression` — XP, самоцвіти, предмети й герої лишаються між рівнями.
- `equipment-unlocks-api` — предмет = нові методи; без потрібного предмета рівень не проходиться навіть з правильним кодом.
- `required-restricted-methods` — рівень вимагає/забороняє певні методи.
- `clean-code-bonus` — прихована бонусна ціль «без problems».
- `code-arena-ladder` — мультиплеєр: код проти коду, рейтинг.
- `level-editor`, `mod-support` (open source: код MIT, арт CC-BY).
- Підписка: додаткові гілки, герої, щомісячні самоцвіти; акаунт — для збереження прогресу; класи з кодом вчителя.
- `localization` (у JSON рівнів — переклади, напр. китайська назва першого рівня).

## Варіації й родичі
- Ozaria (2019) — сюжетна гра тієї ж компанії; CodeCombat Junior та інші продукти (?).
- Родичі в корпусі: [Karel](karel.md) (методи робота й сенсори), [Screeps](screeps.md) і [Bot arenas](bot-arenas.md) (код проти коду онлайн), [The Farmer Was Replaced](the-farmer-was-replaced.md) (справжній Python-подібний код + прогресія відкриває API), [Untrusted](untrusted.md) (JavaScript у грі), [Lightbot](lightbot.md) (той самий шлях від команд до циклів, але іконками).
- **Осі варіацій**: мова (іконки / блоки / справжня мова) · як відкривається API (з рівнем / за спорядження / за дослідження) · хто суперник (статичний рівень / AI-огри / код іншого гравця) · рух (камені-сітка / вільні координати).

## Цікавинки для курсу
- `hero`-обʼєкт з методами, що викликає Python-код студента в пісочниці з лімітом кроків — 🥈 (sandbox + ліміт + звʼязок з рушієм).
- Спорядження відкриває методи (API як інвентар) — 📎.
- Список цілей рівня (required, optional, hidden bonus) зі статусами — 🥉.
- `findNearestEnemy` + `attack` з підходом до цілі — 🥉 (пошук найближчого + рух до радіуса).
- Покадрова детермінована симуляція і програвання з повзунком — 🥈.
- Required/restricted методи — статичний аналіз коду студента (AST) — 🥈.
- Арена «код проти коду» з рейтингом Elo — 🥇.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ код героя; `sensor-predicates` ↔ `findNearestEnemy`, перевірки `if enemy`; `code-editor-window` ↔ редактор справа; `hp-damage`, `item-pickup`, `inventory`/`inventory-items` ↔ спорядження; `shop-between-levels`/`shop-catalog`/`shop-window`; `character-select`; `world-map`/`map-window`; `collect-all`, `destroy-all-enemies`, `reach-exit` ↔ типи цілей; `environment-death` ↔ шипи; `chase-player`, `enemy-patrol` ↔ огри; `in-game-editor`/`editor-window`; `online-multiplayer`, `rating-system`, `leaderboard` ↔ арени; `objective-text`; `language-picker` ↔ вибір мови програмування.
- **Нема** → пропозиції карток:
  - `+real-language-code` «Справжня мова (Python/JS) керує сутністю через API-обʼєкт» · game-logic/program · 🥈.
  - `+equipment-unlocks-api` «Предмет відкриває метод у коді» · game-logic/program · 📎.
  - `+goal-checklist` «Кілька цілей рівня зі статусами, обовʼязкові й бонусні» · game-logic/win · 🥉.
  - `+required-restricted-methods` «Рівень вимагає/забороняє методи» · game-logic/constraints · 🥈.
  - `+clean-code-bonus` «Бонус за код без попереджень» · game-logic/score · 📎.
  - `+code-arena-ladder` «Код проти коду, рейтинг» · game-logic/opponent · 🥇.
  - `+frame-simulation-playback` «Симуляція наперед і програвання кадрів» · code/architecture · 🥈.
  - `+stuck-code-warning` «Попередження про нескінченний цикл» · game-logic/program · 📎.

## Пропозиції до словників
- `+feature:equipment-unlocks-api` — спорядження визначає доступні команди.
- `+feature:required-restricted-methods` — обовʼязкові й заборонені методи рівня.
- `+feature:clean-code-bonus` — бонусна ціль за код без problems.
- `+feature:code-arena-ladder` — рейтингові матчі програм гравців.
- `+ui:goal-checklist` — список цілей із галочками (точніше за `objective-text`).
- `+ui:method-docs-palette` — палітра доступних методів з документацією (споріднене з `+ui:command-palette` Cargo-Bot).
- `+ui:simulation-scrubber` — повзунок кадрів запису симуляції.
- `+cond:api_available(method)` — метод відкритий спорядженням і не заборонений рівнем.
- `+trigger:goal_done(goal)` — одна з цілей рівня виконана (для списку цілей).

## Джерела
- ⭐ [CodeCombat](https://codecombat.com/) — сама гра, перший рівень без реєстрації.
- [Wikipedia: CodeCombat](https://en.wikipedia.org/wiki/CodeCombat) — 2013, засновники (Saines, Erickson, Lott, Winter), open source + редактор рівнів у 2014, 11 курсів, Ozaria 2019.
- [JSON рівня Dungeons of Kithgard](https://codecombat.com/db/level/dungeons-of-kithgard) — цілі humans-survive / getToLocations / прихована clean-code, required `moveRight`, restricted `moveXY`, шипові стіни, камені руху, розвʼязок 78 кадрів.
- [JSON рівня Master of Names](https://codecombat.com/db/level/master-of-names) — required `attack` і `findNearestEnemy`, ціль «вбити трьох огрів», слоти спорядження.
- [GitHub codecombat](https://github.com/codecombat/codecombat) — ліцензії MIT / CC-BY, рівні сайту закриті.
- [WPI analysis](https://web.cs.wpi.edu/~rich/courses/imgd4600-c15/analyses/code-combat/index.html) — спорядження для проходження, самоцвіти й XP, прапорці на мапі, мультиплеєр людей проти огрів, попередження при зависанні.
- [CodaKid review](https://codakid.com/codecombat-review-everything-you-need-to-know-in-2020/) — команди руху, курси, підписка.

## Непевне
- (?) Семантика `moveRight()` у першому світі: «до наступного каменя руху» — висновок з наявності movement stones у JSON, не перевірено.
- (?) Які саме предмети дають які методи (окуляри → `findNearestEnemy`, чоботи → `moveXY`, молот → `buildXY`) — з памʼяті; у JSON видно лише слоти.
- (?) Чи шипи вбивають миттєво, чи шкодять; урон і радіус атаки огрів.
- (?) Повзунок симуляції, палітра методів, `hero.say`, `buildXY` — з памʼяті про інтерфейс.
- (?) Чи є перевірка розвʼязку на інших випадкових seed-ах (Run vs Submit) — `random: setup` поставлено умовно.
- (?) Огляд CodaKid називає бій «покроковим» — суперечить покадровій симуляції; найімовірніше, неточність огляду.
- (?) Кількість рівнів («близько 400» в огляді), перелік світів після Kithgard.
