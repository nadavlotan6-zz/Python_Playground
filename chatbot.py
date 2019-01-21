import re
import random
import spacy

# Load the spacy model: nlp
nlp = spacy.load('en')


sentences = [' i want to fly from boston at 838 am and arrive in denver at 1110 in the morning',
 ' what flights are available from pittsburgh to baltimore on thursday morning',
 ' what is the arrival time in san francisco for the 755 am flight leaving washington',
 ' cheapest airfare from tacoma to orlando',
 ' round trip fares from pittsburgh to philadelphia under 1000 dollars',
 ' i need a flight tomorrow from columbus to minneapolis',
 ' what kind of aircraft is used on a flight from cleveland to dallas',
 ' show me the flights from pittsburgh to los angeles on thursday',
 ' all flights from boston to washington',
 ' what kind of ground transportation is available in denver',
 ' show me the flights from dallas to san francisco',
 ' show me the flights from san diego to newark by way of houston',
 ' what is the cheapest flight from boston to bwi',
 ' all flights to baltimore after 6 pm',
 ' show me the first class fares from boston to denver',
 ' show me the ground transportation in denver',
 ' all flights from denver to pittsburgh leaving after 6 pm and before 7 pm',
 ' i need information on flights for tuesday leaving baltimore for dallas dallas to boston and boston to baltimore',
 ' please give me the flights from boston to pittsburgh on thursday of next week',
 ' i would like to fly from denver to pittsburgh on united airlines',
 ' show me the flights from san diego to newark',
 ' please list all first class flights on united from denver to baltimore',
 ' what kinds of planes are used by american airlines',
 " i'd like to have some information on a ticket from denver to pittsburgh and atlanta",
 " i'd like to book a flight from atlanta to denver",
 ' which airline serves denver pittsburgh and atlanta',
 " show me all flights from boston to pittsburgh on wednesday of next week which leave boston after 2 o'clock pm",
 ' atlanta ground transportation',
 ' i also need service from dallas to boston arriving by noon',
 ' show me the cheapest round trip fare from baltimore to dallas']

patterns = {'goodbye': re.compile(r'bye|farewell', re.UNICODE),
 			'greet': re.compile(r'hello|hi|hey', re.UNICODE),
 			'thankyou': re.compile(r'thank|thx', re.UNICODE)}

rules = {'do you remember (.*)': ['Did you think I would forget {0}',
		 "Why haven't you been able to forget {0}", 'What about {0}',
		 'Yes .. and?'], 'I want (.*)': ['What would it mean if you got {0}',
		 'Why do you want {0}', "What's stopping you from getting {0}"], 
		 'if (.*)': ["Do you really think it's likely that {0}", 'Do you wish that {0}', 
		 'What do you think about {0}', 'Really--if {0}'], 
		 'do you think (.*)': ['if {0}? Absolutely.', 'No chance']}

user_template = 'USER : {0}'
bot_template = 'BOT : {0}'

# Calculate the length of sentences
n_sentences = len(sentences)

# Calculate the dimensionality of nlp
embedding_dim = nlp.vocab.vectors_length

# Initialize the array with zeros: X
X = np.zeros((n_sentences, embedding_dim))

# Iterate over the sentences
for idx, sentence in enumerate(sentences):
    # Pass each each sentence to the nlp object to create a document
    doc = nlp(sentence)
    # Save the document's .vector attribute to the corresponding row in X
    X[idx, :] = doc.vector


# Define a function to find the intent of a message
def match_intent(message):
    matched_intent = None
    for intent, pattern in patterns.items():
        # Check if the pattern occurs in the message 
        if pattern.search(message):
            matched_intent = intent
    return matched_intent

# Define a respond function
def respond(message):
    # Call the match_intent function
    intent = match_intent(message)
    # Fall back to the default response
    key = "default"
    if intent in responses:
        key = intent
    return responses[key]


# Define a function that sends a message to the bot: send_message
def send_message(message):
    # Print user_template including the user_message
    print(user_template.format(message))
    # Get the bot's response to the message
    response = respond(message)
    # Print the bot template including the bot's response.
    print(bot_template.format(response))


# Define match_rule()
def match_rule(rules, message):
    response, phrase = "default", None
    
    # Iterate over the rules dictionary
    for pattern, responses in rules.items():
        # Create a match object
        match = re.search(pattern, message)
        if match is not None:
            # Choose a random response
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    # Return the response and phrase
    return response, phrase


# Define find_name()
def find_name(message):
    name = None
    # Create a pattern for checking if the keywords occur
    name_keyword = re.compile('name|call')
    # Create a pattern for finding capitalized words
    name_pattern = re.compile('[A-Z]{1}[a-z]*')
    if name_keyword.search(message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words)
    return name

'''
# Define respond to name
def respond(message):
    # Find the name
    name = find_name(message)
    if name is None:
        return "Hi there!"
    else:
        return "Hello, {0}!".format(name)
'''


# Define replace_pronouns()
def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        # Replace 'me' with 'you'
        return re.sub('me', 'you', message)
    if 'my' in message:
        # Replace 'my' with 'your'
        return re.sub('my', 'your', message)
    if 'your' in message:
        # Replace 'your' with 'my'
        return re.sub('your', 'my', message)
    if 'you' in message:
        # Replace 'you' with 'me'
        return re.sub('you', 'me', message)

    return message

'''
# Define respond()
def respond(message):
    # Call match_rule
    response, phrase = match_rule(rules, message)
    if '{0}' in response:
        # Replace the pronouns in the phrase
        phrase = replace_pronouns(phrase)
        # Include the phrase in the response
        response = response.format(phrase)
    return response
'''

while True:
	input_string = input('Please enter a sentenc: ')
	send_message(input_string)


# send_message("do you remember your last birthday")
