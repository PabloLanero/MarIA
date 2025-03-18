import cv2
import dlib
import numpy as np
import imutils
from imutils import face_utils

# Inicializar el detector de caras de dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Capturar video desde la cámara web
cap = cv2.VideoCapture(0)

# Definir el tamaño de la pantalla (simulado)
screen_width, screen_height = 1920, 1080

# Parámetros de la cámara (deben calibrarse para tu cámara)
focal_length = 20.0
camera_center = (500 // 2, 500 // 2)  # Centro del frame redimensionado
camera_matrix = np.array(
    [[focal_length * 500, 0, camera_center[0]],
     [0, focal_length * 500, camera_center[1]],
     [0, 0, 1]], dtype="double"
)

# Asumimos que no hay distorsión en la cámara
dist_coeffs = np.zeros((4, 1))

# Definir un modelo 3D de la cara para la estimación de la pose
model_points = np.array([
    (0.0, 0.0, 0.0),          # Punta de la nariz
    (0.0, -330.0, -65.0),     # Mentón
    (-225.0, 170.0, -135.0),  # Esquina izquierda del ojo izquierdo
    (225.0, 170.0, -135.0),   # Esquina derecha del ojo derecho
    (-150.0, -150.0, -125.0), # Esquina izquierda de la boca
    (150.0, -150.0, -125.0)   # Esquina derecha de la boca
])

# Función para estimar la pose de la cabeza
def estimate_head_pose(shape):
    # Puntos 2D de la imagen
    image_points = np.array([
        shape[30],  # Punta de la nariz
        shape[8],   # Mentón
        shape[36],  # Esquina izquierda del ojo izquierdo
        shape[45],  # Esquina derecha del ojo derecho
        shape[48],  # Esquina izquierda de la boca
        shape[54]   # Esquina derecha de la boca
    ], dtype="double")

    # Calcular la pose de la cabeza
    (success, rotation_vector, translation_vector) = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )

    return rotation_vector, translation_vector

# Función para estimar la dirección de la mirada
def estimate_gaze(eye_points, rotation_vector, translation_vector):
    # Calcular el centro del ojo
    eye_center = np.mean(eye_points, axis=0).astype(int)

    # Proyectar el centro del ojo en 3D
    eye_center_3d = np.array([[eye_center[0], eye_center[1], 0]], dtype="double")
    (nose_end_point2D, _) = cv2.projectPoints(
        eye_center_3d, rotation_vector, translation_vector, camera_matrix, dist_coeffs
    )

    # Mapear la dirección de la mirada a la pantalla
    gaze_x = int((nose_end_point2D[0][0][0] / 500) * screen_width)
    gaze_y = int((nose_end_point2D[0][0][1] / 500) * screen_height)

    return gaze_x, gaze_y

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar el frame para un procesamiento más rápido
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen en escala de grises
    faces = detector(gray, 0)

    for face in faces:
        # Predecir los puntos faciales
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Estimar la pose de la cabeza
        rotation_vector, translation_vector = estimate_head_pose(shape)

        # Extraer las coordenadas de los ojos
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        left_eye = shape[lStart:lEnd]
        right_eye = shape[rStart:rEnd]

        # Estimar la dirección de la mirada para cada ojo
        left_gaze = estimate_gaze(left_eye, rotation_vector, translation_vector)
        right_gaze = estimate_gaze(right_eye, rotation_vector, translation_vector)

        # Calcular el punto medio de la mirada
        gaze_x = (left_gaze[0] + right_gaze[0]) // 2
        gaze_y = (left_gaze[1] + right_gaze[1]) // 2

        # Mostrar la dirección de la mirada en la pantalla simulada
        print(f"Gaze Coordinates: ({gaze_x}, {gaze_y})")

        # Dibujar los contornos de los ojos
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # Dibujar un punto en la pantalla simulada
        cv2.circle(frame, (gaze_x // 4, gaze_y // 4), 5, (0, 0, 255), -1)

    # Mostrar el frame
    cv2.imshow("Gaze Recorder", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()