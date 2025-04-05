import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# ----------------------------
# 1. Define Balanced Transitions
# ----------------------------
balanced_transitions = {
    (1, 1, 3): 25000,  # Node 1: 1 → 3 (majority)
    (1, 1, 2): 12000,  # Node 1: 1 → 2 (slightly increased)

    (1, 3, 7): 27000,  # Node 3: 1 → 3 → 7
    (4, 3, 4): 12000,  # Node 3: 4 → 3 → 4

    (3, 7, 6): 35000,  # 🚀 Increased! Node 7: 3 → 7 → 6 (boosted count)
    (3, 7, 8): 12000   # Node 7: 3 → 7 → 8
}

# Additional variety transitions
additional_transitions = {
    (2, 1, 5): 1000,   
    (4, 3, 8): 1000    
}

# ----------------------------
# 2. Define Direction Mapping
# ----------------------------
direction_mapping = {
    (1, 1, 3): "East",
    (1, 1, 2): "West",
    (1, 3, 7): "South",
    (4, 3, 4): "North",
    (3, 7, 6): "East",
    (3, 7, 8): "West",
    (2, 1, 5): "Southeast",
    (4, 3, 8): "Northeast"
}

possible_directions = ["North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest"]

# ----------------------------
# 3. Generate Balanced Transitions
# ----------------------------
def generate_transitions(prev_node, current_node, next_node, count, start_time):
    time_increment = timedelta(seconds=5)
    current_time = start_time
    data = []
    
    for _ in range(count):
        # More realistic speed distribution (Normal dist: Mean 50, StdDev 10, clipped to [20, 80])
        speed = max(20, min(80, np.random.normal(50, 10)))

        # Assign direction dynamically if not in mapping
        direction = direction_mapping.get((prev_node, current_node, next_node), random.choice(possible_directions))

        data.append([
            current_time.strftime("%H:%M:%S"),
            prev_node,
            current_node,
            next_node,
            direction,
            round(speed, 1)  # Round to 1 decimal place
        ])
        current_time += time_increment
    return data, current_time

# ----------------------------
# 4. Create the Balanced Dataset
# ----------------------------
dataset = []
base_time = datetime.strptime("08:00:00", "%H:%M:%S")

# Generate balanced transitions
for key, count in balanced_transitions.items():
    prev_node, current_node, next_node = key
    data_batch, base_time = generate_transitions(prev_node, current_node, next_node, count, base_time)
    dataset.extend(data_batch)

# Generate additional transitions
for key, count in additional_transitions.items():
    prev_node, current_node, next_node = key
    data_batch, base_time = generate_transitions(prev_node, current_node, next_node, count, base_time)
    dataset.extend(data_batch)

# ----------------------------
# 5. Save to CSV
# ----------------------------
df = pd.DataFrame(dataset, columns=["Time", "Previous Node", "Current Node", "Predicted Next Node", "Direction", "Speed (km/h)"])
dataset_path = "balanced_route_prediction_dataset.csv"
df.to_csv(dataset_path, index=False)
print(f"✅ Balanced dataset generated with {len(df)} records and saved as '{dataset_path}'.")
