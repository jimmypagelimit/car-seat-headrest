# Car Seat Headrest 资料库

这是一个关于 Car Seat Headrest 一切的一切的乐队资料库，使用 SQLite 直接存储乐队、专辑、歌曲和成员等信息。

## 本地运行

```bash
python3 database.py        # 创建数据库与初始数据
python3 scrape.py          # 从 MusicBrainz 抓取专辑数据并入库
python3 app.py             # 启动展示页面：http://localhost:8000
```

抓取脚本使用公开的 MusicBrainz API，并保留来源 URL；请遵守其服务条款与请求频率限制。页面无需第三方 Python 依赖。
