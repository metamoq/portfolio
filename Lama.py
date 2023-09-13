import gradio as gr
import time
from ctransformers import AutoModelForCausalLM

def load_llm():
    llm = AutoModelForCausalLM.from_pretrained(
        "codellama-13b-instruct.Q4_K_M.gguf",
        model_type = "llama",
        max_new_tokens = 2048,
        repetition_penalty = 1.13,
        temperature = 0.7
    )
    return llm

def llm_request(message, chat_history):
    llm = load_llm()
    response = llm(
        message
    )
    output_texts = response
    return output_texts

title = "CodeLlama 13B GGUF"

examples = [
    "Напиши мне, что такое эмоциональный интеллект.",
    "Какие сильные стороны самоанализа и саморазвития.",
    "Что такое самостоятельное критическое мышление?"
    ]

gr.ChatInterface(
    fn=llm_request,
    title=title,
    examples=examples
).launch(share=True)

