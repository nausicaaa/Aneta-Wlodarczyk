import sqlalchemy


metadata = sqlalchemy.MetaData()

urls = sqlalchemy.Table(
    'urls',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('url', sqlalchemy.String()),
    sqlalchemy.Column('interval', sqlalchemy.Integer()),
    sqlalchemy.Column('response', sqlalchemy.String()),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime()),
)
