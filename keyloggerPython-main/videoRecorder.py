# --------------------------------------------------------------------------------------------------------
#                                         IMPORTING LIBRARIES

import cv2
import mysql.connector
import os
# --------------------------------------------------------------------------------------------------------

def record_video(output_file, duration=10):
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        with open("log.txt", "a") as f:
            f.write("\n\nUser Opened Camera.\nCould not record video due to some problem.\n")
        return

    # Get the default frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    print("Recording...")

    # Record video for the specified duration
    start_time = cv2.getTickCount()
    while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
        ret, frame = cap.read()
        if ret:
            # Write the frame
            out.write(frame)
        else:
            break

    # Release everything when the job is finished
    cap.release()
    out.release()
    print("Recording finished.")
    print("Recording finished.")

    # --- database code ---
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Zuhu@12#7sp",
        database="keylogger"
    )

    cursor = conn.cursor()

    filepath = os.path.abspath(output_file)

    query = "INSERT INTO video (Filename, Filepath) VALUES (%s, %s)"
    cursor.execute(query, (output_file, filepath))

    conn.commit()

    print("Video path stored in database")
# if __name__ == "__main__":
#     output_file = 'output.avi'
#     record_video(output_file, duration=10)  # Record for 10 seconds
