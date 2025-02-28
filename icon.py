import argparse
from PIL import Image
import numpy as np
import os

def convertPixelTo8bitRgb(pixel):
    # convert rgb pixel to 8-bit format (3r-3g-2b)
    r, g, b = pixel[:3]
    newR = (r * 8 // 256)
    newG = (g * 8 // 256)
    newB = (b * 4 // 256)
    return (newR << 5) + (newG << 2) + newB

def imageToCArray(imagePath, arrayName="image_data", resizeWidth=None, resizeHeight=None):
    try:
        # open and read the image
        img = Image.open(imagePath)
        
        # resize if dimensions provided
        if resizeWidth and resizeHeight:
            img = img.resize((resizeWidth, resizeHeight), Image.Resampling.LANCZOS)
        
        # get image dimensions
        width, height = img.size
        
        # convert image to RGB mode if it's not already
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # get pixel data
        pixels = np.array(img)
        
        # create the c array header with image dimensions
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
        return f"Error converting image: {str(e)}"

def saveCFile(cCode, outputPath):
    try:
        with open(outputPath, 'w') as f:
            f.write(cCode)
        return True
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert a BMP image to an 8-bit RGB C array')
    parser.add_argument('input_file', help='Path to the input BMP image')
    parser.add_argument('-o', '--output', help='Path to the output C file')
    parser.add_argument('-n', '--name', default='image_data', help='Name of the C array (default: image_data)')
    parser.add_argument('-w', '--width', type=int, help='Resize image to specified width')
    parser.add_argument('-t', '--height', type=int, help='Resize image to specified height')
    
    args = parser.parse_args()
    
    if not args.output:
        baseName = os.path.splitext(args.input_file)[0]
        args.output = f"{baseName}.c"
    
    cCode = imageToCArray(args.input_file, args.name, args.width, args.height)
    
    if saveCFile(cCode, args.output):
        print(f"Successfully converted {args.input_file} to {args.output}")
        if args.width and args.height:
            print(f"Image resized to {args.width}x{args.height}")
    else:
        print(f"Failed to save output to {args.output}")

if __name__ == "__main__":
    main()
