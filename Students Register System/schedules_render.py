from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)
@app.route ("/schedules.html")
def show_students():
    # Connect to the database
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='school'
    )

    # Create a cursor
    cursor = cnx.cursor()

    # Execute a query
    query = '''select course_schedules.course_id, course_name, level_name, day, duration, start_time
from course_schedules join courses c on c.course_id = course_schedules.course_id
join levels l on l.level_id = c.level_id'''
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # print(json.loads(results))
    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Define the variables to pass to the template
    context = {
        'results': results,
        'title': 'Schedules List',
    }

    # Render the template and pass the variables to it
    return render_template('schedules.html', **context)


app.run(debug=True)













