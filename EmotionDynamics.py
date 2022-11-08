import numpy as np


class EmotionContainer:
    def __init__(self):
        self._mass = 1000
        self._sxlast = 0
        self._sylast = 0
        self._sxt = 0
        self._syt = 0
        self._sdom = 100
        self._sdomlast = 100
        self._vxlast = 0
        self._vylast = 0
        self._vxt = 0
        self._vyt = 0
        self._vdom = 0
        self._vdomlast = 0
        self._axlast = 0
        self._aylast = 0
        self._axt = 0
        self._ayt = 0
        self._adom = 0
        self._adomlast = 0
        self._dt = 0.1  # 10 Hz!
        self._z = 0
        self._xSignChange = 0
        self._ySignChange = 0
        self._xSign = 0
        self._ySign = 0
        self._xTens = 50
        self._yTens = 10
        self._xReg = 1
        self._yReg = 1
        self._slope = 500  # 500% equals 5!
        self._boredom = 10  # ???
        self._Fx = 0
        self._Fy = 0

    def to_calculate(self):
        self._Fx = - self._xTens * self._sxlast
        self._Fy = - self._yTens * self._sylast
        self._axt = self._Fx / self._mass
        self._vxt = self._axt * self._dt + self._vxlast
        self._sxt = self._vxt * self._dt + self._sxlast

        if (self._sxt > 0 and self._sxlast < 0) or (self._sxt < 0 and self._sxlast > 0):
            self._sxt = self._sxlast = 0
            self._vxlast = 0
            self._axlast = 0
        else:
            self._vxlast = self._vxt
            self._axlast = self._axt
            self._sxlast = self._sxt

        self._ayt = self._Fy / self._mass
        self._vyt = self._ayt * self._dt + self._vylast
        self._syt = self._vyt * self._dt + self._sylast
        self._syt += self._sxt * (self._slope / 100) / self._mass

        if (self._syt > 0 and self._sylast < 0) or (self._syt < 0 and self._sylast > 0):
            self._syt = self._sylast = 0
            self._vylast = 0
            self._aylast = 0
        else:
            self._vylast = self._vyt
            self._aylast = self._ayt
            self._sylast = self._syt

        if self._sxt > 100: self._sxt = 100
        if self._syt > 100: self._syt = 100
        if self._sxt < -100: self._sxt = -100
        if self._syt < -100: self._syt = -100

        if self._xReg > self._sxt > - self._xReg and self._yReg > self._syt > - self._yReg:
            if self._z > -100: self._z -= self._boredom / 1000.
        else:
            self._z = 0.

        # print(f"(x: {self._sxt}), (y: {self._syt}), (z: {self._z})")

    def get_dt(self):
        return self._dt

    def get_pad(self):
        print(f"(x: {self._sxt}), (y: {self._syt}), (z: {self._z})")

    def to_emoimpulse(self, i):
        self._axt = 0
        self._axlast = 0
        self._vxt = 0
        self._vxlast = 0
        self._ayt = 0
        self._aylast = 0
        self._vyt = 0
        self._vylast = 0
        self._sxlast += i
        if self._sxlast > 100: self._sxlast = 100
        if self._sxlast < -100: self._sxlast = -100
        self._sxt += i
        if self._sxt > 100: self._sxt = 100
        if self._sxt < -100: self._sxt = -100

    def to_get_emotion_list(self):
        emotionList = [self._sxt, self._syt, self._z, self._sdom]
        return emotionList

    def to_set_dominance(self, value):
        self._sdom = value


class EmotionConverter:
    def __init__(self):
        self._outer_radius = 0.8
        self._inner_radius = 0.4
        self._emo_index = -1
        self._actualStringConvertElement = ["relaxed", [0, 0, 1.0]]
        self._stringConvertedList = []
        self._temp = [0.0, 0.0, 0.0]
        self._v = []
        self._tempDistance = 0
        self._emoDistance = 0
        self._s = ""

        temp_list = ["angry", [-0.8, 0.8, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["fearful", [-0.8, 0.8, -1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["annoyed", [-0.5, 0.0, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["sad", [-0.5, 0.0, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["joyful-d", [0.8, 0.8, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["joyful-s", [0.8, 0.8, -1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["relaxed-d", [0.0, 0.0, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["sad-s", [-0.5, 0.0, -1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["surprised", [0.1, 0.8, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["startled", [0.1, 0.8, -1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["bored", [0.0, -0.8, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["depressed", [-0.5, 0.0, 1.0]]
        self._stringConvertedList.append(temp_list)
        temp_list = ["neutral", [0.0, 0.0, 0.0]]
        self._stringConvertedList.append(temp_list)

    def convertToClassType(self, lst):
        v = [0.0, 0.0, 0.0]
        if len(lst) == 4:
            emoX = lst[0]
            moodY = lst[1]
            boredomZ = lst[2]
            dominance = lst[3]

            v[0] = ((emoX + moodY) / 200)
            v[1] = (abs(emoX / 100) - abs(boredomZ / 100))
            v[2] = dominance / 100
        return v

    def get_String(self, PADData):
        self._s = "neutral"
        self._actualStringConvertElement = ["neutral", [0, 0, 0]]
        self._emoDistance = 10.0

        for element in self._stringConvertedList:
            self._temp[0] = PADData[0] - (element[1][0])
            self._temp[1] = PADData[1] - (element[1][1])
            self._temp[2] = PADData[2] - (element[1][2])
            self._tempDistance = np.linalg.norm(self._temp)

            if self._tempDistance < self._emoDistance and self._tempDistance < self._outer_radius:
                self._actualStringConvertElement = element
                self._s = element[0]
                self._emoDistance = self._tempDistance
            # print(self._s)
            return self._s

    def get_EmotionLabel(self):
        return self._actualStringConvertElement[0]

    def get_ActualStringConvertElement(self):
        return self._actualStringConvertElement
