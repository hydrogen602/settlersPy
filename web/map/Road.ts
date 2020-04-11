import { HexPoint, RelPoint } from "../graphics/Point";
import { defined } from "../util";
import { Player } from "../mechanics/Player";

export class Road {
    private p1: HexPoint;
    private p2: HexPoint;
    // two endpoints of the line

    private owner: Player;

    constructor(p1: HexPoint, p2: HexPoint, owner: Player) {
        this.p1 = p1;
        this.p2 = p2;
        this.owner = owner;

        defined(p1);
        defined(p2);
        defined(owner);

        this.owner.addRoad(this);
    }

    isEqual(p1: HexPoint, p2: HexPoint): boolean {
        if (p1.isEqual(this.p1) && p2.isEqual(this.p2)) {
            return true
        }
        if (p1.isEqual(this.p2) && p2.isEqual(this.p1)) {
            return true
        }
        return false;
    }

    isAdjacent(p: HexPoint): boolean {
        if (p.isEqual(this.p1) || p.isEqual(this.p2)) {
            return true;
        }
        return false;
    }

    draw(ctx: CanvasRenderingContext2D) {
        ctx.strokeStyle = "black";
        ctx.lineWidth = 14;
        ctx.beginPath();
        const tmp1 = this.p1.toRelPoint();
        const tmp2 = this.p2.toRelPoint();
        ctx.moveTo(tmp1.x, tmp1.y);
        ctx.lineTo(tmp2.x, tmp2.y);
        ctx.stroke();

        ctx.strokeStyle = this.owner.getColor();
        ctx.lineWidth = 10;
        ctx.beginPath();
        ctx.moveTo(tmp1.x, tmp1.y);
        ctx.lineTo(tmp2.x, tmp2.y);
        ctx.stroke();
    }

    static stroke(tmp1: RelPoint, tmp2: RelPoint, ctx: CanvasRenderingContext2D) {
        ctx.strokeStyle = "black";
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.moveTo(tmp1.x, tmp1.y);
        ctx.lineTo(tmp2.x, tmp2.y);
        ctx.stroke();
    }

}