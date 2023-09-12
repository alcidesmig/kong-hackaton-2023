local plugin = {
  PRIORITY = 1000, -- set the plugin priority, which determines plugin execution order
  VERSION = "0.1.0", -- version in X.Y.Z format. Check hybrid-mode compatibility requirements.
}

local json = require("lunajson")
local socket = require("socket")
local ngx = ngx

--- Exit with an unauthorized http response
local function response_error_exit(http_status, msg)
  kong.response.set_header("Content-Type", "application/json; charset=utf-8")
  return kong.response.exit(http_status, '{"message": "' .. msg .. '"}')
end

local function rewrite_body(response)
  local data = {
    msg = response
  }

  local json_string = json.encode(data)

  return json_string
end

local function translate(client, response_msg)
  if client then
    print("Connected to server")
    -- Send data to the server
    client:send(response_msg .. "\n")
  
    -- Receive the servers response
    local response, err = client:receive()
    if response then
      print("Received response from server:", response)
    else
      print("Error receiving response:", err)
    end
    
    local json_string = rewrite_body(response)
    ngx.ctx.response_data = json_string

    -- Close the client socket
    client:close()
  else
    print("Failed to connect to the server")
  end
  
end

-- runs in the 'access_by_lua_block'
function plugin:access(plugin_conf)
  -- It is required to body_filter read the body
  kong.service.request.enable_buffering()
end

function plugin:body_filter(plugin_conf)

  local body_code_location = plugin_conf.field

  if body_code_location ~= nil then

    local host = plugin_conf.host
    local port = plugin_conf.port

    -- Create a socket client
    local client = socket.connect(host, port)

    local funcstr = "local attr = kong.service.response.get_body()." .. body_code_location .. "; return attr;"
    local result, vars = pcall(load(funcstr))

    -- Example description
    translate(client, vars)
    if result == false then
      -- `loadstring(funcstr)' raised an error: take appropriate actions
      -- return response_error_exit(403, "You shall not pass")
      return "Attribute " .. body_code_location .. "not found"
    end
    kong.response.set_raw_body(ngx.ctx.response_data)
  end
end

function plugin:header_filter(plugin_conf)
  -- header_filter > body_filter
  kong.response.clear_header("content-length")
end

-- return our plugin object
return plugin
