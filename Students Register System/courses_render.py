from flask import Flask, render_template
import mysql.connector
import  json
app = Flask(__name__)
@app.route ("/courses.html")
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
    query = '''Select course_id, course_name, level_name, max_capacity, rate_per_hour
from courses join levels l on l.level_id = courses.level_id'''
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
        'title': 'Courses List',
    }

    # Render the template and pass the variables to it
    return render_template('courses.html', **context)


app.run(debug=True)













