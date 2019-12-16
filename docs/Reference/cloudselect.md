<h1 id="cloudselect.cloudselect">cloudselect.cloudselect</h1>

CloudSelect module loads configuration, plugins and invokes Select module.
<h2 id="cloudselect.cloudselect.CloudSelect">CloudSelect</h2>

```python
CloudSelect(self)
```
CloudSelect class that bootstraps application.

Attributes:
configpath     The maximum speed that such a bird can attain.
extension           Th locaosle where these birds congregate to reproduce.

<h3 id="cloudselect.cloudselect.CloudSelect.configuration_exists">configuration_exists</h3>

```python
CloudSelect.configuration_exists(self, name)
```
Check if configuration/profile exists.
<h3 id="cloudselect.cloudselect.CloudSelect.configuration_read">configuration_read</h3>

```python
CloudSelect.configuration_read(self, name=None)
```
Read configuration/profile.
<h3 id="cloudselect.cloudselect.CloudSelect.fabric">fabric</h3>

```python
CloudSelect.fabric(self, configuration, args)
```
Load discovery, group, pathfinder, report plugins.
<h3 id="cloudselect.cloudselect.CloudSelect.fabric_load_plugin">fabric_load_plugin</h3>

```python
CloudSelect.fabric_load_plugin(self, configuration, plugin_type, service_provider, service_stub)
```
Load plugins.
<h3 id="cloudselect.cloudselect.CloudSelect.merge">merge</h3>

```python
CloudSelect.merge(dict1, dict2, path=None)
```
Merge two dictioraries.
<h3 id="cloudselect.cloudselect.CloudSelect.options">options</h3>

```python
CloudSelect.options(self, name, metadata=None)
```
Get plugin/block options.
<h3 id="cloudselect.cloudselect.CloudSelect.parse_args">parse_args</h3>

```python
CloudSelect.parse_args(args)
```
Parse command line arguments.
<h3 id="cloudselect.cloudselect.CloudSelect.plugin">plugin</h3>

```python
CloudSelect.plugin(self, plugin_class, service_provider)
```
Return service provider.
<h3 id="cloudselect.cloudselect.CloudSelect.resolve">resolve</h3>

```python
CloudSelect.resolve(self, reference, base)
```
Resolve strings to objects using standard import and attribute syntax.
<h2 id="cloudselect.cloudselect.complete">complete</h2>

```python
complete()
```
Show completion list.
<h2 id="cloudselect.cloudselect.main">main</h2>

```python
main()
```
Run CloudSelect.
