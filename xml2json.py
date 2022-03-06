import re
import os
import random
import translate

# 数据路径和输出路径
data_path = "D:\\SaveMe\\Baidu_SceneData\\"
out_path = "D:\\SaveMe\\data_dir\\"

# 分割长文本
def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

# 获取一个目录下的所有文件名/文件夹名
def get_all_dirs(data_path):
    dirs = os.listdir(data_path)
    childirs = []
    childname = []
    for dir in dirs:
        childir = data_path + str(dir)
        childirs.append(childir + "\\")
        childname.append(str(dir))
    return childirs, childname

# 获取目录下的所有xml文件名（带路径）
def get_all_xml(file_path):
    dirs = os.listdir(file_path)
    files = []
    for dir in dirs:
        if (dir[-1] == 'l'):
            files.append(file_path + str(dir))
    return files

# 提取xml文件中的所有xml，并将其分为train,dev,test三个文本，比例为7:2:1
def xml2chinese(data_path):
    pattern = re.compile("[\u4e00-\u9fa5]+")
    trainfile = open(out_path + "train.txt", 'w')
    devfile = open(out_path + "dev.txt", 'w')
    testfile = open(out_path + "test.txt", 'w')
    dirs, names = get_all_dirs(data_path)
    trainfile.write("label" + "\t" + "text_a" + "\n")
    devfile.write("label" + "\t" + "text_a" + "\n")
    testfile.write("label" + "\t" + "text_a" + "\n")
    allfile = open(out_path +"all.txt",'w')
    text = []
    count = 1
    # 开始循环，这里的label为文件夹名name
    for dir, name in zip(dirs, names):
        files = get_all_xml(dir)
        # 该文件夹的数目大于500个，取前五百
        if len(files) >= 500:
            files = files[0:500]
        for file in files:
            data = pattern.findall(open(file).read())
            # 如果有中文
            if data:
                # 用逗号连接
                data = ",".join(data)
                # 如果文本大于1000字符，只取前1000字符
                if len(data.__str__()) > 1000:
                    data = data[0:1000]
                text_a = name.__str__() + "\t" + data + "\n"
                text.append(text_a)
                allfile.write(text_a)
            print(file, "   ",count, " over!!!")
            count += 1
    # 打乱文本
    random.shuffle(text)
    # 写入文件
    dev_len, test_len = int(len(text) * 3 / 10), int(len(text) / 10)
    for i in range(0, len(text)):
        if i <= test_len:
            testfile.write(text[i])
        elif i <= dev_len:
            devfile.write(text[i])
        else:
            trainfile.write(text[i])

    return text

# 提取所有键值对，比较混乱，这里用了其他文件的翻译技术。
def xml2node(data_path):
    pattern = re.compile("=\".*?\"")
    pattern2 = re.compile("[\u4e00-\u9fa5]+")
    trainfile = open(out_path + "train.txt", 'w')
    devfile = open(out_path + "dev.txt", 'w')
    testfile = open(out_path + "test.txt", 'w')
    allfile = open(out_path +"all.txt",'w')
    trainfile.write("label" + "\t" + "text_a" + "\n")
    devfile.write("label" + "\t" + "text_a" + "\n")
    testfile.write("label" + "\t" + "text_a" + "\n")
    dirs, names = get_all_dirs(data_path)
    text = []
    ctext = []
    for dir, name in zip(dirs, names):
        files = get_all_xml(dir)
        if len(files) >= 500:
            files = files[0:500]
        for file in files:
            nodes = pattern.findall(open(file).read())
            data = pattern2.findall(open(file).read())
            sets = set()
            for node in nodes:
                if not pattern2.findall(node):
                    sets.add(node[2:-2])
            if data:
                data = ",".join(data)
                if len(data.__str__()) > 1000:
                    data = data[0:1000]
                trandata = translate.connect(data)
                text_a = name.__str__() + "\t" + trandata + "\n"
                ctext.append(text_a)
                print(trandata)
                sets.add(trandata)
                allfile.write(name + "\t" + ",".join(sets) + "\n")
            text.append(name + "\t" + ",".join(sets) + "\n")
            print(file + "over!!!")

    random.shuffle(text)
    random.shuffle(ctext)
    dev_len, test_len = int(len(text) * 3 / 10), int(len(text) / 10)
    for i in range(0, len(text)):
        if i <= test_len:
            testfile.write(text[i])
        elif i <= dev_len:
            devfile.write(text[i])
        else:
            trainfile.write(text[i])

    return


