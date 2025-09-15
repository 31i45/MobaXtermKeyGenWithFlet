# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

# 排除不必要的模块以减小体积
excluded_modules = [
    # 核心排除
    'flet_core.web',  # 排除Flet的Web部分
    # 标准库排除
    'email', 'http', 'xml', 'html', 'calendar', 'sqlite3',
    'pydoc', 'doctest', 'pdb', 'inspect', 'unittest',
    'turtle', 'antigravity', 'this', 'zoneinfo',
    'decimal', 'fractions', 'statistics', 'ipaddress',
    'ctypes', 'winsound', 'msvcrt', 'mmap',
    # 第三方库排除
    'matplotlib', 'numpy', 'pandas', 'scipy', 'sklearn',
    'tkinter', 'PIL', 'PyQt5', 'pyside2', 'wxPython',
    'requests', 'urllib3', 'flask', 'django',
    'cryptography', 'paramiko', 'tensorflow', 'torch',
    # 新增可排除的模块
    'pydantic',  # 从日志看这是实验性模块且可能不需要
    'uvicorn', 'websockets',  # 这些是Web服务器相关模块
    'pygments',  # 代码高亮模块，可能不需要
    'setuptools',  # 可以尝试排除部分setuptools相关内容
]

# 分析阶段配置
a = Analysis(
    ['mobaxterm_keygen_flet.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],  # 移除未找到的隐藏导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    cipher=block_cipher,
    noarchive=True,  # 不创建archive文件以减小体积
)

# PYZ阶段配置 - 最大优化
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
    optimize=2  # 最大优化级别
)

# EXE阶段配置 - Windows平台优化
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MobaXterm许可证生成器',
    debug=False,
    bootloader_ignore_signals=True,
    upx=True,    # 启用UPX压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 无控制台窗口
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mobaxterm.ico',  # 应用图标
)