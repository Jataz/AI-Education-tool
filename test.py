import asyncio
from flask import Flask, request, jsonify
import openai
from concurrent.futures import ThreadPoolExecutor
import functools

app = Flask(__name__)
# Initialize OpenAI client with your API key
client = openai.OpenAI(api_key="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")

# Create a thread pool executor for running synchronous OpenAI API calls asynchronously
executor = ThreadPoolExecutor()

async def run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    func_partial = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(executor, func_partial)

async def generate_educational_content(topic):
    response = await run_in_executor(
        client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Write an educational context about {topic}."}
        ]
    )
    return response.choices[0].message.content

async def generate_question(topic):
    content = await generate_educational_content(topic)
    question_response = await run_in_executor(
        client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Based on the following educational content: '{content}' Generate a relevant question."}
        ]
    )
    question = question_response.choices[0].message.content.strip()
    return content, question

async def assess_answer(question, student_answer):
    assessment_response = await run_in_executor(
        client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": f"Question: {question}\nAnswer: {student_answer}\nIs this answer correct? (Yes/No)"}
        ]
    )
    assessment_str = assessment_response.choices[0].message.content
    return assessment_str

@app.route('/generate_content', methods=['POST'])
async def generate_content():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    content = await generate_educational_content(topic)
    return jsonify({'content': content})

@app.route('/generate_question', methods=['POST'])
async def generate_question_endpoint():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    content, question = await generate_question(topic)
    return jsonify({'content': content, 'question': question})

@app.route('/assess_answer', methods=['POST'])
async def assess_answer_endpoint():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    if not question or not answer:
        return jsonify({'error': 'Question and answer are required'}), 400
    
    assessment = await assess_answer(question, answer)
    return jsonify({'assessment': assessment})

if __name__ == '__main__':
    # Use an ASGI server like Hypercorn or Uvicorn for production
    app.run(debug=True)
