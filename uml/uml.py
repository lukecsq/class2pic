#!/usr/bin/env python

import sys
import re
import yl.cindex

LEVEL = 0
FILES = ''

classObj = []
INFILE = 0

class FileCache(object):
	def __init__(self, name):
		self.__mFile = open(name)
		self.__min   = 0;
		self.__max   = 10;
		self.__line  = [];
		for i in range(0, 10):
			self.__line.append(self.__mFile.readline());

	def __del__(self):
		del self.__line[:]
		self.__mFile.close()

	def readLine(self, line):
		line -= 1;
		if line < self.__min:
			return -1;
		if line >= self.__max:
			del self.__line[:]
			drop = line - self.__max;
			for i in range(0, drop):
				self.__mFile.readline()
			for i in range(0, 10):
				self.__line.append(self.__mFile.readline());
			self.__min = line;
			self.__max = line + 10;

		offset = line - self.__min;
		return str(self.__line[offset])

class ClassObject(object):
	""" definition class object
	"""

	PUBLIC_ACC   = 1
	PRVIVATE_ACC = 3
	PROTECTED_ACC = 2
	BASETYPE = ['int', 'uint32_t', 'int32_t', 'float', 'char', 'size_t', 'bool', 'int64_t',\
		'uint64_t', 'short', 'long', 'double', 'unsigned', 'signed', 'nsecs_t', 'String8', 'string',\
		'uint16_t']

	def __init__(self, name):
		self.__mName = name
		self.__mAccess = self.PUBLIC_ACC
		self.__mPublicFun = []
		self.__mPublicMem = []
		self.__mProtectedFun = []
		self.__mProtectedMem = []
		self.__mPrivatFun = []
		self.__mPrivatMem = []

	def onAccess(self, acc):
		self.__mAccess = acc

	def addFuncion(self, name):
		if (self.__mAccess == self.PUBLIC_ACC):
			self.__mPublicFun.append(name)
		elif(self.__mAccess == self.PROTECTED_ACC):
			self.__mProtectedFun.append(name)
		else:
			self.__mPrivatFun.append(name)

	def addMember(self, name):
		if (self.__mAccess == self.PUBLIC_ACC):
			self.__mPublicMem.append(name)
		elif (self.__mAccess == self.PROTECTED_ACC):
			self.__mProtectedMem.append(name)
		else:
			self.__mPrivatMem.append(name)

	def name(self):
		return str(self.__mName)

	def outString(self):
		print 'class %s {\npublic:' % (self.__mName)

		for fun in self.__mPublicFun:
			print '\t%s' % (fun)

		for mem in self.__mPublicMem:
			print '\t%s' % (mem)

		print 'private:'

		for fun in self.__mPrivatFun:
			print '\t%s' % (fun)

		for mem in self.__mPrivatMem:
			print '\t%s' % (mem)

		print '}\n'

	def outUml(self):
		m = re.compile('([_\d\w]*)').match(self.__mName)
		print 'class %s {' % (m.group(0))

		for fun in self.__mPublicFun:
			print '\t+%s' % (fun)

		for mem in self.__mPublicMem:
			print '\t+%s' % (mem)
		
		for fun in self.__mProtectedFun:
			print '\t#%s' % (fun)

		for mem in self.__mProtectedMem:
			print '\t#%s' % (mem)

		for fun in self.__mPrivatFun:
			print '\t-%s' % (fun)

		for mem in self.__mPrivatMem:
			print '\t-%s' % (mem)

		print '}\n'

	def __isClsPointer(self, line):
		for x in self.BASETYPE:
			if cmp(x, line) == 0:
				return True
	def outFunMem(self):
		print 'public  '
		print self.__mPublicFun
		print self.__mPublicMem
		print 'Protected  '
		print self.__mProtectedFun
		print self.__mProtectedMem
		print 'Privat  '
		print self.__mPrivatFun
		print self.__mPrivatMem

	def outRef(self):
		cls = re.compile('([_\d\w]*)').match(self.__mName).group(0)

		print '\t\'################ %s ##########################' % cls

		for mem in self.__mPublicMem:
			line = re.sub(r'(\bclass\b|\bconst\b)', '', mem).strip()
			typ = re.compile('([_\d\w]*)').match(line).group(0)
			if self.__isClsPointer(typ) is not True:
				print '\t\'### %s' % mem
				if mem.find('*') > 0:
					print '"%s" --o "%s"\n' % (typ, cls)
				else:
					print '"%s" --* "%s"\n' % (typ, cls)

		for mem in self.__mPrivatMem:
			line = re.sub(r'(\bclass\b|\bconst\b)', '', mem).strip()
			typ = re.compile('([_\d\w]*)').match(line).group(0)
			if self.__isClsPointer(typ) is not True:
				print '\t\'### %s' % mem
				if mem.find('*') > 0:
					print '"%s" --o "%s"\n' % (typ, cls)
				else:
					print '"%s" --* "%s"\n' % (typ, cls)


