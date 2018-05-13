from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import diceware
import re

app = Flask(__name__)


wordlist = open('wordlist.txt', 'r')
wordlist_dict = {}
for line in wordlist:
    k, v = line.strip().split('   ')
    wordlist_dict[k.strip()] = v.strip()

wordlist.close()

blacklist = '0987abcdefghijklmnopqrstuvwxyz'


@app.route("/sms", methods=['GET', 'POST'])
def get_action():

    from_number = request.values.get('From')
    body = request.values.get('Body', None).lower()

    resp = MessagingResponse()

    if body == 'riddikulus' or 'ridiculous':
        dw = diceware.handle_options(['-w' 'en_securedrop'])
        passphrase = diceware.get_passphrase(dw)
        resp.message(passphrase)
    elif body == 'roll':
        resp.message('Roll 5 dice per word count you wish to return. Two word count example format: 12345 54321.')
    else:
        numbers = re.findall('\d', body)
        if any(elem in numbers for elem in blacklist) or len(numbers) % 5 > 0:
            resp.message('Value out of range. Please try again. Send `parseltongue` to get a Diceware generated passphrase. Send `roll` to use dice and send results to perform lookup.')
        else:
            passphrase = []
            dicerolls = []
            zipped = zip(*(iter(numbers),) * 5)
            number_strings = list(zipped)
            for nums in number_strings:
                num_strings = ''.join(map(str, nums))
                dicerolls.append(num_strings)
            for number_set in dicerolls:
                word_result = wordlist_dict[number_set]
                passphrase.append(word_result)
            complete_passphrase = ' '.join(passphrase)
            resp.message(complete_passphrase)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port='5000')


            # passphrase = []
            # dicerolls = action.split()
            # for number_set in dicerolls:
            #     word_result = wordlist_dict[number_set]
            #     passphrase.append(word_result)
            # complete_passphrase = ' '.join(passphrase)
            # resp.message(complete_passphrase)




# check for valid chars
# regex for numbers only in a string
# split numbers into fives
# total rolls = count
# word rolls = count divided by 5 - must be a whole number

# from flask import Flask, request
# from twilio.rest import TwilioRestClient
# import twilio.twiml

# import game

# account_sid = "ACXXXXXXXXXXXXXXXXX"
# auth_token = "YYYYYYYYYYYYYYYYYY"
# twilio_client = TwilioRestClient(account_sid, auth_token)

# app = Flask(__name__)

# games = {}

# @app.route("/", methods=['GET', 'POST'])
# def accept_response():
#     from_number = request.values.get('From')
#     body = request.values.get('Body')

#     try:
#         games[from_number].queue.put(body)
#     except KeyError:
#         games[from_number] = game.Game(twilio_client, from_number, "your number goes here")
#         games[from_number].start()

#     return str(twilio.twiml.Response())

# if __name__ == "__main__":
#     app.run(debug=True)
