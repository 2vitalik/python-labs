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

- Фаза: **перший код працює** — мікро-MVP «сторінка + Google OAuth лише @nure.ua» реалізовано в `app/` ([T44](platform/.t/T44--auth-mvp/report.md)); стек затверджено ([T41](.rounds/.t/T41-R--auth-mvp-decisions.md)): FastAPI + MongoDB (Beanie) + Vue 3 + Bootstrap 5.
- Решта вузлів — думання; чекають Q-відповідей (🔴 у MAP). Пріоритет: [T26](.t/T26-Q--roadmap-open-questions.md) → [T08](grading/.t/T08-Q--grading-open-questions.md) → [T06](tasks/.t/T06-Q--tasks-open-questions.md) → [T22](platform/.t/T22-Q--platform-open-questions.md) → [T16](github/.t/T16-Q--github-open-questions.md), решта — як зайде.

## Наступний крок

- Мікро-MVP закрито (реальний вхід підтверджено 2026-07-26) → черга 1 за [T25](.t/T25-B--mvp-strategy.md): каталог завдань; для нього потрібні відповіді на [T37](tasks/.t/T37-Q--taxonomy-questions.md) і [T06](tasks/.t/T06-Q--tasks-open-questions.md).
- Раунд бази знань (2026-08-02): спроєктовано `data/kb/` — чернетковий Markdown-простір контенту (ігри + групи завдань) до каталогу ([T51](.t/T51-P--kb-structure.md)); старт наповнення чекає відповідей на [T52](.t/T52-Q--kb-questions.md) і [T53](games/.t/T53-Q--game-classes-questions.md).
- Паралельно: `>`-відповіді на решту Q-тікетів (насамперед T26) і збір старих Coda/Notion-матеріалів (T26 Q5).
