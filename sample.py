import recommend as rc
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import mysql.connector
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)


@app.route('/')
def start():
    """ This Method is called on the home and this just displays the start.html
    """
    return render_template('start.html')


@app.route('/index_page')
def test():
    """ This Method is called on clicking start button in start.html
    This will calls Test_Start() method , also fetches the questions
    from questions table and gives to index.html and renders index.html.
    """
    global main_id
    global sub_id
    global count1
    main_id, sub_id = Test_Start()
    cursor = conn.cursor(dictionary=True)
    # Fetch data from the 'questions' table
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    # print(questions)
    count1 = len(questions)
    cursor = conn.cursor()
    # Render the HTML template with the fetched data
    return render_template('index.html', questions=questions)


def Test_Start():
    """This Method fetches the current date time and sets the Domain for the exam also
    and calls the EnterMain() and EnterSub() Methods.
    """
    query = "select now();"
    cursor.execute(query)
    date = cursor.fetchone()[0]
    print(date)
    domain = 'DS'
    # inserting date,id,domain into main table
    main_id = EnterMain(cursor, date, domain, tableM)
    # insert date,id into subtopic table
    sub_id = EnterSub(cursor, date, tableS)
    return main_id, sub_id


def check_table_exists(table_name):
    """Function to check if a table exists in the database"""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None


def EnterMain(cursor, date, domain, tableM):
    """ This Method is used to enter data(all null values except date-time and domain)
    into main table(TableM) and then returns the id of that row as main_id
    """

    # Check if the 'sample' table exists
    if not check_table_exists(tableM):
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
    # Check if the 'sample' table exists
    if not check_table_exists(tableS):
        #     create_table_query = """
        # CREATE TABLE """+tableS+""" (
        #     id INT AUTO_INCREMENT PRIMARY KEY,
        #     date timestamp
        # )
        # """
        #     cursor.execute(create_table_query)

        # Create the table and insert data into it in a single SQL statement
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
        # Execute both queries in a single execute call
        cursor.execute(create_table_query)
        cursor.execute("commit;")
        cursor.execute(insert_data_query)
        cursor.execute("commit;")
        cursor.execute(insert_data_query)
        cursor.execute("commit;")
        print("Table 'sample' created successfully.")

        # insert_query = """insert into"""

    query = "SELECT count(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+tableS+"';"
    cursor.execute(query)
    cols = cursor.fetchone()[0]-2
    nulls = ",NULL"*cols
    # print(nulls)
    query = "insert into "+tableS+" values(NULL,'"+str(date)+"'"+nulls+");"
    cursor.execute(query)
    cursor.execute("commit;")

    query = "select id from "+tableS+" where date='"+str(date)+"';"
    cursor.execute(query)
    sub_id = cursor.fetchone()[0]

    print("id of table is", sub_id)
    print("inserting date into the subtopic table is successful")
    return sub_id


@app.route('/submit_answers', methods=['POST'])
def submit_form():
    """ This Method is called when the submit button in the Test page is clicked 
    ids array contains the id(1,2,..etc) of the question and These we can get
    from the hidden field having name as q1_id,q2_id..etc that is present index.html 
    ops array contains the option(A,B,C...etc) that user has selected and These we can get
    from the radio input field having name as q1,q2..etc that is present index.html
    count1 is the count of questions that is found in test() method , it also calls
    enterDataToDB(),result() and Test_End() methods
    """
    ids = []
    ops = []
    for i in range(1, +
                   9+1):
        id = request.form.get('q'+str(i)+'_id')
        op = request.form.get('q'+str(i))
        ids.append(id)
        ops.append(op)
    # print(ids)
    # print(ops)

    enterDataToDB(ids, ops)
    result()
    Test_End(main_id, sub_id)
    return render_template('submit.html')


def enterDataToDB(ids, op):
    """This Method is used to enter the answers that are selected by the user
    into the user table it drops the existing user table and then it 
    creates the user table and enters the data
    """
    select_query = "DROP TABLE IF EXISTS user"
    cursor.execute(select_query)
    select_query = "create table user(id varchar(50),answer varchar(10))"
    cursor.execute(select_query)
    insert_query = "INSERT INTO user VALUES (%s, %s)"
    for i in range(len(ids)):
        values = (ids[i], op[i])
        cursor.execute(insert_query, values)
    conn.commit()


