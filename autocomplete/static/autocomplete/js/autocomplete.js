function phac_aspc_autocomplete_trigger_change(container_id) {
    setTimeout(() => {
        const container = document.getElementById(container_id);
        const el = container.querySelector('.textinput');
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }, 0)
}

function phac_aspc_autocomplete_clear_focus(container, activate_ring) {
    const hasFocus = container.querySelectorAll('.hasFocus'); 
    for (const el of hasFocus) {
        el.classList.remove('hasFocus');
    }

    const el = container.querySelector('.textinput');
    el.removeAttribute('aria-activedescendant');

    if (activate_ring) {
        container.closest('.phac_aspc_form_autocomplete_focus_ring')
            .classList.add('active');
        container.querySelector('.textinput').focus();
    } else {
        container.closest('.phac_aspc_form_autocomplete_focus_ring')
            .classList.remove('active');
    }
}

function phac_aspc_autocomplete_hide_results(container) {
    const results = container.querySelector('.results');
    const el = container.querySelector('.textinput');
    el.setAttribute('aria-expanded', false);
    results.classList.remove('show');
}

phac_aspc_autocomplete_blur_skip = {}
function phac_aspc_autocomplete_blur_handler(event, name, sync = false, item = false) {
    // Handler responsible for blur events
    // Will remove the results when focus is no longer on the component, and update
    // the <input> box value when multiselect is false
    requestAnimationFrame(function () {
        const parent = document.getElementById(`${name}__container`);
        const id = parent.getAttribute('id');
        if (phac_aspc_autocomplete_blur_skip[id]) return false;
        if (!parent.contains(document.activeElement)) {
            // Focus has left the component

            // Reset the component's state
            phac_aspc_autocomplete_closed[id] = false;
            if (phac_aspc_autocomplete_keyup_debounce[id]) {
                clearTimeout(phac_aspc_autocomplete_keyup_debounce[id])
                phac_aspc_autocomplete_keyup_debounce[id] = false;
            }

            // Get reference to <input> box
            const el = document.getElementById(name + '__textinput');

            // Abort active HTMX operations on the input box to avoid race conditions
            htmx.trigger(el, 'htmx:abort');

            // Set the text input value
            const data_el = document.getElementById(name + '__data');
            if (!sync) {
                el.value = '';
            } else {
                el.value = data_el.getAttribute('data-phac-aspc-autocomplete');
            }
            phac_aspc_autocomplete_set_initial_value(parent, true);

            // Get reference to list of results
            const results = document.getElementById(name + '__items');

            // Get reference to aria live area
            const live = document.getElementById(name + '__info');

            // Test if HTMX is currently in the process of swapping
            if (results.classList.contains('htmx-swapping')) {
                // To ensure the results are hidden, wait for HTMX to finish, then hide.
                results.addEventListener(
                    'htmx:afterSettle', () => {
                        phac_aspc_autocomplete_hide_results(parent);
                    }
                );
            }
            // Hide the results
            phac_aspc_autocomplete_hide_results(parent);

            // Clear the live info
            live.innerHTML = '';

            // Change the min-width of the text input back to the (small) default
            parent.querySelector('.textinput')
                .parentElement.classList.remove('ac-active');

            // Ensure no elements remain 'focused', and set focus to input
            phac_aspc_autocomplete_clear_focus(parent, item);
        }
    });
}

function phac_aspc_autocomplete_item_click_handler(event) {
    const container = event.target.closest('.phac_aspc_form_autocomplete');
    const results = container.querySelector('.results');
    const open = results && results.classList.contains('show');
    if (open) {
        phac_aspc_autocomplete_clear_focus(container, true);
        phac_aspc_autocomplete_hide_results(container);
    }
    return true;
}

function phac_aspc_autocomplete_focus_handler(event) {
    const container = event.target.closest('.phac_aspc_form_autocomplete');
    phac_aspc_autocomplete_clear_focus(container, true);
    phac_aspc_autocomplete_set_initial_value(container);
    setTimeout(() => {
        // Announce selected items to screen readers.  (if any)
        const info = container.querySelector('.live_info');
        info.innerHTML += '&nbsp;';    
    }, 100);
}

const phac_aspc_autocomplete_initial_value = {};
function phac_aspc_autocomplete_set_initial_value(container, reset = false) {
    const id = container.getAttribute('id');
    const el = container.querySelector('.textinput');
    if (reset) {
        phac_aspc_autocomplete_initial_value[id] = undefined;
        return;
    }
    if (phac_aspc_autocomplete_initial_value[id] === undefined) {
        phac_aspc_autocomplete_initial_value[id] = el.value;
    }
}

phac_aspc_autocomplete_closed = {};
function phac_aspc_autocomplete_click_handler(event) {
    if (event.target.classList.contains('item')) return true;
    const container = event.target.closest('.phac_aspc_form_autocomplete');
    const id = container.getAttribute('id');
    const results = container.querySelector('.results');
    const open = results && results.classList.contains('show');
    const text_box = container.querySelector('.textinput');

    phac_aspc_autocomplete_set_initial_value(container);
    phac_aspc_autocomplete_clear_focus(container, true);

    phac_aspc_autocomplete_closed[id] = open;
    if (open) {
        phac_aspc_autocomplete_hide_results(container);
    } else {
        text_box.dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
    }
    return false;
}

