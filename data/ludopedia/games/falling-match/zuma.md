---
title: Zuma / Puzz Loop
slug: zuma
aka: [Zuma Deluxe, Puzz Loop, Ballistic, Luxor, marble shooter]
family: falling-match
also: []
klass: avatar
axes:
  field: 1d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2003
platforms: [PC, Mac, Xbox 360, PS2, PS3, PSP, mobile, arcade]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Zuma_(video_game)", best: true, note: "правила Zuma: жаба-стрілець, ланцюг на треку, 3+, бонуси, Zuma-бар, череп, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzz_Loop", note: "Puzz Loop 1998 (Mitchell): відкат ланцюга до збігу, ланцюгові реакції, versus у Puzz Loop 2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=zuma+deluxe+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [projectile-shot, chain-reaction, combo-multiplier, event-points, time-bonus, extra-life-threshold, collect-quota, enemy-reached-base, temporary-modes, explode-area, sequential-levels, level-select, mode-select, score-records, +curve-track-chain, +insert-into-chain, +gap-retraction, +gap-shot, +swap-ammo, +powerup-balls]
proposes: ["+effect:insert", "+effect:retract", "+trigger:gap_closed", "+ui:ammo-pair"]
author: opus
date: 2026-11-09
---

# Zuma / Puzz Loop — ланцюг кольорових куль котиться треком до черепа; вставляєш кулю пострілом, 3+ вибухають, розриви стягуються в комбо

