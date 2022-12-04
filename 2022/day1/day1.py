import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    max_reindeer_calories = 0
    current_reindeer_calories = 0
    all_reindeer_totals = []

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            # New reindeer
            if len(row) == 0:
                all_reindeer_totals.append(current_reindeer_calories)
                max_reindeer_calories = max(max_reindeer_calories, current_reindeer_calories)
                current_reindeer_calories = 0
            # Existing reindeer
            else:
                current_reindeer_calories += int(row.pop())

    print("Max calories = %s" % max_reindeer_calories)

    # Day 1 part 2 - sort and pop 3
    all_reindeer_totals.sort(reverse=True)
    total_top_3 = all_reindeer_totals[0] + all_reindeer_totals[1] + all_reindeer_totals[2]

    print("Top 3 summed = %s" % total_top_3)

