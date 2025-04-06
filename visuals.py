import matplotlib.pyplot as plt
import numpy as np
import matplotlib
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
    score_per = val[0]
    print("visualization-1 Done")
    return score_per, val_counts


def visual2(sub_id, sp, cursor, tableS):
    top10 = {}
    for i in sp:
        query = "select "+i[0]+" from "+tableS+" where id = "+str(sub_id)+";"
        cursor.execute(query)
        top10[i[0]] = cursor.fetchone()[0]
    # print("initial:",top10)
    v2 = bar(top10, 'SKILLS')
    # v2.savefig('static/vis2.png')
    v2.savefig('static/insights/vis2.png', bbox_inches='tight')
    v2.clf()

    print("visualization-2 Done")
    return top10


def visual3(cursor, tableS):
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
    v3.savefig('static/insights/vis3.png', bbox_inches='tight')
    v3.clf()

    print("visualization-3 Done")
    return top10


def visual4(cursor, tableM):
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
    return dates, scores


def visual5(domain, tableM, cursor, main_id, path):
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
    v5.savefig(path)
    v5.clf()

    print("visualization-5 Done")
    return


def visual6(skill, tableS, cursor, sub_id, path):
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
    v6.savefig(path)
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
    plt.savefig('static/insights/vis1.png')
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

    plt.savefig('static/insights/vis4.png', bbox_inches='tight')
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
