
# import warnings
# warnings.filterwarnings('ignore')

# from PIL import Image
# import hashlib
# import os
# from unstructured.partition.pdf import partition_pdf

# # Define directories
# PDF_DIR = "PDF_Doc"  # Folder containing PDF files
# OUTPUT_DIR = "img2"  # Folder to save extracted images
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # Define filtering criteria (adjust as needed)
# MIN_WIDTH = 200   # Minimum width of images
# MIN_HEIGHT = 200  # Minimum height of images
# MIN_FILE_SIZE = 10240  # Minimum file size in bytes (10 KB)

# def calculate_image_hash(image_path):
#     """Calculate the hash of an image."""
#     with Image.open(image_path) as img:
#         img_hash = hashlib.md5(img.tobytes()).hexdigest()
#     return img_hash

# def filter_images(directory):
#     """Filter images based on size, dimensions, and duplicates."""
#     relevant_images = []
#     seen_hashes = set()  # Store hashes to detect duplicates

#     for img_file in os.listdir(directory):
#         img_path = os.path.join(directory, img_file)
#         if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
#             try:
#                 with Image.open(img_path) as img:
#                     width, height = img.size
#                     file_size = os.path.getsize(img_path)

#                     # Apply filters for relevant images
#                     if width >= MIN_WIDTH and height >= MIN_HEIGHT and file_size >= MIN_FILE_SIZE:
#                         img_hash = calculate_image_hash(img_path)

#                         # Check for duplicates using hash
#                         if img_hash not in seen_hashes:
#                             seen_hashes.add(img_hash)
#                             relevant_images.append(img_path)
#                         else:
#                             os.remove(img_path)  # Remove duplicate image
#                     else:
#                         os.remove(img_path)  # Remove irrelevant images
#             except Exception as e:
#                 print(f"Error processing {img_file}: {e}")
#                 continue
#     return relevant_images

# def process_pdfs(pdf_directory, output_directory):
#     """Process all PDFs in the directory and extract images."""
#     seen_hashes = set()  # Store hashes to detect duplicates across all PDFs

#     for pdf_file in os.listdir(pdf_directory):
#         if pdf_file.lower().endswith('.pdf'):
#             pdf_path = os.path.join(pdf_directory, pdf_file)

#             try:
#                 # Extract images from PDF
#                 partition_pdf(
#                     filename=pdf_path,
#                     extract_images_in_pdf=True,
#                     strategy="hi_res",
#                     infer_table_structure=True,
#                     extract_image_block_output_dir=output_directory,
#                 )

#                 # Filter extracted images
#                 print(f"Processing images from: {pdf_file}")
#                 for img_file in os.listdir(output_directory):
#                     img_path = os.path.join(output_directory, img_file)
#                     if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
#                         try:
#                             with Image.open(img_path) as img:
#                                 width, height = img.size
#                                 file_size = os.path.getsize(img_path)

#                                 # Apply filters for relevant images
#                                 if width >= MIN_WIDTH and height >= MIN_HEIGHT and file_size >= MIN_FILE_SIZE:
#                                     img_hash = calculate_image_hash(img_path)

#                                     # Check for duplicates using hash
#                                     if img_hash not in seen_hashes:
#                                         seen_hashes.add(img_hash)
#                                     else:
#                                         os.remove(img_path)  # Remove duplicate image
#                                 else:
#                                     os.remove(img_path)  # Remove irrelevant images
#                         except Exception as e:
#                             print(f"Error processing image {img_file}: {e}")
#                             continue

#             except Exception as e:
#                 print(f"Error processing {pdf_file}: {e}")

# # Process all PDFs in the PDF_Doc folder
# process_pdfs(PDF_DIR, OUTPUT_DIR)

# print(f"Image extraction and filtering completed. Check the '{OUTPUT_DIR}' folder for results.")











# import warnings
# warnings.filterwarnings('ignore')
 
# from PIL import Image
# import hashlib
# import os
# from unstructured.partition.pdf import partition_pdf
 
# # Define directories
# PDF_DIR = "PDF_Doc"  # Folder containing PDF files
# OUTPUT_DIR = "img2"  # Folder to save extracted images
# os.makedirs(OUTPUT_DIR, exist_ok=True)
 
# # Define minimum file size for filtering (10 KB)
# MIN_FILE_SIZE = 10240  # Minimum file size in bytes (10 KB)
 
