# 8bit-bmp-2-c
Takes 8-bit indexed color mode BMPs and turns them into C unsigned char arrays.

A simple Python script that converts a BMP image (should be in 8-bit indexed color mode) into a C array format. The script takes a filename from the user, processes the pixel data, and generates a C header file (.h) containing the pixel data as an array. This is useful for embedding image data in operating systems or microcontrollers.

### Languages and styles used
<p>
    <a href="https://www.python.org/"><img height="28" width="28" src="https://cameronos.github.io/img/icon/python.png" /></a>
</p>

## Screenshots
<img src width=20% src="https://cameronos.github.io/img/audiosetup.jpg">

## Features
- Automatically processes `.bmp` files and converts 8-bit indexed BMP images into a C array.
- Generates a `.h` file with the array named after the BMP file (without extension), including its size in `width*height` format.

## Inspiration
Heavily inspired by [FileToCArray](https://notisrac.github.io/FileToCArray/), but wanted to make a more technical feel... so here we are...

## Usage
To use the script, you need:
- Python 3.x
- Pillow library for image processing

To install Pillow, you can use pip:

```bash
pip install pillow
