export function processInput(conn, keyboardInput){
    var power = 0
    var dir = 0
    if(keyboardInput.checkKey("w")){
        power += .5
    }
    if(keyboardInput.checkKey("s")){
        power -= .5
    }
    if(keyboardInput.checkKey("a")){
        dir += .5
    }
    if(keyboardInput.checkKey("d")){
        dir -= .5
    }
    conn.send({
        "type": "DriveCmd",
        "angle": dir,
        "power": power
    })
}
