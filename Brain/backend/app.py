from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import torch
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from monai import transforms
from monai.inferers import sliding_window_inference
from monai.data import Dataset, DataLoader
from functools import partial
import io
import base64
from PIL import Image
import torch
from monai.networks.nets import SwinUNETR
app = Flask(__name__)
import numpy as np
import base64

from PIL import Image
import nibabel as nib
from flask import send_file

import matplotlib.pyplot as plt


from tensorflow.keras.models import load_model
import cv2

# Enable CORS for all domains (you can also restrict it to specific domains)
CORS(app)

# Ensure you have a directory for saving uploaded files
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'.nii.gz'}

# Function to check file extension
# Function to check file extension
# Function to check file extension
# Function to check file extension
def allowed_file(filename):
    print(f"Uploaded filename: {filename}")  # Debugging line to see the filename
    extensions = app.config['ALLOWED_EXTENSIONS']
    # Check for '.nii.gz' extension specifically
    return filename.lower().endswith(tuple(extensions))

# Dummy model loading function (replace with your model loading code)
def load_model():
    model_path = "./models/SwinUnetR_Model.pt"  # Adjust path if necessary

    # Define the model architecture (ensure it matches the saved model)
    model = SwinUNETR(
        img_size=(128, 128, 64),
        in_channels=1,
        out_channels=1,
        feature_size=48,
        use_checkpoint=True,
    )

    # Load the pre-trained weights
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))["state_dict"])
    
    model.eval()  # Set the model to evaluation mode
    return model

# Define your processing function
def process_image(image_path):
    # Load the image
    img = nib.load(image_path).get_fdata()

    # Preprocessing using MONAI transforms
    test_transform = transforms.Compose([
        transforms.LoadImaged(keys=["image"]),
        transforms.NormalizeIntensityd(keys="image", nonzero=True, channel_wise=True),
    ])

    test_files = [{"image": image_path}]
    test_ds = Dataset(data=test_files, transform=test_transform)
    test_loader = DataLoader(test_ds, batch_size=1, shuffle=False)

    model = load_model()
    
    roi = (128, 128, 64)
    model_inferer_test = partial(
        sliding_window_inference,
        roi_size=roi,
        sw_batch_size=1,
        predictor=model,
        overlap=0.6,
    )

    # Process the image through the model
    with torch.no_grad():
        for batch_data in test_loader:
            image = batch_data["image"].to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

            if image.dim() == 4:
                image = image.unsqueeze(0)

            prob = torch.sigmoid(model_inferer_test(image))  # Get probability map
            seg = prob[0, 0].detach().cpu().numpy()  # Extract the first batch and channel
            seg_out = (seg > 0.5).astype(np.int8)  # Threshold the output to binary mask

            return img, seg_out  # Return both image and segmentation result

# def to_base64(image_array):
#     # Normalize the image values to 0-255 range if needed for grayscale
#     image_array = np.uint8(np.interp(image_array, (image_array.min(), image_array.max()), (0, 255)))

#     image = Image.fromarray(image_array)  # Convert to PIL image
#     buf = io.BytesIO()
#     image.save(buf, format="PNG")  # Save as PNG format (supports transparency and lossless)
#     byte_data = buf.getvalue()

#     return base64.b64encode(byte_data).decode('utf-8')

def to_base64_3d(image_3d):
    # Save each slice as a PNG and store in a list
    slices_base64 = []
    for i in range(image_3d.shape[2]):
        slice_image = Image.fromarray(image_3d[:, :, i])  # Convert each slice to a PIL image
        buf = io.BytesIO()
        slice_image.save(buf, format="PNG")
        byte_data = buf.getvalue()
        slices_base64.append(base64.b64encode(byte_data).decode('utf-8'))
    
    return slices_base64  # Return a list of Base64 strings (one for each slice)

def save_and_convert_slices(img, seg_out):
    # Ensure the output directory exists
    output_folder = "./output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for slice_num in range(img.shape[2]):
        # Extract each slice
        image_slice = img[:, :, slice_num]
        seg_slice = seg_out[:, :, slice_num]

        # Plot the slices
        plt.figure(figsize=(18, 6))

        # Original Image
        plt.subplot(1, 3, 1)
        plt.title(f"Image - Slice {slice_num}")
        plt.imshow(image_slice, cmap="gray")

        # Segmentation Output
        plt.subplot(1, 3, 2)
        plt.title(f"Segmentation - Slice {slice_num}")
        plt.imshow(seg_slice, cmap="gray")

        # Save the plot as an image file in the output folder
        plot_filename = os.path.join(output_folder, f"slice_{slice_num}.png")
        plt.savefig(plot_filename, bbox_inches='tight', pad_inches=0)
        plt.close()  # Close the plot after saving to free memory

    print(f"All slices saved in the {output_folder} folder.")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            # Save the file to the server
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
        
            # Process the image and segmentation
            img, seg_out = process_image(filename)

            # Normalize the 3D image and segmentation for better visualization
            img_normalized = np.interp(img, (img.min(), img.max()), (0, 255)).astype(np.uint8)
            seg_normalized = (seg_out * 255).astype(np.uint8)  # Assuming binary segmentation (0 or 1)

            # Convert 3D image and segmentation to Base64
            img_base64 = to_base64_3d(img_normalized)
            seg_base64 = to_base64_3d(seg_normalized)

            return jsonify({
                "message": "Image processed successfully.",
                "image_3d": img_base64,
                "segmentation_3d": seg_base64
            }), 200

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500



if __name__ == '__main__':
   app.run(debug=True, threaded=True, use_reloader=False, port=5001, host='0.0.0.0')