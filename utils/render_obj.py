from jinja2 import Template

def render_obj(obj,context):

    if isinstance(obj, str):
        # 字符串才做jinja渲染
        return Template(obj).render(**context)
    elif isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k == "sql_check":
                new_dict[k] = v
            else:
                new_dict[k] = render_obj(v, context)
        return new_dict
    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            new_list.append(render_obj(item, context))
        return new_list
    else:
        # int bool None float，直接原样返回
        return obj