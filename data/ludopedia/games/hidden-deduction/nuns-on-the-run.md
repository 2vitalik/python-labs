---
title: Nuns on the Run
slug: nuns-on-the-run
aka: []
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: race
year: 2010
platforms: [board (Mayfair Games)]
links:
  - {kind: other, url: "https://rulespal.com/nuns-on-the-run/rulebook", best: true, note: "повні правила: таємний журнал руху, шум за кубиком, дуга зору 180° до 6 точок, маршрути варти, 15 ходів"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Frédéric_Moyersoen", note: "автор Frédéric Moyersoen; «2010: Nuns on the Run (Mayfair Games)»"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=nuns+on+the+run", note: "пошук BGG; видання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nuns+on+the+Run+board+game+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 60
mechanics: [turn-enforcement, hot-seat, pass-device, enemy-patrol, chase-player, key-and-door, reach-exit, time-out, fog-of-war, objective-text, game-screen, end-screen, +hidden-movement, +team-vs-one, +last-seen-marker, +belief-set-tracking, +vision-cone, +noise-roll-hearing, +movement-speed-noise-tradeoff, +patrol-route-cards, +secret-objective, +one-shot-blessing, +capture-quota-win]
proposes: ["+trigger:noise", "+effect:secret_move", "+effect:roll_dice", "+cond:in_arc", "+ui:movement-sheet", "+ui:turn-track", "+card:vision-cone", "+card:noise-roll-hearing", "+card:movement-speed-noise-tradeoff", "+card:patrol-route-cards", "+card:secret-objective", "+card:one-shot-blessing"]
author: opus
date: 2026-11-09
---

# Nuns on the Run — послушниці таємно крадуться абатством по точках, варта бачить дугою 180° і чує шум за кубиком

## Суть
Настільна гра з прихованим рухом (Frédéric Moyersoen, Mayfair Games, 2010). Кожна послушниця таємно записує свій рух у журнал: треба взяти ключі, дістати бажаний предмет із замкненого місця й повернутися до своєї келії. Один гравець веде двох наглядачок (абатису й пріоресу), що ходять маршрутами з карт, бачать дугою попереду й чують шум. Чим швидше рухаєшся, тим голосніше: темп проти скритності. Клас — `hybrid`: у послушниці один аватар, у варти дві фігури.

## Поле і час
- Мапа абатства — точки, зʼєднані стежками (`field: graph`); номери точок у правилах сягають 134. Келії послушниць — точки 1–6, келія абатиси — 26; зони: сад, клуатр, каплиця, зовнішня стежка.
- Двері: замкнені позначені замком (послушниці — лише з ключами, варта — завжди); більшість дверей блокує зір.
- Хід = 3 фази: рух послушниць → рух варти → зсув маркера ходу. Гра триває 15 ходів; у першому ході послушниці рухаються двічі.
- Видимість: послушниці на полі лише тоді, коли їх бачать; решта — у журналах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Послушниця | player | швидкість, ключі, предмет, стан | таємно ходить 0–5 точок; на полі лише видимою |
| Варта (абатиса, пріореса) | enemy | 3–4 або 5–6 точок, зір 6 точок | іде маршрутом з карти; побачивши чи почувши — переслідує |
| Карта маршруту | supply | колір шляху | веде варту від поточної точки до чорного шестикутника |
| Ключі | pickup | місце з карти бажання | відчиняють замкнені двері; лишаються й після спіймання |
| Бажаний предмет (Secret Wish) | pickup | таємна карта: ключі + місце | треба взяти й донести до келії |
| Жетон шуму | mark | 1 хід | біля варти на найкоротшому шляху до послушниці |
| Жетон «Vanished» | mark | 1 хід | між останньою видимою точкою і наступною в напрямку руху |
| Благословення | supply | разове | одноразова перевага; напр. False Noise — хибний жетон шуму |
| Замкнені двері | gate | замок | прохід послушниці лише з ключами |
| Дерева, колони, статуї | static | — | зору не блокують |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(novices)` → ТО `choose(«стоїть 0 / крадеться 1–2 / іде 3–4 / біжить до 5 точок»)`, `custom: «таємно записати в журнал точку, кількість точок і картку руху»`.
- КОЛИ `line_of_sight(guard, novice)` → ЯКЩО `in_range(guard, novice, 6)` and `custom: «у дузі 180° попереду, без дверей і стін між ними»` → ТО `place(novice_token, dot)` — послушниця видима.
- КОЛИ `custom: «видима послушниця виходить із зору»` → ТО `place(vanished_token, «між останньою видимою і наступною точкою за напрямком»)`.
- КОЛИ `turn_end(novices)` → ЯКЩО `custom: «поза зором варти»` → ТО `custom: «фішка повертається в келію»`, `set_state(novice, on_the_run)`.
- КОЛИ `phase_start(noise)` → ЯКЩО `custom: «варта минулого ходу йшла, а не бігла»` → ТО `custom: «d6 + модифікатор руху (−3 / −2 / −1 / 0) = радіус шуму»`; ЯКЩО `in_range(novice, guard, радіус)` шляхами → ТО `place(noise_token, «біля варти на найкоротшому шляху до послушниці»)`.
- КОЛИ `turn_start(guards)` → ТО кожна варта, що йде, `custom: «d6 = базовий слух»`; ЯКЩО відстань шляхом ≤ базовий слух + модифікатор послушниці → ТО `place(noise_token, guard)`.
- КОЛИ `turn_start(guards)` → ЯКЩО `custom: «нема видимої послушниці, Vanished чи шуму»` → ТО `move(guard, «маршрутом карти: іде 3–4 або біжить 5–6 точок, не менше»)`.
- КОЛИ `reach(guard, «кінець маршруту — чорний шестикутник»)` → ТО `custom: «скинути карту маршруту, взяти нову від цієї точки»`.
- КОЛИ `line_of_sight(guard, novice)` or `custom: «бачить Vanished / має жетон шуму»` → ТО `custom: «варта сходить із маршруту, рух 3–6 точок у будь-якому напрямку»`; інша варта лишається на маршруті.
- КОЛИ `enter(guard, novice)` → ТО `score(+1)` варті, `set_state(novice, caught)`, `take(novice, wish_item)`; ключі лишаються.
- КОЛИ `turn_start(novices)` → ЯКЩО `state(novice, caught)` → ТО `custom: «іти (не бігти) до своєї келії найкоротшим шляхом»`; без шуму й без Vanished.
- КОЛИ `enter(novice, keys_dot)` → ЯКЩО `custom: «рух закінчився тут»` → ТО `pickup(novice, keys)`.
- КОЛИ `custom: «рух крізь замкнені двері»` → ЯКЩО `has(novice, keys)` → ТО прохід; інакше `block`.
- КОЛИ `enter(novice, wish_dot)` → ЯКЩО `custom: «рух закінчився тут»` → ТО `pickup(novice, wish_item)`.
- КОЛИ `enter(novice, own_cell)` → ЯКЩО `has(novice, keys)` and `has(novice, wish_item)` → ТО `win`, гра закінчується одразу.
- КОЛИ `counter(captures, >=, players)` → ТО `win` варти.
- КОЛИ `turn_end(guards)` → ЯКЩО `counter(turn, =, 15)` → ТО `win` варти.
- КОЛИ `turn_end(guards)` → ТО `disappear(noise_token)`, `disappear(vanished_token)` — жоден жетон не живе довше ходу.
- КОЛИ `input(play_blessing)` → ТО `custom: «разова перевага»`, `disappear(blessing)`; кубикове — після кидка.
- Перемога: послушниця — ключі + предмет + келія; кілька в один хід — у кого менше спіймань · варта — спіймань ≥ кількості гравців або 15 ходів минуло.

## Керування і ввід
- Послушниця: картка руху лицем донизу + запис у журнал (точка, кількість, `st/sn/w/r`, `K` — ключі, `SW` — предмет).
- Варта: картка руху (іде / біжить) для кожної фігури, рух фігур по маршруту, кидок слуху.
- Цифрова версія: таємний ввід кожного гравця за `pass-device`, клік по точках.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): мапа абатства, видимі послушниці, варта, жетони шуму і Vanished, `turn-track` (15 ходів) і лічильник спіймань.
- `movement-sheet` — журнал послушниці, видимий лише їй.
- `pass-device` — завіса між таємними ходами.
- `end-screen`: переможець; розкриття журналів.
- Довідкові таблиці винятків зору (сад, клуатр, каплиця) — `help-window`.

## Фічі поза полем
- Гравців до 8: при 8 двоє ведуть по одній варті й виграють командою.
- Варіанти: біг — рівно 5 точок; гандикап досвідченої варти — рух не більше 5.

## Варіації й родичі
- [scotland-yard](scotland-yard.md), [specter-ops](specter-ops.md), [fury-of-dracula](fury-of-dracula.md), [escape-from-the-aliens-in-outer-space](escape-from-the-aliens-in-outer-space.md) — прихований рух; тут навпаки: ховаються **багато**, шукає один.
- [stop-thief](stop-thief.md) — шум як підказка про прихованого.
- **Осі варіацій**: хто ховається «один / усі, крім одного»; канал інформації «зір / шум / сліди»; рух варти «вільний / маршрут-картою»; темп «один / вибір швидкості з ціною шуму».

## Цікавинки для курсу
- Дуга зору 180° на графі з радіусом 6 і блокувальними дверима — 🥉.
- Шум: d6 + модифікатор швидкості проти відстані шляхом (BFS) — 📎.
- Таємний журнал руху і перевірка легальності після розкриття — 📎.
- Маршрут варти з карт і повернення найкоротшим шляхом після погоні — 🥉.
- AI-варта, що веде множину можливих позицій послушниць — 🥇.

## Мапа на каталог
- Є: `turn-enforcement` · `hot-seat` · `pass-device` · `enemy-patrol` · `chase-player` · `key-and-door` · `reach-exit` (келія) · `time-out` (15 ходів) · `fog-of-war` · `objective-text` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+hidden-movement`, `+team-vs-one`, `+last-seen-marker`, `+belief-set-tracking` — уже запропоновано (Scotland Yard, Specter Ops).
  - `+vision-cone` «Дуга зору перед сутністю з радіусом» · entities/combat · 🥉.
  - `+noise-roll-hearing` «Шум: кидок + модифікатор проти відстані» · entities/state · 📎.
  - `+movement-speed-noise-tradeoff` «Швидше = голосніше» · entities/move · 🌱.
  - `+patrol-route-cards` «Маршрут ворога з колоди карт» · entities/move · 📎.
  - `+secret-objective` «Таємна ціль гравця з карти» · game-logic/win · 🌱.
  - `+one-shot-blessing` «Разова перевага в руці» · entities/state · 🌱.
  - `+capture-quota-win` — уже запропоновано (Geister).

## Пропозиції до словників
- `+trigger:noise` — сутність почула шум.
- `+effect:secret_move` — рух без показу на полі (вже пропонувався).
- `+effect:roll_dice` — кидок кубика з модифікатором.
- `+cond:in_arc(a, b, deg, n)` — B у дузі зору A.
- `+ui:movement-sheet` — таємний журнал; `+ui:turn-track` — трек ходів.
- Вжито наявні: `line_of_sight`, `in_range`, `phase_start`, `place`, `supply`.

## Джерела
- ⭐ [RulesPal: Nuns on the Run Rulebook](https://rulespal.com/nuns-on-the-run/rulebook) — компоненти (66 карт), підготовка, журнал руху, модифікатори шуму, зір 180° і 6 точок, винятки зору, маршрути й погоня, спіймання, благословення, перемога, варіанти.
- [de.wikipedia: Frédéric Moyersoen](https://de.wikipedia.org/wiki/Frédéric_Moyersoen) — автор, 2010, Mayfair Games.

## Непевне
- (?) Мінімальна кількість гравців і час партії — правила не кажуть.
- (?) Список 8 благословень (крім False Noise) — не знайшов.
- (?) Чи можуть послушниці проходити крізь точки з іншими фігурами; що буває, коли послушниця сама заходить на точку варти.
- (?) Точна кількість точок на мапі (номери до 134).
