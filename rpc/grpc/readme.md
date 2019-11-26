官方：[python quickstart](https://grpc.io/docs/quickstart/python.html#run-a-grpc-application)

grpc 的环境安装
grpc 的基础: protobuf
grpc helloworld: python 实战 grpc 环境配置
grpc basic: grpc 4 种通信方式
grpc 的基础: protobuf
grpc 使用 protobuf 进行数据传输. protobuf 是一种数据交换格式, 由三部分组成:

# python grpc环境搭建：

protobuf 运行时(runtime): protobuf 运行时所需要的库, 和 protoc 编译生成的代码进行交互
protobuf 运行时(runtime),  安装 grpc 相关的 python 模块(module) 即可
pip install grpcio

protoc: protobuf 编译器(compile), 将 proto 文件编译成不同语言的实现, 这样不同语言中的数据就可以和 protobuf 格式的数据进行交互
使用 protoc 编译 proto 文件, 生成 python 语言的实现, 安装 python 下的 protoc 编译器
pip install grpcio-tools

# Hello world协议proto：
proto 文件: 使用的 proto 语法的文本文件, 用来定义数据格式
proto语法现在有 proto2 和 proto3 两个版本, 推荐使用 proto3, 更加简洁明了

// helloworld.proto
syntax = "proto3";

service Greeter {
    rpc SayHello(HelloRequest) returns (HelloReply) {}
    rpc SayHelloAgain(HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}

#编译 proto 文件命令
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
#命令解释
python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
--python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
--grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
-I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录

#编译后生成的代码:
helloworld_pb2.py: 用来和 protobuf 数据进行交互
helloworld_pb2_grpc.py: 用来和 grpc 进行交互

使用 protobuf 的过程:
编写 proto 文件 -> 使用 protoc 编译 -> 添加 protobuf 运行时 -> 项目中集成
更新 protobuf 的过程:
修改 proto 文件 -> 使用 protoc 重新编译 -> 项目中修改集成的地方
PS: proto3 的语法非常非常的简单, 上手 protobuf 也很轻松, 反而是配置 protoc 的环境容易卡住, 所以推荐使用 python 入门, 配置 protoc 这一步非常省心.

# 最后一步, 编写 helloworld 的 grpc 实现:
服务器端: helloworld_grpc_server.py
from concurrent import futures
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

# 实现 proto 文件中定义的 GreeterServicer
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # 实现 proto 文件中定义的 rpc 调用
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message = 'hello {msg}'.format(msg = request.name))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='hello {msg}'.format(msg = request.name))

def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

#客户端: helloworld_grpc_client.py

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:50051')
    # 调用 rpc 服务
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='czl'))
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='daydaygo'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    run()

运行 python helloworld_grpc_server.py 和 python helloworld_grpc_client.py, 就可以看到效果了
