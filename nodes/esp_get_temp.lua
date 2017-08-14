-- bme280
-- http://esp8266linux.com/tutorials/temperature.html


-- Measure temperature
sda_pin = 3
scl_pin = 2
bme280.init(sda_pin, scl_pin)
T_string = string.format("Temp=%d.%02d", bme280.temp()/100, bme280.temp()%100)
print(T_string)

-- a simple HTTP server
srv = net.createServer(net.TCP)
srv:listen(80, function(conn)
              conn:on("receive", function(sck, payload)
                         print(payload)
                         sck:send(string.format("Temp=%d.%02d", bme280.temp()/100, bme280.temp()%100))
              end)
              conn:on("sent", function(sck) sck:close() end)
end)
