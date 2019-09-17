class DefaultRouter:
	""" Object for switching between databases """

	_ROUTER_TABLE = {
		'users_app'        : 'users_db',
		'projects_app'     : 'projects_db',
	}

	_DEFAULT_DB_NAME = 'default'

	@classmethod
	def _get_db(cls, app_label):
		try:
			return cls._ROUTER_TABLE[app_label]
		except Exception as e:
			return cls._DEFAULT_DB_NAME

	def db_for_read(self, model, **hints):
		""" Get database for read """
		return self._get_db(model._meta.app_label)

	def db_for_write(self, model, **hints):
		""" Get database for read """
		return self._get_db(model._meta.app_label)

	def allow_relation(self, obj1, obj2, **hints):
		""" Determine if relationship is allowed between two objects """
		# print("ALLOW RELATIONS BETWEN %s ,%s" %(obj1._meta.app_label, obj2._meta.app_label))
		return self._get_db(obj1._meta.app_label) == self._get_db(obj2._meta.app_label)

	def allow_migrate(self, db, app_label, model_name= None, **hints):
		""" Ensure that the app's models get created on the right database """
		return db == self._get_db(app_label)