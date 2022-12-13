function phac_aspc_autocomplete_blur_handler(event, name, sync=false) {
    // Handler responsible for blur events
    // Will remove the results when focus is not longer on the component, and update
    // the textbox value when multiselect is false
    requestAnimationFrame(function () {
        const parent = document.getElementById(`${name}__container`);
        if (!parent.contains(document.activeElement)) {
            const el = document.getElementById(name + '__textinput');
            const data_el = document.getElementById(name + '__data');
            if (!sync)  {
                el.value = '';
            } else {
                el.value = data_el.getAttribute('data-phac-aspc-autocomplete');
            }
            document.getElementById(name + '__items').classList.remove('show');
        }
    });
}

function phac_aspc_autocomplete_keydown_handler(event) {
    // Handler responsible for keyboard navigation (up and down arrows, esc key)
    const whereTo = (element, down=true, skip_element=true) => {
        if (!element) return null;
        const dir = down ?
            elem => elem.nextElementSibling : elem => elem.previousElementSibling;

        let el = skip_element ? dir(element) : element;
        while (el) {
            if (el.getAttribute('href')) return el;
            el = dir(el);
        }
        return null;
    }

    if (event.keyCode === 27) {
        event.target.blur();
    } else if (event.keyCode === 40 && event.target.tagName.toUpperCase() === 'INPUT') {
        // down arrow on text element
        const container = event.target.closest('.phac_aspc_form_autocomplete');
        const first = container.querySelector('.results a:first-child');
        const next = whereTo(first, true, false);
        if (next) next.focus();
        return false;
    } else if (event.keyCode === 40) {
        // down arrow on item
        const next = whereTo(event.target);
        if (next) next.focus();
        return false;
    } else if (
        event.keyCode === 38 &&
        event.target.tagName.toUpperCase() !== 'INPUT'
    ) {
        // up arrow on item
        const prev = whereTo(event.target, false);
        if (prev) prev.focus();
        return false;
    }
    return true;
}