import { Inventory } from "./mechanics/Inventory";
import { defined, assert } from "./util";
import { ResourceType } from "./dataTypes";

console.log("test start");

function inventoryTest() {
    let inv = new Inventory();
    defined(inv);
    assert(Boolean(inv));

    assert(inv.get(ResourceType.Brick) == 0);
    assert(inv.get(ResourceType.Lumber) == 0);
    assert(inv.get(ResourceType.Ore) == 0);
    assert(inv.get(ResourceType.Sheep) == 0);
    assert(inv.get(ResourceType.Wheat) == 0);

    inv.set(ResourceType.Brick, 5);
    for (let index = 0; index <= 5; index++) {
        assert(inv.hasEnough(ResourceType.Brick, index));
    }

    assert(!inv.purchase([ResourceType.Lumber], [1]));
    assert(!inv.purchase([ResourceType.Brick, ResourceType.Lumber], [3, 1]));
    

    inv.update(ResourceType.Lumber, 1);

    assert(inv.get(ResourceType.Brick) == 5);
    assert(inv.get(ResourceType.Lumber) == 1);

    assert(inv.purchase([ResourceType.Brick, ResourceType.Lumber], [3, 1]));

    assert(inv.get(ResourceType.Brick) == 2);
    assert(inv.get(ResourceType.Lumber) == 0);
    


    console.log("done with tests")
}

inventoryTest();