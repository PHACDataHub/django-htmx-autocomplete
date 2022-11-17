function phac_aspc_autocomplete_blur_handler(name, sync=false) {
    requestAnimationFrame(function () {
        const parent = document.getElementById(`${name}__container`);
        if (!parent.contains(document.activeElement)) {
            var el = document.getElementById(name + '__textinput');
            var data_el = document.getElementById(name + '__data');
            if (!sync)  {
                el.value = '';
            } else {
                console.log('setting value!');
                el.value = data_el.getAttribute('data-phac-aspc-autocomplete');
                console.log(el.value);
            }
            document.getElementById(name + '__items').classList.remove('show');
        }
    });
}
