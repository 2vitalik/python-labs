---
title: StarVaders (Star★Vaders)
slug: starvaders
aka: [Star★Vaders, Star Vaders]
family: tactics
also: [roguelike, tower-lanes]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2025
platforms: [PC (Windows / macOS), Switch / PS5 (анонс)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2097570/StarVaders/", best: true, note: "трейлер, опис, безкоштовне демо: 3 мехи, 12 пілотів, 400+ карт і артефактів, Chrono Tokens, щоденні забіги й челенджі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/StarVaders", note: "огляд: загарбники згори вниз як у Space Invaders, Heat / Energy / Mana, перегрів, Junk замість HP, нагорода після бою, Pengonauts"}
  - {kind: other, url: "https://www.siliconera.com/review-starvaders-mixes-deckbuilding-with-mech-tactics/", note: "огляд: телеграфовані атаки, 5 карт на хід, Heat і згоряння карт, Junk у скид, 5 Doom — кінець забігу, мапа місій, 3 скидання ходу"}
  - {kind: other, url: "https://games.gg/starvaders/guides/starvaders-mech-guide/", note: "гайд по мехах: Gunner знизу стріляє вгору, Stinger кидає й підбирає карти, Keeper без тіла, Doom у нижніх 3 рядах"}
  - {kind: other, url: "https://games.gg/starvaders/guides/star-vader-deckbuilding-guide/", note: "гайд: Doom і ліміт ходів, Chrono Tokens — відкат і переролл, згоряють між актами, комбо bounty до ×5, Min's Workshop"}
  - {kind: other, url: "https://www.inverse.com/gaming/starvaders-roguelike-deckbuilder-pc-release-balatro-space-invaders", note: "огляд: спуск на 1 ряд за хід, Junk-карти замість шкоди, Doom наступного ходу, штовхання ворогів один на одного"}
  - {kind: fandom, url: "https://starvaders.wiki.gg/wiki/Card", note: "вікі (wiki.gg): типи й рідкості карт, вартість 0–5, ключові слова, Junk-карти, Chrono Token на переролл, колода 10 карт"}
  - {kind: official, url: "https://star-vaders.com/", note: "офіційний сайт, пресскіт"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=StarVaders+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [telegraphed-intents, telegraph-marker, push-object, hp-damage, projectile-shot, explode-area, chain-reaction, combo-multiplier, enemy-reached-base, status-effects, destructible-blocks, run-relics, shop-between-levels, round-currency, difficulty-levels, character-select, world-map, game-screen, end-screen, mode-select, +deck-builder, +deck-draw, +descending-pattern, +doom-track, +overheat-meter, +junk-cards, +card-burn, +reset-turn, +reroll-token, +energy-resource, +mana-pool-spells, +summon-creature, +possess-unit, +collision-damage, +friendly-fire, +boss-fight, +turn-limit, +card-upgrade, +meta-progression, +card-throw-pickup]
proposes: ["+effect:draw_card", "+effect:add_card", "+effect:exhaust", "+effect:reroll", "+effect:possess", "+cond:heat", "+trigger:overheat", "+feature:reset-turn", "+ui:heat-bar", "+ui:doom-meter", "+window:card-reward", "+window:deck-view", "+window:run-map", "+axis:session", "+card:junk-cards", "+card:card-burn", "+card:card-throw-pickup"]
author: opus
date: 2026-11-19
---

# StarVaders — Space Invaders як покрокова картярка: загарбники сповзають рядами, а мех відповідає колодою

## Суть
Роглайк-декбілдер на сітці: згори вниз щоходу сповзають загарбники, оголошуючи, куди вдарять, а ти керуєш одним мехом через руку карт (рух, атака, тактика). Здоровʼя меха нема: удар ворога лише кладе в колоду **Junk-карту**, яка засмічує руку, а програє забіг **Doom** — 5 очок за весь забіг, і нараховують їх вороги, що дійшли до нижніх трьох рядів. Три мехи — три економіки ходу: Gunner грає за Heat і може перегрітися ціною карти, Stinger — за Energy з наелектризованих ворогів, Keeper без тіла на полі призиває й вселяється. Chrono Tokens дають відкотити хід або перекинути нагороду.

## Поле і час
- Прямокутна квадратна сітка; загарбники виставляються згори, мех — у нижній частині (Gunner ходить нижніми рядами й стріляє вгору); розмір сітки в джерелах не названо (?).
- Нижні 3 ряди — зона Doom; карти посилаються й на «верхній / нижній ряд», «центральний стовпець».
- Хід гравця: на старті береш 5 карт і граєш скільки дозволяє ресурс меха; потім хід ворогів — оголошені атаки бʼють у позначені клітини, загарбники спускаються на 1 ряд. Деякі вороги реагують на кожен рух меха.
- Бій має ліміт ходів: коли він вичерпаний, Doom дають усі живі вороги, де б вони не стояли.
- Інформація часткова: клітини, куди вдарять вороги, видно заздалегідь; колода тасується; наступні хвилі й нагороди — випадкові.
- Забіг — кілька актів (щонайменше 4) з мапою місій, магазином і босом наприкінці акту.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мех Gunner | player | Heat (шкала за хід), відкритий з початку | ходить нижньою частиною поля, стріляє вгору кулями й бомбами |
| Мех Stinger | player | Energy (батарея) | ближній бій; кидає власні карти на клітини й підбирає їх; Energy — з ударів по наелектризованих |
| Мех Keeper | player | Mana, що відновлюється; тіла на полі нема | призиває сутності (Turret, Polyp), вселяється в маріонеток і ворогів, знищує їх заради шкоди |
| Загарбник | enemy | HP, bounty, патерн атаки | спускається на 1 ряд за хід; оголошує атаку; у нижніх 3 рядах дає Doom |
| Реактивний загарбник | enemy | — | рухається щоразу, коли рухається мех |
| Щитовий / наелектризований загарбник | enemy | стан Shielded / Shocked | щит гасить удар; Shocked — джерело Energy для Stinger |
| Павук | enemy | — | плете павутину на сусідніх клітинах |
| Павутина | static | — | блокує шлях; знищується лише картою; сама не відновлюється |
| Tick | enemy | bounty 0 | — |
| Time Angel | enemy | висока bounty | ціль для комбо |
| Бос (Overseer, Hemophage, Nessie, Grandmaster) | boss | фази, HP | Overseer має другу фазу; Hemophage ділиться на Hemocytes |
| Бомба гравця | object | радіус | вибухає, коли її знищено або підірвано картою; шкодить сусіднім клітинам |
| Ворожа бомба (Boomer, Blob-Bomb) | hazard | — | на неї діють ті самі карти підриву |
| Призвана сутність Keeper (Turret, Polyp) | ally | кожна копія на полі +1 Mana до ціни | діє за Keeper; її можна знищити заради шкоди |
| Карта Move / Attack / Tactic | supply | вартість 0–5, рідкість Common / Rare / Legendary, ключові слова | рух / атака / тактика; бувають комбіновані типи |
| Junk-карта (Jam, Corruption, Breach, Mangled, Meltdown…) | supply | без рідкості | приходить від ударів і деяких карт; засмічує руку; переважно живе до кінця бою |
| Артефакт | supply | — | пасивна зміна правил до кінця забігу |
| Chrono Token | resource | запас на акт | відкат ходу або переролл пропозиції карт |
| Нижні 3 ряди | zone | лічильник Doom 0–5 на весь забіг | ворог тут наприкінці ходу ворогів додає Doom; 5 — кінець забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
Бій:
- КОЛИ `level_start` → ТО `spawn_at(invaders, top_rows)`.
- КОЛИ `turn_start(player)` → ТО `custom: «взяти 5 карт з колоди»`; шкала Heat заповнюється протягом ходу.
- КОЛИ `input(play, card)` → ЯКЩО `custom: «вистачає Energy / Mana (Gunner грає без перевірки)»` → ТО `custom: «ефект карти»`, `counter(heat|energy|mana, ±cost)`.
- КОЛИ `input(play, move_card)` → ТО `move(mech, cell)` — у межах клітин, які показує карта.
- КОЛИ `input(play, attack_card)` → ТО `custom: «постріл / удар за патерном карти (прямо вгору, V-подібно, рикошетом)»`, `damage(invader, n)`.
- КОЛИ `input(play, push_card)` → ЯКЩО `free(cell_behind)` → ТО `push(invader)`.
- КОЛИ `input(play, push_card)` → ЯКЩО `occupied(cell_behind, invader)` → ТО `damage(invader, n)` обом — передній ряд вганяють у задній.
- КОЛИ `input(play, bomb_card)` → ТО `place(mech, bomb)`.
- КОЛИ `destroyed(bomb)` → ТО `explode(adjacent, n)`; карти Detonator / Big Bang! підривають бомби, Annihilation — з радіусом +2.

Ресурси мехів:
- Gunner: КОЛИ `counter(heat, >, max)` → ТО `custom: «зіграна карта згоряє до кінця бою»`, `end_turn` — перевищити ліміт можна, але дорого.
- Stinger: КОЛИ `custom: «удар по наелектризованому ворогу»` → ТО `counter(energy, +n)`.
- Stinger: КОЛИ `custom: «Flow-карту взято під час свого ходу»` → ТО `custom: «вона грається безкоштовно»`.
- Stinger: КОЛИ `input(throw, card)` → ТО `throw(card)` на клітину поля.
- Stinger: КОЛИ `contact(mech, card)` → ТО `pickup` (?) — карта повертається (у пілота-пастковика вона ще й пастка).
- Keeper: КОЛИ `turn_start(player)` → ТО `counter(mana, +n)` (?).
- Keeper: КОЛИ `input(play, summon_card)` → ТО `spawn(turret|polyp, cell)`, ціна +1 Mana за кожну копію на полі.
- Keeper: КОЛИ `input(play, possess_card)` → ТО `custom: «вселитися в маріонетку чи ворога»`; знищення одержимого — `damage(targets, n)`.

Хід ворогів:
- КОЛИ `turn_end(player)` → ТО `custom: «кожна оголошена атака бʼє в позначені клітини»`, `move(invader, down)` — на 1 ряд.
- КОЛИ `input(play, move_card)` → ЯКЩО `custom: «ворог реактивний»` → ТО `move(invader, cell)` одразу.
- КОЛИ `contact(enemy_attack, mech)` → ТО `custom: «у колоду (скид) додано Junk-карту»` — HP меха нема.
- КОЛИ `contact(enemy_attack, invader)` → ТО `damage(invader, n)` — вороги ранять одне одного.
- КОЛИ `custom: «павук діє»` → ТО `spawn_at(web, adjacent)`.
- КОЛИ `input(play, move_card)` → ЯКЩО `occupied(cell, web)` → ТО `block` — павутину треба знищити картою.

Doom і кінець бою:
- КОЛИ `turn_end(invaders)` → ЯКЩО `custom: «ворог у нижніх 3 рядах»` → ТО `counter(doom, +n)` за кожного, наступного ходу (зазвичай 1, деякі — більше).
- КОЛИ `counter(turn, ==, limit)` → ТО `custom: «кожен живий ворог додає Doom, незалежно від позиції»`.
- КОЛИ `counter(doom, >=, 5)` → ТО `lose` — кінець забігу (Doom не скидається між боями).
- КОЛИ `died(invader)` → ТО `combo(+1)`, `currency(+bounty × multiplier)` — множник ×1 → ×3 → ×5.
- КОЛИ `all_gone(invader)` → ТО `win` (бій), `choose(card|upgrade|artifact)` (?).
- КОЛИ `level_end` → ТО `custom: «колода повертається до стану перед боєм: Junk і створені карти зникають»`.
- КОЛИ `custom: «Overseer переходить у фазу 2»` → ТО `custom: «енергію скинуто, +3 карти гравцю»`.
- КОЛИ `custom: «фаза Hemophage»` → ТО `split(hemophage)` на Hemocytes (?).

Chrono Tokens і забіг:
- КОЛИ `input(rewind)` → ЯКЩО `counter(chrono, >, 0)` → ТО `undo`, `counter(chrono, -1)` — хід переграється (опція: без перетасування колоди).
- КОЛИ `input(reroll, offer)` → ЯКЩО `counter(chrono, >, 0)` → ТО `custom: «нова пропозиція карт, апгрейдів чи артефактів»`, `counter(chrono, -1)`.
- КОЛИ `custom: «новий акт»` → ТО `custom: «невитрачені Chrono Tokens згоряють»`.
- КОЛИ `input(buy|remove, card)` → ЯКЩО `counter(stars, >=, price)` → ТО `currency(-price)` — Min's Workshop: купити карту, видалити карту перед босом, прокачати мех.
- Перемога: пройти акти й фінального боса · Поразка: 5 Doom за забіг · Рахунок: зірки (bounty) — валюта, а не очки.

## Керування і ввід
- Миша: вибрати карту в руці → клітини, куди вона дістане, підсвічено → клік по клітині; вибір можна скасувати, доки карту не зіграно.
- Таймера нема: вороги ходять, коли ти завершив хід.
- Кнопка відкату за Chrono Token; у налаштуваннях Extras — нескінченні токени й «відкат без перетасування колоди», опція save scumming.

## Вікна, меню, HUD
- `character-select`: мех (Gunner; Stinger і Keeper відкриваються) + пілот.
- `custom-window` «мапа місій» (у пресскіті — знімок Globe (?)): вибір місії за оцінкою загрози й нагородою; звичайні й складні бої.
- `game-screen`: сітка з загарбниками й `telegraph-marker` на клітинах майбутніх атак; мех; рука з 5 карт (`pocket`); шкала ресурсу (Heat / Energy / Mana); лічильник Doom; комбо й bounty (?); стоси колоди й скиду; кнопка Chrono Token; `end-turn-button`; `tooltip` з ключовими словами (екран MoreInfo).
- `upgrade-window`: нагорода після бою — карта, апгрейд (Component) або артефакт; переролл за Chrono Token.
- `shop-window`: Min's Workshop — карти за зірки, видалення карт, прокачка меха.
- `custom-window` DeckView — уся колода.
- `end-screen`: кінець забігу (5 Doom чи перемога), розблокування.
- `mode-select` (кампанія · щоденний забіг · челенджі), `difficulty-select` (висхідні складності, Post-Apocalypse і «+»), `settings-window` (Extras, sandbox-налаштування складності з 1.1).
- Переходи: `main-menu` → `character-select` → мапа → бій (`game-screen`) → нагорода → мапа → … → бос → Workshop → наступний акт → `end-screen`.

## Фічі поза полем
- Пілоти: 4 на мех (12 з версії 2.0); пілот задає стартову колоду з 10 карт, свої карти, механіку й стартовий артефакт.
- `meta-progression`: рівні меха 1–5 відкривають нові карти й артефакти в пулі; пілоти — за виконані челенджі; нові вороги й боси — після забігів.
- `mode-daily` (щоденні забіги), челенджі, `difficulty-presets` за висхідними рівнями, sandbox-налаштування складності (1.1).
- Сюжетна кампанія з кількох частин і таємним фіналом; необовʼязкова «справжня кінцівка» в щоденних забігах і челенджах.
- `achievements`, `cloud-save`, 10 мов інтерфейсу, безкоштовне демо.
- 3 випадкові паки карт на забіг (до відкриття — Tempest, Repeater, Spectral).

## Варіації й родичі
- [Into the Breach](into-the-breach.md) — названий натхненням: телеграфовані атаки, штовхання, вороги ранять одне одного, відкат ходу.
- [Space Invaders](../maze-arcade/space-invaders.md) — стрій, що сповзає до гравця; [Mega Man Battle Network](../tower-lanes/mega-man-battle-network.md) і [One Step From Eden](../tower-lanes/one-step-from-eden.md) — карти-дії на сітці; [Fights in Tight Spaces](fights-in-tight-spaces.md), [Card Hunter](card-hunter.md) — картярки на тактичному полі; Slay the Spire, Balatro — з ними порівнюють огляди.
- Dicevaders — інша гра того ж «StarVaders Universe» (?).
- **Осі варіацій**: здоровʼя «HP / Junk-карти в колоду / спільна шкала Doom» · підхід ворогів «з усіх боків / рядами згори вниз» · ліміт ресурсу «жорсткий / можна перевищити ціною карти» · відкат «нема / раз за бій (ITB) / токени на акт» · економіка меха «Heat / Energy за умову / Mana, що відновлюється».

## Цікавинки для курсу
- Шкода як Junk-карти в колоду замість HP, а програш — спільна шкала Doom забігу — 🥉.
- Heat з перевищенням: понад ліміт грати можна, але карта згоряє до кінця бою й хід закінчується — 📎.
- Спуск рядами + зона Doom у нижніх 3 рядах + ліміт ходів, після якого Doom дають усі, — 🥉.
- Телеграф атак + штовхання ворогів одне в одного + friendly fire — 🥈 (перерахунок намірів після кожної дії).
- Chrono Token — одна валюта на два вжитки (відкат ходу / переролл нагород), згорає між актами — 📎 (знімок стану бою).
- Комбо-множник bounty ×1 → ×3 → ×5 за серію вбивств — 🌱.
- Три мехи — три економіки ходу на одному рушії карт — 🥈.
- Карти як сутності поля: Stinger кидає власні карти на клітини й підбирає — 📎.

## Мапа на каталог
- Є: `telegraphed-intents` + `telegraph-marker` ↔ клітини майбутніх атак · `push-object` ↔ карти штовхання · `hp-damage` ↔ HP ворогів і босів · `projectile-shot` ↔ кулі Gunner · `explode-area` ↔ бомби · `chain-reaction` ↔ ланцюги підривів і перескоків (Plasma Fire!) · `combo-multiplier` ↔ bounty до ×5 · `enemy-reached-base` ↔ Doom у нижніх рядах · `status-effects` ↔ Shield, Shock, Frozen · `destructible-blocks` ↔ павутина · `run-relics` ↔ артефакти · `shop-between-levels` + `round-currency` ↔ Min's Workshop і зірки · `difficulty-levels` · `character-select` · `world-map` ↔ мапа місій · `game-screen` · `end-screen` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+junk-cards` «Шкода додає мертві карти в колоду замість HP» · game-logic/lose · 📎 · слот {persist: battle | run}.
  - `+card-burn` «Карта понад ліміт ресурсу згоряє до кінця бою» · game-logic/economy · 📎 — пара з `+overheat-meter`.
  - `+card-throw-pickup` «Карта лягає на клітину поля й підбирається назад» · entities/interact · 📎.
  - Повтори з корпусу: `+deck-builder`, `+deck-draw`, `+descending-pattern` (стрій сповзає рядами), `+doom-track` (шкала до поразки), `+overheat-meter`, `+reset-turn` (Into the Breach; тут — токенами), `+reroll-token`, `+energy-resource`, `+mana-pool-spells`, `+summon-creature`, `+possess-unit`, `+collision-damage`, `+friendly-fire`, `+boss-fight`, `+turn-limit`, `+card-upgrade`, `+meta-progression`.

## Пропозиції до словників
- `+effect:draw_card` — взяти N карт (5 на старті ходу; фаза 2 боса дає +3).
- `+effect:add_card` — додати карту в колоду чи скид (Junk від удару).
- `+effect:exhaust` — карта згоряє до кінця бою (перегрів Gunner).
- `+effect:reroll` — перекинути пропозицію нагород за Chrono Token.
- `+effect:possess` — вселитися в сутність (Keeper).
- `+cond:heat` — рівень Heat проти максимуму меха.
- `+trigger:overheat` — Heat перевищив максимум.
- `+feature:reset-turn` — відкат ходу за токен (Into the Breach — раз за бій).
- `+ui:heat-bar` — шкала Heat; `+ui:doom-meter` — 5 поділок Doom забігу.
- `+window:card-reward` (вибір нагороди після бою) · `+window:deck-view` · `+window:run-map` (мапа місій акту).
- `+axis:session` — значення `run`: забіг з актів, кінець — 5 Doom.
- `+card:junk-cards` · `+card:card-burn` · `+card:card-throw-pickup`.

## Джерела
- ⭐ [Steam: StarVaders](https://store.steampowered.com/app/2097570/StarVaders/) — трейлер і демо, 3 мехи, 12 пілотів, 400+ карт і артефактів, Chrono Tokens «перемотати час», щоденні забіги, челенджі, висхідні складності, 30.04.2025.
- [Wikipedia: StarVaders](https://en.wikipedia.org/wiki/StarVaders) — Pengonauts (Монреаль), натхнення Into the Breach, загарбники згори вниз, Heat / Energy / Mana, перегрів, Junk замість HP, нагорода після бою, анонс Switch.
- [Siliconera](https://www.siliconera.com/review-starvaders-mixes-deckbuilding-with-mech-tactics/) · [Vice](https://www.vice.com/en/article/starvaders-is-a-deckbuilding-roguelike-that-reminds-me-of-mega-man-battle-network-review/) · [Inverse](https://www.inverse.com/gaming/starvaders-roguelike-deckbuilder-pc-release-balatro-space-invaders) · [Gideon's Gaming](https://gideonsgaming.com/starvaders-review/) · [Playday](https://playday.one/2025/04/29/starvaders-review) — огляди: 5 карт на хід, телеграф, реактивні вороги, павутина, Doom у нижніх 3 рядах і 5 Doom = кінець, Junk, три мехи, відкати ходу.
- [games.gg: мехи](https://games.gg/starvaders/guides/starvaders-mech-guide/) · [games.gg: колода](https://games.gg/starvaders/guides/star-vader-deckbuilding-guide/) — ресурси мехів, ліміт ходів і Doom, Chrono Tokens на два вжитки й згоряння між актами, bounty ×5, Min's Workshop.
- [StarVaders Wiki: Card](https://starvaders.wiki.gg/wiki/Card) · [Gunner](https://starvaders.wiki.gg/wiki/Gunner) — типи й рідкості карт, ключові слова, Junk-карти, колода 10 карт, рівні меха 1–5.
- Steam News (API) — патчі: опція нескінченних Chrono Tokens, фаза 2 Overseer, Hemophage, акт 4, ростер 10 загарбників на акт, 12 пілотів у 2.0.

## Непевне
- (?) Розмір сітки (стовпці × ряди) — у жодному відкритому джерелі не названо.
- (?) Скільки Chrono Tokens дають: два огляди кажуть «3 скидання ходу» (за матч / за забіг); вікі — токени й на переролл; games.gg — згоряють між актами.
- (?) Умова перемоги в бою — знищити всіх загарбників чи протриматись до ліміту ходів — прямо ніде не сказано.
- (?) Скидається комбо-множник між ходами чи лише від пропуску вбивства — не знайдено.
- (?) Чи щоденний забіг має спільний seed для всіх — не перевірено.
- (?) Відновлення Mana Keeper за хід і максимум Heat Gunner — числа не знайдено.
- (?) Dicevaders — та сама студія / «всесвіт» лише зі Steam-бандла; не перевіряв.
- (?) Hyperfreeze «заморожує сусідні карти» (у руці) — згадка з вікі-опису карт, механіку сусідства карт у руці не перевірено.
