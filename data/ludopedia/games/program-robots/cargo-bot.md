---
title: Cargo-Bot
slug: cargo-bot
aka: [CargoBot, Cargo Bot]
family: program-robots
also: [thinky]
klass: avatar
axes:
  field: 1d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2012
platforms: [iPad]
links:
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cargo-bot+gameplay", best: true, note: "пошук; геймплей і розвʼязки (гра сама вміє записувати їх у відео)"}
  - {kind: official, url: "https://apps.apple.com/app/id519690804", note: "App Store: Two Lives Left, безкоштовно, v1.0 від 21.04.2012, запис розвʼязків"}
  - {kind: other, url: "https://thenextweb.com/news/cargo-bot-the-first-game-coded-entirely-on-the-ipad-shows-a-promising-future-for-tablet-creation", note: "TNW 2012: Rui Viana, Codea, перша гра, написана на iPad"}
  - {kind: other, url: "https://talk.codea.io/t/cargo-bot-help/4747", note: "форум Codea: модифікатори-кольори, none/rainbow, prog 1 стартує, стек викликів"}
  - {kind: other, url: "https://www.148apps.com/cargo-bot/cargobot-ipad-game-ipad-codea/", note: "огляд: кран, 4 програми, умови за станом ящика"}
stage: v1
coverage: 70
mechanics: [command-program, user-procedures, step-execution, code-editor-window, drag-drop-piece, sequential-levels, level-unlock, level-select, game-screen, end-screen, tutorial-window, save-progress, +crane-stack-columns, +conditional-held-item, +call-stack, +recursion-loop, +command-slots-limit, +stars-by-program-size, +goal-state-preview, +solution-video-record]
proposes: ["+effect:grab", "+effect:release", "+cond:held(a, kind|value)", "+cond:held_any", "+cond:held_none", "+effect:call(fn)", "+effect:stack_push(v)", "+ui:goal-preview", "+ui:program-slots", "+ui:command-palette", "+ui:condition-tabs", "+feature:stars-by-size", "+feature:solution-video"]
author: opus
date: 2026-11-09
---

# Cargo-Bot — запрограмуй кран, щоб переставити ящики в стовпчиках у цільову розкладку

## Суть
Над рядом стовпчиків з кольоровими ящиками їздить кран із клешнею. Гравець складає програму з іконок: вліво, вправо, вниз (взяти/поставити ящик) і виклики програм; кожну команду можна «пофарбувати» умовою — виконати лише тоді, коли в клешні ящик певного кольору, будь-який ящик або нічого. Програм кілька, вони викликають одна одну й самі себе, тож цикли — це рекурсія, а умови «що в клешні» — єдине розгалуження. Мета — привести стовпчики до показаної цільової розкладки; зірки дають за коротку програму. Першу гру, повністю написану на iPad у Codea (Rui Viana, Two Lives Left, 2012).

