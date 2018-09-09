# coding: utf-8
import os

try:
    from config.application import BASE_DIRECTORY
except ImportError:
    BASE_DIRECTORY = os.getcwd()


ROOT = BASE_DIRECTORY
APP = "/app"
APP_HTTP = "/app/http"
APP_PROVIDERS = "/app/providers"
APP_HTTP_CONTROLLERS = "/app/http/controllers"
APP_HTTP_MIDDLEWARE = "/app/http/middleware"
BOOTSTRAP = "/bootstrap"
BOOTSTRAP_CACHE = "/bootstrap/cache"
CONFIG = "/config"
DATABASES = "/databases"
DATABASES_MIGRATIONS = "/databases/migrations"
RESOURCES = "/resources"
RESOURCES_TEMPLATES = "/resources/templates"
RESOURCES_SNIPPETS = "/resources/snippets"
ROUTES = "/routes"
STORAGE = "/storage"
STORAGE_COMPILED = "/storage/compiled"
STORAGE_STATIC = "/storage/static"
STORAGE_UPLOADS = "/storage/uploads"
TESTS = "/tests"
