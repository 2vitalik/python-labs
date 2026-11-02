---
title: Patchwork (Печворк)
slug: patchwork
family: board-digital
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 2014
platforms: [board, PC, mobile, web]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/patchwork/game-rules.php", best: true, note: "повні правила: дії A/B, нейтральна фішка, спецлатки, 7×7, кінець, тай-брейк"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Patchwork_(board_game)", note: "історія, перевидання, Express/Doodle, цифрові версії"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=patchwork", note: "грати в браузері (BGA)"}
  - {kind: other, url: "https://en.doc.boardgamearena.com/Gamehelppatchwork", note: "довідка BGA з правилами"}
  - {kind: steam, url: "https://store.steampowered.com/app/528250/Patchwork/", note: "DIGIDICED, 2016: AI 3 рівні, онлайн, туторіал, playback"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Patchwork+board+game+how+to+play", note: "пошук; пояснення правил"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Patchwork", note: "пошук BGG"}
stage: v1
coverage: 65
mechanics: [round-currency, event-points, drag-drop-piece, hover-highlight, legal-move-highlight, hot-seat, turn-enforcement, ai-opponent, replay, save-game, +polyomino-placement, +piece-rotate-flip, +time-track-turns, +cyclic-market, +track-milestone-events, +first-to-achieve-bonus, +square-detection, +leftover-penalty]
proposes: ["+trigger:cross", "+effect:place", "+cond:fits", "+cond:afford", "+role:supply", "+ui:time-track", "+ui:market-ring", "+ui:piece-tray", "+axis:turn-structure"]
author: opus
date: 2026-11-02
---

# Patchwork — латай ковдру 9×9: латка коштує ґудзики і час, ходить той, хто позаду

## Суть
Два гравці купують поліоміно-латки з кола навколо треку часу й викладають їх на свою ковдру 9×9. Кожна латка має ціну в ґудзиках і ціну в часі; хід отримує той, чия фішка часу **позаду**, тож дешева за часом латка може дати кілька ходів поспіль. Ґудзики на латках дають дохід, коли фішка минає клітини доходу на треку. Наприкінці: ґудзики − 2 за кожну порожню клітину ковдри + 7 за перший заповнений квадрат 7×7.

## Поле і час
- **Три поля**: дві особисті ковдри 9×9 (по одній на гравця) і спільний трек часу — спіраль клітин від старту до центру з позначками доходу й 5 спецлатками 1×1.
- **Ринок**: 33 латки викладені колом (овалом) навколо треку; нейтральна фішка стоїть між латками й визначає «вікно» з трьох наступних за годинниковою стрілкою.
- Хід не чергується: ходить гравець, чия фішка часу далі від кінця; якщо фішки на одній клітині — той, чия фішка зверху (прийшов останнім).
- Гра закінчується, коли обидві фішки дійшли до останньої клітини треку; рух за неї обрізається.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Латка | piece | форма-поліоміно, ціна ґудзиків, ціна часу, ґудзики на ній (дохід) | купується з вікна ринку, кладеться на ковдру будь-якою орієнтацією |
| Ринок латок (коло) | supply | 33 латки по колу, порядок випадковий | після покупки латка зникає, коло «стискається» |
| Нейтральна фішка | object | позиція в колі | визначає 3 доступні латки; переходить на місце купленої |
| Фішка часу | piece | позиція на треку, одна на гравця | рухається вперед на ціну часу / до суперника+1 |
| Ковдра 9×9 | zone | 81 клітина | латки не перекриваються, не виходять за межі |
| Ґудзик | resource | кількість | валюта: платити за латки; наприкінці = очко |
| Клітина доходу на треку | static | позиція | коли фішка минає — дохід = ґудзики на латках ковдри |
| Спецлатка 1×1 (шкіряна) | pickup | 5 штук на треку | хто перший минає — забирає й одразу кладе на ковдру |
| Тайл 7×7 | pickup | +7 очок, один на гру | перший, хто заповнив квадрат 7×7, забирає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО ходить гравець з найменшою позицією на треку; рівність → той, чия фішка зверху.
- Дія A: КОЛИ `input(advance)` → ТО `move(time_token, opponent_pos + 1)`, `currency(+клітин_пройдено)`.
- Дія B: КОЛИ `input(buy(patch))` → ЯКЩО `custom: «латка — одна з 3 наступних за нейтральною фішкою»` and `afford(player, patch.cost)` and `fits(patch, quilt)` → ТО `currency(-patch.cost)`, `move(neutral, patch.slot)`, `place(patch, cells)`, `move(time_token, +patch.time)`; інакше `block`.
- КОЛИ `cross(time_token, income_mark)` → ТО `currency(+сума ґудзиків на латках ковдри)`.
- КОЛИ `cross(time_token, leather_patch)` → ЯКЩО `custom: «спецлатка ще на треку»` → ТО `pickup`, `place(leather_1x1, any_free_cell)` одразу.
- КОЛИ `pattern(square(7))` на ковдрі → ЯКЩО `first_time` (у грі) → ТО `give(player, bonus_7x7)`.
- КОЛИ `reach(time_token, last_cell)` → ТО `custom: «зайвий рух обрізається; дія A платить лише за реально пройдені клітини»`.
- КОЛИ `custom: «обидві фішки на останній клітині»` → ТО `game_over`.
- Купити латку можна лише якщо вміщається й вистачає ґудзиків; інакше лишається дія A.
- Рахунок: `score(+ґудзики)` `score(+7, якщо тайл 7×7)` `score(-2 × порожні клітини ковдри)`. Перемога — більше очок; нічия → хто першим дійшов до кінця треку.

