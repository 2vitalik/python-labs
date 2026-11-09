---
title: Wordbase
slug: wordbase
aka: [wordbase.app, Word Base]
family: word-number
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: setup
  goal: race
year: 2014
platforms: [iOS, Android, web (фан-ремейк 2021)]
links:
  - {kind: play, url: "https://wordbase.app", best: true, note: "фан-ремейк закритого оригіналу (Cyrus Freshman, 2021): грати локально або онлайн, інвайт-лінки, чат, email-сповіщення, статистика"}
  - {kind: other, url: "https://www.androidpolice.com/2014/06/03/new-game-wordbase-is-a-strategic-game-of-vocabulary-vengeance/", note: "Android Police, червень 2014: «гігантський word hunt», слова в будь-якому напрямку з діагоналями, ланцюг на територію суперника, блокування, power-ups, free + premium"}
  - {kind: other, url: "https://www.levelwinner.com/?p=156", note: "поради: «Capture the Flag, а не Scrabble», дві доріжки до бази, блокувати, цінність Q/X/Z, короткі слова"}
  - {kind: other, url: "https://alternativeto.net/software/wordbase--strategic-word-game/about/", note: "Hattrick Ltd; програєш, якщо суперник узяв хоч одну літеру твоєї бази; прорізати ланцюги; power-ups за зібрані літери; чат; гра знята з усіх платформ"}
  - {kind: other, url: "https://www.producthunt.com/products/wordbase-app", note: "ремейк: «the first player to reach the opponent's side wins», будувати базу й відрізати плитки суперника"}
  - {kind: itch, url: "https://uh-software.itch.io/wordbase", note: "сторінка ремейку: оригінал закрився через гроші; режими local / online"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wordbase+word+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-click, path-drawing, word-validation, turn-enforcement, async-multiplayer, online-multiplayer, hot-seat, game-screen, end-screen, +claim-by-word, +word-reuse-ban, +base-row-race, +cut-off-disconnected, +async-match-list]
proposes: ["+role:base", "+cond:path_adjacent", "+card:base-row-race", "+card:cut-off-disconnected"]
author: opus
date: 2026-11-09
---

# Wordbase — склади слово-шлях від своєї бази, захопи його клітини й першим дотягнися до бази суперника

## Суть
Двоє гравців по черзі складають слова на спільному полі літер, як у word hunt (Boggle): літери слова — ланцюжок сусідніх клітин у будь-якому напрямку, з діагоналями. Слово має рости від твоєї території, а його клітини стають твоїми — так «доріжка» повзе до протилежного краю. Хто першим захопить хоч одну літеру бази суперника — виграв; слово можна провести крізь чужий ланцюг і відрізати його від бази. Ядро — Letterpress (`letterpress.md`) + геометрія шляху й гонка, «шахи словами».

