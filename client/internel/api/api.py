import hashlib
import requests
import json
import os
import config

from internel.utils.aes import AES
from internel.utils.sha1 import SHA1


class Session(object):
    """
    错误代码：
        1 —— 连接成功
        0 —— 连接失败
    """
    error = 0
    def __init__(self, url_prefix, token, password):
        # 连接服务器
        self.url_prefix = url_prefix
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict({"token": token})
        try:
            rsp = self.session.get(self.url_prefix + "/ping")
            if rsp.status_code == 200:
                self.error = 1
        except requests.exceptions.ConnectionError:
            return

        # 读取磁盘中存储的用于加密文件的key
        with open(config.WORK_DIR+"/key/key", "rb") as f:
            cipher = f.read()
            aes = AES(SHA1(password.encode()).digest()[:16])
            self.key = aes.decrypt(cipher)
            self.aes = AES(self.key)

    def upload_file(self, file_path):
        # 判断文件是否存在，并读取文件内容
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist!")
            return None
        elif not os.path.isfile(file_path):
            print(f"{file_path} is not a file!")
            return None
        with open(file_path, "rb") as f:
            msg = f.read()
            cipher = self.aes.encrypt(msg)
            checksum = SHA1(cipher).hexdigest()
        path,filename = os.path.split(file_path)
        files = {"file": (filename,cipher)}
        rsp = self.session.post(self.url_prefix + '/upload', files=files, data={'checksum': checksum})
        # 处理响应
        body = json.loads(rsp.content)
        if rsp.status_code != 200:
            return f"Failed to upload file {file_path}, error msg: {body['msg']}"
        if "file exists" in body['msg']:
            return body['msg']
        return "上传成功"

    def download_file(self, id, file_name):
        file_path = os.path.join(config.WORK_DIR,"download",file_name)
        if os.path.isfile(file_path):
            return "因下载目录存在同名文件下载失败"
        else:
            rsp = self.session.get(self.url_prefix + "/download/" + str(id))
            if not rsp.status_code == 200:
                return json.loads(rsp.content)['msg']
            # 解密
            msg = self.aes.decrypt(rsp.content)
            # 保存
            with open(file_path, "wb") as f:
                f.write(msg)
            return "下载成功"


    def get_files(self):
        rsp = self.session.get(self.url_prefix + "/files")
        if rsp.status_code != 200:
            return None, rsp.content
        return json.loads(rsp.content)["data"], None

    def delete_file(self, id):
        rsp = self.session.delete(self.url_prefix + "/file/" + str(id))
        if rsp.status_code != 200:
            return json.loads(rsp.content)['msg']
        return "删除成功"


def test():
    s = Session("http://127.0.0.1:8081/api/v1", "jylsec", "jylsec")

    # 获取所有文件
    files, error = s.get_files()
    if error:
        print(error)
    else:
        print(files)

    # 上传文件
    error = s.upload_file("/Users/Soreat_u/Desktop/Hash Collisions.md")
    if error:
        print(error)
    else:
        print("Upload file success!")

    # 下载文件
    error = s.download_file(2, "/Users/Soreat_u/Desktop/Hash Collisions copy.md")
    if error:
        print(error)
    else:
        print("Download file success!")

    # 删除文件
    error = s.delete_file(2)
    if error:
        print(error)
    else:
        print("Delete file success")


if __name__ == "__main__":
    test()