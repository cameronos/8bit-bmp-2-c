# 8bit-bmp-2-c
Takes 8bit indexed color mode BMPs and turns into C unsinged char arrays.

### Languages and styles used
<p>
    <A href="https://www.python.org/"><img height="28" width="28" src="https://cameronos.github.io/img/icon/python.png" /></a>
</p>

A simple Python script that converts a BMP image (should be in 8-bit indexed color mode) into a C array format. 
Script takes a filename from user, processes the pixel data, and generates a C header file (.h) containing the pixel data as an array. This is useful for embedding image data in operating systems or microcontrollers.

## Features
- Automatically processes .bmp files and converts 8-bit indexed BMP images into a C array.
- Generates a .h file with the array named after the BMP file (without extension), including its size in width*height format.

##Inspiration
Heavily inspired from https://notisrac.github.io/FileToCArray/, but wanted to make a more technical feel... so here we are...

##Usage
To use the script, you need:
- Python 3.x
- Pillow library for image processing

To install Pillow, you can use pip:

```bash
pip install pillow
```

Then, just run icon.py in a terminal and provide it with the file!
