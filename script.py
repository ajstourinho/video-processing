import cv2
import numpy as np
from datetime import datetime 

# print("Current Time =", datetime.now().strftime("%H:%M:%S"))

H = 720
W = 1280

# Read input video
cap = cv2.VideoCapture('input_video.mp4')

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Read the first frame of the video
ret, frame = cap.read()

# Display the first frame and let the user select 4 points
points = []
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow("frame", frame)
        
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", mouse_callback)

while len(points) < 4:
    cv2.imshow("frame", frame)
    cv2.waitKey(1)


# Define the mask based on the selected points
mask = np.zeros((height, width), dtype=np.uint8)
pts = np.array([points], dtype=np.int32)
cv2.fillPoly(mask, pts, (255))

# Define the output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (H, W), isColor=True)


# Process each frame of the video
frame_count = 0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 10 == 1:
        # Apply the mask to the frame
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Define the perspective transform matrix
        dst_points = np.array([[0, 0], [H, 0], [H, W], [0, W]], dtype=np.float32)
        src_points = np.array(points, dtype=np.float32)
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # Apply the perspective transform to the masked frame
        warped = cv2.warpPerspective(masked, M, (H, W))
        
        # Write the warped frame to the output video
        out.write(warped)
        
        print(f'Processed frame {frame_count} of {total_frames}')
    # # Display the output video
    # cv2.imshow("output", warped)
    # cv2.waitKey(1)

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# print("Current Time =", datetime.now().strftime("%H:%M:%S"))
