from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load DialoGPT
dialoggpt = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Custom training data (you can replace this with your own data)
custom_data = [
    ("Hello", "Hi there! How can I help you today?"),
    # Add more custom data here
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]

    # Use custom data for training
    for example in custom_data:
        dialoggpt.train(
            [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": example[0]},
                {"role": "assistant", "content": example[1]},
            ]
        )

    # Generate a response
    response = dialoggpt(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ]
    )[0]["generated_responses"][0]

    return jsonify({"response": response["content"]})


if __name__ == "__main__":
    app.run(debug=True)
