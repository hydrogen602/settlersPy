import { RelPoint, AbsPoint } from "./Point";
import { defined } from "../util";

export class MessageBoard {
    private ctx: CanvasRenderingContext2D;

    private pos = new RelPoint(10, 10);
    private sz: AbsPoint;
    private maxMsgCount: number;

    private board: Array<string> = [];

    constructor(ctx: CanvasRenderingContext2D, size: number, location?: RelPoint) {
        this.ctx = ctx;
        this.maxMsgCount = size;
        this.sz = new AbsPoint(350, 30 * size);

        defined(this.ctx);
        defined(this.maxMsgCount);
        defined(this.sz);

        if (location != undefined) {
            this.pos = location;
        }
    }

    print(msg: string) {
        this.board.push(msg);
        if (this.board.length > this.maxMsgCount) {
            this.board.shift();
        }
        this.draw()
    }

    clear() {
        this.board = [];
    }

    draw() {
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(this.pos.x, this.pos.y, this.sz.x, this.sz.y);
        this.ctx.strokeStyle = "black";
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(this.pos.x, this.pos.y, this.sz.x, this.sz.y);

        if (this.board.length == 0) {
            return;
        }

        this.ctx.font = "16px Arial";
        this.ctx.textAlign = "left";
        this.ctx.textBaseline = "top";
        this.ctx.fillStyle = "black";

        for (let i = 0; i < this.board.length; i++) {
            this.ctx.fillText(this.board[i], this.pos.x + 5, this.pos.y + 10 + 26 * i);
        }
        
    }
}
