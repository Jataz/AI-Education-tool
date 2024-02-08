from flask import Flask, render_template, request, jsonify

from flask_executor import Executor
import openai

import asyncio

client = openai.OpenAI(api_key = "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")

app = Flask(__name__)
executor = Executor(app)


async def generate_educational_content(topic):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Make sure this is the correct model
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Write an educational context about {topic}."}
        ]
    )
    return response.choices[0].message.content

async def generate_question(topic):
    content = await generate_educational_content(topic)  # Await the coroutine here
    question_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Based on the following educational content: '{content}' Generate a relevant question."}
        ]
    )
    question = question_response.choices[0].message.content.strip()
    return content, question


async def assess_answer(question, student_answer):
    assessment_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Question: {question}\nAnswer: {student_answer}\nIs this answer correct? (Yes/No)"}
        ]
    )
    assessment_str = assessment_response.choices[0].message.content
    
    return assessment_str

def run_async(func):
    def wrapper(*args, **kwargs):
        future = executor.submit(asyncio.run, func(*args, **kwargs))
        return future.result()
    return wrapper

# Flask routes remain the same

def run_async(func):
    def wrapper(*args, **kwargs):
        future = executor.submit(asyncio.run, func(*args, **kwargs))
        return future.result()
    return wrapper

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    content = run_async(generate_educational_content)(topic)
    return jsonify({'content': content})

@app.route('/generate_question', methods=['POST'])
async def generate_question_endpoint():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    content, question = await generate_question(topic)
    
    # Convert content and question to strings
    content_str = str(content)
    question_str = str(question)

    return jsonify({'content': content_str, 'question': question_str})


@app.route('/assess_answer', methods=['POST'])
async def assess_answer_endpoint():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    if not question or not answer:
        return jsonify({'error': 'Question and answer are required'}), 400
    
    # Generate the assessment using the question and answer
    assessment_str = await assess_answer(question, answer)

    
    return jsonify({'assessment': assessment_str})

if __name__ == '__main__':
     asyncio.run(app.run(debug=True))