def result():
    """This Method is used to compute the results of the user test by creating temp view
    and creates the pie chart with name pie1.png that shows the Correct and Incorrect
    percentages in it.
    """
    select_query = "DROP VIEW IF EXISTS temp"
    cursor.execute(select_query)
    select_query = "create view temp as select a.id,a.answer,b.difficulty,b.skill,case WHEN a.answer IS NULL THEN -1 when a.answer=b.correct_Answer then 1 else 0 end as result from questions b join user a where a.id=b.id"
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
    # plt.show()
    return


def Test_End(main_id, sub_id):
    """ This Method is the last method that is called finally and this method 
    is mainly used to generate all the other visualizations from the 
    temp table(That contains the user test results).
    This method calls ExitMain(),Exitsub() and visualizations methods.
    """
    resTable = 'temp'
    # inserting remaining into main table
    ExitMain(main_id, resTable)
    # inserting remaining into subtopic table
    sp = ExitSub(sub_id, resTable)
    # visualization-1
    visual1(main_id)
    # visualization-2
    visual2(sub_id, sp)
    # visualization-3
    visual3()
    # visualization-4
    visual4()
    # visualization-5
    # # domain = "DS"
    # visual5(domain)
    # # visualization-6
    # # subtopic = ""
    # visual6(subtopic)


def ExitMain(main_id, resTable):
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


def ExitSub(sub_id, resTable):
    """ This Method is used to enter all the remaining details 
    into the subtopic table(TableS) and it returns the skills 
    that are present inn subtopic table.
    """
    query = "select distinct skill from "+resTable+";"
    cursor.execute(query)
    skills = cursor.fetchall()
    print(skills)

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

    getSkills()
    print("Entering Remaining details into subtopic table is done")
    return skills


def visual1(main_id):
    query = "select score_per,incorrect_per,total,correct,incorrect from " + \
        tableM+" where id = "+str(main_id)+";"
    cursor.execute(query)
    val = list(cursor.fetchone())
    print("000000000", val)
    val_counts = [val[3], val[4], (val[2]-val[3]-val[4])]
    val = val[:-3]
    print("unat", 1-val[0]-val[1])
    print("ABS-unat", abs(1-val[0]-val[1]))
    val.append(abs(1-val[0]-val[1]))
    print("correct-incorrect__________", val)
    pie(val, val_counts)

    print("visualization-1 Done")
    return


def visual2(sub_id, sp):
    top10 = {}
    for i in sp:
        query = "select "+i[0]+" from "+tableS+" where id = "+str(sub_id)+";"
        cursor.execute(query)
        top10[i[0]] = cursor.fetchone()[0]
    # print("initial:",top10)
    v2 = bar(top10, 'SKILLS')
    # v2.savefig('static/vis2.png')
    v2.savefig('static/vis2.png', bbox_inches='tight')
    v2.clf()

    print("visualization-2 Done")
    return


def visual3():
    """ This Method is used to do visualization 3 and the first row(id=1) 
    is used to have the average skills percentage and second row(id=2)
    is used to tell whether the skill having tests are taken atleast 3 times or not
    """
    top10 = {}
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+tableS+"';"
    cursor.execute(query)
    sub = cursor.fetchall()
    print(sub)
    sub.remove(('date',))
    sub.remove(('id',))
    print(sub)
    sub_topics = []
    for i in range(len(sub)):
        sub_topics.append(sub[i][0])
    print(sub_topics)
    for i in sub_topics:
        query = "select "+i+" from "+tableS+" where id = 1;"
        cursor.execute(query)
        top10[i] = cursor.fetchone()[0]
    print("initial:", top10)
    v3 = bar(top10, 'OVERALL SKILLS')
    # v3.savefig('static/vis3.png')
    v3.savefig('static/vis3.png', bbox_inches='tight')
    v3.clf()

    print("visualization-3 Done")
    return


def visual4():
    query = "SELECT date,score_per FROM (SELECT id,date,score_per FROM " + \
        tableM+" ORDER BY id DESC LIMIT 10) AS a ORDER BY id ASC;"
    # SELECT * FROM (select * from s1 ORDER BY id DESC LIMIT 10) as a order by id asc
    cursor.execute(query)
    sub = cursor.fetchall()
    scores = []
    dates = []
    print(sub)
    for i in sub:
        date = str(i[0])
        date = date.replace(" ", "\n")
        dates.append(date)
        # print(date)
        if i[1] is not None:
            scores.append(i[1]*100)
        else:
            scores.append(0*100)
    print("$$$$$$$$$$$$$$", dates, scores)
    scorePlot(dates, scores)

    print("visualization-4 Done")
    return


