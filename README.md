# EIDO example dashboard



## Database

This application uses MongoDB as a database, and makes use of [Beanie](https://beanie-odm.dev)
as an object-document mapper. Beanie integrates perfectly with FastAPI, such that all database
models can simply be defined by a single class in the `models` directory. Pydantic removes the
need to use serializers alongside these model classes, and Beanie takes care of the rest.

When defining a model, there's one more layer of abstraction called `MongoModel`, from which
all database models should inherit. `MongoModel` just adds simple fields for datestamping, but
feel free to extend this class if you want any other custom model fields. `AppBaseModel`
is another fundamental abstraction, used for non-database models. Inherit from this model
if you need to structure incoming/outgoing data, such as for POST or PATCH requests.


## Directory structure

The `app/routers/` directory contains the views, a.k.a. the API endpoints. These are separated in
different types of routes, such as public routes, user-specific routes, or admin routes. The routes
use dependency injection, chiefly calling the service classes.

There exist some base service classes, which allow some common CRUD logic to be reused, such as
throwing a HTTP exception when an patient is not found in the database. Some methods can be called
directly, while others, which might need to specify their schema, will be called from patient
specific service classes. You'll usually create a service class for each model class that you have,
but these can be quite minimal if their simple CRUD operations.

You can also add business logic to these service classes (not the base class, but rather the service class
pertaining to a specific model patient), and call other functions from there.

The `app/integrations` folder contains wrapper classes for interacting with third-party services, such
as those for payments (like stripe), notifications (like FCM), or email (like sendgrid). These integration
classes will generally be called in the service layer. Technically, these are also services, so they are
called as such. They reside in their own folder just to indicate



## Middleware

Internal server errors general imply bugs, there's an exception catching middleware in place
in `app/middleware.py` that can send a slack message to the team when one is thrown. There's
also a handler for 422 errors, which are common in FastAPI (since it's hard, yet essential
to add proper typing to your data schema). The handler is there to simply add more detail to
the response, as the default response can be unhelpful.


## Settings

In `app/settings.py`, we parse environment variables. These may come from Docker, a `.env` file,
or anywhere else. Pydantic coaxes these to snake case, and they become available anywhere in the
app by simply calling `get_settings()`.
