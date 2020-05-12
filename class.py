class Robot(object):
   def __init__(self):
      self.__version = 22

   def getVersion(self):
      print(self.__version)

   def setVersion(self, version):
      self.__version = version

obj = Robot()
obj.__version=48
print(obj.__version)


class Robot1:
   aa=14 
   def __init__(self):
      self.a = 123
      self._b = 123
      self.__c = 123

obj = Robot1()
print(obj.a)
print(obj._b)
#print(obj.__c)
print(Robot1.aa)
