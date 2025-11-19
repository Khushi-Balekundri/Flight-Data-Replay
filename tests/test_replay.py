import pandas as pd
import numpy as np
from src.replay import FDRFrame, generate_replay_frames


def make_dummy_df():
    """Tiny dataset for testing replay pipeline."""
    return pd.DataFrame({
        "Time": [0.0, 1.0, 2.0],
        "Longitude": [10.0, 11.0, 12.0],
        "Latitude": [20.0, 21.0, 22.0],
        "Altitude": [100.0, 110.0, 120.0],
        "Roll (deg)": [0.0, 1.0, 2.0],
        "Pitch (deg)": [5.0, 6.0, 7.0],
        "Yaw (deg)": [10.0, 11.0, 12.0],
    })


def test_generate_fdr_frames_count():
    """Test that generate_fdr_frames produces correct number of frames."""
    df = make_dummy_df()
    frames = list(generate_replay_frames(df))
    assert len(frames) == 3, f"Expected 3 frames, got {len(frames)}"
    print("[OK] Frame count correct")


def test_generate_fdr_frames_type():
    """Test that frames are FDRFrame instances."""
    df = make_dummy_df()
    frames = list(generate_replay_frames(df))
    assert all(isinstance(f, FDRFrame) for f in frames), "Not all frames are FDRFrame instances"
    print("[OK] Frame types correct")


def test_generate_fdr_frames_values():
    """Test that frames have correct values."""
    df = make_dummy_df()
    frames = list(generate_replay_frames(df))
    
    # Test first frame
    f0 = frames[0]
    assert f0.lat == 20.0, f"Expected lat=20.0, got {f0.lat}"
    assert f0.lon == 10.0, f"Expected lon=10.0, got {f0.lon}"
    assert f0.alt == 100.0, f"Expected alt=100.0, got {f0.alt}"
    assert f0.roll == 0.0, f"Expected roll=0.0, got {f0.roll}"
    assert f0.pitch == 5.0, f"Expected pitch=5.0, got {f0.pitch}"
    assert f0.yaw == 10.0, f"Expected yaw=10.0, got {f0.yaw}"
    
    # Test all frames
    expected = [
        (20.0, 10.0, 100.0, 0.0, 5.0, 10.0),
        (21.0, 11.0, 110.0, 1.0, 6.0, 11.0),
        (22.0, 12.0, 120.0, 2.0, 7.0, 12.0),
    ]
    
    for i, (frame, (lat, lon, alt, roll, pitch, yaw)) in enumerate(zip(frames, expected)):
        assert frame.lat == lat, f"Frame {i}: lat mismatch"
        assert frame.lon == lon, f"Frame {i}: lon mismatch"
        assert frame.alt == alt, f"Frame {i}: alt mismatch"
        assert frame.roll == roll, f"Frame {i}: roll mismatch"
        assert frame.pitch == pitch, f"Frame {i}: pitch mismatch"
        assert frame.yaw == yaw, f"Frame {i}: yaw mismatch"
    
    print("[OK] Frame values correct")


def test_generate_fdr_frames_empty():
    """Test that empty dataframe produces no frames."""
    empty_df = pd.DataFrame({
        "Time": [],
        "Longitude": [],
        "Latitude": [],
        "Altitude": [],
        "Roll (deg)": [],
        "Pitch (deg)": [],
        "Yaw (deg)": [],
    })
    
    frames = list(generate_replay_frames(empty_df))
    assert len(frames) == 0, f"Expected 0 frames for empty df, got {len(frames)}"
    print("[OK] Empty dataframe handled correctly")


def test_generate_fdr_frames_single_row():
    """Test single row dataframe."""
    df = pd.DataFrame({
        "Time": [0.0],
        "Longitude": [10.0],
        "Latitude": [20.0],
        "Altitude": [100.0],
        "Roll (deg)": [0.0],
        "Pitch (deg)": [5.0],
        "Yaw (deg)": [10.0],
    })
    
    frames = list(generate_replay_frames(df))
    assert len(frames) == 1, f"Expected 1 frame, got {len(frames)}"
    assert frames[0].lat == 20.0, "Single frame lat mismatch"
    print("[OK] Single row handled correctly")


def test_generate_fdr_frames_large_dataset():
    """Test performance with larger dataset."""
    n = 1000
    df = pd.DataFrame({
        "Time": np.arange(n, dtype=float),
        "Longitude": np.linspace(10, 20, n),
        "Latitude": np.linspace(30, 40, n),
        "Altitude": np.linspace(100, 200, n),
        "Roll (deg)": np.linspace(0, 10, n),
        "Pitch (deg)": np.linspace(0, 10, n),
        "Yaw (deg)": np.linspace(0, 360, n),
    })
    
    frames = list(generate_replay_frames(df))
    assert len(frames) == n, f"Expected {n} frames, got {len(frames)}"
    assert frames[0].lon == 10.0, "First frame lon mismatch"
    assert np.isclose(frames[-1].lon, 20.0), "Last frame lon mismatch"
    print(f"[OK] Large dataset ({n} rows) processed correctly")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        ("Frame Count", test_generate_fdr_frames_count),
        ("Frame Types", test_generate_fdr_frames_type),
        ("Frame Values", test_generate_fdr_frames_values),
        ("Empty DataFrame", test_generate_fdr_frames_empty),
        ("Single Row", test_generate_fdr_frames_single_row),
        ("Large Dataset", test_generate_fdr_frames_large_dataset),
    ]
    
    print("=" * 60)
    print("Running Replay Tests")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\n{name}:")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)