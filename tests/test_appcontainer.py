"""SID contract regressions; these do not imply render/network isolation."""
from __future__ import annotations

import ctypes
import sys
import unittest
from pathlib import Path
from ctypes import wintypes
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

if sys.platform == "win32":
    from animtrain import appcontainer as ac


@unittest.skipUnless(sys.platform == "win32", "Windows SID API required")
class TestAppContainerSID(unittest.TestCase):
    def test_system_sid_is_valid_and_deterministic(self):
        sid = ac.appcontainer_sid()
        self.assertEqual(sid, ac.appcontainer_sid())
        self.assertTrue(ac._a32.IsValidSid(ctypes.create_string_buffer(sid)))
        derive = ctypes.WinDLL("userenv").DeriveAppContainerSidFromAppContainerName
        derive.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.LPVOID)]
        derive.restype = ctypes.c_long
        native = wintypes.LPVOID()
        self.assertEqual(derive(ac.APPCONTAINER_NAME, ctypes.byref(native)), 0)
        try:
            self.assertEqual(sid, ctypes.string_at(native, ac._a32.GetLengthSid(native)))
        finally:
            ac._a32.FreeSid(native)

    def test_hresult_zero_is_success_and_sid_is_freed(self):
        expected = ac.appcontainer_sid()
        memory = ctypes.create_string_buffer(expected)
        def derive(name, out):
            ctypes.cast(out, ctypes.POINTER(wintypes.LPVOID))[0] = ctypes.addressof(memory)
            return 0
        with mock.patch.object(ac._u32, "DeriveAppContainerSidFromAppContainerName", side_effect=derive), \
             mock.patch.object(ac._a32, "FreeSid") as release:
            self.assertEqual(ac.appcontainer_sid(), expected)
        release.assert_called_once()
        self.assertEqual(release.call_args.args[0].value, ctypes.addressof(memory))

    def test_failed_hresult_raises_without_fallback(self):
        with mock.patch.object(ac._u32, "DeriveAppContainerSidFromAppContainerName", return_value=-2147024809):
            with self.assertRaisesRegex(OSError, "HRESULT 0x80070057"):
                ac.appcontainer_sid()

    def test_success_without_sid_is_rejected(self):
        with mock.patch.object(ac._u32, "DeriveAppContainerSidFromAppContainerName", return_value=0):
            with self.assertRaisesRegex(OSError, "without a SID"):
                ac.appcontainer_sid()

    def test_profile_path_allocation_is_released(self):
        expected = ROOT / 'tests'
        memory = ctypes.create_unicode_buffer(str(expected))
        def lookup(sid, out):
            ctypes.cast(out, ctypes.POINTER(wintypes.LPWSTR))[0] = ctypes.cast(memory, wintypes.LPWSTR)
            return 0
        with mock.patch.object(ac._u32, 'GetAppContainerFolderPath', side_effect=lookup), \
             mock.patch.object(ac._ole32, 'CoTaskMemFree') as release:
            self.assertEqual(ac.appcontainer_profile_path(ac.appcontainer_sid()), expected)
        release.assert_called_once()

    def test_missing_profile_fails_before_mkdir_or_acl_change(self):
        with mock.patch.object(ac._u32, 'GetAppContainerFolderPath', return_value=-2147024894), \
             mock.patch.object(ac, 'grant_dir_access') as grant, \
             mock.patch.object(Path, 'mkdir') as mkdir:
            with self.assertRaisesRegex(OSError, 'profile unavailable.*0x80070002'):
                ac.run_appcontainer(['synthetic.exe'], cwd=Path('D:/synthetic-sandbox'),
                    env={}, allowed_dirs=[(Path('D:/synthetic-runtime'), False)])
        grant.assert_not_called()
        mkdir.assert_not_called()

    def test_success_without_profile_folder_is_rejected(self):
        with mock.patch.object(ac._u32, 'GetAppContainerFolderPath', return_value=0):
            with self.assertRaisesRegex(OSError, 'without a folder'):
                ac.appcontainer_profile_path(ac.appcontainer_sid())


if __name__ == "__main__":
    unittest.main()
