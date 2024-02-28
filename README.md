# Video Object Extraction using Singular Value Decomposition (SVD)

Objective

    Demonstrate the use of Singular Value Decomposition (SVD) for extracting moving objects from video files. This technique utilizes SVD to separate the moving foreground from the static background in a video sequence.

Implementation

Dependencies

OpenCV (cv2)
NumPy (np)

Description

    This Python script reads two video files (video1.mp4 and video2.mp4), applies SVD on each frame, and extracts moving objects from the videos. The process involves the following steps:

    1. Read input video files.
    2. Extract frames per second (FPS) and frame size from the videos.
    3. Create output video files for the extracted moving objects.
    4. Perform Singular Value Decomposition (SVD) on each frame.
    5. Reconstruct the frames using a subset of singular values to remove the static background.
    6. Calculate the absolute difference between the original and reconstructed frames.
    7. Apply thresholding to extract moving objects.
    8. Write the extracted objects to output video files.

Parameters

    alpha1 and alpha2: Threshold parameters for extracting moving objects from video1.mp4 and video2.mp4, respectively.
    k and k2: Number of singular values retained for reconstructing frames from video1.mp4 and video2.mp4, respectively.

Output

    output_gray.mp4: Video file containing moving objects extracted from video1.mp4.
    output_gray2.mp4: Video file containing moving objects extracted from video2.mp4.

Notes

    This implementation assumes that the input video files are in .mp4 format.
    Fine-tuning the threshold parameters (alpha1 and alpha2) and the number of retained singular values (k and k2) may be required based on the characteristics of the input videos.
