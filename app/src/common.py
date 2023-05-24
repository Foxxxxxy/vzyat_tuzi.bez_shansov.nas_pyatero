from typing import Union

from pydantic import BaseModel
from pydantic.fields import ModelField


def round_floats(model: Union[BaseModel, list]):
    if isinstance(model, list):
        for i in model:
            round_floats(i)
        return
    if not isinstance(model, BaseModel):
        return

    fields = model.__class__.__fields__
    for field_name, field in fields.items():
        if field.type_ == float:
            try:
                setattr(model, field_name, round(getattr(model, field_name), 2))
            except AttributeError:
                # if field is optional and value is empty - skip it
                pass

        if issubclass(field.type_, BaseModel):
            round_floats(getattr(model, field_name))


def prepare_to_front(model: Union[BaseModel, list]):
    round_floats(model)
