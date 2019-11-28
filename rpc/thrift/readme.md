# Thrift

系统依赖：

系统安装thrift

brew install thrift

# Python

首先需要安装python的thrift包

sudo pip install thrift

# 编写一个简单接IDL文件helloworld.thrift

```
const string HELLO_WORLD = "world"

service HelloWorld {
    void ping(),
    string sayHello(),
    string sayMsg(1:string msg)
}
```

thrift脚本通过Thrift编辑器生成所要求的python开发语言代码。即：

```bash
thrift -r --gen py helloworld.thrift 
```

生成gen-py目录：

```
├── gen-py
│   ├── helloworld
│   │   ├── constants.py
│   │   ├── HelloWorld.py
│   │   ├── HelloWorld-remote
│   │   ├── __init__.py
│   │   └── ttypes.py
│   └── __init__.py
└── helloworld.thrift
```

# Thrift是一个典型的CS结构，客户端和服务端可以使用不同的语言开发。

# 服务端PythonServer.py

```
import sys
sys.path.append('./gen-py')
  
from helloworld import HelloWorld
from helloworld.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket

class HelloWorldHandler:
    def __init__(self):
        self.log = {}

    def ping(self):
        print "ping()"

    def sayHello(self):
        print "sayHello()"
        return "say hello from " + socket.gethostbyname(socket.gethostname())

    def sayMsg(self, msg):
        print "sayMsg(" + msg + ")"
        return "say " + msg + " from " + socket.gethostbyname(socket.gethostname())

handler = HelloWorldHandler()
processor = HelloWorld.Processor(handler)
transport = TSocket.TServerSocket('127.0.0.1',30303)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print "Starting python server..."
server.serve()
print "done!"
```


# 客户端PythonClient.py

```
import sys
sys.path.append('./gen-py')
 
from helloworld import HelloWorld
from helloworld.ttypes import *
from helloworld.constants import *
 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
 
try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 30303)
     
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
     
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
     
    # Create a client to use the protocol encoder
    client = HelloWorld.Client(protocol)
     
    # Connect!
    transport.open()
     
    client.ping()
    print "ping()"
     
    msg = client.sayHello()
    print msg
    msg = client.sayMsg(HELLO_WORLD)
    print msg
    transport.close()
          
except Thrift.TException, tx:
    print "%s" % (tx.message)
```

# 当前目录结构：

├── gen-py
├── helloworld.thrift
├── PythonClient.py
└── PythonServer.py

# 运行server端：

```
$ python PythonServer.py 
Starting python server...
```

# 运行client端：

```
$ python PythonClient.py 
ping()
say hello from 10.27.73.176
say world from 10.27.73.176
```

# server端输出：
```
```
ping()
sayHello()
sayMsg(world)
```
