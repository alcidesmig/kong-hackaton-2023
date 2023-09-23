local socket = require("socket")

local host = "127.0.0.1"
local port = 25564

-- Create a socket client
local client = socket.connect(host, port)

if client then
  print("Connected to server")

  local message = "Smart TV 65 4K LED LG 65UR8750PSA Para você que gosta de reunir a família e os amigos para assistir algum filme engraçado ou maratonar aquela série que prende a atenção de todos, precisa conhecer a Smart TV de 65 LG 65UR8750PSA. Ela possui resolução 4K Ultra HD com tecnologia LED onde você assiste os conteúdos favoritos em alta definição aprimorados com o AI 4K Upscaling, 60Hz de frequência, sistema operacional webOS 23 e processador α5 AI Processor 4K Gen6. Além disso, ainda oferece conectividade via Bluetooth e Wi-Fi que facilitam a conexão com outros dispositivos e periféricos, assistentes virtuais Alexa, Google e Apple, 3 entradas HDMI e 2 USB, ThinQ AI e HDR10. Essa é uma Smart TV completa para ser o centro das atenções da sua sala"
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

