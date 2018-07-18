###  missing 1 required positional argument: 'on_delete'
	>issue
	vent = models.ForeignKey(Event)
    TypeError: __init__() missing 1 required positional argument: 'on_delete'
    >solution
    event = models.ForeignKey(Event,on_delete=models.CASCADE,)
    Since Django 2.x, on_delete is required.
	Deprecated since version 1.9: on_delete will become a required argument in Django 2.0. In older versions it defaults to CASCADE.