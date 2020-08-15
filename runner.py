#!/usr/bin/env python3
import gameServer.serverCode.server as server

if __name__ == "__main__":
    import os 
  
    pid = os.getpid()
    with open('runPID', 'w') as f:
        f.write(str(pid))

    server.main()