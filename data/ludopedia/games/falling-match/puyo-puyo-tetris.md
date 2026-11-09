---
title: Puyo Puyo Tetris
slug: puyo-puyo-tetris
aka: [PPT, ぷよぷよテトリス, Puyo Puyo Tetris S, PPT2, Puyo Puyo Tetris 2]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: survive
year: 2014
platforms: [3DS, Wii U, PS Vita, PS3, PS4, Xbox One, Switch, PC]
links:
  - {kind: fandom, url: "https://puyonexus.com/wiki/Puyo_Puyo_Tetris", best: true, note: "Puyo Nexus — режими Versus/Swap/Fusion/Party/Big Bang: Attack Gauge, свап кожні 25 с, Fusion 8×16, дропсети, Challenge і Adventure"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puyo_Puyo_Tetris", note: "огляд режимів, до 4 гравців, магазин скінів, історія релізів, сиквел PPT2"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Puyo+Puyo+Tetris", note: "пошук; PPT (2018) і PPT2 (2021)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puyo+puyo+tetris+fusion+swap+gameplay", note: "пошук; Fusion і Swap"}
stage: v1
coverage: 60
mechanics: [garbage-attack, simultaneous-versus, online-multiplayer, ai-opponent, rule-variants, mode-select, character-select, inventory-items, temporary-modes, time-out, progress-acceleration, shop-window, theme-select, score-records, end-screen, game-pause, +cross-ruleset-garbage, +attack-gauge-hold, +timed-ruleset-swap, +swap-combo-carryover, +mixed-ruleset-field, +piece-crush-stack, +active-chaining, +mixed-dropset, +relative-speed-damage]
proposes: ["+effect:swap_ruleset", "+effect:crush(a, below)", "+effect:hold_garbage", "+cond:ruleset(side, r)", "+trigger:round_end", "+ui:attack-gauge", "+ui:swap-timer", "+feature:mode-swap", "+feature:mode-fusion", "+feature:mode-party", "+feature:mode-big-bang", "+axis:ruleset"]
author: opus
date: 2026-11-09
---

# Puyo Puyo Tetris — Puyo і Tetris в одній партії: кожен грає за своїми правилами, а сміття летить між правилами

## Суть
Кросовер двох класик: базові правила — точно як у [Puyo Puyo](puyo-puyo.md) (Tsu) і [Tetris](tetris.md) (сучасний гайдлайн); тут описано лише те, що з'являється від їх зустрічі. У Versus кожен гравець обирає правила сам, і пуйо-гравець б'ється з тетріс-гравцем: лінії перетворюються на сміттєві пуйо, ланцюги — на сміттєві рядки. Режими Swap і Fusion змішують правила вже для одного гравця: Swap перемикає його між двома полями за таймером, Fusion кладе пуйо й тетраміно на одне поле. Головна ідея для курсу — дві різні «фізики» за одним інтерфейсом атаки.

