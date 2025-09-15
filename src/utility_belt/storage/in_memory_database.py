class InMemoryDatabase:
    def __init__(self):
        self.data = {}  # Stores key -> {field -> [(timestamp, value), ...]}
        self.expiry_times = {}  # Stores key-expiration time pairs

    def _is_expired(self, key, timestamp):
        if key in self.expiry_times and self.expiry_times[key] <= int(timestamp):
            del self.data[key]
            del self.expiry_times[key]
            return True
        return False

    def set(self, key, field, value, timestamp):
        if not self._is_expired(key, timestamp):
            if key not in self.data:
                self.data[key] = {}
            if field not in self.data[key]:
                self.data[key][field] = []
            self.data[key][field].append((int(timestamp), value))
        return ""

    def get(self, key, field, timestamp):
        if key in self.data and not self._is_expired(key, timestamp):
            if field in self.data[key]:
                return self.data[key][field][-1][1]  # Return the most recent value
        return ""

    def compare_and_set(self, key, field, expected_value, new_value, timestamp):
        if key in self.data and not self._is_expired(key, timestamp) and field in self.data[key]:
            if self.data[key][field][-1][1] == expected_value:
                self.data[key][field].append((int(timestamp), new_value))
                return "true"
        return "false"

    def compare_and_delete(self, key, field, expected_value, timestamp):
        if key in self.data and not self._is_expired(key, timestamp) and field in self.data[key]:
            if self.data[key][field][-1][1] == expected_value:
                del self.data[key][field]
                if not self.data[key]:  # Clean up empty records to prevent memory bloat
                    del self.data[key]
                return "true"
        return "false"

    def look_back(self, key, field, past_timestamp):
        """Retrieve the value of a field at a specific past timestamp."""
        if key in self.data:
            if field in self.data[key]:
                values = self.data[key][field]
                # Find the most recent value before or at 'past_timestamp'
                for timestamp, value in reversed(values):
                    if timestamp <= int(past_timestamp):
                        return value
        return ""

# Instantiate the database and perform tests
db = InMemoryDatabase()

# Test sequence
test_queries = [
    ("SET", 1000, "user1", "age", "30"),
    ("SET", 1500, "user1", "age", "31"),
    ("LOOK_BACK", 1100, "user1", "age"),
    ("GET", 1600, "user1", "age"),
    ("COMPARE_AND_SET", 1700, "user1", "age", "31", "32"),
    ("GET", 1800, "user1", "age"),
    ("COMPARE_AND_DELETE", 1900, "user1", "age", "32"),
    ("GET", 2000, "user1", "age")
]

# Execute test queries and collect results
results = []
for query in test_queries:
    if query[0] == "SET":
        _, timestamp, key, field, value = query
        result = db.set(key, field, value, timestamp)
        results.append(result)
    elif query[0] == "LOOK_BACK":
        _, past_timestamp, key, field = query
        result = db.look_back(key, field, past_timestamp)
        results.append(result)
    elif query[0] == "GET":
        _, timestamp, key, field = query
        result = db.get(key, field, timestamp)
        results.append(result)
    elif query[0] == "COMPARE_AND_SET":
        _, timestamp, key, field, expected_value, new_value = query
        result = db.compare_and_set(key, field, expected_value, new_value, timestamp)
        results.append(result)
    elif query[0] == "COMPARE_AND_DELETE":
        _, timestamp, key, field, expected_value = query
        result = db.compare_and_delete(key, field, expected_value, timestamp)
        results.append(result)

print(results)
