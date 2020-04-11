import { Config } from "../Config"
import { defined } from "../util";

// ws = new WebSocket('ws://127.0.0.1:5050')

export class ConnectionManager {

    private ws: WebSocket
    private url: string;

    private testPhase: number;

    public static instance: ConnectionManager;

    constructor() {
        ConnectionManager.instance = this;

        this.url = 'ws://' + Config.getIP() + ":" + Config.getPort();
        this.ws = new WebSocket(this.url);

        this.ws.onmessage = function(e: MessageEvent) {
            ConnectionManager.instance.onmessage(e);
        };

        this.ws.onopen = function(ev: Event) {
            ConnectionManager.instance.onopen(ev);
        };

        this.testPhase = -1;

        defined(this.url);
        defined(this.ws);
    }

    ready() {
        // passed tests
        return this.testPhase == 2
    }

    send(o: Object) {
        const msg = JSON.stringify(o);
        this.ws.send(msg);
    }

    onopen(ev: Event) {
        this.ws.send('Hi');
        this.testPhase = 0;
    }

    onmessage(e: MessageEvent) {
        if (this.testPhase == 0 && e.data == "Hello") {
            this.testPhase = 1;
            console.log("Successful Echo, Server is alive!");
            this.send({"test": "verify"});
        }
        else {
            try {
                const obj = JSON.parse(e.data);
                if (this.testPhase == 1 && "test" in obj && obj["test"] == "echo verified") {
                    this.testPhase = 2;
                    console.log("JSON echo success");
                }
                
                if ("update" in obj) {
                    // update
                    console.log("got msg")
                    console.log(obj)
                }
            } catch (SyntaxError) {
                // not json
            }
        }
        
    }
}

const c = new ConnectionManager();
