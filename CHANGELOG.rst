Changelog
=========

* 0.2.0 (not released)
    * Use Django cache instead of URL parameters in order to prevent potential remote code execution.
    * Fixed issue where tags with multiple args would not work.
    * Removed template tag args/kwargs always being passed in as strings.

* 0.1 (July 28, 2015)
    * Initial alpha release