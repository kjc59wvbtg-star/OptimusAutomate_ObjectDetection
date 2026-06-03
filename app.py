import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile

st.set_page_config(
    page_title="YOLOv8 Object Detection",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Object Detection using YOLOv8")

st.write(
    "Upload an image and detect objects using the YOLOv8 model."
)

uploaded_file = st.file_uploader(
    "Choose an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    model = YOLO("yolov8n.pt")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp_file:

        image.save(tmp_file.name)

        results = model(tmp_file.name)

    result_image = results[0].plot()

    with col2:
        st.subheader("Detected Objects")
        st.image(result_image, use_container_width=True)

    st.success("Object Detection Completed Successfully!")

    st.subheader("Detection Summary")

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        st.write(
            f"• {class_name} ({confidence:.2f})"
        )