from database import DB
import random
import matplotlib.pyplot as plt
from io import BytesIO
import base64


db = DB()

def analyse_runs(username):
    runs = db.get_runs_by_username(username)

    cur_run = [runs[0][5], runs[0][6], runs[0][7]]
    piechart1 = pie_chart_run(cur_run)
    if len(runs) != 1:
        total = [0,0,0]
        for run in runs[1:]:
            total[0] += run[5]
            total[1] += run[6]
            total[2] += run[7]
        piechart2 = pie_chart_run(total)
    else:
        piechart2 = piechart1

    scores = []
    jumps = []
    squats = []
    dodges = []

    death_by = {
        "box": 0,
        "hurdle": 0,
        "pipe": 0
                }

    for run in runs:
        scores.append(run[3])
        jumps.append(run[5])
        squats.append(run[6])
        dodges.append(run[7])

        death_by[run[4]] += 1
    
    max_frequency = max(death_by.values())
    max_keys = [key for key, value in death_by.items() if value == max_frequency]

    s = "You died most times by: "
    for i in max_keys:
        s += f" {i},"

    line_chart = generate_line_graph([scores, jumps, squats, dodges], ["Scores","Jumps", "Squats", "Dodges"], list(range(1, len(runs)+1)))



    return (piechart1, piechart2, line_chart, s[:-1])


def pie_chart_run(data):
    plt.figure(figsize=(6,6))
    labels = [f"Jumping Jacks: {data[0]}", f"Squats: {data[1]}", f"Dodges: {data[2]}"]

    plt.pie(data, labels=labels, autopct='%1.1f%%')

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return img

def generate_line_graph(datasets, labels, time_labels):
    plt.figure(figsize=(10, 5))
    
    for i, data in enumerate(datasets):
        plt.plot(time_labels, data, marker='o', label=labels[i])
    
    plt.xlabel('time')
    plt.ylabel('Values')
    plt.title('Game Metrics Over Runs')
    plt.legend()
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return img_base64


def decide_spawner(username):
    runs = db.get_runs_by_username(username)

    death_by = {
        "box": 0,
        "hurdle": 0,
        "pipe": 0
                }

    for run in runs:
        death_by[run[4]] += 1

    selected_option = random.choice(list(death_by.keys()), weights=list(death_by.values()))

    return(selected_option)