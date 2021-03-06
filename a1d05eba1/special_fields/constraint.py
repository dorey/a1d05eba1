from ..utils import kassertfrozen
from ..utils.kfrozendict import kfrozendict
from ..utils.kfrozendict import assertfrozen
from ..fields import TranslatedVal, RawValue


class ConstraintVal:
    '''
    Because a row's "constraint_message" is only valid if there is also a
    "constraint", then the two logically should be stored together and validated
    together.

    A constraint looks like one of these structures:

    - string: '${age} > 0'
      message:
        tx0:
          string: "age must be greater than 0"

    # or

    - compile: ["${age}", ">", 0]
      message:
        tx0:
          compile: ["Age must be greater than 0. This is invalid: ", {'$lookup': 'age'}]
    '''

    ROW_KEYS = {
        # by schema
        '1': ['constraint', 'constraint_message'],
        '2': ['constraint'],
    }
    EXPORT_KEY = 'constraint'


    @classmethod
    def in_row(kls, row, schema):
        return 'constraint' in row

    @classmethod
    def pull_from_row(kls, row, content):
        schema = content.schema_version

        if 'constraint' not in row:
            return
        if schema == '1':
            constraint_data = {
                'string': row.get('constraint'),
            }
            constraint_val = kls(content, constraint_data)

            cmessage = row.get('constraint_message', None)
            if 'constraint_message' in row:
                constraint_val.set_message(cmessage)
            yield constraint_val
        elif schema == '2':
            constraint = row.get('constraint')
            (constraint, message) = constraint.popout('message')

            constraint_val = ConstraintVal(content, row.get('constraint'))
            if message:
                constraint_val.set_message(message)
            yield constraint_val


    def __init__(self, content, val):
        self.content = content
        self.key = 'constraint'
        self.val = val
        self._string = val.get('string')
        self.msg_txd = False

    def set_message(self, message):
        self.msg_txd = ConstraintMessage(self.content, message)

    def dict_key_vals_old(self, renames=None):
        yield ('constraint', self._string,)

        if self.msg_txd:
            for (k, val) in self.msg_txd.dict_key_vals_old(renames=renames):
                yield ('constraint_message', val,)

    @kassertfrozen
    def dict_key_vals_new(self, renames=None):
        val = kfrozendict(string=self.val.get('string'))
        if self.msg_txd:
            message = self.msg_txd.dict_key_vals_new()[1]
            val = val.copy(message=message)
        return ('constraint', val)


class ConstraintMessage(TranslatedVal):
    def __init__(self, content, message):
        self.content = content
        self.key = 'constraint_message'
        self.load(message)

    def load_from_old_vals(self, txvals):
        _data = {}
        if isinstance(txvals, str):
            raise NotImplementedError('Values should not be strings'
                                      ' at this stage')
        for (ii, tx) in enumerate(self.content.txs):
            anchor = tx.anchor
            value = txvals[ii]
            _data[anchor] = RawValue(self, value)
        self._val = _data

    def load_from_new_vals(self, message):
        _data = {}
        for (tx, string) in message.items():
            _data[tx] = RawValue(self, string)
        self._val = _data

    @kassertfrozen
    def dict_key_vals_new(self):
        vals = {}
        _vals = dict(self._val)
        for anchor in self.content.txs.anchors:
            vals[anchor] = _vals[anchor].to_dict()
            assertfrozen(vals[anchor])
        return (self.key, kfrozendict(vals))

    def dict_key_vals_old(self, renames=None):
        _vals = dict(self._val)
        vals = ()
        for tx in self.content.txs:
            vals = vals + (
                _vals[tx.anchor].to_string(),
            )
        key = 'constraint_message'
        yield (key, vals)
