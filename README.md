![Lipaper](https://raw.githubusercontent.com/okw-y/Lipaper/main/blob/lipaper-thumbnail.png)
Lipaper - Open Source video wallpaper for Windows written in Python.

## General
Lipaper is a simple Open Source program that allows you to set video files on your Windows as wallpaper.
The application uses PySide6 to display the user interface and LibVLC to play video files.
## Installing
To install, you will need to install all the necessary components for the program to work correctly:

 - Dependencies from the requirements.txt file
 - File ffmpeg.exe (You can download it from the official [website](https://ffmpeg.org/download.html))
 - Files libvlc.dll and libvlccore.dll (You can install the VLC program and take the necessary libraries from there or take them from the blob folder on the github page)
## Building
Original builds are created thanks to the [Nuitka](https://github.com/Nuitka/Nuitka) library. You have the right to use any other library to compile the project (For example: [Pyinstaller](https://github.com/pyinstaller/pyinstaller) or [PyPy](https://github.com/mozillazg/pypy))

Basic parameters for compiling a project using Nuitka:

    python -m nuitka --standalone --windows-disable-console --follow-imports --enable-plugins=pyside6 --output-filename="lipaper" <path/to/main.py>

You also need to add dependencies for an already completed project. These files can be specified at the compilation stage using this parameter, or you can add them manually.

    --include-data-file=<source>=<target>

And in both ways of adding additional files, the basic structure must be respected.
DLL files of the LibVLC library must be located in the `plugins` folder for correct operation.
The ffmpeg.exe file must be located in the same directory as the lipaper.exe executable file.
The folder with program resources must also be located in the same directory as the executable file.
## Contribution
We will be glad to receive any help! Feel free to ask questions about the program. If you have ideas for improving the project or ideas for optimizing it, feel free to write to us about it in [Issues](https://github.com/okw-y/Lipaper/issues)!

For users from Russia and Ukraine: if you wish, you can support me on [DonatePay](https://new.donatepay.ru/@1173848) or [DonationAlerts](https://www.donationalerts.com/r/chazz_potato). I will be sincerely glad to receive any support from you!
## Screenshots
There's nothing here yet :(
