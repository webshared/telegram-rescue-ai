# You must get your own api_id and api_hash from https://my.telegram.org, under API Development.
API_ID = '1432246'
API_HASH = '97439dea6e7b38ec87f17be77812102d'

# Telegram client session name
# No need to change that
SESSION_NAME = 'my_session'

# Where to send reports to?
SEND_TO_TG_CHANNEL = 'KhersonEvacuation'
SEND_TO_TG_USERNAME = None # 'RipleyProject'

# Taken from https://platform.openai.com/account/api-keys
OPENAI_KEY = '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'
OPENAI_MODEL = 'gpt-3.5-turbo'

# List of telegram hannels to process
CHANNELS = [
    # https://t.me/OLESHKYevakuation
    'OLESHKYevakuation',
    # '@helpnova',
]

# Print the prompt and summary?
VERBOSE = True