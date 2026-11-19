---
title: Altered
slug: altered
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [Windows, macOS, Linux]
links:
  - {kind: other, url: "https://buried-treasure.org/2021/05/altered/", best: true, note: "найдокладніший огляд механік: статуя з перпендикулярними руками до 3 клітин, руки з твердою лише долонею, магнітний блок ланцюгами; падіння = відкат; undo скасовує й рестарт; кілька пазлів відкрито одночасно"}
  - {kind: steam, url: "https://store.steampowered.com/app/973250/Altered/", note: "80+ пазлів, 12.03.2021, Glitchheart / Rooftop Panda; теги Sokoban, Grid-Based Movement, Nonlinear; досягнення з іменами персонажів Norn, Seeker, Guard, Burdened"}
  - {kind: other, url: "https://lifeisxbox.eu/review-altered", note: "огляд: 4 персонажі, мета — плитка зі знаком світла, падіння не карає, підказок нема"}
  - {kind: other, url: "https://itch.io/post/2828258/view-in-topic", note: "реліз-пост Glitchheart з двома GIF геймплею (сама сторінка гри на itch уже 404)"}
  - {kind: other, url: "https://www.gamingonlinux.com/2021/02/strange-shape-shifting-puzzler-altered-releases-on-march-12/page=1", note: "анонс релізу: «move and morph yourself around small areas»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Altered+Glitchheart+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, stick-together, button-toggle, reach-exit, undo-unlimited, restart-level, level-unlock, +extendable-arms, +perpendicular-arms, +solid-hand-only-arms, +magnet-chain-attach, +leave-double, +auto-undo-on-fall, +undoable-reset, +character-unlock, +open-world-hub]
proposes: ["+effect:extend", "+effect:retract", "+feature:undo-restart", "+axis:actors", "+card:perpendicular-arms", "+card:solid-hand-only-arms", "+card:magnet-chain-attach", "+card:auto-undo-on-fall"]
author: opus
date: 2026-11-19
---

# Altered — Sokoban, де ти сам частина пазла: висувай руки, чіпляйся магнітом чи лишай дубль, щоб дістатися плитки світла

## Суть
Медитативний Sokoban на парящих плитках: у кожному пазлі треба дійти до плитки зі знаком світла, не впавши з платформи. Ходить не людина, а персонаж-фігура зі своєю силою: золота статуя висуває руки (і ними штовхає ящики), інша — руки, у яких тверда лише долоня, третій — магнітний блок, що чіпляється до інших блоків ланцюгами. Ящики на перемикачах відчиняють ворота. Понад 80 пазлів у відкритому світі, кілька з них доступні одночасно; падіння не карає — гра відкочує хід.

## Поле і час
- Квадратна сітка плиток-платформ над порожнечею; 3D-графіка з видом згори (на GIF — острівці плиток серед осіннього лісу й джунглів).
- Шари: плитки (підлога, перемикачі, ворота, плитка-ціль) + персонаж із руками + ящики.
- Покроково, без таймера й лічильника ходів («no move counter, no time limit, no star rating»).
- Світ відкритий: кілька пазлів доступні одночасно, між ними й між типами персонажів можна перемикатися.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Norn — золота статуя | player | руки до 3 клітин | висуває руки вгору / вниз / ліворуч / праворуч, лише перпендикулярно (не вгору й униз разом); руки штовхають ящики |
| Burdened (?) | player | руки, як у Norn | тверда лише долоня на кінці руки, решта руки не зачіпає обʼєктів |
| Guard (?) — магнітний блок | player | — | рук не має; чіпляється до блоків будь-якою гранню, ланцюгами |
| Seeker (?) | player | — | лишає дубль себе (?) |
| Ящик (червоний куб) | object | — | штовхається на 1; на перемикачі відчиняє ворота |
| Перемикач | switch | — | ящик на ньому відчиняє ворота |
| Ворота | gate | зачинені / відчинені | відкривають новий шлях |
| Плитка світла | static | — | ціль пазла |
| Плитка-платформа | terrain | — | опора; поза плитками — порожнеча |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(character, dir)` — крок плиткою (?).
- КОЛИ `input(arm, dir)` → ЯКЩО `custom: «рука в протилежному напрямку не висунута»` і `counter(arm_length, <, 3)` → ТО `custom: «рука висувається на клітину»` (?).
- КОЛИ `contact(arm, box)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `custom: «рука Burdened проходить клітину з обʼєктом»` → ЯКЩО `custom: «це не долоня на кінці»` → ТО `custom: «обʼєкт не зачеплено»`.
- КОЛИ `adjacent(guard, block)` → ТО `attach(guard, block)` (?) — зчеплення будь-якою гранню, ланцюгом через кілька блоків.
- КОЛИ `input(action)` → ЯКЩО `custom: «персонаж — Seeker»` → ТО `clone(seeker)` (?).
- КОЛИ `enter(box, switch)` → ТО `set_state(gate, open)`.
- КОЛИ `after(move)` → ЯКЩО `not supported(character)` → ТО `undo` — опора є, якщо будь-яка частина персонажа чи його рук торкається плиток; інакше «it'll just reset you to exactly where you were».
- КОЛИ `reach(character, light_tile)` → ТО `win`.
- КОЛИ `input(restart)` → ТО `restart`; рестарт — теж хід, його скасовує undo.
- Перемога: персонаж на плитці світла. · Поразка: нема («no dangers») — падіння відкочується. · Рахунку нема.

## Керування і ввід
- Рух по сітці й керування силою персонажа (висунути / втягнути руку, зчепитися, лишити дубль); точні клавіші — (?).
- Undo без ліміту, рестарт пазла (скасовується undo); повна підтримка контролера (Steam).

## Вікна, меню, HUD
- `game-screen` — 3D-острівець плиток з персонажем; HUD мінімальний (лічильника ходів нема).
- Світ-хаб: пазли розкидані світом, кілька відкрито одночасно; нові персонажі відкриваються з прогресом.
- `main-menu`, `pause-menu`, `settings-window` — (?), джерела їх не описують.

## Фічі поза полем
- `undo` без ліміту, разом зі скасуванням рестарту (`+feature:undo-restart`); `restart-level`.
- Відкритий світ із вибором пазлів; `unlockables` — нові персонажі (досягнення «Unlock the Seeker», «Unlock the Guard», «Unlock the Burdened»).
- `achievements` у Steam (8): The Norn, The Seeker, The Guard, The Burdened, First Steps і три «Unlock…»; Steam Cloud; `gamepad-support`.
- Підказок нема (LifeisXbox: «there are no hints available. Ever.»).

## Варіації й родичі
- [GRAB-O](grab-o.md) — кінцівки, що тягнуться клітинками; [Handshakes](handshakes.md) — руки від бази з бюджетом довжини; [Sokobond](sokobond.md) — зчеплення при дотику; [Heroes of Sokoban](heroes-of-sokoban.md) — персонажі з різними дієсловами.
- **Осі варіацій:** форма персонажа — сталий блок / руки, що висуваються (Norn) / зчеплення з іншими блоками (Guard) / дубль (Seeker) · що в руці тверде — уся рука / лише долоня (Burdened) · падіння — смерть / відкат ходу (тут) · рестарт — поза історією / хід, який скасовує undo (тут).

## Цікавинки для курсу
- Перпендикулярні руки до 3 клітин із забороною протилежних напрямків — 📎.
- Різна колізія для частин одного тіла: рука проходить, долоня штовхає — 📎.
- Магнітне зчеплення будь-якою гранню в ланцюги й рух групою — 🥈.
- Опора «будь-якою частиною» і автоматичний відкат за падіння — 🌱.
- Undo, що скасовує й рестарт (рестарт — запис у стеку) — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ ящики; `multi-cell-size` ↔ персонаж із руками; `stick-together` ↔ магнітне зчеплення; `button-toggle` ↔ перемикач і ворота; `reach-exit` ↔ плитка світла; `undo-unlimited`, `restart-level`; `level-unlock` ↔ нові персонажі й пазли.
- **Нема** → пропозиції карток:
  - `+extendable-arms` «Руки висуваються з тіла на N клітин» · entities/state · 🥉.
  - `+perpendicular-arms` «Руки лише в перпендикулярних напрямках» · entities/legality · 📎 · слот {max: 3}.
  - `+solid-hand-only-arms` «Тверда лише долоня на кінці руки» · entities/legality · 📎.
  - `+magnet-chain-attach` «Зчеплення будь-якою гранню ланцюгом» · entities/interact · 🥈.
  - `+leave-double` «Лишити дубль себе» · entities/spawn · 📎 (?).
  - `+auto-undo-on-fall` «Падіння — автоматичний відкат ходу» · game-logic/lose · 🌱.
  - `+undoable-reset` «Рестарт як хід, що скасовується undo» · game-logic/history · 🌱.
  - `+character-unlock` «Нові персонажі з прогресом» · levels/progression · 🌱.
  - `+open-world-hub` «Відкритий світ із кількома доступними пазлами» · levels/progression · 📎.

## Пропозиції до словників
- `+effect:extend` — висунути руку / частину тіла на клітину; `+effect:retract` — втягнути назад.
- `+feature:undo-restart` — рестарт, який скасовується undo.
- `+axis:actors` — `single`, але персонаж змінюється між пазлами (чотири типи сил).
- `+card:perpendicular-arms`, `+card:solid-hand-only-arms`, `+card:magnet-chain-attach`, `+card:auto-undo-on-fall` — див. «Мапа на каталог».

## Джерела
- ⭐ [Buried Treasure: Altered](https://buried-treasure.org/2021/05/altered/) — золота статуя з перпендикулярними руками на три блоки, «only the hand on the end is solid», магнітний блок «on any of its faces, and in chains», ящики на перемикачах і ворота, відкат падіння, undo скасовує рестарт, кілька пазлів одночасно.
- [Steam: Altered](https://store.steampowered.com/app/973250/Altered/) — 80+ пазлів, дата, розробник і видавець, теги, досягнення з іменами персонажів (через `appdetails`).
- [LifeisXbox: огляд](https://lifeisxbox.eu/review-altered) — 4 персонажі, плитка зі знаком світла, «nothing bad happens when you fall off», підказок нема.
- [itch: реліз-пост Glitchheart](https://itch.io/post/2828258/view-in-topic) — два GIF: золота статуя з двома перпендикулярними руками штовхає червоні ящики на плитки-цілі; зелений персонаж штовхає ящики, наприкінці на полі двоє однакових.
- [GamingOnLinux](https://www.gamingonlinux.com/2021/02/strange-shape-shifting-puzzler-altered-releases-on-march-12/page=1) — «move and morph yourself», 80+ пазлів.

## Непевне
- (?) Відповідність імен і сил: Norn — золота статуя (перший персонаж, «norn… cool to manipulate» у відгуку Steam); «Burdened висуває долоні», «Guard чіпляється до металевих кубів», «Shadow лишає дубль» — лише з пошукового фрагмента опису, сторінки з ним не відкрились; у досягненнях Steam четвертий персонаж — Seeker, не Shadow.
- (?) Як саме ходить статуя з висунутими руками і чи висування руки в стіну зсуває тіло — у джерелах нема.
- (?) Клавіші керування, меню й налаштування — не описані.
- (?) Чи ворота відчинені лише, поки ящик на перемикачі.