## Поле і час
- Поле — ряд позицій (стовпчиків) під рейкою крана: по суті 1D-лінія, у кожній позиції — стек ящиків (останній покладений — зверху). Кількість позицій і висота стеків залежать від рівня (?).
- Кран один, рухається лише вздовж рейки; «вниз» опускає клешню на верх стовпчика і повертає її вгору.
- Над полем — зображення цільової розкладки (goal).
- Час `programmed`: команда = один крок анімації; є прискорення (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кран з клешнею | player | позиція, вміст клешні (ящик кольору c / нічого) | виконує команди програми; тримає ≤ 1 ящик |
| Стовпчик (позиція) | container | стек ящиків | приймає/віддає лише верхній ящик |
| Ящик | object | колір (червоний, зелений, синій, жовтий… (?)) | переноситься краном; поставлений лягає на верх стовпчика |
| Ціль (goal) | mark | розкладка всіх стовпчиків | перемога, коли поточна розкладка збіглась |
| Програма 1…4 | — (програма) | N слотів на рядок (?) | Prog 1 — точка входу; інші — процедури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `program_end` (Prog 1 відпрацювала без зупинки) → ЯКЩО розкладка ≠ цілі → ТО `custom: «спроба невдала, програму можна правити»`.
- КОЛИ `exec(right)` → ЯКЩО `custom: «праворуч є позиція»` → ТО `move(crane, east)`; інакше `crash` (?).
- КОЛИ `exec(left)` → ЯКЩО `custom: «ліворуч є позиція»` → ТО `move(crane, west)`; інакше `crash` (?).
- КОЛИ `exec(down)` → ЯКЩО `not custom: «клешня тримає ящик»` і `custom: «у стовпчику є ящики»` → ТО `custom: «взяти верхній ящик»`.
- КОЛИ `exec(down)` → ЯКЩО `custom: «клешня тримає ящик»` → ТО `custom: «поставити ящик на верх стовпчика»` (`place`).
- КОЛИ `exec(prog k)` → ТО `custom: «покласти адресу повернення на стек викликів, виконати Prog k, повернутись»` — самовиклик дає цикл.
- КОЛИ `exec(cmd)` → ЯКЩО на команді модифікатор кольору c → ТО виконати лише при `custom: «у клешні ящик кольору c»`; інакше пропустити.
- КОЛИ `exec(cmd)` → ЯКЩО модифікатор «none» → ТО виконати лише при порожній клешні.
- КОЛИ `exec(cmd)` → ЯКЩО модифікатор «rainbow» → ТО виконати при будь-якому ящику в клешні.
- КОЛИ `custom: «розкладка стовпчиків збіглася з ціллю»` → ТО `win`, `window(end-screen)` з зірками (навіть посеред нескінченної рекурсії (?)).
- КОЛИ `win` → ТО `custom: «зірки 1–3 за кількістю команд у програмі»`.
- Обмеження: кількість слотів у кожній програмі фіксована — ліміт змушує виносити повтори в процедури.
- Перемога: ціль досягнута · Поразка: нема, лише невдала спроба або аварія крана (?) · Рахунок: зірки за розмір програми (не за кількість рухів крана).

## Керування і ввід
- Тач: перетягнути іконку команди з панелі інструментів (toolbox) у слот програми; перетягнути кольорову «вкладку»-умову на команду; витягти команду зі слоту — видалити.
- Кнопки: Play (запуск з Prog 1), Stop/Reset, швидкість/крок (?).
- Прямого керування краном нема.

## Вікна, меню, HUD
- `main-menu` → `level-select`: набори рівнів за складністю (Tutorial, Easy, … (?)), у кожному — рівні з позначкою зірок.
- `game-screen`: поле з краном і стовпчиками; `goal-preview` — мініатюра цілі; `program-slots` Prog 1–4; `command-palette` (toolbox) з командами й `condition-tabs`; `instruction-highlight` під час виконання; кнопки Play/Stop.
- `tutorial-window` — підказки перших рівнів (?).
- `end-screen` — зірки за розвʼязок, далі/повторити; запис розвʼязку у відео й публікація на YouTube.
- Переходи: level-select → game-screen → (ціль) end-screen → наступний рівень / назад.

## Фічі поза полем
- `levels-sequential`, `level-unlock` всередині наборів; `stars-rating` за коротку програму (3 зірки — найменше команд, часто з нескінченною рекурсією).
- `save-progress` — збережені програми й зірки (?).
- `replay` / запис відео розвʼязку → YouTube.
- Hint-кнопка з підказкою кількості команд (?).
- Безкоштовна, без покупок (App Store).

## Варіації й родичі
- Порти й клони: Windows 10 «CargoBot» (?), веб-клони й шкільні версії (?).
- Родичі в корпусі: [Lightbot](lightbot.md) (той самий каркас слотів і процедур, умова за кольором робота), [RoboZZle](robozzle.md) (умова за кольором клітини, F1–F5), [Karel](karel.md), [Opus Magnum](opus-magnum.md) і [SpaceChem](spacechem.md) (маніпулятор «схопити/відпустити»), класичні «Ханойські вежі» й задача сортування стеків.
- **Осі варіацій**: де умова (вміст клешні / колір актора / колір клітини / сенсор) · поле (лінія стеків / 2D-сітка / висоти) · оцінка (зірки за розмір / за рухи / за час) · цикл (лише рекурсія / окремий repeat).

## Цікавинки для курсу
- Модель «лінія стеків + кран з одним слотом» — 🌱.
- Інтерпретатор 4 програм зі стеком викликів, рекурсією і захистом від нескінченності (ліміт кроків) — 🥈.
- Модифікатори-умови на кожній команді (колір / none / rainbow) — 📎.
- Перевірка цілі після кожного кроку (перемога посеред нескінченного циклу) — 🌱.
- Зірки за розмір програми + пошук мінімальної програми перебором — 🥇.
- Анімація крана й ящиків (опустити, підняти, переїхати) — 🥉.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ програма крана; `user-procedures` ↔ Prog 2–4 і рекурсія; `step-execution` ↔ підсвітка команди; `code-editor-window` ↔ слоти й toolbox; `drag-drop-piece` ↔ перетягування іконок; `sequential-levels`/`level-unlock`/`level-select`; `game-screen`, `end-screen`, `tutorial-window`; `save-progress`.
- **Нема** → пропозиції карток:
  - `+crane-stack-columns` «Кран над рядом стеків: бере/кладе верхній» · entities/interact · 🌱.
  - `+conditional-held-item` «Команда виконується за вмістом клешні/руки» · game-logic/program · 📎.
  - `+call-stack` «Стек викликів процедур» · game-logic/program · 🥉 (уже є у RoboZZle).
  - `+recursion-loop` «Цикл через самовиклик» · game-logic/program · 🥈 (Lightbot, RoboZZle).
  - `+command-slots-limit` «Ліміт слотів програми» · game-logic/constraints · 📎.
  - `+stars-by-program-size` «Зірки за довжину програми» · game-logic/score · 🌱.
  - `+goal-state-preview` «Мініатюра цільового стану поля» · interface/hud · 🌱.
  - `+solution-video-record` «Запис розвʼязку у відео» · interface/results · 🥈.

## Пропозиції до словників
- `+effect:grab` / `+effect:release` — узяти/відпустити обʼєкт маніпулятором (SpaceChem, Opus Magnum).
- `+cond:held(a, kind|value)` — що тримає сутність (пропонували 7 Billion Humans, Opus Magnum); `+cond:held_any` / `+cond:held_none` — «будь-що» і «нічого».
- `+effect:call(fn)` — виклик процедури зі стеком повернення (RoboZZle).
- `+effect:stack_push(v)` — тут для стека викликів.
- `+ui:goal-preview` — мініатюра цілі; `+ui:program-slots` · `+ui:command-palette` · `+ui:condition-tabs` (кольорові вкладки-умови на командах).
- `+feature:stars-by-size` · `+feature:solution-video`.

## Джерела
- ⭐ YouTube: пошук «cargo-bot gameplay» — розвʼязки рівнів, у т. ч. записані самою грою.
- [App Store: Cargo-Bot](https://apps.apple.com/app/id519690804) — опис, Two Lives Left, безкоштовна, запис розвʼязків, історія версій (1.0 — 21.04.2012).
- [TNW 2012](https://thenextweb.com/news/cargo-bot-the-first-game-coded-entirely-on-the-ipad-shows-a-promising-future-for-tablet-creation) — Rui Viana, 4 місяці розробки в Codea, «procedural puzzle-solver».
- [Codea forum: Cargo Bot help](https://talk.codea.io/t/cargo-bot-help/4747) — модифікатори кольорів, none і rainbow, prog 1 стартує, стек викликів.
- [148Apps](https://www.148apps.com/cargo-bot/cargobot-ipad-game-ipad-codea/) — кран, до 4 програм, умови за станом ящика.

## Непевне
- (?) Кількість рівнів: один опис (у результатах пошуку) каже «6 рівнів по 6 пазлів», з tutorial та easy — назви решти наборів не перевірено.
- (?) Кількість слотів у програмах (один опис: «4 рядки, разом 29 команд») — не звірено.
- (?) Що буває при виїзді за край і при «down» на порожній стовпчик з порожньою клешнею — аварія чи no-op.
- (?) Набір кольорів ящиків, межа висоти стовпчика, прискорення/крок, кнопка-підказка.
- (?) Чи перевіряється ціль після кожного кроку (перемога посеред нескінченної рекурсії) — так пишуть гравці про 3-зіркові розвʼязки з нескінченними циклами, але механізм не перевірено.
- (?) Звʼязок Windows-версії «CargoBot» з оригіналом.
- ⭐ — пошуковий URL YouTube: окремого відео не відкривав, Wikipedia-статті нема.
