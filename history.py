import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import json
matplotlib.use('Agg')

def visual1(main_id, cursor, tableM):
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


def visual2(top10):
    v2 = bar(top10, 'SKILLS')
    v2.savefig('static/history/vis2.png', bbox_inches='tight')
    v2.clf()

    print("visualization-2 Done")
    return


def visual3(top10):
    """ This Method is used to do visualization 3 and the first row(id=1) 
    is used to have the average skills percentage and second row(id=2)
    is used to tell whether the skill having tests are taken atleast 3 times or not
    """
    v3 = bar(top10, 'OVERALL SKILLS')
    v3.savefig('static/history/vis3.png', bbox_inches='tight')
    v3.clf()

    print("visualization-3 Done")
    return


def visual4(dates, scores):
    print("$$$$$$$$$$$$$$", dates, scores)
    scorePlot(dates, scores)

    print("visualization-4 Done")
    return


def visual5(domain, tableM, cursor, main_id):
    query = "SELECT date,score_per FROM "+tableM + \
        " WHERE domain = '"+domain+"' and id<="+str(main_id)+";"
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
    v5.savefig('static/history/vis5.png')
    v5.clf()

    print("visualization-5 Done")
    return


def visual6(skill, tableS, cursor, sub_id):
    query = "SELECT date,"+skill+" FROM "+tableS+" where id<="+str(sub_id)+";"
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
    v6.savefig('static/history/vis6.png')
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

    for i in range(3):
        if val_counts[i] == 0:
            data.pop(labels[i])
        else:
            data[labels[i]].extend([val[i], val_counts[i]])
    print(data)
    labels, colors, val, val_counts = [], [], [], []
    for key, value in data.items():
        labels.append(key)
        colors.append(value[0])
        val.append(value[1])
        val_counts.append(value[2])

    plt.pie(val, labels=[f'{label} ({size})' for label, size in zip(
        labels, val_counts)], colors=colors, autopct='%1.1f%%')
    plt.title('Result')
    plt.savefig('static/history/vis1.png')
    plt.clf()
    # plt.show()
    return


def bar(k, title):
    keys = list(k.keys())
    values = list(k.values())
    sorted_index = np.argsort(values)
    sorted_index = reversed(sorted_index)
    k = {keys[i]: values[i] for i in sorted_index}
    if (len(k) > 10):
        k = {key: value for key, value in list(k.items())[:10]}
    categories = list(k.keys())
    values = list(k.values())
    for i in range(len(values)):
        values[i] *= 100
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
    for i, v in enumerate(values):
        plt.text(i, v + 0.1, str(round(v, 2)), ha='center', va='bottom')

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

    plt.savefig('static/history/vis4.png', bbox_inches='tight')
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


def history_plots(cursor, tableM, tableH, test_id):
    sql = "select * from "+tableH+" where id = "+str(test_id)+";"
    cursor.execute(sql)
    k = cursor.fetchall()
    print(k[0][8])
    main_id = k[0][4]
    sub_id = k[0][5]
    v2top = json.loads(k[0][8])
    v3top = json.loads(k[0][9])
    v4dates = json.loads(k[0][10])
    v4scores = json.loads(k[0][11])
    test_table = k[0][12]
    data_dict = json.loads(k[0][13])
    print("sssssssssss", test_table, data_dict)
    data = getData(cursor, test_table, data_dict)
    visual1(main_id, cursor, tableM)
    visual2(v2top)
    visual3(v3top)
    visual4(v4dates, v4scores)
    return main_id, sub_id, data


def getData(cursor, test_table, data_dict):
    if test_table is None:
        return None
    print("hchvhch")
    query = "select * from "+test_table+";"
    cursor.execute(query)
    k = cursor.fetchall()
    print(k)
    vals = ['A', 'B', 'C', 'D']
    data = []
    for i in k:
        if str(i[0]) in data_dict.keys():
            # data.append(i[0], i[1])
            correct = i[vals.index(i[8])+2]
            if data_dict[str(i[0])] == "Unknown":
                select = "Unknown"
            else:
                select = i[vals.index(data_dict[str(i[0])])+2]
            data.append((str(i[0]), i[1], correct, select))
            print(data)
    return data
