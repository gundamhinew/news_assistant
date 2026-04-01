# 国际政经新闻选题程序（GUI）

## 运行

```bash
pip install -r requirements.txt
python src/app.py
```

点击“开始”后，程序会自动抓取配置来源，执行24小时优先（不足扩展48小时）筛选，生成：

- `output/candidates_100.txt`
- `output/candidates_25.txt`

## 当前版本能力

- 全来源池内置（按你给定媒体顺序）
- 自动抓取（RSS优先，主页链接兜底）
- 多标签主题分类 + 主主题输出
- 去重（链接去重 + 标题近似 + 事件近似）
- 100条大列表 + 25条小列表
- GUI一键执行
