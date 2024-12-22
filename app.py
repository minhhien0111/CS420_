import streamlit as st
import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import ast

# Streamlit app setup
st.title("Image Captioning App")
st.write("Upload an image to generate a caption.")

# Specify paths to model and word map files
MODEL_PATH = ".\model\BEST_checkpoint_flickr8k_5_cap_per_img_5_min_word_freq.pth.tar"
WORD_MAP_PATH = ".\model\WORDMAP_flickr8k_5_cap_per_img_5_min_word_freq.json"

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Save the uploaded image to a temporary file
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_image.getbuffer())

    # Open and display the uploaded image
    image = Image.open("temp_image.jpg")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Generate caption using the subprocess
    st.write("Generating caption...")
    try:
        # Run caption.py script with specified parameters
        result = subprocess.run(
            [
                "python", "caption.py",
                "--img", "temp_image.jpg",
                "--model", MODEL_PATH,
                "--word_map", WORD_MAP_PATH,
                "--beam_size", "5"
            ],
            capture_output=True, text=True, check=True
        )
        
        # Check if the result is a list and handle accordingly
        captions = result.stdout.strip().split("\n")  # Assuming each caption is on a new line
        caption = captions[0]  # Get the first caption or choose the best one if it's a list
        # caption = caption[1:-1]
        # # Concatenate the remaining elements into a sentence
        # sentence = " ".join(caption)
        # Convert the string representation of a list into an actual list
        words = ast.literal_eval(caption)

        # Remove the '<start>' and '<end>' tokens
        words = [word for word in words if word not in ['<start>', '<end>']]

        # Join the words into a sentence
        sentence = ' '.join(words)

        st.write("**Caption:**", sentence)

        # Overlay caption on the image
        draw = ImageDraw.Draw(image)
        
        # Load a font; use default if a TTF font is not available
        try:
            font = ImageFont.truetype("arial.ttf", 24)  # You may replace with another font path if available
        except IOError:
            font = ImageFont.load_default()
        
        # Calculate position for the text overlay using textbbox
        text_bbox = draw.textbbox((0, 0), caption, font=font)
        text_width = text_bbox[2] - text_bbox[0]  # width of the text
        text_height = text_bbox[3] - text_bbox[1]  # height of the text
        text_position = (10, image.height - text_height - 10)  # Place caption near the bottom
        
        # Draw a black rectangle to make text more visible
        # draw.rectangle(
        #     [text_position, (text_position[0] + text_width, text_position[1] + text_height)],
        #     fill="black"
        # )
        # Add the caption text
        # draw.text(text_position, caption, fill="white", font=font)

        # Display the image with the caption overlay
        # st.image(image, caption="Image with Caption Overlay", use_container_width=True)

    except subprocess.CalledProcessError as e:
        st.error("Error generating caption.")
        st.error(e.stderr)

    # Remove the temporary image file
    os.remove("temp_image.jpg")
