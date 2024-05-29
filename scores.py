def loadTopScores():
    try:
        with open("top_scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            return scores
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []


def saveTopScores(scores):
    with open("top_scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")
