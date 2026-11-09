---
title: Below the Crown
slug: below-the-crown
aka: []
family: chess-abstract
also: [roguelike, tactics]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2026
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1883920/Below_the_Crown/", best: true, note: "«1 фігура замість 16», виклик фігур на дошку, Undo Tokens або золото, боси, нескінченний і випадковий режими, щоденні челенджі, повтори"}
  - {kind: official, url: "https://misfitsattic.com/below-the-crown/", note: "старт з Турою й Лучником, редактор кімнат, психологічні тести, Discord і сабреддіт"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/below-the-crown-review/", note: "огляд: хід = рух + виклик фігури в полі зору Короля, мат ворожому королю, глухий кут = провал кімнати"}
  - {kind: other, url: "https://aftermath.site/chess-dungeon-crawler-yeah/", note: "фігури з карт, стіни й пастки, обгортання краю, двері до наступної кімнати, обмежене undo, підказка, небезпечні клітини"}
  - {kind: other, url: "https://gamesbeat.com/below-the-crown-is-a-dungeon-crawling-chess-roguelite/", note: "інтервʼю: виклик «де бачиш», лучниця-ферзь, Dark Square, Mad Queen, іменовані фігури з апгрейдами"}
  - {kind: other, url: "https://turnbasedlovers.com/?p=60433", note: "анонс EA: руни підвищують складність за кращі нагороди, заморожування й вибухи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Below+the+Crown+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [piece-move-patterns, piece-capture, piece-drop, checkmate, check-stalemate, no-moves-left, reach-exit, impassable-cells, wrap-edges, legal-move-highlight, threat-range, undo-redo, undo-step, dungeon-generation, run-relics, daily-puzzle, leaderboard, replay, replay-window, in-game-editor, level-exchange, difficulty-levels, character-select, game-screen, +deck-draw, +summon-in-sight, +undo-tokens, +hint-best-move, +ranged-capture, +uncapturable-piece, +piece-level-up, +transform-piece, +freeze-spell, +risk-runes, +boss-fight, +posted-challenges, +psych-questionnaire]
proposes: ["+trigger:cast", "+cond:in_sight", "+feature:undo-tokens", "+feature:posted-challenge", "+window:psych-test"]
author: opus
date: 2026-11-09
---

# Below the Crown — шаховий данж-кроулер: заходиш однією фігурою, решту армії «викликаєш» на дошку посеред кімнати

## Суть
Чарівник спускається в процедурне підземелля по золото для Імператора. Кожна кімната — шахова дошка з ворожими фігурами; гравець починає **з однієї фігури замість шістнадцяти** і щоходу додає нові, **викликаючи їх на клітини в полі зору** свого лідера. Фігури ходять за шаховими правилами; ціль кімнати — мат ворожому королю або вихід лідера до дверей. Роглайт-шар: апгрейди й іменовані фігури, заклинання (заморожування, телепорт, вибухи), руни ризику, Undo Tokens як валюта поряд із золотом.

## Поле і час
- Квадратна дошка-кімната зі **стінами й пастками**; кімнати генеруються процедурно, глибше — небезпечніше й щедріше (GamesBeat).
- Хід гравця (GameGrin): **рух однією фігурою, потім виклик нової** — у межах ліміту фігур на кімнату; далі ходить ворог.
- Ворожі фігури ходять «просто» (за шаховими патернами), доки не зустрінеш босів зі складнішою поведінкою (Steam).
- Інформація повна: гра може показати небезпечні клітини (Aftermath).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник / Король | player | патерн ходу, заклинання | лідер у кімнаті; викликає фігури туди, «де бачить»; має дійти до дверей або вижити до мату (джерела розходяться в назві: wizard vs King) |
| Тура | piece | шаховий патерн | стартова фігура (офіційна сторінка) |
| Лучник / лучниця-ферзь | piece | патерн ферзя, атака на відстані | бʼє з дистанції, не стаючи на клітину цілі (GamesBeat) |
| Пішак, Слон, Кінь | piece | шахові патерни | викликаються з карт; правила як у шахах |
| Dark Square | piece | невразлива | ставиться на дошку, її не можна взяти — «сильно змінює гру» |
| Ворожі фігури | enemy | шахові патерни | беруть і блокують фігури гравця |
| Ворожий король | enemy | — | мат або шах — шлях до перемоги в кімнаті |
| Mad Queen | boss | — | бос: зникає, якщо нікого не атакує |
| Фінальний бос | boss | — | додано у версії 1.0 |
| Стіна | static | — | непрохідна клітина, блокує лінії ходу |
| Пастка / небезпека | hazard | — | клітина з ефектом (?) |
| Двері | static | — | вихід у наступну кімнату для лідера |
| Undo Token | pickup | — | дає один відкат ходу; альтернатива золоту |
| Золото | resource | — | для апгрейдів у підземеллі або «для Імператора» |
| Руна | pickup | — | підвищує складність в обмін на кращі нагороди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `spawn_at(leader, custom: «вхід кімнати»)`; на полі — ворожі фігури за генерацією.
- КОЛИ `input(move, piece, to)` → ЯКЩО `legal(pattern)` і `free(to)` → ТО `move(piece, to)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, enemy)` і `legal(pattern)` → ТО `disappear(enemy)` — взяття.
- КОЛИ `input(attack, archer, target)` → ЯКЩО `line_of_sight(archer, target)` і `legal(queen_pattern)` → ТО `disappear(target)`, лучниця лишається на місці.
- КОЛИ `input(cast, card, cell)` → ЯКЩО `free(cell)` і `line_of_sight(leader, cell)` і `counter(summons, <, limit)` → ТО `place(leader, piece)`, `custom: «карта йде у скид»` (?).
- КОЛИ `input(cast, spell, target)` → ТО `freeze(enemy, 1)` (?) / `teleport(leader, where)` / `explode(shape, n)` / `transform(piece, bishop)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, dark_square)` → ТО `block` — Dark Square не береться.
- КОЛИ `edge(piece)` → ЯКЩО `state(piece, wrap_upgrade)` → ТО `wrap(piece)`.
- КОЛИ `turn_start(enemy)` → ТО `move(enemy, to)` за патерном; ЯКЩО `occupied(to, piece)` → ТО `disappear(piece)`.
- КОЛИ `turn_end(enemy)` → ЯКЩО `state(mad_queen, not_attacking)` → ТО `disappear(mad_queen)` (?) — зникає з дошки.
- КОЛИ `no_moves(enemy_king)` → ЯКЩО `in_check(enemy_king)` → ТО `win` (мат — кімната пройдена).
- КОЛИ `reach(leader, door)` → ТО `next_level`.
- КОЛИ `no_moves(player)` → ТО `lose` кімнати: вихід без бонусів, скарбу й апгрейдів; рестарту кімнати нема (GameGrin).
- КОЛИ `input(undo)` → ЯКЩО `counter(undo_tokens, >=, 1)` → ТО `undo(1)`, `counter(undo_tokens, -1)`.
- КОЛИ `picked(leader, undo_token)` → ТО `counter(undo_tokens, +1)`; ЯКЩО `custom: «вибрано золото»` → ТО `currency(+n)`.
- КОЛИ `picked(leader, rune)` → ТО `custom: «складність +1, нагороди кращі»`.
- КОЛИ `level_end` → ТО `window(upgrade-window)` → `choose(«апгрейд фігури» | «заклинання» | «уміння»)`.
- КОЛИ `custom: «між кімнатами»` → ТО `window(psych-test)` — запитання про стан чарівника й стосунки з фігурами.
- Перемога: мат / шах королю або вихід у двері; пройти підземелля · Поразка: глухий кут без легальних ходів · Рахунок: золото для Імператора (?) і таблиці лідерів.

## Керування і ввід
- Лише миша (Steam: Mouse Only Option, Playable without Timed Input): клік по фігурі → клік по клітині; карта фігури/заклинання → клітина.
- Допомога: обмежене undo, «підказка найкращого ходу», показ небезпечних клітин (Aftermath).
- Збереження будь-коли (Steam: Save Anytime).

## Вікна, меню, HUD
- `main-menu`: забіг · `mode-select` (Infinite / Random Dungeon / Daily Challenge) · `editor-window` (редактор кімнат) · `replay-window` · `leaderboard` · `settings-window`.
- `character-select` — кілька чарівників з різними здібностями.
- `game-screen`: дошка; `pocket` — рука карт фігур і заклинань; лічильник Undo Tokens; золото (`coins`); `legal-move-highlight`; `threat-range` / небезпечні клітини; `hint-marker`; ліміт викликів (`remaining-counter`).
- `upgrade-window` — апгрейди фігур, нові заклинання й уміння.
- `custom-window` → `psych-test` — психологічні запитання («ваші відповіді не буде використано проти вас»).
- `end-screen` — результат забігу; публікація перемоги як челенджу.

## Фічі поза полем
- Роглайт-забіг з процедурними кімнатами; руни ризику; апгрейди; іменовані фігури, що несуть апгрейди далі (GamesBeat).
- Режими: Infinite, Random Dungeon, `mode-daily` (Daily Challenges).
- Спільнота: опублікувати перемогу як челендж іншим; `replay` топ-гравців; `leaderboard-online`.
- `level-editor` — редактор кімнат, завантаження чужих кімнат (`level-sharing`).
- `undo` як колекційний ресурс; `hint`; адаптивна складність (Steam: Adjustable Difficulty); `colorblind-palette` (Color Alternatives); `cloud-save`.

## Варіації й родичі
- Шахові роглайки корпусу: [shotgun-king](shotgun-king.md) (один король проти армії), [ouroboros-king](ouroboros-king.md) (армія фігур і реліквії), [passant](passant.md) (модифікатори правил), [chess-survivors](chess-survivors.md), [pawnbarian](../roguelike/pawnbarian.md) (герой ходить картами-фігурами).
- Дроп фігур з руки: [shogi](shogi.md), [bughouse](bughouse.md); шахові правила: [chess](chess.md).
- **Осі варіацій**: армія — повна зі старту / драфт / **виклик посеред бою** · мета кімнати — мат / взяття короля / вихід у двері · undo — без ліміту / токени як ресурс / нема.

## Цікавинки для курсу
- Виклик фігури лише на клітину в полі зору лідера (лінії ферзя до перешкод) — 🥉.
- Лучниця-ферзь: взяття на відстані без руху — 🌱 поверх `piece-capture`.
- Undo Tokens як валюта, що конкурує із золотом — 📎.
- Показ небезпечних клітин і «підказка найкращого ходу» (minimax на малій дошці) — 🥇.
- Невразлива фігура Dark Square і бос, що зникає без атаки — 🌱 кожна.
- Опублікувати свою перемогу як челендж (той самий seed іншим гравцям) — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `piece-drop` ↔ виклик фігури з руки · `checkmate` · `check-stalemate` · `no-moves-left` ↔ глухий кут · `reach-exit` ↔ двері · `impassable-cells` ↔ стіни · `wrap-edges` ↔ апгрейд обгортання · `legal-move-highlight` · `threat-range` ↔ небезпечні клітини · `undo-redo` / `undo-step` · `dungeon-generation` · `run-relics` ↔ руни й уміння · `daily-puzzle` · `leaderboard` · `replay` / `replay-window` · `in-game-editor` · `level-exchange` · `difficulty-levels` · `character-select` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+deck-draw` «Рука карт фігур і заклинань» · entities/state · 🥉.
  - `+summon-in-sight` «Виклик фігури лише в полі зору лідера» · entities/legality · 🥉.
  - `+undo-tokens` «Undo як колекційний ресурс» · game-logic/history · 📎.
  - `+hint-best-move` «Підказка найкращого ходу» · game-logic/opponent · 🥇.
  - `+ranged-capture` «Взяття на відстані без переміщення» · entities/combat · 🌱.
  - `+uncapturable-piece` «Фігура, яку не можна взяти» · entities/legality · 🌱.
  - `+piece-level-up` «Іменована фігура з апгрейдами між кімнатами» · entities/state · 📎.
  - `+transform-piece` «Заклинання змінює тип фігури» · entities/state · 🌱.
  - `+freeze-spell` «Заморозити ворожу фігуру на хід» · entities/state · 🌱.
  - `+risk-runes` «Руни: складність ↑ — нагорода ↑» · game-logic/difficulty · 📎.
  - `+boss-fight` «Бос із власною поведінкою» · game-logic/waves · 🥉.
  - `+posted-challenges` «Перемога як челендж для інших» · interface/results · 🥈.
  - `+psych-questionnaire` «Запитання гравцю між рівнями як частина сюжету» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:cast` — гравець зіграв карту фігури/заклинання (відмінне від руху).
- `+cond:in_sight` — клітина в полі зору лідера (лінії без перешкод); узагальнення `line_of_sight` на клітину.
- `+feature:undo-tokens` — undo як предмет, що збирається в забігу.
- `+feature:posted-challenge` — опублікувати свою перемогу як завдання для інших.
- `+window:psych-test` — анкета/психологічний тест між рівнями.

## Джерела
- ⭐ [Steam](https://store.steampowered.com/app/1883920/Below_the_Crown/) — 1 фігура замість 16, виклик фігур, заклинання й вибухи, Undo Tokens або золото, боси, Infinite/Random/Daily, челенджі й повтори; EA 10.11.2025, реліз 21.04.2026; Misfits Attic, видавці Misfits Attic і Shochiku.
- [Офіційна сторінка](https://misfitsattic.com/below-the-crown/) — старт з Турою й Лучником, редактор кімнат, психологічні тести.
- [GameGrin, огляд](https://www.gamegrin.com/reviews/below-the-crown-review/) — рух + виклик у полі зору Короля, ліміт викликів, мат, провал без рестарту кімнати.
- [Aftermath](https://aftermath.site/chess-dungeon-crawler-yeah/) — карти фігур, стіни й пастки, обгортання краю, двері, undo, підказка, небезпечні клітини.
- [GamesBeat](https://gamesbeat.com/below-the-crown-is-a-dungeon-crawling-chess-roguelite/) — виклик «де бачиш», лучниця-ферзь, Dark Square, Mad Queen, руни й іменовані фігури.
- [Turn Based Lovers](https://turnbasedlovers.com/?p=60433) — руни ризику, заморожування, вибухи, кастомні дошки.
- YouTube: пошук «Below the Crown gameplay».

## Непевне
- (?) Лідер — «чарівник» (Steam, GamesBeat) чи «Король» (GameGrin); як саме він ходить і чи гине партія з його взяттям.
- (?) Ціль кімнати: мат ворожому королю (GameGrin) vs довести свого лідера до дверей (Aftermath) — можливо, різні типи кімнат.
- (?) Як працюють пастки, звідки береться рука карт і ліміт викликів; чи є мана.
- (?) Поведінка Mad Queen («зникає, якщо не атакує») — з інтервʼю, деталі не перевірено; решта босів невідома.
- (?) Сімʼя: у черзі — `tactics`, покладено в `chess-abstract` за прецедентом шахових роглайків корпусу.
