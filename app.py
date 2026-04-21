from flask import Flask, render_template, request, redirect, url_for
import pickle
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Load your trained models (adjust filenames)
# heart_model = pickle.load(open('models/heart_model.pkl', 'rb'))
# diabetes_model = pickle.load(open('models/diabetes_model.pkl', 'rb'))
# lung_model = pickle.load(open('models/lung_model.pkl', 'rb'))

SYMPTOM_LIST = [
    "Chest Pain", "Shortness of Breath", "Fatigue",
    "Frequent Urination", "Chronic Cough", "Weight Loss",
    "Fever", "Headache", "Nausea", "Dizziness",
    "Joint Pain", "Skin Rash"
]


def symptoms_to_features(selected):
    return [1 if symptom in selected else 0 for symptom in SYMPTOM_LIST]

# Simple AI advice dictionary
ADVICE = {
    "Heart Disease": [
        "Quit smoking and limit salt/fat intake.",
        "Exercise regularly and manage stress.",
        "Medications may include statins, blood thinners, or beta blockers."
    ],
    "Diabetes": [
        "Follow a balanced diet, limit refined carbs.",
        "Exercise 150 minutes per week.",
        "Monitor blood sugar and take prescribed medication/insulin."
    ],
    "Lung Disease": [
        "Stop smoking and avoid pollutants.",
        "Use inhalers or oxygen therapy if prescribed.",
        "Pulmonary rehabilitation and vaccinations are recommended."
    ],
    "No disease detected": [
        "No clear match — further checkup may be needed."
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')

        # Simple rule-based prediction
        if "Chest Pain" in selected_symptoms or "Shortness of Breath" in selected_symptoms:
            prediction = "Heart Disease"
        elif "Fatigue" in selected_symptoms and "Frequent Urination" in selected_symptoms:
            prediction = "Diabetes"
        elif "Chronic Cough" in selected_symptoms and "Weight Loss" in selected_symptoms:
            prediction = "Cancer"
        elif "Fever" in selected_symptoms and "Headache" in selected_symptoms:
            prediction = "COVID-19"
        else:
            prediction = "Unknown Condition"

        return render_template(
            'result.html',
            prediction=prediction,
            symptoms=selected_symptoms
        )

    # For GET requests, show the symptom selection page
    return render_template('symptoms.html')


@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    # Hard-coded diseases and advice
    diseases = {
        "Diabetes": "Maintain a healthy diet, monitor blood sugar, and consult an endocrinologist.",
        "Heart Disease": "Exercise regularly, avoid smoking, and schedule a cardiology checkup.",
        "Cancer": "Seek oncology consultation and follow screening guidelines.",
        "Asthma": "Use prescribed inhalers, avoid triggers, and monitor breathing.",
        "COVID-19": "Isolate if symptomatic, wear masks, and consult a physician."
    }

    if request.method == 'POST':
        selected_disease = request.form.get('disease')
        advice = diseases.get(selected_disease, "No advice available.")
        ai_advice = None

        # Optional AI advice logic
        if selected_disease == "Diabetes":
            ai_advice = "AI Suggestion: Track glucose trends with a mobile app."
        elif selected_disease == "Heart Disease":
            ai_advice = "AI Suggestion: Use a smartwatch to monitor heart rate."
        elif selected_disease == "Cancer":
            ai_advice = "AI Suggestion: AI-powered screening can help detect early signs."
        elif selected_disease == "Asthma":
            ai_advice = "AI Suggestion: Smart inhalers can log usage and predict flare-ups."
        elif selected_disease == "COVID-19":
            ai_advice = "AI Suggestion: Symptom checkers can guide when to seek care."

        return render_template(
            'diagnosis_result.html',
            disease=selected_disease,
            advice=advice,
            ai_advice=ai_advice
        )

    # For GET requests, just show the dropdown
    return render_template('diagnosis.html', diseases=diseases.keys())

@app.route('/hospitals')
def hospitals():
    hospitals = [
        {"name": "City General Hospital", "location": "Tambaram, Chennai", "phone": "+91 44 1234 5678", "services": "24/7 Emergency Services"},
        {"name": "Apollo Hospital", "location": "Guindy, Chennai", "phone": "+91 44 8765 4321", "services": "Cardiac Care, Emergency"},
        {"name": "MIOT International", "location": "Manapakkam, Chennai", "phone": "+91 44 2468 2468", "services": "Multi-specialty, 24/7"}
    ]
    return render_template("hospitals.html", hospitals=hospitals)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments_list = []

    # Handle new comment submission
    if request.method == 'POST':
        new_comment = request.form.get('comment')
        if new_comment.strip():  # avoid empty comments
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('comments.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([new_comment, timestamp])
        return redirect('/comments')  # reload page after saving

    # Load existing comments
    try:
        with open('comments.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:
                    comments_list.append({"text": row[0], "time": row[1]})
    except FileNotFoundError:
        pass  # no comments yet

    return render_template('comments.html', comments=comments_list)


if __name__ == '__main__':
    app.run(debug=True)
