---
title: Game of the Amazons (Амазонки)
slug: amazons
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: territory
year: 1988
platforms: [board, PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Game_of_the_Amazons", best: true, note: "правила, розстановка, територія і «дефектні» території, складність"}
  - {kind: play, url: "https://playabstractgames.com/en/amazons/", note: "грати в браузері проти AI (10 рівнів)"}
  - {kind: other, url: "http://www.chessvariants.org/other.dir/amazons.html", note: "Chess Variant Pages (лінк зі статті Wikipedia)"}
  - {kind: other, url: "http://www.solitairelaboratory.com/amazons.html", note: "Michael Keller: переклад правил, історія"}
  - {kind: other, url: "https://arxiv.org/abs/cs.CC/0502013", note: "Hearn: Amazons is PSPACE-complete"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=amazons", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=game+of+the+amazons+rules", note: "пошук; правила й партії"}
stage: v1
coverage: 80
mechanics: [piece-move-patterns, impassable-cells, no-moves-left, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-greedy, ai-minimax, cell-click, legal-move-highlight, hover-highlight, drag-drop-piece, game-screen, end-screen, help-window, field-size-picker, replay, reachability-check, +move-then-shoot, +permanent-block, +last-mover-wins, +territory-scoring, +move-notation]
proposes: ["+trigger:move_done", "+effect:place", "+cond:path_clear", "+cond:region", "+ui:phase-indicator", "+ui:territory-overlay", "+axis:turn-structure", "+axis:win-condition", "+card:move-then-shoot", "+card:permanent-block", "+card:last-mover-wins"]
author: opus
date: 2026-11-02
---

# Амазонки — хід королевою, потім постріл стрілою, що назавжди замуровує клітину; програє той, хто перший не зможе сходити

## Суть
Кожна сторона має 4 «амазонки», що ходять як шаховий ферзь. Хід складається з двох фаз: перемістити амазонку, а потім з її нової клітини «вистрілити» стрілою (теж ферзевою лінією) — клітина зі стрілою стає стіною до кінця гри. Взять нема: поле лише заростає стінами, і хто першим не може зробити повний хід — програє. Гра природно переходить у підрахунок територій, як го, і є улюбленим обʼєктом комбінаторної теорії ігор та комп'ютерних олімпіад.

## Поле і час
- Дошка 10×10; білі амазонки a4, d1, g1, j4; чорні a7, d10, g10, j7. Стріли — фішки/жетони (шашки, фішки покера).
- Хід = **дві фази**: рух амазонки → постріл стрілою; обидві обовʼязкові. Білі ходять першими.
- Поле монотонно зменшується: кожен хід додає рівно одну непрохідну клітину → гра триває не більше 92 ходів (100 − 8 амазонок).
- Нічия неможлива.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Амазонка | piece | сторона; 4 на сторону | ходить як ферзь на будь-яку відстань по порожніх клітинах; потім стріляє |
| Стріла | static | — | ставиться пострілом; клітина назавжди непрохідна для амазонок і стріл |
| Порожня клітина | terrain | — | прохідна; стає стрілою або ціллю руху |
| Територія | zone | власник | область, досяжна лише амазонками однієї сторони (після розділення) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move(amazon, to))` → ЯКЩО `turn_of(side)` and `custom: «to на ферзевій лінії»` and `path_clear(from, to)` (нема амазонок і стріл на шляху й у цілі) → ТО `move(amazon, to)`; фаза → «постріл».
- КОЛИ `move_done(amazon)` → ТО `custom: «обовʼязковий постріл з нової клітини»`.
- КОЛИ `input(shoot(cell))` → ЯКЩО `custom: «cell на ферзевій лінії від амазонки»` and `path_clear(amazon, cell)` → ТО `place(arrow, cell)`, `set_cell(cell, wall)`, `end_turn`. Стріляти можна і назад, через клітину, з якої щойно пішла амазонка.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` (жодна амазонка не має руху з подальшим пострілом) → ТО `lose(side)`.
- Ендшпіль: коли всі амазонки розділені стрілами на ізольовані області (`region`), гру зазвичай зупиняють і рахують — у кожного стільки ходів, скільки (майже) клітин у його територіях; більший запас перемагає.
- «Дефектна» територія: ходів менше, ніж клітин (найпростіше — три клітини «кутом», амазонка в середині).
- Перемога: останній, хто зміг сходити · Поразка: нема легального ходу на початку свого ходу · Рахунок (неофіційно): різниця запасів ходів у територіях.

## Керування і ввід
- Два кліки/drag на хід: вибрати амазонку → клітина руху; потім клік по клітині пострілу (клієнт підсвічує ферзеві лінії вже з нової позиції).
- Undo фази «рух» до пострілу — природно в цифровій версії (?).
- Нотація: `d1-d7/g7` — рух і клітина стріли (?).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): дошка 10×10, `legal-move-highlight` (для руху, потім для пострілу), `phase-indicator` («рухай» / «стріляй»), `turn-indicator`, `player-clock`, `move-list`, `territory-overlay` (розфарбування областей у ендшпілі).
- `match-setup` / `settings-window`: розмір дошки, рівень AI, колір (Play Abstract Games: 10 рівнів AI).
- `help-window`: правила.
- `end-screen`: хто не зміг сходити, підсумок територій.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `ai-opponent-levels` (браузерні клієнти), `hotseat`, `online-multiplayer` (сайти абстрактних ігор), `replay` партії.
- `custom-difficulty`: менші дошки (6×6, 8×8) для навчання й аналізу (?).
- Computer Olympiad — щорічні турніри програм; гра — класичний полігон для оцінки позицій (mobility, territory).

