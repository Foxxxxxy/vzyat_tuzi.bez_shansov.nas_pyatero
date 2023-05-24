from pydantic import BaseModel
from pydantic.fields import ModelField


def round_floats(model: BaseModel):
    fields = model.__class__.__fields__
    for field_name, field in fields.items():
        if field.type_ == float:
            try:
                setattr(model, field_name, round(getattr(model, field_name), 2))
            except AttributeError:
                # if field is optional and value is empty - skip it
                pass
