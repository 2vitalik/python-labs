---
title: Babble Royale
slug: babble-royale
aka: []
family: word-number
also: []
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2021
platforms: [Windows, macOS]
links:
  - {kind: other, url: "https://biggieblog.com/?p=263", best: true, note: "гайд «Having the Last Word»: поле 31×31, рука з 5 плиток з особистого мішка, активне слово, таймер Next Letter 12 с, Rack Refill, магазин, 4 power-ups, бомба радіусом 3, премії, звуження зони, гарячі клавіші, стратегія"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Babble_Royale", note: "до 16 гравців з однієї плитки, слова — рух і атака, елімінація дотиком, hot zone; Everybody House Games, ранній доступ 15.12.2021"}
  - {kind: steam, url: "https://store.steampowered.com/app/1759440/Babble_Royale/", note: "опис: «You are the last word you made», 16 гравців, лут, гроші за слова, магазин, скіни, Season Zero, free-to-play"}
  - {kind: other, url: "https://wordfinder.yourdictionary.com/blog/the-action-packed-babble-royale-where-scrabble-meets-fortnite", note: "стартова плитка A, рука з 5, будь-який напрям, словник Scrabble, активне слово кольором, глядач після смерті, апгрейди на раунд, косметика за гроші"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Babble+Royale+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [online-multiplayer, word-validation, keyboard-controls, cell-click, event-points, round-currency, in-round-upgrades, shop-catalog, inventory-items, inventory-limit, item-pickup, hp-damage, environment-death, destructible-blocks, game-screen, end-screen, main-menu, shop-window, +premium-squares, +tile-rack, +tile-bag-draw, +word-as-attack, +active-word-avatar, +shrinking-arena, +player-elimination, +last-standing-round, +drop-in-spawn, +timed-tile-refill, +rack-refill-bonus, +kill-feed, +spectate-after-death, +cosmetic-shop]
proposes: ["+trigger:last_standing", "+effect:eliminate", "+ui:kill-feed", "+ui:next-letter-timer", "+ui:placement-indicator", "+ui:zone-border", "+window:drop-phase", "+feature:cosmetic-shop", "+feature:battle-pass"]
author: opus
date: 2026-11-09
---

# Babble Royale — battle royale на дошці Scrabble: ти — своє останнє слово; зʼєднай слово з чужим активним, і суперник вибуває

## Суть
Онлайн-гра на 16 гравців у реальному часі на великій дошці з преміями Scrabble. Кожен гравець — це його **активне слово**: нове слово мусить торкатися активного й стає новим активним, тож слова — це і рух по полю, і атака. Хто першим зіграє слово, що зʼєднує своє активне слово з активним словом суперника, той його вибиває; гаряча зона звужує поле й шкодить тим, чиє слово лишилося зовні. Клас `hybrid`: курсор розстановки плиток як у Scrabble + «аватар»-слово, що мандрує полем.

## Поле і час
- Квадратна дошка 31 × 31 (гайд biggieblog) з преміальними клітинами й клітинами-power-ups; камеру рухають Alt + стрілки.
- Шари: клітина (звичайна / премія / power-up / гаряча зона) + плитка (сіра / активна кольору гравця).
- Real-time: усі грають одночасно, ходів нема — швидкість набору й надходження плиток визначає темп.
- Зона: через 2 хв поле стискається 31→23, далі 15, далі 11, потім — випадковий менший прямокутник (biggieblog).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активне слово гравця | player | колір гравця, HP (максимум — 100 (?)) | останнє зігране слово; нові слова мусять його торкатися |
| Сіра плитка | object | літера | старі слова й слова вибулих; частина поля, бомба руйнує |
| Стартова плитка | object | A (інша літера — за реальні гроші) | перше «тіло» гравця після десанту |
| Рука (rack) | supply | 5 слотів на старті, апгрейд +1 | плитки для слів |
| Особистий мішок | supply | розподіл і вартості як у Scrabble | джерело плиток руки |
| Зелена клітина | terrain | 3× / 5× літери | множить очки літери |
| Синя клітина | terrain | 2× / 3× слова | множить очки слова |
| Клітина power-up | pickup | тип | зіграти слово на неї → предмет в інвентар |
| S-клітина | pickup | — | дає плитку S поза мішком; купити S не можна |
| Бомба | pickup | радіус 3 кроки без діагоналей | знищує сірі плитки навколо активного слова |
| Reroll | pickup | — | замінює всю руку новими з мішка |
| Medkit | pickup | +50 HP (половина максимуму) | лікує |
| Інвентар | supply | 1 слот на старті, апгрейд +1 | тримає power-ups |
| Гаряча зона | hazard | межа звуження | шкода з часом, якщо хоч одна плитка активного слова в ній |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «десант: стартова плитка падає на поле — стрілки керують місцем приземлення»`.
- КОЛИ `input(type word)` → ЯКЩО `in_dictionary(word)` і `custom: «слово торкається власного активного слова»` → ТО `place(player, word tiles)`.
- КОЛИ `input(type word)` → ЯКЩО `custom: «перетин з іншими плитками утворює невалідне слово»` → ТО `block`.
- КОЛИ `after(place)` → ТО `custom: «нове слово стає активним — попереднє сіріє»`.
- КОЛИ `after(place)` → ТО `score(letter values × premiums)` — кожне утворене слово окремо, бонус за довжину; `counter(xp, +n)`.
- КОЛИ `counter(level, +1)` → ТО `currency(+3)`.
- КОЛИ `after(place)` → ЯКЩО `custom: «нове слово зʼєднує моє активне слово з активним словом суперника»` → ТО `custom: «суперник вибухає і вибуває»` — миттєво, незалежно від HP.
- КОЛИ `after(place)` → ЯКЩО `custom: «слово лягло на клітину power-up»` → ТО `pickup(player, power-up)`.
- КОЛИ `timer(12)` (Next Letter, секунди) → ЯКЩО `custom: «у руці є вільний слот»` → ТО `give(player, tile from bag)`; інакше `custom: «таймер скидається»`.
- КОЛИ `custom: «зіграно останню плитку руки»` → ТО `custom: «Rack Refill — повна нова рука безкоштовно»`.
- КОЛИ `input(use bomb)` → ТО `explode(manhattan, 3)` навколо активного слова, `custom: «руйнуються лише сірі плитки — чужі активні слова цілі»`.
- КОЛИ `input(use reroll)` → ТО `custom: «вся рука замінюється новими плитками з мішка»`.
- КОЛИ `input(use medkit)` → ТО `heal(player, 50)`.
- КОЛИ `input(overload)` → ТО `explode(manhattan, 3)`, `take(player, all rack tiles)` — безкоштовна бомба ціною всієї руки.
- КОЛИ `input(buy upgrade)` → ЯКЩО `counter(money, >=, price)` → ТО `currency(-price)`, `custom: «ціна цього апгрейда +1»` — швидше надходження плиток (−1 с), +1 слот руки, +1 слот інвентарю; діють до кінця раунду.
- КОЛИ `input(buy vowel)` → ЯКЩО `counter(money, >=, price)` → ТО `give(player, vowel)`, `custom: «забирає наступну голосну з мішка гравця»` (так само приголосна; змінює статистику майбутніх витягів).
- КОЛИ `schedule(zone)` → ТО `custom: «зона звужується з усіх боків на рівну кількість клітин»`.
- КОЛИ `tick` → ЯКЩО `custom: «хоч одна плитка активного слова в гарячій зоні»` → ТО `damage(player, n)`.
- КОЛИ `hp_zero(player)` → ТО `lose`, `custom: «плитки гравця сіріють»`.
- КОЛИ `died(player)` → ТО `message(kill feed)`, `choose(main menu | spectate)`.
- КОЛИ `custom: «лишився один гравець»` → ТО `win`.
- Перемога: останній живий («have the last word») · Поразка: суперник зʼєднався з твоїм активним словом або HP вичерпано в зоні · Рахунок: очки Scrabble → XP → рівні → гроші раунду.

## Керування і ввід
- Стрілки — зелений індикатор розміщення; Shift — змінити напрям (горизонталь / вертикаль); набір літер з клавіатури — слово; Space / Enter — зіграти.
- Миша теж працює, але клавіатура швидша; Alt + стрілки — рухати мапу.
- Ctrl + T — апгрейд таймера, Ctrl + I — апгрейд інвентарю, Ctrl + R — Overload; утримати Ctrl — список гарячих клавіш.
- Під час десанту стрілки ведуть падаючу плитку.

## Вікна, меню, HUD
- `main-menu`: грати (матчмейкінг на 16) · магазин косметики · налаштування (?).
- `drop-phase` (на `game-screen`): падіння стартової плитки з вибором місця.
- `game-screen`: дошка з `zone-border`, `placement-indicator`, рука (`tile-rack`), `next-letter-timer`, слоти інвентарю (`inventory-bar`), `hp-bar`, гроші (`coins`), XP / рівень, панель магазину апгрейдів, `kill-feed` вибувань.
- `end-screen`: місце в раунді (?); після смерті — вибір головне меню / глядач.
- `shop-window` (косметика): скіни плиток, шапки, емоції, вибір стартової літери — за реальні гроші або зароблене.
- Переходи: main-menu → матчмейкінг → drop-phase → game-screen → (вибув) spectate / main-menu → (переміг) end-screen.

## Фічі поза полем
- `online-multiplayer` на 16; free-to-play з косметикою за гроші (`cosmetic-shop`); Steam-досягнення.
- Режим Golden Royales (опис на Steam пошкоджений) (?).
- Ранній доступ: Season Zero (3–5 місяців); план Season One — нові мапи й механіки, гра в групах, сезонні battle pass; остання оновка — понад 4 роки тому (Steam).
- `spectator` після вибування.

## Варіації й родичі
- Родичі в корпусі: [scrabble.md](scrabble.md) (премії, мішок, словник — основа), [upwords.md](upwords.md), [bananagrams.md](bananagrams.md) (швидкісне викладання без ходів), [letterpress.md](letterpress.md) (слово як захоплення поля), [wordox.md](wordox.md); [../maze-arcade/pac-man-battle-royale.md](../maze-arcade/pac-man-battle-royale.md) — battle royale в іншій сімʼї.
- **Осі варіацій:** звідки «тіло» гравця (активне слово / фішка) · атака (дотик слова / перетин / вибух) · темп (хід / real-time з таймером плиток) · звуження (вибування за межею / шкода з часом).

## Цікавинки для курсу
- Активне слово як аватар: нове слово мусить торкатися попереднього, «тіло» переміщується стрибками — 🥉 (перевірка дотику + рух без координат аватара).
- Елімінація: після кожного викладання перевірити, чи нове слово зʼєднало моє активне з чужим активним (сусідство плиток) — 📎.
- Таймер надходження плиток лише при вільному слоті + Rack Refill за порожню руку — 🌱.
- Особистий мішок з покупкою «наступної голосної» (змінює розподіл подальших витягів) — 📎.
- Бомба: BFS на 3 кроки від усіх плиток активного слова, руйнує лише сірі — 📎.
- Звуження зони за розкладом + шкода, якщо хоч одна плитка в зоні — 🌱.
- Мережева синхронізація 16 гравців, які одночасно кладуть плитки в ті самі клітини (конфлікти) — 👑.

## Мапа на каталог
- Є: `online-multiplayer` · `word-validation` ↔ словник Scrabble · `keyboard-controls` + `cell-click` · `event-points` ↔ очки слів · `round-currency` + `in-round-upgrades` + `shop-catalog` ↔ гроші й апгрейди раунду · `inventory-items` + `inventory-limit` + `item-pickup` ↔ power-ups · `hp-damage` + `environment-death` ↔ зона · `destructible-blocks` ↔ бомба руйнує сірі плитки · `game-screen`, `end-screen`, `main-menu`, `shop-window`.
- **Нема** → пропозиції карток:
  - `+premium-squares`, `+tile-rack`, `+tile-bag-draw` (вже пропоновані Scrabble) — премії, рука, особистий мішок.
  - `+word-as-attack` (вже є в корпусі) — слово атакує суперника.
  - `+active-word-avatar` «Останнє викладене слово — тіло гравця» · entities/move · 🥉.
  - `+shrinking-arena`, `+player-elimination`, `+last-standing-round` (вже пропоновані) — battle royale.
  - `+drop-in-spawn` «Десант: гравець обирає місце приземлення» · entities/spawn · 📎.
  - `+timed-tile-refill` «Нова плитка за таймером, якщо є вільний слот» · game-logic/economy · 🌱.
  - `+rack-refill-bonus` «Порожня рука → повна нова» · game-logic/economy · 🌱.
  - `+kill-feed` «Стрічка вибувань» · interface/hud · 🌱.
  - `+spectate-after-death` «Глядач після вибування» · interface/menus · 📎.
  - `+cosmetic-shop` «Косметика без впливу на гру» · interface/menus · 🌱.

## Пропозиції до словників
- `+trigger:last_standing` (вже пропонований pac-man-battle-royale) — лишився один гравець.
- `+effect:eliminate` — гравець вибуває з матчу (не «смерть з респавном»).
- `+ui:kill-feed` — стрічка вибувань; `+ui:next-letter-timer` — відлік до наступної плитки; `+ui:placement-indicator` — курсор-стрілка напряму слова; `+ui:zone-border` — межа гарячої зони на полі.
- `+window:drop-phase` — фаза десанту з вибором місця.
- `+feature:cosmetic-shop` — косметика за гроші без впливу на гру (ширше за `custom-skins`); `+feature:battle-pass` — сезонний пропуск з рівнями нагород.
- Вісь `control` (кандидат у classes.md): тут `direct` — індикатор стрілками + набір слова з клавіатури.

## Джерела
- ⭐ [biggieblog: Having the Last Word in Babble Royale](https://biggieblog.com/?p=263) — найповніший гайд: поле, рука, мішок, активне слово, таймер плиток, магазин і ціни, power-ups, бомба, премії, зона, гарячі клавіші, стратегія.
- [Wikipedia: Babble Royale](https://en.wikipedia.org/wiki/Babble_Royale) — суть, 16 гравців, hot zone, розробник, дата.
- [Steam: Babble Royale](https://store.steampowered.com/app/1759440/Babble_Royale/) — опис, лут, гроші, магазин, косметика, Season Zero, платформи.
- [WordFinder: Where Scrabble Meets Fortnite](https://wordfinder.yourdictionary.com/blog/the-action-packed-babble-royale-where-scrabble-meets-fortnite) — стартова A, рука з 5, словник Scrabble, активне слово кольором, глядач, апгрейди й косметика.
- YouTube: пошук «Babble Royale gameplay».

## Непевне
- (?) Зона: biggieblog — шкода з часом, якщо плитка активного слова в зоні; WordFinder — автоматичне вибування за межею. Імовірно, правило змінювалося між версіями раннього доступу.
- (?) Розміри 31×31 і етапи звуження, ціни апгрейдів, 12 с таймера — з одного гайду; актуальність для поточної версії не перевірено.
- (?) Максимум HP 100 — виведено з «Medkit +50 HP = половина максимуму».
- (?) Звідки беруться гроші: biggieblog — $3 за рівень XP; WordFinder і Steam — «гроші за слова»; можливо, це одне й те саме через XP.
- (?) Екран результатів матчу, налаштування, режим Golden Royales — не бачив.
