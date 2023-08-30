from sqlalchemy import Column, INT, create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker


class Base(DeclarativeBase):
    id = Column(INT, primary_key=True)

    engine = create_engine(url='postgresql://blog:blog@0.0.0.0:5432/blog')
    session = sessionmaker(bind=engine)

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

    def update_from_attributes(self, obj) -> None:
        for k, v in obj.__dict__.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)
