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

api_key = os.environ.get("API_KEY")
llm_config = {
    "model": "llama3-8b-8192",
    "api_key": api_key,
    "base_url": "https://api.groq.com/openai/v1"
}

medical_assistant = MedicalAssistantAgent(llm_config=llm_config)
nutrition_assistant = NutritionAssistantAgent(llm_config=llm_config)
psychological_assistant = PsychologicalAssistantAgent(llm_config=llm_config)

medical_user_proxy = MedicalUserProxyAgent()

st.title("Medical Assistance System")

# Input fields
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

    # Clear previous outputs
    st.empty()

    # Run the medical query
    for assistant in [medical_assistant, nutrition_assistant, psychological_assistant]:
        medical_user_proxy.initiate_chat(assistant, message=user_message)
    group_chat = GroupChat(agents=[medical_assistant, nutrition_assistant, psychological_assistant, medical_user_proxy], messages=None, max_round=0)
    group_chat_manager = GroupChatManager(groupchat=group_chat)
    try:
        group_chat_manager.run_chat()
    except:
        print("")
    finally:
        # Display responses
        for agent in group_chat.agents:
            if isinstance(agent, AssistantAgent):  
                # Find the latest message from the agent
                agent_messages = [message for message in group_chat.messages if message["sender"] == agent.name]
                latest_response = agent_messages[-1]["content"] if agent_messages else "No response"
                
                st.subheader(f"{agent.name.replace('_', ' ').title()} Response:")
                st.write(latest_response)

