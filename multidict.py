
class MultiDict:
	def __init__(self):
		self.data = []

	def __getitem__(self, k):
		for key, val in self.data:
			if k == key:
				return val

	def __setitem__(self, k, v):
		self.data.append((k, v))

	def keys(self):
		for k,v in self.data:
			yield k

	def values(self):
		for k,v in self.data:
			yield v

	def __str__(self):
		return self.toStr(0)

	def toStr(self, indent):
		out = "{\n"
		for k,v in self.data:
			out+="\t"*(indent+1)+str(k) + " : "+to_str(v, indent+1)+",\n"
		out+="\t"*indent+"}"
		return out

	def __repr__(self):
		return str(self)

def to_str(v, indent):
	try:
		return v.toStr(indent)
	except:
		pass
	return str(v)

