import mysql.connector
from mysql.connector import errorcode
from config import dbconfig


def find_country(cursor, country):
    find_country_query = ("SELECT id FROM country_ratings "
         "WHERE country_name = %s")
    cursor.execute(find_country_query, (country,))
    
    return cursor.fetchone()

def get_country(country):
    try:
        cnx = mysql.connector.connect(**dbconfig)
        cursor = cnx.cursor()
        select_query = ("SELECT * FROM country_ratings "
            "WHERE country_name = %s")
        
        cursor.execute(select_query, (country,))
        result = cursor.fetchone()
        
        cursor.close()
        cnx.close()

        return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            payload = {'message': "Something is wrong with your user name or password", 'status_code': 401}
            raise Exception(payload)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            payload = {'message': "Database does not exist", 'status_code': 400}
            raise Exception(payload)
        else:
            raise Exception(str(err))

def insert_country_rate(country, vote):
    try:
        cnx = mysql.connector.connect(**dbconfig)
        cursor = cnx.cursor()

        result = find_country(cursor, country)

        if result is not None:
            if vote == 'like':
                update_rate = ("UPDATE country_ratings "
                    "SET likes = likes + 1 "
                    "WHERE id = %s"
                )

            elif vote == 'dislike':
                update_rate = ("UPDATE country_ratings "
                    "SET dislikes = dislikes + 1 "
                    "WHERE id = %s"
                )
                
            cursor.execute(update_rate, (result[0],))
            cnx.commit()
        else:
            if vote == 'like':
                insert_country = ("INSERT INTO country_ratings "
                    "(country_name, likes) "
                    "VALUES (%s, %s)"
                )

            elif vote == 'dislike':
                insert_country = ("INSERT INTO country_ratings "
                    "(country_name, dislikes) "
                    "VALUES (%s, %s)")
                
            else:
                insert_country = ("INSERT INTO country_ratings "
                    "(country_name) "
                    "VALUES (%s)"
                )
                
            cursor.execute(insert_country, (country,))
            cnx.commit()
        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise Exception("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise Exception("Database does not exist")
        else:
            raise Exception(err)
    
    cnx.close()