from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import json
import os

app = Flask(__name__)
CORS(app)

def load_context():
    context = {}
    try:
        with open('logs/incident_log.json') as f:
            context['incidents'] = json.load(f)
    except Exception:
        context['incidents'] = []
    try:
        with open('badges/compliance_status.json') as f:
            context['badges'] = json.load(f)
    except Exception:
        context['badges'] = {}
    return context

@app.route('/api/trust_qa', methods=['POST'])
def trust_qa():
    data = request.json
    question = data.get('question', '')
    context = load_context()
    badges = context['badges']
    incidents = context['incidents']
    context_str = f"Compliance Badges: {json.dumps(badges)}\nIncident Log: {json.dumps(incidents[-10:])}\n"

    prompt = (
        "You are a compliance assistant AI. "
        "Answer the question based only on the compliance badges and incident log provided. "
        "If the question asks about controls, certifications, incidents, drills, or compliance status, answer factually based on the provided data. "
        f"---\nEVIDENCE:\n{context_str}\n---\nQUESTION: {question}\nANSWER:"
    )

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ← Cheaper, works with most free-tier accounts!
            messages=[{"role": "system", "content": prompt}],
            max_tokens=256,
            temperature=0.0,
        )
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = f"(Error: {str(e)})"
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(port=5050)


