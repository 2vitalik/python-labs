---
title: 868-HACK (+ Imbroglio, Cinco Paus — мікро-роглайки Michael Brough)
slug: 868-hack
family: roguelike
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: score
year: 2013
platforms: [iOS, Windows, macOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/868-HACK", best: true, note: "6×6, стіни з нагородою і числом ворогів, чотири здібності ворогів, релізи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Michael_Brough_(game_designer)", note: "автор: 868-HACK 6×6, Imbroglio 4×4, Cinco Paus 5×5, .WAIT проти цугцвангу"}
  - {kind: official, url: "https://www.smestorp.com/", note: "сторінка автора: усі ігри з лінками"}
  - {kind: steam, url: "http://store.steampowered.com/app/274700", note: "868-HACK на Steam"}
  - {kind: other, url: "https://mightyvision.blogspot.com/2013/08/868-hack-ios.html", note: "блог автора: релізні нотатки, streak-рахунок, .SCORE"}
  - {kind: other, url: "https://mightyvision.blogspot.com/2016/05/imbroglio.html", note: "Imbroglio: 4×4, «деккбілдинг» на старті, RPG-рівні на крихітній сітці"}
  - {kind: other, url: "https://mightyvision.blogspot.com/2017/12/cinco-paus-dev-notes.html", note: "Cinco Paus: 5 жезлів, ідентифікація вжитком, скарби — дизайн-нотатки"}
  - {kind: other, url: "https://www.killscreen.com/michael-brough-another-tricky-labyrinth-survive/", note: "огляд Imbroglio: серця/діаманти, червоні/сині, годування клітин"}
  - {kind: play, url: "https://smestorp.itch.io/cinco-paus", note: "Cinco Paus для Windows/Mac"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=868-hack+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, hp-damage, chase-player, speed-per-type, projectile-shot, round-currency, event-points, sequential-levels, reach-exit, player-death, spawn-schedule, score-records, inventory-items, +siphon-spawn, +program-abilities, +streak-score, +permadeath, +tile-weapon, +dual-health, +tile-level-up, +use-identify-wand, +collect-resets-board, +wait-turn]
proposes: ["+trigger:input", "+trigger:siphon(wall)", "+trigger:killed_on(tile)", "+cond:has", "+cond:same(color)", "+cond:in_row_col(a, b)", "+effect:siphon(cells)", "+effect:run_program(p)", "+effect:feed(tile)", "+effect:reset_board", "+effect:identify", "+role:resource", "+role:tile", "+ui:resource-counters", "+ui:spawn-number", "+ui:program-slots", "+ui:wand-knowledge", "+window:hero-select", "+window:deck-builder", "+feature:streaks", "+feature:permadeath", "+axis:info=partial"]
author: opus
date: 2026-11-02
---

# 868-HACK — 6×6: висмоктай стіну — отримай ресурс і ворогів; Imbroglio і Cinco Paus — та сама школа

## Суть
Michael Brough робить роглайки на крихітних сітках, де кожна дія — компроміс, а випадковість лише в стартовій позиції. У **868-HACK** (2013) ти — програма на полі 6×6: стіни містять ресурси, але кожен «сифон» стіни **спавнить ворогів** на число, написане на ній, — жадібність і є складністю. Ресурси (кредити, енергія) живлять **програми** — здібності-заклинання; 8 секторів поспіль, а рахунок «серії» сумується між забігами до першої смерті. У файлі ще два родичі того ж автора: **Imbroglio** (4×4, зброя лежить на клітинах поля і росте, коли на ній вбиваєш) і **Cinco Paus** (5×5, пʼять жезлів з невідомими ефектами, які пізнаєш використанням). Жанр за ними зветься «broughlike».

## Поле і час
- 868-HACK: 6×6 клітин, частина — стіни-вузли (схожі на друковану плату), решта — підлога; старт у куті, вихід — в іншому куті (?). Усе поле на екрані, туману нема, але один тип ворога невидимий поза твоїм рядком/стовпцем.
- Хід: одна дія гравця (крок, атака, сифон, програма) → усі вороги ходять; вороги зʼявляються з часом і після сифонів.
- Imbroglio: 4×4; на кожній клітині лежить зброя з колоди гравця (16 карт, обраних до забігу); стіни **між** клітинами генеруються щоразу й перемішуються, коли збираєш скарб.
- Cinco Paus: 5×5, 5 зон (рівнів) по 5 ворогів; вихід завжди відкритий, частина скарбів — у сховищі, до якого треба повертатися.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець-програма (868) | player | HP (3?), кредити, енергія, сифони, очки, слоти програм | 4 напрямки; атака по ворогу на лінії; сифон; запуск програм |
| Стіна-вузол | resource | тип нагороди (кредити / енергія / очки / програма), кількість, **число ворогів** | при сифоні віддає вміст і породжує стільки ворогів |
| Підбирачка на підлозі | pickup | кредити / енергія / сифон / очки | `pickup` при вході |
| Вихід (Download port) | static | — | наступний сектор; після 8-го — кінець забігу |
| Ворог-базовий (virus-подібний) | enemy | 2 HP | переслідує гравця |
| Ворог «крізь стіни» (glitch?) | enemy | 2 HP | ходить по стінах |
| Ворог «подвійний крок» (virus?) | enemy | 2 HP | 2 клітини за хід |
| Ворог «товстий» (daemon?) | enemy | 3 HP | повільно вбивається |
| Ворог-невидимка (cryptog?) | enemy | 2 HP | видно лише в твоєму рядку або стовпці |
| Програма `.XXXX` | pickup | ціна в кредитах/енергії | одноразова-на-сектор (?) здібність: `.WAIT` — пропустити хід (антицугцванг), `.SCORE` — очки |
| Герой (Imbroglio) | player | серця ♥ і діаманти ♦ (дві шкали HP), руна-здібність | 4 напрямки; бʼє зброєю клітини, на якій стоїть |
| Клітина-зброя (Imbroglio) | tile | колір (червоний/синій), шкода, рівень, лічильник «годування» | 4 вбивства на ній → рівень↑ + руна герою |
| Монстр червоний / синій (Imbroglio) | enemy | ♥ або ♦ HP | бʼє по відповідній шкалі героя |
| Скарб-самоцвіт (Imbroglio) | pickup | — | +1 очко, +1 кожної шкали, лабіринт перебудовується |
| Жезл ×5 (Cinco Paus) | pickup | 5 зарядів; ефекти невідомі, випадкові на забіг | промінь по прямій: усі вороги на лінії отримують ефекти; себе не зачепити |
| Ворог ×5 видів (Cinco Paus) | enemy | 1–4 HP; 5-й — 1 HP і «неоднозначна» здібність | наближаються до гравця |
| Зілля / том / самоцвіт / скриня (Cinco Paus) | pickup | — | лікування / ідентифікація / заряд (5 самоцвітів → лампа: перезарядити жезл раз) / 5 очок |
| Артефакт (Cinco Paus) | pickup | вибір з ≥2 | постійний бонус до кінця забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
868-HACK:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`; ЯКЩО `in_row_col(player, enemy)` без стін між ними (?) → ТО `custom: «постріл: перший ворог на лінії −1 HP»`.
- КОЛИ `input(siphon)` → ЯКЩО `has(player, siphon)` → ТО `siphon(adjacent_walls)`: кожна сусідня стіна віддає ресурс (`currency(+n)` / `counter(energy, +n)` / `score(n)` / програма), `spawn_at(enemy × wall.spawn_number, spawn_points)`; `counter(siphons, −1)`.
- КОЛИ `input(program p)` → ЯКЩО `has(credits|energy, ≥ cost(p))` → ТО `run_program(p)`, `currency(−cost)`.
- КОЛИ `timer(every N ходів)` → ТО `spawn_at(enemy, spawn_points)` — затягування теж карається.
- КОЛИ `contact(enemy, player)` → ТО `hp(player, −1)`; `hp_zero(player)` → `lose` (кінець серії).
- КОЛИ `contact(player, exit)` → ТО `next_level` (сектор +1); ЯКЩО `level == 8` → ТО `custom: «забіг завершено, очки → серія»`.
- Рахунок: очки забігу; streak — сума забігів поспіль до першої смерті; посилення ворогів накопичуються з довжиною серії.

Imbroglio:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` (нема стіни між клітинами) → ТО `move(hero, dir)`; ЯКЩО там ворог → ТО атака зброєю клітини, де стоїть герой.
- КОЛИ атакує червона зброя → ТО `damage(enemy.hearts)`; синя → `damage(enemy.diamonds)`.
- КОЛИ `contact(red_monster, hero)` → ТО `hp(hero.hearts, −n)`; синій — по діамантах; будь-яка шкала 0 → `lose`.
- КОЛИ `hp_zero(enemy)` → ТО `feed(tile_under_hero)`; КОЛИ `counter(feed, ==, 4)` → ТО `level_up(tile)`, `give(hero, rune)`.
- КОЛИ `contact(hero, gem)` → ТО `score(1)`, `heal(hearts, 1)`, `heal(diamonds, 1)`, `reset_board` (нові стіни, ті самі клітини-зброя).
- КОЛИ `input(move)` → ТО `custom: «вороги ходять; нові зʼявляються випадково»`.

Cinco Paus:
- КОЛИ `input(wand w, dir)` → ЯКЩО `counter(charges[w], >, 0)` → ТО промінь по прямій; кожен ворог на лінії отримує всі ефекти `w` (сон, поліморф, телепорт геть…); `counter(charges[w], −1)`; `identify(partial w)` — що побачив, те записано.
- Ефекти не діють на гравця («no self-zapping»); деякі ефекти ситуативні й розкриваються лише за умови.
- КОЛИ `contact(player, tome)` → ТО `identify(effect)`; `gem` → `counter(gems, +1)`; 5 самоцвітів → лампа: `custom: «один раз перезарядити жезл»`.
- КОЛИ `contact(enemy, player)` → ТО `hp(player, −1)`; 5 HP, лікує лише зілля.
- КОЛИ `contact(player, exit)` → ТО наступна зона (заряди привʼязані до прогресу зон); 5 зон — фінал.
- Рахунок: скрині по 5 очок; інших функцій очки не мають.

## Керування і ввід
- Тач (iOS) або клавіатура/миша (PC): свайп/стрілка — крок або атака в напрямку; кнопки програм у панелі (868); кнопка сифону.
- Imbroglio: тап по сусідній клітині — хід/атака; тап по зброї — опис; руна героя — окрема кнопка.
- Cinco Paus: вибрати жезл з пʼяти → напрямок; описи «відкритих» властивостей біля жезла.
- Жодного undo; кожен хід зважений — гра «шахова», а не рефлексна.

## Вікна, меню, HUD
- 868-HACK `game-screen`: поле 6×6; на кожній стіні — іконка ресурсу, число й червоне число ворогів (`spawn-number`); `resource-counters` (кредити, енергія, сифони, очки); `program-slots` — ряд кнопок програм з ціною; номер сектора, HP.
- 868-HACK `main-menu`: старт серії, рекорди (single run і streak), налаштування; `leaderboard` онлайн (Game Center/Steam).
- Imbroglio: `hero-select` (8 героїв базово, кожен з окремим табло й обмеженнями колоди) → `deck-builder` (розставити 16 зброй на 4×4) → `game-screen` (поле, ♥/♦, рівні клітин, лічильник самоцвітів, руна) → `end-screen` з рахунком.
- Cinco Paus: `game-screen` з пʼятьма жезлами внизу, на кожному — `wand-knowledge` (відомі властивості, лишок зарядів); вибір артефакту — `choose(options)` між зонами (`upgrade-window`).
- `help-window`: туторіал 868-HACK навчає основам, але комбінації правил — на гравцеві.

## Фічі поза полем
- `streaks` (868): рахунок серії сумується між забігами до смерті — «мета-забіг».
- `leaderboard-online` для одиночного забігу й серії; Imbroglio — табло на кожного героя (без серій — кожен забіг сам по собі).
- `unlockables`: програми 868 відкриваються поступово (або всі одразу на вибір); герої Imbroglio — за зібрані самоцвіти (останній — 128 самоцвітів іншими героями).
- Розширення: 868-HACK PLAN.B (2017, нові програми, режим, бонуси); Imbroglio — Ossuary, Phlogiston, Mizzenmast, режим Draft.
- `permadeath` у всіх трьох; нема збереження посеред забігу (?) крім автосейву.

## Варіації й родичі
- Brough: Zaga-33 (2012, 9×9 — попередник), Corrypt, P1 Select, 868-BACK (сиквел).
- Broughlike-школа: Hoplite (див. `tactics/hoplite`), Mosaic, Rat King; спільне — мала сітка, повна інформація, мало випадковості під час бою, «кожен ресурс — палиця з двох кінців».
- Осі варіацій: **звідки здібності** (підбираєш під час гри / уже на полі / маєш з початку, але не знаєш, що вони роблять); **ціна ресурсу** (спавн ворогів / перебудова лабіринту / заряди); **рахунок** (один забіг / серія забігів); **розмір поля** 4×4 / 5×5 / 6×6.

## Цікавинки для курсу
- Сифон: нагорода з явно підписаною ціною (число ворогів на стіні) — найпростіший «ризик ↔ вигода» — 📎.
- Програми як заклинання з ціною в двох валютах + слоти — 🥉 (таблиця ефектів як дані).
- Streak-рахунок через забіги — 🌱 (але цікаво як дизайн: «одна смерть стирає серію»).
- Imbroglio: зброя належить клітині, а не героєві; клітина росте від убивств на ній; кольорові шкали HP — 🥈 (рух стає вибором зброї).
- Cinco Paus: ефекти жезлів генеруються на забіг і пізнаються поступово — 🥇 (генератор комбінацій + модель знань гравця + UI «що вже відомо»).
- Колекція трьох ігор як урок: та сама сітка, три різні «звідки сила» — 📎 для есе/порівняння.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `chase-player` · `speed-per-type` (подвійний крок) · `projectile-shot` (постріл по лінії / промінь жезла) · `round-currency` (кредити, енергія) · `event-points` · `sequential-levels` (8 секторів / 5 зон) · `reach-exit` · `player-death` · `spawn-schedule` · `score-records` · `inventory-items` (програми, жезли).
- **Нема** → пропозиції карток:
  - `+siphon-spawn` «Ресурс зі стіни ціною спавну ворогів» · game-logic/economy · 📎 · слоти {reward, spawn_count}.
  - `+program-abilities` «Здібності-програми з ціною в ресурсах» · entities/state · 🥉 · слоти {cost, slots}.
  - `+streak-score` «Рахунок серії забігів до першої смерті» · game-logic/score · 🌱.
  - `+tile-weapon` «Зброя лежить на клітині поля» · entities/combat · 🥉.
  - `+dual-health` «Дві шкали HP, кожну бʼє свій колір ворога» · entities/state · 📎.
  - `+tile-level-up` «Клітина росте від подій на ній» · entities/state · 📎 · слот {feeds_per_level}.
  - `+use-identify-wand` «Ефекти предмета генеруються і пізнаються вжитком» · entities/state · 🥇.
  - `+collect-resets-board` «Взяв скарб — лабіринт перебудувався» · levels/generation · 🥉.
  - `+wait-turn` «Пропуск ходу» (уже пропонувалось) — тут як платна програма `.WAIT`.
  - Спільна з Rogue: `+permadeath`.

## Пропозиції до словників
- `+trigger:siphon(wall)` — гравець висмоктав стіну; `+effect:siphon(cells)` — забрати вміст сусідніх стін.
- `+effect:run_program(p)` — виконати здібність зі слоту з ціною.
- `+trigger:killed_on(tile)` + `+effect:feed(tile)` — вбивство «годує» клітину під героєм.
- `+effect:reset_board` — перегенерувати стіни, зберігши клітини/сутності.
- `+cond:in_row_col(a, b)` — на одній лінії без перешкод (постріл, видимість невидимки); `+cond:same(color)` — колір атаки = колір шкали.
- `+role:resource` (стіна-вузол), `+role:tile` (клітина-зброя).
- `+ui:resource-counters` · `+ui:spawn-number` (число ворогів на стіні) · `+ui:program-slots` · `+ui:wand-knowledge` (відомі/невідомі властивості предмета).
- `+window:hero-select` · `+window:deck-builder` (розкласти колоду на поле перед забігом).
- `+feature:streaks` · `+feature:permadeath` · `+axis:info=partial` (усе видно, крім невидимок і невідомих ефектів).
- `+trigger:input` · `+cond:has` · `+effect:identify` — як у Rogue.

## Джерела
- ⭐ [Wikipedia: 868-HACK](https://en.wikipedia.org/wiki/868-HACK) — поле, стіни з нагородою і числом ворогів, здібності ворогів, релізи.
- [Wikipedia: Michael Brough](https://en.wikipedia.org/wiki/Michael_Brough_(game_designer)) — розміри полів трьох ігор, `.WAIT` проти цугцвангу, номінації IGF.
- [smestorp.com](https://www.smestorp.com/) — офіційна сторінка автора з лінками на всі ігри.
- [Блог: 868-HACK iOS](https://mightyvision.blogspot.com/2013/08/868-hack-ios.html) — програми, streak-рахунок.
- [Блог: Imbroglio](https://mightyvision.blogspot.com/2016/05/imbroglio.html) — колода на старті, стіни як «тасування», RPG-рівні.
- [Блог: Cinco Paus dev notes](https://mightyvision.blogspot.com/2017/12/cinco-paus-dev-notes.html) — жезли, заряди, ідентифікація, вороги, скарби.
- [Kill Screen про Imbroglio](https://www.killscreen.com/michael-brough-another-tricky-labyrinth-survive/) — ♥/♦, червоні/сині, 4 вбивства на рівень клітини.
- [Steam: 868-HACK](http://store.steampowered.com/app/274700) · [itch.io: Cinco Paus](https://smestorp.itch.io/cinco-paus).
- YouTube: [пошук «868-hack gameplay»](https://www.youtube.com/results?search_query=868-hack+gameplay).

## Непевне
- (?) Відповідність імен ворогів (virus/glitch/daemon/cryptog) їхнім здібностям — з памʼяті; Wikipedia дає лише чотири здібності без імен.
- (?) Сифон бере саме ортогонально сусідні стіни; що стається зі стіною після сифону — з памʼяті.
- (?) HP гравця 868 = 3, кути старту/виходу, точний розклад спавну за часом — з памʼяті.
- (?) Чи можна стріляти крізь стіни і чи атака — «постріл по лінії» чи «удар у сусідню»; Wikipedia каже лише «can be shot with lasers».
- (?) Список програм окрім `.WAIT` і `.SCORE` не перевірено — тому не наведено.
- (?) Cinco Paus: «5 ефектів на жезл» з дев-нотаток ранньої версії; фінальна гра могла змінитись.
