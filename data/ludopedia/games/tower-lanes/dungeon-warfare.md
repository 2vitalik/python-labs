---
title: Dungeon Warfare
slug: dungeon-warfare
aka: [DW, Dungeon Warfare 2, Dungeon Warfare 3]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2015
platforms: [PC, Mac, Linux, iOS, Android, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/355980", best: true, note: "опис від автора: 26 пасток × 3 рівні, валун, вагонетка, прірва, портали, руни складності, редактор"}
  - {kind: steam, url: "https://store.steampowered.com/app/3419220/Dungeon_Warfare_3/", note: "DW3 (2025): поле будується тайл за тайлом — стіни, прірви, процедурні підземелля"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeon_Warfare_2", note: "сиквел: дати релізів, платформи"}
  - {kind: other, url: "https://gamerblurb.com/articles/dungeon-warfare-3-tips-guide-best-strategies", note: "гайд DW3: штовхання в ями/об стіну, барикади, wrath за ранні хвилі, сховища"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeon+warfare+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, enemy-reached-base, round-currency, hp-damage, projectile-shot, shoot-cooldown, environment-death, status-effects, speed-per-type, impassable-cells, in-round-upgrades, shop-buyback, unit-xp-skills, difficulty-levels, rule-variants, sequential-levels, level-unlock, in-game-editor, level-exchange, achievements-window, +knockback-push, +pit-kill, +maze-by-barricade, +wall-trap, +early-wave-bonus, +difficulty-runes, +trap-mastery]
proposes: ["+effect:knockback", "+effect:fall_into", "+effect:pull_to", "+effect:sell", "+effect:send_wave_early", "+trigger:path_changed", "+cond:on_wall", "+role:trap", "+ui:send-wave-button", "+window:rune-select", "+feature:difficulty-runes", "+feature:trap-mastery", "+card:knockback-push", "+card:pit-kill", "+card:wall-trap", "+card:early-wave-bonus"]
author: opus
date: 2026-11-09
---

# Dungeon Warfare — TD у підземеллі: пастки на підлозі й стінах коридорів, а головна зброя — штовхнути авантюриста в прірву

## Суть
Гравець — володар підземелля: авантюристи хвилями йдуть коридорами від входу до виходу, а він розставляє пастки на клітинах підлоги й стін уздовж шляху. Частина пасток бʼє (дротики, шипи, вогонь), а частина **керує положенням** ворога: штовхає в прірву чи лаву, перекидає на вагонетку, перекриває прохід барикадою, змушуючи йти довшим шляхом. Ядро — комбінації «сповільнити → зібрати в купу → зіштовхнути» замість простого DPS. Досвід за вбивства постійно прокачує пастки між рівнями.

## Поле і час
- Квадратна сітка-мапа рівня з видом згори: коридори (підлога), стіни, прірви/ями, лава та інші особливі клітини; один чи кілька входів і вихід (?).
- Пастки двох типів місця: на клітині підлоги (по ній ідуть вороги) і на клітині стіни, що межує з коридором (бʼють/штовхають у коридор) (?).
- Real-time: хвилі за розкладом; між хвилями й під час них можна будувати; наступну хвилю можна викликати раніше.
- Шлях ворогів — найкоротший прохід коридорами; барикади на підлозі змінюють його (мейзинг у межах коридорів).
- DW3: гравець сам кладе тайли поля — зводить стіни, прорізає прірви, формуючи коридор.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-рука | — | вибрана пастка | ставить, апгрейдить, продає |
| Коридор (підлога) | terrain | — | шлях ворогів; місце підлогових пасток |
| Стіна | static | — | непрохідна; місце настінних пасток; удар об неї оглушує (DW3) |
| Прірва / яма (abyss) | hazard | — | ворог, що потрапив у неї, гине одразу |
| Лава | hazard | — | смертельна/шкодить при попаданні (?) |
| Колія вагонетки | terrain | — | вагонетка перевозить ворогів в інше місце (переспрямування) |
| Вхід | spawner | — | звідси виходять хвилі |
| Вихід (серце підземелля) | static | — | ворог дійшов → втрата життя (?) |
| Дротикова пастка | tower | на стіні (?), радіус, перезаряд | стріляє дротиками вздовж коридору |
| Шипи | hazard | на підлозі | стабільна шкода тим, хто проходить |
| Штовхальна пастка (push) | tower | на стіні (?), сила | відкидає ворогів у напрямку від стіни: у прірву / об стіну |
| Барикада | object | на підлозі, HP (?) | блокує прохід; вороги обходять або ламають (?) |
| Валун | projectile | — | котиться коридором і давить ворогів на шляху |
| Гарпун | tower | — | бʼє здалеку й тягне ворога (?) |
| Смола / сповільнення | hazard | — | сповільнює ворогів (?) |
| Разові (consumable) пастки | tower | обмежені використання | великий сплеск шкоди |
| Портал призову | spawner | — | породжує союзних юнітів, що бʼються з авантюристами |
| Союзний юніт (Wilson, DW3) | ally | — | тримає позицію на вузькому місці |
| Авантюрист | enemy | HP, броня, швидкість, тип (22 типи) | іде шляхом до виходу; деякі мають особливі здібності (лікування, щит, стрибок) (?) |
| Сховище (vault, DW3) | container | скарб | розбивається снарядами пасток (дротики, гарпун) → нагорода |
| Золото | resource | — | за вбивства; витрачається на пастки й апгрейди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `wave_start` (`schedule(waves)`) → ТО `spawn_at(adventurers, entrance)`; вороги `move(a, next_on_path)` до виходу.
- КОЛИ `input(place, trap, cell)` → ЯКЩО `has(gold, cost)` and `free(cell)` and `custom: «тип клітини відповідає пастці: підлога або стіна біля коридору»` → ТО `place(trap)`, `currency(-cost)`.
- КОЛИ `input(upgrade, trap)` → ЯКЩО `has(gold, cost)` → ТО `transform(trap_tier+1)`, `currency(-cost)` (3 рівні на пастку).
- КОЛИ `input(sell, trap)` → ТО `disappear_b`, `currency(+refund)`.
- КОЛИ `in_range(trap, adventurer, r)` → ЯКЩО `custom: «пастка перезарядилась»` → ТО `spawn(projectile)` / `damage(n)`.
- КОЛИ `enter(adventurer, spikes)` → ТО `damage(n)`.
- КОЛИ `in_range(push_trap, adventurer, r)` → ТО `custom: «knockback: відкинути на N клітин від стіни»`.
- КОЛИ `custom: «після відкидання»` → ЯКЩО `cell(x, abyss)` → ТО `custom: «fall_into: ворог падає й гине без огляду на HP»`; ЯКЩО `cell(x, wall)` → ТО `stun(adventurer, n)` (DW3).
- КОЛИ `enter(adventurer, lava)` → ТО `disappear_a` (?).
- КОЛИ `input(trigger, boulder)` / `timer` → ТО `spawn(boulder)`; КОЛИ `contact(boulder, adventurer)` → ТО `damage(n)` (давить усіх на шляху).
- КОЛИ `enter(adventurer, minecart_track)` → ТО `custom: «вагонетка везе ворога колією в інше місце»`.
- КОЛИ `input(place, barricade, cell)` → ЯКЩО `custom: «прохід до виходу лишається»` (?) → ТО `place(barricade)`, `custom: «перерахунок шляху ворогів»`.
- КОЛИ `input(sell, barricade)` → ЯКЩО `custom: «під час хвилі»` → ТО шлях відкривається, вороги повертаються через пастки (DW3); повторно поставити не можна, якщо клітину займає юніт.
- КОЛИ `timer(portal.period)` → ТО `spawn_at(minion, portal)`; союзники бʼються з авантюристами.
- КОЛИ `hp_zero(adventurer)` → ТО `disappear_a`, `currency(+bounty)`, `counter(xp, +n)`.
- КОЛИ `reach(adventurer, exit)` → ТО `lives(-1)` (?), `disappear_a`; КОЛИ `custom: «життя = 0»` → ТО `lose`.
- КОЛИ `input(send_wave_early)` → ТО `custom: «наступна хвиля одразу: більше нагороди; у DW3 — росте wrath, вороги сильніші»`.
- КОЛИ `contact(dart|harpoon, vault)` → ТО `damage(n)`; КОЛИ `hp_zero(vault)` → ТО `give(player, treasure)` (DW3).
- КОЛИ `custom: «остання хвиля знищена»` → ТО `win`, `custom: «зірки/руни за рівень»` (?), `next_level`.
- Перемога: пережити всі хвилі, не втративши всі життя · Поразка: забагато авантюристів дійшли до виходу · Рахунок: золото/досвід; Endless — кількість хвиль.

## Керування і ввід
- Миша (тач на мобільних): вибір пастки з панелі → клік по клітині підлоги/стіни; клік по пастці → апгрейд / продаж.
- Кнопка виклику наступної хвилі раніше; пауза / прискорення (?).
- Ручні активатори окремих пасток (валун) — кліком (?).

## Вікна, меню, HUD
- `main-menu` → `world-map`/`level-select` з рівнями кампанії (40+), зірками/рунами за рівень (?).
- `custom-window` вибору рун складності перед рівнем (`+window:rune-select`): 12 рун, що комбінуються; руна Infinity відкриває Endless.
- `upgrade-window` / `shop-window` дерева постійних апгрейдів пасток за досвід (пасивні апгрейди).
- `game-screen`: мапа підземелля, панель пасток з цінами (`inventory-bar`), `coins` (золото), `lives`, `wave-counter`, `+ui:send-wave-button`, `threat-range` при наведенні на пастку (?), `tooltip`.
- `pause-menu`, `end-screen` (перемога / поразка), `settings-window`, `achievements-window` (30+), `editor-window` (редактор рівнів, Steam Workshop).

## Фічі поза полем
- `levels-sequential` 40+ рукотворних рівнів; `level-unlock`.
- `meta-progression`: досвід за вбивства → постійні апгрейди пасток (`+feature:trap-mastery`; у DW3 майстерність пастки рівня 5 відкриває гілки: більша сила поштовху / шкода / оглушення об стіну).
- `custom-difficulty` через руни (`+feature:difficulty-runes`): 12 модифікаторів, що комбінуються; `mode-endless` після руни Infinity.
- `level-editor` + `level-sharing` (Steam Workshop); `cloud-save`; `achievements`; `localization` (7 мов).
- DW3: процедурні підземелля, тайлове будування поля, сигіли й гнізда (пасивні бафи), прихована колекція сигілів на мапах.

## Варіації й родичі
- Серія: Dungeon Warfare 2 (2018; ПК, Android, iOS) · Dungeon Warfare 3 (2025, Excidium + Valsar) — гравець сам будує поле тайлами.
- Родичі: [dungeon-keeper](dungeon-keeper.md) (підземелля як база), Orcs Must Die! (пастки + штовхання в лаву, 3D), Sanctum, [desktop-tower-defense](desktop-tower-defense.md) і [fieldrunners](fieldrunners.md) (мейзинг барикадами), [emberward](emberward.md), [creeper-world](creeper-world.md).
- **Осі варіацій**: де стоїть пастка — підлога / стіна / обидва · як вбиває — шкода HP / середовище (прірва, лава) / переміщення ворога · шлях — фіксований / барикади-мейзинг / гравець будує поле (DW3) · темп — розклад / виклик хвилі раніше за бонус.

## Цікавинки для курсу
- Відкидання ворога на N клітин з перевіркою клітини призначення (прірва → смерть, стіна → оглушення) — 🥉 (поєднання `push` і `environment-death`).
- Пастки двох «шарів» місця: підлога vs стіна біля коридору — 📎 (легальність розміщення за типом клітини).
- Барикада, що змінює найкоротший шлях, і продаж посеред хвилі, щоб «прокрутити» ворогів удруге — 🥈 (BFS-перерахунок + заборона повністю закрити прохід).
- Валун, що котиться коридором до упору, давлячи всіх — 📎 (`crush-by-slide`).
- Виклик хвилі раніше: ризик ↔ нагорода (wrath у DW3) — 🌱.
- Руни складності, що комбінуються, як модифікатори правил — 📎 (`rule-variants`).
- DW3: гравець кладе тайли коридорів, а вороги шукають шлях по них — 🥈.

## Мапа на каталог
- Є: `tower-placement` ↔ пастки на клітинах · `tower-range` · `enemy-waves` · `enemy-reached-base` · `round-currency` ↔ золото · `hp-damage` · `projectile-shot` + `shoot-cooldown` ↔ дротики · `environment-death` ↔ прірва, лава · `status-effects` ↔ сповільнення, оглушення · `speed-per-type` · `impassable-cells` ↔ стіни, барикади · `in-round-upgrades` ↔ 3 рівні пастки · `shop-buyback` ↔ продаж пастки · `unit-xp-skills` ↔ досвід → апгрейди (наближено: тут XP гравця, не юніта) · `difficulty-levels` + `rule-variants` ↔ руни · `sequential-levels` · `level-unlock` · `in-game-editor` + `level-exchange` ↔ Workshop · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+knockback-push` «Відкидання сутності ефектом» · entities/combat · 🥉 · слот {distance, dir} — не гравець штовхає, а пастка відкидає ворога.
  - `+pit-kill` «Смерть від падіння в прірву/лаву після переміщення» · entities/death · 📎.
  - `+maze-by-barricade` «Перекрити прохід — ворог іде іншим шляхом» · entities/move · 🥈 · слот {must_keep_path}.
  - `+wall-trap` «Розміщення на стіні біля коридору» · entities/legality · 📎.
  - `+early-wave-bonus` «Виклик хвилі раніше за бонус» · game-logic/waves · 🌱.
  - `+difficulty-runes` «Модифікатори складності, що комбінуються» · game-logic/difficulty · 📎.
  - `+trap-mastery` «Постійні апгрейди юнітів за досвід» · game-logic/economy · 🥉.

## Пропозиції до словників
- `+effect:knockback` — відкинути сутність на N клітин від джерела (на відміну від `push`, джерело не рухається слідом).
- `+effect:fall_into` — сутність потрапила в прірву/лаву і гине незалежно від HP.
- `+effect:pull_to` — притягнути ворога до джерела (гарпун) (?).
- `+effect:sell` — прибрати свою споруду з поверненням частини ціни.
- `+effect:send_wave_early` — викликати наступну хвилю раніше розкладу.
- `+trigger:path_changed` — маршрут ворогів перераховано (поставили/прибрали барикаду).
- `+cond:on_wall` — клітина є стіною, що межує з коридором (легальність настінної пастки).
- `+role:trap` — споруда гравця на клітині шляху без власного руху (між `tower` і `hazard`).
- `+ui:send-wave-button` — кнопка «наступна хвиля зараз» із бонусом.
- `+window:rune-select` — вибір модифікаторів складності перед рівнем.
- `+feature:difficulty-runes` · `+feature:trap-mastery`.
- `+card:knockback-push`, `+card:pit-kill`, `+card:wall-trap`, `+card:early-wave-bonus` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Dungeon Warfare](https://store.steampowered.com/app/355980) — 26 пасток із 3 рівнями апгрейду, валун, вагонетка-переспрямування, «кидати воїнів у прірву», портали призову, досвід → постійні апгрейди, 22 типи ворогів, 40+ рівнів, 12 рун складності, Endless (руна Infinity), редактор + Workshop; Valsar, 4.11.2015.
- [Steam: Dungeon Warfare 3](https://store.steampowered.com/app/3419220/Dungeon_Warfare_3/) — поле «тайл за тайлом»: стіни, прірви; процедурні підземелля, Endless, руни; 29.08.2025.
- [Wikipedia: Dungeon Warfare 2](https://en.wikipedia.org/wiki/Dungeon_Warfare_2) — сиквел, дати й платформи.
- [GamerBlurb: DW3 tips](https://gamerblurb.com/articles/dungeon-warfare-3-tips-guide-best-strategies) — штовхання в ями / об стіну (оглушення), барикади й продаж посеред хвилі, wrath, сховища, шипи, валуни, разові пастки, Wilson, сигіли.
- YouTube: пошук «dungeon warfare gameplay».

## Непевне
- (?) Повний список 26 пасток і точні назви (крім дротиків, шипів, штовхальної, барикади, валуна, гарпуна, порталу) — фан-вікі віддає 402, детальних джерел не знайдено.
- (?) Розподіл «підлога / стіна» для конкретних пасток (дротики й поштовх на стіні — з памʼяті).
- (?) Механіка поразки: «життя» за кожного, хто дійшов до виходу, і їх кількість; чи є кілька входів/виходів.
- (?) Лава в DW1 (у промпті черги згадана; в описі Steam — лише прірва).
- (?) Чи можна барикадами повністю закрити прохід, і чи вороги ламають барикади; поведінка гарпуна (тягне?).
- (?) Здібності типів авантюристів (лікарі, щити, стрибки) — з памʼяті.
- (?) Мобільні й Switch-версії першої частини — Switch згадано в огляді Bonus Stage (не відкрився).
