import cv2
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import easyocr
import numpy as np
import pandas as pd
from PIL import Image


SCOPES = [f"TIGERD{x}" for x in range(1,13)] + [None]


@st.experimental_memo
def extract_chip_nums(photo):
    # readimage in format for opencv
    img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_COLOR)

    # instance text detector
    reader = easyocr.Reader(["en"], gpu=False)

    # detect text on image
    text = reader.readtext(img)

    # replace . to - if misread (could be common)
    chip_nums = [t[1].replace(".", "-") for t in text]

    # create boxes around chip nums on picture
    for t in text:
        bbox, text_, score = t

        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)

    mat_img = cv2.cvtColor(
        cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC),
        cv2.COLOR_BGR2RGB,
    )

    return sorted(chip_nums), mat_img


@st.experimental_memo
def process_image(photo, chips_val):

    chip_nums, mat_img = extract_chip_nums(photo)

    flow_cell = {
        "Chip4": chip_nums[3:12:4],
        "Chip3": chip_nums[2:12:4],
        "Chip2": chip_nums[1:12:4],
        "Chip1": chip_nums[:12:4],
    }

    # remove [] and extra '' from pasted string 
    cleaned_string = chips_val.replace("[", "").replace("]", "").replace("'", "")
    chips_input = cleaned_string.split(", ")

    # create df corresponding to num sets
    if len(chip_nums) / 4 == 3:
        df = pd.DataFrame(flow_cell, index=["Set1", "Set2", "Set3"])
    elif len(chip_nums) / 4 == 2:
         df = pd.DataFrame(flow_cell, index=["Set1", "Set2"])
    else:
         df = pd.DataFrame(flow_cell, index=["Set1"])

    # check if chips in pasted list match to numbers read from OCR
    chips_match = all(i in chip_nums for i in chips_input)

    if chips_match:
        st.success("Done processing, user input and computer validation match!")
    else:
        st.error(
            "Done processing, user input and computer validation do not match. Please review further"
        )

    return mat_img, df

def main():

    data = {}

    st.header("Decoding Checklist")

    decoder_name = st.text_input("Enter your name: ")

    microscope = st.selectbox("Select a microscope", SCOPES, index=len(SCOPES) - 1)

    uploaded_photo = st.file_uploader("Choose an image.", type=["jpg","jpeg", "png"])

    if uploaded_photo:

        cross_val = st.text_input(
            "Copy and paste the list of chips assigned to you in the #chip-assignment slack channel: "
        )

        data["Assigned Chips"] = cross_val

        mat_img, df = process_image(uploaded_photo, data["Assigned Chips"])
        st.image(mat_img)
        st.write("Chips read from #chip-assignment: ")
        st.write(cross_val)
        st.write("Chips read by computer: ")
        st.write(df)

    else:
        st.error("Please upload an image and paste in the assigned chips before continuing.")

    st.warning("Find another decoder for secondary validation.")

    chips_match = st.radio("Do the chips match in the uploaded photo and pasted list?", ("Yes", "No"))

    if chips_match == "Yes":
        chips_match_data = True
    else:
        chips_match_data = False

    verifier = st.text_input("Decoder's initials: ")

    st.write("Sign or drawing something fun!")

    canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=5,
    stroke_color="#000000",
    background_color="#E7E7E7",
    update_streamlit=True,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)

    data["Decoder"] = decoder_name
    data["Decoder Validation"] = verifier
    data["Chips Match"] = chips_match_data
    data["Microscope"] = microscope


    st.write(data)

