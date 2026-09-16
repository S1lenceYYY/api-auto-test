from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined)


def render_obj(obj, context):
    if isinstance(obj, str):
        try:
            return env.from_string(obj).render(**context)
        except Exception as e:
            raise ValueError(f"模板渲染失败：{obj}，错误：{e}")
    elif isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k == "sql_check":
                new_dict[k] = v
            else:
                new_dict[k] = render_obj(v, context)
        return new_dict
    elif isinstance(obj, list):
        return [render_obj(item, context) for item in obj]
    else:
        return obj