from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import CFG

mysql_cfg = CFG['dxs']
uri = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    mysql_cfg['user'], mysql_cfg['password'], mysql_cfg['host'], mysql_cfg['db_port'], mysql_cfg['db'],
)
engine = create_engine(uri, pool_recycle=mysql_cfg['pool_recycle'])
Session = sessionmaker(bind=engine)
