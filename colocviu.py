import cv2
import numpy as np
import os

# Read the video file
cap = cv2.VideoCapture('video1.mp4')
cap2 = cv2.VideoCapture('video2.mp4')

# Get frames per second from the video file
fps = cap.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

# Get frame size
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frame_size2 = (int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH)),
               int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Create video files for output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out_gray = cv2.VideoWriter('output_gray.mp4', fourcc,
                           fps, frame_size, isColor=False)

out_gray2 = cv2.VideoWriter('output_gray2.mp4', fourcc,
                            fps2, frame_size2, isColor=False)


# Alpha parameter to extract moving objects (threshold)
alpha1 = 15
alpha2 = 30

singular_values = []
singular_values2 = []

while True:

    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    if not ret or not ret2:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Apply Singular Value Decomposition (SVD)
    U, s, V = np.linalg.svd(gray.astype(np.float32), full_matrices=False)
    U2, s2, V2 = np.linalg.svd(gray2.astype(np.float32), full_matrices=False)

    singular_values.extend(s)
    singular_values2.extend(s2)

    # Reconstruct the frame using a subset of singular values
    k = 60  # Number of singular values retained for video1
    k2 = 70  # Number of singular values retained for video2
    reconstructed_frame = np.dot(U[:, :k], np.dot(np.diag(s[:k]), V[:k, :]))
    reconstructed_frame2 = np.dot(
        U2[:, :k2], np.dot(np.diag(s2[:k2]), V2[:k2, :]))

    # Convert the reconstructed frame to uint8 for further processing
    reconstructed_frame_uint8 = reconstructed_frame.astype(np.uint8)
    reconstructed_frame2_uint8 = reconstructed_frame2.astype(np.uint8)

    # Calculate the absolute difference between the original and reconstructed frame
    diff = cv2.absdiff(gray, cv2.GaussianBlur(
        reconstructed_frame_uint8, (0, 0), 1))
    diff2 = cv2.absdiff(gray2, cv2.GaussianBlur(
        reconstructed_frame2_uint8, (0, 0), 1))

    # Threshold to extract moving objects
    _, thresh = cv2.threshold(diff, alpha1, 225, cv2.THRESH_BINARY)
    _, thresh2 = cv2.threshold(diff2, alpha2, 225, cv2.THRESH_BINARY)

    # Reconstruct the video with moving objects
    out_gray.write(thresh)
    out_gray2.write(thresh2)


# Release resources
cap.release()
cap2.release()
out_gray.release()
out_gray2.release()
