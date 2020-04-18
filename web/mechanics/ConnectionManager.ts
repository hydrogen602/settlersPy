import { Config } from "../Config"
import { defined, assertInt } from "../util";
import { JsonParser } from "../jsonParser";
import { GameMap } from "../map/GameMap";
import { Hex } from "../graphics/Hex";
import { ctx } from "../graphics/Screen";

// ws = new WebSocket('ws://127.0.0.1:5050')

export class ConnectionManager {

    private ws: WebSocket | null;
    private url: string;

    private token: string | null;

    private spinner: HTMLElement;

    public static instance: ConnectionManager;

    constructor(ip: string, port: number) {
        assertInt(port);

        ConnectionManager.instance = this;

        this.url = 'ws://' + ip + ":" + port;

        defined(this.url);

        const tmp: HTMLElement | null = document.getElementById('connectionStatus');
        if (tmp == null) {
            throw new Error("Element with tag 'connectionStatus' not found")
        }
        this.spinner = <HTMLElement>tmp;

        this.ws = null;
        this.token = null;
        this.connect();
    }

    private connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onmessage = function(e: MessageEvent) {
            ConnectionManager.instance.onmessage(e);
        };

        this.ws.onopen = function(ev: Event) {
            ConnectionManager.instance.onopen(ev);
        };

        defined(this.ws);
    }

    doneLoading() {
        this.spinner.style['opacity'] = '0';
    }

    loading() {
        this.spinner.style['opacity'] = '100';
    }

    /**
     * The function handles the JSON.stringify
     * 
     * @param o An object to send.
     */
    send(o: Object) {
        const msg = JSON.stringify(o);
        if (this.ws) {
            this.ws.send(msg);
        }
        else {
            console.log('Disconnected');
        }
        
        this.loading();
    }

    getHistory() {
        if (this.ws) {
            this.ws.send('history');
        }
        else {
            console.log('Disconnected');
        }
        this.loading();
    }

    onopen(ev: Event) {
        if (this.ws) {
            this.ws.send('Hi');
        }
        else {
            console.log('Disconnected');
        }
        
        this.getHistory();
        this.loading();
    }

    onmessage(e: MessageEvent) {
        if (e.data == "Hello") {
            console.log("Successful Echo, Server is alive!");
        }
        else {
            try {
                this.doneLoading();

                const obj = JSON.parse(e.data);

                console.log("got msg");
                console.log(obj);

                if ('token' in obj) {
                    const token: string = JsonParser.requireString(obj, 'token');
                    console.log('yeet')
                    if (!this.token) {
                        // remember the token
                        console.log('Got token', token)
                        this.token = token;
                    }
                }

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
