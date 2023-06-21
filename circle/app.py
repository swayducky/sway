from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This will allow all origins, you can customize to restrict access


@app.route('/api/images', methods=['GET'])
def get_images():
    root_path = 'static/_images'
    root_dir = os.path.join(os.getcwd(), root_path)
    dir_dict = {}

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                rel_dir = os.path.relpath(subdir, root_dir)
                if rel_dir not in dir_dict:
                    dir_dict[rel_dir] = []
                dir_dict[rel_dir].append(os.path.join(root_path, rel_dir, file))
    for value in dir_dict.values():
        value.sort()
    return jsonify(dir_dict)

if __name__ == '__main__':
    app.run(debug=True)
