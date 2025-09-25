from src import i_like_my_lockscreen_wallpaper as ilmlw
import time
import os


if __name__ == "__main__":
    t1 = t2 = 0  # in case one of the t's is removed the program still executes without errors
    t1, file_list = ilmlw.get_wallpaper_imgs()
    t2 = ilmlw.remove_duplicates()

    print(f'Total Elapsed time: {t1+t2:.3f} sec')
    time.sleep(1.5)