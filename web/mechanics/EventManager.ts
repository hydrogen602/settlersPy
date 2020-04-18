import { AbsPoint, RelPoint } from "../graphics/Point";
import { square } from "../util";
import { Hex } from "../graphics/Hex";
import { GameManager } from "./GameManager";
import { Settlement } from "../map/Settlement";
import { ctx } from "../graphics/Screen";
import { Road } from "../map/Road";
import { Tile } from "../map/Tile";
import { ConnectionManager } from "./ConnectionManager";

export class EventManager {

    private constructor() {}

    static distanceFromNearestHexCorner(p: AbsPoint|RelPoint) {
        const abs = p.toAbsPoint(); // if already absolute, it returns a copy of itself
        const backConvertedHex = p.toHexPoint().toAbsPoint();

        return Math.sqrt(square(abs.x - backConvertedHex.x) + square(abs.y - backConvertedHex.y));
    }

    static mouseHoverHandler(e: MouseEvent) {
        if (GameManager.instance.mayPlaceRobber) {
            const p = new RelPoint(e.clientX, e.clientY);

            const m = GameManager.instance.getMap();

            const tile = m.getAllowedRobberPlace(p.toAbsPoint());
            if (tile != undefined) {
                const tileExists = <Tile>tile;
                tileExists.strokeRobber(ctx);
            }
            else {
                GameManager.instance.draw();
            }
        }
        else if (GameManager.instance.mayPlaceSettlement) {            
            const p = new RelPoint(e.clientX, e.clientY);
            const r = EventManager.distanceFromNearestHexCorner(p);
            
            if (r < Hex.getSideLength() / 4) {
                // hovering over a corner
                const h = p.toHexPoint();

                const m = GameManager.instance.getMap();

                if (m.isAllowedSettlement(h)) {
                    const back = h.toRelPoint();
                    Settlement.stroke(back, ctx);
                }
            }
            else {
                GameManager.instance.draw();
            }
        }
        else if (GameManager.instance.mayPlaceCity) {
            const p = new RelPoint(e.clientX, e.clientY);
            const r = EventManager.distanceFromNearestHexCorner(p);

            // strokeCity
            if (r < Hex.getSideLength() / 3.5) {
                const h = p.toHexPoint();

                const m = GameManager.instance.getMap();

                if (m.isAllowedCity(h)) {
                    Settlement.strokeCity(h.toRelPoint(), ctx);
                }
            }
            else {
                GameManager.instance.draw();
            }
        }
        else if (GameManager.instance.mayPlaceRoad) {
            // if (this.roadTmpFirstEnd == undefined) {
            const p = new RelPoint(e.clientX, e.clientY);
            const hArr = p.toDualHexPoint();

            const m = GameManager.instance.getMap();
            
            if (hArr.length == 2 && m.isAllowedRoad(hArr[0], hArr[1])) { // hArr is empty if not over a line
                GameManager.instance.draw();

                // hovering over a line
                Road.stroke(hArr[0].toRelPoint(), hArr[1].toRelPoint(), ctx);
            }
            else {
                GameManager.instance.draw();
            }
        }
    }

    static mouseHandler(e: MouseEvent) {
        const p = new RelPoint(e.clientX, e.clientY);
        const r = EventManager.distanceFromNearestHexCorner(p);
        const m = GameManager.instance.getMap();

        if (GameManager.instance.mayPlaceRobber) {
            const tile = m.getAllowedRobberPlace(p.toAbsPoint());
            // if (tile != undefined) {
            //     const tileExists = <Tile>tile;
            //     GameManager.instance.moveRobber(tileExists);
            //     GameManager.instance.draw();
            //     GameManager.instance.mayPlaceRobber = false;
            // }
            // else {
            //     GameManager.instance.draw();
            // }
        }
        else if (GameManager.instance.mayPlaceSettlement) {            
            
            if (r < Hex.getSideLength() / 4) {
                // clicked on a corner
                const h = p.toHexPoint();
                //console.log("new settlement");

                // if (m.isAllowedSettlement(h)) {
                //     m.addSettlement(new Settlement(h, GameManager.instance.getSelf()));

                //     GameManager.instance.draw();
                //     //console.log("success");
                //     GameManager.instance.print("New Settlement created");
                //     GameManager.instance.mayPlaceSettlement = false;
                // }
                // else {
                //     // console.log("not allowed position");
                //     GameManager.instance.printErr("Illegal Position");
                // }
            }
        }
        else if (GameManager.instance.mayPlaceCity) {
            // strokeCity
            if (r < Hex.getSideLength() / 3.5) {
                const h = p.toHexPoint();

                if (m.isAllowedCity(h)) {
                    m.addCity(h);
                    GameManager.instance.draw();
                    GameManager.instance.print("New City created");
                    GameManager.instance.mayPlaceCity = false;
                }
                else {
                    // console.log("not allowed position");
                    GameManager.instance.printErr("Illegal Position");
                }
            }
        }
        else if (GameManager.instance.mayPlaceRoad) {
            const hArr = p.toDualHexPoint();            
            if (hArr.length == 2) { // hArr is empty if not over a line 
                // if (m.isAllowedRoad(hArr[0], hArr[1])) { // check if road already there
                //     m.addRoad(new Road(hArr[0], hArr[1], GameManager.instance.getSelf()));
                //     GameManager.instance.draw();
                //     GameManager.instance.print("New Road created");
                //     GameManager.instance.mayPlaceRoad = false;
                // }
                // else {
                //     GameManager.instance.printErr("Illegal Position");
                // }
            }
        }
    }

    static purchaseRoad() {
        ConnectionManager.instance.send({'action': 'purchase', 'name': 'road'})
        //GameManager.instance.purchaseRoad();
    }

    static purchaseSettlement() {
        ConnectionManager.instance.send({'action': 'purchase', 'name': 'settlement'})
        //GameManager.instance.purchaseSettlement();
    }

    static purchaseCity() {
        ConnectionManager.instance.send({'action': 'purchase', 'name': 'city'})
        //GameManager.instance.purchaseCity();
    }


}