## Поле і час
- Прямокутне поле випадкових літер; на протилежних краях — бази двох гравців (базовий ряд свого кольору). Розмір у джерелах не названо (?).
- Шари: літера (незмінна) + власник клітини (нейтральна / моя / суперника) + бонусна клітина (?).
- Хід = одне слово; онлайн-партія з чергою ходів (оригінал — проти людей і друзів, ремейк — локально або онлайн).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера, власник none / A / B | стає моєю, коли входить у моє слово (зокрема чужа) |
| База гравця | zone | ряд на своєму краю поля | джерело території; втрата хоч однієї її літери = поразка |
| Ланцюг / територія | zone | звʼязна множина плиток одного кольору від бази | з неї стартують нові слова |
| Бонусна плитка (power-up) | pickup | — | дає перевагу при захопленні (бомба (?)) |
| Гравець A / B | player | колір | ходять по черзі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag path)` → ЯКЩО `custom: «перша літера — моя плитка (база або звʼязана з нею територія)»` (?) → ТО `custom: «шлях продовжується лише в сусідню клітину з 8 і не повертається на вже взяту в цьому слові»`.
- КОЛИ `input(submit)` → ЯКЩО `not in_dictionary(word)` → ТО `message`, `block`.
- КОЛИ `input(submit)` → ЯКЩО `custom: «цю послідовність літер ти вже грав у цій партії»` → ТО `message`, `block`.
- КОЛИ `input(submit)` → ЯКЩО слово валідне → ТО `set_side(word_tiles, me)` — і нейтральні, і чужі плитки; `end_turn`.
- КОЛИ `after(set_side)` → ЯКЩО `not connected(opponent_tiles)` з його базою → ТО `custom: «відрізані плитки суперника втрачені (стають нейтральними?)»` (?) — «cut off your opponent's tiles».
- КОЛИ `custom: «слово захопило бонусну плитку»` → ТО `custom: «power-up: додаткове захоплення навколо»` (?).
- КОЛИ `reach(my_tiles, opponent_base)` → ТО `win` — суперник утратив літеру бази.
- Перемога: першим захопити літеру бази суперника · Поразка: суперник захопив твою · Рахунку очок нема (гонка, не підрахунок).

## Керування і ввід
- Провести пальцем шлях по сусідніх літерах (як у Boggle-подібних), відпустити — подати слово (?); повторне торкання / відхід назад скасовує (?).
- Хід лише у свою чергу; у ремейку — інвайт-лінк другу, чат у партії, email про хід.

## Вікна, меню, HUD
- `game-screen`: поле з кольорами двох гравців, бази на краях, слово, що складається, кнопка подати (?).
- `game-list` (?): список партій «твій хід / їхній» — як у Letterpress; запрошення друга або випадковий суперник.
- `chat-box` у партії (оригінал і ремейк); `stats-window` у ремейку.
- `end-screen`: перемога / поразка, реванш (?).

## Фічі поза полем
- `async-multiplayer` / `online-multiplayer` з друзями й незнайомими; ремейк — ще й `local-multiplayer` на одному пристрої.
- Free + premium («кілька доларів»), in-app покупки (Android Police).
- `chat`, `invite-link`, `stats` (ремейк).

## Варіації й родичі
- Letterpress (`letterpress.md`) — слово з будь-яких літер, захоплення й захист оточенням; Wordbase додає шлях і гонку до краю.
- Boggle (`boggle.md`), SpellTower (`spelltower.md`), Squaredle (`squaredle.md`) — той самий шлях по сусідніх клітинах, без суперника.
- Hex / шахи (`chess-abstract`) — гонка до протилежного краю й блокування.
- **Осі варіацій:** звідки старт слова (будь-де / лише від своєї території) · що з чужими плитками (перефарбувати / не чіпати) · відрізані плитки (лишаються / зникають) · мета (більше плиток / дотик до краю).

## Цікавинки для курсу
- Перевірка шляху: сусідство з 8, без повторів клітини, старт від своєї території — 🌱.
- Після ходу — BFS від бази кожного гравця, усе незвʼязне втрачає власника — 📎 («відрізати» = flood fill).
- Перемога дотиком до ряду бази — 🌱.
- AI: перебір шляхів-слів (trie + DFS по сітці) з оцінкою «наскільки ближче до бази суперника і скільки його плиток відрізано» — 🥇.
- Асинхронні партії, інвайт-лінк і чат (як у ремейку на MERN) — 🥈.

## Мапа на каталог
- Є: `cell-click` / `path-drawing` ↔ шлях по сусідніх літерах · `word-validation` · `turn-enforcement` · `async-multiplayer` / `online-multiplayer` · `hot-seat` ↔ локальна гра в ремейку · `game-screen` · `end-screen`.
- Вже запропоновано в `letterpress.md`: `+claim-by-word`, `+word-reuse-ban`, `+async-match-list`.
- **Нема** → пропозиції карток:
  - `+base-row-race` «Перемога дотиком до бази / ряду суперника» · game-logic/win · 🌱.
  - `+cut-off-disconnected` «Плитки, відрізані від бази, втрачаються» · game-logic/constraints · 📎 · слоти {neighbours: 4|8}.

## Пропозиції до словників
- `+role:base` — база гравця на краю поля (є в корпусі).
- `+cond:path_adjacent` — наступна клітина шляху сусідня з попередньою (є в корпусі; тут — 8 напрямків).
- `+card:base-row-race`, `+card:cut-off-disconnected` — див. «Мапа на каталог».

## Джерела
- ⭐ [wordbase.app](https://wordbase.app) — фан-ремейк у браузері (переадресовує на freshman.dev/wordbase; SPA, правил текстом не прочитано).
- [Android Police, 2014](https://www.androidpolice.com/2014/06/03/new-game-wordbase-is-a-strategic-game-of-vocabulary-vengeance/) — суть, напрямки слів, ланцюг на територію суперника, power-ups, онлайн, ціна.
- [LevelWinner: поради](https://www.levelwinner.com/?p=156) — «Capture the Flag», дві доріжки, блокування, рідкісні літери.
- [AlternativeTo](https://alternativeto.net/software/wordbase--strategic-word-game/about/) — Hattrick Ltd, поразка за одну літеру бази, power-ups, чат, гру знято.
- [Product Hunt](https://www.producthunt.com/products/wordbase-app) · [itch.io](https://uh-software.itch.io/wordbase) — ремейк 2021, local / online, інвайт-лінки, чат, сповіщення, статистика.
- YouTube: пошук «wordbase word game gameplay».

## Непевне
- (?) Розмір поля (на памʼять — 10 × 13) і розподіл літер — у відкритих джерелах не названо.
- (?) Чи слово мусить починатись саме з моєї плитки — джерела кажуть «ланцюг тягнеться від бази до території суперника», але правила старту прямо не цитують.
- (?) Що відбувається з відрізаними плитками (стають нейтральними чи зникають) — є лише «cut off your opponent's tiles».
- (?) Power-ups: які саме (бомби, супербомби?) і як діють — Android Police каже лише «power-ups», AlternativeTo — «колекціонування літер дає power-ups».
- (?) Керування жестом, кнопки, `game-list`, реванш — з аналогії з Letterpress, не перевірено; рік виходу iOS-версії — може бути раніший за червень 2014 (AlternativeTo додав гру в січні 2014).
- Згадка в `letterpress.md` «бомби, доріжка до протилежного краю» — з памʼяті того агента; тут підтверджено лише доріжку до бази.
