# coding=utf-8
from baidu_map_engine import baidu_map

t=baidu_map()
print "Search by name:"
input = {"placename":"银行","max_long":"40","min_long":"39","max_lat":"117","min_lat":"116"}
print "input: " + str(input)
print t.search_by_name(input)
print "---------------------------------------------"

print t.search_by_name({"placename":"银行","max_long":"0","min_long":"0","max_lat":"0","min_lat":"0"})
print "---------------------------------------------"

print t.search_by_name({})
print "---------------------------------------------"
print "Search coordinate:"
print t.search_coordinate({"longitude":"120.167930","latitude":"30.277693"})  

print "---------------------------------------------"
print t.search_coordinate({"longitude":"39.983424","latitude":"116.322987"})  

print "---------------------------------------------"
print t.search_coordinate({"longitude":"39.983424"})  
print "---------------------------------------------"

print "Search bounding box"
print t.search_bounding_box({"max_long":"121.53300","min_long":"121.53068","max_lat":"29.86300","min_lat":"29.86123"})
print "---------------------------------------------"


print t.search_bounding_box({"max_long":"121.53300","max_lat":"29.86300","min_lat":"29.86123"})
print "---------------------------------------------"

print t.search_bounding_box({"max_long":"120.53300","min_long":"120.53333","max_lat":"40.00000","min_lat":"40.00000"})
print "---------------------------------------------"


