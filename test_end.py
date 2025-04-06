import matplotlib.pyplot as plt
import visuals as vsl
import matplotlib
import json
matplotlib.use('Agg')


def enterDataToDB(conn, ids, op):
    """This Method is used to enter the answers that are selected by the user
    into the user table it drops the existing user table and then it 
    creates the user table and enters the data
    """
    cursor = conn.cursor()
    select_query = "DROP TABLE IF EXISTS user"
    cursor.execute(select_query)
    select_query = "create table user(id varchar(50),answer varchar(10))"
    cursor.execute(select_query)
    insert_query = "INSERT INTO user VALUES (%s, %s)"
    for i in range(len(ids)):
        values = (ids[i], op[i])
        cursor.execute(insert_query, values)
    conn.commit()

def result(cursor, table):
    """This Method is used to compute the results of the user test by creating temp view
    and creates the pie chart with name pie1.png that shows the Correct and Incorrect
    percentages in it.
    """
    select_query = "DROP VIEW IF EXISTS temp"
    cursor.execute(select_query)
    select_query = "create view temp as select a.id,a.answer,b.difficulty,b.skill,case WHEN a.answer IS NULL THEN -1 when a.answer=b.correct_Answer then 1 else 0 end as result from " + \
        table+" b join user a where a.id=b.id"
    cursor.execute(select_query)
    select_query = ""
    q1 = "select * from temp"
    cursor.execute(q1)
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
        id, answer, diff, skill, result = row
        print(
            f"ID: {id}, answer: {answer},difficulty:{diff},skill:{skill},result: {result}")

    query = "select count(result) from temp where result=1"
    cursor.execute(query)
    correct = cursor.fetchone()[0]
    query = "select count(result) from temp"
    cursor.execute(query)
    total = cursor.fetchone()[0]

    print(correct, total)

    labels = ['Correct', 'Incorrect']
    sizes = [correct, (total-correct)]
    samples = [9, 0]
    print(sizes)
    colors = ['green', 'red']
    
    plt.pie(sizes, labels=[f'{label} ({size})' for label, size in zip(
        labels, samples)], colors=colors, autopct='%1.1f%%')
    plt.title('Result')
    plt.savefig('static/pie1.png')
    plt.clf()
    query = "SELECT q.id,q.question, CASE \
           WHEN q.correct_answer = 'A' THEN q.option_A \
           WHEN q.correct_answer = 'B' THEN q.option_B \
           WHEN q.correct_answer = 'C' THEN q.option_C \
           WHEN q.correct_answer = 'D' THEN q.option_D \
           ELSE 'Unknown' END AS correct_option,\
       CASE \
           WHEN t.answer = 'A' THEN q.option_A\
           WHEN t.answer = 'B' THEN q.option_B\
           WHEN t.answer = 'C' THEN q.option_C\
           WHEN t.answer = 'D' THEN q.option_D\
           ELSE 'Unknown' \
       END AS selected_option \
        FROM "+table+" q \
        JOIN temp t ON q.id = t.id AND q.skill = t.skill \
        WHERE t.result IN (0, -1);"
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def Test_End(main_id, sub_id, conn, tableM, tableS, tableH, history_id, test_table, data):
    """ This Method is the last method that is called finally and this method 
    is mainly used to generate all the other visualizations from the 
    temp table(That contains the user test results).
    This method calls ExitMain(),Exitsub() and visualizations methods.
    """
    resTable = 'temp'
    cursor = conn.cursor()
    # inserting remaining into main table
    ExitMain(main_id, resTable, cursor, tableM)
    # inserting remaining into subtopic table
    sp = ExitSub(sub_id, resTable, conn, tableS)
    # visualization-1
    score, val_counts = vsl.visual1(main_id, cursor, tableM)
    # visualization-2
    v2top = vsl.visual2(sub_id, sp, cursor, tableS)
    # visualization-3
    v3top = vsl.visual3(cursor, tableS)
    # visualization-4
    v4dates, v4scores = vsl.visual4(cursor, tableM)
    v2top = json.dumps(v2top)
    v3top = json.dumps(v3top)
    v4dates = json.dumps(v4dates)
    v4scores = json.dumps(v4scores)
    data_dict = json.dumps(data)
    query = "update "+tableH+" set main_id = "+str(main_id)+",sub_id = "+str(sub_id)+",score="+str(score)+",val_counts='" + \
        str(val_counts)+"',v2top=(%s),v3top=(%s),v4dates=(%s),v4scores=(%s),test_table=(%s),data=(%s) where id ="+str(history_id)
    cursor.execute(query, (v2top, v3top, v4dates,
                   v4scores, test_table, data_dict))
    cursor.execute("commit;")


