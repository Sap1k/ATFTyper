# ATFTyper
A neat little program to read the text from the "All Ten Fingers" program, and write them back.

## How does it work?
This program uses the Pillow and PyTesseract libraries to read the text from the screen, and then uses the keyboard library to type the text into the program.
This program has been optimized for Czech characters, but it might work well for English too :)

## Requirements
All the required Python libraries are specified in the requirements.txt file.

You either need to set `use_system_tesseract`to `True` in the `config.yaml` file and install the unofficial Windows Tesseract binaries to `C:\Program Files\Tesseract-OCR` **or** include a Windows binary of Tesseract in `program_dir/Tesseract-builtin`, where program_dir is the directory containing ATFTyper. 
**DO NOT** forget to install the Czech language data for Tesseract, as the program will otherwise crash.

## Things to note
The default config expects that you've got a 1440p monitor @ 100% scaling. If your configuration differs, please change the `bbox` variable in the `config.yaml` file. The `area_debug` variable can assist you in adjusting the borderbox.

Please make sure you've changed your system keyboard to Czech Qwerty and ATF's keyboard to Qwerty (cs). This seems to be a limitation of the keyboard library, so I cannot do much about it.

After hitting "Jde se psát!", you have 2 seconds to click into the ATF typing window before the program starts typing. If you choose to type another line and hit "Ano" at the prompt, you again have 2 seconds before the program makes a space for you, so that it can read the next line properly.

