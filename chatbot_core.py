# chatbot_core.py

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load pre-trained DialoGPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Track conversation history
chat_history_ids = None

def get_bot_response(user_input, history_ids=None):
    global chat_history_ids
    
    # Encode user input and add to chat history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Append new input to history
    bot_input_ids = torch.cat([history_ids, new_input_ids], dim=-1) if history_ids is not None else new_input_ids
    
    # Generate response from model
    output_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the last output token (only bot response)
    response = tokenizer.decode(output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return response, output_ids
