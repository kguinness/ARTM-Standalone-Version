import cv2


def test_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Error: Unable to open camera at index {index}.")
        return
    print(f"Camera at index {index} opened successfully.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame not captured!")
            break

        cv2.imshow("Camera Test", frame)
        # Press 'q' to quit the window.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test_camera(0)
