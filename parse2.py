from multidict import MultiDict as odict
from bitstring import Bits, ConstBitStream
import FileReader as fr

def parse(filename):
	out = odict()
	with fr.FileReader(filename) as f:
		out['base'] = parse_base(f)
		out['dlc'] = parse_dlcs(f)
		out['blocks'] = parse_blocks(f)
		out['compressed'] = parse_compressed(f)
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

def parse_dlcs(f):
	dlcs = odict()
	while f.peek_int() != 0:
		dlcs[unknown()] = f.read_bytes(16)
		dlcs[unknown()] = f.read_bytes(4)
		dlcs['dlc'] = f.read_string()
	return dlcs

def parse_blocks(f):
	last_read = f.pos
	positions = list(f.findall('0x40000000'))
	f.pos = last_read
	blocks = odict()
	if f.pos < positions[0]:
		assert((positions[0]-f.pos)%8==0)
		blocks['prefix'] = f.read_bytes((positions[0]-f.pos)//8)
	assert(f.pos == positions[0])
	for i in range(len(positions)-1):
		assert(f.pos == positions[i])
		assert((positions[i+1]-positions[i])%8==0)
		if i == 27:
			blocks[str(i)] = parse_block_27(f, positions[i], positions[i+1])
		else:
			blocks[str(i)] = f.read_bytes((positions[i+1] - positions[i])//8)
	return blocks

def parse_block_27(f, start, end):
	data = odict()
	end-=5*8
	data[unknown()] = f.read_bytes((end-start)//8)
	data['VictoryFlag1'] = bytes([f.read_byte()])
	data['VictoryFlag2'] = bytes([f.read_byte()])
	data['VictoryFlag3'] = bytes([f.read_byte()])
	data['VictoryFlag4'] = bytes([f.read_byte()])
	data['VictoryFlag5'] = bytes([f.read_byte()])
	return data


def parse_compressed(f):
	#todo - this just reads the rest at the moment
	compressed = odict()
	compressed[unknown()] = f.read_bytes((f.bits.length-f.pos)//8)
	assert(f.pos == f.bits.length)
	return compressed

def unknown():
	return "UnknownElement"+str(next(unknown.gen))

def unknown_gen():
	a = 0
	while True:
		yield a
		a+=1
unknown.gen = unknown_gen()

def flatten(val):
	try:
		out = b''
		for v in val.values():
			out += flatten(v)
		return out
	except AttributeError:
		return to_bits(val)

def to_bits(val):
	if isinstance(val, int):
		return ConstBitStream(uintle=val, length=32)
	elif isinstance(val, str):
		return to_bits(len(val)) + val.encode()
	return val

def test(filename):
	raw_bytes = open(filename,'rb').read()
	processed_bytes = flatten(parse(filename)).bytes
	index = 0
	for v1, v2 in zip(raw_bytes, processed_bytes):
		index+=1
		if v1 != v2:
			print(raw_bytes[:index+10])
			print(processed_bytes[:index+10])
			assert(False)


if __name__ == "__main__":
	import sys
	val = parse(sys.argv[1])
	print(val)
	test(sys.argv[1])

