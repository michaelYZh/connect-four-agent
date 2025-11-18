"""
Four-in-a-row LLM arena Gradio app
"""

from arena.game import Game
from arena.board import RED, YELLOW
from arena.llm import LLM
import gradio as gr
from dotenv import load_dotenv


css = """
footer{display:none !important}
"""

js = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

ALL_MODEL_NAMES = LLM.all_model_names()


def message_html(game) -> str:
    """
    Return the message for the top of the UI
    """
    return f'<div style="text-align: center;font-size:18px">{game.board.message()}</div>'


def load_callback(red_llm, yellow_llm):
    """
    Callback called when the game is started. Create a new Game object for the state.
    """
    game = Game(red_llm, yellow_llm)
    enabled = gr.Button(interactive=True)
    message = message_html(game)
    return (
        game,
        game.board.svg(),
        message,
        "",
        "",
        enabled,
        enabled,
        enabled,
    )


def move_callback(game):
    """
    Callback called when the user clicks to do a single move.
    """
    game.move()
    message = message_html(game)
    if_active = gr.Button(interactive=game.board.is_active())
    return (
        game,
        game.board.svg(),
        message,
        game.thoughts(RED),
        game.thoughts(YELLOW),
        if_active,
        if_active,
    )


def run_callback(game):
    """
    Callback called when the user runs an entire game. Reset the board and run the game.
    Yield interim results so the UI updates.
    """
    enabled = gr.Button(interactive=True)
    disabled = gr.Button(interactive=False)
    game.reset()
    message = message_html(game)
    yield (
        game,
        game.board.svg(),
        message,
        game.thoughts(RED),
        game.thoughts(YELLOW),
        disabled,
        disabled,
        disabled,
    )
    while game.board.is_active():
        game.move()
        message = message_html(game)
        yield (
            game,
            game.board.svg(),
            message,
            game.thoughts(RED),
            game.thoughts(YELLOW),
            disabled,
            disabled,
            disabled,
        )
    yield (
        game,
        game.board.svg(),
        message,
        game.thoughts(RED),
        game.thoughts(YELLOW),
        disabled,
        disabled,
        enabled,
    )


def model_callback(player_name, game, new_model_name):
    """
    Callback when the user changes the model
    """
    player = game.players[player_name]
    player.switch_model(new_model_name)
    return game


def red_model_callback(game, new_model_name):
    """
    Callback when red model is changed
    """
    return model_callback(RED, game, new_model_name)


def yellow_model_callback(game, new_model_name):
    """
    Callback when yellow model is changed
    """
    return model_callback(YELLOW, game, new_model_name)


def player_section(name, default):
    """
    Create the left and right sections of the UI
    """
    with gr.Row():
        gr.HTML(f'<div style="text-align: center;font-size:18px">{name} Player</div>')
    with gr.Row():
        dropdown = gr.Dropdown(ALL_MODEL_NAMES, value=default, label="LLM", interactive=True)
    with gr.Row():
        gr.HTML('<div style="text-align: center;font-size:16px">Inner thoughts</div>')
    with gr.Row():
        thoughts = gr.HTML(label="Thoughts")
    return thoughts, dropdown


def make_display():
    """
    The Gradio UI to show the Game, with event handlers
    """
    with gr.Blocks(
        title="Connect Four Battle",
        css=css,
        js=js,
        theme=gr.themes.Default(primary_hue="sky"),
    ) as blocks:
        game = gr.State()

        with gr.Row():
            gr.HTML('<div style="text-align: center;font-size:24px">Connect 4 Agents</div>')
        with gr.Row():
            with gr.Column(scale=1):
                red_thoughts, red_dropdown = player_section("🔴 Red", ALL_MODEL_NAMES[0])
            with gr.Column(scale=2):
                with gr.Row():
                    message = gr.HTML('<div style="text-align: center;font-size:18px">The Board</div>')
                with gr.Row():
                    board_display = gr.HTML()
                with gr.Row():
                    with gr.Column(scale=1):
                        move_button = gr.Button("Next move")
                    with gr.Column(scale=1):
                        run_button = gr.Button("Run game", variant="primary")
                    with gr.Column(scale=1):
                        reset_button = gr.Button("Start Over", variant="stop")
            with gr.Column(scale=1):
                yellow_thoughts, yellow_dropdown = player_section("🟡 Yellow", ALL_MODEL_NAMES[1])

        blocks.load(
            load_callback,
            inputs=[red_dropdown, yellow_dropdown],
            outputs=[
                game,
                board_display,
                message,
                red_thoughts,
                yellow_thoughts,
                move_button,
                run_button,
                reset_button,
            ],
        )
        move_button.click(
            move_callback,
            inputs=[game],
            outputs=[
                game,
                board_display,
                message,
                red_thoughts,
                yellow_thoughts,
                move_button,
                run_button,
            ],
        )
        red_dropdown.change(red_model_callback, inputs=[game, red_dropdown], outputs=[game])
        yellow_dropdown.change(
            yellow_model_callback, inputs=[game, yellow_dropdown], outputs=[game]
        )
        run_button.click(
            run_callback,
            inputs=[game],
            outputs=[
                game,
                board_display,
                message,
                red_thoughts,
                yellow_thoughts,
                move_button,
                run_button,
                reset_button,
            ],
        )
        reset_button.click(
            load_callback,
            inputs=[red_dropdown, yellow_dropdown],
            outputs=[
                game,
                board_display,
                message,
                red_thoughts,
                yellow_thoughts,
                move_button,
                run_button,
                reset_button,
            ],
        )

    return blocks


if __name__ == "__main__":
    load_dotenv(override=True)
    app = make_display()
    app.launch(inbrowser=True)
