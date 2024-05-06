import json
from werkzeug.utils import secure_filename
import os, base64, imghdr, re
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
# import face_recognition
# from PIL import Image
# from io import BytesIO
# import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

mime_extensions = {
        'image/png': 'png',
        'image/jpeg': 'jpg',
        'image/gif': 'gif',
}

def upload_photo(file, path):
    if file.filename == '':
            return False

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        return True
    else:
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getExtension(encoded_string):
    mime_match = re.search(r'^data:(.*?);', encoded_string)
    if mime_match:
        mime_type = mime_match.group(1)
        
        if mime_type in mime_extensions:
            return mime_extensions[mime_type]
    return None

def upload_base64(encoded_string, path, filename):
    try:
        d = encoded_string.split(',')
        extension = getExtension(d[0])
        binary_data = base64.b64decode(d[1])
        filename = filename +'.'+ extension
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(binary_data)
        return True
    except Exception as e:
        print("Une erreur est survenue lors de l'upload du fichier :", e)
        return False

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
            base64_data = base64.b64encode(image_data)
            base64_string = base64_data.decode('utf-8')
            return base64_string
    except Exception as e:
        print("Erreur lors de la conversion de l'image en base64 :", str(e))
        return None


def roles_required(*roles):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get("roles", [])
            print(user_roles,roles)
            if any(role in user_roles for role in roles):
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized"}), 403
        return decorator
    return wrapper

def getMonId():
    current = get_jwt_identity()
    return json.loads(current)['id']


# def reconnaissance_faciale(user_photos,photo):
#     images = [face_recognition.load_image_file(p) for p in user_photos]
#     encoded_images = [face_recognition.face_encodings(img)[0] for img in images]

#     a_trouver = base64_toencode(photo)
#     results = face_recognition.compare_faces(encoded_images, a_trouver)
#     print(results)
#     return results

# def base64_toencode(photo):
#     image_data = base64.b64decode(photo)

#     image_2 = Image.open(BytesIO(image_data))
#     image_2_np = np.array(image_2)
#     face_encodings_2 = face_recognition.face_encodings(image_2_np)

#     if len(face_encodings_2) > 0:
#         face_encoding_2 = face_encodings_2[0]
#         return face_encoding_2
#     else:
#         print("Aucun visage n'a été détecté dans l'image.")
#         return False

# def login_faciale(users, photo):
#     photos = [user.photo for user in users]
#     results = reconnaissance_faciale(photos,photo)
#     for i in range(len(results)):
#         if results[i] == True:
#             return users[i]
#     return None
