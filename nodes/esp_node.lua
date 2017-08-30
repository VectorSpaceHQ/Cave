-- Read temperature and light

moduleID=2

light = adc.read(0)
print("light: ".. light)

-- init mqtt client without logins, keepalive timer 120s
m = mqtt.Client("clientid", 120)


m:on("connect", function(client) print ("connected") end)
m:on("offline", function(client) print ("offline") end)

-- on publish message receive event
m:on("message", function(client, topic, data)
  print(topic .. ":" )
  if data ~= nil then
    print(data)
  end
end)

-- for TLS: m:connect("192.168.11.118", secure-port, 1)
m:connect("10.0.0.31", 1883, 0, function(client)
  print("connected")
  -- Calling subscribe/publish only makes sense once the connection
  -- was successfully established. You can do that either here in the
  -- 'connect' callback or you need to otherwise make sure the
  -- connection was established (e.g. tracking connection status or in
  -- m:on("connect", function)).

  -- subscribe topic with qos = 0
  client:subscribe("/RPiThermostat/nodes", 0, function(client) print("subscribe success") end)
  -- publish a message with data = hello, QoS = 0, retain = 0
  client:publish("/RPiThermostat/nodes", "connected", 0, 0, function(client) print("sent") end)
end,
function(client, reason)
  print("failed reason: " .. reason)
end)


local ow_pin = 3
ds18b20.setup(ow_pin)
T=1
ds18b20.read(
   function(ind,rom,res,temp,tdec,par)
      temp = temp * 1.8 + 32
      print(temp)
      T = temp
   end,{});

if not tmr.create():alarm(10000, tmr.ALARM_AUTO, function()
                             m:publish("/RPiThermostat/nodes", T..", "..adc.read(0), 0, 0, function(client) print("sent") end)
                         end)
then
   print("whoopsie")
end
