#!/usr/bin/env python3
"""
Example usage of Personal History v0.01
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import PersonalHistoryV001

def example_workflow():
    """Complete example workflow"""
    print("Personal History v0.01 - Example Workflow")
    print("=" * 60)
    
    # Step 1: Create identity
    print("\n1. Creating identity...")
    identity = PersonalHistoryV001.create_identity("William Acevedo")
    print(f"   Name: {identity.get('name')}")
    print(f"   Identity hash: {identity['identity_hash'][:16]}...")
    
    # Step 2: Create activities for a day
    print("\n2. Creating activities...")
    
    # Morning: Family breakfast
    breakfast = PersonalHistoryV001.create_activity(
        "family",
        {"activity": "breakfast", "meal": "pancakes", "with": ["wife", "son"]},
        45,  # 45 minutes
        shareable=True
    )
    
    # Late morning: Work
    work = PersonalHistoryV001.create_activity(
        "work",
        {"project": "personal_history", "task": "v0.01 implementation"},
        120,  # 2 hours
        shareable=True
    )
    
    # Afternoon: Exercise
    exercise = PersonalHistoryV001.create_activity(
        "exercise",
        {"activity": "running", "distance_km": 5.2},
        28,  # 28 minutes
        shareable=True
    )
    
    # Evening: Cooking
    cooking = PersonalHistoryV001.create_activity(
        "cooking",
        {"meal": "kotlet_schabowy", "for_people": 3},
        40,  # 40 minutes
        shareable=True
    )
    
    # Private activity (not shareable)
    private = PersonalHistoryV001.create_activity(
        "personal",
        {"activity": "doctor_appointment"},
        60,  # 1 hour
        shareable=False
    )
    
    print(f"   Created {5} activities")
    print(f"   Shareable: 4, Private: 1")
    
    # Step 3: Create day
    print("\n3. Creating day...")
    day = PersonalHistoryV001.create_day(
        date="2024-01-01",
        activities=[breakfast, work, exercise, cooking, private],
        note="New Year's Day - Family, work, exercise, and traditional dinner"
    )
    print(f"   Date: {day['date']}")
    print(f"   Activities: {len(day['activities'])}")
    print(f"   Day hash: {day['hash'][:16]}...")
    
    # Step 4: Create file
    print("\n4. Creating Personal History file...")
    ph_file = PersonalHistoryV001.create_file(identity, [day])
    print(f"   Version: {ph_file['version']}")
    print(f"   Timeline: {len(ph_file['timeline'])} days")
    
    # Step 5: Sign file
    print("\n5. Signing file...")
    signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
    ph_file["signature"] = signature
    print(f"   Signature: {signature[:32]}...")
    
    # Step 6: Save file
    print("\n6. Saving file...")
    output_file = "example_william_2024.ph.json"
    PersonalHistoryV001.save_file(ph_file, output_file)
    print(f"   Saved to: {output_file}")
    
    # Step 7: Load and verify
    print("\n7. Loading and verifying...")
    loaded_file = PersonalHistoryV001.load_file(output_file)
    print(f"   Loaded: {loaded_file['identity'].get('name', 'Unknown')}")
    
    # Verify signature
    is_valid = PersonalHistoryV001.verify_file(loaded_file, identity["public_key"])
    print(f"   Signature valid: {is_valid}")
    
    # Verify forward chain
    chain_valid = PersonalHistoryV001.verify_forward_chain(loaded_file)
    print(f"   Forward chain valid: {chain_valid}")
    
    # Step 8: Analyze time
    print("\n8. Analyzing time...")
    analysis = PersonalHistoryV001.analyze_time(loaded_file)
    print(f"   Total tracked: {analysis['total_tracked_hours']:.1f} hours")
    
    print(f"\n   Time by activity:")
    for activity_type, stats in analysis['activity_totals'].items():
        hours = stats['total_minutes'] / 60
        percentage = (stats['total_minutes'] / analysis['total_tracked_minutes']) * 100
        shareable_pct = (stats['shareable_count'] / stats['count']) * 100
        print(f"     {activity_type:12} {hours:5.1f}h ({percentage:.0f}%), "
              f"{shareable_pct:.0f}% shareable")
    
    # Step 9: Export shareable
    print("\n9. Exporting shareable activities...")
    shareable = PersonalHistoryV001.export_shareable(loaded_file)
    print(f"   Shareable days: {len(shareable)}")
    
    # Count shareable activities
    total_shareable = sum(len(day['activities']) for day in shareable)
    print(f"   Shareable activities: {total_shareable}")
    
    # Step 10: Demonstrate selective disclosure
    print("\n10. Demonstrating selective disclosure...")
    print(f"   In file: 'Work: 2 hours'")
    print(f"   Hidden: Exact start/end times")
    print(f"   Can reveal: 'Work: 2 hours (09:00-11:00)' if needed")
    
    print("\n" + "=" * 60)
    print("✅ Example workflow complete!")
    print(f"\nFile created: {output_file}")
    print("\nTry these commands:")
    print(f"  python3 -m cli verify {output_file}")
    print(f"  python3 -m cli analyze {output_file}")
    
    return output_file

def demonstrate_cli_equivalent():
    """Show equivalent CLI commands"""
    print("\n" + "=" * 60)
    print("Equivalent CLI Commands")
    print("=" * 60)
    
    print("\nTo achieve the same result with CLI:")
    print("""
# Initialize identity
ph init --name "William Acevedo"

# Add activities
ph add family --duration 45 --with-people "wife,son" --meal "pancakes"
ph add work --duration 120 --project "personal_history"
ph add exercise --duration 28 --distance 5.2
ph add cooking --duration 40 --meal "kotlet_schabowy" --for-people 3
ph add personal --duration 60 --private

# Check pending
ph pending

# Sync to history file
ph sync --yes

# Analyze
ph analyze ~/.personal_history/history.ph.json
""")

if __name__ == "__main__":
    try:
        example_workflow()
        demonstrate_cli_equivalent()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()