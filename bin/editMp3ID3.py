#!/usr/bin/env python
# -*- coding:utf-8 *-*

__author__ = "SL"
__version__ = "1.0"
__description_ = "修改MP3文件的ID3信息, 如标题, 编号, 作者, 专辑"


import os
# mutagen == 1.42.0
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK


class EditMp3ID3(object):
    def __init__(self, filePath):
        if not os.path.exists(filePath):
            print "%s Not exist" % filePath
            exit(1)

        self.filePath = filePath
        self.files = self._getFiles()
        self.audio = []

        self.info = dict(
            TIT2=None,
            TPE1=None,
            TALB=None,
            TRCK=None
        )


    def _getFiles(self):
        file_list = []
        for root, subdirs, files in os.walk(self.filePath):
            for file in files:
                filefullpath = os.path.join(root, file)
                """print filefullpath"""
                if os.path.split(filefullpath)[1][-4:] == ".mp3":
                    file_list.append(filefullpath)

        return file_list

    # 传入mp3、jpg的本地路径以及其他字符串
    def getSongInfo(self):
        filesAndaudio = []
        for f in self.files:
            ad = ID3(f)
            # print ad.get('TIT2')
            # print ad.get('TPE1')
            # print ad.get('TALB')
            # print ad.get('TRCK')
            filesAndaudio.append((os.path.split(f)[1], ad))
        return filesAndaudio

    def setSongInfo(self, audio, songtitle="", songartist="", songalbum="", songnumber="", songpicpath=None):
        # audio = ID3(songfilepath)
        audio.update_to_v23()  # 把可能存在的旧版本升级为2.3
        if songpicpath is not None:
            img = open(songpicpath, 'r')
            audio['APIC'] = APIC(  # 插入专辑图片
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Cover',
                data=img.read()
            )
            img.close()
        audio['TIT2'] = TIT2(  # 插入歌名
            encoding=3,
            text=[songtitle]
        )
        audio['TPE1'] = TPE1(  # 插入第一演奏家、歌手、等
            encoding=3,
            text=[songartist]
        )
        audio['TALB'] = TALB(  # 插入专辑名称
            encoding=3,
            text=[songalbum]
        )
        audio['TRCK'] = TRCK(  # 编号
            encoding=3,
            text=[songnumber]
        )
        audio.save()  # 记得要保存


if __name__ == '__main__':
    mp3Path = os.path.join("d:", u"/Music/鬼吹灯全集-艾宝良/鬼吹灯第1部1卷-精绝古城(48集全)64K珍藏版[讲播：艾宝良]")
    editMp3 = EditMp3ID3(mp3Path)
    ad = editMp3.getSongInfo()
    num = 0
    for f,a in ad:
        num += 1
        filename = f.split("]")[1].split(".")[0]
        other = u"艾宝良"
        bum = u"鬼吹灯第1部1卷-精绝古城"

        print f.split("]")[1].split(".")[0]
        editMp3.setSongInfo(a, filename, other, bum, u""+str(num))
