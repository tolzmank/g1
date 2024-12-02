
from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_tolzmank"
app.config["MYSQL_PASSWORD"] = "1874"
app.config["MYSQL_DB"] = "cs340_tolzmank"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Check connection to the MySQL database
with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        print("Connected to MySQL database successfully!")
        cur.close()
    except Exception as e:
        print(f"Failed to connect to MySQL database: {e}")

# Routes
@app.route('/')
def index():
    return redirect("/users")

# -- CRUD: users --
@app.route('/users', methods=['GET'])
def show_users():
    query = "SELECT * FROM users"
    cur = mysql.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()
    return render_template('table.j2', 
                            data = users,
                            table_name = 'Users',
                            obj_name = 'user',
                            Obj_Name = 'User',
                            id = 'user_id',
                            main_name = 'username',
                            display_names = {
                                'ID': 'user_id',
                                'Username': 'username',
                                'Email': 'email'
                            }
                           )


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        if request.form.get("Add_User"):
            username = request.form['username']
            email = request.form['email']
            query = "INSERT INTO users (username, email) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (username, email))
            mysql.connection.commit()
        return redirect("/users")


@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
def update_user(user_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM users WHERE user_id = %s" % (user_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        user = cur.fetchall()
        return render_template("table_update.j2", 
                                item_data = user,
                                table_name = 'Users',
                                obj_name = 'user',
                                Obj_Name = 'User',
                                obj_names = 'users',
                                ID = 'ID',
                                id = 'user_id',
                                display_names = {
                                    'ID': 'user_id',
                                    'Username': 'username',
                                    'Email': 'email'
                                    }
                               )


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_User"):
            # grab user form inputs
            user_id = request.form["user_id"]
            username = request.form["username"]
            email = request.form["email"]

            # no null inputs
            query = "UPDATE users SET users.username = %s, users.email = %s WHERE users.user_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (username, email, user_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/users")


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if request.method == "GET":
        query = "DELETE FROM users WHERE user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        mysql.connection.commit()

        return redirect("/users")



# -- CRUD: locations --
@app.route('/locations', methods=['GET'])
def show_locations():
    query = "SELECT * FROM locations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    locations = cur.fetchall()
    return render_template('table.j2', 
                            data=locations,
                            table_name = 'Locations',
                            obj_name = 'location',
                            Obj_Name = 'Location',
                            id = 'location_id',
                            main_name = 'location_name',
                            display_names = {
                                'ID': 'location_id',
                                'Location Name': 'location_name', 
                                'Coordinates': 'coordinates'
                            }
                           )


