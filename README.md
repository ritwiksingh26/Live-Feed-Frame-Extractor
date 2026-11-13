# Live Feed Frame Extractor

A small Flask web app that opens your webcam in the browser, captures frames from the live feed, and saves them on the server as timestamped PNG images using OpenCV.

## Tech stack

Python · Flask · OpenCV · NumPy · HTML/JavaScript (`getUserMedia`, `fetch`)

## Run it locally

```bash
pip install flask opencv-python numpy
python camera.py
```

Then open http://127.0.0.1:5000 and allow camera access. Captured frames are saved to the `images/` folder.
