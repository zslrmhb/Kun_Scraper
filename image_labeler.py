import os

# Relabel the image of the specified path from 0 to last index

path = "some path"


for root, dirs, files in os.walk(path):
    count = 0
    for file in files:

        original_path = path + '/' + file
        new_path = path + '/' + str(count) + ".jpg"
        if not os.path.exists(new_path):
            print(file)
            os.rename(original_path, new_path)
        count += 1