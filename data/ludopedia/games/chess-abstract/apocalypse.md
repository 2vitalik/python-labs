---
title: Apocalypse (Апокаліпсис, одночасні шахи коней і пішаків)
slug: apocalypse
aka: [Apocalypse chess, Апокаліпсис]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: wego
  opponent: hotseat
  info: hidden
  random: none
  goal: state
year: 1976
platforms: [paper, board, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Apocalypse_(chess_variant)", best: true, note: "5×5, вершники й піхотинці, таємний запис ходів, розвʼязання зіткнень, штрафні очки, перетворення/передислокація, кінець гри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=apocalypse+chess+variant", note: "пошук"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, pawn-promotion, hot-seat, pass-device, ai-opponent, cell-click, game-screen, end-screen, help-window, state-as-data, unit-tests, +double-blind-choice, +submit-turn, +simultaneous-resolution, +penalty-points, +promotion-cap-redeploy, +capture-count-win]
proposes: ["+trigger:submit", "+trigger:move_reveal", "+cond:same_target", "+effect:forfeit", "+ui:submit-button", "+ui:penalty-counter", "+window:move-reveal", "+feature:submit-turn", "+card:simultaneous-resolution", "+card:penalty-points", "+card:promotion-cap-redeploy"]
author: opus
date: 2026-11-09
---

# Apocalypse — мініатюрні шахи, де обидва ходять одночасно і зіткнення вирішують правила

## Суть
Варіант C. S. Elliott (1976, журнал Games & Puzzles): на дошці 5×5 у кожного 2 вершники (ходять конем) і 5 піхотинців (пішаки без подвійного кроку). Обидва гравці **таємно записують хід, потім відкривають одночасно**; якщо фігури зустрілися на одній клітині — діє таблиця зіткнень. Мета — лишитися з піхотинцями, коли в суперника їх нема. Головне не «який хід найкращий», а «що зробить суперник у цей самий момент».

## Поле і час
- Дошка 5×5; стартова розстановка — за діаграмою статті (вершники в кутах першого ряду (?)).
- Хід = фаза запису (обидва, приховано) → одночасне відкриття → розвʼязання. Черговості нема.
- Кожен гравець рухає рівно одну фігуру за хід.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вершник | piece | ×2; кінь | хід конем; на спільній клітині бʼє піхотинця |
| Піхотинець | piece | ×5; пішак | 1 вперед, бʼє навскіс уперед; без подвійного кроку; на останньому ряду ⇒ вершник або передислокація |
| Записаний хід | mark | прихований до відкриття | фіксує фігуру, ціль і (для передислокації) клітину |
| Штрафне очко | — | 0…2 | за нелегальний хід; 2 = поразка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(write_move)` обох гравців → ТО `custom: «обидва ходи відкриваються одночасно»` (`+trigger:move_reveal`), далі обидва ходи виконуються з розвʼязанням зіткнень.
- КОЛИ `custom: «обидва ходи ведуть в одну клітину»` (`+cond:same_target`) → ЯКЩО вершник проти піхотинця → ТО `disappear_b` піхотинця, вершник стає на клітину.
- КОЛИ `custom: «обидва ходи ведуть в одну клітину»` → ЯКЩО `same(a, b, kind)` → ТО `disappear_both`.
- КОЛИ `custom: «піхотинець оголосив взяття навскіс, а ціль пішла»` → ТО `move(footman, diagonal)` — хід виконується як крок навскіс без взяття.
- КОЛИ `custom: «фігура ходить на клітину, де стоїть ворог, що лишився на місці»` → ТО `disappear_b` (звичайне взяття).
- КОЛИ `input(move)` → ЯКЩО `not legal(move)` → ТО `block`, `counter(penalty, +1)` — хід втрачено.
- КОЛИ `counter(penalty, >=, 2)` → ТО `lose` (форфейт).
- КОЛИ `reach(footman, last_rank)` → ЯКЩО `count(own_horseman, <, 2)` → ТО `transform(horseman)`.
- КОЛИ `reach(footman, last_rank)` → ЯКЩО `count(own_horseman, ==, 2)` → ТО `custom: «передислокувати на будь-яку вільну клітину не на останньому ряду; клітина записується разом з ходом»`.
- КОЛИ `input(move, last_footman, last_rank)` → ЯКЩО `count(own_horseman, <, 2)` → ТО `block` — не можна вести єдиного піхотинця на останній ряд.
- КОЛИ `custom: «в одного гравця є піхотинці, у суперника — нема»` → ТО `win`.
- КОЛИ `custom: «обидва втратили останнього піхотинця одним ходом»` → ТО `draw`.
- КОЛИ `no_moves(side)` → ЯКЩО `custom: «в обох ще є піхотинці»` → ТО `draw`.
- Перемога: лишитися з піхотинцями · 2 штрафи суперника. Нічия: одночасна втрата останніх · немає ходів. Рахунку нема.

## Керування і ввід
- Паперова/настільна: кожен пише хід на аркуші (фігура, з, на; для передислокації — ще клітина), потім обидва показують.
- (цифрова версія) Вибрати фігуру → клітину → `submit-button`; до відкриття хід суперника схований; hot-seat вимагає `pass-device` між записами.
- Після відкриття — анімація обох ходів і підсвітка зіткнення.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Проти AI · З другом (hot-seat) · Правила → `help-window`.
- `game-screen`: дошка 5×5, `legal-move-highlight`, `submit-button`, статус «суперник записав / ще думає», `penalty-counter` для кожного, лічильник піхотинців (`remaining-counter`).
- `pass-device` — завіса між записами в hot-seat.
- `move-reveal` — показ обох ходів одночасно з поясненням зіткнення («вершник зʼїв піхотинця», «обидва зникли»).
- `end-screen`: перемога / нічия / форфейт за штрафи.

## Фічі поза полем
- `hotseat` з завісою, `ai-opponent-levels` (AI має обирати змішану стратегію (?)), `rules-page`, `history` записаних ходів.

## Варіації й родичі
- Apocalypse Mini-Chess — з чотирма вершниками (?).
- Одночасні ходи в сімʼї: Kung-Fu у [chess-rule-twists](chess-rule-twists.md) (реальний час, без таємності), [5d-chess](5d-chess.md) (submit-хід); таємний вибір — `double-blind-choice` у [chess-2-sequel](chess-2-sequel.md).
- Поза сімʼєю: Diplomacy (одночасні накази й конфлікти), RoboRally/Frozen Synapse (`time: wego`).
- **Осі варіацій**: черговість (по черзі / одночасно / реальний час) · таємність (відкритий / записаний хід) · зіткнення (сильніший бʼє / обидва гинуть / відскок) · покарання за нелегальний хід (повтор / штраф / поразка).

## Цікавинки для курсу
- Фаза WEGO: запис двох ходів, відкриття, детерміноване розвʼязання — 📎.
- Таблиця зіткнень (вершник > піхотинець, однакові — обидва гинуть, «ціль пішла» — крок навскіс) — 🌱.
- Штрафні очки за нелегальний хід як механіка, а не помилка вводу — 🌱.
- Перетворення з обмеженням кількості (≤2 вершники) і передислокація — 🌱.
- AI для одночасних ходів: матриця виграшів і змішана стратегія замість minimax — 🥇.
- Hot-seat із прихованим ходом: завіса й чесне відкриття — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `legal-move-highlight` · `pawn-promotion` ↔ піхотинець → вершник · `hot-seat`, `pass-device` ↔ завіса між записами · `ai-opponent` · `cell-click` · `game-screen`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+double-blind-choice`, `+submit-turn` (є в сімʼї) — тут таємний хід фігурою.
  - `+capture-count-win` (є в сімʼї) — знищити всіх піхотинців.
  - `+simultaneous-resolution` «Одночасні ходи з таблицею зіткнень» · game-logic/opponent · 📎 · слоти {collision_table}.
  - `+penalty-points` «Штраф за нелегальний хід, N штрафів = поразка» · game-logic/lose · 🌱 · слоти {limit: 2}.
  - `+promotion-cap-redeploy` «Перетворення з лімітом кількості, інакше — передислокація» · entities/legality · 🌱.

## Пропозиції до словників
- `+trigger:submit` — підтверджую (5d-chess): гравець зафіксував хід.
- `+trigger:move_reveal` — одночасне відкриття прихованих ходів обох сторін.
- `+cond:same_target` — два ходи ведуть в одну клітину.
- `+effect:forfeit` — підтверджую: поразка за порушення (штрафи).
- `+ui:submit-button` — підтверджую; `+ui:penalty-counter` — штрафні очки гравця.
- `+window:move-reveal` — екран відкриття обох ходів з поясненням.
- `+feature:submit-turn` — підтверджую.
- `+card:simultaneous-resolution`, `+card:penalty-points`, `+card:promotion-cap-redeploy` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Apocalypse (chess variant)](https://en.wikipedia.org/wiki/Apocalypse_(chess_variant)) — автор і рік, 5×5, 2 вершники + 5 піхотинців, таємний запис, зіткнення (вершник/піхотинець, однакові), «ціль пішла», штрафи, перетворення до 2 вершників і передислокація, перемога/нічия.
- YouTube — пошукова сторінка.

## Непевне
- (?) Точна стартова розстановка (вершники в кутах, 3 піхотинці між ними + 2 на краях другого ряду) — з діаграми, якої я не бачив; chessvariants.org віддає 403.
- (?) Що стається, коли фігури міняються місцями («проходять одна крізь одну») або обидві бʼють одна одну — у статті не описано; ймовірно, обидва ходи виконуються.
- (?) Apocalypse Mini-Chess з чотирма вершниками — лише зі зведення пошуку, не відкривав.
- (?) Публікація в Games & Puzzles № 53 — зі зведення пошуку.
- (?) Чи «пас» дозволено без штрафу, коли нема ходу, — неперевірене джерело каже так, Wikipedia — нічия за відсутності ходів.
