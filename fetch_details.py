import recommend as rc

def getDomains(cursor):
    query = "select domain from domain_tests;"
    cursor.execute(query)
    domains = list(cursor.fetchall())
    return domains


def getTests(cursor, domain):
    query = "select test_table from Domain_Tests where domain='"+domain.lower() + \
        "';"
    cursor.execute(query)
    test_table = cursor.fetchone()[0]
    query = "select tests,questions_table,Topics from "+test_table+" ;"
    cursor.execute(query)
    tests = list(cursor.fetchall())
    return tests


def getques(cursor, table):
    query = "select * from "+table+";"
    cursor.execute(query)
    ques = list(cursor.fetchall())
    return ques


def getIds(cursor, tableM, tableS):
    query = "SELECT id FROM "+tableM+" ORDER BY id DESC LIMIT 1;"
    cursor.execute(query)
    main_id = cursor.fetchone()
    if main_id:
        main_id = main_id[0]
    query = "SELECT id FROM "+tableS+" ORDER BY id DESC LIMIT 1;"
    cursor.execute(query)
    sub_id = cursor.fetchone()
    if sub_id:
        sub_id = sub_id[0]
    return main_id, sub_id


def getSkills(conn, tableS):
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

    # Sort the dictionary based on its values using sorted() with a lambda function
    high_scores = dict(
        sorted(high_scores.items(), key=lambda item: item[1], reverse=True))
    high_scores = dict(list(high_scores.items())[:5])
    low_scores = dict(
        sorted(low_scores.items(), key=lambda item: item[1], reverse=True))
    low_scores = dict(list(low_scores.items())[:5])
    print("High:", high_scores)
    print("Low:", low_scores)
    print(list(high_scores.keys()))
    print(list(low_scores.keys()))
    return high_scores, low_scores


def getRecom(conn, tableS):
    hskills, lskills = getSkills(conn, tableS)
    print(hskills, lskills)
    print(type(hskills))
    print("___hskills", hskills)
    # WSkills = ["coding", "aptitude", "English"]
    WSkills = hskills.keys()
    print(WSkills)
    dataset = 'Exam_Recommendation.csv'
    val = 'Exam Name'
    rexms = rc.RecommendExam(WSkills, dataset, val)
    # SSkills = ["coding", "aptitude", "English"]
    SSkills = lskills.keys()
    print(SSkills)
    dataset = 'job_recommendation.csv'
    val = 'job'
    rjobs = rc.RecommendJob(SSkills, dataset, val)
    return hskills, rjobs, lskills, rexms


def getHistory(cursor, table):
    query = "select id,test,domain,score,val_counts from "+table+";"
    cursor.execute(query)
    history = list(cursor.fetchall())
    return history


def getProfileDetails(conn, username):
    cursor = conn.cursor(
        dictionary=True)
    if username == '':
        username = 'root'
    print(username)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    profile = cursor.fetchall()
    return profile


def getExamCount(cursor, tableH, domain, test):
    query = "select count(*) from "+tableH + \
        " where domain = '"+domain+"' and test = '"+test+"';"
    print(query)
    cursor.execute(query)
    exam_count = cursor.fetchone()[0]
    return exam_count
