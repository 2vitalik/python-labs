# Класи й осі опису гри

Джерело: [T49](../../../.dev/games/.t/T49-B--game-classes.md) + `data/wiki/games/_classes.md`; тут — EN-значення для шапки файла гри. ✅ прийнято · ⏳ кандидат.

## klass — клас за актором (хто діє) ✅

- `avatar` — керуєш однією сутністю на полі (Pac-Man, Sokoban, роглайки).
- `cursor` — дієш «рукою» по клітинах без аватара (Minesweeper, match-3, 2048, PvZ, TD).
- `figure` — керуєш набором фігур, кожна зі своїми правилами (шахи, тактики, Ricochet Robots).
- `puzzle` — поле статичне, хід = розмітка клітин, мета = обмеження (судоку, Picross, Tatham).
- `hybrid` ⏳ — домінантного класу нема; у «Суті» сказати, які два.

## axes — осі ✅ (значення ⏳, де позначено)

- `field`: `square` · `hex` · `graph` (нестандартна суміжність) · `free` (вільні координати, GUI) · `iso` ⏳ (ізометрична сітка) · `layers` ⏳ (кілька шарів/висот: Mahjong, FFT) · `1d` ⏳ (лінія/смуга) · `3d` ⏳ (воксельна сітка) · `nested` ⏳ (поле всередині поля: Parabox, Recursed) · `hyperbolic` ⏳ (HyperRogue) · `pyramid` ⏳ (піраміда рядів, кожна клітина спирається на дві нижні) · `tri` ⏳ (трикутна сітка) · `tube` ⏳ (поле на циліндрі: краї зшито, Tempest-подібні).
- `time`: `turn` (хід = тік) · `realtime` (тіки таймера) · `static` (пазл без часу) · `rhythm` ⏳ (тік = такт музики) · `programmed` ⏳ (гравець задає програму, вона виконується) · `wego` ⏳ (усі планують одночасно, потім виконання: Frozen Synapse, RoboRally).
- `opponent`: `none` · `ai` · `hotseat` · `online` ⏳ · `coop` ⏳ · `live` ⏳ (жива людина онлайн у реальному часі на тому ж полі).
- `info`: `full` · `hidden` (туман, міни, закриті фігури) · `partial` ⏳ (частково відкрито: Into the Breach показує наміри ворогів) · `asymmetric` ⏳ (сторони бачать різне: один знає, інший вгадує).

Значення `pyramid` · `tri` · `tube` · `live` · `asymmetric` додано 2026-11-19 ([T364](../../../.dev/games/.t/T364--ludopedia-wave4/plan.md), вибір T266 Q4a): їх пропонували агенти хвилі 3; файли, де стоїть найближче наявне значення, не переписувались.
- `random`: `none` · `setup` ⏳ (випадковість лише в генерації) · `runtime` ⏳ (випадковість під час гри: спавн, кубики) · `both` ⏳.
- `goal`: `score` (очки/виживання) · `state` (досягти стану) · `constraints` (задовольнити всі обмеження) · `survive` ⏳ · `race` ⏳ (дійти першим) · `territory` ⏳ (захопити більше поля) · `collect` ⏳ (зібрати все/квоту) · `none` ⏳ (іграшка без мети: Townscaper, Powder Toy).

## Кандидати на нові осі ⏳ (пропонувати через `+axis:`)

- `control`: `direct` (клавіша = рух) · `indirect` (вказуєш ціль, сутність іде сама) · `programmed` (список команд наперед) · `swipe-all` (хід рухає все поле: 2048).
- `actors`: `single` · `party` (кілька підконтрольних по черзі) · `swarm` (багато однакових).
- `undo`: `none` · `unlimited` · `limited` · `rewind` (безперервний час назад).
- `session`: `level` (дискретні рівні) · `endless` · `daily` · `match` (партія).
- `rules` (хвиля 3): `fixed` · `unlocked` (правила відкриваються по ходу гри) · `switchable` (гравець перемикає правила).
- `signal` (хвиля 3): гра про передачу сигналу чи хвилі полем — значення ще не усталені.

## 🔥 Осі, підтверджені корпусом (2026-11-02, 114 ігор)

`control` ×16 (direct · indirect · programmed · swipe-all · drag-path · grab-throw) · `session` ×14 · `undo` ×13 · `actors` ×7 · нові: `gravity` ×5 (none · down · up · per-type · toward-center) · `turn-structure` ×4 (sequential · time-track · simultaneous · wego). Значення осей ✅, яких просили: `field: layers` (FFT, Mahjong), `time: rhythm`, `time: programmed`. Відкрите: клас для Tetris/Puyo (`avatar` чи `cursor`) — [analysis/00-curator-notes.md](../analysis/00-curator-notes.md).
