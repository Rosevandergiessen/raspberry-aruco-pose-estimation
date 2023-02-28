import numpy as np
import cv2
import scipy.io as sio
import time
cap = cv2.VideoCapture(0)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
camera_matrix = np.array([[455.02997185573196, 0.0, 304.25823494844855],
[0.0, 449.08945487685196, 270.4636881649448], [0.0, 0.0, 1.0]])
dist_coeff = np.array([0.6355568969455541, -4.812966487663507,
0.04144806239501737, -0.020533499220346838, 10.667183912534734])
t = time.time()

# sample every ’h ’ seconds
h = 0.2

# T is total experiment time in seconds
T = 10
N = int(T/h)
data_time = np.zeros([N, 1])
data_trans = np.zeros([N, 3])
data_rots = np.zeros([N, 3])
data_img = np.zeros([N, 480 , 640]).astype(np.uint8)
starttime = time.time()
for i in range (N) :
    data_time[i , 0] = time.time() - starttime

# Capture frame-by-frame
ret, frame = cap.read()

# Operat ions on the frame come he r e
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Marker Tracking
res = cv2.aruco.detectMarkers(gray, dictionary)
# Draw marker , e s t ima t e pose , draw a x i s .
if len (res[0]) > 0 :
    cv2.aruco.detectMarkers(gray, res[0], res[1], (0 , 255, 127))
    rvecs, tvecs, _objPoints= cv2.aruco.estimatePoseSingleMarkers
    (res[0], 0.05, camera_matrix, dist_coeff)
    cv2 . aruco . drawAxis(gray, camera_matrix, dist_coeff, rvecs, tvecs, 0.1) ;
    print('rotation', rvecs)
    print('translation', tvecs)
    data_trans [i, :] = tvecs[:][:]
    data_rots [i, :] = rvecs[:][:]
    data_img [i, :, :] = gray
elif i > 0 :
    data_trans[i, :] = data_trans[ i-1, :]
    data_rots[i, :] = data_rots[ i-1, :]
    data_img[i, :, :] = gray
# Display the resulting frame - press q to quit
cv2.imshow('frame', gray)
if cv2.waitkey(1) & 0xFF == ord('q') :
    pausetime = np.max(np.array([0, h-(time.time() - t)]))
time.sleep(pausetime)
print(time.time() -t)
t = time.time()
print(data_time)
print(data_rots)
print(data_trans)
# Create .matfile with rotations array, translation  array & captured video
sio.savemat( 'Rotation_Translation.mat' , dict(vidframes=data_img ,
rmat=data_rots , tmat=data_trans, timemat=data_time))
imsize = gray.shape
# Re l eas e the captur e
cap.release()
cv2.destroyAllWindows()
