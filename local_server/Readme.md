Local Server
======================

# Server - A communication link between the UI server and the process controlling the outlets. 
## Communication links:

- local server (this) <---- websocket ----> Django server
- local server (this) <---- Unix connection ----> Outlet controller