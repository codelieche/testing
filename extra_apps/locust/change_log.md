# 修改locust源码记录

## 添加增加并发用户数的接口
### 修改文件及内容
- `locust/web.py` 添加`swarm_add()`方法

```python
@app.route('/swarm/add', methods=["POST"])
def swarm_add():
    """
    由于在测试过程中，要逐步增加并发用户数，需要添加接口
    同时还需要修改runners.py
    :return:
    """
    assert request.method == "POST"

    locust_count = int(request.form["locust_count"])
    hatch_rate = float(request.form["hatch_rate"])
    runners.locust_runner.add_hatching(locust_count, hatch_rate)
    response = make_response(json.dumps({'success': True, 'message': 'Swarming add user number'}))
    response.headers["Content-type"] = "application/json"
    return response
```

- `locust/runners.py`的`LocustRunner`添加方法`add_hatching`

```python
def add_hatching(self, locust_count=None, hatch_rate=None, wait=False):
    self.num_clients += locust_count
    if locust_count > 0:
        # 当传入的locust_count大于0的时候，增加并发用户数
        self.spawn_locusts(spawn_count=locust_count)
    elif locust_count < 0:
        # 当传入的locust_count是个负数的时候，减少并发用户数
        self.kill_locusts(kill_count=locust_count)
```

- `locust/runners.py`的`LocalLocustRunner(LocustRunner):`添加`add_hatching`

```python
def add_hatching(self, locust_count=None, hatch_rate=None, wait=False):
    # 添加并发用户数修改
    self.hatching_greenlet = gevent.spawn(lambda: super(LocalLocustRunner, self).add_hatching(locust_count, hatch_rate, wait=wait))
    self.greenlet = self.hatching_greenlet

```

## 对reset数据进行修改