def ExitMain(main_id, resTable, cursor, tableM):
    """ This Method is used to enter all the remaining details 
    into the main table(TableM)
    """
    query = "select count(id) from "+resTable+";"
    cursor.execute(query)
    t = cursor.fetchone()[0]
    print(t)

    query = "select count(result) from "+resTable+" where result=1;"
    cursor.execute(query)
    c = cursor.fetchone()[0]
    print(c)

    query = "select count(result) from "+resTable+" where result=0;"
    cursor.execute(query)
    i = cursor.fetchone()[0]
    print(i)

    query = "select coalesce(sum(case when difficulty='hard' then 5 when difficulty='easy' then 1 when difficulty='medium' then 3 else 0 end),0)/(select sum(case when difficulty='hard' then 5 when difficulty='easy' then 1 when difficulty='medium' then 3 else 0 end) from "+resTable+") from "+resTable+" where result=1;"
    cursor.execute(query)
    sp = cursor.fetchone()[0]
    print(sp)

    query = "select coalesce(sum(case when difficulty='hard' then 5 when difficulty='easy' then 1 when difficulty='medium' then 3 else 0 end),0)/(select sum(case when difficulty='hard' then 5 when difficulty='easy' then 1 when difficulty='medium' then 3 else 0 end) from "+resTable+") from "+resTable+" where result=0;"
    cursor.execute(query)
    ip = cursor.fetchone()[0]
    print(ip)

    query = "update "+tableM+" set total="+str(t)+",correct="+str(c)+",incorrect="+str(
        i)+",score_per="+str(sp)+",incorrect_per="+str(ip)+" where id ="+str(main_id)
    cursor.execute(query)
    cursor.execute("commit;")

    print("Entering Remaining details into main table is done")
    return


def ExitSub(sub_id, resTable, conn, tableS):
    """ This Method is used to enter all the remaining details 
    into the subtopic table(TableS) and it returns the skills 
    that are present inn subtopic table.
    """
    cursor = conn.cursor()
    query = "select distinct skill from "+resTable+";"
    cursor.execute(query)
    skills = cursor.fetchall()
    print("ES____", skills)

    for i in skills:
        print(i)
        query = "select coalesce(sum(case when difficulty='hard' then 5 when difficulty='medium' then 3 when difficulty='easy' then 1 else 0 end),0)/(select sum(case when difficulty='hard' then 5 when difficulty='medium' then 3 when difficulty='easy' then 1 else 0 end) from " + \
            resTable+" where skill='" + \
                i[0]+"') from "+resTable+" where skill='"+i[0]+"' and result=1;"
        cursor.execute(query)
        per = cursor.fetchone()[0]
        # print("per",per)

        query = "select count(*) from information_schema.columns where table_schema ='server' and table_name='" + \
            tableS+"' and column_name='"+i[0]+"';"
        cursor.execute(query)
        cnt = cursor.fetchone()[0]
        # print("cnt",cnt)

        if (cnt == 0):
            query = "alter table "+tableS+" add column "+i[0]+" double;"
            cursor.execute(query)
        query = "update "+tableS+" set " + \
            i[0]+"="+str(per)+" where id ="+str(sub_id)
        cursor.execute(query)
        cursor.execute("commit;")

        # making average
        if (cnt != 0):
            query = "select avg("+i[0]+") from "+tableS+" where id>2;"
            cursor.execute(query)
            avg = cursor.fetchone()[0]
        else:
            avg = per

        # print(avg)
        query = "update "+tableS+" set "+i[0]+"="+str(avg)+" where id=1;"
        cursor.execute(query)
        cursor.execute("commit;")

        # this section for setting weak and strong skills
        query = "select "+i[0]+" from "+tableS+" where id=2;"
        print(query)
        cursor.execute(query)
        k = cursor.fetchone()[0]
        print("dsjdshjdqkqwvei_____", k)
        if k != 1:
            print("entered")
            query = "select count("+i[0]+") from "+tableS+";"
            cursor.execute(query)
            Exams_count = cursor.fetchone()[0]
            if Exams_count > 3:
                print("Updating the table")
                query = "update "+tableS+" set "+i[0]+"=1 where id=2;"
                cursor.execute(query)
                cursor.execute("commit;")
        else:
            print(i[0], " is useful to determine skills ", k)

    print("Entering Remaining details into subtopic table is done")
    return skills


def remove_tables(cursor):
    query = "drop table if exists user;"
    cursor.execute(query)
    print("user table Dropped successfully")
    query = "drop view if exists temp;"
    cursor.execute(query)
    print("temp view dropped successfully")
    return


def getDict(data):
    dataDict = {}
    for i in data:
        dataDict[i[0]] = list(i[3].split('.'))[0]
    print(dataDict)
    return dataDict
