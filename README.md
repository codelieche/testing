# Web Performance Testing
> 网站性能测试

## locust说明
- 由于需要对locust的源码进行修改，所以,进入`extra_apps/locust`安装locust
	- `cd extra_apps/locust`
	- `python setup.py install`
	- 如果环境中安装了locust,请先卸载: `pip uninstall locustio`


## 关于ldap
`account.ldap`是`django-python3-ldap`的插件。在settings中，配置ldap相关的配置。
**注意版本**，否则会报错。

```
django-python3-ldap==0.9.13
ldap3==1.4.0
```

