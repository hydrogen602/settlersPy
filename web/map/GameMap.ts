import { HexPoint, AbsPoint } from "../graphics/Point";
import { Tile } from "./Tile";
import { defined } from "../util";
import { Settlement } from "./Settlement";
import { canvas } from "../graphics/Screen";
import { Road } from "./Road";
import { GameManager } from "../mechanics/GameManager";
import { JsonParser } from "../jsonParser";
import { ctx } from "../graphics/Screen";

export class GameMap {
    private sz: number;
    private tilesArr: Array<Tile>;
    private settlementsArr: Array<Settlement>;
    private roadsArr: Array<Road>;
    private ctx: CanvasRenderingContext2D;

    static instance: GameMap;

    // offset of map on screen in order to move around the map
    // currLocation: RelPoint;

    constructor(size: number, ctx: CanvasRenderingContext2D, tiles: Array<Tile>) {
        GameMap.instance = this;

        this.sz = size;
        this.ctx = ctx;

        defined(this.sz);
        defined(this.ctx);

        this.tilesArr = tiles;

        defined(this.tilesArr);

        this.settlementsArr = [];
        this.roadsArr = [];
    }

    static fromJson(data: object): GameMap {
        JsonParser.requireName(data, 'GameMap');

        const n = JsonParser.requireNumber(data, '_GameMap__size');
        const tilesArr_tmp: Array<any> = JsonParser.requireArray(data, 'tiles');

        const tilesArr: Array<Tile> = [];
        for (const t of tilesArr_tmp) {
            tilesArr.push(Tile.fromJson(t));
        }

        return new GameMap(n, ctx, tilesArr);
    }

    getTiles() {
        return this.tilesArr;
    }

    getSettlements() {
        return this.settlementsArr;
    }

    getRoads() {
        return this.roadsArr;
    }

    getCtx() {
        return this.ctx;
    }

    isWithinMap(h: HexPoint): boolean {
        const n = this.sz;

        if (h.x < 0 || h.x > 2 * n - 1) {
            return false;
        }
        const yAllowance = Math.abs(h.x - n + 0.5) - n + 0.5;
        if (h.y < yAllowance || h.y > 2 * n - yAllowance) {
            return false;
        }
        return true;
    }

    getAllowedRobberPlace(a: AbsPoint): Tile | undefined {
        let currTile = GameManager.instance.getRobber().getTile()
        for (const t of this.tilesArr) {
            if (t.isInside(a) && t != currTile) {
                return t;
            }
        }

        return undefined;
    }

    isAllowedSettlement(h: HexPoint): boolean {
        if (!this.isWithinMap(h)) {
            return false;
        }

        // console.log("new?", h)
        const conflicts = this.settlementsArr.filter(s => {
            // console.log("check", s.getHexPoint())
            const hp = s.getHexPoint();
            return h.isNeighbor(hp) || h.isEqual(hp);
        });

        if (conflicts.length > 0) { // allowed if no conflicts
            return false;
        }

        if (!GameManager.instance.isEarlyRound()) {

            const currPlayer = GameManager.instance.getCurrentPlayer();

            let permitted = false;
            currPlayer.getRoads().forEach(r => {
                if (r.isAdjacent(h)) {
                    permitted = true;
                }
            });

            if (!permitted) {
                return false;
            }
        }

        return true;
    }

    isAllowedCity(h: HexPoint) {
        // at settlement
        const currPlayer = GameManager.instance.getCurrentPlayer();
        let permitted = false;
        currPlayer.getSettlements().forEach(s => {
            const settlementLoc = s.getHexPoint();
            if (settlementLoc.isEqual(h) && !s.isCity()) {
                permitted = true;
            }
        });

        return permitted;
    }

    isAllowedRoad(p1: HexPoint, p2: HexPoint): boolean {
        if (!p1.isNeighbor(p2) || p1.isEqual(p2)) {
            // if the points aren't adjacent or are the same, do not allow
            return false;
        }

        if (!this.isWithinMap(p1)) {
            return false;
        }
        if (!this.isWithinMap(p2)) {
            return false;
        }

        // next to road or settlement owned
        const currPlayer = GameManager.instance.getCurrentPlayer();
        let permitted = false;
        currPlayer.getSettlements().forEach(s => {
            const settlementLoc = s.getHexPoint();
            if (settlementLoc.isEqual(p1) || settlementLoc.isEqual(p2)) {
                permitted = true;
            }
        });

        if (!permitted) {
            currPlayer.getRoads().forEach(r => {
                if (r.isAdjacent(p1) || r.isAdjacent(p2)) {
                    permitted = true;
                }
            });
        }

        if (!permitted) {
            return false;
        }

        const conflicts = this.roadsArr.filter(r => {
            return r.isEqual(p1, p2);
        });

        return conflicts.length == 0;
    }

    addSettlement(s: Settlement) {
        defined(s);
        this.settlementsArr.push(s);
    }

    addCity(h: HexPoint) {
        defined(h);
        const currPlayer = GameManager.instance.getCurrentPlayer();

        const re = currPlayer.getSettlements().filter(s => {
            const settlementLoc = s.getHexPoint();
            return settlementLoc.isEqual(h);
        });

        if (re.length < 0 || re.length > 1) {
            throw "Illegal Number of Settlements";
        }

        if (re.length == 1) {
            re[0].upgrade();
        }
        else {
            throw "Illegal Position";
        }
    }

    addRoad(r: Road) {
        defined(r)
        this.roadsArr.push(r);
    }

    draw_SHOULD_ONLY_BE_CALLED_BY_GAME_MANAGER() {
        this.ctx.clearRect(0, 0, canvas.width, canvas.height);

        this.ctx.fillStyle = 'blue';
        this.ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);

        this.ctx.strokeStyle = 'black';
        this.ctx.lineWidth = 1;
        this.tilesArr.forEach(e => {
            e.draw(this.ctx);
        });

        this.tilesArr.forEach(e => {
            e.highlightIfActive(this.ctx);
        });

        this.roadsArr.forEach(r => {
            r.draw(this.ctx);
        });

        this.settlementsArr.forEach(s => {
            s.draw(this.ctx);
        });
    }
}
