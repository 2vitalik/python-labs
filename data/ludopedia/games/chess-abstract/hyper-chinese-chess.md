---
title: Hyper Chinese Chess (即时象棋：旧棋新弈, сянці в реальному часі)
slug: hyper-chinese-chess
aka: [即时象棋：旧棋新弈, 即时象棋, Real-time Xiangqi, Сянці в реальному часі]
family: chess-abstract
also: [roguelike]
klass: figure
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: setup
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4059530/", best: true, note: "опис: AP макс. 4, +1 кожні 3 с, хід = 1 AP, одночасні ходи, перехоплення, режими, туман, фракція шахів"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=4059530&l=schinese", note: "Steam API, китайський опис: 帅印 / 刻印 / 战法, військові кошти → позаігрові технології"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4059530&count=15&maxlength=3000", note: "патчноути 1.1.0–2.0.0: швидкості фігур, сектор 90°, кулдаун генерала 2 с, мапи, роглайк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hyper+Chinese+Chess+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [piece-move-patterns, piece-capture, speed-per-type, movement-animation, realtime-ai, ai-opponent, difficulty-levels, online-multiplayer, lobby-window, match-setup, game-settings, fog-of-war, pawn-promotion, run-relics, sequential-levels, tutorial-window, achievements-window, attract-demo, game-screen, main-menu, end-screen, cell-click, drag-drop-piece, +action-points, +realtime-ap-regen, +piece-cooldown, +directional-hit-arc, +army-select, +meta-progression, +escort-goal, +random-endgame-start]
proposes: ["+trigger:arrived", "+cond:in_arc", "+effect:move_over_time", "+ui:ap-counter", "+ui:cooldown-ring", "+feature:ap-regen-setting", "+window:run-map", "+card:realtime-ap-regen", "+card:directional-hit-arc", "+card:random-endgame-start", "+card:escort-goal"]
author: opus
date: 2026-11-09
---

# Hyper Chinese Chess — сянці без черги: ходиш, коли є очки дій, фігури їдуть у часі й перехоплюються на льоту

## Суть
[Сянці](xiangqi.md) з тими самими фігурами й патернами, але **без черги ходів**: обидва гравці діють одночасно, кожен хід коштує 1 очко дій (AP), а AP відновлюються з часом (макс. 4, +1 кожні 3 с за замовчуванням). Фігури рухаються не миттєво, тому маршрут суперника можна прочитати й **перехопити посеред руху**; накопичені AP дають «серію» з кількох фігур (колісниця + кінь + гармата). Навколо ядра — кампанія-навчання, челенджі з особливими правилами, роглайк-експедиції з рекрутингом фігур і онлайн із мапами, туманом і фракцією західних шахів. Розробник — 上弦月工作室 AscentGames, реліз 6.11.2025.

