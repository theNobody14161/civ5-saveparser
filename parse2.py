from multidict import MultiDict as odict
import FileReader as fr

def parse(filename):
	out = odict()
	with fr.FileReader(filename) as f:
		out['base'] = parse_base(f)
		#out['compressed'] = parse_compressed(f)
	return out

def parse_base(f):
	out = odict()
	out['version'] = parse_version(f)
	out['game'] = parse_game(f)
	out['civilization'] = f.read_string()
	out['handicap'] = f.read_string()
	out['era'] = parse_era(f)
	out['gamespeed'] = f.read_string()
	out['worldsize'] = f.read_string()
	out['mapscript'] = f.read_string()
	out[unknown()] = f.read_bytes(4)
	return out

def parse_version(f):
	version = odict()
	version['const_string'] = f.read_bytes(4)
	version['save'] = f.read_int()
	version['game'] = f.read_string()
	version['build'] = f.read_string()
	return version

def parse_game(f):
	game = odict()
	game['currentturn'] = f.read_int()
	game[unknown()] = f.read_bytes(1)
	return game

def parse_era(f):
	era = odict()
	era['starting'] = f.read_string()
	era['current'] = f.read_string()
	return era

def unknown():
	return "UnknownElement"+str(next(unknown.gen))

def unknown_gen():
	a = 0
	while True:
		yield a
		a+=1
unknown.gen = unknown_gen()

if __name__ == "__main__":
	import sys
	print(parse(sys.argv[1]))
