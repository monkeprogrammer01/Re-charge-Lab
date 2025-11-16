function addWater() {
    fetch('/tracker/update-water/', {
        method: 'POST',
        body: JSON.stringify({glasses: 1})
    }).then(() => {
        updateProgressBars();
    });
}