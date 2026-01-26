//public DONE
function phac_aspc_autocomplete_trigger_change(container_id) {
    setTimeout(() => {
        const container = document.getElementById(container_id);
        const el = container.querySelector('.textinput');
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }, 0)
}
//private DONE
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
//private DONE
function phac_aspc_autocomplete_hide_results(container) {
    const results = container.querySelector('.results');
    const el = container.querySelector('.textinput');
    el.setAttribute('aria-expanded', false);
    results.classList.remove('show');
}

phac_aspc_autocomplete_blur_skip = {}
// public method DONE
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

//public DONE
function phac_aspc_autocomplete_item_click_handler(event) {
    // once an item is clicked, before HTMX swaps in new values
    // focus on the text input and hide the results
    const container = event.target.closest('.phac_aspc_form_autocomplete');
    const results = container.querySelector('.results');
    const open = results && results.classList.contains('show');
    if (open) {
        phac_aspc_autocomplete_clear_focus(container, true);
        phac_aspc_autocomplete_hide_results(container);
    }
    return true;
}
//public DONE
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
//private DONE
function phac_aspc_autocomplete_set_initial_value(container, reset = false) {
    // stores current value of text input in variable
    // to enable restoring this value if a new value is not selected
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
//public DONE
function phac_aspc_autocomplete_click_handler(event) {
    if (event.target.classList.contains('item')){
        // This never happens?
        return true;
    }
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
//public DONE
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
//public DONE
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


KEY_CODES = {
    ENTER: 13,
    ESCAPE: 27,
    UP_ARROW: 38,
    DOWN_ARROW: 40,
    BACKSPACE: 8,
    PAGE_UP: 33,
    PAGE_DOWN: 34,
    BEGINNING_OF_PRINTABLE_KEYS: 48,
}

class PhacAutocomplete {
    /*        
        Instances are stateless, creation has zero side-effects
        state is stored in static properties

        instances don't cache anything, they never go stale either

        A bit arbitrary what behavior goes in static vs instance methods
    */ 

    componentId //only instance variable

    static existingValuesById = {
        /* 
            Existing values are stored 
            to reset the input to its previous value
            if a new value is not selected
        */

    }
    static closedStateById = {
        /*  
            TODO: wtf is this
        */
    }

    static debouncedKeyUpTimeoutsById = {
        /*
        here we store timeout references for debounced keyup events
        we store them in case we need to clear them
        */
    }

    static debouncedKeyDownTimeoutsById = {
        /*
        here we store timeout references for debounced keydown events
        we store them in case we need to clear them
        */
    }

    static blurSkipsById = {
        // TODO idk what this does yet
    }

    constructor(componentId) {
        this.componentId = componentId;
    }

    static getClosestComponentId(element){
        const ac_root = element.closest('[data-autocomplete-root]');
        if(!ac_root){
            return null;
        }
        if(!isEnabledAcRoot(ac_root)){
            return null;
        }
        return ac_root.getAttribute('data-autocomplete-componentId');
    }

    static getInstanceForElement(element){
        const componentId = this.getClosestComponentId(element);
        if(!componentId){
            return null;
        }

        return new this(componentId);

    }


    static emitChangeEvent(containerId){
        // imperatively emit 'change' event, 
        // in case consumer code is listening
        setTimeout(() => {
            const container = document.getElementById(containerId);
            const el = container.querySelector('.textinput');
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }, 0)
    }

    static focusInputHandler(event){
        const instance = this.getInstanceForElement(event.target);

        instance.resetFocus(true);
        instance.storeExistingValue();
        setTimeout(() => {
            // Announce selected items to screen readers.  (if any)
            const info = instance.getInfo();
            info.innerHTML += '&nbsp;';    
        }, 100);

    }

    static inputClickHandler(event){
        const instance = this.getInstanceForElement(event.target);
        instance.storeExistingValue();
        instance.resetFocus(true);

        const isOpen = instance.getIsOpen();
        if (isOpen) {
            instance.hideResults();
        } else {
            instance.setIsClosed( false );
            instance.triggerNewSearch();
        }

        return false
    }

    static itemClickHandler(event){
        const instance = this.getInstanceForElement(event.target);
        if(instance.getIsOpen()){
            instance.resetFocus(true);
            instance.hideResults();
        }
        return true;
    }

    static inputFocusHandler(event){
        const instance = this.getInstanceForElement(event.target);
        instance.resetFocus(true);
        instance.storeExistingValue();
        setTimeout(() => {
            // Announce selected items to screen readers.  (if any)
            const info = instance.getInfo();
            info.innerHTML += '&nbsp;';    
        }, 100);
    }

    static keyUpHandler(event){
        if (event.keyCode === KEY_CODES.ENTER) {
            return false;
        }

        const instance = this.getInstanceForElement(event.target);
        const componentId = instance.getComponentId();

        const existingValue = instance.getExistingValue();
        instance.storeExistingValue();

        if( this.debouncedKeyUpTimeoutsById[componentId] ){
            clearTimeout( this.debouncedKeyUpTimeoutsById[componentId] );
            this.debouncedKeyUpTimeoutsById[componentId] = false;
        }
        
        const value = event.target.value;
        
        const timeOut = setTimeout( () => {
            const isClosedValue = instance.getIsClosedValue();
            
            // if value has changed and it's still open, trigger new search
            if( !isClosedValue && value != existingValue ){
                instance.triggerNewSearch();
            } else if (
                // this probably isn't common?
                // but if results are closed, and then user backspaces to empty
                // reopen the results
                isClosedValue &&
                value != existingValue &&
                value == ''
            ) {
                instance.setIsClosed( false );
            }

            instance.storeExistingValue(value);
        }, 250);

        this.debouncedKeyUpTimeoutsById[componentId] = timeOut;

        return true;

    }

    static keyDownHandler(event){
        // this is complex
        const keyCode = event.keyCode;
        const instance = this.getInstanceForElement(event.target);
        const componentId = instance.getComponentId();

        if(!event.target.classList.contains('textinput')){
            console.warn('keydown event on non textinput element in autocomplete component');
            return true;
        }

        if(keyCode >= KEY_CODES.BEGINNING_OF_PRINTABLE_KEYS){
            // Expands the min-width of text input to a reasonable size when typing
            instance.getInput().parentElement.classList.add('ac-active');
        } else if(keyCode === KEY_CODES.BACKSPACE && instance.getInput().value.length === 1){
            // Shrinks the min-width of text input back to the (small) default if
            // the text input is empty due to backspacing

            instance.getInput().parentElement.classList.remove('ac-active');
        }


        const getWhatToFocus = (instance, down = true, skip_element = true, count = 1) => {
            // this could be an instance method

            // determine which element should receive focus
            if(!instance){
                return null;
            }

            const results = instance.getResultItems();
            const currentlyFocused = instance.getContainer().querySelector('.hasFocus');
            const mustSkip = Boolean(currentlyFocused);
            const fallback = down ?
                results.querySelector('a:first-child')
                : results.querySelector('a:last-child');
            let element = currentlyFocused || fallback;
            if(!element){
                return null;
            }
            const dir = down ?
                elem => elem.nextElementSibling
                : elem => elem.previousElementSibling;

            let el = skip_element && mustSkip ? dir(element) : element;
            let counter = count;
            while(el && counter > 0){
                if(el.getAttribute('href')){
                    if(counter === 1){
                        return el;
                    }
                }
                if(counter !== 1){
                    counter -= 1;
                }
                el = dir(el);
            }
            if(counter > 0){
                return fallback;
            }
            return null;

        }

        const switchFocus = (element, instance) => {
            // this could be an instance method
            instance.resetFocus();
            const input = instance.getInput();
            input.setAttribute('aria-activedescendant', element.getAttribute('id'));
            element.classList.add('hasFocus');
            element.scrollIntoView({ block: 'nearest' })
        }

        const selectFocusedItem = (instance) => {
            // this could be an instance method
            const item = instance.getContainer().querySelector('.hasFocus');
            if(item){
                item.dispatchEvent(new Event('click'));
            }
            return item;
        }

        const focusWhenResultsShown = (instance, timeout, up) => {
            // this could be an instance method
            // uses polling to wait for the results to be shown before
            // moving focus.
            const componentId = instance.getComponentId();
            const results = instance.getResultItems();
            if(!results || !results.classList.contains('show')){
                if(timeout > 0){
                    if( this.debouncedKeyDownTimeoutsById[componentId] ){
                        clearTimeout( this.debouncedKeyDownTimeoutsById[componentId] );
                    }
                    this.debouncedKeyDownTimeoutsById[componentId] =
                        setTimeout(
                            () => focusWhenResultsShown(instance, timeout - 100, up),
                            100
                        );
                }
                return false;
            }
            // TODO: investigate if this is the bug?
            this.debouncedKeyDownTimeoutsById[componentId] = undefined;
            instance.setIsClosed( false );
            if(up){
                const prev = getWhatToFocus(instance, false);
                if(prev){
                    switchFocus(prev, instance);
                }
            } else {
                const next = getWhatToFocus(instance, true, false);
                if(next){
                    switchFocus(next, instance);
                }
            }

        }

        const getPageSize = (instance) => {
            const container = instance.getContainer();
            const exampleItem = container.querySelector('.item');
            const r1 = container.getBoundingClientRect();
            const r2 = exampleItem.getBoundingClientRect();
            return Math.floor((r1.bottom - r1.top) / (r2.bottom - r2.top));
        }


        instance.storeExistingValue();

        if(keyCode === KEY_CODES.ESCAPE){
            if(instance.getIsOpen()){
                instance.resetFocus(true);
                instance.hideResults();
                instance.setIsClosed( true );
            } else {
                event.target.value = '';
            }
        }

        else if(keyCode === KEY_CODES.ENTER){
            if(instance.getIsOpen()){
                selectFocusedItem(instance);
                instance.resetFocus(true);
                instance.hideResults();
            }
            return false;
        } else if (
            keyCode === KEY_CODES.BACKSPACE && instance.getInput().value.length === 0
        ) {
            const chips = instance.getChips();
            if(chips.length > 0){
                chips[chips.length - 1].querySelector('a').dispatchEvent(new Event('click'));
            }
        } else if(keyCode === KEY_CODES.PAGE_UP){
            if(instance.getIsOpen()){
                const prev = getWhatToFocus(
                    instance,
                    false,
                    true,
                    getPageSize(instance)
                );
                if(prev){
                    switchFocus(prev, instance);
                }
                return false;
            }
        } else if(keyCode === KEY_CODES.PAGE_DOWN){

            if(instance.getIsOpen()){
                const next = getWhatToFocus(
                    instance,
                    true,
                    true,
                    getPageSize(instance)
                );
                if(next){
                    switchFocus(next, instance);
                }
                return false;
            }
        } else if(keyCode === KEY_CODES.DOWN_ARROW){
            // down arrow
            // Open the results if they are not shown
            if(!instance.getIsOpen()){
                //event.target.dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
                instance.triggerNewSearch();
                if(event.altKey){

                    instance.setIsClosed( false );
                }
                else {
                    focusWhenResultsShown(instance, 3000);
                }
            } else {
                const next = getWhatToFocus(instance);
                if(next){
                    switchFocus(next, instance);
                }
            }
            return false;
        } else if(keyCode === KEY_CODES.UP_ARROW){
            // up arrow on item
            // Open the results if they are not shown
            if(!instance.getIsOpen()){
                instance.triggerNewSearch();
                if(event.altKey){
                    instance.setIsClosed( false );
                } else {
                    focusWhenResultsShown(instance, 3000, true);
                }
            } else {
                const prev = getWhatToFocus(instance, false);
                if(prev){
                    switchFocus(prev, instance);
                }
            }
            return false;
        } else {
            instance.setIsClosed( false );
        }
        instance.resetFocus(true);
        return true;
    }

    static blurHandler(event, name, sync=false, item=false){
        // Handler responsible for blur events
        // Will remove the results when focus is no longer on the component, and update
        // the <input> box value when multiselect is false
        const instance = this.getInstanceForElement(event.target);
        const componentId = instance.getComponentId();

        requestAnimationFrame( () => {
            const container = instance.getContainer();
            if(this.blurSkipsById[componentId]){
                return false;
            }
            if( !container.contains(document.activeElement) ){
                // Focus has left the component

                // Reset the component's state
                instance.setIsClosed( false );
                if( this.debouncedKeyUpTimeoutsById[componentId] ){
                    clearTimeout( this.debouncedKeyUpTimeoutsById[componentId] )
                    this.debouncedKeyUpTimeoutsById[componentId] = false;
                }

                //also abort any active htmx operations 
                const input = instance.getInput();
                htmx.trigger(input, 'htmx:abort');

                // Set the text input value, using the syncronized 'data' element 
                if(!sync){
                    input.value = '';
                } else {
                    const dataContainer = instance.getDataContainer();
                    input.value = dataContainer.getAttribute('data-phac-aspc-autocomplete');
                }
                instance.resetExistingValue();
                
                const results = instance.getResultItems();
                const live = instance.getInfo();

                // Test if HTMX is currently in the process of swapping
                if(results.classList.contains('htmx-swapping')){
                    // To ensure the results are hidden, wait for HTMX to finish, then hide.
                    results.addEventListener(
                        'htmx:afterSettle', () => {
                            instance.hideResults();
                        }
                    );
                }
                // Hide the results
                instance.hideResults();
                
                // Clear the live info
                live.innerHTML = '';

                // Change the min-width of the text input back to the (small) default
                instance.getInput().parentElement.classList.remove('ac-active');
                
                // Ensure no elements remain 'focused', and set focus to input
                instance.resetFocus(item);
            }
        });
    }

    //getters
    getComponentId(){
        return this.componentId;
    }
    getContainer(){
        return document.getElementById(`${this.getComponentId()}__container`);
    }
    getInput(){
        return this.getContainer().querySelector(`#${this.getComponentId()}__textinput`);
    }
    getInputWrapper(){
        return this.getContainer().querySelector(`#${this.getComponentId()}`);
    }
    getResultItems(){
        return this.getContainer().querySelector(`#${this.getComponentId()}__items`);
    }
    getInfo(){
        return this.getContainer().querySelector(`#${this.getComponentId()}__info`);
    }
    getDataContainer(){
        return this.getContainer().querySelector(`#${this.getComponentId()}__data`);
    }
    getFocusRing(){
        return this.getContainer().closest('.phac_aspc_form_autocomplete_focus_ring');
    }
    getIsOpen(){
        const results = this.getResultItems();
        return results && results.classList.contains('show');
    }
    getIsMulti(){
        return this.getContainer().hasAttribute('data-autocomplete-multiselect');
    }


    // behavioral methods

    storeExistingValue(value=null){

        if(value === null){
            value = this.getInput().value;
        }
        this.constructor.existingValuesById[this.getComponentId()] = value;
    }

    getExistingValue(){
        return this.constructor.existingValuesById[this.getComponentId()];
    }

    resetExistingValue(){
        this.constructor.existingValuesById[this.getComponentId()] = undefined;
    }

    resetFocus(shouldFocusRing){
        const hasFocus = this.getContainer().querySelectorAll('.hasFocus'); 
        for (const el of hasFocus) {
            el.classList.remove('hasFocus');
        }

        this.getInput().removeAttribute('aria-activedescendant');
        if (shouldFocusRing) {
            this.getFocusRing().classList.add('active');
            this.getInput().focus();
        } else {
            this.getFocusRing().classList.remove('active');
        }

    }

    getIsClosedValue(){
        // whether the stored value indicates the results are closed
        // Different than getIsOpen, which checks the live DOM state
        return this.constructor.closedStateById[this.getComponentId()] || false;
    }


    setIsClosed(isClosed){
        this.constructor.closedStateById[this.getComponentId()] = isClosed;
    }

    hideResults(){
        this.getInput().setAttribute('aria-expanded', false);
        this.getResultItems().classList.remove('show');
        this.setIsClosed( true );
    }

    triggerNewSearch(){
        this.getInput().dispatchEvent(new Event('phac_aspc_autocomplete_trigger'));
    }

    getSrDescription(){
        return this.getContainer().querySelector(`#${this.getComponentId()}__sr_description`);
    }

    getChips(){
        return this.getContainer().querySelectorAll(`#${this.getComponentId()}_ac_container li.chip`);
    }

    clear(){
        this.getInput().value = '';
        this.getInputWrapper().innerHTML = '';
        this.getResultItems().innerHTML = '';
        this.getInfo().innerHTML = '';
        this.getDataContainer().removeAttribute('data-phac-aspc-autocomplete');
        this.getChips().forEach(chip => chip.remove());
        
        const sr = this.getSrDescription()
        if (sr) {
            sr.innerHTML = '';
        }
    }


}


function isEnabledAcRoot(element){
    if(!element){
        return false;
    }
    if(!element.hasAttribute('data-autocomplete-root')){
        return false;
    }
    if(element.hasAttribute('data-autocomplete-disabled')){
        return false;
    }
    return true;
}

function initializeGlobalAutocompleteListeners(){

    const skipBlurOnEvents = ['mousedown', 'mouseup'];

    for(const eventName of skipBlurOnEvents){
        document.addEventListener(eventName, function(event){
            const ac_root = event.target.closest('[data-autocomplete-root]');
            if(!isEnabledAcRoot(ac_root)){
                return;
            }
            const componentId = ac_root.getAttribute('data-autocomplete-componentId');
            phac_aspc_autocomplete_blur_skip[componentId] = true;
        });
    }
   

    document.addEventListener('click', function(event){
        const target = event.target;
        const ac_root = target.closest('[data-autocomplete-root]');
        if(!isEnabledAcRoot(ac_root)){
            return;
        }
        if (
            target === ac_root ||
            target.classList.contains('ac_container') ||
            target.classList.contains('textinput')
        ){
            return PhacAutocomplete.inputClickHandler(event);
        }
    });


    document.body.addEventListener(
        'htmx:afterSettle', (event) => {
            const ac_root = event.detail.elt.closest('[data-autocomplete-root]');
            if(!isEnabledAcRoot(ac_root)){
                return;
            }
            const componentId = ac_root.getAttribute('data-autocomplete-componentId');
            const toggleurl = ac_root.getAttribute('data-autocomplete-toggleurl');

            if (event.detail.elt.getAttribute('id') === `${componentId}__items`) {
                const shown = event.detail.elt.classList.contains('show');
                const el = document.querySelector(`#${componentId}__textinput`);
                el.setAttribute('aria-expanded', shown);	
            } else if (
                event.detail.elt.getAttribute('id') === componentId &&
                event.detail.pathInfo.requestPath === toggleurl
            ) {
                PhacAutocomplete.emitChangeEvent(`${componentId}__container`);
            }
        }
    );
    document.body.addEventListener(
        'htmx:oobAfterSwap', (event) => {

            const instance = PhacAutocomplete.getInstanceForElement(event.detail.elt);
            if(!instance){
                return;
            }

            if (event.detail.elt.getAttribute('id') === instance.getInput().getAttribute('id')) {
                setTimeout(() => {
                    if(instance){
                        // instance.storeExistingValue();
                        instance.resetExistingValue();
                    }
                    //phac_aspc_autocomplete_set_initial_value(document.querySelector(`#${componentId}__container`), true);
                    const input = instance.getInput()
                    input.selectionStart = input.selectionEnd = input.value.length;
                }, 0)
            }
        }
    );
    document.body.addEventListener('htmx:configRequest', function(event) {
        const ac_root = event.detail.elt.closest('[data-autocomplete-root]');
        if(!ac_root){
            return;
        }
        if (
            ac_root.contains(event.detail.elt) &&
            event.detail.path.endsWith('/toggle')
        ) {
            // HTMX will include the entire form for non get requests, so we update
            // it here.  If the name is being used in multiple locations in the
            // form, without this intervention it will not work as expected.
            event.detail.parameters = {
                ...event.detail.parameters,
                ...htmx.values(event.detail.elt, 'get'),
            }
        }
    });

}

initializeGlobalAutocompleteListeners();


    