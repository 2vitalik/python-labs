# python-labs — робоча памʼять проєкту

Вебсистема для організації лабораторних: студенти роблять ігри на клітинному полі, заявляють виконані завдання з каталогу, накопичують монетки; викладач (Vitalik) прозоро оцінює, планує захисти, веде зауваження. Заміна старої системи Coda-таблички + Notion. Стартовий брейндамп — [T01](.rounds/.t/T01-R--braindump-readback.md), структура вузлів — [T02](.t/T02-P--node-structure.md), стратегія MVP — [T25](.t/T25-B--mvp-strategy.md).

Метод — жива спека: `/Users/v4u/Dropbox/v4/Dev/My/dev-md-rules/APPROACH.md` (компактний шар DEV.md — у кожній сесії). Реєстр тікетів — [MAP.md](MAP.md), дерево вузлів — [TREE.md](TREE.md).

## Вузли (карта)

- Контент курсу: [games](games/README.md) · [tasks](tasks/README.md) — що студенти роблять і за що отримують монетки.
- Оцінювання: [grading](grading/README.md) — монетки, шкала, політики.
- Процес: [reports](reports/README.md) · [defense](defense/README.md) · [remarks](remarks/README.md) · [journal](journal/README.md).
- Курсові: [coursework](coursework/README.md).
- Інтеграції: [github](github/README.md) · [tgbot](tgbot/README.md).
- Реалізація: [platform](platform/README.md).

## Стан

- Фаза: **перший код працює** — мікро-MVP «сторінка + Google OAuth лише @nure.ua» ([T44](platform/.t/T44--auth-mvp/report.md)) + **профіль v1** ([T64](platform/.t/T64--profile-v1/report.md)) + **каталог v1** ([T71](platform/.t/T71--catalog-v1/report.md)): `/games` + `/tasks` з деревом зон, пошуком і адмін-формами, сид 17 ігор + 162 завдання з wiki; стек затверджено ([T41](.rounds/.t/T41-R--auth-mvp-decisions.md)): FastAPI + MongoDB (Beanie) + Vue 3 + Bootstrap 5.
- Решта вузлів — думання; чекають Q-відповідей (🔴 у MAP). Пріоритет: [T26](.t/T26-Q--roadmap-open-questions.md) → [T08](grading/.t/T08-Q--grading-open-questions.md) → [T06](tasks/.t/T06-Q--tasks-open-questions.md) → [T22](platform/.t/T22-Q--platform-open-questions.md) → [T16](github/.t/T16-Q--github-open-questions.md), решта — як зайде.

## Наступний крок

- **Пілот «Моя гра»: етапи A і B виконано** (2026-08-15/16, рішення — [T87](.rounds/.t/T87-R--game-round-decisions.md) + [T89](platform/.t/T89-Q--my-game-questions.md)): обʼєктна модель [T83](reports/.t/T83-B--game-objects-model.md) прийнята; каталог 209 карток з типами вікон ([T88](tasks/.t/T88--catalog-objects-seed/report.md)); бекенд `/api/works` зі смоуком 35/35 ([T91](platform/.t/T91--my-game-backend/report.md), дизайн — [T90](platform/.t/T90-P--my-game-v1-design.md)). Далі етап C — фронт; механіки — окрема сесія (T86 Q1c); Vitalik: ревізія чернеток + активація `window`-карток.
- Профіль v1 працює (2026-08-04, [T64](platform/.t/T64--profile-v1/report.md)); CSS — Bootstrap 5 остаточно (чат після [T62](platform/.t/T62-C--css-frameworks.md)); імпорт багатогруповий з оновленням наявних → Vitalik: повторний імпорт `cist.txt` на живій базі.
- **Каталог v1 реалізовано** (2026-08-05, [T71](platform/.t/T71--catalog-v1/report.md)) за рішеннями [T70](.rounds/.t/T70-R--catalog-decisions.md): таксономія-фасети прийнята, сид залито; Vitalik: клік-тест + ревізія чернеток (ціни/статуси).
- Далі за [T25](.t/T25-B--mvp-strategy.md): кабінет студента — вибір завдань і заявки ([T10](reports/.t/T10-Q--reports-open-questions.md)); паралельно — міграція v3 у каталог за командою (T37 Q4).
- База знань **`data/wiki/`** створена і наповнена чернетками (2026-08-03, рішення — [T54](.rounds/.t/T54-R--kb-round-decisions.md)): `games/` — 17 ігор у 4 класах, `tasks/` — 6 зон + вся v3-сировина в staging; далі — правки Vitalik і поступове зведення сировини.
- Паралельно: `>`-відповіді на решту Q-тікетів (насамперед T26) і збір старих Coda/Notion-матеріалів (T26 Q5).
