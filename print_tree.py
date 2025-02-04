import os  
  
def tree(directory, prefix=''):  
    """Recursively prints a directory tree structure."""  
    # Get a sorted list of the entries in the directory  
    entries = sorted(os.listdir(directory))  
    entries_count = len(entries)  
    for index, entry in enumerate(entries):  
        entry_path = os.path.join(directory, entry)  
        # Determine the connector based on the position of the entry  
        if index == entries_count - 1:  
            connector = '└── '  
            extension = '    '  
        else:  
            connector = '├── '  
            extension = '│   '  
        # Print the entry  
        print(prefix + connector + entry)  
        # Recurse into directories  
        if os.path.isdir(entry_path):  
            tree(entry_path, prefix + extension)  
  
if __name__ == '__main__':  
    # Specify the directory you want to tree. Here, '.' means the current directory.  
    root_directory = '.'  
    print(os.path.basename(os.path.abspath(root_directory)))  
    tree(root_directory)  