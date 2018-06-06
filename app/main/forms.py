from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError


class BindQueryForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('查询绑定')


class ChangeBindForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('更换绑定')


class AuthLogForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('查询认证历史')