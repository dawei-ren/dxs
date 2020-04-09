from sqlalchemy import update, insert, delete, select
from sqlalchemy.sql import and_
from sqlalchemy import desc, text
import sqlalchemy as sa

from chat.libs.errors import DBError

from chat.dbs.models import MODELS
from chat.dbs import Session


def get_session():
    return Session()


def get_model(model):
    model = MODELS.get(model)
    return model


def insert_data(model, valuedict):
    """
    增加
    """
    if isinstance(valuedict, dict):
        query = insert(model).values(**valuedict)
        return query.execute()
    else:
        return -1


def update_data(model, wheredict, valuedict):
    """
    修改
    """
    condition = []
    if isinstance(wheredict, dict) and isinstance(valuedict, dict):
        for k, v in wheredict.items():
            condition.append(eval("{}.{}=='{}'".format(model.__name__, k, v)))

        query = update(model).where(*condition).values(**valuedict)

        return query.execute()

    else:
        return -1


def delete_data(model, wheredict):
    """
    删除
    """
    condition = []
    if isinstance(wheredict, dict):
        for k, v in wheredict.items():
            condition.append(eval("{}.{}=='{}'".format(model.__name__, k, v)))

        query = delete(model).where(*condition)
        return query.execute()

    else:
        return -1


def select_data(model, wheredict=None):
    """
    查询
    """
    condition = []
    if isinstance(wheredict, dict):
        for k, v in wheredict.items():
            condition.append(eval("{}.{}=='{}'".format(model.__name__, k, v)))

        query = select([model]).where(and_(*condition))

    else:
        query = select([model])

    query = query.execute()
    return [
        {k: v.strftime("%Y-%m-%d %H:%M:%S") if k == "created_time" or k == "updated_time" else v for k, v in q.items()}
        for q in query]


def save_obj(model, data):
    """
    保存数据
    :param model: 模型名称
    :param data: 数据dict
    """
    try:
        sess = get_session()
        m = get_model(model)
        val_data = {k: v for k, v in data.items() if k in m.column_names()}
        not_val_data = {k: v for k, v in data.items() if k not in m.column_names()}

        if model == 'user':
            obj = m(**val_data)
            obj.set_password(val_data.get('password'))
        else:
            obj = m(**val_data)
        sess.add(obj)
        sess.commit()
        return obj.to_dict()
    except sa.exc.IntegrityError as e:
        raise DBError("记录已存在!", 400)
    except Exception as e:
        raise DBError()
    finally:
        sess.close()


def save_many_obj(model, data):
    """
    保存数据
    :param model: 模型名称
    :param data: 数据dict
    :return: 保存的实体
    """
    try:
        sess = get_session()
        m = get_model(model)
        fields = m.column_names()
        val_data = []
        not_val_data = []
        for d in data:
            val_data.append({k: v for k, v in d.items() if k in fields})
            tmp_not_val = {k: v for k, v in d.items() if k not in fields}
            if tmp_not_val:
                not_val_data.append(tmp_not_val)
        obj_list = []
        for obj in val_data:
            obj_list.append(m(**obj))
        sess.add_all(obj_list)
        sess.commit()
        return [obj.to_dict() for obj in obj_list]
    except sa.exc.IntegrityError as e:
        raise DBError("记录已存在!", 400)
    except Exception as e:
        raise DBError()
    finally:
        sess.close()


def update_single_obj(model, filters, data):
    """
    更新符合条件的第一条数据
    :param model: 模型名称
    :param filters: 查询条件列表
    :param data: 更新dict
    :return: 更新后实体
    """
    try:
        sess = get_session()
        m = get_model(model)
        val_data = {k: v for k, v in data.items() if k in m.column_names()}
        not_val_data = {k: v for k, v in data.items() if k not in m.column_names()}
        query = sess.query(m)
        if filters:
            for f in filters:
                query = query.filter(text(f))
        obj = query.first()
        if obj:
            for k, v in val_data.items():
                setattr(obj, k, v)
            sess.add(obj)
            sess.commit()
            return obj.to_dict()
        else:
            raise DBError(msg='记录不存在', code=400)
    except sa.exc.IntegrityError as e:
        raise DBError("记录已存在!", 400)
    except DBError as e:
        raise e
    except Exception as e:
        raise DBError()
    finally:
        sess.close()