## Керування і ввід
- Вибір дії: клік по одній із трьох підсвічених латок ринку або кнопка «пройти й отримати ґудзики».
- Розміщення: drag латки на ковдру, поворот на 90° і дзеркало (кнопки/клавіші/жест), підтвердження; нелегальна позиція підсвічується.
- Спецлатку 1×1 і тайл 7×7 гра пропонує/видає автоматично; дохід нараховується сам.
- Черга ходів — за треком часу, не по колу: інтерфейс мусить явно показувати, чий хід і чому.

## Вікна, меню, HUD
(цифрова версія — DIGIDICED/Steam і BGA)
- `main-menu`: Онлайн · Локальна гра (pass-and-play) · Проти AI (легкий/середній/важкий) · Туторіал · Playback · Налаштування.
- `tutorial-window`: інтерактивне навчання по кроках.
- `game-screen`: дві ковдри 9×9 (своя велика, суперника видно); `time-track` у центрі з фішками, клітинами доходу й спецлатками; `market-ring` — коло латок з підсвіченими трьома доступними й позначкою нейтральної фішки; на кожній латці ціна ґудзиків і часу; `coins`-лічильник ґудзиків і «дохід з ковдри» кожного гравця; `turn-indicator`; `drag-ghost` латки над ковдрою з `legal-move-highlight`; кнопки поворот / дзеркало / підтвердити.
- `tooltip` над латкою: ціна, час, дохід.
- `end-screen`: розкладка рахунку (ґудзики, +7, −2×порожні) для обох.
- `replay-window` (Playback): перегляд своїх найкращих партій і партій топ-гравців.
- `settings-window`: фони й візерунки ковдри, звук, мова (8 мов).
- Переходи: main-menu → (режим) game-screen → end-screen → main-menu / replay-window.

## Фічі поза полем
- `ai-opponent-levels` (3 рівні), `online-multiplayer` (крос-платформа, рейтинг), `hotseat` / локальна гра, `tutorial`.
- `replay` (Playback), `achievements`, `cloud-save`, `custom-skins` (фони й візерунки), `localization`.
- BGA: асинхронна гра «по ходу на день» і реальний час (`turn-timer`).
- Соло: Patchwork Automa (2018) — 24 карти штучного суперника.

