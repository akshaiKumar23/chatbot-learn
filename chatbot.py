# chatbot.py
from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import json

app = Flask(__name__)


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    knowledge_base = load_knowledge_base("knowledge_base.json")
    user_input = request.form.get("user_input")

    if user_input.lower() == "quit":
        return jsonify({"response": "Goodbye!"})

    best_match = find_best_match(
        user_input, [q["question"] for q in knowledge_base["questions"]]
    )

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({"response": answer})
    else:
        return jsonify({"response": "I don't know the answer. Can you teach me?"})


if __name__ == "__main__":
    app.run(debug=True)