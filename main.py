import os
import re
import sys

import music_tag

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('参数不正确，将专辑信息写入album_info.txt，再运行\npython main.py [专辑文件夹绝对路径]')
        exit(-1)
    dir_path = sys.argv[1]
    album_info = {}
    with open('album_info.txt', 'r', encoding='utf-8') as f:
        album_info['artist'] = f.readline()  # 第一行，作者
        album_info['album'] = f.readline()  # 第二行，专辑名
        l = f.readline()  # 后续，每首歌歌名
        album_info['titles'] = []
        while l:
            album_info['titles'].append(l.strip())
            l = f.readline()
    files = os.listdir(dir_path)
    musics = []
    pattern = re.compile('.*\\.(aac|aiff|dsf|flac|m4a|mp3|ogg|opus|wav|wv)$')
    for f in files:
        if pattern.match(f):
            musics.append(os.path.join(dir_path, f))
    if len(album_info['titles']) != len(musics):
        print(f'文件夹{dir_path}中文件数量与album_info.txt中的信息不匹配')
        exit(-1)
    for (f, title) in zip(musics, album_info['titles']):
        f = music_tag.load_file(f)
        f['title'] = title
        f['artist'] = album_info['artist']
        f['album'] = album_info['album']
        f.save()