def visual5(domain):
    query = "SELECT date,score_per FROM "+tableM+" WHERE domain = '"+domain+"';"
    cursor.execute(query)
    domain_sub = cursor.fetchall()

    domain_count = 0
    Top_scores = []
    for i in range(len(domain_sub)-1, -1, -1):
        if domain_sub[i][1] != None and domain_count < 10:
            Top_scores.insert(0, domain_sub[i])
            domain_count += 1
    domain_sub = Top_scores
    scores = []
    dates = []
    for i in domain_sub:
        date = str(i[0])
        date = date.replace(" ", "\n")
        dates.append(date)
        scores.append(i[1]*100)
    v5 = linePlot(dates, scores, domain, 'limegreen')
    v5.subplots_adjust(bottom=0.25)
    v5.savefig('static/vis5.png')
    v5.clf()

    print("visualization-5 Done")
    return


def visual6(skill):
    query = "SELECT date,"+skill+" FROM "+tableS+";"
    cursor.execute(query)
    skills_sub = cursor.fetchall()
    # print(skills_sub)
    skill_count = 0
    Top_scores = []
    for i in range(len(skills_sub)-1, 1, -1):
        if skills_sub[i][1] != None and skill_count < 10:
            Top_scores.insert(0, skills_sub[i])
            skill_count += 1
    skills_sub = Top_scores
    scores = []
    dates = []
    # print(skills_sub)
    for i in skills_sub:
        date = str(i[0])
        date = date.replace(" ", "\n")
        dates.append(date)
        scores.append(i[1]*100)
    v6 = linePlot(dates, scores, skill, 'gold')
    v6.subplots_adjust(bottom=0.25)
    v6.savefig('static/vis6.png')
    v6.clf()

    print("visualization-6 Done")
    return


# representations used in visualizations

def pie(val, val_counts):
    data = {}
    data['Correct'] = ['green']
    data['Incorrect'] = ['red']
    data['Unattempted'] = ['yellow']
    # print(data)
    labels = ['Correct', 'Incorrect', 'Unattempted']
    # sample_val_counts = val_counts.copy()
    # colors = ['green', 'red', 'yellow']

    # print(val, val_counts, labels, colors)
    for i in range(3):
        # print(sample_val_counts)
        if val_counts[i] == 0:
            data.pop(labels[i])
        else:
            data[labels[i]].extend([val[i], val_counts[i]])
    print(data)
    # print(val, val_counts, labels, colors)
    labels, colors, val, val_counts = [], [], [], []
    for key, value in data.items():
        labels.append(key)
        colors.append(value[0])
        val.append(value[1])
        val_counts.append(value[2])

    plt.pie(val, labels=[f'{label} ({size})' for label, size in zip(
        labels, val_counts)], colors=colors, autopct='%1.1f%%')
    plt.title('Result')
    plt.savefig('static/vis1.png')
    plt.clf()
    # plt.show()
    return


def bar(k, title):
    keys = list(k.keys())
    values = list(k.values())
    sorted_index = np.argsort(values)
    sorted_index = reversed(sorted_index)
    k = {keys[i]: values[i] for i in sorted_index}
    # print("sorted:",k)
    if (len(k) > 10):
        k = {key: value for key, value in list(k.items())[:10]}
    # print("final top 10:",k)

    categories = list(k.keys())
    values = list(k.values())
    for i in range(len(values)):
        values[i] *= 100
    # print("top scores:",values)
    first_n_bars = 5
    color_first_n = 'green'
    color_remaining = 'gold'
    colors = [color_first_n if i <
              first_n_bars else color_remaining for i in range(len(categories))]
    plt.bar(categories, values, color=colors)
    plt.xlabel('Subtopics', fontweight='bold')
    plt.ylabel('Score', fontweight='bold')
    plt.title(title)
    plt.ylim(0, 105)
    plt.xticks(rotation='vertical')
    # Add bar values on top of the bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.1, str(round(v, 2)), ha='center', va='bottom')

    # plt.show()
    return plt


