import base64
import unittest

try:
    import cv2
    import numpy as np
    from backend.cv_backend import FACE_NAME_RE, _decode_face_image
except ImportError:
    cv2 = None
    np = None
    FACE_NAME_RE = None
    _decode_face_image = None


@unittest.skipUnless(cv2 is not None, "OpenCV backend dependencies are not installed")
class FaceInputTests(unittest.TestCase):
    def test_name_policy_rejects_traversal_and_accepts_safe_names(self):
        self.assertTrue(FACE_NAME_RE.fullmatch("Safety Operator_1"))
        self.assertFalse(FACE_NAME_RE.fullmatch("../operator"))
        self.assertFalse(FACE_NAME_RE.fullmatch(""))

    def test_decode_accepts_a_valid_jpeg(self):
        ok, encoded = cv2.imencode(".jpg", np.zeros((8, 8, 3), dtype=np.uint8))
        self.assertTrue(ok)
        decoded = _decode_face_image(base64.b64encode(encoded.tobytes()).decode())
        self.assertEqual(decoded.shape[:2], (8, 8))

    def test_decode_rejects_invalid_base64(self):
        with self.assertRaises(ValueError):
            _decode_face_image("not-valid-base64!")


if __name__ == "__main__":
    unittest.main()
