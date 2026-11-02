---
title: NMBR 9
slug: nmbr-9
family: board-digital
also: [word-number]
klass: cursor
axes:
  field: layers
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2017
platforms: [board, web]
links:
  - {kind: other, url: "https://yucata.de/en/Rules/Nmbr9", best: true, note: "повні правила: рівень 0, опора ≥2 плиток без звисів і дірок, рахунок число × рівень"}
  - {kind: play, url: "https://yucata.de/en/Rules/Nmbr9", note: "Yucata — грати онлайн (система роздає числа замість карт)"}
  - {kind: other, url: "https://fgbradleys.com/wp-content/uploads/rules/nmbr9%20-%20rules.pdf", note: "рулбук (PDF)"}
  - {kind: other, url: "https://www.meeplelikeus.co.uk/nmbr-9-2017/", note: "рецензія: правила, «пасьянс на всіх», хатні правила"}
  - {kind: other, url: "https://opinionatedgamers.com/2017/04/20/dale-yu-review-of-nmbr9/", note: "рецензія Dale Yu"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=NMBR+9", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=NMBR+9+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, event-points, completion-detection, score-records, game-settings, +polyomino-placement, +piece-rotate-flip, +named-resource-all-place, +simultaneous-turns, +stacking-support, +level-multiplier-scoring, +connected-placement, +card-deck-sequence]
proposes: ["+effect:place", "+cond:fits", "+cond:supported", "+cond:covers_n", "+cond:adjacent_same_level", "+trigger:deck_empty", "+role:supply", "+ui:called-tile", "+ui:level-view", "+ui:support-highlight", "+ui:score-preview", "+window:round-summary", "+axis:turn-structure", "+axis:field-bounds", "+card:stacking-support", "+card:level-multiplier-scoring"]
author: opus
date: 2026-11-02
---

# NMBR 9 — цифри-поліоміно, складені в піраміду: очки = цифра × поверх, але лише на повній опорі

## Суть
Колода з 20 карт (кожна цифра 0–9 двічі) відкривається по одній; **усі** гравці одночасно беруть плитку названої цифри й кладуть у свою власну споруду на столі. Плитка — поліоміно у формі цифри. Класти можна на стіл (рівень 0, зʼєднано з іншими) або **зверху** — лише повністю на плитки нижче, без звисів і дірок, і перекриваючи щонайменше дві плитки. Плитка рахує `цифра × рівень`: на столі — 0. Ядро — 3D-пакування: будуєш широку основу, щоб велика девʼятка стала на третій поверх.

## Поле і час
- Поле необмежене: квадратна сітка на столі, без меж, у кількох **шарах** (рівень 0, 1, 2, …). Клітина шару — порожня або зайнята квадратом плитки.
- Плитка — поліоміно цифри (0–9) з квадратів сітки; повертається довільно (90°), але лише цифрою догори (без дзеркала).
- Хід = одна відкрита карта; усі кладуть одночасно. 20 ходів, кінець — після вичерпання колоди.
- Гравці не взаємодіють: спільний лише порядок цифр.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-цифра | tile | значення 0–9, форма-поліоміно | кладеться на рівень L; не рухається після |
| Рівень (шар) | zone | номер L ≥ 0 | множник очок плиток цього шару |
| Карта числа | supply | 20 = 2 × (0–9) | відкривається по одній, задає цифру ходу |
| Запас плиток | supply | 80 = 8 × (0–9) на коробку; по 2 кожної цифри на гравця | звідси береш плитку названої цифри |
| Споруда гравця | zone | набір шарів | лише власна; обмежень розміру нема |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(round)` → ТО `custom: «відкрити верхню карту — цифру d»`.
- КОЛИ `custom: «цифру названо»` → ТО кожен гравець `input(place(tile(d), rot, level, cells))`; одночасно, обовʼязково.
- Перша плитка: `place` будь-де на рівень 0.
- КОЛИ `place(tile, level 0)` → ЯКЩО `fits(tile, cells)` and `custom: «принаймні одне ребро квадрата торкається плитки рівня 0»` → ТО `place`; інакше `block`.
- КОЛИ `place(tile, level L ≥ 1)` → ЯКЩО `supported(every square)` (під кожним квадратом — квадрат рівня L−1, без звисів і дірок) and `covers_n(tiles_below, ≥ 2)` → ТО `place`; інакше `block`.
- ЯКЩО на рівні L вже є плитки → ТО нова плитка рівня L теж мусить торкатися ребром плитки цього рівня; перша плитка рівня — без цієї умови.
- Можна класти на будь-який легальний рівень, не обовʼязково найвищий; плитку після покладення не рухають.
- КОЛИ `deck_empty` → ТО підрахунок: `score(+value × level)` для кожної плитки; рівень 0 — 0.
- Перемога: найбільша сума; нічия — спільна перемога. Соло — на рекорд (100+ — «відмінно»).

## Керування і ввід
- Цифрова версія: drag-n-drop плитки на сітку, обертання клавішею/колесом; наведення показує примару плитки і чи легальна позиція (зелена/червона).
- Перемикач видимого рівня або ізометричний вид — щоб бачити, що під плиткою.
- Одночасний хід: чекати, доки всі поклали; Yucata — система сама роздає числа.

## Вікна, меню, HUD
(цифрова версія — Yucata)
- `match-setup`: 1–4 гравці.
- `game-screen`: своя споруда (вид згори з тінню рівнів або `level-view` — вибір шару); `called-tile` — поточна цифра; `remaining-counter` — скільки карт лишилось; `support-highlight` — квадрати, що не мають опори; `score-preview` — поточний рахунок; `opponent-boards`.
- `round-summary` / `end-screen`: розклад рахунку по рівнях (Σ цифр × рівень), переможець.
- `help-window`: правило опори з прикладами «звис / дірка / одна опора».
- Переходи: match-setup → game-screen ×20 → end-screen.

## Фічі поза полем
- Соло на рекорд (`score-records`, `leaderboard-local`).
- Хатні правила: перемішати колоду вдруге для 2 гравців, ланцюг соло-партій (Meeple Like Us).
- `seed-input` — природна фіча цифрового клону: та сама послідовність цифр для всіх / щоденна (?).
- Undo в межах ходу до підтвердження — цифрова зручність (?).

## Варіації й родичі
- Родичі «одне називається — всі кладуть»: Take It Easy (гекси), Tiny Towns (ресурси), Cartographers (форми), Railroad Ink.
- Родичі поліоміно: Blokus, Patchwork, Tetris; родичі шарів і опори: Hive (жук на вежі), Jenga, Mahjong-пасьянс (шари), Santorini (поверхи).
- **Осі варіацій**: геометрія (плоско / шари з опорою / 3D-вокселі) · правило опори (кожен квадрат / центр мас / ≥ N плиток знизу) · множник очок (рівень / висота² / лише верх) · хто обирає фігуру (колода для всіх / драфт / свій вибір).

## Цікавинки для курсу
- Поліоміно-цифри з поворотами на необмеженій сітці — 🥉.
- Шари з перевіркою «кожен квадрат має опору, дві різні плитки знизу» — 🥈 (3D-масив або словник рівнів + ідентифікатори плиток).
- Зʼєднаність у межах рівня (торкання ребром) — 📎.
- Рахунок `value × level` — 🌱.
- Ізометричний рендер або перемикач шарів у консолі — 🥉.
- AI, що максимізує очікуваний рахунок за рештою колоди (20 ходів, відомий склад) — 👑.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `event-points` · `completion-detection` · `score-records` · `game-settings`.
- **Нема** → пропозиції карток:
  - `+polyomino-placement` (як Blokus/Patchwork) · `+piece-rotate-flip` (тут лише поворот, без дзеркала).
  - `+named-resource-all-place` (як Tiny Towns) · `+simultaneous-turns` (як Cartographers).
  - `+stacking-support` «Кладка поверхом вище на повній опорі» · entities/legality · 🥈 · слоти {min_tiles_below: 2, overhang: false}.
  - `+level-multiplier-scoring` «Очки = значення × рівень» · game-logic/score · 🌱.
  - `+connected-placement` (як Kingdomino/Sagrada) — тут у межах шару.
  - `+card-deck-sequence` «Колода задає порядок фігур для всіх» · levels/generation · 🌱 · слот {deck: 2×(0–9)}.

## Пропозиції до словників
- `+cond:supported` — уже 🔥 у conditions; тут — під кожним квадратом плитки є квадрат на рівні нижче.
- `+cond:covers_n(tiles_below, n)` — плитка спирається на ≥ n різних плиток (NMBR 9).
- `+cond:adjacent_same_level` — торкається ребром плитки того ж рівня.
- `+trigger:deck_empty` — колоду вичерпано → кінець (NMBR 9; родич `+trigger:board_full` з Take It Easy).
- `+effect:place` · `+cond:fits` · `+role:supply`.
- `+ui:called-tile` (як Take It Easy) · `+ui:level-view` — вибір/перемикання видимого шару · `+ui:support-highlight` — квадрати без опори · `+ui:score-preview` · `+window:round-summary`.
- `+axis:turn-structure` = `simultaneous` · `+axis:field-bounds` = `unbounded` (як Hive).
- `+card:stacking-support` · `+card:level-multiplier-scoring`.

## Джерела
- ⭐ [Yucata: NMBR 9 rules](https://yucata.de/en/Rules/Nmbr9) — 80 плиток (8 × 0–9), 20 карт, правила рівня 0 і вищих (повна опора, ≥2 плитки, без звисів і дірок), рахунок, кінець.
- [Рулбук (PDF, fgbradleys)](https://fgbradleys.com/wp-content/uploads/rules/nmbr9%20-%20rules.pdf).
- [Meeple Like Us](https://www.meeplelikeus.co.uk/nmbr-9-2017/) — Peter Wichmann, 2017, 1–4 гравці, хатні правила.
- [Opinionated Gamers: Dale Yu](https://opinionatedgamers.com/2017/04/20/dale-yu-review-of-nmbr9/) — рецензія.
- YouTube: пошук «NMBR 9 how to play».

## Непевне
- (?) Видавці (Abacusspiele — DE, Z-Man Games — EN) — з памʼяті.
- (?) Точні форми плиток-цифр (скільки квадратів у кожній) — не перевірено; PDF рулбука не відкривав.
- (?) Офіційних цифрових версій (застосунок, Steam, BGA) не знайдено; Yucata — єдиний перевірений онлайн-майданчик.
- (?) Соло-шкала «100+ — відмінно» — з рецензії/пошуку, не з рулбука.
