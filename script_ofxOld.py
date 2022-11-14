import sys
import os
import logging
from ofxparse import OfxParser
import codecs

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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
    with codecs.open(ofx_path, 'r+') as file:
        ofx = OfxParser.parse(file)

        account = ofx.account
        statement = account.statement
        for transaction in statement.transactions:
            logging.info(f'Transaction type: {transaction.type}.\n')
            logging.info(f'Transaction amount: {transaction.amount}.\n')
            if transaction.type.lower() == 'payment':
                if transaction.amount >= 0:
                    new_amount = -1 * transaction.amount
                    logging.info(f'New transaction amount: {new_amount}.\n')
                    file.findal
                    print(file.tell())
                    print(f'f:{file.readline()}')

                    transaction.amount = new_amount


