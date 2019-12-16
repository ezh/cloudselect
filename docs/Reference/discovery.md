<h1 id="cloudselect.discovery.discovery">cloudselect.discovery.discovery</h1>

Module providing Discovery service base class and service provider.
<h1 id="cloudselect.discovery.stub">cloudselect.discovery.stub</h1>


<h1 id="cloudselect.discovery.aws">cloudselect.discovery.aws</h1>

Module collecting instances from AWS cloud.
<h2 id="cloudselect.discovery.aws.AWS">AWS</h2>

```python
AWS(self)
```
Class implementing discovery service plugin.
<h3 id="cloudselect.discovery.aws.AWS.run">run</h3>

```python
AWS.run(self)
```
Collect AWS instances.
<h3 id="cloudselect.discovery.aws.AWS.instances">instances</h3>

```python
AWS.instances(self)
```
Collect AWS instances.
<h3 id="cloudselect.discovery.aws.AWS.find">find</h3>

```python
AWS.find()
```
Discover instances in AWS cloud.
<h3 id="cloudselect.discovery.aws.AWS.get_option">get_option</h3>

```python
AWS.get_option(options, option_name, profile, region)
```
Get an option from more precise to more general.
<h3 id="cloudselect.discovery.aws.AWS.get_ip">get_ip</h3>

```python
AWS.get_ip(self, instance, config)
```
Get instance IP.
<h3 id="cloudselect.discovery.aws.AWS.get_key">get_key</h3>

```python
AWS.get_key(self, instance, config)
```
Get instance key.
<h3 id="cloudselect.discovery.aws.AWS.get_metadata">get_metadata</h3>

```python
AWS.get_metadata(instance)
```
Get instance metadata.
<h3 id="cloudselect.discovery.aws.AWS.get_user">get_user</h3>

```python
AWS.get_user(self, instance, config)
```
Get instance user.
<h3 id="cloudselect.discovery.aws.AWS.tag">tag</h3>

```python
AWS.tag(instance, tag)
```
Flatten instance tags.
<h1 id="cloudselect.discovery.local">cloudselect.discovery.local</h1>

Module collecting instances from shell output.
<h2 id="cloudselect.discovery.local.Local">Local</h2>

```python
Local(self)
```
Class implementing discovery service plugin.
<h3 id="cloudselect.discovery.local.Local.run">run</h3>

```python
Local.run(self)
```
Collect instances from shell output.
<h3 id="cloudselect.discovery.local.Local.instances">instances</h3>

```python
Local.instances(self)
```
Collect instances from shell output.
<h3 id="cloudselect.discovery.local.Local.get_key">get_key</h3>

```python
Local.get_key(self, host)
```
Get key for ssh host.
<h3 id="cloudselect.discovery.local.Local.get_user">get_user</h3>

```python
Local.get_user(self, host)
```
Get user for SSH host.
