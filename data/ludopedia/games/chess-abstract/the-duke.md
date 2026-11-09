---
title: The Duke
slug: the-duke
aka: [Герцог]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: partial
  random: runtime
  goal: state
year: 2013
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/the-duke/rulebook", best: true, note: "текст правил роздрібного видання: склад (12 видів), розстановка, хід або виставлення з мішка, іконки Move/Jump/Slide/Strike/Command, переворот, Mountain/Fort/Flags, 4 варіанти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Duke_(board_game)", note: "6×6, по 3 плитки на старті, Guard як шах, Holcomb & McLaughlin, Catalyst Game Labs, Mensa Select 2014"}
  - {kind: other, url: "https://web.archive.org/web/20150417015759/http://www.catalystgamelabs.com/download/The%20Duke%20Rulebook%20Lo-Res_FINAL.pdf", note: "PDF правил Kickstarter-видання (24 с.): усі 8 іконок (Jump Slide, Dread, Defense), Enhanced Abilities, Dragon, Dynastic Dispute"}
  - {kind: other, url: "https://cs.uwaterloo.ca/~dtompkin/archive/dtlib/base/The%20Duke.pdf", note: "PDF правил роздрібного видання ©2012 (16 с.): Fort не перестрибнути, Dark Rider на 5 Пікінерів"}
  - {kind: other, url: "https://rulespal.com/duke-lords-legacy/rulebook", note: "Duke: Lords' Legacy — пізніша гра на тому ж ядрі (не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=the+duke+catalyst+game+labs+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, selection-highlight, last-move-highlight, no-move-into-check, impassable-cells, hot-seat, turn-enforcement, ai-opponent, ai-minimax, cell-click, drag-drop-piece, hover-highlight, codex-window, match-setup, rule-variants, game-screen, main-menu, end-screen, help-window, state-as-data, unit-tests, +flip-every-move, +tile-bag-draw, +summon-adjacent, +capture-in-place, +king-capture-win, +command-move, +freeze-aura, +defense-direction, +neutral-monster-turn, +capture-the-flag, +draft-pick, +tile-draft-three-keep-one, +custom-piece-stickers, +move-or-build]
proposes: ["+effect:draw_tile", "+effect:command", "+cond:on_icon", "+ui:flip-preview", "+ui:bag-meter", "+ui:icon-legend", "+card:command-move", "+card:freeze-aura", "+card:defense-direction", "+card:neutral-monster-turn", "+card:custom-piece-stickers", "+card:icon-move-grid"]
author: opus
date: 2026-11-09
---

# The Duke — кожна плитка після ходу перевертається на інший візерунок руху; нові війська тягнеш наосліп із мішка і ставиш поруч із Герцогом

## Суть
Абстрактна дуель Jeremy Holcomb і Stephen McLaughlin (Catalyst Game Labs, 2013) на дошці 6×6. Фігури — деревʼяні плитки з **сіткою руху** на кожному боці: іконки показують, куди плитка може піти, стрибнути, ковзнути, вдарити здалеку чи наказати іншій. Після будь-якої дії плитка перевертається — і наступного разу ходить зовсім інакше. Хід — або дія плиткою, або витягти випадкову плитку з мішка й поставити поруч зі своїм Герцогом; мета — взяти Герцога суперника (є «Guard» — аналог шаху).

## Поле і час
- Дошка 6×6 (36 клітин), один шар; у клітині ≤1 плитка (+ можливо Terrain під нею: Fort, Flag).
- Орієнтація: напис на плитці завжди дивиться на власника — сітка руху відносна до гравця («вперед» = від себе).
- Покроково; ходить першим той, хто першим розставився. Пасу нема.
- Інформація: свій зворотний бік можна дивитись будь-коли, чужий — ні (якщо не домовились); довідка правил (с. 15–16) показує всі плитки. Порядок плиток у мішку — випадковий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герцог (Duke) | piece | 2 боки; стартовий бік | король: узяли — поразка; виставлення нових плиток — лише поруч із ним |
| Піхотинець (Footman) | piece | ×3 (2 на старті + 1 у мішку) | патерн на плитці; ставиться поруч із Герцогом на старті |
| Пікінер (Pikeman) | piece | ×3 | є Strike на звороті (приклад правил) |
| Лицар · Чарівник · Рейнджер · Провидець · Генерал · Священник · Чемпіон · Маршал · Лучник | piece | по ×1 | у кожного свій патерн на обох боках; Провидець у прикладі — 1 по діагоналі або Jump на 2 вперед/вліво/вправо; Лучник — Strike |
| Драгун · Ассасин · Довгий лучник (Kickstarter) | piece | по ×1 | Драгун — Move вперед, Jump вперед-навскіс, Slide назад-навскіс; Ассасин — Jump Slide |
| Герцогиня · Оракул (Enhanced, KS) | piece | подвійна рамка, римська цифра | мають особливі здібності (Summon, Divination…) |
| Мішок | container | плитки гравця | тягнуть наосліп; порожній — більше не виставляєш |
| Mountain | static | 1 шт., випадкова клітина | не увійти, не перестрибнути; блокує Strike по лінії |
| Fort | terrain | 1 шт., випадкова клітина | вхід Move/Slide; одна плитка; Strike по ній не діє; захищає від Dread |
| Flag ×2 | pickup | — | несе плитка, що стала на нього; передається сусідній своїй |
| Dragon (KS) | neutral | 2 боки: спокійний / розлючений | ходить сам між ходами гравців: бʼє, що може; розлютити — штовхнути Slide-ом |

Іконки сітки руху (усі, що описують правила; не всі є в базовій коробці):

| Іконка | Роль | Параметри | Поведінка |
|---|---|---|---|
| Move | mark | клітина сітки | іти туди прямою, якщо шлях вільний; ворог там — взяти; своя — не можна |
| Jump | mark | клітина сітки | стрибнути через будь-що; ворог — взяти |
| Slide | mark | напрям | ковзати на будь-яку кількість клітин до перешкоди; ворог у кінці — взяти |
| Jump Slide | mark | напрям | Slide, що ігнорує сусідню плитку в цьому напрямі (крім Mountain) |
| Strike | mark | клітина | зняти ворога там, не рухаючись |
| Command | mark | ≥2 клітини | пересунути свою плитку з однієї Command-клітини в іншу; сама не рухається |
| Dread | mark | клітини | після ходу будь-яка плитка там замерзає до початку ходу її власника |
| Defense | mark | клітини | ворог не бере цю плитку прямою, що проходить через Defense-клітину |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «Duke на одну з двох центральних клітин свого краю, 2 Footman ортогонально поруч; решта — у мішок»`; усі виставлені плитки — стартовим боком угору.
- КОЛИ `turn_start(side)` → ТО `choose(рух плиткою | нова плитка з мішка | Enhanced Ability)` — рівно одне, пасу нема.
- КОЛИ `input(move, tile, to)` → ЯКЩО `custom: «to позначено Move на поточному боці»` (`+cond:on_icon`) і `free(path)` і `not occupied(to, own_tile)` → ТО `move(tile, to)`; ворог у to — `disappear(enemy)`.
- КОЛИ `input(jump, tile, to)` → ЯКЩО `custom: «to позначено Jump»` і `not occupied(to, own_tile)` → ТО `move(tile, to)` через будь-які плитки; ворог — `disappear(enemy)`.
- КОЛИ `input(slide, tile, dir, n)` → ЯКЩО `custom: «dir має Slide»` і `free(path)` → ТО `slide(tile, dir)` на n клітин; кінцева з ворогом — `disappear(enemy)`; Jump Slide — те саме, але першу клітину в напрямі ігнорує.
- КОЛИ `input(strike, tile, cell)` → ЯКЩО `custom: «cell позначено Strike»` і `occupied(cell, enemy)` → ТО `disappear(enemy)`; плитка лишається на місці.
- КОЛИ `input(command, tile, from, to)` → ЯКЩО `custom: «from і to — Command-клітини tile»` і `occupied(from, own_tile)` і `not occupied(to, own_tile)` → ТО `custom: «пересунути own_tile з from у to»` (`+effect:command`); ворог у to — `disappear(enemy)`; Mountain Command не блокує (лише не можна стати на неї).
- КОЛИ `after(move|jump|slide|strike|command)` → ТО `set_state(tile, other_side)` — переворот навіть після Strike і Command; плитка, яку пересунули Command-ом, не перевертається.
- КОЛИ `input(place)` → ЯКЩО `custom: «мішок не порожній»` і `free(cell_adjacent_to_duke)` → ТО `custom: «витягти випадкову плитку»` (`+effect:draw_tile`), `place(player, tile)` стартовим боком на вільну клітину, що має спільну **сторону** з Герцогом.
- КОЛИ `input(place)` → ЯКЩО `custom: «усі 4 сусіди Герцога зайняті або край»` → ТО `block` — треба ходити плиткою; витягнуту плитку ставити обовʼязково, навіть під удар.
- КОЛИ `input(any_action)` → ЯКЩО `custom: «після дії суперник наступним ходом може взяти мого Герцога»` → ТО `block` (`legal` = не підставляти Герцога).
- КОЛИ `after(any_action)` → ЯКЩО `custom: «тепер я можу взяти Герцога суперника наступним ходом»` → ТО `message("Guard")` — обовʼязкове оголошення.
- КОЛИ `destroyed(duke(B))` → ТО `win` для A.
- Dread: КОЛИ `after(any_action)` → ЯКЩО `custom: «плитка під іконкою Dread»` і `not state(tile, duke|has_dread|in_fort)` → ТО `set_state(tile, frozen)` — не рухається, не бʼється, не командується; КОЛИ `turn_start(owner)` → ЯКЩО `custom: «Dread більше не покриває»` → ТО `clear_state(tile, frozen)`.
- Defense: КОЛИ `input(capture, tile, target)` → ЯКЩО `custom: «пряма до target проходить через Defense-клітину target»` → ТО `block`; Jump і Strike мусять іти прямою, якщо вона є; Command ігнорує Defense.
- Mountain: КОЛИ `input(move|slide|jump, tile, path)` → ЯКЩО `custom: «шлях входить у Mountain або перестрибує її»` → ТО `block`; Strike — `block`, якщо лінія центрів перетинає клітину Mountain (діагональний «кут у кут» — можна).
- Fort: КОЛИ `input(strike, tile, cell)` → ЯКЩО `occupied(cell, fort)` → ТО `block`; увійти — лише Move/Slide/Jump Slide; роздрібне видання: Fort не перестрибнути; KS: перестрибнути можна, стати Jump-ом — ні.
- Flag: КОЛИ `enter(tile, flag)` → ТО `custom: «плитка несе прапор»`; КОЛИ `input(pass_flag, to_tile)` → ЯКЩО `adjacent(holder, to_tile)` (спільна сторона) → ТО `custom: «прапор переходить»`, `end_turn`.
- Dragon (KS): КОЛИ `turn_end(any)` → ЯКЩО `custom: «Дракон може когось взяти»` → ТО `custom: «бере (кілька — випадково), бік і орієнтація не змінюються»`; на краю — лише розвертається.
- Dragon: КОЛИ `input(slide, tile, dragon_cell)` → ТО `push(dragon)` на 1, `set_state(dragon, enraged)`, `choose(орієнтація)`; розлючений наступного проміжного ходу бʼє Strike-ом до 2 плиток, інакше `move(dragon, rng_dir)` з поворотом на 90°; після взяття — `clear_state(dragon, enraged)`.
- Enhanced: Summon — `set_state(duke, other_side)`, `teleport(tile, adjacent_to_duke)`; Divination — `set_state(tile, start_side)`, `custom: «витягти 3, поставити 1, решту — у мішок або знищити»`; Escape — `custom: «пожертвувати сусідню свою»`, `teleport(tile, duke_start_square)`; Ransom — обмін полоненими.
- Перемога: взяти Герцога · Поразка: свій Герцог узятий · Рахунок: нема (крім варіанта Counting Coup).

## Керування і ввід
- Настільна: пересунути плитку й перевернути; витягти з мішка наосліп; оголосити «Guard».
- (цифрова версія) Клік по своїй плитці → підсвітка клітин за іконками поточного боку, різним кольором за типом (рух / стрибок / ковзання / удар / наказ); наведення — `flip-preview` (як ходитиме після перевороту; для своїх плиток).
- Кнопка «Витягти плитку» → підсвітка вільних клітин поруч із Герцогом; Command — два кліки: кого й куди.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати · Варіанти → `match-setup` · Плитки → `codex-window` · Правила → `help-window`.
- `match-setup`: Terrain (Mountain / Fort / Dragon), Enhanced-плитки так/ні, варіант (стандарт / Counting Coup / Trophy Hunters / Dark Rider / Dynastic Dispute), AI або друг.
- `character-select` для Dynastic Dispute: по черзі обрати вид плиток у свій мішок, той самий вид суперника йде в коробку.
- `game-screen`: дошка 6×6; плитки з сіткою поточного боку; `turn-indicator`; `bag-meter` (скільки лишилось у мішку); `captured-pieces`; `selection-highlight`, `legal-move-highlight` з типом іконки, `last-move-highlight`; `toast` «Guard!».
- `codex-window`: усі плитки з обома сторонами (довідка с. 15–16), легенда іконок (`icon-legend`).
- `end-screen`: «Герцога взято», Реванш.
- Переходи: main-menu → match-setup → (character-select) → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: Terrain, Enhanced Abilities, альтернативні цілі.
- Конструктор плиток: чисті плитки + аркуш наліпок з іконками (Customization Tiles) — гравці роблять власні фігури (`+card:custom-piece-stickers`).
- Розширення (Robin Hood, Musketeer, Arthurian Legends — згадані в правилах): нові плитки, Dread/Defense, Escape/Ransom.

## Варіації й родичі
- Counting Coup: прапор кожного на краю; 1 очко за хід, що закінчився поруч із ворожим прапором (по стороні); 3 очки — перемога; Герцог не головний.
- Trophy Hunters / Other Objective: прапор на домашньому краю суперника; принести ворожий прапор на свій край — перемога.
- Dark Rider: 4 (KS) або 5 (роздріб) Пікінерів проти одного Лицаря; Пікінер на краю суперника замерзає; Лицар виграє, взявши 3.
- Dynastic Dispute / Logistical Nightmare: драфт видів плиток у мішок.
- Родичі: [shogi-rule-twists](shogi-rule-twists.md) (Kyoto Shogi — фігура перевертається після кожного ходу) · [onitama](onitama.md) (патерн ходу з карти, що міняється) · [ploy](ploy.md) (напрямки на фігурі) · [chess](chess.md) (Guard ≈ шах) · [banqi](banqi.md) (випадковість того, що виходить на дошку).
- **Осі варіацій**: де записано патерн (вид фігури / сам предмет — The Duke) · коли патерн міняється (ніколи / після кожного ходу / за карткою) · як фігура входить на дошку (уся на старті / з мішка наосліп / з руки) · дія без руху (Strike, Command — так / ні).

## Цікавинки для курсу
- Сітка руху як дані: 5×5 (і більше) матриця іконок на кожен бік, генератор ходів читає матрицю — 📎; дзеркалення для другого гравця — 🌱.
- Вісім типів іконок з різною логікою шляху (пряма, стрибок, ковзання, ковзання з пропуском, удар здалеку, наказ) — 🥉.
- Переворот після кожної дії (крім плитки, переміщеної Command-ом) — 🌱.
- Мішок + виставлення поруч із Герцогом + «треба поставити навіть під удар» — 📎.
- Легальність «не підставляй Герцога» = перевірка всіх відповідей суперника — 🥇 (як `no-move-into-check`).
- Dread (заморозка аурою) і Defense (захист з напрямку) — 🥉 кожна.
- Дракон: нейтральна сутність з власним «проміжним» ходом і випадковим вибором — 🥈.
- Редактор плиток із наліпок-іконок — 🥈 (дані + рендер сітки).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ сітки іконок · `piece-capture` · `legal-move-highlight`, `selection-highlight`, `last-move-highlight`, `hover-highlight` · `no-move-into-check` ↔ не підставляти Герцога · `impassable-cells` ↔ Mountain · `hot-seat`, `turn-enforcement` · `ai-opponent`, `ai-minimax` · `cell-click`, `drag-drop-piece` · `codex-window` ↔ довідка плиток · `match-setup`, `rule-variants` · `game-screen`, `main-menu`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- Наявні пропозиції корпусу: `+flip-every-move` (див. [shogi-rule-twists](shogi-rule-twists.md), там уже названо The Duke) · `+tile-bag-draw` · `+summon-adjacent` (тут — лише поруч із Герцогом) · `+capture-in-place` (Strike) · `+king-capture-win` · `+capture-the-flag` (Trophy Hunters) · `+draft-pick` (Dynastic Dispute) · `+tile-draft-three-keep-one` (Divination) · `+move-or-build` (хід: дія або виставлення).
- **Нема** → пропозиції карток:
  - `+icon-move-grid` «Патерн ходу як сітка іконок на самій фігурі» · entities/legality · 📎 · слоти {icons: [move, jump, slide, jump_slide, strike, command], size: 5×5}.
  - `+command-move` «Фігура пересуває свою сусідню між позначеними клітинами» · entities/legality · 📎.
  - `+freeze-aura` «Клітини навколо фігури заморожують будь-кого до ходу власника» · entities/state · 🥉 · слоти {immune: [duke, same_aura]}.
  - `+defense-direction` «Фігуру не взяти з позначених напрямків» · entities/combat · 🥉.
  - `+neutral-monster-turn` «Нейтральна фігура ходить сама між ходами гравців» · game-logic/opponent · 🥈 · слоти {states: [calm, enraged], target: random}.
  - `+custom-piece-stickers` «Конструктор власних фігур з наліпок-іконок» · levels/editor · 🥈.

## Пропозиції до словників
- `+effect:draw_tile` — підтверджую (isle-of-skye): витягти N плиток з мішка.
- `+effect:command` — підтверджую (hover-bovver, exit-taito): тут наказ пересунути свою плитку між Command-клітинами.
- `+cond:on_icon(cell, icon)` — клітина позначена іконкою певного типу на поточному боці фігури.
- `+ui:flip-preview` — підтверджую (shogi-rule-twists): що буде на звороті після ходу.
- `+ui:bag-meter` — підтверджую (dynamine): скільки плиток лишилось у мішку.
- `+ui:icon-legend` — легенда типів іконок сітки руху.
- `+card:command-move`, `+card:freeze-aura`, `+card:defense-direction`, `+card:neutral-monster-turn`, `+card:custom-piece-stickers`, `+card:icon-move-grid` — див. «Мапа на каталог».

## Джерела
- ⭐ [RulesPal: The Duke rulebook](https://rulespal.com/the-duke/rulebook) — склад роздрібного видання, розстановка, «рух або нова плитка», 5 іконок, переворот, безпека Герцога, Mountain/Fort/Flags, Counting Coup, Other Objective, Dark Rider, Logistical Nightmare.
- [Wikipedia: The Duke](https://en.wikipedia.org/wiki/The_Duke_(board_game)) — 6×6, по 3 плитки на старті, Guard ≈ шах, terrain і чисті плитки, автори, Catalyst, нагороди.
- [PDF правил Kickstarter-видання (архів)](https://web.archive.org/web/20150417015759/http://www.catalystgamelabs.com/download/The%20Duke%20Rulebook%20Lo-Res_FINAL.pdf) — 8 іконок з Jump Slide, Dread, Defense; приклад ходів Провидця/Драгуна/Ассасина; Enhanced Abilities (Summon, Divination, Escape, Ransom); Dragon; Trophy Hunters, Dark Rider, Dynastic Dispute; Customization Tiles.
- [PDF правил роздрібного видання](https://cs.uwaterloo.ca/~dtompkin/archive/dtlib/base/The%20Duke.pdf) — ©2012; 12 видів, Mountain/Fort/2 Flags; Fort не перестрибнути; Dark Rider на 5 Пікінерів.
- YouTube: пошук «the duke catalyst game labs how to play».

## Непевне
- (?) Точні сітки руху кожної плитки (обидва боки) — лише на картинках правил (с. 15–16), текстом не бачив; у таблиці — тільки приклади з тексту правил.
- (?) Що буде, якщо в гравця нема жодної легальної дії (усі ходи підставляють Герцога, мішок порожній чи Герцог оточений) — правила не кажуть; ймовірно, це поразка, як мат.
- (?) Склад розходиться між виданнями: KS — +Dragoon, Assassin, Longbowman, Duchess, Oracle і Dragon замість Fort; роздріб — 12 видів, Fort. Записано обидва.
- (?) Цифрові версії (застосунок, онлайн) — не перевірено; вікна описано як «(цифрова версія)».
