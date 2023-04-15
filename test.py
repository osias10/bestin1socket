#!/usr/bin/python3
import bestin

t = bestin.Bestin('127.0.0.1', 9999, '1.1.1.1', 10000)

req = t.XMLRequest("remote_access_light", "status", 5, "switch1", " ")

res = t.requestToWallpad(req)

res2 = t.ParseXMLResponse(res)

print(res)

print(res2)