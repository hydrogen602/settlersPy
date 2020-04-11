import { Biome, biomeDistributionArray, Desert } from "./Biome";
import { defined, assertInt, randomInt, shuffle } from "../util";
import { HexPoint, AbsPoint } from "../graphics/Point"
import { Hex } from "../graphics/Hex"
import { Settlement } from "./Settlement";
import { Config } from "../Config";

export class Tile {
    private p: HexPoint;
    private landType: Biome;
    private diceValue: number;
    private center: AbsPoint;

    private active: boolean = false; // whether this round's die roll matches this tile

    private static diceValueChoices = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12];

    private static localBiomeDistributionArray = biomeDistributionArray.slice();
    private static localDiceValueChoices = Tile.diceValueChoices.slice();

    private isDisabledByRobber = false;

    static shuffle() {
        Tile.localDiceValueChoices = shuffle(Tile.localDiceValueChoices);
        Tile.localBiomeDistributionArray = shuffle(Tile.localBiomeDistributionArray);
    }

    constructor(location: HexPoint, landType?: Biome, diceValue?: number) {
        if (diceValue) {
            assertInt(diceValue)
            this.diceValue = diceValue;
        } else {
            // diceValue should be 2 <= n <= 12 && n != 7
            // distribution:
            //      2 3 3 4 4 5 5 6 6 8 8  9  9  9  10 10 11 11 12
            //      | | | | | | | | | | |  |  |  |  |  |  |  |  |
            //      0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
            // out of 19

            if (Config.getN() == 3) {
                this.diceValue = <number>Tile.localDiceValueChoices.pop();
            }
            else {
                this.diceValue = Tile.diceValueChoices[randomInt(19)];
            }
            
        }

        if (landType) {
            this.landType = landType;
        } else {
            if (Config.getN() == 3) {
                this.landType = <Biome>Tile.localBiomeDistributionArray.pop();
            }
            else {
                this.landType = biomeDistributionArray[randomInt(19)];
            }
        }

        if (this.landType == Desert) {
            this.diceValue = 0;
        }

        this.p = location;
        this.center = Hex.getCenterOfHex(location.y, location.x); // flip on purpose

        defined(this.diceValue);
        defined(this.landType);
        defined(this.p);
        defined(this.center);
    }

    getDiceValue() {
        return this.diceValue;
    }

    getLandType() {
        return this.landType;
    }

    getPos() {
        return this.p;
    }

    // activate if die matches this tile. Also does production
    activateIfDiceValueMatches(value: number, settlements: Array<Settlement>) {
        assertInt(value);
        if (value == this.diceValue && !this.isDisabledByRobber) { // no profits if the robber is around
            this.active = true;
            
            // find neighboring settlements and award resource
            Hex.getHexCorners(this.p.y, this.p.x).forEach(c => {
                settlements.forEach(s => {
                    if (s.isHere(c)) {
                        s.production(this.landType.getResourceType());
                    }
                })
            })
            
        }
    }

    deactivate() {
        this.active = false;
    }

    highlightIfActive(ctx: CanvasRenderingContext2D) {
        if (this.active && !this.isDisabledByRobber) {
            ctx.strokeStyle = "white";
            ctx.lineWidth = 4;
            Hex.strokeHex(this.p.y, this.p.x, ctx);
        }
    }

    arriveRobber() {
        this.isDisabledByRobber = true;
    }

    departRobber() {
        this.isDisabledByRobber = false;
    }

    draw(ctx: CanvasRenderingContext2D) {
        ctx.fillStyle = this.landType.getColor();

        Hex.fillHex(this.p.y, this.p.x, ctx);

        const relCenter = this.center.toRelPoint();

        if (this.landType != Desert) {
            ctx.font = "20px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillStyle = "black";
            ctx.fillText(this.diceValue.toString(), relCenter.x, relCenter.y);
        }
        
        ctx.strokeStyle = "black";
        ctx.lineWidth = 1;

        Hex.strokeHex(this.p.y, this.p.x, ctx);

        if (this.isDisabledByRobber) {
            this.strokeRobber(ctx);
        }
    }

    strokeRobber(ctx: CanvasRenderingContext2D) {
        const relCenter = this.center.toRelPoint();

        const apo = Hex.getSideLength() / 3.5 + 2;
        const xStep = 0.5773502691896257 * apo; // Math.tan(Math.PI / 6) * apo;

        ctx.strokeStyle = "red";
        ctx.lineWidth = 5;

        ctx.beginPath();
        ctx.moveTo(relCenter.x + xStep, relCenter.y - apo);
        ctx.lineTo(relCenter.x + 2 * xStep, relCenter.y);
        ctx.lineTo(relCenter.x + xStep, relCenter.y + apo);
        ctx.lineTo(relCenter.x - xStep, relCenter.y + apo);
        ctx.lineTo(relCenter.x - 2 * xStep, relCenter.y);
        ctx.lineTo(relCenter.x - xStep, relCenter.y - apo);
        ctx.closePath();

        ctx.stroke();
    }

    // this method is from http://www.playchilla.com/how-to-check-if-a-point-is-inside-a-hexagon
    isInside(pos: AbsPoint): boolean
    {
        // vertical = apothem
        const q2x: number = Math.abs(pos.x - this.center.x);
        const q2y: number = Math.abs(pos.y - this.center.y);

        const vert = Hex.getApothem();
        const hori = Hex.getSideLength() / 2;

        if (q2x > hori*2 || q2y > vert) return false;
        return vert * 2 * hori - vert * q2x - 2* hori * q2y >= 0;
    }
}
