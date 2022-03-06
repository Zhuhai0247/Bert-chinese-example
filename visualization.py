from visualdl import LogWriter
from visualdl import LogReader

reader = LogReader(file_path='D:\\SaveMe\\shuffle,bs=16,chinese,0-500,1000\\visualization\\vdlrecords.1646539506.log')
tags = reader.get_tags()
data = reader.get_data('scalar', 'EVAL/acc')
print(data,tags)


'''
if __name__ == '__main__':
    value = [i/1000.0 for i in range(1000)]
    # 初始化一个记录器
    with LogWriter(logdir="D:\\SaveMe\\reshuffle,bs=16,chinese\\visualization\\") as writer:
        for step in range(1000):
            # 向记录器添加一个tag为`acc`的数据
            writer.add_scalar(tag="acc", step=step, value=value[step])
            # 向记录器添加一个tag为`loss`的数据
            writer.add_scalar(tag="loss", step=step, value=1/(value[step] + 1))
'''
