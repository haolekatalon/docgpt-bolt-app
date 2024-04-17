import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from rag_chain.chain import chain

load_dotenv()
id_pattern = "<@U[\w\d]+>"



# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def reformat(text):
    """Reformat answers from the model to be more presentable in Slack output"""
    
    # replace the double asterisks with single asterisk for bold
    
    bold_pattern = r'\s\*\*(.*?)\*\*\s'
    
    def replace_asterisks(match):
        return ' *' + match.group(1) + '* '  # Replace with one asterisk before and after the captured text
    
    text = re.sub(bold_pattern, replace_asterisks, text)
    
    # reformat the URL markup
    
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # Function to replace Markdown links with <link|link text> pattern
    def replace_markdown_links(match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f'<{link_url}|{link_text}>'
    
    text = re.sub(link_pattern, replace_markdown_links, text)
    
    return text
    

######### Event handlers

@app.event("app_mention")
def event_test(event, say):
    text = re.sub(id_pattern, '', event["text"]) # remove the bot id
    answer = "\n" + chain.invoke({
        "question": text,
        "chat_history": []
        })
    
    formatted = reformat(answer)
    
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": formatted},
            }
        ],
        text=f"Hey there <@{event['user']}>!"
    )
    
@app.event("message")
def handle_message_events(body, logger):
    pass

@app.command("/askdocs")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    text = command['text']
    answer = "\n" + chain.invoke({
        "question": text,
        "chat_history": []
        })
    formatted = reformat(answer)
    respond(f"{formatted}")

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()