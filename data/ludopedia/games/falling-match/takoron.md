---
title: Takoron (Octomania)
slug: takoron
aka: [たころん, のーコネパズル たころん, Noukone Puzzle Takoron, Noumiso Konekone Puzzle Takoron, Octomania, たっち☆たころん, たころぉんらいん]
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2007
platforms: [arcade, Wii, mobile, PC, iOS]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/たころん", best: true, note: "правила: числа-кулі в сітці-рамці, ≥N однакових → зникнення, піна-ланцюг, діамант, їжаки-сміття, режими ひとりで / ふたりで / とことん, відмінності Wii"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Octomania", note: "Wii: курсор 2×2 обертає проти годинникової, ортогонально звʼязані однакові зникають разом, поразка — поле повне 3 с, до 4 гравців"}
  - {kind: other, url: "http://www.worthplaying.com/article/2008/5/18/reviews/51356-wii-review-octomania/", note: "огляд Worthplaying: рамки 3×3 з числом у центрі, обертання в обидва боки, режими Arcade / Original / Non-Stop / Online, 2-на-2"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=takoron+octomania+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, spawn-schedule, progress-acceleration, chain-reaction, garbage-attack, simultaneous-versus, ai-opponent, online-multiplayer, character-select, mode-select, game-screen, end-screen, +rotate-2x2, +numbered-net-quota, +connected-group-pop, +lingering-chain-residue, +spawn-pause-during-chain, +recolor-power, +garbage-adjacent-clear, +overflow-timer]
proposes: ["+cond:count_in(zone, kind, op, n)", "+card:numbered-net-quota", "+card:lingering-chain-residue", "+card:spawn-pause-during-chain"]
author: opus
date: 2026-11-09
---

# Takoron — крути восьминогів курсором 2×2, доки на рамці з числом N не збереться N однакових

## Суть
Падаючий пазл у темі такоякі від Compile Heart (автори-нащадки Puyo Puyo). На поле падають кольорові восьминоги; по полю розкидані **рамки-сітки 3×3 з числом N у центрі**. Гравець курсором 2×2 обертає четвірку восьминогів, «закочуючи» їх на рамку: коли на рамці стоїть ≥ N восьминогів одного кольору, вони зникають разом з одноколірними сусідами, а рамка зникає. Зникнення лишає **піну** свого кольору, яка якийсь час живе й ланцюжить кожного однакового восьминога, що її торкнувся, — ланцюг триває, доки піна не згасла. У versus ланцюги скидають супернику їжаків-сміття.

