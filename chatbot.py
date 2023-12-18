from openai import OpenAI
from time import sleep
from os import environ

client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))
assistant_id = environ.get('ASSISTANT_ID')

class Chatbot():
    def __init__(self) -> None:
        self.thread = client.beta.threads.create()

    # send message, get bot response
    def process_message(self, user_input):
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=assistant_id
        )

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            if run.status != "queued" and run.status != "in_progress":
                break
            sleep(1)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages.data[0].content[0].text.value
        else:
            raise Exception("Error: did not receive Completed status")