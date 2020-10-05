"""Terminal capability builder patterns."""
# std imports
import re

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 requires 3rd party library (backport)
    from ordereddict import OrderedDict  # pylint: disable=import-error

__all__ = (
    'CAPABILITY_DATABASE',
    'CAPABILITIES_RAW_MIXIN',
    'CAPABILITIES_ADDITIVES',
    'CAPABILITIES_CAUSE_MOVEMENT',
)

CAPABILITY_DATABASE = OrderedDict((
    ('bell', ('bel', {})),
    ('carriage_return', ('cr', {})),
    ('change_scroll_region', ('csr', {'nparams': 2})),
    ('clear_all_tabs', ('tbc', {})),
    ('clear_screen', ('clear', {})),
    ('clr_bol', ('el1', {})),
    ('clr_eol', ('el', {})),
    ('clr_eos', ('clear_eos', {})),
    ('column_address', ('hpa', {'nparams': 1})),
    ('cursor_address', ('cup', {'nparams': 2, 'match_grouped': True})),
    ('cursor_down', ('cud1', {})),
    ('cursor_home', ('home', {})),
    ('cursor_invisible', ('civis', {})),
    ('cursor_left', ('cub1', {})),
    ('cursor_normal', ('cnorm', {})),
    ('cursor_report', ('u6', {'nparams': 2, 'match_grouped': True})),
    ('cursor_right', ('cuf1', {})),
    ('cursor_up', ('cuu1', {})),
    ('cursor_visible', ('cvvis', {})),
    ('delete_character', ('dch1', {})),
    ('delete_line', ('dl1', {})),
    ('enter_blink_mode', ('blink', {})),
    ('enter_bold_mode', ('bold', {})),
    ('enter_dim_mode', ('dim', {})),
    ('enter_fullscreen', ('smcup', {})),
    ('enter_standout_mode', ('standout', {})),
    ('enter_superscript_mode', ('superscript', {})),
    ('enter_susimpleript_mode', ('susimpleript', {})),
    ('enter_underline_mode', ('underline', {})),
    ('erase_chars', ('ech', {'nparams': 1})),
    ('exit_alt_charset_mode', ('rmacs', {})),
    ('exit_am_mode', ('rmam', {})),
    ('exit_attribute_mode', ('sgr0', {})),
    ('exit_ca_mode', ('rmcup', {})),
    ('exit_fullscreen', ('rmcup', {})),
    ('exit_insert_mode', ('rmir', {})),
    ('exit_standout_mode', ('rmso', {})),
    ('exit_underline_mode', ('rmul', {})),
    ('flash_hook', ('hook', {})),
    ('flash_screen', ('flash', {})),
    ('insert_line', ('il1', {})),
    ('keypad_local', ('rmkx', {})),
    ('keypad_xmit', ('smkx', {})),
    ('meta_off', ('rmm', {})),
    ('meta_on', ('smm', {})),
    ('orig_pair', ('op', {})),
    ('parm_down_cursor', ('cud', {'nparams': 1})),
    ('parm_left_cursor', ('cub', {'nparams': 1, 'match_grouped': True})),
    ('parm_dch', ('dch', {'nparams': 1})),
    ('parm_delete_line', ('dl', {'nparams': 1})),
    ('parm_ich', ('ich', {'nparams': 1})),
    ('parm_index', ('indn', {'nparams': 1})),
    ('parm_insert_line', ('il', {'nparams': 1})),
    ('parm_right_cursor', ('cuf', {'nparams': 1, 'match_grouped': True})),
    ('parm_rindex', ('rin', {'nparams': 1})),
    ('parm_up_cursor', ('cuu', {'nparams': 1})),
    ('print_screen', ('mc0', {})),
    ('prtr_off', ('mc4', {})),
    ('prtr_on', ('mc5', {})),
    ('reset_1string', ('r1', {})),
    ('reset_2string', ('r2', {})),
    ('reset_3string', ('r3', {})),
    ('restore_cursor', ('rc', {})),
    ('row_address', ('vpa', {'nparams': 1})),
    ('save_cursor', ('sc', {})),
    ('scroll_forward', ('ind', {})),
    ('scroll_reverse', ('rev', {})),
    ('set0_des_seq', ('s0ds', {})),
    ('set1_des_seq', ('s1ds', {})),
    ('set2_des_seq', ('s2ds', {})),
    ('set3_des_seq', ('s3ds', {})),
    # this 'color' is deceiving, but often matching, and a better match
    # than set_a_attributes1 or set_a_foreground.
    ('color', ('_foreground_color', {'nparams': 1, 'match_any': True,
                                     'numeric': 1})),
    ('set_a_foreground', ('color', {'nparams': 1, 'match_any': True,
                                    'numeric': 1})),
    ('set_a_background', ('on_color', {'nparams': 1, 'match_any': True,
                                       'numeric': 1})),
    ('set_tab', ('hts', {})),
    ('tab', ('ht', {})),
    ('italic', ('sitm', {})),
    ('no_italic', ('sitm', {})),
))

