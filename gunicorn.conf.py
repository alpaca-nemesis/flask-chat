# ./gunicorn.conf.py
workers = 1    # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
bind = "0.0.0.0:8088"
