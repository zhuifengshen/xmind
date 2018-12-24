# XMind
**XMind** 是基于 Python 实现，提供了对 **XMind 思维导图**进行创建、解析、更新的一站式解决方案！

#### 1、支持原生以下功能的创建和解析
- 画布
- 话题
- 图标
- 标签
- 备注
- 批注
- 联系
- 样式

#### 2、支持
- 支持转换为Dict/Json数据格式（转换级别：文件级别、Sheet级别、话题级别、评论级别）
- 支持多种保存方式（直接覆盖更新、另存为更新、只保存核心内容content.xml、只保存内容和样式content.xml & comments.xml & styles.xml、不保存更新记录节约内存、默认保存所有内容）

### 一、安装方式
```
pip install XMind
```

### 二、版本升级
```
pip install -U XMind
```

### 三、使用方式
```
# load an existing file or create a new workbook if nothing is found
workbook = xmind.load("demo.xmind")
# get the first sheet(a new workbook has a blank sheet by default)
sheet1 = workbook.getPrimarySheet()
design_sheet1(sheet1)
# create sheet2
gen_sheet2(workbook, sheet1)
# now we save as test.xmind
xmind.save(workbook, path='test.xmind')
```


### 四、自动化测试与发布

#### 1、自动化单元测试
```
python3 -m unittest discover
```

#### 2、一键打 Tag 并上传至 PYPI 
每次在 __about__.py 更新版本号后，运行以下命令，实现自动化更新打包上传至 [PYPI](https://pypi.org/) ，同时根据其版本号自动打 Tag 并推送到仓库：
```
python3 setup.py pypi
```


### 五、致谢
在此，衷心感谢 **XMind 思维导图**官方创造了如此高价值的产品，同时还开源 [xmind-sdk-python](https://github.com/xmindltd/xmind-sdk-python) ，本项目正是基于此工具进行扩展和升级，受益匪浅，感恩！
后续，也将继续根据实际项目需要，定期进行维护更新和完善，欢迎大伙的使用和意见反馈，谢谢。

（如果本项目对你有帮助的话，欢迎 _**star**_ ）


```
The MIT License (MIT)

Copyright (c) 2013 XMind, Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
