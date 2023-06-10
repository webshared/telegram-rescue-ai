import config
import duckdb
import openai
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

openai.api_key = config.OPENAI_KEY
api_id = config.API_ID
api_hash = config.API_HASH

client = TelegramClient(config.SESSION_NAME, api_id, api_hash)
client.start()

channels = config.CHANNELS
send_report_to_channel = config.SEND_TO_TG_CHANNEL
send_report_to_username = config.SEND_TO_TG_USERNAME
verbose = config.VERBOSE

# Set up DuckDB
db = duckdb.connect('processed_messages.db')
db.execute('CREATE TABLE IF NOT EXISTS processed_messages (message_id VARCHAR PRIMARY KEY)')

def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=config.OPENAI_MODEL,
            messages=[
                    {"role": "system", "content": """
                        You are a rescue chat bot which can detect evacuation requests and mission people announcements in the telegram Chat History and provide concise digest for rescuers, citing all the details.
                        You provide the digest in russian langugage for rescuers using this format for each request: location, town or village, address | situation | names, addresses, comments, phone numbers, and all other useful information | link to the User Message URL
                        You are as detailed as possible, do not skip any information provided. You never add any excessive details which are not essential.
                    """},
                    {"role": "user", "content": prompt}
                ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except openai.InvalidRequestError as e:
        print('OpenAI Error', str(e))
        return None

async def get_messages(client, channel_username):
    if verbose:
        print('channel_username', channel_username)

    # Get the Channel entity from the username
    channel = await client.get_entity(channel_username)

    all_messages = ''  # This will hold all the message texts
    all_ids = []  # This will hold all the message IDs

    # Get the last 10 messages from the channel
    messages = await client(GetHistoryRequest(
        peer=channel,
        limit=10,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    all_messages = ''

    # Add each message's text to the all_messages string,
    # and its ID to the all_ids list
    for message in messages.messages:
        # Create a unique ID from the channel name and message ID
        unique_id = f'{channel_username}-{message.id}'

        # Skip already processed messages
        result = db.execute(f'SELECT * FROM processed_messages WHERE message_id = \'{unique_id}\'').fetchall()
        if result:
            continue

        # all_messages += f'Date: {message.date}\nUser message: """{message.message}\n"""\n\n'
        all_messages += f"---\n"
        all_messages += f"User message URL: https://t.me/{channel_username}/{message.id}\n"
        all_messages += f'User message: """{message.message}\n"""\n\n'

        all_ids.append(unique_id)
        # print(f'Message ID: {message.id}')
        # print(f'From ID: {message.from_id}')
        # print(f'To ID: {message.to_id}')
        # print(f'Date: {message.date}')
        # print(f'Message: {message.message}')
        # print(f'Out: {message.out}')
        # print(f'Mentioned: {message.mentioned}')
        # print(f'Media: {message.media}')
        # print(f'Reply Markup: {message.reply_markup}')
        # print('------')

    return all_messages, all_ids  # Return the collected messages and IDs

async def send_message_to_channel(client, channel_username, message):
    channel = await client.get_entity(channel_username)
    await client.send_message(entity=channel, message=message)

async def send_message_to_user(client, user_id, message):
    user = await client.get_entity(user_id)
    await client.send_message(entity=user, message=message)

for channel_username in channels:
    all_messages, all_ids = client.loop.run_until_complete(get_messages(client, channel_username))
    if all_ids:
        prompt = f'Chat History:\n{all_messages}\n\nConcise digest for Russian speaking rescue boat operators, to post into Telegram channel:'
        if verbose:
            print(prompt)
        report = generate_text(prompt)
        if verbose:
            print(report)

        if report is not None:
            if report.startswith('Sorry, I couldn'):
                print("Report doesn't contain any relevant information.")
            else:
                if send_report_to_channel:
                    client.loop.run_until_complete(send_message_to_channel(client, send_report_to_channel, report))
                if send_report_to_username:
                    client.loop.run_until_complete(send_message_to_user(client, send_report_to_username, report))

        # Mark all processed messages
        for unique_id in all_ids:
            db.execute(f'INSERT INTO processed_messages (message_id) VALUES (\'{unique_id}\')')
    else:
        print('No new messages.')
