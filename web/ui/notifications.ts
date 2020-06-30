import { assert } from "../util";


const box = document.getElementById('notificationBannerBox');
if (box == null) {
    throw Error("Could not find div of id 'notificationBannerBox'");
}

const playerLobbyBox = document.getElementById('pregameLobbyBox');
if (playerLobbyBox == null) {
    throw Error("Could not find div of id 'pregameLobbyBox'");
}

export function makePlayerList(playerNames: Array<string>, readyPlayers: Array<string>) {
    // playerNames is all players
    assert(playerNames.length >= readyPlayers.length, "what???");

    if (playerLobbyBox != null) {
        for (const node of playerLobbyBox.children) {
            if (node.tagName == 'p') {
                node.remove();
            }
        }
        

        for (const name of playerNames) {
            const pTag = document.createElement('p');
            pTag.innerText = name;
            if (name in readyPlayers) {
                pTag.setAttribute('ready','')
            }
            playerLobbyBox.appendChild(pTag);
        }
    }
    
}

export function newNotification(msg: string, error?: boolean) {
    let isError = false;
    if (error) {
        isError = true;
    }

    function deleteOldestNotification() {
        if (box != null && box.childElementCount > 0) {
            box.children[0].remove();
        }
    }

    const newDiv = document.createElement('div');
    newDiv.classList.add('notificationBanner');
    if (isError) {
        newDiv.classList.add('notificationBannerError');
    }
    newDiv.innerText = msg;
    newDiv.onclick = function () { newDiv.remove(); };

    box?.appendChild(newDiv);

    setTimeout(deleteOldestNotification, 10000);
}