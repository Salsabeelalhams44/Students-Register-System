import datetime
import mariadb


def register_new_student():
    student_name = input('Enter your name: ')
    date_of_birthday = input('Enter your date of birthday in format year-month-day:  ').format('yyyy-mm-dd')
    level = input('choose your level One, Two, Three, Four, Five, Six: ')
    mobile_number = input('Enter your mobile number: ')
    email = input('Enter your email: ')
    address = input('Enter your address: ')

    conn = mariadb.connect(
        user="root",
        password="123456789",
        host="localhost",
        db="school"
    )
    cursor = conn.cursor()
    if conn:
        print('sucessfull')
        query1= f""" Insert into contacts(mobile_number, email)values('{mobile_number}','{email}')"""
        cursor.execute(query1)
        # query2= f""" select level_id from levels where level_name='{level}'"""
        # cursor.execute(query2)
        # for find_level in cursor:
        #     print('find level =', find_level , 'in index:', find_level[0])
        query3= f""" Insert into addresses(address_name) values('{address}')"""
        cursor.execute(query3)
        contact_id = f""" select contact_id from contacts"""
        cursor.execute(contact_id)
        for cont_id in cursor:
            print(cont_id[0])
        level_id = f""" select level_id from levels  where level_name='{level}'"""
        cursor.execute(level_id)
        for lvl_id in cursor:
            print(lvl_id[0])
        address_id = f"""select address_id from addresses where address_name = '{address}'"""
        cursor.execute(address_id)
        for add_id in cursor:
            print(add_id[0])
        query4 = f""" Insert into students(student_name,contact_id, address_id, level_id,BOD)
         values('{student_name}',
        '{cont_id[0]}','{add_id[0]}','{lvl_id[0]}','{date_of_birthday}')"""
        cursor.execute(query4)
        conn.commit()
        print('You registered successfully !!')
    else:
        print('wrong!!')


def enroll_course():

    student_id = int(input('Enter your id: '))
    course_id = int(input('Enter course id that need to enroll: '))
    course_hour = int(input('Enter the number of hour for the course: '))

    conn = mariadb.connect(
        user="root",
        password="123456789",
        host="localhost",
        db="school"
    )
    cursor = conn.cursor()
    if conn:
        print('sucessfull')
        level_id = f""" select level_id from students where student_id ='{student_id}' """
        cursor.execute(level_id)
        for lvl_id in cursor:
            print(lvl_id[0])
        course_level =  f""" select level_id from courses where course_id ='{course_id}' """
        cursor.execute(course_level)
        for cou_id in cursor:
            print(cou_id[0])
        student_id_check= f""" select student_id from enrollment_histories where course_id ='{course_id}'"""
        cursor.execute(student_id_check)
        for student_id_check in cursor:
            print(student_id_check)
        capacity_check = f""" select max_capacity from courses"""
        if lvl_id[0] == cou_id[0] and student_id_check != student_id and capacity_check != 0 :
            query4 = f""" Insert into enrollment_histories(student_id,course_id, enroll_date,total)
                     values('{student_id}',
                    '{course_id}','{datetime.datetime.now()}','{course_hour}')"""
            cursor.execute(query4)
            # decrement course capacity after any successful enrollment operation
            decrement_max_capacity = f""" update courses max_capacity set max_capacity= max_capacity-1
             where course_id= '{course_id}'"""
            cursor.execute(decrement_max_capacity)
            conn.commit()
            print('Course enrolled successfully')
        else:
            print('This course not allow for you to enroll it')
    else:
        print('wrong!!')


def create_new_course():
    course_code = input('Enter the course code that need add it:  ')
    course_name = input('Enter course name: ')
    max_capacity = input('Enter the max capacity for course: ')
    price = float(input('Enter the price for the course: '))
    level = input('Enter the level that allow student to take this course'
                  '(One, first, second, three, four, five, six): ')
    conn = mariadb.connect(
        user="root",
        password="123456789",
        host="localhost",
        db="school"
    )
    cursor = conn.cursor()
    if conn:
        print('sucessfull')
        course_level = f""" select level_id from levels where level_name = '{level}'"""
        cursor.execute(course_level)
        c_lv=" "
        for c_lv in cursor:
            print(c_lv[0])
        query = f""" Insert into courses(course_id,level_id, course_name,max_capacity, rate_per_hour)
        values('{course_code}','{c_lv[0] }' ,'{course_name}','{max_capacity}','{price}')"""
        cursor.execute(query)
        conn.commit()
        print('create course done successfully')
    else:
        print('wrong!!')


