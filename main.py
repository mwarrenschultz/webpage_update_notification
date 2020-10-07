from bs4 import BeautifulSoup
from pathlib import Path
import pickle
import sys

sys.path.append('/home/mschultz/code/log-data-scraping/requester')
from requester import Requester
from twilio.rest import Client


def send_message(msg):
    """
    Function sends text message to my cell phone using Twilio API
    :param msg: str
    :return: MessageInstance
    """
    message = client.messages.create(to=my_phone, from_=twilio_number, body=msg)
    return message


if __name__ == '__main__':

    # credentials kept in file outside of shared directory.
    # Formatted as account sid and authorization token separated by colon (':')
    with open('/home/mschultz/Documents/twilio_credentials.txt', 'r') as infile:
        account_sid, auth_token = infile.readline().strip().split(':')

    client = Client(account_sid, auth_token)

    my_phone = "+18476820777"
    twilio_number = "+13126638594"

    savedoc = Path('mem.dat')
    url = 'https://shop.nwnprod.com/'

    rsession = Requester()
    r = rsession.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    dat = soup.find('div', {'data-section-id': 'featured-collection'})

    if savedoc.exists():
        with open(savedoc, 'rb') as infile:
            prevtext = pickle.load(infile)
        if prevtext != dat.text:
            message = send_message('NWN! Website has been updated')
            print(message.status)

    with open(savedoc, 'wb') as outfile:
        pickle.dump(dat.text, outfile)
