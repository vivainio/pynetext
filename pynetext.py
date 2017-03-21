import clr

from System import Type
from System.Reflection import BindingFlags

def _create_dict(d):
    return dict((e.Key, to_python_object(e.Value)) for e in d)

def _create_list(ent):
    return list(to_python_object(e) for e in ent)

def _create_kv(ent):
    return {to_python_object(ent.Key): to_python_object(ent.Value)}

def _create_set(ent):
    return set(to_python_object(e) for e in ent)

def dump_type(o):
    """ Dumps some summary info for debugging purposes """
    typ = o.GetType()
    print "Type: %s %s " % (typ.Name, typ.FullName)
    print "Interfaces:", [intf.Name for intf in typ.GetInterfaces()]


LOOKUP_CONVERTERS = {
    'HashSet`1': _create_set,
    'KeyValuePair`2': _create_kv,
    'Hashtable': _create_dict,
    'Dictionary`2': _create_dict,
    'List`1': _create_list
}


ENUMERABLE = Type.GetType("System.Collections.IEnumerable")


def to_python_object(obj):
    """ convert (possibly) CLR object to native Python equivalent """
    try:
        typ = obj.GetType()
    except AttributeError:
        # handles all python types
        return obj

    converter = LOOKUP_CONVERTERS.get(typ.Name)
    if converter:
        return converter(obj)

    if ENUMERABLE.IsAssignableFrom(typ):
        return _create_list(obj)

    print "no conv", typ, typ.FullName
    return obj

def get_clr_type(typ):
    """ simulate typeof(T) or GetClrType from IronPython.

    Horrible hack, redo.

    See https://github.com/pythonnet/pythonnet/issues/432
    """
    name = typ.__module__ + "." + typ.__name__
    return Type.GetType(name)


class Reflect(object):
    """ Reflect on a type """
    def __init__(self, typ):
        self.typ = get_clr_type(typ)

    def methods(self):
        """ public methods """
        return self.typ.GetMethods(
            BindingFlags.Instance |
            BindingFlags.Static | BindingFlags.Public)



