# 基础镜像
FROM python:3.8-slim-bullseye

# 工作目录
WORKDIR /app

# 修改源
ADD sources.list /etc/apt/

# 安装 tzdata 包并设置时区
RUN apt-get update && apt-get install -y tzdata vim
ENV TZ=Asia/Shanghai

# 复制项目文件到容器中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install eventlet

# 暴露端口
#EXPOSE 5000
EXPOSE 8000

# 运行应用
#CMD ["python", "app.py"]
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
