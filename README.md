# justlog

A python wrapper for the justlog API


## Usage

```python
from justlogwrapper import JustLogApi

j = JustLogApi()

r = j.date_channel_logs("xqc", "2023", "1", "5")
print(r.status_code)
print(r.message)
print(r.data)
```

# Not Finished





