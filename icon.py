import argparse
import os
import numpy as np
from PIL import Image
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def convertPixelTo8bitRgb(pixel):
    r, g, b = pixel[:3]
    newR = (r * 8 // 256)
    newG = (g * 8 // 256)
    newB = (b * 4 // 256)
    return (newR << 5) + (newG << 2) + newB

def imageToCArray(imagePath, arrayName="image_data", resizeWidth=None, resizeHeight=None):
    try:
        if not os.path.exists(imagePath):
            print(f"{Fore.RED}Error: File '{imagePath}' not found!{Style.RESET_ALL}")
            return None
        
        img = Image.open(imagePath)
        
        if resizeWidth and resizeHeight:
            img = img.resize((resizeWidth, resizeHeight), Image.Resampling.LANCZOS)
        
        width, height = img.size
        
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        pixels = np.array(img)
        
        cCode = [
            f"// © Orange Computers 2024",
            f"// image dimensions: {width}x{height}",
            f"#define IMAGE_WIDTH {width}",
            f"#define IMAGE_HEIGHT {height}",
            f"const unsigned char {arrayName}[] = {{"
        ]
        
        bytesPerLine = 0
        for y in range(height):
            lineValues = []
            for x in range(width):
                pixel = pixels[y, x]
                rgb8bit = convertPixelTo8bitRgb(pixel)
                lineValues.append(f"0x{rgb8bit:02X}")
                bytesPerLine += 1
                
                if bytesPerLine % 16 == 0 and not (y == height-1 and x == width-1):
                    cCode.append("    " + ", ".join(lineValues) + ",")
                    lineValues = []
                
        if lineValues:
            if y == height-1:
                cCode.append("    " + ", ".join(lineValues))
            else:
                cCode.append("    " + ", ".join(lineValues) + ",")
        
        cCode.append("};")
        return "\n".join(cCode)
    
    except Exception as e:
        print(f"{Fore.RED}Error processing image: {str(e)}{Style.RESET_ALL}")
        return None

def saveCFile(cCode, outputPath):
    try:
        with open(outputPath, 'w') as f:
            f.write(cCode)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving file: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert a BMP image to an 8-bit RGB C array')
    parser.add_argument('input_file', help='Path to the input BMP image')
    parser.add_argument('-o', '--output', help='Path to the output C file')
    parser.add_argument('-n', '--name', default='image_data', help='Name of the C array (default: image_data)')
    parser.add_argument('-w', '--width', type=int, help='Resize image to specified width')
    parser.add_argument('-t', '--height', type=int, help='Resize image to specified height')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"{Fore.RED}Error: Input file '{args.input_file}' does not exist.{Style.RESET_ALL}")
        return
    
    if not args.output:
        baseName = os.path.splitext(args.input_file)[0]
        args.output = f"{baseName}.c"
    
    cCode = imageToCArray(args.input_file, args.name, args.width, args.height)
    
    if cCode:
        if saveCFile(cCode, args.output):
            print(f"{Fore.GREEN}Successfully converted {Fore.CYAN}{args.input_file} {Fore.GREEN}to {Fore.CYAN}{args.output}{Style.RESET_ALL}")
            if args.width and args.height:
                print(f"{Fore.YELLOW}Image resized to {args.width}x{args.height}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to save output to {Fore.CYAN}{args.output}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
