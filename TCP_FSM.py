'''
Problem: https://www.codewars.com/kata/54acc128329e634e9a000362/javascript
'''

class FSMachine():
    
    # define states as class attributes inside the FSMachine class
    CLOSED = 'CLOSED'
    LISTEN = 'LISTEN'
    SYN_SENT = 'SYN_SENT'
    SYN_RCVD = 'SYN_RCVD'
    ESTABLISHED = 'ESTABLISHED'
    CLOSE_WAIT = 'CLOSE_WAIT'
    LAST_ACK = 'LAST_ACK'
    FIN_WAIT_1 = 'FIN_WAIT_1'
    FIN_WAIT_2 = 'FIN_WAIT_2'
    CLOSING = 'CLOSING'
    TIME_WAIT = 'TIME_WAIT'

    def __init__(self):
        self.state = self.CLOSED
        # used dict of dict for faster and easier transition rules
        self.transitions = {
            self.CLOSED: {
                'APP_PASSIVE_OPEN': self.LISTEN,
                'APP_ACTIVE_OPEN': self.SYN_SENT
            },
            self.LISTEN: {
                'RCV_SYN': self.SYN_RCVD,
                'APP_SEND': self.SYN_SENT,
                'APP_CLOSE': self.CLOSED
            },
            self.SYN_RCVD: {
                'APP_CLOSE': self.FIN_WAIT_1,
                'RCV_ACK': self.ESTABLISHED
            },
            self.SYN_SENT: {
                'RCV_SYN': self.SYN_RCVD,
                'RCV_SYN_ACK': self.ESTABLISHED,
                'APP_CLOSE': self.CLOSED
            },
            self.ESTABLISHED: {
                'APP_CLOSE': self.FIN_WAIT_1,
                'RCV_FIN': self.CLOSE_WAIT
            },
            self.FIN_WAIT_1: {
                'RCV_FIN': self.CLOSING,
                'RCV_FIN_ACK': self.TIME_WAIT,
                'RCV_ACK': self.FIN_WAIT_2
            },
            self.CLOSING: {
                'RCV_ACK': self.TIME_WAIT
            },
            self.FIN_WAIT_2: {
                'RCV_FIN': self.TIME_WAIT
            },
            self.TIME_WAIT: {
                'APP_TIMEOUT': self.CLOSED
            },
            self.CLOSE_WAIT: {
                'APP_CLOSE': self.LAST_ACK
            },
            self.LAST_ACK: {
                'RCV_ACK': self.CLOSED
            }
        }
        
    def move_state(self, action:str):
        try:
            self.state = self.transitions[self.state][action]
            return self.state
        except:
            self.state = 'ERROR'
            return self.state
    
    def process_actions(self, actions=list):
        loop_index = 0
        while (loop_index < len(actions)):
            self.move_state(actions[loop_index])
            loop_index += 1
            if self.state == 'ERROR': # conditions to save processing time in case state hits ERROR before the end of actions list
                return self.state
        return self.state

    
def main(actions=list):
    fsm1 = FSMachine()
    return fsm1.process_actions(actions)

        
if __name__ == '__main__':
    # test case
    actions = ["APP_PASSIVE_OPEN", "APP_SEND", "RCV_SYN_ACK"]
    actions2 = ["APP_ACTIVE_OPEN"]
    actions3 = ["APP_ACTIVE_OPEN", "RCV_SYN_ACK", "APP_CLOSE", "RCV_FIN_ACK", "RCV_ACK"]
    print(main(actions))
    