# def calculate_image_hash(image_path):
#     """Calculate the hash of an image."""
#     with Image.open(image_path) as img:
#         img_hash = hashlib.md5(img.tobytes()).hexdigest()
#     return img_hash
 
# def process_pdfs(pdf_directory, output_directory):
#     """Process all PDFs in the directory and extract images."""
#     seen_hashes = set()  # Store hashes to detect duplicates across all PDFs
 
#     for pdf_file in os.listdir(pdf_directory):
#         if pdf_file.lower().endswith('.pdf'):
#             pdf_path = os.path.join(pdf_directory, pdf_file)
 
#             try:
#                 # Extract images from PDF
#                 partition_pdf(
#                     filename=pdf_path,
#                     extract_images_in_pdf=True,
#                     strategy="hi_res",
#                     infer_table_structure=True,
#                     extract_image_block_output_dir=output_directory,
#                 )
 
#                 # Filter extracted images
#                 print(f"Processing images from: {pdf_file}")
#                 for img_file in os.listdir(output_directory):
#                     img_path = os.path.join(output_directory, img_file)
#                     if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
#                         try:
#                             file_size = os.path.getsize(img_path)
 
#                             # Apply file size filter only
#                             if file_size >= MIN_FILE_SIZE:  # Keep if >= 10 KB
#                                 img_hash = calculate_image_hash(img_path)
 
#                                 # Check for duplicates using hash
#                                 if img_hash not in seen_hashes:
#                                     seen_hashes.add(img_hash)
#                                 else:
#                                     os.remove(img_path)  # Remove duplicate image
#                             else:
#                                 os.remove(img_path)  # Remove images < 10 KB
#                         except Exception as e:
#                             print(f"Error processing image {img_file}: {e}")
#                             continue
 
#             except Exception as e:
#                 print(f"Error processing {pdf_file}: {e}")
 
# # Process all PDFs in the PDF_Doc folder
# process_pdfs(PDF_DIR, OUTPUT_DIR)
 
# print(f"Image extraction and filtering completed. Check the '{OUTPUT_DIR}' folder for results.")




# import warnings
# warnings.filterwarnings('ignore')

# from PIL import Image
# import hashlib
# import os
# from unstructured.partition.pdf import partition_pdf

# # Define directories
# PDF_DIR = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot/PDF_Doc"  # Folder containing PDF files
# OUTPUT_DIR = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot/img2"  # Folder to save extracted images
# DUMP_DIR = "image_dump"  # Folder to save images < 10 KB

# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(DUMP_DIR, exist_ok=True)

# # Define minimum file size for filtering (10 KB)
# MIN_FILE_SIZE = 10240  # Minimum file size in bytes (10 KB)

# def calculate_image_hash(image_path):
#     """Calculate the hash of an image."""
#     with Image.open(image_path) as img:
#         img_hash = hashlib.md5(img.tobytes()).hexdigest()
#     return img_hash

# def process_pdfs(pdf_directory, output_directory, dump_directory):
#     """Process all PDFs in the directory and extract images."""
#     seen_hashes = set()  # Store hashes to detect duplicates across all PDFs

#     for pdf_index, pdf_file in enumerate(os.listdir(pdf_directory), start=1):
#         if pdf_file.lower().endswith('.pdf'):
#             pdf_path = os.path.join(pdf_directory, pdf_file)
#             pdf_base_name = os.path.splitext(pdf_file)[0]  # Remove .pdf extension

#             try:
#                 # Extract images from PDF
#                 partition_pdf(
#                     filename=pdf_path,
#                     extract_images_in_pdf=True,
#                     strategy="hi_res",
#                     infer_table_structure=True,
#                     extract_image_block_output_dir=output_directory,
#                 )

#                 # Filter extracted images
#                 print(f"Processing images from: {pdf_file}")

#                 used_count = 1  # Counter for used images (≥10 KB)
#                 unused_count = 1  # Counter for unused images (<10 KB)

#                 for img_file in os.listdir(output_directory):
#                     img_path = os.path.join(output_directory, img_file)
#                     if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
#                         try:
#                             file_size = os.path.getsize(img_path)

#                             # Apply file size filter
#                             if file_size >= MIN_FILE_SIZE:  # Keep if ≥ 10 KB
#                                 img_hash = calculate_image_hash(img_path)

#                                 # Check for duplicates using hash
#                                 if img_hash not in seen_hashes:
#                                     seen_hashes.add(img_hash)

