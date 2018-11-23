from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User, Role, Factory, Eqp
from flask_login import current_user
from ..util.wtf.wtf_field import MultiCheckboxField
from mongoengine.queryset import QuerySet


def switch_table_and_return_query_set(collection, name):
    new_collection = collection.switch_collection(collection(), name)
    new_objects = QuerySet(collection,new_collection._get_collection())
    return new_objects


class LoginForm(Form):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegisterForm(Form):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    # username = StringField('Username', validators=[Required(), Regexp('^[A-Za-z][A-Za-z]*$', 0, 'name must be letter')])
    password = PasswordField('密码',
                             validators=[Required(),
                                         EqualTo('confirm',
                                         message='密码错误')])
    confirm = PasswordField('确认密码', validators=[Required()])
    factoryID = SelectField('工厂号', coerce=str)
    role = SelectField('登录权限', coerce=int)
    # eqp = SelectField('负责设备', coerce=int, choices=[], validators=[Required()])
    submit = SubmitField('注册')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        factorys = [f.FID for f in Factory.objects]
        self.factoryID.choices = [(factory, factory) for factory, factory in zip(factorys, factorys)]
        self.role.choices = [(role.RID, role.name) for role in Role.objects.order_by("+RID")]

    def validate_ID(self, field):
        if User.objects(UID=field.data).first():
            raise ValidationError('工号已被注册')

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username has been register')


class UserEdit(Form):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    role = SelectField('登录权限', coerce=int)
    EqpID = MultiCheckboxField('可操作设备')
    submit = SubmitField('确认修改')

    def __init__(self, *args, **kwargs):
        super(UserEdit, self).__init__(*args, **kwargs)
        Eqp_new = switch_table_and_return_query_set(Eqp, current_user.factoryID.FID + 'eqp')
        self.role.choices = [(role.RID, role.name) for role in Role.objects.order_by("+RID")]
        self.EqpID.choices = [(e.EID, e.EID) for e in Eqp_new.all()]