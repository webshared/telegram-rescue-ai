# You must get your own api_id and api_hash from https://my.telegram.org, under API Development.
API_ID = 'YOUR_APP_ID'
API_HASH = 'YOUR_APP_HASH'

# Telegram client session name
# No need to change that
SESSION_NAME = 'my_session'

# Where to send reports to?
SEND_TO_TG_CHANNEL = 'KhersonEvacuation'
SEND_TO_TG_USERNAME = None

# Taken from https://platform.openai.com/account/api-keys
OPENAI_KEY = 'YOUR_OPENAI_API_KEY'
OPENAI_MODEL = 'gpt-3.5-turbo'

# List of telegram hannels to process
CHANNELS = [
    # https://t.me/OLESHKYevakuation
    'OLESHKYevakuation',
    # '@helpnova',
]

# Print the prompt and summary?
VERBOSE = True