## Поле і час
- Квадратна сітка; розмір у клітинах — (?). Рамки 3×3 стоять у фіксованих місцях поля, у центрі — куля з числом.
- Real-time: восьминоги прибувають згори з часом; **поки на полі є піна, нові не падають** (JA-вікі).
- З часом зростають числа на рамках і кількість кольорів восьминогів.
- Versus: два (Wii — до чотирьох) поля поруч, кожен на своєму.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Восьминіг (タコ) | tile | колір | падає на поле; переміщується лише обертанням курсора |
| Рамка з числом (金網 + 数字の玉) | zone | 3×3, число N у центрі | ≥ N одноколірних на клітинах рамки → зникнення; використана рамка зникає |
| Піна (アワ) | object | колір, час життя | лишається на місці зникнення; однаковий восьминіг, що торкнувся, — зникає (ланцюг); згасає з часом |
| Діамант (ダイヤ) | pickup | — | зʼявляється за умовою (?); зʼєднаний з піною — перефарбовує всіх восьминогів поля в її колір |
| Морський їжак (ウニ) | object | — | сміття від суперника; рамкою не знімається; зникає від піни / зникнення сусідів |
| Курсор 2×2 | player | позиція | обертає вміст на 90° (Wii — в обидва боки) |
| Персонаж | neutral | колір-підпис, ефект діаманта (Wii) | ころん, アンジェリク, ドラモ, カニざえもん та ін.; на Wii діамант залежить від персонажа |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → ЯКЩО `count(foam, ==, 0)` → ТО `spawn_at(octopus, top)`, `fall(octopus)` (поки є піна — падіння стоїть).
- КОЛИ `input(dir)` → ТО `move(cursor, dir)`.
- КОЛИ `input(rotate)` → ТО `rotate(cursor_2x2, ±90)` — чотири восьминоги під курсором міняються місцями по колу (EN-вікі: кнопка A — проти годинникової; Worthplaying — обидва напрямки).
- КОЛИ `settled` → ЯКЩО `custom: «на клітинах рамки з числом N стоїть ≥ N восьминогів одного кольору»` → ТО `clear(group)`, `custom: «разом з ними зникають усі одноколірні, ортогонально звʼязані з ними»`, `disappear(net)`.
- КОЛИ `after(clear)` → ТО `spawn_at(foam, cleared_cells)`, `set_state(foam, fading, dur)`.
- КОЛИ `contact(octopus, foam)` → ЯКЩО `same(octopus, foam, color)` → ТО `clear(group)`, `counter(chain, +1)`, нова піна; аркада — лише після обертання курсором, Wii — автоматично від дотику.
- КОЛИ `state_off(foam, fading)` → ТО `disappear(foam)`; ланцюг закінчено, падіння відновлюється.
- КОЛИ `custom: «умова появи діаманта»` (?) → ТО `spawn_at(diamond, field)`.
- КОЛИ `contact(diamond, foam)` → ТО `transform(all_octopus, foam_color)` (аркада); Wii — `custom: «ефект залежить від персонажа»`.
- КОЛИ `after(clear)` → ЯКЩО `mode(versus)` і `chain(n)` → ТО `send_garbage(urchin, n)`; Wii: ЯКЩО `same(chain, character, color)` → ТО більше їжаків.
- КОЛИ `settled` → ЯКЩО `occupied(net_cell, urchin)` → ТО `custom: «їжак не рахується в N рамки»`.
- КОЛИ `after(clear)` → ЯКЩО `adjacent_count(urchin, cleared_or_foam, >=, 1)` → ТО `disappear(urchin)`.
- КОЛИ `timer(every)` → ТО `custom: «на нових рамках більші числа, у потоці більше кольорів»` (де беруться нові рамки — (?)).
- КОЛИ `custom: «поле заповнене повністю»` → ТО `lose` (аркада); Wii: ЯКЩО `timer(>=, 3s)` поспіль → ТО `lose`.
- КОЛИ `custom: «поле суперника заповнене»` → ТО `counter(wins, +1)`; КОЛИ `counter(wins, ==, 2)` → ТО `win` (ふたりで — до двох перемог).
- Перемога: суперник переповнився (story, versus) · Поразка: власне поле повне · Рахунок — (?) (джерела не описують).

