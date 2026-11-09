---
title: ElecHead
slug: elechead
aka: [Elec Head]
family: grid-platformer
also: [connect-rotate]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Switch, Xbox One, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ElecHead", best: true, note: "геймплей: заряд поверхонь дотиком голови, пунктирні блоки, ліфти, лампи, кидок голови й 10 с, 6 стадій з варпами, чекпойнти-пазли, 20 чипів і дві кінцівки"}
  - {kind: steam, url: "https://store.steampowered.com/app/1456880/ElecHead/", note: "реліз 14.10.2021, 13 досягнень, повна підтримка геймпада, 29 мов"}
  - {kind: itch, url: "https://namatakahashi.itch.io/elechead", note: "GameMaker, демо TGS для Windows; коментарі про керування й меню-іконки"}
  - {kind: other, url: "https://www.nintendoworldreport.com/review/60774/elechead-switch-review", note: "огляд NWR: стрибок, кидок голови, варпи, 20 чипів, палітри, ~2 години"}
  - {kind: other, url: "https://www.vice.com/en/article/elechead-is-the-smartest-video-game-ive-played-this-year/", note: "огляд Vice: платформа їде до тебе, вогняні кулі, кидок у кількох напрямках, варп без доступу до платформи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ElecHead+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, keyboard-controls, gravity-fall, carrier-platform, touch-death, player-death, respawn, checkpoint, item-pickup, collect-quota, key-and-door, pause-menu, theme-select, achievements-window, +electric-signal, +conductive-surface, +throw-item, +separation-timer, +flip-screen-rooms, +warp-menu, +collectible-secrets, +multiple-endings]
proposes: ["+cond:powered", "+card:conductive-surface", "+card:separation-timer", "+card:warp-menu", "+feature:multiple-endings"]
author: opus
date: 2026-11-09
---

# ElecHead — робот-лампочка заряджає все, чого торкається головою; голову можна кинути, але тіло без неї живе 10 секунд

## Суть
Пазл-платформер японського інді-автора Nama Takahashi. Робот Elec **електризує будь-яку поверхню, якої торкається його голова**: заряджені поверхні світяться жовтим і вмикають механізми — пунктирні блоки стають твердими, ліфти їдуть, лампи стріляють смертельним розрядом. Пізніше голову можна **кинути** й керувати тілом, яке струму не проводить, але за 10 секунд голову треба підібрати — інакше Elec вибухає. Головоломка — у тому, що увімкнене одночасно допомагає й шкодить.

## Поле і час
- Світ із кімнат-екранів на тайловій сітці; Elec рухається піксельно (ходьба, стрибок), але механізми — це блоки сітки, і заряд іде по поверхнях блоків.
- Шість стадій; на початку кожної — варп; пазли інколи займають кілька кімнат.
- Реальний час: ліфти їдуть, лампи стріляють, таймер голови тікає, поки вона окремо.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Elec (тіло + голова) | player | з головою / без | ходить і стрибає; голова заряджає поверхню дотику |
| Голова (кинута) | projectile | ≤ 10 с окремо | летить на фіксовану відстань у вибраному напрямку, лежить і заряджає, де впала |
| Металева поверхня / блок | terrain | заряджена / ні | світиться жовтим, поки звʼязана з головою (?) |
| Пунктирний блок | gate | є / нема | заряджений → твердий; без заряду → прохідний |
| Ліфт | platform | фіксований напрям | заряджений → їде у своєму напрямку, везе Elec |
| Рухома платформа | platform | — | заряджена → їде (напр., до гравця) |
| Лампа | hazard | — | заряджена, поки звʼязана з головою металом, → смертельний розряд |
| Вогняні кулі | hazard | — | вмикаються зарядом (?) |
| Чекпойнт | switch | — | перезаписує точку відродження; інколи його треба обійти |
| Варп | static | активований / ні | дозволяє перенестись зі стадії на стадію через меню паузи |
| Чип даних | pickup | 20 на гру | лічильник; усі 20 відчиняють двері на початку 6-ї стадії |
| Секретний предмет | pickup | — | відкриває нову палітру кольорів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `contact(head, surface)` → ТО `set_state(surface, charged)`; `custom: «заряд іде по всій металевій поверхні, звʼязаній з головою»` (?).
- КОЛИ `contact(body, surface)` → ЯКЩО `not state(elec, has_head)` → ТО `custom: «тіло не проводить — поверхня не заряджається»`.
- КОЛИ `state_on(dotted_block, charged)` → ТО `set_cell(dotted_block, solid)`; КОЛИ `state_off(…)` → ТО `set_cell(dotted_block, empty)` (?).
- КОЛИ `tick` → ЯКЩО `state(lift, charged)` → ТО `move(lift, own_dir)`; Elec на ліфті їде разом (`carry`).
- КОЛИ `tick` → ЯКЩО `state(bulb, charged)` → ТО `custom: «лампа випускає розряд»`; КОЛИ `contact(elec, discharge)` → ТО `lose`, `respawn(elec, checkpoint)`.
- КОЛИ `input(throw, dir)` → ЯКЩО `state(elec, has_head)` → ТО `throw(head, dir)`, `timer(head, 10)`.
- КОЛИ `contact(body, head)` → ТО `attach(head, body)`, `timer(stop)`.
- КОЛИ `counter(head_timer, ==, 0)` → ЯКЩО `not state(elec, has_head)` → ТО `explode`, `respawn(elec, checkpoint)`.
- КОЛИ `enter(elec, checkpoint)` → ТО `custom: «точка відродження = цей чекпойнт»` — інколи це робить пазл нерозвʼязним, тож чекпойнт обходять.
- КОЛИ `input(pause → warp N)` → ЯКЩО `custom: «варп N активовано»` → ТО `teleport(elec, warp_N)`.
- КОЛИ `picked(elec, chip)` → ТО `counter(chips, +1)`; КОЛИ `counter(chips, ==, 20)` → ТО `custom: «двері на початку 6-ї стадії відчинено»`.
- КОЛИ `picked(elec, secret)` → ТО `custom: «нова палітра»`.
- Перемога: дійти до фінального пристрою (звичайна кінцівка) або через двері чипів (альтернативна). · Поразка: смерть → відродження на чекпойнті, без лічильника життів (?).

## Керування і ввід
- Ходьба й стрибок; кнопка кидка голови (у кількох напрямках, за оглядом Vice); ↓ теж має дію, яку гра не пояснює (коментар на itch).
- Клавіатура або геймпад (Xbox); точна розкладка — (?).

## Вікна, меню, HUD
- `main-menu` (?) і `game-screen` — кімната, Elec, світіння заряджених поверхонь; таймер відʼєднаної голови — (?).
- `pause-menu` — іконки без тексту (коментар на itch), звідти — варпи на початки стадій.
- `map-window` (?) — не згадано; переміщення між стадіями — варп-меню.
- `end-screen` — дві кінцівки; з v1.0.x можна пропустити титри кінцівки (devlog itch).
- `achievements-window` — 13 досягнень (Steam).

## Фічі поза полем
- `checkpoint` + `respawn` як частина пазлу; `warp`-меню (`world-map`-подібна навігація стадіями).
- `collectibles` (20 чипів) → альтернативна кінцівка; секрети → `theme-select` (палітри).
- `achievements`, `localization` (29 мов на Steam), `gamepad-support`.

## Варіації й родичі
- У сімʼї: [That Gravity Glow](that-gravity-glow.md), [Kiki the Nano Bot](kiki-the-nano-bot.md) (пазл-платформери з одним незвичним правилом).
- Поза сімʼєю: Downwell (відсилка-секрет), ігри з сигналами/проводами (`connect-rotate`): тут «провід» — сама поверхня рівня.
- Прототип 2016 року (номінант Japan Game Awards, аматорський розділ); план на 10 стадій скорочено до 6.
- Осі варіацій: **хто проводить** — голова / тіло / предмет; **скільки триває відʼєднання** — без ліміту / таймер (10 с, тут); **що вмикає струм** — блоки / ліфти / пастки.

## Цікавинки для курсу
- Заряд поверхні дотиком і поширення по звʼязаному металу (flood fill по блоках) — 🥉.
- Пунктирні блоки, ліфти, лампи як реакції на стан «заряджено» — 📎 кожна.
- Кидок голови з таймером відʼєднання 10 с і вибухом — 📎.
- Чекпойнт, який треба обійти, і варп-меню як елемент розвʼязку — 🥉.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `gravity-fall`; `carrier-platform` ↔ ліфти; `touch-death` ↔ розряд лампи, вогонь; `player-death` + `respawn` + `checkpoint`; `item-pickup` + `collect-quota` ↔ 20 чипів; `key-and-door` ↔ двері, що відчиняються чипами; `pause-menu`; `theme-select` ↔ палітри; `achievements-window`.
- **Нема** → пропозиції карток:
  - `+conductive-surface` «Поверхня, якої торкається гравець, стає заряженою й живить механізми» · entities/state · 🥉.
  - `+separation-timer` «Частина гравця окремо не довше N тіків» · entities/state · 📎 · слот {limit: 10 s}.
  - `+warp-menu` «Перенесення на відкриті варпи з меню паузи» · levels/progression · 🌱.
  - `+electric-signal`, `+throw-item`, `+flip-screen-rooms`, `+collectible-secrets` — уже пропоновані в корпусі.
  - `+multiple-endings` «Кінцівка залежить від зібраного» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:powered` — сутність під струмом (вже пропонувалась іншими файлами; тут: блоки, ліфти, лампи).
- `+card:conductive-surface`, `+card:separation-timer`, `+card:warp-menu` — див. вище.
- `+feature:multiple-endings` — різні кінцівки за зібраними предметами.

## Джерела
- ⭐ [Wikipedia: ElecHead](https://en.wikipedia.org/wiki/ElecHead) — механіка заряду, пунктирні блоки, ліфти, лампи, кидок голови й 10 с, 6 стадій і варпи, чекпойнти-пазли, 20 чипів, дві кінцівки, палітри, платформи й дати.
- [Steam](https://store.steampowered.com/app/1456880/ElecHead/) — дата, досягнення, мови, геймпад.
- [itch.io](https://namatakahashi.itch.io/elechead) — GameMaker, демо, коментарі (↓ без пояснення, меню-іконки, 6 світів).
- [Nintendo World Report](https://www.nintendoworldreport.com/review/60774/elechead-switch-review) — стрибок, кидок голови, варпи, чипи, палітри, тривалість.
- [Vice](https://www.vice.com/en/article/elechead-is-the-smartest-video-game-ive-played-this-year/) — платформа до гравця, вогняні кулі, кидок у кількох напрямках, 10 с, варпи без доступу до платформи.
- [TV Tropes: Conspicuous Electric Obstacle](https://tvtropes.org/pmwiki/pmwiki.php/Main/ConspicuousElectricObstacle) — фрагмент у пошуку: лампи стріляють, поки Elec і лампа звʼязані металевою поверхнею (сама сторінка не відкрилась).
- YouTube: пошук «ElecHead gameplay».

## Непевне
- (?) Чи заряд поширюється на всю звʼязану металеву конструкцію, чи лише на поверхню дотику: Wikipedia — «всі поверхні при контакті», TV Tropes (фрагмент) — звʼязок «через металеву поверхню».
- (?) Чи пунктирні блоки зникають одразу після зняття заряду; поведінка вогняних куль; шипи й інші пастки.
- (?) Розкладка кнопок, дія ↓, HUD-таймер голови, головне меню, наявність лічильника життів.
- (?) Значення «какашок»-іконок з огляду NWR (рецензент припускав мітки глухих кутів).
