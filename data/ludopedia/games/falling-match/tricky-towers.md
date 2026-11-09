---
title: Tricky Towers
slug: tricky-towers
aka: []
family: falling-match
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: race
year: 2016
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/437920/", best: true, note: "опис: 3 режими, до 4 гравців локально/онлайн, 17+ заклять, випробування, турніри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tricky_Towers", note: "фізика замість рядів, півклітинний крок, режими Race/Survival/Puzzle, 18 заклять світлої/темної магії"}
  - {kind: official, url: "https://www.trickytowers.com/", note: "3 режими, до 4 гравців, 50 випробувань"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tricky+towers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, piece-rotate-flip, keyboard-controls, simultaneous-versus, online-multiplayer, ai-opponent, mode-select, character-select, event-effects, leaderboard, score-records, sequential-levels, game-pause, end-screen, next-queue, +rigid-body-stacking, +no-line-clear, +fall-off-penalty, +race-to-height, +spell-light-dark, +half-cell-nudge, +below-line-puzzle]
proposes: ["+trigger:fell_off(a, where)", "+effect:impulse(a, dir)", "+cond:stable(a, t)", "+feature:mode-race", "+axis:physics", "+card:rigid-body-stacking", "+card:spell-light-dark"]
author: opus
date: 2026-11-09
---

# Tricky Towers — тетраміно на фізичній вежі: ряди не зникають, вежа хитається, суперники кидають темну магію

## Суть
Кожен гравець — чарівник, що складає вежу з тетраміно на вузькій платформі. На відміну від Tetris, ряди не очищаються, а фігури — фізичні тіла: вежа хитається, фігури зісковзують і падають униз. Мета залежить від режиму: першим досягти фінішної лінії (Race), поставити задану кількість фігур, не впустивши забагато (Survival), або вмістити якомога більше під лінією (Puzzle). Закляття світлої магії зміцнюють свою вежу, темної — шкодять суперникам.

