---
title: Quantum Chess (Квантові шахи, Cantwell)
slug: quantum-chess
aka: [Квантові шахи, QC, Quantum Chess Remastered]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: runtime
  goal: state
year: 2016
platforms: [PC, web, mobile]
links:
  - {kind: other, url: "https://ar5iv.labs.arxiv.org/html/1906.05836", best: true, note: "Cantwell, «Quantum Chess: Developing a Mathematical Framework and Design Methodology» — повні правила: split/merge, вимірювання, пішаки, рокіровка, перемога"}
  - {kind: other, url: "https://arxiv.org/abs/1906.05836", note: "та сама стаття, сторінка arXiv"}
  - {kind: steam, url: "https://store.steampowered.com/app/453870/Quantum_Chess/", note: "Quantum Realm Games: режими, Quantum Lab, Alchemy League, Universal QC, кільця ймовірності"}
  - {kind: play, url: "https://chess.quantumnative.io/", note: "браузерна версія (quantumchess.net перенаправляє сюди)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quantum+chess+anyone+can+quantum", note: "пошук; відео IQIM «Anyone Can Quantum» (згадане в подяках статті)"}
stage: v1
coverage: 45
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, pawn-promotion, drag-drop-piece, cell-click, ai-opponent, online-multiplayer, async-multiplayer, hot-seat, move-timer, rating-system, undo-redo, in-game-editor, tutorial-window, achievements-window, level-bank, game-screen, end-screen, state-as-data, +superposition-move, +measurement-collapse, +king-capture-win, +castling, +en-passant, +probability-ring, +branching-sandbox, +seasonal-rules-ladder]
proposes: ["+effect:measure", "+effect:entangle", "+cond:superposed", "+cond:path_blocked_prob", "+trigger:measured", "+ui:probability-ring", "+ui:phase-dial", "+ui:split-slider", "+window:quantum-lab", "+feature:seasonal-rules", "+axis:random", "+card:superposition-move", "+card:measurement-collapse"]
author: opus
date: 2026-11-09
---

# Quantum Chess — фігура може стояти у двох клітинах одразу, а взяття «вимірює» дошку

## Суть
Шахи, де стан дошки — квантова суперпозиція: кожна клітина має ймовірність бути зайнятою. Окрім звичайних ходів, фігура може **розщепитися** у дві клітини (split), дві половинки — **злитися** назад (merge), а хід крізь клітину в суперпозиції заплутує (entangle) фігури. Коли хід може поставити дві різні фігури в одну клітину (взяття, блок), гра **вимірює** дошку й випадково вирішує, де фігура насправді. Шаху нема — мета взяти короля так, щоб у суперника лишилась нульова ймовірність мати короля. Тут цей варіант описано окремо від короткого рядка в [chess-rule-twists.md](chess-rule-twists.md): повні правила Cantwell і цифрова гра Quantum Realm Games.

## Поле і час
- Дошка 8×8, стандартна розстановка й черга ходу.
- Стан — суперпозиція над 64 кубітами (кубіт на клітину) + класичний вектор «тип фігури в клітині» + класичні прапори: хто ходить, права рокіровки, файл en passant.
- Клітина «зайнята», якщо ймовірність фігури в ній ненульова.
- **Заборона подвійного заповнення**: клітина ніколи не може з ненульовою ймовірністю містити дві **різні** фігури; однакові фігури (той самий тип і колір) можуть ділити клітину.
- Випадковість — лише у вимірюваннях (два результати: 1 — хід застосовано, 0 — дошка лишається як була).
- Дизайн-ціль Cantwell: правила тримають суперпозицію малою, щоб гру можна було симулювати на класичному компʼютері, і квантові ефекти (інтерференція через комплексні амплітуди) лишались значущими, а не просто «кубиком».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | амплітуди по клітинах | стрибок на 1; split/merge-стрибок; шаху нема — може стати під бій і рокіруватись через биті поля |
| Кінь | piece | амплітуди | стрибок; split/merge-стрибок (рівні амплітуди i/√2 у двох цілях) |
| Слон, тура, ферзь | piece | амплітуди + кубіт шляху | ковзання: шлях вільний → хід, заблокований → фігура лишається (у тій гілці); split/merge-ковзання |
| Пішак | piece | амплітуди | крок на порожню клітину або до свого пішака; подвійний крок зі старту; бʼє навскоси (ціль може бути в суперпозиції); вперед не бʼє; не розщеплюється (?) |
| Половинка фігури | piece | частка ймовірності (кільце) | ходить, загрожує й блокує як ціла фігура; зливається з іншою половинкою того самого типу |
| Клітина в суперпозиції | zone | ймовірність зайнятості | ковзання крізь неї заплутує фігуру, що ковзає, з фігурою в ній |
| Взята фігура (ancilla) | — | допоміжний кубіт | «кишеня», куди переходить амплітуда взятої фігури |

