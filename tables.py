def check_table_exists(cursor, table_name):
    """Function to check if a table exists in the database"""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def createTableH(cursor, tableH):
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
        v4scores varchar(2048),
        test_table varchar(1024),
        data varchar(2048)
    )
    """
        cursor.execute(create_table_query)
        print("Table 'History' created successfully.")
    return


def createTableM(cursor, tableM):
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
        print("Table main created successfully.")
    return


def createTableS(cursor, tableS):
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
        print("Table sub created successfully.")
    return
