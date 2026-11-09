---
title: Rabi Laby (Rabi×Rabi)
slug: rabi-laby
aka: [Rabi×Rabi, ラビ×ラビ, Rabbit Labyrinth, Rabbit★Labyrinth, Rabi Laby 2, Rabi Laby 3, Кролячий лабіринт]
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 2010
platforms: [mobile (au BREW, iOS), DSiWare, 3DS, PS Vita, PS4, Switch]
links:
  - {kind: other, url: "https://apps.apple.com/lk/app/id369863865?l=en-gb", best: true, note: "Rabbit Labyrinth (iOS): правила — Аліса несе кролика, стрибає з нього, відмикає замки; кролик підривається й ламає цеглу в 4 боки, носить ключ; 30 рівнів, рекорд часу"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%93%C3%97%E3%83%A9%E3%83%93", note: "серія: персонажі й мешканці рівнів (Чеширський кіт, карткові солдати, Грифон, Черепаха, краб, жаба, гусінь, привид), дати й платформи"}
  - {kind: other, url: "https://nintendo.com/en-gb/Games/Nintendo-DSiWare/Rabi-Laby-696743.html", note: "DSiWare: перемикання між Алісою й Рабі, ключ і вихід, 50 рівнів, медалі"}
  - {kind: other, url: "https://www.nintendo.com/en-gb/Games/Nintendo-DSiWare/Rabi-Laby-2-780634.html", note: "Rabi Laby 2: монети-підказки, медалі за ефективність відкривають бонус-рівні, 50 рівнів"}
  - {kind: other, url: "https://www.nintendolife.com/reviews/2011/03/rabi_laby_dsiware", note: "рецензія (у фетчі 403; бачено в пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rabi+Laby+DSiWare+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, gravity-fall, party-switch, carrier-platform, destructible-blocks, blast-wave, key-and-door, reach-exit, touch-death, environment-death, enemy-patrol, timed-despawn, sequential-levels, level-unlock, level-select, score-records, +carry-object, +partner-boost, +self-destruct, +key-courier, +knockback, +one-use-platform, +hint-pickup, +efficiency-medals, +bonus-stage]
proposes: ["+effect:knockback", "+card:partner-boost", "+card:key-courier", "+card:one-use-platform", "+card:hint-pickup", "+card:efficiency-medals"]
author: opus
date: 2026-11-09
---

# Rabi Laby — Аліса і кролик Рабі (Лілі) по черзі: з голови кролика стрибок вищий, а кролик підривається й ламає цеглу

## Суть
Дует-платформер за мотивами «Аліси в Країні чудес»: гравець перемикається між Алісою й кроликом, і рівень проходиться лише їхньою співпрацею. Аліса стрибає низько, зате падає повільно, носить кролика чи предмети на голові, відмикає замки й мусить дійти до виходу. Кролик стрибає високо, носить ключ туди, куди Аліса не дістає, і **самопідривом** руйнує цеглу в чотирьох сусідніх клітинах. Мешканці рівнів — то вороги (дотик = промах), то «транспорт», на якому можна їхати.

## Поле і час
- Бічний вид, клітинна розмітка: цегла, замки й блоки займають клітини, вибух кролика бʼє по 4 сусідніх клітинах (`field: square`).
- Real-time з гравітацією; вороги й тварини рухаються самі, неактивний персонаж стоїть (?).
- Рівень вміщується на екран або скролить — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аліса | player | низький стрибок, повільне падіння | несе кролика або предмет на голові; відмикає замки; її вихід завершує рівень |
| Рабі (Лілі) | player | високий стрибок | самопідрив ламає цеглу хрестом; носить ключ; не любить води |
| Цегла | object | — | непрохідна; руйнується лише вибухом кролика |
| Ключ | pickup | колір | відмикає замок того ж кольору |
| Замок (keyhole) | gate | колір | відкривається Алісою з ключем свого кольору |
| Вихід (gateway, двері) | static | — | Аліса дійшла — рівень пройдено |
| Чеширський кіт | enemy | стоїть / ходить | блокує шлях високими стрибками; одні стрибають, коли підходиш, інші ходять туди-сюди; відкидає героїв |
| Карткові солдати | enemy | 2 типи | одні ходять туди-сюди й стрибають на стіни, інші ходять повільно й періодично трусять землю; дотик = промах |
| Капелюшник / капелюх (Cap) | object | — | Аліса піднімає на голову або штовхає; правий за сходинку |
| Грифон | neutral | рух по вертикалі або горизонталі | везе того, хто сів, у недосяжні місця |
| Черепаха Квазі | neutral | — | перевозить через ями з шипами |
| Краб | neutral | — | ходить туди-сюди над водою, везе Рабі |
| Жаба | neutral | 1 використання | стрибає; стати на неї — висота стрибка кролика; потім зникає |
| Гусінь | neutral | — | повільна платформа; згодом стає коконом і зупиняється |
| Привид | enemy | — | підлітає й лякає: Аліса завмирає на мить; кролика не чіпає |
| Чорний кролик | enemy | — | у руїнах кружляє по платформах; дотик = промах; магія не діє |
| Шипи | hazard | — | дотик = промах (?) |
| Вода | hazard | — | для кролика непрохідна (?) |
| Монета-підказка | pickup | — | Rabi Laby 2: дає підказку на рівні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(switch)` → ТО `custom: «активний персонаж: Аліса ↔ Рабі»`.
- КОЛИ `input(jump)` → ЯКЩО `state(active, alice)` → ТО `custom: «низький стрибок, повільне падіння»`; ЯКЩО `state(active, rabi)` → ТО `custom: «високий стрибок»`.
- КОЛИ `contact(alice, rabi)` (Аліса стрибнула з кролика) → ТО `custom: «Аліса злітає вище, ніж сама»`.
- КОЛИ `input(lift)` → ЯКЩО `adjacent(alice, rabi)` або `adjacent(alice, cap)` → ТО `carry(alice, rabi|cap)` — на голові.
- КОЛИ `input(explode)` → ЯКЩО `state(active, rabi)` → ТО `explode(cross, 1)`: цегла в 4 сусідніх клітинах `disappear`; що далі з кроликом — `custom: «повертається»` (?).
- КОЛИ `contact(alice, brick)` або `contact(rabi, brick)` → ТО `block`.
- КОЛИ `contact(rabi, key)` або `contact(alice, key)` → ТО `pickup`; кролик доставляє ключ до Аліси через місця, куди їй не дістатися.
- КОЛИ `contact(alice, keyhole)` → ЯКЩО `has(alice, key)` і `same(key, keyhole, color)` → ТО `disappear_b`; інакше `block`.
- КОЛИ `contact(alice, cap)` збоку → ТО `push`.
- КОЛИ `contact(alice, card_soldier)` або `contact(rabi, card_soldier)` → ТО `lose` (промах).
- КОЛИ `contact(any, black_rabbit)` → ТО `lose`.
- КОЛИ `in_range(cheshire_cat, alice, n)` → ТО `custom: «стрибає»`; КОЛИ `contact(cheshire_cat, alice|rabi)` → ТО `custom: «відкидає героя вбік»`.
- КОЛИ `blocked(card_soldier)` → ТО `custom: «стрибає на стіну»`; повільний солдат — КОЛИ `timer(every)` → ТО `custom: «трусить землю»` (наслідок для героїв — (?)).
- КОЛИ `contact(alice|rabi, gryphon|mock_turtle|crab)` згори → ТО `carry(creature, rider)`; Черепаха — через шипи, краб — Рабі над водою.
- КОЛИ `contact(alice|rabi, frog)` згори → ТО `custom: «підкидає на висоту стрибка кролика»`, `disappear_b`.
- КОЛИ `timer(n)` → ТО `transform(caterpillar, cocoon)` — платформа зупиняється.
- КОЛИ `in_range(ghost, alice, n)` → ТО `stun(alice, n)`; Рабі привид не діє; в Episode 3 вибух кролика знищує привидів.
- КОЛИ `contact(alice, gateway)` → ТО `win`, `next_level`, `custom: «рекорд часу рівня»`.
- КОЛИ `level_end` → ТО `custom: «медаль-ранг за ефективність проходження»`; медалі відкривають бонус-рівні (Rabi Laby 2).
- КОЛИ `contact(alice|rabi, hint_coin)` → ТО `pickup`; КОЛИ `input(hint)` → ЯКЩО `has(team, hint_coin)` → ТО `custom: «показати підказку»` (Rabi Laby 2).
- Перемога: Аліса у виході. · Поразка: дотик ворога → промах і рестарт рівня (?); лічильника життів, схоже, нема (?). · Рахунок: час проходження і медалі.

## Керування і ввід
- Хрестовина — ходьба, кнопки — стрибок, перемикання персонажа, підняти/покласти, підрив (точне призначення — (?)).
- Сенсорний екран DSi у джерелах не згаданий; iOS-версія — екранні кнопки (?).

## Вікна, меню, HUD
- `splash-screen` (?) — титул.
- `level-select`: на старті відкрито 5 рівнів з 30 (iOS), далі — після проходження; позначки медалей (DSiWare).
- `dialogue-window` — сюжетні сцени Країни чудес між рівнями (?).
- `game-screen`: рівень; HUD — `timer-elapsed` (час проходження), активний персонаж (?), монети-підказки (Rabi Laby 2).
- `hints-window` — підказка за монету (Rabi Laby 2).
- `end-screen`: час, медаль-ранг (?).
- `pause-menu` (?) — продовжити, рестарт, вихід.
- Переходи: level-select → game-screen → (Аліса у виході) end-screen → level-select / наступний рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 30 рівнів (iOS), 50 (DSiWare і Rabi Laby 2).
- `stars-rating`-аналог: медалі-ранги за ефективність; у Rabi Laby 2 вони відкривають бонус-рівні.
- `leaderboard-local`-аналог: найкращий час кожного рівня (iOS).
- `hint`: монети-підказки, розкидані по рівнях (Rabi Laby 2).

## Варіації й родичі
- Rabbit★Labyrinth (au BREW, 02.2010; iOS v1.0 13.05.2010, 30 рівнів) → Rabi×Rabi / Rabi Laby (DSiWare, JP 1.09.2010; покращений порт, 50 рівнів).
- Rabi Laby 2 (DSiWare, 2011): Королева посилає котів; монети-підказки, медалі відкривають бонус-рівні.
- Rabi Laby Gaiden: Witch's Cat (3DS, 2011): героїня Арісія — людина або Чеширська кішка (як кішка — подвійний стрибок, як Лілі); магія Дюбуа ламає й рухає блоки, лід перетворює ворогів на крижані блоки, вогонь проганяє привидів.
- Rabi Laby 3 / Episode 3 (3DS, 2012): вибух кролика знищує привидів.
- Rabi×Rabi: Puzzle Outstories (Vita 2017, PS4/Switch 2018) — збірка 1, 2, Witch's Cat і 3 з оновленою графікою й новим вмістом.
- Родичі в сімʼї: `catrap` і `toki-tori` (дует / набір дій), `lode-runner` (вибух/копання цегли), `boxboy` (герой як інструмент); The Lost Vikings — партія з різними вміннями.
- Осі варіацій:
  - **як руйнувати**: кирка/лопата (Lode Runner) / самопідрив напарника хрестом (Rabi Laby) / магія (Witch's Cat);
  - **як підняти висоту стрибка**: стати на напарника / одноразова жаба / їхати на тварині;
  - **хто має дійти до виходу**: один ключовий герой (Аліса) / усі (`kwirk`).

## Цікавинки для курсу
- Два аватари з різною фізикою стрибка (висота, швидкість падіння) і перемикання — 🥉.
- Стрибок з голови напарника як «сходинка»: аватар — опора для іншого — 📎.
- Самопідрив хрестом, що ламає лише цеглу, — 🌱 (картка `blast-wave` з radius 1).
- Ключ, який носить «не той» персонаж: доставка предмета між героями — 📎.
- Тварини-транспорт з різними траєкторіями (грифон, краб, черепаха) і одноразова жаба — 🥉 (сімʼя `carrier-platform`).
- Медаль-ранг за ефективність + відкриття бонус-рівнів — 📎.

## Мапа на каталог
- Є: `move-by-input` ↔ ходьба; `gravity-fall` ↔ падіння; `party-switch` ↔ Аліса ↔ Рабі; `carrier-platform` ↔ Грифон, черепаха, краб, гусінь; `destructible-blocks` + `blast-wave` ↔ цегла й вибух хрестом; `key-and-door` ↔ ключ і замок кольору; `reach-exit` ↔ gateway; `touch-death` + `environment-death` ↔ солдати, шипи; `enemy-patrol` ↔ солдати й коти; `timed-despawn` ↔ жаба, кокон; `sequential-levels` + `level-unlock` + `level-select`; `score-records` ↔ рекорд часу.
- **Нема** → пропозиції карток:
  - `+carry-object` (вже пропонована) — Аліса несе кролика/капелюх на голові.
  - `+partner-boost` «Стрибок з напарника вище» · entities/move · 📎.
  - `+self-destruct` (вже пропонована) — підрив кролика.
  - `+key-courier` «Предмет доставляє інший персонаж» · entities/interact · 📎.
  - `+knockback` (вже пропонована) — Чеширський кіт відкидає.
  - `+one-use-platform` «Платформа-трамплін на одне використання» · entities/interact · 🌱 — жаба.
  - `+hint-pickup` «Монета-підказка на рівні» · game-logic/economy · 🌱.
  - `+efficiency-medals` «Медаль-ранг за ефективність проходження» · game-logic/score · 📎.
  - `+bonus-stage` (вже пропонована) — бонус-рівні за медалі.

## Пропозиції до словників
- `+effect:knockback(a, dir)` — сутність відкидає іншу на кілька клітин (Чеширський кіт).
- `+card:partner-boost`, `+card:key-courier`, `+card:one-use-platform`, `+card:hint-pickup`, `+card:efficiency-medals` — див. «Мапа на каталог».

## Джерела
- ⭐ [App Store: Rabbit Labyrinth](https://apps.apple.com/lk/app/id369863865?l=en-gb) — уміння Аліси й кролика, цегла лише від вибуху, ключі й замки кольору, вихід, Чеширський кіт, Грифон/Черепаха/Cap, 30 рівнів, 5 відкрито на старті, рекорд часу.
- [ja.wikipedia: ラビ×ラビ](https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%93%C3%97%E3%83%A9%E3%83%93) — персонажі серії й мешканці рівнів з поведінкою, Witch's Cat, Episode 3, дати й платформи.
- [Nintendo UK: Rabi Laby](https://nintendo.com/en-gb/Games/Nintendo-DSiWare/Rabi-Laby-696743.html) — перемикання персонажів, ключ і вихід, 50 рівнів, медалі.
- [Nintendo UK: Rabi Laby 2](https://www.nintendo.com/en-gb/Games/Nintendo-DSiWare/Rabi-Laby-2-780634.html) — високий стрибок і підрив Рабі, монети-підказки, медалі за ефективність → бонус-рівні.
- [Nintendo Life](https://www.nintendolife.com/reviews/2011/03/rabi_laby_dsiware) — рецензія (у фетчі 403; опис — з результатів пошуку).
- YouTube: пошук «Rabi Laby DSiWare gameplay».

## Непевне
- (?) Що стається з кроликом після самопідриву (зникає й повертається на місце / одразу поруч); чи вибух шкодить Алісі й ворогам у першій грі.
- (?) Котрі мешканці є вже в першій грі, а котрі зʼявились у Episode 2/3 — JA-вікі описує серію загалом.
- (?) Чи мають обидва персонажі дійти до виходу: iOS-опис каже «Аліса», сторінка Rabi Laby 2 — «використати обох».
- (?) Шипи, вода для кролика, ефект «трусіння землі» солдатом, рахунок життів — не перевірено.
- (?) Західні дати DSiWare: Time Extension (у результатах пошуку) — 14.03.2011, Nintendo UK — 27.12.2012; можливо, різні регіони.
- (?) Розробник: JA-вікі називає лише видавця Silver Star Japan; на заході — Agetec.
