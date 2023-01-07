from flask import Flask, render_template
import mysql.connector
import  json
app = Flask(__name__)
@app.route ("/students.html")
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
    query = '''SELECT student_id, student_name, mobile_number, email, level_name, address_name, BOD
             FROM students join contacts c 
                 on c.contact_id = students.contact_id join levels l 
                     on l.level_id = students.level_id join addresses a 
                         on a.address_id = students.address_id '''
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Define the variables to pass to the template
    context = {
        'results': results,
        'title': 'Student List',
    }

    # Render the template and pass the variables to it
    return render_template('students.html', **context)


app.run(debug=True)