## Поле і час
- Versus/Party/Big Bang: до 4 гравців, у кожного своє поле за обраними правилами (поле Puyo і колодязь Tetris різних розмірів поруч на одному екрані).
- Swap: у гравця **два поля** (Puyo і Tetris), активне одне; перемикання кожні 25 с, незалежно від того, чи фігура долетіла.
- Fusion: одне поле 8×16, у черзі змішано пари пуйо й тетраміно за дропсетом персонажа.
- Big Bang: раундова структура — раунди з таймером, між ними підрахунок і «удар» по повільнішим.
- Час real-time; у Fusion (як Active rule у Puyo Puyo!! 20th) можна кидати наступну фігуру, поки ланцюг ще лопається або тетраміно повільно тисне пуйо.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пуйо-гравець | player | правила Tsu | як у puyo-puyo.md; атака — сміттєві пуйо |
| Тетріс-гравець | player | гайдлайн (hold, T-spin, B2B) | як у tetris.md; атака — сміттєві рядки або пуйо (проти пуйо-суперника) |
| Attack Gauge | container | накопичена атака | тетріс-атака проти пуйо-суперника складається тут; відпускається лише фігурою, що **не** очистила лінію |
| Сміттєві пуйо / рядки | hazard | — | що саме падає — визначають правила одержувача, а не відправника |
| Два поля Swap | zone | Puyo-поле, Tetris-поле | активне одне; неактивне «застигає», але каскад, почате до свапу, продовжується |
| Fusion-поле | zone | 8×16 | спільне для пуйо й тетраміно |
| Тетраміно у Fusion | piece | 7 форм | падаючи, тоне під пуйо: роздавлює стовпці пуйо під собою |
| Пара пуйо у Fusion | piece | 2 кольори | лопається групою 4+ як звичайно |
| Особлива фігура Fusion | piece | 1 на дропсет | або фігура, що перемикається між пуйо і тетраміно, або золотий 1–2-клітинний тетріс-блок |
| Предмет Party | pickup | бафф собі / дебафф суперникам | застосовується під час партії |
| Чорна діра Big Bang | spawner | — | у кінці раунду всмоктує згенероване сміття і «вибухає» на поля повільніших |
| Дропсет персонажа | spawner | 8 пуйо-дропів + 2 тетраміно + 1 особлива (стандарт) | задає порядок форм у Fusion і Puyo-режимах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ЯКЩО `mode(versus)` → ТО `choose(ruleset: puyo | tetris)` для кожного гравця окремо; у Swap і Fusion вибору нема.
- КОЛИ `pattern(group(4+, same_color))` у пуйо-гравця → ТО `send_garbage(n)`; ЯКЩО `custom: «правила одержувача — Tetris»` → ТО `custom: «сміття приходить рядками»`.
- КОЛИ `custom: «тетріс-гравець очистив лінії»` → ЯКЩО `custom: «серед суперників є пуйо-гравець»` → ТО `counter(attack_gauge, +n)` замість миттєвої відправки.
- КОЛИ `locked(tetromino)` → ЯКЩО `not custom: «фігура очистила лінію»` і `counter(attack_gauge, >, 0)` → ТО `send_garbage(attack_gauge)`, `counter(attack_gauge, = 0)`.
- КОЛИ `timer(25s)` → ЯКЩО `mode(swap)` → ТО `custom: «swap_ruleset — активне поле міняється»`; поточна фігура падає далі без керування.
- КОЛИ `custom: «свап стався під час каскаду»` → ЯКЩО `pattern(...)` на новому полі → ТО `combo(+1)` — Swap Combo: збиги до і після перемикання рахуються одним комбо.
- КОЛИ `custom: «будь-яке з двох полів Swap переповнилось»` → ТО `lose` (гравець вибуває).
- КОЛИ `custom: «тетраміно падає у Fusion»` → ЯКЩО `occupied(cells_below, puyo)` → ТО `custom: «crush — тетраміно тоне під пуйо, роздавлюючи стовпець»`; знову зверху з'являються лише **кольорові** пуйо, сміття знищується.
- КОЛИ `custom: «рядок Fusion заповнено блоками тетраміно»` → ТО `clear(row)` (?); КОЛИ `pattern(group(4+))` пуйо → ТО `clear(group)`, ланцюг як у Tsu.
- КОЛИ `input(drop)` → ЯКЩО `mode(fusion)` і `custom: «ланцюг ще триває»` → ТО `custom: «наступна фігура вже падає (Active)»`.
- КОЛИ `picked(player, item)` → ЯКЩО `mode(party)` → ТО `custom: «бафф собі або дебафф суперникам»`; поразки від переповнення нема.
- КОЛИ `timer(<=, 0)` → ЯКЩО `mode(party)` → ТО `win` гравцеві з найбільшим `score`.
- КОЛИ `phase_start(round)` → ЯКЩО `mode(big_bang)` → ТО `custom: «пуйо-гравець у Fever (готові ланцюги), тетріс-гравець у Lucky Attack (готові заготовки)»`.
- КОЛИ `custom: «round_end у Big Bang»` → ТО `damage(slower_players, n)` пропорційно відставанню від лідера; `custom: «поле тріскається»`.
- КОЛИ `custom: «поле Big Bang повністю розбите»` → ТО `lose` (вибув); останній — `win`.
- КОЛИ `custom: «поле переповнилось»` → ЯКЩО `mode(versus|swap|fusion)` → ТО `lose`; виграє остання сторона/команда.
- Перемога: остання сторона на полі (Versus, Swap, Fusion, Big Bang) або найбільше очок (Party). Рахунок: як у базових правилах; кредити за ігри — у магазин.