## Суть
Кольорові кулі ланцюгом котяться звивистим треком до «ями» (череп у Zuma). Нерухомий у центрі стрілець (кам'яна жаба) крутиться за курсором і вистрілює кулю — вона **вставляється** в ланцюг у місці влучання. Якщо поруч склалось 3+ одного кольору — вибух; у розриві кінці можуть стягнутися назад і, якщо кольори на стику збігаються, вибухнути знову (ланцюгова реакція). Рівень закінчується, коли заповнено шкалу (нові кулі більше не йдуть) і все, що лишилось, знищено.

## Поле і час
- Ігрова логіка — **одновимірна**: ланцюг = послідовність куль уздовж кривої (трек), позиція — відстань по треку. Прицілювання й політ кулі — у вільних 2D-координатах.
- Real-time: ланцюг повзе з постійною швидкістю, ближче до кінця пришвидшується (?); тунелі ховають частину треку, на деяких рівнях два треки.
- Рівень «Space» (Zuma) — трек невидимий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жаба-стрілець | player | кут, 2 кулі (поточна + запасна) | крутиться за курсором; клік — постріл; можна поміняти кулі місцями |
| Куля в ланцюгу | tile | колір (4–6 за етапом) | їде треком; 3+ сусідніх одного кольору вибухають |
| Летюча куля | projectile | колір | летить прямо; влучила в ланцюг → вставляється між кулями |
| Сегмент ланцюга | object | позиція на треку | задній штовхає передній; після розриву — розділені сегменти |
| Куля-бонус | pickup | тип | вибухнула в групі → ефект: Backwards / Slow-down / Accuracy / Explosion |
| Монета | pickup | — | зʼявляється біля треку; влучити кулею → очки й шкала |
| Череп (яма) | static | кінець треку | куля дійшла → втрачено життя |
| Zuma-бар | mark | заповнення | росте з очками; повний → нові кулі не спавняться |
| Генератор ланцюга | spawner | — | на початку треку додає кулі, доки бар не повний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «бар не повний»` → ТО `spawn_at(ball, track_start)`; задній сегмент `push` передні вздовж треку.
- КОЛИ `input(aim)` → ТО `face(frog, cursor)`; КОЛИ `input(swap)` → ТО `swap(current, reserve)`.
- КОЛИ `input(fire)` → ТО `throw(ball, dir)`; `custom: «нова запасна — колір з наявних на треку»` (?).
- КОЛИ `contact(ball, chain)` → ТО `custom: «insert — куля вставляється в ланцюг у точці влучання, сусіди розсуваються»`.
- КОЛИ `pattern(line(3+, same_color))` → ТО `clear(group)`, `score(n)`, `counter(zuma_bar, +n)`.
- КОЛИ `after(clear)` → ЯКЩО `same(end_left, end_right, color)` → ТО `custom: «retract — передній сегмент відкочується назад до заднього»`, `combo(+1)` і нова перевірка збігу на стику.
- КОЛИ `after(clear)` → ЯКЩО `not same(end_left, end_right, color)` → ТО `custom: «передній сегмент стоїть, задній доганяє й зʼєднується»` (?).
- КОЛИ `custom: «gap_closed»` → ЯКЩО `pattern(line(3+, same_color))` → ТО `clear(group)`, `combo(+1)` — каскад.
- Бонуси очок: `custom: «combo — один постріл дав кілька вибухів»` · `custom: «chain — поспіль постріли, кожен з вибухом»` · `custom: «gap shot — куля пролетіла крізь розрив ланцюга»` · `score(n)` за Ace Time — рівень пройдено швидше за норму (25 с – 4 хв залежно від рівня).
- КОЛИ `contact(ball, coin)` → ТО `pickup`, `score(n)`, `counter(zuma_bar, +n)`.
- КОЛИ `after(clear)` → ЯКЩО `custom: «у групі куля Backwards»` → ТО `custom: «ланцюг коротко їде назад»`; Slow-down → `speed(chain, ×k)` на час; Accuracy → `speed(shot, ×k)` + `custom: «прицільна стрілка»`; Explosion → `explode(radius_small)`.
- КОЛИ `reach(ball, skull)` → ТО `lives(-1)`, `restart` рівня; ЯКЩО `custom: «життів нема»` → `lose`.
- КОЛИ `counter(score, >=, 50000·k)` → ТО `lives(+1)` (Adventure).
- КОЛИ `all_gone(ball)` → ЯКЩО `custom: «бар повний»` → ТО `win`, `next_level`.
- Puzz Loop: бонус-предмети на кулях сповільнюють ланцюг або прибирають усі кулі одного кольору; кулі за ціллю → кінець гри.

## Керування і ввід
- Мишка: курсор — напрям жаби; ЛКМ — постріл; ПКМ — поміняти поточну й запасну кулю.
- Аркада Puzz Loop: поворот гармати кнопками/крутилкою (?), кнопка пострілу.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Adventure · Gauntlet · Options · Help · (рекорди).
- `map-window` — храми з етапами (Adventure), відкриття наступного храму.
- `level-select` — Gauntlet Practice: будь-який уже досягнутий рівень.
- `game-screen`: трек з ланцюгом, жаба з двома кулями (`next-tile-preview` на спині жаби), `custom: «ammo-pair»`, `progress-bar` (Zuma-бар), `lives`, `score`, `popup-text` (Combo/Chain/Gap bonus), монети.
- `end-screen` рівня (Ace Time, бонуси) · `end-screen` Game Over → `leaderboard`.
- `help-window`, `settings-window` (звук, повний екран).

## Фічі поза полем
- `levels-sequential` + `level-unlock`: храми → етапи по 5–7 рівнів; кольори 4 → 5 (етапи 4–6) → 6 (з етапу 7); прихований 4-й храм (етапи 10–12), рівень «Space».
- `mode-endless` (Gauntlet Survival: кольори й швидкість ростуть), ранги Rabbit → Eagle → Jaguar → Sun God.
- `mode-practice` (Gauntlet Practice), `leaderboard-local`.
- Puzz Loop 2: `mode-versus` на двох.

## Варіації й родичі
- Puzz Loop (1998, Mitchell; Ballistic) — оригінал: спіраль до центру, відкат до збігу. Puzz Loop 2 (2001) — versus. Magnetica (DS, 2006).
- Клони: Luxor, Tumblebugs, Bonsai Blast, Zuma's Revenge (2009).
- Родичі в корпусі: Puzzle Bobble (постріл кулькою з рикошетом), Magical Drop, Klax (смуга, що їде на гравця).
- **Осі варіацій**: геометрія треку (спіраль / крива / кілька треків / тунелі) · стрілець (центр-поворот / рух уздовж краю) · поведінка розриву (магніт за кольором / завжди стягується / стоїть) · мета (бар-квота / вижити) · бонус-кулі (сповільнення, назад, вибух, колір).

## Цікавинки для курсу
- Ланцюг як список з позиціями вздовж параметричної кривої — 🥉.
- Вставка кулі в список у точці влучання з розсуванням — 📎.
- Розрив і стягування сегментів з перевіркою стику (магніт за кольором) — 🥈 (кілька сегментів, швидкості, каскад).
- Перетин променя з кулями на кривій (куди влучить постріл) — 📎.
- Бонуси Backwards/Slow/Accuracy/Explosion як тимчасові режими — 🌱.
- Квота-бар, після якої спавн зупиняється — 🌱.

## Мапа на каталог
- Є: `projectile-shot` · `chain-reaction` · `combo-multiplier` · `event-points` · `time-bonus` (Ace Time) · `extra-life-threshold` (50 000) · `collect-quota` (Zuma-бар) · `enemy-reached-base` (куля в черепі) · `temporary-modes` (Slow, Backwards) · `explode-area` (Explosion) · `sequential-levels` · `level-select` · `mode-select` · `score-records`.
- **Нема** → пропозиції карток:
  - `+curve-track-chain` «Ланцюг куль їде кривою» · entities/move · 🥉 · слоти {speed, track}.
  - `+insert-into-chain` «Постріл вставляє елемент у послідовність» · entities/interact · 📎.
  - `+gap-retraction` «Розрив стягується, якщо кінці одного кольору» · entities/interact · 🥈.
  - `+gap-shot` «Бонус за постріл крізь розрив» · game-logic/score · 🌱.
  - `+swap-ammo` «Поміняти поточний і запасний снаряд» · interface/input · 🌱.
  - `+powerup-balls` «Бонус спрацьовує, коли його куля у вибуху» · entities/interact · 📎.

## Пропозиції до словників
- `+effect:insert` — вставити сутність у послідовність/ланцюг між сусідами (зсуваючи решту).
- `+effect:retract` — сегмент ланцюга відкочується назад до іншого (магніт за кольором).
- `+trigger:gap_closed` — два сегменти ланцюга знову зʼєднались (точка перевірки каскаду).
- `+ui:ammo-pair` — поточний і запасний снаряд на стрільці з перемиканням.

## Джерела
- ⭐ [Wikipedia: Zuma](https://en.wikipedia.org/wiki/Zuma_(video_game)) — механіка, бонуси очок і бонус-кулі, Adventure (3 життя, +1 за 50 000, кольори етапів), Gauntlet і ранги, суперечка з Mitchell.
- [Wikipedia: Puzz Loop](https://en.wikipedia.org/wiki/Puzz_Loop) — оригінал 1998: відкат до збігу, ланцюгові реакції, бонус-предмети, Puzz Loop 2 versus, клони.

## Непевне
- (?) Поведінка розриву, коли кольори не збігаються (передній стоїть, задній доганяє) — з памʼяті; Wikipedia Zuma цього не описує.
- (?) Колір наступної кулі лише з наявних кольорів — з памʼяті.
- (?) Пришвидшення ланцюга ближче до черепа і точні формули очок — не перевірено.
- (?) Керування в аркадному Puzz Loop — не перевірено.
- (?) zuma.fandom.com віддає 402 — у лінки не клав.
