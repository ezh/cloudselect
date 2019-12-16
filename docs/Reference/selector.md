<h1 id="cloudselect.selector">cloudselect.selector</h1>


Module that invoke FZF on list of discovered instances.

This module is invoked by CloudSelect when all data is prepared:
- configuration is loaded;
- plugins are resolved and loaded;
- arguments are parsed.

The entry point is select function.

<h2 id="cloudselect.selector.Selector">Selector</h2>

```python
Selector(self)
```
Selector class that selects cloud instances.
