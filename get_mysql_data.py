import mysql.connector
from mysql.connector import Error

#TODO: For all execpt blocks it should redirect to new page (error.html) and create a modal and show error in it


def create_connection():
    global connection
    connection = mysql.connector.connect(host='localhost',
                                         database='inventory_management',
                                         user='dhananjay',
                                         password='123')


def insert_into_product_movement(movement_id, from_location, to_location,
                                 product_id, quantity):
    try:
        cursor = connection.cursor()
        if from_location is None:
            insert_statement = f'insert into ProductMovement(movement_id, to_location, product_id, quantity) values(%s, %s, %s, %s)'
            vals = (movement_id, to_location, product_id, quantity)

        elif to_location is None:
            insert_statement = f'insert into ProductMovement(movement_id, from_location, product_id, quantity) values(%s, %s, %s, %s)'
            vals = (movement_id, from_location, product_id, quantity)
        else:
            insert_statement = f'insert into ProductMovement(movement_id, from_location, to_location, product_id, quantity) values(%s, %s, %s, %s, %s)'
            vals = (movement_id, from_location, to_location, product_id,
                    quantity)

        cursor.execute(insert_statement, vals)
        connection.commit()
    except Error as e:
        print(f'Error: {e}')


def insert_into_product(product_id, product):
    try:
        cursor = connection.cursor()

        insert_statement = f'insert into Product values(%s, %s)'
        vals = (product_id, product)

        cursor.execute(insert_statement, vals)
        connection.commit()
    except Error as e:
        print(f'Error {e}')


def insert_into_location(location_id, location):

    try:
        cursor = connection.cursor()

        insert_statement = f'insert into Location values(%s, %s)'
        vals = (location_id, location)

        cursor.execute(insert_statement, vals)
        connection.commit()

    except Error as e:
        print(f'Error {e}')


def get_from_table(table, col='*'):
    try:
        cursor = connection.cursor()
        cursor.execute(f'select {col} from {table}')
        return cursor.fetchall()
    except Error as e:
        print(f'Error: {e}')


def delete_row_from(table, row_id):
    try:
        cursor = connection.cursor()
        if table == 'ProductMovement':
            column_name = 'movement_id'
        else:

            column_name = table.lower() + '_id'
        delete_statement = f'delete from {table} where {column_name}= {row_id}'

        cursor.execute(delete_statement)
        connection.commit()
    except Error as e:
        print(f'Error {e}')


def update_table_product_movement(row_id, from_location, to_location,
                                  product_id, quantity):
    try:
        cursor = connection.cursor()
        vals = (row_id, from_location, to_location, product_id, quantity,
                row_id)
        update_statement = f"update ProductMovement set movement_id = %s, from_location = %s, to_location = %s, product_id = %s, quantity = %s where movement_id = %s"
        cursor.execute(update_statement, vals)
        connection.commit()
    except Error as e:
        print(f'Error: {e}')


# Used to update table Location and Product
def update_table(first_col, first_col_value, second_col, second_col_value,
                 table_name):
    try:
        cursor = connection.cursor()
        update_statement = f'update {table_name} set {first_col}= %s, {second_col} = %s where {first_col} = {first_col_value}'
        vals = (first_col_value, second_col_value)
        cursor.execute(update_statement, vals)
        connection.commit()
    except Error as e:
        print(f'Error : {e}')

    pass
