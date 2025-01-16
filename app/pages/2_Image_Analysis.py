import streamlit as st
from openai import Client
from dotenv import load_dotenv
from PIL import Image, ImageStat, ImageEnhance, ImageFilter 
import os
import numpy as np
import cv2 

# Load environment variables
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = Client(api_key=openai_api_key)

# Page content
st.title("Your Astrophotography Image Processing Assistant")
st.write("Upload your astrophotography images for expert feedback.")

# File uploader for image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

def analyze_image(image_path):
    """
    Analyzes various properties of the image, including resolution, brightness, contrast,
    saturation, sharpness, noise level, dynamic range, color balance, and chromatic aberration.
    :param image_path: Path to the image file.
    :return: Dictionary containing image properties.
    """
    # Open the image
    img = Image.open(image_path)
    
    # Get resolution
    width, height = img.size
    
    # Calculate brightness and contrast
    grayscale_img = img.convert("L")
    stat = ImageStat.Stat(grayscale_img)
    brightness = stat.mean[0]
    contrast = stat.stddev[0]
    
    # Calculate saturation
    hsv_img = img.convert("HSV")
    _, s, _ = hsv_img.split()
    saturation_stat = ImageStat.Stat(s)
    saturation = saturation_stat.mean[0] / 255  # Normalize to [0, 1]
    
    # Calculate sharpness
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    sharpness_stat = ImageStat.Stat(edges)
    sharpness = sharpness_stat.mean[0]
    
    # Calculate noise level
    noise = stat.stddev[0]
    
    # Calculate dynamic range
    pixel_values = np.array(grayscale_img).flatten()
    dynamic_range = pixel_values.max() - pixel_values.min()
    
    # Calculate color balance
    r, g, b = img.split()
    r_mean = ImageStat.Stat(r).mean[0]
    g_mean = ImageStat.Stat(g).mean[0]
    b_mean = ImageStat.Stat(b).mean[0]
    color_balance = {
        "red_mean": r_mean,
        "green_mean": g_mean,
        "blue_mean": b_mean
    }
    
    # Calculate chromatic aberration
    lab_img = img.convert("LAB")
    _, a, b = lab_img.split()
    chroma_stat_a = ImageStat.Stat(a)
    chroma_stat_b = ImageStat.Stat(b)
    chromatic_aberration = {
        "a_channel_stddev": chroma_stat_a.stddev[0],
        "b_channel_stddev": chroma_stat_b.stddev[0]
    }
    
    return {
        "resolution": f"{width}x{height}",
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
        "sharpness": sharpness,
        "noise_level": noise,
        "dynamic_range": dynamic_range,
        "color_balance": color_balance,
        "chromatic_aberration": chromatic_aberration
    }

# Process the uploaded image
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Add an Analyze button
    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):
            try:
                # Analyze the image locally
                image_properties = analyze_image(uploaded_file)

                # Generate a summary to send to OpenAI
                prompt = f"""
                You are an expert astrophotographer. A user has uploaded an image for feedback.
                The image has the following properties:
                - Resolution: {image_properties['resolution']}
                - Brightness: {image_properties['brightness']}
                - Contrast: {image_properties['contrast']}
                - Saturation: {image_properties['saturation']}
                - Sharpness: {image_properties['sharpness']}
                - Noise Level: {image_properties['noise_level']}
                - Dynamic Range: {image_properties['dynamic_range']}
                - Color Balance: {image_properties['color_balance']}
                - Chromatic Aberration: {image_properties['chromatic_aberration']}
                Provide feedback on this image and suggest how the user can improve their astrophotography techniques.
                The image should look natural-looking and not over-processed. So not too bright or too dark, and not too much contrast
                and saturated. Don't mention the resolution, brightness, contrast, saturation, sharpness, noise level, dynamic range, color balance, and chromatic aberration
                numbers and instead, alanyze the image based on those numbers and give a general feedback based on the numbers. The image can be a wide image
                of foreground terrestial objects and night sky or deep-sky image.
                """

                # Call OpenAI for detailed feedback
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                feedback = response.choices[0].message.content
                st.success("Analysis Complete!")
                st.write(feedback)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
