import { ResourceType } from "../dataTypes";
import { defined } from "../util";

export class Biome {

    private abundance: number; // out of 19
    private resource: ResourceType;
    private color: string;

    protected constructor(abundance: number, resource: ResourceType, color: string) {
        this.abundance = abundance;
        this.resource = resource;
        this.color = color;
    }

    public getAbundance() {
        defined(this.abundance);
        return this.abundance;
    }

    public getResourceType() {
        defined(this.resource);
        return this.resource;
    }

    public getColor() {
        defined(this.color);
        return this.color;
    }
}

export const Desert = new (class Desert extends Biome {
    constructor() {
        super(1, ResourceType.NoResource, 'yellow');
    }
})();

export const Grassland = new (class Grassland extends Biome {
    constructor() {
        super(4, ResourceType.Sheep, 'limegreen');
    }
})();

export const Forest = new (class Forest extends Biome {
    constructor() {
        super(4, ResourceType.Lumber, 'forestgreen');
    }
})();

export const Mountain = new (class Mountain extends Biome {
    constructor() {
        super(3, ResourceType.Ore, 'dimgray');
    }
})();

export const Farmland = new (class Farmland extends Biome {
    constructor() {
        super(4, ResourceType.Wheat, 'goldenrod');
    }
})();

export const Quarry = new (class Quarry extends Biome {
    constructor() {
        super(3, ResourceType.Brick, 'firebrick');
    }
})();

export const biomes: Array<Biome> = [Desert, Grassland, Forest, Mountain, Farmland, Quarry];

export const biomeDistributionArray = function() {
    let tmp_biomeDistributionArray: Array<Biome> = [];
    biomes.forEach((e: Biome) => {
        for (let i = 0; i < e.getAbundance(); i++) {
            tmp_biomeDistributionArray.push(e);
        }
    });
    return tmp_biomeDistributionArray;
}();
