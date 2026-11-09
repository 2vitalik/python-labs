---
title: Quixo
slug: quixo
aka: [Квіксо]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1995
platforms: [board, Ludii]
links:
  - {kind: other, url: "https://ludii.games/details.php?keyword=Quixo", best: true, note: "Ludii: 25 кубиків з колом, хрестиком і 4 порожніми гранями; береш з краю, засуваєш у ряд; 5 у лінію; Thierry Chapeau, Gigamic, 1995"}
  - {kind: other, url: "https://www.ultraboardgames.com/quixo/game-rules.php", note: "правила: не з тим самим місцем, свій символ догори, чужу лінію склав — програв, пропуску ходу нема"}
  - {kind: other, url: "https://www.ultraboardgames.com/quixo/four-player-rules.php", note: "правила на 4: команди навпроти, «вістря» на кубику вказує, хто з пари може його брати"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tic-tac-toe_variants#Quixo", note: "Quixo серед варіантів хрестиків-нуликів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Generalized_game", note: "узагальнений Quixo — EXPTIME-complete (Mishiba, Takenaga 2020)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Quixo+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [legal-move-highlight, selection-highlight, cell-click, drag-drop-piece, hover-highlight, hot-seat, turn-enforcement, ai-opponent, ai-minimax, last-move-highlight, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +line-win, +insert-shift, +edge-pick, +no-return-spot, +opponent-line-loss, +team-play, +win-line-highlight]
proposes: ["+cond:not_origin", "+trigger:line_for_opponent", "+ui:push-arrows", "+ui:win-line", "+ui:team-pointer", "+feature:team-2v2", "+card:insert-shift", "+card:edge-pick", "+card:opponent-line-loss"]
author: opus
date: 2026-11-09
---

# Quixo — береш кубик з краю, ставиш своїм знаком догори й засуваєш у ряд з іншого кінця, зсуваючи весь ряд; 5 у лінію

## Суть
Хрестики-нулики 5×5, де нічого не ставиться на порожнє: поле від початку заповнене 25 кубиками з порожньою гранню догори. Хід — узяти з периметра порожній або свій кубик, повернути своїм знаком (коло / хрестик) догори і засунути назад у будь-який кінець ряду чи стовпця, що утворив отвір, зсунувши решту на одну. Повертати в те саме місце не можна, чужі кубики брати не можна. Хто склав 5 своїх у лінію, виграв; склав лінію суперника — програв, навіть якщо одночасно склав свою. Thierry Chapeau, Gigamic, 1995.

## Поле і час
- Квадрат 5×5, завжди повний (25 кубиків); периметр — 16 клітин (підрахунок).
- Стан клітини: порожня грань / коло / хрестик (на 4 — ще й напрям «вістря»).
- Отвір після взяття кубика лежить на периметрі; засувати можна з кінця того ж рядка або стовпця, але не в саме місце взяття. Отже, кутовий кубик має 2 варіанти, крайовий не кутовий — 3 (підрахунок за правилом).
- Хід = одна вставка; пропустити хід не можна (на 4 — лише коли нема жодного дозволеного кубика).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик | tile | грань: blank / X / O; на 4 — вістря | береться з краю, повертається знаком гравця, засувається в ряд |
| Периметр | zone | 16 клітин | лише звідси береться кубик |
| Ряд / стовпець отвору | zone | 5 клітин | зсувається на 1 у бік отвору, коли кубик засувають з протилежного кінця |
| Лінія з 5 | zone | рядок, стовпець або діагональ | 5 однакових знаків — кінець гри |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: усі 25 кубиків порожньою гранню догори; гравці обирають знак і хто ходить першим.
- КОЛИ `input(pick, cube)` → ЯКЩО `cell(cube, edge)` and (`state(cube, blank)` or `state(cube, own)`) → ТО `take(player, cube)`; інакше `block`. У першому раунді доступні лише порожні.
- КОЛИ `input(pick, cube)` → ЯКЩО `state(cube, opponent)` → ТО `block`.
- КОЛИ `after(take)` → ТО `set_side(cube, own)` — знак гравця догори, навіть якщо вже був свій.
- КОЛИ `input(push, line_end)` → ЯКЩО `custom: «кінець ряду або стовпця, що містить отвір»` and `custom: «не те саме місце, звідки взято»` (`+cond:not_origin`) → ТО `shift(line, toward_hole)`, `place(cube, line_end)`.
- КОЛИ `after(shift)` → ЯКЩО `pattern(line(5), own)` and `not pattern(line(5), opponent)` → ТО `win`.
- КОЛИ `after(shift)` → ЯКЩО `pattern(line(5), opponent)` (`+trigger:line_for_opponent`) → ТО `lose` — навіть якщо склалась і своя лінія.
- КОЛИ `turn_start(side)` → ТО хід обовʼязковий: `pass_turn` заборонено.
- 4 гравці: КОЛИ `input(pick, cube)` → ЯКЩО `state(cube, own_team)` and `custom: «вістря кубика спрямоване на мене»` → ТО дозволено; після вставки гравець сам задає напрям вістря (собі чи партнерові). Хід — за годинниковою стрілкою; команди сидять навпроти; чи можна радитись — домовляються наперед.
- Перемога: 5 своїх знаків у рядку, стовпці чи діагоналі (і оголосити) · Поразка: створити лінію суперника · Рахунок: нема.

## Керування і ввід
- Настільна: витягти кубик з краю, повернути, засунути з торця ряду — ряд фізично зсувається.
- (цифрова версія) Клік по кубику периметра → підсвітка 2–3 `push-arrows` на кінцях доступних рядів → клік по стрілці; або drag кубика до торця ряду. Анімація зсуву ряду.
- 4 гравці: після вставки — поворот вістря (кнопкою або drag).

## Вікна, меню, HUD
- `main-menu` (цифрова версія): 2 гравці / 4 гравці (команди) / проти AI.
- `settings-window`: складність AI, хто першим, тема кубиків.
- `game-screen`: поле 5×5 з кубиками, `selection-highlight` взятого, `push-arrows`, `legal-move-highlight` (доступні кубики периметра), `turn-indicator`, `last-move-highlight` (зсунутий ряд), `win-line` наприкінці; на 4 — `team-pointer` (вістря).
- `end-screen`: переможець і виграшна лінія, або «склав лінію суперника — поразка».
- `help-window`: правила, включно з поразкою за чужу лінію.
- Переходи: main-menu → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels` — Ludii (загальні AI двіжка).
- `mode-versus` 1 на 1 і `team-2v2` — режими гри одним набором.
- `hotseat`; `rules-page`.
- Нагороди: Mensa Select (Wikipedia — список лауреатів), Games 100 (Wikipedia — список).

## Варіації й родичі
- «N у лінію» — [line-games](line-games.md) (гомоку, Pente-подібні) і [pente](pente.md); Quixo — поле завжди повне, лінія змінюється зсувом.
- Зсув ряду вставкою з краю — родич [labyrinth](../board-digital/labyrinth.md) (плитка засувається з краю), [shobu](shobu.md) (штовхання каменя), [abalone](abalone.md) (штовхання ряду); «засунути з краю» в падаючих — Connect 4 (`+column-drop` у line-games).
- Того ж видавця — [quarto](../board-digital/quarto.md) (Gigamic) (?), Pylos.
- Командна гра 2×2 з «вістрям»-адресатом — рідкість: дозвіл на хід кодується в самій фігурі.
- Осі варіацій: **розмір поля** (5×5 / більше — EXPTIME-complete узагальнення) · **звідки брати** (лише периметр / будь-звідки) · **заборона повернення** (те саме місце / тієї ж стороною) · **чужа лінія** (поразка / нічия / не рахується).

## Цікавинки для курсу
- Генерація ходів: 16 кубиків периметра × 2–3 торці, фільтр «свій або порожній», заборона «те саме місце» — 🌱.
- Зсув ряду/стовпця з вставкою на кінці (`deque.rotate`-подібно, але з заміною) — 🌱.
- Перевірка 12 ліній 5×5 після кожного ходу з пріоритетом «чужа лінія → поразка» — 🌱.
- Режим 2×2 з вістрям-адресатом: стан кубика = знак + напрям — 📎.
- AI: розвʼязати 5×5 ретроградним аналізом (3^25 станів з симетріями й бітмасками) — 👑 (?) — або minimax з альфа-бета для гри — 🥇.

## Мапа на каталог
- Є: `legal-move-highlight`, `selection-highlight`, `hover-highlight`, `last-move-highlight` · `cell-click`, `drag-drop-piece` · `hot-seat`, `turn-enforcement`, `ai-opponent`, `ai-minimax` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `state-as-data`, `unit-tests`.
- **Нема** → пропозиції карток:
  - `+line-win` (див. line-games.md).
  - `+insert-shift` «Вставити фігуру з торця ряду, зсунувши ряд на 1» · entities/move · 📎 · слоти {from: perimeter, forbid_origin: true} (сусід `row-conveyor`, але зсув — наслідок вставки, а не рух смуги).
  - `+edge-pick` «Брати фігуру лише з периметра» · entities/legality · 🌱.
  - `+no-return-spot` «Не можна повернути туди, звідки взяв» · entities/legality · 🌱.
  - `+opponent-line-loss` «Склав лінію суперника — програв» · game-logic/lose · 🌱.
  - `+team-play` (є в сімʼї) — 2×2 навпроти.
  - `+win-line-highlight` — підсвітка виграшної лінії (див. `+ui:win-line` у line-games).

## Пропозиції до словників
- `+cond:not_origin` — ціль ходу не збігається з місцем, звідки взято фігуру.
- `+trigger:line_for_opponent` — хід склав шаблон на користь суперника (Quixo, «самогубні» лінії).
- `+ui:push-arrows` — стрілки на торцях рядів, куди можна засунути; `+ui:win-line` (уже пропонувалось у line-games); `+ui:team-pointer` — напрям вістря на кубику (кому з команди можна).
- `+feature:team-2v2` — командний режим двох пар за одним полем.
- `+card:insert-shift`, `+card:edge-pick`, `+card:opponent-line-loss` — див. «Мапа на каталог».

## Джерела
- ⭐ [Ludii: Quixo](https://ludii.games/details.php?keyword=Quixo) — компоненти (25 кубиків: коло, хрестик, 4 порожні), взяття з периметра порожнього або свого, вставка в ряд, лінія з 5; Thierry Chapeau, Gigamic, 1995.
- [UltraBoardGames: правила Quixo](https://www.ultraboardgames.com/quixo/game-rules.php) — перший раунд лише порожні, свій знак догори, вибір торця, заборона того ж місця, поразка за лінію суперника, без пропуску ходу.
- [UltraBoardGames: Quixo на 4](https://www.ultraboardgames.com/quixo/four-player-rules.php) — команди навпроти, за годинниковою, «вістря» кубика, ті самі заборони, поразка команди за чужу лінію.
- [Wikipedia: Tic-tac-toe variants](https://en.wikipedia.org/wiki/Tic-tac-toe_variants#Quixo) — Quixo як варіант хрестиків-нуликів 5×5 для 2 гравців або команд.
- [Wikipedia: Generalized game](https://en.wikipedia.org/wiki/Generalized_game) — узагальнений Quixo EXPTIME-complete (Mishiba, Takenaga 2020).

## Непевне
- (?) Що 5×5 Quixo розвʼязано (нічия при ідеальній грі) — з памʼяті (статті ~2020), не перевіряв; тому 👑 у «Цікавинках» із (?).
- (?) Quarto і Pylos як ігри Gigamic — з памʼяті (і з quarto.md, де теж (?)).
- (?) Чи кут дає рівно 2 варіанти вставки — висновок з правила «будь-який торець ряду з отвором, крім місця взяття», в джерелах прямо не сказано.
- (?) Wikipedia (список Game of the Year) пише видавцем 1995 року Great American Trading Company — бачив лише у сніпеті пошуку Вікіпедії; Ludii — Gigamic.
- (?) Онлайн-платформи (BGA, застосунки) не перевіряв — у шапці лише board і Ludii.
