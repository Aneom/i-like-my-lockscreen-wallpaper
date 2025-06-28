import hashlib
import os
import random
import shutil
import string
import time
from PIL import Image

USER_NAME: str = os.getlogin()
WIN_WALLPAPER_PATH: str = f'C:/Users/{USER_NAME}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/'
final_wallpaper_path: str = f'C:/Users{USER_NAME}/Pictures/wallpapers/lockscreen/'


def timeit(func: callable):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        ret = func(*args, **kwargs)
        t = time.time() - t0

        print(f'Function "{func.__name__}" took: {t:.3f} sec')
        
        if ret is None:
            return t
        else: 
            return t, ret
    return wrapper


def rnd_name_gen(length=16, char_pool=string.ascii_lowercase + string.digits) -> str:
    """
    Creates a random string, that consists of elements of a single or multiple character pools.
    :param length: Length of the randomly generated string
    :param char_pool: Character pool (default is lowercase english letters + digits)
    :return: String of random characters
    """
    # English letters = 26, Numbers = 10. If the size of the string to be produced is 16 (default), then this equals to
    # (26+10)^16 = 8*10^24 different character combinations
    rnd_name = str().join(random.choices(population=char_pool, k=length))
    return rnd_name


@timeit
def remove_portrait_images(path: str) -> None:
    """
    Removes portrait images with width=1080 and height=1920
    :param path: Path to search for portrait images
    :return:
    """
    file_list: list[str] = os.listdir(path)

    for file_name in file_list:
        image = Image.open(path + file_name)
        image.close()  # IMPORTANT STEP! otherwise the file cannot be deleted because it's open by PIL
        width, height = image.size

        if width == 1080 and height == 1920:
            os.remove(path + file_name)
    return


@timeit
def remove_duplicates(path: str = final_wallpaper_path) -> None:
    """
    Removes duplicate images, based on the notion that two identical files share the same hash.
    Here we use SHA-1, to create an identity for each image. A set which contains hashes is periodically being built. If
    the hash of a newly read image, matches the hash of the hash set, that image is removed, otherwise it's hash gets added
    to the hash set.
    :param path: Path which contains the files that we wish to check
    :return:
    """
    # https://stackoverflow.com/questions/74751254/removing-all-duplicate-images-with-different-filenames-from-a-directory
    file_list: list[str] = os.listdir(path)

    hash_set: set[bytes] = set()
    # We use sets instead of lists because searching, inserting and deleting an object from a set is more efficient.

    for file_name in file_list:
        digest: bytes = hashlib.sha1(open(path + file_name, 'rb').read()).digest()

        if digest not in hash_set:
            hash_set.add(digest)
        else:
            os.remove(path + file_name)
    return


@timeit
def main() -> list[str]:
    path: str = WIN_WALLPAPER_PATH
    new_path: str = final_wallpaper_path
    file_list: list[str] = os.listdir(path)

    if not os.path.exists(new_path):
        os.makedirs(new_path)

    for file_name in file_list:
        image = Image.open(path + file_name)
        image.close()

        if image.width == 1920 and image.height == 1080 and not file_name.endswith('jpg'):
            shutil.copy(path + file_name, new_path + file_name)
            new_name: str = rnd_name_gen()
            os.rename(new_path + file_name, new_path + str(new_name) + '.jpg')    
    return file_list


if __name__ == "__main__":  # https://www.youtube.com/watch?v=g_wlZ9IhbTs

    t1 = t2 = t3 = 0  # in case one of the t's is removed the program still executes without errors
    t1, file_list = main()
    t2 = remove_duplicates()
    # t3 = remove_portrait_images(final_wallpaper_path)  # not needed since portrait images are filtered out at main()

    print(f'Total Elapsed time: {t1+t2+t3:.3f} sec')
    time.sleep(1.5)