def create_new_schedule():
    conn = mariadb.connect(
        user="root",
        password="123456789",
        host="localhost",
        db="school"
    )
    cursor = conn.cursor()
    if conn:
        print('sucessfull')
        course_id = int(input('Enter course id that need to create schedule for it: '))
        day = int(input('''Choose the number of day for course from the menu:  
                        1- Saturday
                        2- Sunday
                        3- Monday
                        4- Tuesday
                        5- Wednesday
                         '''))
        duration = int(input('Enter the duration for this course: '))
        start_time = input('Enter the start time for the course: ').format('HH:MM')
        y = f""" select * from course_schedules"""
        cursor.execute(y)
        for cc in cursor:
            print(len(cc))
        if len(cc)==0:
            query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                    values('{course_id}','{day}', '{duration}', '{start_time}')"""
            cursor.execute(query1)
            print('create schedule done successfully')
            conn.commit()
        else:
            check_exist_course = f""" select course_id from course_schedules where course_id='{course_id}' """
            cursor.execute(check_exist_course)
            tt = ""
            for tt in cursor:
                print( tt)
            if len(tt)==0:
                check_level = f""" select level_id from courses where course_id='{course_id}'"""
                cursor.execute(check_level)
                for levvl in cursor:
                    print('check level= ', levvl[0])
                if levvl[0] == 1:
                    get_course_id = f"""create view v_schedule1 as
                            select course_schedules.course_id, day, duration, start_time from course_schedules
                                                        join courses on courses.level_id = 1"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule1 where day = '{day}'
                                                        and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    ress=""
                    for ress in cursor:
                        print('res = ', ress)
                    if len(ress) == 0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day =  ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                 values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule1"""
                        cursor.execute(del_view)
                        conn.commit()
                    else:
                        print('Another course exist at the same time')
                elif levvl[0] == 2:
                    get_course_id = f"""create view v_schedule2 as
                                            select course_schedules.course_id, day, duration, start_time from course_schedules
                                                                        join courses on courses.level_id = 2"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule2 where day = '{day}'
                                                                        and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    res2=""
                    for res2 in cursor:
                        print('res = ', res2)
                    if len(res2) == 0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day = ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                                 values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule2"""
                        cursor.execute(del_view)
                        conn.commit()
                    else:
                        print('Another course exist at the same time')
                elif levvl[0] == 3:
                    get_course_id = f"""create view v_schedule3 as
    select course_schedules.course_id, day, duration, start_time from course_schedules
     join courses on courses.level_id = 3"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule3 where day = '{day}'
                                                                                        and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    res3=""
                    for res3 in cursor:
                        print('res = ', res3)
                    if len(res3) ==0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day = ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                                                 values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule3"""
                        cursor.execute(del_view)
                        conn.commit()
                    else:
                        print('Another course exist at the same time')
                elif levvl[0] == 4:
                    get_course_id = f"""create view v_schedule4 as
                    select course_schedules.course_id, day, duration, start_time
                     from course_schedules join courses on courses.level_id = 4"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule4 where day = '{day}'
                                                                                                and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    res4=""
                    for res4 in cursor:
                        print('res = ', res4)
                    if len(res4) == 0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day = ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                                                         values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule4"""
                        cursor.execute(del_view)
                        conn.commit()

                    else:
                        print('Another course exist at the same time')
                elif levvl [0]== 5:
                    get_course_id = f"""create view v_schedule5 as select course_schedules.course_id, day, duration, start_time
                     from course_schedules join courses on courses.level_id = 5"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule5 where day = '{day}'
                                                                                                and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    res5=""
                    for res5 in cursor:
                        print('res = ', res5)
                    if len(res5) == 0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day = ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                                                         values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule5"""
                        cursor.execute(del_view)
                        conn.commit()
                    else:
                        print('Another course exist at the same time')
                elif levvl [0]== 6:
                    get_course_id = f"""create view v_schedule6 as select course_schedules.course_id, day, duration, start_time from course_schedules join courses on courses.level_id = 6"""
                    cursor.execute(get_course_id)
                    get_day = f""" select day, duration, start_time from v_schedule6 where day = '{day}'
                                                                                        and  start_time= '{start_time}' """
                    cursor.execute(get_day)
                    res6=""
                    for res6 in cursor:
                        print('res = ', res6)
                    if len(res6) == 0:
                        if day == 1:
                            day = 'Saturday'
                        elif day == 2:
                            day = 'Sunday'
                        elif day == 3:
                            day = 'Monday'
                        elif day == 4:
                            day = ' Tuesday'
                        elif day == 5:
                            day = ' Wednesday'
                        query1 = f"""insert into course_schedules(course_id, day, duration, start_time)
                                                                                 values('{course_id}','{day}', '{duration}', '{start_time}')"""
                        cursor.execute(query1)
                        print('create schedule done successfully')
                        conn.commit()
                        del_view = f"""drop view v_schedule6"""
                        cursor.execute(del_view)
                        conn.commit()
            else:
                print('Another course exist at the same time')

    else:
        print('wrong!!')

def  display_student_courses_schedule():
    student_id = int(input('Enter your id: '))
    conn = mariadb.connect(
        user="root",
        password="123456789",
        host="localhost",
        db="school"
    )
    cursor = conn.cursor()
    if conn:
        print('successful')
        query = f""" select   enrollment_histories.course_id, course_name, day, duration, start_time 
                from enrollment_histories join courses 
                on enrollment_histories.course_id=courses.course_id 
                join course_schedules
                 on  courses.course_id = course_schedules.course_id
                where student_id='{student_id}'"""
        cursor.execute(query)
        for fd in cursor:
            print('course id: ', fd[0])
            print('course name: ', fd[1])
            print('Day: ', fd[2])
            print('Duration: ', fd[3])
            print('Start time: ', fd[4])
            print('--------------------------')
        conn.commit()
    else:
        print('wrong!!')


while True:
    menu = int(input(""" Select the number of process that need to do from the menu
                     1- Register New Student
                     2- Enroll Course
                     3- Create New Course
                     4- Create New Schedule
                     5- Display Student Courses Schedule
                     6- exit
                     """))

    if menu == 1:
        register_new_student()

    elif menu == 2:
        enroll_course()

    elif menu == 3:
        create_new_course()

    elif menu == 4:
        create_new_schedule()

    elif menu == 5:
        display_student_courses_schedule()
    elif menu==6:
        exit()


    else:
        print('Invalid input, enter the correct number')


