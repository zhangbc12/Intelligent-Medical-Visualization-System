from flask import Flask, render_template, request
from Emergency.emergency_crawler import schedule_download
import schedule
import threading
import AED.aed_postion_processor as aed
import argparse
import QASystem.kqba as kbqa

app = Flask(__name__)

aed_processor = aed.DataProcessor("AED/data")

intent_labels = ["query_symptom", "query_cureway", "query_period", "query_rate", "query_checklist",
                 "query_department", "query_disease"]
intent_describes = ["Symptoms", "Treatments", "Treatment cycle", "Healing rate", "Check items", "Department",
                    "Possible illnesses for the symptoms", ]


@app.route('/')
def index():
    return render_template("index.html", intentions=None)

@app.route('/qa', methods=["GET", "POST"])
def qa():
    if args.qa == 1 and request.method == "POST":
        question = request.form.get("question")
        if not question or question is "":
            return render_template("qa.html")
        answer = "对不起，您的问题我不知道，我今后会努力改进的。"

        entities = handler.get_entity(question)
        if not entities:
            return render_template('qa.html', answer=answer)

        # 用户选择后精准回答
        intent_user = request.form.get("intention")
        if intent_user:
            # process intentions
            intent_before = [intent_describes[intent_labels.index(intent)] for intent in entities["intentions"]]
            entities["intentions"] = [intent_labels[intent_describes.index(intent_user)]]
            answer = handler.get_answer(entities)
            return render_template("qa.html", question=question, answer=answer, intentions=intent_before)

        # 意图模糊，提示用户选择
        elif len(entities["intentions"]) > 1:
            intent_before = [intent_describes[intent_labels.index(intent)] for intent in entities["intentions"]]
            return render_template("qa.html", question=question, intentions=intent_before)

        answer = handler.get_answer(entities)
        return render_template('qa.html', question=question, answer=answer)

    return render_template("qa.html", intentions=None)


@app.route('/emergency-map')
def map():
    return render_template("emergency-map.html")


@app.route('/aed-map', methods=["POST", "GET"])
def aed_map():
    if request.method == "POST":
        lnglat = request.form.get("lnglat")
        if lnglat :
            lng, lat = float(lnglat.split(',')[0]), float(lnglat.split(',')[1])
        else:
            return render_template("aed-map.html")
        k = 8
        closest_k = aed_processor.closest_k(lng, lat, k)

        return render_template("aed-map.html", closest_k=closest_k, lnglat=lnglat)

    return render_template("aed-map.html")


def emergency_thread(interval):
    schedule.every(interval).seconds.do(schedule_download)
    while True:
        schedule.run_pending()


def aed_thread(interval):
    schedule.every(interval).seconds.do(aed_processor.schechule_download)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Configuration')
    parser.add_argument('-q', '--qa', type=int, help='Whether to run QA System', default=0)
    parser.add_argument('-e', '--emergency', type=int, help='Cycle time for obtaining emergency map data', default=900)
    parser.add_argument('-a', '--aed', type=int, help='Cycle time for obtaining AED map data', default=1800)

    args = parser.parse_args()

    thread1 = threading.Thread(target=emergency_thread, args={args.emergency, })
    thread2 = threading.Thread(target=aed_thread, args={args.aed, })
    thread1.start()
    thread2.start()

    if args.qa == 1:
        handler = kbqa.KBQA()
    else:
        pass

    app.run()
