from neural_neighbor.nn_style_transfer import neural_neighbor_style_transfer


def main():
    # To run this you have to cd into style_transfer and run python main.py
    neural_neighbor_style_transfer(
        content_path="./images/content/anneborg_256.jpg",
        style_path="./images/style/S4.jpg",
        output_path="./output.jpg",
        size=256,  # comment this line out if you have more than 6GB VRAM
    )


if __name__ == "__main__":
    main()
