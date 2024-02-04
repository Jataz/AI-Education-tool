import openai

openai.api_key = 'YOUR_API_KEY'  # Replace with your OpenAI API key

def generate_content(topic):
    prompt = f"Topic: {topic}\n\n"
    prompt += "Context:"
    response = openai.Completion.create(
        engine='text-davinci-003',  # Use the GPT-3.5 engine
        prompt=prompt,
        max_tokens=200,  # Adjust the maximum number of tokens as needed
        n=1,  # Generate a single completion
        stop=None,  # Let the model determine the completion automatically
        temperature=0.7,  # Adjust the temperature for more or less randomness in the output
        top_p=1.0,  # Adjust the top_p value for more controlled output
    )
    generated_content = response.choices[0].text.strip()
    return generated_content