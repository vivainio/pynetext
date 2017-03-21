import clr

from System import Environment
from System.Collections import IDictionary, ICollection
from System.Collections.Generic import Dictionary, KeyValuePair, HashSet, List

from System import Type, Func
from System.Linq import Enumerable


from pynetext import to_python_object, dump_type

def test_conv(o, typ):
    converted = to_python_object(o)
    if not isinstance(converted, typ):
        print "Expected", typ, "got", converted, "for:"
        dump_type(o)
        assert False
    return converted



def test():
    e = Environment.GetEnvironmentVariables()
    test_conv(e, dict)

    l = e.Values
    test_conv(l, list)

    d = Dictionary[str, int]()
    d['foo'] = 222
    converted = test_conv(d, dict)
    assert converted['foo'] == 222

    kv = KeyValuePair[str,str]("foo", "bar")
    converted = test_conv(kv, dict)
    assert "foo" in converted
    assert len(converted) == 1

    hs = HashSet[str]()
    hs.Add("setmember")
    converted = test_conv(hs, set)
    assert "setmember" in converted

    l = List[str]()
    l.Add("foo")
    l.Add("baz")
    converted = test_conv(l, list)
    assert 'foo' in converted

    f = Func[str, str](lambda s : 'hello' +s)
    en = Enumerable.Select[str, str](l,f)

    converted = test_conv(en, list)
    assert u'hellobaz' in converted

test()
