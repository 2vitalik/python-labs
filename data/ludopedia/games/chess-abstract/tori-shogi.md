---
title: Tori shogi (Пташине шогі)
slug: tori-shogi
aka: [禽将棋, 鳥将棋, Bird shogi, Torishogi, Пташине шогі]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: state
year: 1799
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tori_shogi", best: true, note: "7×7, 16 птахів, ходи всіх фігур, зона з 2 рядів, обовʼязкове перетворення, обмеження дропу ластівок, повторення, гандикапи, нотація Hodges"}
  - {kind: play, url: "https://www.pychess.org/variants/torishogi", note: "pychess: правила, пат = поразка, порушення повторення = поразка, набори фігур International / кандзі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tori+shogi+rules", note: "пошук; правила"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, piece-capture, piece-drop, pocket, pawn-promotion, no-move-into-check, check-stalemate, checkmate, legal-move-highlight, last-move-highlight, cell-click, drag-drop-piece, turn-enforcement, move-timer, ai-opponent, online-multiplayer, move-notation, match-setup, theme-select, game-screen, end-screen, help-window, state-as-data, unit-tests, +promotion-zone, +handicap-setup, +perpetual-ban, +blockable-leap, +chiral-pieces, +drop-file-limit, +no-drop-mate, +stalemate-loss]
proposes: ["+cond:in_zone", "+cond:drop_mate", "+cond:file_count", "+trigger:repetition_started_by", "+feature:handicap", "+window:handicap-select", "+card:chiral-pieces", "+card:drop-file-limit", "+card:no-drop-mate", "+card:stalemate-loss"]
author: opus
date: 2026-11-09
---

# Tori shogi — пташине шогі 7×7 з дропами, де лівий і правий перепели ходять дзеркально

## Суть
Шогі-варіант 1799 року (Тойота Ґенрю; традиційно приписують його вчителю Ōhashi Sōei): 7×7, у кожного 16 «птахів», мета — взяти чи заматувати **фенікса** (короля). Як у [шогі](shogi.md), узяті фігури йдуть у руку й скидаються як свої — це один з двох традиційних варіантів шогі з дропами. Незвичне: **дві хіральні фігури** (лівий і правий перепели — дзеркальні патерни), стрибуни, що досяжні лише на частині дошки (фазан, гуска), і 8 ластівок-пішаків з власними обмеженнями дропу.

