from PIL import Image
import os

# Function to print colored text in the terminal
def print_colored(message, color_code):
    print(f"{color_code}{message}\033[0m")

def bmp_to_c_array(filename):
    # open bmp file using pillow
    img = Image.open(filename)

    # check if image is in 8-bit indexed color mode
    if img.mode != 'P':
        raise ValueError("Image must be in 8-bit indexed color mode")

    width, height = img.size
    pixel_data = list(img.getdata())

    # extract array name from the filename (remove .bmp extension)
    array_name = os.path.splitext(filename)[0]

    # prepare c array with height and width macros
    c_array = f"#define ICON_HEIGHT {height}\n"
    c_array += f"#define ICON_WIDTH {width}\n\n"
    c_array += f"unsigned char {array_name}[{width}*{height}] = {{\n"

    # process image data row by row
    for i in range(0, len(pixel_data), width):
        row_data = pixel_data[i:i + width]
        row_str = ', '.join(f"0x{pixel:02x}" for pixel in row_data)
        c_array += f"  {row_str},\n"

    # remove the last comma and close the array definition
    c_array = c_array.rstrip(',\n') + "\n};"

    return c_array

def main():
    filename = input("Please enter the name of the BMP file (without .bmp extension): ")

    # automatically add .bmp extension if missing
    filename += '.bmp'

    # check if the file exists
    if not os.path.isfile(filename):
        print_colored(f"Error: {filename} does not exist.", "\033[91m")  # Red text
        return

    try:
        # convert bmp to c array format
        c_array = bmp_to_c_array(filename)

        # output file name will be same as input filename with .h extension
        output_filename = os.path.splitext(filename)[0] + '.h'

        # write c array to the output header file
        with open(output_filename, 'w') as f:
            f.write(c_array)

        print_colored(f"Successfully converted the BMP to C array and saved to {output_filename}", "\033[92m")  # Green text

    except Exception as e:
        print_colored(f"Error: {e}", "\033[91m")  # Red text

if __name__ == "__main__":
    main()
