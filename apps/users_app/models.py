from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
import uuid
from django.utils.translation import gettext as _
from datetime import datetime
from django.core.mail import send_mail
import jwt
from django.contrib.auth.hashers import Argon2PasswordHasher
from django.utils.crypto import get_random_string

admin_email = getattr(settings, 'ADMIN_EMAIL')
restore_password_link = getattr(settings, 'RESTORE_PASSWORD_LINK')

jwt_settings = getattr(settings, 'JWT_SETTINGS')

class CustomModelMixin:

    def update(self, **fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)

class User(models.Model, CustomModelMixin):
    """ Custom user model """
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    email = models.EmailField(_("Email"), max_length= 256, blank= False, unique= True)
    password = models.CharField(_("Password"), max_length= 265, blank= False)
    is_active = models.BooleanField(_("Is active?"), default= True)
    deleted_date = models.DateTimeField(_("Deleted date"), blank= True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add= True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now= True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'users_app'

    _tokenize_fields = (
        'id', 'email', 'password', 'created_at'
        )

    hasher = Argon2PasswordHasher()

    @property
    def tokenize_fields(self):
        payload = {}
        print("META: ", self._meta)
        for field in self._tokenize_fields:
            payload[field] = getattr(self, field)
        return payload

    def __str__(self):
        return self.email

    def _generate_confirm_code(self):
        return restore_password_link + get_random_string()

    @classmethod
    def _hash_password(cls, password):
        cls.hasher.encode(password, get_random_string())

    def _check_hash(self, password):
        cls.hasher.verify(password)

    def _encode_token(self):
        return jwt.encode(
            self.tokenize_fields,
            jwt_settings['JWT_SECRET_KEY'],
            jwt_settings['JWT_ALGORITHM'],
        ).decode('utf-8')

    @staticmethod
    def _decode_token(token, context= None):
        return jwt.decode(
            token,
            jwt_settings['JWT_SECRET_KEY'],
            jwt_settings['JWT_VERIFY'],
            options= {
                'verify_exp': jwt_settings['JWT_VERIFY_EXPIRATION'],
            },
            leeway= jwt_settings['JWT_LEEWAY'],
            audience= jwt_settings['JWT_AUDIENCE'],
            issuer= jwt_settings['JWT_ISSUER'],
            algorithms= [jwt_settings['JWT_ALGORITHM']]
        )

    @classmethod
    def login(cls, login, password):
        user = cls.objects.filter(email= login).first()
        if not (user or user._check_hash(password)):
            raise Exception("Invalid password or email")
        return user._encode_token()

    @classmethod
    def find_by_token(cls, token, context= None):
        try:
            payload = cls._decode_token(token, context)
            user = cls.objects.filter(email= payload['email'], id= payload['id']).first()
            if not (user or user._check_hash(payload['password'])):
                raise GraphQLJWTError(_('Password was changed'))
            del payload['password']
        except jwt.ExpiredSignature:
            raise GraphQLJWTError(_('Signature has expired'))
        except jwt.DecodeError:
            raise GraphQLJWTError(_('Error decoding signature'))
        except jwt.InvalidTokenError:
            raise GraphQLJWTError(_('Invalid token'))
        return payload

    @classmethod
    def find_by_id(cls, user_id):
        return cls.objects.filter(id= user_id).first()

    def delete(self):
        self.deleted_date = datetime.utcnow()
        self.is_active = False
        self.profile.delete()
        self.save()

class UserProfile(models.Model, CustomModelMixin):
    """ User profile """
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    photo_url = models.CharField(_("Photo url"), max_length= 256, blank= True)
    photo_name = models.CharField(_("Photo name"), max_length= 256, blank= True)
    name = models.CharField(_("Name"), max_length= 256, blank= True)

    user = models.OneToOneField("User", on_delete= models.CASCADE)

    created_at = models.DateTimeField(_("Created at"), auto_now_add= True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now= True)

class StripeCustomer(models.Model, CustomModelMixin):
    """ Stripe customer model """
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    email = models.EmailField(_("Email"), max_length= 256, blank= False, unique= True)

    user = models.OneToOneField("User", on_delete= models.CASCADE)

    created_at = models.DateTimeField(_("Created at"), auto_now_add= True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now= True)

class ConfirmCode(models.Model, CustomModelMixin):
    """ Confirm code sended after changing password """
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    activated = models.BooleanField(_("Is activated?"), default= False)
    receiver = models.CharField(_("Receiver"), max_length= 265)

    created_at = models.DateTimeField(_("Created at"), auto_now_add= True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now= True)
