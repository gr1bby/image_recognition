import face_recognition

from PIL import Image


ROTATION_ANGLES = (0, 90, 180, 270)


def get_face(path: str, face_path: str) -> None | str:
    for angle in ROTATION_ANGLES:
        img = Image.open(path)
        rotated = img.rotate(angle=angle, expand=True)
        rotated.save(path)

        image = face_recognition.load_image_file(path)
        faces_locations = face_recognition.face_locations(image)

        if faces_locations:
            for face_location in faces_locations:
                top, right, bottom, left = face_location

                face_image = image[top:bottom, left:right]

                pil_img = Image.fromarray(face_image).resize((150, 150))
                pil_img.save(face_path)
                return None

    return 'Face not found! Try again!'
