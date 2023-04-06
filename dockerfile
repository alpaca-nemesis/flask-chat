# 基于的基础镜像，这里使用python，开发版本是 3.x ，基础镜像也写 3.x 就可以，这样可以保持版本一致，避免 Python 版本差异带来的问题
FROM python:3.10
# /app 是要部署到服务器上的路径
WORKDIR /app
# Docker 避免每次更新代码后都重新安装依赖,先将依赖文件拷贝到项目中
COPY requirements.txt requirements.txt
# 执行指令，安装依赖
RUN pip install -r requirements.txt
# COPY指令和ADD指令功能和使用方式类似。只是COPY指令不会做自动解压工作。
# 拷贝项目文件和代码
COPY . .
# 执行指令，字符串间是以空格间隔
CMD ["gunicorn", "main:app", "-c", "./gunicorn.conf.py"]
