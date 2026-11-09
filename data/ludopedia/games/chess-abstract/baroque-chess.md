---
title: Baroque chess / Ultima (Бароккові шахи)
slug: baroque-chess
aka: [Ultima, Ультима, Бароккові шахи]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1962
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Baroque_chess", best: true, note: "повні правила: фігури, способи взяття, симетрії розстановки, варіанти Maxima/Renaissance/Rococo"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=baroque+chess+ultima+rules", note: "пошук; пояснення правил"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, cell-click, drag-drop-piece, hot-seat, ai-opponent, turn-enforcement, rule-variants, help-window, game-screen, end-screen, +custodial-capture, +withdrawal-capture, +leap-capture, +coordinator-capture, +immobilizer-aura, +chameleon-capture, +king-capture-win, +setup-symmetry-choice]
proposes: ["+trigger:move_away", "+cond:adjacent_enemy", "+cond:sandwiched", "+cond:immobilized", "+effect:capture_as", "+ui:frozen-marker", "+ui:capture-preview", "+window:setup-choice", "+card:custodial-capture", "+card:immobilizer-aura", "+card:chameleon-capture"]
author: opus
date: 2026-11-09
---

# Ultima / Baroque chess — шість фігур, і кожна бере по-своєму: затиском, відходом, стрибком, перехрестям, мімікрією

## Суть
Шаховий набір на дошці 8×8, але майже всі фігури ходять як ферзь, а різниця — **у способі взяття**: пішак затискає ворога між собою й своєю фігурою, «відступник» бʼє, відходячи від сусіда, «стрибун» перестрибує жертву, координатор бере по перехрестю зі своїм королем, імобілізатор нікого не бʼє, але паралізує сусідів, а хамелеон копіює спосіб взяття того, кого бʼє. Мета — взяти короля. Це найкращий у корпусі приклад «взяття ≠ хід на клітину жертви» — шість окремих правил захоплення на одному рушії.

