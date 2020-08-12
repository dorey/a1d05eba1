from .transformer import Transformer
from .transformer_list import TransformerList

from .anchors_when_needed import AnchorsFromNameOrRandom
from .kobo_rename_kuid_to_anchor import RenameKuidToAnchor
from .xlsform_aliases import XlsformRenames
from .xlsform_replace_truthy_strings import ReplaceTruthyStrings
from .xlsform_translations import XlsformTranslations

from .anchors_when_needed import DumpExtraneousAnchorsFW
from .choices_by_list_name import ChoicesToListFW
from .remove_translated_from_root import RemoveTranslatedFromRootFW
from .settings_and_choices_to_lists import SettingsChoicesToListFW

from .choices_by_list_name import ChoicesByListNameRW
from .remove_empty_rows import RemoveEmptiesRW
from .v1_renames import V1RenamesRW
from .xlsform_choices import XlsformChoicesRW
from .xlsform_metas_to_settings import MetasToSurveyRootRW
from .xlsform_translations import EnsureTranslationListRW
from .xlsform_unwrap_settings_from_list import UnwrapSettingsFromListRW
