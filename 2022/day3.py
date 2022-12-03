import csv
import sys

def calculate_priority(item):
    # a-z = 1-26
    # A-Z = 27-52

    ordinal = ord(item)
    # capital letter
    if ordinal < 96:
        return ordinal - 64 + 26
    else:
        return ordinal - 96


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    total_priority = 0;

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            total_items = list(row[0])
            assert len(total_items) % 2 == 0

            sack1 = total_items[:int((len(total_items)/2))]
            sack2 = total_items[int(len(total_items) / 2):]

            assert len(sack1) == len(sack2)

            shared = set([x for x in sack1 if x in sack2]).pop()
            priority = calculate_priority(shared)

            total_priority += priority

            print("%s / %s" % (shared, priority))

        print(total_priority)
