"""Read-only SC2 telemetry. Format: OpenCity2k/SC2k-docs (sc2 file spec.md)."""
import struct,json,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
GRAPH_NAMES=['population_graph','residents','commerce','industry','traffic','pollution','property_value','crime','power_capacity','water_capacity','health','education','unemployment','national_gnp','national_population_graph','interest_rate']
def decode(b):
 out=bytearray();p=0
 while p<len(b):
  n=b[p];p+=1
  if n<128:
   if p+n>len(b):raise ValueError('Truncated literal')
   out.extend(b[p:p+n]);p+=n
  elif n>128:
   if p>=len(b):raise ValueError('Truncated run')
   out.extend([b[p]]*(n-127));p+=1
  if len(out)>1000000:raise ValueError('Oversized chunk')
 return bytes(out)
def parse(path):
 b=Path(path).read_bytes()
 if b[:4]!=b'FORM' or b[8:12]!=b'SCDH' or struct.unpack('>I',b[4:8])[0]!=len(b)-8:raise ValueError('Not a complete SC2 city')
 chunks={};p=12
 while p<len(b):
  tag=b[p:p+4].decode('ascii');n=struct.unpack('>I',b[p+4:p+8])[0];p+=8
  if p+n>len(b):raise ValueError('Truncated chunk')
  chunks[tag]=b[p:p+n] if tag in ['CNAM','ALTM'] else decode(b[p:p+n]);p+=n
 m=chunks['MISC'];g=chunks['XGRP']
 if len(m)!=4800 or len(g)!=3328:raise ValueError('Unsupported city layout')
 num=lambda o:struct.unpack_from('>i',m,o)[0]
 age=num(16);founded=num(12)
 graphs={name:list(struct.unpack_from('>52i',g,i*208)) for i,name in enumerate(GRAPH_NAMES)}
 metrics={name:values[0] for name,values in graphs.items()}
 metrics.update(population=num(0x102c)+num(0x1020),funds=num(0x14),bonds=num(0x18),debt=num(0x18)*10000,life_expectancy=num(0x48),education_quotient=num(0x4c),workforce=num(0x44),national_population=num(0x50),residential_demand=num(0x718),commercial_demand=num(0x71c),industrial_demand=num(0x720))
 return dict(time=time.time(),save_time=Path(path).stat().st_mtime,city=chunks.get('CNAM',b'\x00Astra Lab')[1:].split(b'\0')[0].decode('ascii','replace'),year=founded+age//300,month=age%300//25+1,day=age%25+1,age=age,metrics=metrics,graphs=graphs,sha256=hashlib.sha256(b).hexdigest(),source='Read-only SC2 save; graph values are latest monthly samples')
if __name__=='__main__':
 import sys
 print(json.dumps(parse(sys.argv[1]),indent=2))