## Поле і час
- Дошка сянці (9×10 перетинів, палац, річка — див. [xiangqi.md](xiangqi.md)); онлайн — 5 готових мап і «випадковий ендшпіль» (старт з однієї з кількох ендшпільних позицій), розміри мап (?).
- Час — real-time: у кожного свій запас AP, спільний для всіх його фігур; черги нема.
- Хід фігури триває в часі; швидкість залежить від типу (патчі: кінь +20 %, слон +100 %, радник −20 %).
- Камера top-down / 2.5D (теги Steam).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Генерал (帅/将) | piece | royal; кулдаун 2 с після ходу (v1.2.0) | 1 крок ортогонально в палаці |
| Радник (士) | piece | speed −20 % | діагональ у палаці; без «战争践踏» з v1.1.0 |
| Слон (相/象) | piece | speed +100 % | діагональ через 1, не за річку (як у сянці (?)); без «战争践踏» |
| Кінь (马) | piece | speed +20 %, стрибок/ривок | патерн коня сянці з блокуванням «ноги» |
| Колісниця (车) | piece | slider | ортогонально на будь-яку відстань |
| Гармата (炮) | piece | slider | рух як колісниця, бʼє через рівно один екран |
| Солдат (兵/卒) | piece | — | уперед; після річки ще й убік |
| Західні фігури (фракція шахів) | piece | на окремих мапах онлайн | король, ферзь, тура, слон, кінь без блокування, пішак → ферзь на дальньому ряду |
| Запас AP | resource | макс. 4; +1 / 3 с; хід = 1 | спільний для всіх фігур гравця |
| Фігура в русі | piece | напрямок, швидкість | шкодить лише ворогам у секторі 90° по ходу (v1.1.0) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(3s)` → ЯКЩО `counter(ap, <, 4)` → ТО `counter(ap, +1)` (швидкість відновлення налаштовується в онлайн-кімнаті; у челенджах — повільніша на вищій складності).
- КОЛИ `input(move, piece, to)` → ЯКЩО `counter(ap, >=, 1)` і `custom: «to за патерном сянці (блок ноги коня, екран гармати, палац, річка)»` і `not state(piece, cooldown)` → ТО `counter(ap, -1)`, `custom: «фігура рушає до to зі швидкістю свого типу»` (`+effect:move_over_time`).
- Черги нема: обидва гравці подають ходи будь-коли, поки є AP (`turn_of` не перевіряється).
- КОЛИ `contact(moving_piece, enemy_piece)` → ЯКЩО `custom: «ворог у секторі 90° за напрямком руху»` (`+cond:in_arc`) → ТО `disappear(enemy_piece)` — перехоплення на льоту; бічний «помах» не бʼє (з v1.1.0).
- КОЛИ `custom: «фігура дійшла до цілі»` (`+trigger:arrived`) → ЯКЩО `occupied(to, enemy)` → ТО `disappear(enemy)` (?).
- КОЛИ `input(move, general, to)` → ТО після ходу `set_state(general, cooldown, 2s)`; КОЛИ `timer(2s)` → ТО `clear_state(general, cooldown)`.
- Туман (режим): КОЛИ `tick` → ЯКЩО `mode(fog)` → ТО `reveal(околиця своїх фігур)`, `hide(решта поля)`; ворожі фігури підходять невидимими.
- Фракція шахів: КОЛИ `reach(pawn, last_rank)` → ТО `transform(pawn, queen)`; КОЛИ `input(move, knight)` → ТО блок «ноги» не діє.
- Челендж «孤军护送» (самотній конвой): КОЛИ `reach(escort_soldier, target)` → ТО `win`; КОЛИ `died(escort_soldier)` → ТО `lose` (?).
- Челендж «兵马破阵»: перемогти меншими силами проти переважних; бос-бої — асиметричні армії.
- Роглайк: КОЛИ `level_end` (перемога в бою) → ТО `choose(рекрут фігури | 帅印 печатка | 刻印 гравіювання | 战法 тактика)` (?); КОЛИ `game_over` → ТО `currency(+військові кошти)` → позаігрові технології.
- Перемога: взяття / мат генерала (?) · Поразка: втрата генерала (?) · Рахунку нема (у роглайку — військові кошти).

## Керування і ввід
- Лише мишею або лише дотиком (категорії Steam): клік фігури → клік цілі (або drag); хід подається миттєво, якщо є AP.
- Тактика — «зберегти» AP і виконати серію ходів кількома фігурами за секунду-дві; читати маршрут фігури суперника й ставити свою на перетин шляху.

## Вікна, меню, HUD
- `main-menu`: фоном програються демонстрації розвʼязків ендшпілів (`attract-demo`, v2.0.0); Одиночна гра → перемикач «Кампанія / Челендж» угорі ліворуч; Роглайк; Мультиплеєр; Налаштування; Досягнення.
- `level-select` кампанії (поетапне навчання керування, ходів, бою) і челенджів.
- `match-setup` / `lobby-window` онлайн: підбір суперника, запрошення друга, вибір з 5 мап, швидкість відновлення AP, туман, фракція шахів; `loading-screen` при зʼєднанні.
- `game-screen`: дошка, `ap-counter` / смуга AP обох сторін (?), фігури в русі з анімацією, `cooldown-ring` генерала (?), `fog-overlay` у режимі туману.
- `run-map` роглайку: 3 поверхи, 9 боїв (?), вибір нагород між боями; позаігрове дерево технологій за військові кошти.
- `end-screen`: перемога / поразка; `achievements-window` (13 досягнень, напр. «王不见王», «向我开炮»).
- `settings-window`: гучність, мова (EN, 简体, 繁體, 日本語).

## Фічі поза полем
- `mode-classic` (кампанія), `mode-puzzle` (челенджі з особливими правилами), роглайк з `meta-progression` і рівнями «сходження», `online-multiplayer` з підбором і кімнатами, `ai-opponent-levels` (новий AI v2.0.0 «виграє 98 % у старого»).
- `custom-rules` онлайн: мапа, швидкість AP, туман, фракція.
- `achievements`, `localization` (4 мови), саундтрек DLC.

## Варіації й родичі
- База — [xiangqi.md](xiangqi.md); real-time шахи без черги з кулдаунами — Kung-Fu Chess у [chess-rule-twists.md](chess-rule-twists.md) (там кулдаун фігури, тут — спільний запас AP); туман і приховані фігури сянці — [jieqi.md](jieqi.md), [banqi.md](banqi.md).
- Західні фігури проти сянці — ідея змішаних армій, як у [chess-with-different-armies.md](chess-with-different-armies.md).
- **Осі варіацій**: темп (черга / кулдаун фігури / спільний запас AP) · рух (миттєвий / у часі зі швидкістю типу) · взяття (на клітині / перехоплення в русі за сектором) · інформація (повна / туман) · армія (сянці / шахи).

## Цікавинки для курсу
- Запас AP з регенерацією по таймеру й вартістю ходу — 📎.
- Рух у часі: позиція фігури між перетинами, швидкість за типом, перехоплення зіткненням з сектором 90° — 🥈.
- Перевести покроковий генератор ходів сянці в real-time (легальність перевіряти в момент подачі, конфлікти прибуття) — 🥈.
- Туман: видимість як обʼєднання околиць своїх фігур, `reveal`/`hide` щотіку — 🥉.
- AI в реальному часі, що планує серію ходів під накопичені AP — 🥇.
- Роглайк-оболонка над партією: рекрутинг фігур і модифікатори правил між боями — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns`, `piece-capture` ↔ фігури сянці · `speed-per-type` ↔ кінь/слон/радник · `movement-animation` ↔ рух у часі · `realtime-ai`, `ai-opponent`, `difficulty-levels` · `online-multiplayer`, `lobby-window`, `match-setup`, `game-settings` ↔ мапа, AP, туман · `fog-of-war` · `pawn-promotion` ↔ пішак → ферзь · `run-relics` ↔ печатки/гравіювання/тактики · `sequential-levels` + `tutorial-window` ↔ кампанія · `achievements-window` · `attract-demo` ↔ демо ендшпілів у меню · `game-screen`, `main-menu`, `end-screen` · `cell-click`, `drag-drop-piece`.
- **Нема** → пропозиції карток:
  - `+action-points` (корпус), `+piece-cooldown` (див. chess-rule-twists.md), `+army-select` (корпус), `+meta-progression` (корпус).
  - `+realtime-ap-regen` «Запас очок дій, що відновлюється в реальному часі» · game-logic/opponent · 📎 · слоти {max: 4, regen_s: 3, cost: 1}.
  - `+directional-hit-arc` «Шкода лише в секторі напрямку руху» · entities/combat · 🥉 · слоти {arc_deg: 90}.
  - `+random-endgame-start` «Старт з випадкової ендшпільної позиції» · levels/generation · 🌱.
  - `+escort-goal` «Довести визначену фігуру до цілі» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:arrived` — рух у часі завершився, фігура на цілі.
- `+cond:in_arc` — ціль у секторі N° відносно напрямку руху.
- `+effect:move_over_time` — рух до клітини зі швидкістю, а не миттєво.
- `+ui:ap-counter`, `+ui:cooldown-ring` — голоси (корпус).
- `+feature:ap-regen-setting` — швидкість відновлення AP як параметр кімнати.
- `+window:run-map` — карта забігу роглайку (корпус: `+feature:run-map`).
- `+card:realtime-ap-regen`, `+card:directional-hit-arc`, `+card:random-endgame-start`, `+card:escort-goal` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Hyper Chinese Chess](https://store.steampowered.com/app/4059530/) — розробник, реліз 6.11.2025, AP (макс. 4, +1/3 с, хід = 1), одночасні ходи й перехоплення, кампанія, челенджі, роглайк, туман, фракція шахів, онлайн з випадковими ендшпілями, теги, мови.
- [Steam API, китайський опис](https://store.steampowered.com/api/appdetails?appids=4059530&l=schinese) — та сама AP-формула дослівно, 帅印 / 刻印 / 战法, військові кошти → позаігрові технології, 13 досягнень, лише миша / лише дотик.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=4059530&count=15&maxlength=3000) — 5 патчноутів: 1.1.0 (швидкості, сектор 90°, без «战争践踏» для слона й радника, 5 мап, налаштування AP), 1.2.0 (кулдаун генерала 2 с, фракція шахів, мови), 2.0.0 (роглайк 3 поверхи / 9 боїв, кампанія, челенджі, «випадковий ендшпіль», новий AI).
- YouTube — пошук; трейлер «Gameplay Demo PV» є на Steam-сторінці.

## Непевне
- (?) Умова перемоги (взяття генерала чи мат, чи діє «генерали не бачать один одного» — є досягнення «王不见王») — у джерелах не названа; один пошуковий агрегатор писав «мат генералу», не підтверджено.
- (?) Що таке «战争践踏» (war trample) — здатність фігур, у патчноуті лише згадана.
- (?) Як саме розвʼязується зіткнення: хто гине, якщо обидві фігури рухаються одна на одну; чи бʼє фігура, що прибула в зайняту клітину.
- (?) Пошуковий агрегатор писав «+1 AP щосекунди» — Steam-опис каже «за замовчуванням +1 кожні 3 с», беру Steam.
- (?) Черга в описі «спільний запас очок дій» — запас у кожного гравця свій, спільний лише для його фігур.
- (?) Ефекти печаток, гравіювань і тактик, дерево технологій, розміри мап, радіус туману — не описані.
- Шапка: `info: full` — базовий режим; туман — окремий режим. `also: [roguelike]` — за роглайк-експедиціями.
