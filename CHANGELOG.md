# Changelog

## [0.6.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.6.1...v0.6.2) (2023-03-14)


### Bug Fixes

* **a11y:** no-styles support, SR improvements for multiselect ([#30](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/30)) ([4be3b5a](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/4be3b5ae98fb1514c9b5b987c25918eb9a1871ec))

## [0.6.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.6.0...v0.6.1) (2023-03-01)


### Bug Fixes

* Removed chips from accessible content ([a5e06e2](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a5e06e212a9faafe54e3bb5d4a224c2e755dd55b))

## [0.6.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.5.1...v0.6.0) (2023-02-09)


### ⚠ BREAKING CHANGES

* `no_result_text` and `narrow_search_text` replaced by the `custom_strings` dictionary.

### Features

* Component is now WCAG 2.1 compliant ([3c040f3](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3c040f344682a2d3801db2d072611520a3e0dfc1))

## [0.5.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.5.0...v0.5.1) (2023-01-26)


### Bug Fixes

* Allow adding elements when original input element is missing ([a359982](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/a3599828030df7045b836be4650b13b9dc59264b))
* Fix multi-select issue when component id and name don't match ([42d0a88](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/42d0a8889d9ea018a19eaf94a2b38750d1345515))
* Removed erroneous text ([3eb2179](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/3eb21798e90ae172b0f85eac8c27d0410180c2f0))

## [0.5.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.3...v0.5.0) (2023-01-26)


### Features

* Added configuration option for component_id ([f675405](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/f6754059f238b1a3c5c2ee4599df61dd72fa4f40))


### Documentation

* add missing imports in readme ([b61cb85](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b61cb85eddfe363f177b445329bd131e9dc99285))

## [0.4.3](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.2...v0.4.3) (2022-12-23)


### Bug Fixes

* flash of unstyled SVG; disabled field height ([#15](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/15)) ([31dd027](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/31dd027ddefe4c75dac310e9d92a6d4732d80228))
* ignore htmx directives when reloaded from another process ([63a2f78](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/63a2f78f025868be3b22b7a4e6489343110b1cec))

## [0.4.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.1...v0.4.2) (2022-12-22)


### Bug Fixes

* Blur now hides the results under htmx race conditions ([b08a678](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b08a6789dedeb1503d94d1628fab9b14d2f515bc))
* Widget uses disabled and required from attributes only ([b7a0da4](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/b7a0da46ce2d3d123380daa5582ee05904970111))

## [0.4.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.4.0...v0.4.1) (2022-12-20)


### Bug Fixes

* hide extra row unless necessary; styling improvements ([#11](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/11)) ([c627620](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c62762093974f5d1c1ee43d45364a70fbd502a35))

## [0.4.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.3.0...v0.4.0) (2022-12-15)


### Features

* Added navigation using home, end, pageup and pagedown keys ([2457d9e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/2457d9e16404abb2b2df43c0065e05d49bfbfa42))

## [0.3.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.2.0...v0.3.0) (2022-12-15)


### Features

* Added backspace keyboard navigation ([49f2c64](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/49f2c645be011d3063ad1259b4ddd4cbb371b869))

## [0.2.0](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.2...v0.2.0) (2022-12-13)


### Features

* Added keyboard navigation support ([44d15c7](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/44d15c7996b1e3e45f20c5f5fdc78cb9e34a4187))
* Added support for disabled attribute ([c29bde1](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/c29bde163fcbb7e3f7b7c29f0c5d9b707e78be01))

## [0.1.2](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.1...v0.1.2) (2022-12-12)


### Bug Fixes

* Improved blur handling ([5681830](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/5681830810ef3425e019a140dff1b03a024c5c18)), closes [#4](https://github.com/PHACDataHub/django-htmx-autocomplete/issues/4)

## [0.1.1](https://github.com/PHACDataHub/django-htmx-autocomplete/compare/v0.1.0...v0.1.1) (2022-12-09)


### Bug Fixes

* Included static files in bdist ([6d34a99](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/6d34a992b85f23f8805218c97d68764e0702df14))

## 0.1.0 (2022-12-09)


### Features

* Class and Widget based autocomplete component ([43c019e](https://github.com/PHACDataHub/django-htmx-autocomplete/commit/43c019e7694105b9aa4cc76039de4990a9f01d28))
