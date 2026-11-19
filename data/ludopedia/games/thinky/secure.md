---
title: Secure
slug: secure
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://toombler.itch.io/secure", best: true, note: "грати в браузері; «A block pushing game with a mysterious goal»; керування Z/R/WASD/X/Esc/M; теги rule-discovery, Sokoban; коментарі: 17 рівнів, «reverse sokoban»"}
  - {kind: play, url: "https://dario-zubovic.github.io/PuzzleScript/play.html?p=57084dce3c309bd2f57e5c2bb301fa02", note: "мобільна версія й сирці (посилання автора)"}
  - {kind: other, url: "https://gist.github.com/Toomber/57084dce3c309bd2f57e5c2bb301fa02", note: "PuzzleScript-сирці (gist 31.07.2021): поштовх, платформи, заливка досяжності, умова «жоден ящик не рушить», 17 рівнів + чернетки"}
  - {kind: other, url: "https://coreyhardt.wordpress.com/2021/11/26/worth-your-time-secure/", note: "огляд Corey Hardt (26.11.2021): «mysterious twist», мету не розкриває"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Secure+Toombler+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, reachability-check, deadlock-detection, completion-detection, undo-redo, undo-unlimited, restart-level, sequential-levels, level-select, level-unlock, save-progress, level-from-txt, idle-animation, event-effects, sound-effects, +rule-discovery, +immobilize-all-goal, +confirm-to-win]
proposes: ["+cond:pushable", "+axis:rules-discovered", "+card:immobilize-all-goal", "+card:confirm-to-win"]
author: opus
date: 2026-11-19
---

# Secure — Sokoban навпаки з прихованою метою: рівень пройдено, коли жоден ящик більше не можна зсунути

## Суть
Покроковий PuzzleScript-сокобан на 17 рівнів, де мету ніде не названо: опис каже лише «block pushing game with a mysterious goal», і правило гравець відкриває сам (тег itch `rule-discovery`). За сирцями мета — **закріпити всі ящики**: після кожного ходу гра заливкою шукає клітини, досяжні для гравця, і якщо з жодної не можна штовхнути жоден ящик, ящики міняють вигляд, а X/Enter веде далі. Тобто deadlock, якого в Sokoban уникають, тут і є ціллю (коментатори: «reverse sokoban», гравець — «source of entropy»).

