import { ResourceType } from "../dataTypes";
import { defined, assertInt, assert } from "../util";

// my own inventory system cause map is limited

// requirements - map based/ like
// get - set - update
// verify enough resources

export class Inventory {
    
    private content: Map<ResourceType, number>;

    constructor() {
        this.content = new Map()
        for (let i in ResourceType) {
        
            if (Number(i).toString() != "NaN" && i != '0') { // '0' is Desert -> NoResource
                // js is retarded    /\
                // for thinking that ||
                // NaN == NaN is false
                //
                this.content.set(Number(i), 0);
            }
        }
    }

    keys() {
        return this.content.keys();
    }

    get(k: ResourceType): number {
        const tmp = this.content.get(k);
        defined(tmp);
        return <number>tmp;
    }

    set(k: ResourceType, n: number) {
        assertInt(n);
        this.content.set(k, n);
    }

    update(k: ResourceType, n: number) {
        // adds n
        assertInt(n);
        const currValue = this.get(k);
        this.set(k, n + currValue);
    }

    hasEnough(k: ResourceType, min: number): boolean {
        assertInt(min);
        const currValue = this.get(k);
        return currValue >= min;
    }

    // attempts to purchase some good
    // returns true on success and false on failure
    //
    // given a list of resources and how many of each are required,
    // it checks if there are enough resources
    // if there are not enough resources, it returns false
    // if there are enough, it removes from the inventory and returns true
    purchase(kArr: Array<ResourceType>, costArr: Array<number>): boolean {
        assert(kArr.length == costArr.length);
        costArr.forEach(c => assertInt(c));

        // check if enough resources
        for (let i = 0; i < kArr.length; i++) {
            // console.log(kArr[i], costArr[i]);
            if (!this.hasEnough(kArr[i], costArr[i])) {
                return false;
            }
        }

        // remove stuff
        for (let i = 0; i < kArr.length; i++) {
            this.update(kArr[i], -costArr[i]);
        }
        return true;
    }
}
