---
title: Chessarama
slug: chessarama
aka: []
family: chess-abstract
also: [thinky, push-slide]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2023
platforms: [PC, Xbox One, Xbox Series X/S, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1831830/Chessarama/", best: true, note: "8 ігор: Dragon Slayers (захисти пішака від дракона), Lady Ronin (шахи + Sokoban), Soccer Chess…; 100+ рівнів, 100+ челенджів, daily/weekly, класичні шахи"}
  - {kind: other, url: "https://umgamer.com/fr-fr/articles/review-chessarama-is-great-for-logic-games-fans-and-brings-innovation-to-chess?changedomain", note: "огляд: кампанія — 4 пазл-ігри по 24–34 фази з відкриттям за XP і корона-челенджами; Battles — 5 складностей; правила кожної гри"}
  - {kind: other, url: "https://steamcommunity.com/app/1831830/reviews/?browsefilter=toprated", note: "відгуки: Farm Life як тур коня, ланцюг пасів, Pawn Mania з казковими фігурами, без undo, вікно ходів фігури"}
  - {kind: other, url: "https://cogconnected.com/review/chessarama-review/", note: "огляд: паркани на фермі, ліміт ходів, дві звʼязані ділянки, XP відкриває міні-ігри, онлайн-шахи"}
  - {kind: other, url: "https://xbox.com/en-US/games/store/1/9N390R15QCG4", note: "Xbox: 8 ігор, дата, ціна"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chessarama+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, hover-highlight, cell-click, push-object, impassable-cells, cell-transform, visited-trail, move-limit, pawn-promotion, checkmate, destroy-all-enemies, ai-opponent, difficulty-levels, online-multiplayer, move-timer, daily-puzzle, leaderboard, level-unlock, sequential-levels, restart-level, help-window, profile-stats, theme-select, +knight-tour-cover, +revisit-resets-cell, +twin-sync-move, +ball-pass, +chess-push, +capture-only-unprotected, +sweep-undefended, +protect-target, +fairy-pieces, +random-setup, +chess-soccer, +optional-challenges, +weekly-challenge, +skin-unlock-progression]
proposes: ["+cond:defended", "+effect:pass", "+effect:sweep_undefended", "+card:knight-tour-cover", "+card:revisit-resets-cell", "+card:twin-sync-move", "+card:chess-push", "+card:capture-only-unprotected", "+card:sweep-undefended", "+card:fairy-pieces", "+card:chess-soccer"]
author: opus
date: 2026-11-19
---

# Chessarama — вісім ігор, де фігури ходять як у шахах, але цілі нові: зорати поле конем, віддати пас, проштовхнутись ферзем, провести пішака повз дракона

## Суть
Збірка Minimol Games (2023): звичайні патерни ходу шахових фігур і вісім нових цілей у тематичних діорамах. **Кампанія** — чотири пазл-гри (Farm Life, Street Soccer, Lady Ronin, Dragon Slayers), по 24–34 фази, відкриваються за досвід (XP). **Battles** — чотири партії проти ШІ на випадкових розстановках (Knight Supreme, Soccer Chess, Last Stand, Pawn Mania) з п'ятьма складностями. Окремо — класичні шахи з ШІ й онлайн. Ядро для курсу — один генератор ходів фігур, на який навішано різні умови перемоги й різні «фізики» поля (оранка, пас, штовхання, атака по незахищених).

## Поле і час
- Квадратна шахова сітка різного розміру й форми в кожній грі (ділянка ферми, футбольне поле, доріжка з драконом) (?); клітини з властивостями: зорана / дика, паркан, конус, ворота, кінець доріжки.
- Пазли — покроково без суперника (Farm Life, Street Soccer, Lady Ronin) або з реакцією світу на хід (дракон у Dragon Slayers). Battles — почергово з ШІ.
- Класичні шахи — з годинником (типово 5 хв + 5 с, вибір контролю часу).
- Анімація після кожного ходу, без пропуску (за відгуком) — темп задає гра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінь-фермер (Farm Life) | piece | 1–2 на полі | L-хід; клітина, куди став, зорюється |
| Клітина ферми | terrain | дика / зорана | зорана вдруге — знищена, знову дика |
| Паркан | static | — | Farm Life: клітина, куди коню не можна; Knight Supreme: «огороджена клітина», хід у неї — умова челенджу (?) |
| Фігури-футболісти (Street Soccer) | piece | тип фігури | пас і удар — на будь-яку клітину, куди фігура могла б піти |
| Мʼяч | object | у кого | переходить пасом за патерном фігури |
| Конус | static | — | перешкода на пізніх рівнях Street Soccer |
| Ворота | zone | — | мʼяч у воротах = гол |
| Ронін (Lady Ronin) | player | ферзь; невразливий | ходить як ферзь, бʼє незахищених, штовхає фігури як Sokoban |
| Ворожі фігури (Lady Ronin) | enemy | тип фігури | захищають одна одну; згодом і ферзі |
| Сьогун | boss | король | ціль після всіх інших фігур |
| Пішак-герой (Dragon Slayers) | piece | — | іде доріжкою до серця дракона; у кінці стає ферзем |
| Фігури-охоронці | piece | тип фігури | захищають тих, хто в полі їхнього удару |
| Дракон | enemy | — | після кожного ходу пішака атакує дошку |
| Армії Knight Supreme | piece | король + кілька коней | партія до мату |
| Ферзі Last Stand | piece | кілька | проти ворожої армії; треба взяти всіх |
| Казкові фігури (Pawn Mania) | piece | Camel, Alfil, Dabbabah… | на них перетворюється пішак |
| Ворожа армія ШІ | enemy | складність 1–5 | грає партію проти гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- Спільне: КОЛИ `input(move, piece, to)` → ЯКЩО `legal(move)` (патерн фігури) і `free(to)` → ТО `move(piece, to)`; інакше `block`.
- **Farm Life:** КОЛИ `enter(knight, field_cell)` → ЯКЩО `state(cell, wild)` → ТО `set_cell(cell, plowed)`.
- КОЛИ `enter(knight, field_cell)` → ЯКЩО `state(cell, plowed)` → ТО `set_cell(cell, wild)` («знищив зоране»).
- КОЛИ `input(move, knight, to)` → ЯКЩО `cell(to, fence)` → ТО `block`.
- КОЛИ `input(move, knight_1, to)` → ЯКЩО `count(knight, ==, 2)` → ТО `custom: «другий кінь ходить одночасно з першим на сусідній ділянці»` (?).
- КОЛИ `counter(moves, >, limit)` → ТО `restart` (рівні з лімітом ходів) (?).
- КОЛИ `counter(plowed, ==, all_cells)` → ТО `win`.
- **Street Soccer:** КОЛИ `input(pass, piece_with_ball, to)` → ЯКЩО `legal(move)` за патерном фігури → ТО `custom: «мʼяч переходить у клітину / до фігури»` (`+effect:pass`).
- КОЛИ `input(pass, …)` → ЯКЩО `occupied(path, cone)` → ТО `block`.
- КОЛИ `reach(ball, goal)` → ТО `win`.
- **Lady Ronin:** КОЛИ `input(capture, ronin, enemy)` → ЯКЩО `legal(move)` і `not custom: «ворога захищає інша фігура»` (`+cond:defended`) → ТО `disappear_b`; інакше `block`.
- КОЛИ `input(move, ronin, to)` → ЯКЩО `occupied(to, piece)` → ТО `push(piece)` (`custom: «фігури штовхають одна одну, як ящики Sokoban»`) (?).
- КОЛИ `contact(enemy, ronin)` → ТО `custom: «роніна не можна взяти»`.
- КОЛИ `all_gone(enemy)` → ТО `custom: «сьогун стає доступним»`.
- КОЛИ `contact(ronin, shogun)` → ЯКЩО `count(enemy, ==, 0)` → ТО `win`.
- **Dragon Slayers:** КОЛИ `after(move(pawn))` → ТО `custom: «дракон атакує дошку»`: для кожної фігури ЯКЩО `not custom: «у полі удару іншої своєї фігури»` → ТО `disappear` (`+effect:sweep_undefended`).
- КОЛИ `died(pawn)` → ТО `lose`, `restart`.
- КОЛИ `reach(pawn, path_end)` → ТО `transform(pawn, queen)`, `win`.
- **Knight Supreme:** КОЛИ `no_moves(enemy)` → ЯКЩО `in_check(enemy_king)` → ТО `win` (мат); фігури — король і коні з обох боків; на полі огороджені клітини (?).
- **Soccer Chess:** КОЛИ `turn_start(side)` → ТО `choose(move piece | pass ball)` за патерном ходу фігури; узяття фігур дозволене (?).
- КОЛИ `reach(ball, enemy_goal)` → ТО `score(+1)`.
- **Last Stand:** КОЛИ `all_gone(enemy)` → ТО `win`.
- КОЛИ `reach(enemy_pawn, last_rank)` → ТО `transform(pawn, piece)`, `custom: «повітряні удари прибирають перетворених пішаків»` (?).
- **Pawn Mania:** КОЛИ `reach(pawn, last_rank)` → ТО `choose(any piece, incl. Camel, Alfil, Dabbabah)`, `transform(pawn, chosen)`.
- Battles: КОЛИ `level_start` → ТО `custom: «випадкова розстановка»`.
- КОЛИ `turn_end(player)` → ТО `custom: «хід ШІ обраної складності»`.
- Челенджі: КОЛИ `level_end` → ЯКЩО `custom: «виконано умову корони: гол турою, ≤ 12 ходів, перемога без ходу королем, 6 голів конем…»` → ТО `counter(xp, +bonus)`.
- КОЛИ `level_end` (пазл розвʼязано) → ЯКЩО `first_time` → ТО `counter(xp, +n)`; повтор — без XP. КОЛИ `counter(xp, >=, threshold)` → ТО `unlock(game|board|figure_set)`.
- Класичні шахи: звичайні правила; КОЛИ `timer(clock, ==, 0)` → ТО `lose`.
- Перемога: ціль гри (зорати все, гол, сьогун, пішак у кінці доріжки, мат, знищити армію). · Поразка: пішака вбив дракон; програна партія; у пазлах — глухий кут → рестарт. · Рахунок: XP за пазли, перемоги й челенджі; рейтинг і таблиці лідерів.

## Керування і ввід
- Миша або геймпад: вибрати фігуру → клітина ходу; пас — так само, клітина-адресат (?).
- Наведення на фігуру — віконце з назвою й патерном ходу (особливо для казкових).
- Undo нема ні в пазлах, ні в партіях: помилка → рестарт рівня; кнопки «назад» у меню теж нема (за відгуком).

## Вікна, меню, HUD
- `main-menu`: Campaign · Battles · Matches (класичні шахи) · Challenges (daily / weekly / Live) · профіль · колекція · налаштування (розділи — з оглядів і патчів, точні назви пунктів (?)).
- `puzzle-select` кампанії: 4 гри, фази з позначками пройдено / корона-челендж (?).
- `match-setup` Battles: гра + складність (Very Easy … Very Hard); Matches: контроль часу, «той самий набір фігур, що в суперника».
- `game-screen`: діорама з полем; HUD — `objective-text` (умова корони), `move-counter` на рівнях з лімітом (?), `tooltip` патерну фігури, `player-clock` у матчах.
- `skin-select`: 24 набори фігур і дошки (Farmer, Soccer, Samurai, Dragon), відкриті за XP і челенджі.
- `leaderboard` + `profile-window` (час гри загалом і по режимах, найдовший пазл, XP-ранг).
- `help-window` — внутрішній мануал правил кожної гри.
- `settings-window`: продуктивність, доступність (кольори, комфорт камери), прискорення гри, мова (21).
- Переходи: main-menu → гра → фаза → (ціль) наступна фаза / (глухий кут) рестарт; Battles → складність → партія → результат.

## Фічі поза полем
- `levels-sequential` + `level-unlock` за XP (гра відкривається порогом досвіду); 100+ пазлів, 100+ челенджів.
- `daily-puzzle` + weekly (Live Challenges), `leaderboard-online` з бейджами.
- `ai-opponent-levels` (5), `online-multiplayer` для класичних шахів, `turn-timer`.
- `unlockables`: набори фігур і дошки; `achievements`, `stats` у профілі.
- `colorblind-palette` (Color Alternatives), `gamepad-support`, `localization`.
- Нема `undo` і `hint` (за відгуками).

## Варіації й родичі
- У корпусі: [chess-rule-twists](chess-rule-twists.md) (правило-надбудова над шахами), [really-bad-chess](really-bad-chess.md) (випадкові армії, тижневі виклики), [chess-with-different-armies](chess-with-different-armies.md) і [fairy-chess-conditions](fairy-chess-conditions.md) (казкові фігури), [chessformer](chessformer.md) (шаховий пазл зі статичною ціллю), [chess-survivors](chess-survivors.md), [shotgun-king](shotgun-king.md); Sokoban-штовхання — [kwirk](../push-slide/kwirk.md).
- Farm Life — родич задачі туру коня; Street Soccer і Soccer Chess — шахово-футбольні гібриди; Dragon Slayers — «захисти ціль» поверх правила «незахищене гине».
- **Осі варіацій:** що дає хід — «узяття (шахи) / оранка клітини / пас мʼяча / поштовх»; хто відповідає — «нікого / середовище (дракон) / ШІ-армія»; що таке перемога — «мат / усі клітини / гол / дійти доріжкою / знищити всіх».

## Цікавинки для курсу
- Один генератор ходів фігур, багато режимів: ціль і реакція середовища як окремі модулі — 🥈 (архітектура «правило-плагін»).
- Farm Life: тур коня з «повторне відвідування скасовує» + розвʼязувач пошуком з поверненням — 🥉 (з двома синхронними конями — 🥇).
- Dragon Slayers: після кожного ходу пішака — обчислити множину захищених клітин і прибрати решту — 📎.
- Lady Ronin: правило «бити лише незахищених» + штовхання фігур — 🥉.
- Street Soccer: пошук ланцюга пасів за патернами фігур до воріт (BFS по «хто має мʼяч») — 🥉.
- Pawn Mania: перетворення з вибором серед казкових фігур (Camel, Alfil, Dabbabah) — 📎.
- Челенджі-корони як додаткові умови рівня («гол турою», «≤ 12 ходів») — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `hover-highlight` ↔ віконце патерну · `cell-click` · `push-object` ↔ Lady Ronin · `impassable-cells` ↔ паркани, конуси · `cell-transform` + `visited-trail` ↔ оранка · `move-limit` · `pawn-promotion` ↔ Pawn Mania, Dragon Slayers · `checkmate` ↔ Knight Supreme · `destroy-all-enemies` ↔ Last Stand, Lady Ronin · `ai-opponent` + `difficulty-levels` ↔ 5 складностей · `online-multiplayer` + `move-timer` ↔ матчі · `daily-puzzle` · `leaderboard` · `level-unlock` + `sequential-levels` ↔ XP і фази · `restart-level` · `help-window` ↔ мануал · `profile-stats` · `theme-select` ↔ набори фігур і дошки.
- **Нема** → пропозиції карток:
  - `+knight-tour-cover` «Покрий усі клітини ходами коня» · game-logic/win · 📎 · слот {piece: knight}.
  - `+revisit-resets-cell` «Повторний візит скасовує позначку клітини» · entities/interact · 🌱.
  - `+twin-sync-move` «Один хід рухає дві фігури синхронно» · entities/move · 🥉 (?).
  - `+ball-pass` (повтор) — пас мʼяча за патерном фігури-власника.
  - `+chess-push` «Шахові фігури штовхають одна одну» · entities/legality · 🥉.
  - `+capture-only-unprotected` «Бити можна лише незахищену фігуру» · entities/legality · 📎.
  - `+sweep-undefended` «Після події гинуть усі незахищені» · entities/combat · 📎 · слот {trigger: pawn_move}.
  - `+protect-target` (повтор) — пішак-герой.
  - `+fairy-pieces` «Казкові фігури (Camel, Alfil, Dabbabah)» · entities/legality · 📎.
  - `+random-setup` (повтор) — випадкові розстановки Battles.
  - `+chess-soccer` «Хід = рух фігури або пас; гол = очко» · game-logic/win · 🥉.
  - `+optional-challenges`, `+weekly-challenge`, `+skin-unlock-progression` — повтори.

## Пропозиції до словників
- `+cond:defended(a)` — фігуру тримає під захистом інша фігура своєї сторони (Lady Ronin, Dragon Slayers); протилежність ✅ `in_check`.
- `+effect:pass(ball, to)` — мʼяч переходить за патерном фігури, сама фігура лишається.
- `+effect:sweep_undefended` — прибрати всі незахищені фігури (атака дракона).
- `+card:knight-tour-cover`, `+card:revisit-resets-cell`, `+card:twin-sync-move`, `+card:chess-push`, `+card:capture-only-unprotected`, `+card:sweep-undefended`, `+card:fairy-pieces`, `+card:chess-soccer` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Chessarama](https://store.steampowered.com/app/1831830/Chessarama/) — 8 ігор, правила Dragon Slayers («дракон атакує дошку щоразу, як рушить пішак; гине кожна незахищена фігура»), Lady Ronin («шахи + Sokoban»), Soccer Chess; 100+ рівнів і 100+ челенджів, daily/weekly, 24 набори фігур, класичні шахи, функції доступності.
- [Огляд umgamer (ex-Cardsrealm)](https://umgamer.com/fr-fr/articles/review-chessarama-is-great-for-logic-games-fans-and-brings-innovation-to-chess?changedomain) — кампанія 4 × 24–34 фази, XP-відкриття, корона-челенджі; оранка й знищення зораного, другий кінь; пас і удар за патерном; ронін невразливий, бʼє лише незахищених; Battles з 5 складностями.
- [Steam: відгуки](https://steamcommunity.com/app/1831830/reviews/?browsefilter=toprated) — тур коня, ланцюг пасів, Pawn Mania з Camel і Alfil, Soccer Chess «рух або пас», нема undo, віконце патерну фігури, 100 пазлів + 4 випадкові партії.
- [COGconnected](https://cogconnected.com/review/chessarama-review/) — паркани, ліміт ходів, «дві одночасні звʼязані ділянки», повтор пазлу без XP, онлайн-шахи.
- [Xbox Store](https://xbox.com/en-US/games/store/1/9N390R15QCG4) — список 8 ігор, реліз 5.12.2023.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1831830&count=40&maxlength=4000) — патчі 2024: Dabbabah у Pawn Mania, «Aerial Attacks» у Last Stand, паркани в Knight Supreme, контроль часу матчів, дошки за XP; реліз Android (вересень 2025).

## Непевне
- (?) Як саме ходить другий кінь у Farm Life — той самий вектор на сусідній ділянці чи власний хід; формулювання джерел — «одночасно».
- (?) Механіка штовхання в Lady Ronin: хто кого штовхає й коли (ронін фігуру на шляху чи будь-яка фігура при ході) — лише «штовхають одна одну, як у Sokoban».
- (?) Порядок дій у Street Soccer (спершу розставити фігури, потім ланцюг пасів?) і чи удар по воротах — окремий хід.
- (?) Soccer Chess: чи можна брати фігури й за що перемога (кількість голів?); Last Stand: що таке «повітряні удари» і хто їх кличе.
- (?) Ліміт ходів як поразка чи лише як челендж; наявність `move-counter` у HUD; форма й розмір полів кожної гри.
- (?) Набори Pawn Mania (усі казкові фігури) і вибір перетворення гравцем — з відгуків; правила класичних шахів у Matches — стандартні.
