---
title: "XCOM: Chimera Squad"
slug: xcom-chimera-squad
aka: [Chimera Squad, XCS]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2020
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/XCOM:_Chimera_Squad", best: true, note: "breach mode з точками входу, interleaved turns, 11 агентів без permadeath, неспокій районів"}
  - {kind: steam, url: "https://store.steampowered.com/app/882100/", note: "офіційний опис: Breach Mode, Interleaved Turns, team-up, City 31 і анархія як годинник"}
  - {kind: wiki, url: "https://www.ufopaedia.org/Breaching_(Chimera)", note: "UFOpaedia: точки прориву, слоти, модифікатори, First Impression, Surprised/Alerted/Aggressive"}
  - {kind: wiki, url: "https://www.ufopaedia.org/Tactical_Combat_(Chimera)", note: "UFOpaedia: таймлайн, вміння зсуву черги, 1–3 енкаунтери, bleeding out 4 раунди, андроїди, підкріплення, цивільні"}
  - {kind: wiki, url: "https://www.ufopaedia.org/Anarchy_(Chimera)", note: "UFOpaedia: 9 районів з неспокоєм 0–5, шкала анархії 14 (19) секцій, game over"}
  - {kind: wiki, url: "https://www.ufopaedia.org/Field_Teams_(Chimera)", note: "UFOpaedia: польові команди, спеціалізації, вміння з перезарядкою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=XCOM+Chimera+Squad+breach+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, destructible-blocks, status-effects, unit-xp-skills, inventory-items, reinforcements, spawn-points, telegraphed-intents, legal-move-highlight, reachable-highlight, path-preview, ai-opponent, destroy-all-enemies, time-out, permadeath, difficulty-levels, save-autosave, map-window, placement-screen, character-select, +breach-phase, +interleaved-timeline, +turn-order-manipulation, +cover-system, +flanking, +hit-chance, +bleed-out-revive, +subdue-capture, +civilian-rescue, +district-unrest, +field-teams, +encounter-chain]
proposes: ["+trigger:breach", "+trigger:timeline_turn", "+cond:breach_slot_free", "+effect:delay_turn", "+effect:advance_turn", "+effect:stabilize", "+effect:subdue", "+ui:timeline-bar", "+ui:breach-point-card", "+ui:reinforcement-alert", "+window:breach-planner", "+window:city-map", "+window:hq-screen", "+feature:mission-fail-on-death", "+axis:turn-structure=alternating-unit"]
author: opus
date: 2026-11-09
---

# XCOM: Chimera Squad — тактика з укриттями, де бій починається з вибиття дверей, а ходи всіх юнітів — одна спільна черга

## Суть
Невеликий загін іменних агентів зачищає приміщення серіями коротких **енкаунтерів** (1–3 на місію). Кожен енкаунтер починається з **фази прориву (breach)**: гравець розставляє агентів по точках входу (двері, стіна, вентиляція), задає порядок — і агенти по черзі вриваються та стріляють по заскоченим ворогам. Далі — бій як у XCOM з укриттями, але без «фаз сторін»: **одна черга (timeline)**, де агенти й вороги чергуються поюнітно, а вміння можуть зсувати когось у черзі. Агенти не гинуть назавжди: смерть = провал місії.

## Поле і час
- Поле — квадратна сітка з поверхами й укриттями на ребрах клітин, як у [xcom](xcom.md); приміщення компактні, багато дверей і вікон.
- Енкаунтер = окрема кімната/зона; між ними загін переходить далі, поранені лишаються пораненими.
- Час — покроковий, **interleaved**: таймлайн показує порядок окремих юнітів (агент, ворог, агент…); «хід» = дія одного юніта, «раунд» = прохід усього таймлайну. Початковий порядок задає лише розстановка в breach.
- Випадковість: шанс влучання й криту, модифікатори точок прориву випадкові; мапи фіксовані.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Агент (Godmother, Terminal, Verge, Torque…) | piece | HP, Aim, Defense, Dodge, Mobility, унікальні вміння, ранг | рух + дія як у XCOM; власні breach-дії та вміння |
| Андроїд | piece | слабший | замінює непритомного агента в наступному енкаунтері; втрата не провалює місію |
| Ворог (гібрид, бандит, сектоїд…) | enemy | HP, Aim, стан Surprised/Alerted/Aggressive | AI: ховається, стріляє, тікає до цивільних |
| Елітний ворог / ватажок | boss | більше HP, вміння зсуву черги (Tyranny, Tempo Surge) | ламає порядок таймлайну |
| Точка прориву (двері) | gate | слотів N, модифікатори | звичайний вхід з випадковими бонусами/штрафами |
| Спецточка (стіна, захищені двері, вентиляція) | gate | потребує предмет або агента | без штрафів, кращі бонуси |
| Укриття низьке / високе | terrain | — | зменшує шанс влучання по тому, хто за ним; руйнується |
| Точка підкріплення | spawner | череп-трикутник на мапі | сюди виходять вороги після попередження в таймлайні |
| Цивільний | neutral | — | рятується, коли агент підходить поруч; гине — росте неспокій |
| Предмет утиліти (граната, аптечка) | supply | заряди | не коштує дії |
| Евакуація / зона виходу | zone | — | завершення місії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (енкаунтер) → ТО `window(breach-planner)`; КОЛИ `input(assign, agent, point)` → ЯКЩО `custom: «у точці є вільний слот»` and (`custom: «звичайна точка»` or `has(agent, required_item)`) → ТО `place(agent, point)`.
- КОЛИ `input(breach)` → ТО `custom: «агенти входять у заданому порядку; кожен робить одну breach-дію (зазвичай постріл по цілі)»`; порядок входу = позиції в таймлайні.
- КОЛИ `custom: «агент першим входить через точку з First Impression»` → ТО `custom: «його постріл не промахується»`.
- КОЛИ `input(breach)` → ТО `set_state(enemy, surprised|alerted|aggressive)`; ЯКЩО `state(enemy, surprised)` → ТО `custom: «штраф Defense; після прориву лише біжить в укриття»`; ЯКЩО `state(enemy, aggressive)` → ТО `custom: «стріляє в агента під час прориву»`.
- КОЛИ `input(run_for_cover, agent)` → ТО `set_state(agent, guarded, until_breach_end)` (+Defense, +Dodge).
- КОЛИ `custom: «прорив завершено»` → ТО `move(agent, cover_near_point)`.
- Таймлайн: КОЛИ `turn_end(unit)` → ТО `custom: «ходить наступний юніт таймлайну, хоч свій, хоч ворожий»`.
- КОЛИ `turn_start(agent)` → ТО `custom: «рух + дія (дві дії; атака завершує хід)»` (?); `use(agent, utility)` — без витрати дії.
- КОЛИ `input(team_up, agent)` → ЯКЩО `custom: «раз на місію»` (?) → ТО `custom: «агент переходить на 2-гу позицію таймлайну»`.
- КОЛИ `input(delay_skill, agent, enemy)` (Pin Down, Relocate, Soulfire) → ТО `custom: «ворог зсувається далі в черзі»`.
- КОЛИ `input(shoot, a, t)` → ЯКЩО `line_of_sight(a, t)` → ТО `prob(hit)` → `damage(t, n)` — шанс з укриттям і флангом як у [xcom](xcom.md).
- КОЛИ `input(subdue, a, t)` → ТО `damage(t, small)`; ЯКЩО `hp_zero(t)` → ТО `custom: «ворог затриманий, а не вбитий»` — більший шанс Intel за місію (+20 % за кожного, 100 % за 5).
- КОЛИ `hp_zero(agent)` → ТО `set_state(agent, bleeding_out, 4)` — 4 раунди.
- КОЛИ `input(stabilize, ally, agent)` → ЯКЩО `adjacent(ally, agent)` → ТО `clear_state(agent, bleeding_out)`, `set_state(agent, unconscious)`.
- КОЛИ `counter(bleeding_out, ==, 0)` → ТО `custom: «агент гине»`, `lose` (місія провалена; у Hardcore — уся гра).
- КОЛИ `custom: «агент отримав bleeding out (або HP < половини, з шансом)»` → ТО `custom: «шрам: −стат до тренування або часу»`.
- Підкріплення: КОЛИ `schedule(timeline)` → ТО `custom: «попередження в таймлайні за кілька ходів»`, потім `spawn_at(enemy, reinforcement_point)` зі своїм слотом у черзі.
- КОЛИ `adjacent(agent, civilian)` → ТО `custom: «цивільного врятовано»`; КОЛИ `died(civilian)` → ТО `custom: «+20 % ризику неспокою району»`.
- Перемога енкаунтера: `all_gone(enemy)` (вбиті або затримані) → наступний енкаунтер або `win`. Поразка: смерть агента, загибель цивільних понад межу, таймер мети.
- Місто: КОЛИ `custom: «день минає»` → ЯКЩО `counter(unrest(district), ==, 5)` → ТО `counter(anarchy, +1)`; КОЛИ `counter(anarchy, ==, max)` → ТО `game_over`.

## Керування і ввід
- Breach-планувальник: перетягнути агентів на точки, обрати breach-дії, порядок; переглянути модифікатори кожної точки.
- Під час прориву — сповільнений час: для кожного агента по черзі клік по цілі.
- Далі як у XCOM: клік клітини — рух (синя/жовта зона), панель вмінь унизу, вибір цілі, панель пострілу з відсотком.
- Таймлайн угорі показує порядок і підсвічує, хто ходить; наведення на портрет — юніт на мапі.

## Вікна, меню, HUD
- `main-menu`: Continue, New Game (складність, Ironman/Hardcore, опції), Load, Options.
- `breach-planner`: точки прориву з `breach-point-card` (слоти, вимоги, бонуси/штрафи), агенти, breach-дії.
- `game-screen`: поле; `timeline-bar` угорі; `reachable-highlight` дві зони; `path-preview`; іконки укриття; `hp-bar`; `reinforcement-alert` у таймлайні; `ability-buttons`; `objective-text`.
- Панель пострілу: шанс влучання, крит, модифікатори (як у [xcom](xcom.md)).
- `hq-screen` — штаб: Assembly (дослідження), Supply (магазин, андроїди), Training (ранги, лікування шрамів), Spec Ops (завдання агентів), Field Teams.
- `city-map` — мапа City 31: 9 районів, неспокій 0–5, шкала анархії, ситуації на вибір (`map-window`).
- `squad-select` перед місією (`character-select`); `end-screen` — підсумок; `pause-menu`; `settings-window`.

## Фічі поза полем
- Кампанія з розслідуваннями фракцій; 11 іменних агентів, ранги й нові вміння; агентів не можна втратити назавжди.
- Стратегічний шар: щоденний вибір ситуації, неспокій районів, анархія як годинник поразки; польові команди (Finance / Security / Technology) знижують неспокій і дають ресурси; вміння команд з перезарядкою в днях.
- Ironman / Hardcore (`mode-hardcore`): смерть агента закінчує гру; `difficulty-presets`; `autosave`.
- Опція Extended City Anarchy (шкала 19 замість 14) — `custom-rules`.

## Варіації й родичі
- Батько: [xcom](xcom.md) (2 дії, укриття, фланг, Overwatch, фази сторін); Chimera Squad міняє фази на спільну чергу і додає breach.
- Родичі: [tactical-breach-wizards](tactical-breach-wizards.md) (вхід через двері й вікна), [invisible-inc](invisible-inc.md) (компактні приміщення), [banner-saga](banner-saga.md) (почергові ходи сторін), [final-fantasy-tactics](final-fantasy-tactics.md) (черга за швидкістю, без фаз).
- Осі варіацій:
  - **початок бою**: звичайна розстановка / приховування до виявлення (XCOM 2) / фаза прориву з першими пострілами (Chimera Squad);
  - **черга**: фази сторін / почергово по юнітах (CS, TBS) / за швидкістю (FFT);
  - **смерть**: permadeath (XCOM) / провал місії (CS) / KO до кінця бою (Triangle Strategy).

## Цікавинки для курсу
- Breach-фаза: розподіл агентів по точках з місткістю й вимогами + сповільнений вхід по черзі — 🥉.
- Спільний таймлайн агентів і ворогів з вміннями «зсунь ворога назад / мене вперед» — 🥉 (черга як список, вставки).
- Bleeding out з таймером 4 раунди й стабілізацією сусідом — 🌱.
- Затримання замість убивства (Subdue): шкода, що на 0 HP дає інший результат — 🌱.
- Підкріплення з попередженням у таймлайні за N ходів — 📎.
- Місто: 9 районів з неспокоєм, переповнення → анархія → game over — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` · `destructible-blocks` ↔ укриття й стіни · `status-effects` · `unit-xp-skills` ↔ ранги агентів · `inventory-items` ↔ утиліти · `reinforcements` + `spawn-points` ↔ точки-черепи · `telegraphed-intents` ↔ попередження в таймлайні · `legal-move-highlight` + `reachable-highlight` + `path-preview` · `ai-opponent` · `destroy-all-enemies` · `time-out` ↔ таймер мети · `permadeath` ↔ Hardcore · `difficulty-levels` · `save-autosave` · `map-window` ↔ City 31 · `placement-screen` ↔ breach · `character-select`.
- **Нема** → пропозиції карток:
  - `+breach-phase` «Фаза прориву з точками входу» · game-logic/opponent · 🥉 · слот {points, slots, modifiers}.
  - `+interleaved-timeline` «Спільна черга юнітів обох сторін» · game-logic/opponent · 🥉.
  - `+turn-order-manipulation` «Вміння зсувають юніта в черзі» · entities/combat · 📎.
  - `+cover-system`, `+flanking`, `+hit-chance` (з XCOM).
  - `+bleed-out-revive` «Таймер стікання кровʼю й стабілізація» · entities/combat · 🌱 (родич `+death-countdown` з FFT).
  - `+subdue-capture` «Затримати замість убити» · entities/combat · 🌱.
  - `+civilian-rescue` «Порятунок цивільних дотиком» · entities/combat · 🌱.
  - `+district-unrest` «Неспокій регіонів → загальна анархія» · progression · 📎.
  - `+field-teams` «Пасивні команди в регіонах з вміннями» · progression · 📎.
  - `+encounter-chain` «Місія = ланцюг енкаунтерів зі станом загону» · progression · 📎.

## Пропозиції до словників
- `+trigger:breach` (є як пропозиція з Tactical Breach Wizards) — старт прориву в енкаунтер.
- `+trigger:timeline_turn(a)` — настав хід юніта A у спільній черзі (точніше за `turn_start` для чергування).
- `+cond:breach_slot_free(point)` — у точці прориву є місце.
- `+effect:delay_turn(a, n)` / `+effect:advance_turn(a, pos)` — зсунути юніта назад / на позицію в черзі.
- `+effect:stabilize(a)` — зупинити таймер смерті; `+effect:subdue(a)` — вивести з бою без убивства.
- `+ui:timeline-bar` — спільна черга з портретами; `+ui:breach-point-card` — картка точки входу; `+ui:reinforcement-alert` — значок майбутнього підкріплення в черзі.
- `+window:breach-planner` — розстановка по точках прориву; `+window:city-map` — райони й неспокій; `+window:hq-screen` — штаб між місіями.
- `+feature:mission-fail-on-death` — смерть персонажа = провал місії замість permadeath.
- `+axis:turn-structure=alternating-unit` — спільна черга з чергуванням юнітів.

## Джерела
- ⭐ [Wikipedia: XCOM: Chimera Squad](https://en.wikipedia.org/wiki/XCOM:_Chimera_Squad) — breach mode, interleaved turns, 11 агентів, без permadeath (провал місії), неспокій районів, Ironman.
- [Steam: XCOM: Chimera Squad](https://store.steampowered.com/app/882100/) — Breach Mode, Interleaved Turns, team-up і комбо, City 31 і анархія.
- [UFOpaedia: Breaching](https://www.ufopaedia.org/Breaching_(Chimera)) — точки, слоти, вимоги спецточок, випадкові модифікатори, First Impression, стани ворогів, Run for Cover.
- [UFOpaedia: Tactical Combat](https://www.ufopaedia.org/Tactical_Combat_(Chimera)) — таймлайн, вміння зсуву черги, утиліти без дії, 1–3 енкаунтери, Subdue, bleeding out 4 раунди, андроїди, підкріплення, цивільні, шрами.
- [UFOpaedia: Anarchy](https://www.ufopaedia.org/Anarchy_(Chimera)) — 9 районів, неспокій 0–5, анархія 14/19, game over.
- [UFOpaedia: Field Teams](https://www.ufopaedia.org/Field_Teams_(Chimera)) — спеціалізації, ціни в Intel, вміння з перезарядкою.
- YouTube: пошук «XCOM Chimera Squad breach gameplay».

## Непевне
- (?) Чи хід агента — саме дві дії «рух + дія» як у XCOM 2 (Wikipedia: «move, attack, take cover, abilities»).
- (?) Team Up — «раз на місію» і чи це той самий механізм, що «змусити юніта діяти наступним».
- (?) Межа загиблих цивільних для провалу, точні модифікатори точок прориву.
- (?) Розмір загону (4 агенти) — за загальним описом, у відкритих сторінках цифри не бачив.