## Варіації й родичі
- Розміри дошки й кількість амазонок (менші — для навчання й розвʼязання) (?).
- Родичі: Isolation / «Isola» (рух + знищення клітини) (?), Quoridor (рух або стіна) [quoridor.md](quoridor.md), го (територія) [go.md](go.md), Tron (поле заростає слідом).
- **Осі варіацій**:
  - **Структура ходу**: рух · рух **або** блок (Quoridor) · рух **і** блок (Amazons) · рух лишає слід (Tron).
  - **Звідки ставиться блок**: від фігури по лінії (стріла) · будь-куди · на клітину, з якої пішов.
  - **Кінець**: нема ходів = поразка (нормальна гра, CGT) · нема ходів = перемога (місер).

## Цікавинки для курсу
- Двофазний хід (рух → постріл) з обома фазами в одному ході й скасуванням першої — 📎.
- Ферзева лінія з перевіркою чистого шляху, двічі за хід, з урахуванням щойно звільненої клітини — 🌱.
- `no_moves` як єдина умова кінця: перевірка «чи є хоч один рух+постріл» — 📎.
- Розділення поля на регіони (flood fill) + підрахунок територій для раннього завершення — 🥉.
- AI: розгалуження ~2 000+ ходів на початку; оцінка за мобільністю/«хто ближче до клітини» (BFS-відстані ферзем) — 🥇 (?).
- Точний підрахунок ходів у дефектній території = гамільтонів шлях — 👑 (NP-hard, Buro 2000).

## Мапа на каталог
- Є: `piece-move-patterns` ↔ ферзевий рух · `impassable-cells` ↔ стріли · `no-moves-left` ↔ програш · `hot-seat` · `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-greedy` / `ai-minimax` · `cell-click` + `legal-move-highlight` + `hover-highlight` + `drag-drop-piece` · `game-screen` · `end-screen` · `help-window` · `field-size-picker` · `replay` · `reachability-check` ↔ розділення територій.
- **Нема** → пропозиції карток:
  - `+move-then-shoot` «Рух, потім дія з нової клітини» · game-logic/opponent · 📎 · слоти {action: shoot|build|place} — Amazons; родич `+move-or-build` (Quoridor).
  - `+permanent-block` «Клітина блокується назавжди» · entities/legality · 🌱 — стріла як стіна до кінця гри.
  - `+last-mover-wins` «Виграє той, хто сходив останнім» · game-logic/win · 🌱 — дзеркало `no-moves-left`.
  - `+territory-scoring` (з go.md) — підрахунок ізольованих областей.
  - `+move-notation` — запис двофазного ходу.

## Пропозиції до словників
- `+trigger:move_done` — підтверджую (з ataxx.md): після руху амазонки відкривається фаза пострілу.
- `+effect:place` — постріл кладе стрілу на клітину.
- `+cond:path_clear(a, b)` — пряма лінія між клітинами вільна (ферзь, тура, стріла); ≠ `path_exists` (будь-який шлях) і ≠ `line_of_sight` (тут — для руху, з урахуванням ще не завершеного ходу).
- `+cond:region(cell)` — клітина належить області, досяжній лише однією стороною.
- `+ui:phase-indicator` — підказка, яка фаза ходу зараз (рух/постріл, рух/дроп).
- `+ui:territory-overlay` — підтверджую (з go.md).
- `+axis:turn-structure` — значення `compound` (кілька обовʼязкових фаз в одному ході).
- `+axis:win-condition` — значення `last-mover` (нормальна гра CGT).

## Джерела
- ⭐ [Wikipedia: Game of the Amazons](https://en.wikipedia.org/wiki/Game_of_the_Amazons) — розстановка, хід + постріл, «останній, хто сходив, виграє», дефектні території, складність (NP-hard ендшпіль, PSPACE-complete), Computer Olympiad.
- [Play Abstract Games: Amazons](https://playabstractgames.com/en/amazons/) — коротко правила, гра проти AI з 10 рівнями.
- [Chess Variant Pages: Amazons](http://www.chessvariants.org/other.dir/amazons.html) — правила й історія (лінк зі статті Wikipedia).
- [Solitaire Laboratory: El Juego de las Amazonas](http://www.solitairelaboratory.com/amazons.html) — Michael Keller, переклад правил 1994.
- [Hearn: Amazons is PSPACE-complete](https://arxiv.org/abs/cs.CC/0502013) — для тих, хто хоче теорії.
- YouTube: пошук «game of the amazons rules».

## Непевне
- (?) Формат нотації `d1-d7/g7`, менші дошки 6×6/8×8 як навчальні варіанти, Isola як родич — з памʼяті.
- (?) Оцінка розгалуження ~2 000 ходів на старті й популярні евристики AI (queen/king distance) — з памʼяті про літературу.
- (?) Undo фази руху до пострілу в конкретних клієнтах не перевірено.
