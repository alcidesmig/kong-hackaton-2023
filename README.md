# kong-hackaton-2023

## About this project

This project is a Lua-based plugin for Kong API Gateway that help translate specific fields in json to more than 60 languages. The default target language is English, but it can be changed with the use of the "X-Translate-To" header.

The plugin operates by intercepting the response from the upstream, forwarding it to the translation server via socket, and responding to the client with the translated message.

<b>The plugin still in experimentation phase, so it is possible to find some bugs - please report it!</b>


### Kong Plugin Configuration Parameters

| Parameter name       | Required | Description | Default value | Type   |
|----------------------|----------|-------------|---------------|--------|
| socket_host          | true         |  Translate Server Address           |               | String |
| socket_port         | true         | Translate Server Port         |               | Number |
| body_location_field   | true        | If defined, the plugin code will get field from request.body.<configuration>            |               | String |
| translate_to_header | false        | If defined, set the target translate language via Header.       |               | String |

### Enabling the plugin on a Service

Configure this plugin on a Service with the declarative configuration:

```bash
_format_version: "2.1"
_transform: true
services:
- name: ecommerce-service
  url: http://localhost:8080
  retries: 0
  connect_timeout: 5000
  write_timeout: 5000
  read_timeout: 5000
  routes:
  - name: my-product
    regex_priority: 200
    strip_path: false
    methods: [GET]
    protocols: [http]
    response_buffering: false
    paths:
    - /products/
    plugins:
    - name: kong-plugin-internationalization
      config:
        socket_host: "localhost"
        socket_port: 25564
        body_location_field: description
```

### Using APIs

The `docker-compose.yml` file brings some example setup. After running `docker-compose up -d`, it is possible to test the setup with the following calls:

#### E-commerce example API

Calls the back-end directly:

```bash
curl backend:8000/products/5293b118-d8c2-4c63-b5bf-027eec118126
```

#### Kong API

Translate back-end (Portugues) to default language (English):

```bash
curl kong-gateway:8000/products/5293b118-d8c2-4c63-b5bf-027eec118126
```

Translate back-end (Portugues) to specific language (Italian):

```bash
curl kong-gateway:8000/products/5293b118-d8c2-4c63-b5bf-027eec118126 -H "X-Translate-To: Italian"
```

## Translation Engine

The "translator" folder contains one translation engine capable of identifying, translating and caching content for the following languages (as both origin or target language)

> Afrikaans, Arabic, Azerbaijani, Belarusian, Bulgarian, Bengali, Bosnian, Catalan, Czech, Welsh, Danish, German, Greek, English, Spanish, Estonian, Persian, Finnish, French, Irish, Gujarati, Hebrew, Hindi, Croatian, Hungarian, Armenian, Indonesian, Icelandic, Italian, Japanese, Georgian, Kazakh, Korean, Ganda, Lithuanian, Latvian, Macedonian, Mongolian, Marathi, Malay, Dutch, Punjabi, Polish, Portuguese, Romanian, Russian, Slovak, Somali, Albanian, Serbian, Swedish, Swahili, Tamil, Thai, Tagalog, Tswana, Turkish, Ukrainian, Urdu, Vietnamese, Xhosa, Yoruba, Chinese, Zulu

### How it works?

The engine creates a multithreading socket server that waits for a sentence and responds to that sentence translated into the desired language.

The AI library used for translation is [dl-translate](https://github.com/xhluca/dl-translate), and for language identification is [lingua-py](https://github.com/pemistahl/lingua-py).

### Settings

The following environment variables can be used for configuring the translation engine:

| Environment Variable            | Default Value | Description                                      |
|-------------------------|---------------|--------------------------------------------------|
| CACHE_ENABLED           | False    | Enable or disable caching                       |
| LANGUAGE_AUTODETECT_ENABLED | False | Enable or disable language autodetection       |
| DEFAULT_LANGUAGE_SRC    | Portuguese    | Default source language for translations        |
| LANGUAGE_TARGET         | English       | Target language for translations                |
| MAX_PAYLOAD_SIZE       | 4096          | Maximum payload size for server communication   |
| SERVER_PORT             | 25564         | Port number for the server to listen on         |

### Deployment

For Kubernetes deployment, the translation engine can be deployed as sidecar of Kong container or as a separated system with a dedicated GPU. For non-containerized deployments, it is recommended to deploy the translation engine in a machine with an intermediate GPU.

However, the engine can run directly on the CPU. In this case, it is recommended to enable the cache setting, with Redis caching, as the inferences will be longer.

## TODO List

This plugin is still evolving, and the next features planned are:

- add test cases
- make a performance test
- improves performance between the Kong Plugin and the Translate Server
- add AI Models to describe images
- add other AI Models
- voice response with product description
- publish a release of the plugin at luarocks.org

## Credits

made with :heart: by Alcides Mignoso (https://www.linkedin.com/in/alcidesmig/) and Mateus Fonseca (https://www.linkedin.com/in/mateus-lima-fonseca/)
