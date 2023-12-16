import psycopg2, sys
import settings


def create_record(values):
    try:
        connection = psycopg2.connect(
            host=settings.HOST,
            database=settings.DATABASE,
            user=settings.USER,
            password=settings.PASSWORD,
            port=settings.PORT,
        )

        print("Database opened successfully")
        cursor = connection.cursor()
        for (k, v) in enumerate(values):
            insert_query = "INSERT INTO products (name) VALUES (%s)"
            cursor.execute(insert_query, (v,))
        connection.commit()
        cursor.close()
        connection.close()

        print(f"Запись в базу данных успешно произведена!")
    except Exception as e:
        print(f"Ошибка при записи в базу данных: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_record(sys.argv[1:])
    else:
        create_record("t-shirt")
