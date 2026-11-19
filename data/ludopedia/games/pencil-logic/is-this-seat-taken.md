---
title: "Is This Seat Taken?"
slug: is-this-seat-taken
aka: ["Це місце зайняте?"]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2025
platforms: [PC (Windows, macOS, Linux), Nintendo Switch, iOS, Android]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3035120/Is_This_Seat_Taken/", best: true, note: "суть, сцени (кінотеатр, автобус, весілля, таксі), без таймерів; трейлери, демо"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Is_This_Seat_Taken%3F", note: "зірка за рівень, спецрівень світу, 5 світів по 5–6 рівнів, 3–4 секції в рівні, платформи, нагороди"}
  - {kind: other, url: "https://www.thesixthaxis.com/2025/02/14/is-this-seat-taken-preview-a-cosy-puzzler-that-plays-with-the-stress-of-human-interaction/", note: "превʼю: drag-and-drop, картка бажань, таксі, лімузин, автобус з посадкою й висадкою"}
  - {kind: other, url: "https://butwhytho.net/?p=239609", note: "рецензія: до 3 бажань на персонажа, реакція обличчям, незадоволені не блокують прогрес, бонусний рівень"}
  - {kind: other, url: "https://www.followchain.org/?p=74760", note: "проходження: усі типи сцен, стоячі місця, черги, перемикачі кондиціонера, парасоль і ламп"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3035120&count=25", note: "Steam News: демо, патч якості (автозбереження, підтвердження Confirm), огляд RPS"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Is+This+Seat+Taken+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [satisfy-constraints, completion-detection, drag-drop-piece, hover-highlight, sequential-levels, level-unlock, save-autosave, restart-level, pause-menu, confirm-dialog, language-picker, +relation-clues, +trait-aura, +stop-sequence, +environment-toggle, +stars-rating, +bonus-stage, +soft-fail-progress, +reaction-feedback]
proposes: ["+cond:next_to", "+cond:in_front_of", "+ui:wish-card", "+ui:wish-counter", "+ui:stop-progress", "+card:trait-aura", "+card:stop-sequence", "+card:environment-toggle"]
author: opus
date: 2026-11-19
---

# Is This Seat Taken? — розсади фігурки-пасажирів так, щоб кожне бажання про місце й сусідів виконалось

## Суть
Затишний логічний пазл від Poti Poti Studio: гравець рукою-курсором перетягує персонажів-фігурки (кола, квадрати, трикутники) на місця в таксі, автобусі, кінотеатрі, на весіллі тощо. У кожного до трьох бажань: місце біля вікна, сидіти самому, поруч із конкретною людиною, подалі від запаху чи гучної музики; частина бажань — це риси, що заважають сусідам. Це задача розсадки з обмеженнями (як загадка Ейнштейна), де обмеження подані репліками персонажів, а не таблицею.

## Поле і час
- Поле — схема місць сцени згори: ряди сидінь із вікном і проходом, стоячі місця, столи з кріслами, черги, танцмайданчик, рушники на пляжі; суміжність задає сцена (поруч у ряду, навпроти за столом, попереду / позаду в кінотеатрі), тому `field: graph`.
- Біля сцени — зона очікування (тротуар, зупинка), звідки беруть персонажів.
- Рівень поділено на 3–4 секції (зупинки): після Confirm частина персонажів виходить, приходять нові, решта лишається на місцях.
- Без таймерів і таблиць рекордів; 5 світів-міст (Барселона, Брюссель, Лондон, Нью-Йорк, знову Барселона) по 5–6 рівнів і спецрівень у кожному.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | piece | імʼя, тег (напр. «Kid»), 1–3 бажання | перетягується на місце; обличчям і реплікою показує, чи задоволений |
| Місце | zone | тип: біля вікна / прохід / кінець ряду / стояче / за столом / на сцені | вміщує одного персонажа |
| Бажання про місце | static | «window seat», «I need to be on stage», «I need a computer» | перевіряє тип місця або предмет біля нього |
| Бажання про людину | static | «I want to be with my parent Riley» | перевіряє, хто сидить поруч |
| Риса-джерело | static | «I forgot to shower», гучна музика, балачки, великий капелюх | робить незадоволеними чутливих сусідів (запах, сон, огляд позаду) |
| Предмет сцени | static | попкорн, страва на тарілці, компʼютер, багаж | частина бажань привʼязана до нього |
| Перемикач середовища | switch | кондиціонер (потяг), парасоля (пляж), лампа з комахами (пікнік) | змінює, кому де комфортно |
| Зупинка | zone | номер секції | після Confirm — висадка й нові пасажири |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, p, s)` → ЯКЩО `free(s)` → ТО `move(p, s)`, `sound(drop)`.
- КОЛИ `input(drag, p, s)` → ЯКЩО `occupied(s, q)` → ТО `swap(p, q)` (?).
- КОЛИ `input(hover, p)` → ТО `custom: «картка внизу: імʼя, тег і список бажань із галочками»`.
- Біля вікна / у проході: ЯКЩО `cell(seat(p), window)` / `cell(seat(p), aisle)`.
- Сам: ЯКЩО `custom: «сусідні місця порожні або p у кінці ряду»`.
- Поруч із людиною (батько, партнер): ЯКЩО `in_range(p, q, 1)` (`+cond:next_to`).
- Чутливий до запаху: ЯКЩО `not in_range(p, smelly, 1)`; сонний: ЯКЩО `not in_range(p, noisy, 1)` — балакун будить сусіда, що спить.
- Кінотеатр: ЯКЩО `custom: «прямо попереду p не сидить персонаж у великому капелюсі»` (`+cond:in_front_of`); любитель попкорну — ЯКЩО `in_range(p, popcorn_holder, 1)`.
- Предмет: ЯКЩО `custom: «біля місця p є потрібна річ (страва, компʼютер)»`; на сцені — `cell(seat(p), stage)`.
- КОЛИ `input(toggle, env)` → ТО `set_state(env, on|off)` — кондиціонер, парасоля, лампа; від стану залежать бажання поруч (?).
- КОЛИ `custom: «бажання p виконано»` → ТО `set_state(wish, checked)`, `counter(likes, +1)`, `animate(happy_face)`; інакше `message(complaint)` і кисле обличчя.
- КОЛИ `input(confirm)` → ЯКЩО `custom: «хтось сидить на «не своєму» місці»` → ТО `window(confirm-dialog)`; після згоди — `custom: «наступна зупинка: частина персонажів виходить, нові чекають у зоні очікування»`.
- КОЛИ `level_end` → ЯКЩО `counter(likes, ==, total)` → ТО `custom: «зірка рівня»`; `next_level` — у будь-якому разі.
- КОЛИ `custom: «зібрано всі зірки світу»` → ТО `unlock(special_level)`.
- Перемога: рівень проходиться завжди; зірка — за 100 % бажань у всіх секціях. · Поразка: нема. · Рахунок: лічильник 👍 x/y і зірки.

## Керування і ввід
- Рука-курсор: захопити персонажа й кинути на місце (миша, тач, геймпад із допомогою наведення курсора; є режими «лише миша», «лише клавіатура», «лише тач»).
- Наведення на персонажа — картка бажань; натиснення на перемикач середовища — увімк/вимк.
- Confirm — завершити секцію; пауза — кнопка у кутку.

## Вікна, меню, HUD
- `game-screen`: сцена згори; ліворуч угорі кнопка паузи; угорі — `+ui:stop-progress` (крапки секцій-зупинок); ліворуч унизу — `+ui:wish-card` (імʼя, тег, бажання з галочками); праворуч унизу — блокнот із кнопкою Confirm і `+ui:wish-counter` «👍 x/y ⭐»; репліки персонажів бульбашками.
- `pause-menu`: продовжити, Restart (з підтвердженням), налаштування, вихід (?).
- `confirm-dialog`: Confirm з кимось не на своєму місці; Restart.
- `dialogue-window`: сюжетні сценки з Nat (актор-ромб) між рівнями.
- `level-select` (?): міста-світи з рівнями й зірками, спецрівень світу; вигляд не бачив.
- `settings-window`: 19 мов (з українською), гучність, кольорові альтернативи й «Camera Comfort» (доступність).
- Переходи: вибір рівня → `game-screen` (секція 1) → Confirm → секція 2 … → кінець рівня → наступний рівень; усі зірки світу → спецрівень.

## Фічі поза полем
- `levels-sequential` по містах + `level-unlock` спецрівня за всі зірки (`stars-rating`); бонусні сцени — весілля, пікнік, музей, побачення, пляж.
- `autosave` посеред рівня: вихід і повернення на ту саму зупинку (патч якості 2025).
- `restart-level` з паузи; без таймерів, рахунку й таблиць — «no-pressure».
- `localization` (19 мов), `colorblind-palette`-подібні «Color Alternatives», `touch-controls`, `gamepad-support`, `achievements` (Steam).
- Демо: Барселона — 5 рівнів і спецрівень.

## Варіації й родичі
- Задача розсадки з відношеннями — [zebra-puzzle.md](zebra-puzzle.md) (атрибути в таблиці), [murdoku.md](murdoku.md) (люди по кімнатах на сітці), [sherlock.md](sherlock.md) (відношення між рядами).
- Реальна «задача розсадки гостей» (wedding seating problem) — та сама модель: граф місць + бажані й небажані пари.
- **Осі варіацій**: простір — ряди / столи / черги / вільні точки · бажання — про тип місця / про сусіда / про предмет / риса, що діє на інших · рівень — одна розсадка / кілька зупинок із переносом · ціна невиконання — блок / лише без зірки.

## Цікавинки для курсу
- Модель «граф місць + бажання як предикати» з перевіркою кожного бажання й галочками на картці — 📎.
- Риси-джерела, що діють на сусідів (запах, шум, капелюх закриває огляд позаду) — 📎: перевірка залежить від двох персонажів і геометрії сцени.
- Кілька зупинок з переносом стану: хтось виходить, нові приходять, розсадка лишається — 🥉.
- Перемикачі середовища як частина розвʼязку (кондиціонер, парасолі) — 📎.
- Розвʼязувач розсадки бектрекінгом із відсіканням за бажаннями — 🥈; генератор сцени з єдиною повною розсадкою — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `completion-detection` ↔ усі бажання виконано; `drag-drop-piece` ↔ рука-курсор; `hover-highlight` ↔ картка під курсором; `sequential-levels`, `level-unlock` ↔ міста й спецрівні; `save-autosave` ↔ збереження посеред рівня; `restart-level`, `pause-menu`, `confirm-dialog`; `language-picker` ↔ 19 мов.
- **Нема** → пропозиції карток:
  - `+relation-clues` (повтор: zebra-puzzle, murdoku, sherlock) — бажання «поруч із …», «подалі від …».
  - `+trait-aura` «Риса персонажа впливає на сусідів» · entities/interact · 📎 · слот {range: next|front|row}.
  - `+stop-sequence` «Рівень із кількох зупинок: висадка, нові пасажири, розсадка лишається» · levels/progression · 🥉.
  - `+environment-toggle` «Перемикач середовища змінює вимоги персонажів» · entities/interact · 📎.
  - `+stars-rating` (повтор) · `+bonus-stage` (повтор) — спецрівень за всі зірки світу.
  - `+soft-fail-progress` «Іти далі можна з невиконаними обмеженнями; нагорода — лише за все» · levels/progression · 🌱.
  - `+reaction-feedback` «Обличчя й репліка персонажа показують стан обмеження» · interface/hud · 🌱.

## Пропозиції до словників
- `+cond:next_to` — двоє на сусідніх місцях (повтор із zebra-puzzle і murdoku).
- `+cond:in_front_of` — місце прямо попереду (кінотеатр, черга, фото).
- `+ui:wish-card` — картка персонажа з бажаннями й галочками; `+ui:wish-counter` — «👍 x/y ⭐»; `+ui:stop-progress` — крапки зупинок рівня.
- `+card:trait-aura`, `+card:stop-sequence`, `+card:environment-toggle` — див. мапу.

## Джерела
- ⭐ [Steam: Is This Seat Taken?](https://store.steampowered.com/app/3035120/Is_This_Seat_Taken/) — суть, сцени, «no timers or leaderboards», трейлери, демо; скриншоти таксі, автобуса (картка «Albert · Kid: I forgot to shower / I want to be with my parent Riley», лічильник 10/39), весілля, вечірки.
- [Wikipedia](https://en.wikipedia.org/wiki/Is_This_Seat_Taken%3F) — зірка за рівень, спецрівень світу, 5 світів, 3–4 секції, платформи, нагороди (BAFTA Family, IGF).
- [TheSixthAxis, превʼю](https://www.thesixthaxis.com/2025/02/14/is-this-seat-taken-preview-a-cosy-puzzler-that-plays-with-the-stress-of-human-interaction/) — drag-and-drop, картка бажань, таксі, лімузин (по 2 бажання), автобус із посадкою й висадкою.
- [But Why Tho, рецензія](https://butwhytho.net/?p=239609) — до 3 бажань, реакції, невиконання не блокує, бонусний рівень, платформи.
- [Followchain, проходження](https://www.followchain.org/?p=74760) — сцени, стоячі місця, черги літака, перемикачі середовища, бонусні рівні.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3035120&count=25) — демо (Барселона), патч якості, фікс «балакун не будив сонного», огляд RPS (попкорн, ковбойські капелюхи).
- YouTube: пошук «Is This Seat Taken gameplay».

## Непевне
- (?) Чи кидок на зайняте місце міняє персонажів місцями — «swapping seats» в огляді GamingOnLinux, механіки не бачив.
- (?) Повний перелік типів бажань і рис — відомі лише приклади з оглядів і скриншотів.
- (?) Чи перемикачі середовища (кондиціонер, парасолі, лампи) вмикає гравець, чи їхній стан задає секція — проходження каже лише «можна ввімкнути / вимкнути на етапі».
- (?) Вигляд екрана вибору рівнів і паузи, є чи нема undo.
- (?) Версія для PlayStation — сторінка PS Store є в результатах пошуку, не відкривав; Wikipedia її не називає.
