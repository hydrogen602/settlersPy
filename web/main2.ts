import { ConnectionManager } from "./mechanics/ConnectionManager";
import { GameMap } from "./map/GameMap"
import { ctx } from "./graphics/Screen";
import { JsonParser } from "./jsonParser";
import { assert, defined } from "./util";
//import { currLocation, centerOfScreen, maxDistance } from "./graphics/Point";
import { newNotification } from "./ui/notifications";

interface Dictionary<T> {
    [key: string]: T;
}

class BasicPlayer {
    
    public name: string;
    private token: string;
    public color: string;

    private static allPlayers: Dictionary<BasicPlayer> = {};

    constructor(name: string, token: string, color: string) {
        this.name = name;
        this.token = token;
        this.color = color;
    }

    static updateFromArray(obj: Array<object>) {
        for (const p of obj) {
            JsonParser.requireName(p, 'Player');
            const token = JsonParser.requireString(p, 'token');
            //console.log(JsonParser.requireString(p, 'name'));

            if (!(token in this.allPlayers)) {
                const newPlayer = this.fromJson(p);
                this.allPlayers[token] = newPlayer;
            }
        }
    }

    private static fromJson(obj: object) {
        JsonParser.requireName(obj, 'Player');

        return new BasicPlayer(
            JsonParser.requireString(obj, 'name'),
            JsonParser.requireString(obj, 'token'),
            JsonParser.requireString(obj, 'color')
        );
    }
}

class Game {

    public isTurn: boolean;
    public map: GameMap;
    public roundNum: number;

    

    static instance: Game;

    private static hasInit: boolean = false
    
    constructor() {
        assert(!Game.hasInit, "Already Initialized");
        Game.hasInit = true;

        Game.instance = this;

        this.isTurn = false;

        this.map = new GameMap(ctx);

        this.roundNum = 0;

        defined(this.map);
        defined(this.isTurn);
        defined(this.roundNum);
    }

    public draw() {
        this.map.draw_SHOULD_ONLY_BE_CALLED_BY_GAME_MANAGER();
    }
}



function main(ip: string, port: number, name: string) {
    const g = new Game();
    const conn = new ConnectionManager(ip, port, name, messageHandler);

    function messageHandler(obj: object) {
        // obj is some object from a json
    
        const name = JsonParser.askName(obj)
        if (name == "") {
            // not a class but special message
            const msg_type = JsonParser.requireString(obj, 'type');

            if (msg_type == 'notification') {
                const msg = JsonParser.requireString(obj, 'content');
                newNotification(msg);
            }
            else if (msg_type == 'error') {
                const msg = JsonParser.requireString(obj, 'content');
                newNotification(msg, true);
            }
        }
    
        if (name == "Game") {
            newNotification('Game update');
            g.map.updateFromJson(JsonParser.requireObject(obj, 'gameMap'));
            g.map.draw_SHOULD_ONLY_BE_CALLED_BY_GAME_MANAGER();

            BasicPlayer.updateFromArray(JsonParser.requireArray(obj, 'players'));
        }
    }
}

main('localhost', 5000, 'debugPlayer');

// ====> Works but feels weird to use
// document.addEventListener("wheel", function (e) {
//     console.log(e);
//     const limit = 5;

//     currLocation.x -= Math.max(-limit, Math.min(e.deltaX, limit));
//     currLocation.y -= Math.max(-limit, Math.min(e.deltaY, limit));

//     currLocation.x = Math.max(-maxDistance, Math.min(currLocation.x - centerOfScreen.x, maxDistance)) + centerOfScreen.x;
//     currLocation.y = Math.max(-maxDistance, Math.min(currLocation.y - centerOfScreen.y, maxDistance)) + centerOfScreen.y;

//     Game.instance.draw();
// });


