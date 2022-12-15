function phac_aspc_autocomplete_blur_handler(event, name, sync=false, item=false) {
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
            // Reset focus back to textbox if a search result item triggered the blur
            if (item) el.focus();
            document.getElementById(name + '__items').classList.remove('show');
        }
    });
}

const phac_aspc_autocomplete_keydown_debounce = {};
function phac_aspc_autocomplete_keydown_handler(event) {
    // Handler responsible for keyboard navigation (up, down, esc and backspace)
    const debounce = phac_aspc_autocomplete_keydown_debounce;
    const whereTo = (element, down=true, skip_element=true) => {
        // This function determines which element should receive focus
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
    const focusWhenResultsShown = (container, timeout) => {
        // This function uses polling to wait for the results to be shown before
        // moving focus.
        const results = container.querySelector('.results');
        if (!results || !results.classList.contains('show')) {
            if (timeout > 0) {
                if (debounce[container.getAttribute('id')])
                    clearTimeout(debounce[container.getAttribute('id')]);
                debounce[container.getAttribute('id')] =
                    setTimeout(
                        () => focusWhenResultsShown(container, timeout - 100),
                        100
                    );
            }
            return false;
        }
        debounce[container.getAttribute('id')] = undefined;
        const first = results.querySelector('a:first-child');
        const next = whereTo(first, true, false);
        if (next) next.focus();
    }

    if (event.keyCode === 27) {
        // Escape key
        event.target.blur();
    } else if (
        event.target.tagName.toUpperCase() === 'INPUT' &&
        event.keyCode === 8 &&
        event.target.value.length === 0
    ) {
        // Backspace key on text input
        const container = event.target.closest('.phac_aspc_form_autocomplete');
        const chip = container.querySelectorAll('.chip a');
        if (chip.length > 0) chip[chip.length - 1].dispatchEvent(new Event('click'));
    } else if (event.keyCode === 40 && event.target.tagName.toUpperCase() === 'INPUT') {
        // down arrow on text element
        const container = event.target.closest('.phac_aspc_form_autocomplete');
        const results = container.querySelector('.results');
        // Open the results if they are not shown
        if (!results || !results.classList.contains('show'))
            event.target.dispatchEvent(new Event('input'));
        focusWhenResultsShown(container, 3000);
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