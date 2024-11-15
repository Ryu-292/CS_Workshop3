import matplotlib.pyplot as plt
import csv

def read_player_data(csv_file):
    players = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            player_name = row[0]
            try:
                score = int(row[4])
            except (IndexError, ValueError):
                score = -1  # Assuming the score is in the 5th column (index 4)

            players.append((player_name, score))

    # Sort players by score in descending order
    players.sort(key=lambda x: x[1], reverse=True)
    return players

def generate_and_save_plot(players, save_path='leaderboard_graph.png'):
    # Plot the data using matplotlib and save it as an image
    player_names = [p[0] for p in players]
    scores = [p[1] if p[1] != -1 else 0 for p in players]

    plt.figure(figsize=(10, 5))
    plt.bar(player_names, scores, color='skyblue')
    plt.xlabel('Players')
    plt.ylabel('Scores')
    plt.title('All Players Scores')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(save_path, dpi=100)
    plt.close()

# Example usage if you want to generate the plot separately
if __name__ == "__main__":
    players = read_player_data('player_data.csv')
    generate_and_save_plot(players)
