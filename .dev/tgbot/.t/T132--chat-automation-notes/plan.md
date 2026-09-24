# T132 · Chat Automation, нотатки /note, ефемерні команди, Guest Mode — план

`2026-09-24` · ⚙️ задача

Контекст: відповіді Vitalik на [T131](../T131-Q--message-log-2.md) у чаті — Q1 бот адмін форуму + privacy off; Q2 Chat Automation, зберігати все; Q3 лише вибрані користувачі (усі студенти в контактах); Q5 дві команди — видима студенту й невидима; Q6 Guest Mode про запас, ефемерні `/note` у форумі зараз. Дослідження — [T130](../T130-C--signal-from-private-chat.md).

## План

1. Журнал бізнес-чатів: `log.incoming` на `dp.business_message`, правки й видалення (`edited_business_message`, `deleted_business_messages`) — той самий `messages`.
2. Модель `Note` (`notes`): студент (email або tg id), текст, хто, видима чи ні, звідки.
3. `bot/notes.py`: `/note <текст>` у чаті зі студентом (Chat Automation) — тихо: нотатка + видалити команду з чату + алерт; «📝 …» — видима нотатка; `/note` у форумі (ефемерно) і в чаті з ботом — студент з відповіді або з ніка; підключення Chat Automation — алерт із правами.
4. Вид алерту `note`; реєстрація `/note` як ефемерної команди для адмінів груп при старті бота.
5. Guest Mode: `guest_message` → інтро однією відповіддю + журнал.
6. Смоук `tests/smoke_notes.py`; README бота (як підключити), README вузла, CHANGELOG.
