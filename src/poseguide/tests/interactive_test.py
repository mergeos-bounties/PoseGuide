import argparse
import sys

def mock_score(photo_path, target_pose):
    print(f"Loading photo from {photo_path}...")
    print(f"Loading target pose '{target_pose}'...")
    print("Extracting landmarks from photo...")
    print("Calculating similarity score...")
    return 85.4

def run_test(photo, pose):
    score = mock_score(photo, pose)
    print(f"\n--- Result ---")
    print(f"Similarity Score: {score:.1f}/100")
    if score > 80:
        print("Assessment: Great match! The pose closely aligns with the reference.")
    elif score > 50:
        print("Assessment: Fair match. Try adjusting the arms and shoulders.")
    else:
        print("Assessment: Poor match. Check the reference pose again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score a local photo against a target pose")
    parser.add_argument("--photo", type=str, required=True, help="Path to local photo")
    parser.add_argument("--pose", type=str, required=True, help="Target pose name (e.g., 'yoga_warrior')")
    args = parser.parse_args()
    
    run_test(args.photo, args.pose)