## Керування і ввід
- Ті самі кнопки для обох правил: ←/→ зсув, ↓ soft drop, A/B поворот; у Tetris — ще hold і hard drop.
- У Swap гравець мусить «перемкнути голову» разом із полем: клавіші ті самі, сенс — інший (пара пуйо крутиться навколо осі, тетраміно — за SRS).
- До 4 гравців: локально (кожен свій контролер), онлайн або проти CPU.

## Вікна, меню, HUD
- `main-menu`: Adventure · Solo Arcade (Versus, Swap, Fusion, Party, Big Bang, Challenge) · Multiplayer Arcade · Online (Puzzle League, Free Play) · Lessons (?) · Options · Shop.
- `character-select` — персонаж = дропсет і голос; одразу ж `custom: «ruleset-select»` (Puyo / Tetris) для Versus.
- `mode-select` — п'ять змішаних режимів.
- `game-screen`: 2–4 поля поруч; у тетріс-гравця проти пуйо — `custom: «attack-gauge»` збоку від колодязя; у пуйо — `garbage-meter`; у Swap — `custom: «swap-timer»` і мініатюра неактивного поля (?); `next-piece-preview`, `hold-slot`, `score`, `popup-text` «N Chain!/Tetris!/T-Spin».
- `end-screen` раунду й матчу (лічильник перемог), Adventure — зірки 1–3 за челендж.
- `shop-window` — скіни пуйо й тетраміно, голосові пакети за кредити (1 000–2 500).

## Фічі поза полем
- `feature:mode-swap` · `mode-fusion` · `mode-party` · `mode-big-bang` — змішані режими (пропозиції).
- Adventure: 7 актів по 10 стадій + 3 бонусні; стадія — бій з CPU або соло-челендж; `stars-rating` (Fever Trial Lv.8: 10 000 / 35 000 / 60 000).
- Challenge соло: Endless Puyo (рівень за очки), Endless Fever (ланцюги поповнюють таймер), Tiny Puyo (менше поле), Marathon (150 ліній, рівень кожні 10), Sprint (40 ліній на час), Ultra (3 хв на очки).
- `online-multiplayer` (рейтинговий Puzzle League), `ai-opponent-levels`, `unlockables` (скіни, голоси), `theme-select`.

## Варіації й родичі
- Базові правила: [puyo-puyo](puyo-puyo.md) (Tsu, Fever), [tetris](tetris.md) (гайдлайн), [tetris-effect](tetris-effect.md) (Zone ≈ Lucky Attack), [tetrinet](tetrinet.md) (предмети в мультиплеєрі ≈ Party), [super-puzzle-fighter-ii-turbo](super-puzzle-fighter-ii-turbo.md) (асиметричні атаки персонажів), [lumines](lumines.md) (зміна «скіна» = зміна темпу).
- Puyo Puyo Tetris 2 (2020/2021): ті самі режими + Skill Battle (персонажі з навичками й HP) (?).
- **Осі варіацій**: як змішати правила (кожен своє / по черзі за таймером / на одному полі) · конверсія атаки (миттєво / через накопичувач) · хто визначає форму сміття (відправник / одержувач) · умова поразки (переповнення / таймер і очки / HP поля).

## Цікавинки для курсу
- Спільний інтерфейс атаки для двох різних правил (адаптер «очки атаки → сміття за правилами одержувача») — 🥉: чисте ООП-завдання на поліморфізм поля.
- Attack Gauge: атака відпускається лише фігурою без очищення — 📎.
- Swap: два стани гри, перемикання за таймером, каскад неактивного поля продовжує тікати — 🥈 (два ігрові цикли, один ввід).
- Fusion: тетраміно тоне крізь пуйо й роздавлює їх, два типи «зникнення» на одній сітці — 🥇 (конфлікт двох гравітацій).
- Big Bang: відносна шкода «на скільки ти повільніший за лідера» — 🌱.
- Party-предмети як бафф/дебафф — 📎.

