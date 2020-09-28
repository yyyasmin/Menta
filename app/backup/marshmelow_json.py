###  FROM  https://flask-marshmallow.readthedocs.io/en/latest/

class Single_parentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = General_txt

    id = ma.auto_field()
    name = ma.auto_field()
    kids = ma.auto_field()


class kidSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = General_txt
        include_fk = True