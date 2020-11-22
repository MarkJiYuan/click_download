import os
import time
import base64

from flask import (
    Flask,
    url_for,
    render_template,
    request,
    send_from_directory,
    abort
)
from flask_cors import CORS
from click_encrypt import getcryptor
from click_orm import File, create, update, retrieve, delete

from configparser import ConfigParser
cp = ConfigParser()
cp.read(os.path.abspath('settings.conf'))

host = cp.get('flask_app', 'host')
port = cp.get('flask_app', 'port')


file_type_map = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "image/png": "png",
    "image/jpeg": "jpeg",
    "text/markdown": "md",
    "application/msword": "doc",
    "application/zip": "zip",
    "application/vnd.rar": "rar",
    "application/x-7z-compressed": "7z"
}

app = Flask(__name__)
CORS(app)
directory = os.path.join(os.path.dirname(__file__), 'files/')
aescryptor = getcryptor()

@app.route('/home')
def index():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['upload_file']

    # 文件名
    name = f.filename.split(".")[0]
    # 文件后缀
    filetype = file_type_map.get(f.mimetype, None)

    # 文件密钥
    text = name[:15] + str(round(time.time(), 6))
    en_text = aescryptor.aesencrypt(text)
    en_text = base64.urlsafe_b64encode(en_text).decode("utf-8")
    
    # 保存数据库
    data = {
        "name": name,
        "filetype": filetype,
        "path": "",
        "en_text": en_text,
        "count": 3
    }
    row_num = create(data)

    # 用id和时间戳生成文件名
    path = f"{row_num}_{time.time()}"

    # 存储文件
    abspath = os.path.abspath(f"files/{path}")
    f.save(abspath)

    # 更新数据库记录的path
    update(File.id == row_num, {"path": path})

    return {
        "download_link": f"{host}:{port}/download?en_text={en_text}"
    }
    
@app.route('/download', methods=['GET'])
def download_file():
    en_text = request.args.get("en_text")

    result = retrieve(File.en_text == en_text).one_or_none()
    if not result:
        return "file not exists"
    elif result.count == 0:
        delete(File.id == result.id)
        os.remove(os.path.join(directory, result.path))
        return "file not exists"
    else:
        filename = result.name
        filetype = result.filetype
        update(File.id == result.id, {"count": result.count - 1})

        return send_from_directory(directory=directory, 
                                   filename=result.path, 
                                   as_attachment=True, 
                                   attachment_filename=f"{filename}.{filetype}")
            
    abort(404)


if __name__ == '__main__':
    from waitress import serve
    serve(app, listen=f'*:{port}')