## Мапа на каталог
- Є: `garbage-attack` (між різними правилами) · `simultaneous-versus` · `online-multiplayer` · `ai-opponent` · `rule-variants` (вибір правил кожним гравцем) · `mode-select` · `character-select` (дропсет) · `inventory-items` (Party) · `temporary-modes` (Fever/Lucky Attack) · `time-out` (Party, Ultra) · `progress-acceleration` (Marathon, Endless) · `shop-window` · `theme-select` · `score-records` · `end-screen` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+cross-ruleset-garbage` «Сміття між різними правилами: форму визначає одержувач» · game-logic/opponent · 🥉.
  - `+attack-gauge-hold` «Атака накопичується й відпускається фігурою без очищення» · game-logic/opponent · 📎.
  - `+timed-ruleset-swap` «Перемикання між двома полями з різними правилами за таймером» · game-logic/constraints · 🥈.
  - `+swap-combo-carryover` «Комбо переживає перемикання полів» · game-logic/score · 📎.
  - `+mixed-ruleset-field` «Два типи фігур з різними правилами на одному полі» · entities/interact · 🥇.
  - `+piece-crush-stack` «Фігура тоне крізь стос, роздавлюючи його» · entities/interact · 🥉.
  - `+active-chaining` «Можна ходити, поки триває каскад» · entities/legality · 📎 (спільна з Zoo Keeper).
  - `+mixed-dropset` «Черга з різнотипних фігур за таблицею персонажа» · entities/spawn · 🌱.
  - `+relative-speed-damage` «Шкода за відставання від лідера в раунді» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+effect:swap_ruleset` — змінити активні правила/поле гравця (Swap).
- `+effect:crush(a, below)` — фігура знищує те, крізь що проходить вниз (Fusion).
- `+effect:hold_garbage` — покласти атаку в накопичувач замість відправки (Attack Gauge).
- `+cond:ruleset(side, r)` — сторона грає за правилами r (Puyo/Tetris).
- `+trigger:round_end` — кінець раунду з таймером (Big Bang); `round` ще нема в життєвому циклі.
- `+ui:attack-gauge` — накопичувач власної атаки; `+ui:swap-timer` — відлік до перемикання полів.
- `+feature:mode-swap`, `+feature:mode-fusion`, `+feature:mode-party`, `+feature:mode-big-bang` — змішані режими.
- `+axis:ruleset` — `single` · `per-player` (кожен свої) · `alternating` (Swap) · `merged` (Fusion).

## Джерела
- ⭐ [Puyo Nexus: Puyo Puyo Tetris](https://puyonexus.com/wiki/Puyo_Puyo_Tetris) — Attack Gauge, свап кожні 25 с і Swap Combo, Big Bang (чорні діри), Party, Fusion 8×16 (crush, Active, дропсет 8+2+1, особлива фігура), Challenge і Adventure, очки Tetris.
- [Wikipedia: Puyo Puyo Tetris](https://en.wikipedia.org/wiki/Puyo_Puyo_Tetris) — до 4 гравців, вибір правил, опис режимів, магазин, релізи, PPT2.
- Steam: пошук «Puyo Puyo Tetris».

## Непевне
- (?) Як саме чиститься рядок у Fusion, якщо в ньому є пуйо (чи пуйо рахуються заповненням); чи сміття у Fusion — пуйо чи рядки.
- (?) Коефіцієнти конверсії «лінії ↔ сміттєві пуйо» — Puyo Nexus їх не дає.
- (?) Чи видно неактивне поле у Swap (мініатюра) — не підтверджено.
- (?) Список предметів Party і точна шкода Big Bang не знайдені.
- (?) Пункти головного меню (Lessons, Puzzle League) — з пам'яті.
- (?) Skill Battle у PPT2 — Wikipedia його не згадує.
