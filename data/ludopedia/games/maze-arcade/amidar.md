---
title: Amidar
slug: amidar
family: maze-arcade
also: []
klass: avatar
axes:
  field: graph
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: territory
year: 1982
platforms: [arcade, Atari 2600, Casio PV-1000, Gakken VFD handheld]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Amidar", best: true, note: "Amidar-рух (Amidakuji), Tracer, кнопка Jump ×3, бонус чотирьох кутів, чергування рівнів"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/アミダー", note: "очки, правило «лише сусідні до захопленого прямокутники», бонус-стадія з фруктом"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ghost_Leg", note: "Amidakuji — правило, за яким ходять вороги"}
  - {kind: play, url: "https://archive.org/details/arcade_pepper2", note: "Internet Arcade — Pepper II, клон grid capture (оригінал Amidar там не знайдено)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=amidar+arcade+1982+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, touch-death, player-death, pattern-automaton, chase-player, temporary-modes, respawn, event-points, collect-all, sequential-levels, progress-acceleration, speed-per-type, mode-indicator, status-panel, game-screen, leaderboard, +grid-line-field, +amidakuji-walker, +path-replay-chaser, +edge-walker, +line-paint-box-fill, +adjacent-to-owned-rule, +limited-escape-charges, +corner-power-up, +escalating-kill-points, +amidakuji-bonus-round, +extra-life-threshold]
proposes: ["+trigger:region_closed", "+effect:paint", "+effect:fill", "+effect:jump_all", "+cond:adjacent_owned", "+ui:charges-left", "+window:bonus-round", "+feature:operator-settings", "+card:amidakuji-walker", "+card:path-replay-chaser"]
author: opus
date: 2026-11-02
---

# Amidar — фарбуй гратку, замикай прямокутники; вороги ходять за правилами «драбинки» Amidakuji

## Суть
Гравець бігає по лініях прямокутної гратки і фарбує пройдені відрізки; коли всі чотири сторони прямокутника пофарбовані, він заливається. Рівень пройдено, коли залито всі прямокутники — перша гра жанру **grid capture**. Вороги рухаються не за гравцем, а за детермінованим «Amidar-рухом» — правилами японської лотереї Amidakuji (драбинка: униз, на кожній перекладині — вбік). Єдиний переслідувач — Tracer, що повторює точний шлях гравця.

## Поле і час
- Поле — не клітини, а **граф ліній**: вертикальні стовпи з горизонтальними перекладинами (як Amidakuji), що утворюють прямокутники різного розміру. Гравець і вороги ходять лише по лініях.
- Нерухомий екран; real-time. Ворогів більшає і вони швидшають з рівнем; Tracer починає погоню раніше.
- Рівні чергуються: непарні — мавпа (Copier) і «мисливці» (Police/Thief); парні — валик (Rustler) і свині (Cattle).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мавпа / валик | player | життя | рух 4 напрямки по лініях; фарбує пройдене |
| Відрізок лінії | zone | пофарбовано / ні | фарбується проходом гравця |
| Прямокутник | zone | значення в очках (парні рівні) | заливається, коли пофарбовані всі 4 сторони |
| Кутовий прямокутник | zone | 4 на полі | усі 4 залиті → тимчасова сила |
| Ворог (мисливець / свиня) | enemy | швидкість за рівнем | Amidar-рух: униз-вгору, бере кожну перекладину |
| Tracer | enemy | лічильник кіл | обходить периметр N кіл, потім іде точно слідом гравця |
| Переможений ворог | object | — | на горизонталі зникає; на вертикалі падає донизу й оживає після сили |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «є лінія в напрямку dir»` → ТО `move(player, dir)`, `paint(segment)`, `score(10)` за відрізок.
- КОЛИ `custom: «усі 4 сторони прямокутника пофарбовані»` → ТО `fill(box)`, `score(box_value)` (парні рівні).
- Парні рівні: ЯКЩО `custom: «прямокутник не прилягає до вже залитих»` → ТО не заливається; відхід назад або новий прямокутник «рве» лінію — неприєднані відрізки зникають (валику «бракує фарби»).
- Ворог (кожен тік): `move(enemy, vertical_dir)`; КОЛИ `custom: «перехрестя з горизонталлю»` → ТО `custom: «звернути на неї до наступної вертикалі»`; на верхньому/нижньому краю → `custom: «вбік до першої вертикалі, розворот»` — правило Amidakuji, без жодної випадковості.
- Tracer: `custom: «обхід периметра»`; КОЛИ `counter(laps, ==, N)` → ТО `custom: «іде точно по сліду гравця; паузи не копіює»` — вагання = Tracer наздоганяє.
- КОЛИ `input(jump)` → ЯКЩО `counter(jumps, >, 0)` → ТО `custom: «усі вороги підстрибують — гравець проходить під ними»`, `counter(jumps, -1)`; лічильник = 3 на рівень/життя.
- КОЛИ `custom: «залито 4 кутові прямокутники»` → ТО `set_state(player, power, duration)`, вороги змінюють колір, інша музика.
- КОЛИ `contact(player, enemy)` → ЯКЩО `state(player, power)` → ТО `disappear_b`, `score(200 → 400 → 800 → 1600)`; ворог на вертикалі падає донизу і `respawn` після кінця сили. Інакше → `lose`.
- КОЛИ `custom: «залито всі прямокутники»` → ТО `win` рівня → бонус-стадія → `next_level`.
- Бонус-стадія: персонаж їде верхнім рядом; гравець зупиняє його в потрібний момент — він спускається драбинкою Amidakuji до фрукта внизу (5000 очок).
- Перемога: нема (нескінченна аркада). Поразка: 0 життів. Рахунок: 10 за відрізок/точку, значення прямокутників, вороги під силою, фрукт; життя за порогами оператора.

## Керування і ввід
- 4-позиційний джойстик + одна кнопка Jump (до 3 разів на рівень/життя).
- Поворот можливий лише на перехресті ліній; між вузлами — лише вперед/назад.
- Бонус-стадія — одна дія «стоп» у правильний момент.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen`.
- `game-screen` — гратка; HUD: `score`, `hi-score`, `lives`, `level-number`, лишок стрибків (`custom: «charges-left»`), зміна кольору ворогів/музики як `mode-indicator`.
- `custom-window`: бонус-стадія Amidakuji з фруктами внизу.
- `leaderboard` — ініціали.
- Переходи: attract → game-screen (непарний) → бонус-стадія → game-screen (парний) → … → (0 життів) ініціали → attract.

## Фічі поза полем
- `levels-sequential` з чергуванням двох тем/правил; `progress-acceleration` (швидкість, кількість ворогів, ранній Tracer).
- `operator-settings` — пороги життя; два набори ROM: складніший Stern і легший Konami (`custom-rules` на рівні заліза).
- `leaderboard-local`; рекорди Twin Galaxies окремо для кожної версії.

## Варіації й родичі
- Порти: Atari 2600 (Parker Brothers), Casio PV-1000, Gakken VFD-кишенькова.
- Клони grid capture: Pepper II, Make Trax/Crush Roller, Rally-X-подібні; родичі — Pac-Man (лабіринт + вороги), Qix/Xonix (захоплення території), Q*bert (фарбування).
- Осі: **як ходять вороги** — переслідування (Pac-Man) / детермінований автомат (Amidakuji) / повтор сліду гравця (Tracer); **як захоплюється** — фарба відрізків (тут) / слід (Xonix) / стрибок на куб (Q*bert); **порятунок** — енерджайзер / обмежені стрибки / кути.

## Цікавинки для курсу
- Amidar-рух ворогів: детермінований автомат на графі ліній (униз + кожна перекладина) — 🥉, і гарне завдання показати «Amidakuji = перестановка».
- Tracer: черга кроків гравця, яку ворог відтворює з затримкою, але без пауз — 📎 (deque позицій).
- Заливка прямокутника, коли всі 4 сторони пофарбовані — 📎 (граф ребер → грані).
- Правило «лише суміжні до захопленого» + неприєднані лінії зникають — 🥉.
- Обмежені 3 «стрибки» як аварійний вихід — 🌱.
- Бонус чотирьох кутів → невразливість з наростаючими очками — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `touch-death` · `player-death` · `pattern-automaton` (Amidar-рух) · `chase-player` (Tracer, особливий варіант) · `temporary-modes` (сила кутів) · `respawn` (впалі вороги) · `event-points` · `collect-all` (усі прямокутники) · `sequential-levels` · `progress-acceleration` · `speed-per-type` · `mode-indicator` · `status-panel` · `game-screen` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+grid-line-field` «Поле-граф ліній: рух по ребрах, захоплення граней» · entities/legality · 🥉.
  - `+amidakuji-walker` «Ворог ходить за правилом драбинки» · entities/move · 🥉.
  - `+path-replay-chaser` «Ворог повторює точний шлях гравця з затримкою» · entities/move · 📎 · слот {delay_laps}.
  - `+edge-walker` (вже Q*bert) — Tracer до погоні обходить периметр.
  - `+line-paint-box-fill` «Пофарбувати 4 сторони → залити прямокутник» · game-logic/win · 📎.
  - `+adjacent-to-owned-rule` «Захоплювати можна лише суміжне з уже захопленим» · entities/legality · 🥉.
  - `+limited-escape-charges` «Аварійна дія з лімітом зарядів на рівень» · entities/state · 🌱 · слот {charges: 3}.
  - `+corner-power-up` «Сила за захоплення всіх кутів» · game-logic/score · 🌱.
  - `+escalating-kill-points` (вже Pac-Man) — 200/400/800/1600.
  - `+amidakuji-bonus-round` «Бонус-раунд: вибрати момент старту, драбинка веде до призу» · levels/progression · 📎.
  - `+extra-life-threshold` (вже Pac-Man).

## Пропозиції до словників
- `+trigger:region_closed` (вже Xonix) — прямокутник замкнено фарбою.
- `+effect:paint` · `+effect:fill` — фарбувати ребро / залити грань.
- `+effect:jump_all` — усі вороги підстрибують (гравець проходить під ними).
- `+cond:adjacent_owned` — грань прилягає до захопленої.
- `+ui:charges-left` — лишок зарядів дії (стрибки).
- `+window:bonus-round` (вже Pipe Mania) — Amidakuji між рівнями.
- `+feature:operator-settings` (🔥) — пороги життів.
- `+card:amidakuji-walker`, `+card:path-replay-chaser` — див. вище.

## Джерела
- ⭐ [Wikipedia: Amidar](https://en.wikipedia.org/wiki/Amidar) — Amidar-рух за правилом Amidakuji, Tracer по сліду гравця, Jump ×3, бонус кутів, чергування мавпа/валик, версії Stern/Konami, порти.
- [Wikipedia JA: アミダー](https://ja.wikipedia.org/wiki/アミダー) — очки (10 / прямокутник / 200–1600 / фрукт 5000), правило суміжності на парних рівнях, бонус-стадія.
- [Wikipedia: Ghost Leg (Amidakuji)](https://en.wikipedia.org/wiki/Ghost_Leg) — сама «драбинка», з якої взято рух ворогів.
- [Internet Arcade: Pepper II](https://archive.org/details/arcade_pepper2) — грати клон grid capture у браузері.
- YouTube: пошук «amidar arcade 1982 gameplay».

## Непевне
- (?) Jump: EN Wikipedia — підстрибують вороги, гравець проходить під ними; JA — стрибає сам гравець. Ефект однаковий, механіка різна.
- (?) Tracer обходить периметр проти годинникової (EN) чи за годинниковою (JA).
- (?) Непарні рівні: EN — «збирає кокосові горіхи», JA — «точки по 10 очок»; чи потрібно там заливати прямокутники так само — обидві статті кажуть, що рівень закінчує залиття всіх.
- (?) Розмір гратки (стовпів/перекладин) і кількість прямокутників; оригінальної Amidar в Internet Arcade не знайшов.
