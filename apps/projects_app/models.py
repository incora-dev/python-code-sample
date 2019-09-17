from django.db import models
import uuid
from django.utils.translation import gettext as _

class Project(models.Model):
    """ User profile """
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable= False)
    title = models.CharField(_("Title"), max_length= 256)
    description = models.CharField(_("Description"), max_length= 256, blank= True)
    is_active = models.BooleanField(_("Is active?"), default= True)

    user = models.OneToOneField("User", on_delete= models.CASCADE)

    created_at = models.DateTimeField(_("Created at"), auto_now_add= True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now= True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        app_label = 'projects_app'

    def __str__(self):
    	return self.title
