from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class MedicalAssistantAgent(AssistantAgent):
    def __init__(self, name="medical_assistant", llm_config=None):
        system_message = "You are a medical assistant. Provide medical remedies for diseases based on the user's symptoms, age, and gender."
        super().__init__(name=name, system_message=system_message, llm_config=llm_config)

class MedicalUserProxyAgent(UserProxyAgent):
    def __init__(self, name="user_proxy", llm_config=None):
        super().__init__(name=name, llm_config=llm_config)

llm_config = {
    "model": "llama3-8b-8192",                      # Replace with the appropriate model
    "api_key": "",                                  # Replace with your API key
    "base_url": "https://api.groq.com/openai/v1"    # Replace with your llm base_url (if applicable)
}

assistant = MedicalAssistantAgent(llm_config=llm_config)
user_proxy = MedicalUserProxyAgent()

group_chat = GroupChat(agents=[assistant, user_proxy], messages=[], max_round=5)
group_chat_manager = GroupChatManager(groupchat=group_chat)

def initiate_medical_query():
    disease = input("Please enter the disease or condition: ")
    symptoms = input("Please describe your symptoms: ")
    age = input("Please enter your age: ")
    gender = input("Please enter your gender: ")
    medical_history = input("Please enter the diseases you have been previously diagnosed with")

    user_message = (
        f"Find a remedy for {disease}.\n"
        f"Symptoms: {symptoms}\n"
        f"Age: {age}\n"
        f"Gender: {gender}"
    )

    user_proxy.initiate_chat(assistant, message=user_message)
    group_chat_manager.run_chat()

if __name__ == "__main__":
    initiate_medical_query()