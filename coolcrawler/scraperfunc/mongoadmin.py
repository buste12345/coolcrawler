# myapp/mongoadmin.py

# Import the MongoAdmin base class
from mongonaut.sites import MongoAdmin

# Import your custom models
from scraperfunc.models import googlespider

# Instantiate the MongoAdmin class
# Then attach the mongoadmin to your model
googlespider.mongoadmin = MongoAdmin()