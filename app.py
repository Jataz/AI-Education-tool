from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, world!"

@app.route('/submit_topic', methods=['POST'])
def submit_topic():
    topic = request.form['topic']  # Assuming the student submits the topic via a form field
    # Process the topic and generate the context, question, and answer assessment
    # ...
    return "Topic submitted successfully"

@app.route('/submit_topic', methods=['POST'])
def submit_topic():
    topic = request.json['topic']
    # Process the topic and generate the context, question, and answer assessment
    # ...
    return jsonify({"message": "Topic submitted successfully"})

if __name__ == '__main__':
    app.run()