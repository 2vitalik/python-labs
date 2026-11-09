---
title: Shōbu (Шобу)
slug: shobu
aka: [SHŌBU, Shobu, Шобу]
family: chess-abstract
also: [board-digital, push-slide]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2019
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/shobu/game-rules.php", best: true, note: "повні правила: 4 дошки, домашні дошки, пасивний і агресивний хід, штовхання, обмеження, перемога"}
  - {kind: other, url: "https://rulespal.com/shobu/rulebook", note: "те саме + приклади: діагональний хід на 2, блокування двома каменями"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Shobu", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shobu+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, legal-move-highlight, cell-click, drag-drop-piece, hover-highlight, turn-enforcement, hot-seat, ai-opponent, ai-minimax, push-object, game-screen, main-menu, end-screen, help-window, undo-step, +multi-board-field, +mirrored-second-move, +home-board-rule, +push-off-board-capture, +push-limit-one, +clear-one-board-win, +move-notation]
proposes: ["+trigger:pushed_off", "+cond:opposite_color(board_a, board_b)", "+cond:home_board(board, side)", "+effect:repeat_move(vector, board)", "+ui:passive-vector-arrow", "+ui:board-color-badge", "+feature:plan-aggressive-first", "+card:mirrored-second-move", "+card:multi-board-field"]
author: opus
date: 2026-11-09
---

# Shōbu — дві дії за хід на чотирьох дошках: пасивний хід удома повторюється агресивним на дошці іншого кольору й виштовхує камені

## Суть
Два гравці, чорні й білі камені, чотири малі дошки: дві темні й дві світлі, по дві «домашні» в кожного. Хід — пара рухів **одним і тим самим вектором**: спершу пасивний (без штовхання) своїм каменем на своїй домашній дошці, потім агресивний — тим самим напрямком і відстанню на дошці протилежного кольору, де вже можна штовхнути камінь суперника. Перемагає той, хто виштовхне всі камені суперника з **будь-якої однієї** дошки. Ядро — зчеплення двох рухів: пасивний хід лише «дозволяє» агресивний.

## Поле і час
- Чотири квадратні дошки 2×2 у квадраті, мотузка ділить стіл навпіл: ближчі до гравця дві дошки — його домашні, одна темна й одна світла. Розмір кожної дошки — у «Непевне».
- Кожна дошка — окреме поле: камені не переходять між дошками; вихід за край = камінь знято з гри.
- На кожній дошці по чотири камені кожного кольору на старті (розстановка — за малюнком правил).
- Хід — пасивний + агресивний рух, обидва обовʼязкові; чорні ходять першими.
- Інформація повна, випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Камінь гравця | piece | колір black/white | рух 1–2 клітини в будь-якому з 8 напрямків без стрибків |
| Камінь суперника | piece | — | може бути зсунутий агресивним ходом |
| Темна дошка | zone | колір dark | одна домашня в кожного гравця |
| Світла дошка | zone | колір light | одна домашня в кожного гравця |
| Домашня дошка | zone | власник | тут дозволено пасивний хід |
| Мотузка | static | — | межа між домашніми дошками гравців |
| Край дошки | static | — | виштовхнутий за нього камінь — з гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(p)` → ТО `custom: «потрібні два рухи одним вектором: пасивний, потім агресивний»`.
- Пасивний: КОЛИ `input(move(stone, dir, n))` → ЯКЩО `custom: «дошка — домашня для p»` and `custom: «n = 1 або 2»` and `free(path)` → ТО `move(stone, dir)` × n; штовхати й стрибати не можна, інакше `block`.
- Агресивний: КОЛИ `after(passive)` → ЯКЩО `custom: «дошка протилежного кольору до дошки пасивного ходу»` and `custom: «той самий напрямок і відстань»` → ТО `move(stone, dir)` × n — дошка може бути своєю домашньою або суперника.
- Штовхання: КОЛИ `contact(stone, enemy_stone)` у агресивному русі → ЯКЩО `custom: «за штовхнутим каменем на шляху нема іншого каменя»` → ТО `push(enemy_stone)` на відстань руху; штовхання необовʼязкове.
- Два камені: КОЛИ `contact(stone, enemy_stone)` → ЯКЩО `custom: «на лінії руху два камені підряд»` → ТО `block`.
- Свій камінь: КОЛИ `contact(stone, own_stone)` в агресивному русі → ТО `block`; свої не штовхаються.
- Виштовхування: КОЛИ `edge(enemy_stone)` → ТО `disappear(enemy_stone)` — з гри назавжди.
- Звʼязаність: КОЛИ `custom: «агресивний рух неможливий»` → ТО `custom: «пасивний теж недійсний — обрати інший пасивний»`.
- Перемога: КОЛИ `custom: «на якійсь дошці не лишилось каменів суперника»` → ТО `win`.
- Порада правил (не правило): `custom: «спершу знайти агресивний хід, потім пасивний, що його дозволяє»`.

## Керування і ввід
- Цифрова версія: вибрати камінь на домашній дошці → клітина призначення (`legal-move-highlight` лише для пасивних рухів, що мають хоча б одне агресивне продовження).
- Після пасивного — стрілка-вектор (`passive-vector-arrow`, кандидат) і підсвічені камені на дошках протилежного кольору, якими можна повторити вектор; клік по одному завершує хід.
- Корисне в цифрі: режим «спершу агресивний» — обрати бажаний агресивний рух, гра підбирає пасивні.
- Скасування пасивного до завершення ходу; повний `undo-step` — у грі з AI.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Грати проти AI / Hotseat · Правила → `help-window` · Налаштування.
- `match-setup`: колір, рівень AI.
- `game-screen`: 4 дошки з позначками кольору (`board-color-badge`, кандидат) і власника; `turn-indicator`; фаза (пасивний / агресивний); лічильник каменів на кожній дошці (`remaining-counter`); `move-list` (?).
- `end-screen`: переможець і дошка, з якої виштовхнуто всі камені.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `hotseat`, `ai-opponent-levels` (?); `undo`; `rules-page` з анімацією пари рухів.
- `history` / нотація ходів (?) — офіційної нотації в джерелах нема.

## Варіації й родичі
- Родичі «хід задає обмеження наступному»: [onitama](onitama.md) (картка ходу переходить супернику), [kamisado](kamisado.md) (колір клітини визначає наступну фігуру).
- Штовхання з поля: [abalone](abalone.md) (більшість штовхає меншість), [hey-thats-my-fish](../board-digital/hey-thats-my-fish.md) — інший тип «поле зникає».
- Кілька полів одночасно — [5d-chess](5d-chess.md) (поля-часові лінії).
- **Осі варіацій**: звʼязок двох рухів (той самий вектор / дзеркальний / будь-який) · де пасивний (лише вдома / будь-де) · дошка агресивного (протилежного кольору / будь-яка інша) · сила штовхання (1 камінь / ряд / більшість) · мета (очистити одну дошку / сумарна кількість).

## Цікавинки для курсу
- Поле з чотирьох незалежних дошок 4×4 (?) з кольором і власником — модель і рендер — 🌱.
- Генерація легальних ходів як пар (пасивний, агресивний) з однаковим вектором і перевіркою протилежного кольору — 📎.
- Штовхання з обмеженнями: не більше одного каменя, не свій, виштовхнутий за край — знято — 📎.
- Фільтр «пасивний легальний лише якщо є агресивне продовження» для підсвітки — 🥉.
- Minimax / alpha-beta для гри з малим полем, але великим розгалуженням пар рухів — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` (1–2 у 8 напрямках) · `push-object` (агресивний рух) · `legal-move-highlight` · `cell-click` · `drag-drop-piece` · `hover-highlight` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `ai-minimax` · `undo-step` · `game-screen` · `main-menu` · `end-screen` · `help-window`.
- Уже в корпусі: `+move-notation`.
- **Нема** → пропозиції карток:
  - `+multi-board-field` «Кілька незалежних полів з власними властивостями (колір, власник)» · interface/render · 📎.
  - `+mirrored-second-move` «Другий рух повторює вектор першого на іншому полі» · entities/legality · 🥉 · слоти {link: same-vector}.
  - `+home-board-rule` «Певна дія — лише на своїх полях» · entities/legality · 🌱.
  - `+push-off-board-capture` «Виштовхнутий за край — знятий» · entities/combat · 🌱.
  - `+push-limit-one` «Штовхнути можна лише один обʼєкт, ряд із двох блокує» · entities/legality · 🌱.
  - `+clear-one-board-win` «Перемога — очистити від суперника будь-яке з полів» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:pushed_off(a)` — обʼєкт виштовхнуто за край поля іншим (на відміну від `edge` — власний вихід).
- `+cond:opposite_color(board_a, board_b)` — поля різного кольору.
- `+cond:home_board(board, side)` — поле належить стороні.
- `+effect:repeat_move(vector, board)` — повторити рух тим самим вектором в іншому місці.
- `+ui:passive-vector-arrow` · `+ui:board-color-badge`.
- `+feature:plan-aggressive-first` — режим вводу «спершу другий рух».
- `+card:mirrored-second-move` · `+card:multi-board-field`.

## Джерела
- ⭐ [UltraBoardGames: Shobu rules](https://www.ultraboardgames.com/shobu/game-rules.php) — компоненти, домашні дошки, пасивний і агресивний хід, штовхання, обмеження, перемога.
- [RulesPal: Shobu rulebook](https://rulespal.com/shobu/rulebook) — приклади: діагональний рух на 2, блокування двома каменями.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Shobu); YouTube: пошук «Shobu how to play».

## Непевне
- (?) Розмір кожної дошки 4×4 і розстановка (чотири камені в ряд біля кожного гравця) — з памʼяті й черги; текст правил лише «as shown».
- (?) Автори (Manolis Vranas, Jamie Sajdak) і видавець (Smirk & Laughter Games) — з памʼяті; статті Wikipedia про гру нема (лінк черги веде на місто Шобу).
- (?) Чи може агресивний рух штовхнути камінь, якщо на його шляху перед штовханням ще один камінь (рух на 2) — RulesPal лише «двома каменями блоковано».
- (?) Цифрові версії й офіційна нотація — у джерелах нема; вікна гіпотетичні.
- Сімʼя: правила й еталони (Onitama, Abalone) — `chess-abstract`, а не `board-digital`, куди ставила черга.
