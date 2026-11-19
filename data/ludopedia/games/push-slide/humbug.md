---
title: Humbug
slug: humbug
aka: [Humbug 2]
family: push-slide
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: collect
year: 2018
platforms: [iOS, iPadOS, macOS (Apple Silicon)]
links:
  - {kind: other, url: "https://www.pocketgamer.com/humbug/review/", best: true, note: "огляд Pocket Gamer, 30.11.2018: свайп, павук ковзає до краю й падає, якщо не підставити жука, равлик — упор, цвіркун стрибає через стіни й відштовхується від спин, ліміт ходів"}
  - {kind: other, url: "https://apps.apple.com/us/app/humbug/id1436145670", note: "App Store: Dunderbit; безкоштовна з рекламою й монетами; історія версій — жуки-beetles і яйця (2019), таргани й гусениці (2020), двічі по +50 рівнів"}
  - {kind: other, url: "https://apps.apple.com/us/app/humbug-2/id6753792967", note: "Humbug 2 (2026): без реклами, 30 рівнів безкоштовно, 250+ у повній, редактор і рівні спільноти; жуки «walk, jump or fly»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Humbug+Dunderbit+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [swipe-gestures, move-by-input, party-switch, inertia-slide, collect-all, move-limit, undo-redo, restart-level, sequential-levels, world-map, in-game-editor, editor-palette, editor-erase, +stop-on-entity, +fall-off-edge, +edge-walls, +jump-over, +multi-jump, +flying-move, +paid-hint, +community-levels]
proposes: ["+effect:jump", "+card:stop-on-entity"]
author: opus
date: 2026-11-19
---

# Humbug — свайпом рухай жуків із різним ходом: павук ковзає до упору й падає з краю, цвіркун перестрибує стіни, а зібрати треба всі зірки за обмежену кількість ходів

## Суть
Острівці з плиток у ізометрії, на них — жуки й зіркові плитки. Свайп рухає одного жука за його власним правилом: павук пролітає всю лінію й падає з краю, якщо на шляху нема іншого жука; равлик повільний, зате ним зручно перепиняти павука; цвіркун стрибає через стіни й «відштовхується від спин» інших жуків. Мета — зібрати зірки, не проскочивши повз і не вийшовши за ліміт ходів; пізніші оновлення додали нових жуків, а Humbug 2 (2026) — редактор і рівні спільноти.

## Поле і час
- Квадратна сітка плиток неправильної форми, намальована в ізометрії; краї плиток місцями мають бортики-стінки; порожнеча довкола — обрив.
- Теми плиток — трава, дерево, лід, желе, темний камінь (на знімках); чи впливає тема на рух — невідомо (?).
- Хід = один свайп одного жука; лічильник «MOVES LEFT» угорі зменшується.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Павук | piece | — | ковзає вздовж лінії до упору; упором служить інший жук; без упору падає з краю |
| Равлик | piece | — | «slow but steady» — мабуть, крок на плитку (?); упор для павука |
| Цвіркун (коник) | piece | — | стрибає через стіни; приземлившись на спину жука, відштовхується й летить далі |
| Сонечко | piece | — | є на знімках, у описі Thinky Games (?); хід не бачив |
| Метелик, бджола (Humbug 2) | piece | — | літають (Humbug 2: «walk, jump or fly») (?) |
| Жук (beetle), яйце | piece | — | додані у v2.0.0 (2019) (?) |
| Тарган, гусениця | piece | — | додані у v2.2.4 (2020) (?) |
| Плитка | terrain | тема | по ній ходять; за краєм — обрив |
| Зіркова плитка | zone | у Humbug 2 буває 1–3 зірки | мета: зібрати всі |
| Бортик на краю плитки | static | сторона | зупиняє ковзання; цвіркун перестрибує (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe, spider)` → ЯКЩО `occupied(line_ahead, bug)` → ТО `slide(spider, dir)`, `counter(moves_left, -1)` — зупиняється на клітині перед жуком.
- КОЛИ `edge(spider)` → ТО `fall(spider)` — «tumble off the edge», мабуть, провал рівня (?).
- КОЛИ `input(swipe, snail)` → ЯКЩО `free(next_cell)` → ТО `move(snail, dir)`, `counter(moves_left, -1)` (?).
- КОЛИ `input(swipe, cricket)` → ТО `custom: «стрибок через стіну; з чужої спини — ще один стрибок далі»`, `counter(moves_left, -1)`.
- КОЛИ `enter(bug, star_tile)` → ЯКЩО `custom: «жук закінчив хід на плитці»` → ТО `custom: «зірку зібрано»` (?).
- КОЛИ `all_gone(star)` → ТО `win`, `currency(+n)` — монети за пройдений рівень (?).
- КОЛИ `counter(moves_left, ==, 0)` → ЯКЩО `count(star, >, 0)` → ТО `lose`.
- КОЛИ `input(undo)` → ТО `undo`, `currency(-10)` — так на знімках ранніх версій; з v1.2.0 «undo made free».
- КОЛИ `input(hint)` → ТО `custom: «підказка за монети»` (?).
- Перемога: усі зірки зібрано. · Поразка: ходи скінчились, а зірки лишились; павук злетів з краю (?). · Рахунок: нема; монети — валюта підказок і раннього відкриття рівнів.

## Керування і ввід
- Свайп по жуку в бік руху (сенсорний екран); на Mac — те саме мишею (?).
- Кнопки: UNDO (з ціною в монетах), HINT (лампочка), рестарт, меню.

## Вікна, меню, HUD
- `game-screen` — острівець; угорі: `undo-button` з ціною «10 🪙», `move-counter` «N MOVES LEFT», `hint-button`; унизу: `level-number`, `restart-button`, меню.
- `shop-window` — «No Ads» і пакети монет (in-app).
- Humbug 2: `main-menu` (My levels · Play · Store); `map-window` — стежка з вузлами-рівнями; `editor-window` (Move · Themes · Toolbox · Erase); `custom-window` спільноти (вкладки My levels / Community, поділитись, видалити); `help-window` (кнопка «Rules» на рівні); нижня панель Menu · Restart · Undo · Hint.
- Переходи: меню → мапа / список → рівень → (зірки зібрано) наступний.

## Фічі поза полем
- `undo` (спершу за монети, з v1.2.0 безкоштовний), `restart-level`, `hint` за монети (`+paid-hint`), `levels-sequential`.
- Модель: безкоштовна гра з рекламою; «No Ads» $2.99, монети пакетами.
- Оновлення контенту: v2.0.0 — +50 рівнів, жуки (beetles) і яйця; v2.2.4 — +50 рівнів, таргани й гусениці.

## Варіації й родичі
### Humbug 2 (2026)
- Той самий принцип «у кожного жука свій хід»; жуки ходять, стрибають і літають; у рівнях — плитки з кількома зірками, кільця, яйця (на знімках) (?).
- Без реклами; 30 рівнів безкоштовно, повна гра — 250+ рівнів; `world-map` зі стежкою рівнів.
- `level-editor` (палітра «Toolbox», «Themes», «Erase», переміщення), `level-sharing` і `user-levels-browser` — рівні спільноти.

### Родичі й осі
- [Ricochet Robots](ricochet-robots.md) — фігура ковзає до першої перешкоди, інші фігури — упори (`+stop-on-entity`).
- [Ice-sliding puzzles](ice-sliding-puzzles.md) — ковзання до упору; [Slayaway Camp](slayaway-camp.md) — ковзання з наслідком удару.
- Осі варіацій:
  - **хід фігури**: крок (равлик) / ковзання до упору (павук) / стрибок через стіну й ланцюг відскоків (цвіркун) / політ (Humbug 2);
  - **що за краєм**: стіна / обрив і падіння (тут);
  - **мета**: фігура на цілі / усі цілі зібрано за ліміт ходів (тут).

## Цікавинки для курсу
- Кілька типів фігур з різними правилами руху на одному полі — 🥉 (поліморфізм: клас на тип жука).
- Ковзання до першого жука, падіння з краю, якщо упору нема — 📎.
- Стрибок цвіркуна з ланцюгом відскоків від спин — 📎.
- Зібрати всі зірки за N ходів — 🌱.
- BFS-розвʼязувач для кількох фігур і ліміту ходів — 🥈.
- Редактор рівнів зі збереженням і обміном (Humbug 2) — 🥈.

## Мапа на каталог
- Є: `swipe-gestures` + `move-by-input`; `party-switch` ↔ свайп обирає жука; `inertia-slide` ↔ павук; `collect-all` ↔ усі зірки; `move-limit` ↔ «MOVES LEFT»; `undo-redo`, `restart-level`; `sequential-levels`, `world-map` (Humbug 2); `in-game-editor` + `editor-palette` + `editor-erase` (Humbug 2).
- **Нема** → пропозиції карток:
  - `+stop-on-entity`, `+fall-off-edge`, `+edge-walls`, `+jump-over`, `+multi-jump`, `+flying-move`, `+paid-hint`, `+community-levels` (є в корпусі).

## Пропозиції до словників
- `+effect:jump` — стрибок фігури через перешкоду (тут — `custom`).
- `+card:stop-on-entity` — ковзання до першої фігури на лінії як окрема картка; у корпусі тег уже в пʼяти іграх.

## Джерела
- ⭐ [Pocket Gamer: Humbug review](https://www.pocketgamer.com/humbug/review/) — правила павука, равлика й цвіркуна, мета «guiding them to their designated resting point… without overshooting or exceeding your move count».
- [App Store: Humbug](https://apps.apple.com/us/app/humbug/id1436145670) — розробник Dunderbit, дата 22.11.2018, модель, історія версій; 8 знімків (HUD, жуки, теми плиток).
- [App Store: Humbug 2](https://apps.apple.com/us/app/humbug-2/id6753792967) — опис 2026, 8 знімків (мапа, редактор, спільнота, кнопка Rules).

## Непевне
- (?) Рухи равлика, сонечка, метелика, жука-beetle, яйця, таргана й гусениці не бачив; «ladybugs, snails and spiders» і «grasshoppers» — зі сніпетів пошуку (Thinky Games, Google Play), сторінок не відкривав.
- (?) Чи зірку збирає жук, що лише проходить через плитку, чи тільки той, що зупинився («without overshooting» каже за друге).
- (?) Що стається з павуком, який злетів, — провал рівня чи просто втрачений жук.
- (?) Чи є версія для Android (згадка Google Play в сніпеті) і чи Humbug 2 вийшов поза iOS.
