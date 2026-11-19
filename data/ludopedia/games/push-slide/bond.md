---
title: BOND
slug: bond
aka: [BOND Lite, "BOND Lite: Block Push Puzzle"]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2024
platforms: [PC (Windows), Linux (SteamOS), iOS (Lite), Android (Lite)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2835670/BOND/", best: true, note: "Gustav Almström, Dennis Qvarfordt Hammarlind, 28.05.2024; «Bind together, clone yourself and fly over the obstacles in your path!»; три кліпи й трейлер ≈41 с: зчеплення, клонер, камені в рові, оверворлд"}
  - {kind: official, url: "https://gustavalmstrom.com/bond/presskit.html", note: "прескіт: «evolution of the classic Sokoban», «Cloners let you make copies of other objects», міст із клонованих каменів, 64 рівні"}
  - {kind: official, url: "https://gustavalmstrom.com/bond/game.html", note: "сторінка гри: Steam, App Store, Google Play"}
  - {kind: other, url: "https://apps.apple.com/gb/app/bond-lite-block-push-puzzle/id6479915184", note: "BOND Lite (iOS): безкоштовне демо, перші 21 рівень повної гри"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.gustavalmstrom.pusher_lite", note: "BOND Lite (Android)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BOND+Gustav+Almstrom+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [move-4dir, push-object, stick-together, gravity-fall, height-levels, fill-hole, completion-detection, sequential-levels, world-map, +exact-cover-outline, +cloner-element, +multi-agent-sync, +rigid-shape-fall, +arrow-launch, +bind-on-touch]
proposes: ["+effect:launch", "+cond:shape_match", "+role:cloner", "+card:bind-on-touch", "+card:cloner-copy", "+card:arrow-launch", "+card:fill-ghost-shape"]
author: opus
date: 2026-11-19
---

# BOND — синій куб чіпляє до себе кубики-«серця», клонує себе й камені та має точно заповнити напівпрозору фігуру-ціль

## Суть
Воксельний 3D-Sokoban, де гравець — не один куб, а **тіло з кубів**: зелені кубики з серцем, до яких він підходить, синіють і зчіплюються з ним («Bind together»). Мета рівня — поставити тіло так, щоб воно точно заповнило напівпрозору синю фігуру; тому тіло доводиться нарощувати до потрібної форми. Друга лінія — **клонери**: вони копіюють обʼєкти, і з клонованих каменів будують міст через рів (прескіт). Ще є помаранчеві блоки зі стрілками, що дають «перелетіти» перешкоди, і камені, які падають у рів і стають підлогою.

## Поле і час
- Воксельна сітка з висотами (`field: 3d`): острів-рівень із ровами, уступами й стовпами; камера під кутом, фіксована (?).
- Хід = зсув тіла на клітину; без вводу нічого не рухається.
- Тіло тверде: зсувається цілим; довге тіло може лягти мостом через рів, спираючись краями (кадр мануала Steam, трейлер).
- Рівень складається з кубів, що злітаються, і розсипається, коли розвʼязаний; рівні обʼєднано оверворлдом — воксельною мапою зі стежками й назвами рівнів («Highway 61»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синій куб (тіло гравця) | player | кількість кубів, форма | зсувається цілим; чіпляє «серця»; кілька окремих синіх тіл ходять одночасно (?) |
| Зелений куб із серцем | ally | — | коли тіло поруч, синіє й стає його частиною |
| Сірий камінь | object | — | штовхається; без опори падає; у рові стає підлогою-мостом |
| Клонер (рожевий напівпрозорий куб) | spawner | — | копіює обʼєкт, що в ньому: куб тіла, камінь |
| Блок зі стрілкою (помаранчевий, ▲ / ▷) | terrain | напрям стрілки | «підкидає» чи несе тіло в напрямку стрілки («fly over the obstacles») (?) |
| Фігура-ціль (напівпрозора синя) | zone | форма | заповнити тілом точно — рівень пройдено |
| Земля, рови, уступи | static | висота | опора й перешкоди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cells)` → ТО `move(body, dir)` — тіло зсувається цілим; окремі сині тіла рухаються одночасно (трейлер, зелений рівень із двома кубами).
- КОЛИ `adjacent(body, heart_cube)` → ТО `attach(body, heart_cube)` — зелений куб синіє й стає частиною тіла (трейлер, перший рівень: тіло росте до бруска з чотирьох).
- КОЛИ `contact(body, stone)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `turn_end` → ЯКЩО `not supported(stone)` → ТО `fall(stone)` — камінь у рові стає опорою, по ньому переходять на інший бік (трейлер).
- КОЛИ `turn_end` → ЯКЩО `custom: «жоден куб тіла не має опори»` → ТО `fall(body)` — тіло-міст тримається, поки спирається хоча б одним кубом (?).
- КОЛИ `enter(object, cloner)` → ТО `clone(object)` — копія куба приєднується до тіла, копії каменя складаються в стовп чи міст (прескіт: «if they clone the stone-block enough times» — міст через рів) (?).
- КОЛИ `enter(body, arrow_block)` → ТО `custom: «летіти в напрямку стрілки до упору»` (опис «fly over the obstacles in your path», трейлер: тіло проходить над прірвою смугою зі стрілками ▷) (?).
- КОЛИ `custom: «тіло точно заповнило фігуру-ціль»` → ТО `win`, `next_level` — рівень розсипається, складається наступний.
- Перемога: тіло (чи тіла) збігається з напівпрозорою фігурою. · Поразка: не показано; падіння за край — (?). · Рахунок: нема.

## Керування і ввід
- Чотири напрямки руху тіла; ПК — геймпад (повна підтримка) і клавіатура (?); мобільна Lite-версія — дотик (?).
- Undo й рестарт у джерелах не згадано (?).

## Вікна, меню, HUD
- Оверворлд (`map-window`): воксельна мапа зі стежками з білих позначок, назва рівня над входом («Highway 61»), біля стежок — сірі камені (?).
- `game-screen`: рівень-острів; HUD у кліпах не видно.
- Перехід «зібрати / розсипати» рівень із кубів між оверворлдом і рівнем.
- Меню й налаштування — (?); 10 мов інтерфейсу (Steam).

## Фічі поза полем
- 64 рівні, «кожен учить чогось нового» (прескіт); оновлення «Level rework» (2025): рівень «Damned dam» звужено, «tool meditation levels» переставлено, «Finesse» прибрано.
- Безкоштовна BOND Lite для iOS / Android — перші 21 рівень повної гри, без реклами.
- Steam Cloud, повна підтримка геймпада; музика й звуки — Dennis Qvarfordt Hammarlind.

## Варіації й родичі
- [stackrobats](../grid-platformer/stackrobats.md) — дотик вмикає акробатів, і звʼязна група ходить разом; [sokobond](../thinky/sokobond.md) — атоми зчіплюються при контакті.
- [boxboy](../grid-platformer/boxboy.md) — герой видавлює з себе коробки, щоб будувати міст; [patricks-parabox](../thinky/patricks-parabox.md) — клонування ящиків.
- [order-of-the-sinking-star](../thinky/order-of-the-sinking-star.md) — кілька героїв ходять разом; [sokoban](sokoban.md) — база.
- Осі варіацій:
  - **хто «я»**: один куб (Sokoban) / тіло, що росте, чіпляючи інші (тут) / змійка (Snakebird);
  - **мета**: ящики на цілях / тіло точно заповнює фігуру-контур (тут);
  - **звідки беруться нові обʼєкти**: нізвідки / клонер копіює наявний (тут) / герой видавлює з себе (BoxBoy).

## Цікавинки для курсу
- Тіло з кубів, що росте від «сердець» і рухається як тверда фігура (перевірка вільності для всіх кубів) — 🥉.
- Перевірка «тіло точно заповнило фігуру-ціль» (рівність множин клітин) — 📎.
- Клонер, що копіює обʼєкт, і мости з копій — 🥉.
- Падіння твердої фігури: падає, лише коли жоден куб не має опори — 🥉.
- Оверворлд-мапа зі стежками й назвами рівнів — 📎.

## Мапа на каталог
- Є: `move-4dir`; `push-object` ↔ камені; `stick-together` ↔ «серця» зчіплюються з тілом; `gravity-fall` ↔ камені падають у рів; `height-levels` ↔ уступи й стовпи; `fill-hole` ↔ камінь у рові стає підлогою; `completion-detection`; `sequential-levels` + `world-map` ↔ оверворлд.
- **Нема** → пропозиції карток:
  - `+bind-on-touch` «Обʼєкт поруч приєднується до тіла гравця й далі рухається з ним» · entities/interact · 🥉 (родич `stick-together`, але росте саме аватар).
  - `+cloner-copy` «Клонер копіює обʼєкт, що в нього потрапив» · entities/spawn · 🥉 (підтверджує `+cloner-element`).
  - `+arrow-launch` «Блок зі стрілкою кидає чи несе тіло в напрямку стрілки» · entities/move · 📎 (?).
  - `+fill-ghost-shape` «Мета — тілом точно заповнити напівпрозору фігуру» · game-logic/win · 📎 (родич `+exact-cover-outline`).
  - `+multi-agent-sync`, `+rigid-shape-fall` — підтверджую наявні нові теги.

## Пропозиції до словників
- `+effect:launch` — підкинути / понести тіло в напрямку стрілки (уже пропонований іншими іграми).
- `+cond:shape_match` — форма тіла збігається з фігурою-ціллю (уже пропонована).
- `+role:cloner` — клітина-копіювальник (ширше, ніж `spawner`: копіює те, що в неї ввійшло).
- `+card:bind-on-touch`, `+card:cloner-copy`, `+card:arrow-launch`, `+card:fill-ghost-shape`.

## Джерела
- ⭐ [Steam: BOND](https://store.steampowered.com/app/2835670/BOND/) — опис («Bind together, clone yourself and fly over the obstacles»), мови, контролер; три кліпи (зчеплення з «серцями», клонер і тіло-міст, камені в рові) і трейлер ≈41 с; новина «Level rework» (2025).
- [Прескіт](https://gustavalmstrom.com/bond/presskit.html) — «evolution of the classic Sokoban», «Cloners let you make copies of other objects», міст із клонованих каменів, 64 рівні, історія розробки.
- [Сторінка гри](https://gustavalmstrom.com/bond/game.html) — посилання на Steam, App Store, Google Play.
- [App Store: BOND Lite](https://apps.apple.com/gb/app/bond-lite-block-push-puzzle/id6479915184) — демо з 21 рівнем, «Bind together, clone yourself, or fly over the obstacles».
- YouTube: пошук «BOND Gustav Almstrom puzzle gameplay».

## Непевне
- (?) Як саме працює клонер: копія зʼявляється в сусідньому клонері, над ним чи на місці; чи копія куба гравця завжди приєднана до тіла.
- (?) Що роблять помаранчеві блоки зі стрілками ▲ / ▷: підкидають, несуть як конвеєр, чи це траєкторія польоту; чи їх можна штовхати.
- (?) Чи окремі сині тіла завжди рухаються разом і чи зливаються, зустрівшись; чи буває кілька фігур-цілей.
- (?) Сірий камінь із рожевим серцем на скріншоті — окремий тип обʼєкта (?).
- (?) Undo, рестарт, меню й налаштування; що буває при падінні тіла за край.
