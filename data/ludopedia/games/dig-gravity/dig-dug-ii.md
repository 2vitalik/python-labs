---
title: Dig Dug II
slug: dig-dug-ii
family: dig-gravity
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1985
platforms: [arcade, NES/Famicom, Famicom Disk System, X68000, PSP, DS, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dig_Dug_II", best: true, note: "острів згори, розломи, потоплення, овоч після 3 обвалів, втеча ворогів"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ディグダグII", note: "JA: дві кнопки, «ガケクズシ», eye-change крізь тріщини, FC-риба й Special Flag, 72 стадії FC"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dig_Dug", note: "оригінал: насос, Пука, Фігар — спільне з другою частиною"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dig+dug+ii+arcade+gameplay", note: "пошук; геймплей аркади"}
  - {kind: other, url: "https://strategywiki.org/wiki/Dig_Dug_II", note: "StrategyWiki (не відкрилась для перевірки — 403)"}
stage: v1
coverage: 65
mechanics: [move-4dir, touch-death, environment-death, player-death, destroy-all-enemies, chase-player, event-points, combo-multiplier, sequential-levels, score-records, status-panel, reachability-check, +pump-inflate, +fire-breath, +ghost-phase, +flee-last-enemy, +bonus-item-spawn, +extra-life-threshold, +fault-line-crack, +region-split-sink]
proposes: ["+effect:sink", "+effect:crack", "+cond:on_stake", "+ui:lives", "+ui:level-number", "+card:fault-line-crack", "+card:region-split-sink"]
author: opus
date: 2026-11-02
---

# Dig Dug II — розколи острів по розломах і втопи шматок разом з ворогами

## Суть
Діг Даг (Тайдзо Хорі) ходить островом згори і бʼє відбійним молотком у кілки, що стоять на лініях розломів. Тріщина бігає вздовж розлому; коли тріщини відрізають від острова шматок, **менша частина тоне** разом з усіма, хто на ній стоїть. Насос із першої частини лишився, але головна зброя — геометрія: розрізати поле так, щоб у воду пішло якомога більше ворогів (і не сам гравець). Копання тунелів тут нема — «копання» перетворилось на розрізання поверхні.

