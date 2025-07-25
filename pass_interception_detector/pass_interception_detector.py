class PassAndInterceptionDetector:
    def __init__(self):
        # No initialization parameters needed for now
        pass

    def detect_passes(self, ball_acquisition, player_assignment):
        """
        Detect passes between players of the same team.
        """
        passes = [0] * len(ball_acquisition)

        for frame in range(1, len(ball_acquisition)):
            prev_holder = ball_acquisition[frame - 1]
            current_holder = ball_acquisition[frame]

            # Ignore frames where ball possession is invalid or unchanged
            if prev_holder == -1 or current_holder == -1 or prev_holder == current_holder:
                continue

            # Get teams of previous and current ball holders
            prev_team = player_assignment[frame - 1].get(prev_holder, -1)
            current_team = player_assignment[frame].get(current_holder, -1)

            # Mark a pass only if both holders belong to the same valid team
            if prev_team != -1 and current_team != -1 and prev_team == current_team:
                passes[frame] = current_team

        return passes

    def detect_interceptions(self, ball_acquisition, player_assignment):
        """
        Detect interceptions where ball possession changes between players of different teams.
        """
        interceptions = [0] * len(ball_acquisition)

        prev_holder = -1
        prev_team = -1

        for frame in range(1, len(ball_acquisition)):
            current_holder = ball_acquisition[frame]
            current_team = player_assignment[frame].get(current_holder, -1)

            # Interception occurs if ball changes holder to a different team
            if (
                prev_holder != -1 and current_holder != -1 and current_holder != prev_holder and
                prev_team != -1 and current_team != -1 and current_team != prev_team
            ):
                interceptions[frame] = current_team

            # Update previous holder and team for next frame
            if current_holder != -1:
                prev_holder = current_holder
                prev_team = current_team

        return interceptions
