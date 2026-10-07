from marshmallow import Schema,fields,validate

class TravelerCreateSchema(Schema):

    name = fields.Str(
        required=True,
        validate=validate.Length(min=3,max=100)
    )

    email = fields.Email(
        required=True
    )