## Поле і час
- Дошка 8×8, стандартний набір Staunton (фігури перейменовано й перевернуто одну туру).
- Розстановка як у шахах, але перед партією кожен гравець робить **два вибори симетрії**: центр (можна поміняти місцями короля й відступника-ферзя) і кути (котра тура стоїть догори дриґом: прямо — координатор, перевернута — імобілізатор).
- Покроковий хід, білі першими; на клітині ≤1 фігура; свої фігури ніколи не бʼють своїх.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | royal | ходить на 1, як шаховий; бʼє заходом на клітину жертви; без рокіровки |
| Пішак / Pincer (Squeezer) | piece | — | ходить як тура; бʼє **затиском**: ворог ортогонально між клітиною приходу пішака і своєю фігурою; навскоси не бʼє; не перетворюється |
| Відступник / Withdrawer (ферзь) | piece | — | ходить як ферзь; бʼє ворога, що стоїть поруч, **відходячи** від нього по прямій |
| Довгий стрибун / Long leaper (кінь) | piece | — | ходить як ферзь; бʼє, **перестрибуючи** ворога по прямій (кілька жертв по одній лінії, якщо між ними є порожні клітини для приземлення) |
| Координатор / Coordinator (пряма тура) | piece | — | ходить як ферзь; після ходу бере ворогів на двох клітинах: (його файл × ряд свого короля) і (файл короля × його ряд) |
| Імобілізатор / Immobilizer (перевернута тура) | piece | — | ходить як ферзь; нікого не бере; усі ворожі фігури поруч (8 сусідів) не можуть ходити |
| Хамелеон / Chameleon, Imitator (слон) | piece | — | ходить як ферзь; бере ворога **тим способом, яким бере сама жертва**; паралізує ворожого імобілізатора поруч; не бере хамелеонів; короля бере, починаючи хід поруч і стаючи на його клітину |
| Знерухомлена фігура | piece | стан `frozen` | лишається на місці, доки поруч ворожий імобілізатор; у деяких версіях власник може замість ходу зняти її з дошки |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух:
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «p — не король і не пішак»` and `custom: «шлях як у ферзя вільний»` → ТО `move(p, to)`.
- КОЛИ `input(move(pawn, to))` → ЯКЩО `custom: «шлях як у тури вільний»` → ТО `move(pawn, to)`.
- КОЛИ `input(move(king, to))` → ЯКЩО `custom: «на 1 клітину в будь-якому з 8 напрямків»` → ТО `move(king, to)`; ЯКЩО `occupied(to, enemy)` → ТО `disappear_b`.
- КОЛИ `input(move(p, …))` → ЯКЩО `state(p, frozen)` → ТО `block`.
- КОЛИ `adjacent8(enemy_immobilizer, p)` → ТО `set_state(p, frozen)`; КОЛИ `custom: «імобілізатор пішов/узятий»` → ТО `clear_state(p, frozen)`.
- Варіант: КОЛИ `input(remove(p))` → ЯКЩО `state(p, frozen)` → ТО `disappear_a`, `end_turn` (самогубство замість ходу).

Взяття (усі — наслідок звичайного ходу, жертва зазвичай не на клітині приходу):
- Pincer: КОЛИ `after(move(pawn, to))` → ЯКЩО `custom: «ворог ортогонально поруч з to, а за ним — своя фігура»` → ТО `disappear_b` (до 4 жертв за хід — по одній у кожному напрямку (?)).
- Withdrawer: КОЛИ `after(move(withdrawer, dir))` → ЯКЩО `custom: «до ходу ворог стояв поруч у протилежному від dir напрямку»` → ТО `disappear_b`.
- Long leaper: КОЛИ `input(move(leaper, to))` → ЯКЩО `custom: «на лінії ворог(и), за кожним — порожня клітина; своїх і двох ворогів поспіль нема»` → ТО `disappear_b` для кожного перестрибнутого.
- Coordinator: КОЛИ `after(move(coord, to))` → ЯКЩО `occupied(custom: «клітина (file(to), rank(own_king))», enemy)` → ТО `disappear_b`; так само для `(file(own_king), rank(to))`.
- Immobilizer: нічого не бере; лише `set_state(frozen)` сусідам.
- Chameleon: КОЛИ `input(move(cham, to))` → ЯКЩО `custom: «хід був би взяттям, якби chameleon мав спосіб взяття жертви»` → ТО `disappear_b` (затиск лише проти пішаків, відхід — проти відступника, стрибок — проти стрибуна, координація — проти координатора).
- Chameleon vs король: КОЛИ `input(move(cham, king_cell))` → ЯКЩО `custom: «chameleon почав хід поруч з ворожим королем»` → ТО `disappear_b`, `win`.
- Chameleon vs імобілізатор: КОЛИ `adjacent8(cham, enemy_immobilizer)` → ТО `set_state(enemy_immobilizer, frozen)` (взаємний параліч).
- КОЛИ `contact(p, own_piece)` → ТО `block` (свої не беруться ніколи); хамелеон не бере хамелеона.

Кінець партії:
- КОЛИ `custom: «ворожий король узятий будь-яким способом»` → ТО `win`.
- Перемога: взяття короля · Пат і «голий король» — стаття не уточнює (див. «Непевне»).

## Керування і ввід
- Звичайний хід фігурою (клік-клік або drag); взяття відбувається автоматично після ходу — бажано показувати, хто буде знятий, до підтвердження.
- Перед першим ходом — два вибори симетрії (центр, кути) кожного гравця; нотація прикладу: `1. Kd1 & We1, Ke8 & Wd8` (центр), `2. Ia1 & Ch1, Ih8 & Ca8` (кути).
- Варіант із самогубством: окрема дія «зняти знерухомлену фігуру».

## Вікна, меню, HUD
- (цифрова версія) `setup-choice` — вибір симетрії центру і кутів перед партією.
- `game-screen`: дошка з `frozen-marker` на паралізованих фігурах, `legal-move-highlight`, `capture-preview` (які фігури зникнуть після цього ходу), `turn-indicator`, `captured-pieces`.
- `help-window` — правила взяття кожної фігури (без цього гра нечитабельна).
- `end-screen` — король узятий.
- Переходи: main-menu → match-setup → setup-choice → game-screen → end-screen.

## Фічі поза полем
- (цифрова версія) `hotseat`, `ai-opponent-levels`, `rules-page` з анімацією кожного способу взяття.
- `custom-rules` — перемикачі суперечливих правил: множинне взяття стрибуна, самогубство знерухомленої фігури, правки Abbott після 1962.

## Варіації й родичі
- Сам Abbott згодом вважав гру хибною і пропонував поправки; спільнота здебільшого грає за правилами 1962. Є регіональні версії (популярна серед студентів Кембриджа 1974).
- Leaper-варіант: стрибун бере лише першого ворога, якщо за ним порожньо (без множинних стрибків).
- **Maxima** (Roberto Lavieri, 2003): дошка 8×9 з додатковими клітинами, циліндр, король ходить конем, нові фігури Mage і Guard. **Optima** — подібна до Maxima.
- **Renaissance** (Matthew Monchalin, 1975): 9×9, взяті переходять на інший бік і дропаються; Resurrector (Swapper/Ankh), Bomb, Pusher, Puller.
- **Rococo** (Peter Aronson, David Howe, 2002): 10×10 для взяття, рух у внутрішніх 8×8; Advancer, Swapper, «cannonball pawns» (ходять як король, бʼють стрибком).
- Родичі в корпусі: затиск — як у [go.md](go.md)/хнефатафлі й Ataxx-перефарбуванні ([ataxx.md](ataxx.md)); стрибок-взяття — [checkers.md](checkers.md); параліч — родич «заморожування» Arimaa ([arimaa.md](arimaa.md)); інші твісти — [chess-rule-twists.md](chess-rule-twists.md).
- **Осі варіацій**: як береться жертва (заходом · затиском · відходом · перестрибом · перехрестям з королем · копією способу жертви) · аура фігури (нема · параліч сусідів) · множинні взяття (так · лише перша жертва) · розстановка (фіксована · з вибором симетрії).

## Цікавинки для курсу
- Custodial capture (затиск) з чотирма напрямками — 📎.
- Withdrawal (взяття відходом) і long leap з кількома жертвами — 🥉: взяття не на клітині приходу.
- Координатор: «віртуальні» клітини перетину з власним королем — 🥉.
- Імобілізатор як аура (стан сусідів перераховується після кожного ходу будь-кого) — 🥉.
- Хамелеон: взяття поліморфне — правило взяття береться з типу жертви (диспетчеризація за парою типів) — 🥈; плюс спецвипадки (король, імобілізатор, хамелеон).
- `capture-preview` — показати всі зняті фігури до ходу — 📎, але без нього гра незрозуміла.
- AI: генератор ходів із шістьма правилами взяття + minimax — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ ферзь/тура/король · `piece-capture` ↔ лише король бере «як у шахах» · `legal-move-highlight` · `cell-click` · `drag-drop-piece` · `hot-seat` · `ai-opponent` · `turn-enforcement` · `rule-variants` ↔ поправки Abbott, Leaper-варіант · `help-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+custodial-capture` «Взяття затиском між двома своїми» · entities/combat · 📎 — Baroque, хнефатафл, Hasami Shogi.
  - `+withdrawal-capture` «Взяття відходом від сусіда» · entities/combat · 📎 — Baroque, Fanorona.
  - `+leap-capture` «Взяття перестрибом» · entities/combat · 📎 — шашки, Baroque.
  - `+coordinator-capture` «Взяття на перехресті з іншою своєю фігурою» · entities/combat · 🥉.
  - `+immobilizer-aura` «Аура паралічу сусідніх ворогів» · entities/state · 🥉.
  - `+chameleon-capture` «Взяття способом жертви» · entities/combat · 🥈.
  - `+king-capture-win` — підтверджую (chess-rule-twists).
  - `+setup-symmetry-choice` «Вибір дзеркальних варіантів розстановки перед партією» · levels/generation · 🌱.

## Пропозиції до словників
- `+trigger:move_away(a, b)` — A відійшов від сусіда B (відступник).
- `+cond:adjacent_enemy(a, dir)` — у напрямку dir поруч ворог.
- `+cond:sandwiched(b, by)` — B між двома фігурами сторони by по прямій (затиск; хнефатафл, го-подібні).
- `+cond:immobilized(p)` — фігуру паралізує сусідня аура (окремо від загального `state`, бо перераховується щоходу).
- `+effect:capture_as(type)` — взяти способом іншого типу фігури (хамелеон).
- `+ui:frozen-marker` — позначка паралізованої фігури.
- `+ui:capture-preview` — підсвітити фігури, що зникнуть після ходу.
- `+window:setup-choice` — вибір варіанта розстановки перед партією.
- `+card:custodial-capture` · `+card:immobilizer-aura` · `+card:chameleon-capture`.

## Джерела
- ⭐ [Wikipedia: Baroque chess](https://en.wikipedia.org/wiki/Baroque_chess) — розстановка й симетрії, рух, усі способи взяття, хамелеон-спецвипадки, перемога взяттям короля, Abbott 1962 / Ultima 1963, варіанти Maxima, Optima, Renaissance, Rococo.
- [Chess Variant Pages: Immobilizer](https://chessvariants.com/piececlopedia.dir/immobilizer.html) — лінк з черги; відповів 403, не прочитано.
- YouTube — пошук «baroque chess ultima rules».

## Непевне
- (?) Пат і «голий король» — Wikipedia прямо каже, що не розглядає їх для стандартного Baroque.
- (?) Чи може пішак-затискач узяти кілька ворогів за хід (по одному в кожному з 4 напрямків) — логічно з визначення, у статті не сказано явно.
- (?) Хамелеон проти координатора й стрибуна — деталі (напр., хамелеон-координатор бере лише координаторів на перехресті) — переказ узагальненого правила «копіює спосіб жертви».
- (?) Чи паралізує імобілізатор по діагоналі — «adjacent» у статті; 8 сусідів — за загальноприйнятим тлумаченням.
- (?) Цифрові реалізації (онлайн-портали, Ludii, Zillions) — не перевіряв; `platforms: web` — припущення.
- (?) Сторінку Chess Variant Pages (403) не прочитано — тонкощі з неї відсутні.
