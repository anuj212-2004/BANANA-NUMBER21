import json

class Leaderboard:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_scores(self):
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, name, score, level):
        self.scores.append({"name": name, "score": score, "level": level})
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]  # Keep only top 10 scores
        self.save_scores()

    def is_high_score(self, score):
        return len(self.scores) < 10 or score > self.scores[-1]['score']

    def get_scores(self):
        return self.scores

if __name__ == "__main__":
    # Test the Leaderboard class
    leaderboard = Leaderboard()
    print("Leaderboard initialized")