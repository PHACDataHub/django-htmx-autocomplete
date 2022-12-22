function phac_aspc_autocomplete_blur_handler(event, name, sync=false, item=false) {
    // Handler responsible for blur events
    // Will remove the results when focus is not longer on the component, and update
    // the <input> box value when multiselect is false
    requestAnimationFrame(function () {
        const parent = document.getElementById(`${name}__container`);
        if (!parent.contains(document.activeElement)) {
            // Focus has left the component

            // Get reference to <input> box
            const el = document.getElementById(name + '__textinput');

            // Abort active HTMX operations on the input box to avoid race conditions
            htmx.trigger(el, 'htmx:abort');

            // Set the text input value
            const data_el = document.getElementById(name + '__data');
            if (!sync)  {
                el.value = '';
            } else {
                el.value = data_el.getAttribute('data-phac-aspc-autocomplete');
            }

            // Reset focus back to <input> box if a menu item triggered the blur
            if (item) el.focus();

            // Get reference to list of results
            const results = document.getElementById(name + '__items');

            // Test if HTMX is currently in the process of swapping
            if (results.classList.contains('htmx-swapping')) {
                // To ensure the results are hidden, wait for HTMX to finish, then hide.
                results.addEventListener(
                    'htmx:afterSettle', () => results.classList.remove('show')
                );
            }
            // Hide the results
            results.classList.remove('show');

            // Change the min-width of the text input back to the (small) default
            parent.querySelector('.textinput')
                .parentElement.classList.remove('ac-active');
        }
    });
}

const phac_aspc_autocomplete_keydown_debounce = {};
function phac_aspc_autocomplete_keydown_handler(event) {
    if (event.target.classList.contains('textinput') && event.keyCode > 47) {
        // Expands the min-width of text input to a reasonable size when typing
        event.target.parentElement.classList.add('ac-active');
    } else if (event.target.classList.contains('textinput') && event.keyCode === 8
                && event.target.value.length === 1) {
        // Shrinks the min-width of text input back to the (small) default if
        // the text input is empty due to backspacing
        event.target.parentElement.classList.remove('ac-active');
    }
    // Handler responsible for keyboard navigation (up, down, esc and backspace)
    const debounce = phac_aspc_autocomplete_keydown_debounce;
    const whereTo = (element, down=true, skip_element=true, count=1) => {
        // This function determines which element should receive focus
        if (!element) return null;
        const dir = down ?
            elem => elem.nextElementSibling : elem => elem.previousElementSibling;

        let el = skip_element ? dir(element) : element;
        let last_el = el;
        let counter = count;
        while (el && counter > 0) {
            if (el.getAttribute('href')) {
                if (counter === 1) return el;
                last_el = el;
            }
            if (counter !== 1) counter -= 1;
            el = dir(el);
        }
        if (last_el && counter > 0) return last_el;
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

    const getPageSize = (container, element) => {
        const r1 = container.getBoundingClientRect();
        const r2 = element.getBoundingClientRect();
        return Math.floor((r1.bottom - r1.top) / (r2.bottom - r2.top));
    }

    const container = event.target.closest('.phac_aspc_form_autocomplete');
    const results = container.querySelector('.results');
    if (event.keyCode === 27) {
        // Escape key on text input or item
        if (results && results.classList.contains('show')) {
            results.classList.remove('show');
        } else if (event.target.tagName.toUpperCase() === 'INPUT') {
            event.target.value = '';
        }
        if (event.target.tagName.toUpperCase() !== 'INPUT') {
            container.querySelector('.textinput').focus();
        }
    } else if (
        event.target.tagName.toUpperCase() === 'INPUT' &&
        event.keyCode === 8 &&
        event.target.value.length === 0
    ) {
        // Backspace key on text input
        const chip = container.querySelectorAll('.chip a');
        if (chip.length > 0) chip[chip.length - 1].dispatchEvent(new Event('click'));
    } else if (event.target.tagName.toUpperCase() !== 'INPUT' && event.keyCode === 36) {
        // Home key
        if (results) {
            const top = whereTo(
                results.querySelector('a:first-child'),
                true,
                false
            );
            if (top) top.focus();
            return false;
        }
    } else if (event.target.tagName.toUpperCase() !== 'INPUT' && event.keyCode === 35) {
        // End key
        if (results) {
            const bottom = whereTo(
                results.querySelector('a:last-child'),
                false,
                false
            );
            if (bottom) bottom.focus();
            return false;
        }
    } else if (event.target.tagName.toUpperCase() !== 'INPUT' && event.keyCode === 33) {
        // Page up key
        if (results) {
            const prev = whereTo(
                event.target,
                false,
                true,
                getPageSize(results, event.target)
            );
            if (prev) prev.focus();
            return false;
        }
    } else if (event.target.tagName.toUpperCase() !== 'INPUT' && event.keyCode === 34) {
        // Page down key
        if (results) {
            const next = whereTo(
                event.target,
                true,
                true,
                getPageSize(results, event.target)
            );
            if (next) next.focus();
            return false;
        }
    } else if (event.keyCode === 40 && event.target.tagName.toUpperCase() === 'INPUT') {
        // down arrow on text element
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
