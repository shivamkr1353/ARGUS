# ARGUS: Raspberry Pi 4 Hardware Integration Guide

Transitioning the ARGUS system from a PC-based prototype to a physical hardware prototype using a Raspberry Pi 4 is a great next step. Since your project relies on cloud APIs (NVIDIA NIM, Google STT, Edge TTS), the Raspberry Pi will act as an **edge node**—capturing data, sending it to the cloud, and playing back the response. 

Here is the step-by-step roadmap to integrate your hardware components.

---

## 1. Hardware Setup & Connections

### **Raspberry Pi 4 Board**
- Use a **Raspberry Pi 4 (4GB or 8GB RAM)**.
- Install **Raspberry Pi OS (64-bit)** using the official Raspberry Pi Imager. The 64-bit version is highly recommended for better memory management and Python package compatibility.

### **Camera Module**
- **Option A (USB Webcam):** The easiest method. Plug it into one of the blue USB 3.0 ports. `cv2.VideoCapture(0)` in your `vision.py` will usually recognize it immediately.
- **Option B (Pi Camera Module V2/V3):** Connect it via the CSI ribbon cable port on the Pi. You will need to enable the camera interface in `raspi-config` (or use the modern `libcamera` stack). OpenCV can read from this via the `v4l2` (Video4Linux) driver using `/dev/video0`.

### **Microphone & Speaker**
- **Microphone:** A USB microphone is strongly recommended for Raspberry Pi because it bypasses the Pi's lack of onboard analog-to-digital audio inputs. Plug it into a USB port.
- **Speaker:** You can use the Pi's built-in 3.5mm audio jack connected to a portable speaker, or a USB/Bluetooth speaker. 
- **Configuration:** You will need to configure `ALSA` or `PulseAudio` on the Pi to set your USB Mic as the default recording device and your Speaker as the default playback device.

---

## 2. Software Dependencies on the Pi

The Pi runs a Linux environment (Debian-based). You will need to install system-level packages before your Python requirements will work.

Open the Pi's terminal and run:
```bash
sudo apt update && sudo apt upgrade -y

# Required for OpenCV
sudo apt install libopencv-dev python3-opencv -y

# Required for PyAudio (Microphone access)
sudo apt install portaudio19-dev python3-pyaudio -y

# Audio playback utilities (for Edge-TTS)
sudo apt install mpv ffmpeg alsa-utils -y
```

After installing system dependencies, you can create a virtual environment on the Pi and install your `requirements.txt`.

---

## 3. Modifying the Code for Headless Operation

Right now, your main application uses **Streamlit**, which is great for PC debugging but not ideal for a wearable/headless prototype where there is no screen.

**Recommendation:** Create a new entry point, e.g., `main_headless.py`, that runs a continuous loop without a graphical interface.

**Example Flow for `main_headless.py`:**
1. **Wait for Trigger:** The Pi constantly listens for a wake word (e.g., "Hey Argus") or waits for a physical push-button connected to the Pi's GPIO pins.
2. **Capture Image:** Once triggered, the script triggers `vision.py` to snap a frame from the camera.
3. **Capture Audio:** The script triggers `speech.py` to record the user's question via the USB mic.
4. **Process:** Send the image and audio transcript to the NVIDIA NIM API (as you currently do).
5. **Output:** Receive the text response, pass it to Edge-TTS, and play the generated audio through the speaker.

*Tip: If you still want the Streamlit UI for debugging, you can run Streamlit on the Pi and access the dashboard from your laptop's browser by navigating to `http://<RASPBERRY_PI_IP>:8501`.*

---

## 4. Managing Power & Thermals

Since you are building a physical prototype to demonstrate:
- **Power:** Use a high-quality USB-C power bank (at least 3A / 15W output) to power the Pi 4 and the peripherals simultaneously. 
- **Thermals:** The Pi 4 runs hot, especially when streaming video. Attach passive heatsinks to the CPU and RAM chips, or use a small cooling fan to prevent thermal throttling.

---

## 5. Potential Challenges to Anticipate

1. **Audio Routing:** Linux audio (ALSA/PulseAudio) can be notoriously finicky. Test your mic and speaker using simple terminal commands before running Python:
   - Test Mic: `arecord -d 5 test.wav`
   - Test Speaker: `aplay test.wav`
2. **Network Dependency:** Your system heavily relies on cloud APIs. Ensure the Pi is connected to a stable Wi-Fi network (or a mobile hotspot from your phone) during the demonstration.
3. **Latency:** Because the Pi has a slower Wi-Fi chip and processor than your PC, capturing the image and routing the network request might add 1-2 seconds of latency compared to your laptop.

## Next Steps
When you are ready to move the code to the Pi, I can help you write the `main_headless.py` script and the bash scripts needed to make the system start automatically when the Raspberry Pi turns on!
