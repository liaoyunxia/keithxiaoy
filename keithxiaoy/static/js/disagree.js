(function() {
    var button = document.getElementById('disagree');
    var dialog = document.getElementById('dialog');
    /** // polyfill **/
    if (! dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    /** // polyfill End **/
    button.addEventListener('click', function() {
        dialog.showModal();
    });
    dialog.querySelector('#close').addEventListener('click', function() {
        dialog.close();
    });
})();