## Поле і час
- Вид згори: острів неправильної форми в морі; на ньому кілки (stakes) і пунктирні лінії розломів між ними; великі раунди FC прокручуються (оглядовий скрол перед стартом).
- Поле — сітка, рух і тріщини по осях; тріщина ділить острів на звʼязні компоненти, вода навколо — край поля.
- Real-time; вороги з часом стрибають у море по одному (втеча), раунд закінчується, коли ворогів не лишилось.
- Обвали не переносяться між раундами: кожен раунд — нова форма острова і розкладка кілків.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Діг Даг | player | життя | 4 напрямки; насос уперед; стоячи на кілку — тріщина в обраному напрямку |
| Суша острова | terrain | компонента звʼязності | по ній ходять усі; відрізана менша компонента тоне |
| Кілок (stake) | static | — | точка, з якої можна пустити тріщину |
| Розлом (fault line) | terrain | пунктир між кілками | шлях, яким біжить тріщина |
| Тріщина | static | — | відкрита лінія; звичайні вороги її не переходять (?) |
| Море | hazard | — | усе, що опинилось на шматку, який тоне, гине |
| Насос (гарпун) | projectile | коротка дальність | влучив → ворог зупинений; повторні натискання надувають до вибуху |
| Пука | enemy | — | ходить сушею до гравця; інколи «очі» — летить прямо крізь тріщини |
| Фігар | enemy | вогонь ліворуч/праворуч | як Пука + вогонь, що проходить крізь тріщини; збоку — подвійні очки |
| Овоч | pickup | — | після 3 обвалів зʼявляється у випадковому місці; бонус очок |
| Риба (FC) | pickup | червона 500 / фіолетова 5000 | вистрибує після обвалу одноклітинного шматка; бʼється молотком |
| Special Flag (FC) | pickup | +1 життя | після 5 поспіль овочів, скинутих у море |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(digdug, dir)` сушею; ЯКЩО `cell(target, sea)` → ТО `block`.
- КОЛИ `input(drill, dir)` → ЯКЩО `on_stake(digdug)` → ТО `crack(fault, dir)`: `custom: «тріщина біжить розломом до наступного кілка або берега»` (?).
- КОЛИ `pattern(region_closed)` → ТО `sink(smaller_region)`: усі сутності на ній `disappear`; `score` за кількістю потоплених ворогів (більше разом — значно більше).
- КОЛИ `sink(region)` → ЯКЩО `occupied(region, digdug)` → ТО `lose`, `lives(-1)`.
- КОЛИ `counter(collapses, ==, 3)` → ТО `spawn_at(vegetable, random)`; КОЛИ `contact(digdug, vegetable)` → ТО `pickup`, `score(n)`.
- КОЛИ `input(fire)` → ЯКЩО `free(ahead)` → ТО `spawn(pump)`; КОЛИ `contact(pump, enemy)` → ТО `freeze(enemy)`; повторний `input(fire)` → `custom: «стадія надування +1»`, остання → `disappear_b`, `score`.
- КОЛИ `custom: «ворога надуто»` → ЯКЩО Фігар і `facing(digdug, horizontal)` → ТО `score(×2)`; очки не залежать від місця (на відміну від шарів Dig Dug).
- КОЛИ `rng(p)` → ТО `set_state(enemy, eyes)`: `move(enemy, straight)` крізь тріщину; перейшов → `clear_state(eyes)`.
- КОЛИ `line_of_sight(fygar, digdug)` по горизонталі → ТО `custom: «вогонь на кілька клітин, крізь тріщини»`; `contact(fire, digdug)` → `lose`.
- КОЛИ `contact(enemy, digdug)` → ЯКЩО `not state(enemy, frozen)` → ТО `lose`, `lives(-1)`.
- КОЛИ `timer(round_limit)` → ТО `custom: «вороги по одному біжать до берега і стрибають у море»` (раунд закінчується без очок за них).
- КОЛИ `all_gone(enemy)` → ТО `next_level`.
- FC: КОЛИ `sink(region of 1 cell)` → ТО `spawn_at(fish, sea)`; удар молотком → `score(500|5000)`. КОЛИ `counter(vegetables_sunk, ==, 5)` поспіль → ТО `spawn(special_flag)` → `lives(+1)`.
- Перемога раунду: вороги знищені/потоплені/втекли. Поразка: дотик, вогонь, тонучий шматок → −1 життя; 0 → `game_over`. Рахунок: насос, потоплення пачкою, овочі, риба (FC).

## Керування і ввід
- Важіль 4 напрямки; кнопка 1 — насос (тиснути повторно — надувати); кнопка 2 — молоток: працює лише стоячи на кілку, тріщина йде в напрямку важеля.
- Тактика — вибір кілка й напрямку: спершу заманити ворогів на шматок, потім замкнути контур.

## Вікна, меню, HUD
- `splash-screen` / `attract-demo` (FC має демо посеред гри).
- `game-screen`: острів, море; HUD — `score`, `hi-score`, `lives`, `level-number`.
- `custom-window` «Round N» + оглядовий скрол острова (FC, великі раунди).
- `end-screen` «Game Over» → `leaderboard` (аркада).

## Фічі поза полем
- `levels-sequential`: FC — 72 стадії; нічні фони й нові кольори ґрунту (FC).
- `leaderboard-local` (аркада), бонусне життя за очки й Special Flag (FC).
- Перевидання в колекціях Namco Museum, Arcade Archives (Switch/PS4).

## Варіації й родичі
- Dig Dug (1982) — копання в розрізі, камені; Dig Dug Island (2008, онлайн-мультиплеєр, закрито); Dig Dug: Digging Strike (DS) — гібрид обох механік.
- Родичі за «розрізанням»: Qix/Xonix (замкнути область — але там вона зафарбовується, а тут зникає з умістом).
- **Осі варіацій**: що відбувається з відрізаним — «зафарбовується (Qix) / тоне з умістом (DD2) / падає (обвал)»; яка частина зникає — «менша / та, де нема гравця / та, що не торкається якоря»; хто перетинає розріз — «ніхто / лише в особливому стані (очі)».

## Цікавинки для курсу
- Розрізання поля і пошук компонент звʼязності (flood fill) після кожної тріщини; менша зникає разом з умістом — 🥇 (граф поля змінюється в рантаймі, порівняння площ, хто де стоїть).
- Тріщина від кілка вздовж наперед заданого розлому — 🥉 (рух по графу розломів до наступного вузла).
- Очки за пачку потоплених — комбо від одного геометричного рішення — 📎.
- Насос з кількох натискань (повтор з Dig Dug) — 🥉.
- Ворог-«очі», що перетинає тріщини лише прямо — 📎 (зміна правила проходу за станом).
- Овоч після N обвалів, риба після одноклітинного обвалу — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `touch-death` · `environment-death` ↔ потонути · `player-death` · `destroy-all-enemies` · `chase-player` · `event-points` · `combo-multiplier` ↔ кілька ворогів одним обвалом · `sequential-levels` · `score-records` · `status-panel` · `reachability-check` ↔ компоненти звʼязності острова.
- **Нема** → пропозиції карток:
  - `+fault-line-crack` «Тріщина вздовж розлому від кілка» · entities/interact · 🥉 · слоти {stops_at: next_stake|edge, dirs: 4}.
  - `+region-split-sink` «Відрізана частина поля зникає з умістом» · entities/interact · 🥇 · слоти {which: smaller|without_player, kills: all}.
  - Повтори з Dig Dug: `+pump-inflate`, `+fire-breath`, `+ghost-phase` (тут — лише крізь тріщини, прямо), `+flee-last-enemy` (тут — за таймером, у море), `+bonus-item-spawn` (після 3 обвалів); з корпусу — `+extra-life-threshold`.

## Пропозиції до словників
- `+effect:sink` — частина поля разом з умістом зникає (тоне); відрізняється від `clear`, бо знищує сутності на клітинах.
- `+effect:crack` — провести непрохідну лінію-розріз уздовж заданого шляху.
- `+cond:on_stake` — гравець стоїть на клітині-активаторі (узагальнення: `cell(digdug, stake)` — можна обійтись ⏳ `cell`, тому слабка пропозиція).
- `+ui:lives`, `+ui:level-number` — ⏳, повтор.
- Тригер `pattern(region_closed)` ⏳ — тут ключовий: замкнений контур тріщин.

## Джерела
- ⭐ [Wikipedia: Dig Dug II](https://en.wikipedia.org/wiki/Dig_Dug_II) — острів згори, розломи, менша частина тоне з усім умістом, овоч після трьох обвалів, вороги стрибають у воду, версії й перевидання.
- [Wikipedia JA: ディグダグII](https://ja.wikipedia.org/wiki/ディグダグII) — дві кнопки (насос / тріщина з кілка), «ガケクズシ», eye-change крізь тріщини, вогонь крізь тріщини, FC-риба 500/5000, Special Flag, 72 стадії.
- [Wikipedia: Dig Dug](https://en.wikipedia.org/wiki/Dig_Dug) — спільні вороги і насос.
- YouTube: пошук «dig dug ii arcade gameplay».

## Непевне
- (?) Чи тріщина біжить строго до наступного кілка або берега, чи на фіксовану довжину розлому — джерела кажуть лише «тріщина в обраному напрямку».
- (?) Чи може Діг Даг переходити відкриту тріщину — з памʼяті так; вороги — лише в стані «очей».
- (?) Таблиця очок за потоплення N ворогів і за овочі — не знайдено (StrategyWiki 403).
- (?) Кількість раундів аркади і стартові життя не перевірено; 72 — FC.
- (?) Скільки стадій надування у DD2 — вважаю як у Dig Dug.
