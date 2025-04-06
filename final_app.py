# import recommend as rc
import fetch_details
import test_start
import test_end
import tables
import visuals as vsl
import history as his
import json
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Generate a random secret key
secret_key = os.urandom(24)
# Set the secret key for the application
app.secret_key = secret_key


# Before request handler to redirect all requests to '/' if accessed externally
@app.before_request
def check_access():
    print("checking")
    if not request.path.startswith('/static'):
        if request.endpoint not in ['login', 'signup', 'Main', 'home', 'help_page'] and 'internal_access' not in session:
            return redirect(url_for('Main'))
        elif request.endpoint == 'home' and 'internal_access' not in session:
            print("login")
            msg = "Please Login To Access"
            return render_template('login.html', message=msg)


@app.route('/')
def Main():
    session.pop('internal_access', None)
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_name
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (username,))
            user = cursor.fetchone()
        user_name = user[1]
        if user_name == 'root':
            user_name = ''
        if user and user[2] == password:
            session['internal_access'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    if request.method == 'GET':
        message = session.pop('message', None)
        return render_template('login.html', message=message)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("this is signup")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        cpass = request.form['cpass']
        phone = request.form['phone']
        email = request.form['email']
        gender = request.form['gender']
        qualification = request.form['qualification']
        areas = request.form['skill']
        print(username, password, cpass, phone,
              email, gender, qualification, areas)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return render_template('signup.html', error="Username already exists.")
        else:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return render_template('signup.html', error="email already exists.")
            else:
                cursor.execute(
                    "INSERT INTO users (username, password,email,phone,gender,qualification,areas) VALUES (%s, %s,%s,%s,%s,%s,%s)", (username, password, email, phone, gender, qualification, areas))
                cursor.execute("commit;")
                session['message'] = "Signup Successful! LOGIN To Enter Portal!"
                return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('internal_access', None)
    return redirect(url_for('login'))


@app.route('/helproute')
def help_route():
    if 'internal_access' not in session:
        return render_template('main_page.html')
    else:
        return render_template('home.html')


@app.route('/home')
def home():
    global path, main_id, sub_id, dropdown_selected_domain, dropdown_selected_skill, tableH, tableM, tableS
    # print("index")
    # user_name = ''
    tableM = user_name + 'Main_U'
    tableS = user_name + 's1'
    tableH = user_name + "history"
    path = "insights"
    dropdown_selected_domain = "None"
    dropdown_selected_skill = "None"
    tables.createTableH(cursor, tableH)
    tables.createTableM(cursor, tableM)
    tables.createTableS(cursor, tableS)
    main_id, sub_id = fetch_details.getIds(cursor, tableM, tableS)
    if main_id is None:
        vsl.empPlot("static/"+path+"/vis3.png", 2024)
        vsl.empPlot("static/"+path+"/vis4.png", 2024)
    else:
        vsl.visual3(cursor, tableS)
        vsl.visual4(cursor, tableM)
    print("home", main_id, sub_id)
    return render_template('home.html')


@app.template_filter('json_to_list')
def json_to_list(json_str):
    return json.loads(json_str)


@app.route('/Take_test')
def test_click():
    domains = fetch_details.getDomains(cursor)
    print(domains)
    session['take_test_visited'] = True
    return render_template('testclick.html', domains=domains)


@app.route('/Analytics', methods=['GET', 'POST'])
def analytics():
    print(main_id, sub_id)
    global dropdown_selected_domain, dropdown_selected_skill
    # print(dropdown_selected_domain, dropdown_selected_skill)
    # print("start")
    path5 = "static/"+path+"/vis5.png"
    path6 = "static/"+path+"/vis6.png"
    print(path5, path6)
    if request.method == 'POST':
        # print("post")
        if (request.form.get('selected_domain') != None):
            dropdown_selected_domain = request.form.get('selected_domain')
        if (request.form.get('selected_skill') != None):
            dropdown_selected_skill = request.form.get('selected_skill')
        print("skill", dropdown_selected_skill)
        print("domain", dropdown_selected_domain)
        # selected_domain = None
        # selected_skill = None
        if dropdown_selected_domain != "None" and dropdown_selected_domain is not None and main_id is not None:
            vsl.visual5(dropdown_selected_domain,
                        tableM, cursor, main_id, path5)
        else:
            vsl.empPlot(path5, 2024)

        if dropdown_selected_skill != "None" and dropdown_selected_skill is not None and sub_id is not None:
            vsl.visual6(dropdown_selected_skill, tableS, cursor, sub_id, path6)
        else:
            vsl.empPlot(path6, 2024)
    else:
        vsl.empPlot(path5, 2024)
        vsl.empPlot(path6, 2024)

    # Get domain options
    query = "SELECT DISTINCT domain FROM " + tableM + ";"
    cursor.execute(query)
    domains = ["None"]
    temp = cursor.fetchall()
    for i in temp:
        domains.append(i[0])
    # domains.extend(list())
    domain_options = domains
    # print(domain_options)

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
    details = fetch_details.getProfileDetails(conn, user_name)[0]
    return render_template('analytics.html', d_options=domain_options, s_options=skill_options, selected_domain=dropdown_selected_domain, selected_skill=dropdown_selected_skill, path=path, username=details['username'])


@app.route('/Recommendations')
def recommendations():
    sskills, rjobs, wskills, rexms = fetch_details.getRecom(conn, tableS)
    print(sskills, rjobs, wskills, rexms)
    sskills_vals = list(sskills.values())
    sskills = list(sskills.keys())
    wskills_vals = list(wskills.values())
    wskills = list(wskills.keys())
    return render_template('recommendations.html', strong_skills=sskills, strong_skills_vals=sskills_vals, weak_skills=wskills, weak_skills_vals=wskills_vals, rec_jobs=rjobs, rec_exms=rexms)


@app.route('/History')
def history():
    history = fetch_details.getHistory(cursor, tableH)
    details = fetch_details.getProfileDetails(conn, user_name)[0]
    print(history)
    return render_template('history.html', history=history, username=details['username'], id=details['id'])


@app.route('/Help')
def help_page():
    return render_template('help.html')


@app.route('/Test_page', methods=['POST', 'GET'])
def TestPage():
    global flag
    if 'take_test_visited' not in session:
        print("subash")
        return redirect(url_for('test_click'))
    global selected_domain
    print("hello")
    if request.method == 'POST':
        session['test_page_visited'] = True
        selected_domain = request.form.get('domain_option')
        # Do something with the input data, for example, print it
        print("Domain:", selected_domain)
    tests = fetch_details.getTests(cursor, selected_domain)
    print(tests)
    message = None
    if flag:
        flag = False
        message = "Exam limit Exceeds"
    return render_template('testPage.html', tests=tests, message=message)


@app.route('/Instructions', methods=['POST', 'GET'])
def Instructions():
    if 'test_page_visited' not in session:
        return redirect(url_for('test_click'))
    global test_name, flag, test_table
    session['instruction_visited'] = True
    selected_domain_test = request.form.get('test_option')
    print("ss", selected_domain_test)
    s = list(selected_domain_test[1:-1].split(','))
    print(s)
    selected_domain_test = [s[0], s[1], s[2:]]
    test_name = s[0]
    test_table = s[1]
    exam_count = fetch_details.getExamCount(
        cursor, tableH, selected_domain, test_name)
    if exam_count >= max_exam_count:
        flag = True
        return redirect(url_for('TestPage'))
    print(selected_domain_test)
    return render_template('instructions.html', test_table=selected_domain_test, domain=selected_domain)


@app.route('/Test', methods=['POST', 'GET'])
def Test():
    """ This Method is called on clicking start button in start.html
    This will calls Test_Start() method , also fetches the questions
    from questions table and gives to index.html and renders index.html.
    """
    if 'instruction_visited' not in session:
        return redirect(url_for('test_click'))
    global main_id, sub_id, history_id, flag
    main_id, sub_id = test_start.Test_Start(
        cursor, tableM, tableS, selected_domain)
    history_id = test_start.enterHistory(
        cursor, tableH, test_name, selected_domain, tableM, main_id)
    selected_test_table = request.form.get('inst_option')
    print(selected_test_table)
    ques = fetch_details.getques(conn.cursor(
        dictionary=True), selected_test_table)
    # print(ques)
    session.pop('instruction_visited', None)
    session.pop('take_test_visited', None)
    session.pop('test_page_visited', None)
    return render_template('test.html', test_data=ques)


@app.route('/TestAnalytics', methods=['POST', 'GET'])
def TestAnalytics():
    global main_id, sub_id, path, dropdown_selected_skill, dropdown_selected_domain
    print(request.form)
    if len(request.form) == 0:
        return render_template('home.html')
    # print(type(request.form))
    # print("sss", request.form['form_id'])
    if request.form.get('selc_answers') is not None:
        selected_ans = request.form.get('selc_answers')
        data = json.loads(selected_ans)
        print(data)
        ids = []
        options = []
        ans = ['A', 'B', 'C', 'D']
        for i in data:
            ids.append(i['id'])
            if i['answer'] is not None:
                options.append(ans[i['answer']])
            else:
                options.append(None)
            # print(i['answer'], type(i['answer']))
        print(ids, options)
        test_end.enterDataToDB(conn, ids, options)
        data = test_end.result(cursor, test_table)
        data_dict = test_end.getDict(data)
        test_end.Test_End(main_id, sub_id, conn, tableM,
                          tableS, tableH, history_id, test_table, data_dict)
        test_end.remove_tables(cursor)
        print(data)
    elif request.form.get('test_option') is not None:
        test_id = request.form.get('test_option')
        print(test_id)
        # test_id = 1
        main_id, sub_id, data = his.history_plots(
            cursor, tableM, tableH, test_id)
        path = 'history'
        dropdown_selected_domain = "None"
        dropdown_selected_skill = "None"
        print(data)
    return render_template('analtics_after_test.html', path=path, data=data)


@app.route('/Profile')
def Profile():
    details = fetch_details.getProfileDetails(conn, user_name)[0]
    print(details)
    if 'id' in details:
        details.pop('id')
    if 'password' in details:
        details.pop('password')
    details['areas'] = list(details['areas'].split(','))
    print(details)
    return render_template('profile.html', details=details)


db_password = "Nithin@714"
db_name = "server"
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

user_name = ''
max_exam_count = 40
flag = False
app.run()

conn.close()
