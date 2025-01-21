import cv2

camera_index = 2  # Cambia según el índice de tu cámara
cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer la cámara.")
        break

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

