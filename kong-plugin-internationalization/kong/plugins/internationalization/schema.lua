local typedefs = require "kong.db.schema.typedefs"

local PLUGIN_NAME = "internationalization"

local schema = {
  name = PLUGIN_NAME,
  fields = {
    -- the 'fields' array is the top-level entry with fields defined by Kong
    { consumer = typedefs.no_consumer },  -- this plugin cannot be configured on a consumer (typical for auth plugins)
    { protocols = typedefs.protocols_http },
    { config = {
        -- The 'config' record is the custom part of the plugin schema
        type = "record",
        fields = {
          -- a standard defined field (typedef), with some customizations
          { socket_host = { type = "string", required = true }, },
          { socket_port = { type = "number", required = true }, },
          { body_location_field = { type = "string", required = true }, },
          { translate_to_header = { type = "string", required = false }, },
        },
      },
    },
  },
}

return schema
