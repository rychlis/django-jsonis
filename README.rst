django-jsonis
=============

Helper library that can be used in combination with Django Class-Based views to return JSON responses.

Features
--------
- JSONApiResponseMixin providing render_api_response and render_api_error_response methods
- Accept JSON request payload
- JSONApiFormView that can be used for simple JSON APIs using django.forms
- JSON Web token validation (pending to be moved into separate package)
- JSONTestClient providing utilities that can be used to test created APIs
- Default JSONEncoder handling Decimal numbers
- Simple jsonify template filter (add 'jsonis' to your application list in settings)

License
-------
This software is licensed under MIT.

TODO
----
- Examples!
- Documentation
- Code Cleanup
- Tests