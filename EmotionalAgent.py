from EmotionDynamics import EmotionConverter, EmotionContainer
import sched
import random
import time


class EmotionalAgent:
    def __init__(self):
        self.myEmotionContainer = EmotionContainer()
        self.myEmotionConverter = EmotionConverter()
        self.myEmotionContainer.to_calculate()

        # output_thread = threading.Thread(target=self.calculate_emotions())
        # output_thread.daemon = True
        # output_thread.start()

        self._schedule = sched.scheduler(time.time, self.myEmotionContainer.get_dt())
        self._emoimp = 0

    def calculate_emotions(self):
        time.sleep(1)
        self.myEmotionContainer.to_calculate()
        self.myEmotionConverter.get_String(
            self.myEmotionConverter.convertToClassType(self.myEmotionContainer.to_get_emotion_list()))
        self._schedule = sched.scheduler(time.time, self.myEmotionContainer.get_dt())
        self._schedule.enter(self.calculate_emotions())

    def send_random_emoimpulse(self):
        self._emoimp = random.randrange[50] - 25
        print(self._emoimp)
        self.myEmotionContainer.to_emoimpulse(self._emoimp)
        self._schedule = sched.scheduler(time.time, 10)
        self._schedule.enter(self.send_random_emoimpulse())

    def get_emotion_label(self):
        return self.myEmotionConverter.get_String(
            self.myEmotionConverter.convertToClassType(self.myEmotionContainer.to_get_emotion_list()))

    def send_impulse(self, i):
        self.myEmotionContainer.to_emoimpulse(i)

    def set_dominance(self, i):
        self.myEmotionContainer.to_set_dominance(i)

    def get_pad(self):
        self.myEmotionContainer.get_pad()
