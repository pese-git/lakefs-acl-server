import pytest

from app.db.session import engine
from app.models import Base


@pytest.fixture(autouse=True, scope="function")
def setup_db():
    # Перед каждым тестом сбрасываем и создаём таблицы заново
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
