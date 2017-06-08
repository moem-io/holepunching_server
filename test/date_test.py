from sqlalchemy.dialects.mysql import TIMESTAMP
import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import Column


created_date = Column(
    TIMESTAMP,
    default=datetime.datetime.utcnow,
    server_default=text('CURRENT_TIMESTAMP')
)
