import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class GroupChatManager:
    def __init__(self, groupchat):
        self.groupchat = groupchat

    def run_chat(self):
        try:
            self.groupchat.start()
            while not self.groupchat.is_finished():
                self.groupchat.step()
        except IndexError as e:
            if len(self.groupchat.messages) == 0:
                print("No messages have been exchanged yet.")
            else:
                print("An error occurred while accessing messages:", e)


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

GROQAI_API_KEY = os.environ.get("GROQAI_API_KEY")
llm_config = {
    "model": "llama3-8b-8192",
    "api_key": GROQAI_API_KEY,
    "base_url": "https://api.groq.com/openai/v1"
}

medical_assistant = MedicalAssistantAgent(llm_config=llm_config)
nutrition_assistant = NutritionAssistantAgent(llm_config=llm_config)
psychological_assistant = PsychologicalAssistantAgent(llm_config=llm_config)

medical_user_proxy = MedicalUserProxyAgent()

group_chat = GroupChat(agents=[medical_assistant, nutrition_assistant, psychological_assistant, 
                               medical_user_proxy], messages=[], max_round=5)

def initiate_medical_query():
    disease = input("Please enter the disease or condition: ")
    symptoms = input("Please describe your symptoms: ")
    age = input("Please enter your age: ")
    gender = input("Please enter your gender: ")
    medical_history = input("Please enter the diseases you have been previously diagnosed with: ")

    user_message = (
        f"Disease or condition: {disease}\n"
        f"Symptoms: {symptoms}\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Medical history: {medical_history}"
    )

    for assistant in [medical_assistant, nutrition_assistant, psychological_assistant]:
        medical_user_proxy.initiate_chat(assistant, message=user_message)
    
    group_chat_manager = GroupChatManager(groupchat=group_chat)

    group_chat_manager.run_chat()

if __name__ == "__main__":
    initiate_medical_query()
