import os
import md2xmind

# md格式的源文件路径
file_path = os.path.abspath(os.path.join(os.getcwd(), 'test.md'))

# 第一个参数是源文件
# 第二个参数是生成的文件名称，生成的文件位于运行命令行的文件夹中
md2xmind.start_trans_file(file_path, 'test2','test2')
