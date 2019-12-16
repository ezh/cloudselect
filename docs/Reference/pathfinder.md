<h1 id="cloudselect.pathfinder.pathfinder">cloudselect.pathfinder.pathfinder</h1>

Module providing PathFinder service base class and service provider.
<h1 id="cloudselect.pathfinder.stub">cloudselect.pathfinder.stub</h1>


<h1 id="cloudselect.pathfinder.bastion">cloudselect.pathfinder.bastion</h1>

Module that enrich instances with jumphosts.
<h2 id="cloudselect.pathfinder.bastion.Bastion">Bastion</h2>

```python
Bastion(self)
```
Bastion implementation.
<h3 id="cloudselect.pathfinder.bastion.Bastion.run">run</h3>

```python
Bastion.run(self, instance, instances)
```
Enrich instance with jumphost if any.
<h3 id="cloudselect.pathfinder.bastion.Bastion.find_jumphost">find_jumphost</h3>

```python
Bastion.find_jumphost(self, metadata_key, value_pattern, instance)
```
Find jumphost among instances.
