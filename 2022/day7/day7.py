import csv
import sys
from enum import Enum


class DirSizeComparison(Enum):
    GT = 1
    LT = 2

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
        self.total_dir_size = 0

    def add_child(self, child_entry):
        if child_entry.filename not in self.children:
            child_entry.parent_directory = self
            self.children[child_entry.filename] = child_entry

    def get_size_for_dir(self):
        if self.entry_type == DirectoryEntryType.FILE:
            return None
        if self.total_dir_size == 0:
            __total_size = 0
            for child in self.children.values():
                if child.entry_type == DirectoryEntryType.DIR:
                    __total_size += child.get_size_for_dir()
                else:
                    __total_size += child.size
            self.total_dir_size = __total_size

        return self.total_dir_size
        # return __total_size

    def get_dir(self, dir_name):
        return self.children[dir_name]

    def __str__(self):
        return "[%s - %s, size = %s, total_dir_size = %s, children = %s]" % \
               (self.entry_type, self.filename, self.size, self.total_dir_size, len(self.children))


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
                self.__current_directory.add_child(DirectoryEntry(__all_parts[1], DirectoryEntryType.DIR))
            else:
                self.__current_directory.add_child(DirectoryEntry(__all_parts[1], DirectoryEntryType.FILE,
                                                                  size=int(__all_parts[0])))

    # return directories AND their corresponding sizes for all directories
    # that exceed size_to_find total
    def find_dirs_with_size(self, size_to_find, directory=None, size_comparison_op=DirSizeComparison.LT):
        all_dirs = []
        traverse_directory = self.__root_directory if directory is None else directory
        for child in traverse_directory.children.values():
            if child.entry_type == DirectoryEntryType.DIR and (
                    (size_comparison_op == DirSizeComparison.LT and child.get_size_for_dir() <= size_to_find) or
                    (size_comparison_op == DirSizeComparison.GT and child.get_size_for_dir() >= size_to_find)):
                all_dirs.append(child)
            child_qualifying_dirs = self.find_dirs_with_size(size_to_find, child, size_comparison_op)
            for qualified_dir in child_qualifying_dirs:
                all_dirs.append(qualified_dir)
        return all_dirs

    def total_root_folder_size(self):
        return self.__root_directory.get_size_for_dir()

    def find_directory_to_delete(self):
        root_dir_size = self.total_root_folder_size()
        total_space_available = 70000000
        space_required = 30000000

        current_unused_space = total_space_available - root_dir_size
        min_size_for_deletion = space_required - current_unused_space

        smallest_dir_to_delete = None
        all_dirs_with_size = self.find_dirs_with_size(min_size_for_deletion,
                                                      size_comparison_op=DirSizeComparison.GT)
        for deletion_candidate in all_dirs_with_size:
            if smallest_dir_to_delete is None or \
                    deletion_candidate.get_size_for_dir() <= smallest_dir_to_delete.get_size_for_dir():
                smallest_dir_to_delete = deletion_candidate

        return smallest_dir_to_delete


if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception("No file provided as a parameter")

    with open(sys.argv.pop()) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')

        all_lines = []
        for line in reader:
            all_lines.append(line)

        cp = CommandProcessor(all_lines)
        print("TOTAL SIZE = %s" % cp.total_root_folder_size())

        # Part 1 - total them all up
        total_size = 0
        for sub_directory in cp.find_dirs_with_size(100000):
            total_size += sub_directory.get_size_for_dir()
        print("Part 1 - total_size = %s" % total_size)

        # Part 2 - find directory to delete
        print("Part 2 - Directory to delete = %s" % cp.find_directory_to_delete())
