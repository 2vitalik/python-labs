---
title: Cogs
slug: cogs
aka: []
family: connect-rotate
also: [push-slide]
klass: cursor
axes:
  field: 3d
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2009
platforms: [Windows, macOS, iOS, Linux, Android, PS3 (PlayStation Home)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cogs_(video_game)", best: true, note: "механіка: «пʼятнашки» на гранях 3D-обʼєкта, шестерні/пара/дзвони, 10 зірок, платформи, нагороди"}
  - {kind: steam, url: "https://store.steampowered.com/app/26500/Cogs/", note: "50 рівнів, віджети, режими Inventor / Time Challenge 30 с / Move Challenge 10 ходів, досягнення"}
  - {kind: other, url: "https://www.impulsegamer.com/pc/pccogs.htm", note: "огляд 2009: режими, ~50 рівнів, розблокування"}
  - {kind: other, url: "https://apps.apple.com/app/id413489665", note: "Mac App Store: опис режимів, ремастер 2025"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cogs+2009+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, pipe-connectors, connectivity-check, completion-detection, move-counter, move-limit, time-out, level-unlock, mode-select, puzzle-select, achievements-window, movement-animation, +sliding-tile-board, +gear-train, +steam-flow, +multi-face-board, +double-sided-tiles, +camera-orbit, +star-scoring, +melody-timing]
proposes: ["+effect:slide_tile", "+effect:spin", "+cond:meshed", "+ui:camera-orbit", "+card:gear-train", "+card:multi-face-board"]
author: opus
date: 2026-11-09
---

# Cogs — «пʼятнашки», з яких складається машина: зсувай плитки, щоб зачепити шестерні, провести пару й заграти мелодію

## Суть
Пазл з плиток, що зсуваються в порожнє місце, як у класичних «пʼятнашках», але мета — не впорядкувати картинку, а **зібрати працюючий механізм**: на плитках шестерні, труби, частини машини, і правильне розташування змушує колеса крутитися, пару — текти до моторів і повітряних куль, молоточки — бити в дзвони. Пізні пазли лежать на гранях 3D-обʼєктів: сітка переходить з грані на грань, важать обидва боки плитки, обʼєкт треба обертати. Ранні рівні вчать одну деталь, пізні поєднують кілька.

## Поле і час
- Поле — прямокутні сітки плиток з однією діркою; у 2D — одна панель, у 3D — грані обʼєкта, де пазл може охоплювати кілька граней чи «обгортати» обʼєкт; лицьовий і зворотний бік плитки мають значення.
- Механізм працює постійно: щойно ланцюг з'єднано, шестерні крутяться, пара тече — перевірка стану, а не тіки (`time: static`).
- Час і кількість ходів не обмежують розвʼязання в Inventor, але впливають на зірки; у челенджах — жорсткі ліміти (30 с або 10 ходів).
- Камера — обертання обʼєкта, щоб бачити інші грані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дірка (порожнє місце) | zone | 1 на сітку (?) | сюди зсувається сусідня плитка |
| Порожня плитка | tile | — | лише займає місце, зсувається |
| Плитка з шестернею | tile (conduit) | розмір шестерні | передає обертання зачепленим сусідам; різні розміри міняють швидкість |
| Шестерня-привід | source | крутиться від мотора | джерело обертання |
| Колесо / пропелер-ціль | sink | — | має закрутитись — частина умови перемоги |
| Плитка з трубою | tile (conduit) | виходи на сторони | веде кольорову пару/газ далі |
| Джерело пари | source | колір | живить трубопровід |
| Мотор / повітряна куля | sink | колір (?) | працює/надувається, коли до нього дійшла пара |
| Дзвін (chime) | sink | нота | звучить від удару молоточка |
| Молоточок | object | привід від шестерень | б'є в дзвін; мелодія має збігтися за таймінгом |
| Рамка / нерухома частина | static | — | не зсувається, частина механізму |
| 3D-обʼєкт | zone | кілька граней-сіток | грані зʼєднані краями; обертається камерою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, tile)` → ЯКЩО `custom: «плитка сусідить з діркою»` → ТО `custom: «плитка зсувається в дірку»` (`+effect:slide_tile`), `counter(moves, +1)`.
- КОЛИ `input(click, tile)` → ЯКЩО `not custom: «плитка сусідить з діркою»` → ТО `block`.
- КОЛИ `custom: «плитка переходить через ребро обʼєкта»` → ТО `custom: «продовжує рух на сусідній грані; показує інший бік»` (3D-пазли).
- КОЛИ `custom: «шестерня зачепилась за ту, що крутиться»` (`+cond:meshed`) → ТО `custom: «крутиться в протилежний бік зі швидкістю за відношенням розмірів»` (`+effect:spin`).
- КОЛИ `custom: «труба зʼєднана з джерелом пари»` → ТО `custom: «пара тече далі по зʼєднаних портах»`; дійшла до кулі — `custom: «куля надувається»`, до мотора — `custom: «мотор працює»`.
- КОЛИ `custom: «молоточок крутиться від механізму»` → ТО `custom: «б'є в дзвін»`; ЯКЩО `custom: «порядок і такт ударів = мелодія»` → умова виконана.
- КОЛИ `all_constraints_met` (усі цілі машини працюють) → ТО `win`, `window(end-screen)` із зірками.
- КОЛИ `custom: «рівень пройдено»` → ТО `score(3)` за проходження, `score(0..3)` за ходи, `score(0..3)` за час, ще `score(1)`, якщо обидва — максимум (до 10 зірок).
- КОЛИ `counter(stars_total, >=, n)` → ТО `unlock(next_puzzles)`.
- КОЛИ `custom: «пройдено в Inventor»` → ТО `unlock(time_challenge(level))`.
- Time Challenge: КОЛИ `counter(time, >=, 30)` → ЯКЩО `not all_constraints_met` → ТО `lose`.
- Move Challenge: КОЛИ `counter(moves, >, 10)` → ЯКЩО `not all_constraints_met` → ТО `lose`.
- Перемога: механізм працює повністю · Поразка: лише в челенджах (час/ходи) · Рахунок: зірки 0–10.

