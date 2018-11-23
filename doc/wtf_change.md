# wtf.html 的改动

在 util.wtf 中加入了一个自定义的 multicheckboxfield, 用于管理员修改工程师的设备查看权限

同时, 在 /usr/local/python3.5/lib/python3.5/site-packages/flask_bootstrap/templates/bootstrap/wtf.html 中做出如下修改

在 84 行之后加入

```html
{%- elif 'Multi' in field.type  -%}
  <div class="multiField">
    <label>{{ field.label }}</label><br/>
    {% for item in field -%}
      {% call _hz_form_wrap(horizontal_columns, form_type, True, required=required) %}
        {{form_field(item,form_type,horizontal_columns,button_map)}}
      {% endcall %}
    {% endfor %}
  </div>
```

同时将 42 行改为

```html
<div class="checkbox-inline">
```