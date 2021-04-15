export class KeyboardInput{
    constructor(){
        this.keysDown = {}
        document.addEventListener("keydown", this.keydown.bind(this))
        document.addEventListener("keyup", this.keyup.bind(this))
    }

    keydown(evt){
        this.keysDown[evt.key] = true
    }

    keyup(evt){
        if(evt.key in this.keysDown){
            this.keysDown[evt.key] = false
        }
    }

    checkKey(key){
        return key in this.keysDown && this.keysDown[key]
    }
}