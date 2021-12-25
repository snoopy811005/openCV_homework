import cv2

cap = cv2.VideoCapture('./video/videoplayback.mp4')  # play video file
FPS = cap.get(cv2.CAP_PROP_FPS)  # Frame Per Second
F_Count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # frame count
print(f'FPS : {FPS:.2f} ms, Frame_Count : {F_Count}')

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
ratio = cap.get(cv2.CAP_PROP_FRAME_WIDTH) / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # cap.get得到相機/視訊檔案的屬性
w = 400
h = int(w / ratio)
cv2.resizeWindow('frame', w, h)  # change frame size

fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 編碼
# 建立 VideoWriter 物件，輸出影片至 output.mp4，FPS 值為 23.95
out = cv2.VideoWriter('./output.mp4', fourcc, FPS, (w, h))

counter = 0
while cap.isOpened():
    counter += 1

    ret, frame = cap.read()
    if not ret: break

    if counter <= 100:
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, '1.flip(horizontal)', (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif counter > 100 and counter <= 200:
        frame = cv2.Canny(frame, 100, 200)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        cv2.putText(frame, '2.canny(edge)', (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    elif counter > 200 and counter <= 300:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cv2.putText(frame, '3.rotate(90)', (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif counter > 300 and counter <= 400:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        T, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
        frame = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        cv2.putText(frame, '4.GaussianBlur', (40, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, '5.threshold', (40, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame, '6.BGRtoRGB', (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    c = cv2.waitKey(25)  # 25 ms per frame     1/FPS
    if not ret or c == 27:  # key escape
        break

    frame = cv2.resize(frame, (w, h))
    cv2.imshow('frame', frame)
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)