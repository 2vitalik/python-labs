---
title: Squadro
slug: squadro
aka: [Сквадро]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 2018
platforms: [board, web]
links:
  - {kind: other, url: "https://export.gigamic.com/wp-content/uploads/2021/01/GIGAMIC_INS-RULES_SQUADRO_07-2018.pdf", best: true, note: "офіційні правила Gigamic (PDF, EN на с. 2): швидкість за крапками біля слота, розворот на краю зі зупинкою, перестрибування й повернення, 4 з 5"}
  - {kind: play, url: "https://ludii.games/details.php?keyword=Squadro", note: "Ludii: коротко правила, Adrián Jiménez Pascual (березень 2015), Gigamic 2018"}
  - {kind: wiki, url: "https://fr.wikipedia.org/wiki/Squadro", note: "FR-вікі: склад, правила, тактичні поради, Grand Prix du Jouet 2019"}
  - {kind: other, url: "https://rulespal.com/squadro/rulebook", note: "текст правил англійською"}
  - {kind: other, url: "https://en.boardgamearena.com/doc/Tips_squadro", note: "BGA: поради до цифрової версії (бачив у результатах пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Squadro+Gigamic+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, online-multiplayer, cell-click, hover-highlight, legal-move-highlight, last-move-highlight, path-preview, movement-animation, goal-counter, remaining-counter, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +crossing-lanes, +lane-speed-by-cell, +round-trip-race, +turnaround-stop, +jump-send-back, +race-quota-win]
proposes: ["+trigger:return_home", "+effect:jump_over", "+cond:returning", "+ui:speed-dots", "+card:crossing-lanes", "+card:lane-speed-by-cell", "+card:round-trip-race", "+card:jump-send-back"]
author: opus
date: 2026-11-09
---

# Squadro — 5 фішок туди й назад через смуги суперника; швидкість дає слот, перескок відкидає ворога на базу

## Суть
У кожного 5 фішок, кожна у своїй смузі; смуги двох гравців перпендикулярні й перетинаються в центрі дошки. Хід — посунути одну фішку рівно на стільки клітин, скільки крапок вигравірувано біля її стартового слота; на протилежному краю вона розвертається і назад іде вже зі швидкістю слота розвороту (швидка туди — повільна назад). Якщо фішка проходить через ворожу (або групу ворожих), вона перестрибує їх і зупиняється одразу за ними, а перестрибнуті повертаються на початок свого відрізка шляху. Перший, хто поверне додому 4 з 5 фішок, виграє.

## Поле і час
- Квадратна сітка: 5 смуг одного гравця × 5 смуг іншого = 5×5 клітин-перетинів, по краях — стартові слоти й слоти розвороту (фізично ~7×7 (?)).
- Біля кожного стартового слота і кожного слота розвороту — крапки (1–3): це швидкість фішки на відповідному відрізку шляху. Приклад із правил: туди 3, назад 1.
- Свої фішки ніколи не зустрічаються (кожна у своїй паралельній смузі); зустрічі — лише з ворожими на перетинах.
- Покроково, двоє; першого гравця визначає жереб. Пасу нема: ходити мусиш (FR-вікі радить іноді «жертвувати» фішку — ілюзія цугцвангу). Партія 15–40 хв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка | piece | ×5 у кожного; напрям (вістря); фаза: туди / назад; швидкість | рухається лише вперед по своїй смузі на `speed` клітин |
| Стартовий слот | zone | крапки 1–3 (швидкість туди) | старт; сюди повертається перестрибнута фішка, що ще не розвернулась; повернення сюди назад = фініш |
| Слот розвороту | zone | крапки 1–3 (швидкість назад) | досягнувши, фішка розвертається і зупиняється; сюди повертається перестрибнута фішка, що вже розвернулась |
| Клітина-перетин | terrain | 25 | у ній може стояти фішка; через ворожу фішку стрибають |
| Смуга | zone | ×5 на гравця | шлях однієї фішки туди й назад |
| Фішки вдома | zone | лічильник 0–5 | фінішовані фішки знято з дошки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «5 фішок кожного на стартових слотах, вістрям до центру»`; перший гравець — `rng`.
- КОЛИ `input(piece)` → ЯКЩО `turn_of(side)` → ТО `move(piece, forward)` × `speed` — уся швидкість, якщо ніщо не зупинить; пас — `block`.
- КОЛИ `reach(piece, far_edge)` → ТО `face(piece, back)`, `speed(piece, dots(turnaround_slot))`, `custom: «рух зупиняється, навіть якщо лишились кроки»`, `end_turn`.
- КОЛИ `contact(piece, enemy)` (кінцева клітина зайнята ворогом або ворог на шляху) → ТО `custom: «перестрибнути всіх ворогів, що стоять поспіль, і стати на першу порожню клітину за ними; рух закінчено, навіть якщо лишились кроки»` (`+effect:jump_over`).
- КОЛИ `after(jump_over)` → ЯКЩО `not custom: «перестрибнута фішка вже розвернулась»` (`+cond:returning`) → ТО `teleport(enemy, start_slot)`.
- КОЛИ `after(jump_over)` → ЯКЩО `returning(enemy)` → ТО `teleport(enemy, turnaround_slot)` — повертається на початок зворотного відрізка, швидкість назад зберігається.
- КОЛИ `reach(piece, start_slot)` → ЯКЩО `returning(piece)` (`+trigger:return_home`) → ТО `disappear(piece)`, `counter(home, +1)` — фішку знято, більше не ходить.
- КОЛИ `counter(home, >=, 4)` → ТО `win`.
- Перемога: першим повернути 4 з 5 фішок · Поразка: суперник зробив це раніше · Рахунок: нема; нічия неможлива (?).

## Керування і ввід
- Настільна: пересунути одну свою фішку по жолобу смуги; розвернути на краю; перестрибнуті ворожі фішки суперник переставляє на базу.
- (цифрова версія) Клік по своїй фішці — хід однозначний (у фішки один напрям і одна швидкість), тож досить одного кліку; наведення показує кінцеву клітину й ворогів, яких буде відкинуто (`path-preview`).
- Не більше 5 варіантів ходу — зручно для мобільного вводу.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати → `match-setup` (людина / AI / онлайн, годинник) · Правила → `help-window` · `settings-window`.
- `game-screen`: дошка з перпендикулярними смугами; `speed-dots` біля кожного слота; вістря-напрям на фішці; `turn-indicator`; `goal-counter` — скільки фішок кожного вже вдома (до 4); `path-preview`; `last-move-highlight` (включно з відкинутими фішками); `movement-animation` перестрибування.
- `end-screen`: хто першим повернув 4 фішки; реванш.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `online-multiplayer` — Board Game Arena (сторінка порад BGA).
- `ai-opponent-levels`: дерево мале (≤5 ходів), minimax глибоко — сильний AI просто.
- `turn-timer` у цифровій версії (?).

## Варіації й родичі
- Автор Adrián Jiménez Pascual (концепт березень 2015), видавець Gigamic 2018; Grand Prix du Jouet 2019 (стратегічна гра) — FR-вікі.
- Перегони з відкиданням суперника на старт: Ludo / «Не сердься» / Sorry! (там випадковість кубика; тут швидкість детермінована клітиною).
- Перпендикулярні шляхи двох сторін: [quoridor](quoridor.md) (перегони до протилежного краю), [breakthrough-loa](breakthrough-loa.md) (дійти до краю), шлях туди й назад — нагадує повернення додому в [halma-chinese-checkers](halma-chinese-checkers.md) лише за метою.
- Клітина керує ходом — споріднено з [kamisado](kamisado.md), де колір клітини диктує, якою фігурою ходити.
- **Осі варіацій**: швидкість (фіксована / від клітини / від кубика) · що робить зустріч (блок / взяття / перескок + відкидання) · куди відкидає (на старт / на початок відрізка) · мета (усі / k з n фішок).

## Цікавинки для курсу
- Дві системи перпендикулярних смуг на одній сітці; фішка = (смуга, позиція, фаза, швидкість) — 🌱.
- Рух на N з перескоком групи ворогів і зупинкою за нею; розворот із зупинкою на краю — 📎.
- Відкидання: на старт або на слот розвороту залежно від фази — 🌱.
- Перемога за квотою 4 з 5 і зняття фінішованих — 🌱.
- AI: alpha-beta з оцінкою «сума лишку шляху / швидкість» — 🥉; аналіз «цугцвангу», коли кожен хід підставляє фішку, — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух на швидкість слота · `hot-seat`, `turn-enforcement`, `move-timer` · `ai-opponent`, `ai-minimax` · `online-multiplayer` ↔ BGA · `cell-click`, `hover-highlight`, `legal-move-highlight`, `last-move-highlight`, `path-preview` ↔ куди прийде фішка, `movement-animation` · `goal-counter` ↔ фішки вдома, `remaining-counter` ↔ скільки ще треба · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+crossing-lanes` «Дві системи перпендикулярних смуг на одному полі» · entities/move · 🌱.
  - `+lane-speed-by-cell` «Швидкість фігури задає слот, з якого вона стартувала / розвернулась» · entities/move · 🌱 · слоти {out: [..], back: [..]}.
  - `+round-trip-race` «Туди й назад: перегони з розворотом на краю» · game-logic/win · 🌱.
  - `+turnaround-stop` «На краю — розворот і зупинка, залишок ходу згорає» · entities/move · 🌱.
  - `+jump-send-back` «Перескок через ворога відкидає його на початок відрізка шляху» · entities/interact · 📎 · слоти {to: start | segment_start}.
  - `+race-quota-win` «Перемога — k з n фігур дійшли» · game-logic/win · 🌱 · слоти {k: 4, n: 5}.

## Пропозиції до словників
- `+trigger:return_home` — фігура повернулась на свій старт після розвороту (Squadro; повернення в домівку в перегонах).
- `+effect:jump_over` — перестрибнути сутність/групу і стати на першу вільну клітину за нею.
- `+cond:returning` — фігура вже розвернулась і йде назад (фаза шляху).
- `+ui:speed-dots` — позначки швидкості біля слотів поля.
- `+card:crossing-lanes`, `+card:lane-speed-by-cell`, `+card:round-trip-race`, `+card:jump-send-back` — див. «Мапа на каталог».

## Джерела
- ⭐ [Gigamic: правила Squadro (PDF)](https://export.gigamic.com/wp-content/uploads/2021/01/GIGAMIC_INS-RULES_SQUADRO_07-2018.pdf) — склад (дошка, 5+5 фішок), рух на число крапок біля слота, повна дистанція «якщо ніщо не заважає», розворот із зупинкою (приклад 3 → 1), перестрибування однієї чи кількох фішок, повернення на старт / слот розвороту, зняття фінішованих, 4 з 5.
- [Ludii: Squadro](https://ludii.games/details.php?keyword=Squadro) — коротке зведення, автор і роки.
- [Wikipedia FR: Squadro](https://fr.wikipedia.org/wiki/Squadro) — правила, тактика (жертва фішки, «ілюзія цугцвангу», фішки зі швидкістю 1 — для атаки), Grand Prix du Jouet 2019.
- [RulesPal: Squadro](https://rulespal.com/squadro/rulebook) — той самий текст правил англійською.
- [BGA: Tips Squadro](https://en.boardgamearena.com/doc/Tips_squadro) — цифрова версія на BGA (сторінку не відкривав, лише в результатах пошуку).

## Непевне
- (?) Точна розкладка швидкостей по смугах — у тексті правил лише приклад «3 туди, 1 назад»; огляди згадують фішки 1 і 3, FR-вікі — «фішки 2 і 3 для захисту». Схоже на 1/3, 3/1, 2/2, 3/1, 1/3 (сума 4), але не бачив діаграми.
- (?) Фізичний розмір дошки (7×7 зі слотами) — не названо.
- (?) Що буває, коли перескок групи ворогів упирається в край (першої порожньої клітини за групою нема в межах смуги).
- (?) Нічия: при обовʼязковому ході й детермінованих правилах зациклення теоретично можливе — правила не кажуть.
- (?) Функції цифрової версії BGA (таймер, рейтинг) — сторінку не відкривав.
