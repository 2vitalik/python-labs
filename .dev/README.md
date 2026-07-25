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

- Фаза: думання/проєктування; рішень ще нема — все чекає відповідей на Q-тікети (🔴 у MAP).
- Вирішено стартувати «чергу 0.5» перед контентним MVP: мікро-застосунок «сторінка + Google OAuth лише @nure.ua» ([T38](.rounds/.t/T38-R--auth-mvp-readback.md), [T39](platform/.t/T39-B--stack-rethink.md)).
- Пріоритет відповідей: [T40](platform/.t/T40-Q--auth-mvp-questions.md) → [T26](.t/T26-Q--roadmap-open-questions.md) → [T08](grading/.t/T08-Q--grading-open-questions.md) → [T06](tasks/.t/T06-Q--tasks-open-questions.md) → [T22](platform/.t/T22-Q--platform-open-questions.md) → [T16](github/.t/T16-Q--github-open-questions.md), решта — як зайде.

## Наступний крок

- Vitalik відповідає на [T40](platform/.t/T40-Q--auth-mvp-questions.md) (мікро-MVP авторизації) → задача-тека з `plan.md` і перший код.
- Паралельно: `>`-відповіді на решту Q-тікетів (насамперед T26) і збір старих Coda/Notion-матеріалів (T26 Q5).
