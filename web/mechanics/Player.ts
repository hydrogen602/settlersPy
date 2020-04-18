import { defined, assertInt } from "../util";
import { Settlement } from "../map/Settlement";
import { ResourceType } from "../dataTypes";
import { Road } from "../map/Road";
import { MessageBoard } from "../graphics/MessageBoard";
import { ctx } from "../graphics/Screen";
import { RelPoint } from "../graphics/Point";
import { GameManager } from "./GameManager";
import { Inventory } from "./Inventory";

export class Player {
    private color: string;
    private settlements: Array<Settlement> = [];
    private roads: Array<Road> = [];
    private name: string;
    private inventory: Inventory;

    private invBoard: MessageBoard;

    private static playerCount = 0;

    constructor(color: string, name: string) {
        this.color = color;
        this.name = name;
        this.settlements = [];
        defined(color);
        defined(name);

        this.inventory = new Inventory();

        this.invBoard = new MessageBoard(ctx, 6, new RelPoint(window.innerWidth - 250 - 5, 5 + 6 * 30 * Player.playerCount));
        Player.playerCount += 1;

        defined(this.invBoard);
        this.updateInvBoard();
    }

    getRoads() {
        return this.roads;
    }

    getSettlements() {
        return this.settlements;
    }

    getColor() {
        return this.color;
    }

    getName() {
        return this.name;
    }

    addSettlement(s: Settlement) {
        this.settlements.push(s);
    }

    addRoad(r: Road) {
        this.roads.push(r);
    }

    giveResource(r: ResourceType, amount: number) {
        assertInt(amount);
        this.inventory.update(r, amount)
        this.updateInvBoard();
    }

    genericTrade(toPlayer: ResourceType, n: number, fromPlayer: ResourceType, m: number): boolean {
        assertInt(n);
        assertInt(m);
        if (this.inventory.hasEnough(fromPlayer, m)) {
            // trade !!
            this.inventory.update(fromPlayer, -m);
            this.inventory.update(toPlayer, n);

            return true;
        }
        else {
            return false; // trade failed cause not enough resources
        }
    }

    bankTrade(toPlayer: ResourceType, fromPlayer: ResourceType): boolean {
        return this.genericTrade(toPlayer, 1, fromPlayer, 4);
    }

    // purchaseRoad() {
    //     if (GameManager.instance.mayPlaceRoad) {
    //         GameManager.instance.printErr("Place road before buying another");
    //         return;
    //     }
    //     if (GameManager.instance.getCurrentPlayer() != this) {
    //         throw "Not this player's turn";
    //     }

    //     if (this.inventory.purchase([ResourceType.Brick, ResourceType.Lumber], [1, 1])) {
    //         GameManager.instance.mayPlaceRoad = true;
    //         GameManager.instance.print("Place new road");
    //         this.updateInvBoard();
    //     }
    //     else {
    //         GameManager.instance.printErr("Can't afford road");
    //     }
    // }

    // purchaseCity() {
    //     if (GameManager.instance.mayPlaceCity) {
    //         GameManager.instance.printErr("Place city before buying another");
    //         return;
    //     }
    //     if (GameManager.instance.getCurrentPlayer() != this) {
    //         throw "Not this player's turn";
    //     }
    //     // requires 3 ore and 2 wheat
    //     if (this.inventory.purchase([ResourceType.Wheat, ResourceType.Ore], [2, 3])) {
    //         // new city!
    //         GameManager.instance.mayPlaceCity = true;
    //         GameManager.instance.print("Place new city");
    //         this.updateInvBoard();
    //     }
    //     else {
    //         GameManager.instance.printErr("Can't afford city");
    //     }
    // }

    // purchaseSettlement() {
    //     if (GameManager.instance.mayPlaceSettlement) {
    //         GameManager.instance.printErr("Place settlement before buying another");
    //         return;
    //     }
    //     if (GameManager.instance.getCurrentPlayer() != this) {
    //         throw "Not this player's turn";
    //     }

    //     if (this.inventory.purchase(
    //             [ResourceType.Brick, ResourceType.Lumber, ResourceType.Sheep, ResourceType.Wheat], [1, 1, 1, 1])) {

    //         // new settlement!
    //         GameManager.instance.mayPlaceSettlement = true;
    //         GameManager.instance.print("Place new settlement");
    //         this.updateInvBoard();
    //     }
    //     else {
    //         GameManager.instance.printErr("Can't afford settlement");
    //     }
    // }

    private updateInvBoard() {
        this.invBoard.clear();
        this.invBoard.print(this.name);

        for (const k of this.inventory.keys()) {
            this.invBoard.print(ResourceType[k] + ": " + this.inventory.get(k));
        }     
    }

    draw() {
        this.invBoard.draw();
    }

    debug() {
        console.log(this)
        this.settlements.forEach(e => {
            console.log("  ", e)
        });
        console.log("  Inv:", this.inventory);
    }


}