import os
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class MedicalAssistantAgent(AssistantAgent):
    def __init__(self, name="medical_assistant", llm_config=None):
        system_message = "You are a medical assistant. Provide medical remedies for diseases based on the user's symptoms, age, and gender."
        super().__init__(name=name, system_message=system_message, llm_config=llm_config)

class NutritionAssistantAgent(AssistantAgent):
    def __init__(self, name="nutrition_assistant", llm_config=None):
        system_message = "You are a nutrition assistant. Provide dietary advice and meal plans based on the user's nutritional needs and goals."
        super().__init__(name=name, system_message=system_message, llm_config=llm_config)

class PsychologicalAssistantAgent(AssistantAgent):
    def __init__(self, name="psychological_assistant", llm_config=None):
        system_message = "You are a psychological assistant. Provide mental health support and coping strategies based on the user's emotional state and experiences."
        super().__init__(name=name, system_message=system_message, llm_config=llm_config)

class MedicalUserProxyAgent(UserProxyAgent):
    def __init__(self, name="user_proxy", llm_config=None):
        super().__init__(name=name, llm_config=llm_config, human_input_mode="NEVER", max_consecutive_auto_reply=0)


llm_config = {
    "model": "llama3-8b-8192",
    "api_key": "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",
    "base_url": "https://api.groq.com/openai/v1"
}

medical_assistant = MedicalAssistantAgent(llm_config=llm_config)
nutrition_assistant = NutritionAssistantAgent(llm_config=llm_config)
psychological_assistant = PsychologicalAssistantAgent(llm_config=llm_config)

medical_user_proxy = MedicalUserProxyAgent()

st.title("Medical Assistance System")

disease = st.text_input("Please enter the disease or condition:")
symptoms = st.text_area("Please describe your symptoms:")
age = st.number_input("Please enter your age:", min_value=0, max_value=150, step=1)
gender = st.radio("Please select your gender:", options=["Male", "Female", "Other"])
medical_history = st.text_area("Please enter the diseases you have been previously diagnosed with:")

if st.button("Get Assistance"):
    user_message = (
        f"Disease or condition: {disease}\n"
        f"Symptoms: {symptoms}\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Medical history: {medical_history}"
    )
    user_message_dict = {
        "Disease or condition": disease,
        "Symptoms": symptoms,
        "Age": age,
        "Gender": gender,
        "Medical history": medical_history
    }

    # st.empty()

    messages = {}
    for assistant in [medical_assistant, nutrition_assistant, psychological_assistant]:
        messages[assistant] = medical_user_proxy.initiate_chat(assistant, message=user_message)

    st.subheader("Medical Assistant Output:")
    for message in messages[medical_assistant].chat_history:
        st.write(message["content"])

    st.subheader("Nutrition Assistant Output:")
    for message in messages[nutrition_assistant].chat_history:
        st.write(message["content"])

    st.subheader("Psychological Assistant Output:")
    for message in messages[psychological_assistant].chat_history:
        st.write(message["content"])