## Поле і час
- Дошка 7×7; Black ходить першим, у гандикапній партії — White (сильніший).
- Старт (від Black): тиловий ряд — перепел, фазан, журавель, фенікс, журавель, фазан, перепел; сокіл — перед феніксом; ластівки — 7 на наступному ряду і ще одна на ряд далі (?); White — дзеркально.
- Зона перетворення — **два дальні ряди** (від рядка, де стоїть ворожий сокіл).
- Поза дошкою — рука кожного з узятими (неперетвореними) фігурами.
- Хід = рух фігури або дроп. Годинник: основний час + байо-йомі (pychess).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фенікс (鵬) | piece | royal; ×1 | 1 клітина в 8 напрямках; мета партії |
| Сокіл (鷹) | piece | ×1; ⇒ орел | 1 клітина в усі боки, крім прямо назад |
| Орел (鵰, перетворений сокіл) | piece | — | будь-яка відстань по діагоналях уперед і прямо назад; 1–2 клітини по діагоналях назад (блокується); 1 крок уперед і вбік |
| Журавель (鶴) | piece | ×2 | 1 клітина в усі боки, крім убік (ліворуч/праворуч) |
| Фазан (雉) | piece | leaper; ×2 | стрибок рівно на 2 прямо вперед; або 1 крок по діагоналі назад; досяжна ~половина дошки |
| Лівий перепел (鶉) | piece | slider; ×1; хіральна | будь-яка відстань прямо вперед і по діагоналі назад-праворуч; 1 крок по діагоналі назад-ліворуч |
| Правий перепел (鶉) | piece | slider; ×1; хіральна | дзеркально до лівого |
| Ластівка (燕) | piece | ×8; ⇒ гуска | 1 вперед, бʼє так само |
| Гуска (鴈, перетворена ластівка) | piece | leaper | стрибок рівно на 2 по діагоналі вперед або на 2 прямо назад; досяжна ~чверть дошки |
| Рука | zone | лічильник за типом | узяті фігури, повертаються неперетвореними |
| Зона перетворення | zone | 2 дальні ряди | хід у / з / усередині → обовʼязкове перетворення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `legal(move)` → ТО `move(piece, to)`, `end_turn`; `legal` — патерн фігури + не лишати фенікса під шахом.
- Слайдери (перепели, орел) зупиняються на взятті й не проходять крізь фігури; стрибуни (фазан, гуска) перестрибують.
- КОЛИ `contact(piece, enemy_piece)` → ТО `disappear(enemy_piece)`, `give(side, unpromoted(kind))`; фігура в руці — вже своя.
- КОЛИ `after(move)` → ЯКЩО `custom: «старт або фініш у зоні перетворення»` (`+cond:in_zone`) і фігура — ластівка чи сокіл → ТО `transform(swallow→goose | falcon→eagle)` — обовʼязково, вибору нема.
- КОЛИ `input(drop, kind, cell)` → ЯКЩО `has(side, kind)` і `free(cell)` → ТО `place(side, kind)` неперетвореною, `take(side, kind)`, `end_turn`; дроп не бʼє і не перетворює.
- КОЛИ `input(drop, swallow, cell)` → ЯКЩО `custom: «cell на дальньому ряду»` → ТО `block`.
- КОЛИ `input(drop, swallow, cell)` → ЯКЩО `custom: «у вертикалі вже 2 свої неперетворені ластівки»` (`+cond:file_count`) → ТО `block` (у шогі ліміт 1, тут 2; гуски не рахуються).
- КОЛИ `input(drop, swallow, cell)` → ЯКЩО `custom: «дроп дає негайний мат»` (`+cond:drop_mate`) → ТО `block` (pychess: такий дроп = `lose`).
- КОЛИ `turn_start(side)` → ЯКЩО `in_check(phoenix)` і `no_moves(side)` → ТО `lose` (мат).
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` і `not in_check(phoenix)` → ТО `lose` (пат — поразка, pychess).
- КОЛИ `contact(piece, enemy_phoenix)` → ТО `win` (на практиці здаються раніше).
- КОЛИ `repetition(3)` (дошка + руки + черга) → ТО `custom: «той, хто почав цикл, мусить змінити хід»` (`+trigger:repetition_started_by`); pychess — інакше `lose`. Вічний шах окремо не описаний — випливає з цього правила.
- Нелегальний хід у живій грі → `lose` (у дружніх партіях можна відкотити).
- Гандикап: КОЛИ партія з форою → ТО `custom: «White прибирає лівого перепела / сокола / сокола й лівого перепела / сокола й обох перепелів, ходить першим»`; прибрані фігури не йдуть у руку.
- Перемога: мат · взяття фенікса · пат суперника · порушення повторення суперником · Нічиєї за правилами нема (?).

## Керування і ввід
- (цифрова версія, pychess) клік або drag фігури → підсвітка легальних клітин; дроп — з панелі руки; перетворення автоматичне (без діалогу).
- Здача, пропозиція нічиєї, годинник з байо-йомі; гандикап — при створенні партії.

## Вікна, меню, HUD
- (цифрова версія, pychess)
- `match-setup`: варіант Tori shogi, час, байо-йомі, гандикап (`handicap-select`), проти AI / людини.
- `game-screen`: дошка 7×7 з координатами, два `pocket`, два `player-clock`, `move-list` у нотації Hodges (`Sw`, `Q`, `Pt`, `Cr`, `Fa`, `Ph`; `+Sw` — гуска; `-`, `x`, `*` дроп, `+` перетворення), `last-move-highlight`, `legal-move-highlight`.
- `settings-window`: набір фігур — International (піктограми, за замовчуванням) або традиційний кандзі з позначками 左/右 над перепелами (`theme-select`).
- `end-screen`: мат / пат / порушення повторення / тайм-аут.
- Переходи: lobby → match-setup → game-screen → end-screen → аналіз.

## Фічі поза полем
- `handicap` — чотири типові фори прибиранням фігур (див. правила).
- `online-multiplayer` і AI на pychess; турніри в Лондоні й Ройстоні у 1990-х — на початку 2000-х (Wikipedia).
- `move-notation` — система George Hodges (1976): вертикаль-цифра + горизонталь-літера, `1a` — правий верхній кут від Black.

## Варіації й родичі
- База — [shogi.md](shogi.md); великі історичні варіанти — [large-shogi-variants.md](large-shogi-variants.md); міні — [dobutsu-shogi.md](dobutsu-shogi.md), [shogi-rule-twists.md](shogi-rule-twists.md).
- Wa shogi (11×11, теж тварини й птахи) — можливо, єдиний інший традиційний варіант з дропами; Yari shogi (7×9) — інша гра на 7 вертикалей.
- **Осі варіацій**: хіральність (симетричні фігури / пари «лівий-правий») · ліміт пішаків у вертикалі при дропі (1 у шогі / 2 тут) · перетворення (вибір / обовʼязкове) · пат (нічия в шахах / поразка тут і в сянці) · повторення (нічия / обовʼязок змінити хід).

## Цікавинки для курсу
- Хіральні фігури: патерн лівого перепела, правий — віддзеркаленням по вертикалі; плюс поворот на 180° для суперника — 🌱.
- Орел: слайдер + блокований дворазовий крок по діагоналі назад — комбінований патерн у генераторі ходів — 📎.
- Параметризовані обмеження дропу (дальній ряд, ліміт у вертикалі = 2, заборона мату дропом ластівки) — 🥈; перевірка «дроп = мат» усередині перевірки легальності — 🥇.
- Повторення з «хто почав цикл»: історія позицій з руками й визначення ініціатора — 🥈.
- Досяжність стрибунів: які клітини взагалі доступні фазану й гусці (BFS за патерном) — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 9 типів · `piece-capture` · `piece-drop` + `pocket` · `pawn-promotion` ↔ ластівка → гуска, сокіл → орел · `no-move-into-check`, `check-stalemate`, `checkmate` · `legal-move-highlight`, `last-move-highlight`, `cell-click`, `drag-drop-piece` · `turn-enforcement`, `move-timer` ↔ байо-йомі · `ai-opponent`, `online-multiplayer` · `move-notation` ↔ Hodges · `match-setup` ↔ гандикап · `theme-select` ↔ набори фігур · `game-screen`, `end-screen`, `help-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+promotion-zone`, `+handicap-setup` (див. shogi.md); `+perpetual-ban` (див. xiangqi.md) — тут «ініціатор змінює хід»; `+blockable-leap` (див. xiangqi.md) — крок орла назад.
  - `+chiral-pieces` «Дзеркальні пари фігур (лівий / правий)» · entities/move · 🌱 · слоти {mirror_axis}.
  - `+drop-file-limit` «Ліміт однотипних фігур у вертикалі при дропі» · entities/legality · 📎 · слоти {kind, n} — nifu як n=1.
  - `+no-drop-mate` «Заборона мату дропом» · entities/legality · 🥇 · слоти {kind, penalty: block|lose}.
  - `+stalemate-loss` «Пат — поразка» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+cond:in_zone` — голос (shogi.md та ін.): старт/фініш ходу в зоні перетворення.
