import cv2  # type: ignore

#membaca file xml
face_ref = cv2.CascadeClassifier("face_ref.xml")

# Verify if the cascade file is loaded
if face_ref.empty():
    print("Error: Face cascade file not found or unable to load.")
    exit()

# buka kamera
camera = cv2.VideoCapture(1)

# mengecek apakah kamera sudah terbuka
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Data dummy untuk nama dan umur (bisa diganti dengan sistem pengenalan wajah yang lebih canggih)
person_info = {
    "default": {"name": "Unknown", "age": "??"},
    "1": {"name": "ozan", "age": "20"},
    "2": {"name": "Sarah", "age": "20"},
}

def face_detection(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_ref.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)  # Ubah jika perlu
    )
    return faces

def draw_boxes(frame):
    faces = face_detection(frame)
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        # Ambil informasi nama & umur (bisa dihubungkan ke sistem pengenalan wajah)
        person_id = str(i + 1) if str(i + 1) in person_info else "default"
        name = person_info[person_id]["name"]
        age = person_info[person_id]["age"]

        # Tampilkan nama dan umur di atas wajah
        text = f"Nama: {name}, Umur: {age}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def close_window():
    camera.release()
    cv2.destroyAllWindows()

def main():
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        frame = cv2.flip(frame, 1)  # Mirror effect
        draw_boxes(frame)
        cv2.imshow("ozancam", frame)

        # tekan 'q' untuk menutup
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    close_window()

if __name__ == '__main__':
    main()
