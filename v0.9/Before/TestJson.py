import json  
 
s = {"name":"niaochao","point":{"lat":"39.990","lng":"116.397"},"desc":"aoyunhuizhuchangdi"},
    {"name":"beidapingpangqiuguan","point":{"lat":"39.988","lng":"116.315"},"desc":"pingpangqiubisaichangdi"},
    {"name":"beijinggongrentiyuchang","point":{"lat":"39.930","lng":"116.446"},"desc":"zuqiubisaichangdi"}  
s2 = '\''+s+'\''
locations = json.loads(s2)  
print str(len(locations)) 
for key in s:
    print key 
for location in locations:  
    print location["name"]  
    print location["point"]["lat"]