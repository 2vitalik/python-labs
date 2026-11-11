# T279 · Опис гри v5 — реалізація — план

`2026-11-10` · ⚙️ задача · рішення й контракт — [T278](../../../games/.t/T278-P--game-desc-v5-design.md) · попереднє — [T275](../T275--game-desc-v4/report.md) · звіт — [report.md](report.md)

Ранкова диктовка Vitalik після перегляду v4 (перед показом студентам). Спершу закомічено v4 пʼятьма комітами (`35846e5`…`1feda3f`) — це точка повернення; усе нижче — поверх, у робочому дереві.

## Хвиля 0 — оркестратор (до агентів)

- [x] Коміти v4 (на прохання Vitalik), без push.
- [x] T278 — рішення §1–§14.
- [x] Цеглинки: `windowJumps.js` (`ruleJumps`, `why`), `PairAdvice.vue` (поради-пари винесені з `WindowCard`), `core/ui/form.js` (`changed`, `reset`).
- [x] §13: плашка «Не збережено» внизу екрана й позначка «Markdown» на описі гри (`MyGameForm.vue`, `MyGamePage.vue`).

## Хвиля 1 — девʼять агентів Opus паралельно, кожен зі своїми файлами

| агент | розділ T278 | файли |
|---|---|---|
| plus | §1 «＋» питає назву | `TaskAdd.vue`, `TaskAddPart.vue` (нов.), `gameAdd.js`, `taskMeta.js` |
| cards | §2, §4, §5, §6 картки сутності й вікна, «Переходи й дії», підписи, форма вікна | `EntityCard`, `WindowCard`, `EntityForm`, `WindowForm`, `MenuItems`, `MenuForm`, `MenuTarget`, `FieldCard`, `EntityRules`, `EntityStats`, `LevelCard`, `PartLabel` (нов.) |
| tiles | §3 плитки властивостей поля | `OptionCards`, `FieldProps`, `FieldForm`, `OptionInfo` (нов.), `options.py` |
| rules | §7 «та», заперечення, сторони | `rules.js`, `Rule*.vue`, `ArgFields`, `Pieces`, `ruleViews.js`, `models/vocab.py` |
| graph | §8 схема вікон | `graphLayout.js`, `graphTree.js`, `GameGraph`, `GraphOutline`, `GraphPanel` |
| shell | §9, §10 порядок секцій і категорій, таблиця «Код» / «Супровід» | `GameEditor`, `sections.js`, `SectionHead`, `ZoneSection`, `SubzoneRows`, `ZoneTable` (нов.), `zones.py`, `_map.md` |
| advice | §11 поради | `catalog.js` (PAIRS), `hints.js`, `Hints.vue`, `PairAdvice.vue`, `advice.js` (нов.) |
| history | §12 історія змін гри | `routes/game_history.py` (нов.), `smoke_game_history.py` (нов.), `GameHistoryPage.vue` (нов.), `api.js`, `router.js`, `main.py` |
| catalog | §13 «Логіка»: картки, що насправді про сутність чи правило | `catalog/logic2.yaml`, `apply2.py`, знімок `data/catalog/` |

## Хвиля 2 — оркестратор

- [x] Зведення: збірка, лінт, 12 смоуків на `python_labs_v5m_smoke`.
- [x] Браузер — на стенді 8031/5031 (`python_labs_stand`, без токена бота: дев шле справжні алерти): `/tasks`, «＋» тип вікна й сутності, редактор (порядок секцій, переходи, поради, плитки поля, правила, схема), пісочниця зі «Скинути», історія з вердиктом, ідея, зміна основи, 390 px, темна тема; дев 5030 — лише погляд.
- [x] «Не збережено» без причини — не відтворилось; плашка називає, що саме не збережено.
- [x] Правки після перевірки: авто-заявки поза історією, шапка гри на телефоні, текст поради з однаковими назвами, знімок каталогу з `[ ]` у назві.
- [x] Звіт, [T280](../../../games/.t/T280-Q--game-desc-v5-choices.md), README вузлів, CHANGELOG, STATUS.
