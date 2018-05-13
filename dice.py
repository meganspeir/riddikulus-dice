from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import diceware
import re
import os

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

    if body == 'riddikulus':
        dw = diceware.handle_options(['-w' 'en_securedrop'])
        passphrase = diceware.get_passphrase(dw)
        resp.message(passphrase)
    elif body == 'roll':
        resp.message('Roll 5 dice per word count you wish to return. Two word count example format: 12345 54321.')
    else:
        numbers = re.findall('\d', body)
        if any(elem in numbers for elem in blacklist) or len(numbers) % 5 > 0:
            resp.message('Value out of range. Please try again. Send `riddikulus` to get a Diceware generated passphrase. Send `roll` to use dice and send results to perform lookup.')
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
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

