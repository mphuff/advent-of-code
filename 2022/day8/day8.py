import csv
import sys


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        # Parse input out
        all_data = []
        line_num = 0
        for line in reader:
            for character in range(0, len(line[0])):
                if len(all_data) <= line_num:
                    all_data.append([])
                all_data[line_num].append(line[0][character])
            line_num += 1

        print(all_data)

        # Problem 1 - visible trees
        total_visible_trees = 0
        row_pos = 0
        inner_trees_visible = []
        for row in all_data:
            line_length = len(row)
            char_pos = 0
            # First and last row is fully visible
            if row_pos == 0 or row_pos == len(all_data) - 1:
                total_visible_trees += len(row)
            else:
                for character in row:
                    current_tree = int(character)
                    # Outside edge of each row is visible
                    if char_pos == 0 or char_pos == line_length - 1:
                        total_visible_trees += 1
                    # trees are only visible if they're taller from either of 4 directions
                    else:
                        # Assume visible, set to False if we find it's hidden
                        visible_ltr = True
                        visible_rtl = True
                        visible_ttb = True
                        visible_btt = True
                        # BRUTE FORCE METHOD
                        # iterate from left to see if visible
                        for col in range(0, char_pos - 1):
                            if int(all_data[row_pos][col]) >= current_tree:
                                visible_ltr = False
                                break

                        # iterate from right to see if visible
                        for col in reversed(range(char_pos + 1, len(row))):
                            if int(all_data[row_pos][col]) >= current_tree:
                                visible_rtl = False
                                break

                        # iterate from top to see if visible
                        for row_num in range(0, row_pos - 1):
                            if int(all_data[row_num][char_pos]) >= current_tree:
                                visible_ttb = False
                                break

                        # iterate from bottom to see if visible
                        for row_num in reversed(range(row_pos + 1, len(all_data))):
                            if int(all_data[row_num][char_pos]) >= current_tree:
                                visible_btt = False
                                break

                        if visible_btt or visible_ttb or visible_ltr or visible_rtl:
                            inner_trees_visible.append("%s,%s" % (row_pos, char_pos))

                        # increase visible trees if visible from ANY direction
                        total_visible_trees += 1 if (visible_btt or visible_ttb or visible_ltr or visible_rtl) else 0

                    char_pos += 1
            row_pos += 1

        print("Inner trees visible = %s" % inner_trees_visible)
        print("Problem 1 - total visible trees = %s" % total_visible_trees)

