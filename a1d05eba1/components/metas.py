import re

from .base_component import SurveyComponentWithDict

from ..utils.kfrozendict import kfrozendict
from ..utils import kassertfrozen
from ..special_fields.tags import _expand_tags


class Meta:
    def __init__(self, key, name=None, tags=None, **kwargs):
        if tags is None:
            tags = ()
        self.type = key
        self._kwargs = kwargs
        self.name = name or self.type
        self._name_is_specified = self.name != self.type
        self.tags = tags

    @kassertfrozen
    def to_key_values(self):
        if len(self.tags) == 0:
            if self._name_is_specified:
                return (self.type, self.name)
            else:
                return (self.type, True)
        val = kfrozendict({'tags': self.tags})
        if self._name_is_specified:
            val['name'] = self.name
        return (self.type, val)

    def _tag_strings_schema_1(self):
        out = {'tags': [], 'hxl': []}
        for tag in self.tags:
            mtch = re.match('^hxl:(.*)$', tag)
            if mtch:
                out['hxl'].append(mtch.group(1))
            else:
                out['tags'].append(tag)
        for (key, vals) in out.items():
            if len(vals) > 0:
                yield (key, ' '.join(vals))

    @kassertfrozen
    def to_dict_schema_1(self):
        out = kfrozendict(name=self.name,
                          type=self.type)
        if len(self.tags) == 0:
            return out
        tags = {}
        for (tag_key, tag_string) in self._tag_strings_schema_1():
            tags[tag_key] = tag_string
        return out.copy(**tags)

def load_meta(key, val):
    if val is True:
        return Meta(key=key, name=key, tags=())
    elif isinstance(val, str):
        return Meta(key=key, name=val)
    elif isinstance(val, (dict, kfrozendict)):
        return Meta(key=key, **val)
    raise ValueError('unhandled meta')

class Metas(SurveyComponentWithDict):
    _metas = ()

    def load(self):
        if self.content.schema_version == '1':
            _existing_metas = self.content.data.get('metas', {})
            metas = {}
            if _existing_metas:
                metas.update(_existing_metas)
            for row in self.content.data.get('survey', []):
                if row.get('type') in self.content.META_TYPES:
                    (row, _type) = kfrozendict(row).popout('type')
                    metas[_type] = kfrozendict(row)
            self._load_metas(metas)
        else:
            _metas = self.content.data.get('metas', {})
            self._load_metas(_metas)

    def _load_metas(self, metas):
        for (key, val) in metas.items():
            if isinstance(val, (dict, kfrozendict)):
                (val, _hxl) = val.popout('hxl', '')
                (val, _tags) = val.popout('tags', '')
                if _hxl or _tags:
                    val = val.copy(tags=_expand_tags(hxl=_hxl, tags=_tags))
            _meta = load_meta(key, val)
            if _meta:
                self._metas = self._metas + (_meta,)

    def items(self):
        return self._metas

    def items_schema_1(self):
        for meta in self._metas:
            row = meta.to_dict_schema_1()
            if row:
                yield row

    def any(self):
        return len(self._metas) > 0

    @kassertfrozen
    def to_frozen_dict(self, schema='2'):
        out = ()
        for meta in ordered_(self._metas):
            out = out + (
                meta.to_key_values(),
            )
        return kfrozendict(**dict(out))

def ordered_(metas):
    # exports (xml) depend on metas being in order.
    _by_type = dict([(mm.type, mm) for mm in metas])
    # an incomplete list of metas to pass tests
    _meta_type_order = ['start', 'end']

    # out_metas = []
    for mtype in _meta_type_order:
        if mtype in _by_type:
            yield _by_type.pop(mtype)
    for val in _by_type.values():
        yield val
