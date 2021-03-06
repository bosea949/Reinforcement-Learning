import random
import math

def categorical_draw(probs):
  z = random.random()
  cum_prob = 0.0
  for i in range(len(probs)):
    prob = probs[i]
    cum_prob += prob
    if cum_prob > z:
      return i

  return len(probs) - 1

class Exp3_gamma():
  def __init__(self,weights,gamma,bias,learning_rate):
    self.weights = weights
    self.gamma=gamma
    self.bias=bias
    self.learning_rate=learning_rate
    return
  
  def initialize(self, n_arms):
    self.weights = [1.0 for i in range(n_arms)]
    return
  
  def select_arm(self):
    n_arms = len(self.weights)
        
    total_weight=sum(self.weights)
    probs = [0.0 for i in range(n_arms)]
    for arm in range(n_arms):
      probs[arm] = (1-self.gamma)*(self.weights[arm]/total_weight)+(self.gamma/float(n_arms))
    return categorical_draw(probs)
  
  def update(self, chosen_arm, reward):
    n_arms = len(self.weights)  
    total_weight = sum(self.weights)
    probs = [0.0 for i in range(n_arms)]
    for arm in range(n_arms):
      probs[arm] = (1-self.gamma)*(self.weights[arm]/total_weight)+(self.gamma/float(n_arms))
     
    chosen_arm_reward = ((reward+self.bias)/probs[chosen_arm])
    
    "The if and else in the for loop is the indicator part"
    for arm in range(n_arms):
        if arm ==chosen_arm:
            growth_factor = math.exp(self.learning_rate*chosen_arm_reward)
            
            "Scaling down the weights if python considers the new weight as infinity"
            if self.weights[arm] * growth_factor==math.inf:
                self.weights=[math.exp(-400)*self.weights[arm] for arm in range(n_arms)]

        else:
            growth_factor = math.exp(self.learning_rate*(self.bias/probs[arm]))# For other arms its just the learning rate*(bias/probability)(Due to the indicator function)
            
            "Scaling down the weights if python considers the new weight as infinity"
            if self.weights[arm] * growth_factor==math.inf:
                self.weights=[math.exp(-400)*self.weights[arm] for arm in range(n_arms)]

        
        self.weights[arm] = self.weights[arm] * growth_factor
        
    "Scaling down the weights if python considers the total weight as infinity"
    if sum(self.weights)==math.inf:
        self.weights=[math.exp(-400)*self.weights[arm] for arm in range(n_arms)]
  