const phac_aspc_autocomplete_keyup_debounce = {};
function phac_aspc_autocomplete_keyup_handler(event) {
    if (event.keyCode === 13) return false;
    const debounce = phac_aspc_autocomplete_keyup_debounce;
    const value = phac_aspc_autocomplete_initial_value;
    const elem = event.target;

    const container = elem.closest('.phac_aspc_form_autocomplete');
    const id = container.getAttribute('id');

    phac_aspc_autocomplete_set_initial_value(container);

    if (debounce[id]) {
        clearTimeout(debounce[id]);
        debounce[id] = false;
    }

    const v = elem.value;

    debounce[id] = setTimeout(() => {
        if (!phac_aspc_autocomplete_closed[id] && v != value[id]) {
            elem.dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
        } else if (
            phac_aspc_autocomplete_closed[id] &&
            v != value[id] &&
            v == ''
        ) {
            phac_aspc_autocomplete_closed[id] = false;
        }
        value[id] = v;
    }, 250);
    return true;
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
    const whereTo = (container, down = true, skip_element = true, count = 1) => {
        // This function determines which element should receive focus
        // TODO: bug with down
        if (!container) return null;
        const results = container.querySelector('.results');
        let element = container.querySelector('.hasFocus');
        const must_skip = Boolean(element);
        const fallback = down ? results.querySelector('a:first-child')
            : results.querySelector('a:last-child');
        if (!element) element = fallback;
        if (!element) return null;
        const dir = down ?
            elem => elem.nextElementSibling : elem => elem.previousElementSibling;

        let el = skip_element && must_skip ? dir(element) : element;
        let counter = count;
        while (el && counter > 0) {
            if (el.getAttribute('href')) {
                if (counter === 1) return el;
            }
            if (counter !== 1) counter -= 1;
            el = dir(el);
        }
        if (counter > 0) return fallback;
        return null;
    }
    const switchFocus = (element, container) => {
        phac_aspc_autocomplete_clear_focus(container);
        const el = container.querySelector('.textinput');
        el.setAttribute('aria-activedescendant', element.getAttribute('id'));
        element.classList.add('hasFocus');
        element.scrollIntoView({ block: 'nearest' })
    }
    const selectFocusedItem = (container) => {
        const item = container.querySelector('.hasFocus');
        if (item) {
            item.dispatchEvent(new Event('click'));
        }
        return item;
    }
    const focusWhenResultsShown = (container, timeout, up) => {
        // This function uses polling to wait for the results to be shown before
        // moving focus.
        const id = container.getAttribute('id');
        const results = container.querySelector('.results');
        if (!results || !results.classList.contains('show')) {
            if (timeout > 0) {
                if (debounce[id])
                    clearTimeout(debounce[id]);
                debounce[id] =
                    setTimeout(
                        () => focusWhenResultsShown(container, timeout - 100, up),
                        100
                    );
            }
            return false;
        }
        debounce[id] = undefined;
        phac_aspc_autocomplete_closed[id] = false;
        if (up) {
            const prev = whereTo(container, false);
            if (prev) switchFocus(prev, container);
        } else {
            const next = whereTo(container, true, false);
            if (next) switchFocus(next, container);
        }
    }

    const getPageSize = (container) => {
        const r1 = container.getBoundingClientRect();
        const r2 = container.querySelector('.item').getBoundingClientRect();
        return Math.floor((r1.bottom - r1.top) / (r2.bottom - r2.top));
    }

    const container = event.target.closest('.phac_aspc_form_autocomplete');
    const results = container.querySelector('.results');
    const id = container.getAttribute('id');

    phac_aspc_autocomplete_set_initial_value(container);

    if (event.keyCode === 27) {
        // Escape key
        if (results && results.classList.contains('show')) {
            phac_aspc_autocomplete_clear_focus(container, true);
            phac_aspc_autocomplete_hide_results(container);
            phac_aspc_autocomplete_closed[id] = true;
        } else {
            event.target.value = '';
        }
    } else if (event.keyCode === 13) {
        // Enter key
        if (results && results.classList.contains('show')) {
            selectFocusedItem(container);
            phac_aspc_autocomplete_clear_focus(container, true);
            phac_aspc_autocomplete_hide_results(container);
        }
        return false;
    } else if (
        event.keyCode === 8 &&
        event.target.value.length === 0
    ) {
        // Backspace key on text input
        const chip = container.querySelectorAll('.chip a');
        if (chip.length > 0) chip[chip.length - 1].dispatchEvent(new Event('click'));
    } else if (event.keyCode === 33) {
        // Page up key
        if (results) {
            const prev = whereTo(
                container,
                false,
                true,
                getPageSize(results)
            );
            if (prev) switchFocus(prev, container);
            return false;
        }
    } else if (event.keyCode === 34) {
        // Page down key
        if (results) {
            const next = whereTo(
                container,
                true,
                true,
                getPageSize(results)
            );
            if (next) switchFocus(next, container);
            return false;
        }
    } else if (event.keyCode === 40) {
        // down arrow
        // Open the results if they are not shown
        if (!results || !results.classList.contains('show')) {
            event.target.dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
            if (event.altKey) {
                phac_aspc_autocomplete_closed[id] = false;
            } else {
                focusWhenResultsShown(container, 3000);
            }
        } else {
            const next = whereTo(container);
            if (next) switchFocus(next, container);
        }
        return false;
    } else if (event.keyCode === 38) {
        // up arrow on item
        // Open the results if they are not shown
        if (!results || !results.classList.contains('show')) {
            event.target.dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
            if (event.altKey) {
                phac_aspc_autocomplete_closed[id] = false;
            } else {
                focusWhenResultsShown(container, 3000, true);
            }
        } else {
            const prev = whereTo(container, false);
            if (prev) switchFocus(prev, container);
        }
        return false;
    } else {
        phac_aspc_autocomplete_closed[id] = false;
    }
    phac_aspc_autocomplete_clear_focus(container, true);
    return true;
}
