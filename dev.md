# dev.md
这个文件仅开发（仅dev分支可见）


我的思路是先定义一些输入系统的信号形式：文本，声音，图像等，而这个系统需要做出回应。现在假设输入的文本为text。接着定义一些基本操作（每个基本操作可以看做对api的一次调用）与语法，比如`语句简化`，`构造语意树`，`目得提取`等"运算符"以及`条件分支`，`循环`等对api结果的操作。然后编写操作步骤的程序运行

# python环境
导出环境
```sh
conda env export --name ai > environment.yml
```
创造环境
```sh
conda env create -f environment.yml
```
同步环境
```bash
conda env update -f environment.yml
```