CAPABILITIES_RAW_MIXIN = {
    'bell': re.escape('\a'),
    'carriage_return': re.escape('\r'),
    'cursor_left': re.escape('\b'),
    'cursor_report': re.escape('\x1b') + r'\[(\d+)\;(\d+)R',
    'cursor_right': re.escape('\x1b') + r'\[C',
    'exit_attribute_mode': re.escape('\x1b') + r'\[m',
    'parm_left_cursor': re.escape('\x1b') + r'\[(\d+)D',
    'parm_right_cursor': re.escape('\x1b') + r'\[(\d+)C',
    'restore_cursor': re.escape(r'\x1b\[u'),
    'save_cursor': re.escape(r'\x1b\[s'),
    'scroll_forward': re.escape('\n'),
    'set0_des_seq': re.escape('\x1b(B'),
    'tab': re.escape('\t'),
}
_ANY_NOTESC = '[^' + re.escape('\x1b') + ']*'

CAPABILITIES_ADDITIVES = {
    'link': ('link',
             re.escape('\x1b') + r'\]8;' + _ANY_NOTESC + ';' +
             _ANY_NOTESC + re.escape('\x1b') + '\\\\'),
    'color256': ('color', re.escape('\x1b') + r'\[38;5;\d+m'),
    'on_color256': ('on_color', re.escape('\x1b') + r'\[48;5;\d+m'),
    'color_rgb': ('color_rgb', re.escape('\x1b') + r'\[38;2;\d+;\d+;\d+m'),
    'on_color_rgb': ('on_color_rgb', re.escape('\x1b') + r'\[48;2;\d+;\d+;\d+m'),
    'shift_in': ('', re.escape('\x0f')),
    'shift_out': ('', re.escape('\x0e')),
    # sgr(...) outputs strangely, use the basic ANSI/EMCA-48 codes here.
    'set_a_attributes1': (
        'sgr', re.escape('\x1b') + r'\[\d+m'),
    'set_a_attributes2': (
        'sgr', re.escape('\x1b') + r'\[\d+\;\d+m'),
    'set_a_attributes3': (
        'sgr', re.escape('\x1b') + r'\[\d+\;\d+\;\d+m'),
    'set_a_attributes4': (
        'sgr', re.escape('\x1b') + r'\[\d+\;\d+\;\d+\;\d+m'),
    # this helps where xterm's sgr0 includes set0_des_seq, we'd
    # rather like to also match this immediate substring.
    'sgr0': ('sgr0', re.escape('\x1b') + r'\[m'),
    'backspace': ('', re.escape('\b')),
    'ascii_tab': ('', re.escape('\t')),
    'clr_eol': ('', re.escape('\x1b[K')),
    'clr_eol0': ('', re.escape('\x1b[0K')),
    'clr_bol': ('', re.escape('\x1b[1K')),
    'clr_eosK': ('', re.escape('\x1b[2K')),
}

CAPABILITIES_CAUSE_MOVEMENT = (
    'ascii_tab',
    'backspace',
    'carriage_return',
    'clear_screen',
    'column_address',
    'cursor_address',
    'cursor_down',
    'cursor_home',
    'cursor_left',
    'cursor_right',
    'cursor_up',
    'enter_fullscreen',
    'exit_fullscreen',
    'parm_down_cursor',
    'parm_left_cursor',
    'parm_right_cursor',
    'parm_up_cursor',
    'restore_cursor',
    'row_address',
    'scroll_forward',
    'tab',
)
