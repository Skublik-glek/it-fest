Для начала работы:
- Откройте файл vars.py
- Вставте vk acces token в значение переменной VK_TOKEN
- Вставте telegram bot token в значение переменной TG_TOKEN
- Вставте короткое название группы в значение переменной group_name, 
например если ссылка группы выглядит как "https://vk.com/fushkaland", 
вы должны написать в значение переменной строку "fushkaland"
- запустите bot.py

Описание:
Это бот, позволяющий отслеживать новости из группы вк по заданным хэштэгам. 
Для начала пользователь использует команду /subscribe, которая подписывает его,
если пользователь больше не хочет получать новые новости, он испоьзует команду /unsubscribe.
Если пользователю нужно получать новости с определёнными хештэгами, он использует команду /addteg <хэштэг>.
Чтобы ознакомиться с полным списком команд используйте /help, /info - контактные данные организаторов.

Составляющие проекта:
vars.py - файл, содержащий токены для работы с API приложений
vk_hendler.py - подуль отслеживающий новости группы вк
data.json - файл базы данных, содержащий данные о пользователях, по типу подписок и хэштэгов.
bot.py - модуль, отвечающий за работу команд tg бота и запускающий всё работу.
