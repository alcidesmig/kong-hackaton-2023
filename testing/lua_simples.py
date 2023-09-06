local socket = require("socket")

local host = "127.0.0.1"
local port = 12345

-- Create a socket client
local client = socket.connect(host, port)

if client then
  print("Connected to server")

  local message = "É um livro ou pilha de páginas de papel que geralmente são pautadas e usadas para fins como fazer anotações"
  print("Sending data to server:", message)

  -- Send data to the server
  client:send(message .. "\n")

  -- Receive the servers response
  local response, err = client:receive()
  if response then
    print("Received response from server:", response)
  else
    print("Error receiving response:", err)
  end

  -- Close the client socket
  client:close()
else
  print("Failed to connect to the server")
end

