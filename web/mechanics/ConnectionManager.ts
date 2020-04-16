import { Config } from "../Config"
import { defined, assertInt } from "../util";
import { JsonParser } from "../jsonParser";
import { GameMap } from "../map/GameMap";
import { Hex } from "../graphics/Hex";
import { ctx } from "../graphics/Screen";

// ws = new WebSocket('ws://127.0.0.1:5050')

export class ConnectionManager {

    private ws: WebSocket
    private url: string;

    public static instance: ConnectionManager;

    constructor(ip: string, port: number) {
        assertInt(port);

        ConnectionManager.instance = this;

        this.url = 'ws://' + ip + ":" + port;
        this.ws = new WebSocket(this.url);

        this.ws.onmessage = function(e: MessageEvent) {
            ConnectionManager.instance.onmessage(e);
        };

        this.ws.onopen = function(ev: Event) {
            ConnectionManager.instance.onopen(ev);
        };

        defined(this.url);
        defined(this.ws);
    }

    send(o: Object) {
        const msg = JSON.stringify(o);
        this.ws.send(msg);
    }

    getHistory() {
        this.ws.send('history')
    }

    onopen(ev: Event) {
        this.ws.send('Hi');
        this.getHistory();
    }

    onmessage(e: MessageEvent) {
        if (e.data == "Hello") {
            console.log("Successful Echo, Server is alive!");
        }
        else {
            try {
                const obj = JSON.parse(e.data);

                console.log("got msg")
                console.log(obj)

                if (JsonParser.askName(obj) == 'GameMap' && GameMap.instance == undefined) {
                    const g = GameMap.fromJson(obj);
                    g.draw_SHOULD_ONLY_BE_CALLED_BY_GAME_MANAGER();
                    ctx.fillStyle = 'black';
                }

            } catch (e) {
                if (e.name == 'SyntaxError') {
                    console.log('Got invalid JSON')
                }
                else {
                    console.log(e)
                    console.log(e.data)
                }
            }
        }
        
    }
}