## Керування і ввід
- Аркада: рух курсора + кнопка обертання (?); вимога «обертати, щоб ланцюг спрацював».
- Wii: пульт як вказівник (IR) або горизонтальний хват — хрестовина рухає курсор 2×2, кнопка обертає; огляди радять хват, бо IR-ціль незручна.
- iPhone «たっち☆たころん» — дотик (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: ひとりで (сюжет проти CPU) · ふたりで (versus) · とことん (нескінченний); Wii (EN): Arcade · Original (кооп і 2-на-2) · Non-Stop · Online.
- `character-select` — персонаж (на Wii він задає колір-підпис і ефект діаманта).
- `game-screen`: поле(я) з рамками, курсор 2×2, лічильник ланцюга (?), смуга їжаків, що прийдуть (?).
- `dialogue-window` — сюжетні сцени ひとりで (?).
- `lobby-window` — онлайн Wii: випадковий суперник або friend code.
- `end-screen` — перемога / поразка; у とことん — титули й рейтинг «タコタコ認定» (`stats-window`?).

## Фічі поза полем
- `mode-endless` (とことん), сюжет проти CPU зі стадіями, `mode-versus` до 2 перемог.
- Wii: `local-multiplayer` до 4 гравців, `mode-coop`, команди 2-на-2, `online-multiplayer` (Nintendo Wi-Fi Connection), `rank-tiers` — титули за виконані умови в とことん.
- Порти: i-appli/BREW, PC-онлайн «たころぉんらいん» (2008–2010), iPhone (2009).

## Варіації й родичі
- Аркада (NAOMI) → Wii (2007 JP, 2008 NA як Octomania): автоланцюг від дотику, ефект діаманта за персонажем, колір-підпис множить сміття, кооп і онлайн.
- Родичі в корпусі: [puyo-puyo](puyo-puyo.md) (ланцюги, сміття, що знімається сусіднім зникненням), [hexic](hexic.md) і [gururin](gururin.md) (обертання групи плиток), [tidalis](tidalis.md), [six-match](six-match.md).
- **Осі варіацій**: умова зникнення (лінія N / звʼязна група N / **квота N однакових на рамці**) · ланцюг (каскад після падіння / **слід-піна, що живе T секунд**) · як рухати плитки (падаюча пара / обмін сусідів / **обертання 2×2**).

## Цікавинки для курсу
- Рамка-квота: порахувати одноколірних на 8 (9?) клітинах рамки й зняти їх разом з flood fill звʼязаних — 📎.
- Обертання вмісту 2×2 курсором — 🌱.
- Піна з таймером життя як «вікно ланцюга» + пауза спавну, поки піна жива, — 🥉 (стан, що впливає на правило спавну).
- Діамант, що перефарбовує все поле в колір піни, — 🌱.
- Їжаки-сміття, які рамка не бачить, а знімає лише сусіднє зникнення, — 📎.
- Поразка «поле повне 3 секунди поспіль» — 🌱.

## Мапа на каталог
- Є: `gravity-fall` ↔ восьминоги падають; `spawn-schedule` ↔ потік з паузою на піну; `progress-acceleration` ↔ більші числа й більше кольорів; `chain-reaction` ↔ ланцюг через піну; `garbage-attack` ↔ їжаки; `simultaneous-versus`; `ai-opponent` ↔ сюжет; `online-multiplayer` (Wii); `character-select`, `mode-select`, `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+numbered-net-quota` «Рамка з числом N: N однакових на її клітинах → зникнення» · entities/interact · 📎 · слоти {size: 3×3, n}.
  - `+lingering-chain-residue` «Слід зникнення живе T і ланцюжить однакових, хто торкнувся» · game-logic/score · 🥉 · слоти {ttl, auto: bool}.
  - `+spawn-pause-during-chain` «Поки триває ланцюг, нові плитки не падають» · entities/spawn · 🌱.
  - Повтор чужих: `+rotate-2x2` (Bejeweled-родина), `+connected-group-pop` (Puyo), `+recolor-power` (діамант), `+garbage-adjacent-clear` (їжаки), `+overflow-timer` (3 с).

## Пропозиції до словників
- `+cond:count_in(zone, kind, op, n)` — кількість сутностей виду в зоні (тут — на клітинах рамки); у реченнях поки `custom`.
- `+card:numbered-net-quota`, `+card:lingering-chain-residue`, `+card:spawn-pause-during-chain` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: たころん](https://ja.wikipedia.org/wiki/たころん) — правила (рамка з числом, ≥N однакових, рамка зникає), піна й ланцюг, пауза падіння, діамант, їжаки, режими, персонажі, відмінності Wii, порти й дати.
- [Wikipedia: Octomania](https://en.wikipedia.org/wiki/Octomania) — курсор 2×2 і обертання, ортогонально звʼязані однакові, їжаки знімаються сусіднім зникненням, поразка після 3 с переповнення, до 4 гравців, онлайн.
- [Worthplaying: Octomania review](http://www.worthplaying.com/article/2008/5/18/reviews/51356-wii-review-octomania/) — рамки 3×3 з числом у центрі, обертання в обидва боки, режими Arcade / Original / Non-Stop / Online, 2-на-2, хват пульта.

## Непевне
- (?) Розмір поля, кількість кольорів, як саме восьминоги «падають» (стосом з гравітацією чи на вільні клітини) і чи осідають після зникнень.
- (?) Чи рахуються 8 клітин навколо кулі, чи всі 9; чи сама куля з числом зникає разом з рамкою і де зʼявляються нові рамки.
- (?) Умова появи діаманта; на Wii ефекти діаманта за персонажами не перелічені.
- (?) Їжаки: JA — знімаються «зʼєднанням з піною», EN — «ортогонально поруч із восьминогами, що зникають»; узгоджено як «поруч із зникненням або піною».
- (?) Рахунок і бонуси; павер-апи, згадані в огляді Worthplaying без назв.
- (?) Рік аркади: JA — 22.02.2007, EN — 2006 (NAOMI).
- Рядок черги каже «восьминогів **її** кольору» — у джерелах куля лише з числом, а однакові мають бути восьминоги між собою.
