-- If you're not sure your plugin is executing, uncomment the line below and restart Kong
-- then it will throw an error which indicates the plugin is being loaded at least.

--assert(ngx.get_phase() == "timer", "The world is coming to an end!")

---------------------------------------------------------------------------------------------
-- In the code below, just remove the opening brackets; `[[` to enable a specific handler
--
-- The handlers are based on the OpenResty handlers, see the OpenResty docs for details
-- on when exactly they are invoked and what limitations each handler has.
---------------------------------------------------------------------------------------------



local plugin = {
  PRIORITY = 1000, -- set the plugin priority, which determines plugin execution order
  VERSION = "0.1.0", -- version in X.Y.Z format. Check hybrid-mode compatibility requirements.
}

local http = require("resty.http")
local json = require("lunajson")
local socket = require("socket")

local ngx = ngx

function plugin:init_worker()

  -- your custom code here
  kong.log.debug("saying hi from the 'init_worker' handler")

end --]]

--- Exit with an unauthorized http response
local function response_error_exit(http_status, msg)
  kong.response.set_header("Content-Type", "application/json; charset=utf-8")
  return kong.response.exit(http_status, '{"message": "' .. msg .. '"}')
end

local function rewrite_body()
  local data = {
    msg = ngx.ctx.response_data
  }

  local json_string = json.encode(data)

  kong.response.set_header("content-length", #json_string)
end

-- runs in the 'access_by_lua_block'
function plugin:access(plugin_conf)

  -- your custom code here
kong.log("phase access custom")
kong.log.inspect(plugin_conf)   -- check the logs for a pretty-printed config!

local host = plugin_conf.host
local port = plugin_conf.port

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
  ngx.ctx.response_data = response
  rewrite_body()
  -- Close the client socket
  client:close()
else
  print("Failed to connect to the server")
end

end

function plugin:body_filter(plugin_conf)
  local body = kong.response.get_raw_body()
  if body ~= nil then
    kong.log.inspect(body)
  end

  local data = {
    msg = ngx.ctx.response_data
  }

  local json_string = json.encode(data)
  kong.response.set_raw_body(json_string)
end

function plugin:header_filter(plugin_conf)
  -- kong.response.set_header("content-length", 0)
end

-- return our plugin object
return plugin
