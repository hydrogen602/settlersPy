import { EventManager } from "../mechanics/EventManager";

// https://stackoverflow.com/questions/15661339/how-do-i-fix-blurry-text-in-my-html5-canvas

const PIXEL_RATIO = (function () {
    const ctx: any = document.createElement("canvas").getContext("2d"),
        dpr = window.devicePixelRatio || 1,
        bsr: any = ctx["webkitBackingStorePixelRatio"] ||
              ctx["mozBackingStorePixelRatio"] ||
              ctx["msBackingStorePixelRatio"] ||
              ctx["oBackingStorePixelRatio"] ||
              ctx["backingStorePixelRatio"] || 1;

    return dpr / bsr;
})();


function createHiDPICanvas(w: number, h: number, ratio: number) {
    if (!ratio) { ratio = PIXEL_RATIO; }
    const can = document.createElement("canvas");
    can.width = w * ratio;
    can.height = h * ratio;
    can.style.width = w + "px";
    can.style.height = h + "px";

    let context = function() {
        const tmp = can.getContext("2d");
        if (tmp == null) {
            throw "CanvasRenderingContext2D is null";
        }
        return tmp;
    }();
    
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    can.id = "main";
    return can;
}

const windowWidth = window.innerWidth //-18-25
const windowHeight = window.innerHeight // -6 //-18-10

//Create canvas with the device resolution.
const myCanvas = createHiDPICanvas(windowWidth, windowHeight, 0);

const box = function() {
    const tmp = document.getElementById("box");
    if (tmp == null) {
        throw "Could not find element with id box";
    }
    return tmp;
}();

box.appendChild(myCanvas);

export const canvas = myCanvas;

export const ctx = function() {
    const tmp = myCanvas.getContext("2d");
    if (tmp == null) {
        throw "CanvasRenderingContext2D is null";
    }
    return tmp;
}();

// end of stackoverflow code

// my html interaction code

const controlBox = function() {
    const tmp = document.getElementById("control");
    if (tmp == null) {
        throw "Could not find element with id control";
    }
    return tmp;
}();

function newButton(name: string) {
    const x = document.createElement('button')
    x.id = name.replace(' ', '-');
    x.innerText = name;
    x.classList.add("purchase");

    controlBox.appendChild(x);

    return x;
}

const newRd = newButton("Purchase New Road");
newRd.onclick = EventManager.purchaseRoad;

const newSet = newButton("Purchase New Settlement");
newSet.onclick = EventManager.purchaseSettlement;

const newCity = newButton("Purchase New City");
newCity.onclick = EventManager.purchaseCity;
