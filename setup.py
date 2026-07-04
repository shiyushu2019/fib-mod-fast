#!/usr/bin/env python
# setup.py
import sys
import glob
from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import os

# 1. 提取所有 .pyx 文件名参数
pyx_files = [arg for arg in sys.argv[1:] if arg.endswith('.pyx')]

# 2. 从 sys.argv 中移除这些文件
for arg in pyx_files:
    sys.argv.remove(arg)

# 3. 如果没有找到 .pyx，则自动搜索当前目录
if not pyx_files:
    pyx_files = glob.glob('*.pyx')
    if not pyx_files:
        print("错误：没有找到 .pyx 文件，请指定要编译的文件。")
        sys.exit(1)

# 4. 自动补全 setuptools 参数
if not any(arg in sys.argv for arg in ['build_ext', '--help', '-h', '--version']):
    sys.argv.insert(1, 'build_ext')
    sys.argv.insert(2, '--inplace')

# 5. 构建 Extension 对象列表，显式链接 GMP 库
extensions = []
for pyx in pyx_files:
    # 模块名 = 文件名去掉 .pyx
    module_name = pyx.replace('.pyx', '')
    ext = Extension(
        module_name,
        sources=[pyx],
        libraries=['gmp', 'mpfr', 'mpc'],
        library_dirs=['/data1/conda_envs/jssnu005/sys/play/lib'],  # 就是这个！
    )
    include_dirs=['/data1/conda_envs/jssnu005/sys/play/include']
    extensions.append(ext)

# 6. 调用 cythonize 并执行 setup
setup(ext_modules=cythonize(extensions))