## Правила (КОЛИ → ЯКЩО → ТО)
Невимірювальні ходи:
- КОЛИ `input(move(p, to))` → ЯКЩО `free(to)` or `same(p, occupant, type)` and `custom: «p — кінь або король»` → ТО `move(p, to)` (Standard Jump: повний обмін зайнятості).
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «p — слон/тура/ферзь»` → ТО `custom: «Standard Slide: керовано кубітом шляху — у гілках з вільним шляхом фігура переходить, з заблокованим — лишається»`; якщо шлях частково в суперпозиції — `custom: «фігури заплутуються»`.
- КОЛИ `input(split(p, a, b))` → ЯКЩО `free(a)` or `same(p, a)` and `free(b)` or `same(p, b)` → ТО `split(p)` у `a` і `b` з рівними амплітудами; кількість фігур зберігається.
- КОЛИ `input(split_slide(p, a, b))` → ТО `split(p)`; `custom: «кожен маршрут перевіряється на блок; заблокований маршрут у своїй гілці не відбувається»`.
- КОЛИ `input(merge(p@a, p@b, to))` → ЯКЩО `same(p@a, p@b, type)` and (`free(to)` or `same(to, p)`) → ТО `merge(p@a, p@b → to)`.
- Хід легальний, лише якщо його умови виконані **і** він змінює суперпозицію зайнятості (порожній хід заборонено).

Вимірювальні ходи (захист від подвійного заповнення):
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «p — кінь/король»` and `occupied(to, other_type)` and `custom: «to у суперпозиції»` → ТО `custom: «measure(to)»`: `prob(empty)` → `move(p, to)`; інакше `block` (Blocked Jump).
- КОЛИ `input(capture(p, to))` → ЯКЩО `custom: «p — кінь/король»` and `occupied(to, enemy)` → ТО `custom: «measure(source)»`: p справді в джерелі → `disappear_b` (амплітуда — в ancilla), `move(p, to)`; інакше хід не відбувся (Capture Jump).
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «p ковзає, ціль зайнята іншою фігурою в суперпозиції»` → ТО `custom: «measure(to, path)»` → хід або `block` (Blocked Slide).
- КОЛИ `input(capture(p, to))` → ЯКЩО `custom: «p ковзає на ворожу фігуру»` → ТО `custom: «measure(path, source, target)»`: взяття, якщо шлях вільний і джерело зайняте, або шлях заблокований і ціль порожня (Capture Slide).
- КОЛИ `input(pawn_capture(to))` → ТО `custom: «кероване взяття: діє лише в гілках, де присутні і пішак, і ціль»`.
- КОЛИ `input(pawn_step)` → ЯКЩО `custom: «ціль або шлях подвійного кроку в суперпозиції з іншою фігурою»` → ТО `custom: «measure як Blocked Jump/Slide»`; подвійний крок крізь клітину в суперпозиції заплутує пішака.
- En passant: три випадки (звичайний; блокований своєю фігурою в суперпозиції; взяття ворожої фігури в суперпозиції); прапор en passant ставиться, лише якщо вимірювання подвійного кроку дало 1.
- КОЛИ `input(castle)` → ЯКЩО `custom: «король і тура ще не брали участі в жодному ході, навіть такому, що лишив їх на місці в одній з гілок»` → ТО `custom: «класична рокіровка з вимірюванням проти подвійного заповнення»`; split/merge з рокіровкою заборонені.
- КОЛИ `reach(pawn, last_rank)` → ТО `transform(choice)` (нотація `a7a8Q`).

Кінець партії:
- Шаху й мату нема; король береться як будь-яка фігура.
- КОЛИ `after(move)` → ЯКЩО `custom: «у суперника нульова ймовірність мати короля на дошці»` → ТО `win`.
- КОЛИ `after(move)` → ЯКЩО `custom: «в обох сторін одночасно нульова ймовірність короля»` → ТО `draw`.
- Перемога: король суперника «зник з усіх гілок» · Нічия: обидва королі зникли одночасно.

## Керування і ввід
- Звичайний хід — drag/клік як у шахах.
- Split: обрати фігуру і дві цілі (режим розщеплення); merge: обрати дві половинки й ціль.
- Universal QC (Premium): `phase-dial` — фаза розщеплення під будь-яким кутом і `split-slider` — нерівні частки (приклад Steam: 79 % / 21 %).
- Alchemy League: merge прибрано, натомість фазовий диск змушує половинки інтерферувати й визначає, де опиниться фігура.
- Takeback-запити онлайн; undo і гілкування ходів у Quantum Lab.

## Вікна, меню, HUD
- `main-menu`: Learn (tutorial + гайди) → `tutorial-window`; Puzzles → `puzzle-select`; vs AI → `match-setup`; Pass-and-play → `match-setup`; Online (ranked/casual, live/correspondence, турніри) → `lobby-window`; Quantum Lab → `quantum-lab`.
- `game-screen`: дошка з `probability-ring` на кожній половинці (скільки фігури в ній), `legal-move-highlight`, `player-clock`, `turn-indicator`, `captured-pieces`; для Alchemy — `phase-dial`.
- `quantum-lab` — пісочниця: розставити позицію, грати проти AI або себе, undo й гілкування ходів, Universal QC.
- `achievements-window` (Steam), `editor-window` (редактор рівнів), `end-screen` (король узятий / нічия), `stats-window`/рейтинг (?).
- Переходи: main-menu → lobby/match-setup → game-screen → end-screen; main-menu → quantum-lab.

## Фічі поза полем
- `tutorial` + in-app guides; `puzzle-bank`.
- `ai-opponent-levels` — до «Aqaqaq», квантового рушія розробників; ranked-гравцям під час очікування підбирають бота близького рейтингу.
- `online-multiplayer`: ranked і casual, live і кореспонденція, турніри (Swiss, round robin, knockout, arena), кросплей з браузером; `spectator` з годинниками; turn notifications.
- `hotseat` — pass-and-play без акаунта; `mode-sandbox` — Quantum Lab.
- `seasonal-rules` — Alchemy League: безкоштовна сезонна драбина зі змінними правилами.
- `level-editor`, `achievements`, `theme-select` (Cloud Chamber), takeback-запити.

## Варіації й родичі
- Короткий запис цього варіанта — у [chess-rule-twists.md](chess-rule-twists.md); там же Kriegspiel/Dark (невизначеність через приховування, а не через суперпозицію).
- Selim Akl, «Quantum Chess» (Queen's University; ідея з 2010 р.) — інша версія: квантова непередбачуваність, щоб люди й компʼютери мали рівні труднощі.
- Режими самої гри: класичні правила Cantwell · Alchemy League (без merge, фазова інтерференція) · Universal QC (довільна фаза й нерівний split).
- [5d-chess.md](5d-chess.md) — інший спосіб «множити» позицію: гілки часу замість суперпозиції; [lichess-variants.md](lichess-variants.md) — Atomic, Antichess (взяття короля як мета).
- Cantwell пропонує той самий підхід для шашок і реверсі ([checkers.md](checkers.md), [reversi.md](reversi.md)).
- **Осі варіацій**: де стоїть фігура (одна клітина · кілька з ймовірністю) · хто вирішує колапс (вимірювання при конфлікті · завжди при взятті) · частки split (рівні · довільні) · фаза (без · фіксована · довільна) · мета (мат · взяття короля з імовірністю 0).

## Цікавинки для курсу
- Класична спрощена модель: фігура = словник «клітина → ймовірність», split ділить навпіл, merge складає — 🥉.
- Вимірювання при конфлікті (взяття/блок) з `rng` і колапсом пов'язаних половинок — 🥈.
- Заплутування через ковзання крізь суперпозицію (корельовані гілки, а не незалежні ймовірності) — 🥇: потрібне представлення станів як множини світів.
- Повна модель: вектор амплітуд на 64 кубітах, комплексна інтерференція (унітарні з множником i) — 👑.
- Правило «легальний лише хід, що змінює суперпозицію» + заборона подвійного заповнення — 🥈.
- `probability-ring` і фазовий диск як UI для невидимого стану — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` (з вимірюванням) · `legal-move-highlight` · `pawn-promotion` · `drag-drop-piece` · `cell-click` · `ai-opponent` ↔ рушій Aqaqaq · `online-multiplayer` · `async-multiplayer` ↔ кореспонденція · `hot-seat` ↔ pass-and-play · `move-timer` · `rating-system` ↔ ranked · `undo-redo` ↔ Quantum Lab · `in-game-editor` ↔ редактор рівнів · `tutorial-window` · `achievements-window` · `level-bank` ↔ пазли · `game-screen` · `end-screen` · `state-as-data` ↔ стан як вектор.
- **Нема** → пропозиції карток:
  - `+superposition-move` (є в chess-rule-twists) — підтверджую; слоти {split: equal|weighted, merge: on|off}.
  - `+measurement-collapse` «Вимірювання при конфлікті клітини, колапс гілок» · entities/state · 🥇.
  - `+king-capture-win` — підтверджую (з chess-rule-twists).
  - `+castling` / `+en-passant` — підтверджую (з chess.md), тут з вимірюванням.
  - `+probability-ring` «Індикатор частки фігури» · interface/render · 📎.
  - `+branching-sandbox` «Пісочниця з undo-деревом ходів» · game-logic/history · 🥈.
  - `+seasonal-rules-ladder` «Сезонна драбина зі змінними правилами» · interface/results · 🥉.