## Керування і ввід
- Миша/тач: клік або тап по плитці біля дірки — вона зсувається.
- Обертання 3D-обʼєкта (drag/жести) для огляду граней.
- Ходи рахуються, тож бездумне клацання знижує зірки.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Inventor / Time Challenge / Move Challenge) → `puzzle-select` (рівні зі зірками, замки) → `game-screen`.
- `game-screen`: пазл-обʼєкт, `move-counter`, `timer-elapsed` (у Time Challenge — `timer-countdown`), `restart-button` (?), керування камерою (`+ui:camera-orbit`).
- `end-screen`: розклад зірок (проходження, ходи, час, бонус).
- `achievements-window` — Steam-досягнення; `settings-window` (звук, графіка, ?).
- Переходи: main-menu → mode-select → puzzle-select → game-screen → end-screen → puzzle-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock` за зірками (близько 50 пазлів); `stars-rating` до 10 на рівень.
- `mode-time-attack` (30 с) і режим ліміту ходів (10) — розблоковуються пазлом у Inventor; `achievements` (Steam); `localization` — 14 мов.
- Версії: 2009 Win/Mac/iOS, 2011 Linux (Humble Indie Bundle 3), Android (Humble Bundle for Android 2), 3D-версія в PlayStation Home (PS3, 2011), ремастер на Unity (2025) для власників Steam.
- Потрапила в Potato Sack ARG перед Portal 2 — додано пазли на тему Portal 2.

## Варіації й родичі
- Класичні «пʼятнашки» (`sliding-tile-permutation`) — те саме переміщення, але мета — перестановка; Pipe Mania має бонус-раунд «пʼятнашки з трубами»; Loco-Motion — «пʼятнашки» з колією під потягом, що їде.
- Родичі за зʼєднанням: Infinity Loop і Plumber (поворот плиток-труб), Pipe Mania (потік від джерела), Chromatron і Deflektor (промінь до приймачів).
- **Осі варіацій**: як змінюється поле — поворот плитки / зсув у дірку / зсув ряду · що тече — обертання (шестерні) / рідина (труби) / сигнал у часі (дзвони) · поверхня — площина / грані 3D / тор · ліміт — без / час / ходи.

## Цікавинки для курсу
- «Пʼятнашки» як ядро: дірка + сусідня плитка, лічильник ходів — 🌱.
- Передача обертання: BFS по зачеплених шестернях з напрямком (чергування знаку) і швидкістю (відношення розмірів); конфлікт напрямків = заклинило (?) — 🥉.
- Потік пари по портах від джерела до куль/моторів (flood fill за `pipe-connectors`) — 📎.
- Сітка на гранях куба: сусідство через ребра й перехід на інший бік плитки — 🥈.
- Мелодія з дзвонів: перевірка порядку й таймінгу ударів при обертанні механізму — 🥈.
- Зірки 3 + 3 + 3 + 1 за проходження, ходи, час і бездоганність — 🌱.

## Мапа на каталог
- Є: `cell-click` · `pipe-connectors` (труби на плитках) · `connectivity-check` (джерело ↔ ціль) · `completion-detection` (машина працює) · `move-counter` · `move-limit` (Move Challenge, 10) · `time-out` (Time Challenge, 30 с) · `level-unlock` (зірками) · `mode-select` · `puzzle-select` · `achievements-window` · `movement-animation` (зсув плиток, обертання шестерень).
- **Нема** → пропозиції карток:
  - `+sliding-tile-board` «Плитки зсуваються в дірку» · entities/move · 📎.
  - `+gear-train` «Передача обертання шестернями» · entities/interact · 🥉 · слоти {ratio, direction}.
  - `+steam-flow` «Потік від джерела по трубах до приймачів» · entities/interact · 📎.
  - `+multi-face-board` «Сітка на гранях 3D-обʼєкта» · interface/render · 🥈.
  - `+double-sided-tiles` «Плитка з двома значущими боками» · entities/state · 📎.
  - `+camera-orbit` «Обертання обʼєкта/камери навколо пазла» · interface/render · 🥉.
  - `+star-scoring` «Зірки за проходження, ходи й час» · game-logic/score · 🌱.
  - `+melody-timing` «Ціль — правильна послідовність звуків у часі» · game-logic/win · 🥈.

## Пропозиції до словників
- `+effect:slide_tile(tile)` — плитка зсувається в сусідню дірку (є й у Loco-Motion).
- `+effect:spin(a, dir, speed)` — сутність починає обертатися (шестерня, колесо, пропелер).
- `+cond:meshed(a, b)` — дві шестерні зачеплені (сусідні клітини, зубці стикуються).
- `+ui:camera-orbit` — керування обертанням 3D-пазла.

## Джерела
- ⭐ [Wikipedia: Cogs](https://en.wikipedia.org/wiki/Cogs_(video_game)) — пʼятнашки на гранях 3D-обʼєкта, обидва боки плиток, шестерні різних розмірів, кольорова пара до моторів і куль, молоточки й мелодія, 10 зірок, платформи, нагороди, Potato Sack.
- [Steam](https://store.steampowered.com/app/26500/Cogs/) — 50 рівнів, перелік віджетів (шестерні, труби, кулі, дзвони, молоточки, колеса, пропелери), три режими, досягнення, 14 мов.
- [Impulse Gamer, огляд 2009](https://www.impulsegamer.com/pc/pccogs.htm) — режими, ~50 рівнів, розблокування.
- [Mac App Store](https://apps.apple.com/app/id413489665) — опис режимів, версія 2.0 (2025).
- YouTube — пошуковий лінк.

## Непевне
- (?) Чи зсувається лише одна сусідня плитка, чи цілий ряд до дірки одним кліком — джерела кажуть лише «sliding block puzzle».
- (?) Кількість дірок на 3D-обʼєкті (одна на грань чи одна на весь пазл).
- (?) Чи має колір пари відповідати кольору кулі/мотора — Wikipedia згадує «colored steam», без правила відповідності.
- (?) Що буває при конфлікті напрямків шестерень (заклинювання) — не перевірено.
- (?) Вікна `restart-button`, `settings-window` і деталі `puzzle-select` — з загальних описів, скріншотів не бачив.
