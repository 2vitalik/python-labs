---
title: Rytmos
slug: rytmos
aka: []
family: connect-rotate
also: [push-slide, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PC, Mac, Switch, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1634220/Rytmos/", best: true, note: "сторінка Steam: лабіринти на гранях кубічних планет, кожен розвʼязок — музична петля, 20+ музичних іграшок, трейлер"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rytmos", note: "геймплей: лінія йде прямо до перешкоди, може перетинати себе, має повернутись у старт; вузли = звуки; Gold за всі вузли; лід, портали, камені"}
  - {kind: other, url: "https://www.nintendoworldreport.com/reviewmini/63206/rytmos-switch-review", note: "огляд Switch: системи по 3 планетоїди × 6 граней, кубик льоду, розриви-варпи, планетоїд стає інструментом"}
  - {kind: other, url: "https://gameinformer.com/review/rytmos/music-to-my-ears", note: "огляд: диск крізь стовпи, лід ковзає до стіни, камені рухаються разом із диском, loop recorder"}
  - {kind: other, url: "https://developer.apple.com/news/?id=34m9vbvv", note: "Apple: емітери (тон/перкусія/акорд), кнопки, музика залежить від розвʼязку, jam mode"}
  - {kind: other, url: "https://www.pcgamesinsider.biz/interviews-and-opinion/73140/floppy-club-discuss-combining-game-creation-with-music-creation/", note: "інтервʼю: 6 секвенцій на планету, гра як великий секвенсор"}
  - {kind: other, url: "https://www.pocketgamer.com/rytmos/app-army-assemble/", note: "відгуки мобільних гравців: петля пальцем, пропуск пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rytmos+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [inertia-slide, push-object, teleport, impassable-cells, button-toggle, path-drawing, path-cut, skip-level, world-map, level-unlock, sequential-levels, sound-effects, background-music, game-screen, map-window, +closed-loop-path, +visit-all-nodes, +multi-agent-sync, +path-as-sequencer, +cube-faces, +jam-mode, +self-crossing-path, +bonus-goal-all-nodes]
proposes: ["+trigger:pass_through", "+effect:play_note", "+window:jam-mode", "+window:liner-notes", "+ui:loop-sequencer", "+feature:music-history-notes", "+card:path-as-sequencer", "+card:closed-loop-path"]
author: opus
date: 2026-11-09
---

# Rytmos — веди лінію-диск гранями кубічної планети так, щоб вона ковзнула до упору, зібрала звукові вузли й замкнулась у петлю, що грає музику

## Суть
Пазл-секвенсор від Floppy Club (Копенгаген): кожна з шести граней кубічного планетоїда — лабіринт, у якому гравець проводить лінію від старту й назад у старт. Лінія рухається **прямо до перешкоди** (як ковзання по льоду), може перетинати себе, а кожен вузол-емітер, через який вона пройшла, стає нотою: замкнена петля — це одна музична доріжка, шість граней — шість доріжок однієї пісні. Розвʼязок необовʼязково має пройти всі вузли — «Gold» дають за всі, тож два гравці можуть отримати різну музику.

## Поле і час
- Планетоїд — куб; кожна грань — окреме квадратне поле-лабіринт зі стінами, вузлами й механізмами; між гранями — поворот планети.
- Хід = одне ковзання в обраному напрямку до упору; лінія лишається слідом.
- Розриви на поверхні переносять лінію в іншу точку, даючи «неможливі» кути (?) — у межах грані чи між гранями — не перевірено.
- Музика: петля відтворюється циклом; порядок і відстані між вузлами задають ритм (гра — «великий секвенсор»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Диск (голова лінії) | player | напрямок | ковзає прямо до перешкоди, лишає лінію |
| Лінія | mark | — | може перетинати сама себе; має повернутись у старт |
| Старт | terminal (custom) | — | початок і кінець петлі |
| Вузол-емітер | mark | звук: тон / перкусія / акорд | лінія, що пройшла крізь нього, додає звук у доріжку |
| Стіна / стовп | static | — | зупиняє ковзання |
| Кубик льоду | object | — | лінія його штовхає; ковзає до стіни, далі слугує упором або закриває глухий кут |
| Камінь-орігамі | object | — | рухається разом із диском (?) |
| Портал / розрив | terrain | пара (?) | переносить лінію в іншу точку, рух триває |
| Кнопка | switch | ціль (?) | спрацьовує, коли лінія проходить, — змінює щось на грані (?) |
| Планетоїд | zone | 6 граней | після 6 петель стає музичним інструментом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `slide(disc, dir)`; лінія тягнеться слідом; інакше `block`.
- КОЛИ `blocked(disc)` → ТО `custom: «ковзання закінчено, новий злам лінії»`.
- КОЛИ `contact(disc, node)` (проїзд крізь вузол) → ТО `sound(node.tone)`, `mark(node, passed)`.
- КОЛИ `contact(disc, line)` → ТО `custom: «перетин власної лінії дозволений, ковзання триває»`.
- КОЛИ `contact(disc, ice)` → ЯКЩО `free(cell_behind_ice)` → ТО `push`, `slide(ice, dir)` до стіни; інакше `block` (лід як упор).
- КОЛИ `input(dir)` → ЯКЩО на грані є камінь → ТО `move(rock, dir)` разом із диском (?).
- КОЛИ `enter(disc, portal)` → ТО `teleport(disc, pair)`, ковзання триває в тому ж напрямку (?).
- КОЛИ `contact(disc, button)` → ТО `custom: «кнопка змінює стан механізму грані»` (?).
- КОЛИ `input(back)` (провести назад по лінії) → ТО `undo(1)` — останній відрізок стирається.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля закінчилась у старті»` → ТО `win` (грань), `custom: «петля стає доріжкою пісні»`.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `counter(nodes_passed, =, nodes_total)` → ТО `custom: «нагорода Gold»`.
- КОЛИ `counter(faces_done, =, 6)` → ТО `transform(planetoid, instrument)`, `unlock(instrument)`, `window(jam)`.
- КОЛИ `input(skip)` → ТО `next_level` (складну грань можна пропустити).
- Перемога: петля замкнена в старті. · Поразка: нема. · Рахунок: Gold, якщо пройдено всі вузли.

## Керування і ввід
- ПК: курсор задає напрям — лінія йде в бік курсора до перешкоди; Switch — аналоговий стік; мобільні — малювання пальцем.
- Поворот планетоїда — щоб перейти до наступної грані.
- Відкат — повести лінію назад по сліду.
- Jam-режим: грати на відкритому інструменті, записувати петлі, накладати модифікатори (bit crusher, low-pass, delay, stutter).

## Вікна, меню, HUD
- `map-window`: сонячні системи, кожна — музичний жанр (мбіра Зімбабве, ефіопський джаз, гамелан, японська ambient-музика…); планетоїди — вузли.
- `game-screen`: планетоїд з поточною гранню; лінія, вузли, механізми; доріжки, що вже грають.
- `jam-mode` (custom-window): інструмент планетоїда + loop recorder + модифікатори; 20+ музичних іграшок.
- `liner-notes` (custom-window): нотатки про історію жанру кожної системи.
- `settings-window` (?) — не перевірено.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `world-map`: системи → планетоїди → 6 граней; завершений планетоїд відкриває наступний.
- `skip-level`; `stars-rating`-подібна Gold-нагорода за всі вузли.
- `unlockables`: 20+ інструментів і модифікаторів; `mode-sandbox` (jam) без правил.
- `rules-page`-подібне: історія музичних жанрів у нотатках.
- Демо безкоштовне, повна версія — покупкою (мобільні).

## Варіації й родичі
- Ковзання до упору: [ice-sliding-puzzles](../push-slide/ice-sliding-puzzles.md), [Ice Path](../thinky/ice-path.md), [Tomb of the Mask](../push-slide/tomb-of-the-mask.md), [Quell](../push-slide/quell.md).
- Лінія і петля: [LYNE](lyne.md), [Flow Free](flow-free.md), [Cosmic Express](cosmic-express.md); замкнена петля як обмеження — Slitherlink/Masyu (pencil-logic).
- Осі варіацій: **рух лінії**: по клітині (Flow Free) / до упору (Rytmos) · **мета лінії**: зʼєднати термінали / замкнути петлю · **вузли**: обовʼязкові / бонусні (Gold) · **вихід**: перемога / музика з розвʼязку.

## Цікавинки для курсу
- Ковзання до упору + слід + перевірка повернення в старт — 📎.
- Лід, що штовхається і ковзає, стаючи новим упором — 🌱 (родич `push-object` + `inertia-slide`).
- Портал з продовженням руху в тому ж напрямку — 🌱.
- Петля як секвенсор: вузли на шляху → ноти з часом, пропорційним пройденій відстані — 🥉.
- Gold-критерій «усі вузли» як окрема перевірка поверх перемоги — 🌱.
- Розвʼязувач: BFS по станах (позиція, напрям, позиції льоду, множина вузлів) — 🥈.

## Мапа на каталог
- Є: `inertia-slide` ↔ ковзання лінії; `push-object` ↔ лід; `teleport` ↔ портали; `impassable-cells` ↔ стіни; `button-toggle` ↔ кнопки (?); `path-drawing` + `path-cut` ↔ малювання й відкат; `skip-level`; `world-map` + `level-unlock` + `sequential-levels` + `map-window`; `sound-effects` + `background-music`.
- **Нема** → пропозиції карток:
  - `+closed-loop-path` «Шлях має повернутись у старт» · game-logic/win · 🌱.
  - `+visit-all-nodes` (з LYNE) — тут лише для Gold; `+bonus-goal-all-nodes` «Необовʼязкова ціль поверх перемоги» · game-logic/score · 🌱.
  - `+self-crossing-path` «Лінія може перетинати себе» · interface/input · 🌱.
  - `+multi-agent-sync` — камінь, що рухається з диском (?).
  - `+path-as-sequencer` «Шлях як музична секвенція» · interface/sound · 🥉.
  - `+cube-faces` «Поле — грані куба з поворотом» · interface/render · 🥉.
  - `+jam-mode` «Пісочниця-інструмент після рівня» · interface/sound · 📎.

## Пропозиції до словників
- `+trigger:pass_through(a, node)` — лінія пройшла крізь вузол, не зупиняючись (тут вжито `contact`).
- `+effect:play_note(note)` — додати ноту в доріжку (точніше за `sound`).
- `+window:jam-mode` — вільна гра на відкритому інструменті з записом петель.
- `+window:liner-notes` — нотатки про історію музики світу.
- `+ui:loop-sequencer` — доріжки граней, що грають разом.
- `+feature:music-history-notes` — освітній текст до кожної системи.
- `+card:path-as-sequencer`, `+card:closed-loop-path`.

## Джерела
- ⭐ [Steam: Rytmos](https://store.steampowered.com/app/1634220/Rytmos/) — лабіринти на гранях кубічних планет, петлі-доріжки, 20+ іграшок, інструменти й модифікатори, 28.02.2023.
- [Wikipedia: Rytmos](https://en.wikipedia.org/wiki/Rytmos) — лінія до перешкоди, самоперетин, повернення в старт, вузли = звуки, 6 поверхонь, Gold, лід/портали/камені, платформи й дати.
- [Nintendo World Report](https://www.nintendoworldreport.com/reviewmini/63206/rytmos-switch-review) — 3 планетоїди × 6 граней на систему, лід як упор, розриви-варпи, інструмент.
- [Game Informer](https://gameinformer.com/review/rytmos/music-to-my-ears) — диск крізь стовпи, лід до стіни, камені з диском, loop recorder.
- [Apple Developer: Behind the Design](https://developer.apple.com/news/?id=34m9vbvv) — емітери, кнопки, різна музика в різних розвʼязках, jam mode.
- [PC Games Insider: інтервʼю](https://www.pcgamesinsider.biz/interviews-and-opinion/73140/floppy-club-discuss-combining-game-creation-with-music-creation/) — 6 секвенцій, гра як секвенсор, темп і лад.
- [Pocket Gamer: App Army](https://www.pocketgamer.com/rytmos/app-army-assemble/) — петля пальцем, пропуск пазлів, демо.
- YouTube: пошук «Rytmos gameplay».

## Непевне
- (?) Кількість систем/планетоїдів: NWR — «3 планетоїди на систему», Game Informer — «сім небесних тіл» і «18» (неясно чого).
- (?) Камені «рухаються з диском» — одне речення огляду; синхронно в тому ж напрямку — припущення.
- (?) Дія кнопок і чи портали ведуть на іншу грань.
- (?) Як саме керують на ПК (клік-напрям чи drag) і чи є кнопка undo, крім відведення лінії назад.
- (?) Чи час ноти в петлі залежить від довжини відрізка — висновок з «гра — секвенсор».
