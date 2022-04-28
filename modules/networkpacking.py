import numpy
import struct

def packmap(gamemap) -> bytes:
  width = len(gamemap[0])
  height = len(gamemap)
  sizebytes = struct.pack(">hh", width, heigh)
  mapbytes = numpy.array(gamemap, dtype=numpy.bool_).tobytes()
  return sizebytes + mapbytes

def unpackmap(mapbytes):
  width, height = struct.unpack_from(">hh", mapbytes)
  
