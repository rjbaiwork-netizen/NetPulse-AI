from app.plugins.mikrotik.routeros_api import _decode_length, _encode_length


def test_routeros_length_round_trip_boundaries() -> None:
    for value in (0, 1, 127, 128, 16383, 16384, 2097151, 2097152, 268435455, 268435456):
        assert _encode_length(value)


def test_word_length_small_values() -> None:
    assert _encode_length(0) == b"\\x00"
    assert _encode_length(127) == b"\\x7f"
    assert _encode_length(128) == b"\\x80\\x80"
