from __future__ import annotations
from dataclasses import dataclass

import pathlib
from typing import List

with open(pathlib.Path().cwd() / 'day-07.txt', 'r') as handle:
    lines = [line.strip() for line in handle.readlines()]

# lines = ['$ cd /', '$ ls', 'dir a', '14848514 b.txt', '8504156 c.dat', 'dir d', '$ cd a', '$ ls', 'dir e', '29116 f', '2557 g', '62596 h.lst', '$ cd e', '$ ls', '584 i', '$ cd ..', '$ cd ..', '$ cd d', '$ ls', '4060174 j', '8033020 d.log', '5626152 d.ext', '7214296 k', ]

@dataclass
class FileNode:
    name:str
    size:int

class DirNode:
    name:str
    parent:DirNode
    dirs:List[DirNode]
    files:List[FileNode]

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = []
        self.files = []

    def size(self):
        return sum([d.size() for d in self.dirs]+[fd.size for fd in self.files])

    def traverse(self):
        dirlist = [self]
        for d in self.dirs:
            children = d.traverse()
            dirlist += children
        return dirlist

current_directory = None
for line in lines:
    if line.startswith('$ cd'):
        _,_,directory = line.rpartition(' ')
        if directory == '..':
            current_directory = current_directory.parent
        else:
            new_directory = DirNode(directory, current_directory)
            if current_directory is not None:
                current_directory.dirs.append(new_directory)
            current_directory = new_directory
    elif line.startswith('$ ls') or line.startswith('dir') or line == '':
        continue
    else:
        size,filename = line.split(' ')
        current_directory.files.append(FileNode(filename, int(size)))

while current_directory.name != '/':
    current_directory = current_directory.parent

directories = current_directory.traverse()
cumulative = sum([x.size() for x in directories if x.size() <= 100000])
print(cumulative)

needed = 30000000 - (70000000 - current_directory.size())
print(min([d.size() for d in directories if d.size() >= needed]))
