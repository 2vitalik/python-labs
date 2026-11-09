---
title: Pâquerette Down the Bunburrows
slug: paquerette-down-the-bunburrows
aka: [Paquerette Down the Bunburrows, Bunburrows]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2023
platforms: [PC (Windows; Steam, Epic)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1628610/", best: true, note: "кролики тікають, коли підходиш, тунелями й уникаючи тупиків; пастки, кайло, морква; 5 нір; 100+ кроликів"}
  - {kind: other, url: "https://gamepretty.com/?p=99448", note: "гайд-правила: дистанція < 3 по прямій, пріоритет вперед > ліво > право, тунелі, стоси й кроленята, кайло/лопата/ласощі, undo і reset"}
  - {kind: other, url: "https://gameluster.com/paquerette-down-the-bunburrows-review-cutesy-cottontail-capers-in-crazy-coney-chambers/", note: "огляд: кролик ходить лише коли ходиш ти, ловля в загоні, пастка-клітка, домашні ловлі, налаштування"}
  - {kind: other, url: "https://store.epicgames.com/p/paquerette-down-the-bunburrows-2fd777?lang=en-US", note: "сторінка Epic Games Store"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Paquerette+Down+the+Bunburrows+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, controls-remap, impassable-cells, dig-terrain, item-pickup, inventory-items, undo-redo, restart-level, collect-quota, stairs-levels, +flee-player, +dead-end-avoid, +corner-capture, +trap-squares, +bait-lure, +stack-breed, +dig-down-layer, +sleeping-enemy, +undo-keeps-progress, +home-capture-bonus]
proposes: ["+effect:flee", "+effect:lure", "+cond:dead_end", "+feature:undo-keeps-progress", "+feature:input-repeat-delay", "+feature:entity-speed-settings", "+card:dead-end-avoid", "+card:corner-capture", "+card:stack-breed", "+card:dig-down-layer", "+card:undo-keeps-progress"]
author: opus
date: 2026-11-09
---

# Pâquerette Down the Bunburrows — лови кроликів, які тікають за детермінованим правилом і обирають нори без тупиків

## Суть
Pâquerette спускається в кролячі нори й ловить кроликів. Кролик не ворог і не ящик: він **тікає**, щойно героїня опиниться з ним на одній прямій ближче ніж за 3 клітини, обираючи напрям за фіксованим пріоритетом і уникаючи видимих тупиків. Зловити можна лише того, кому нема куди бігти, — загнаного в непомічений тупик чи пастку. Гра — «пазл про алгоритм пошуку шляху»: гравець вивчає правило втечі й використовує його проти кролика; кайло, лопата, пастки й морква змінюють поле і маршрути.

## Поле і час
- Кожен рівень — кімната на квадратній сітці; кімнати складено **вертикальними норами** (Northern, Center, Southern, Eastern, Western), рівень під рівнем (C-1 … C-13 і глибше) — тому `field: layers`.
- Між рівнями — нори-дірки: падіння в нору переносить на рівень нижче; лопатою можна викопати діру й обрати, де опинитись унизу; підйом назад — тим самим шляхом.
- Шари клітини: підлога / копана земля / незрушна земля + стіни (руйнівні й ні) + тунелі (лише для кроликів) + обʼєкти (пастки, ласощі) + істоти.
- Хід = крок героїні; після нього рухаються кролики (зазвичай на 1, у коридорі й тунелі — далі). Героїня не діє, доки кролики не зупинились. Таймера нема.
- Видно всю кімнату; «поле зору» має лише кролик (прямі лінії від нього).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Pâquerette | player | інструменти (кайло, лопата, пастки, ласощі) | крок 4 напрямки; ступила на загнаного кролика — зловила |
| Кролик | neutral | домашня кімната | тікає, якщо героїня на прямій, < 3 клітин, без перешкод між ними; пріоритет вперед > ліво > право; уникає тупиків і пасток, які бачить |
| Стос кроликів | neutral | розмір N | 2+ кролики в одній клітині; повільніший, не входить у тунелі, «труситься» при зміні напрямку; дає кроленят |
| Кроленя | — (лічильник) | — | +1 за кожного кролика, що приєднався до стосу; ловити стос не треба |
| Стіна | static | руйнівна / незрушна | непрохідна; руйнівну ламає кайло |
| Тунель | terrain | може мати тупики | лише для кроликів; кролик біжить, доки не вийде; двоє кроликів, що зустрілись у тунелі, розривають його |
| Нора-дірка | terrain | — | падіння на рівень нижче (героїня чи кролик) |
| Незрушна земля | static | — | лопата не копає |
| Пастка-клітка | object | — | ловить кролика або змінює його маршрут (кролик її уникає); можна підняти назад |
| Ласощі (морква) | pickup | — | приманює кролика туди, куди він сам не піде |
| Кайло | pickup | — | ламає стіни й тунелі (зокрема між рівнями нори) |
| Лопата | pickup | — | копає діру під героїнею |
| Центральне світло C-13 | static | — | стати в нього → у паузі відкривається «Return to Surface» |
| Ophéline | neutral | — | на поверхні: розмова й апгрейди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(paquerette, dir)`; далі `phase_start(bunnies)`.
- КОЛИ `phase_start(bunnies)` → ЯКЩО `line_of_sight(bunny, paquerette)` і `in_range(bunny, paquerette, 2)` → ТО `move(bunny, away)` (`custom: «тікати»`).
- КОЛИ `phase_start(bunnies)` (вибір напрямку) → ЯКЩО `not free(away)` або `custom: «попереду видно тупик чи пастку»` → ТО `move(bunny, left)`; інакше `move(bunny, right)`; тупик — лише коли інших варіантів нема.
- КОЛИ `custom: «кролик у коридорі, де можна лише вперед»` → ТО `custom: «біжить до наступного повороту чи розвилки»`.
- КОЛИ `enter(bunny, tunnel)` → ТО `custom: «біжить тунелем за тим самим пріоритетом, доки не вийде»`; бачить повороти й тупики лише по прямих від себе.
- КОЛИ `contact(paquerette, bunny)` → ЯКЩО `custom: «кролику нема куди втекти»` → ТО `pickup`, `counter(captured, +1)`.
- КОЛИ `enter(bunny, trap)` → ТО `set_state(bunny, caught)`, `counter(captured, +1)`; КОЛИ `input(take_trap)` → ТО `pickup` (клітку можна переставити — `place`).
- КОЛИ `custom: «два кролики в одній клітині»` → ТО `merge(bunny, bunny → stack)`, `counter(babies, +1)`; кожен наступний кролик у стосі — ще `counter(babies, +1)`.
- КОЛИ `custom: «два кролики зустрілись у тунелі»` → ТО `set_cell(tunnel, floor)` (тунель розривається).
- КОЛИ `repetition` (кролик ганяє між тунелями по колу) → ТО `set_state(bunny, asleep)`; сплячого не підняти.
- КОЛИ `input(pickaxe, dir)` → ЯКЩО `has(paquerette, pickaxe)` і `not cell(target, unbreakable)` → ТО `set_cell(target, floor)`.
- КОЛИ `input(dig)` → ЯКЩО `has(paquerette, shovel)` і `not cell(here, undiggable)` → ТО `set_cell(here, hole)`, `custom: «спуск на рівень нижче в ту саму позицію»`.
- КОЛИ `enter(a, hole)` → ТО `custom: «a падає на рівень нижче»`; КОЛИ `custom: «прибуття в нову кімнату»` → ТО `custom: «перешкода в клітині прибуття зникає»`.
- КОЛИ `custom: «кролик бачить ласощі»` → ТО `custom: «іде до ласощів»` (`+effect:lure`).
- КОЛИ `pickup` (кролика) → ЯКЩО `custom: «це домашня кімната кролика, і стос не трусився»` → ТО `counter(home_captures, +1)`.
- КОЛИ `input(undo)` → ТО `undo(1)` разом із переходами між кімнатами; повтор — до останнього входу в нору; **зловлені кролики після undo лишаються зловленими**.
- КОЛИ `input(reset)` → ТО `restart` від моменту входу в рівень.
- КОЛИ `enter(paquerette, central_light)` → ТО `unlock(return_to_surface)`.
- Перемога: нема одного фіналу рівня — мета гри зібрати 100+ кроликів, кроленят і «домашні» ловлі; є прихована глибина (Forgotten Burrows, зона E-13, секретна кімната). · Поразка: нема. · Рахунок: лічильники кроликів, кроленят, домашніх ловель.

## Керування і ввід
- Стрілки / WASD або геймпад — крок; окремі дії для інструментів (кайло в напрямку, лопата під собою, поставити/підняти пастку, покласти ласощі) (?); undo, reset, пауза.
- Перепризначення клавіатури й геймпада з основною й альтернативною клавішею; затримка повтору вводу; окрема швидкість анімації руху героїні й кроликів.

## Вікна, меню, HUD
- `main-menu` (?): Продовжити · Налаштування · Вихід.
- `game-screen`: кімната; HUD — лічильник зловлених (?), інструменти в запасі (`inventory-bar`) (?), назва рівня (C-13 тощо).
- `pause-menu`: Resume · Reset · Return to Surface (після C-13) · налаштування · вихід.
- `dialogue-window`: розмова з Ophéline на поверхні; апгрейди.
- `stats-window`: «компʼютер» — апгрейд, що веде облік зловлених і кроленят.
- `settings-window`: клавіатура/геймпад, затримка повтору, швидкості руху, сітка, ліміт FPS, повноекранний/віконний, звук, мова (EN, FR, JA, ZH).
- Переходи: поверхня → вхід у нору → кімнати вниз через дірки → (C-13) Return to Surface → поверхня.

## Фічі поза полем
- `autosave` на старті кожного рівня; нелінійний порядок — можна покинути важку кімнату й повернутися (вхід через різні нори).
- `undo` з глибиною до входу в нору + `restart-level`; історія undo стирається при виході (`+feature:undo-keeps-progress` — прогрес ловлі не відкочується).
- `grid-toggle`, `remap-controls`, `speed-control` для героїні й кроликів окремо (`+feature:entity-speed-settings`), `localization`.
- `collectibles`-мета: кроленята, домашні ловлі, секретні кімнати.

## Варіації й родичі
- Осі варіацій:
  - **як реагує ціль на гравця**: стоїть (ящик Sokoban) / тікає від сусіда до упору (Slayaway Camp) / тікає за лінією зору < 3 з пріоритетом напрямків (Pâquerette) / тікає «найкоротшим шляхом від» (DROD `+flee-player`);
  - **як ловиш**: дотик (Pac-Man) / загнати в глухий кут і ступити / пастка;
  - **чи бачить ціль тупики**: ні / по прямих від себе;
  - **взаємодія цілей**: нема / стос із приплодом.
- Родичі: [slayaway-camp](slayaway-camp.md) (жертва тікає), [hitman-go](hitman-go.md) (детерміновані NPC), Hoplite і DROD (передбачувана поведінка як пазл), [sokoban](sokoban.md) (загнати в кут — навпаки, deadlock тут корисний).

## Цікавинки для курсу
- Правило втечі: пряма лінія, < 3 клітин, без перешкод → крок від героїні з пріоритетом вперед > ліво > право — 📎.
- Уникання тупиків «по прямих від себе» (ray-cast у 4 боки + перевірка, чи коридор глухий) — 🥉.
- Ловля = «ціль не має легального ходу» + крок на неї — 🌱, але з гарним зворотним зв'язком до `no-moves-left`.
- Стос кроликів: злиття в клітині, лічильник приплоду, інші правила руху стосу — 📎.
- Рівні нори шарами: діра лопатою, падіння, підйом, перешкоди в клітині прибуття зникають — 🥉.
- Undo, що не відкочує метапрогрес (зловлені лишаються) — 📎: розділення стану рівня і стану гри.
- Розвʼязувач «як зловити кролика» BFS по (героїня, кролики, пастки, інструменти) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `controls-remap`; `impassable-cells` ↔ стіни/незрушна земля; `dig-terrain` ↔ кайло ламає стіни; `item-pickup` + `inventory-items` ↔ інструменти; `undo-redo` + `restart-level` ↔ undo/reset; `collect-quota` ↔ 100+ кроликів; `stairs-levels` ↔ рівні нори вглиб.
- **Нема** → пропозиції карток:
  - `+flee-player` (DROD, Slayaway Camp) · слот {range: 2, priority: forward>left>right}.
  - `+dead-end-avoid` «Втікач уникає видимих тупиків» · entities/move · 🥉.
  - `+corner-capture` «Ловля загнаної цілі кроком на неї» · game-logic/win · 🌱.
  - `+trap-squares` (вже пропонована) — пастка-клітка, яку можна переставити.
  - `+bait-lure` «Приманка тягне сутність до себе» · entities/move · 📎 (і рамен у Chew Man Fu).
  - `+stack-breed` «Дві сутності в клітині → стос + приплід» · entities/spawn · 📎.
  - `+dig-down-layer` «Копання діри на рівень нижче» · levels/progression · 📎.
  - `+sleeping-enemy` (вже пропонована) — кролик засинає від зациклення.
  - `+undo-keeps-progress` «Undo не відкочує метапрогрес» · game-logic/history · 📎.
  - `+home-capture-bonus` «Бонус за ловлю в домашній кімнаті» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:flee` — сутність тікає від джерела (тут — крок від героїні; Slayaway — ковзання від вбивці).
- `+effect:lure` — ласощі ведуть кролика до себе.
- `+cond:dead_end` — клітина/коридор попереду глухий (вже ×1 у Nurimisaki — інший зміст, тут для руху).
- `+feature:undo-keeps-progress`, `+feature:input-repeat-delay`, `+feature:entity-speed-settings` — окрема швидкість анімації гравця й NPC.
- `+card:dead-end-avoid`, `+card:corner-capture`, `+card:stack-breed`, `+card:dig-down-layer`, `+card:undo-keeps-progress` — див. вище.

## Джерела
- ⭐ [Steam: Paquerette Down the Bunburrows](https://store.steampowered.com/app/1628610/) — кролики тікають тунелями, уникаючи тупиків, «smart yet predictable»; пастки, кайло, морква; 5 нір; Ophéline на поверхні; 100+ кроликів і кроленята.
- [GamePretty: Beginner's Guide](https://gamepretty.com/?p=99448) — правило «in a straight line, less than 3 squares away», пріоритет Forward > Left > Right, коридори, тунелі, сон від зациклення, стоси, кайло/лопата/ласощі, undo/reset, нори і C-13.
- [Gameluster: review](https://gameluster.com/paquerette-down-the-bunburrows-review-cutesy-cottontail-capers-in-crazy-coney-chambers/) — рух кролика лише слідом за ходом героїні, ловля в загоні, пастки-клітки, домашні ловлі, автосейв, налаштування й мови.
- [Epic Games Store](https://store.epicgames.com/p/paquerette-down-the-bunburrows-2fd777?lang=en-US) — друга вітрина.
- YouTube: пошук «Paquerette Down the Bunburrows gameplay».

## Непевне
- (?) Межа дистанції: «less than 3 squares» — 1–2 клітини; записано `in_range(…, 2)`.
- (?) Що кролик робить, коли не може ні вперед, ні ліворуч, ні праворуч — назад чи стоїть (тоді він «загнаний»).
- (?) Чи кролик на відкритому полі біжить на 1 клітину, а не до упору — Gameluster: «usually one space».
- (?) Клавіші інструментів, вигляд HUD і наявність окремого лічильника на екрані гри.
- (?) Скільки рівнів у кожній норі і що в кінці (кінцівки, «Hell» біля E-13) — гайд згадує лише орієнтири.
- (?) Значення «стос не трусився» для домашньої ловлі — фраза гайду без пояснення механіки трусіння.
