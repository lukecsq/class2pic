# class2pic
C++源代码自动分析工具，得到UML类图、函数间调用关系网图及相关文档

配置：
--java 

    自行配置JDK

--graphviz

    sudo apt install graphviz

--libclang

    sudo apt-get install libclang-dev
  
    sudo ln -s /usr/lib/llvm-3.8/lib/libclang.so /usr/lib/libclang.so
  
  其中“llvm-3.8”根据安装的实际版本修改版本号

/in 文件夹放入待分析的C++源程序

/out文件夹是输出的图和文本

运行：python demo.py
