

const box = document.getElementById('notificationBannerBox');
if (box == null) {
    throw Error("Could not find div of id 'notificationBannerBox'");
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