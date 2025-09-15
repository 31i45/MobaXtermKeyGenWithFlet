# MobaXterm 许可证生成器

一个使用 Flet (基于 Python) 开发的简单 MobaXterm 许可证生成工具。

缺点，flet 不能设置应用左上角的 logo，打包成的 Windows 应用比较大。

## 安装依赖
```bash
pip install flet
```

## 运行程序
```bash
python .\mobaxterm_keygen_flet.py
```

## 打包成可执行文件
```bash
pyinstaller --clean MobaXterm_keygen_flet.spec
```