0x00

系统安装thrift
brew install thrift

首先需要安装python的thrift包
sudo pip install thrift
1
0x01
编写一个简单接IDL文件helloworld.thrift

const string HELLO_WORLD = "world"

service HelloWorld {
    void ping(),
    string sayHello(),
    string sayMsg(1:string msg)
}
thrift脚本通过Thrift编辑器生成所要求的python开发语言代码。即：

thrift -r --gen py helloworld.thrift 
1
生成gen-py目录：

├── gen-py
│   ├── helloworld
│   │   ├── constants.py
│   │   ├── HelloWorld.py
│   │   ├── HelloWorld-remote
│   │   ├── __init__.py
│   │   └── ttypes.py
│   └── __init__.py
└── helloworld.thrift
1
2
3
4
5
6
7
8
9
0x02
Thrift是一个典型的CS结构，客户端和服务端可以使用不同的语言开发。本文以python为例：
PythonServer.py

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
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
PythonClient.py

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
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
当前目录结构：

├── gen-py
├── helloworld.thrift
├── PythonClient.py
└── PythonServer.py
1
2
3
4
0x03
运行server端：

$ python PythonServer.py 
Starting python server...
1
2
运行client端：

$ python PythonClient.py 
ping()
say hello from 10.27.73.176
say world from 10.27.73.176
1
2
3
4
server端输出：

ping()
sayHello()
sayMsg(world)
1
2
3
0x04 使用thriftpy
thriftpy（现已更新为thriftpy2）对thrift进行了封装，可以动态解析thrift接口文件。项目地址：https://github.com/Thriftpy/thriftpy2

安装thriftpy2
sudo pip install thriftpy2
1
编写IDL
pingpong.thrift

service PingService {
    string ping(),
}
service AargsPingService {
    string ping(1:string ping);
}
service Sleep {
    oneway void sleep(1: i32 seconds)
}
1
2
3
4
5
6
7
8
9
编写代码
server.py

# coding=utf-8
import thriftpy2
from thriftpy2.rpc import make_server
pp_thrift = thriftpy2.load("pingpong.thrift", module_name="pp_thrift")

# 实现.thrift文件定义的接口
class Dispatcher(object):
    def ping(self):
        print("ping pong!")
        return 'pong'

def main():
    # 定义监听的端口和服务
    server = make_server(pp_thrift.PingService, Dispatcher(), '127.0.0.1', 6000)
    print("serving...")
    server.serve()
if __name__ == '__main__':
    main()
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
client.py

# coding=utf-8
import thriftpy2
#from thriftpy2.rpc import client_context
from thriftpy2.rpc import make_client
# 读入thrift文件，module_name最好与server端保持一致，也可以不保持一致
pp_thrift = thriftpy2.load("pingpong.thrift", module_name="pp_thrift")

def main():
    #with client_context(pp_thrift.PingService, '127.0.0.1', 6000) as c:
    #    pong = c.ping()
    #    print(pong)
    client = make_client(pp_thrift.PingService, '127.0.0.1', 6000)
    print(client.ping())
if __name__ == '__main__':
    main()
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
注释里是另一种创建链接的方式。

目录结构：

├── client.py
├── pingpong.thrift
└── server.py
1
2
3
运行
运行server端：

$ python server.py 
serving...
1
2
运行client端：

$ python client.py 
pong
1
2
server端输出：

ping pong!
