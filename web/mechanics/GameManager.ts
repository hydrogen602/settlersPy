import { Player } from "./Player";
import { GameMap } from "../map/GameMap";
import { defined } from "../util";
import { MessageBoard } from "../graphics/MessageBoard";
import { RelPoint } from "../graphics/Point";
import { Robber } from "./Robber";
import { Tile } from "../map/Tile";
import { ConnectionManager } from "./ConnectionManager";

export class GameManager {

    private isTurn: boolean;
    private map: GameMap;
    private rounds: number = 1;
    private msgBoard: MessageBoard;
    private errBoard: MessageBoard;

    private self: Player;

    private players: Array<Player>;

    private rob: Robber;

    static instance: GameManager;

    // game states
    mayPlaceSettlement = false;
    mayPlaceCity = false;
    mayPlaceRoad = false;

    mayPlaceRobber = false;

    constructor(map: GameMap) {
        GameManager.instance = this
        this.map = map;

        this.isTurn = false;


        this.msgBoard = new MessageBoard(map.getCtx(), 3);
        this.errBoard = new MessageBoard(map.getCtx(), 1, new RelPoint(10, 10 + 90));

        this.msgBoard.print("Hello World!");

        this.rob = new Robber(this.map.getTiles());

        this.self = new Player('blue', 'self');
        this.players = [this.self];


        defined(this.map);
        defined(this.msgBoard);
        defined(this.rob);
        defined(this.self);
        defined(this.players);
    }

    getSelf() {
        return this.self;
    }

    getRobber() {
        return this.rob;
    }

    getMap() {
        return this.map;
    }

    isCurrentPlayer() {
        return this.isTurn;
    }

    isEarlyRound(): boolean {
        return this.rounds <= 2; // first two rounds are special initialization rounds
    }

    private nextTurn() {
        if (this.mayPlaceCity || this.mayPlaceRoad || this.mayPlaceSettlement) {
            this.printErr("Unplaced Infrastructure");
            return;
        }
        else if (this.mayPlaceRobber) {
            this.printErr("Unmoved Robber");
            return;
        }

        this.msgBoard.clear();
        this.errBoard.clear();

        ConnectionManager.instance.send({'action': 'nextTurn'});
    }

    print(msg: string) {
        this.msgBoard.print(msg);
        this.errBoard.clear();
    }

    printErr(msg: string) {
        this.errBoard.print(msg);
    }

    draw() {
        this.map.draw_SHOULD_ONLY_BE_CALLED_BY_GAME_MANAGER();
        this.msgBoard.draw();
        this.errBoard.draw();
        // this.players.forEach(p => {
        //     p.draw();
        // });
    }

    moveRobber(t: Tile) {
        // this.rob.moveTo(t);
    }

}
