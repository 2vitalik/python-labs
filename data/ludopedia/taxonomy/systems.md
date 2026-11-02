# Системи класифікації — як вони поєднуються

Одна гра має **один дім і багато вимірів** — той самий принцип, що в каталозі завдань («дім + теги», [T33](../../../.dev/tasks/.t/T33-B--task-taxonomy.md)). Жодна система не головна; разом вони дають фасетний пошук.

## 1. Сімʼя-лінія (тека) — звідки виросла, що робиш найчастіше

17 тек ([families.md](families.md)). Корисна для навігації людиною і для «родичів»: усі Sokoban-подібні поруч. Слабка для гібридів — тому `also:`.

## 2. Клас за актором (`klass`) — хто діє · [T49](../../../.dev/games/.t/T49-B--game-classes.md)

`avatar · cursor · figure · puzzle (· hybrid)`. Головна вісь для **курсу**: визначає скелет роботи студента (аватар рухається / рука клікає / фігури ходять / розмітка перевіряється). Перетинається з сімʼями навскіс: у `maze-arcade` майже всі avatar, у `pencil-logic` — puzzle, у `tactics` — figure, у `build-sim` — cursor.

## 3. Осі (`axes`) — незалежні виміри · `vocab/classes.md`

`field · time · opponent · info · random · goal` (+ кандидати `control · actors · undo · session`). Осі майже незалежні: «судоку на гексах на час» описується без нових понять. Для пошуку: «усі real-time ігри з прихованою інформацією».

## 4. Дієслово гравця — що саме робить рука

`push · dig · run · climb · match · mark · reveal · move-piece · command · place · build · program · connect · rotate · guess`. Це дрібніша версія сімʼї, корисна для **механік**: одне дієслово проходить через багато сімей (`place` є в TD, build-sim, board-digital). У шапці не окреме поле — виводиться з тегів `mechanics`.

## 5. Теги механік (`mechanics`) — композиція з карток

Гра = множина slug-ів каталогу (+ пропозицій). Це і є «лудеми» (T98 М1): дає матрицю ігри × механіки (`index/mechanics.md`), пошук «усі ігри з `push-object` і `gravity-fall`» (= Boulder Dash-подібні), і міру новизни гри для корпусу (скільки `+`).

## 6. Зовнішні таксономії (для звірки, не для шапки)

- Steam-теги: Grid-Based Movement, Sokoban, Turn-Based Tactics, Roguelike, Puzzle, Match 3, Tower Defense, Programming, Logic, Hidden Object.
- BGG-механіки: Grid Movement, Tile Placement, Pattern Building, Polyomino, Hexagon Grid, Square Grid, Enclosure, Connection, Area Majority, Deduction.
- Thinky Games: теги механік сучасних головоломок (sokoban-like, rule-based, time-manipulation, gravity…).
- Nikoli / puzz.link: ~100 жанрів паперових пазлів з канонічними назвами.
- Wikipedia: списки (chess variants, Nikoli puzzle types, roguelikes, tile-matching video games, puzzle video games).

## Як поєднувати в системі опису для студентів

- Студент обирає **клас** (скелет) і **гру-основу** (сімʼя дає родичів-донорів механік) → бачить картки механік, типові для сімʼї (з корпусу: частоти `index/mechanics.md`) → набирає свою композицію.
- Корпус відповідає на «як це буває»: по тегу — список ігор з прикладами; по сімʼї — осі варіацій (у секції «Варіації й родичі» кожного файла).
