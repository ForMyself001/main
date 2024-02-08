import sqlite3
from datetime import datetime, timedelta


def check_and_insert_messages():
    # Подключаемся к базе данных
    print("Подключение к базе данных...")
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    print("Подключение к базе данных выполнено успешно.")

    # Получаем список всех пользователей
    print("Получение списка пользователей...")
    cursor.execute('SELECT DISTINCT user FROM users')
    users = cursor.fetchall()
    print("Список пользователей получен.")

    # Переменная для отслеживания наличия сообщений
    messages_exist = False

    # Цикл по каждому пользователю
    for user in users:
        user = user[0]  # Получаем имя пользователя из кортежа
        print(f"Проверка дат для пользователя: {user}")
        # Цикл по каждому дню недели
        count = 0
        for i in range(7):
            # Вычисляем дату i дней назад от текущей даты
            date = datetime.now() - timedelta(days=i)
            # Форматируем дату в строку YYMMDDHHMMSS
            datestr = date.strftime('%y%m%d')

            # Проверяем, есть ли запись для данного пользователя и данной даты
            cursor.execute('SELECT COUNT(*) FROM users WHERE user=? AND datastr LIKE ?', (user, f'{datestr}%'))
            exist_date = cursor.fetchone()[0]
            if exist_date > 0:
                count += 1

            # Если есть запись, добавляем сообщение в другую таблицу
            if count == 7:
                message = "Есть запись"
                cursor.execute('INSERT INTO messages (user, message) VALUES (?, ?)', (user, message))
                conn.commit()
                # Выводим сообщение о наличии записи
                print(message)
                # Устанавливаем флаг, что сообщения были найдены
                messages_exist = True

    # Если сообщения не были найдены, выводим сообщение об этом
    if not messages_exist:
        print("Сообщения отсутствуют.")

    # Закрываем соединение с базой данных
    conn.close()
    print("Соединение с базой данных закрыто.")


# Вызываем функцию для проверки и добавления сообщений
check_and_insert_messages()
