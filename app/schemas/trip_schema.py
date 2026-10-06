from marshmallow import Schema,fields,validate

class TripCreateSchema(Schema):
    destination = fields.Str(
        required=True,
        validate=validate.Length(min=3,max=100)
    )

    start_date = fields.Date(
        required=True
    )

    end_date = fields.Date(
        required=True
    )
    budget = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )
    max_travelers = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

class TripResponseSchema(Schema):
    id = fields.Int()
    destination = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    budget = fields.Int()
    max_travelers = fields.Int()
    current_travelers=fields.Int()
    expenses=fields.Int()
    status = fields.Function(
        lambda obj: obj.status.value
    )
