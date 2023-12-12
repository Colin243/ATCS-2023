class FSM:
    def __init__(self, initial_state):
        # Dictionary (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        if next_state is not None:
            self.state_transitions[(input_symbol, state)] = (action, next_state)
        else:
            self.state_transitions[(input_symbol, state)] = (action, state)

    def get_transition(self, input_symbol, state):
        return self.state_transitions[(input_symbol, state)]

    def process(self, input_symbol):
        update = self.get_transition(input_symbol, self.current_state)
        if update[0] is not None:
            update[0]()
        self.current_state = update[1]
