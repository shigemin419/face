from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import cv2

app = Flask(__name__)

# アップロードされた画像を保存するディレクトリ
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                return render_template('index.html', uploaded_image=file.filename)
    return render_template('index.html')

@app.route('/detect_faces/<filename>')
def detect_faces(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔検出用のカスケード分類器をロード
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # 検出された顔に矩形を描画
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 結果の画像を保存
    processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
    cv2.imwrite(processed_filepath, img)

    return render_template('index.html', uploaded_image=filename, processed_image='processed_' + filename)

if __name__ == '__main__':
    app.run(debug=True)
