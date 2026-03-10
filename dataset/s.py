import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

# Load the original and handwritten images
original_img_path = "original.jpg"
handwritten_img_path = "handwritten.jpg"

original = cv2.imread(original_img_path, cv2.IMREAD_GRAYSCALE)
handwritten = cv2.imread(handwritten_img_path, cv2.IMREAD_GRAYSCALE)

# Check if images are loaded properly
if original is None:
    raise FileNotFoundError(f"Image not found: {original_img_path}")
if handwritten is None:
    raise FileNotFoundError(f"Image not found: {handwritten_img_path}")

# Resize handwritten image to match the original image size
handwritten = cv2.resize(handwritten, (original.shape[1], original.shape[0]))

# Determine the appropriate win_size
min_dim = min(original.shape[0], original.shape[1])
win_size = min(7, min_dim) if min_dim >= 7 else min_dim | 1  # Ensure win_size is odd

# Compute Structural Similarity Index (SSIM)
similarity_index, diff = ssim(original, handwritten, win_size=win_size, full=True)

# Normalize the difference image
diff = (diff * 255).astype("uint8")

# Apply thresholding to highlight differences
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Display results
print(f"Similarity Score: {similarity_index:.2f}")

# Show images
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(original, cmap='gray')
axes[0].set_title("Original Image")
axes[1].imshow(handwritten, cmap='gray')
axes[1].set_title("Handwritten Image")
axes[2].imshow(thresh, cmap='gray')
axes[2].set_title("Differences Highlighted")

for ax in axes:
    ax.axis("off")

plt.show()
