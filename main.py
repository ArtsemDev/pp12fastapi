from src.database import User


with User.session() as s:
    user = User(name='admin', email='admin@admin.com', password='qwerqwer')
    s.add(user)
    s.commit()