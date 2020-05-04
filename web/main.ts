
// import { ctx } from "./graphics/Screen";
//import { GameMap } from "./map/GameMap";
// import { currLocation, maxDistance, centerOfScreen } from "./graphics/Point";
//import { Player } from "./mechanics/Player";
// import { EventManager } from "./mechanics/EventManager";
// import { GameManager } from "./mechanics/GameManager";
import { ConnectionManager } from "./mechanics/ConnectionManager";

function main() {
    
    // cm.getHistory(); <- called onopen

    //const m = new GameMap(Config.getN(), ctx);

    //GameManager.instance = new GameManager(m, [new Player('blue', 'Blue Team'), new Player('green', 'Green Team')]);
    
    //GameManager.instance.draw();
}

function setup() {
    
    const name = (<HTMLInputElement>document.getElementById("nameInput")).value;
    const ip = (<HTMLInputElement>document.getElementById("ipAddrInput")).value;
    const port = (<HTMLInputElement>document.getElementById("portInput")).value;

    const cm = new ConnectionManager(ip, parseInt(port), name);

    (<HTMLElement>document.getElementById("introBannerCover")).hidden = true;
}

const maybeButton = document.getElementById("submitInput");
if (maybeButton == null) {
    throw new Error("missing submit button");
}
else {
    const button = <HTMLElement>maybeButton;
    button.onclick = setup
}

// ctx.fillStyle = 'black';
// ctx.fillRect(currLocation.x, currLocation.y, 10, 10); 

// document.addEventListener("wheel", function (e) {
//     const limit = 5;

//     currLocation.x -= Math.max(-limit, Math.min(e.deltaX, limit));
//     currLocation.y -= Math.max(-limit, Math.min(e.deltaY, limit));

//     currLocation.x = Math.max(-maxDistance, Math.min(currLocation.x - centerOfScreen.x, maxDistance)) + centerOfScreen.x;
//     currLocation.y = Math.max(-maxDistance, Math.min(currLocation.y - centerOfScreen.y, maxDistance)) + centerOfScreen.y;

//     GameManager.instance.draw();
// });

// document.onmousedown = EventManager.mouseHandler;
// document.onmousemove = EventManager.mouseHoverHandler;

// window.onkeypress = (e: KeyboardEvent) => {
//     if (e.key == 'p') {
//         console.log("Debug Players:")
//         GameManager.instance.debugPlayers();
//     }
//     if (e.key == 't') {
//         GameManager.instance.playTurn();
//     }
// }

//console.info("Starting Game");
//GameManager.instance.playTurn();
