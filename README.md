# Automation Involving Multi-System Interaction from a GRC Perspective

## Introduction and Motivation

We claim without rigorous proof (since we believe this is self-evident) that any complex system can be decomposed as a collection of interacting sub-systems. Many business processes can similarly be decomposed. In addition, many software solutions require a mechanism of integrating (at least some components) of existing systems. 
Moreover, when working with vendor systems, there may extra requirements that need to be implemented by vendor to support integration with other systems. For example consider a vendor based modeling platform that is hosted in the cloud environment and accessible via a web interface. To watch this system for changes, one must observe some data underlying the interface. It could be a database for example. If the third-party system does not expose the pertinent data via an API endpoint for example, a request to provide that would be needed.

The use case is the following: Certain business processes should be triggered when certain activities take place. Here are some examples:


## The System
The Diagram below is a summary of the system. There core components are:

- **System Environments** to watch

   - We assume without loss of generality that our systems to watch are models.
   - A config file in the enviroment defines the specifics of monitoring e.g. which files change constitute a change to be monitored in a change management use-case
   - The functionality is in the /msg-dispatcher/src/...
- **Message Dispatcher**
  - This is a go server in ./msg-dispatcher/src/main.go
      - Updates the "database"(proxied by a ./data.json file)
- **View Engine** (Optional but important for illustrative purposes)
   - This is represented by an express application that uses pug as a templating engine in ./view-engine/index.js

```mermaid

%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': 'teal', 'secondaryColor':'lightblue', 'tertiaryColor':'grey'}}}%%
graph TD
          A[Multi-level System Automation] --> EnvWatcher(Environment Watcher)
          EnvWatcher --> |API Call with model change info| MsgDispatcher[fa:fa-gear Dispatcher API Endpoint]
          MsgDispatcher -->|API Call| Sys1[System_1 i.e. API EndPoint]
          MsgDispatcher -->|API Call| SysDots[System_2...L-1]
          MsgDispatcher -->|API Call| SysL[System_L i.e. API EndPoint]

          EnvWatcher --> |Monitor Environment|M1[fa:fa-gear Model 1]
          M1 --> |watch| F1[fa:fa-file File_1 ... File_N_1]
          M1 --> Config1[fa:fa-file Config File]
          EnvWatcher --> |Monitor Environments| Mdots[fa:fa-cogs Models 2 ... K-1]
          EnvWatcher --> |Monitor Environment| MK[fa:fa-cog Model K]
          MK --> |watch| FK[fa:fa-file File_1 ... File_N_K]          


         subgraph Model Environment K
           MK
           FK
          end
         subgraph Model Environments2..K-1
           Mdots
          end

         subgraph Model Environment1
           M1
           F1
           Config1
          end
```          
## Possible Enhancements
- Dockerization
- (Possibly only Applicable to systems with available source code) - Incorporate a classification of changes to categories based on extent/impact etc. NLP can be leveraged i.e. if the semantics of programming languages can be learned, this can form the basis of classification model 