@app.route('/add_location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        if request.form.get("Add_Location"):
            location_name = request.form['location_name']
            coordinates = request.form['coordinates']
            query = "INSERT INTO locations (location_name, coordinates) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location_name, coordinates))
            mysql.connection.commit()
        return redirect("/locations")


@app.route('/update_location/<int:location_id>', methods=['POST', 'GET'])
def update_location(location_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM locations WHERE location_id = %s" % (location_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        location = cur.fetchall()
        return render_template("table_update.j2", 
                                item_data = location,
                                table_name = 'Locations',
                                obj_name = 'location',
                                Obj_Name = 'Location',
                                obj_names = 'locations',
                                id = 'location_id',
                                display_names = {
                                    'ID': 'location_id',
                                    'Location Name': 'location_name',
                                    'Coordinates': 'coordinates'
                                    }
                               )


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_Location"):
            # grab user form inputs
            location_id = request.form["location_id"]
            location_name = request.form["location_name"]
            coordinates = request.form["coordinates"]

            # no null inputs
            query = "UPDATE locations SET locations.location_name = %s, locations.coordinates = %s WHERE locations.location_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (location_name, coordinates, location_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/locations")


@app.route('/delete_location/<int:location_id>', methods=['GET', 'POST'])
def delete_location(location_id):
    if request.method == "GET":
        query = "DELETE FROM locations WHERE location_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (location_id,))
        mysql.connection.commit()
        return redirect("/locations")



# -- CRUD: stations --
@app.route('/stations', methods=['GET'])
def show_stations():
    query = "SELECT * FROM stations"
    cur = mysql.connection.cursor()
    cur.execute(query)
    stations = cur.fetchall()
    return render_template('table.j2', 
                            data = stations,
                            table_name = 'Stations',
                            obj_name = 'station',
                            Obj_Name = 'Station',
                            id = 'station_id',
                            main_name = 'station_name',
                            display_names = {
                                'ID': 'station_id',
                                'Station Code': 'station_code',
                                'Station Name': 'station_name',
                                'Station URL': 'station_url',
                                'Date Refreshed': 'date_refreshed'
                            }
                           )


@app.route('/add_station', methods=['POST'])
def add_station():
    if request.method == 'POST':
        if request.form.get("Add_Station"):
            station_code = request.form['station_code']
            station_name = request.form['station_name']
            station_url = request.form['station_url']
            date_refreshed = request.form['date_refreshed']
            query = "INSERT INTO stations (station_code, station_name, station_url, date_refreshed) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (station_code, station_name, station_url, date_refreshed))
            mysql.connection.commit()
        return redirect("/stations")


@app.route('/update_station/<int:station_id>', methods=['POST', 'GET'])
def update_station(station_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM stations WHERE station_id = %s" % (station_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        station = cur.fetchall()
        return render_template("table_update.j2", 
                            item_data = station,
                            table_name = 'Stations',
                            obj_name = 'station',
                            Obj_Name = 'Station',
                            id = 'station_id',
                            main_name = 'station_name',
                            display_names = {
                                'ID': 'station_id',
                                'Station Code': 'station_code',
                                'Station Name': 'station_name',
                                'Station URL': 'station_url',
                                'Date Refreshed': 'date_refreshed'
                            }
                               )


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_Station"):
            # grab user form inputs
            station_id = request.form["station_id"]
            station_code = request.form["station_code"]
            station_name = request.form["station_name"]
            station_url = request.form["station_url"]
            date_refreshed = request.form["date_refreshed"]

            # no null inputs
            query = "UPDATE stations SET stations.station_code = %s, stations.station_name = %s, stations.station_url = %s, stations.date_refreshed = %s WHERE stations.station_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (station_code, station_name, station_url, date_refreshed, station_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/stations")


@app.route('/delete_station/<int:station_id>', methods=['GET', 'POST'])
def delete_station(station_id):
    if request.method == "GET":
        query = "DELETE FROM stations WHERE station_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (station_id,))
        mysql.connection.commit()
        return redirect("/stations")



# -- CRUD: conditions --
@app.route('/conditions', methods=['GET'])
def show_conditions():
    query = "SELECT * FROM conditions"
    cur = mysql.connection.cursor()
    cur.execute(query)
    conditions = cur.fetchall()
    return render_template('table.j2', 
                            data = conditions,
                            table_name = 'Conditions',
                            obj_name = 'condition',
                            Obj_Name = 'Condition',
                            id = 'condition_id',
                            main_name = 'condition_type',
                            display_names = {
                                'ID': 'condition_id',
                                'Condition Type': 'condition_type',
                                'Measurement Unit': 'measurement_unit',
                            }
                           )


@app.route('/add_condition', methods=['POST'])
def add_condition():
    if request.method == 'POST':
        if request.form.get("Add_Condition"):
            condition_type = request.form['condition_type']
            measurement_unit = request.form['measurement_unit']
            query = "INSERT INTO conditions (condition_type, measurement_unit) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (condition_type, measurement_unit))
            mysql.connection.commit()
        return redirect("/conditions")


@app.route('/update_condition/<int:condition_id>', methods=['POST', 'GET'])
def update_condition(condition_id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM conditions WHERE condition_id = %s" % (condition_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        condition = cur.fetchall()
        return render_template("table_update.j2",                             
                                item_data = condition,
                                table_name = 'Conditions',
                                obj_name = 'condition',
                                Obj_Name = 'Condition',
                                id = 'condition_id',
                                main_name = 'condition_type',
                                display_names = {
                                    'ID': 'condition_id',
                                    'Condition Type': 'condition_type',
                                    'Measurement Unit': 'measurement_unit',
                            })


    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Update_Condition"):
            # grab user form inputs
            condition_id = request.form["condition_id"]
            condition_type = request.form["condition_type"]
            measurement_unit = request.form["measurement_unit"]

            # no null inputs
            query = "UPDATE conditions SET conditions.condition_type = %s, conditions.measurement_unit = %s WHERE conditions.condition_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (condition_type, measurement_unit, condition_id))
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/conditions")


@app.route('/delete_condition/<int:condition_id>', methods=['GET', 'POST'])
def delete_condition(condition_id):
    if request.method == "GET":
        query = "DELETE FROM conditions WHERE condition_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (condition_id,))
        mysql.connection.commit()

        return redirect("/conditions")







# Listener
if __name__ == "__main__":
    app.run(port=3180, debug=True)