#                                     # Rename and move the image
#                                     new_name = f"used_{pdf_base_name}_{used_count}.png"
#                                     used_count += 1
#                                     os.rename(img_path, os.path.join(output_directory, new_name))
#                                 else:
#                                     os.remove(img_path)  # Remove duplicate image
#                             else:
#                                 # Rename and move small images
#                                 new_name = f"unused_{pdf_base_name}_{unused_count}.png"
#                                 unused_count += 1
#                                 os.rename(img_path, os.path.join(dump_directory, new_name))

#                         except Exception as e:
#                             print(f"Error processing image {img_file}: {e}")
#                             continue

#             except Exception as e:
#                 print(f"Error processing {pdf_file}: {e}")

# # Process all PDFs in the PDF_Doc folder
# process_pdfs(PDF_DIR, OUTPUT_DIR, DUMP_DIR)

# print(f"Image extraction and filtering completed. Check '{OUTPUT_DIR}' for filtered images and '{DUMP_DIR}' for small images.")








import warnings
warnings.filterwarnings('ignore')
 
from PIL import Image
import hashlib
import os
import shutil
from unstructured.partition.pdf import partition_pdf
 
# Define directories
PDF_DIR = "PDF_Doc"  # Folder containing PDF files
OUTPUT_DIR = "img2"  # Folder to save extracted images
DUMP_DIR = "image_dump"  # Folder to save images < 10 KB
TEMP_DIR = "temp_images"  # Temporary folder for extracted images
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DUMP_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
 
# Define minimum file size for filtering (10 KB)
MIN_FILE_SIZE = 10240  # Minimum file size in bytes (10 KB)
 
def calculate_image_hash(image_path):
    """Calculate the hash of an image."""
    with Image.open(image_path) as img:
        img_hash = hashlib.md5(img.tobytes()).hexdigest()
    return img_hash
 
def process_pdfs(pdf_directory, output_directory, dump_directory, temp_directory):
    """Process all PDFs in the directory and extract images."""
    seen_hashes = set()  # Store hashes to detect duplicates across all PDFs
 
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            pdf_base_name = os.path.splitext(pdf_file)[0]  # Remove .pdf extension
            # Create a temp subfolder for the current PDF's images
            pdf_temp_dir = os.path.join(temp_directory, pdf_base_name)
            os.makedirs(pdf_temp_dir, exist_ok=True)
 
            try:
                # Extract images from PDF into the temp directory
                partition_pdf(
                    filename=pdf_path,
                    extract_images_in_pdf=True,
                    strategy="hi_res",
                    infer_table_structure=True,
                    extract_image_block_output_dir=pdf_temp_dir,
                )
 
                # Process extracted images
                print(f"Processing images from: {pdf_file}")
 
                used_count = 1  # Counter for used images (≥10 KB)
                unused_count = 1  # Counter for unused images (<10 KB)
 
                for img_file in os.listdir(pdf_temp_dir):
                    img_path = os.path.join(pdf_temp_dir, img_file)
                    if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            file_size = os.path.getsize(img_path)
 
                            # Apply file size filter
                            if file_size >= MIN_FILE_SIZE:  # Keep if ≥ 10 KB
                                img_hash = calculate_image_hash(img_path)
 
                                # Check for duplicates using hash
                                if img_hash not in seen_hashes:
                                    seen_hashes.add(img_hash)
 
                                    # Rename and move the image
                                    new_name = f"used_{pdf_base_name}_{used_count}.png"
                                    used_count += 1
                                    os.rename(img_path, os.path.join(output_directory, new_name))
                                else:
                                    os.remove(img_path)  # Remove duplicate image
                            else:
                                # Rename and move small images
                                new_name = f"unused_{pdf_base_name}_{unused_count}.png"
                                unused_count += 1
                                os.rename(img_path, os.path.join(dump_directory, new_name))
 
                        except Exception as e:
                            print(f"Error processing image {img_file}: {e}")
                            continue
 
                # Remove the temp subfolder after processing
                shutil.rmtree(pdf_temp_dir)
 
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
 
# Process all PDFs in the PDF_Doc folder
process_pdfs(PDF_DIR, OUTPUT_DIR, DUMP_DIR, TEMP_DIR)
 
print(f"Image extraction and filtering completed. Check '{OUTPUT_DIR}' for filtered images and '{DUMP_DIR}' for small images.")