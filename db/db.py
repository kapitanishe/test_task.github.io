import psycopg2, datetime
from loguru import logger
from time_counter import TimeCounter

# TODO: все, что касается констант должно лежать в конфиге
# TODO: пароли и логины это ОЧЕНЬ чувствительные данные они ОБЯЗАТЕЛЬНО должны браться из ".env" файла
db_name = "test_task"
db_user = "postgres"
db_password = "1236"
db_host = "localhost"

# TODO: создание соединения и получения курсору стоит реализовать иначе (как вариант через контекстный менеджер, пример отправил тебе в телеге)
conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host)
cur = conn.cursor()


# TODO: это разбивается и переезжает в соответствующие файлы модуля db, а в этом файле останется логика подключения к дб
# def get_users():
#     try:
#         cur.execute("SELECT user_name AS username FROM users")  # TODO: запросы лучше положить в переменную(можно прям в этой же функции, но можно и вынести, если запрос может использоваться где то еще), а потом эту переменную уже использовать.
#     except Exception as exc:
#         logger.exception("Не удалось получить список пользователей из базы", exc)
#
#     colnames = [desc[0] for desc in cur.description]
#     rowdicts = [dict(zip(colnames, row)) for row in cur.fetchall()]
#     users = {"count": cur.rowcount, "username": rowdicts}
#     return users
#
#
# def get_boards():
#     try:
#         cur.execute("select * from boards")
#     except Exception as exc:
#         logger.exception("Не удалось получить перечень досок из базы", exc)
#     colnames = [desc[0] for desc in cur.description]
#     rowdicts = [dict(zip(colnames, row)) for row in cur.fetchall()]
#     boards = {"count": cur.rowcount, "boards": rowdicts}
#
#     return boards
#
#
# def post_board(new_board_name, new_board_user_id):
#     dt_now = datetime.datetime.now()
#     postgres_insert_query = f"""INSERT INTO boards (board_name, created_at, last_updated_at, status_id, user_id)
#                                 VALUES ('{new_board_name}', '{dt_now}', '{dt_now}', 1, '{new_board_user_id}')"""
#     try:
#         cur.execute(postgres_insert_query)
#     except Exception as exc:
#         logger.exception("Не удалось создать новую доску в базе данных", exc)
#     conn.commit()
#     rows_count = cur.rowcount
#     return rows_count
#
#
# def del_board(del_board_name):
#     postgres_del_query = f"""DELETE FROM boards WHERE board_name = '{del_board_name}'"""
#     try:
#         cur.execute(postgres_del_query)
#     except Exception as exc:
#         logger.exception("Не удалось удалить доску из базы данных", exc)
#     conn.commit()
#     rows_count = cur.rowcount
#     return rows_count
#
#
# def get_cards():
#     try:
#         cur.execute("select * from cards")
#     except Exception as exc:
#         logger.exception("Не удалось получить список карточек из базы", exc)
#     colnames = [desc[0] for desc in cur.description]
#     rowdicts = [dict(zip(colnames, row)) for row in cur.fetchall()]
#     boards = {"count": cur.rowcount, "cards": rowdicts}
#     return boards
#
#
# def post_card(new_card_name, new_card_board_name, new_card_description, new_card_estimation):
#     try:
#         cur.execute(f"SELECT board_id FROM boards WHERE board_name = '{new_card_board_name}';")
#     except Exception as exc:
#         logger.exception("Не удалось извлечь данные о доске из базы данных", exc)
#     board_id = cur.fetchone()[0]
#     dt_now = datetime.datetime.now()
#     postgres_insert_query = f"""INSERT INTO cards
#                                 (assignee, board, created_at, description, estimation, status, title)
#                                 VALUES (1, '{board_id}', '{dt_now}', '{new_card_description}', '{new_card_estimation}', 1, '{new_card_name}');"""
#     try:
#         cur.execute(postgres_insert_query)
#     except Exception as exc:
#         logger.exception("Не удалось создать новую карточку в базе данных", exc)
#     conn.commit()
#     rows_count = cur.rowcount
#     return rows_count
#
#
# def del_card(del_card_title):
#     postgres_del_query = f"""DELETE FROM cards WHERE title = '{del_card_title}'"""
#     try:
#         cur.execute(postgres_del_query)
#     except Exception as exc:
#         logger.exception("Не удалось удалить карточку из базы данных", exc)
#     conn.commit()
#     rows_count = cur.rowcount
#     return rows_count
#
#
# def update_card(card_title, board_name):
#     try:
#         cur.execute(f"SELECT board_id FROM boards WHERE board_name = '{board_name}';")
#     except Exception as exc:
#         logger.exception("Не удалось извлечь данные о доске из базы данных", exc)
#     board_id = cur.fetchone()[0]
#     try:
#         cur.execute(f"SELECT status FROM cards WHERE board = '{board_id}' AND title = '{card_title}'")
#     except Exception as exc:
#         logger.exception("Не удалось извлечь статус карточки из базы данных", exc)
#     status = cur.fetchone()[0]
#     if status == 1 or status == 2:
#         status += 1
#     else:
#         response = "Задача уже выполнена!"
#         return response
#     record_update = f"""UPDATE cards
#                         SET status = '{status}', last_updated_at = '{datetime.datetime.now()}'
#                         WHERE board = '{board_id}' AND title = '{card_title}';"""
#     try:
#         cur.execute(record_update)
#     except Exception as exc:
#         logger.exception("Не удалось изменить карточку в базе данных", exc)
#     conn.commit()
#     try:
#         cur.execute(f"""SELECT title, boards.board_name AS board, status_name AS status
#                         FROM cards
#                         INNER JOIN boards ON cards.board = boards.board_id
#                         INNER JOIN status ON cards.status = status.status_id
#                         WHERE board = '{board_id}' AND title = '{card_title}';""")
#     except Exception as exc:
#         logger.exception("Не удалось получить обновленную карточку из базы данных", exc)
#     colnames = [desc[0] for desc in cur.description]
#     card_updated = [dict(zip(colnames, row)) for row in cur.fetchall()]
#     return card_updated
#
#
# def get_cards_by_column(board_name_in_query, column_name_in_query, assignee_in_query):
#     try:
#         cur.execute(f"""SELECT estimation FROM cards
#                         WHERE assignee = (SELECT user_id FROM users WHERE user_name = '{assignee_in_query}') AND
#                         status = (SELECT status_id FROM status WHERE status_name = '{column_name_in_query}');""")
#     except Exception as exc:
#         logger.exception("Не удалось срок выполнения задачи на карточке из базы данных", exc)
#     list_of_tuples = cur.fetchall()
#     res = TimeCounter(list_of_tuples)
#     try:
#         final_estimation = res.final_estimation()
#     except Exception as exc:
#         logger.exception("Не удалось высчитать длительность работ в карточках", exc)
#     try:
#         cur.execute(f"""SELECT title, boards.board_name AS board, status_name AS status, description,
#                         user_name AS assignee, estimation, cards.created_at AS created_at, user_name AS created_by,
#                         cards.last_updated_at AS last_updated_at, user_name AS last_updated_by
#                         FROM cards
#                         INNER JOIN boards ON cards.board = boards.board_id
#                         INNER JOIN status ON cards.status = status.status_id
#                         INNER JOIN users ON cards.assignee = users.user_id
#                         WHERE boards.board_name = '{board_name_in_query}' AND status_name = '{column_name_in_query}' AND
#                         user_name = '{assignee_in_query}';""")
#     except Exception as exc:
#         logger.exception("Не удалось получить отчет по колонке", exc)
#     rows_count = cur.rowcount
#     colnames = [desc[0] for desc in cur.description]
#     cards_selected = [dict(zip(colnames, row)) for row in cur.fetchall()]
#     response = dict(board=board_name_in_query, column=column_name_in_query, assignee=assignee_in_query,
#                     count=rows_count, estimation=final_estimation, cards=cards_selected)
#     return response
