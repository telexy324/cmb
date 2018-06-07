from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from flask_uploads import UploadSet, DOCUMENTS
from flask_wtf.file import FileField, FileAllowed, FileRequired
#from manage import files


class BindQueryForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('查询绑定')


class ChangeBindForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('更换绑定')


class AuthLogForm(FlaskForm):
    faccountid = StringField('方宽ID', validators=[DataRequired(message='请填写!'), Length(0, 8)])
    submit = SubmitField('查询认证历史')

files = UploadSet('files', DOCUMENTS)

class UploadForm(FlaskForm):
    upload = FileField('请选择文件, 格式为xls或xlsx, 不超过100MB', validators=[FileRequired(),FileAllowed(files, '只接受文件!')])
    submit = SubmitField('文件上传')