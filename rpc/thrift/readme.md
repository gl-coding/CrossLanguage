# Facebook开源的跨语言RPC框架。Thrift

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

thirft使用socket进行数据传输，数据以特定的格式发送，接收方进行解析。我们定义好thrift的IDL文件后，就可以使用thrift的编译器来生成双方语言的接口、model，在生成的model以及接口代码中会有解码编码的代码。

TTransport层
代表thrift的数据传输方式，thrift定义了如下几种常用数据传输方式

TSocket: 阻塞式socket；
TFramedTransport: 以frame为单位进行传输，非阻塞式服务中使用；
TFileTransport: 以文件形式进行传输；
TProtocol层
代表thrift客户端和服务端之间传输数据的协议，通俗来讲就是客户端和服务端之间传输数据的格式(例如json等)，thrift定义了如下几种常见的格式

TBinaryProtocol: 二进制格式；
TCompactProtocol: 压缩格式；
TJSONProtocol: JSON格式；
TSimpleJSONProtocol: 提供只写的JSON协议；
thrift支持的Server模型
thrift主要支持以下几种服务模型

TSimpleServer: 简单的单线程服务模型，常用于测试；
TThreadPoolServer: 多线程服务模型，使用标准的阻塞式IO；
TNonBlockingServer: 多线程服务模型，使用非阻塞式IO(需要使用TFramedTransport数据传输方式);
THsHaServer: THsHa引入了线程池去处理，其模型读写任务放到线程池去处理，Half-sync/Half-async处理模式，Half-async是在处理IO事件上(accept/read/write io)，Half-sync用于handler对rpc的同步处理；
thrift IDL文件
thrift IDL不支持无符号的数据类型，因为很多编程语言中不存在无符号类型，thrift支持一下几种基本的数据类型

byte: 有符号字节
i16: 16位有符号整数
i32: 32位有符号整数
i64: 63位有符号整数
double: 64位浮点数
string: 字符串
此外thrift还支持以下容器类型：

list: 一系列由T类型的数据组成的有序列表，元素可以重复；
set: 一系列由T类型的数据组成的无序集合，元素不可重复；
map: 一个字典结构，Key为K类型，Value为V类型，相当于java中的HashMap；
thrift容器中元素的类型可以是除了service之外的任何类型，包括exception
