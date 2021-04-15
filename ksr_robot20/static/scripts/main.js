import * as wsConn from './conn.js'
import * as input from './input.js'
import { processInput } from './processInput.js'

const PORT = 4342
var ip = document.location.hostname || 'localhost'
var conn = null
var keyboardInput = null

function main(){
    conn = new wsConn.Conn(ip, PORT)
    keyboardInput = new input.KeyboardInput()
    requestAnimationFrame(inputLoop)
}

function inputLoop(){
    processInput(conn, keyboardInput)
    setTimeout(inputLoop, 100)
}

main()