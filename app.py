from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for
import get_mysql_data

app = Flask(__name__)
# TODO: Add something to find the number of elements (quantity at a certain location) (for dashbard)
# TODO: Create dashboard like this
#location  A    B   C
#Product
#Quantity

get_mysql_data.create_connection()


@app.route('/<row_id>', methods=['POST'])
def delete(row_id):
    table = ""
    if 'ProductMovement' in request.form:
        table = 'ProductMovement'
    elif "Product" in request.form:
        table = 'Product'
    elif "Location" in request.form:
        table = 'Location'
    if request.form.get('edit'):
        row_id = request.form.get('edit')
        row = get_mysql_data.get_from_table(table, row_id)
    elif request.form.get('delete'):
        get_mysql_data.delete_row_from(table, row_id)

    return redirect(url_for(table))


# Homepage
@app.route('/', methods=['GET', 'POST'])
def ProductMovement():
    # Inserting data into product movement
    if request.method == 'POST':
        locations = get_mysql_data.get_from_table('Location')
        movement_id = request.form.get('movement_id')
        to_location = request.form.get('to_location')
        from_location = request.form.get('from_location')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        if to_location == '':
            to_location = None
        if from_location == '':
            from_location = None

        for loc_id, location in locations:
            if location.lower() == str(to_location).lower():
                to_location = loc_id
            if location.lower() == str(from_location).lower():
                from_location = loc_id

        print(to_location, from_location)
        print(locations)

        get_mysql_data.insert_into_product_movement(movement_id, from_location,
                                                    to_location, product_id,
                                                    quantity)

    rows = get_mysql_data.get_from_table('ProductMovement')

    locations = get_mysql_data.get_from_table(table="Location", col='*')
    li = list()
    temp = list()

    for row in rows:
        temp = list()
        for item in row:
            temp.append(item)
        li.append(temp)

    rows = li
    for row in rows:
        for item in row:
            for location in locations:
                if location[0] == row[3]:
                    row[3] = location[1]
                if location[0] == row[2]:
                    row[2] = location[1]

    return render_template('index.html',
                           rows=rows,
                           table="ProductMovement",
                           cols=[
                               'ID', 'Timestamp', 'From Location',
                               'To Location', 'Product id', 'Quantity'
                           ])


@app.route('/dashboard')
def Dashboard():
    from_location = get_mysql_data.get_from_table(table='ProductMovement',
                                                  col='from_location')
    to_location = get_mysql_data.get_from_table('ProductMovement',
                                                'to_location')
    quantity = get_mysql_data.get_from_table('ProductMovement', col='quantity')
    product_id = get_mysql_data.get_from_table('ProductMovement',
                                               col='product_id')
    locations = get_mysql_data.get_from_table(table="Location", col='*')
    products = get_mysql_data.get_from_table("Product")
    length = len(quantity)
    table = dict()
    # keeping 100 items of each in every location (warehouse)
    table = defaultdict(lambda: 100, table)

    # creating dict with product_id and all warehouses_id (cross join)
    for i in range(length):
        from_loc = f'{product_id[i][0]}_{from_location[i][0]}'
        to_loc = f'{product_id[i][0]}_{to_location[i][0]}'
        if from_location[i][0] == None:
            table[to_loc] = table[to_loc] + quantity[i][0]
        elif to_location[i][0] == None:
            table[from_loc] = table[from_loc] - quantity[i][0]
        else:
            table[from_loc] = table[from_loc] - quantity[i][0]
            table[to_loc] = table[to_loc] + quantity[i][0]

    return render_template('dashboard.html',
                           locations=get_mysql_data.get_from_table(
                               table="Location", col='*'),
                           products=get_mysql_data.get_from_table("Product"),
                           table=table)


@app.route('/product', methods=['POST', 'GET'])
def Product():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = request.form.get('product')
        get_mysql_data.insert_into_product(product_id, product)
        return render_template('product.html',
                               rows=get_mysql_data.get_from_table("Product"))
    else:
        return render_template('product.html',
                               rows=get_mysql_data.get_from_table("Product"),
                               table="Product",
                               cols=['Product ID', 'Product'])


@app.route('/location', methods=['POST', 'GET'])
def Location():
    if request.method == 'POST':
        location_id = request.form.get('location_id')
        location = request.form.get('location')
        get_mysql_data.insert_into_location(location_id, location)

    return render_template('location.html',
                           rows=get_mysql_data.get_from_table(table="Location",
                                                              col='*'),
                           table="Location",
                           cols=['Location ID', 'Location'])


@app.route('/edit_row', methods=["POST"])
def edit_row():
    table_name = request.form.get('table')
    if table_name == 'ProductMovement':
        row_id = request.form.get('id')
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        if to_location == '':
            to_location = None
        if from_location == '':
            from_location = None

        locations = get_mysql_data.get_from_table('Location', col='location')
        for row in locations:
            if row[1].lower() == str(to_location).lower():
                to_location = row[0]
            if row[1].lower() == str(from_location).lower():
                from_location = row[0]

        get_mysql_data.update_table_product_movement(row_id, from_location,
                                                     to_location, product_id,
                                                     quantity)
    else:
        first_col = table_name.lower() + '_id'
        first_col_value = request.form.get('id')
        second_col = table_name.lower()
        second_col_value = request.form.get(second_col)
        get_mysql_data.update_table(first_col, first_col_value, second_col,
                                    second_col_value, table_name)

    # It probably doesn't do anything
    # Sends True as response to ajax post request
    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