def found_class(node):
	""" Found class define'
	"""
	global INFILE
	global LEVEL

	def tripfun(fun):
		pos = fun.find(')')
		if (pos > 0):
			return fun[:pos+1];
		return fun

	cn = re.sub(r'(\bpublic\b|\bvirtual\b|\bstruct\b|\bclass\b|{)', '', INFILE.readLine(node.location.line)).strip()
	# print 'Found class %d [[%s], %s=%s, line=%s]' % (LEVEL, node.spelling, node.displayname,cn, node.location)

	obj = ClassObject(cn)
	classObj.append(obj)
	LEVEL += 1
	lastval=''
	for c in node.get_children():
		val = INFILE.readLine(c.location.line).strip()
		#print 'node :: %s, %s, line %d' % (c.kind, c.spelling, c.location.line)
		if yl.cindex.CursorKind.CLASS_DECL == c.kind:
			found_class(c);

		if yl.cindex.CursorKind.CXX_METHOD == c.kind:
			#print 'CXX_METHOD :: %s, line %d' % (tripfun(val), c.location.line)
			obj.addFuncion(tripfun(val))

		if yl.cindex.CursorKind.CONSTRUCTOR == c.kind:
			#print 'CONSTRUCTOR :: %s, line %d' % (tripfun(val), c.location.line)
			obj.addFuncion(tripfun(val))

		if yl.cindex.CursorKind.DESTRUCTOR == c.kind:
			#print 'DESTRUCTOR :: %s' % (tripfun(val))
			obj.addFuncion(tripfun(val))

		if yl.cindex.CursorKind.FIELD_DECL == c.kind:
			#print 'FIELD_DECL :: %s' % (val)
			if val != lastval:
				obj.addMember(val);

		if yl.cindex.CursorKind.CXX_ACCESS_SPEC_DECL == c.kind:
			#print 'CXX_ACCESS :: %s' % (val)
			if val.find('public') >= 0:
				obj.onAccess(1);
			elif val.find('protected') >= 0:
				obj.onAccess(2);
			else:
				obj.onAccess(3);
		lastval=val;

	LEVEL -= 1

def find_typerefs(node):
	""" Find all references to the type named 'typename'
	"""
	global LEVEL
	global FILES
	# Recurse for children of this node
	if node.location.file is not None and cmp(str(node.location.file), FILES) != 0:
		return;

	# print 'Found %d[file=%s, line=%s, col=%s]\n' % (LEVEL, node.location.file, node.location.line, node.location.column)

	if yl.cindex.CursorKind.CLASS_DECL == node.kind or yl.cindex.CursorKind.STRUCT_DECL == node.kind:
		found_class(node)
	else:
		for c in node.get_children():
			find_typerefs(c)


def main(argv):
	global FILES
	global LEVEL
	global INFILE

	print '@startuml\n'
	index = yl.cindex.Index.create()

	for filename in sys.argv[1:]:
		tu = index.parse(filename)
		print '\'Translation unit:', tu.spelling
		INFILE = FileCache(filename);

		FILES = str(tu.spelling)
		LEVEL = 0
		find_typerefs(tu.cursor)

	for obj in classObj:
		obj.outUml()
		#print '======='

	for obj in classObj:
		line = re.sub(r'(\bpublic\b|\bvirtual\b)', '', obj.name())  # = 'BaseA: Base,  A'
		line = re.sub('\s+', '', line)      #  = 'BaseA:Base,A'
		cls  = re.split(r'[:,]', line)     #  = ['BaseA', 'Base', 'A']
		if len(cls) > 1:
			print '\t\'### %s' % obj.name()
		for i in range(1, len(cls)):
			print '"%s" <|-- "%s"' % (cls[i], cls[0])
		if len(cls) > 1:
			print '\n'

	for obj in classObj:
		obj.outRef()

	print '@enduml\n'
	#for obj in classObj:
		#obj.outFunMem()
	

if __name__ == '__main__':
	main(sys.argv)
	#print '--uml finish--'



