
from collections import deque
import sys
import time

class State(object):


  def __init__(self, guards, prisoners, boats):
    self.guards = guards
    self.prisoners = prisoners
    self.boats = boats


  def successors(self):
    if self.boats == 1:
      sgn = -1
      direction = "from the original shore to the new shore"
    else:
      sgn = 1
      direction = "back from the new shore to the original shore"
    for m in range(3):
      for c in range(3):
        newState = State(self.guards+sgn*m, self.prisoners+sgn*c, self.boats+sgn*1);
        if m+c >= 1 and m+c <= 2 and newState.isValid():    # check whether action and resulting state are valid
          action = "take %d guards and %d prisoners %s. %r" % ( m, c, direction, newState)
          yield action, newState


  def isValid(self):
    # first check the obvious
    if self.guards < 0 or self.prisoners < 0 or self.guards > 3 or self.prisoners > 3 or (self.boats != 0 and self.boats != 1):
      return False
    # then check whether guards outnumbered by prisoners
    if self.prisoners > self.guards and self.guards > 0:    # more prisoners then guards on original shore
      return False
    if self.prisoners < self.guards and self.guards < 3:    # more prisoners then guards on other shore
      return False
    return True


  def is_goal_state(self):
    return self.prisoners == 0 and self.guards == 0 and self.boats == 0


  def __repr__(self):
    return "< State (%d, %d, %d) >" % (self.guards, self.prisoners, self.boats)



class Node(object):


  def __init__(self, parent_node, state, action, depth):
    self.parent_node = parent_node
    self.state = state
    self.action = action
    self.depth = depth


  def expand(self):
    for (action, succ_state) in self.state.successors():
      succ_node = Node(
                       parent_node=self,
                       state=succ_state,
                       action=action,
                       depth=self.depth + 1)
      yield succ_node


  def extract_solution(self):
    solution = []
    node = self
    while node.parent_node is not None:
      solution.append(node.action)
      node = node.parent_node
    solution.reverse()
    return solution


def breadth_first_tree_search(initial_state):
  initial_node = Node(
                      parent_node=None,
                      state=initial_state,
                      action=None,
                      depth=0)
  fifo = deque([initial_node])
  num_expansions = 0
  max_depth = -1
  while True:
    if not fifo:
      print "%d expansions" % num_expansions
      return None
    node = fifo.popleft()
    if node.depth > max_depth:
      max_depth = node.depth
      print "[depth = %d] %.2fs" % (max_depth, time.clock())
    if node.state.is_goal_state():
      print "%d expansions" % num_expansions
      solution = node.extract_solution()
      return solution
    num_expansions += 1
    fifo.extend(node.expand())


def usage():
  print >> sys.stderr, "usage:"
  print >> sys.stderr, "    %s" % sys.argv[0]
  raise SystemExit(2)


def main():
  initial_state = State(3,3,1)
  solution = breadth_first_tree_search(initial_state)
  if solution is None:
    print "no solution"
  else:
    print "solution (%d steps):" % len(solution)
    for step in solution:
      print "%s" % step
  print "elapsed time: %.2fs" % time.clock()

main()
