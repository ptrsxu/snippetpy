"""
A colleciton of snippet for database/persistence technology.

Normally there are a few ways to deal with data persistence:

  - file. (Mostly with special format such as json, xml, etc.)
  - marshal. (Serialize basic python types such as int/str/tuple/list/dict
    etc. User defined classes and their instances cannot be serialized by
    marshal. It's fast.)
  - pickle/cPickle. (It can dump general objects including user defined
    classes/instances. We can define the __getstate__/__setstate__ methods
    of our classes to specify the dump/load operations by pickle. It's
    fast but still slower than marshal.)
  - shelve. (dict with persistence.)
  - database.

"""
