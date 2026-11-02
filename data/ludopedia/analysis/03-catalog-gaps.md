# 03 · Прогалини каталогу завдань — пропозиції карток з корпусу

`2026-11-02` · корпус: **~230 ігор** · джерела чисел — [index/mechanics.md](../index/mechanics.md) (теги `+` у шапках) і [index/harvest.md](../index/harvest.md) (рядки «`+slug` «Назва» · зона · монетка» із секцій «Мапа на каталог»). Чернетки карток у форматі `tasks.yaml` — **[03-cards-draft.yaml](03-cards-draft.yaml)** (117 карток, усі ✍️, slug-и без колізій з наявними 209; злиття — копіювання потрібних рядків у `data/catalog/tasks.yaml` під ту саму зону/підзону й `catalog_io.py import`).

## Як читати цифри

Два незалежні лічильники на одну пропозицію: (а) скільки ігор поставили тег `+slug` у `mechanics` (широке «ця механіка тут є»), (б) скільки ігор виписали картку в «Мапі на каталог» із зоною й монеткою (вужче «це варто окремої картки»). Для рішення важливіший (б), для частоти механіки у світі — (а). Поріг — правило трьох по (а).

## Топ прогалин (а ≥ 6)

| `+картка` | (а) тегів | (б) карток | Куди | Ціна | Чому важливо |
|---|---|---|---|---|---|
| `undo-redo` | **41** | 18 | game-logic/save → підзона `history` | сімʼя 📎/🥉/🌱/🥈 | у третині ігор; у каталозі лише `editor-undo`. Undo — один із найкорисніших навчальних патернів (стек станів, команда/відкат) |
| `world-map` | 12 | 9 | levels/progression | 🥉 | прогресія вузлами замість списку рівнів |
| `chain-reaction` | 10 | 4 | game-logic/score | 🥉 | каскади match-3, ланцюги Puyo, детонації — алгоритмічне ядро сімʼї падаючих |
| `permadeath` | 10 | — | game-logic/lose | 🌱 | роглайки, Fire Emblem; пара до `player-death` з життями |
| `seed-share` | 10 | — | game-logic/save (history) | 📎 | відтворюваний рівень за seed — дешево, навчально (random.seed) |
| `dig-terrain` | 8 | — | entities/interact | 📎 | Boulder Dash-лінія: копання як окрема дія, не рух |
| `move-notation` | 8 | — | game-logic/save (history) | 🥉 | запис ходів, перегляд, експорт — фігурні |
| `wrap-edges` | 8 | 7 | entities/move | 🌱 | тор — Pac-Man, Life, Labyrinth |
| `code-editor-window` · `step-execution` · `command-program` · `user-procedures` · `sensor-predicates` | 7 / 7 / 6 / 4 / 4 | — | **нова підзона game-logic/program** | 🥈 / 📎 / 🥉 / 🥈 / 🥉 | цілий клас ігор (Karel, Lightbot, RoboRally, 7BH, Farmer Was Replaced), якого в таксономії курсу нема — див. 04 |
| `extra-life-threshold` | 7 | 5 | game-logic/score | 🌱 | аркадна класика; слот {every} |
| `tile-rotate` | 7 | 5 | entities/state | 🌱 | орієнтація плитки як стан + поворот як хід |
| `item-identification` | 6 | — | entities/state | 📎 | роглайки: невідоме до використання |
| `leftover-penalty` | 6 | — | game-logic/score | 🌱 | настолки: мінус за залишок |
| `line-match-clear` | 6 | 3 | entities/interact | 📎 | Lines 98, Dr. Mario |
| `unit-xp-skills` (`pilot-xp-skills`) | 6 | — | entities/state | 🥉 | юніт росте: FE, ITB, Wesnoth |
| `polyomino-placement` | 6 | — | entities/legality | 🥉 | Blokus, Patchwork, Rampart, Tiny Towns |
| `roll-off-rounded` | 6 | — | entities/move | 📎 | Boulder Dash: камінь скочується з округлого |
| `solve-into-undo` | 6 | — | — | — | деталь Tatham (розвʼязок як хід в undo-ланцюгу) — у картку не йде, це нотатка до `undo-redo` |
| `tower-placement` · `tower-range` | 6 / 5 | — | entities/combat | 🥉 / 📎 | TD-сімʼя: у каталозі TD представлений лише через `pvz-lite` |
| `wall-follower` | 6 | 2 | entities/move | 🥉 | жук Chip's Challenge, світлячок Boulder Dash; слот {side} |
| `word-validation` | 6 | — | game-logic/constraints | 🥉 | словесні: словник, пошук |

Далі (а = 4–5): `button-toggle`, `cascade-gravity`, `coverage-area`, `dot-mark`, `edge-marking`, `explode-3x3`, `fill-hole`, `fog-of-war`, `garbage-attack`, `height-levels`, `hunger-clock`, `neighbor-count-clue`, `one-way-cell`, `path-cut`, `piece-rotate-flip`, `repetition-draw`, `share-result`, `state-string`, `streak-stats`, `beam-tracing`, `carrier-platform`, `destructible-blocks`, `entity-rotate`, `level-password`, `line-of-sight-attack`, `mirror-reflect`, `move-limit`, `multi-select`, `next-queue`, `no-guess-generation`, `party-switch`, `pass-turn`, `pawn-promotion`, `pipe-connectors`, `rule-variants`, `run-relics`, `single-loop-check`, `stairs-levels`, `status-effects`. Усі — у YAML-чернетці з зоною й ціною.

## Структурні пропозиції (не окремі картки)

1. **Підзона `game-logic/history` «Історія ходів»** — undo/redo/rewind/restart, нотація ходів, seed, код стану, replay. Зараз ці речі розмазані між `save` і `results`; корпус показує, що це окремий, дуже частий вимір (undo 54 ігри, replay 26, seed 20, notation 8).
2. **Підзона `game-logic/program` «Програма гравця»** — для класу program-robots (див. 04: пропозиція пʼятого класу `programmed`). Картки: програма команд, процедури, сенсори, покрокове виконання, FSM-програма, редактор коду як вікно.
3. **Сімʼя `explosion`** навколо наявної `blast-wave` (хрест): дитина `explode-area` (3×3/радіус) + слот «що лишається» (`into`) — Boulder Dash перетворює вибух у діаманти, Supaplex/XOR — у порожнечу.
4. **Сімʼя `highlights`** в interface/hud: підсвітки виділення/легальних ходів/конфліктів/останнього ходу/досяжності/загрози/телеграфу/шляху — 8 дітей 🌱/📎; зараз є лише `legal-move-highlight` [chess].
5. **Сімʼя `undo-redo`**: `undo-step` 📎 · `undo-unlimited` 🥉 · `redo` 🌱 · `rewind` 🥈 · `restart-level` 🌱.
6. **Типи вікон** (тег `window`): +19 карток із 02 (`editor-window`, `stats-window`, `mode-select`, `map-window`, `difficulty-select`, `puzzle-select`, `lobby-window`, `tutorial-window`, `replay-window`, `codex-window`, `achievements-window`, `character-select`, `game-over-continue`, `level-password`, `match-setup`, `attract-demo`, `placement-screen`, `pass-device`, `code-editor-window`) і розщеплення `end-screen` на `win-screen`/`lose-screen`/`round-summary`.
7. **Сімʼя падаючих блоків** взагалі відсутня в каталозі (є лише `tile-merge` [2048]): `cascade-gravity`, `line-match-clear`, `connected-group-pop`, `chain-reaction`, `garbage-attack`, `next-queue`, `hold-piece`, `bag-randomizer`, `ghost-piece` — 9 карток для класу `cursor`, який у курсі «легалізовано», але майже не оснащено.
8. **Пазли-розмітки**: `neighbor-count-clue`, `line-sum-clue`, `connectivity-check`, `single-loop-check`, `no-adjacent-check`, `edge-marking`, `dot-mark`, `multi-select`, `no-guess-generation` — доповнюють `markup-validity`/`completion-detection`/`unique-puzzle-generation`, що вже є.
9. **Теги гри в картках**: багато пропозицій привʼязані до ігор, яких нема серед 17 `BaseGame` (Tetris, Bejeweled, Into the Breach, Baba, Hexcells…). У YAML-чернетці `[games]` лишені лише для наявних slug-ів; решта — в описі. Якщо каталог ігор розширювати (T36 Q1), першими кандидатами з корпусу за кількістю карток-донорів є **Tetris, Bejeweled/match-3, Into the Breach, Minesweeper-варіанти, Baba Is You, Chip's Challenge, Boulder Dash (глибше), Rogue**.

## Що не пропоную в каталог (і чому)

- Слова-дублі наявних карток: `+pull-object` ↔ немає, пропоную; але `+teleport-pair`, `+key-and-door`, `+inertia-slide` агенти іноді писали з `+` помилково — лінт ловить лише невідомі теги, не дублікати змісту; при злитті перевіряти очима.
- Специфічне для одної гри (`+seat-taint`, `+flying-general`, `+amoeba-growth`): лишається в корпусі як приклад «як це буває» для Д3, не в прайсі.
- Дрібні UI-слова (`+tooltip`, `+toast`, `+popup-text`) — у YAML як 🌱 лише три найчастіші; решта — словник `ui-elements.md`.
