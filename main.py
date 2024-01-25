from application.application import main as application
import click


animation_speed = 0.10
background_animation_speed = 0.5
transition_speed = 0.05


@click.command()
@click.option("-a", "--animation-speed", default=0.1, help="")
@click.option("-b", "--background-animation-speed", default=0.5, help="")
@click.option("-t", "--transition-speed", default=0.05, help="")
def main(animation_speed, background_animation_speed, transition_speed):
    application(animation_speed, background_animation_speed, transition_speed)


if __name__ == "__main__":
    main()
