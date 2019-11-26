const string HELLO_WORLD = "world"

service HelloWorld {
    void ping(),
    string sayHello(),
    string sayMsg(1:string msg)
}