## Поле і час
- Вільні координати з 2D-фізикою (Unity): платформа-основа, гравітація, тертя, обертальні моменти. Фігура до приземлення рухається з кроком у пів клітини.
- Real-time, кілька веж поруч (до 4 гравців) — кожен гравець має своє поле; камера підіймається за висотою вежі (?).
- Ряди ніколи не очищаються; простір над платформою необмежений, нижче — падіння «в безодню».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура (тетраміно) | player | форма 1 з 7, орієнтація | рухається з кроком ½, обертається, падає повільно або прискорено; після контакту стає фізичним тілом |
| Фігура вежі | object | маса, тертя | фізичне тіло: лежить, ковзає, перекидається, може впасти з вежі |
| Платформа | static | ширина | основа вежі |
| Фінішна лінія | zone | висота | Race: вежа, що стабільно перетнула її, перемагає (?) |
| Лазерна / обмежувальна лінія | zone | висота | Puzzle: фігури мають лишатися під нею |
| Чарівник | neutral | скін | аватар гравця біля вежі; косметичний |
| Закляття світлої магії | pickup | тип | зміцнює свою вежу (захист від темної магії, фіксація фігур (?)) |
| Закляття темної магії | pickup | тип | шкодить вежам суперників: незручна фігура, руйнування, перешкода (?) |
| Подія фізики | zone | тривалість | тимчасово: фігури вдвічі більші, слизькі або падають швидше |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move_left|move_right)` → ЯКЩО `free(target)` → ТО `move(piece, dir)` на ½ клітини.
- КОЛИ `input(rotate)` → ТО `rotate(piece, 90)`.
- КОЛИ `tick` → ТО `fall(piece)` повільно; КОЛИ `input(drop)` → ТО `speed(piece, ×k)`.
- КОЛИ `contact(piece, tower|platform)` → ТО `custom: «фігура стає фізичним тілом; керування переходить до наступної з черги»`.
- КОЛИ `tick` → ТО `custom: «фізичний крок: гравітація, тертя, зіткнення, моменти — вежа хитається»`.
- КОЛИ `custom: «fell_off(piece) — фігура впала нижче платформи»` → ТО `disappear(piece)`; ЯКЩО `mode(survival)` → ТО `lives(-1)` (втрата здоровʼя).
- КОЛИ `counter(lives, ==, 0)` → ТО `lose` (Survival).
- КОЛИ `reach(tower, finish_line)` → ЯКЩО `custom: «вежа стабільна певний час»` → ТО `win` (Race) (?).
- КОЛИ `custom: «фігура перетнула лінію зверху»` → ТО `custom: «кінець спроби»` (Puzzle); рахунок — кількість фігур під лінією.
- КОЛИ `counter(placed, ==, quota)` → ЯКЩО `count(dropped, <, limit)` → ТО `win` (Survival).
- КОЛИ `custom: «гравець отримав закляття»` → ТО `choose` світле (на себе) або темне (на суперника) — `custom: «механізм отримання не перевірено»`.
- КОЛИ `custom: «темне закляття»` → ТО `custom: «шкода вежі суперника / збільшена чи слизька фігура / перешкода»`.
- КОЛИ `custom: «світле закляття»` → ТО `custom: «зміцнення вежі (зчеплення фігур) / захист»` (?).
- КОЛИ `custom: «подія фізики»` → ТО `set_state(pieces, big|slippery|fast, dur)`.
- КОЛИ `level_end` → ТО `counter(points, +n)` переможцю; матч (кубок) — до порогу очок (?).
- Перемога: Race — перша вежа до фінішу · Survival — квота без надмірних падінь · Puzzle — найбільше під лінією. Поразка: Survival — здоровʼя вичерпано.

## Керування і ввід
- Геймпад або клавіатура: ←/→ — зсув на ½, кнопка — поворот, ↓ — прискорене падіння (?). Для локального мультиплеєра потрібні контролери (Steam).
- Ввід лише до контакту фігури; потім вона — у владі фізики.

## Вікна, меню, HUD
- `main-menu`: мультиплеєр (локальний/онлайн), одиночна гра (випробування, режими), налаштування, магазин косметики.
- `mode-select`: Race · Survival · Puzzle.
- `character-select` — вибір чарівника (+ DLC Indie Friends, Spirit Animals) і набору цеглин (Gem, Galaxy, Holographic, Candy).
- `custom: «trials-map»` — 50 випробувань для одного гравця (`level-select`).
- `game-screen`: 1–4 вежі поруч, `next-piece-preview`, фінішна / обмежувальна лінія (`danger-line`), `lives` (Survival), іконки заклять (?).
- `end-screen` раунду й підсумок матчу; `leaderboard` (випробування, одиночні режими).
- `lobby-window` для онлайну; `shop-window` (Points Shop, косметика).

## Фічі поза полем
- `local-multiplayer` до 4 · `online-multiplayer` (PvP) · `mode-versus` · турніри локальні/онлайн (Tournament party pack).
- Одиночна гра: 50 `trials` (умови на рівень, `levels-sequential`), одиночні Survival/Puzzle з рекордом, Race проти AI (з версії Xbox One).
- `achievements`, `leaderboard-online`, `custom-skins` (паки цеглин, чарівники), `localization` (20 мов).

## Варіації й родичі
- Попередники WeirdBeard: 99 Bricks Classic (2009, Kongregate), 99 Bricks Wizard Academy (2014).
- Родичі: Tetris (ті самі тетраміно, але ряди не зникають), Suika Game (фізика замість сітки), Jenga-подібні стекінг-ігри.
- **Осі варіацій**: поле (сітка / фізика) · ряди (очищаються / ні) · мета (виживання / висота-гонка / щільність під лінією) · втручання суперника (сміття / закляття) · крок руху (клітина / пів клітини).

## Цікавинки для курсу
- Тетраміно як тверді тіла (pymunk/Box2D) з падінням зі стека — 🥉 (готовий солвер, але склеювання форм і стабільність).
- Детекція «вежа стабільна N секунд над лінією» — 📎.
- Три режими на одному двіжку (гонка, квота з життями, щільність під лінією) — 📎.
- Система заклять світла/темрява з вибором цілі — 🥉.
- Тимчасові події фізики (більші, слизькі, швидші фігури) — 🌱.
- Онлайн до 4 гравців із синхронізацією фізики — 👑 (детермінізм фізики між клієнтами).

## Мапа на каталог
- Є: `gravity-fall` · `piece-rotate-flip` · `keyboard-controls` · `simultaneous-versus` · `online-multiplayer` · `ai-opponent` · `mode-select` · `character-select` · `event-effects` (події фізики) · `leaderboard` · `score-records` · `sequential-levels` (випробування) · `game-pause` · `end-screen` · `next-queue`.
- **Нема** → пропозиції карток:
  - `+rigid-body-stacking` «Складання фізичних фігур» · entities/move · 🥉.
  - `+no-line-clear` «Ряди не очищаються» · game-logic/rules · 🌱 (варіант-перемикач для Tetris-подібних).
  - `+fall-off-penalty` «Штраф за фігуру, що впала з поля» · game-logic/score · 🌱.
  - `+race-to-height` «Гонка до висоти» · game-logic/win · 📎 · слоти {height, hold_time}.
  - `+spell-light-dark` «Закляття: на себе або на суперника» · game-logic/opponent · 🥉.
  - `+half-cell-nudge` «Рух з кроком у пів клітини» · entities/move · 🌱.
  - `+below-line-puzzle` «Максимум фігур під лінією» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:fell_off(a, where)` — сутність впала за межу поля/платформи (≠ `edge`: тут через фізику, не рух гравця).
- `+effect:impulse(a, dir)` — фізичний поштовх тілу (спільне з Suika; темна магія).
- `+cond:stable(a, t)` — тіло/структура нерухома не менше t (фініш Race).
- `+feature:mode-race` — режим «першим до цілі» у versus.
- `+axis:physics` — фізичне поле `rigid` (підтримую пропозицію з Suika).
- `+card:rigid-body-stacking`, `+card:spell-light-dark` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Tricky Towers](https://store.steampowered.com/app/437920/) — 3 режими, до 4 гравців локально й онлайн, 17+ заклять (темні — шкодять, захисні — бережуть свою вежу), випробування, турніри, паки цеглин, 20 мов.
- [Wikipedia: Tricky Towers](https://en.wikipedia.org/wiki/Tricky_Towers) — ряди не очищаються, фігури падають з вежі, крок ½, події (подвійний розмір, слизькі, швидше), Race/Survival/Puzzle, 18 заклять, платформи, 99 Bricks.
- [trickytowers.com](https://www.trickytowers.com/) — 50 випробувань, 4 гравці.

## Непевне
- (?) Назви й точні ефекти 18 заклять (памʼять: ліани, що скріплюють вежу; збільшена фігура; блискавка, що руйнує фігуру; туман) — у відкритих джерелах не названі, fandom віддав 402, один WebSearch нічого не дав.
- (?) Як отримуються закляття (за кількість поставлених фігур / за висоту) і скільки можна тримати.
- (?) Кількість життів у Survival, правило «стабільність N секунд» на фініші Race, система очок кубка — з памʼяті.
- (?) Розкладка кнопок, камера за висотою вежі, наявність `next-piece-preview` у HUD.
