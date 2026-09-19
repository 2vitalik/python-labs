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

- **Дальня мета — лудопедія** (мрія Vitalik, 2026-08-17): єдина мова опису ігрового розмаїття без синтаксису; north star і мапа — [T98](games/.t/T98-B--ludopedia.md). Система лабораторних — перший мешканець цієї мови. **Будівництво йде, Д0–Д2 / E1–E4 закрито** (2026-08-18…19, [T100](.rounds/.t/T100-R--ludopedia-kickoff.md) → [T101](platform/.t/T101--ludopedia-core/report.md) + [T103](platform/.t/T103--ludopedia-slots/report.md)): сутності + правила-речення «КОЛИ→ТО» + інбокс знахідок `/refs` + слоти параметрів у заявках живі в пілоті; питання — [T102](games/.t/T102-Q--ludopedia-build-questions.md), пояснення Д3–Д6 — [T104](games/.t/T104-C--ludopedia-d3-d6.md).

- Фаза: **перший код працює** — мікро-MVP «сторінка + Google OAuth лише @nure.ua» ([T44](platform/.t/T44--auth-mvp/report.md)) + **профіль v1** ([T64](platform/.t/T64--profile-v1/report.md)) + **каталог v1** ([T71](platform/.t/T71--catalog-v1/report.md)): `/games` + `/tasks` з деревом зон, пошуком і адмін-формами, сид 17 ігор + 162 завдання з wiki; стек затверджено ([T41](.rounds/.t/T41-R--auth-mvp-decisions.md)): FastAPI + MongoDB (Beanie) + Vue 3 + Bootstrap 5.
- **Telegram-бот — пустишка в коді** (2026-09-19, [T106](tgbot/.t/T106--tgbot-stub/report.md)): `app/api/bot/` на aiogram, `/start` + привʼязка за [T58](tgbot/.t/T58-C--tg-link-binding.md); живий запуск чекає `TG_BOT_TOKEN`; функції — після [T20](tgbot/.t/T20-Q--tgbot-open-questions.md).
- Решта вузлів — думання; чекають Q-відповідей (🔴 у MAP). Пріоритет: [T26](.t/T26-Q--roadmap-open-questions.md) → [T08](grading/.t/T08-Q--grading-open-questions.md) → [T06](tasks/.t/T06-Q--tasks-open-questions.md) → [T22](platform/.t/T22-Q--platform-open-questions.md) → [T16](github/.t/T16-Q--github-open-questions.md), решта — як зайде.

## Наступний крок

- **Пілот «Моя гра»: етапи A–D закрито** (2026-08-15…17, рішення — [T87](.rounds/.t/T87-R--game-round-decisions.md) + [T89](platform/.t/T89-Q--my-game-questions.md) + [T92](platform/.t/T92-Q--naming-urls.md), всі «a»): обʼєктна модель [T83](reports/.t/T83-B--game-objects-model.md) прийнята; каталог 209 карток з типами вікон ([T88](tasks/.t/T88--catalog-objects-seed/report.md)); моделі `Game`/`Part`/`Claim`, бекенд `/api/my/game…`, фронт `/my/game` + `/students` + `/students/<nick>` і **граф переходів** ([T91](platform/.t/T91--my-game-backend/report.md) + [T93](platform/.t/T93--my-game-front/report.md) + [T94](platform/.t/T94--passport-graph/report.md), дизайн — [T90](platform/.t/T90-P--my-game-v1-design.md)). Vitalik: великий клік-тест + активація `window`-карток. **Сесія механік відбулась** (2026-08-17): розбір драбини на Танчиках [T95](games/.t/T95-B--mechanics-deep-dive.md) + модель сутностей/слотів/таблиці [T96](platform/.t/T96-P--entities-slots-model.md).
- **Лудопедія: код E1–E4 закрито** (2026-08-18…19, [T100](.rounds/.t/T100-R--ludopedia-kickoff.md) → [T101](platform/.t/T101--ludopedia-core/report.md) + [T103](platform/.t/T103--ludopedia-slots/report.md)): сутності з ролями, правила-речення `Rule`, інбокс знахідок `/refs`, слоти параметрів `Task.slots`+`Claim.params` (сид на 20 картках через YAML); смоук 70/70. Vitalik: клік-тест + [T102](games/.t/T102-Q--ludopedia-build-questions.md) + реакція на [T104](games/.t/T104-C--ludopedia-d3-d6.md) (Д3–Д6 людською мовою); [T97](games/.t/T97-Q--mechanics-session-questions.md)/[T99](games/.t/T99-Q--ludopedia-questions.md) — за бажанням формально. Далі: Д3 приклади на картках (після «ок») · раунд grading · заявки-гаманець ([T10](reports/.t/T10-Q--reports-open-questions.md)).
- **Перші рішення оцінювання** (2026-08-16, [T08](grading/.t/T08-Q--grading-open-questions.md) Q1–Q2): бали лише ростуть; захистів — мінімум (лише охочі на 80+), деталі — [grading](grading/README.md).
- Профіль v1 працює (2026-08-04, [T64](platform/.t/T64--profile-v1/report.md)); CSS — Bootstrap 5 остаточно (чат після [T62](platform/.t/T62-C--css-frameworks.md)); імпорт багатогруповий з оновленням наявних → Vitalik: повторний імпорт `cist.txt` на живій базі.
- **Каталог v1 реалізовано** (2026-08-05, [T71](platform/.t/T71--catalog-v1/report.md)) за рішеннями [T70](.rounds/.t/T70-R--catalog-decisions.md): таксономія-фасети прийнята, сид залито; Vitalik: клік-тест + ревізія чернеток (ціни/статуси).
- Далі за [T25](.t/T25-B--mvp-strategy.md): кабінет студента — вибір завдань і заявки ([T10](reports/.t/T10-Q--reports-open-questions.md)); паралельно — міграція v3 у каталог за командою (T37 Q4).
- База знань **`data/wiki/`** створена і наповнена чернетками (2026-08-03, рішення — [T54](.rounds/.t/T54-R--kb-round-decisions.md)): `games/` — 17 ігор у 4 класах, `tasks/` — 6 зон + вся v3-сировина в staging; далі — правки Vitalik і поступове зведення сировини.
- Паралельно: `>`-відповіді на решту Q-тікетів (насамперед T26) і збір старих Coda/Notion-матеріалів (T26 Q5).
