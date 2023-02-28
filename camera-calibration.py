import numpy as np
import cv2
import yaml

# Termination criteria
criteria = (cv2 .TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# Prepare object points
objp = np.zeros(( 6 * 7, 3), np.float32)
objp[:,:2] = np.mgrid[ 0 : 7 , 0 : 6 ].T.reshape(-1 ,2)
# Arrays to store object points and image points from all the images .
objpoints = [ ] # 3d point in real world space
imgpoints = [ ] # 2d points in image plane .
cap = cv2.VideoCapture(0)
found = 0
while(found < 10): # This value can be changed
    ret, img = cap . read ( ) # Capture frame-by-frame
    gray = cv2 . cvtColor ( img , cv2 .COLOR_BGR2GRAY)
# Find the chessboard corners
    ret, corners = cv2 . findChessboardCorners(gray, (7, 6), None)
# If found, add object points and image points
    if ret == True :
        objpoints.append(objp) # Every loop objp is the same, in 3D

        corners2 = cv2.cornerSubPix(gray , corners, (11 ,11) , (-1 ,-1) , criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        img = cv2.drawChessboardCorners (img, (7, 6), corners2, ret)
        found += 1

    cv2 . imshow('img', img )
    cv2 . waitKey ( 10 )

# Release the capture
cap.release()
cv2.destroyAllWindows()
ret, mtx, dist ,rvecs ,tvecs = cv2.calibrateCamera(objpoints, imgpoints,
gray.shape[ : : -1], None, None)

# Transform the matrix to list and save as .yaml
data = {'camera-matrix' : np.asarray(mtx).tolist(), 'dist_coeff' :
np.asarray(dist).tolist()}
with open ("calibration.yaml", "w") as f :
    yaml.dump(data, f)
