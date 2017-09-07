# python3

import os


def change_subtitle_name():
    # traversal mkv files
    for parent, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('mkv'):
                # find prefix of a mkv file
                prefix = filename[0:25]
                subtitle_name = search_subtitle(prefix)
                correct_name = filename.replace('mkv', 'ass')
                print(correct_name)
                print(subtitle_name)
                if correct_name != subtitle_name:  
                    os.rename(subtitle_name, correct_name)

def search_subtitle(prefix):
    # find subtitle filename
    for parent, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.startswith(prefix) and filename.endswith('ass'):
                return filename

if __name__ == '__main__':
    change_subtitle_name()