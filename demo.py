#coding:utf-8
import os
import shutil
cpp_path='./in/'
f='';
for filename in os.listdir(cpp_path):
	if os.path.splitext(filename)[1] == ".cpp" or os.path.splitext(filename)[1] == ".c":
		f=f+' '+cpp_path+filename
Gcmd='g++ -fdump-rtl-expand'+f
os.system(Gcmd) #G++ 
os.system("python ./function/func.py") #python
os.system("dot -Tpng -Grankdir=LR -o ./out/function.png ./out/1.dot") # dot
RTL_path='./'
for i in os.listdir(RTL_path):
	if os.path.splitext(i)[1] == ".expand"  or os.path.splitext(i)[1] == ".out":
		shutil.move(i, './function/RTL/'+i) 
os.remove('./out/1.dot')
print '--function finish--'

#cpp_path='./in/'
f='';
for filename in os.listdir(cpp_path):
	if os.path.splitext(filename)[1] == ".cpp" or os.path.splitext(filename)[1] == ".hpp":
		f=f+' '+cpp_path+filename
Gcmd='python ./uml/uml.py'+f+' > ./out/uml.txt'
os.system(Gcmd) 
os.system("java -jar ./uml/plantuml.jar ./out/uml.txt") 
print '--uml finish--'
