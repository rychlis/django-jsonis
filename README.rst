django-jsonis
=============

Helper library that can be used in combination with Django Class-Based views to return JSON responses.

Features
--------
- JSONApiResponseMixin providing render_api_response and render_api_error_response methods
- Accepting JSON encoding of POST request body
- JSONApiFormView that can be used for simple JSON APIs using django.forms
- JSON Web token validation (pending to be moved into separate package)
- JSONTestClient providing utilities taht can be used to test created APIs
- Default JSONEncoder handling Decimal numbers
- Simple jsonify template tag (you will need to install jsonis)

License
-------
This software is licensed under MIT.

TODO
----
- Documentation
- Code Cleanup
- Tests