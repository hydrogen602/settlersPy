import { GameManager } from "./GameManager";
import { Desert } from "../map/Biome";
import { randomInt, defined } from "../util";
import { Tile } from "../map/Tile";

export class Robber {

    private place: Tile;

    constructor(tiles: Array<Tile>) {

        this.place = tiles[0];

        // let found = false;
        // for (const k of tiles) {
        //     if (k.getLandType() == Desert) {
        //         this.place = k;
        //         found = true;
        //         break
        //     }
        // }

        // if (!found) {
        //     const randoKey = randomInt(tiles.length);
        //     this.place = tiles[randoKey];
        // }

        defined(this.place);

        // this.place.arriveRobber();
    }

    getTile() {
        return this.place;
    }

    moveTo(t: Tile) {
        // tell server

        // this.place.departRobber();
        // this.place = t;
        // this.place.arriveRobber();
    }

    // draw() {} handled by Tile

}