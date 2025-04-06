def Test_Start(cursor, tableM, tableS, domain):
    """This Method fetches the current date time and sets the Domain for the exam also
    and calls the EnterMain() and EnterSub() Methods.
    """
    query = "select now();"
    cursor.execute(query)
    date = cursor.fetchone()[0]
    print(date)
    main_id = EnterMain(cursor, date, domain, tableM)
    sub_id = EnterSub(cursor, date, tableS)
    return main_id, sub_id

def check_table_exists(cursor, table_name):
    """Function to check if a table exists in the database"""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None


def enterHistory(cursor, tableH, test_name, selected_domain, tableM, main_id):
    if not check_table_exists(cursor, tableH):
        create_table_query = """
    CREATE TABLE """+tableH+""" (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date timestamp,
        test varchar(1024),
        domain varchar(1024),
        main_id int,
        sub_id int,
        score double,
        val_counts varchar(2048),
        v2top varchar(2048),
        v3top varchar(2048),
        v4dates varchar(2048),
        v4scores varchar(2048)
    )
    """
        cursor.execute(create_table_query)
        print("Table 'History' created successfully.")
    query = "select date from "+tableM+" where id = "+str(main_id)+";"
    cursor.execute(query)
    date = cursor.fetchone()[0]
    print(date)
    query = "insert into "+tableH + \
        " values(NULL,%s,%s,%s,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);"
    cursor.execute(query, [date, test_name, selected_domain])
    cursor.execute("commit;")


    query = "SELECT id FROM "+tableH+" ORDER BY id DESC LIMIT 1;"
    cursor.execute(query)
    history_id = cursor.fetchone()[0]
    return history_id


def EnterMain(cursor, date, domain, tableM):
    """ This Method is used to enter data(all null values except date-time and domain)
    into main table(TableM) and then returns the id of that row as main_id
    """

    if not check_table_exists(cursor, tableM):
        create_table_query = """
    CREATE TABLE """+tableM+""" (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date timestamp,
        total int,
        correct int,
        incorrect int,
        domain varchar(50),
        score_per double,
        incorrect_per double
    )
    """
        cursor.execute(create_table_query)
        print("Table 'sample' created successfully.")

    query = "insert into "+tableM + \
        " values(NULL,%s,NULL,NULL,NULL,%s,NULL,NULL);"
    cursor.execute(query, [date, domain])
    cursor.execute("commit;")
    query = "select id from "+tableM+" where date='"+str(date)+"';"
    cursor.execute(query)
    main_id = cursor.fetchone()[0]
    print("id of table is", main_id)
    print("inserting date into the main table is successful")
    return main_id


def EnterSub(cursor, date, tableS):
    """ This Method is used to enter data(all null values except date-time)
    into subtopic table(TableS) and then returns the id of that row as sub_id.
    Here each column is one subtopic in this table.
    """
    if not check_table_exists(cursor, tableS):
       
        create_table_query = """
        CREATE TABLE """+tableS+""" (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date TIMESTAMP
        )
        """
        insert_data_query = """
        INSERT INTO """+tableS+""" (date)
        VALUES ("1999-01-01 00:00:00")
        """
        cursor.execute(create_table_query)
        cursor.execute("commit;")
        cursor.execute(insert_data_query)
        cursor.execute("commit;")
        cursor.execute(insert_data_query)
        cursor.execute("commit;")
        print("Table 'sample' created successfully.")


    query = "SELECT count(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+tableS+"';"
    cursor.execute(query)
    cols = cursor.fetchone()[0]-2
    nulls = ",NULL"*cols
    query = "insert into "+tableS+" values(NULL,'"+str(date)+"'"+nulls+");"
    cursor.execute(query)
    cursor.execute("commit;")

    query = "select id from "+tableS+" where date='"+str(date)+"';"
    cursor.execute(query)
    sub_id = cursor.fetchone()[0]

    print("id of table is", sub_id)
    print("inserting date into the subtopic table is successful")
    return sub_id
