import bestin

t = bestin.Bestin('127.0.0.1', 9999, '1.1.1.1')

testReq = t.XMLRequest("testreq", "testaction", "dev1", "unit1", "ctrl1")

t.request("aaaa")
