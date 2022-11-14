import sys
import os
import logging
from ofxparse import OfxParser
import codecs
import re

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if arg == "-p":
            ofx_path = sys.argv[i+1]
            if ofx_path.endswith(".ofx"):
                break
            else:
                logging.error(f"\tNot a ofx file \n\t Path: {ofx_path}")
                sys.exit()


logging.info(f"Path={ofx_path}\n")

if os.path.exists(ofx_path):
    # Read in the file
    with open(ofx_path, 'r') as file:
        file_data = file.read()

    with codecs.open(ofx_path, 'r') as file:
        ofx = OfxParser.parse(file)

        account = ofx.account
        statement = account.statement
        for transaction in statement.transactions:
            logging.info(f'Transaction type: {transaction.type}.\n')
            logging.info(f'Transaction amount: {transaction.amount}.\n')
            typeTemp = transaction.type
            if typeTemp.lower() == 'payment':
                if transaction.amount >= 0:
                    new_amount = -1 * transaction.amount
                    logging.info(f'New transaction amount: {new_amount}.\n')
                    logging.info(f'transaction.date: {transaction.date}.\n')

                    # TODO add regex between </TRNAMT> and <FITID>
                    #  like r'([a-z|A-Z|0-9|<|>|\|/|\n| |\t|á|ê|é|â|ã]*)' ?
                    # Replace the target string
                    regex = f'(<TRNAMT>' + r'[\n| |\t]*' + f'{transaction.amount}' + r'[\n| |\t]*' + '</TRNAMT>' + \
                            r'[\n| |\t]*' + f'<FITID>' + r'[\n| |\t]*' + \
                            f'{transaction.id}' + r'[\n| |\t]*' + '</FITID>)'

                    new_string = f'<TRNAMT>{new_amount}</TRNAMT>\n' \
                                 f'<FITID>{transaction.id}</FITID>'

                    patter_found_list = re.findall(regex, file_data)
                    if len(patter_found_list) == 0:
                        logging.error("Editing file didn't work")
                        logging.error(patter_found_list[0])
                    logging.info(patter_found_list[0])
                    file_data = file_data.replace(patter_found_list[0], new_string)

    # Write the file out again
    # Removing the .ofx
    new_filename = f'{ofx_path[:len(ofx_path)-4]}FIXED.ofx'
    with open(new_filename, 'w') as file:
        file.write(file_data)

