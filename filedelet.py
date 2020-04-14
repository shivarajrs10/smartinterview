import os
import shutil


def create_dir():
    dir_path = os.getcwd() + '/storage'

    try:
        os.mkdir(dir_path)
        print(dir_path)
    except OSError as error:
        pass


create_dir()


def Delete_files():
    folder = 'storage'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# Delete_files()
