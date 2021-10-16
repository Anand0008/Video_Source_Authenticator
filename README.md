# Video Source Authenticator 🎥🔐

**Created by Anand Wankhade**

## Overview
A cryptographic steganography tool designed to verify the authenticity of video sources. This prototype embeds encrypted digital signatures (ECC + AES-GCM) directly into video frames using Least Significant Bit (LSB) steganography. It aims to provide a tamper-evident mechanism for video forensic analysis.

## Key Features
-   **Hybrid Encryption**: Uses Elliptic Curve Cryptography (ECC - Brainpool Curve) for key exchange and AES-GCM for authenticated encryption of messages.
-   **LSB Steganography**: Embeds the encrypted signature invisibly into the pixel data of video frames.
-   **Frame Extraction & Reassembly**: Automatically decomposes video into frames for processing and reconstructs them into a playable video file.
-   **Tamper Detection**: The cryptographic signature ensures that any modification to the video frames will invalidate the authentication tag.

## Tech Stack
-   **Language**: Python 3.8+
-   **Cryptography**: `pycryptodome` (AES), `tinyec` (ECC)
-   **Video Processing**: `moviepy`, `opencv-python` (cv2), `ffmpeg`
-   **Steganography**: `stegano`
-   **GUI**: `tkinter`

## Project Structure
-   `src/authenticator.py`: Main application script with GUI. Handles encryption, frame extraction, embedding, and video reconstruction.

## Setup & Usage
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure `ffmpeg` is installed and in your system PATH.*

2.  **Run the Application**:
    ```bash
    python src/authenticator.py
    ```

3.  **Workflow**:
    -   **Encrypt**: Enter a message/signature -> Click "Encrypt".
    -   **Select Video**: Click "Insert video file".
    -   **Embed**: Click "Extract frames and embed" to hide the signature in frames.
    -   **Combine**: Click "Combine Video" to generate the signed output video.

## Disclaimer
This is a research prototype demonstrating the feasibility of video steganography for authentication. It is not intended for production cryptographic use without further security auditing.

---
*Developed as part of a research initiative on digital forensics.*
