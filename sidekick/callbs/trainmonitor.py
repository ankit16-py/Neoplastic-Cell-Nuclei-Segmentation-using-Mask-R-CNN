from tensorflow.keras import callbacks
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json
import os

class TrainMonitor(callbacks.BaseLogger):
    def __init__(self, figPath, jsonPath=None, startAt=0):
        super(TrainMonitor, self).__init__()

        self.figPath= figPath
        self.jsonPath= jsonPath
        self.startAt= startAt

    def on_train_begin(self, logs={}):
        self.H={}
        self.L={}

        if self.jsonPath is not None:
            if os.path.exists(self.jsonPath):
                self.H = json.loads(open(self.jsonPath).read())

                if self.startAt > 0:
                    for k in self.H.keys():
                        self.H[k] = self.H[k][:self.startAt]
                        
        if os.path.exists("outs/loss_values.json"):
            self.L= json.loads(open("outs/loss_values.json").read())                

    def on_epoch_end(self, epoch, logs={}):
        for keys, values in logs.items():
            l= self.H.get(keys, [])
            l.append(float(values))
            self.H[keys] = l

        if self.jsonPath is not None:
            with open(self.jsonPath, 'w') as f:
                f.write(json.dumps(self.H))
                f.close()

        if len(self.H["loss"]) > 1:
            N = np.arange(0, len(self.H["loss"]), 1)
            plt.style.use("ggplot")
            plt.figure()
            plt.plot(N, self.H["loss"], label="train_loss")
            plt.plot(N, self.H["val_loss"], label="val_loss")
            plt.title("Training Losses [Epoch {}]".format(len(self.H["loss"])))
            plt.xlabel("Epoch #")
            plt.ylabel("Loss")
            plt.legend()
            plt.savefig(self.figPath)
            plt.close()
        
        self.L[len(self.H["loss"])]= [self.H["loss"][-1], self.H["val_loss"][-1]]
        
        with open("outs/loss_values.json", "w") as fw:
            fw.write(json.dumps(self.L))
            fw.close()
            