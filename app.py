import os
import gradio as gr
from huggingface_hub import InferenceClient

# Aap Hugging Face ka koi bhi achha text model use kar sakte hain
# Jaise: "meta-llama/Meta-Llama-3-8B-Instruct" ya "mistralai/Mistral-7B-Instruct-v0.2"
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3")

# System prompt jo model ko batayega ki use PhyFarm ka AI assistant banna hai
SYSTEM_PROMPT = """
You are the PhyFarm AI Chatbot, a helpful, friendly, and expert agricultural assistant.
Your goal is to help farmers understand PhyFarm's smart agriculture ecosystem, IoT devices, hydroponics automation, and general farming practices.
Provide clear, easy-to-understand, and practical advice in simple language. You can respond in a mix of Hindi and English if requested.
"""

def respond(message, chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Purani chat history ko formatting me add karna
    for user_msg, bot_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
        
    messages.append({"role": "user", "content": message})
    
    response = ""
    
    # Hugging Face API se response stream karna
    try:
        for msg in client.chat_completion(messages, max_tokens=512, stream=True):
            token = msg.choices[0].delta.content
            if token:
                response += token
                yield response
    except Exception as e:
        yield f"Sorry, I encountered an error: {str(e)}. Please check your API connection."

# Gradio UI Design
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌾 PhyFarm AI Chatbot 🤖")
    gr.Markdown("Welcome! Ask me anything about PhyFarm's smart agricultural services or farming guidance.")
    
    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Ask about PhyFarm automation, crop health, or sensor data...", label="Your Question")
    clear = gr.ClearButton([msg, chatbot])

    def user(user_message, history):
        return "", history + [[user_message, ""]]

    def bot(history):
        user_message = history[-1][0]
        # Purani history bina current message ke pass karni hai
        chat_history = history[:-1] 
        
        # Generator se live text update hoga
        for updated_response in respond(user_message, chat_history):
            history[-1][1] = updated_response
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

if __name__ == "__main__":
    demo.launch()
