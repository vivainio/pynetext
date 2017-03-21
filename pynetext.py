import clr

from System import Type

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


def to_python_object(o):
    """ convert (possibly) CLR type to native Python equivalent """
    try:
        typ = o.GetType()
    except AttributeError:
        # handles all python types
        return o

    converter = LOOKUP_CONVERTERS.get(typ.Name)
    if converter:
        return converter(o)

    if ENUMERABLE.IsAssignableFrom(typ):
        return _create_list(o)

    print "no conv", typ, typ.FullName
    return o
