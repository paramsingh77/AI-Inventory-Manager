# import torch
# from transformers import Idefics2Processor, Idefics2ForConditionalGeneration
# from PIL import Image

# token = "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"

# # Check if CUDA is available
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # Load the processor and model
# processor = Idefics2Processor.from_pretrained("HuggingFaceM4/idefics2-8b", use_auth_token=token)
# model = Idefics2ForConditionalGeneration.from_pretrained("HuggingFaceM4/idefics2-8b", use_auth_token=token).to(device)

# def analyze_image_with_idefics(image_path):
#     # Load the image
#     image = Image.open(image_path)

#     # Prepare the prompt
#     prompt = "Describe the text content visible in this image."
    
#     # Process the input
#     inputs = processor(text=prompt, images=[image], return_tensors="pt").to(device)

#     # Generate the output
#     outputs = model.generate(**inputs, max_new_tokens=100)

#     # Decode the output
#     result = processor.batch_decode(outputs, skip_special_tokens=True)[0]

#     return result.strip()

# # Use the function
# image_path = './uploads/product-labels-1-ezgif.com-webp-to-jpg-converter.jpg'
# analysis = analyze_image_with_idefics(image_path)
# print("Image analysis:", analysis)


import easyocr
from PIL import Image
import numpy as np


def extract_text_from_image(image_path, languages=['en']):
    """
    Extract text from an image using EasyOCR.
    
    Args:
    image_path (str): Path to the image file.
    languages (list): List of language codes. Default is ['en'] for English.
    
    Returns:
    str: Extracted text from the image.
    """
    # Initialize the OCR reader
    reader = easyocr.Reader(languages)
    
    # Read the image
    image = Image.open(image_path)
    image_np = np.array(image)
    
    # Perform OCR
    results = reader.readtext(image_np)
    
    # Extract and join the detected text
    extracted_text = ' '.join([result[1] for result in results])
    
    return extracted_text

# Example usage
image_path = './uploads/product-labels-1-ezgif.com-webp-to-jpg-converter.jpg'
languages = ['en', 'no']  # English and Norwegian

try:
    extracted_text = extract_text_from_image(image_path, languages)
    print("Extracted text:")
    print(extracted_text)
except Exception as e:
    print(f"An error occurred: {str(e)}")