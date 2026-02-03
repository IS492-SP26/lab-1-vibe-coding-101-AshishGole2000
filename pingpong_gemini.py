import curses
import time

def main(stdscr):
    # Setup the screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100) # Refresh every 100ms

    sh, sw = stdscr.getmaxyx()
    WINNING_SCORE = 5

    # Game elements characters
    PADDLE_CHAR = '|'
    BALL_CHAR = 'O'

    # Create paddles and ball
    paddle_height = sh // 4
    paddle1_y = (sh - paddle_height) // 2
    paddle2_y = (sh - paddle_height) // 2
    paddle1_x = 5
    paddle2_x = sw - 6

    # Ball initial position and velocity
    ball_y, ball_x = sh // 2, sw // 2
    ball_vy, ball_vx = 1, 2 # velocity y, velocity x

    # Scores
    player1_score = 0
    player2_score = 0

    while True:
        # Get user input
        key = stdscr.getch()

        if key == ord('q'):
            break
        # Player 1 controls
        if key == ord('w') and paddle1_y > 0:
            paddle1_y -= 2
        if key == ord('s') and paddle1_y < sh - paddle_height:
            paddle1_y += 2
        # Player 2 controls
        if key == curses.KEY_UP and paddle2_y > 0:
            paddle2_y -= 2
        if key == curses.KEY_DOWN and paddle2_y < sh - paddle_height:
            paddle2_y += 2

        # Update ball position
        ball_y += ball_vy
        ball_x += ball_vx

        # Ball collision with top/bottom walls
        if ball_y <= 0 or ball_y >= sh - 1:
            ball_vy *= -1

        # Ball collision with paddles
        # Paddle 1
        if ball_x <= paddle1_x + 1 and paddle1_y <= ball_y < paddle1_y + paddle_height:
            ball_vx *= -1
        # Paddle 2
        if ball_x >= paddle2_x - 1 and paddle2_y <= ball_y < paddle2_y + paddle_height:
            ball_vx *= -1

        # Score points
        if ball_x < 0: # Player 2 scores
            player2_score += 1
            ball_y, ball_x = sh // 2, sw // 2
            ball_vx *= -1
        elif ball_x >= sw: # Player 1 scores
            player1_score += 1
            ball_y, ball_x = sh // 2, sw // 2
            ball_vx *= -1

        # Drawing
        stdscr.clear()

        # Draw scores
        score_text = f"Player 1: {player1_score} | Player 2: {player2_score}"
        stdscr.addstr(0, sw // 2 - len(score_text) // 2, score_text)

        # Draw paddles
        for i in range(paddle_height):
            stdscr.addch(paddle1_y + i, paddle1_x, PADDLE_CHAR)
            stdscr.addch(paddle2_y + i, paddle2_x, PADDLE_CHAR)

        # Draw ball
        stdscr.addch(ball_y, ball_x, BALL_CHAR)

        stdscr.refresh()

        # Check for winner
        if player1_score >= WINNING_SCORE or player2_score >= WINNING_SCORE:
            winner = "Player 1" if player1_score > player2_score else "Player 2"
            stdscr.nodelay(0) # Make getch() wait for input
            win_text = f"{winner} Wins! Press any key to exit."
            stdscr.addstr(sh // 2, sw // 2 - len(win_text) // 2, win_text)
            stdscr.refresh()
            stdscr.getch() # Wait for user to press a key
            break

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except curses.error as e:
        print(f"Error running curses application: {e}")
        print("Note: The 'curses' library is not supported on Windows by default.")
        print("Please run this game on a Linux or macOS system.")
