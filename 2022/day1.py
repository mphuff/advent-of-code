import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    max_reindeer_calories = 0
    current_reindeer_calories = 0
    total_unique_reindeer = 0
    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # New reindeer
            if len(row) == 0:
                max_reindeer_calories = max(max_reindeer_calories, current_reindeer_calories)
                current_reindeer_calories = 0
                total_unique_reindeer += 1
            # Existing reindeer
            else:
                current_reindeer_calories += int(row.pop())

    print("Max calories = %s" % max_reindeer_calories)
    print("Total evaluated reindeer = %s" % total_unique_reindeer)
