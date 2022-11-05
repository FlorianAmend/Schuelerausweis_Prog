import random
bid_write = open('numBid.txt', 'a')
bid_read = open('numBid.txt', 'r')

#Funktion for creating new numbers to the 'numBid.txt' file
def create_bid_num():
    count = 0
    while(count != 50000):
        a = random.randint(700000000000,999999999999)
        count += 1
        bid_write.write(str(a) + "\n")

bid_num = []


class BidCreate:
    def __init__(self):
        self.get_bid()
        self.del_line_bid()

    def get_bid(self):
        with open('numBid.txt', 'r') as bid:
            bid_unconv = bid.readlines(5)
            for element in bid_unconv:
                bid_num.append(int(element.strip()))


    def del_line_bid(self):
        lines = []

        with open('numBid.txt', 'r') as fp:
            lines = fp.readlines()


        with open('numBid.txt', 'w') as fp:
            for number, line in enumerate(lines):
                if number not in [0]:
                    fp.write(line)





BidCreate()
print(bid_num)
