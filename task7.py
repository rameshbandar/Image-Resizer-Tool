import os
from PIL import Image
from tkinter import filedialog, Tk

def resize_images(input_folder, output_folder, width=None, height=None, quality=85, output_format='JPEG'):
    """
    Resize all images in a folder and save them to another folder
    
    Parameters:
        input_folder (str): Path to folder containing original images
        output_folder (str): Path to save resized images
        width (int): Target width (None to maintain aspect ratio)
        height (int): Target height (None to maintain aspect ratio)
        quality (int): Quality for JPEG (1-100)
        output_format (str): Output format ('JPEG', 'PNG', etc.)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Supported image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    
    # Process each file in input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            try:
                # Open image file
                img_path = os.path.join(input_folder, filename)
                img = Image.open(img_path)
                
                # Calculate new dimensions while maintaining aspect ratio
                if width and height:
                    new_size = (width, height)
                elif width:
                    ratio = width / float(img.size[0])
                    new_size = (width, int(float(img.size[1]) * ratio))
                elif height:
                    ratio = height / float(img.size[1])
                    new_size = (int(float(img.size[0]) * ratio), height)
                else:
                    print("No dimensions specified. Using original size.")
                    new_size = img.size
                
                # Resize image
                resized_img = img.resize(new_size, Image.LANCZOS)
                
                # Prepare output filename
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}.{output_format.lower()}"
                output_path = os.path.join(output_folder, output_filename)
                
                # Save resized image
                resized_img.save(output_path, format=output_format, quality=quality)
                print(f"Resized {filename} -> {output_filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def select_folder(title):
    """Open folder selection dialog"""
    root = Tk()
    root.withdraw()  # Hide the main window
    folder = filedialog.askdirectory(title=title)
    return folder

if __name__ == "__main__":
    print("=== Image Resizer Tool ===")
    
    # Get folders using GUI
    input_folder = select_folder("Select input folder with images")
    if not input_folder:
        print("No input folder selected. Exiting.")
        exit()
    
    output_folder = select_folder("Select output folder for resized images")
    if not output_folder:
        print("No output folder selected. Exiting.")
        exit()
    
    # Get resize parameters
    print("\nResize options:")
    print("1. Set width (height auto-adjusted)")
    print("2. Set height (width auto-adjusted)")
    print("3. Set both width and height (may distort image)")
    choice = input("Enter choice (1-3): ")
    
    width, height = None, None
    if choice == '1':
        width = int(input("Enter width in pixels: "))
    elif choice == '2':
        height = int(input("Enter height in pixels: "))
    elif choice == '3':
        width = int(input("Enter width in pixels: "))
        height = int(input("Enter height in pixels: "))
    else:
        print("Invalid choice. Using original dimensions.")
    
    # Get output format
    output_format = input("Enter output format (JPEG/PNG) [JPEG]: ").upper() or 'JPEG'
    
    # Get quality (for JPEG)
    quality = 85
    if output_format == 'JPEG':
        quality = int(input("Enter JPEG quality (1-100) [85]: ") or 85)
    
    # Process images
    print("\nStarting image processing...")
    resize_images(input_folder, output_folder, width, height, quality, output_format)
    print("\nImage resizing complete!")


