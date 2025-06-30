# Changelog

## [0.6.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.1...v0.6.0) (2025-06-30)


### ⚠ BREAKING CHANGES

* major API and routing changes ([#60](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/60))
* `no_result_text` and `narrow_search_text` replaced by the `custom_strings` dictionary.

### Features

* Ability to filter items based on current user ([be8bcc7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/be8bcc72b10630493e7523960a90efbd86580920))
* Added backspace keyboard navigation ([49f2c64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/49f2c645be011d3063ad1259b4ddd4cbb371b869))
* Added configuration option for component_id ([f675405](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/f6754059f238b1a3c5c2ee4599df61dd72fa4f40))
* Added keyboard navigation support ([44d15c7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/44d15c7996b1e3e45f20c5f5fdc78cb9e34a4187))
* Added navigation using home, end, pageup and pagedown keys ([2457d9e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/2457d9e16404abb2b2df43c0065e05d49bfbfa42))
* Added support for disabled attribute ([c29bde1](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c29bde163fcbb7e3f7b7c29f0c5d9b707e78be01))
* Allow name field to be overriden ([725524d](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/725524d94c5b00ef3bb805dede5995a96e0af161))
* allow showing HTML options, vary chip/input display ([#77](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/77)) ([d096ec4](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/d096ec40bff718e9c72e929a843f8876f617523b))
* Class and Widget based autocomplete component ([43c019e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/43c019e7694105b9aa4cc76039de4990a9f01d28))
* Component is now WCAG 2.1 compliant ([3c040f3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3c040f344682a2d3801db2d072611520a3e0dfc1))
* major API and routing changes ([#60](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/60)) ([0208d64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/0208d64e86dd0e89e1b9a09704638b60f5af6e85))


### Bug Fixes

* **a11y:** no-styles support, SR improvements for multiselect ([#30](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/30)) ([4be3b5a](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/4be3b5ae98fb1514c9b5b987c25918eb9a1871ec))
* Allow adding elements when original input element is missing ([a359982](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a3599828030df7045b836be4650b13b9dc59264b))
* allow toggling to a different item ([2c48a51](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/2c48a513da44ba6bdfab1c8bda0128f3a6a7d6e5))
* block unauthenticated mistake in docs ([#81](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/81)) ([d938b90](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/d938b90277df686f7f0e5b8f9c9f773cd95f62c5))
* Blur now hides the results under htmx race conditions ([b08a678](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b08a6789dedeb1503d94d1628fab9b14d2f515bc))
* chip should have hx-target this ([#55](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/55)) ([5e39f63](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5e39f63e1f9f86baa1f5d5c6c0e213534795cf4d))
* dont repeatedly evaluate queryset in model ACs ([df80e21](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/df80e214708f5fadd6a03e4e46ed3b7295a4649a))
* escape key was hiding autocomplete even after subsequent letter presses ([6e737e3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6e737e339b62c4d7f252f2d126f6cbc9f6bfb064))
* Fix handling of return widget return values when using ModelChoiceField ([17ccdb6](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/17ccdb6540cec7ccc5cf019eeeee7bef3ff9488f)), closes [#33](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/33)
* fix lazy placeholders json bug ([ef4ab31](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/ef4ab31dec53e9b81dd9163b00e04fc094015dc4))
* Fix multi-select issue when component id and name don't match ([42d0a88](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/42d0a8889d9ea018a19eaf94a2b38750d1345515))
* flash of unstyled SVG; disabled field height ([#15](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/15)) ([31dd027](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/31dd027ddefe4c75dac310e9d92a6d4732d80228))
* Formset support ([#69](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/69)) ([d6e7975](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/d6e7975852adac1aeaa23f48c081b28e5cc8a2ad))
* Handles forms that was on change ([de6820c](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/de6820c30b480ca5453f367942da7ecd4526c344)), closes [#38](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/38)
* hide extra row unless necessary; styling improvements ([#11](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/11)) ([c627620](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c62762093974f5d1c1ee43d45364a70fbd502a35))
* ignore htmx directives when reloaded from another process ([63a2f78](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/63a2f78f025868be3b22b7a4e6489343110b1cec))
* Improved blur handling ([5681830](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5681830810ef3425e019a140dff1b03a024c5c18)), closes [#4](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/4)
* Included static files in bdist ([6d34a99](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6d34a992b85f23f8805218c97d68764e0702df14))
* model-autocomplete bug ([#66](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/66)) ([e53b3a0](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/e53b3a0b26c63b84881574814255037558a47a3c))
* only count queryset once ([3cce56b](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3cce56b5cb9102242e5a67f794b8030e156fadff))
* prevent autofill ([#78](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/78)) ([8ee7de2](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/8ee7de249d0a2b2f344dd8c4f38c44aca46ef2d7))
* Removed chips from accessible content ([a5e06e2](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a5e06e212a9faafe54e3bb5d4a224c2e755dd55b))
* Removed erroneous text ([3eb2179](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3eb21798e90ae172b0f85eac8c27d0410180c2f0))
* selecting an item swaps its inherited hx-target ([c018677](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c018677925033c35abd4bb4c0e99699bce96d75a))
* str-based IDs break when non-multiselect ([1a1d883](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/1a1d883075d71597e831eb92ed07ca323c34a150))
* Widget uses disabled and required from attributes only ([b7a0da4](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b7a0da46ce2d3d123380daa5582ee05904970111))
* xss: unescaped component_prefix ([#82](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/82)) ([a419131](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a419131e67ae7dfc124344c1535b1b03806aeff3))


### Dependencies

* add debug-toolbar for development ([b95d9c9](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b95d9c94b7187a9ab55cd71c872f3ec1dadd96ff))


### Reverts

* Ability to filter items based on current user ([bf3d343](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/bf3d343fcdd7d800d2b98eeee57e2f3f6d5ef024))


### Documentation

* add missing imports in readme ([b61cb85](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b61cb85eddfe363f177b445329bd131e9dc99285))

## [1.0.5](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.4...v1.0.5) (2024-11-27)

### Bug Fixes

- fix issue with dynamic formsets

## [1.0.4](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.3...v1.0.4) (2024-11-26)

### Bug Fixes

- fix issue in single-select when toggling to a different element

## [1.0.3](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.2...v1.0.3) (2024-11-26)

### Bug Fixes

- fix issue with lazy placeholder strings causing a json serialization exception

## [1.0.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.1...v1.0.2) (2024-11-25)

### Bug Fixes

- fix issue with model-autocomplete repeatedly evaluating queryset, causing N queries for N items

## [1.0.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v1.0.0...v1.0.1) (2024-11-25)

### Bug Fixes

- fix issue when model-autocomplete is used with a model that doesn't have `name` property

## [1.0.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.8.4...v1.0.0) (2024-11-22)

### ⚠ BREAKING CHANGES

- major API and routing changes ([#60](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/60))
- `no_result_text` and `narrow_search_text` replaced by the `custom_strings` dictionary.

### Features

- Ability to filter items based on current user ([be8bcc7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/be8bcc72b10630493e7523960a90efbd86580920))
- Added backspace keyboard navigation ([49f2c64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/49f2c645be011d3063ad1259b4ddd4cbb371b869))
- Added configuration option for component_id ([f675405](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/f6754059f238b1a3c5c2ee4599df61dd72fa4f40))
- Added keyboard navigation support ([44d15c7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/44d15c7996b1e3e45f20c5f5fdc78cb9e34a4187))
- Added navigation using home, end, pageup and pagedown keys ([2457d9e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/2457d9e16404abb2b2df43c0065e05d49bfbfa42))
- Added support for disabled attribute ([c29bde1](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c29bde163fcbb7e3f7b7c29f0c5d9b707e78be01))
- Allow name field to be overriden ([725524d](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/725524d94c5b00ef3bb805dede5995a96e0af161))
- Class and Widget based autocomplete component ([43c019e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/43c019e7694105b9aa4cc76039de4990a9f01d28))
- Component is now WCAG 2.1 compliant ([3c040f3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3c040f344682a2d3801db2d072611520a3e0dfc1))
- major API and routing changes ([#60](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/60)) ([0208d64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/0208d64e86dd0e89e1b9a09704638b60f5af6e85))

### Bug Fixes

- **a11y:** no-styles support, SR improvements for multiselect ([#30](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/30)) ([4be3b5a](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/4be3b5ae98fb1514c9b5b987c25918eb9a1871ec))
- Allow adding elements when original input element is missing ([a359982](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a3599828030df7045b836be4650b13b9dc59264b))
- Blur now hides the results under htmx race conditions ([b08a678](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b08a6789dedeb1503d94d1628fab9b14d2f515bc))
- chip should have hx-target this ([#55](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/55)) ([5e39f63](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5e39f63e1f9f86baa1f5d5c6c0e213534795cf4d))
- escape key was hiding autocomplete even after subsequent letter presses ([6e737e3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6e737e339b62c4d7f252f2d126f6cbc9f6bfb064))
- Fix handling of return widget return values when using ModelChoiceField ([17ccdb6](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/17ccdb6540cec7ccc5cf019eeeee7bef3ff9488f)), closes [#33](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/33)
- Fix multi-select issue when component id and name don't match ([42d0a88](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/42d0a8889d9ea018a19eaf94a2b38750d1345515))
- flash of unstyled SVG; disabled field height ([#15](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/15)) ([31dd027](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/31dd027ddefe4c75dac310e9d92a6d4732d80228))
- Handles forms that was on change ([de6820c](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/de6820c30b480ca5453f367942da7ecd4526c344)), closes [#38](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/38)
- hide extra row unless necessary; styling improvements ([#11](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/11)) ([c627620](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c62762093974f5d1c1ee43d45364a70fbd502a35))
- ignore htmx directives when reloaded from another process ([63a2f78](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/63a2f78f025868be3b22b7a4e6489343110b1cec))
- Improved blur handling ([5681830](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5681830810ef3425e019a140dff1b03a024c5c18)), closes [#4](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/4)
- Included static files in bdist ([6d34a99](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6d34a992b85f23f8805218c97d68764e0702df14))
- model-autocomplete bug ([#66](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/66)) ([e53b3a0](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/e53b3a0b26c63b84881574814255037558a47a3c))
- Removed chips from accessible content ([a5e06e2](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a5e06e212a9faafe54e3bb5d4a224c2e755dd55b))
- Removed erroneous text ([3eb2179](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3eb21798e90ae172b0f85eac8c27d0410180c2f0))
- selecting an item swaps its inherited hx-target ([c018677](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c018677925033c35abd4bb4c0e99699bce96d75a))
- str-based IDs break when non-multiselect ([1a1d883](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/1a1d883075d71597e831eb92ed07ca323c34a150))
- Widget uses disabled and required from attributes only ([b7a0da4](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b7a0da46ce2d3d123380daa5582ee05904970111))

### Reverts

- Ability to filter items based on current user ([bf3d343](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/bf3d343fcdd7d800d2b98eeee57e2f3f6d5ef024))

### Documentation

- add missing imports in readme ([b61cb85](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b61cb85eddfe363f177b445329bd131e9dc99285))

## [0.8.4](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.8.3...v0.8.4) (2024-07-30)

### Bug Fixes

- chip should have hx-target this ([#55](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/55)) ([5e39f63](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5e39f63e1f9f86baa1f5d5c6c0e213534795cf4d))

## [0.8.3](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.8.2...v0.8.3) (2023-08-04)

### Bug Fixes

- selecting an item swaps its inherited hx-target ([c018677](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c018677925033c35abd4bb4c0e99699bce96d75a))

## [0.8.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.8.1...v0.8.2) (2023-07-07)

### Bug Fixes

- escape key was hiding autocomplete even after subsequent letter presses ([6e737e3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6e737e339b62c4d7f252f2d126f6cbc9f6bfb064))

## [0.8.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.8.0...v0.8.1) (2023-06-28)

### Reverts

- Ability to filter items based on current user ([bf3d343](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/bf3d343fcdd7d800d2b98eeee57e2f3f6d5ef024))

## [0.8.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.7.1...v0.8.0) (2023-06-27)

### Features

- Ability to filter items based on current user ([be8bcc7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/be8bcc72b10630493e7523960a90efbd86580920))

### Bug Fixes

- str-based IDs break when non-multiselect ([1a1d883](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/1a1d883075d71597e831eb92ed07ca323c34a150))

## [0.7.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.7.0...v0.7.1) (2023-05-16)

### Bug Fixes

- Handles forms that was on change ([de6820c](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/de6820c30b480ca5453f367942da7ecd4526c344)), closes [#38](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/38)

## [0.7.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.6.2...v0.7.0) (2023-04-27)

### Features

- Allow name field to be overriden ([725524d](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/725524d94c5b00ef3bb805dede5995a96e0af161))

### Bug Fixes

- Fix handling of return widget return values when using ModelChoiceField ([17ccdb6](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/17ccdb6540cec7ccc5cf019eeeee7bef3ff9488f)), closes [#33](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/33)

## [0.6.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.6.1...v0.6.2) (2023-03-14)

### Bug Fixes

- **a11y:** no-styles support, SR improvements for multiselect ([#30](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/30)) ([4be3b5a](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/4be3b5ae98fb1514c9b5b987c25918eb9a1871ec))

## [0.6.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.6.0...v0.6.1) (2023-03-01)

### Bug Fixes

- Removed chips from accessible content ([a5e06e2](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a5e06e212a9faafe54e3bb5d4a224c2e755dd55b))

## [0.6.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.5.1...v0.6.0) (2023-02-09)

### ⚠ BREAKING CHANGES

- `no_result_text` and `narrow_search_text` replaced by the `custom_strings` dictionary.

### Features

- Component is now WCAG 2.1 compliant ([3c040f3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3c040f344682a2d3801db2d072611520a3e0dfc1))

## [0.5.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.5.0...v0.5.1) (2023-01-26)

### Bug Fixes

- Allow adding elements when original input element is missing ([a359982](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a3599828030df7045b836be4650b13b9dc59264b))
- Fix multi-select issue when component id and name don't match ([42d0a88](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/42d0a8889d9ea018a19eaf94a2b38750d1345515))
- Removed erroneous text ([3eb2179](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3eb21798e90ae172b0f85eac8c27d0410180c2f0))

## [0.5.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.3...v0.5.0) (2023-01-26)

### Features

- Added configuration option for component_id ([f675405](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/f6754059f238b1a3c5c2ee4599df61dd72fa4f40))

### Documentation

- add missing imports in readme ([b61cb85](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b61cb85eddfe363f177b445329bd131e9dc99285))

## [0.4.3](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.2...v0.4.3) (2022-12-23)

### Bug Fixes

- flash of unstyled SVG; disabled field height ([#15](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/15)) ([31dd027](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/31dd027ddefe4c75dac310e9d92a6d4732d80228))
- ignore htmx directives when reloaded from another process ([63a2f78](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/63a2f78f025868be3b22b7a4e6489343110b1cec))

## [0.4.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.1...v0.4.2) (2022-12-22)

### Bug Fixes

- Blur now hides the results under htmx race conditions ([b08a678](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b08a6789dedeb1503d94d1628fab9b14d2f515bc))
- Widget uses disabled and required from attributes only ([b7a0da4](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b7a0da46ce2d3d123380daa5582ee05904970111))

## [0.4.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.0...v0.4.1) (2022-12-20)

### Bug Fixes

- hide extra row unless necessary; styling improvements ([#11](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/11)) ([c627620](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c62762093974f5d1c1ee43d45364a70fbd502a35))

## [0.4.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.3.0...v0.4.0) (2022-12-15)

### Features

- Added navigation using home, end, pageup and pagedown keys ([2457d9e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/2457d9e16404abb2b2df43c0065e05d49bfbfa42))

## [0.3.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.2.0...v0.3.0) (2022-12-15)

### Features

- Added backspace keyboard navigation ([49f2c64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/49f2c645be011d3063ad1259b4ddd4cbb371b869))

## [0.2.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.2...v0.2.0) (2022-12-13)

### Features

- Added keyboard navigation support ([44d15c7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/44d15c7996b1e3e45f20c5f5fdc78cb9e34a4187))
- Added support for disabled attribute ([c29bde1](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c29bde163fcbb7e3f7b7c29f0c5d9b707e78be01))

## [0.1.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.1...v0.1.2) (2022-12-12)

### Bug Fixes

- Improved blur handling ([5681830](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5681830810ef3425e019a140dff1b03a024c5c18)), closes [#4](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/4)

## [0.1.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.0...v0.1.1) (2022-12-09)

### Bug Fixes

- Included static files in bdist ([6d34a99](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6d34a992b85f23f8805218c97d68764e0702df14))

## 0.1.0 (2022-12-09)

### Features

- Class and Widget based autocomplete component ([43c019e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/43c019e7694105b9aa4cc76039de4990a9f01d28))
