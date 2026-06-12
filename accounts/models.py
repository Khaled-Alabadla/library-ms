from django.db import models
import bcrypt


class UserManager(models.Manager):
    def create_user(self, username, email, password):
        """Create and return a `User` with a bcrypt-hashed password."""
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('Users must have an email address')

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = self.model(username=username, email=email, password=hashed)
        user.save()
        return user


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        """Verify password using bcrypt."""
        try:
            return bcrypt.checkpw(raw_password.encode(), self.password.encode())
        except Exception:
            return False

    def get_username(self):
        return self.username