def scorePlot(categories, values):
    bar_color = 'lightblue'
    line_color = 'red'
    plt.bar(categories, values, color=bar_color, label='Bar Graph')
    plt.plot(categories, values, color=line_color,
             marker='o', linestyle='-', label='Line Plot')
    plt.xlabel('\nDate', fontweight='bold')
    plt.ylabel('Score', fontweight='bold')
    plt.title('OVERALL PERFORMANCE')
    plt.xticks(rotation='vertical')
    plt.ylim(0, 105)
    plt.legend()
    plt.subplots_adjust(bottom=0.25)

    # Add bar values on top of the bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.1, str(round(v, 2)), ha='center', va='bottom')

    plt.savefig('static/vis4.png', bbox_inches='tight')
    plt.clf()
    # plt.show()
    return


def linePlot(dates, scores, title, color):
    plt.plot(dates, scores, color=color, marker='o')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('\nScore', fontweight='bold')
    if (color == 'limegreen'):
        plt.title(title.upper()+' DOMAIN PERFORMANCE')
    else:
        plt.title(title.upper()+' SKILL PERFORMANCE')
    plt.ylim(0, 110)
    plt.xticks(rotation="vertical")
    for i in range(len(dates)):
        plt.text(dates[i], scores[i]+2, str(round(scores[i], 1)),
                 ha='center', va='bottom')
    # plt.show()
    return plt


def empPlot(path, year):
    plt.plot()
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('\nScore', fontweight='bold')
    plt.ylim(0, 110)
    plt.xlim(2000, year)
    plt.savefig(path)
    plt.clf()
    print("empt")
    return


def getSkills():
    query = "select * from "+tableS+" where id < 3;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    skills = cursor.fetchall()
    # print(k)
    # print(type(k))
    for skill in skills:
        skill.pop('id', None)

    # Use the second dictionary as a filter criteria
    criteria_dict = skills[1]

    # Modify the first dictionary based on the criteria
    skills_scores = {key: value for key,
                     value in skills[0].items() if criteria_dict.get(key) == 1}

    print(skills_scores)

    # Initialize empty dictionaries for high and low value pairs
    high_scores = {}
    low_scores = {}

    # Iterate through each item in skills and classify based on their values
    for key, value in skills_scores.items():
        if value > 0.75:
            high_scores[key] = value
        elif value < 0.35:
            low_scores[key] = value

    print("High:", high_scores)
    print("Low:", low_scores)

    print(list(high_scores.keys()))
    print(list(low_scores.keys()))
    return list(high_scores.keys()), list(low_scores.keys())


@app.route('/result1_page')
def show_test_result():
    return render_template('result1.html')


@app.route('/result2_page', methods=['GET', 'POST'])
def show_overall_result():
    global selected_domain, selected_skill
    # print("start")
    if request.method == 'POST':
        # print("post")
        if (request.form.get('selected_domain') != None):
            selected_domain = request.form.get('selected_domain')
        if (request.form.get('selected_skill') != None):
            selected_skill = request.form.get('selected_skill')
        # print("skill", selected_skill)
        # print("domain", selected_domain)
        # selected_domain = None
        # selected_skill = None
        if selected_domain != "None" and selected_domain is not None:
            visual5(selected_domain)
        else:
            empPlot('static/vis5.png', 2024)

        if selected_skill != "None" and selected_skill is not None:
            visual6(selected_skill)
        else:
            empPlot('static/vis6.png', 2024)

    # Get domain options
    query = "SELECT DISTINCT domain FROM " + tableM + ";"
    cursor.execute(query)
    domains = ["None"]
    domains.extend(list(cursor.fetchall()[0]))
    domain_options = domains

    # Get skill options
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tableS + "';"
    cursor.execute(query)
    sub = cursor.fetchall()
    sub.remove(('date',))
    sub.remove(('id',))
    skills = ["None"]
    for i in range(len(sub)):
        skills.append(sub[i][0])
    skill_options = skills

    # print("end")

    hskills, lskills = getSkills()
    WSkills = ["coding", "aptitude", "English"]
    dataset = 'Exam_Recommendation.csv'
    val = 'Exam Name'
    rexms = rc.RecommendExam(WSkills, dataset, val)
    SSkills = ["coding", "aptitude", "English"]
    dataset = 'job_recommendation.csv'
    val = 'job'
    rjobs = rc.RecommendJob(SSkills, dataset, val)

    return render_template('result2.html', d_options=domain_options, s_options=skill_options, selected_domain=selected_domain, selected_skill=selected_skill, exams=rexms, jobs=rjobs, wskills=lskills, sskills=hskills)


db_password = "Tejas@root29"
db_name = "server"
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database=db_name
)
cursor = conn.cursor()
tableM = "main_U"
tableS = "s1"
selected_domain = "None"
selected_skill = "None"

app.run()

conn.close()
