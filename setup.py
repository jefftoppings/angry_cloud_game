import os
os.environ['TCL_LIBRARY'] = r'C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tk8.6'



from cx_Freeze import setup,Executable

includefiles = ['cloud_background.png','ding.wav','racecar.png','raincloud.png','raindrop.png',
                'splash.wav','game_over.wav', 'Darude - Sandstorm.mp3', "Explosion.wav", 'flaming_racecar.png',
                'raindrop_small.png', 'raincloud_icon.ico']
includes = []
packages = ['pygame']


setup(
    name = "AngryCloud",
    version = '1.0',
    description = "Jeff's first game project",
    author = "Jeffrey Toppings",
    options = {'build_exe': {'includes': includes, 'packages': packages, 'include_files':includefiles}},
    executables = [Executable('angry_cloud.py')]
    )
