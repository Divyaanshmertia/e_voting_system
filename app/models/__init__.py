# in app/models/__init__.py


from .User import User
from .Candidate import Candidate
from .Vote import Vote
from .UserImage import UserImage

# The import statements above ensure that these classes are recognized
# by SQLAlchemy when the application starts. This is particularly important
# for functionality like creating database tables and handling migrations.
