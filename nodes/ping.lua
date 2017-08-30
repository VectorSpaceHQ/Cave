ds18bs0 = require("ds18b20")
conn=net.createConnection(net.TCP, false)
conn:on("receive", function(conn, payload) print("GET done.", payload) end )
conn:connect(3306,"10.0.0.31")
conn:send("GET /store.php?heap=" .. read_temp(nil, F, nil, 1) .." HTTP/1.1\r\nHost: 10.0.0.31\r\n" .. "Connection: keep-alive\r\nAccept: */*\r\n\r\n")
--TODO
--change heap dump to specific table
--get read from DS18B20 - DONE
--https://github.com/nodemcu/nodemcu-firmware/tree/master/lua_modules/ds18b20
--mysql data U:node, no password 