- `+cond:drop_mate` — дроп дає негайний мат.
- `+cond:file_count` — кількість фігур виду у вертикалі (рядку) порівняно з N.
- `+trigger:repetition_started_by` — повторення, з визначенням сторони, що почала цикл.
- `+feature:handicap`, `+window:handicap-select` — голоси (shogi.md).
- `+card:chiral-pieces`, `+card:drop-file-limit`, `+card:no-drop-mate`, `+card:stalemate-loss` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Tori shogi](https://en.wikipedia.org/wiki/Tori_shogi) — автор і рік, 7×7, ходи всіх фігур і перетворених, зона з двох рядів, обовʼязкове перетворення, три обмеження дропу ластівок, шах/мат, повторення («ініціатор змінює хід»), чотири гандикапи, нотація Hodges, турніри.
- [pychess: Tori shogi](https://www.pychess.org/variants/torishogi) — ті самі ходи, ≤2 ластівки у вертикалі, мат дропом ластівки = поразка, пат = поразка, порушення повторення = поразка, байо-йомі, набори фігур International / кандзі з 左/右.
- YouTube — пошук.

## Непевне
- (?) Точне розташування восьмої ластівки (на ряд попереду решти, у якій вертикалі) — діаграму Wikipedia в текстовій витяжці не прочитати.
- (?) Пат = поразка й мат дропом = поразка — лише pychess; Wikipedia про пат мовчить.
- (?) Нічиєї як такої нема — висновок з правила повторення, явного рядка в джерелах не бачив.
- (?) Рік 1799 — за Wikipedia (стаття просить більше джерел); перша публікація 1828.
- (?) Чи на pychess є AI саме для Tori shogi (Fairy-Stockfish) — не перевіряв.