## Поле і час
- Квадратна сітка; рівні — ASCII-карти PuzzleScript, від 7×7 до 14 клітин завширшки (за сирцями); край — стіни з автоматичною рамкою.
- Шари колізій: фон · платформа · гравець / стіна / руйнована стіна / ящик / закріплений ящик · службові маркери (заливка, «ящик незрушний», перемога) · таймери анімації.
- Хід = один крок гравця; логіка лише на ввід (`time: turn`); `realtime_interval 0.1` крутить тільки анімацію простою гравця й «перелив» ящика після поштовху.
- Мета перевіряється «пізніми» правилами в кінці кожного ходу; рівні згруповано автором: вступ (1–4), платформи (5–7), «два ящики біля стіни — застрягли» (8–12), ящики в лабіринті платформ (13–14), ящики, недосяжні для гравця (15–17).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець («іскристий самоцвіт») | player | анімація простою на 60 кадрів | рух 4 напрямки, штовхає один ящик |
| Ящик | object | 9 кадрів переливу після поштовху | зсувається на 1, якщо за ним нема ящика, стіни чи платформи |
| Закріплений ящик | object | — | зʼявляється замість усіх ящиків, коли мету виконано; не штовхається, блокує всіх |
| Стіна | static | — | непрохідна для всіх |
| Платформа | terrain | — | гравець ходить, ящик заїхати не може |
| Руйнована стіна | static | — | блокує гравця; ящик, штовхнутий у неї, зникає разом із нею (у 17 рівнях не стоїть) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; платформа для гравця вільна.
- КОЛИ `contact(player, box)` → ЯКЩО `custom: «за ящиком нема ящика, закріпленого ящика, стіни чи платформи»` → ТО `push(box)`, `move(player, dir)`; інакше `block` (другий ящик — перешкода, ланцюгом не штовхаються).
- КОЛИ `contact(box, breakable_wall)` → ТО `disappear_both` — правило є в сирцях, у рівнях не вжито.
- КОЛИ `turn_end(player)` → ТО `custom: «заливка: позначити клітини, досяжні від гравця через клітини без ящиків і стін»`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «для кожного ящика нема досяжної сусідньої клітини, з якої поштовх уперед вільний (не ящик, не стіна, не платформа)»` → ТО `transform(box, secured_box)` для всіх ящиків, `sound(secured)`.
- КОЛИ `input(action)` → ЯКЩО `state(level, secured)` → ТО `win`, `next_level`; без закріплення X нічого не робить.
- КОЛИ `input(action)` → ЯКЩО `level(==, 17)` → ТО `message(«The End. Thanks for playing!»)` замість переходу (лише коли рівень закріплено); далі кожне X — `message(«...»)`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі ящики незрушні з досяжної області + X/Enter. · Поразки нема; стан, де ящик уже не закріпити, — лише undo/рестарт. · Рахунку нема.

## Керування і ввід
- WASD або стрілки — крок; Z — undo; R — рестарт; X або Enter — «далі» після розвʼязання; Esc — до вибору рівнів / меню; M — звук.
- Мобільна версія (dario-zubovic.github.io) — та сама гра для тач-екранів.

## Вікна, меню, HUD
- `main-menu` PuzzleScript: назва й автор.
- `level-select` з блокуванням нерозвʼязаних (`level_select_lock`): секції «1/17» … «17/17»; повтор розвʼязаних рівнів.
- `tutorial-window`: перед 1-м рівнем — «Press X to proceed after solving a level.»
- `game-screen`: лише поле, без HUD; сигнал досягнення мети — ящики стають «закріпленими» зі звуком.
- `end-screen`: у 17-му рівні «The End. Thanks for playing!»
- Переходи: меню → вибір рівня → рівень → (закріплено + X) наступний рівень; Esc → вибір рівня.

## Фічі поза полем
- `undo` без ліміту, `restart-level` (R).
- `level-unlock` + `level-select`: розвʼязані рівні відкриті для повтору.
- `save-progress` у браузері (коментатор: у Firefox розвʼязані рівні не зʼявлялись у виборі).
- `sound-toggle` (M); власний піксельний шрифт.
- Нема підказок, редактора, рахунку.

## Варіації й родичі
- Нереалізовані ями: автор згадує невикористані рівні з ямою внизу сирців; Stingby12 зробив 6 фанатських концептів. У сирцях — ідеї: яма, що знищує ящики й заповнюється; тимчасовий слід, яким себе блокуєш; «кулька», що відскакує від стіни.
- Родичі: [Sokoban](../push-slide/sokoban.md) — той самий поштовх, протилежна мета; [Understand](understand.md) і [Linelith](linelith.md) — правило відкриваєш сам; [Baba Is You](baba-is-you.md) — мета як змінна частина гри.
- **Осі варіацій**: мета Sokoban-рівня — ящики на цілях / гравець на виході / **жоден ящик не рушить** (Secure) · мета названа / прихована, гра лише сигналізує досягнення · поштовх — один ящик / ряд · спецклітини — непрохідні для всіх / лише для ящиків (платформа).

## Цікавинки для курсу
- Заливка досяжних клітин від гравця після кожного ходу — 📎 (BFS по сітці).
- Перемога «жоден ящик не можна штовхнути з досяжної області» — 🥉 (BFS + перевірка 4 напрямків для кожного ящика).
- Прихована мета з сигналом досягнення (ящики міняють вигляд, X — підтвердження) — 🌱.
- Клітина, прохідна для гравця й непрохідна для ящика (платформа) — 🌱.
- Розвʼязувач BFS по станах «гравець + ящики» до глобального предиката «усе закріплено» — 🥈.
- Узагальнення до повної перевірки «ящик ніколи не зрушить» (класичний аналіз deadlock-ів Sokoban) — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ WASD/стрілки; `push-object` ↔ поштовх одного ящика; `impassable-cells` ↔ стіни (для всіх) і платформи (лише для ящиків); `reachability-check` ↔ заливка від гравця; `deadlock-detection` ↔ перевірка «ящик незрушний» (тут це мета); `completion-detection` ↔ закріплення всіх ящиків; `undo-redo` + `undo-unlimited` + `restart-level`; `sequential-levels` + `level-select` + `level-unlock` + `save-progress`; `level-from-txt` ↔ ASCII-рівні; `idle-animation` ↔ «дихання» гравця; `event-effects` ↔ перелив ящика й перетворення на закріплені; `sound-effects`.
- **Нема** → пропозиції карток:
  - `+immobilize-all-goal` «Перемога: жоден обʼєкт не можна зсунути» · game-logic/win · 🥉 · слот {scope: reachable | global}.
  - `+confirm-to-win` «Мету досягнуто — гра сигналізує, гравець підтверджує клавішею» · game-logic/win · 🌱.
  - `+rule-discovery` (уже в корпусі) — мету не названо, її виводять із реакції гри.

## Пропозиції до словників
- `+cond:pushable` — обʼєкт можна зсунути з досяжної для гравця клітини (Secure; родич `free` + `path_exists`).
- `+axis:rules-discovered` — нове значення для осі-кандидата `rules` (`fixed` · `unlocked` · `switchable`): мету не сказано, її виводять із реакції гри (Secure; у understand.md — як `+axis:rules-known`).
- `+card:immobilize-all-goal`, `+card:confirm-to-win` — див. вище.

## Джерела
- ⭐ [itch.io: Secure](https://toombler.itch.io/secure) — опис «mysterious goal», керування, PuzzleScript, теги; коментарі: 17 рівнів, «reverse sokoban», важкі 11/14/15, невикористані рівні з ямою.
- [Gist із сирцями](https://gist.github.com/Toomber/57084dce3c309bd2f57e5c2bb301fa02) — OBJECTS / LEGEND / RULES: поштовх, платформа, руйнована стіна, заливка `FillMarker`, `CrateCannotBePushed` → `WonCrate`, X для перемоги, фінал «The End»; 17 секцій і коментарі автора про групи рівнів.
- [Мобільна версія](https://dario-zubovic.github.io/PuzzleScript/play.html?p=57084dce3c309bd2f57e5c2bb301fa02) — гра й сирці (посилання автора).
- [Corey Hardt: Worth your time — Secure](https://coreyhardt.wordpress.com/2021/11/26/worth-your-time-secure/) — огляд: «compact, elegant, simple», мету не розкриває.
- [Stingby12: Secure Pit Levels Concepts](https://github.com/Stingby12/Secure-Pit-Levels-Concepts/blob/main/Full%20code) — фанатські рівні з ямою (лінк зі сторінки itch, не відкривав).
- YouTube: пошук «Secure Toombler puzzlescript».

## Непевне
- (?) Рік: gist створено 31.07.2021, коментарі на itch — «близько пʼяти років тому»; дату публікації на itch сторінка не показує.
- (?) Руйнована стіна є в правилах, але в 17 рівнях не стоїть — схоже на лишок ідей; у грі не перевірено.
- (?) Прапорці `level_select`, `custom_font` — з форка PuzzleScript (схоже на PuzzleScript Plus), не з оригінального puzzlescript.net.
- (?) Тач-керування мобільної версії — з підпису «mobile-friendly», не перевірено.
