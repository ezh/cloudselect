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
<h3 id="cloudselect.selector.Selector.complete">complete</h3>

```python
Selector.complete(self, cline, cpoint)
```
List profiles for shell completion.
<h3 id="cloudselect.selector.Selector.edit">edit</h3>

```python
Selector.edit(self, configuration)
```
Edit profile or shared configuration file if file is None.
<h3 id="cloudselect.selector.Selector.execute">execute</h3>

```python
Selector.execute(program, args, **kwargs)
```
Execute a command in a subprocess and returns its standard output.
<h3 id="cloudselect.selector.Selector.fzf_select">fzf_select</h3>

```python
Selector.fzf_select(self, instances)
```
Invoke FZF with list of instances and return selected.
<h3 id="cloudselect.selector.Selector.get_editor">get_editor</h3>

```python
Selector.get_editor(self)
```
Get editor path.
<h3 id="cloudselect.selector.Selector.profile_list">profile_list</h3>

```python
Selector.profile_list(self)
```
List available profiles.
<h3 id="cloudselect.selector.Selector.profile_process">profile_process</h3>

```python
Selector.profile_process(self)
```
Run selection process for the specific profile.
<h3 id="cloudselect.selector.Selector.select">select</h3>

```python
Selector.select(self)
```
Entry point. Select instances.
