---
title: Evil Eye
slug: evil-eye
aka: ["Evil Eye (iamshyguy)", "Лихе око"]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [web]
links:
  - {kind: itch, url: "https://iamshyguy.itch.io/evil-eye", best: true, note: "грати в браузері (PuzzleScript, автор Milanvis / iamshyguy), натхнення й плейтестери"}
  - {kind: other, url: "https://html-classic.itch.zone/html/18348460/index.html?v=1784155137", note: "HTML гри: повний PuzzleScript-сирець — око, зомбі, кажан, слід крові, сцени; усі 17 рівнів"}
  - {kind: other, url: "https://www.bontegames.com/2026/08/evil-eye-browser.html", note: "анонс Bart Bonte (14 серп. 2026): «horror inspired sokoban puzzler about hiding»; коментарі з підказками"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Evil+Eye+puzzlescript+iamshyguy", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, reach-exit, touch-death, environment-death, visited-trail, spawn-schedule, reachability-check, undo-unlimited, restart-level, level-select, level-unlock, sequential-levels, save-progress, level-from-txt, movement-animation, event-effects, sound-effects, +sector-flood-fill, +hide-from-gaze, +release-threat-on-demand, +darkness-spread, +charge-in-line, +time-clone-replay, +failed-move-no-turn, +playable-cutscene, +zone-skins]
proposes: ["+trigger:aligned", "+effect:spread", "+effect:replay", "+effect:cancel_turn", "+window:playable-cutscene", "+ui:threat-countdown", "+card:hide-from-gaze", "+card:release-threat-on-demand", "+card:darkness-spread", "+card:charge-in-line", "+card:failed-move-no-turn"]
author: opus
date: 2026-11-19
---

# Evil Eye — забарикадуйся меблями, натисни X і переживи погляд ока, що заливає всі досяжні клітини

## Суть
Покрокова хоррор-головоломка на PuzzleScript «про хованки»: у кожній кімнаті вихід замкнено дверима, і відчинити їх можна лише одним способом — натиснути X і **випустити Око**. Око «бачить» кожну клітину, до якої з дверей можна дійти порожньою підлогою; якщо гравець серед них — темрява поглинає рівень. Тож спершу треба **зібрати з меблів «фортецю»**, що відрізає тебе від дверей, пережити погляд, а потім розібрати барикаду й дійти до виходу. Далі додаються зомбі, що біжать по рядку чи стовпцю, і кажан, що повторює твої перші 16 ходів. 17 рівнів у трьох актах між грабельними сценами.

## Поле і час
- Квадратна сітка, малі кімнати (≈5×5 … 12×7) у рамці стін; нижній рядок — HUD (у рівнях з кажанами — двоцифровий відлік).
- Три зони з однаковими правилами й різними спрайтами (підміняються правилами за фоном): дім (шухляди, двері), цвинтар (камені, ворота), мавзолей (смолоскипи, плита).
- Шари: фон → слід крові (по шару на напрям і фазу) → «горбки» → обʼєкти (гравець, стіни, меблі, двері, зомбі, кажан — усі на одному шарі) → погляд Ока і темрява.
- Хід = успішний крок гравця; невдалий крок (у стіну, у меблі, що не рушать) скасовується повністю — не рахується ні для відліку, ні для ворогів. Після ходу — каскад `again`: зомбі біжать, кажан летить, Око озирається, темрява розтікається.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | рух 4 напрямки; штовхає меблі на 1 (без ланцюга); кровить — лишає слід |
| Око | enemy | зʼявляється у дверях за X | погляд заливає всі клітини, досяжні від дверей без стін і меблів; бачить гравця → темрява; ні → озирається й зникає |
| Двері виходу (двері / ворота / плита) | gate | — | тверді, доки не випущено Око; після нього клітина виходу вільна |
| Вихід | static | під дверима | перемога, коли на ньому гравець |
| Меблі (шухляда / камінь / смолоскип) | object | вигляд за зоною | штовхаються на 1; блокують погляд і рух; на «горбок» не заходять |
| Горбок | terrain | — | прохідний для гравця й ворогів, непрохідний для меблів |
| Стіна | static | вигляд за зоною | блокує рух і погляд |
| Погляд | zone | червоне напівпрозоре | позначка клітин, які бачить Око; зникає разом з ним |
| Темрява | hazard | — | після «побачило» розтікається на всіх сусідів щокадру, крізь стіни; гравець у ній зникає |
| Зомбі | enemy | — | після ходу гравця в тому ж рядку чи стовпці біжить до нього до упору; штовхає меблі; поруч із гравцем — зʼїдає; завмирає, поки Око назовні |
| Кажан | enemy | 8 фаз × 2 кадри = 16 кроків | зʼявляється на старті, коли відлік дійшов до 0; пролітає записані 16 ходів гравця, штовхаючи меблі; заблокований — розсіюється димом; влетів у гравця — гравець гине |
| Слід крові | mark | напрям + фаза 1–8 | запис кожного ходу гравця; у рівнях з кажаном — 16 ходів з номерами фаз |
| Дим | object | 4 кадри | ефект зникнення кажана |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `mark(from_cell, blood_dir_phase)` (слід: напрям і фаза).
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` → ТО `block`, `custom: «скасувати весь хід: відлік і вороги не рушають»`.
- КОЛИ `contact(player, furniture)` → ЯКЩО `free(cell_behind)` і `not cell(cell_behind, bump)` → ТО `push`, `move(player, dir)`; інакше хід скасовано.
- КОЛИ `input(action)` → ЯКЩО `counter(countdown, >, 0)` → ТО `block` (X не працює, поки йде відлік).
- КОЛИ `input(action)` → ЯКЩО `occupied(exit, door)` → ТО `transform(door, eye)`.
- КОЛИ `spawned(eye)` → ТО `custom: «погляд заливає всі клітини, досяжні від Ока через клітини без стін і меблів»` (`mark(cells, gaze)`).
- КОЛИ `spawned(eye)` → ЯКЩО `path_exists(eye, player)` → ТО `set_state(eye, sees)`, `sound(alarm)`, `spawn_at(darkness, eye)`.
- КОЛИ `tick` → ЯКЩО `occupied(cell, darkness)` → ТО `custom: «темрява займає всіх 4 сусідів, крізь стіни»`.
- КОЛИ `contact(darkness, player)` → ТО `disappear(player)` — рівень не пройти, лише undo/рестарт.
- КОЛИ `spawned(eye)` → ЯКЩО `not path_exists(eye, player)` → ТО `sound(relief)`, `custom: «Око дивиться ліворуч, праворуч»`, `disappear(eye)`, `clear(gaze)` — клітина виходу відкрита.
- КОЛИ `enter(player, exit)` → ТО `win`, `next_level`.
- КОЛИ `turn_end` → ЯКЩО `custom: «зомбі в одному рядку чи стовпці з гравцем (перешкоди між ними не важать)»` і `not state(eye, out)` → ТО `move(zombie, toward_player)`, повторно щокадру, доки рух можливий.
- КОЛИ `contact(zombie, furniture)` → ЯКЩО `free(cell_behind)` і `not cell(cell_behind, bump)` → ТО `push`; інакше `block`.
- КОЛИ `adjacent(zombie, player)` → ТО `custom: «зомбі займає клітину гравця»`, `disappear(player)`.
- КОЛИ `turn_end` → ЯКЩО `counter(countdown, >, 0)` → ТО `counter(countdown, -1)`; фаза сліду = `custom: «номер пари ходів 1–8»`.
- КОЛИ `counter(countdown, ==, 0)` → ТО `spawn_at(bat, start_cell)`.
- КОЛИ `tick` → ЯКЩО `state(bat, phase_k)` і `occupied(bat_cell, blood_k)` → ТО `move(bat, blood_dir)` — кажан пролітає слід каскадом, гравець не встигає діяти.
- КОЛИ `contact(bat, furniture)` → ЯКЩО `free(cell_behind)` і `not cell(cell_behind, bump)` → ТО `push`.
- КОЛИ `blocked(bat)` → ТО `transform(bat, smoke)`, `disappear(bat)`.
- КОЛИ `contact(bat, player)` → ТО `transform(bat, smoke)`, `disappear(player)`.
- КОЛИ `counter(bat_steps, ==, 16)` → ТО `transform(bat, smoke)`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Сцени: вступ — силует іде лише ліворуч до дверей дому; цвинтар — з могил піднімаються руки; печера — кожен крок запалює випадкові очі кажанів; фінал — гравець сідає на трон і стає мертвим королем.
- Перемога: гравець на клітині виходу. · Поразка: формально нема — гравець зникає (темрява, зомбі, кажан), рівень лишається непройденим до undo/R. · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — крок або поштовх; X — випустити Око; Z — undo; R — рестарт (титул PuzzleScript підказує клавіші).
- Мишки й сенсорних жестів у описі нема (?).

## Вікна, меню, HUD
- `main-menu` — титул PuzzleScript Next: «Continue» / «Level Select» / «New Game».
- `level-select` — секції «Scene 1: Intro», 1–6, «Scene 2: Zombies», 7–10, «Scene 3: Bats», 11–17, «Scene 4: End»; непройдені далі першої відкритої — замкнені.
- `game-screen` — кімната + рядок HUD; у рівнях з кажаном — `+ui:threat-countdown` (відлік ходів до кажана).
- `custom-window` — повідомлення між актами: «Press X to unleash it», «You are not alone», «Other threats must be dealt with first».
- `+window:playable-cutscene` — сцени-рівні (будинок під місяцем, цвинтар, печера кажанів, тронна зала) з власними умовами завершення.
- Переходи: титул → вибір секції → рівень → (вихід) наступний рівень або сцена.

## Фічі поза полем
- `undo` (∞), `restart-level`; `level-select` з блокуванням (`level-unlock`), `continue` — прогрес у браузері.
- `levels-sequential` у трьох актах, кожен відкривається повідомленням і сценою.
- Звук на кожну подію (у описі — «PuzzleScript random sound effect button» як натхнення).
- Підказок, лічильника ходів, редактора нема.

## Варіації й родичі
- Натхнення (за сторінкою itch): Secure (Toombler), Hiding Spot (Corey Martin), Ao Oni (noprops), пісня «Evil Eye» Franz Ferdinand.
- Осі варіацій «загроза, від якої ховаєшся»:
  - **як бачить**: по прямій до перешкоди (`line-of-sight-attack`, [Headlong Hunt](headlong-hunt.md)) / заливка досяжних клітин (Око тут) / ряд чи стовпець навіть крізь стіни (зомбі тут);
  - **коли бʼє**: щоходу / лише коли гравець сам натиснув X (Око) / після відліку (кажан);
  - **як рухається**: стоїть / біжить до упору / повторює твій записаний шлях (кажан, `+time-clone-replay`).
- Родичі: [Sokoban](sokoban.md) (штовхання), [Headlong Hunt](headlong-hunt.md) (зір по лініях, укриття), [Prince of Darkness Jr.](prince-of-darkness-jr.md) (світло вбиває, ящик дає тінь), [Hitman GO](hitman-go.md) (вороги з правилами зору).

## Цікавинки для курсу
- Погляд Ока = заливка (BFS) від дверей крізь вільні клітини + перевірка «гравець у компоненті» — 📎; сама ідея «побудуй стіну з ящиків навколо себе» — гарне завдання на звʼязність.
- Темрява, що поширюється на сусідів щокадру крізь усе (клітинний автомат) — 🌱.
- Зомбі: «у рядку/стовпці → біжи до упору», повтор у кадрах `again` — 📎.
- Кажан: запис ходів у слід з номерами фаз і повтор шляху з поштовхами; блок → дим — 🥈 (детермінований «привид минулого»).
- Невдалий хід не рахується (скасування всього ходу) — 🌱, але важливо для відліків.
- Грабельні сцени як рівні з власними умовами перемоги (дійти до дверей, засвітити всі очі, сісти на трон) — 📎.
- Розвʼязувач: BFS по станах (гравець, меблі, зомбі, відлік і слід) з перевіркою погляду при X — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ меблі; `impassable-cells` ↔ стіни, горбки лише для меблів; `reach-exit`; `touch-death` ↔ зомбі, кажан; `environment-death` ↔ темрява; `visited-trail` ↔ слід крові; `spawn-schedule` ↔ кажан після 16 ходів; `reachability-check` ↔ погляд Ока; `undo-unlimited` + `restart-level`; `level-select` + `level-unlock` + `sequential-levels` + `save-progress`; `level-from-txt`; `movement-animation`, `event-effects` (дим, темрява), `sound-effects`.
- **Нема** → пропозиції карток:
  - `+sector-flood-fill` (є в корпусі) — області, замкнені стінами; тут — у реальному часі гри.
  - `+hide-from-gaze` «Сховатися від погляду, що заливає досяжні клітини» · entities/legality · 🥉.
  - `+release-threat-on-demand` «Гравець сам випускає загрозу (X), коли готовий» · game-logic · 🌱.
  - `+darkness-spread` «Хвиля, що поглинає все поле крізь стіни» · entities/interact · 🌱.
  - `+charge-in-line` «Ворог біжить до гравця, щойно той у рядку/стовпці» · entities/move · 📎.
  - `+time-clone-replay` (є в корпусі, Loophole) — тут повтор 16 ходів по сліду з поштовхами.
  - `+failed-move-no-turn` «Хід у стіну не рахується» · game-logic · 🌱.
  - `+playable-cutscene` «Сцена як міні-рівень із власною умовою» · levels/progression · 📎.
  - `+zone-skins` «Зона змінює спрайти без зміни правил» · interface/graphics · 🌱.

## Пропозиції до словників
- `+trigger:aligned` — дві сутності в одному рядку чи стовпці без перевірки перешкод (зомбі); `line_of_sight` вимагає вільної лінії.
- `+effect:spread` — стан переходить на сусідні клітини щокадру (темрява; повтор з Boulder Dash).
- `+effect:replay` — сутність повторює записані ходи іншої (кажан).
- `+effect:cancel_turn` — скасувати весь хід, ніби вводу не було (PuzzleScript `cancel`).
- `+window:playable-cutscene` — сцена, у якій гравець рухається, з окремою умовою завершення.
- `+ui:threat-countdown` — HUD-відлік ходів до появи загрози.
- `+card:hide-from-gaze`, `+card:release-threat-on-demand`, `+card:darkness-spread`, `+card:charge-in-line`, `+card:failed-move-no-turn` — див. «Мапу на каталог».

## Джерела
- ⭐ [itch: Evil Eye by iamshyguy](https://iamshyguy.itch.io/evil-eye) — гра в браузері, натхнення, плейтестери, теги PuzzleScript / Sokoban, рейтинг 4.9.
- [HTML гри з сирцем](https://html-classic.itch.zone/html/18348460/index.html?v=1784155137) — правила: X перетворює двері на Око, заливка погляду крізь клітини без стін і меблів, темрява, зомбі (`[zombie | ... | player]`), відлік і слід крові з фазами, кажан, що йде по сліду й штовхає меблі, «невдалий хід скасовує хід»; секції й повідомлення; 17 рівнів + 4 сцени.
- [bontegames: Evil Eye](https://www.bontegames.com/2026/08/evil-eye-browser.html) — «Press X to unleash it, if you dare… sokoban puzzler about hiding»; коментарі: фортеця від Ока, зомбі, час прильоту кажана, вогонь (смолоскипи) біля кажана.

## Непевне
- (?) Відлік: у сирці стартує з 17, але правила першого кадру одразу зменшують його — на екрані, ймовірно, 16; кажан повторює саме 16 записаних ходів.
- (?) Як саме поводиться Око на кількох виходах і чи можна випустити його двічі — у рівнях по одних дверях.
- (?) Сенсорне керування й миша — PuzzleScript їх підтримує, але сторінка гри про це мовчить.
- (?) Рядок черги: «око бачить по прямій» — за сирцем погляд Ока заливає досяжні клітини; по прямій (рядок/стовпець) «бачать» зомбі.
