from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

class Chat(Agent):
    def __init__(self):
        self.chat_agent = Agent(
            "google-gla:gemini-2.5-flash",
            system_prompt="you are a impersonator bot that impersonates the person based on the provided resume and coverletters, you will answer questions as if you are that person."
        )

        self.result= None
    
    def chat(self, prompt:str)-> dict:
        message_history = self.result.all_messages() if self.result else None

        self.result = self.chat_agent.run_sync(prompt, message_history=message_history)

        return {"user": prompt, "bot": self.result.output}
    
if __name__ == "__main__":
    bot = Chat()
    result = bot.chat("Hello there!")
    print(result)

    result = bot.chat("General Kenobi!")
    print(result)