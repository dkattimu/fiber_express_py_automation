# Production Environment Watcher

## Prerequisites
- Consists of both environment watcher (simulated here) and a confluence (documentation) watcher(this is not simulated here but existence will be assumed) 
- There exists a mechanism to identify production environments e.g. a .mrm.env.toml file that will hold config of environment

    - environment will support dev, test/qa as well as production versions. 
    - focus from this point will be on the production environment

       - identification of model (processing component)
       - identification of inputs (assumptions, data etc) 
       - a way of specifying in .mrm.model.env file what should be watched

            - Typically, would watch both assumptions and the processing components







## Design

### Environment Watcher
- specify folder (root) to search for _mrm.model_env.toml files

    - the _mrm.model_env.toml file will configure environment e.g. specify what files should be watched

- env-watcher.py will loop perpertually (in a fault tolerant manner) through file system and once change is detected will send an api call to msg-dispatcher
- env-watchter.py will also monitor documentation for changes too

    - dispatcher will then relay msg to inventory (will be simulated by either a log or msg on web-page)  

### Messaging Bridge
-  In this POC implemented as a Go server
-  API endpoints to populate DB (implemented as a json file in POC)  which can then rendered by webclient via pug      