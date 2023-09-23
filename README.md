# kong-hackaton-2023


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
