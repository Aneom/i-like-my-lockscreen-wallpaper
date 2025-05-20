# I like my lockscreen wallpaper
A simple Python script that places the Microsoft Spotlight [(read more)](https://en.wikipedia.org/wiki/Windows_Spotlight) lock screen wallpapers, in your Pictures folder.

Briefly, this script:
1. Retrieves the already existing image files, which are located in a standard directory in Windows (`WIN_WALLPAPER_PATH` variable in the script)
2. Converts them to the jpeg format using advanced image processing techniques (appends `.jpeg` at the end of the filename)
3. Saves them to a prespecified location (`wallpaper_folder_path`) with a random 16-digit filename.
4. Checks for duplicate images and deletes them
4. Lastly, a timing function is used to calculate the elapsed time of each function

## Prerequisites

* Python Imaging Library (PIL) (do `pip install pillow` in the command line if you don't have it installed)

## Future Plans

* Wallpaper recognition using AI: change the wallpaper name based on what is depicted in the image.


