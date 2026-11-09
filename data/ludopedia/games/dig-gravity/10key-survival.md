---
title: 10key Survival
slug: "10key-survival"
aka: []
family: dig-gravity
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2026
platforms: [web (HTML5)]
links:
  - {kind: itch, url: "https://houseduck.itch.io/10key-survival", best: true, note: "опис, керування, картинки «як грати»: копання клавіш утриманням напрямку, картки рівня, NUM LOCK-код, Golden Fever, миша з Lv7, пробіл з Lv14, постійні апгрейди, місячний рейтинг"}
  - {kind: other, url: "https://houseduck.itch.io/10key-survival/devlog/1739536/10key-survival-the-trailer-in-your-language-en-de-", note: "devlog: трейлер 5 мовами; нескінченна плата-клавіатура, drift і трансформація в робота, миша й пробіл, клітки NUM LOCK"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=10key+Survival+houseduck", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, keyboard-controls, dig-terrain, destructible-blocks, hp-damage, infinite-field, in-round-upgrades, combo-multiplier, chase-player, telegraph-marker, blast-wave, shoot-cooldown, popup-text, leaderboard, save-progress, shop-window, game-pause, language-picker, +xp-level-up, +choose-upgrade, +meta-progression, +card-rarity, +block-hardness, +score-fever, +typed-escape-code, +skill-keys-on-avatar, +seasonal-ranking]
proposes: ["+effect:repair", "+cond:cooldown_ready", "+ui:durability-bar", "+ui:exp-bar", "+window:code-entry", "+feature:seasonal-leaderboard", "+card:typed-escape-code", "+card:skill-keys-on-avatar", "+card:score-fever"]
author: opus
date: 2026-11-09
---

# 10key Survival — живий нампад прогризає нескінченну клавіатуру: бий клавіші, обирай картки, тікай від миші

## Суть
Аркадний роглайт про копання: гравець — цифровий блок клавіатури (тенкей), що прогризається крізь нескінченну 3D-клавіатуру на друкованій платі. Утримання напрямку бʼє клавіші попереду: вони тріскають і розлітаються, викидаючи скрап, золоті клавіші й скрині. За рівень — вибір 1 з 3 карток (нове вміння, сильніше вміння або ремонт); вміння «сідають» на власні клавіші нампада й натискаються тими ж цифрами на справжній клавіатурі. З 7-го рівня полює миша, з 14-го (повна версія) пробіл бʼє хрестом, а клітка NUM LOCK вимагає набрати показаний код.

## Поле і час
- Квадратна сітка клавіш (3D-рендер, камера згори під кутом); під розбитими клавішами — плата. Поле нескінченне в напрямку копання.
- Аватар великий: нампад займає кілька клітин-клавіш (?).
- Real-time; ритм задають утримання напрямку, перезарядки вмінь і рівні (Lv).
- Тип клавіш: звичайні, сталеві (STEEL Lv1 — міцніші (?)), розжарені червоні (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Нампад (тенкей) | player | DURABILITY %, EXP, Lv, сила удару | рух 4 напрямки (8 / 4 / 6 / 5); утримання напрямку бʼє клавіші попереду; вміння на клавішах 7, 9, 1, 2, 3, 0, ., Enter |
| Клавіша | object | міцність | тріскає й розбивається від ударів; дає очки, EXP, лут |
| Сталева клавіша | object | рівень | міцніша за звичайну (?) |
| Скрап | resource | — | валюта постійних апгрейдів між забігами |
| Золота клавіша | pickup | — | вилітає з клавіш; GOLD (?) |
| Скриня | container | — | вилітає з клавіш; вміст (?) |
| Миша | enemy | — | з Lv7 полює; таран по смузі, підсвіченій червоним |
| Пробіл | hazard | — | з Lv14 (повна версія) бʼє хрестом |
| Клітка NUM LOCK | hazard | код, таймер | заковує нампад; звільнення — набрати показаний код |
| Golden Fever | — | тривалість | тимчасово 2× очки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(ahead)` → ТО `move(numpad, dir)`.
- КОЛИ `input(dir)` (утримання) → ЯКЩО `occupied(ahead, key)` → ТО `damage(key, hit_power)`.
- КОЛИ `hp_zero(key)` → ТО `disappear(key)`, `score(+n)`, `counter(exp, +n)`, `counter(combo, +1)`.
- КОЛИ `hp_zero(key)` → ЯКЩО `prob(p)` → ТО `spawn(scrap|gold_key|chest)`.
- КОЛИ `contact(numpad, scrap|gold_key)` → ТО `pickup`.
- КОЛИ `counter(exp, >=, next_level)` → ТО `counter(level, +1)`, `window(upgrade-window)`, `choose(3 cards)`: нове вміння (на наступну вільну клавішу) / сильніше вміння / ремонт.
- КОЛИ `input(skill_key)` → ЯКЩО `custom: «вміння не на перезарядці»` → ТО ефект вміння: LASER — `custom: «спалює 10 клавіш попереду»`; DASH — `custom: «ривок на 6 клавіш, розбиваючи все»`; SHOCKWAVE — `custom: «хвиля навколо (?)»`; далі `timer(start, cooldown)`.
- КОЛИ `input(repair)` → ТО `heal(numpad, 15%)`; картка REPAIR KIT — `heal(numpad, 25%)`.
- КОЛИ `custom: «спрацювала Golden Fever»` → ТО `multiplier(2)` на обмежений час.
- КОЛИ `level_start` → ЯКЩО `level(>=, 7)` → ТО `spawn(mouse)`; КОЛИ `custom: «миша готує таран»` → ТО `custom: «смуга тарану підсвічується червоним»`; КОЛИ `contact(mouse, numpad)` → ТО `damage(numpad, n)` (?).
- КОЛИ `level_start` → ЯКЩО `level(>=, 14)` → ТО `custom: «пробіл періодично бʼє»`, `explode(cross)`.
- КОЛИ `contact(numpad, numlock)` → ТО `set_state(numpad, caged)`; КОЛИ `input(digits)` → ЯКЩО `custom: «введений код = показаний»` → ТО `clear_state(numpad, caged)`; таймер клітки (?).
- КОЛИ `hp_zero(numpad)` → ТО `game_over` (?), скрап забігу → постійні апгрейди.
- Перемога: нема — копати якнайглибше й пережити мишу. · Поразка: міцність нампада 0 (?). · Рахунок: очки за клавіші й лут, комбо, ×2 у Golden Fever → місячний рейтинг.

## Керування і ввід
- Рух / копання: 8 4 5 6 нампада, стрілки або WASD (5 — вниз).
- Вміння: 7 9 1 2 3 0 . Enter або Q E Z X C Alt Space — фізичні клавіші відповідають клавішам аватара.
- NUM LOCK: набрати цифри, Backspace — стерти. Картки: 1 / 2 / 3. Пауза: P або Esc.
- Тач: утримувати, щоб кермувати (віртуальний джойстик), тапати кнопки вмінь; на екрані вибору карток — утримати порожнє місце, щоб побачити поле.

## Вікна, меню, HUD
- `game-screen`: поле клавіш; HUD — `durability-bar` з %, Lv, `exp-bar`, `combo-meter` (×85), `popup-text` (+2.8k), плитка вміння з `skill-bar`-перезарядкою (SHOCKWAVE 7s), кнопка REPAIR +15%, `telegraph-marker` смуги тарану миші («GET OUT OF THE RED!»), смуга стану «SHAKING IT OFF» (?); на самому нампаді — замкнені й відкриті клавіші вмінь.
- `upgrade-window`: «LEVEL N! Pick one», три картки з рідкістю (N, R) і позначками NEW / USE NOW.
- `custom-window` NUM LOCK ESCAPE CODE: шість цифр, курсор, смуга часу, «Tap the keys on the tenkey».
- Хаб із вкладками SHOP · MODULES · 10KEY · UPGRADE · RANKING: `shop-window`; MODULES — колекція (лише повна версія); UPGRADE — постійні апгрейди (DRILL, CELL, MOTOR, MAGNET, SKILL, CHIP, HOUSING, HOT-SWAP, SWITCH; рівні 1/5, ціна у скрапі); `leaderboard` — сезон «This season / Last season», пʼєдестал, таймер до кінця сезону.
- `pause-menu` (P / Esc).

## Фічі поза полем
- `meta-progression`: скрап → постійні апгрейди (DRILL: «Hits harder, keys break sooner», сила удару 2 → 3).
- Прогрес рівня: DRIFT (Lv7) і TRANSFORM (Lv14, повна версія) змінюють форму аватара — дрейфова клавіатура, робот.
- `leaderboard-online`: місячний рейтинг; `autosave` прогресу в браузері.
- `localization` (8 мов), `touch-controls`; демо в браузері, повна версія — Google Play, App Store, Steam (заявлено).

## Варіації й родичі
- У сімʼї: [pocket-mine](pocket-mine.md) (копання вниз з бонусами забігу), [mr-driller](mr-driller.md) (бурити, поки не скінчився ресурс), [downwell](downwell.md) (роглайт униз), [motherload](motherload.md) (копання й апгрейди).
- Поза сімʼєю: роглайти з вибором 1 з 3 карток на рівень (Vampire Survivors-подібні).
- **Осі варіацій**: аватар — 1 клітина (Dig Dug) / кілька клітин з власними клавішами-вміннями (10key); загроза — повітря й завали (Mr. Driller) / мисливець і періодичні удари (10key); тема поля — земля / клавіатура, де ввід і поле — те саме.

## Цікавинки для курсу
- Вміння на клавішах аватара = ті самі фізичні клавіші: розкладка як частина ігрового світу — 📎.
- Клітка NUM LOCK: міні-гра «набери код на нампаді» з таймером посеред real-time — 🌱.
- Утримання напрямку = серія ударів по міцності клавіші; сталеві клавіші міцніші — 📎.
- Картки рівня 1 з 3 з рідкістю, «нове вміння йде на наступну вільну клавішу» — 🥉.
- Таран миші з телеграфованою червоною смугою — 📎.
- Удар пробілом хрестом (`blast-wave`) — 🌱.
- Нескінченна генерація клавіатури з типами клавіш і лутом — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `dig-terrain` + `destructible-blocks` ↔ клавіші; `hp-damage` ↔ міцність нампада; `infinite-field` ↔ нескінченна клавіатура; `in-round-upgrades` ↔ картки рівня; `combo-multiplier` ↔ ×N; `chase-player` ↔ миша; `telegraph-marker` ↔ червона смуга; `blast-wave` ↔ пробіл хрестом; `shoot-cooldown` ↔ перезарядка вмінь; `popup-text`; `leaderboard`; `save-progress`; `shop-window`; `game-pause`; `language-picker`.
- Повтори з корпусу: `+xp-level-up` · `+choose-upgrade` · `+meta-progression`.
- **Нема** → пропозиції карток:
  - `+typed-escape-code` «Клітка: набери показаний код, щоб вирватись» · entities/state · 🌱 · слоти {digits: 6, time}.
  - `+skill-keys-on-avatar` «Вміння сидять на клавішах аватара, фізична клавіша = ігрова» · interface/input · 📎.
  - `+score-fever` «Тимчасовий режим ×2 очок» · game-logic/score · 🌱.
  - `+card-rarity` «Рідкість карток вибору (N, R…)» · game-logic/economy · 🌱.
  - `+block-hardness` «Блоки різної міцності проти сили удару» · entities/state · 📎.
  - `+seasonal-ranking` «Рейтинг із сезонами (місяць)» · game-logic/score · 🥉.

## Пропозиції до словників
- `+effect:repair` — відновити міцність аватара (повтор з корпусу).
- `+cond:cooldown_ready` — вміння не на перезарядці.
- `+ui:durability-bar` — смуга міцності аватара; `+ui:exp-bar` — смуга досвіду до рівня.
- `+window:code-entry` — модал введення коду поверх гри з таймером.
- `+feature:seasonal-leaderboard` — рейтинг, що скидається щомісяця, з таблицею минулого сезону.
- `+card:typed-escape-code`, `+card:skill-keys-on-avatar`, `+card:score-fever` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: 10key Survival](https://houseduck.itch.io/10key-survival) — опис, керування, картинки «Dig through the keyboard», «Level up, pick a card», NUM LOCK, Golden Fever, «Dodge the mouse's charge», «Permanent upgrades», «Climb the monthly ranking»; Godot, HTML5, 8 мов.
- [Devlog: трейлер](https://houseduck.itch.io/10key-survival/devlog/1739536/10key-survival-the-trailer-in-your-language-en-de-) — суть одним абзацом, демо до рівня 15.
- YouTube: пошук «10key Survival houseduck».

## Непевне
- (?) Чи рух дискретний по клітинах-клавішах, чи вільний над сіткою («drift»); скільки клітин займає нампад.
- (?) Демо закінчується на Lv8 (сторінка) чи на Lv15 (devlog).
- (?) Що таке «SHAKING IT OFF» — стан після удару миші чи її підготовка; чи миша шкодить міцності.
- (?) Як потрапляють у клітку NUM LOCK і що буде, якщо не встигнути з кодом; вміст скринь; роль золотих клавіш (валюта чи очки).
- (?) Що вичерпує міцність (удари по клавішах, миша, пробіл) і чи міцність 0 = кінець забігу.
