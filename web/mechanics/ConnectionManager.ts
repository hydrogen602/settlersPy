import { defined, assertInt } from "../util";
import { JsonParser } from "../jsonParser";
import { GameMap } from "../map/GameMap";
import { Hex } from "../graphics/Hex";
import { ctx } from "../graphics/Screen";
import { newNotification } from "../ui/notifications";

// ws = new WebSocket('ws://127.0.0.1:5050')

export class ConnectionManager {

    private ws: WebSocket | null;
    private url: string;

    private token: string | null;

    private connected: boolean;

    private failedAttempts: number;

    private spinner: HTMLElement;

    private onmessageCallback: (obj: object) => void;

    public static instance: ConnectionManager;

    constructor(ip: string, port: number, name: string, onmessage: (obj: object) => void) {
        assertInt(port);

        ConnectionManager.instance = this;

        this.url = 'ws://' + ip + ":" + port + '/' + name;

        this.onmessageCallback = onmessage;

        defined(this.url);

        const tmp: HTMLElement | null = document.getElementById('connectionStatus');
        if (tmp == null) {
            throw new Error("Element with tag 'connectionStatus' not found")
        }
        this.spinner = <HTMLElement>tmp;

        this.failedAttempts = 0;

        this.ws = null;
        this.token = null;
        this.connected = false;
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

        this.ws.onclose = function(ev: Event) {
            ConnectionManager.instance.onclose(ev);
        }

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

        this.failedAttempts = 0;

        newNotification('Connected to Server');

        this.connected = true;
        
        this.getHistory();
        this.loading();
    }

    onclose(ev: Event) {
        this.connected = false;
        newNotification('Lost Connection', true);

        this.failedAttempts += 1;

        console.log(this.failedAttempts);

        if (this.failedAttempts > 10) {
            newNotification('No longer trying to connect', true);
            return;
        }
        
        setTimeout(function() {
            newNotification('Reconnecting...');
            ConnectionManager.instance.loading();
            ConnectionManager.instance.connect();
        }, 3000);
        
    }

    onmessage(e: MessageEvent) {
        if (e.data == "Hello") {
            console.log("Successful Echo, Server is alive!");
        }
        else {
            try {
                this.doneLoading();

                const obj = JSON.parse(e.data);

                console.log("got msg:", obj);

                if ('token' in obj) {
                    const token: string = JsonParser.requireString(obj, 'token');
                    if (!this.token) {
                        // remember the token
                        console.log('Got token', token)
                        this.token = token;
                    }
                    return;
                }

                this.onmessageCallback(obj);
            } catch (e) {
                if (e.name == 'SyntaxError') {
                    console.log('Got invalid JSON')
                }
                else {
                    console.log('Error:', e)
                    console.log('Error data:', e.data)
                }
            }
        }
        
    }
}
