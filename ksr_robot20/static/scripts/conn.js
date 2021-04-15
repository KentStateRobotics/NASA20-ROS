export class Conn{
    constructor(ip, port){
        this.ip = ip
        this.port = port
        this.connect()
    }

    connect(){
        this.conn = new WebSocket("ws://" + this.ip + ':' + this.port)
        this.conn.onmessage = this.onMessage
        this.conn.onopen = this.onOpen
        this.conn.onclose = this.onClose
    }

    onMessage(msg){

    }

    onOpen(evt){
        console.log("OPEN")
    }

    onClose(evt){
        console.log("CLOSE")
    }

    send(msg){
        if(this.conn.readyState == WebSocket.OPEN){
            this.conn.send(JSON.stringify(msg))
        }
    }
}