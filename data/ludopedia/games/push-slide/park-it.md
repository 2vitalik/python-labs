---
title: Park It!
slug: park-it
aka: []
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2989830/Park_It/", best: true, note: "опис (78 рівнів, «Consider the direction of the vehicle», «side turns», «without running out of gas»), 10 знімків, трейлер, 11 досягнень"}
  - {kind: official, url: "https://mishleto.com/presskit/", note: "пресскіт Mishleto (соло-студія, Стамбул): факти, ті самі механіки, 78 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Park+It+Mishleto+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-by-input, keyboard-controls, impassable-cells, floor-types, party-switch, move-limit, undo-redo, restart-level, sequential-levels, movement-animation, game-settings, language-picker, +vehicle-drive, +relative-turn-controls, +orientation-goal, +fuel-per-move, +side-turn, +camera-view-toggle]
proposes: ["+effect:side_turn", "+ui:fuel-gauge", "+card:side-turn"]
author: opus
date: 2026-11-19
---

# Park It! — заведи авто на паркомісце стрілкою в потрібний бік, поки не скінчилось пальне: вперед, назад і бічні повороти

## Суть
На огородженому майданчику-клітинці стоїть авто з запасом пального; його треба поставити на смугасте паркомісце так, щоб авто дивилось у бік стрілки. Кожен хід — крок уперед, назад чи бічний поворот — палить літр, тож пазл про найкоротшу траєкторію з урахуванням напряму. Далі зʼявляються шини й конуси, плями мастила, сині кола, кротовини та кілька авто, між якими перемикаєшся.

## Поле і час
- Квадратна сітка-майданчик з огорожею, кути й виступи; 3D-рендер, камера під кутом, клавіша Tab змінює ракурс.
- Хід = одна дія авто; без вводу нічого не відбувається.
- Рівні нумеровані «світ-рівень» (1-1 … 6-8 на знімках): поле пшениці, пляж, хмари, осінній ліс, космос; разом 78.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Авто (позашляховик) | player | напрям; пальне (число над авто) | крок уперед / назад, бічний поворот; кожен хід −1 л |
| Інше авто (сіре число над ним) | player | своє пальне | неактивне — перешкода; перемикання клавішею Space (?) |
| Паркомісце | zone | стрілка напряму, мітка «P» | ціль: авто на ньому, дивиться вздовж стрілки |
| Огорожа | static | — | непрохідна межа й внутрішні перегородки |
| Шини (стос), конуси | static | — | перешкоди на клітинах |
| Пляма мастила | terrain | — | у трейлері авто крутить на ній (?) |
| Синє коло | terrain | — | авто на ньому розвертається (?) |
| Кротовина (космос) | terrain | пара (?) | (?) телепорт |
| Світлофор | static | — | стоїть на клітині (рівень 3-8), поведінку не бачив (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(forward)` → ЯКЩО `free(cell_ahead)` → ТО `move(car, facing)`, `counter(fuel, -1)`.
- КОЛИ `input(back)` → ЯКЩО `free(cell_behind)` → ТО `move(car, back)`, `counter(fuel, -1)`.
- КОЛИ `input(turn_left|turn_right)` → ЯКЩО `free(side_cell)` → ТО `custom: «бічний поворот: розворот на 90° із заїздом у сусідню клітину»`, `counter(fuel, -1)` (?).
- КОЛИ `input(dir)` → ЯКЩО `counter(fuel, ==, 0)` → ТО `block` — далі лише undo чи рестарт.
- КОЛИ `blocked(car)` → ТО `block` — огорожа, шини, конуси, інше авто (?).
- КОЛИ `enter(car, oil_spill)` → ТО `custom: «авто крутить»` (?).
- КОЛИ `enter(car, blue_ring)` → ТО `rotate(car, 90)` (?).
- КОЛИ `enter(car, wormhole)` → ТО `teleport(car, pair)` (?).
- КОЛИ `input(switch)` → ТО `custom: «керування переходить на інше авто»`.
- КОЛИ `enter(car, spot)` → ЯКЩО `facing(car, spot_arrow)` → ТО `set_state(car, parked)`.
- КОЛИ `all_on(car, spot)` → ТО `win`, `next_level`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: усі авто на своїх місцях, кожне — у бік стрілки. · Поразка: формально нема; пальне скінчилось чи авто в глухому куті → undo / рестарт. · Рахунок: нема (?), гасло трейлера — «Optimize your moves».

## Керування і ввід
- Клавіатура (Keyboard Only Option) або геймпад (Full controller support): W — уперед, S — назад (табличка в 1-1), бічні повороти — окремі клавіші (табличка з поворотами); Space — інше авто (табличка «SPACE»).
- Колонка кнопок ліворуч із підписами клавіш: Esc — назад, F1 — налаштування, Tab — камера, Z — undo, R — рестарт.

## Вікна, меню, HUD
- `game-screen` — майданчик; угорі праворуч — номер «світ-рівень» зі стрілкою назад і каністра пального «N L» (`+ui:fuel-gauge`); над кожним авто — число пального (жовте в активного, сіре в решти); над паркомісцями — мітки «P»; таблички-підказки клавіш прямо на мапі.
- `settings-window` (F1) — гучність окремо (Custom Volume Controls), мова інтерфейсу (~100 мов).
- `level-select` — (?) кнопка «назад» біля номера рівня, мабуть, веде до вибору.
- Переходи: рівень → (усі запарковані) наступний рівень; Esc — назад у меню (?).

## Фічі поза полем
- `undo`, `restart-level`; `levels-sequential` (78 рівнів у світах).
- `achievements` (11: «First Park!», «Boom!», «Honk!», «Beachy.», «Disaster Cat.»…), `cloud-save`, `gamepad-support`, `volume-sliders`, `localization`.

## Варіації й родичі
- [Rush Hour](rush-hour.md), [Unblock Me / Parking Jam](unblock-me.md) — паркувальна тема, але авто ковзають уздовж своєї осі, без поворотів і пального.
- [Couch Installation Service](couch-installation-service.md) — рух, що завжди повертає предмет; [Billy Bumbum](billy-bumbum.md), [Lost in Cheese](lost-in-cheese.md) — мета з орієнтацією й лічильник ходів.
- Осі варіацій:
  - **як рухається авто**: ковзає вздовж осі (Rush Hour) / крок із кермуванням і бічним поворотом (тут) / виїжджає свайпом до краю (Parking Jam);
  - **мета**: вивести одне авто / звільнити поле / поставити кожне авто в місце з напрямом (тут);
  - **ресурс**: без ліміту / пальне на кожне авто (тут).

## Цікавинки для курсу
- Авто на сітці зі станом (x, y, напрям): уперед / назад / бічний поворот — 📎.
- Мета з орієнтацією: клітина + стрілка — 🌱.
- Пальне як бюджет ходів у кожного авто окремо + перемикання між авто — 🥉.
- Клітини, що змінюють напрям чи місце (сині кола, мастило, кротовини) — 📎 кожна.
- BFS по станах (x, y, напрям, пальне) — мінімум пального на рівень — 🥈.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `impassable-cells` ↔ огорожа, шини, конуси; `floor-types` ↔ мастило, сині кола, кротовини; `party-switch` ↔ кілька авто, Space; `move-limit` ↔ пальне; `undo-redo`, `restart-level`; `sequential-levels`; `movement-animation` ↔ поворот із клубами диму; `game-settings`, `language-picker`.
- **Нема** → пропозиції карток:
  - `+vehicle-drive`, `+relative-turn-controls`, `+orientation-goal`, `+fuel-per-move` (є в корпусі; тут поворот теж коштує літр), `+camera-view-toggle` (є в корпусі).
  - `+side-turn` «Бічний поворот: розворот на 90° із заїздом у сусідню клітину» · entities/move · 📎.

## Пропозиції до словників
- `+effect:side_turn` — поворот авто зі зсувом у сусідню клітину одним ходом (тут — `custom`).
- `+ui:fuel-gauge` — каністра пального активного авто + число над кожним авто.
- `+card:side-turn` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Park It!](https://store.steampowered.com/app/2989830/Park_It/) — опис механік, 11 досягнень, мови, контролер; 10 знімків (HUD, світи, перешкоди, кілька авто) і трейлер («PARK IT the right way», «Optimize your moves», «With different mechanics») — кадри з нього дивився.
- [Пресскіт Mishleto](https://mishleto.com/presskit/) — дата 28.07.2025, Windows, 78 рівнів, ті самі три механіки.

## Непевне
- (?) Геометрія бічного повороту — за кадрами трейлера: авто розвертається на 90° і опиняється в сусідній клітині; які клавіші — не бачив.
- (?) Що роблять мастило, сині кола, кротовини й світлофор — бачив лише на знімках і в трейлері.
- (?) Чи врізання в перешкоду — це «Boom!» і провал, чи просто заборонений хід.
- (?) Чи всі авто мають паркуватися і чи пальне в кожного своє (на знімках числа різні, каністра — одна).
- (?) Розподіл 78 рівнів за світами (видно 1-1 … 6-8 і 2-12) і чи є екран вибору рівня.
