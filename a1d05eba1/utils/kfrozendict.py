from collections.abc import Mapping


class kfrozendict(Mapping):
    """
    pulled from pypi's `frozendict` library which
    itself seems to be inspired by https://stackoverflow.com/a/2704866

    this is an immutable wrapper around python dictionaries
    """
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self._hash = None

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def add(self, **kwargs):
        raise Exception('just use copy')
        # print('just use copy()')
        # alias for copy()
        return self.copy(**kwargs)

    def popout(self, key):
        val = None
        keyvals = []
        for (ikey, ival) in self.items():
            if ikey == key:
                val = ival
            else:
                keyvals.append(
                    (ikey, ival)
                )
        return (
            self.__class__(dict(keyvals)),
            val,
        )

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in self._dict.items():
                h ^= hash((key, value))
            self._hash = h
        return self._hash

    def copy_in(self, **kwargs):
        for (k, val) in kwargs.items():
            kwargs[k] = kfrozendict.freeze(val)
        return self.copy(**kwargs)

    @classmethod
    def unfreeze(kls, val):
        if isinstance(val, (kls, dict)):
            return dict([
                (ikey, kls.unfreeze(ival))
                for (ikey, ival) in val.items()
            ])
        elif isinstance(val, (list, tuple)):
            return list([
                kls.unfreeze(ival) for ival in val
            ])
        # elif isinstance(val, dict):
        #     import pdb; pdb.set_trace()
        else:
            return val

    @classmethod
    def freeze(kls, val):
        # print('kls', val)
        if isinstance(val, (kls, dict)):
            return kls([
                (ikey, kls.freeze(ival))
                for (ikey, ival) in val.items()
            ])
        elif isinstance(val, (list, tuple)):
            return tuple([
                kls.freeze(ival) for ival in val
            ])
        else:
            return val