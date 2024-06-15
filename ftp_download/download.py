import os
from ftplib import FTP_TLS
import json
from pathlib import Path
import tqdm


# 下载文件
def download(remote, local):
    local_file = local / (name := Path(remote).name)
    size = ftps.size(remote)
    print("正在下载文件%s\n文件大小%.2fMB" % (name, (size_MB := (size/(10**6)))))
    f = open(local_file, 'wb')
    chunk_size = 0.008192
    bar_format = "{desc}: {percentage:3.0f}%|{bar}|{n:.2f}MB/{total:.2f}MB  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"

    def write_file(byte):
        f.write(byte)
        pbar.update(chunk_size)

    with tqdm.tqdm(desc="下载进度", total=size_MB, unit='MB', bar_format=bar_format) as pbar:
        ftps.retrbinary(f'RETR {remote}', write_file)

    f.close()


# 获取文件大小信息
def get_inf(remote_dir):
    d = ftps.nlst(remote_dir)
    return max(d)


with open("config.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

# 登录ftps服务器
ftps = FTP_TLS()
ftps.connect(data["Host"])
ftps.set_debuglevel(data["Debug"])
ftps.login(data["User"], data["Password"])
ftps.prot_p()

files = data["File_Position"]
for r, l in files.items():
    download_file = get_inf(r)
    local_folder = Path(l)
    if Path(download_file).name in os.listdir(local_folder):
        print("文件重复，不需下载")
    else:
        download(download_file, local_folder)
ftps.close()
