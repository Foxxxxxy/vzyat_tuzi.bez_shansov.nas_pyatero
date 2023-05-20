# todo здесь будет тяжелая логика с pdf
from sqlalchemy.orm import Session


def make_pdf():
    return 'pdf'


def join_request_with_model(request_list, model_class, schema_class, update_strategy, db: Session):
    request_list.sort(key=lambda x: x.id)
    model_list: list[model_class] = db.query(model_class).filter(model_class.id.in_([eq.id for eq in request_list])).order_by(model_class.id)
    responses = [
        schema_class(
            **update_strategy(equipment_request, equipment_model)
            # equipment=equipment_model,
            # amount=equipment_request.amount,
            # total_expenses=equipment_model.average_price_dollar * RUBS_FOR_DOLLAR * equipment_request.amount,
        )
        for equipment_request, equipment_model
        in zip(request_list, model_list)
    ]
    return responses