## Варіації й родичі
- **Patchwork Express** (2018): більші латки, менша ковдра, простіший рахунок; **Patchwork Doodle** (2019): roll-and-write, форму задає кубик; **Stack'n Stuff** (2022) — та сама система з меблями у вантажівці.
- Ретеми (Winter, Americana, Halloween, Valentine's, Folklore) — механіка та сама.
- Пізніші друки посунули першу спецлатку далі по треку (вона була надто рано).
- Родичі: Blokus (поліоміно), A Feast for Odin, Bärenpark, The Isle of Cats (поліоміно-заповнення), Tokaido і Thebes (трек часу: ходить останній).
- **Осі варіацій**: черга ходів (по колу / хто позаду на треку) · ціна (лише гроші / гроші + час) · ринок (відкритий / вікно з N після фішки / драфт) · рахунок (заповнення / порожні клітини як штраф / бонус за фігуру 7×7).

## Цікавинки для курсу
- Трек часу як черга ходів: «ходить той, хто позаду, а при рівності — хто прийшов останнім» — 📎 (пріоритетна черга з тай-брейком).
- Циклічний ринок з вікном 3 після нейтральної фішки (видалення з кільця, зсув вікна) — 📎 (кільцевий список/`deque`).
- Події «минув клітину треку» (дохід, спецлатка) — 🥉: треба перевіряти всі клітини між старою й новою позицією, а не лише кінцеву.
- Пошук першого повного квадрата 7×7 на 9×9 — 📎 (префіксні суми або перебір 9 позицій).
- Підказка/AI «яка латка вигідніша»: оцінка ґудзики/час/площа + перевірка, чи взагалі вміщається (перебір орієнтацій і позицій) — 🥈.
- Повний AI з оцінкою кінця гри (minimax/MCTS на двох «годинниках») — 🥇.

## Мапа на каталог
- Є: `round-currency` (ґудзики: дохід і витрати) · `event-points` (−2/+7) · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `hot-seat` · `turn-enforcement` · `ai-opponent` · `replay` · `save-game`.
- **Нема** → пропозиції карток:
  - `+polyomino-placement` — як у Blokus (без правила кутів).
  - `+piece-rotate-flip` — 8 орієнтацій латки.
  - `+time-track-turns` «Черга ходів за треком часу» · game-logic/opponent · 🥉 · слот {tie: last_arrived|first} — дія коштує час, ходить той, хто позаду.
  - `+cyclic-market` «Кільцевий ринок з вікном після фішки» · game-logic/economy · 📎 · слот {window: 3}.
  - `+track-milestone-events` «Події при проходженні клітин треку» · game-logic/economy · 🥉 — дохід, бонус-предмет першому.
  - `+first-to-achieve-bonus` «Бонус першому, хто досяг» · game-logic/score · 🌱 — тайл 7×7 (родичі: «найдовша дорога» в Ticket to Ride).
  - `+square-detection` «Пошук повного квадрата k×k» · game-logic/constraints · 📎 · слот {k: 7}.
  - `+leftover-penalty` — тут штраф за порожню клітину (−2).

## Пропозиції до словників
- `+trigger:cross(a, mark)` — фішка пройшла через клітину (не обовʼязково зупинилась): дохід, спецлатка. Відрізняється від `reach`/`enter`.
- `+effect:place` · `+cond:fits` — як у Blokus.
- `+cond:afford(a, cost)` — вистачає валюти (ширше за `has`: порівняння з ціною).
- `+role:supply` — коло латок як спільний запас.
- `+ui:time-track` — трек часу/очок з фішками гравців; `+ui:market-ring` — кільце товарів з підсвіченим доступним вікном; `+ui:piece-tray` — тут власні латки, що чекають розміщення (спецлатка).
- `+axis:turn-structure` = `time-track`.

## Джерела
- ⭐ [UltraBoardGames: Patchwork rules](https://www.ultraboardgames.com/patchwork/game-rules.php) — склад (33 латки, 5 спецлатки, 1 тайл), дії A/B, вікно 3 латок, події треку, кінець, тай-брейк.
- [Wikipedia: Patchwork](https://en.wikipedia.org/wiki/Patchwork_(board_game)) — автор Уве Розенберг, версії, Express/Doodle/Automa, цифрові видання.
- [BGA: Patchwork](https://en.boardgamearena.com/gamepanel?game=patchwork) і [довідка BGA](https://en.doc.boardgamearena.com/Gamehelppatchwork) — правила й гра в браузері.
- [Steam: Patchwork](https://store.steampowered.com/app/528250/Patchwork/) — режими цифрової версії (AI ×3, онлайн, локально, туторіал, Playback).
- YouTube: пошук «Patchwork board game how to play».

## Непевне
- (?) Кількість клітин доходу на треку (9) і точна довжина треку (~53) — з памʼяті; джерела не називають.
- (?) Діапазони цін латок (ґудзики 0–10, час 1–6) — з памʼяті.
- (?) Чи дохід дають і за ґудзики на спецлатках/тайлі 7×7 — ні (на них ґудзиків нема), з памʼяті.
- (?) Меню цифрової версії зібране за описом Steam, не з власного запуску; назви пунктів можуть відрізнятись.
