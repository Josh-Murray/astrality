"""Tests for astrality.actions.CopyAction."""

from pathlib import Path

from astrality.actions import CopyAction


def test_copy_action_using_all_parameters(tmpdir):
    """All three parameters should be respected."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()

    target = Path(tmpdir) / 'target'
    target.mkdir()

    file1 = temp_dir / 'file1'
    file1.write_text('file1 content')

    file2 = temp_dir / 'file2'
    file2.write_text('file2 content')

    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()

    file3 = temp_dir / 'recursive' / 'file3'
    file3.write_text('file3 content')

    copy_options = {
        'content': str(temp_dir),
        'target': str(target),
        'include': r'file(\d)',
    }
    copy_action = CopyAction(
        options=copy_options,
        directory=temp_dir,
        replacer=lambda x: x,
        context_store={},
    )
    copy_action.execute()

    assert (target / '1').read_text() == file1.read_text()
    assert (target / '2').read_text() == file2.read_text()
    assert (target / 'recursive' / '3').read_text() == file3.read_text()


def test_copying_without_renaming(tmpdir):
    """When include is not given, keep copy name."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()

    target = Path(tmpdir) / 'target'
    target.mkdir()

    file1 = temp_dir / 'file1'
    file1.touch()

    file2 = temp_dir / 'file2'
    file2.touch()

    recursive_dir = temp_dir / 'recursive'
    recursive_dir.mkdir()

    file3 = temp_dir / 'recursive' / 'file3'
    file3.touch()

    copy_options = {
        'content': str(temp_dir),
        'target': str(target),
    }
    copy_action = CopyAction(
        options=copy_options,
        directory=temp_dir,
        replacer=lambda x: x,
        context_store={},
    )
    copy_action.execute()

    assert (target / 'file1').read_text() == file1.read_text()
    assert (target / 'file2').read_text() == file2.read_text()
    assert (target / 'recursive' / 'file3').read_text() == file3.read_text()


def test_copying_file_to_directory(tmpdir):
    """If copying from directory to file, place file in directory."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()

    target = Path(tmpdir) / 'target'
    target.mkdir()

    file1 = temp_dir / 'file1'
    file1.touch()

    copy_options = {
        'content': str(file1),
        'target': str(target),
        'include': r'file1',
    }
    copy_action = CopyAction(
        options=copy_options,
        directory=temp_dir,
        replacer=lambda x: x,
        context_store={},
    )
    copy_action.execute()

    assert (target / 'file1').read_text() == file1.read_text()


def test_setting_permissions_on_target_copy(tmpdir):
    """If permissions is provided, use it for the target."""
    temp_dir = Path(tmpdir) / 'content'
    temp_dir.mkdir()

    target = Path(tmpdir) / 'target'
    target.mkdir()

    file1 = temp_dir / 'file1'
    file1.touch()
    file1.chmod(0o770)

    copy_options = {
        'content': str(file1),
        'target': str(target),
        'include': r'file1',
        'permissions': '777',
    }
    copy_action = CopyAction(
        options=copy_options,
        directory=temp_dir,
        replacer=lambda x: x,
        context_store={},
    )
    copy_action.execute()

    assert ((target / 'file1').stat().st_mode & 0o000777) == 0o777