## Пропозиції до словників
- `+effect:measure(cells)` — вимірювання з двома результатами, колапс суперпозиції (у chess-rule-twists — теж; підтверджую).
- `+effect:entangle(a, b)` — корелювати стани двох фігур (ковзання крізь суперпозицію).
- `+cond:superposed(cell)` — клітина зайнята з імовірністю 0 < p < 1.
- `+cond:path_blocked_prob(path)` — шлях заблокований у частині гілок.
- `+trigger:measured(p)` — після вимірювання (ланцюг: колапс → перевірка короля).
- `+ui:probability-ring` · `+ui:phase-dial` · `+ui:split-slider` (нерівний split).
- `+window:quantum-lab` — пісочниця з гілкуванням ходів.
- `+feature:seasonal-rules` — змінні правила за сезонами (Alchemy League).
- `+axis:random` — значення `measurement` (випадковість лише як колапс стану, керована гравцем).
- `+card:superposition-move` · `+card:measurement-collapse`.

## Джерела
- ⭐ [ar5iv: Cantwell, Quantum Chess](https://ar5iv.labs.arxiv.org/html/1906.05836) — повна математична рамка: кубіти, заборона подвійного заповнення, усі типи ходів (Standard/Split/Merge Jump/Slide, Blocked/Capture), пішаки, en passant, рокіровка, правила 5, 10, 11 (без шаху, перемога, нічия).
- [arXiv: 1906.05836](https://arxiv.org/abs/1906.05836) — сторінка статті (PDF).
- [Steam: Quantum Chess](https://store.steampowered.com/app/453870/Quantum_Chess/) — Quantum Realm Games, Early Access 12.12.2016, реліз 28.02.2017, ремастер; режими, Quantum Lab, Alchemy League, Universal QC, кільця, Windows/macOS/Linux.
- [chess.quantumnative.io](https://chess.quantumnative.io/) — браузерна версія («chess where pieces split, free in your browser»).
- [Wikipedia: Quantum chess](https://en.wikipedia.org/wiki/Quantum_chess) — коротко про версію Akl (Queen's).
- YouTube — пошук «quantum chess anyone can quantum».

## Непевне
- (?) Чи можуть пішаки розщеплюватись: у chess-rule-twists записано «ні»; у відкритому фрагменті статті split описано лише для коня/короля (jump) і слона/тури/ферзя (slide) — отже, ймовірно, ні.
- (?) Перетворення пішака в суперпозиції (у що, з якою ймовірністю) — у прочитаній частині статті лише нотація.
- (?) Мобільна платформа: Steam згадує web і mobile для теми Cloud Chamber; окремих застосунків не відкривав.
- (?) Рік: правила Cantwell — 2016 (Early Access Steam — грудень 2016); стаття arXiv — 2019.
- (?) Правило 50 ходів / повторення — у статті не знайшов.
- (?) Точний вигляд меню (назви пунктів) — реконструйовано з опису режимів на Steam.
