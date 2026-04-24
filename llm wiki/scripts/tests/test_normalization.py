import os
import shutil
import pytest
import sys

# Add lib directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))

from exporter import ObsidianExporter

@pytest.fixture
def temp_vault(tmp_path):
    vault = tmp_path / "test_vault"
    vault.mkdir()
    return str(vault)

def test_normalize_title():
    exporter = ObsidianExporter("dummy")
    
    # Test prefix stripping
    assert exporter.normalize_title("Re: SF Tennis") == "sf-tennis"
    assert exporter.normalize_title("Fwd: Re: Important Info") == "important-info"
    assert exporter.normalize_title("[SF TENNIS] Weekly Update") == "weekly-update"
    assert exporter.normalize_title("Re: [PROJECT] Let's go!") == "lets-go"
    
    # Test case and characters
    assert exporter.normalize_title("Hello World 123!") == "hello-world-123"
    assert exporter.normalize_title("Multiple   Spaces") == "multiple-spaces"
    assert exporter.normalize_title("Under_Scores") == "under-scores"
    assert exporter.normalize_title("---Hyphen-Check---") == "hyphen-check"

def test_de_duplication_identical_content(temp_vault):
    exporter = ObsidianExporter(temp_vault)
    data = {
        "title": "SF Tennis",
        "summary": "Weekly tennis info",
        "tags": ["tennis", "sf"],
        "markdown_content": "See you at the courts!",
        "key_points": ["Courts at 5pm", "Bring water"]
    }
    
    # First export
    path1 = exporter.export(data)
    assert os.path.exists(path1)
    assert os.path.basename(path1) == "sf-tennis.md"
    
    # Second export (identical content)
    path2 = exporter.export(data)
    assert path1 == path2
    assert len(os.listdir(temp_vault)) == 1

def test_de_duplication_different_content(temp_vault):
    exporter = ObsidianExporter(temp_vault)
    data1 = {
        "title": "SF Tennis",
        "summary": "Weekly tennis info",
        "tags": ["tennis"],
        "markdown_content": "Content 1",
        "key_points": ["Point 1"]
    }
    data2 = {
        "title": "SF Tennis",
        "summary": "DIFFERENT info",
        "tags": ["tennis"],
        "markdown_content": "Content 2",
        "key_points": ["Point 2"]
    }
    
    # First export
    path1 = exporter.export(data1)
    
    # Second export (different content)
    path2 = exporter.export(data2)
    assert path1 != path2
    assert os.path.basename(path2) == "sf-tennis-(1).md"
    assert len(os.listdir(temp_vault)) == 2
