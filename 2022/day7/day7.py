import csv
import sys
from enum import Enum


class DirectoryEntryType(Enum):
    FILE = 1
    DIR = 2

    def __str__(self):
        return "[%s]" % self.name


class DirectoryEntry:
    def __init__(self, filename, entry_type, parent_directory=None, size=None):
        self.filename = filename
        self.size = size
        self.entry_type = entry_type
        self.parent_directory = parent_directory
        self.children = {}

    def add_child(self, child_entry):
        if child_entry.filename not in self.children:
            self.children[child_entry.filename] = child_entry

    def get_size_for_dir(self):
        if self.entry_type == DirectoryEntryType.FILE:
            return None
        total_size = 0
        for child in self.children.values():
            if child.entry_type == DirectoryEntryType.DIR:
                total_size += child.get_size_for_dir()
            else:
                total_size += child.size
        return total_size

    def get_dir(self, dir_name):
        return self.children[dir_name]

    def calc_directory_path(self):
        if self.parent_directory is None:
            return self.filename
        else:
            return "%s/%s" % (self.parent_directory.calc_directory_path(), self.filename)

    def __str__(self):
        return "[%s - %s, size = %s, children = %s]" % \
               (self.entry_type, self.filename, self.size, len(self.children))


class CommandProcessor:
    # Track current directory as we're processing the input
    __current_directory = None
    # Track current command as we're processing the input
    __current_command = ""
    # Identify the root directory and track that
    __root_directory = None

    def __init__(self, lines):
        self.lines = lines
        self.build_dir_structure()

    def build_dir_structure(self):
        for __line in self.lines:
            self.__process_command(__line)
        return

    # Assume first line "changes directory" to /
    def __process_command(self, __all_parts):
        if __all_parts[0] == "$":
            # ls command, no explicit action to take
            self.__current_command = __all_parts[1]
            if __all_parts[1] == "cd":
                if __all_parts[2] == '..':
                    self.__current_directory = self.__current_directory.parent_directory
                elif __all_parts[2] == '/':
                    if self.__root_directory is None:
                        self.__root_directory = DirectoryEntry('/', DirectoryEntryType.DIR)
                        self.__current_directory = self.__root_directory
                else:
                    self.__current_directory = self.__current_directory.get_dir(__all_parts[2])
        else:
            if __all_parts[0] == "dir":
                self.__current_directory.add_child(DirectoryEntry(__all_parts[1], DirectoryEntryType.DIR,
                                                                  parent_directory=self.__current_directory))
            else:
                self.__current_directory.add_child(DirectoryEntry(__all_parts[1], DirectoryEntryType.FILE,
                                                                  parent_directory=self.__current_directory,
                                                                  size=int(__all_parts[0])))

    # return directories AND their corresponding sizes for all directories
    # that exceed size_to_find total
    def find_dirs_with_max_size(self, size_to_find, directory=None):
        all_dirs = []
        traverse_directory = self.__root_directory if directory is None else directory
        for child in traverse_directory.children.values():
            if child.entry_type == DirectoryEntryType.DIR and child.get_size_for_dir() <= size_to_find:
                all_dirs.append(child)
            child_qualifying_dirs = self.find_dirs_with_max_size(size_to_find, child)
            for qualified_dir in child_qualifying_dirs:
                all_dirs.append(qualified_dir)
        return all_dirs

    def total_size(self):
        return self.__root_directory.get_size_for_dir()


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        all_lines = []
        for line in reader:
            all_lines.append(line)

        cp = CommandProcessor(all_lines)
        print("TOTAL SIZE = %s" % cp.total_size())

        # Part 1 - total them all up
        total_size = 0
        for sub_directory in cp.find_dirs_with_max_size(100000):
            print("%s //// %s" % (sub_directory, sub_directory.get_size_for_dir()))
            total_size += sub_directory.get_size_for_dir()
        print(total_size)