def update_all_obj(model, filters, data):
    """
    更新符合条件的所有数据
    :param model: 模型名称
    :param filters: 查询条件列表
    :param data: 更新dict
    :return: 更新的记录条数
    """
    try:
        sess = get_session()
        m = get_model(model)
        val_data = {k: v for k, v in data.items() if k in m.column_names()}
        not_val_data = {k: v for k, v in data.items() if k not in m.column_names()}
        query = sess.query(m)
        if filters:
            for f in filters:
                query = query.filter(text(f))
        obj = query.all()
        upd_cnt = 0
        if obj:
            for o in obj:
                for k, v in val_data.items():
                    setattr(o, k, v)
                sess.add(o)
                upd_cnt += 1
            sess.commit()
        return upd_cnt
    except Exception as e:
        raise
    finally:
        sess.close()


def del_obj(model, filters=None):
    """
    删除数据
    :param model: 模型名称
    :param filters: 查询条件列表
    :return: 删除记录数据
    """
    try:
        sess = get_session()
        m = get_model(model)
        query = sess.query(m)
        if filters:
            for f in filters:
                query = query.filter(text(f))
        obj = query.all()
        del_cnt = 0
        if obj:
            for o in obj:
                sess.delete(o)
                del_cnt += 1
            sess.commit()
            return del_cnt
        else:
            raise DBError(msg='记录不存在', code=400)
    except DBError as e:
        raise e
    except Exception as e:
        raise DBError()
    finally:
        sess.close()


def get_all_obj(model, filters=None,sort=None, limit=None):
    """
    创建操作的时候，获取的数据中的全部数据，如果之前在数据中 就做更新操作
    :param model: 
    :param filters: 
    :param sort: 
    :param limit: 
    :return: 
    """
    try:
        sort_by_dict = {
            'desc': sa.desc,
            'asc': sa.asc
        }
        sess = get_session()
        m = get_model(model)
        query = sess.query(m)
        if filters:
            for f in filters:
                query = query.filter(text(f))
        totalCount = query.count()
        if sort:
            for s in sort:
                field = s['field']
                order = sort_by_dict.get(s['order'], '')
                query = query.order_by(order(field))
        if limit:
            offset = limit['offset']
            count = limit['count']
            query = query.offset(offset).limit(count)
        if totalCount:
            data = [x.to_dict() for x in query.all()]
        else:
            data = []
        return totalCount, data
    except Exception as e:
        raise DBError()
    finally:
        sess.close()


def get_obj(model, filters=None, sort=None, limit=None, all=False):
    """
    按条件查询数据
    :param model: 模型名称
    :param filters: 查询条件列表
    :param sort: 排序字典列表
    :param limit: offset limit字典
    :return: 记录数，记录列表
    """
    # try:
    sort_by_dict = {
        'desc': sa.desc,
        'asc': sa.asc
    }
    sess = get_session()
    m = get_model(model)
    query = sess.query(m)

    if filters:
        for f in filters:
            query = query.filter(text(f))

    if all == False:
        if 'deleted' in m.column_names():
            query = query.filter(text('deleted=0'))
    totalCount = query.count()
    if sort:
        for s in sort:
            field = s['field']
            order = sort_by_dict.get(s['order'], '')
            query = query.order_by(order(field))

    if limit:
        offset = limit['offset']
        count = limit['count']
        query = query.offset(offset).limit(count)

    if totalCount:
        data = [x.to_dict() for x in query.all()]
    else:
        data = []
    return totalCount, data
    # except Exception as e:
    #     raise DBError()
    # finally:
    #     sess.close()


if __name__ == '__main__':
    pass
