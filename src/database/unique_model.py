class UniqueMixin(object):
    """
    Add the as_unique() function to a database object, to get the existing instance if it already
    exists in the database, and otherwise create a new instance.

    Example: two datasets have the same License. Creating a new License() for both datasets will
    lead to having the same license twice in the database (or a unique-constraint-failed exception).
    Solution: use License.as_unique(session).

    Copied from https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObject
    """

    @classmethod
    def _unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def _unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, *arg, **kw):
        return _unique(session, cls, cls._unique_hash, cls._unique_filter, cls, arg, kw)


def _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw):
    cache = getattr(session, "_unique_cache", None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*arg, **kw))
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj
