from ftplib import FTP_TLS
import ftplib
from pathlib import Path
import json


def dir_exist(remote_dir):  #判断文件夹是否存在
    remote_dir_parent = remote_dir.parent
    dirs = []
    def get_dirs(resp):
        nonlocal dirs
        for i in resp.split('\n'):
            if i[0]=='d':
                dirs.append(i.split()[-1])
    ftps.dir(remote_dir_parent.as_posix(), get_dirs)
    if remote_dir.name in dirs:
        return True
    else:
        return False

def make(remote_dir, path=None): # '/1/2/3/4'
    print(remote_dir)
    dir_to_make=remote_dir.as_posix()
    if dir_exist(remote_dir.parent):
        ftps.mkd(dir_to_make)
        return dir_to_make
    else:
        ftps.mkd(make(remote_dir.parent, remote_dir))
        return path.as_posix()
        
    
    
    
    
def make_dir(remote_path, path=None): #'/1/2/3'
    print(f"正在对{remote_path}操作")
    parent_path = remote_path.parent
    def dir_exist(x):
        nonlocal dirs
        for i in x.split('\n'):
            if i[0]=='d':
               dirs.append(i.split()[-1]) 
    dirs = []
    ftps.dir(parent_path.as_posix(), dir_exist)
    if remote_path.name in dirs:                        # 如果该文件夹已经存在，停止函数
        print(f'{remote_path.as_posix()}已存在')
        return True
    else:
        print(f'{remote_path.as_posix()}不存在')
        try:
            ftps.mkd(remote_path.as_posix())
            print(f'{remote_path.as_posix()}创建成功')
            return path
        except ftplib.error_perm:
            print('无法创建')
            ftps.mkd(make_dir(parent_path, remote_path))

    
with open('../config.json','r', encoding='utf-8') as js:
    data = json.load(js)

ftps = FTP_TLS()
ftps.set_debuglevel(data['debug_level'])
ftps.connect(data['host'], data['port'])
ftps.login(data['user'],data['password'])
ftps.prot_p()

for local, remote in data['local_remote'].items():
    local_file_path = Path(local)
    remote_file_path = (Path(remote) / local_file_path.name).as_posix()
    with open(local_file_path, 'rb') as f:
        ftps.storbinary(f'STOR {remote_file_path}', f)
ftps.close()