"""Bộ kiểm thử đơn vị (Unit tests) cho playlist_manager.py
"""

import unittest
from io import StringIO
from unittest.mock import patch
from playlist_manager import (
    la_stt_hop_le,
    nhap_stt,
    hien_thi_playlist,
    them_bai_hat,
    thay_doi_thu_tu,
    xoa_bai_hat
)

class TestPlaylistManager(unittest.TestCase):

    def test_la_stt_hop_le(self):
        # Hợp lệ
        self.assertTrue(la_stt_hop_le("1", 3))
        self.assertTrue(la_stt_hop_le("3", 3))
        
        # Không hợp lệ
        self.assertFalse(la_stt_hop_le("0", 3))
        self.assertFalse(la_stt_hop_le("4", 3))
        self.assertFalse(la_stt_hop_le("-1", 3))
        self.assertFalse(la_stt_hop_le("abc", 3))
        self.assertFalse(la_stt_hop_le("", 3))
        self.assertFalse(la_stt_hop_le(" 2 ", 3))  # isdigit() trả về False nếu có khoảng trắng

    @patch("builtins.input", side_effect=["0"])
    def test_nhap_stt_huy(self, mock_input):
        result = nhap_stt("Nhập", 3, cho_phep_huy=True)
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["99", "2"])
    def test_nhap_stt_sai_roi_dung(self, mock_input):
        result = nhap_stt("Nhập", 3)
        self.assertEqual(result, 2)

    @patch("builtins.input", side_effect=["Hello"])
    def test_them_bai_hat_thanh_cong(self, mock_input):
        playlist = ["A", "B"]
        them_bai_hat(playlist)
        self.assertIn("Hello", playlist)
        self.assertEqual(len(playlist), 3)

    @patch("builtins.input", side_effect=[""])
    def test_them_bai_hat_rong_huy(self, mock_input):
        playlist = ["A", "B"]
        them_bai_hat(playlist)
        self.assertEqual(len(playlist), 2)

    @patch("builtins.input", side_effect=["1", "3"])
    def test_thay_doi_thu_tu(self, mock_input):
        playlist = ["Bài 1", "Bài 2", "Bài 3"]
        thay_doi_thu_tu(playlist)
        # Chuyển "Bài 1" (vị trí 1) sang vị trí 3
        # Thứ tự mong muốn: ["Bài 2", "Bài 3", "Bài 1"]
        self.assertEqual(playlist, ["Bài 2", "Bài 3", "Bài 1"])

    @patch("builtins.input", side_effect=["2", "y"])
    def test_xoa_bai_hat(self, mock_input):
        playlist = ["Bài 1", "Bài 2", "Bài 3"]
        xoa_bai_hat(playlist)
        self.assertEqual(playlist, ["Bài 1", "Bài 3"])

if __name__ == "__main__":
    unittest.main()
