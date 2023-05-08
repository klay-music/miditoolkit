from miditoolkit.midi.parser import _check_note_within_range
from miditoolkit.midi.containers import Note
from copy import deepcopy

import pytest


def assert_notes_equal(note1, note2):
    assert note1.velocity == note2.velocity
    assert note1.pitch == note2.pitch
    assert note1.start == note2.start
    assert note1.end == note2.end


@pytest.fixture
def start_tick():
    return 100


@pytest.fixture
def end_tick():
    return 200


@pytest.fixture
def velocity():
    return 100


@pytest.fixture
def pitch():
    return 60


@pytest.fixture
def note(start_tick, end_tick, velocity, pitch):
    return Note(
        velocity=velocity,
        pitch=pitch,
        start=start_tick,
        end=end_tick,
    )


def test__check_note_within_range_with_shift(
    note, start_tick, end_tick, velocity, pitch
):
    """Note is entirely within range"""
    orig_note = deepcopy(note)

    range_start_tick = note.start - 10
    range_end_tick = note.end + 10

    shift = True
    offset = start_tick - range_start_tick

    exp = Note(
        velocity=velocity,
        pitch=pitch,
        start=offset,
        end=offset + end_tick - start_tick,
    )

    got = _check_note_within_range(
        note=note,
        st=range_start_tick,
        ed=range_end_tick,
        shift=shift,
    )
    assert_notes_equal(got, exp)
    # note should be unchanged
    assert_notes_equal(note, orig_note)


def test__check_note_within_range_note_starts_before_range(
    note, end_tick, velocity, pitch
):
    """Note starts before range, ends within range"""
    orig_note = deepcopy(note)

    range_start_tick = note.start + 10
    range_end_tick = note.end + 10

    shift = True

    exp = Note(
        velocity=velocity,
        pitch=pitch,
        start=0,
        end=end_tick - range_start_tick,
    )

    got = _check_note_within_range(
        note=note,
        st=range_start_tick,
        ed=range_end_tick,
        shift=shift,
    )
    assert_notes_equal(got, exp)
    # note should be unchanged
    assert_notes_equal(note, orig_note)


def test__check_note_within_range_note_ends_after_range(
    note, start_tick, velocity, pitch
):
    """Note starts within range, ends after range"""
    orig_note = deepcopy(note)

    range_start_tick = note.start - 10
    range_end_tick = note.end - 10

    shift = True
    offset = start_tick - range_start_tick

    exp = Note(
        velocity=velocity,
        pitch=pitch,
        start=offset,
        end=range_end_tick - range_start_tick,
    )

    got = _check_note_within_range(
        note=note,
        st=range_start_tick,
        ed=range_end_tick,
        shift=shift,
    )
    assert_notes_equal(got, exp)
    # note should be unchanged
    assert_notes_equal(note, orig_note)


def test__check_note_within_range_note_starts_after_ends_after_range(note):
    """Note starts after range, ends after range"""
    orig_note = deepcopy(note)

    range_start_tick = note.start + 10
    range_end_tick = note.end - 10

    shift = True

    exp = None

    got = _check_note_within_range(
        note=note,
        st=10,
        ed=range_end_tick - range_start_tick,
        shift=shift,
    )
    assert got is exp
    # note should be unchanged
    assert_notes_equal(note, orig_note)


def test__check_note_within_range_note_contains_range(note, velocity, pitch):
    """Note starts before range and ends after range"""
    orig_note = deepcopy(note)

    range_start_tick = note.start + 10
    range_end_tick = note.end - 10

    shift = True

    exp = Note(
        velocity=velocity,
        pitch=pitch,
        start=0,
        end=range_end_tick - range_start_tick,
    )

    got = _check_note_within_range(
        note=note,
        st=range_start_tick,
        ed=range_end_tick,
        shift=shift,
    )
    assert_notes_equal(got, exp)
    # note should be unchanged
    assert_notes_equal(note, orig_note)


def test__check_note_within_range_false(note):
    for range_start_tick, range_end_tick in [
        (0, 50),  # range before note
        (300, 400),  # range after note
    ]:
        for shift in [True, False]:
            got = _check_note_within_range(
                note=note,
                st=range_start_tick,
                ed=range_end_tick,
                shift=shift,
            )
            assert (
                got is None
            ), f"Failed for range: ({range_start_tick}, {range_end_tick})"
